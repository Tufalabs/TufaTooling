
from typing import List


class Dataset:


    def __init__(self, data: List[]= None) -> None:
        self.data =  data if data else []
        



    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        return self.data[index]
    
    def filter(self, func:callable):

        return Dataset(func(self.data))
    
    def sort(self, key:callable):
        pass

        
    

