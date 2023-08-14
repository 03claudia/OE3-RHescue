from typing import Union
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Interpretors.WordInterpretor import WordInterpretor
from Layout import Layout
from Types import Type
from Stategies.AvalStrat.Measured import Measured
from Stategies.AvalStrat.Measurer import Measurer
from Stategies.AvalStrat.Question import Question


class StratParser:
    def __init__(self, parser: Union[ExcelInterpretor, WordInterpretor], name_divider: str = "[") -> None:
        self.parser = parser
        self.name_divider = name_divider

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

        # print(self.__debug(measured_list))

        return list(measured_list)

    def get_output_layout(self, title: str, measured_list: list[Measured]) -> Layout:
        self.output = {"layout": []}
        layout = self.output["layout"]

        # definir um titulo
        layout.append({"type": Type.HEADER, "label": title, "row-span": 1, "col-span": "full"})
        layout.append({"type": Type.CONTENT, "rows": []})

        measured_names: list[str] = []
        for measured in measured_list:
            measured_names.append(measured.get_name())

        layout[1]["rows"].append({"type": Type.MEASURED, "label": "Avaliado", "row-span": 1, "rows": measured_names})

        measurer_names: list[str] = []
        measurer_list = measured_list[0].get_measurers()

        for measurer in measurer_list:
            measurer_names.append(measurer.get_name())   

        layout[1]["rows"].append({"type": Type.MEASURER, "label": "Avaliador", "row-span": 2, "rows": measurer_names})

        # preciso de organizar melhor este codigo
        question_label_list: list[str] = []
        for question in self.__get_all_questions(measured_list):
            if question.get_question_without_name(self.name_divider) not in question_label_list:
                layout[1]["rows"].append({"type": Type.MEASURE, "label": question.get_question_without_name(self.name_divider), "row-span": 1, "rows": []})
                question_label_list.append(question.get_question_without_name(self.name_divider))
            for grade, measurer in question.get_grades():
                layout[1]["rows"][-1]["rows"].append({"measurer": measurer.get_name(), "measured": measured.get_name(), "grade": grade})

        layout = Layout(False, "", "")
        layout.set_data_directly(self.output)
        return layout

    def __get_all_questions(self, list: list[Measured]) -> list[Question]:
        questions: list[Question] = []
        for measured in list:
            for question in measured.get_questions():
                questions.append(question)
        return questions
                
        
