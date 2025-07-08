from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np

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
        A = self.amdahl()
        return tiempo_original / A

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
    """
    Genera una figura matplotlib con la gráfica A vs k para cada f en f_values.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for f in f_values:
        A_values = [GPU(f=f, k=k).amdahl() for k in k_range]
        ax.plot(list(k_range), A_values, label=f'f = {f}', linewidth=2, marker='o')
    
    ax.set_xlabel('Factor de mejora k', fontsize=12)
    ax.set_ylabel('Aceleración A', fontsize=12)
    ax.set_title('Aceleración A vs Factor de mejora k para distintos valores de f', fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1, 15)
    
    return fig

def graficar_comparacion_componentes():
    """Genera gráfica comparativa de todos los componentes."""
    componentes = calcular_todos_componentes()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Gráfico 1: Aceleración A
    nombres = list(componentes.keys())
    aceleraciones = [componentes[nombre]["A"] for nombre in nombres]
    
    bars1 = ax1.bar(range(len(nombres)), aceleraciones, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    ax1.set_xlabel('Componentes')
    ax1.set_ylabel('Aceleración A')
    ax1.set_title('Aceleración por Componente')
    ax1.set_xticks(range(len(nombres)))
    ax1.set_xticklabels([nombre.split()[0] for nombre in nombres], rotation=45)
    ax1.grid(True, alpha=0.3)
    
    # Añadir valores sobre las barras
    for bar, valor in zip(bars1, aceleraciones):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01,
                f'{valor:.3f}', ha='center', va='bottom')
    
    # Gráfico 2: Límite teórico Amax
    amax_values = [componentes[nombre]["Amax"] for nombre in nombres]
    
    bars2 = ax2.bar(range(len(nombres)), amax_values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    ax2.set_xlabel('Componentes')
    ax2.set_ylabel('Aceleración Máxima Amax')
    ax2.set_title('Límite Teórico por Componente')
    ax2.set_xticks(range(len(nombres)))
    ax2.set_xticklabels([nombre.split()[0] for nombre in nombres], rotation=45)
    ax2.grid(True, alpha=0.3)
    
    # Añadir valores sobre las barras
    for bar, valor in zip(bars2, amax_values):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.05,
                f'{valor:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
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