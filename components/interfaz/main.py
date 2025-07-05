import streamlit as st
from .state import inicializar_session_state
from .analypsis import Datos

def mostrar_interfaz():
    st.set_page_config(page_title="Simulador Optimización de Hardware(GPU)")
    inicializar_session_state()

    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='margin-bottom: 0; color: white;'>S. Optimización de Hardware(GPU)</h1>
        <p style='font-size: 18px; color: gray;'>Simulador de Optimización de Hardware(GPU)</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        opciones = ["Núcleos CUDA", "Memoria VRAM", "Unidades de texturizado", "Interconexión NVLink"]
        seleccion_gpu = st.selectbox("Componente", opciones, key="gpu")

    with col2:
        porcentaje_uso = st.slider("Mejora (%)", min_value=1, max_value=100, value=35, key="f_slider")
        f = porcentaje_uso / 100

    with col3:
        k = st.number_input("Factor mejora", min_value=2, step=1, key="k_input")

    st.markdown("---")
    st.write("### Datos actuales:")
    st.write(f"- Componente: {seleccion_gpu}")
    st.write(f"- Fracción mejorable (f): {f}")
    st.write(f"- Factor de mejora (k): {k}")

    # Botones
    col_calcular, col_limpiar = st.columns([1, 1])

    with col_calcular:
        if st.button("📊 Calcular aceleración"):
            Datos(nombre=seleccion_gpu, f=f, k=k)

    with col_limpiar:
        if st.button("🧹 Limpiar datos"):
            st.session_state.resultados = None
            st.session_state.tiempo_original = 50.0

    # Mostrar resultados
    if st.session_state.resultados:
        r = st.session_state.resultados
        st.success("✅ Resultados:")
        st.write(f"- Componente: `{r['nombre']}`")
        st.write(f"- Aceleración A: `{r['A']:.4f}`")
        st.write(f"- Aceleración máxima Amax: `{r['Amax']:.4f}`")

        # Tiempo editable
        st.markdown("---")
        tiempo = st.number_input("⏱ Tiempo original (segundos)", min_value=0.0, value=st.session_state.get("tiempo_original", 50.0), step=0.5, key="tiempo_original")
        nuevo_tiempo = tiempo / r["A"]
        mejora_pct = (1 - nuevo_tiempo / tiempo) * 100

        st.info(f"🔁 Tiempo nuevo estimado: `{nuevo_tiempo:.2f} s`")
        st.info(f"📈 Mejora total estimada: `{mejora_pct:.2f}%`")