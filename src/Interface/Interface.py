import streamlit as st
import json

options=['Excel de Input','Marketing','Recursos Humanos','VPE']

def interface():
    ficheiros=None
    
    st.title("Avaliação de Desempenho") 
    selected_page=st.sidebar.selectbox('Escolha um página',options)

    if selected_page=='Excel de Input':
        ficheiros=input()
        
    if selected_page=='Marketing':
        layout_MK()

    if selected_page=='Recursos Humanos':
        layout_RH()      

    if ficheiros is not None: 
        return ficheiros    

 
        
def input():
    st.write("\n\n")

    st.write("Faça o upload dos arquivos para a avaliação de desempenho.")

    files_list=[]

    num_files = len(options)-1

    for i in range (num_files):
        file = st.file_uploader(f"Upload do Arquivo {options[i+1]}", type=["xlsx"])
        if file is not None:
            files_list.append(file)

    
    if st.button("Processar Arquivos"):
       if len(files_list)==num_files:
            st.write('Ficheiros processados:')
            for file in files_list:
             st.write(file.name)
            return files_list
       else:
           st.write('Dê upload a todos os ficheiros')
    

def layout_MK():

    file= open("./layouts/MK.json", 'r', encoding="UTF-8")
    data=json.loads(file.read())

    
    st.write("\n\n")
    st.title('Marketing')

    for i in data['layout']:
        if 'MEASURED'== i['type']:
            names=(i['names'])
            nome_avaliados=st.text_input('Nomes dos avaliados:',value=names)
            i['names']=nome_avaliados

    
    st.write("\n\n")

    for i in data['layout']:
        if 'MEASURER'== i['type']:
            name=(i['label'])
            nome_avaliador=st.text_input('Nome da coluna do avaliador:',value=name)
            i['label']=nome_avaliador


    #PARA REMOVER UMA QUESTÃO É SO DEIXAR O ESPAÇO EM BRANCO.

    st.write("\n\n")
    questions=[]
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

      

            i['questions']=questions   
              




    if st.button('Concluido'):
        st.write(data['layout'])
      
      

      

  
    
def layout_RH():

    file= open("./layouts/RH.json", 'r',encoding="UTF-8")
    data=json.loads(file.read())

    
    st.write("\n\n")
    st.title('Recursos Humanos')

    for i in data['layout']:
        if 'MEASURED'== i['type']:
            names=(i['names'])
            nome_avaliados=st.text_input('Nomes dos avaliados:',value=names)
            i['names']=nome_avaliados

    
    st.write("\n\n")

    for i in data['layout']:
        if 'MEASURER'== i['type']:
            name=(i['label'])
            nome_avaliador=st.text_input('Nome da coluna do avaliador:',value=name)
            i['label']=nome_avaliador


    #PARA REMOVER UMA QUESTÃO É SO DEIXAR O ESPAÇO EM BRANCO.

    st.write("\n\n")
    questions=[]
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

      

            i['questions']=questions   
              




    if st.button('Concluido'):
        st.write(data['layout'])

  
        


 




    
