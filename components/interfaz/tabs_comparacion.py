import streamlit as st
import pandas as pd
from core.processing import calcular_todos_componentes, graficar_comparacion_componentes

def mostrar_tab_comparacion():
    """Mostrar el tab de comparación completa de componentes"""
    st.header("📊 Comparación Completa de Componentes")
    
    # Calcular todos los componentes
    resultados = calcular_todos_componentes()
    
    # Crear DataFrame para mostrar resultados
    df_resultados = pd.DataFrame(resultados).T
    df_resultados = df_resultados.round(4)
    
    st.subheader("📋 Tabla de Resultados")
    st.dataframe(df_resultados, use_container_width=True)
    
    # Gráfico comparativo
    st.subheader("📊 Gráficos Comparativos")
    fig_comp = graficar_comparacion_componentes()
    # st.pyplot(fig_comp)
    st.plotly_chart(fig_comp, use_container_width=True)

    
    # Análisis del mejor componente
    st.markdown("---")
    st.subheader("🏆 Análisis de Mejor Componente")
    
    # Encontrar el componente con mayor aceleración
    mejor_comp = max(resultados.items(), key=lambda x: x[1]["A"])
    
    col8, col9 = st.columns(2)
    
    with col8:
        st.success(f"🥇 **Mejor componente**: {mejor_comp[0]}")
        st.write(f"• Aceleración: {mejor_comp[1]['A']:.4f}")
        st.write(f"• Límite teórico: {mejor_comp[1]['Amax']:.4f}")
        st.write(f"• Fracción mejorable: {mejor_comp[1]['f']:.2f}")
    
    with col9:
        st.info("**Justificación:**")
        st.write(f"Los núcleos CUDA ofrecen la mayor aceleración ({mejor_comp[1]['A']:.4f}) debido a su alta fracción mejorable (f=0.35), lo que significa que el 35% del procesamiento puede beneficiarse de la optimización.")