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

class File:
    file = None 
    page_name = "No name"
    config = {}
    file_index = 0

def add_new_page(saved_files: list[File]):
    name = st.text_input("Enter file name:")

    # write to a new file named with page_name
    if st.button("Create"):
        file_index = saved_files.__len__() + 1
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
        st.session_state.saved_files = load_saved_files() 

    if "error" in st.session_state:
        st.error(st.session_state.error)
        st.session_state.error = None

    if "pages" not in os.listdir("./src"):
        os.makedirs("./src/pages")

    if "new_file" in st.session_state and st.session_state.new_file is not None:
        file: File = st.session_state.new_file
        try:
            print(f"file.page_name: {file.page_name}")
            if file.page_name in os.listdir("./src/pages"):
                st.error(f"File {file.page_name} already exists.")
            else:
                with open(f"./src/pages/{file.page_name}.py", "w") as f:
                    f.write(f"import Interface.Interface as Interface\n")
                    f.write(f"import streamlit as st\n")
                    f.write(f"\n")
                    f.write(f"saved_files = st.session_state.saved_files\n")
                    f.write(f"st.write(\"{file.page_name}\")\n")
                    f.write(f"Interface.ler_ficheiro(saved_files[{file.file_index}])\n")
                st.write(f"File {file.page_name} created successfully.")
                st.session_state.new_file = None
        except Exception as e:
            st.error(f"An error occurred: {e}")
        save_saved_files(st.session_state.saved_files)

    st.title('RHescue')
    st.write('\n')
    
    add_new_page(st.session_state.saved_files)


def ler_ficheiro(file: File):
    uploaded_file = None
    uploaded_file = st.file_uploader("Upload excel", key=f"input {file.page_name}")
    option = st.selectbox(
    'Tipo de Avaliacao',
    ('Avaliacao Mensal', 'Avaliacao VPE', 'Avalicao Presidente'))
    if uploaded_file is not None:
        file.file = uploaded_file
        data = None
        try:
            data = pd.read_excel(uploaded_file)
        except:
            data = pd.read_csv(uploaded_file, sep=";")
        st.dataframe(data, hide_index=True, height=200)

    return uploaded_file
    

def save_saved_files(saved_files: list[File], filename="saved_files.txt"):
    with open(filename, "w") as f:
        for file in saved_files:
            f.write(f"{file.page_name},{file.file_index}\n")

def load_saved_files(filename="saved_files.txt"):
    saved_files = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                page_name, file_index = line.strip().split(',')
                file = File()
                file.page_name = page_name
                file.file_index = file_index
                saved_files.append(file)
    return saved_files
