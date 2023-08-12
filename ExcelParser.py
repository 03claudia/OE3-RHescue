

from Measured import Measured
from Measurer import Measurer
from Question import Question
from Types import Type
from layout import Layout
import pandas as pd

class ExcelParser:
    def __init__(self, layout: Layout) -> None:
        self.layout = layout
        self.target_file = self.__read_excel()
    
    def parse(self):
        self.result: list = []

        # Pega em todas as perguntas do layout
        questions = self.layout.get_type(Type.QUESTIONS)[0]["questions"]

        questions_index_list: list = []
        for question in questions:
            questions_index_list.append(self.__find_index_of_column(question["label"]))

        question_list: list[Question] = []
        for question in questions_index_list:
            question_list.append(Question(question[0], question[1]))
        

        # Pega em todos os avaliadores
        measurer_label = self.layout.get_type(Type.MEASURER)[0]
        measurer_index = self.__find_index_of_column(measurer_label["label"])
        measurers = self.__get_column_values(measurer_index[0])

        measurers_list: list[Measurer] = []
        for measurer in measurers:
            measurers_list.append(Measurer(measurer[1], measurer[0]))
        
        measured_names = self.layout.get_type(Type.MEASURED)[0]["names"]
        measured_list: list[Measured] = []
        for measured in measured_names:
            measured_list.append(Measured(measured, question_list))
             
        # Cria as perguntas todas



        self.__process_questions(questions, measurer)



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

    def __process_questions(self, questions: list, measurer: list) -> list:
        for question in questions:
            print(self.__find_index_of_column(question["label"]))
        
    
    def __find_index_of_column(self, label: str) -> list | int:
        label_to_find = label

        matching_columns = [col for col in self.target_file.columns if label_to_find.lower() in col.lower()]

        result = []
        if matching_columns:
            for col_name in matching_columns:
                col_index = self.target_file.columns.get_loc(col_name)
                result.append((col_index, col_name))
        else:
            print(f"No column matching label '{label_to_find}' found.")
        
        if len(result) == 1:
            return result[0]
        
        return result

    def __get_column_values(self, index: int) -> list:
        values = self.target_file.iloc[:, index].values.tolist()
        indexes = [i for i in range(len(values))]
        return list(zip(indexes, values))
    
    def __get_questions_index_of_measured(self, measured: str) -> list:
        pass        