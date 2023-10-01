from xlsxwriter.workbook import Worksheet
from Log.Logger import Logger
import xlsxwriter

class Dropdown:
    options: str 
    people: list[str]

    def __init__(self, people: list[str], dropdown_pos: str):
        self.people = people
        self.options = ""
        self.dropdown_pos = dropdown_pos

    def if_(self, dropdown_option: str, set_cell_to: str):
        if not self.options[dropdown_option]:
            self.logger.print_error("A opção " + dropdown_option + " não foi adicionada ao dropdown")

        option = f"=IF({self.dropdown_pos}=\"{dropdown_option}\", {set_cell_to}, \"\")" 
        prev_option = self.options

        if prev_option != "":
            self.options = f"{prev_option} & {option}"
            return

        self.options = option

    def get_options(self) -> str:
        return self.options

    def draw_dropdown(self, row, col):
        worksheet: xlsxwriter.Worksheet = Worksheet.get_worksheet_by_name(self.page_name)
        worksheet.data_validation(row, col, row, col, {"validate": "list", "source": list(self.options.keys())})

    def reset(self):
        self.options = ""
