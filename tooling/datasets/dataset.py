
from typing import List


class Dataset:


    def __init__(self, data: List[dict]= None, 
                 question_col:str = "question",
                 answer_col: str = "answer") -> None:
        self.data =  data if data else []
        self.answer_col = answer_col
        self.question_col = question_col
        self.recommended_rubric = None


    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        return self.data[index]
    
    def filter(self, func:callable):
        return Dataset(func(self.data))
    
    def sort(self, key:callable):
        pass

    def to_hf_dataset(self):
        pass

    @classmethod
    def from_json(clf, json_path):
        pass

    @classmethod
    def from_csv(clf, csv_path):
        pass
    
        
    

