

# Entry point do programa
from enum import Enum
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Printers.ExcelPrinter import ExcelPrinter
from Types import Type
from Layout import Layout
from Stategies.AvalStrat.StratParser import StratParser

def transform_excel(config_file, input_file, output_filename):
    layout_input = Layout(True, config_file, input_file)
    
    excel_interpretor = ExcelInterpretor(layout_input)

    avaliation_strategy = StratParser(excel_interpretor)
    question_list = avaliation_strategy.parse()

    layout_output = avaliation_strategy.convert_to_layout(question_list)
    excel_printer = ExcelPrinter(layout_output)
    excel_printer.print(output_filename)

if __name__ == "__main__":
    transform_excel("./layouts/RH.json", "./exemplos/Avaliacao-Membro-RH.xlsx", "./output/Output-Avaliacao-Membro-RH.xlsx")