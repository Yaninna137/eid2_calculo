import streamlit as st
from core.processing import graficar_A_vs_k

def mostrar_tab_graficos():
    """Mostrar el tab de gráficos A vs k"""
    st.header("📈 Gráficos A vs k según Requisitos")
    
    st.subheader("Gráfico requerido: A vs k para f = 0.25 y f = 0.35")
    
    # Gráfico específico solicitado
    fig_req = graficar_A_vs_k([0.25, 0.35])
    st.pyplot(fig_req)
    
    st.markdown("---")
    st.subheader("🔍 Análisis Adicional: Todos los Componentes")
    
    # Gráfico con todos los valores f de los componentes
    f_values = [0.20, 0.25, 0.35]  # VRAM/NVLink, Texturizado, CUDA
    fig_all = graficar_A_vs_k(f_values)
    st.pyplot(fig_all)
    
    # Interpretación
    st.info("""
    **Interpretación de los gráficos:**
    
    • **f = 0.35 (Núcleos CUDA)**: Muestra la mayor aceleración potencial
    • **f = 0.25 (Unidades de texturizado)**: Aceleración intermedia
    • **f = 0.20 (VRAM/NVLink)**: Menor aceleración debido a la fracción mejorable más baja
    
    Observa cómo el límite teórico se alcanza más rápidamente con valores altos de f.
    """)