


from ...models.model import Model
from ...utils.extractor.extractors import xml_tag_extractor
from .rubric import RubricProtocol

import logging

PROMPT = """
You are an LLM judge your goal is to judge whether the following is correct

Ground Truth: {ground_truth}

Answer: {answer}

Output your answer 0 for incorrect 1 for correct in <answer> tags
"""

class JudgeError(ValueError):
    pass

class LLMJudge:   
    
    def __init__(self, marker: Model = None, batch_size: int = 128) -> None:
        default_marker = Model("gpt-4o-mini") 
        self._marker = marker if marker else default_marker
        self._batch_size = batch_size

    async def __call__(self, answer: str, ground_truth: str) -> int:
        
        
        # Fix: Use named parameters in format
        formatted_prompt = PROMPT.format(ground_truth=ground_truth, answer=answer)
        
        # Fix: Use the correct marker variable
        judge_output = await self._marker.generate(formatted_prompt)
        
        judge_scoring = xml_tag_extractor(judge_output, "answer")

        try:
            score = int(judge_scoring)
        except ValueError:
            logging.warning("LLM Judge did not output valid response")
            raise JudgeError("Invalid LLM judge response")

        return score

# Test







