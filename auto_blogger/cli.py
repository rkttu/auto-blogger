"""CLI interface for auto-blogger."""

import typer
from rich.console import Console
from rich.panel import Panel
from typing import Optional
from pathlib import Path

from .generator import BlogGenerator
from .config import Config

app = typer.Typer(help="AI-powered blog post generator using LangChain")
console = Console()


@app.command()
def generate(
    topic: str = typer.Argument(..., help="Blog post topic or title"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file path (default: stdout)"
    ),
    language: str = typer.Option(
        "Korean", "--language", "-l", help="Language for the blog post"
    ),
    tone: str = typer.Option(
        "professional", "--tone", "-t", help="Tone of the blog post (professional, casual, technical)"
    ),
    length: str = typer.Option(
        "medium", "--length", help="Length of the post (short, medium, long)"
    ),
    research: bool = typer.Option(
        False, "--research", "-r", help="Gather reference materials from MCP servers"
    ),
    author: str = typer.Option(
        "Auto-Blogger", "--author", "-a", help="Author name for YAML front matter"
    ),
):
    """Generate a blog post with SEO-optimized front matter (keywords, abstract)."""
    try:
        config = Config.load()
        
        if not config.openai_api_key:
            console.print("[red]Error: OPENAI_API_KEY not set. Please set it in .env file or environment variable.[/red]")
            raise typer.Exit(1)
        
        console.print(Panel(f"[bold blue]Generating blog post about:[/bold blue] {topic}", expand=False))
        console.print(f"[dim]Language: {language} | Tone: {tone} | Length: {length}[/dim]")
        console.print(f"[dim]SEO: Auto-generating keywords and abstract | Author: {author}[/dim]")
        
        if research:
            if config.mcp_servers:
                console.print(f"[dim]Research: Enabled ({len(config.mcp_servers)} MCP server(s))[/dim]")
            else:
                console.print("[yellow]Warning: Research enabled but no MCP servers configured in .env[/yellow]")
        
        console.print()
        
        with console.status("[bold green]Generating content..."):
            generator = BlogGenerator(config)
            content = generator.generate(
                topic=topic,
                language=language,
                tone=tone,
                length=length,
                use_research=research,
                author=author
            )
        
        if output:
            output.write_text(content, encoding="utf-8")
            console.print(f"\n[green]✓[/green] Blog post saved to: {output}")
        else:
            console.print("\n" + "="*60)
            console.print(content)
            console.print("="*60)
        
    except Exception as e:
        console.print(f"[red]Error generating blog post: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def init():
    """Initialize configuration file."""
    config_path = Path(".env")
    
    if config_path.exists():
        overwrite = typer.confirm(".env file already exists. Overwrite?")
        if not overwrite:
            console.print("[yellow]Initialization cancelled.[/yellow]")
            raise typer.Exit(0)
    
    template = """# Auto-Blogger Configuration
OPENAI_API_KEY=your-api-key-here
DEFAULT_MODEL=gpt-4o-mini
DEFAULT_LANGUAGE=Korean
DEFAULT_TONE=professional
DEFAULT_LENGTH=medium
TEMPERATURE=0.7

# OpenAI-compatible API endpoint (optional)
# For Azure OpenAI: https://your-resource.openai.azure.com/
# For other compatible services: https://api.your-service.com/v1
OPENAI_API_BASE=

# MCP Servers (comma-separated URLs for HTTP-based MCP servers)
# Example: MCP_SERVERS=http://localhost:8000,https://api.example.com/mcp
MCP_SERVERS=
"""
    
    config_path.write_text(template)
    console.print(f"[green]✓[/green] Configuration file created: {config_path}")
    console.print("[yellow]Please edit .env and add your OpenAI API key.[/yellow]")


@app.command()
def version():
    """Show version information."""
    from . import __version__
    console.print(f"auto-blogger version {__version__}")


if __name__ == "__main__":
    app()
