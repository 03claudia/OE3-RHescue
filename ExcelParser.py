

from Types import Type
from layout import Layout
import pandas as pd

class ExcelParser:
    def __init__(self, layout: Layout) -> None:
        self.layout = layout
        self.target_file = self.__read_excel()
    
    def parse(self):
        self.result: list = []

        layout = self.layout.get_data()
        questions = self.layout.get_type(Type.QUESTIONS)[0]

        # Pega em todos os avaliadores
        measurer_label = self.layout.get_type(Type.MEASURER)[0]
        measurer_index = self.__find_index_of_column(measurer_label["label"])
        measurer = self.__get_column_values(measurer_index)

        print(measurer)



    def __read_excel(self) -> pd.DataFrame:
        try:
            file = pd.read_excel(self.layout.get_filepath())
            return file
        except FileNotFoundError:
            print("File not found.")
            exit(1)
        except Exception as e:
            print(e)
            exit(1)

    def __compact_results(self, questions, measured) -> list:
        result = []
        columns = self.target_file.columns

        result = self.layout
        for question in questions["questions"]:
            col_index = self.__find_index_of_column(question["label"])

        print(questions["questions"])
    
    def __find_index_of_column(self, label: str) -> int:
        label_to_find = label

        matching_columns = [col for col in self.target_file.columns if label_to_find.lower() in col.lower()]

        if matching_columns:
            for col_name in matching_columns:
                return self.target_file.columns.get_loc(col_name)
        else:
            print(f"No column matching label '{label_to_find}' found.")

    def __get_column_values(self, index: int) -> list:
        return self.target_file.iloc[:, index].values.tolist()