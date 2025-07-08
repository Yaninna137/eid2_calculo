import streamlit as st
import matplotlib.pyplot as plt
from core.processing import (
    GPU, encontrar_mejor_componente, 
    analizar_impacto_nvlink, comparar_texturizado_vs_vram
)

def mostrar_tab_especificos():
    """Mostrar el tab de análisis específicos requeridos"""
    st.header("🔍 Análisis Específicos Requeridos")
    
    # Pregunta 3: Tiempo de renderizado y componente para 30% de aceleración
    st.subheader("❓ Pregunta 3: Análisis de Núcleos CUDA y Objetivo 30%")
    
    col10, col11 = st.columns(2)
    
    with col10:
        st.write("**Si el renderizado tarda 50 ms originalmente:**")
        cuda_gpu = GPU(f=0.35, k=5)
        tiempo_cuda = cuda_gpu.tiempo_optimizado(50.0)
        st.success(f"⏱️ Tiempo con núcleos CUDA optimizados: {tiempo_cuda:.2f} ms")
        
    with col11:
        st.write("**Componente para lograr 30% de aceleración (A ≥ 1.30):**")
        candidatos = encontrar_mejor_componente(1.30)
        if candidatos:
            st.success(f"🎯 Mejor opción: {candidatos[0][0]}")
            st.write(f"Aceleración: {candidatos[0][1]:.4f}")
        else:
            st.warning("Ningún componente individual logra 30% de aceleración")

    st.markdown("---")
    
    # Pregunta 5: Análisis de NVLink
    st.subheader("❓ Pregunta 5: ¿Por qué NVLink tiene impacto limitado?")
    
    nvlink_analisis = analizar_impacto_nvlink()
    
    col12, col13 = st.columns(2)
    
    with col12:
        st.write("**Análisis numérico:**")
        st.write(f"• Aceleración actual (k=10): {nvlink_analisis['A_actual']:.4f}")
        st.write(f"• Límite teórico: {nvlink_analisis['Amax']:.4f}")
        st.write(f"• Fracción mejorable: {nvlink_analisis['fraccion_limitante']:.2f}")
        
        st.warning("""
        **Explicación:** A pesar de tener k=10, NVLink está limitado por su 
        fracción mejorable f=0.20. Esto significa que solo el 20% del procesamiento 
        puede beneficiarse de la optimización, limitando el impacto global.
        """)
    
    with col13:
        # Gráfico de NVLink vs k
        fig_nvlink, ax = plt.subplots(figsize=(8, 5))
        ax.plot(nvlink_analisis['k_values'], nvlink_analisis['aceleraciones'], 
               'ro-', linewidth=2, markersize=6)
        ax.axhline(y=nvlink_analisis['Amax'], color='r', linestyle='--', 
                  alpha=0.7, label=f'Límite teórico = {nvlink_analisis["Amax"]:.3f}')
        ax.set_xlabel('Factor de mejora k')
        ax.set_ylabel('Aceleración A')
        ax.set_title('NVLink: Aceleración vs Factor k')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig_nvlink)

    st.markdown("---")
    
    # Pregunta 6: Comparación Texturizado vs VRAM
    st.subheader("❓ Pregunta 6: Texturizado vs VRAM")
    
    comparacion = comparar_texturizado_vs_vram()
    
    col14, col15 = st.columns(2)
    
    with col14:
        st.write("**🎨 Unidades de Texturizado:**")
        st.write(f"• f = {comparacion['texturizado']['f']:.2f}")
        st.write(f"• k = {comparacion['texturizado']['k']}")
        st.write(f"• A = {comparacion['texturizado']['A']:.4f}")
        st.write(f"• A_max = {comparacion['texturizado']['Amax']:.4f}")
        
    with col15:
        st.write("**💾 Memoria VRAM:**")
        st.write(f"• f = {comparacion['vram']['f']:.2f}")
        st.write(f"• k = {comparacion['vram']['k']}")
        st.write(f"• A = {comparacion['vram']['A']:.4f}")
        st.write(f"• A_max = {comparacion['vram']['Amax']:.4f}")
    
    # Conclusión de la comparación
    if comparacion['texturizado']['A'] > comparacion['vram']['A']:
        ganador = "Unidades de Texturizado"
        razon = f"mayor fracción mejorable (f={comparacion['texturizado']['f']:.2f} vs f={comparacion['vram']['f']:.2f})"
    else:
        ganador = "Memoria VRAM"
        razon = f"mejor factor de mejora compensando la menor fracción mejorable"
        
    st.success(f"""
    **🏆 Conclusión:** {ganador} es mejor debido a {razon}.
    
    Diferencia de aceleración: {abs(comparacion['texturizado']['A'] - comparacion['vram']['A']):.4f}
    """)