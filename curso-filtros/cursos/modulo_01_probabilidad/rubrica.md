# Rúbrica de Evaluación — Módulo 1: Fundamentos de Probabilidad e Inferencia Bayesiana

**Módulo**: `modulo_01` | **Versión**: 1.0 | **Fecha**: 2026-05-20

---

## Criterios de evaluación

### R-M1-01: Normalización del posterior

**Descripción**: El posterior calculado por el estudiante debe ser una distribución de probabilidad válida: suma/integra a 1.

**Método de verificación**:
```python
# Caso discreto (grilla de theta)
assert abs(posterior_array.sum() - 1.0) < 1e-6, "Posterior no normalizado"

# Caso Beta-Binomial (verificación analítica)
from scipy import stats
alpha_n = alpha_0 + k_caras
beta_n  = beta_0  + k_soles
# Beta está normalizada por definición; verificar parámetros positivos
assert alpha_n > 0 and beta_n > 0, "Parámetros de la Beta deben ser positivos"
assert abs(stats.beta.mean(alpha_n, beta_n) - alpha_n / (alpha_n + beta_n)) < 1e-10
```

**Tolerancia**: diferencia absoluta $< 10^{-6}$ para integrales numéricas; $< 10^{-10}$ para cómputos analíticos.

**Nivel**: Base (todos los estudiantes).

---

### R-M1-02: Monotonicidad con evidencia acumulada

**Descripción**: Con observaciones que superan la mitad de los ensayos siendo "caras" ($k/n > 0.5$), la media posterior debe ser estrictamente mayor que la media del prior. Si $k/n < 0.5$, la media posterior debe ser menor que la del prior. La creencia se mueve en la dirección de los datos.

**Método de verificación**:
```python
# Con theta_real = 0.7 y N_OBS = 30, esperamos E[θ|datos] > E[prior]
E_prior    = alpha_0 / (alpha_0 + beta_0)          # media del prior
E_posterior = alpha_n / (alpha_n + beta_n)          # media del posterior

fraccion_caras = k_caras / N_OBS
if fraccion_caras > E_prior:
    assert E_posterior > E_prior, (
        f"Posterior {E_posterior:.4f} debería > prior {E_prior:.4f} "
        f"cuando {fraccion_caras:.2f} > {E_prior:.2f}"
    )
elif fraccion_caras < E_prior:
    assert E_posterior < E_prior, (
        f"Posterior {E_posterior:.4f} debería < prior {E_prior:.4f} "
        f"cuando {fraccion_caras:.2f} < {E_prior:.2f}"
    )
```

**Tolerancia**: verificación de desigualdad estricta (sin tolerancia numérica).

**Nivel**: Base (todos los estudiantes).

---

### R-M1-03: Convergencia con evidencia infinita

**Descripción**: A medida que el número de observaciones $n \to \infty$ con proporción fija de caras $p = k/n$, la media y la moda del posterior convergen al verdadero $\theta_{\text{real}}$. Con $n$ grande (≥ 1000), la diferencia $|E[\theta \mid \text{datos}] - \theta_{\text{real}}| < 0.01$.

**Método de verificación**:
```python
import numpy as np
rng = np.random.default_rng(42)
theta_real = 0.7
N_grande   = 1000
obs_grandes = rng.binomial(1, theta_real, size=N_grande)

alpha_inf = alpha_0 + obs_grandes.sum()
beta_inf  = beta_0  + (N_grande - obs_grandes.sum())
E_inf     = alpha_inf / (alpha_inf + beta_inf)

assert abs(E_inf - theta_real) < 0.01, (
    f"Con n={N_grande}, E[θ|datos]={E_inf:.4f} debe estar a <0.01 de θ_real={theta_real}"
)
```

**Tolerancia**: $|E[\theta \mid \text{datos}] - \theta_{\text{real}}| < 0.01$ con $n \geq 1000$.

**Nivel**: Base para la observación cualitativa; nivel avanzado para la verificación cuantitativa.
