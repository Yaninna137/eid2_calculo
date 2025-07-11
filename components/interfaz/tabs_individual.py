import streamlit as st
import matplotlib.pyplot as plt
from core.processing import GPU
from .layout import get_datos_componentes
import plotly.graph_objects as go

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
    k_range = list(range(1, 21))
    A_values = [GPU(f=f_usuario, k=k).amdahl() for k in k_range]

    # Crear figura Plotly
    fig = go.Figure()

    # Línea A vs k
    fig.add_trace(go.Scatter(
        x=k_range,
        y=A_values,
        mode='lines+markers',
        name=f'f = {f_usuario:.2f}',
        line=dict(color='#4DD0E1', width=3),
        marker=dict(size=6),
        hovertemplate='k=%{x}<br>A=%{y:.3f}<extra></extra>'
    ))

    # Línea límite Amax
    fig.add_trace(go.Scatter(
        x=[min(k_range), max(k_range)],
        y=[Amax]*2,
        mode='lines',
        name=f'Límite teórico = {Amax:.3f}',
        line=dict(color='red', width=2, dash='dash')
    ))

    # Línea vertical k seleccionado
    fig.add_trace(go.Scatter(
        x=[k_usuario, k_usuario],
        y=[0, max(A_values)],
        mode='lines',
        name=f'k seleccionado = {k_usuario}',
        line=dict(color='orange', width=2, dash='dot')
    ))

    # Punto seleccionado
    fig.add_trace(go.Scatter(
        x=[k_usuario],
        y=[A],
        mode='markers+text',
        marker=dict(color='red', size=10),
        text=[f"A = {A:.3f}"],
        textposition="top center",
        showlegend=False
    ))

    # Diseño general
    fig.update_layout(
        title=dict(text=f"Aceleración vs Factor de mejora - {seleccion_gpu}", x=0.5, xanchor='center'),
        xaxis=dict(title='Factor de mejora k', gridcolor="#333333", color="#FFFFFF"),
        yaxis=dict(title='Aceleración A', gridcolor="#333333", color="#FFFFFF",dtick=0.2),
        plot_bgcolor="#00132a",
        paper_bgcolor="#01011c",
        font=dict(color="#FFFFFF"),
        legend=dict(
            bgcolor="#1C012D",
            bordercolor="#444",
            borderwidth=1
        ),
        margin=dict(t=40, b=40, l=40, r=20)
    )

    # Mostrar gráfico
    st.plotly_chart(fig, use_container_width=True)
