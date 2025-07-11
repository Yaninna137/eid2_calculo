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
        <h1 style='margin-bottom: 0; color: #B368FF;'>🎮 Simulador Optimización GPU</h1>
        <p style='font-size: 20px; color: #666;'>Análisis mediante Ley de Amdahl - Grupo Par</p>
    </div>
    """, unsafe_allow_html=True)

def mostrar_sidebar():
    """Mostrar el sidebar con información teórica"""
    with st.sidebar:
        st.header("📚 Información Teórica")
        st.markdown("#### ⨺ Ley de Amdahl")

        st.latex(r"A = \frac{1}{(1 - f) + \frac{f}{k}}")

        st.markdown("#### ⨺ Límite Teórico de Aceleración")

        st.latex(r"A_{\text{max}} = \frac{1}{1 - f}")
        st.markdown("""
        <div style='
            background-color: #150120;
            padding: 15px 20px;
            border-radius: 10px;
            color: rgba(255, 255, 255, 0.85);
            font-size: 16px;
            line-height: 1.6;
        '>
            <b>Donde:</b><br>
            • <b>f</b>: Fracción mejorable<br>
            • <b>k</b>: Factor de mejora<br>
            • <b>A</b>: Aceleración obtenida
        </div>
        """, unsafe_allow_html=True)

        
        st.markdown("---")
        st.markdown("### 🔹 Componentes GPU")

        bloque_html = """
        <div style='
            background-color: #150120;
            padding: 10px 15px;
            border-radius: 10px;
            margin-bottom: 6px;
            font-size: 16px;
            color: rgba(255,255,255,0.92);
        '>
            <b>{nombre}</b>: <span style='color: #CCCCCC;'>{info}</span>
        </div>
        """

        componentes_info = {
            "Núcleos CUDA": "f = 0.35, k = 5",
            "Memoria VRAM": "f = 0.20, k = 3", 
            "Unidades de Texturizado": "f = 0.25, k = 7",
            "Interconexión NVLink": "f = 0.20, k = 10"
        }

        for nombre, info in componentes_info.items():
            st.markdown(bloque_html.format(nombre=nombre, info=info), unsafe_allow_html=True)


def get_datos_componentes():
    """Retorna los datos fijos de los componentes GPU"""
    return {
        "Núcleos CUDA": {"f": 0.35, "k": 5},
        "Memoria VRAM": {"f": 0.20, "k": 3},
        "Unidades de texturizado": {"f": 0.25, "k": 7},
        "Interconexión NVLink": {"f": 0.20, "k": 10},
    }