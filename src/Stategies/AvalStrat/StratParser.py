"""
{
    "layout": [
        { 
            "type": "HEADER",
            "label": "Avaliação Semestral dos Membros de RH"
            "row-span": 1,
            "col-span": full,
        },
        { 
            "type": "CONTENT",
            "rows": [
                { 
                    "type": "MEASURER",
                    "label": "Avaliador",
                    "row-span": 2,
                    "rows": [
                        "Inês Geraldes", "Inês Bastos", "Cláudia Santos"
                    ]
                },
                {
                    "type": "MEASURED",
                    "label": "Avaliado",
                    "row-span": 1,
                    "rows": [
                        "Inês Geraldes", "Inês Bastos", "Cláudia Santos"
                    ]
                },
                {
                    "type": "MEASURE",
                    "label": "1. O membro conseguiu alcançar os objetivos, estabelecidos a priori, das tarefas pelas quais foi responsável.",
                    "row-span": 1,
                    "rows": [
                        {
                            "measurer": "Inês Geraldes",
                            "measured": "Inês Geraldes",
                            "grade": 6
                        },
                        {
                            "measurer": "Inês Geraldes",
                            "measured": "Inês Geraldes",
                            "grade": 6
                        },
                        {
                            "measurer": "Inês Geraldes",
                            "measured": "Inês Geraldes",
                            "grade": 6
                        },
                    ]
                }
                ...
            ]
        }
    ]
}
"""

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
        layout.append({"type": Type.HEADER.name, "label": title, "row-span": 1, "col-span": "full"})
        layout.append({"type": Type.CONTENT.name, "rows": []})

        measured_names: list[str] = []
        for measured in measured_list:
            measured_names.append(measured.get_name())

        layout[1]["rows"].append({"type": Type.MEASURED.name, "label": "Avaliado", "row-span": 1, "rows": measured_names})

        measurer_names: list[str] = []
        measurer_list = measured_list[0].get_measurers()

        for measurer in measurer_list:
            measurer_names.append(measurer.get_name())   

        layout[1]["rows"].append({"type": Type.MEASURER.name, "label": "Avaliador", "row-span": 2, "rows": measurer_names})

        # preciso de organizar melhor este codigo
        mapper = dict[str, list[str]]()
        for measured in measured_list:
            for question in measured.get_questions():

                question_label = question.get_question_without_name(self.name_divider)
                if  question_label not in mapper.keys():
                    mapper.update({question.get_question_without_name(self.name_divider): []})

                for grade, measurer in question.get_grades():
                    mapper[question_label].append({"measurer": measurer.get_name(), "measured": measured.get_name(), "grade": str(grade)})
        
        for key in mapper.keys():
            layout[1]["rows"].append({"type": Type.MEASURE.name, "label": key, "row-span": 1, "rows": mapper[key]})


        layout = Layout(False, "", "")
        layout.set_data_directly(self.output)
        return layout
                
        
