

from typing import Union
from Measured import Measured
from Measurer import Measurer
from Question import Question
from Types import Type
from Layout import Layout
import pandas as pd

class ExcelParser:
    def __init__(self, layout: Layout) -> None:
        self.layout = layout
        self.target_file = self.__read_excel()
    
    def parse(self):
        self.result: list = []

        # Pega em todas as perguntas do layout
        questions = self.layout.get_type(Type.QUESTIONS)[0]["questions"]

        question_list: list = []
        for question in questions:
            columns: list[tuple] = self.__find_index_and_value_of_column(question["label"])
            for column in columns:
                question_list.append(Question(column[0], column[1]))

        # Pega em todos os avaliadores
        measurer_label = self.layout.get_type(Type.MEASURER)[0]
        measurer_index: int = self.__find_index_and_value_of_column(measurer_label["label"])
        measurers = self.__get_column_values(measurer_index[0])

        measurers_list: list[Measurer] = []
        for measurer in measurers:
            measurers_list.append(Measurer(measurer[1], measurer[0]))
        
        measured_names = self.layout.get_type(Type.MEASURED)[0]["names"]
        
        measured_list: list[Measured] = []
        for measured_name in measured_names:
            measured_list.append(Measured(measured_name, question_list.copy()))

        for measured in measured_list:
            for measurer in measurers_list:
                measurer.evaluated_with(measured, self.target_file)
             
        for measured in measured_list:
            for question in measured.get_questions():
                for grade, measurer in question.get_grades():
                    print(f"\n\nAvaliado [{measured.get_name()}]\nAvaliador [{measurer.get_name()}]\n{question.get_question()}\nNota {grade}")

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
        
    
    def __find_index_and_value_of_column(self, label: str) -> Union[list, int]:
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

    def __get_column_values(self, index: int) -> list:
        values = self.target_file.iloc[:, index].values.tolist()
        indexes = [i for i in range(len(values))]
        return list(zip(indexes, values))    