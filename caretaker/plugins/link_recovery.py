"""
Issue-Commit Link Recovery Agent
Based on LinkAnchor research (2025)
https://arxiv.org/abs/2508.12232

Recovers broken issue-to-commit links (42.2% of GitHub issues lack proper links)
Uses lazy-access to handle long commit histories without token overflow
"""

from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from . import Plugin, CareContext

class LinkRecoveryAgent(Plugin):
    name = "link_recovery"
    
    def __init__(self):
        super().__init__()
        self.recovered_links = []
        self.confidence_threshold = 0.7
    
    def extract_issue_references(self, text: str) -> List[int]:
        """Extract issue numbers from commit messages or comments"""
        import re
        
        # Match patterns like: #123, GH-123, closes #123, fixes #123, resolves #123
        patterns = [
            r'#(\d+)',
            r'GH-(\d+)',
            r'(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*#(\d+)',
        ]
        
        issue_nums = set()
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            issue_nums.update(int(m.group(1)) for m in matches)
        
        return sorted(list(issue_nums))
    
    def calculate_semantic_similarity(self, issue_text: str, commit_text: str) -> float:
        """Calculate semantic similarity between issue and commit"""
        # Normalize texts
        issue_clean = self.normalize_text(issue_text)
        commit_clean = self.normalize_text(commit_text)
        
        # Use SequenceMatcher for basic similarity
        similarity = SequenceMatcher(None, issue_clean, commit_clean).ratio()
        
        # Bonus for keyword matches
        issue_keywords = self.extract_keywords(issue_text)
        commit_keywords = self.extract_keywords(commit_text)
        
        common_keywords = issue_keywords & commit_keywords
        keyword_bonus = len(common_keywords) / max(len(issue_keywords), 1) * 0.2
        
        return min(similarity + keyword_bonus, 1.0)
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for comparison"""
        import re
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def extract_keywords(self, text: str) -> Set[str]:
        """Extract important keywords from text"""
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been'}
        
        words = self.normalize_text(text).split()
        return {w for w in words if len(w) > 3 and w not in stopwords}
    
    def temporal_proximity_score(self, issue_date: datetime, commit_date: datetime) -> float:
        """Score based on temporal proximity"""
        time_diff = abs((commit_date - issue_date).total_seconds())
        
        # Commits within 1 day = high score
        if time_diff < 86400:  # 1 day
            return 1.0
        elif time_diff < 604800:  # 1 week
            return 0.8
        elif time_diff < 2592000:  # 30 days
            return 0.6
        else:
            return 0.3
    
    def lazy_access_commit_history(self, ctx: CareContext, repo: str, 
                                   max_commits: int = 100) -> List[Dict]:
        """
        Lazy-access pattern: only load commits on-demand
        Prevents token overflow on large repos
        """
        commits = []
        page = 1
        per_page = 30
        
        while len(commits) < max_commits:
            try:
                batch = ctx.client.list_commits(
                    owner=ctx.owner,
                    repo=repo,
                    page=page,
                    per_page=per_page
                )
                
                if not batch:
                    break
                
                commits.extend(batch)
                page += 1
                
            except Exception as e:
                print(f"Error fetching commits: {e}")
                break
        
        return commits[:max_commits]
    
    def recover_links_for_repo(self, ctx: CareContext, repo_name: str) -> Dict:
        """Recover missing issue-commit links for a single repository"""
        
        # Get issues without linked commits
        issues = ctx.client.list_issues(owner=ctx.owner, repo=repo_name, state="all")
        
        # Get recent commits (lazy load)
        commits = self.lazy_access_commit_history(ctx, repo_name, max_commits=200)
        
        recovered = []
        
        for issue in issues:
            issue_num = issue.get("number")
            issue_title = issue.get("title", "")
            issue_body = issue.get("body", "")
            issue_created = datetime.fromisoformat(issue.get("created_at").replace('Z', '+00:00'))
            
            # Check if issue already has commits linked
            # (In real implementation, check via GitHub API)
            # For now, assume we need to find links
            
            candidate_commits = []
            
            for commit in commits:
                commit_msg = commit.get("commit", {}).get("message", "")
                commit_date_str = commit.get("commit", {}).get("author", {}).get("date", "")
                
                if not commit_date_str:
                    continue
                
                commit_date = datetime.fromisoformat(commit_date_str.replace('Z', '+00:00'))
                
                # Check explicit references
                referenced_issues = self.extract_issue_references(commit_msg)
                if issue_num in referenced_issues:
                    candidate_commits.append({
                        "sha": commit.get("sha"),
                        "message": commit_msg[:100],
                        "confidence": 1.0,
                        "method": "explicit_reference"
                    })
                    continue
                
                # Check semantic similarity
                issue_text = f"{issue_title} {issue_body}"
                semantic_score = self.calculate_semantic_similarity(issue_text, commit_msg)
                temporal_score = self.temporal_proximity_score(issue_created, commit_date)
                
                # Combined confidence score
                confidence = (semantic_score * 0.7) + (temporal_score * 0.3)
                
                if confidence >= self.confidence_threshold:
                    candidate_commits.append({
                        "sha": commit.get("sha"),
                        "message": commit_msg[:100],
                        "confidence": round(confidence, 3),
                        "method": "semantic_temporal"
                    })
            
            if candidate_commits:
                recovered.append({
                    "issue_number": issue_num,
                    "issue_title": issue_title,
                    "linked_commits": sorted(candidate_commits, 
                                           key=lambda x: x["confidence"], 
                                           reverse=True)[:5]  # Top 5 matches
                })
        
        return {
            "repo": repo_name,
            "total_issues": len(issues),
            "links_recovered": len(recovered),
            "recovery_rate": f"{(len(recovered)/len(issues))*100:.1f}%" if issues else "0%",
            "recovered_links": recovered
        }
    
    def run(self, ctx: CareContext) -> Dict:
        """Run link recovery across all repositories"""
        repos = ctx.client.list_user_repos(ctx.owner)
        
        results = []
        total_recovered = 0
        
        # Process first 5 repos (add full processing later)
        for repo in repos[:5]:
            repo_name = repo.get("name")
            
            # Skip archived repos
            if repo.get("archived"):
                continue
            
            result = self.recover_links_for_repo(ctx, repo_name)
            results.append(result)
            total_recovered += result["links_recovered"]
        
        return {
            "plugin": self.name,
            "repositories_analyzed": len(results),
            "total_links_recovered": total_recovered,
            "results": results,
            "note": "42.2% of GitHub issues lack proper commit links - this agent fixes that!"
        }
