"""
Módulo de chat para Emma.
Gestiona la comunicación con Ollama y las sesiones de chat.
"""

import os
import json
import time
import uuid
import requests
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from .config import Config

# Configurar el logger para este módulo
logger = logging.getLogger(__name__)

class Message:
    """Clase para representar un mensaje en la conversación."""
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el mensaje a un diccionario."""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Crea un mensaje desde un diccionario."""
        msg = cls(data["role"], data["content"])
        if "timestamp" in data:
            msg.timestamp = data["timestamp"]
        return msg

class Conversation:
    """Clase para gestionar una conversación."""
    def __init__(self, system_prompt: str = ""):
        self.id = str(uuid.uuid4())
        self.messages: List[Message] = []
        if system_prompt:
            self.add_system_message(system_prompt)
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
    
    def add_system_message(self, content: str) -> None:
        """Añade un mensaje del sistema."""
        self.messages.append(Message("system", content))
        self.updated_at = datetime.now().isoformat()
    
    def add_user_message(self, content: str) -> None:
        """Añade un mensaje del usuario."""
        self.messages.append(Message("user", content))
        self.updated_at = datetime.now().isoformat()
    
    def add_assistant_message(self, content: str) -> None:
        """Añade un mensaje del asistente."""
        self.messages.append(Message("assistant", content))
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la conversación a un diccionario."""
        return {
            "id": self.id,
            "messages": [msg.to_dict() for msg in self.messages],
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Conversation':
        """Crea una conversación desde un diccionario."""
        conv = cls()
        conv.id = data.get("id", str(uuid.uuid4()))
        conv.messages = [Message.from_dict(msg) for msg in data.get("messages", [])]
        conv.created_at = data.get("created_at", datetime.now().isoformat())
        conv.updated_at = data.get("updated_at", datetime.now().isoformat())
        return conv
    
    def to_ollama_messages(self) -> List[Dict[str, str]]:
        """Convierte los mensajes al formato esperado por Ollama."""
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]
    
    def get_last_messages(self, limit: int) -> List[Message]:
        """Obtiene los últimos mensajes de la conversación."""
        return self.messages[-limit:] if limit > 0 else self.messages

class ChatSession:
    """Clase para gestionar una sesión de chat con Ollama."""
    def __init__(self, config: Config):
        self.config = config
        
        # Preparar el prompt del sistema con información del usuario
        system_prompt = config.system_prompt
        if "Oz" not in system_prompt and config.user_name == "Oz":
            system_prompt += f" Estás interactuando con {config.user_name}, un usuario de la interfaz Emma."
            
        self.conversation = Conversation(system_prompt)
        
        # Asegurarse de que la URL de la API no termina con una barra
        base_url = config.ollama_host.rstrip('/')
        self.ollama_url = f"{base_url}/api/chat"
        
        # URL para verificar la versión de Ollama
        self.version_url = f"{base_url}/api/version"
        
        # Verificar la versión de Ollama (opcional, solo en modo verbose)
        if config.verbose:
            try:
                version_response = requests.get(self.version_url, timeout=2)
                if version_response.status_code == 200:
                    version_data = version_response.json()
                    logger.info(f"Versión de Ollama: {version_data.get('version', 'desconocida')}")
            except Exception as e:
                logger.warning(f"No se pudo verificar la versión de Ollama: {str(e)}")
        
        # Crear directorio para conversaciones si no existe
        if config.save_conversations:
            os.makedirs(config.conversation_dir, exist_ok=True)
    
    def get_response(self, user_input: str) -> str:
        """Obtiene una respuesta del modelo de Ollama."""
        # Añadir mensaje del usuario
        self.conversation.add_user_message(user_input)
        
        # Preparar la solicitud para Ollama
        messages = self.conversation.to_ollama_messages()
        request_data = {
            "model": self.config.model,
            "messages": messages,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens,
                "top_p": self.config.top_p,
                "top_k": self.config.top_k
            },
            "stream": False  # Asegurarse de que no se usa streaming
        }
        
        if self.config.verbose:
            logger.debug(f"Solicitud a Ollama: {json.dumps(request_data, indent=2)}")
        
        try:
            # Hacer la solicitud a Ollama
            response = requests.post(self.ollama_url, json=request_data)
            response.raise_for_status()
            
            try:
                # Procesar la respuesta
                response_data = response.json()
                if self.config.verbose:
                    logger.debug(f"Respuesta de Ollama: {json.dumps(response_data, indent=2)}")
                
                # Intentar extraer el mensaje del asistente con manejo de diferentes formatos
                assistant_message = ""
                if "message" in response_data and "content" in response_data["message"]:
                    assistant_message = response_data["message"]["content"]
                elif "response" in response_data:
                    # Formato alternativo que algunas versiones de Ollama pueden usar
                    assistant_message = response_data["response"]
                else:
                    # Si no podemos encontrar el mensaje en el formato esperado, intentamos buscar en cualquier clave
                    for key, value in response_data.items():
                        if isinstance(value, dict) and "content" in value:
                            assistant_message = value["content"]
                            break
                        elif isinstance(value, str) and value.strip():
                            assistant_message = value
                            break
            
            except json.JSONDecodeError as json_err:
                logger.warning(f"Error al decodificar JSON: {str(json_err)}")
                # Si hay un error al decodificar el JSON, intentamos usar la respuesta en texto plano
                assistant_message = response.text.strip()
                if assistant_message.startswith("{") and "}" in assistant_message:
                    # Intenta extraer solo la primera parte JSON válida
                    try:
                        valid_json = assistant_message.split("}")[0] + "}"
                        json_data = json.loads(valid_json)
                        if "message" in json_data and "content" in json_data["message"]:
                            assistant_message = json_data["message"]["content"]
                    except:
                        pass  # Si falla, mantenemos la respuesta en texto plano
            
            # Si después de todos los intentos no tenemos una respuesta
            if not assistant_message:
                logger.error("No se pudo obtener una respuesta del modelo")
                assistant_message = "Lo siento, no pude generar una respuesta."
            
            # Añadir mensaje del asistente
            self.conversation.add_assistant_message(assistant_message)
            
            # Guardar la conversación si está habilitado
            if self.config.save_conversations:
                self._save_conversation()
            
            return assistant_message
            
        except requests.RequestException as e:
            logger.error(f"Error al comunicarse con Ollama: {str(e)}")
            error_msg = f"Error al comunicarse con Ollama: {str(e)}"
            self.conversation.add_assistant_message(error_msg)
            return error_msg
    
    def change_personality(self, personality_name: str) -> bool:
        """Cambia la personalidad del asistente."""
        system_prompt = self.config.get_personality(personality_name)
        if system_prompt:
            # Asegurarse de que el prompt incluye información del usuario si no la contiene ya
            if self.config.user_name not in system_prompt:
                system_prompt += f" Estás conversando con {self.config.user_name}."
                
            # Iniciar una nueva conversación con la nueva personalidad
            self.conversation = Conversation(system_prompt)
            return True
        return False
    
    def _save_conversation(self) -> None:
        """Guarda la conversación actual en un archivo JSON."""
        try:
            filename = f"{self.conversation.id}.json"
            filepath = os.path.join(self.config.conversation_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.conversation.to_dict(), f, indent=2, ensure_ascii=False)
                
            if self.config.verbose:
                logger.debug(f"Conversación guardada en {filepath}")
                
        except Exception as e:
            logger.error(f"Error al guardar la conversación: {str(e)}")
    
    def load_conversation(self, conversation_id: str) -> bool:
        """Carga una conversación desde un archivo JSON."""
        try:
            filepath = os.path.join(self.config.conversation_dir, f"{conversation_id}.json")
            
            if not os.path.exists(filepath):
                logger.error(f"No se encontró la conversación {conversation_id}")
                return False
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.conversation = Conversation.from_dict(data)
            return True
            
        except Exception as e:
            logger.error(f"Error al cargar la conversación: {str(e)}")
            return False
    
    def list_conversations(self) -> List[Dict[str, Any]]:
        """Lista todas las conversaciones guardadas."""
        conversations = []
        
        try:
            if not os.path.exists(self.config.conversation_dir):
                return conversations
                
            for filename in os.listdir(self.config.conversation_dir):
                if filename.endswith(".json"):
                    filepath = os.path.join(self.config.conversation_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    # Extraer información resumida
                    summary = {
                        "id": data.get("id", ""),
                        "created_at": data.get("created_at", ""),
                        "updated_at": data.get("updated_at", ""),
                        "message_count": len(data.get("messages", [])),
                        "preview": data.get("messages", [{}])[0].get("content", "")[:50] + "..."
                    }
                    conversations.append(summary)
                    
            # Ordenar por fecha de actualización (más reciente primero)
            conversations.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
            
        except Exception as e:
            logger.error(f"Error al listar las conversaciones: {str(e)}")
            
        return conversations 