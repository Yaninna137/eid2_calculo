import streamlit as st
from .interfaz.layout import configurar_pagina, mostrar_encabezado, mostrar_sidebar
from .interfaz.tabs_individual import mostrar_tab_individual
from .interfaz.tabs_comparacion import mostrar_tab_comparacion
from .interfaz.tabs_graficos import mostrar_tab_graficos
from .interfaz.tabs_especificos import mostrar_tab_especificos
from .interfaz.resumen_ejecutivo import mostrar_resumen_ejecutivo
from core.state import inicializar_session_state

def main():
    """Función principal que ejecuta la aplicación Streamlit"""
    
    # Configurar la página
    configurar_pagina()
    
    # Inicializar el estado de la sesión
    inicializar_session_state()
    
    # Mostrar encabezado
    mostrar_encabezado()
    
    # Mostrar sidebar
    mostrar_sidebar()
    
    # Crear las pestañas principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Análisis Individual", 
        "📊 Comparación Completa", 
        "📈 Gráficos A vs k", 
        "🔍 Análisis Específicos",
        "📋 Resumen Ejecutivo"
    ])
    
    # Mostrar contenido de cada pestaña
    with tab1:
        mostrar_tab_individual()
    
    with tab2:
        mostrar_tab_comparacion()
    
    with tab3:
        mostrar_tab_graficos()
    
    with tab4:
        mostrar_tab_especificos()
    
    with tab5:
        mostrar_resumen_ejecutivo()

if __name__ == "__main__":
    main()