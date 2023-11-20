import streamlit as st
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

        
def interface():
    if 'saved_files' not in st.session_state:
        st.session_state.saved_files: list[File] = []
    if 'page_selected' not in st.session_state:
        st.session_state.page_selected = 'home' 

    st.title('RHescue')
    st.write('\n')


    st.sidebar.title('Menu')
    if st.sidebar.button("Home") or st.session_state.page_selected == "home":
        st.session_state.page_selected = "home"
        home(st.session_state.saved_files) 

    for file in st.session_state.saved_files:
        if st.sidebar.button(f"Page {file.page_name}", key=file.page_name) or st.session_state.page_selected == file.page_name:
            st.session_state.page_selected = file.page_name
            ler_ficheiro(file)

    if st.sidebar.button("+"):
       file = File()
       file.page_name = st.session_state.saved_files.__len__() + 1
       st.session_state.saved_files.append(file)

def ler_ficheiro(file: File):

    file_name = st.text_input("Enter file name:", key=f"{file.page_name} name")
    uploaded_file = st.file_uploader("Upload excel", key=f"input {file.page_name}")

    if uploaded_file is not None:
        file.file = uploaded_file
        data = None
        try:
            data = pd.read_excel(uploaded_file)
        except:
            data = pd.read_csv(uploaded_file, sep=";")
        st.dataframe(data, hide_index=True, height=200)

    if st.button("Guardar", disabled = uploaded_file == None):
        if file_name == "":
            file_name = "default"
        file.page_name = file_name
        st.success(f"File {file_name} saved successfully.")
    return uploaded_file, file_name 
    
def home(saved_files: list[File]):
    st.write("Home")
    for file in saved_files:
        st.write(file.page_name)

    st.button("Processar")
