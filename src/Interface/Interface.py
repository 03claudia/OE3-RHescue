import streamlit as st



def interface():
    
    st.markdown("<center><h1>Avaliação de Desempenho</h1></center>", unsafe_allow_html=True)

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
    


 




    