# Entry point do programa
import shutil
import streamlit as st
import ntpath
import sys
from threading import Thread
from pandas.io.common import os
from Interface.File import File

from Log.Logger import Logger
from Interface.Interface import interface
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Printers.ExcelPrinter import ExcelPrinter
from Stategies.AvalStrat.Question import Question
from Config import Config
from Stategies.AvalStrat.AvaliationStrategy import AvaliationStrategy
import threading

from Stategies.ResultStrategy.Results import Results
from Types import Type

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

def transform_excel(process_name, config_file, input_file, output_sheet, is_config_file = True):
    global lock
    logger = Logger(process_name)
    logger.set_lock(lock)

    layout_input = Config(logger=logger, read_layout_from_file=is_config_file, layout=config_file) 

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
        # preciso de saber o tipo de ficheiro que estamos a ler, se é av mensal, anual, etc...

    group_name: str = ""
    try:
        group_name= layout_input.get_type(Type.AVALTYPE)[0]['label']
    except:
        # Caso este erro ocorra, fiquem a saber que só impossibilita que os resultados
        # sejam processados corretamente, mas claro, recomendo que acrescentem
        # {"type": "AVAL_TYPE", "label": "..."} nas configurações
        logger.print_critical_error(f"No avaliation type provided for {process_name}.json, use \"type\":\"AVALTYPE\"")

    with lock:
        global global_result 
        global_result.append(Group(questions=question_list, group_name=group_name))

def async_transform_excel(process_name, config_file, input_file, output_sheet, is_config_file = True):
    t1 = Thread(target=transform_excel, args=(process_name, config_file, input_file, output_sheet, is_config_file))
    t1.start()
    return t1

def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # Save the file to a local directory
        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        return file_path
    return None

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

xlsxfiles= None
if i_active:
    input = None
    # lê todos os ficheiros dentro da pasta /exemplos
    xlsxfiles = [os.path.join(root,name) 
                for root, _, files in os.walk("exemplos")
                for name in files
                if name.endswith((".xlsx", ".xls"))]
        
else:
    xlsxfiles = interface()


if os.path.exists("./output"):
    shutil.rmtree("./output", ignore_errors=True)

# esvaziar todos os logos sempre que existe um
# re-run do programa
Logger.all_logs = []

threads_used: [] = []

if xlsxfiles is not None:
    if i_active:
        for excel in xlsxfiles:

            if excel == "result.xlsx":
                continue
            
            filename = ntpath.basename(excel).split('.')[0] if i_active else excel.name.split('.')[0]
            th = async_transform_excel(
                process_name=filename,
                config_file=f"./layouts/{filename}.json",
                input_file=excel,
                output_sheet=filename
            )
            threads_used.append(th)
    else:
        for file in xlsxfiles:
            if file.active == False or file.file is None:
                continue

            excel: File = file
            
            st.success(f"Processando {excel.page_name}...")
            file_path = save_uploaded_file(excel.file)
            
            th = async_transform_excel(
                process_name=excel.page_name,
                config_file=excel.config,
                input_file=file_path,
                output_sheet=excel.page_name,
                is_config_file=False
            )
            threads_used.append(th)

    progress_text = "A processar os ficheiros. Por favor, aguarde."
    percent_complete = 0
    my_bar = st.progress(0, text=progress_text)


    for thread in threads_used:
        my_bar.progress(percent_complete + 15, text=progress_text)
        thread.join()

    my_bar.progress(percent_complete + 50, text=progress_text)

    # Depois de se ter analisado todos
    # os exceis, podemos criar o ralatório final
    # com tudo organizado
    logger = Logger("MAIN THREAD")
    logger.print_info("Loading results... into result.xlsx")

    result = Results(global_result)

    # Processa os resultados das avalicações mensais
    # nada está a ser desenhado!!! apenas processado
    result.process_av_des_mensal("./output/result.xlsx", lock)

    result.draw_dropdown("./output/result.xlsx")

    prograss_text = "A processar os resultados. Por favor, aguarde."
    my_bar.progress(percent_complete + 100, text=progress_text)

    if not i_active:
        st.title("Resultados prontos")
        st.code("\n".join(Logger.all_logs))
        
            # Assuming your Excel file is located at './output/result.xlsx'
        excel_file_path = "./output/result.xlsx"
        with open("./output/result.xlsx", "rb") as file:
            # Create a download button for the Excel file
            st.download_button(
                label="Download Excel workbook",
                data=file,
                file_name="result.xlsx",
                key="download_button"
            )

    my_bar.empty()
