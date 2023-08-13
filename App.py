

# Entry point do programa
from enum import Enum
from ExcelParser import ExcelParser
from Types import Type
from Layout import Layout


if __name__ == "__main__":
    layout = Layout(True, "./layouts/exemplo.json", "./exemplos/Avaliacao-Membro-RH.xlsx")
    excel_parser = ExcelParser(layout)

    excel_parser.parse()