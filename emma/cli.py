"""
CLI module for Emma - Refactored for modular architecture
"""

import os
import sys
import typer
from typing import List, Optional
from enum import Enum
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
import logging

from .config import Config
from .chat import ChatSession
from .memory import SimpleMemory, ConversationMemory
from .utils import (
    setup_logging, 
    print_welcome_message, 
    print_system_info,
    format_conversation_list,
    check_ollama_availability
)

app = typer.Typer(help="Emma - Extended command interface")
console = Console()
logger = setup_logging()

class PersonalityType(str, Enum):
    """Available personality types"""
    DEFAULT = "default"
    CREATIVE = "creativa"
    TECHNICAL = "técnica"
    CONCISE = "concisa"
    EDUCATIONAL = "educativa"
    SEXY = "sexy"
    HOMUNCULUS = "homunculus"

@app.command()
def chat():
    """Start an interactive chat session."""
    # Check Ollama availability
    if not check_ollama_availability():
        console.print("[bold red]Error: Could not connect to Ollama. Make sure it's running.[/bold red]")
        return 1
    
    try:
        # Load configuration
        config = Config.from_file()
        
        # Start chat session
        session = ChatSession(config)
        
        print_welcome_message(config)
        
        # Main chat loop
        while True:
            user_input = Prompt.ask(f"\n[bold green]{config.user_name}[/bold green]")
            
            # Special commands
            if user_input.lower() == "/exit":
                console.print("[bold yellow]Goodbye![/bold yellow]")
                break
                
            if user_input.lower() == "/clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                print_welcome_message(config)
                continue
                
            if user_input.lower() == "/help":
                show_help()
                continue
                
            if user_input.lower().startswith("/personality"):
                handle_personality_command(user_input, session, config)
                continue
            
            # Get response from model
            response = session.get_response(user_input)
            
            # Display response
            if config.use_panels:
                console.print(Panel(response, title="[bold blue]Emma[/bold blue]", 
                                    border_style="blue", expand=False))
            else:
                console.print(f"[bold blue]Emma:[/bold blue] {response}")
            
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Session terminated by user.[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        logger.error(f"Error in execution: {str(e)}", exc_info=True)
        return 1
    
    return 0

@app.command()
def configure():
    """Interactive configuration of Emma."""
    config = Config.from_file()
    
    console.print("[bold]Emma Configuration[/bold]")
    console.print("======================\n")
    
    # Model configuration
    console.print("[bold cyan]Model Configuration[/bold cyan]")
    config.model = Prompt.ask("Model", default=config.model)
    config.temperature = float(Prompt.ask("Temperature", default=str(config.temperature)))
    config.max_tokens = int(Prompt.ask("Max tokens", default=str(config.max_tokens)))
    
    # Conversation configuration
    console.print("\n[bold cyan]Conversation Configuration[/bold cyan]")
    config.save_conversations = Confirm.ask("Save conversations?", default=config.save_conversations)
    
    # Ollama configuration
    console.print("\n[bold cyan]Ollama Configuration[/bold cyan]")
    config.ollama_host = Prompt.ask("Ollama host", default=config.ollama_host)
    
    # Save configuration
    if config.save():
        console.print("\n[bold green]Configuration saved successfully.[/bold green]")
    else:
        console.print("\n[bold red]Error saving configuration.[/bold red]")

@app.command()
def personalities(
    list_all: bool = typer.Option(False, "--list", "-l", help="List all personalities"),
    add: bool = typer.Option(False, "--add", "-a", help="Add a new personality"),
    remove: str = typer.Option(None, "--remove", "-r", help="Remove a personality"),
    view: str = typer.Option(None, "--view", "-v", help="View a personality")
):
    """Manage available personalities."""
    config = Config.from_file()
    
    if list_all:
        table = Table(title="Available Personalities")
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="green")
        table.add_column("Preview", style="yellow")
        
        personalities = config.list_personalities()
        for personality in personalities:
            table.add_row(
                personality['name'],
                personality['description'],
                personality['prompt']
            )
        
        console.print(table)
        return
    
    if view:
        personality_info = config.get_personality_info(view)
        if personality_info:
            console.print(Panel(
                personality_info['prompt'],
                title=f"[bold]Personality: {personality_info['name']}[/bold]",
                subtitle=f"Description: {personality_info['description']}",
                border_style="green"
            ))
        else:
            console.print(f"[bold red]Personality '{view}' not found.[/bold red]")
        return
    
    if remove:
        if config.remove_personality(remove):
            console.print(f"[bold green]Personality '{remove}' removed successfully.[/bold green]")
        else:
            console.print(f"[bold red]Could not remove personality '{remove}'.[/bold red]")
        return
    
    if add:
        name = Prompt.ask("Name of the new personality")
        description = Prompt.ask("Description of the personality")
        prompt = Prompt.ask("System prompt for this personality")
        
        if config.add_personality(name, prompt, description):
            console.print(f"[bold green]Personality '{name}' added successfully.[/bold green]")
        else:
            console.print("[bold red]Error adding personality.[/bold red]")
        return

def show_help():
    """Show help for available commands."""
    help_text = """
Available commands:

[bold green]Basic:[/bold green]
  /help - Show this help
  /clear - Clear the screen
  /exit - Exit Emma

[bold green]Personality:[/bold green]
  /personality list - List available personalities
  /personality set <name> - Change personality
  /personality info <name> - View personality details
  /personality add <name> - Add new personality
  /personality remove <name> - Remove personality

[bold green]Memory:[/bold green]
  /memory list - List saved conversations
  /memory load <id> - Load a conversation
  /memory clear - Clear current conversation
"""
    console.print(Panel(help_text, title="[bold]Emma Help[/bold]", border_style="blue"))

def handle_personality_command(command: str, session, config):
    """Handle personality-related commands."""
    parts = command.split()
    
    if len(parts) < 2:
        console.print("[bold red]Usage: /personality <action> [name][/bold red]")
        return
    
    action = parts[1].lower()
    
    if action == "list":
        table = Table(title="Available Personalities")
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="green")
        
        personalities = config.list_personalities()
        for personality in personalities:
            table.add_row(personality['name'], personality['description'])
        
        console.print(table)
        
    elif action == "set":
        if len(parts) < 3:
            console.print("[bold red]Usage: /personality set <name>[/bold red]")
            return
        
        personality_name = parts[2]
        if session.change_personality(personality_name):
            console.print(f"[bold green]Changed personality to: {personality_name}[/bold green]")
        else:
            console.print(f"[bold red]Could not change to personality: {personality_name}[/bold red]")
    
    elif action == "info":
        if len(parts) < 3:
            console.print("[bold red]Usage: /personality info <name>[/bold red]")
            return
        
        personality_name = parts[2]
        personality_info = config.get_personality_info(personality_name)
        
        if personality_info:
            console.print(Panel(
                personality_info['prompt'],
                title=f"[bold]Personality: {personality_info['name']}[/bold]",
                subtitle=f"Description: {personality_info['description']}",
                border_style="green"
            ))
        else:
            console.print(f"[bold red]Personality '{personality_name}' not found.[/bold red]")
    
    else:
        console.print(f"[bold red]Unknown personality action: {action}[/bold red]")

def handle_memory_command(command: str, memory):
    """Handle memory-related commands."""
    parts = command.split()
    
    if len(parts) < 2:
        console.print("[bold red]Usage: /memory <action> [id][/bold red]")
        return
    
    action = parts[1].lower()
    
    if action == "list":
        conversations = memory.list_conversations()
        if conversations:
            format_conversation_list(conversations)
        else:
            console.print("[yellow]No saved conversations found.[/yellow]")
    
    elif action == "load":
        if len(parts) < 3:
            console.print("[bold red]Usage: /memory load <id>[/bold red]")
            return
        
        conversation_id = parts[2]
        if memory.load_conversation(conversation_id):
            console.print(f"[bold green]Loaded conversation: {conversation_id}[/bold green]")
        else:
            console.print(f"[bold red]Could not load conversation: {conversation_id}[/bold red]")
    
    elif action == "clear":
        memory.clear_conversation()
        console.print("[bold green]Conversation cleared.[/bold green]")
    
    else:
        console.print(f"[bold red]Unknown memory action: {action}[/bold red]")

if __name__ == "__main__":
    app() 