
from .model import Model



class ReasoningModel(Model):

    def __init__(self, model: str, max_tokens: int = 1024, temperature: float = 0.7, top_p: float = 0.95, top_k: int | None = None, stream: bool = False, **kwargs) -> None:
        super().__init__(model, max_tokens, temperature, top_p, top_k, stream, **kwargs)
        


    def generate_with_reasoning(self, prompt: str, temperature=None, max_tokens=None):
        pass

    def generate_without_reasoning(self, prompt: str, temperature=None, max_tokens=None):
        pass