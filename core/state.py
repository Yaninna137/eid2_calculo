import streamlit as st

def inicializar_session_state():
    if 'resultados' not in st.session_state:
        st.session_state['resultados'] = None
    if 'tiempo_original' not in st.session_state:
        st.session_state['tiempo_original'] = 50.0