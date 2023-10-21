import random
from Config import Config
from Log.Logger import Logger
from Printers.ExcelPrinter import ExcelPrinter
from Stategies.AvalStrat.Measured import Measured
from Stategies.AvalStrat.Question import Question
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
                    if measured.get_name() not in all_people_names:
                        all_people_names.append(measured.get_name())

        self.dropdown = Dropdown(all_people_names, "A1")
        self.final_layout = []


    def convert_xy_to_excel(self, x: int, y: int) -> str:
        return f"{chr(x)}{y}"

    def _get_num_of_non_obs_questions(self, questions: list):
        num = 0
        for question in questions:
            if not question.is_observation():
                num += 1
        return num
    
    def _filter_obs_questions(self, questions: list):
        return [question for question in questions if not question.is_observation()]
    
    def _get_groups_by_name(self, name: str) -> list['Group']:
        av_mensal_groups = []
        for group in self.data:
            gn = group.group_name
            if name not in gn:
                continue

            av_mensal_groups.append(group)
        return av_mensal_groups
    

    def _process_questions_headings(self, questions: list[Question], num_of_questions, styles):
        index = num_of_questions
        tmp_item_changed = None 
        for question in self._filter_obs_questions(questions):
            if question.is_observation():
                # skip observations...
                if index == 1:
                    if tmp_item_changed is not None:
                        tmp_item_changed["break-line"] = False
                    # if the last question is an
                    # observation, the last item needs to break
                    last_item = self.final_layout[-1]
                    last_item["break-line"] = True
                    tmp_item_changed = last_item
                index -= 1
                continue
            q: Question = question

            # draw the questions
            self.__add_item_to_layout(
                id = index,
                label= q.get_question(),
                col_span= 1,
                row_span= 1, 
                end_result = self.final_layout,
                break_line= (index == 1),
                item = {
                    "border": "thin",
                    "border-color": "000000",
                    },
                style_list=styles,
                major = False,
                major_span= False,
            )
            index -= 1

    def _process_medias(self, num_of_questions: int, questions: list["Question"]):
            index = num_of_questions
            medias_by_person_by_question = {} 

            for question in self._filter_obs_questions(questions):

                median_dict: dict[str, float] = {}
                for person in self.dropdown.people:
                    median_dict[person] = {"median": 0, "n_aval": 1}

                for grade, measured, _ in question.get_grades():
                    if type(grade) == str:
                        continue
                    median_dict[measured.get_name()]["median"] += grade
                    median_dict[measured.get_name()]["n_aval"] += 1

                for person in median_dict.keys():
                    median = median_dict[person]["median"] / median_dict[person]["n_aval"]
                    if median == 0:
                        median = "-"

                    self.dropdown.if_(dropdown_option=person, set_cell_to=(median))   

                medias_by_person_by_question[question.get_question()] = median_dict

                # Draw media of the grades 
                self.__add_item_to_layout(
                    id = index,
                    label= self.dropdown.get_options(),
                    col_span= 1,
                    row_span= 1, # if not is_observation else config.process_dimentions_of(Type.MEASURER, "output")["col-span"],
                    end_result = self.final_layout,
                    break_line= (bool)(index == 1),
                    item = {
                        "border": "thin",
                        "border-color": "000000",
                        },
                    style_list=[],
                    major = False,
                    major_span= False,
                )
                self.dropdown.reset()
                index -= 1

            return medias_by_person_by_question

                


    def _add_title(self, title: str, num_of_questions: int, styles):
        self.__add_item_to_layout(
            id = 0,
            label= title, 
            col_span= num_of_questions,
            row_span= 1, 
            end_result = self.final_layout,
            break_line= True,
            item = {
                    "border": "thin",
                    "border-color": "000000",
                    "bg-color": "cccccc"
                },
            style_list= styles,
            major = False,
            major_span= False,
        )

    def _process_total_media(self, medias_by_person_by_question, styles, num_of_questions):
        # "person": {
        #   "sum": total_sum,
        #   "n_question": total_questions
        # }
        person_total_media = {} 

        # init this data structure
        for person in self.dropdown.people:
            person_total_media[person] = {"sum": 0, "n_question": 0}

        for question in medias_by_person_by_question.keys():
            for person in medias_by_person_by_question[question]:
                singular_media = medias_by_person_by_question[question][person]["median"] / medias_by_person_by_question[question][person]["n_aval"]
                if singular_media != "-":
                    person_total_media[person]["sum"] += singular_media
                    person_total_media[person]["n_question"] += 1 

        for person in person_total_media.keys():
            self.logger.print_info(f"P: {person} -> {person_total_media[person]}")
            # Desenhar a media final da pessoa
            self.dropdown.if_(dropdown_option=person, set_cell_to=(person_total_media[person]["sum"] / person_total_media[person]["n_question"]))   

        self.__add_item_to_layout(
            id = 0,
            label= self.dropdown.get_options(),
            col_span= num_of_questions,
            row_span= 1, # if not is_observation else config.process_dimentions_of(Type.MEASURER, "output")["col-span"],
            end_result = self.final_layout,
            break_line= True,
            item = {
                "border": "thin",
                "border-color": "000000",
                },
            style_list= styles,
            major = False,
            major_span= False,
        )
        self.dropdown.reset()



    def process_av_des_mensal(self, final_path, lock):
        # nome do excel tem de comecar com "gen_m"
        GROUP_ID:str = "gen_m"

        border_style_binder = StyleBinder(Style.BORDER, self.__get_item_property({}, Style.BORDER, "thin"))
        border_color_binder = StyleBinder(Style.BORDER_COLOR, self.__get_item_property({}, Style.BORDER_COLOR, "000000"))
                    
        av_mensal_groups = self._get_groups_by_name(GROUP_ID)
        medias_by_person_by_questions = None

        for group in av_mensal_groups:
            num_of_questions= self._get_num_of_non_obs_questions(group.questions)
            # usado para dar skip às observações
            self._add_title("Avaliação Mensal", num_of_questions, [border_style_binder, border_color_binder])
            self._process_questions_headings(group.questions, num_of_questions, [border_style_binder, border_color_binder])
            medias_by_person_by_questions = self._process_medias(num_of_questions, group.questions)
            self._process_total_media(medias_by_person_by_questions, [border_style_binder, border_color_binder], num_of_questions)

            config = self.get_config()
            printer: ExcelPrinter = ExcelPrinter(config, "resultado")
            printer.set_lock(lock)

            # desenha cada grupo separadamente
            self.draw_results(printer, final_path)
            self.final_layout = []


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

    def draw_dropdown(self, filepath: str):
        self.dropdown.draw_dropdown(filepath)

    def draw_results(self, excel_printer: ExcelPrinter, filepath: str):
        excel_printer.print(filepath)

    def get_config(self) -> Config:
        self.final_layout.append({"num-columns": 40})
        final = {"layout": self.final_layout}
        config: Config = Config(False, final)
        return config

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

    def __get_item_property(self, item, style: Style, default_to = None):
        try:
            return item[style.value[0]]
        except:
            return default_to

