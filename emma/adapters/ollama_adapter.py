"""
Ollama adapter for Emma - Integration with Ollama API
"""

import requests
import logging
import re
from typing import List, Dict, Any, Optional
from ..core.base import BaseLLMAdapter, BaseConfig

logger = logging.getLogger(__name__)


class OllamaAdapter(BaseLLMAdapter):
    """Adapter for Ollama LLM service."""
    
    def __init__(self, config: BaseConfig):
        super().__init__(config)
        
        # Ensure the API URL doesn't end with a slash
        base_url = config.ollama_host.rstrip('/')
        self.ollama_url = f"{base_url}/api/chat"
        self.version_url = f"{base_url}/api/version"
        
        # Verify Ollama version (optional, only in verbose mode)
        if config.verbose:
            self._verify_ollama_version()
    
    def _verify_ollama_version(self) -> None:
        """Verify Ollama version and log it."""
        try:
            version_response = requests.get(self.version_url, timeout=2)
            if version_response.status_code == 200:
                version_data = version_response.json()
                logger.info(f"Ollama version: {version_data.get('version', 'unknown')}")
        except Exception as e:
            logger.warning(f"Could not verify Ollama version: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if Ollama service is available."""
        try:
            response = requests.get(self.version_url, timeout=2)
            return response.status_code == 200
        except Exception:
            return False
    
    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response from Ollama."""
        # Prepare request data
        request_data = {
            "model": self.config.model,
            "messages": messages,
            "options": {
                "temperature": kwargs.get("temperature", self.config.temperature),
                "num_predict": kwargs.get("max_tokens", self.config.max_tokens),
                "top_p": kwargs.get("top_p", self.config.top_p),
                "top_k": kwargs.get("top_k", self.config.top_k)
            },
            "stream": False
        }
        
        try:
            # Make request to Ollama
            response = requests.post(self.ollama_url, json=request_data)
            response.raise_for_status()
            
            # Process response
            response_data = response.json()
            
            if "message" in response_data and "content" in response_data["message"]:
                return response_data["message"]["content"].strip()
            elif "response" in response_data:
                return response_data["response"].strip()
            else:
                logger.error(f"Unexpected response format from Ollama: {response_data}")
                return "Error: Unexpected response format from Ollama"
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error communicating with Ollama: {str(e)}")
            return f"Error: Could not communicate with Ollama - {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error in Ollama response: {str(e)}")
            return f"Error: Unexpected error - {str(e)}"
    
    def analyze_prompt(self, user_input: str) -> Optional[str]:
        """Analyze user input to determine if search is needed."""
        # Prepare analysis prompt
        analysis_prompt = f"""
        Analyze the following user prompt and determine if it requires a search.
        If it requires search, respond with the appropriate search command.
        If it doesn't require search, respond with "NO_SEARCH".
        
        Prompt: {user_input}
        """
        
        # Prepare request for Ollama
        request_data = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": analysis_prompt}
            ],
            "options": {
                "temperature": 0.1,  # Low temperature for more deterministic responses
                "num_predict": 100,
                "top_p": 0.9,
                "top_k": 40
            },
            "stream": False
        }
        
        try:
            # Make request to Ollama
            response = requests.post(self.ollama_url, json=request_data)
            response.raise_for_status()
            
            # Process response
            response_data = response.json()
            analysis_result = ""
            
            if "message" in response_data and "content" in response_data["message"]:
                analysis_result = response_data["message"]["content"].strip()
            elif "response" in response_data:
                analysis_result = response_data["response"].strip()
            
            # If result is not "NO_SEARCH", assume it's a search command
            if analysis_result != "NO_SEARCH":
                return analysis_result
            
            return None
            
        except Exception as e:
            logger.error(f"Error in prompt analysis: {str(e)}")
            return None
    
    def process_search_commands(self, response: str) -> str:
        """Process search commands in the response."""
        # Replace search commands with user-friendly messages
        def replace_search(match):
            search_type = match.group(1)
            search_term = match.group(2)
            
            if search_type == "search":
                return f"[Searching internet for: {search_term}]"
            elif search_type == "memory":
                return f"[Searching memory for: {search_term}]"
            elif search_type == "query":
                return f"[Searching database for: {search_term}]"
            else:
                return match.group(0)
        
        # Apply replacements
        processed_response = re.sub(
            r'<(search|memory|query)>(.*?)</\1>',
            replace_search,
            response,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        return processed_response 