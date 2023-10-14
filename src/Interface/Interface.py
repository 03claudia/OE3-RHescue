import streamlit as st
import json

options=['Excel de Input','Marketing','Recursos Humanos','VPE']


data_mk=None


def interface():

    global data_mk
    global data_rh

    file_mk= open("./layouts/Avaliacao-Membros-MKT.json", 'r', encoding="UTF-8")
    data_mk=json.loads(file_mk.read()) 

    file_rh= open("./layouts/Avaliacao-Membro-RH.json", 'r', encoding="UTF-8")
    data_rh=json.loads(file_rh.read()) 



    ficheiros=None
    
    
    st.title("Avaliação de Desempenho") 
   
        
    selected_page=st.sidebar.selectbox('Escolha um página',options)

    if selected_page=='Excel de Input':
        ficheiros=input()
        
    if selected_page=='Marketing':
        data_mk=layout_MK(data_mk)
        
    if selected_page=='Recursos Humanos':
        data_rh=layout_RH(data_rh)      

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



def layout_MK(data):


    st.write("\n\n")
    st.title('Marketing')
    
    if st.button('Adicionar uma pergunta'):
        for i in data['layout']:
            if 'QUESTIONS'==i['type']:
                i['questions'].append({'label':'','type':'NUMBER'})
        with open("./layouts/Avaliacao-Membros-MKT.json", 'w', encoding="UTF-8") as file:
            file.write(json.dumps(data_mk, indent=2))
        file.close()

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
                    tipo=st.selectbox(f'Escolha a opção da pergunta {num_question}:',['NUMBER','OBSERVATION'])
                elif j['type']=='OBSERVATION':
                    tipo=st.selectbox(f'Escolha a opção {num_question}',['OBSERVATION','NUMBER'])
                
                if question != '' and tipo != '':
                    questions.append({'label':question,'type':tipo})
                num_question+=1

      

            i['questions']=questions   
              




    if st.button('Concluido'):
        st.write(data['layout'])
        with open("./layouts/Avaliacao-Membros-MKT.json", 'w', encoding="UTF-8") as file:
            file.write(json.dumps(data_mk, indent=2))
        file.close()
        return data

        
      
      

      

  
    
def layout_RH(data):

    st.write("\n\n")
    st.title('Recursos Humanos')
    
    if st.button('Adicionar uma pergunta'):
        for i in data['layout']:
            if 'QUESTIONS'==i['type']:
                i['questions'].append({'label':'','type':'NUMBER'})
        with open("./layouts/Avaliacao-Membro-RH.json", 'w', encoding="UTF-8") as file:
            file.write(json.dumps(data_rh, indent=2))
        file.close()

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
                    tipo=st.selectbox(f'Escolha a opção da pergunta {num_question}:',['NUMBER','OBSERVATION'])
                elif j['type']=='OBSERVATION':
                    tipo=st.selectbox(f'Escolha a opção {num_question}',['OBSERVATION','NUMBER'])
                
                if question != '' and tipo != '':
                    questions.append({'label':question,'type':tipo})
                num_question+=1

      

            i['questions']=questions   
              




    if st.button('Concluido'):
        st.write(data['layout'])
        with open("./layouts/Avaliacao-Membro-RH.json", 'w', encoding="UTF-8") as file:
            file.write(json.dumps(data_rh, indent=2))
        file.close()
        return data
  
        


 




    
