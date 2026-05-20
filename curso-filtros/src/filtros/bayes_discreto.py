"""Filtro bayesiano discreto sobre grilla 1D.

Implementa el ciclo predict/update del filtro bayesiano para espacios de
estados discretos finitos. Modelo de sensor Gaussiano centrado en el estado.
"""

import numpy as np
from numpy.typing import NDArray
from scipy import stats


class BayesFiltroDiscreto:
    """Filtro bayesiano discreto (grilla 1D).

    Mantiene una distribución de creencia (belief) sobre N estados discretos
    y la actualiza con el ciclo predicción-corrección bayesiano.

    Args:
        grilla: Array 1D de N valores de estado (posiciones del espacio discreto).
        T_matrix: Matriz de transición NxN donde T[i, j] = P(x'=i | x=j).
        sigma_sensor: Desviación estándar del ruido del sensor (modelo Gaussiano).
        prior: Distribución inicial. Si es None, se usa uniforme normalizada.
    """

    def __init__(
        self,
        grilla: NDArray[np.float64],
        T_matrix: NDArray[np.float64],
        sigma_sensor: float,
        prior: NDArray[np.float64] | None = None,
    ) -> None:
        n = grilla.shape[0]
        if T_matrix.shape != (n, n):
            raise ValueError(f"T_matrix debe ser ({n},{n}), recibida {T_matrix.shape}")
        if sigma_sensor <= 0.0:
            raise ValueError(f"sigma_sensor debe ser > 0, recibida {sigma_sensor}")

        self._grilla: NDArray[np.float64] = grilla.astype(np.float64)
        self._T: NDArray[np.float64] = T_matrix.astype(np.float64)
        self._sigma: float = float(sigma_sensor)

        if prior is None:
            self._belief: NDArray[np.float64] = np.ones(n, dtype=np.float64) / n
        else:
            if prior.shape != (n,):
                raise ValueError(f"prior debe tener forma ({n},), recibida {prior.shape}")
            total = prior.sum()
            if total <= 0.0:
                raise ValueError("prior no puede ser todo cero")
            self._belief = (prior / total).astype(np.float64)

    def predecir(self) -> None:
        """Paso de predicción: Chapman-Kolmogorov.

        bel_bar[x'] = Σ_x  P(x' | x) · bel[x]
        En forma matricial: bel_bar = T @ bel
        """
        self._belief = self._T @ self._belief

    def actualizar(self, z: NDArray[np.float64]) -> None:
        """Paso de corrección: regla de Bayes con sensor Gaussiano.

        bel[x'] = η · P(z | x') · bel_bar[x']

        Args:
            z: Observación escalar empaquetada en array shape (1,).

        Raises:
            ValueError: Si el posterior colapsa a cero (likelihood demasiado estrecha).
        """
        obs = float(z[0])
        likelihood: NDArray[np.float64] = stats.norm.pdf(
            self._grilla, loc=obs, scale=self._sigma
        ).astype(np.float64)
        unnorm = likelihood * self._belief
        total = float(unnorm.sum())
        if total < 1e-300:
            raise ValueError(
                f"El posterior colapsó a cero — observación z={obs:.4f} es imposible "
                f"dado el prior actual (sigma_sensor={self._sigma})"
            )
        self._belief = unnorm / total

    @property
    def estado(self) -> NDArray[np.float64]:
        """Estimado MAP: posición de la grilla con mayor probabilidad."""
        return np.array([self._grilla[int(np.argmax(self._belief))]], dtype=np.float64)

    @property
    def covarianza(self) -> NDArray[np.float64]:
        """Varianza de la distribución de creencia como matriz 1x1."""
        mu = float(np.dot(self._grilla, self._belief))
        var = float(np.dot((self._grilla - mu) ** 2, self._belief))
        return np.array([[var]], dtype=np.float64)

    @property
    def belief(self) -> NDArray[np.float64]:
        """Distribución de creencia completa (copia defensiva)."""
        return self._belief.copy()
