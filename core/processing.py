from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go 
@dataclass
class GPU:
    f: float  # Fracción mejorable (porcentaje en decimal, ej. 0.35)
    k: int    # Factor de mejora

    def amdahl(self) -> float:
        """Calcula la aceleración A según la Ley de Amdahl."""
        return 1 / ((1 - self.f) + self.f / self.k)

    def amdahl_max(self) -> float:
        """Calcula el límite teórico de aceleración cuando k -> ∞."""
        if self.f >= 1.0:
            return float('inf')  # o algún valor muy grande para indicar límite infinito
        return 1 / (1 - self.f)

    def tiempo_optimizado(self, tiempo_original: float) -> float:
        """Calcula el tiempo optimizado dado el tiempo original."""
        return tiempo_original * ((1 - self.f) + self.f / self.k)

    def porcentaje_mejora(self, tiempo_original: float) -> float:
        """Calcula el porcentaje de mejora total."""
        tiempo_opt = self.tiempo_optimizado(tiempo_original)
        return (1 - tiempo_opt / tiempo_original) * 100

def calcular_todos_componentes():
    """Calcula A y Amax para todos los componentes de GPU."""
    componentes = {
        "Núcleos CUDA": {"f": 0.35, "k": 5},
        "Memoria VRAM": {"f": 0.20, "k": 3},
        "Unidades de texturizado": {"f": 0.25, "k": 7},
        "Interconexión NVLink": {"f": 0.20, "k": 10},
    }
    
    resultados = {}
    for nombre, datos in componentes.items():
        gpu = GPU(f=datos["f"], k=datos["k"])
        resultados[nombre] = {
            "f": datos["f"],
            "k": datos["k"],
            "A": gpu.amdahl(),
            "Amax": gpu.amdahl_max()
        }
    
    return resultados

def encontrar_mejor_componente(aceleracion_objetivo: float = 1.30):
    """Encuentra qué componente puede lograr la aceleración objetivo."""
    componentes = calcular_todos_componentes()
    
    candidatos = []
    for nombre, datos in componentes.items():
        if datos["A"] >= aceleracion_objetivo:
            candidatos.append((nombre, datos["A"]))
    
    if candidatos:
        # Ordenar por aceleración descendente
        candidatos.sort(key=lambda x: x[1], reverse=True)
        return candidatos
    else:
        return None

def graficar_A_vs_k(f_values, k_range=range(1, 16)):
    #     """
    #     Genera una figura matplotlib con la gráfica A vs k para cada f en f_values.
    #     """
    fig = go.Figure()
    colores = ["#4DD0E1", "#FFB74D", "#BA68C8", "#9575CD", "#81C784"]

    for i, f in enumerate(f_values):
        A_values = [GPU(f=f, k=k).amdahl() for k in k_range]
        fig.add_trace(go.Scatter(
            x=list(k_range),
            y=A_values,
            mode='lines+markers',
            name=f'f = {f}',
            line=dict(color=colores[i % len(colores)], width=3),
            marker=dict(size=6),
            hovertemplate="k = %{x}<br>A = %{y:.3f}<extra></extra>"
        ))

    fig.update_layout(
        title=dict(text="Aceleración A vs Factor de mejora k para distintos valores de f", x=0.5, xanchor='center'),
        xaxis=dict(title="k (Nº de procesadores)", gridcolor="#2A2A2A", color="#FFFFFF"),
        yaxis=dict(title="A (Aceleración)", gridcolor="#2A2A2A", color="#FFFFFF"),
        plot_bgcolor="#00132a", #"#00000f",
        paper_bgcolor="#01011c",
        font=dict(color="#FFFFFF"),
        legend=dict(bgcolor='#1C012D', bordercolor="#444444", borderwidth=1)
    )
    return fig  

def graficar_comparacion_componentes():
    import plotly.graph_objects as go

    componentes = calcular_todos_componentes()
    nombres = list(componentes.keys())
    A_vals = [componentes[n]["A"] for n in nombres]
    Amax_vals = [componentes[n]["Amax"] for n in nombres]

    colores_A = ['#00B8D9', '#FFB74D', '#BA68C8', '#81C784']
    colores_Amax = ['#00B8D9', '#FFB74D', '#BA68C8', '#81C784']

    # Gráfico de barras agrupadas
    fig = go.Figure(data=[
        go.Bar(
            name='Aceleración A',
            x=nombres,
            y=A_vals,
            marker_color=colores_A,
            text=[f"{a:.3f}" for a in A_vals],
            textposition='outside'
        ),
        go.Bar(
            name='Aceleración Máxima Amax',
            x=nombres,
            y=Amax_vals,
            marker_color=colores_Amax,
            opacity=0.5,
            text=[f"{a:.2f}" for a in Amax_vals],
            textposition='outside'
        )
    ])

    # Diseño del gráfico
    fig.update_layout(
        barmode='group',
        title=dict(text="Comparación de Aceleración por Componente", x=0.5,xanchor='center'),
        plot_bgcolor='#00132a',
        paper_bgcolor='#01011c',
        font=dict(color="#FFFFFF"),
        xaxis=dict(
            title='Componentes',
            tickangle=-15,
            gridcolor="#333333",
            color="#FFFFFF"
        ),
        yaxis=dict(
            title='Aceleración',
            gridcolor="#333333",
            color="#FFFFFF"
        ),
        legend=dict(
            bgcolor='#1C012D',
            bordercolor="#444444",
            borderwidth=1
        ),
        margin=dict(t=60, b=60, l=40, r=20)
    )

    return fig

def analizar_impacto_nvlink():
    """Analiza por qué NVLink tiene impacto limitado a pesar de k=10."""
    nvlink = GPU(f=0.20, k=10)
    
    # Comparar con diferentes valores de k para la misma f
    k_values = [1, 2, 3, 5, 10, 15, 20]
    aceleraciones = [GPU(f=0.20, k=k).amdahl() for k in k_values]
    
    return {
        "k_values": k_values,
        "aceleraciones": aceleraciones,
        "A_actual": nvlink.amdahl(),
        "Amax": nvlink.amdahl_max(),
        "fraccion_limitante": 0.20
    }

def comparar_texturizado_vs_vram():
    """Compara optimización de unidades de texturizado vs memoria VRAM."""
    texturizado = GPU(f=0.25, k=7)
    vram = GPU(f=0.20, k=3)
    
    return {
        "texturizado": {
            "A": texturizado.amdahl(),
            "Amax": texturizado.amdahl_max(),
            "f": 0.25,
            "k": 7
        },
        "vram": {
            "A": vram.amdahl(),
            "Amax": vram.amdahl_max(),
            "f": 0.20,
            "k": 3
        }
    }