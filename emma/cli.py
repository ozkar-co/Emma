"""
Módulo CLI para Emma.
Proporciona una interfaz de línea de comandos extendida para Emma.
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
    check_ollama_availability,
    get_available_personalities
)

app = typer.Typer(help="Emma - Interfaz extendida de comandos")
console = Console()
logger = setup_logging()

class PersonalityType(str, Enum):
    """Tipos de personalidad disponibles"""
    DEFAULT = "default"
    CREATIVE = "creativa"
    TECHNICAL = "técnica"
    CONCISE = "concisa"
    EDUCATIONAL = "educativa"

@app.command()
def chat():
    """Inicia una sesión de chat interactiva."""
    # Comprobar disponibilidad de Ollama
    if not check_ollama_availability():
        console.print("[bold red]Error: Could not connect to Ollama. Make sure it's running.[/bold red]")
        return 1
    
    try:
        # Cargar configuración
        config = Config.from_file()
        
        # Iniciar sesión de chat
        session = ChatSession(config)
        
        print_welcome_message(config)
        
        # Bucle principal de chat
        while True:
            user_input = Prompt.ask(f"\n[bold green]{config.user_name}[/bold green]")
            
            # Comandos especiales
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
            
            # Obtener respuesta del modelo
            response = session.get_response(user_input)
            
            # Mostrar respuesta
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
    """Configuración interactiva de Emma."""
    config = Config.from_file()
    
    console.print("[bold]Configuración de Emma[/bold]")
    console.print("======================\n")
    
    # Configuración del modelo
    console.print("[bold cyan]Configuración del modelo[/bold cyan]")
    config.model = Prompt.ask("Modelo", default=config.model)
    config.temperature = float(Prompt.ask("Temperatura", default=str(config.temperature)))
    config.max_tokens = int(Prompt.ask("Tokens máximos", default=str(config.max_tokens)))
    
    # Configuración de la conversación
    console.print("\n[bold cyan]Configuración de la conversación[/bold cyan]")
    config.system_prompt = Prompt.ask("Prompt del sistema", default=config.system_prompt)
    config.save_conversations = Confirm.ask("¿Guardar conversaciones?", default=config.save_conversations)
    
    # Configuración de Ollama
    console.print("\n[bold cyan]Configuración de Ollama[/bold cyan]")
    config.ollama_host = Prompt.ask("Host de Ollama", default=config.ollama_host)
    
    # Guardar configuración
    if config.save():
        console.print("\n[bold green]Configuración guardada correctamente.[/bold green]")
    else:
        console.print("\n[bold red]Error al guardar la configuración.[/bold red]")

@app.command()
def personalities(
    list_all: bool = typer.Option(False, "--list", "-l", help="Listar todas las personalidades"),
    add: bool = typer.Option(False, "--add", "-a", help="Añadir una nueva personalidad"),
    remove: str = typer.Option(None, "--remove", "-r", help="Eliminar una personalidad"),
    view: str = typer.Option(None, "--view", "-v", help="Ver una personalidad")
):
    """Gestiona las personalidades disponibles."""
    config = Config.from_file()
    
    if list_all:
        table = Table(title="Personalidades Disponibles")
        table.add_column("Nombre", style="cyan")
        table.add_column("Descripción", style="green")
        
        for name, prompt in config.personalities.items():
            description = prompt[:50] + "..." if len(prompt) > 50 else prompt
            table.add_row(name, description)
        
        console.print(table)
        return
    
    if view:
        if view in config.personalities:
            console.print(Panel(
                config.personalities[view],
                title=f"[bold]Personalidad: {view}[/bold]",
                border_style="green"
            ))
        else:
            console.print(f"[bold red]La personalidad '{view}' no existe.[/bold red]")
        return
    
    if remove:
        if config.remove_personality(remove):
            if config.save():
                console.print(f"[bold green]Personalidad '{remove}' eliminada correctamente.[/bold green]")
            else:
                console.print("[bold red]Error al guardar la configuración.[/bold red]")
        else:
            console.print(f"[bold red]No se pudo eliminar la personalidad '{remove}'.[/bold red]")
        return
    
    if add:
        name = Prompt.ask("Nombre de la nueva personalidad")
        if name in config.personalities:
            overwrite = Confirm.ask(f"La personalidad '{name}' ya existe. ¿Deseas sobrescribirla?")
            if not overwrite:
                return
        
        prompt = Prompt.ask("Prompt de sistema para esta personalidad")
        config.add_personality(name, prompt)
        
        if config.save():
            console.print(f"[bold green]Personalidad '{name}' añadida correctamente.[/bold green]")
        else:
            console.print("[bold red]Error al guardar la configuración.[/bold red]")
        return

def show_help():
    """Muestra la ayuda de los comandos disponibles."""
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
"""
    console.print(Panel(help_text, title="[bold]Emma Help[/bold]", border_style="blue"))

def handle_memory_command(command: str, memory):
    """Gestiona los comandos relacionados con la memoria."""
    if memory is None:
        console.print("[bold yellow]El sistema de memoria no está activado.[/bold yellow]")
        return
    
    parts = command.split(maxsplit=2)
    if len(parts) < 2:
        console.print("[bold red]Comando incompleto. Usa 'help' para ver la sintaxis.[/bold red]")
        return
    
    cmd = parts[1].lower()
    
    if cmd == "clear":
        if memory.clear():
            console.print("[bold green]Memoria limpiada correctamente.[/bold green]")
        else:
            console.print("[bold red]Error al limpiar la memoria.[/bold red]")
    
    elif cmd == "add" and len(parts) >= 3:
        add_parts = parts[2].split(maxsplit=1)
        if len(add_parts) < 2:
            console.print("[bold red]Debes especificar clave y valor.[/bold red]")
            return
        
        key, value = add_parts
        if memory.add(key, value):
            console.print(f"[bold green]Elemento añadido a la memoria: {key}[/bold green]")
        else:
            console.print("[bold red]Error al añadir a la memoria.[/bold red]")
    
    elif cmd == "get" and len(parts) >= 3:
        key = parts[2]
        value = memory.get(key)
        if value is not None:
            console.print(Panel(
                f"{value}",
                title=f"[bold]Memoria: {key}[/bold]",
                border_style="green"
            ))
        else:
            console.print(f"[bold yellow]No se encontró el elemento '{key}' en la memoria.[/bold yellow]")
    
    elif cmd == "search" and len(parts) >= 3:
        query = parts[2]
        results = memory.search(query)
        
        if not results:
            console.print("[bold yellow]No se encontraron resultados.[/bold yellow]")
            return
        
        table = Table(title=f"Resultados de búsqueda para '{query}'")
        table.add_column("Clave", style="cyan")
        table.add_column("Valor", style="green")
        
        for result in results:
            table.add_row(result["key"], str(result["value"]))
        
        console.print(table)
    
    else:
        console.print("[bold red]Comando de memoria no reconocido.[/bold red]")

def handle_personality_command(command: str, session, config):
    """Gestiona los comandos relacionados con las personalidades."""
    parts = command.split(maxsplit=2)
    if len(parts) < 2:
        console.print("[bold red]Comando incompleto. Usa 'help' para ver la sintaxis.[/bold red]")
        return
    
    cmd = parts[1].lower()
    
    if cmd == "list":
        personalities = get_available_personalities(config)
        
        table = Table(title="Personalidades Disponibles")
        table.add_column("Nombre", style="cyan")
        table.add_column("Descripción", style="green")
        
        for name, prompt in personalities.items():
            description = prompt[:50] + "..." if len(prompt) > 50 else prompt
            table.add_row(name, description)
        
        console.print(table)
    
    elif cmd == "set" and len(parts) >= 3:
        personality = parts[2]
        if session.change_personality(personality):
            console.print(f"[bold green]Personalidad cambiada a: {personality}[/bold green]")
        else:
            console.print(f"[bold red]No se pudo cambiar a la personalidad: {personality}[/bold red]")
    
    elif cmd == "info" and len(parts) >= 3:
        personality = parts[2]
        if personality in config.personalities:
            console.print(Panel(
                config.personalities[personality],
                title=f"[bold]Personalidad: {personality}[/bold]",
                border_style="green"
            ))
        else:
            console.print(f"[bold red]La personalidad '{personality}' no existe.[/bold red]")
    
    else:
        console.print("[bold red]Comando de personalidad no reconocido.[/bold red]")

if __name__ == "__main__":
    app() 