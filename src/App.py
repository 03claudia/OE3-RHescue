# Entry point do programa
from threading import Thread
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Printers.ExcelPrinter import ExcelPrinter
from Stategies.AvalStrat.Question import Question
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
    print(f"{output_filename} criado com sucesso.")


def async_transform_excel(config_file, input_file, output_filename):
    t1 = Thread(target=transform_excel, args=(config_file, input_file, output_filename))
    t1.start()
    return t1


if __name__ == "__main__":
    rh = async_transform_excel(
        config_file="./layouts/RH.json",
        input_file="./exemplos/Avaliacao-Membro-RH.xlsx",
        output_filename="./output/Output-Avaliacao-Membro-RH.xlsx",
    )
    vpe = async_transform_excel(
        config_file="./layouts/VicePresidenteExterno.json",
        input_file="./exemplos/Avaliacao-Vice-Presidente-Externo.xlsx",
        output_filename="./output/Output-Avaliacao-VPE.xlsx",
    )
    mkt = async_transform_excel(
        config_file="./layouts/MK.json",
        input_file="./exemplos/Avaliacao-Membros-MKT.xlsx",
        output_filename="./output/Output-Avaliacao-Membro-MK.xlsx",
    )
    rh.join()
    vpe.join()
    mkt.join()
