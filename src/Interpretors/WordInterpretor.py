
# Só de exemplo, não é usado no projeto

from typing import Union
from Layout import Layout
from Stategies.AvalStrat.Measured import Measured
import pandas as pd


class WordInterpretor:
    def __init__(self, layout: Layout) -> None:
        self.layout = layout
        self.target_file = self.read_doc()

    def read_doc(self) -> pd.DataFrame:
        pass
            
    def find_index_and_value_of_column(self, label: str) -> Union[list, int]:
        pass

    def get_column_values(self, index: int) -> list:
        pass
    