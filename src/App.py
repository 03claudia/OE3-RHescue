

# Entry point do programa
from enum import Enum
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Types import Type
from Layout import Layout
from Stategies.AvalStrat.StratParser import StratParser


if __name__ == "__main__":
    layout = Layout(True, "./layouts/exemplo.json", "./exemplos/Avaliacao-Membro-RH.xlsx")
    
    excel_interpretor = ExcelInterpretor(layout)
    avaliation_strategies = StratParser(excel_interpretor)

    avaliation_measured_list = avaliation_strategies.parse()