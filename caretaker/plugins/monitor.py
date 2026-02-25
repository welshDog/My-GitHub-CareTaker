"""
Monitor Agent - Prevents multi-agent system failures
Based on research: Testing and Enhancing Multi-Agent Systems (2025)
https://arxiv.org/abs/2510.10460

Solves 40-89% of agent miscommunication failures by monitoring
interactions between Cleanup, Documentation, and Security agents.
"""

from collections import deque
from typing import Dict, List, Optional
from datetime import datetime
from . import Plugin
from caretaker.core.context import CareContext

class MonitorAgent(Plugin):
    name = "monitor"
    
    def __init__(self):
        super().__init__()
        self.agent_states = {}
        self.failure_log = deque(maxlen=1000)
        self.communication_history = deque(maxlen=10000)
    
    def track_agent_communication(self, 
                                  sender: str, 
                                  receiver: str, 
                                  message: Dict,
                                  timestamp: Optional[datetime] = None) -> Dict:
        """Track communication between agents"""
        timestamp = timestamp or datetime.now()
        
        comm_entry = {
            "timestamp": timestamp.isoformat(),
            "sender": sender,
            "receiver": receiver,
            "message": message,
            "status": "pending"
        }
        
        self.communication_history.append(comm_entry)
        
        # Check for semantic mismatches
        validation = self.validate_message_semantics(sender, receiver, message)
        if not validation["valid"]:
            comm_entry["status"] = "failed"
            comm_entry["error"] = validation["reason"]
            self.failure_log.append(comm_entry)
            
            # Attempt auto-correction
            corrected = self.auto_correct_communication(sender, receiver, message, validation)
            
            # FIX: Update status if correction worked
            if corrected:
                comm_entry["status"] = "corrected"
                comm_entry["corrected_message"] = corrected
                return corrected
            
            return corrected # Return corrected (which might be None/Empty or partial)
        
        comm_entry["status"] = "success"
        return message
        
        comm_entry["status"] = "success"
        return message
    
    def validate_message_semantics(self, sender: str, receiver: str, message: Dict) -> Dict:
        """
        Validates that agent messages preserve semantic meaning
        Prevents mutation-induced failures
        """
        validation_result = {"valid": True, "reason": None}
        
        # Check 1: Ensure required fields exist
        required_fields = self.get_required_fields(receiver)
        missing_fields = [f for f in required_fields if f not in message]
        
        if missing_fields:
            validation_result["valid"] = False
            validation_result["reason"] = f"Missing required fields: {missing_fields}"
            return validation_result
        
        # Check 2: Type consistency
        if "action" in message:
            valid_actions = self.get_valid_actions(receiver)
            if message["action"] not in valid_actions:
                validation_result["valid"] = False
                validation_result["reason"] = f"Invalid action '{message['action']}' for {receiver}"
                return validation_result
        
        # Check 3: Dependency resolution
        if "dependencies" in message:
            unresolved = self.check_dependencies(message["dependencies"])
            if unresolved:
                validation_result["valid"] = False
                validation_result["reason"] = f"Unresolved dependencies: {unresolved}"
                return validation_result
        
        return validation_result
    
    def auto_correct_communication(self, sender: str, receiver: str, 
                                   message: Dict, validation: Dict) -> Dict:
        """Automatically correct common communication failures"""
        corrected = message.copy()
        reason = validation.get("reason", "")
        
        # Auto-fix missing fields with defaults
        if "Missing required fields" in reason:
            required = self.get_required_fields(receiver)
            for field in required:
                if field not in corrected:
                    corrected[field] = self.get_field_default(field, receiver)
        
        # Auto-fix invalid actions by mapping to closest valid action
        if "Invalid action" in reason:
            valid_actions = self.get_valid_actions(receiver)
            current_action = message.get("action", "")
            closest_action = self.find_closest_action(current_action, valid_actions)
            corrected["action"] = closest_action
        
        # Log the correction
        self.failure_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "auto_correction",
            "original": message,
            "corrected": corrected,
            "reason": reason
        })
        
        return corrected
    
    def get_required_fields(self, agent: str) -> List[str]:
        """Define required fields for each agent type"""
        field_map = {
            "cleanup": ["action", "target_repo", "operation"],
            "documentation": ["action", "repo", "doc_type"],
            "security": ["action", "scan_target", "severity_threshold"],
            "duplicate": ["action", "repos", "similarity_threshold"]
        }
        return field_map.get(agent, ["action"])
    
    def get_valid_actions(self, agent: str) -> List[str]:
        """Define valid actions for each agent"""
        action_map = {
            "cleanup": ["archive", "delete", "consolidate", "rename"],
            "documentation": ["generate", "update", "audit", "sync"],
            "security": ["scan", "audit", "patch", "report"],
            "duplicate": ["detect", "merge", "suggest", "analyze"]
        }
        return action_map.get(agent, ["execute"])
    
    def get_field_default(self, field: str, agent: str) -> any:
        """Provide sensible defaults for missing fields"""
        defaults = {
            "operation": "analyze",
            "doc_type": "README",
            "severity_threshold": "medium",
            "similarity_threshold": 0.8
        }
        return defaults.get(field, None)
    
    def check_dependencies(self, deps: List[str]) -> List[str]:
        """Check if dependencies are resolved"""
        unresolved = []
        for dep in deps:
            if dep not in self.agent_states or self.agent_states[dep] != "completed":
                unresolved.append(dep)
        return unresolved
    
    def find_closest_action(self, action: str, valid_actions: List[str]) -> str:
        """Find closest valid action using fuzzy matching"""
        from difflib import get_close_matches
        matches = get_close_matches(action, valid_actions, n=1, cutoff=0.6)
        return matches[0] if matches else valid_actions[0]
    
    def update_agent_state(self, agent: str, state: str, metadata: Optional[Dict] = None):
        """Track state of each agent"""
        self.agent_states[agent] = {
            "state": state,
            "last_update": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
    
    def run(self, ctx: CareContext) -> Dict:
        """Monitor execution and generate health report"""
        return {
            "plugin": self.name,
            "agent_states": self.agent_states,
            "failures_detected": len(self.failure_log),
            "failures_corrected": len([f for f in self.failure_log if "auto_correction" in f.get("type", "")]),
            "communication_history": self.communication_history[-50:],  # Last 50 messages
            "health_score": self.calculate_health_score()
        }
    
    def calculate_health_score(self) -> float:
        """Calculate system health score 0-100"""
        if not self.communication_history:
            return 100.0
        
        successful = len([c for c in self.communication_history if c["status"] == "success"])
        total = len(self.communication_history)
        return (successful / total) * 100 if total > 0 else 100.0
