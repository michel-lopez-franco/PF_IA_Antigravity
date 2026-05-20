"""Filtro de Kalman lineal para sistemas de espacio de estados Gaussianos.

Modelo: x_{k+1} = F x_k + w_k,  w_k ~ N(0, Q)
        z_k     = H x_k + v_k,  v_k ~ N(0, R)
"""

import numpy as np
from numpy.typing import NDArray


class KalmanLineal:
    """Filtro de Kalman para sistemas lineales con ruido Gaussiano.

    Args:
        F: Matriz de transición de estado (n x n).
        H: Matriz de observación (m x n).
        Q: Covarianza del ruido de proceso (n x n), semidefinida positiva.
        R: Covarianza del ruido de medición (m x m), definida positiva.
        x0: Estado inicial (n,). Por defecto ceros.
        P0: Covarianza inicial (n x n). Por defecto identidad.
    """

    def __init__(
        self,
        F: NDArray[np.float64],
        H: NDArray[np.float64],
        Q: NDArray[np.float64],
        R: NDArray[np.float64],
        x0: NDArray[np.float64] | None = None,
        P0: NDArray[np.float64] | None = None,
    ) -> None:
        n = F.shape[0]
        m = H.shape[0]

        if F.shape != (n, n):
            raise ValueError(f"F debe ser cuadrada ({n}×{n}), recibida {F.shape}")
        if H.shape != (m, n):
            raise ValueError(f"H debe ser ({m}×{n}), recibida {H.shape}")
        if Q.shape != (n, n):
            raise ValueError(f"Q debe ser ({n}×{n}), recibida {Q.shape}")
        if R.shape != (m, m):
            raise ValueError(f"R debe ser ({m}×{m}), recibida {R.shape}")

        self._F: NDArray[np.float64] = F.astype(np.float64)
        self._H: NDArray[np.float64] = H.astype(np.float64)
        self._Q: NDArray[np.float64] = Q.astype(np.float64)
        self._R: NDArray[np.float64] = R.astype(np.float64)
        self._n: int = n
        self._m: int = m

        self._x: NDArray[np.float64] = (
            np.zeros(n, dtype=np.float64) if x0 is None else x0.astype(np.float64)
        )
        self._P: NDArray[np.float64] = (
            np.eye(n, dtype=np.float64) if P0 is None else P0.astype(np.float64)
        )

    def predecir(self) -> None:
        """Paso de predicción: propaga estado y covarianza.

        x_{k|k-1} = F x_{k-1|k-1}
        P_{k|k-1} = F P_{k-1|k-1} F^T + Q
        """
        self._x = self._F @ self._x
        self._P = self._F @ self._P @ self._F.T + self._Q

    def actualizar(self, z: NDArray[np.float64]) -> None:
        """Paso de corrección: incorpora la observación z.

        Innovación:    y    = z - H x_{k|k-1}
        Covarianza S:  S    = H P_{k|k-1} H^T + R
        Ganancia K:    K    = P_{k|k-1} H^T S^{-1}
        Actualización: x    = x_{k|k-1} + K y
                       P    = (I - K H) P_{k|k-1}

        Args:
            z: Observación con forma (m,) o (m,1).
        """
        z_flat = np.atleast_1d(z).flatten().astype(np.float64)
        if z_flat.shape != (self._m,):
            raise ValueError(
                f"z debe tener forma ({self._m},), recibida {z_flat.shape}"
            )

        y = z_flat - self._H @ self._x                          # innovación (m,)
        S = self._H @ self._P @ self._H.T + self._R             # covarianza de innovación (m x m)
        K = self._P @ self._H.T @ np.linalg.inv(S)             # ganancia de Kalman (n x m)

        self._x = self._x + K @ y                               # estado actualizado
        I_KH = np.eye(self._n, dtype=np.float64) - K @ self._H
        self._P = I_KH @ self._P                                # covarianza actualizada

        # Simetrización para evitar acumulación de error numérico
        self._P = 0.5 * (self._P + self._P.T)

    @property
    def estado(self) -> NDArray[np.float64]:
        """Estimado actual del estado (copia defensiva)."""
        return self._x.copy()

    @property
    def covarianza(self) -> NDArray[np.float64]:
        """Covarianza actual del estimado (copia defensiva)."""
        return self._P.copy()
