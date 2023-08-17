from typing import Union
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Interpretors.WordInterpretor import WordInterpretor
from Layout import Layout
from Types import Style, Type
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

    # Parte mais complexa do código todo
    def convert_to_layout(self, question_list: list[Question]) -> Layout:
        output = {"layout": []}
        final_layout = output["layout"]

        config = self.parser.get_layout()

        question_names = self.__get_questions_names(question_list)
        num_questions = len(question_names)
        
        self.__header_conversion(config, final_layout, question_names, num_questions)
        self.__content_conversion(config, final_layout, question_list, num_questions)        
        
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
                            measurer.get_name(): {}
                        })
                    if not tmp_result[measurer.get_name()].get(measured.get_name()):
                        tmp_result[measurer.get_name()].update({
                            measured.get_name(): []
                        })
                    tmp_result[measurer.get_name()][measured.get_name()].append({"grade": grade, "question": question})
        
        return tmp_result

    def __header_conversion(self, config: Layout, final_layout: list, question_names: list[str], num_questions: int):

        for leaf in config.leaf_iter("output"):
            dimentions = config.process_dimentions_of(Type(leaf["type"]), "output")
            break_line = True if leaf["type"] == Type.HEADER.name else False

            if leaf["type"] == Type.MEASURE.name:
                internal_index = 0
                for question_name in question_names:
                    self.__apply_interlaced(leaf, list(question_name)[0], self.__bind_bg_color, self.__unbind_bg_color, "CCCCCC", "FFFFFF")
                    self.__add_item_to_layout(
                        layout = final_layout, 
                        item = leaf, 
                        label=question_name,  
                        row_span= config.process_dimentions_of(Type.MEASURED, "output")["row-span"], 
                        col_span= dimentions["col-span"], 
                        break_line= internal_index == (num_questions - 1),
                    ) 
                    internal_index += 1

                self.__end_interlaced(leaf)
                continue

            if leaf["type"] == Type.HEADER.name:
                dimentions = config.process_dimentions_of(Type.HEADER, "output", self.__get_max_span(config, num_questions))
            
            self.__add_item_to_layout(
                layout = final_layout, 
                item = leaf, 
                label= self.__get_label(leaf),  
                row_span= dimentions["row-span"], 
                col_span= dimentions["col-span"], 
                break_line= break_line,
            ) 
        
    def __content_conversion(self, config: Layout, final_layout: list, question_list: list[Question], num_questions: int):

        dimentions = config.process_dimentions_of(Type.MEASURE, "output")

        # Isto configura o conteúdo
        measured_list: list[Measured] = self.__get_measured_list(question_list)
        measurer_list: list[Measurer] = measured_list[0].get_measurers()

        # Contém todas as informações configuradas nos arquivos json
        measure_leaf = config.get_type(Type.MEASURE, config.get_data("output"))[0]

        # passo intermediário, os dados estavam muito desorganizados e era dificil colocá-los no estado correto
        tmp_result = self.__organize_content(measured_list, measurer_list, question_list)

        for measurer in measurer_list:
            index = 0

            self.__add_item_to_layout(
                label= measurer.get_name(),
                layout = final_layout,
                item = measure_leaf,
                row_span= dimentions["row-span"] * len(measured_list),
                col_span= config.process_dimentions_of(Type.MEASURER, "output")["col-span"],
                major= True,
                major_span= num_questions,
            )
            
            for measured in measured_list:
                self.__add_item_to_layout(
                    label= measured.get_name(),
                    col_span= config.process_dimentions_of(Type.MEASURED, "output")["col-span"],
                    row_span= dimentions["row-span"],
                    layout = final_layout,
                    item = measure_leaf,
                    offset_col= (index != 0) * config.process_dimentions_of(Type.MEASURER, "output")["col-span"],
                )

                internal_index = 0
                for grade in tmp_result[measurer.get_name()][measured.get_name()]:
                    
                    question_number: str = grade["question"].get_question_letter(0)

                    self.__apply_interlaced(measure_leaf, question_number, self.__bind_bg_color, self.__unbind_bg_color, "DDDDDD", "FFFFFF")
                    self.__bind_border_style(measure_leaf, "thin")
                    self.__bind_border_color(measure_leaf, "AAAAAA")

                    self.__add_item_to_layout(
                        label= grade["grade"],
                        col_span= dimentions["col-span"],
                        row_span= dimentions["row-span"],
                        layout = final_layout,
                        break_line= internal_index == (num_questions - 1),
                        item = measure_leaf,
                    )

                    self.__unbind_border_style(measure_leaf)
                    self.__unbind_border_color(measure_leaf)

                    internal_index += 1

                self.__end_interlaced(measure_leaf)

                index += 1

    prev_border_style = None
    
    def __bind_border_style(self, item, value):
        self.prev_border_style = item[Style.BORDER.value[0]] if item[Style.BORDER.value[0]] else "thin"
        item[Style.BORDER.value[0]] = value

    def __unbind_border_style(self, item):
        item[Style.BORDER.value[0]] = self.prev_border_style
        self.prev_border_style = None
        

    prev_border_color = None

    def __bind_border_color(self, item, value):
        self.prev_border_color = item[Style.BORDER_COLOR.value[0]] if item[Style.BORDER_COLOR.value[0]] else "000000"
        item[Style.BORDER_COLOR.value[0]] = value

    def __unbind_border_color(self, item):
        item[Style.BORDER_COLOR.value[0]] = self.prev_border_color
        self.prev_border_color = None

    prev_bg_color = None

    def __bind_bg_color(self, item, value):
        self.prev_bg_color = item[Style.BG_COLOR.value[0]] if item[Style.BG_COLOR.value[0]] else "ffffff"
        item[Style.BG_COLOR.value[0]] = value
    
    def __unbind_bg_color(self, item):
        item[Style.BG_COLOR.value[0]] = self.prev_bg_color
        self.prev_bg_color = None

    first_content = None
    use_second_pattern = False
    unbinder = None

    def __apply_interlaced(self, item, content, binder, unbinder, value1, value2):
        unbinder(item = item)

        if not self.first_content:
            self.first_content = content            

        self.unbinder = unbinder

        if content == self.first_content:
            self.use_second_pattern = not self.use_second_pattern
        
        if self.use_second_pattern:
            binder(item = item, value = value2)
        else:
            binder(item = item, value = value1)
    
    def __end_interlaced(self, item):
        self.unbinder(item = item) if self.unbinder else None
        self.first_content = None
        self.use_second_pattern = False
        self.unbinder = None
        

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
    
    def __add_item_to_layout(self, layout, item, label, row_span, col_span, break_line = False, major = False, major_span = 0, offset_col = 0):
        layout.append({
            Style.LABEL.value[0]: label,
            Style.COL_SPAN.value[0]: col_span,
            Style.ROW_SPAN.value[0]: row_span,
            Style.MAJOR.value[0]: major,
            Style.MAJOR_SPAN.value[0]: major_span,

            Style.BG_COLOR.value[0]: self.__get_item_property(item, Style.BG_COLOR, "ffffff"),
            Style.TEXT_COLOR.value[0]: self.__get_item_property(item, Style.TEXT_COLOR, "000000"),
            Style.X_ALIGNMENT.value[0]: self.__get_item_property(item, Style.X_ALIGNMENT, "center"),
            Style.Y_ALIGNMENT.value[0]: self.__get_item_property(item, Style.Y_ALIGNMENT, "center"),
            Style.BORDER.value[0]: self.__get_item_property(item, Style.BORDER, None),
            Style.BORDER_COLOR.value[0]: self.__get_item_property(item, Style.BORDER_COLOR, "000000"),

            "offset-col": offset_col,
            "break-line": break_line,
        })

    def __get_item_property(self, item, style: Style, default_to = None):
        try:
            return item[style.value[0]]
        except:
            return default_to

    def __debug(self, measured_list: list[Measured]) -> str:
        final_str = ""
        for measured in measured_list:
            for question in measured.get_questions():
                for grade, measurer in question.get_grades():
                    final_str += f"\n\nAvaliado [{measured.get_name()}]\nAvaliador [{measurer.get_name()}]\n{question.get_question()}\nNota {grade}"
        return final_str
