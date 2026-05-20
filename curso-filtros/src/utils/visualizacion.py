"""Visualizaciones para filtros bayesianos — Plotly (estático) y Rerun (tiempo real)."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
from numpy.typing import NDArray


def plot_estimacion(
    estados_reales: NDArray[np.float64],
    estimados: NDArray[np.float64],
    covarianzas: NDArray[np.float64] | None = None,
    titulo: str = "Estimación de estado",
    idx_estado: int = 0,
    unidad_x: str = "pasos",
    unidad_y: str = "posición",
) -> go.Figure:
    """Figura Plotly con estado real, estimado y banda ±2σ opcional.

    Args:
        estados_reales: shape (T, n) o (T,).
        estimados: shape (T, n) o (T,).
        covarianzas: shape (T, n, n). Si se provee se dibuja banda ±2σ.
        titulo: título del gráfico.
        idx_estado: índice del estado a graficar (0=posición, 1=velocidad...).
        unidad_x: etiqueta del eje x.
        unidad_y: etiqueta del eje y.

    Returns:
        Figura Plotly exportable con write_html().
    """
    real = np.asarray(estados_reales, dtype=np.float64)
    est = np.asarray(estimados, dtype=np.float64)

    if real.ndim == 2:
        real = real[:, idx_estado]
    if est.ndim == 2:
        est = est[:, idx_estado]

    T = len(real)
    t = np.arange(T)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=real, mode="lines", name="Estado real",
                             line={"color": "black", "dash": "dot"}))
    fig.add_trace(go.Scatter(x=t, y=est, mode="lines", name="Estimado",
                             line={"color": "royalblue"}))

    if covarianzas is not None:
        covs = np.asarray(covarianzas, dtype=np.float64)
        if covs.ndim == 3:
            sigma = np.sqrt(covs[:, idx_estado, idx_estado])
        else:
            sigma = np.sqrt(covs)

        upper = est + 2 * sigma
        lower = est - 2 * sigma
        fig.add_trace(go.Scatter(
            x=np.concatenate([t, t[::-1]]),
            y=np.concatenate([upper, lower[::-1]]),
            fill="toself",
            fillcolor="rgba(65,105,225,0.15)",
            line={"color": "rgba(255,255,255,0)"},
            name="±2σ",
        ))

    fig.update_layout(
        title=titulo,
        xaxis_title=f"Tiempo [{unidad_x}]",
        yaxis_title=f"{unidad_y}",
        legend={"orientation": "h"},
    )
    return fig


def plot_particulas(
    particulas: NDArray[np.float64],
    pesos: NDArray[np.float64],
    estado_real: NDArray[np.float64] | None = None,
    titulo: str = "Distribución de partículas",
    unidad_y: str = "posición",
) -> go.Figure:
    """Figura Plotly con histograma de partículas ponderado y estado real.

    Args:
        particulas: shape (N,) o (N, n) — posición de cada partícula.
        pesos: shape (N,) — pesos normalizados.
        estado_real: escalar o array — estado verdadero (línea de referencia).
        titulo: título del gráfico.
        unidad_y: etiqueta del eje y.

    Returns:
        Figura Plotly.
    """
    parts = np.asarray(particulas, dtype=np.float64)
    w = np.asarray(pesos, dtype=np.float64)

    if parts.ndim == 2:
        parts = parts[:, 0]

    estimado = float(np.sum(parts * w))

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=parts,
        nbinsx=40,
        name="Partículas",
        marker_color="steelblue",
        opacity=0.7,
    ))
    fig.add_vline(x=estimado, line_color="royalblue", line_width=2,
                  annotation_text="Estimado", annotation_position="top right")

    if estado_real is not None:
        val = float(np.asarray(estado_real).flat[0])
        fig.add_vline(x=val, line_color="black", line_dash="dot", line_width=2,
                      annotation_text="Real", annotation_position="top left")

    fig.update_layout(
        title=titulo,
        xaxis_title=f"{unidad_y}",
        yaxis_title="Conteo",
        legend={"orientation": "h"},
    )
    return fig
