
from typing import Optional



def xml_tag_extractor(text:str, tag) -> Optional[str]:

    index_start = text.rfind(f"<{tag}>")
    index_value_start = index_start+ len(f"<{tag}>")
    index_end = text.find(f"</{tag}>", index_value_start)

    if index_start == -1 or index_end == -1:
        return None

    return text[index_value_start:index_end]
    