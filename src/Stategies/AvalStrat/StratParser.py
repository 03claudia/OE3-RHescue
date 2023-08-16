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

    def convert_to_layout(self, measured_list: list[Measured]) -> Layout:
        initial_layout: Layout = self.parser.get_layout()
        type_used = "output"

        self.output = {"layout": []}
        self.output["layout"].append({"type": Type.CONTENT.name, "rows": []})
        layout = self.output["layout"][0]["rows"]
        other = self.output["layout"]

        # TODO acabar isto
        index = 0
        for element in initial_layout.leaf_iter(type_used=type_used):

            if element["type"] == Type.HEADER.name:
                title = element["label"]
                dimentions = initial_layout.process_dimentions_of(Type.HEADER, type_used=type_used)
                label = self.__get_label(element)

                # append to the beggining
                other.append({"type": Type.HEADER.name, "label": title, "col-span": dimentions["col-span"], "row-span": dimentions["row-span"]})

                continue

            elif element["type"] == Type.MEASURER.name:
                dimentions = initial_layout.process_dimentions_of(Type.MEASURER, type_used=type_used)
                label = self.__get_label(element)

                layout.append({"type": Type.MEASURER.name, "label": label, "col-span": dimentions["col-span"], "row-span": dimentions["row-span"], "rows": []})

                measurer_names: list[str] = self.__get_measurer_names(measured_list)
                layout[index]["rows"] += measurer_names
            
            elif element["type"] == Type.MEASURED.name:
                dimentions = initial_layout.process_dimentions_of(Type.MEASURED, type_used=type_used)
                label = self.__get_label(element)

                layout.append({"type": Type.MEASURED.name, "label": label, "col-span": dimentions["col-span"], "row-span": dimentions["row-span"], "rows": []})

                measured_names: list[str] = self.__get_measured_names(measured_list)
                layout[index]["rows"] += measured_names
            
            elif element["type"] == Type.MEASURE.name:
                dimentions = initial_layout.process_dimentions_of(Type.MEASURE, type_used=type_used)

                tmp_struct = dict[str, list[str]]()
                for question_name in self.__get_questions_names(measured_list):
                    tmp_struct.update({question_name: []})

                    for measured in measured_list:
                        tmp_list = measured.get_grade_and_measurer_list(question_name)

                        for grade, measurer in tmp_list:
                            tmp_struct[question_name].append({"measurer": measurer.get_name(), "measured": measured.get_name(), "grade": str(grade)})

                internal_index = 0
                for question_label in tmp_struct.keys():
                    layout.append({"type": Type.MEASURE.name, "label": question_label, "col-span": dimentions["col-span"], "row-span": dimentions["row-span"], "rows": []})

                    layout[index + internal_index]["rows"] += tmp_struct[question_label]
                    internal_index += 1
                index += internal_index - 1

            index += 1


        layout = Layout(False, "", "")
        layout.set_data_directly(self.output)
        print(self.output)
        return layout
    
    def __get_measurer_names(self, measured_list: list[Measured]) -> list[str]:
        measurer_names: list[str] = []
        for measurer in measured_list[0].get_measurers():
            measurer_names.append(measurer.get_name())
        return measurer_names
    
    def __get_measured_names(self, measured_list: list[Measured]) -> list[str]:
        measured_names: list[str] = []
        for measured in measured_list:
            measured_names.append(measured.get_name())
        return measured_names
    
    def __get_questions_names(self, measured_list: list[Measured]) -> list[str]:
        questions_names: list[str] = []
        for measured in measured_list:
            for question in measured.get_questions():
                question_label = question.get_question_without_name(self.name_divider)
                if question_label not in questions_names:
                    questions_names.append(question_label)
        return questions_names

    def __get_label(self, element) -> str:
        try:
            return element["label"]
        except:
            return "Label não definido"
        
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
