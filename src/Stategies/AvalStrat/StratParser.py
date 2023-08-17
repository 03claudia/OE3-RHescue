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

    # depende bastante de excel para excel e do que queremos fazer com o excel
    def parse(self) -> list[Question]:
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
        for measurer in measurer_list:
            for measured in measured_list:    
                measurer.evaluate(measured, file)

        # print(self.__debug(measured_list))
        result = Question.mix_questions(question_list)
        return Question.mix_questions(question_list)

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
            measured_list.append(Measured(measured_name, question_list))
        return measured_list

    """
    [
        {
            "label": "titulo",
            "row-span": 1,
            "col-span": 1,
        },
        {
            "label": "titulo",
            "row-span": 1,
            "col-span": 1,
        }
    ]
    """

    def convert_to_layout(self, question_list: list[Question]) -> Layout:
        output = {"layout": []}
        final_layout = output["layout"]

        config = self.parser.get_layout()

        question_names = self.__get_questions_names(question_list)
        num_questions = len(question_names)
        
        # Isto só configura os headers
        for leaf in config.leaf_iter("output"):
            dimentions = config.process_dimentions_of(Type(leaf["type"]), "output")
            break_line = True if leaf["type"] == Type.HEADER.name else False

            if leaf["type"] == Type.MEASURE.name:
                internal_index = 0
                for question_name in question_names:
                    final_layout.append({
                        "label": question_name,
                        "col-span": dimentions["col-span"],
                        "row-span": dimentions["row-span"],
                        "break-line": internal_index == (num_questions - 1),
                        "major": False
                    })
                    internal_index += 1
                continue

            if leaf["type"] == Type.HEADER.name:
                dimentions = config.process_dimentions_of(Type.HEADER, "output", self.__get_max_span(config, num_questions))
            
            final_layout.append({
                    "label": self.__get_label(leaf),
                    "col-span": dimentions["col-span"],
                    "row-span": dimentions["row-span"],
                    "break-line": break_line,
                    "major": False
            })

        dimentions = config.process_dimentions_of(Type.MEASURE, "output")

        # Isto configura o conteúdo
        measured_list: list[Measured] = self.__get_measured_list(question_list)
        measurer_list: list[Measurer] = measured_list[0].get_measurers()

        # passo intermediário, os dados estavam muito desorganizados e era dificil colocá-los no estado correto
        tmp_result = self.__organize_content(measured_list, measurer_list, question_list)

        for measurer in measurer_list:
            index = 0
            final_layout.append({
                "label": measurer.get_name(),
                "col-span": config.process_dimentions_of(Type.MEASURER, "output")["col-span"],
                "row-span": dimentions["row-span"] * num_questions,
                "break-line": False,
                "major": True,
                "major-span": num_questions,
            })
            
            for measured in measured_list:
                
                final_layout.append({
                    "label": measured.get_name(),
                    "col-span": config.process_dimentions_of(Type.MEASURED, "output")["col-span"],
                    "row-span": dimentions["row-span"],
                    "break-line": False,
                    "offset-col": index != 0,
                    "major": False,
                })
                internal_index = 0
                for grade in tmp_result[measurer.get_name()][measured.get_name()]:
                    final_layout.append({
                        "label": grade,
                        "col-span": dimentions["col-span"],
                        "row-span": dimentions["row-span"],
                        "break-line": internal_index == (num_questions - 1),
                        "major": False
                    })
                    internal_index += 1
                index += 1
        
        print(output)
        result = Layout(False, "", "")
        result.set_data_directly(output)
        return result

    def __organize_content(self, measured_list: list[Measured], measurer_list: list[Measurer], question_list: list[Question]) -> dict[str: dict[str: list[int]]]:
        # passo intermediario
        tmp_result = {}

        for measurer in measurer_list:
            for question in question_list:
                for grade, measured in question.get_grade_by_measurer(measurer):
                    if not tmp_result.get(measurer.get_name()):
                        tmp_result.update({
                            measurer.get_name(): {
                                
                            }
                        })
                    if not tmp_result[measurer.get_name()].get(measured.get_name()):
                        tmp_result[measurer.get_name()].update({
                            measured.get_name(): []
                        })
                    tmp_result[measurer.get_name()][measured.get_name()].append(grade)
        
        return tmp_result


    def __get_measured_list(self, question_list: list[Measured]) -> list[Measured]:
        measured_list: list[Measured] = []
        for question in question_list:
            for _, measured, _ in question.get_grades():
                if measured not in measured_list:
                    measured_list.append(measured)
        return measured_list
    
    def __get_questions_names(self, question_list: list[Question]) -> list[str]:
        questions_names: list[str] = []
        for question in question_list:
            question_label = question.get_question_without_name(self.name_divider)
            if question_label not in questions_names:
                questions_names.append(question_label)
        return questions_names

    def __get_label(self, element) -> str:
        try:
            return element["label"]
        except:
            return "Label não definido"
        
    def __get_max_span(self, config, n_questions, property = "col-span") -> int:
        measured_col_span = config.process_dimentions_of(Type.MEASURED, "output")[property]
        measurer_col_span = config.process_dimentions_of(Type.MEASURER, "output")[property]
        question_col_span = config.process_dimentions_of(Type.MEASURE, "output")[property] * n_questions
        
        return measured_col_span + measurer_col_span + question_col_span
    

    def __debug(self, measured_list: list[Measured]) -> str:
        final_str = ""
        for measured in measured_list:
            for question in measured.get_questions():
                for grade, measurer in question.get_grades():
                    final_str += f"\n\nAvaliado [{measured.get_name()}]\nAvaliador [{measurer.get_name()}]\n{question.get_question()}\nNota {grade}"
        return final_str
