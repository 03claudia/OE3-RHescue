import random
from Config import Config
from Log.Logger import Logger
from Stategies.AvalStrat.Measured import Measured
from Stategies.AvalStrat.StyleBinder import StyleBinder
from Stategies.ResultStrategy.Dropdown import Dropdown
import xlsxwriter

from Types import Style, Type
# CUIDADO COM OS NOMES DOS FICHEIROS
class Results:

    data:list['Group']
    measured: list['Measured']
    dropdown: Dropdown
    logger: Logger
    final_layout: [str] 
    all_people: list[Measured]

    def __init__(self, data: list['Group'], logger = Logger("")) -> Config:
        # todo
        self.data = data
        self.logger = logger
        workbook = xlsxwriter.Workbook("output/result.xlsx")

        # presuposto, aqui o programa pode partir 
        all_people_names = []
        for group in self.data:
            for question in group.questions:
                for _, measured, _ in question.get_grades():
                    if measured not in all_people_names:
                        all_people_names.append(measured.get_name())
                        self.all_people.append(measured)

        self.dropdown = Dropdown(workbook, all_people_names, "A1")
        self.final_layout = []


    def convert_xy_to_excel(self, x: int, y: int) -> str:
        return f"{chr(x)}{y}"

    # nome do excel tem de comecar com "gen_m"
    def process_av_des_mensal(self):
        
        for group in self.data:
            filename = group.group_name
            if "gen_m" not in filename:
                continue

            for question in group.questions:
                for grade, measured, measurer in question.get_grades():
                    self.dropdown.add_condition_to(measured.get_name(), grade, ) 
                    pass

                # self.__add_item_to_layout(
                #     id = 0,
                #     label= note,
                #     col_span= 1,
                #     row_span= , # if not is_observation else config.process_dimentions_of(Type.MEASURER, "output")["col-span"],
                #     end_result = self.final_layout,
                #     break_line= internal_index == (num_questions - 1),
                #     item = measure_leaf,
                #     style_list=[border_style_binder, border_color_binder],
                #     major = is_observation,
                #     major_span= len(measured_list),
                # )


    # nome do excel tem de comecar com "gen_s"
    def process_av_des_sem(self):
        pass

    # nome do excel tem de comecar com "mem_proj_<nome do projeto>"
    def process_av_sem_mem_proj(self):
        pass

    # nome do excel tem de comecar com "pm_proj_<nome do projeto>"
    def process_av_sem_pm_proj(self):
        pass
        
    # nome do excel tem de comecar com "coord_proj_<nome do projeto>"
    def process_av_sem_coord_proj(self):
        pass

    def __get_max_span(self, config: Config, n_questions: int, property: str = "col-span") -> int:
        measured_col_span = config.process_dimentions_of(Type.MEASURED, "output")[property]
        measurer_col_span = config.process_dimentions_of(Type.MEASURER, "output")[property]
        question_col_span = config.process_dimentions_of(Type.MEASURE, "output")[property] * n_questions
        
        return measured_col_span + measurer_col_span + question_col_span
    
    def __add_item_to_layout(self, end_result: list, item: dict, label: str, row_span: int, col_span: int, break_line: bool = False, major: bool = False, major_span: int = 0, offset_col: int = 0, style_list: list[StyleBinder] = [], id: int = random.randrange(0x666666, 0xFFFFFF)):

        if len(style_list) > 0:
            for style in style_list:
                style.bind(item)
            
        end_result.append({
            Style.ID.value[0]: id,
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

        if len(style_list) > 0:
            for style in style_list:
                style.unbind(item)

