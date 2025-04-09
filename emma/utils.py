"""
Módulo de utilidades para Emma.
Contiene funciones auxiliares para el proyecto.
"""

import os
import sys
import logging
import platform
from datetime import datetime
from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .config import Config

console = Console()
logger = logging.getLogger(__name__)

def setup_logging(
    level: int = logging.INFO,
    log_dir: str = "logs",
    log_file: str = None
) -> logging.Logger:
    """Configura el sistema de logging."""
    # Crear directorio de logs si no existe
    os.makedirs(log_dir, exist_ok=True)
    
    # Configurar nombre de archivo de log
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"emma_{timestamp}.log")
    
    # Configurar el logger
    logger = logging.getLogger("emma")
    logger.setLevel(level)
    
    # Evitar duplicación de handlers
    if not logger.handlers:
        # Configurar handler para archivo
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Configurar handler para consola
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            "%(levelname)s: %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    return logger

def print_welcome_message(config: Config) -> None:
    """Imprime un mensaje de bienvenida."""
    welcome_text = f"""
¡Bienvenido/a a Emma, {config.user_name}!

Una interfaz de chat para interactuar con modelos de Ollama.
    
Modelo actual: [bold blue]{config.model}[/bold blue]
Temperatura: [bold]{config.temperature}[/bold]
    
Comandos disponibles:
  [bold green]exit, quit, salir[/bold green] - Salir de Emma
  [bold green]clear, limpiar[/bold green] - Limpiar la pantalla
  [bold green]help, ayuda[/bold green] - Mostrar ayuda adicional
    
¡Escribe tu mensaje y comienza a conversar!
"""
    console.print(Panel(welcome_text, title="[bold]Emma v0.1.0[/bold]", 
                        border_style="green", expand=False))

def print_system_info() -> None:
    """Imprime información del sistema."""
    info = {
        "Sistema Operativo": f"{platform.system()} {platform.release()}",
        "Versión de Python": platform.python_version(),
        "Directorio de Trabajo": os.getcwd(),
        "Usuario": os.getlogin(),
    }
    
    table = Table(title="Información del Sistema")
    table.add_column("Propiedad", style="green")
    table.add_column("Valor", style="blue")
    
    for key, value in info.items():
        table.add_row(key, value)
    
    console.print(table)

def format_conversation_list(conversations: list) -> None:
    """Formatea y muestra una lista de conversaciones."""
    if not conversations:
        console.print("[yellow]No hay conversaciones guardadas.[/yellow]")
        return
    
    table = Table(title="Conversaciones Guardadas")
    table.add_column("ID", style="dim")
    table.add_column("Fecha de Creación", style="green")
    table.add_column("Última Actualización", style="blue")
    table.add_column("Mensajes", style="cyan")
    table.add_column("Vista Previa", style="yellow")
    
    for conv in conversations:
        # Formatear fechas
        created = datetime.fromisoformat(conv["created_at"]).strftime("%Y-%m-%d %H:%M")
        updated = datetime.fromisoformat(conv["updated_at"]).strftime("%Y-%m-%d %H:%M")
        
        table.add_row(
            conv["id"][:8] + "...",  # ID corto
            created,
            updated,
            str(conv["message_count"]),
            conv["preview"]
        )
    
    console.print(table)

def check_ollama_availability(host: str = "http://localhost:11434") -> bool:
    """Verifica si Ollama está disponible."""
    import requests
    
    # Asegurarse de que la URL no termina con una barra
    host = host.rstrip('/')
    version_url = f"{host}/api/version"
    
    try:
        response = requests.get(version_url, timeout=3)
        if response.status_code == 200:
            # Intentar obtener la versión para verificar que la respuesta es válida
            try:
                version_data = response.json()
                version = version_data.get("version", "desconocida")
                logger.info(f"Ollama disponible (versión: {version})")
            except Exception as json_err:
                logger.warning(f"Ollama disponible pero no se pudo obtener información de versión: {str(json_err)}")
            return True
        else:
            logger.warning(f"Ollama respondió con código de estado inesperado: {response.status_code}")
            return False
    except requests.ConnectionError:
        logger.error(f"No se pudo conectar con Ollama en {host}. Asegúrate de que Ollama esté en ejecución.")
        return False
    except requests.Timeout:
        logger.error(f"Tiempo de espera agotado al intentar conectar con Ollama en {host}.")
        return False
    except Exception as e:
        logger.error(f"Error desconocido al verificar la disponibilidad de Ollama: {str(e)}")
        return False

def format_duration(seconds: float) -> str:
    """Formatea una duración en segundos a una representación legible."""
    if seconds < 60:
        return f"{seconds:.2f} segundos"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutos"
    else:
        hours = seconds / 3600
        return f"{hours:.2f} horas"

def get_available_personalities(config: Config) -> Dict[str, str]:
    """Obtiene las personalidades disponibles en la configuración."""
    return config.personalities 