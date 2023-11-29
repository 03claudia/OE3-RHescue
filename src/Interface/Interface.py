from Config import Config
from Interface.File import File
from Interface.Pages import Pages
import streamlit as st
import os
import json
from st_material_table import st_material_table
import pandas as pd
from io import StringIO
import streamlit as st


Av_Mensal=['Avaliacao-Membros-MKT','Avaliacao-Membro-RH']
Av_Trimestral=[]
Av_Projeto=[]
Av_Direcao=['Avaliacao-Vice-Presidente-Externo']


def add_new_page(saved_files: list[File]):
    name = st.text_input("Enter file name:")

    # write to a new file named with page_name
    if st.button("Create"):
        file_index = saved_files.__len__() 
        print(name)
        # save file in /pages
        file = File()
        file.file = None
        file.file_index = file_index
        file.page_name = name if name != "" else "default"
        file.config = {}

        st.session_state.new_file = file
        st.session_state.saved_files.append(file)


        
def interface():
    if "saved_files" not in st.session_state:
        st.session_state.saved_files = Pages.load_app_state() 

    if "error" in st.session_state:
        st.error(st.session_state.error)
        st.session_state.error = None

    if "pages" not in os.listdir("./src"):
        os.makedirs("./src/pages")

    if "new_file" in st.session_state and st.session_state.new_file is not None:
        file: File = st.session_state.new_file
        Pages.create_page(file)
        Pages.load_app_state(st.session_state.saved_files)
        st.session_state.new_file = None

    Pages.save_app_state(st.session_state.saved_files)
    st.title('RHescue')
    st.write('\n')
    
    add_new_page(st.session_state.saved_files)


def ler_ficheiro(file: File):
    st.code(file)
    uploaded_file = None
    uploaded_file = st.file_uploader("Upload excel", key=f"input {file.page_name}")

    default_options = []
    folder_path = "./layouts/"
    
    # Get a list of all files in the folder
    file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Print the list of files
    for file_i in file_list:
        default_options.append(file_i)

    option = st.selectbox('Tipo de Avaliacao', default_options)
    current_config = Config(read_layout_from_file=True, layout=folder_path + option)
    st.code(current_config.get_data_as_json() if current_config else "No config loaded")

    customize_config(current_config)

    if uploaded_file is not None:
        file.file = uploaded_file
        for f in st.session_state.saved_files:
            if file.file_index == f.file_index:
                f.file = uploaded_file
                f.page_name = file.page_name
                f.config = current_config 
                f.file_index = file.file_index
        Pages.save_app_state(st.session_state.saved_files)
        data = None

    if file.file is not None:
        try:
            data = pd.read_excel(file.file)
            st.dataframe(data, hide_index=True, height=200)
        except:
            try:
                data = pd.read_csv(file.file, sep=";")
                st.dataframe(data, hide_index=True, height=200)
            except:
                st.error("File format not supported.")
    return uploaded_file
    

def customize_config(config: Config):
    json_config = config.get_data_as_json()["layout"]

    avaliated_people: list[str] = []
    list_questions: list[dict] = []
    col1 = "Pergunta"
    col2 = "Tipo"
    # encontra os nomes das pessoas a ser avaliadas
    for row in json_config:
        if row["type"] == "MEASURED":
            for name in row["names"]:
                avaliated_people.append(name)
        if row["type"] == "QUESTIONS":
            for question in row["questions"]:
                row = {col1: question["label"], col2:question["type"]}
                list_questions.append(row)
    
    df = pd.DataFrame(list_questions)

        

    new_people = st.text_input("Escreve o nome das pessoas a avaliar: (separado por vírgula)", key="new_people", value=", ".join(avaliated_people))
    edited_df = st.data_editor(df, num_rows="dynamic")
