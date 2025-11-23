"""
Core module for Emma - Modular Architecture
"""

from .base import BaseLLMAdapter, BaseMemory, BaseConfig
from .types import Message, Conversation, ChatSession

__all__ = [
    'BaseLLMAdapter',
    'BaseMemory', 
    'BaseConfig',
    'Message',
    'Conversation',
    'ChatSession'
] 