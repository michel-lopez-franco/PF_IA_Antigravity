# Contrato: Interfaz Python de Filtros

**Branch**: `001-curso-filtros-bayesianos` | **Date**: 2026-05-20

Todos los filtros en `src/filtros/` DEBEN implementar el `FiltroProtocol` definido
a continuación. Esto garantiza que el Módulo 5 puede comparar los cinco filtros con
la misma interfaz sin condicionales.

## Protocolo Python (src/filtros/__init__.py)

```python
from typing import Protocol
import numpy as np
from numpy.typing import NDArray

class FiltroProtocol(Protocol):
    """Interfaz común para todos los filtros del curso."""

    def predecir(self) -> None:
        """Paso de predicción: propaga estado y covarianza un paso de tiempo."""
        ...

    def actualizar(self, z: NDArray[np.float64]) -> None:
        """Paso de actualización: incorpora observación z al estado estimado."""
        ...

    @property
    def estado(self) -> NDArray[np.float64]:
        """Estado estimado actual x̂ₖ, shape (n,)."""
        ...

    @property
    def covarianza(self) -> NDArray[np.float64]:
        """Covarianza del error Pₖ, shape (n, n). Debe ser positiva-definida."""
        ...
```

## Contrato por filtro

### BayesFiltroDiscreto

```python
class BayesFiltroDiscreto:
    def __init__(
        self,
        creencia: NDArray[np.float64],       # prior, shape (N,), suma 1
        modelo_transicion: NDArray[np.float64],  # shape (N, N)
        modelo_sensor: NDArray[np.float64],       # shape (N,) dado z actual
    ) -> None: ...

    def predecir(self) -> None:
        """Chapman-Kolmogorov: creencia_pred = T @ creencia"""

    def actualizar(self, z: NDArray[np.float64]) -> None:
        """Bayes: creencia = L(z|x) * creencia_pred, normalizado"""

    @property
    def estado(self) -> NDArray[np.float64]:
        """MAP: argmax(creencia), convertido a vector shape (1,)"""

    @property
    def covarianza(self) -> NDArray[np.float64]:
        """Varianza de la distribución discreta, shape (1, 1)"""
```

### KalmanLineal

```python
class KalmanLineal:
    def __init__(
        self,
        x0: NDArray[np.float64],   # estado inicial, shape (n,)
        P0: NDArray[np.float64],   # covarianza inicial, shape (n, n)
        F: NDArray[np.float64],    # matriz de transición, shape (n, n)
        H: NDArray[np.float64],    # matriz de observación, shape (m, n)
        Q: NDArray[np.float64],    # covarianza ruido proceso, shape (n, n)
        R: NDArray[np.float64],    # covarianza ruido medición, shape (m, m)
    ) -> None: ...
```

### EKFiltro

```python
class EKFiltro:
    def __init__(
        self,
        x0: NDArray[np.float64],
        P0: NDArray[np.float64],
        f: Callable[[NDArray[np.float64]], NDArray[np.float64]],   # función de transición
        h: Callable[[NDArray[np.float64]], NDArray[np.float64]],   # función de observación
        F_jacobiano: Callable[[NDArray[np.float64]], NDArray[np.float64]],  # ∂f/∂x
        H_jacobiano: Callable[[NDArray[np.float64]], NDArray[np.float64]],  # ∂h/∂x
        Q: NDArray[np.float64],
        R: NDArray[np.float64],
    ) -> None: ...
```

### UKFiltro

```python
class UKFiltro:
    def __init__(
        self,
        x0: NDArray[np.float64],
        P0: NDArray[np.float64],
        f: Callable[[NDArray[np.float64]], NDArray[np.float64]],
        h: Callable[[NDArray[np.float64]], NDArray[np.float64]],
        Q: NDArray[np.float64],
        R: NDArray[np.float64],
        alpha: float = 1e-3,   # dispersión de sigma points
        beta: float = 2.0,     # distribución prior (2 = Gaussiana)
        kappa: float = 0.0,    # parámetro de escala secundario
    ) -> None: ...
```

### FiltroPArticulas

```python
class FiltroPArticulas:
    def __init__(
        self,
        N: int,                         # número de partículas
        x0_dist: Callable[[], NDArray[np.float64]],  # distribución inicial
        f: Callable[[NDArray[np.float64]], NDArray[np.float64]],  # dinámica
        h: Callable[[NDArray[np.float64]], NDArray[np.float64]],  # observación
        ruido_proceso: Callable[[int], NDArray[np.float64]],     # muestrador Q
        log_likelihood: Callable[[NDArray[np.float64], NDArray[np.float64]], float],
    ) -> None: ...

    @property
    def ess(self) -> float:
        """Effective Sample Size: 1 / sum(w²). Diagnóstico de degeneración."""
```

## Garantías de contrato

1. `estado` y `covarianza` son propiedades de solo lectura — no modificar directamente.
2. `covarianza` DEBE ser positiva-definida; si no lo es, el filtro DEBE lanzar `ValueError`.
3. `predecir()` y `actualizar()` son el único mecanismo de avance — no hay step().
4. Los filtros son stateful: mantienen `x̂ₖ` y `Pₖ` internamente tras cada llamada.
5. Ningún filtro importa `filterpy` o `pykalman` — son para validación externa únicamente.
