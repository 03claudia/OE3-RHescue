import streamlit as st
import json


def interface():


    num=int(2)
    options=['Excel de Input','Layout Marketing']
    st.title("Avaliação de Desempenho") 
    selected_page=st.sidebar.selectbox('Escolha um página',options)
    st.sidebar.write('\n\n\n\n\n\n')
    st.sidebar.progress(num/4)

    if selected_page=='Excel de Input':
        input()
        

    if selected_page=='Layout Marketing':
        layout_MK() 
        


 
        
def input():
    st.write("\n\n")

    st.write("Faça o upload dos arquivos para a avaliação de desempenho.")

    files_list=[]

    num_files = st.slider("Quantidade de Arquivos", min_value=1, max_value=10, value=1)

    for i in range (num_files):
        file = st.file_uploader(f"Upload do Arquivo {i+1}", type=["xlsx"])
        if file is not None:
            files_list.append(file)

    
    if st.button("Processar Arquivos"):
       st.write('Ficheiros processados:')
       for file in files_list:
           st.write(file.name)
       return files_list
    

def layout_MK():
    questions=[]
    st.write("\n\n")
    st.title('Marketing')
    measured=st.text_input('Nomes dos avaliados:',value='')

    num_questions = st.slider("Quantidade de questões:", min_value=1, max_value=10, value=1)

    for i in range(num_questions):
        question=st.text_input(f'Questao {i+1}',value='')
        if question != '':
            questions.append()

    st.button('Concluido')   
  
        


 




    
