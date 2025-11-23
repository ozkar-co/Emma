"""
Personality Manager for Emma - Handles personality loading and management
"""

import os
import yaml
import logging
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class PersonalityManager:
    """Manages personality loading and storage."""
    
    def __init__(self, personalities_dir: str = "personalities"):
        self.personalities_dir = Path(personalities_dir)
        self.personalities: Dict[str, str] = {}
        self._ensure_personalities_dir()
        self._load_personalities()
    
    def _ensure_personalities_dir(self) -> None:
        """Ensure the personalities directory exists."""
        self.personalities_dir.mkdir(exist_ok=True)
    
    def _load_personalities(self) -> None:
        """Load all personality files from the personalities directory."""
        if not self.personalities_dir.exists():
            logger.warning(f"Personalities directory {self.personalities_dir} does not exist")
            return
        
        # Load personality files
        for file_path in self.personalities_dir.glob("*.yaml"):
            try:
                personality_name = file_path.stem
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'prompt' in data:
                        self.personalities[personality_name] = data['prompt']
                        logger.info(f"Loaded personality: {personality_name}")
                    else:
                        logger.warning(f"Invalid personality file format: {file_path}")
            except Exception as e:
                logger.error(f"Error loading personality {file_path}: {str(e)}")
        
        # If no personalities loaded, create default ones
        if not self.personalities:
            self._create_default_personalities()
    
    def _create_default_personalities(self) -> None:
        """Create default personality files."""
        default_personalities = {
            "default": {
                "name": "Default",
                "description": "Friendly and versatile assistant",
                "prompt": "Eres Emma, una asistente virtual inteligente y amigable."
            },
            "creativa": {
                "name": "Creativa",
                "description": "Creative assistant with great imagination",
                "prompt": "Eres Emma, una asistente creativa con gran imaginación."
            },
            "técnica": {
                "name": "Técnica",
                "description": "Technical expert in programming and technology",
                "prompt": "Eres Emma, una asistente técnica experta en programación y tecnología."
            },
            "concisa": {
                "name": "Concisa",
                "description": "Brief and direct responses",
                "prompt": "Eres Emma, una asistente que proporciona respuestas breves y directas."
            },
            "educativa": {
                "name": "Educativa",
                "description": "Educational assistant with clear explanations",
                "prompt": "Eres Emma, una asistente educativa que explica conceptos de manera clara y didáctica."
            }
        }
        
        for personality_id, personality_data in default_personalities.items():
            self._save_personality_file(personality_id, personality_data)
            self.personalities[personality_id] = personality_data['prompt']
    
    def _save_personality_file(self, personality_id: str, data: Dict) -> None:
        """Save a personality to a YAML file."""
        file_path = self.personalities_dir / f"{personality_id}.yaml"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            logger.info(f"Created personality file: {file_path}")
        except Exception as e:
            logger.error(f"Error saving personality file {file_path}: {str(e)}")
    
    def get_personality(self, name: str = "default") -> str:
        """Get personality prompt by name."""
        return self.personalities.get(name, self.personalities.get("default", ""))
    
    def add_personality(self, name: str, prompt: str, description: str = "") -> bool:
        """Add a new personality."""
        try:
            personality_data = {
                "name": name.capitalize(),
                "description": description,
                "prompt": prompt
            }
            
            self._save_personality_file(name, personality_data)
            self.personalities[name] = prompt
            logger.info(f"Added personality: {name}")
            return True
        except Exception as e:
            logger.error(f"Error adding personality {name}: {str(e)}")
            return False
    
    def remove_personality(self, name: str) -> bool:
        """Remove a personality."""
        if name == "default":
            logger.warning("Cannot remove default personality")
            return False
        
        try:
            file_path = self.personalities_dir / f"{name}.yaml"
            if file_path.exists():
                file_path.unlink()
            
            if name in self.personalities:
                del self.personalities[name]
            
            logger.info(f"Removed personality: {name}")
            return True
        except Exception as e:
            logger.error(f"Error removing personality {name}: {str(e)}")
            return False
    
    def list_personalities(self) -> List[Dict[str, str]]:
        """List all available personalities."""
        personalities_list = []
        
        for personality_id, prompt in self.personalities.items():
            file_path = self.personalities_dir / f"{personality_id}.yaml"
            description = ""
            
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        description = data.get('description', '')
                except Exception:
                    pass
            
            personalities_list.append({
                'id': personality_id,
                'name': personality_id.capitalize(),
                'description': description,
                'prompt': prompt[:100] + "..." if len(prompt) > 100 else prompt
            })
        
        return personalities_list
    
    def get_personality_info(self, name: str) -> Optional[Dict[str, str]]:
        """Get detailed information about a personality."""
        if name not in self.personalities:
            return None
        
        file_path = self.personalities_dir / f"{name}.yaml"
        description = ""
        
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    description = data.get('description', '')
            except Exception:
                pass
        
        return {
            'id': name,
            'name': name.capitalize(),
            'description': description,
            'prompt': self.personalities[name]
        } 