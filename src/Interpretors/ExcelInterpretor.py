

from typing import Union
from Types import Type
from Layout import Layout
import pandas as pd

class ExcelInterpretor:
    layout: Layout 
    target_file: pd.DataFrame

    def __init__(self, layout: Layout) -> None:
        self.layout = layout
        self.target_file = self.read_doc()
    
    def read_doc(self) -> pd.DataFrame:
        try:
            file = pd.read_excel(self.layout.get_filepath())
            return file
        except FileNotFoundError:
            print("File not found.")
            exit(1)
        except Exception as e:
            print(e)
            exit(1)
        
    
    def find_index_and_value_of_column(self, label: str) -> Union[list, int]:
        label_to_find = label

        matching_columns = [col for col in self.target_file.columns if label_to_find.lower() in col.lower()]

        result = []
        if matching_columns:
            for col_name in matching_columns:
                col_index = self.target_file.columns.get_loc(col_name)
                result.append((col_index, col_name))
        else:
            print(f"\nNo column matching label '{label_to_find}' found.")
        
        if len(result) == 1:
            return result[0]
        
        return result

    def get_column_values(self, index: int) -> list:
        values = self.target_file.iloc[:, index].values.tolist()
        indexes = [i for i in range(len(values))]
        return list(zip(indexes, values))    
    
    def get_layout(self) -> Layout:
        return self.layout
    
    def get_target_file(self) -> pd.DataFrame:
        return self.target_file