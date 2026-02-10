#!/usr/bin/env python3
"""Enhanced CareTaker CLI with v2.0 agents"""

import click
import shutil
import os
from caretaker.plugins import get_plugin
from caretaker.core.context import build_context

@click.group()
def cli():
    """GitHub CareTaker v2.0 - Neurodivergent-Friendly Repository Management"""
    pass

@cli.command()
@click.option('--owner', required=True, help='GitHub username or org')
def monitor(owner):
    """Run Monitor Agent to check multi-agent system health"""
    ctx = build_context(owner)
    
    agent = get_plugin('monitor')
    result = agent.run(ctx)
    
    click.echo(f"🔍 Monitor Agent Report:")
    click.echo(f"   Health Score: {result['health_score']:.1f}%")
    click.echo(f"   Failures Detected: {result['failures_detected']}")
    click.echo(f"   Failures Corrected: {result['failures_corrected']}")

@cli.command()
@click.option('--owner', required=True)
@click.option('--output', required=False, help='Optional output file path for report')
def explore(owner, output):
    """Run Repository Explorer to analyze code structure"""
    ctx = build_context(owner)
    
    agent = get_plugin('repo_explorer')
    result = agent.run(ctx)
    
    click.echo(f"🗺️  Repository Explorer:")
    click.echo(f"   Analyzed Path: {result['analyzed_path']}")
    click.echo(f"   Modules: {result['stats']['modules']}")
    click.echo(f"   Endpoints: {result['stats']['endpoints']}")
    click.echo(f"   External Services: {result['stats']['services']}")
    click.echo(f"   Artifacts Generated:")
    for file in result['files_generated']:
        click.echo(f"     - {file}")
    
    if output:
        # Copy the JSON artifact to the requested output path
        src_json = result['files_generated'][0] # Assuming first is JSON based on plugin logic
        shutil.copy2(src_json, output)
        click.echo(f"   Report exported to: {output}")

@cli.command()
@click.option('--owner', required=True)
def recover_links(owner):
    """Run Link Recovery Agent to fix broken issue-commit links"""
    ctx = build_context(owner)
    
    agent = get_plugin('link_recovery')
    result = agent.run(ctx)
    
    click.echo(f"🔗 Link Recovery Agent:")
    click.echo(f"   Repositories: {result['repositories_analyzed']}")
    click.echo(f"   Links Recovered: {result['total_links_recovered']}")

if __name__ == '__main__':
    cli()
