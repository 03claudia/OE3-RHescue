

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

    avaliation_strategies = StratParser(excel_interpretor)
    avaliation_measured_list = avaliation_strategies.parse()

    # por acaso é o mesmo layout
    layout_output = avaliation_strategies.get_output_layout("Titulo qualquer", avaliation_measured_list)

    excel_printer = ExcelPrinter(layout_output)
    excel_printer.print("./output/Output-Avaliacao-Membro-RH.xlsx")

