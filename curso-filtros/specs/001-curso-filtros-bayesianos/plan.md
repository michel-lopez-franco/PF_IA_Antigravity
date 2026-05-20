# Implementation Plan: Curso Completo de Filtros Bayesianos

**Branch**: `001-curso-filtros-bayesianos` | **Date**: 2026-05-20 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-curso-filtros-bayesianos/spec.md`

## Summary

Construir un curso completo de Filtros Bayesianos en cinco módulos (Probabilidad, Bayes
Discreto, Familia Kalman, Partículas, Proyecto Integrador) para audiencia mixta (carrera +
posgrado). Cada módulo entrega un notebook teórico y uno práctico con derivaciones sin saltos,
simulaciones reproducibles (seed fijo), validación numérica automática y evaluación autoguiada.
El código fuente de los filtros vive en `src/filtros/` (Python 3.12+, mypy --strict); los
notebooks usan exclusivamente NumPy/SciPy para implementar y Plotly/Rerun para visualizar.

## Technical Context

**Language/Version**: Python 3.12+ (constitution-mandated)

**Primary Dependencies**:
- `numpy` ≥ 2.0, `scipy` ≥ 1.13 — implementación de filtros y álgebra lineal
- `plotly` ≥ 5.22 — visualizaciones estáticas en notebooks (constitution Principio V)
- `rerun-sdk` ≥ 0.16 — animaciones en tiempo real, paso a paso de filtros (Principio V)
- `jupyter`, `nbconvert` — ejecución y exportación de notebooks
- `nbval` — pruebas automatizadas de notebooks en CI (constitution Toolchain)
- `filterpy`, `pykalman` — referencia de validación únicamente (celdas marcadas, FR-006)
- `sqlite3` stdlib — persistencia local de progreso y caché de resultados (Principio III)

**Storage**: SQLite local — `filtros.db` en raíz del repositorio (constitution-mandated, no cloud)

**Testing**: `pytest` + `pytest-cov` (coverage ≥ 80%) + `nbval` en todos los notebooks

**Target Platform**: Jupyter Notebook / JupyterLab local, Linux / macOS / Windows, sin GPU

**Project Type**: course-module + biblioteca Python + CLI

**Performance Goals**: Cada notebook ejecuta "Run All" en < 60 segundos en hardware estándar
de estudiante; dataset sintético ≤ 1000 puntos por simulación

**Constraints**: Sin cloud, sin descarga de datos externos, implementaciones con NumPy/SciPy
únicamente (filterpy/pykalman solo en celdas de validación marcadas)

**Scale/Scope**: 5 módulos (módulo 3 con 3 sub-módulos), 14 notebooks, 5 implementaciones
de filtros, 5 rúbricas, 1 glosario, 1 CLI

## Constitution Check

*GATE: Debe pasar antes de Phase 0. Re-verificar tras Phase 1.*

| Principio | Requerimiento | Estado |
|-----------|---------------|--------|
| I — Tipado estático | `mypy --strict` en todo `src/` | ✅ Diseño respeta: interfaces tipadas con Protocol |
| II — Tests obligatorios | pytest ≥ 80% cobertura + nbval | ✅ tests/ cubre src/; CI ejecuta nbval |
| III — SQLite local | `filtros.db` local, sin cloud | ✅ Solo sqlite3 stdlib, sin ORM externo |
| IV — UX comandos cortos | `filtros run`, `filtros plot` ≤ 3 tokens | ✅ CLI en src/cli/main.py con typer |
| V — Plotly / Rerun | Plotly = estático, Rerun = tiempo real | ✅ Notebooks usan Plotly; demo en tiempo real usa Rerun |
| VI — YAGNI | Sin abstracciones especulativas | ✅ Cada filtro es clase independiente, sin jerarquía prematura |
| VII — Rigor matemático | Derivaciones completas | ✅ Plan incluye secciones de derivación paso a paso |
| VIII — 50/50 | 1 notebook teórico + 1 práctico por módulo | ✅ |
| IX — Estructura de módulo | 7 secciones obligatorias | ✅ Plantillas en plantillas/ |
| X — Notebooks ejecutables | Run All sin intervención | ✅ nbval en CI |
| XI — Reproducibilidad | np.random.seed(42) en celda 1 | ✅ Convención de notebooks enforced |
| XII — Validación numérica | Celda de validación vs filterpy/scipy | ✅ FR-006 |
| XIII — Criterios medibles | assert en ejercicios | ✅ |
| XIV — Errores comunes | ≥ 2 por módulo | ✅ |
| XV — Español técnico | Todo en español, términos EN definidos | ✅ |
| XVI — Cierre reflexivo | ¿Qué aprendiste? + ¿Qué sigue? | ✅ Últimas celdas de cada notebook |

**Veredicto del gate**: PASS — sin violaciones. Sin entradas en Complexity Tracking.

## Arquitectura Pedagógica por Módulo

### Módulo 1: Fundamentos de Probabilidad e Inferencia Bayesiana

**Objetivo central**: El estudiante puede enunciar y aplicar el Teorema de Bayes en casos
discretos y continuos, y distinguir prior, likelihood y posterior con interpretación probabilística
correcta.

**Prerequisitos externos** (al curso): Cálculo integral, álgebra lineal básica, Python con NumPy.

**Contenido teórico** (notebook `01_teoria.ipynb`):
1. Probabilidad condicional y regla de la cadena
2. Teorema de Bayes (derivación desde axiomas de Kolmogorov)
3. Distribuciones discretas (Bernoulli, Binomial) con ejemplos
4. Variables aleatorias continuas: Gaussiana, media, varianza, convolucion
5. Inferencia bayesiana: ciclo prior → likelihood → posterior → prior actualizado
6. Caso conjugado Gaussiano: derivación analítica

**Contenido práctico** (notebook `02_practica.ipynb`):
- Simulación de lanzamiento de moneda sesgada con actualización bayesiana secuencial
- Visualización Plotly de evolución del posterior con cada observación
- Ejercicio guiado: dado prior Beta(2,2) y 10 observaciones, calcular posterior analítico
- Reto: implementar estimación bayesiana de la media gaussiana con prior Gaussiano conjugado

**Evaluación**: 3 problemas de inferencia con solución analítica + tolerancia 1e-4

---

### Módulo 2: Filtro Bayesiano Discreto

**Objetivo central**: El estudiante implementa el ciclo predict/update del filtro bayesiano
discreto y observa convergencia de la distribución de creencia (belief) en un sistema de
seguimiento 1D con estado discreto.

**Prerequisitos**: Módulo 1 completo (Bayes, distribuciones, ciclo prior–posterior).

**Contenido teórico** (notebook `01_teoria.ipynb`):
1. Modelo de espacio de estados discreto: {x_k, z_k, estado oculto}
2. Ecuación de Chapman-Kolmogorov (paso de predicción): derivación
3. Regla de Bayes aplicada a la medición (paso de actualización)
4. Normalización de la distribución de creencia
5. Ejemplo binario (puerta): derivación completa con tablas numéricas paso a paso
6. Extensión a estado N-dimensional discreto (seguimiento en grilla)

**Contenido práctico** (notebook `02_practica.ipynb`):
- Dataset sintético: seguimiento en grilla 1D de 20 posiciones, T=100 pasos
- Implementación `BayesFiltroDiscreto` en NumPy (predict + update)
- Validación contra `filterpy.discrete_bayes`
- Visualización Plotly: mapa de calor belief(t, x) mostrando convergencia
- Ejercicio guiado: implementar modelo de movimiento y modelo de sensor
- Reto: sistema con múltiples agentes en grilla (belief multimodal)

**Evaluación**: RMSE de la estimación MAP vs. estado verdadero < 2.0 en dataset estándar

---

### Módulo 3: Familia Kalman — Sub-módulo 3a (Kalman Lineal)

**Objetivo central**: El estudiante deriva y implementa el filtro de Kalman para sistemas
lineales Gaussianos y verifica optimidad (MMSE).

**Prerequisitos**: Módulos 1–2, álgebra matricial, gaussianas multivariadas.

**Contenido teórico** (notebook `3a/01_teoria.ipynb`):
1. Modelo de espacio de estados lineal: xₖ = Fxₖ₋₁ + Bwₖ, zₖ = Hxₖ + vₖ
2. Propagación de gaussiana multivariada (predict): derivación covariance prediction
3. Actualización: ganancia de Kalman K derivada desde criterio MMSE
4. Ecuaciones de Riccati y estado estacionario
5. Ejemplo numérico: seguimiento 1D posición-velocidad, 5 pasos con matrices concretas

**Contenido práctico** (notebook `3a/02_practica.ipynb`):
- Dataset: vehículo 1D, velocidad constante, Q=0.1, R=1.0, T=200
- `KalmanLineal` en NumPy: predict(), update(), estado(), covarianza()
- Validación contra `filterpy.KalmanFilter`
- Plotly: trayectoria estimada vs. real + banda de incertidumbre (±2σ)
- Ejercicio: ajustar Q y R manualmente y observar efecto en el filtro
- Reto: implementar filtro de información (forma alternativa del Kalman)

---

### Módulo 3: Sub-módulo 3b (Filtro de Kalman Extendido — EKF)

**Objetivo central**: El estudiante lineariza funciones no lineales via Jacobiano y entiende
cuándo esta aproximación falla.

**Prerequisitos**: 3a completo, derivadas parciales y cálculo Jacobiano.

**Contenido teórico** (notebook `3b/01_teoria.ipynb`):
1. Recordatorio de Jacobiano: definición, cálculo para f: Rⁿ → Rᵐ (3 ejemplos)
2. Modelo no lineal: xₖ = f(xₖ₋₁) + wₖ, zₖ = h(xₖ) + vₖ
3. Linealización de primer orden: Fₖ = ∂f/∂x|ₓ̂, Hₖ = ∂h/∂x|ₓ̂
4. EKF predict y update con Jacobianos
5. Análisis de error de aproximación: cuándo el EKF diverge
6. Ejemplo numérico: sensor de rango (z = √(x² + y²) + ruido)

**Contenido práctico** (notebook `3b/02_practica.ipynb`):
- Dataset: vehículo 2D con medición de rango (no lineal), T=200
- `EKFiltro` en NumPy: Jacobiano analítico computado, predict(), update()
- Validación contra `filterpy.ExtendedKalmanFilter`
- Plotly: trayectoria 2D con incertidumbre elipsoidal
- Ejercicio: introducir no-linealidad fuerte y observar divergencia del EKF
- Reto: implementar EKF con Jacobiano numérico (diferencias finitas)

---

### Módulo 3: Sub-módulo 3c (Filtro de Kalman Unscented — UKF)

**Objetivo central**: El estudiante entiende y deriva la transformada unscented y comprueba
que captura estadísticas de segundo orden mejor que la linealización.

**Prerequisitos**: 3a, 3b completos; esperanza de funciones no lineales.

**Contenido teórico** (notebook `3c/01_teoria.ipynb`):
1. Motivación: limitación del EKF con no-linealidades fuertes
2. Transformada Unscented: idea central (propagar puntos, no funciones)
3. Selección de sigma points: 2n+1 puntos, parámetros α, β, κ — derivación
4. Cómputo de pesos Wₘ y Wc
5. UKF predict y update completo
6. Comparación UKF vs EKF: error de aproximación en 2D con curvaturas
7. Ejemplo numérico: mismo dataset 3b con ambos métodos

**Contenido práctico** (notebook `3c/02_practica.ipynb`):
- Dataset: mismo vehículo 2D (rango), mismo seed → comparación directa con EKF
- `UKFiltro` en NumPy: sigma_points(), unscented_transform(), predict(), update()
- Validación contra `filterpy.UnscentedKalmanFilter`
- Plotly: overlay UKF vs EKF vs estado real para comparación visual
- Ejercicio: variar parámetro α y observar efecto en dispersión de sigma points
- Reto: UKF con función de observación bearing-only (ángulo, sin distancia)

---

### Módulo 4: Filtro de Partículas (Sequential Monte Carlo)

**Objetivo central**: El estudiante implementa un filtro de partículas con remuestreo y
entiende cuándo supera a los filtros de la familia Kalman.

**Prerequisitos**: Módulos 1–3 completos; muestreo Monte Carlo básico.

**Contenido teórico** (notebook `01_teoria.ipynb`):
1. Motivación: distribuciones no-Gaussianas, multimodales, discontinuas
2. Importancia muestral: distribución propuesta q(x) y pesos de importancia
3. Algoritmo SIR: sequential importance resampling, pseudocódigo
4. Degeneración de partículas: diagnóstico via ESS (Effective Sample Size)
5. Estrategias de remuestreo: multinomial, sistemático, residual
6. Problema del localizador de robots: por qué Kalman falla aquí
7. Ejemplo numérico: 100 partículas, sistema bimodal, T=50 pasos

**Contenido práctico** (notebook `02_practica.ipynb`):
- Dataset: sistema no lineal con ruido no Gaussiano (mixtura), T=200
- `FiltroPArticulas` en NumPy: inicializar, propagar, pesar, remuestrear
- Validación visual contra distribución verdadera (scipy.stats)
- Plotly: animación snapshot de partículas en t=10, 50, 100, 200
- Rerun: animación en tiempo real del cloud de partículas convergiendo
- Ejercicio: reducir N partículas de 1000 a 50 y observar degradación
- Reto: implementar remuestreo adaptativo (remuestrear solo si ESS < N/2)

---

### Módulo 5: Proyecto Integrador Comparativo

**Notebook guiado** (`01_proyecto_guiado.ipynb`) — evaluación base:
- Sección 1: Dataset unificado — tres escenarios (lineal-Gaussiano, mildly nonlinear,
  strongly nonlinear/non-Gaussian) generados con seed=42
- Sección 2: Ejecución de los 5 filtros (Bayes discreto, Kalman, EKF, UKF, Partículas)
  sobre los 3 escenarios con andamiaje — celdas con firma de función provista
- Sección 3: Tabla comparativa (RMSE, varianza del error, tiempo de cómputo)
- Sección 4: Sub-análisis familia Kalman (lineal vs EKF vs UKF)
- Sección 5: Justificación guiada — 6 preguntas estructuradas con espacio de respuesta
- Sección 6: ¿Qué aprendiste? + ¿Qué sigue?

**Extensión abierta** (`02_extension_abierta.ipynb`) — reto opcional posgrado:
- Plantilla mínima: celda de contexto, seed, sin andamiaje
- El estudiante define el problema, selecciona filtros, implementa, compara y justifica
- La rúbrica evalúa: coherencia de supuestos, corrección de implementación,
  calidad del argumento de selección

## Estructura Estándar de Notebooks

### Plantilla: Notebook Teórico (`plantillas/plantilla_teoria.ipynb`)

| # | Tipo | Contenido obligatorio |
|---|------|-----------------------|
| 1 | Markdown | Header: título, módulo, tipo=TEÓRICO, fecha |
| 2 | Markdown | `## Objetivos de aprendizaje` — lista numerada ≥ 3 items |
| 3 | Markdown | `## Prerequisitos` — lista con vínculos a módulos anteriores |
| 4 | Code | Imports + `np.random.seed(42)` + verificación de versiones |
| 5 | Markdown | `## Intuición` — explicación informal, sin fórmulas |
| 6–N | Markdown+Code | `## Derivación formal` — celdas alternadas: texto matemático + código de verificación |
| N+1 | Code+Markdown | `## Ejemplo numérico paso a paso` — valores concretos, cada operación comentada |
| N+2 | Markdown | `## Errores comunes` — ≥ 2 errores con síntoma / diagnóstico / solución |
| N+3 | Markdown | `## ¿Qué aprendiste?` — ≥ 5 bullets en primera persona plural |
| N+4 | Markdown | `## ¿Qué sigue?` — módulo siguiente + cómo este módulo lo habilita |

### Plantilla: Notebook Práctico (`plantillas/plantilla_practica.ipynb`)

| # | Tipo | Contenido obligatorio |
|---|------|-----------------------|
| 1 | Markdown | Header: título, módulo, tipo=PRÁCTICO, fecha |
| 2 | Markdown | `## Objetivos de práctica` + `## Prerequisitos` |
| 3 | Code | `np.random.seed(42)` + imports + `assert sys.version_info >= (3, 12)` |
| 4 | Code | Generación del dataset sintético (función `generar_dataset`) |
| 5 | Code | **[CELDA DE VALIDACIÓN — NO MODIFICAR]** Referencia filterpy/scipy |
| 6–M | Code+Markdown | Implementación del filtro (celdas con andamiaje `# TODO:`) |
| M+1 | Code | `## Validación numérica` — `assert abs(rmse_student - rmse_ref) < TOL` |
| M+2 | Code+Markdown | `## Ejercicios guiados` — ejercicio base con andamiaje |
| M+3 | Code+Markdown | `## Reto` (opcional) — sin andamiaje, criterio de éxito en comentario |
| M+4 | Markdown | `## ¿Qué aprendiste?` + `## ¿Qué sigue?` |

## Convenciones de Notebooks

### Orden de celdas
- La celda 1 SIEMPRE es markdown de encabezado (no code).
- La celda de seed SIEMPRE es la primera celda de código, antes de cualquier importación.
- Las celdas de validación marcadas `[CELDA DE VALIDACIÓN — NO MODIFICAR]` DEBEN aparecer
  ANTES de la implementación del estudiante para que el número de referencia esté disponible.
- Ninguna celda depende de output de una celda con índice mayor (nunca hacia adelante).

### Semilla y reproducibilidad
```python
# Celda 1 de código — siempre igual en todos los notebooks
import numpy as np
import sys
np.random.seed(42)
assert sys.version_info >= (3, 12), f"Se requiere Python 3.12+, tienes {sys.version}"
```

### Estándares de visualización (Plotly)
Toda figura Plotly DEBE incluir:
```python
fig.update_layout(
    title="<Título descriptivo>",
    xaxis_title="<Variable> [<unidad>]",
    yaxis_title="<Variable> [<unidad>]",
)
```
Si hay más de una serie: `fig.add_trace(..., name="<Nombre de serie>")` obligatorio.
Exportación: `fig.write_html("output/<nombre>.html")` al final de cada celda de figura.

### Pruebas de consistencia automáticas
Cada notebook práctico incluye al final una celda de smoke-test:
```python
# Smoke-test — se ejecuta automáticamente con nbval
assert rmse_student < rmse_umbral, f"RMSE {rmse_student:.4f} supera umbral {rmse_umbral}"
assert np.all(np.isfinite(estado_estimado)), "Hay NaN o inf en la estimación — ver Errores comunes"
assert tiempo_ejecucion < 60.0, f"Notebook tardó {tiempo_ejecucion:.1f}s, máx permitido: 60s"
```

## Diseño de Simulaciones

### Dataset central: Seguimiento de vehículo 1D-2D

El dataset del curso modela un vehículo cuyo estado evoluciona a través de tres escenarios
de complejidad creciente, todos generados con `np.random.seed(42)`:

| Escenario | Dinámica | Observación | Primer uso | Filtro óptimo |
|-----------|----------|-------------|------------|---------------|
| S1: Lineal-Gaussiano | xₖ = Fxₖ₋₁ + wₖ, w ~ N(0,Q) | zₖ = Hxₖ + vₖ, v ~ N(0,R) | M2 (discretizado) | Kalman |
| S2: No lineal suave | xₖ = f(xₖ₋₁) + wₖ (seno) | zₖ = ‖xₖ‖ + vₖ (rango) | M3b | EKF / UKF |
| S3: No lineal fuerte | xₖ = f(xₖ₋₁) + wₖ (bimodal) | zₖ = h(xₖ) (bearing-only) | M4 | Partículas |

**Parámetros fijos (todos los módulos)**:
- T = 200 pasos de tiempo
- Q = 0.1 (ruido de proceso)
- R = 1.0 (ruido de medición)
- Δt = 0.1 s (paso temporal)
- x₀ = [0.0, 1.0]ᵀ (posición, velocidad inicial)

### Observación de convergencia
En cada módulo práctico se incluye una figura de convergencia:
- Eje x: tiempo k
- Eje y: error de estimación |x̂ₖ - xₖ|
- Líneas: estimación del filtro, banda ±2σ, estado real
- Indicador: punto de convergencia donde error < 2σ por primera vez

### Observación de robustez (Módulo 5)
Tres experimentos de robustez en el notebook guiado:
1. Aumento de ruido de proceso Q: ¿qué filtro degrada más rápido?
2. Fallo de sensor (observaciones faltantes durante 20 pasos): ¿qué filtro recupera mejor?
3. Violación de supuesto de Gaussianidad (ruido Laplaciano): ¿cuánto pierde Kalman?

## Plan de Contenidos Matemáticos por Nivel de Dificultad

| Nivel | Módulo | Contenido matemático | Herramienta Python |
|-------|--------|---------------------|-------------------|
| 1 — Fundamentos | M1 | Probabilidad condicional, Bayes, Gaussiana 1D | `scipy.stats` |
| 2 — Discreto | M2 | Chapman-Kolmogorov discreto, normalización | NumPy vectorized |
| 3 — Matricial | M3a | Gaussiana multivariada, matrices de covarianza, MMSE | NumPy linalg |
| 4 — Jacobiano | M3b | Derivadas parciales, linealización de primer orden | NumPy + derivación manual |
| 5 — Sigma points | M3c | Transformada unscented, parámetros α/β/κ, pesos | NumPy |
| 6 — Monte Carlo | M4 | Importancia muestral, ESS, remuestreo | NumPy random |
| 7 — Comparativo | M5 | RMSE, NEES, complejidad O(n), análisis de trade-offs | NumPy + pandas para tabla |

**Puentes matemáticos** (recordatorios autocontenidos en notebook teórico):
- M3b: recordatorio de Jacobiano (2 páginas) antes de la derivación del EKF
- M3c: recordatorio de esperanza de función no lineal antes de la transformada unscented
- M4: recordatorio de importancia muestral antes del SIR

## Estrategia de Evaluación

### Formativa (dentro de cada módulo)

1. **Celdas de verificación intermedia** — en el notebook teórico, tras cada derivación
   hay una celda de código que computa el resultado analítico con valores concretos:
   ```python
   # Verificación: posterior debe sumar 1.0
   assert abs(posterior.sum() - 1.0) < 1e-10, "La distribución no está normalizada"
   ```

2. **Preguntas de comprensión** — celdas Markdown con `> ❓ Pregunta: ...` antes de los
   ejercicios guiados. No tienen validación automática; son reflexivas.

3. **Criterios de éxito en ejercicios base** — cada ejercicio base termina con:
   ```python
   print(f"✅ RMSE = {rmse:.4f} (umbral: {UMBRAL:.4f}) — {'APROBADO' if rmse < UMBRAL else 'REVISAR'}")
   ```

### Sumativa (por módulo)

**Mini-evaluación** (sección final del notebook práctico): 3–5 problemas sin andamiaje,
con soluciones en un archivo separado `rubrica.md`. Los criterios son siempre:
- Numérico con tolerancia: `assert abs(resultado - esperado) < TOL`
- Gráfico con característica verificable: pendiente positiva, convergencia visible, etc.
- Conceptual verificable: el estudiante puede modificar un parámetro y predecir el efecto

**Rúbrica por módulo** (archivo `rubrica.md`):

| ID | Criterio | Verificación | Tolerancia | Nivel |
|----|----------|-------------|------------|-------|
| R-01 | Posterior normalizado | `sum(posterior) ≈ 1.0` | 1e-10 | Base |
| R-02 | RMSE filtro vs. referencia | `|RMSE_student - RMSE_ref| < TOL` | 1e-4 | Base |
| R-03 | Convergencia en < T/2 pasos | `conv_step < T // 2` | — | Base |
| R-04 | Justificación de parámetros | Prosa coherente con supuestos | — | Reto |

### Evaluación del Módulo 5 (integrador)

**Notebook guiado (base)**:
- 6 preguntas de justificación estructurada — rúbrica en `rubrica.md`
- Tabla comparativa — verificada automáticamente con `assert` en celda de validación

**Extensión abierta (posgrado)**:
- Evaluado por pares o instructor con rúbrica holística de 4 dimensiones:
  coherencia de supuestos, corrección técnica, completitud de comparación, calidad argumentativa

## Cronograma de Producción

| Fase | Entregables | Esfuerzo estimado |
|------|-------------|-------------------|
| A — Infraestructura | `src/` completo (5 filtros + utils + CLI + db), `tests/`, `pyproject.toml`, `Makefile`, `glosario.md` | 5 días |
| B — Módulo 1 | 2 notebooks + `rubrica.md` | 4 días |
| C — Módulo 2 | 2 notebooks + `rubrica.md` | 4 días |
| D — Módulo 3a | 2 notebooks (Kalman lineal) | 3 días |
| E — Módulo 3b | 2 notebooks (EKF) | 4 días |
| F — Módulo 3c | 2 notebooks (UKF) | 4 días |
| G — Módulo 4 | 2 notebooks + `rubrica.md` | 5 días |
| H — Módulo 5 | notebook guiado + extensión + `rubrica.md` | 5 días |
| I — Integración | nbval CI pass, nbconvert export, review pedagógico | 3 días |
| **Total** | | **~37 días de producción** |

**Dependencias de producción**:
- Fase A debe completarse antes de cualquier notebook (filtros en `src/` son importados)
- Módulos 1–2 pueden producirse en paralelo
- Módulos 3a → 3b → 3c deben producirse en ese orden (contenido acumulativo)
- Módulo 4 puede producirse en paralelo con 3c
- Módulo 5 requiere que 1–4 estén terminados y en `src/`

## Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Módulo 3 demasiado largo (3 sub-módulos = 6 notebooks) | Alta | Alto | Sub-módulos independientes; estudiante puede pausar entre 3a, 3b, 3c |
| UKF sigma points: confusión con α, β, κ | Alta | Medio | Notebook 3c inicia con ejemplo 1D con números redondos antes de la fórmula general |
| Notebooks > 50 celdas: fatiga cognitiva | Media | Alto | Límite: teórico ≤ 30 celdas, práctico ≤ 25 celdas; split en sub-módulos si excede |
| EKF/UKF difícil para audiencia de carrera | Alta | Medio | Jacobiano pre-calculado en andamiaje; estudiante implementa el loop, no el álgebra |
| Divergencia numérica en EKF (no diagnosticada) | Media | Alto | Celda de verificación de matriz de covarianza positiva-definida + mensaje de error accionable |
| Inconsistencia de seed entre versiones de numpy | Baja | Alto | Pinear numpy en `pyproject.toml`; documentar versión exacta en celda de header |
| Dataset sintético muy complejo para módulos iniciales | Media | Medio | Dataset escalonado: M1 usa 50 puntos, M2 usa 100, M3+ usa 200 |
| Rerun.io no disponible en todos los entornos | Media | Bajo | Rerun es opcional (demo en M4); fallback Plotly snapshot si rerun-sdk no instalado |

## Criterios de Calidad Verificables por Módulo

### Módulo 1

- [ ] El notebook teórico contiene derivación de Bayes en ≥ 5 pasos numerados desde los axiomas
- [ ] El ejemplo numérico calcula un posterior con valores concretos y verifica `sum(posterior)≈1`
- [ ] El notebook práctico ejecuta "Run All" en < 30 s
- [ ] El ejercicio base termina con `assert abs(posterior_calculado - posterior_esperado) < 1e-4`
- [ ] La sección "Errores comunes" documenta: (1) confundir P(A|B) con P(B|A), (2) prior impropio
- [ ] nbval pasa sin errores

### Módulo 2

- [ ] Derivación de Chapman-Kolmogorov en ≥ 3 pasos con matrices concretas
- [ ] `BayesFiltroDiscreto.predict()` + `update()` en NumPy, RMSE < `filterpy` ± 1e-6
- [ ] Visualización Plotly: mapa de calor belief(t,x) con título, ejes y leyenda
- [ ] Convergencia verificable: `assert conv_step < T // 2` sobre dataset estándar
- [ ] nbval pasa sin errores

### Módulo 3a (Kalman Lineal)

- [ ] Ganancia de Kalman derivada desde criterio MMSE en ≥ 4 pasos matriciales
- [ ] `KalmanLineal.predict()` + `update()` en NumPy, residuo vs filterpy < 1e-8
- [ ] Banda de incertidumbre ±2σ visible en Plotly con ≥ 95% de puntos reales dentro
- [ ] Ejercicio: variar Q/R con assert sobre cobertura de banda de confianza
- [ ] nbval pasa sin errores

### Módulo 3b (EKF)

- [ ] Recordatorio de Jacobiano presente (≥ 2 ejemplos numéricos) antes de la derivación del EKF
- [ ] `EKFiltro` RMSE < `filterpy.ExtendedKalmanFilter` ± 1e-4 sobre S2
- [ ] Celda de diagnóstico de divergencia: `assert np.all(np.linalg.eigvals(P) > 0)`
- [ ] Ejercicio de divergencia intencional documentado con solución en "Errores comunes"
- [ ] nbval pasa sin errores

### Módulo 3c (UKF)

- [ ] Parámetros α, β, κ explicados con efecto numérico visible (tabla comparativa)
- [ ] `UKFiltro` RMSE ≤ EKF RMSE en S2 (verificado con assert)
- [ ] Overlay UKF vs EKF vs real en Plotly con 3 series claramente diferenciadas
- [ ] Ejercicio bearing-only completo con RMSE < umbral definido en rúbrica
- [ ] nbval pasa sin errores

### Módulo 4 (Partículas)

- [ ] ESS definido y calculado en cada paso: `assert ess > N * 0.1` antes de remuestreo
- [ ] Animación Plotly de partículas en t=10,50,100,200 con N visible en título
- [ ] Rerun demo funciona con fallback Plotly si rerun-sdk no instalado
- [ ] Reto adaptativo: RMSE con remuestreo adaptativo ≤ remuestreo sistemático ± 5%
- [ ] nbval pasa sin errores

### Módulo 5 (Proyecto Integrador)

- [ ] Tabla comparativa contiene exactamente 5 métodos × 3 métricas × 3 escenarios
- [ ] Sub-análisis familia Kalman: tabla 3×3 (métodos × escenarios) + conclusión guiada
- [ ] Las 6 preguntas de justificación tienen espacio de respuesta y rúbrica en `rubrica.md`
- [ ] Extensión abierta: plantilla sin andamiaje presente, con rúbrica holística de 4 dimensiones
- [ ] nbval pasa sobre notebook guiado sin errores; extensión solo verificada manualmente

## Project Structure

### Documentation (this feature)

```text
specs/001-curso-filtros-bayesianos/
├── plan.md              ← este archivo
├── research.md          ← decisiones de tecnología y diseño
├── data-model.md        ← entidades y relaciones del curso
├── quickstart.md        ← cómo instalar y ejecutar
├── contracts/
│   ├── notebook-contract.md     ← esquema de celda obligatorio por tipo
│   └── filter-contract.md       ← interfaz Python de los filtros
└── tasks.md             ← generado por /speckit-tasks
```

### Source Code (repository root)

```text
cursos/
├── modulo_01_probabilidad/
│   ├── 01_teoria.ipynb
│   ├── 02_practica.ipynb
│   └── rubrica.md
├── modulo_02_bayes_discreto/
│   ├── 01_teoria.ipynb
│   ├── 02_practica.ipynb
│   └── rubrica.md
├── modulo_03_familia_kalman/
│   ├── 3a_kalman_lineal/
│   │   ├── 01_teoria.ipynb
│   │   └── 02_practica.ipynb
│   ├── 3b_ekf/
│   │   ├── 01_teoria.ipynb
│   │   └── 02_practica.ipynb
│   ├── 3c_ukf/
│   │   ├── 01_teoria.ipynb
│   │   └── 02_practica.ipynb
│   └── rubrica.md
├── modulo_04_particulas/
│   ├── 01_teoria.ipynb
│   ├── 02_practica.ipynb
│   └── rubrica.md
├── modulo_05_proyecto_integrador/
│   ├── 01_proyecto_guiado.ipynb
│   ├── 02_extension_abierta.ipynb
│   └── rubrica.md
└── plantillas/
    ├── plantilla_teoria.ipynb
    └── plantilla_practica.ipynb

src/
├── filtros/
│   ├── __init__.py
│   ├── bayes_discreto.py       ← BayesFiltroDiscreto
│   ├── kalman_lineal.py        ← KalmanLineal
│   ├── ekf.py                  ← EKFiltro
│   ├── ukf.py                  ← UKFiltro
│   └── particulas.py           ← FiltroPArticulas
├── utils/
│   ├── __init__.py
│   ├── dataset.py              ← generar_dataset(scenario, T, seed)
│   ├── metricas.py             ← rmse(), nees(), ess()
│   └── visualizacion.py        ← plot_estimacion(), plot_particulas()
├── cli/
│   ├── __init__.py
│   └── main.py                 ← CLI: filtros run / filtros plot / filtros export
└── db/
    ├── __init__.py
    └── progreso.py             ← ProgresoEstudiante (SQLite)

tests/
├── filtros/
│   ├── test_bayes_discreto.py
│   ├── test_kalman_lineal.py
│   ├── test_ekf.py
│   ├── test_ukf.py
│   └── test_particulas.py
├── utils/
│   ├── test_dataset.py
│   └── test_metricas.py
└── db/
    └── test_progreso.py

db/
└── migrations/
    └── 001_initial.sql

glosario.md
pyproject.toml
Makefile
```

**Structure Decision**: Separación `cursos/` (contenido pedagógico, notebooks) vs `src/`
(código importable, tipado, testeado). Los notebooks importan de `src/filtros/` para
la celda de validación pero reimplementan los filtros desde cero para el ejercicio.

## Complexity Tracking

> Sin violaciones — no se requieren entradas.
