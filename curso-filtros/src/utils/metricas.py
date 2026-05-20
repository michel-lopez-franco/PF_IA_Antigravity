"""Métricas de evaluación para filtros bayesianos."""

import numpy as np
from numpy.typing import NDArray


def rmse(
    estimados: NDArray[np.float64],
    reales: NDArray[np.float64],
) -> float:
    """Raíz del error cuadrático medio entre estimados y reales.

    Args:
        estimados: shape (T,) o (T, n).
        reales: misma shape que estimados.

    Returns:
        RMSE escalar (float).
    """
    diff = np.asarray(estimados, dtype=np.float64) - np.asarray(reales, dtype=np.float64)
    return float(np.sqrt(np.mean(diff**2)))


def nees(
    estimados: NDArray[np.float64],
    reales: NDArray[np.float64],
    covarianzas: NDArray[np.float64],
) -> float:
    """Error cuadrático normalizado promedio (NEES).

    Un filtro consistente tiene NEES ≈ n (dimensión del estado).

    Args:
        estimados: shape (T, n) — estados estimados.
        reales: shape (T, n) — estados verdaderos.
        covarianzas: shape (T, n, n) — covarianzas estimadas.

    Returns:
        NEES escalar promediado sobre T pasos.
    """
    est = np.asarray(estimados, dtype=np.float64)
    real = np.asarray(reales, dtype=np.float64)
    covs = np.asarray(covarianzas, dtype=np.float64)

    T = est.shape[0]
    nees_sum = 0.0
    for k in range(T):
        e = real[k] - est[k]
        P_inv = np.linalg.inv(covs[k])
        nees_sum += float(e @ P_inv @ e)
    return nees_sum / T


def ess(pesos: NDArray[np.float64]) -> float:
    """Tamaño efectivo de muestra (Effective Sample Size).

    ESS = 1 / Σwᵢ². Para pesos uniformes: ESS = N.
    Para degeneración total (un peso = 1): ESS = 1.

    Args:
        pesos: shape (N,) — pesos normalizados (suman 1).

    Returns:
        ESS escalar en (0, N].
    """
    w = np.asarray(pesos, dtype=np.float64)
    return float(1.0 / np.sum(w**2))
