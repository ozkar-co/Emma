"""
Core types for Emma - Data structures and models
"""

import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Represents a message in a conversation."""
    role: str = Field(..., description="Role of the message sender (system, user, assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create message from dictionary."""
        return cls(**data)


class Conversation(BaseModel):
    """Represents a conversation with messages."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    messages: List[Message] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    def add_message(self, role: str, content: str) -> None:
        """Add a new message to the conversation."""
        self.messages.append(Message(role=role, content=content))
        self.updated_at = datetime.now().isoformat()
    
    def add_system_message(self, content: str) -> None:
        """Add a system message."""
        self.add_message("system", content)
    
    def add_user_message(self, content: str) -> None:
        """Add a user message."""
        self.add_message("user", content)
    
    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message."""
        self.add_message("assistant", content)
    
    def to_ollama_messages(self) -> List[Dict[str, str]]:
        """Convert messages to Ollama format."""
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]
    
    def get_last_messages(self, limit: int) -> List[Message]:
        """Get the last N messages from the conversation."""
        return self.messages[-limit:] if limit > 0 else self.messages
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert conversation to dictionary."""
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Conversation':
        """Create conversation from dictionary."""
        return cls(**data)


class ChatSession(BaseModel):
    """Represents a chat session with conversation and configuration."""
    conversation: Conversation
    config: 'BaseConfig'
    
    class Config:
        arbitrary_types_allowed = True
    
    def get_response(self, user_input: str) -> str:
        """Get response from the LLM adapter."""
        raise NotImplementedError("Subclasses must implement get_response")
    
    def change_personality(self, personality_name: str) -> bool:
        """Change the personality of the session."""
        raise NotImplementedError("Subclasses must implement change_personality") 