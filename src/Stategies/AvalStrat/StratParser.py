from typing import Union
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Interpretors.WordInterpretor import WordInterpretor
from Types import Type
from Stategies.AvalStrat.Measured import Measured
from Stategies.AvalStrat.Measurer import Measurer
from Stategies.AvalStrat.Question import Question


class StratParser:
    question_list: list[Question] = []
    measurer_list: list[Measurer] = []
    measured_list: list[Measured] = []

    def __init__(self, parser: Union[ExcelInterpretor, WordInterpretor]):
        self.parser = parser

    def __get_questions(self, questions_in_layout) -> list[Question]:
        question_list: list = []
        for question in questions_in_layout:
            columns: list[tuple] = self.parser.find_index_and_value_of_column(question["label"])
            for column in columns:
                question_list.append(Question(column[0], column[1]))
        
        return question_list

    def __get_measurers(self, measurers_in_layout) -> list[Measurer]:
        measurer_index: int = self.parser.find_index_and_value_of_column(measurers_in_layout["label"])
        measurers = self.parser.get_column_values(measurer_index[0])

        measurers_list: list[Measurer] = []
        for measurer in measurers:
            measurers_list.append(Measurer(measurer[1], measurer[0]))

        return measurers_list

    def __get_measured(self, measured_names_in_layout, question_list: list[Question]) -> list[Measured]:
        measured_list: list[Measured] = []
        for measured_name in measured_names_in_layout:
            measured_list.append(Measured(measured_name, question_list.copy()))
        return measured_list

    def __debug(self, measured_list: list[Measured]) -> str:
        final_str = ""
        for measured in measured_list:
            for question in measured.get_questions():
                for grade, measurer in question.get_grades():
                    final_str += f"\n\nAvaliado [{measured.get_name()}]\nAvaliador [{measurer.get_name()}]\n{question.get_question()}\nNota {grade}"
        return final_str


    def parse(self) -> list[Measured]:
        self.result: list = []
        layout = self.parser.get_layout()
        file = self.parser.get_target_file()

        # Pega em todas as perguntas do layout
        questions = layout.get_type(Type.QUESTIONS)[0]["questions"]
        question_list: list[Question] = self.__get_questions(questions)

        # Pega em todos os avaliadores
        measurer_label = layout.get_type(Type.MEASURER)[0]
        measurer_list: list[Measurer] = self.__get_measurers(measurer_label)
        
        # Pega em todos os avaliados
        measured_names = layout.get_type(Type.MEASURED)[0]["names"]
        measured_list: list[Measured] = self.__get_measured(measured_names, question_list)

        # Avalia cada avaliado com cada avaliador
        # e guarda o resultado no próprio avaliado
        for measured in measured_list:
            for measurer in measurer_list:
                measurer.evaluate(measured, file)

        print(self.__debug(measured_list))

        return list(measured_list)