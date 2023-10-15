import streamlit as st
import json


Av_Mensal=['Avaliacao-Membros-MKT','Avaliacao-Membro-RH']
Av_Trimestral=[]
Av_Projeto=[]
Av_Direcao=['Avaliacao-Vice-Presidente-Externo']


data_mk=None

def abrir(file):
    file_data= open(f'./layouts/{file}.json', 'r', encoding="UTF-8")
    data=json.loads(file_data.read())

    return data 


def escrever(file,data):
    with open(f'./layouts/{file}.json', 'w', encoding="UTF-8") as file:
        file.write(json.dumps(data, indent=2))
        file.close()

def ficheiros(num_files,name,files_list):
    for i in range (num_files):
        file = st.file_uploader(f"Upload do Arquivo {name[i]}", type=["xlsx"])
        if file is not None:
            files_list.append(file)
    return files_list        


def layout(file_name):
    st.write("\n\n")
    st.title(f'{file_name}')

    data=abrir(file_name)
    
    if st.button('Adicionar uma pergunta'):
        for i in data['layout']:
            if 'QUESTIONS'==i['type']:
                i['questions'].append({'label':'','type':'NUMBER'})
        escrever(file_name,data)

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
        st.write('Alterações efetuadas')
        escrever(file_name,data)
        




def interface():
    st.title('RHescue')
    st.write('\n')
   
    ficheiros=None
    st.sidebar.title('Input de Ficheiros')
    if st.sidebar.checkbox('Inserir Ficheiros', value=True):
        ficheiros=input()

    st.sidebar.title('Desempenho Mensal')
    if st.sidebar.checkbox('Alterar Configurações AM'):
        selected_page_AM=st.sidebar.selectbox('Escolha um página',Av_Mensal)
        
        for i in range(len(Av_Mensal)):
            if selected_page_AM== Av_Mensal[i]:
                layout(Av_Mensal[i])
                
          

    
    st.sidebar.title('Direção e Presidência')
    if st.sidebar.checkbox('Alterar Configurações DIR/PRES'):
        selected_page_Dir=st.sidebar.selectbox('Escolha um página',Av_Direcao)
        for i in range(len(Av_Direcao)):
            if selected_page_Dir==Av_Direcao[i]:
                layout(Av_Direcao[i])
            


    if ficheiros is not None: 
        return ficheiros  
      

   
        
def input():
    files_list=[]
    st.write("\n\n")

    st.title("Avaliação de Desempenho Mensal.")
    Num_Av_Mensal=len(Av_Mensal)
    files_list=ficheiros(Num_Av_Mensal,Av_Mensal,files_list)


    st.title('Direção e Presidência.')
    Num_Av_Dir=len(Av_Direcao)
    files_list=ficheiros(Num_Av_Dir,Av_Direcao,files_list)

    num_files=Num_Av_Mensal+Num_Av_Dir

    if st.button("Processar Arquivos"):
       if len(files_list)==num_files:
            st.write('Ficheiros processados:')
            for file in files_list:
             st.write(file.name)
            return files_list
       else:
           st.write('Dê upload a todos os ficheiros')



