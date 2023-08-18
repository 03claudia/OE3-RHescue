

# Entry point do programa
from enum import Enum
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Printers.ExcelPrinter import ExcelPrinter
from Stategies.AvalStrat.Question import Question
from Types import Type
from Config import Config
from Stategies.AvalStrat.AvaliationStrategy import AvaliationStrategy

def transform_excel(config_file, input_file, output_filename):
    layout_input = Config(read_layout_from_file=True, layout=config_file)
    excel_interpretor = ExcelInterpretor(layout_input, input_file)

    avaliation_strategy = AvaliationStrategy(excel_interpretor)
    question_list: list[Question] = avaliation_strategy.parse()
    layout_output = avaliation_strategy.convert_to_layout(question_list)

    excel_printer = ExcelPrinter(layout_output)
    excel_printer.print(output_filename)

if __name__ == "__main__":
    transform_excel(
        config_file="./layouts/RH.json", 
        input_file="./exemplos/Avaliacao-Membro-RH.xlsx", 
        output_filename="./output/Output-Avaliacao-Membro-RH.xlsx"
    )