# Entry point do programa
import ntpath
import sys
from threading import Thread
from pandas.io.common import os

from streamlit import logger
from Log.Logger import Logger
from Interface.Interface import interface
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Printers.ExcelPrinter import ExcelPrinter
from Stategies.AvalStrat.Question import Question
from Config import Config
from Stategies.AvalStrat.AvaliationStrategy import AvaliationStrategy
import threading

from Stategies.ResultStrategy.Results import Results

# var global usada para bloquear threads,
# convém ser uma var global
lock = threading.Lock()

class Group:
    group_name: str
    questions: list[Question]
    def __init__(self, questions, group_name) -> None:
        self.questions = questions
        self.group_name = group_name

global_result: list[Group] = []

def transform_excel(process_name, config_file, input_file, output_sheet):
    global lock
    logger = Logger(process_name)
    logger.set_lock(lock)

    layout_input = Config(logger=logger, read_layout_from_file=True, layout=config_file)
    excel_interpretor = ExcelInterpretor(logger = logger, config=layout_input, input_file=input_file)

    logger.print_info(f"Reading {process_name}'s excel file...")

    avaliation_strategy = AvaliationStrategy(logger = logger, parser= excel_interpretor)
    question_list: list[Question] = avaliation_strategy.parse()

    logger.print_info(f"Parsing {process_name}'s excel file...")

    layout_output = avaliation_strategy.convert_to_layout(question_list)
    excel_printer = ExcelPrinter(layout = layout_output, logger = logger, page_name=output_sheet)

    # extremamente importante para quando estivermos a utilizar
    # threads
    excel_printer.set_lock(lock)
    excel_printer.print("./output/result.xlsx")

    logger.print_success(f"{output_sheet} criado com sucesso.")
    with lock:
        global global_result 
        global_result.append(Group(questions=question_list, group_name=output_sheet))

def async_transform_excel(process_name, config_file, input_file, output_sheet):
    t1 = Thread(target=transform_excel, args=(process_name, config_file, input_file, output_sheet))
    t1.start()
    return t1

# main
Logger.set_log_type(sys.argv)

# check if user wants to check some "mini-instructions"
help = [arg for arg in sys.argv if arg in ["-h", "--help"]]
if help:
    print(
    """
    Usage:
    -v, --verbose   - Display every info possible
    -d, --debug     - Used to display usefull debug information
    -i, --interface - Disable the GUI
    """
    )
    exit(0)

# check if user wants to run interface
i_active = [arg for arg in sys.argv if arg in ["-i", "-iv", "-vi", "-id", "-di", "--interface"]]
input=None

if i_active:
    input = None
else:
    input = interface()

# lê todos os ficheiros dentro da pasta /exemplos
xlsxfiles = [os.path.join(root,name) 
             for root, _, files in os.walk("exemplos")
             for name in files
             if name.endswith((".xlsx", ".xls"))]

threads_used: [] = []
for excel in xlsxfiles:
    if excel == "result.xlsx":
        continue
    filename = ntpath.basename(excel).split('.')[0]
    th = async_transform_excel(
        process_name=filename,
        config_file=f"./layouts/{filename}.json",
        input_file=excel,
        output_sheet=filename
    )
    threads_used.append(th)

for thread in threads_used:
    thread.join()

# Depois de se ter analisado todos
# os exceis, podemos criar o ralatório final
# com tudo organizado
logger = Logger("MAIN THREAD")
logger.print_info("Loading results... into result.xlsx")
final_output: Config = Results.parse(global_result)
excel_printer = ExcelPrinter(final_output, "Resultados")
excel_printer.print("./output/result.xlsx")

