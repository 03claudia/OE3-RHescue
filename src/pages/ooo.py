import Interface.Interface as Interface
import streamlit as st

saved_files = st.session_state.saved_files
st.write("ooo")
Interface.ler_ficheiro(saved_files[5])
