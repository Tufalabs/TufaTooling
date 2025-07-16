import os
import json
import logging
import requests
import aiohttp
from typing import Dict, List, Optional, Union, Any

logger = logging.getLogger(__name__)

class APIError(ValueError):
    """Error raised when the OpenRouter API returns an error."""
    def __init__(self, status_code=None, message=None, response_body=None):
        self.status_code = status_code
        self.response_body = response_body
        msg = f"API Error"
        if status_code:
            msg += f" ({status_code})"
        if message:
            msg += f": {message}"
        super().__init__(msg)

class OpenRouter:
    """Client for the OpenRouter API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key required via argument or OPENROUTER_API_KEY environment variable")
        
        self.base_url = "https://openrouter.ai/api/v1"
    
    def _prepare_payload(self, prompt, model, max_tokens, temperature, top_p, top_k, stream, **kwargs):
        """Helper to prepare the request payload for both sync and async methods"""
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream,
            **({"top_k": top_k} if top_k is not None else {}),
            **({"prompt": prompt} if isinstance(prompt, str) else {"messages": prompt}),
            **kwargs
        }
        return payload
        
    def generate(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        model: str = "anthropic/claude-3-opus-20240229",
        *,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 0.95,
        top_k: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> str:
        """Generate text from a prompt using OpenRouter API and return just the content."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = self._prepare_payload(prompt, model, max_tokens, temperature, top_p, top_k, stream, **kwargs)
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                stream=stream
            )
            
            # Handle errors directly instead of using raise_for_status()
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                except:
                    error_msg = f"HTTP {response.status_code}"
                
                raise APIError(
                    status_code=response.status_code,
                    message=error_msg,
                    response_body=response.text
                )
            
            if stream:
                return response  # Can't extract text directly from stream
            
            data = response.json()
            
            # Extract just the text content
            if 'choices' in data and len(data['choices']) > 0:
                if 'message' in data['choices'][0]:
                    return data['choices'][0]['message']['content']
                elif 'text' in data['choices'][0]:
                    return data['choices'][0]['text']
            
            # If we can't find the content in the expected location
            raise APIError(message=f"Unexpected response format: {data}")
                
        except requests.RequestException as e:
            # Convert to our APIError with the original exception as the cause
            if hasattr(e, 'response') and e.response:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('error', {}).get('message', str(e))
                except:
                    error_msg = str(e)
                
                raise APIError(
                    status_code=e.response.status_code if hasattr(e.response, 'status_code') else None,
                    message=error_msg,
                    response_body=e.response.text if hasattr(e.response, 'text') else None
                ) from e
            
            # If there's no response object, just wrap the original exception
            raise APIError(message=str(e)) from e
    
    async def generate_async(
        self,
        prompt: Union[str, List[Dict[str, str]]],
        model: str = "anthropic/claude-3-opus-20240229",
        *,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 0.95,
        top_k: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> str:
        """Generate text from a prompt using OpenRouter API and return just the content."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = self._prepare_payload(prompt, model, max_tokens, temperature, top_p, top_k, stream, **kwargs)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    # Handle errors directly
                    if response.status >= 400:
                        error_text = await response.text()
                        try:
                            error_data = await response.json()
                            error_msg = error_data.get('error', {}).get('message', f"HTTP {response.status}")
                        except:
                            error_msg = f"HTTP {response.status}"
                        
                        raise APIError(
                            status_code=response.status,
                            message=error_msg,
                            response_body=error_text
                        )
                    
                    data = await response.json()
                    
                    # Extract just the text content
                    if 'choices' in data and len(data['choices']) > 0:
                        if 'message' in data['choices'][0]:
                            return data['choices'][0]['message']['content']
                        elif 'text' in data['choices'][0]:
                            return data['choices'][0]['text']
                    
                    # If we can't find the content in the expected location
                    raise APIError(message=f"Unexpected response format: {data}")
        
        except aiohttp.ClientError as e:
            # Convert aiohttp errors to APIError
            raise APIError(message=f"Request error: {str(e)}") from e

    def stream_tokens(self, response):
        """Process streaming response and yield tokens as they arrive."""
        for line in response.iter_lines():
            if not line:
                continue
                
            line = line[6:] if line.startswith(b'data: ') else line
            if line.strip() == b'[DONE]':
                break
                
            try:
                data = json.loads(line)
                if delta := data.get('choices', [{}])[0].get('delta', {}).get('content'):
                    yield delta
            except json.JSONDecodeError:
                continue  # Skip invalid JSON lines silently
    
    async def stream_tokens_async(self, response):
        """Process streaming response asynchronously and yield tokens as they arrive."""
        async for line in response.content:
            if not line:
                continue
                
            line_str = line.decode('utf-8')
            if line_str.startswith('data: '):
                line_str = line_str[6:]
            if line_str.strip() == '[DONE]':
                break
                
            try:
                data = json.loads(line_str)
                if delta := data.get('choices', [{}])[0].get('delta', {}).get('content'):
                    yield delta
            except json.JSONDecodeError:
                continue  # Skip invalid JSON lines silently

# Convenience functions
def generate(prompt, model="anthropic/claude-3-opus-20240229", api_key=None, **kwargs):
    """Convenience function for quick generation with OpenRouter."""
    return OpenRouter(api_key).generate(prompt=prompt, model=model, **kwargs)

async def generate_async(prompt, model="anthropic/claude-3-opus-20240229", api_key=None, **kwargs):
    """Convenience function for quick async generation with OpenRouter."""
    return await OpenRouter(api_key).generate_async(prompt=prompt, model=model, **kwargs)