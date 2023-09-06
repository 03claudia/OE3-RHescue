# Entry point do programa
import sys
from threading import Thread
from Log.Logger import Logger
from Interface.Interface import interface
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Printers.ExcelPrinter import ExcelPrinter
from Stategies.AvalStrat.Question import Question
from Config import Config
from Stategies.AvalStrat.AvaliationStrategy import AvaliationStrategy


def transform_excel(process_name, config_file, input_file, output_filename):
    logger = Logger(process_name)

    layout_input = Config(logger=logger, read_layout_from_file=True, layout=config_file)
    excel_interpretor = ExcelInterpretor(logger = logger, config=layout_input, input_file=input_file)

    logger.print_info(f"Reading {process_name}'s excel file...")

    avaliation_strategy = AvaliationStrategy(logger = logger, parser= excel_interpretor)
    question_list: list[Question] = avaliation_strategy.parse()

    logger.print_info(f"Parsing {process_name}'s excel file...")

    layout_output = avaliation_strategy.convert_to_layout(question_list)
    excel_printer = ExcelPrinter(layout = layout_output, logger = logger)
    excel_printer.print(output_filename)

    logger.print_success(f"{output_filename} criado com sucesso.")

def async_transform_excel(process_name, config_file, input_file, output_filename):
    t1 = Thread(target=transform_excel, args=(process_name, config_file, input_file, output_filename))
    t1.start()
    return t1


if __name__ == "__main__":
    Logger.set_log_type(sys.argv)

    # check if user wants to check some "mini-instructions"
    help = [arg for arg in sys.argv if arg in ["-h", "--help"]]
    if help:
        print(
        """
        Usage:
        -v, --verbose   - Display every info possible
        -d, --debug     - Used to display usefull debug information
        -i, --interface - Activate the GUI
        """
        )
        exit(0)

    # check if user wants to run interface
    i_active = [arg for arg in sys.argv if arg in ["-i", "--interface"]]
    input=None

    if not i_active:
        input = None
    else:
        input = interface()
    
    rh = async_transform_excel(
        process_name="RH",
        config_file="./layouts/RH.json",
        input_file=input[1] if input is not None else "./exemplos/Avaliacao-Membro-RH.xlsx",
        output_filename="./output/Output-Avaliacao-Membro-RH.xlsx",
    )
    vpe = async_transform_excel(
        process_name="VPE",
        config_file="./layouts/VicePresidenteExterno.json",
        input_file=input[2] if input is not None else "./exemplos/Avaliacao-Vice-Presidente-Externo.xlsx",
        output_filename="./output/Output-Avaliacao-VPE.xlsx",
    )
    mkt = async_transform_excel(
        process_name="MK",
        config_file="./layouts/MK.json",
        input_file=input[0] if input is not None else "./exemplos/Avaliacao-Membros-MKT.xlsx",
        output_filename="./output/Output-Avaliacao-Membro-MK.xlsx",
     
    )
    rh.join()
    vpe.join()
    mkt.join() 
