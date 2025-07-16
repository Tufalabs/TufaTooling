
import asyncio
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass

from ..utils.inference.inference import OpenRouter, generate

class Model:
    def __init__(self, 
                model: str,
                max_tokens: int = 1024,
                temperature: float = 0.7,
                top_p: float = 0.95,
                top_k: Optional[int] = None,
                stream: bool = False,
                **kwargs
                 ) -> None:
        
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.stream = stream
        self.kwargs = kwargs
        
        self.client = OpenRouter()

    async def generate(self, prompt: str, temperature=None, max_tokens=None):
        """Generate text using the configured model (async)."""
        return await self.client.generate_async(
            prompt=prompt, 
            model=self.model,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens,
            top_p=self.top_p,
            top_k=self.top_k,
            stream=self.stream,
            **self.kwargs
        )
        
    async def batch_generate(self, prompts: List[str], temperature=None, max_tokens=None):
        """Generate text for multiple prompts in parallel."""
       
        # Create tasks for all prompts
        tasks = []
        for prompt in prompts:
            task = self.client.generate_async(
                prompt=prompt, 
                model=self.model,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                top_p=self.top_p,
                top_k=self.top_k,
                stream=self.stream,
                **self.kwargs
            )
            tasks.append(task)
        
        # Run all tasks concurrently and wait for all to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results, converting exceptions to error messages if needed
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                # If there was an error, include the error message instead of the result
                processed_results.append(f"Error: {str(result)}")
            else:
                processed_results.append(result)
        
        return processed_results
    