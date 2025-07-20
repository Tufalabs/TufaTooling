


from ..model import Model


class CLIModelInterface(Model):

    async def __init__(self, model: str, max_tokens: int = 1024, temperature: float = 0.7, top_p: float = 0.95, top_k: int | None = None, stream: bool = False, **kwargs) -> None:
        super().__init__(model, max_tokens, temperature, top_p, top_k, stream, **kwargs)

        while True:
            prompt = input("Enter your prompt")
            response_text = await self.generate(prompt=prompt)
            self._print_response(response_text)    

            
    @staticmethod
    def _print_response(text):
        print("-"*10)
        print(text)
        print("-"*10)
    

    