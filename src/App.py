

# Entry point do programa
from enum import Enum
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Printers.ExcelPrinter import ExcelPrinter
from Types import Type
from Layout import Layout
from Stategies.AvalStrat.StratParser import StratParser


if __name__ == "__main__":
    layout_input = Layout(True, "./layouts/exemplo_input.json", "./exemplos/Avaliacao-Membro-RH.xlsx")
    
    excel_interpretor = ExcelInterpretor(layout_input)

    avaliation_strategy = StratParser(excel_interpretor)
    question_list = avaliation_strategy.parse()

    for aval in question_list:
        print(aval)

    layout_output = avaliation_strategy.convert_to_layout(question_list)

    """ # por acaso é o mesmo layout
    

    excel_printer = ExcelPrinter(layout_output)
    excel_printer.print("./output/Output-Avaliacao-Membro-RH.xlsx") """

