import streamlit as st
import layout_int
import json


def interface():


    num=int(2)
    options=['Excel de Input','Layout Marketing']
    st.title("Avaliação de Desempenho") 
    selected_page=st.sidebar.selectbox('Escolha um página',options)
    st.sidebar.write('\n\n\n\n\n\n')
    st.sidebar.progress(num/4)

    
    if selected_page=='Excel de Input':
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
                
        

    if selected_page=='Layout Marketing':
        l=layout_int('Marketing')
        l.interface()
        


 
        
    

  
        


 




    
