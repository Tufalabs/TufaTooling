
from typing import Callable, List
from math import ceil

from tooling.models.model import Model
from tooling.datasets.dataset import Dataset


def benchmark(model: Model, 
              dataset: Dataset, 
              marker: callable,
              batch_size:int= 128,
              system_prompt:str = "",
              model_solutions:List[str] = "",
              ):
    
    if not model_solutions:
        model_solutions = model.batch_generate(dataset, batch_size=batch_size)
    
    
    total = 0
    for solution in model_solutions:
        score = marker(solution)
        total += score    

    return score/len(dataset)



        



                    
                    
