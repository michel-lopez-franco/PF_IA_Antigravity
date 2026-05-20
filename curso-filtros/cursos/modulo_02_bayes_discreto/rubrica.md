# Rúbrica de Evaluación — Módulo 2: Filtro Bayesiano Discreto

**Módulo**: `modulo_02` | **Versión**: 1.0 | **Fecha**: 2026-05-20

---

## Criterios de evaluación

### R-M2-01: Normalización del belief en cada paso

**Descripción**: En cada paso del filtro (tanto tras predicción como tras corrección), la suma del vector belief debe ser exactamente 1. La normalización es condición necesaria para que el belief sea una distribución de probabilidad válida.

**Método de verificación**:
```python
# Verificar normalización tras cada paso de corrección
for k in range(T_PASOS):
    assert abs(history_belief[k].sum() - 1.0) < 1e-6, (
        f"Belief en paso k={k} no normalizado: suma = {history_belief[k].sum():.8f}"
    )
```

**Tolerancia**: suma del belief $\in [1 - 10^{-6},\ 1 + 10^{-6}]$ en cada paso.

**Nivel**: Base (todos los estudiantes).

---

### R-M2-02: RMSE del estimado MAP

**Descripción**: El RMSE del estimado MAP (posición del máximo del belief en cada paso) respecto al estado real debe ser menor que 2.0 celdas sobre el dataset estándar (N=20, T=100, σ_mov=1.0, σ_sensor=1.5). La implementación se compara contra la referencia de filterpy con tolerancia $10^{-6}$.

**Método de verificación**:
```python
from src.utils.metricas import rmse as calcular_rmse
import numpy as np

rmse_student = float(np.sqrt(np.mean((estimados_student - estados_reales)**2)))
assert rmse_student < 2.0, f"RMSE {rmse_student:.4f} ≥ 2.0 — el filtro no converge"

# Comparación con referencia filterpy (si disponible)
# assert abs(rmse_student - rmse_ref) < 1e-6
```

**Tolerancia**: RMSE < 2.0 (criterio independiente); diferencia con referencia $< 10^{-6}$ (criterio de equivalencia).

**Nivel**: Base para RMSE < 2.0; nivel avanzado para equivalencia con filterpy.

---

### R-M2-03: Convergencia del belief en menos de T/2 pasos

**Descripción**: El filtro debe convergir (primer paso donde el error MAP < 2 celdas) en menos de la mitad del tiempo total de la simulación. Para T=100, la convergencia debe ocurrir antes del paso 50.

**Método de verificación**:
```python
# Encontrar el primer paso donde el error MAP < 2 celdas
errores_k = np.abs(estimados_student - estados_reales)
conv_steps = np.where(errores_k < 2.0)[0]
assert len(conv_steps) > 0, "El filtro no convergió en ningún paso"

conv_step = int(conv_steps[0])
assert conv_step < T_PASOS // 2, (
    f"Convergencia en paso {conv_step} ≥ T/2={T_PASOS//2} — el filtro converge demasiado lento"
)
print(f"Convergencia en paso {conv_step} < T/2={T_PASOS//2}  ✓")
```

**Tolerancia**: primer paso con error < 2 celdas debe ser < 50 (con los parámetros estándar del notebook).

**Nivel**: Base (criterio verificable numéricamente en el notebook práctico).
