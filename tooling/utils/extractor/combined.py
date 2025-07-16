

from typing import Any, Callable




class CombinedParser:

    def __init__(self, *parsers: Callable):
        """Takes in mutliple functions and combines them"""

        self.parsers = parsers


    def __call__(self, text:str) -> Any:
        for parser in self.parsers:
            text = parser(text)
        return text
    
    
