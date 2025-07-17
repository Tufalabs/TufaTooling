


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

def llm_judge(answer, ground_truth, model="gpt-4o-mini") -> int:
    model = Model(model=model)
    
    formatted_prompt = PROMPT.format(ground_truth, answer)
    
    judge_output = xml_tag_extractor(formatted_prompt, "answer")

    try:
        score = int(judge_output)
    except ValueError:
        score = 0
        logging.warn("LLM Judge did not output valid response")
        raise JudgeError

    return score

    

    



