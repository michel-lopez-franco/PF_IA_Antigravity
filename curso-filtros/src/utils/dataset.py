"""Generación de datasets sintéticos reproducibles para el curso."""

import numpy as np
from numpy.typing import NDArray

_ESCENARIOS_VALIDOS = ("S1", "S2", "S3")

# Parámetros fijos del curso (data-model.md)
_Q_DEFAULT = 0.1   # varianza ruido de proceso
_R_DEFAULT = 1.0   # varianza ruido de medición
_X0 = np.array([0.0, 1.0])  # estado inicial [posición, velocidad]
_DT = 1.0


def generar_dataset(
    escenario: str,
    T: int = 200,
    seed: int = 42,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Genera (estados_verdaderos, observaciones) para el escenario dado.

    Args:
        escenario: "S1" lineal+Gaussiano, "S2" observación no lineal (rango),
                   "S3" dinámica no lineal + ruido no Gaussiano.
        T: número de pasos de tiempo.
        seed: semilla NumPy para reproducibilidad.

    Returns:
        estados: shape (T, 2) — [posición, velocidad] en cada paso.
        observaciones: shape (T, 1).

    Raises:
        ValueError: si escenario no es uno de S1, S2, S3.
    """
    if escenario not in _ESCENARIOS_VALIDOS:
        raise ValueError(
            f"Escenario '{escenario}' no válido. Opciones: {_ESCENARIOS_VALIDOS}"
        )
    rng = np.random.default_rng(seed)

    if escenario == "S1":
        return _generar_s1(rng, T)
    elif escenario == "S2":
        return _generar_s2(rng, T)
    else:
        return _generar_s3(rng, T)


def _generar_s1(
    rng: np.random.Generator, T: int
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """S1: movimiento lineal con ruido Gaussiano (modelo vehículo 1D)."""
    # F: matriz de transición cinemática
    F = np.array([[1.0, _DT], [0.0, 1.0]])
    Q_chol = np.sqrt(_Q_DEFAULT)
    R_chol = np.sqrt(_R_DEFAULT)

    estados = np.zeros((T, 2))
    observaciones = np.zeros((T, 1))
    x = _X0.copy()

    for k in range(T):
        x = F @ x + rng.normal(0.0, Q_chol, size=2)
        estados[k] = x
        observaciones[k, 0] = x[0] + rng.normal(0.0, R_chol)

    return estados.astype(np.float64), observaciones.astype(np.float64)


def _generar_s2(
    rng: np.random.Generator, T: int
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """S2: misma dinámica que S1 pero observación no lineal (rango desde origen)."""
    F = np.array([[1.0, _DT], [0.0, 1.0]])
    Q_chol = np.sqrt(_Q_DEFAULT)
    R_s2 = 0.5
    R_chol = np.sqrt(R_s2)

    estados = np.zeros((T, 2))
    observaciones = np.zeros((T, 1))
    x = _X0.copy()

    for k in range(T):
        x = F @ x + rng.normal(0.0, Q_chol, size=2)
        estados[k] = x
        # Observación: distancia euclidiana desde el origen (sensor fijo)
        rango = np.sqrt(x[0] ** 2 + 1.0)
        observaciones[k, 0] = rango + rng.normal(0.0, R_chol)

    return estados.astype(np.float64), observaciones.astype(np.float64)


def _generar_s3(
    rng: np.random.Generator, T: int
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """S3: dinámica no lineal + ruido no Gaussiano (cola pesada via Laplace)."""
    Q_s3 = 0.5
    R_chol = np.sqrt(_R_DEFAULT)

    estados = np.zeros((T, 2))
    observaciones = np.zeros((T, 1))
    x = _X0.copy()

    for k in range(T):
        # Dinámica no lineal: velocidad modulada periódicamente
        vel_new = x[1] * np.cos(0.05 * k) + rng.laplace(0.0, np.sqrt(Q_s3 / 2))
        pos_new = x[0] + x[1] * _DT + rng.laplace(0.0, np.sqrt(Q_s3 / 2))
        x = np.array([pos_new, vel_new])
        estados[k] = x
        observaciones[k, 0] = x[0] + rng.normal(0.0, R_chol)

    return estados.astype(np.float64), observaciones.astype(np.float64)
