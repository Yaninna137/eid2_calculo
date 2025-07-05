import streamlit as st
from core.processing import GPU

def Datos(nombre: str, f: float, k: int):
    gpu = GPU(f=f, k=k)
    A = gpu.amdahl()
    Amax = gpu.amdahl_max()

    st.session_state.resultados = {
        "nombre": nombre,
        "A": A,
        "Amax": Amax
    }
