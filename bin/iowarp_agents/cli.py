#!/usr/bin/env python3
"""
IOWarp Agents CLI - Beautiful command-line interface for managing scientific AI agents
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.text import Text
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree
from rich.markdown import Markdown
import requests

console = Console()

# Agent metadata
AGENTS_REPO_URL = "https://api.github.com/repos/iowarp/iowarp-agents/contents/agents"
AGENTS_RAW_URL = "https://raw.githubusercontent.com/iowarp/iowarp-agents/main/agents"

# Supported platforms and their paths
PLATFORMS = {
    "claude": {
        "name": "Claude Code",
        "local_path": ".claude/agents",
        "global_path": "~/.claude/agents",
        "description": "Claude Code AI assistant with subagent support"
    },
    "opencode": {
        "name": "OpenCode",
        "local_path": ".opencode/agent",
        "global_path": "~/.config/opencode/agent",
        "description": "OpenCode AI development environment with MCP support"
    }
}

class AgentManager:
    """Manages agent operations"""
    
    def __init__(self):
        self.console = Console()
        self._agents_cache = None
    
    def fetch_available_agents(self) -> Dict[str, Dict]:
        """Fetch available agents from GitHub repository and local warpio-agents"""
        if self._agents_cache:
            return self._agents_cache
            
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
            ) as progress:
                task = progress.add_task("Fetching available agents...", total=None)
                
                response = requests.get(AGENTS_REPO_URL, timeout=10)
                response.raise_for_status()
                
                agents = {}
                for item in response.json():
                    if item['name'].endswith('.md') and item['name'] != 'README.md':
                        # Skip warpio-agents directory - we'll load these locally
                        if item['name'] == 'warpio-agents':
                            continue
                            
                        agent_name = item['name'][:-3]  # Remove .md extension
                        
                        # Fetch agent content to parse metadata
                        agent_response = requests.get(f"{AGENTS_RAW_URL}/{item['name']}", timeout=10)
                        agent_response.raise_for_status()
                        
                        metadata = self._parse_agent_metadata(agent_response.text)
                        agents[agent_name] = {
                            'filename': item['name'],
                            'download_url': agent_response.url,
                            'source': 'github',
                            'platform_compatibility': ['claude'],  # Standard agents are Claude compatible
                            **metadata
                        }
                
                progress.update(task, description="Loading local warpio agents...")
                
                # Add local warpio-agents
                warpio_agents = self._load_local_warpio_agents()
                agents.update(warpio_agents)
                
                progress.update(task, completed=True)
                self._agents_cache = agents
                return agents
                
        except requests.RequestException as e:
            self.console.print(f"[red]Error fetching agents: {e}[/red]")
            # Still try to load local warpio agents even if GitHub fails
            warpio_agents = self._load_local_warpio_agents()
            return warpio_agents
        except Exception as e:
            self.console.print(f"[red]Unexpected error: {e}[/red]")
            return {}
    
    def _parse_agent_metadata(self, content: str) -> Dict:
        """Parse agent metadata from markdown frontmatter"""
        lines = content.split('\n')
        if not lines[0].strip() == '---':
            return {}
        
        metadata = {}
        in_frontmatter = True
        i = 1
        
        while i < len(lines) and in_frontmatter:
            line = lines[i].strip()
            if line == '---':
                in_frontmatter = False
                break
            
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                
                if key == 'tools' and ',' in value:
                    metadata[key] = [tool.strip() for tool in value.split(',')]
                else:
                    metadata[key] = value
            i += 1
        
        # Extract description from content if not in metadata
        if 'description' not in metadata and i < len(lines):
            content_lines = lines[i+1:]  # Skip the --- line
            for line in content_lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    metadata['description'] = line
                    break
        
        return metadata
    
    def _load_local_warpio_agents(self) -> Dict[str, Dict]:
        """Load warpio-agents from local directory structure and group by base name"""
        warpio_agents = {}
        agent_platforms = {}  # Track platforms for each agent
        
        # Get the script's directory and navigate to warpio-agents
        script_dir = Path(__file__).parent.parent.parent  # bin/iowarp_agents -> bin -> root
        warpio_dir = script_dir / "agents" / "warpio-agents"
        
        if not warpio_dir.exists():
            return warpio_agents
        
        # First pass: collect agents and their platforms
        for platform_folder in ['claude', 'opencode']:
            platform_dir = warpio_dir / platform_folder
            if not platform_dir.exists():
                continue
                
            for agent_file in platform_dir.glob("*.md"):
                agent_name = agent_file.stem
                
                try:
                    content = agent_file.read_text(encoding='utf-8')
                    metadata = self._parse_agent_metadata(content)
                    
                    # Group by base agent name (without platform suffix)
                    base_name = f"warpio-{agent_name}"
                    
                    if base_name not in agent_platforms:
                        agent_platforms[base_name] = {
                            'platforms': [],
                            'files': {},
                            'metadata': metadata
                        }
                    
                    agent_platforms[base_name]['platforms'].append(platform_folder)
                    agent_platforms[base_name]['files'][platform_folder] = str(agent_file)
                    
                except Exception as e:
                    self.console.print(f"[yellow]Warning: Could not load {agent_file.name}: {e}[/yellow]")
        
        # Second pass: create grouped agents with all platforms
        for base_name, info in agent_platforms.items():
            warpio_agents[base_name] = {
                'filename': f"{base_name}.md",  # Generic filename
                'local_path': info['files'],  # Dict of platform -> path
                'source': 'local',
                'platform_compatibility': info['platforms'],
                'agent_type': 'warpio',
                'platforms_available': info['platforms'],
                **info['metadata']
            }
        
        return warpio_agents

def get_agent_display_name(agent_name: str) -> str:
    """Convert agent name to display name"""
    return agent_name.replace('-', ' ').title()

def get_category_icon(agent_name: str) -> str:
    """Get appropriate icon for agent category"""
    icons = {
        'data-io': '💾',
        'analysis': '📊', 
        'viz': '📊',
        'hpc': '🚀',
        'performance': '🚀',
        'research': '📚',
        'doc': '📚',
        'workflow': '⚙️',
        'orchestrator': '⚙️'
    }
    
    for key, icon in icons.items():
        if key in agent_name.lower():
            return icon
    
    return '🤖'  # Default icon

def _show_detailed_agent(agent_name: str, agent_data: Dict):
    """Show detailed agent information"""
    icon = get_category_icon(agent_name)
    display_name = get_agent_display_name(agent_name)
    
    panel_content = f"[bold]{icon} {display_name}[/bold]\n\n"
    panel_content += f"[dim]ID:[/dim] {agent_name}\n"
    
    if 'description' in agent_data:
        description = agent_data['description']
        if len(description) > 120:
            description = description[:120] + "..."
        panel_content += f"[dim]Description:[/dim] {description}\n"
    
    # Show platform compatibility
    platforms = agent_data.get('platform_compatibility', ['claude'])
    panel_content += f"[dim]Platforms:[/dim] {', '.join(platforms)}\n"
    
    # Show warpio-specific info
    if agent_data.get('agent_type') == 'warpio':
        warpio_platform = agent_data.get('warpio_platform', '')
        if 'mode' in agent_data:
            panel_content += f"[dim]Mode:[/dim] {agent_data['mode']}\n"
        panel_content += f"[dim]Optimized for:[/dim] {warpio_platform}\n"
    
    # Show tools information
    if 'tools' in agent_data:
        tools = agent_data['tools']
        if isinstance(tools, list):
            tools_str = ', '.join(tools[:3])
            if len(tools) > 3:
                tools_str += f" (+{len(tools) - 3} more)"
            panel_content += f"[dim]Tools:[/dim] {tools_str}\n"
        elif isinstance(tools, str) and tools:
            panel_content += f"[dim]Tools:[/dim] {tools}\n"
    
    # Different border colors for different types
    border_style = "magenta" if agent_data.get('agent_type') == 'warpio' else "blue"
    console.print(Panel(panel_content.strip(), border_style=border_style, padding=(1, 2)))

@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option()
def cli(ctx):
    """
    🤖 IOWarp Agents - Beautiful CLI for Scientific AI Agents
    
    Manage and install specialized AI subagents for scientific computing workflows.
    """
    if ctx.invoked_subcommand is None:
        # Show welcome message and available commands
        console.print()
        console.print(Panel.fit(
            "[bold blue]🤖 IOWarp Agents CLI[/bold blue]\n\n"
            "[dim]Specialized AI subagents for scientific computing workflows[/dim]",
            border_style="blue"
        ))
        console.print()
        
        # Show available commands
        commands_table = Table(show_header=False, box=None, padding=(0, 2))
        commands_table.add_column("Command", style="cyan bold")
        commands_table.add_column("Description", style="dim")
        
        commands_table.add_row("list", "List all available agents")
        commands_table.add_row("install", "Install an agent for a specific platform")
        commands_table.add_row("uninstall", "Remove an installed agent")
        commands_table.add_row("status", "Show installation status of agents")
        commands_table.add_row("update", "Update agents to latest versions")
        
        console.print("Available commands:")
        console.print(commands_table)
        console.print()
        console.print("[dim]Use --help with any command for more information[/dim]")
        console.print()

@cli.command()
@click.option('--detailed', '-d', is_flag=True, help='Show detailed information about each agent')
@click.option('--platform', '-p', help='Filter agents by platform compatibility (claude, opencode)')
def list(detailed, platform):
    """📋 List all available agents"""
    
    manager = AgentManager()
    agents = manager.fetch_available_agents()
    
    if not agents:
        console.print("[red]No agents found or unable to fetch agent list.[/red]")
        return
    
    # Filter by platform if specified
    if platform:
        filtered_agents = {
            name: data for name, data in agents.items()
            if platform in data.get('platform_compatibility', [])
        }
        if not filtered_agents:
            console.print(f"[yellow]No agents found for platform '{platform}'[/yellow]")
            console.print(f"[dim]Available platforms: {', '.join(PLATFORMS.keys())}[/dim]")
            return
        agents = filtered_agents
    
    console.print()
    header_text = f"[bold green]Available IOWarp Agents[/bold green] [dim]({len(agents)} total"
    if platform:
        header_text += f", {platform} compatible"
    header_text += ")[/dim]"
    
    console.print(Panel.fit(header_text, border_style="green"))
    console.print()
    
    if detailed:
        # Categorize agents for detailed view
        standard_agents = {}
        warpio_agents = {}
        
        for agent_name, agent_data in sorted(agents.items()):
            if agent_data.get('agent_type') == 'warpio':
                warpio_agents[agent_name] = agent_data
            else:
                standard_agents[agent_name] = agent_data
        
        # Show standard agents first
        if standard_agents:
            console.print("[bold blue]Standard IOWarp Agents[/bold blue]")
            console.print()
            for agent_name, agent_data in standard_agents.items():
                _show_detailed_agent(agent_name, agent_data)
                console.print()
        
        # Show warpio agents
        if warpio_agents:
            if standard_agents:
                console.print()
            console.print("[bold magenta]Warpio Agents (Deployment Orchestration)[/bold magenta]")
            console.print()
            for agent_name, agent_data in warpio_agents.items():
                _show_detailed_agent(agent_name, agent_data)
                console.print()
            
    else:
        # Compact grid view
        items = []
        for agent_name, agent_data in sorted(agents.items()):
            icon = get_category_icon(agent_name)
            display_name = get_agent_display_name(agent_name)
            
            # Special handling for warpio agents - show platforms in brackets
            if agent_data.get('agent_type') == 'warpio':
                platforms = agent_data.get('platform_compatibility', [])
                platform_text = f"({', '.join(platforms)})" if platforms else ""
                display_name = display_name.replace('Warpio ', '')  # Remove 'Warpio' prefix
                card = f"[bold]{icon} {display_name}[/bold]\n[dim]{agent_name}[/dim]\n[dim]{platform_text}[/dim]"
            else:
                # Standard agents - show platform compatibility normally  
                platforms = agent_data.get('platform_compatibility', ['claude'])
                platform_text = f"[dim]{'/'.join(platforms)}[/dim]"
                card = f"[bold]{icon} {display_name}[/bold]\n[dim]{agent_name}[/dim]\n{platform_text}"
            
            items.append(Panel(card, border_style="blue", padding=(0, 1)))
        
        # Display in columns
        console.print(Columns(items, equal=True, expand=True))
    
    console.print()
    console.print("[dim]Use 'iowarp-agents install <agent-name> <platform>' to install an agent[/dim]")
    console.print(f"[dim]Supported platforms: {', '.join(PLATFORMS.keys())}[/dim]")
    console.print()

@cli.command()
@click.argument('agent_name', required=False)
@click.argument('platform', required=False)
@click.argument('scope', required=False)
def install(agent_name, platform, scope):
    """💾 Install an agent for a specific platform"""
    
    manager = AgentManager()
    agents = manager.fetch_available_agents()
    
    if not agents:
        console.print("[red]Unable to fetch agent list. Please check your internet connection.[/red]")
        return
    
    # Interactive agent selection if not provided
    if not agent_name:
        agent_name = _select_agent(agents)
        if not agent_name:
            return
    
    # Validate agent exists
    if agent_name not in agents:
        console.print(f"[red]Agent '{agent_name}' not found.[/red]")
        console.print("[dim]Use 'iowarp-agents list' to see available agents.[/dim]")
        return
    
    agent_data = agents[agent_name]
    
    # Check platform compatibility before interactive selection
    compatible_platforms = agent_data.get('platform_compatibility', ['claude'])
    if platform and platform not in compatible_platforms:
        console.print(f"[yellow]Warning: Agent '{agent_name}' is optimized for {', '.join(compatible_platforms)} but you selected {platform}[/yellow]")
        if not Confirm.ask("Continue anyway?", default=False):
            return
    
    # Interactive platform selection if not provided
    if not platform:
        platform = _select_platform()
        if not platform:
            return
    
    # Validate platform
    if platform not in PLATFORMS:
        console.print(f"[red]Platform '{platform}' not supported.[/red]")
        console.print(f"[dim]Supported platforms: {', '.join(PLATFORMS.keys())}[/dim]")
        return
    
    # Interactive scope selection if not provided
    if not scope:
        scope = _select_scope()
        if not scope:
            return
    
    # Validate scope
    if scope not in ['local', 'global']:
        console.print(f"[red]Scope '{scope}' not valid. Use 'local' or 'global'.[/red]")
        return
    
    # Perform installation
    _install_agent(agent_name, agents[agent_name], platform, scope)

def _select_agent(agents: Dict[str, Dict]) -> Optional[str]:
    """Interactive agent selection"""
    console.print()
    console.print("[bold cyan]Select an agent to install:[/bold cyan]")
    console.print()
    
    agent_list = list(sorted(agents.keys()))
    
    # Create a numbered list
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("", style="cyan bold", width=4)
    table.add_column("Agent", style="bold")
    table.add_column("Description", style="dim")
    
    for i, agent_name in enumerate(agent_list, 1):
        icon = get_category_icon(agent_name)
        display_name = get_agent_display_name(agent_name)
        description = agents[agent_name].get('description', 'No description available')[:80]
        if len(agents[agent_name].get('description', '')) > 80:
            description += '...'
        
        table.add_row(f"{i})", f"{icon} {display_name}", description)
    
    console.print(table)
    console.print()
    
    while True:
        try:
            choice = IntPrompt.ask(
                "Enter your choice", 
                default=1, 
                console=console,
                show_default=True
            )
            
            if 1 <= choice <= len(agent_list):
                selected_agent = agent_list[choice - 1]
                console.print(f"[green]Selected:[/green] {get_agent_display_name(selected_agent)}")
                return selected_agent
            else:
                console.print(f"[red]Invalid choice. Please enter a number between 1 and {len(agent_list)}.[/red]")
                
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Installation cancelled.[/yellow]")
            return None

def _select_platform() -> Optional[str]:
    """Interactive platform selection"""
    console.print()
    console.print("[bold cyan]Select target platform:[/bold cyan]")
    console.print()
    
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("", style="cyan bold", width=4)
    table.add_column("Platform", style="bold")
    table.add_column("Description", style="dim")
    
    platform_list = list(PLATFORMS.keys())
    
    for i, platform_key in enumerate(platform_list, 1):
        platform_info = PLATFORMS[platform_key]
        table.add_row(f"{i})", platform_info['name'], platform_info['description'])
    
    console.print(table)
    console.print()
    
    while True:
        try:
            choice = IntPrompt.ask(
                "Enter your choice", 
                default=1, 
                console=console,
                show_default=True
            )
            
            if 1 <= choice <= len(platform_list):
                selected_platform = platform_list[choice - 1]
                console.print(f"[green]Selected:[/green] {PLATFORMS[selected_platform]['name']}")
                return selected_platform
            else:
                console.print(f"[red]Invalid choice. Please enter a number between 1 and {len(platform_list)}.[/red]")
                
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Installation cancelled.[/yellow]")
            return None

def _select_scope() -> Optional[str]:
    """Interactive scope selection"""
    console.print()
    console.print("[bold cyan]Select installation scope:[/bold cyan]")
    console.print()
    
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("", style="cyan bold", width=4)
    table.add_column("Scope", style="bold")
    table.add_column("Description", style="dim")
    
    table.add_row("1)", "Local project", "Install in current project (./.claude/agents or ./.opencode/agent)")
    table.add_row("2)", "Global installation", "Install for all projects (~/.claude/agents or ~/.config/opencode/agent)")
    
    console.print(table)
    console.print()
    
    while True:
        try:
            choice = IntPrompt.ask(
                "Enter your choice", 
                default=1, 
                console=console,
                show_default=True
            )
            
            if choice == 1:
                console.print("[green]Selected:[/green] Local project")
                return "local"
            elif choice == 2:
                console.print("[green]Selected:[/green] Global installation")
                return "global"
            else:
                console.print("[red]Invalid choice. Please enter 1 or 2.[/red]")
                
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Installation cancelled.[/yellow]")
            return None

def _install_agent(agent_name: str, agent_data: Dict, platform: str, scope: str):
    """Install the specified agent"""
    platform_info = PLATFORMS[platform]
    
    # Check platform compatibility
    compatible_platforms = agent_data.get('platform_compatibility', ['claude'])
    if platform not in compatible_platforms:
        console.print()
        console.print(Panel.fit(
            f"[bold yellow]⚠️  Platform Compatibility Warning[/bold yellow]\n\n"
            f"Agent '{agent_name}' is optimized for: {', '.join(compatible_platforms)}\n"
            f"You're installing for: {platform}\n\n"
            f"The agent may not work optimally on this platform.",
            border_style="yellow"
        ))
        if not Confirm.ask("Continue with installation?", default=False):
            return
    
    # Determine target directory
    if scope == "local":
        target_dir = Path(platform_info['local_path'])
    else:
        target_dir = Path(platform_info['global_path']).expanduser()
    
    # Create target directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine target filename - for warpio agents, use simplified names
    if agent_data.get('agent_type') == 'warpio':
        # Remove platform suffix from display name for cleaner filenames
        base_name = agent_name.replace('warpio-', '').replace('-claude', '').replace('-opencode', '')
        if platform == 'opencode':
            target_filename = f"warpio-{base_name}.md"
        else:
            target_filename = f"{base_name}.md"
    else:
        target_filename = agent_data['filename']
    
    target_file = target_dir / target_filename
    
    console.print()
    console.print(Panel.fit(
        f"[bold blue]Installing Agent[/bold blue]\n\n"
        f"[dim]Agent:[/dim] {get_agent_display_name(agent_name)}\n"
        f"[dim]Type:[/dim] {agent_data.get('agent_type', 'standard')}\n"
        f"[dim]Platform:[/dim] {platform_info['name']}\n"
        f"[dim]Scope:[/dim] {scope}\n"
        f"[dim]Target:[/dim] {target_file}",
        border_style="blue"
    ))
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            if agent_data.get('source') == 'local':
                # Copy from local warpio-agents file
                task = progress.add_task("Copying local agent...", total=None)
                
                progress.update(task, description="Reading local agent file...")
                
                # Handle grouped warpio agents with platform-specific files
                if agent_data.get('agent_type') == 'warpio' and isinstance(agent_data.get('local_path'), dict):
                    platform_files = agent_data['local_path']
                    if platform not in platform_files:
                        raise FileNotFoundError(f"No {platform} version found for {agent_name}")
                    source_file = platform_files[platform]
                else:
                    source_file = agent_data['local_path']
                
                with open(source_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                progress.update(task, description="Writing agent file...")
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(content)
            else:
                # Download from GitHub
                task = progress.add_task("Downloading agent...", total=None)
                
                response = requests.get(agent_data['download_url'], timeout=30)
                response.raise_for_status()
                
                progress.update(task, description="Writing agent file...")
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
            
            progress.update(task, completed=True)
        
        console.print()
        console.print(Panel.fit(
            f"[bold green]✅ Installation Successful![/bold green]\n\n"
            f"Agent '{get_agent_display_name(agent_name)}' has been installed to:\n"
            f"[dim]{target_file}[/dim]\n\n"
            f"The agent is now available in {platform_info['name']}.",
            border_style="green"
        ))
        
        # Show usage instructions
        console.print()
        console.print("[bold cyan]Usage Instructions:[/bold cyan]")
        if platform == "claude":
            console.print("• Use [bold]/agents[/bold] command in Claude Code")
            console.print(f"• Or mention: [dim]\"Use the {agent_name.replace('warpio-', '').replace('-claude', '')} to help me...\"[/dim]")
        elif platform == "opencode":
            if agent_data.get('mode') == 'primary':
                console.print("• Use [bold]Tab key[/bold] to cycle through primary agents")
                console.print(f"• Or mention: [dim]\"Switch to {agent_name.replace('warpio-', '').replace('-opencode', '')} for...\"[/dim]")
            else:
                base_name = agent_name.replace('warpio-', '').replace('-opencode', '')
                console.print(f"• Invoke with: [bold]@{base_name}[/bold]")
                console.print(f"• Or mention: [dim]\"@{base_name} help me with...\"[/dim]")
            console.print("• Navigate sessions: [dim]Ctrl+Right/Left[/dim]")
        
        console.print()
        
    except Exception as e:
        console.print()
        console.print(Panel.fit(
            f"[bold red]❌ Installation Failed[/bold red]\n\n"
            f"Error: {str(e)}",
            border_style="red"
        ))

@cli.command()
@click.argument('agent_name', required=False)
@click.argument('platform', required=False)
@click.argument('scope', required=False)
def uninstall(agent_name, platform, scope):
    """🗑️  Remove an installed agent"""
    console.print("[yellow]Uninstall functionality coming soon![/yellow]")

@cli.command()
def status():
    """📊 Show installation status of agents"""
    console.print("[yellow]Status functionality coming soon![/yellow]")

@cli.command()
def update():
    """🔄 Update agents to latest versions"""
    console.print("[yellow]Update functionality coming soon![/yellow]")

def main():
    """Entry point for the CLI"""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()