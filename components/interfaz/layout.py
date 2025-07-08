import streamlit as st

def configurar_pagina():
    """Configurar la página principal de Streamlit"""
    st.set_page_config(
        page_title="Simulador Optimización GPU - Ley de Amdahl",
        page_icon="🎮",
        layout="wide"
    )

def mostrar_encabezado():
    """Mostrar el encabezado principal de la aplicación"""
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='margin-bottom: 0; color: #FF6B6B;'>🎮 Simulador Optimización GPU</h1>
        <p style='font-size: 20px; color: #666;'>Análisis mediante Ley de Amdahl - Grupo Par</p>
    </div>
    """, unsafe_allow_html=True)

def mostrar_sidebar():
    """Mostrar el sidebar con información teórica"""
    with st.sidebar:
        st.header("📚 Información Teórica")
        st.markdown("""
        **Ley de Amdahl:**
        
        A = 1 / ((1-f) + f/k)
        
        Donde:
        - **f**: Fracción mejorable
        - **k**: Factor de mejora
        - **A**: Aceleración obtenida
        
        **Límite teórico:**
        
        A_max = 1 / (1-f)
        """)
        
        st.markdown("---")
        st.header("🔧 Componentes GPU")
        componentes_info = {
            "Núcleos CUDA": "f=0.35, k=5",
            "Memoria VRAM": "f=0.20, k=3", 
            "Unidades texturizado": "f=0.25, k=7",
            "Interconexión NVLink": "f=0.20, k=10"
        }
        
        for comp, info in componentes_info.items():
            st.write(f"**{comp}**: {info}")

def get_datos_componentes():
    """Retorna los datos fijos de los componentes GPU"""
    return {
        "Núcleos CUDA": {"f": 0.35, "k": 5},
        "Memoria VRAM": {"f": 0.20, "k": 3},
        "Unidades de texturizado": {"f": 0.25, "k": 7},
        "Interconexión NVLink": {"f": 0.20, "k": 10},
    }