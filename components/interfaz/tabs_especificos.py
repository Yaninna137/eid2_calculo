import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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
        st.markdown("<span style='color:#cccccc; font-size:16px;'><strong>Si el renderizado tarda 50 ms originalmente:</strong></span>", unsafe_allow_html=True)
        cuda_gpu = GPU(f=0.35, k=5)
        tiempo_cuda = cuda_gpu.tiempo_optimizado(50.0)
        st.success(f"⏱️ Tiempo con núcleos CUDA optimizados: {tiempo_cuda:.2f} ms")
        
    with col11:
        st.markdown("<span style='color:#cccccc; font-size:16px;'><strong>Componente para lograr 30% de aceleración (A ≥ 1.30):</strong></span>", unsafe_allow_html=True)
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
    
    col11, _, col13 = st.columns([1, 0.01, 2])

    with col11:
        st.markdown("""
        <style>
            .bloque-analisis {{
                color: #cccccc;
                font-size: 16px;
                line-height: 1.6;
                margin-bottom: 15px;
            }}
            .bloque-analisis strong {{
                color: #ffffff;
                font-size: 17px;
            }}
        </style>
        <div class='bloque-analisis'>
            <strong>Análisis numérico:</strong><br>
            • Aceleración actual (k=10): {a_actual:.4f}<br>
            • Límite teórico: {amax:.4f}<br>
            • Fracción mejorable: {f_mejorable:.2f}
        </div>
        """.format(
            a_actual=nvlink_analisis['A_actual'],
            amax=nvlink_analisis['Amax'],
            f_mejorable=nvlink_analisis['fraccion_limitante']
        ), unsafe_allow_html=True)

        st.warning("""
        **Explicación:** A pesar de tener k=10, NVLink está limitado por su 
        fracción mejorable f=0.20. Esto significa que solo el 20% del procesamiento 
        puede beneficiarse de la optimización, limitando el impacto global.
        """)
    
    with col13:
        # Nuevo gráfico mejorado con Plotly
        k_vals = nvlink_analisis['k_values']
        A_vals = nvlink_analisis['aceleraciones']
        A_max = nvlink_analisis['Amax']
        
        fig_nvlink = go.Figure()

        # Línea A vs k
        fig_nvlink.add_trace(go.Scatter(
            x=k_vals,
            y=A_vals,
            mode='lines+markers',
            name='Aceleración (A)',
            line=dict(color='#4DD0E1', width=3),
            marker=dict(size=7, color='#00C4FF'),
            hovertemplate="k = %{x}<br>A = %{y:.3f}<extra></extra>"
        ))

        # Línea horizontal Amax
        fig_nvlink.add_trace(go.Scatter(
            x=[min(k_vals), max(k_vals)],
            y=[A_max, A_max],
            mode='lines',
            name=f'Límite teórico Amax = {A_max:.2f}',
            line=dict(color='#FF4C4C', width=2, dash='dot'),
            hoverinfo='skip'
        ))

        # Diseño visual mejorado
        fig_nvlink.update_layout(
            title="📉 Aceleración de NVLink según k",
            title_font=dict(size=18, color='#FFFFFF'),
            margin=dict(t=60, b=40, l=40, r=20),
            plot_bgcolor='#00132a',
            paper_bgcolor='#01011c',
            font=dict(color='#FFFFFF'),
            xaxis=dict(
                title="k (Factor de mejora)",
                color="#FFFFFF",
                gridcolor="#333333",
                zeroline=False
            ),
            yaxis=dict(
                title="A (Aceleración)",
                color="#FFFFFF",
                gridcolor="#333333",
                zeroline=False
            ),
            legend=dict(
                bgcolor='#1C012D',
                bordercolor='#444444',
                borderwidth=1,
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )

        st.plotly_chart(fig_nvlink, use_container_width=True)


    st.markdown("---")
    
    # Pregunta 6: Comparación Texturizado vs VRAM
    st.subheader("❓ Pregunta 6: Texturizado vs VRAM")
    st.markdown("""
    <style>
        .capsula-lista {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 8px;
            margin-bottom: 16px;
        }
        .capsula {
            background-color: #0a0a1a; /* Más profundo que #00000f */
            color: #ffffff;
            padding: 6px 16px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 500;
            box-shadow: 0 0 3px rgba(255, 255, 255, 0.1);
            width: fit-content;
        }
    </style>
    """, unsafe_allow_html=True)
    
    
    comparacion = comparar_texturizado_vs_vram()
    
    col14, col15 = st.columns(2)
        
    with col14:
        st.markdown(f"""
        <h5>Unidades de Texturizado 🎨</h5>
        <div class='capsula-lista'>
            <div class='capsula'>f = {comparacion['texturizado']['f']:.2f}</div>
            <div class='capsula'>k = {comparacion['texturizado']['k']}</div>
            <div class='capsula'>A = {comparacion['texturizado']['A']:.4f}</div>
            <div class='capsula'>Aₘₐₓ = {comparacion['texturizado']['Amax']:.4f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col15:
        st.markdown(f"""
        <h5>Memoria VRAM 💾</h5>
        <div class='capsula-lista'>
            <div class='capsula'>f = {comparacion['vram']['f']:.2f}</div>
            <div class='capsula'>k = {comparacion['vram']['k']}</div>
            <div class='capsula'>A = {comparacion['vram']['A']:.4f}</div>
            <div class='capsula'>Aₘₐₓ = {comparacion['vram']['Amax']:.4f}</div>
        </div>
        """, unsafe_allow_html=True)

    
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