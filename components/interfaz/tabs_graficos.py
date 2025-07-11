import streamlit as st
from core.processing import graficar_A_vs_k

def mostrar_tab_graficos():
    """Mostrar el tab de gráficos A vs k"""
    st.header("📈 Gráficos A vs k según Requisitos")
    st.markdown("""
    <style>
        .capsula-linea {
            display: flex; 
            align-items: center; 
            gap: 12px; 
            font-size: 18px; 
            color: rgba(255, 255, 255, 0.75);
            font-weight: 500;
            margin-bottom: 15px;
        }
        .capsula {
            background-color: #1a1a2e;
            color: #ffffff;
            padding: 6px 16px;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 600;
            box-shadow: 0 0 5px rgba(255, 255, 255, 0.1);
        }
    </style>
    <div class='capsula-linea'>
        <span>Gráfico requerido: A vs k para</span>
        <div class='capsula'>f = 0.25</div>
        <span>y</span>
        <div class='capsula'>f = 0.35</div>
    </div>
    """, unsafe_allow_html=True)


    # Gráfico específico solicitado
    fig_req = graficar_A_vs_k([0.25, 0.35])
    # st.pyplot(fig_req)
    st.plotly_chart(fig_req, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🔍 Análisis Adicional: Todos los Componentes")
    
    # Gráfico con todos los valores f de los componentes
    f_values = [0.20, 0.25, 0.35]  # VRAM/NVLink, Texturizado, CUDA
    fig_all = graficar_A_vs_k(f_values)
    # st.pyplot(fig_all)
    st.plotly_chart(fig_all, use_container_width=True)
    
    # Interpretación
    st.info("""
    **Interpretación de los gráficos:**
    
    • **f = 0.35 (Núcleos CUDA)**: Muestra la mayor aceleración potencial
    • **f = 0.25 (Unidades de texturizado)**: Aceleración intermedia
    • **f = 0.20 (VRAM/NVLink)**: Menor aceleración debido a la fracción mejorable más baja
    
    Observa cómo el límite teórico se alcanza más rápidamente con valores altos de f.
    """)