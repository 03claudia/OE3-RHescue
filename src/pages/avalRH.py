import Interface.Interface as Interface
import streamlit as st

saved_files = st.session_state.saved_files
st.write("avalRH")
Interface.ler_ficheiro(saved_files[3])
