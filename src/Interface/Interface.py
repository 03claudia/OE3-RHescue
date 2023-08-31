import streamlit as st
import json


def interface():


    num=int(2)
    options=['Excel de Input','Configurações Marketing',]
    st.title("Avaliação de Desempenho") 
    selected_page=st.sidebar.selectbox('Escolha um página',options)
    st.sidebar.write('\n\n\n\n\n\n')
    st.sidebar.progress(num/4)
   
    if selected_page=='Excel de Input':
        input()
        

    if selected_page=='Configurações Marketing':
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

    file= open("./layouts/MK.json", 'r',encoding="UTF-8")
    data=json.loads(file.read())

    questions=[]
    st.write("\n\n")
    st.title('Marketing')

    for i in data['layout']:
        if 'MEASURED'== i['type']:
            names=(i['names'])

    _=st.text_input('Nomes dos avaliados:',value=names)
    st.write("\n\n")

    for i in data['layout']:
        if 'MEASURER'== i['type']:
            name=(i['label'])

    _=st.text_input('Nome da coluna do avaliador:',value=name)
    st.write("\n\n")
    num_question=1
    for i in data['layout']:
        if 'QUESTIONS'== i['type']:
            questoes=(i['questions'])
            for j in questoes:
                question=st.text_input(f'Questao {num_question}:',value=j['label'])
                if j['type']=='NUMBER':
                    tipo=st.selectbox(f'Escolha a opção da pergunta {num_question}:',['Número','Observação'])
                elif j['type']=='OBSERVATION':
                    tipo=st.selectbox(f'Escolha a opção {num_question}',['Observação','Número'])

                if question != '':
                    questions.append((question,tipo))
                num_question+=1
                   


    st.button('Concluido')   
  
        


 




    
