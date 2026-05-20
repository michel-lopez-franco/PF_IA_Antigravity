from typing import Protocol

import numpy as np
from numpy.typing import NDArray


class FiltroProtocol(Protocol):
    """Interfaz común para todos los filtros del curso."""

    def predecir(self) -> None:
        """Propaga estado y covarianza un paso de tiempo."""
        ...

    def actualizar(self, z: NDArray[np.float64]) -> None:
        """Incorpora observación z al estado estimado."""
        ...

    @property
    def estado(self) -> NDArray[np.float64]:
        """Estado estimado actual x̂ₖ, shape (n,)."""
        ...

    @property
    def covarianza(self) -> NDArray[np.float64]:
        """Covarianza del error Pₖ, shape (n, n). Debe ser positiva-definida."""
        ...
