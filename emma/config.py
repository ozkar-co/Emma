"""
Módulo de configuración para Emma.
Gestiona la carga y validación de configuraciones desde archivos YAML.
"""

import os
import yaml
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "model": "gemma3:1b",
    "temperature": 0.7,
    "max_tokens": 2000,
    "top_p": 0.9,
    "top_k": 40,
    "context_size": 4096,
    "system_prompt": "Eres Emma, una asistente virtual inteligente y amigable.",
    "chat_history_limit": 20,
    "save_conversations": True,
    "conversation_dir": "conversations",
    "verbose": False,
    "ollama_host": "http://localhost:11434",
    "api_key": "",
    "user_name": "Tú",
    "use_panels": True,
    "personalities": {
        "default": "Eres Emma, una asistente virtual inteligente y amigable.",
        "creativa": "Eres Emma, una asistente creativa con gran imaginación.",
        "técnica": "Eres Emma, una asistente técnica experta en programación y tecnología.",
        "concisa": "Eres Emma, una asistente que proporciona respuestas breves y directas.",
        "educativa": "Eres Emma, una asistente educativa que explica conceptos de manera clara y didáctica."
    }
}

class Config(BaseModel):
    """Clase de configuración para Emma."""
    model: str = Field(default="gemma3:1b", description="Modelo de Ollama a utilizar")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Temperatura para la generación de texto")
    max_tokens: int = Field(default=2000, ge=1, description="Número máximo de tokens a generar")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Valor de top_p para la generación de texto")
    top_k: int = Field(default=40, ge=0, description="Valor de top_k para la generación de texto")
    context_size: int = Field(default=4096, ge=0, description="Tamaño del contexto a mantener")
    system_prompt: str = Field(default="Eres Emma, una asistente virtual inteligente y amigable.", description="Prompt del sistema para definir el comportamiento del asistente")
    chat_history_limit: int = Field(default=20, ge=0, description="Número máximo de mensajes a mantener en el historial")
    save_conversations: bool = Field(default=True, description="Guardar las conversaciones en disco")
    conversation_dir: str = Field(default="conversations", description="Directorio para guardar las conversaciones")
    verbose: bool = Field(default=False, description="Modo verboso para depuración")
    ollama_host: str = Field(default="http://localhost:11434", description="Host de la API de Ollama")
    api_key: str = Field(default="", description="Clave de API (si es necesaria)")
    user_name: str = Field(default="Tú", description="Nombre a mostrar para el usuario en el chat")
    use_panels: bool = Field(default=True, description="Mostrar mensajes de Emma en paneles/recuadros")
    personalities: Dict[str, str] = Field(default_factory=dict, description="Diccionario de personalidades disponibles")

    @classmethod
    def from_file(cls, file_path: str = "config.yaml") -> 'Config':
        """Carga la configuración desde un archivo YAML."""
        config_data = DEFAULT_CONFIG.copy()
        
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_config = yaml.safe_load(f)
                    if file_config:
                        config_data.update(file_config)
            else:
                logger.warning(f"Archivo de configuración {file_path} no encontrado. Usando configuración por defecto.")
                # Crear el archivo de configuración con valores por defecto
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            logger.error(f"Error al cargar la configuración: {str(e)}")
        
        return cls(**config_data)
    
    def save(self, file_path: str = "config.yaml") -> bool:
        """Guarda la configuración en un archivo YAML."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.model_dump(), f, default_flow_style=False, allow_unicode=True)
            return True
        except Exception as e:
            logger.error(f"Error al guardar la configuración: {str(e)}")
            return False
    
    def get_personality(self, name: str = "default") -> str:
        """Obtiene una personalidad por su nombre."""
        return self.personalities.get(name, self.system_prompt)
    
    def add_personality(self, name: str, prompt: str) -> None:
        """Añade una nueva personalidad."""
        self.personalities[name] = prompt
    
    def remove_personality(self, name: str) -> bool:
        """Elimina una personalidad."""
        if name in self.personalities and name != "default":
            del self.personalities[name]
            return True
        return False 