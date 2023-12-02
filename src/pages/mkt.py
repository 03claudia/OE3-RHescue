import Interface.Interface as Interface
import streamlit as st

saved_files = st.session_state.saved_files
st.write("mkt")
Interface.ler_ficheiro(saved_files[2])
