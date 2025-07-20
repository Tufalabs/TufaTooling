
from typing import Optional


from typing import Protocol, Optional

class ExtractorProtocol(Protocol):
    """
    Protocol for text extraction functions.
    
    Extractors take a text input and extract specific content from it,
    returning the extracted text or None if not found.
    """
    
    def __call__(self, text: str, *args, **kwargs) -> Optional[str]:
        """
        Extract content from text.
        
        Args:
            text: The input text to extract from
            *args: Additional positional arguments (e.g., tag name for XML extractor)
            **kwargs: Additional keyword arguments
            
        Returns:
            Extracted text content, or None if not found
        """
        ...



def boxed(text:str) -> Optional[str]:

    index_start = text.rfind("boxed{")
    index_end = text.lfind("}", index_start)

    if index_start == -1 or index_end == -1:
        return None

    return text[index_start:index_end]

def xml_tag_extractor(text:str, tag) -> Optional[str]:

    index_start = text.rfind(f"<{tag}>")
    index_value_start = index_start+ len(f"<{tag}>")
    index_end = text.find(f"</{tag}>", index_value_start)

    if index_start == -1 or index_end == -1:
        return None

    return text[index_value_start:index_end]

