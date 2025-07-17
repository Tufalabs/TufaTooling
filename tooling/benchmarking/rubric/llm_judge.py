


from ...models.model import Model
from ...utils.extractor.extractors import xml_tag_extractor

import logging

PROMPT = """

You are an LLM judge your goal is to judge whether the following is correct

Ground Truth {ground_truth}

Answer {answer}


Output your answer 0 for incorrect 1 for correct in <answer> tags
"""


class JudgeError(ValueError):
    pass


class LLMJudge():
    
    def __init__(self, marker:Model = None, batch_size:int = 128) -> None:
        
        default_marker = Model("gpt-4o-mini") 

        self._marker =  marker if marker else default_marker
        self._batch_size = batch_size


    async def __call__(self, answer:str, ground_truth:str, model:Model = None) -> logging.Any:
        
        marker = model if model else self._marker


        
        formatted_prompt = PROMPT.format(ground_truth, answer)

        judge_ouput = await marker.generate(formatted_prompt, self._marker)

        
        judge_scoring = xml_tag_extractor(judge_ouput, "answer")

        try:
            score = int(judge_scoring)
        except ValueError:
            score = 0
            logging.warn("LLM Judge did not output valid response")
            raise JudgeError

        return score


    

    



