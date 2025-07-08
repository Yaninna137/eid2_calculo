import streamlit as st
import matplotlib.pyplot as plt
from core.processing import GPU
from .layout import get_datos_componentes

def mostrar_tab_individual():
    """Mostrar el tab de análisis individual de componentes"""
    st.header("🎯 Análisis Individual de Componentes")
    
    # Obtener datos de componentes
    datos_componentes = get_datos_componentes()

    col1, col2 = st.columns([2, 1])

    with col1:
        opciones = list(datos_componentes.keys())
        seleccion_gpu = st.selectbox("🔧 Seleccionar Componente", opciones, key="gpu")

    with col2:
        f_fijo = datos_componentes[seleccion_gpu]["f"]
        k_fijo = datos_componentes[seleccion_gpu]["k"]
        st.metric("Fracción mejorable (f)", f"{f_fijo:.2f}")
        st.metric("Factor de mejora (k)", f"{k_fijo}")

    # Sliders para modificar fracción mejorable f y factor k en columnas lado a lado
    st.markdown("---")
    st.subheader("🎛️ Experimentación con Fracción Mejorable (f) y Factor k")

    col_f, col_k = st.columns(2)

    with col_f:
        f_usuario = st.slider(
            "Modificar fracción mejorable (f)",
            min_value=0.0, max_value=1.0, value=f_fijo, step=0.01
        )

    with col_k:
        k_usuario = st.slider(
            "Modificar factor de mejora (k)",
            min_value=1, max_value=20, value=k_fijo, step=1
        )

    # Crear instancia GPU con valores modificados
    gpu = GPU(f=f_usuario, k=k_usuario)
    A = gpu.amdahl()
    Amax = gpu.amdahl_max()

    # Mostrar resultados en métricas
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.metric("🚀 Aceleración A", f"{A:.4f}")
    
    with col4:
        st.metric("⚡ Límite teórico A_max", f"{Amax:.4f}")
    
    with col5:
        eficiencia = (A / Amax) * 100 if Amax != 0 else 0
        st.metric("📊 Eficiencia", f"{eficiencia:.1f}%")

    # Análisis de tiempo
    st.markdown("---")
    st.subheader("⏱️ Análisis de Tiempo de Renderizado")
    
    col6, col7 = st.columns(2)
    
    with col6:
        tiempo_original = st.number_input(
            "Tiempo original de renderizado (ms)", 
            min_value=0.1, max_value=1000.0, value=50.0, step=0.1
        )
    
    with col7:
        tiempo_opt = gpu.tiempo_optimizado(tiempo_original)
        mejora_pct = gpu.porcentaje_mejora(tiempo_original)
        
        st.success(f"⏱️ Tiempo optimizado: {tiempo_opt:.2f} ms")
        st.success(f"📈 Mejora total: {mejora_pct:.2f}%")

    # Gráfico individual
    st.markdown("---")
    st.subheader(f"📈 Gráfico A vs k para {seleccion_gpu} con f = {f_usuario:.2f}")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    k_range = range(1, 21)
    A_values = [GPU(f=f_usuario, k=k).amdahl() for k in k_range]
    
    ax.plot(list(k_range), A_values, 'b-', linewidth=2, label=f'f = {f_usuario:.2f}')
    ax.axhline(y=Amax, color='r', linestyle='--', alpha=0.7, label=f'Límite teórico = {Amax:.3f}')
    ax.axvline(x=k_usuario, color='orange', linestyle='--', alpha=0.7, label=f'k seleccionado = {k_usuario}')
    ax.scatter([k_usuario], [A], color='red', s=100, zorder=5)
    
    ax.set_xlabel('Factor de mejora k')
    ax.set_ylabel('Aceleración A')
    ax.set_title(f'Aceleración vs Factor de mejora - {seleccion_gpu}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)