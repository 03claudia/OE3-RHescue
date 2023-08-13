
from typing import Union

from Interpretors.ExcelInterpretor import ExcelInterpretor
from Interpretors.WordInterpretor import WordInterpretor
from Types import Type
from Stategies.AvalStrat.Measured import Measured
from Stategies.AvalStrat.Measurer import Measurer
from Stategies.AvalStrat.Question import Question


class StratParser:
    def __init__(self, parser: Union[ExcelInterpretor, WordInterpretor]):
        self.parser = parser

    def parse(self) -> list[Measured]:
        self.result: list = []

        parser = self.parser
        layout = self.parser.get_layout()
        file = self.parser.get_target_file()

        # Pega em todas as perguntas do layout
        questions = layout.get_type(Type.QUESTIONS)[0]["questions"]

        question_list: list = []
        for question in questions:
            columns: list[tuple] = parser.find_index_and_value_of_column(question["label"])
            for column in columns:
                question_list.append(Question(column[0], column[1]))

        # Pega em todos os avaliadores
        measurer_label = layout.get_type(Type.MEASURER)[0]
        measurer_index: int = parser.find_index_and_value_of_column(measurer_label["label"])
        measurers = parser.get_column_values(measurer_index[0])

        measurers_list: list[Measurer] = []
        for measurer in measurers:
            measurers_list.append(Measurer(measurer[1], measurer[0]))
        
        measured_names = layout.get_type(Type.MEASURED)[0]["names"]
        
        measured_list: list[Measured] = []
        for measured_name in measured_names:
            measured_list.append(Measured(measured_name, question_list.copy()))

        for measured in measured_list:
            for measurer in measurers_list:
                measurer.evaluated_with(measured, file)
             
        for measured in measured_list:
            for question in measured.get_questions():
                for grade, measurer in question.get_grades():
                    print(f"\n\nAvaliado [{measured.get_name()}]\nAvaliador [{measurer.get_name()}]\n{question.get_question()}\nNota {grade}")
        
        return measured_list