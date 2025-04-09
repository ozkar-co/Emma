"""
Módulo de memoria para Emma.
Gestiona el almacenamiento y recuperación de conocimiento para mejorar
las respuestas del modelo en conversaciones largas o múltiples sesiones.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

# Configurar el logger para este módulo
logger = logging.getLogger(__name__)

class Memory:
    """Clase base para los sistemas de memoria."""
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def add(self, key: str, value: Any) -> bool:
        """Añade un elemento a la memoria."""
        raise NotImplementedError("Debe ser implementado por subclases")
    
    def get(self, key: str) -> Optional[Any]:
        """Recupera un elemento de la memoria."""
        raise NotImplementedError("Debe ser implementado por subclases")
    
    def search(self, query: str, limit: int = 5) -> List[Any]:
        """Busca elementos relevantes en la memoria."""
        raise NotImplementedError("Debe ser implementado por subclases")
    
    def clear(self) -> bool:
        """Limpia toda la memoria."""
        raise NotImplementedError("Debe ser implementado por subclases")

class SimpleMemory(Memory):
    """Implementación simple de memoria basada en diccionario."""
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.data = {}
        self.save_path = config.get("memory_file", "emma_memory.json")
        self._load()
    
    def add(self, key: str, value: Any) -> bool:
        """Añade un elemento a la memoria."""
        self.data[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        return self._save()
    
    def get(self, key: str) -> Optional[Any]:
        """Recupera un elemento de la memoria."""
        if key in self.data:
            return self.data[key]["value"]
        return None
    
    def search(self, query: str, limit: int = 5) -> List[Any]:
        """
        Busca elementos relevantes en la memoria.
        Esta implementación simple solo busca coincidencias exactas o parciales.
        """
        results = []
        query = query.lower()
        
        for key, data in self.data.items():
            if query in key.lower() or (
                isinstance(data["value"], str) and query in data["value"].lower()
            ):
                results.append({
                    "key": key,
                    "value": data["value"],
                    "timestamp": data["timestamp"]
                })
                
                if len(results) >= limit:
                    break
                    
        return results
    
    def clear(self) -> bool:
        """Limpia toda la memoria."""
        self.data = {}
        return self._save()
    
    def _save(self) -> bool:
        """Guarda la memoria en disco."""
        try:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error al guardar la memoria: {str(e)}")
            return False
    
    def _load(self) -> bool:
        """Carga la memoria desde disco."""
        try:
            if os.path.exists(self.save_path):
                with open(self.save_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                return True
        except Exception as e:
            logger.error(f"Error al cargar la memoria: {str(e)}")
        return False

class ConversationMemory:
    """
    Clase para gestionar el contexto de conversaciones anteriores
    y proporcionar memoria a largo plazo para el modelo.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.memory_file = config.get("memory_file", "conversation_memory.json")
        self.max_entries = config.get("memory_max_entries", 100)
        self.entries: List[Dict[str, Any]] = []
        self._load()
    
    def add_conversation_summary(self, conversation_id: str, summary: str, tags: List[str] = None) -> bool:
        """Añade un resumen de conversación a la memoria."""
        if tags is None:
            tags = []
            
        entry = {
            "id": conversation_id,
            "summary": summary,
            "tags": tags,
            "timestamp": datetime.now().isoformat()
        }
        
        # Evitar duplicados
        self.entries = [e for e in self.entries if e["id"] != conversation_id]
        
        # Añadir nueva entrada
        self.entries.append(entry)
        
        # Limitar tamaño
        if len(self.entries) > self.max_entries:
            self.entries = sorted(
                self.entries, 
                key=lambda x: x["timestamp"], 
                reverse=True
            )[:self.max_entries]
        
        return self._save()
    
    def search_relevant_memories(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Busca memorias relevantes basadas en el texto de consulta.
        Implementación simple basada en coincidencia de palabras clave.
        """
        query_words = set(query.lower().split())
        results = []
        
        for entry in self.entries:
            # Comprobar coincidencia en resumen
            summary_words = set(entry["summary"].lower().split())
            tag_words = set(tag.lower() for tag in entry["tags"])
            
            # Calcular puntuación simple (coincidencia de palabras)
            summary_match = len(query_words.intersection(summary_words))
            tag_match = len(query_words.intersection(tag_words))
            score = summary_match + (tag_match * 2)  # Las etiquetas tienen más peso
            
            if score > 0:
                results.append({
                    "id": entry["id"],
                    "summary": entry["summary"],
                    "score": score,
                    "timestamp": entry["timestamp"]
                })
        
        # Ordenar por puntuación y limitar resultados
        return sorted(results, key=lambda x: x["score"], reverse=True)[:limit]
    
    def get_all_tags(self) -> List[str]:
        """Obtiene todas las etiquetas únicas en la memoria."""
        all_tags = set()
        for entry in self.entries:
            all_tags.update(entry.get("tags", []))
        return sorted(list(all_tags))
    
    def clear(self) -> bool:
        """Limpia toda la memoria de conversaciones."""
        self.entries = []
        return self._save()
    
    def _save(self) -> bool:
        """Guarda la memoria en disco."""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.entries, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error al guardar la memoria de conversaciones: {str(e)}")
            return False
    
    def _load(self) -> bool:
        """Carga la memoria desde disco."""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.entries = json.load(f)
                return True
        except Exception as e:
            logger.error(f"Error al cargar la memoria de conversaciones: {str(e)}")
        
        self.entries = []
        return False 