"""
Base classes for Emma - Abstract interfaces and base implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class BaseConfig(BaseModel):
    """Base configuration class for Emma."""
    model: str = Field(default="gemma3:1b", description="Model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Temperature for text generation")
    max_tokens: int = Field(default=2000, ge=1, description="Maximum tokens to generate")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Top-p value for text generation")
    top_k: int = Field(default=40, ge=0, description="Top-k value for text generation")
    context_size: int = Field(default=4096, ge=0, description="Context size to maintain")
    system_prompt: str = Field(default="", description="System prompt for the assistant")
    chat_history_limit: int = Field(default=20, ge=0, description="Maximum messages to keep in history")
    save_conversations: bool = Field(default=True, description="Save conversations to disk")
    conversation_dir: str = Field(default="conversations", description="Directory to save conversations")
    verbose: bool = Field(default=False, description="Verbose mode for debugging")
    user_name: str = Field(default="Tú", description="User name to display in chat")
    use_panels: bool = Field(default=True, description="Show Emma messages in panels/boxes")
    
    @abstractmethod
    def get_personality(self, name: str = "default") -> str:
        """Get personality by name."""
        pass
    
    @abstractmethod
    def add_personality(self, name: str, prompt: str) -> None:
        """Add a new personality."""
        pass
    
    @abstractmethod
    def remove_personality(self, name: str) -> bool:
        """Remove a personality."""
        pass


class BaseLLMAdapter(ABC):
    """Base class for LLM adapters."""
    
    def __init__(self, config: BaseConfig):
        self.config = config
    
    @abstractmethod
    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response from the LLM."""
        pass
    
    @abstractmethod
    def analyze_prompt(self, user_input: str) -> Optional[str]:
        """Analyze user input to determine if search is needed."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the LLM service is available."""
        pass


class BaseMemory(ABC):
    """Base class for memory systems."""
    
    def __init__(self, config: BaseConfig):
        self.config = config
    
    @abstractmethod
    def save_conversation(self, conversation: 'Conversation') -> bool:
        """Save a conversation to memory."""
        pass
    
    @abstractmethod
    def load_conversation(self, conversation_id: str) -> Optional['Conversation']:
        """Load a conversation from memory."""
        pass
    
    @abstractmethod
    def list_conversations(self) -> List[Dict[str, Any]]:
        """List all saved conversations."""
        pass
    
    @abstractmethod
    def search_memory(self, query: str) -> List[Dict[str, Any]]:
        """Search in memory for relevant information."""
        pass 