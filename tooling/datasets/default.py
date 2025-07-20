"""
Fetches datasets and returns in standerdised format 
"""


from typing import Tuple, Callable
from .dataset import Dataset
from tooling.benchmarking.rubric.rubric import RubricProtocol



def GPQA(train_size=None, test_size = None) -> Tuple[Dataset, Dataset, RubricProtocol]:
    """
    Returns Rubric
    """
    pass
