"""
Chat module for Emma - Refactored for modular architecture
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from .config import Config
from .core.types import Conversation, Message
from .adapters import OllamaAdapter
from .personalities import PersonalityManager

logger = logging.getLogger(__name__)


class ChatSession:
    """Chat session for Emma - Refactored for modular architecture."""
    
    def __init__(self, config: Config, personality_manager: Optional[PersonalityManager] = None):
        self.config = config
        self.llm_adapter = OllamaAdapter(config)
        self.personality_manager = personality_manager or PersonalityManager()
        
        # Initialize conversation with default personality
        system_prompt = self.personality_manager.get_personality("default")
        self.conversation = Conversation()
        if system_prompt:
            self.conversation.add_system_message(system_prompt)
        
        # Create conversations directory if needed
        if config.save_conversations:
            os.makedirs(config.conversation_dir, exist_ok=True)
    
    def get_response(self, user_input: str) -> str:
        """Get response from the LLM adapter."""
        try:
            # Add user message to conversation
            self.conversation.add_user_message(user_input)
            
            # Analyze prompt for search requirements
            search_command = self.llm_adapter.analyze_prompt(user_input)
            
            if search_command:
                # If search is needed, return the search command
                response = search_command
            else:
                # Get response from LLM
                messages = self.conversation.to_ollama_messages()
                response = self.llm_adapter.generate_response(messages)
                
                # Process search commands in response
                response = self.llm_adapter.process_search_commands(response)
            
            # Add assistant response to conversation
            self.conversation.add_assistant_message(response)
            
            # Save conversation if enabled
            if self.config.save_conversations:
                self._save_conversation()
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting response: {str(e)}")
            error_msg = f"Error: {str(e)}"
            self.conversation.add_assistant_message(error_msg)
            return error_msg
    
    def change_personality(self, personality_name: str) -> bool:
        """Change the personality of the session."""
        try:
            # Get new personality prompt
            new_prompt = self.personality_manager.get_personality(personality_name)
            if not new_prompt:
                logger.warning(f"Personality '{personality_name}' not found")
                return False
            
            # Create new conversation with new personality
            self.conversation = Conversation()
            self.conversation.add_system_message(new_prompt)
            
            logger.info(f"Changed personality to: {personality_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error changing personality: {str(e)}")
            return False
    
    def _save_conversation(self) -> None:
        """Save the current conversation to disk."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}_{self.conversation.id[:8]}.json"
            filepath = os.path.join(self.config.conversation_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.conversation.to_dict(), f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Conversation saved to: {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving conversation: {str(e)}")
    
    def load_conversation(self, conversation_id: str) -> bool:
        """Load a conversation from disk."""
        try:
            # Find conversation file
            for filename in os.listdir(self.config.conversation_dir):
                if conversation_id in filename and filename.endswith('.json'):
                    filepath = os.path.join(self.config.conversation_dir, filename)
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    self.conversation = Conversation.from_dict(data)
                    logger.info(f"Loaded conversation: {conversation_id}")
                    return True
            
            logger.warning(f"Conversation not found: {conversation_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error loading conversation: {str(e)}")
            return False
    
    def list_conversations(self) -> List[Dict[str, Any]]:
        """List all saved conversations."""
        conversations = []
        
        try:
            if not os.path.exists(self.config.conversation_dir):
                return conversations
            
            for filename in os.listdir(self.config.conversation_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.config.conversation_dir, filename)
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        conversations.append({
                            'id': data.get('id', ''),
                            'filename': filename,
                            'created_at': data.get('created_at', ''),
                            'updated_at': data.get('updated_at', ''),
                            'message_count': len(data.get('messages', []))
                        })
                        
                    except Exception as e:
                        logger.warning(f"Error reading conversation file {filename}: {str(e)}")
            
            # Sort by updated_at (most recent first)
            conversations.sort(key=lambda x: x['updated_at'], reverse=True)
            
        except Exception as e:
            logger.error(f"Error listing conversations: {str(e)}")
        
        return conversations
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the current conversation."""
        return {
            'id': self.conversation.id,
            'message_count': len(self.conversation.messages),
            'created_at': self.conversation.created_at,
            'updated_at': self.conversation.updated_at,
            'last_message': self.conversation.messages[-1].content if self.conversation.messages else None
        } 