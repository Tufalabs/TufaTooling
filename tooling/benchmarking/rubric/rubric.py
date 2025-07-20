from typing import Protocol, runtime_checkable
from ...models.model import Model


@runtime_checkable
class RubricProtocol(Protocol):
    """
    Protocol for rubric functions that evaluate answers against ground truth.
    
    Rubrics can be implemented as simple async functions or as classes with __call__ methods.
    They should return integer scores (typically 0 for incorrect, 1 for correct, but can
    support multi-point scoring systems).
    """
    
    async def __call__(self, answer: str, ground_truth: str) -> int:
        """
        Evaluate an answer against the ground truth.
        
        Args:
            answer: The answer to evaluate (e.g., model output)
            ground_truth: The correct/expected answer
            model: Optional model override for rubrics that need model access
            
        Returns:
            Integer score (typically 0 for incorrect, 1 for correct)
            
        Raises:
            May raise exceptions for invalid inputs or evaluation errors
        """
        ...


