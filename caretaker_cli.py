#!/usr/bin/env python3
"""Enhanced CareTaker CLI with v2.0 agents"""

import click
from caretaker.plugins import (
    DuplicatesPlugin, 
    MonitorAgent, 
    RepoExplorerAgent,
    LinkRecoveryAgent
)
from caretaker.core.config import load_config
from caretaker.core.github_client import GitHubClient

class CareContext:
    def __init__(self, owner, client):
        self.owner = owner
        self.client = client

@click.group()
def cli():
    """GitHub CareTaker v2.0 - Neurodivergent-Friendly Repository Management"""
    pass

@cli.command()
@click.option('--owner', required=True, help='GitHub username or org')
def monitor(owner):
    """Run Monitor Agent to check multi-agent system health"""
    cfg = load_config()
    client = GitHubClient(cfg['github_token'], cfg['base_url'])
    ctx = CareContext(owner, client)
    
    agent = MonitorAgent()
    result = agent.run(ctx)
    
    click.echo(f"🔍 Monitor Agent Report:")
    click.echo(f"   Health Score: {result['health_score']:.1f}%")
    click.echo(f"   Failures Detected: {result['failures_detected']}")
    click.echo(f"   Failures Corrected: {result['failures_corrected']}")

@cli.command()
@click.option('--owner', required=True)
def explore(owner):
    """Run Repository Explorer to analyze code structure"""
    cfg = load_config()
    client = GitHubClient(cfg['github_token'], cfg['base_url'])
    ctx = CareContext(owner, client)
    
    agent = RepoExplorerAgent()
    result = agent.run(ctx)
    
    click.echo(f"🗺️  Repository Explorer:")
    click.echo(f"   Analyzed Path: {result['analyzed_path']}")
    click.echo(f"   Modules: {result['stats']['modules']}")
    click.echo(f"   Endpoints: {result['stats']['endpoints']}")
    click.echo(f"   External Services: {result['stats']['services']}")
    click.echo(f"   Artifacts Generated:")
    for file in result['files_generated']:
        click.echo(f"     - {file}")

@cli.command()
@click.option('--owner', required=True)
def recover_links(owner):
    """Run Link Recovery Agent to fix broken issue-commit links"""
    cfg = load_config()
    client = GitHubClient(cfg['github_token'], cfg['base_url'])
    ctx = CareContext(owner, client)
    
    agent = LinkRecoveryAgent()
    result = agent.run(ctx)
    
    click.echo(f"🔗 Link Recovery Agent:")
    click.echo(f"   Repositories: {result['repositories_analyzed']}")
    click.echo(f"   Links Recovered: {result['total_links_recovered']}")

if __name__ == '__main__':
    cli()
