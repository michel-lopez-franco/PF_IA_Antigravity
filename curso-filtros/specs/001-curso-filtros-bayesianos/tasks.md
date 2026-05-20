---
description: "Task list — Curso Completo de Filtros Bayesianos"
---

# Tasks: Curso Completo de Filtros Bayesianos

**Input**: Design documents from `specs/001-curso-filtros-bayesianos/`

**Prerequisites**: plan.md ✅ spec.md ✅ research.md ✅ data-model.md ✅ contracts/ ✅

**Tests**: Tests MANDATORY per project constitution (pytest, coverage ≥ 80% + nbval on all notebooks).

**Organization**: Phases 1–2 son fundamento compartido. Fases 3–9 por módulo. Fase 10 polish.
Cada tarea incluye **DoD** (Definition of Done) y **Esfuerzo estimado**.

## Formato: `[ID] [P?] [Story?] Descripción con ruta de archivo`

- **[P]**: Puede ejecutarse en paralelo (archivos distintos, sin dependencias incompletas)
- **[Story]**: US1=Progresión pedagógica, US2=Práctica autoguiada, US3=Autoevaluación, US4=Proyecto integrador
- **Esfuerzo**: h=horas, d=días de producción (~6h trabajo efectivo por día)

---

## Phase 1: Setup (Infraestructura base)

**Purpose**: Estructura de directorios, herramientas y configuración del proyecto.

- [x] T001 Crear estructura de directorios: `cursos/`, `src/filtros/`, `src/utils/`, `src/cli/`, `src/db/`, `tests/`, `db/migrations/`, `plantillas/`
  - **DoD**: Todos los directorios existen; `__init__.py` vacío en cada subpaquete de `src/`
  - **Esfuerzo**: 0.5h

- [x] T002 [P] Crear `pyproject.toml` con dependencias: numpy≥2.0, scipy≥1.13, plotly≥5.22, rerun-sdk≥0.16, jupyter, nbconvert, nbval, filterpy, pykalman, typer; devDeps: mypy, ruff, pytest, pytest-cov
  - **DoD**: `uv sync` completa sin errores; `python -c "import numpy, scipy, plotly"` exits 0
  - **Esfuerzo**: 0.5h

- [x] T003 [P] Crear `Makefile` con targets: `check` (mypy+ruff), `test` (pytest --cov), `nbval` (pytest --nbval-lax cursos/), `ci` (check+test+nbval)
  - **DoD**: `make ci` completa en entorno limpio
  - **Esfuerzo**: 0.5h

- [x] T004 [P] Inicializar `glosario.md` con estructura: encabezado, sección "Términos en inglés" vacía, sección "Notación matemática" vacía
  - **DoD**: Archivo existe en raíz; estructura markdown válida
  - **Esfuerzo**: 0.5h

- [x] T005 Crear `db/migrations/001_initial.sql` con tablas `progreso` y `metrica_run` según data-model.md
  - **DoD**: SQL válido; `sqlite3 :memory: < db/migrations/001_initial.sql` exits 0
  - **Esfuerzo**: 0.5h

---

## Phase 2: Foundational (Bloqueante para todos los módulos)

**Purpose**: Implementaciones de filtros, utilidades, plantillas y CLI. NADA de notebooks hasta completar esta fase.

**⚠️ CRÍTICO**: Las fases 3–9 no pueden comenzar hasta que esta fase esté completa.

- [x] T006 Implementar `src/filtros/__init__.py` con `FiltroProtocol` (Protocol de Python 3.12) según `contracts/filter-contract.md`
  - **DoD**: `mypy --strict src/filtros/__init__.py` pasa; Protocol tiene `predecir()`, `actualizar()`, `estado`, `covarianza`
  - **Esfuerzo**: 1h

- [x] T007 [P] Implementar `src/utils/dataset.py` — función `generar_dataset(escenario, T, seed)` para S1/S2/S3 según data-model.md
  - **DoD**: mypy pass; `generar_dataset("S1", 200, 42)` retorna `(estados, observaciones)` con shapes correctos; reproducible con mismo seed
  - **Esfuerzo**: 2h

- [x] T008 [P] Implementar `src/utils/metricas.py` — funciones `rmse()`, `nees()`, `ess()` con type hints
  - **DoD**: mypy pass; `rmse(np.zeros(5), np.zeros(5))` = 0.0; `ess(np.ones(N)/N)` = N
  - **Esfuerzo**: 1h

- [x] T009 [P] Implementar `src/utils/visualizacion.py` — `plot_estimacion()` (Plotly) y `plot_particulas()` (Plotly + Rerun fallback)
  - **DoD**: mypy pass; genera figura Plotly con título, ejes etiquetados, leyenda; `write_html()` funciona
  - **Esfuerzo**: 2h

- [x] T010 [P] Implementar `src/db/progreso.py` — clase `ProgresoEstudiante` con SQLite (sqlite3 stdlib): `marcar_completado()`, `consultar_rmse()`, `listar_progreso()`
  - **DoD**: mypy pass; integración test pasa; `filtros.db` creado localmente; migración 001 aplicada
  - **Esfuerzo**: 2h

- [x] T011 [P] Crear `tests/utils/test_dataset.py` — tests para generar_dataset (shapes, reproducibilidad, tres escenarios)
  - **DoD**: pytest pasa; cobertura src/utils/dataset.py ≥ 80%
  - **Esfuerzo**: 1h

- [x] T012 [P] Crear `tests/utils/test_metricas.py` — tests para rmse, nees, ess (valores conocidos, edge cases)
  - **DoD**: pytest pasa; cobertura src/utils/metricas.py ≥ 80%
  - **Esfuerzo**: 1h

- [x] T013 [P] Crear `tests/db/test_progreso.py` — tests de integración con SQLite en memoria
  - **DoD**: pytest pasa; usa `":memory:"` como db; cobertura src/db/progreso.py ≥ 80%
  - **Esfuerzo**: 1h

- [x] T014 Implementar `src/cli/main.py` — CLI con typer: `filtros run`, `filtros plot`, `filtros export` (max 3 tokens cada uno)
  - **DoD**: mypy pass; `filtros --help` muestra todos los subcomandos; `filtros run --modulo 1` invoca nbconvert sin error
  - **Esfuerzo**: 2h

- [x] T015 [P] Crear `plantillas/plantilla_teoria.ipynb` — notebook teórico vacío siguiendo `contracts/notebook-contract.md` (celdas markdown con títulos de sección, seed en celda 3)
  - **DoD**: nbval pasa en entorno limpio; todas las secciones obligatorias presentes; seed visible en celda 3
  - **Esfuerzo**: 1h

- [x] T016 [P] Crear `plantillas/plantilla_practica.ipynb` — notebook práctico vacío con celda de validación marcada, celda de smoke-test, seed
  - **DoD**: nbval pasa; celda `[CELDA DE VALIDACIÓN — NO MODIFICAR]` presente; smoke-test `assert tiempo < 60` presente
  - **Esfuerzo**: 1h

**Checkpoint**: Fundación lista — `make test` pasa con cobertura ≥ 80%; plantillas verificadas por nbval.

---

## Phase 3: Módulo 1 — Probabilidad e Inferencia Bayesiana (US1, P1)

**Goal**: El estudiante entiende y aplica el Teorema de Bayes en casos discretos y continuos.

**Independent Test**: Módulo 1 completo + nbval pass + estudiante resuelve ejercicio base de posterior con `|resultado - analítico| < 1e-4`.

- [x] T017 [US1] Crear `cursos/modulo_01_probabilidad/01_teoria.ipynb` — derivación de Bayes desde axiomas de Kolmogorov, Gaussiana 1D, inferencia conjugada
  - **DoD**: 7 secciones obligatorias + Errores comunes (≥2) + ¿Qué aprendiste? (≥5 bullets) + ¿Qué sigue?; seed(42); Run All < 30s; nbval pass
  - **Esfuerzo**: 1d

- [x] T018 [US2] Crear `cursos/modulo_01_probabilidad/02_practica.ipynb` — actualización bayesiana secuencial con moneda sesgada, visualización Plotly de evolución del posterior
  - **DoD**: Celda de validación `|posterior_student - analítico| < 1e-4`; Plotly con título, eje x=observaciones, eje y=P(θ); smoke-test < 30s; nbval pass
  - **Esfuerzo**: 1d

- [x] T019 [US3] Crear `cursos/modulo_01_probabilidad/rubrica.md` — 3 criterios: (1) normalización del posterior, (2) monotonicidad con evidencia acumulada, (3) límite con evidencia infinita
  - **DoD**: Cada criterio tiene ID (R-M1-XX), descripción, método de verificación, tolerancia numérica donde aplica
  - **Esfuerzo**: 0.5d

- [x] T020 [US1] [US2] QA técnico modulo_01 — ejecutar `pytest --nbval-lax cursos/modulo_01_probabilidad/`; verificar seed, secciones, tolerancias
  - **DoD**: nbval pasa sin warnings; todas las secciones obligatorias verificadas con grep en JSON del notebook
  - **Esfuerzo**: 0.5d

- [x] T021 [US1] QA pedagógico modulo_01 — revisar derivación (sin saltos), errores comunes, cierre reflexivo, terminología en español
  - **DoD**: Ningún "puede demostrarse que" sin cita; ≥2 errores comunes con síntoma+diagnóstico+solución; ¿Qué aprendiste? en primera persona plural; todos los términos EN definidos en español
  - **Esfuerzo**: 0.5d

**Checkpoint**: Módulo 1 independientemente completable y testeado.

---

## Phase 4: Módulo 2 — Filtro Bayesiano Discreto (US1, US2, P1)

**Goal**: Implementación del ciclo predict/update en NumPy; convergencia observable en grilla 1D.

**Independent Test**: `BayesFiltroDiscreto` pasa tests unitarios; notebook práctico pasa nbval con RMSE < filterpy ± 1e-6.

- [x] T022 Implementar `src/filtros/bayes_discreto.py` — clase `BayesFiltroDiscreto` (predict + update + estado + covarianza), numpy only
  - **DoD**: mypy --strict pass; `predict()` implementa Chapman-Kolmogorov; `update()` normaliza posterior; tests pasan
  - **Esfuerzo**: 0.5d

- [x] T023 [P] Crear `tests/filtros/test_bayes_discreto.py` — tests: prior uniforme, prior concentrado, update con likelihood cero, normalización
  - **DoD**: pytest pasa; cobertura src/filtros/bayes_discreto.py ≥ 80%; edge case prior-todo-cero lanza ValueError
  - **Esfuerzo**: 0.5d

- [x] T024 [US1] Crear `cursos/modulo_02_bayes_discreto/01_teoria.ipynb` — derivación Chapman-Kolmogorov, paso de actualización, ejemplo puerta con tablas numéricas paso a paso
  - **DoD**: 7 secciones + Errores comunes ≥2; derivación en ≥3 pasos con matrices concretas; ejemplo puerta con 5 pasos calculados manualmente; nbval pass
  - **Esfuerzo**: 1d

- [x] T025 [US2] Crear `cursos/modulo_02_bayes_discreto/02_practica.ipynb` — seguimiento en grilla 1D (N=20, T=100), Plotly heatmap belief(t,x), convergencia MAP
  - **DoD**: `|RMSE_student - RMSE_filterpy| < 1e-6`; heatmap Plotly con colorbar, título, ejes; `conv_step < T//2` assert; nbval pass
  - **Esfuerzo**: 1d

- [x] T026 [US3] Crear `cursos/modulo_02_bayes_discreto/rubrica.md` — criterios R-M2-01 (normalización), R-M2-02 (RMSE), R-M2-03 (convergencia < T/2)
  - **DoD**: Cada criterio verificable con assert en código; nivel base/reto indicado
  - **Esfuerzo**: 0.5d

- [x] T027 [US1] [US2] QA modulo_02 — nbval + revisión pedagógica
  - **DoD**: nbval pasa; belief suma 1.0 en cada paso (assert); convergencia mapa de calor legible; todos los términos EN (belief, prior, posterior, predict, update) definidos en español en su primera aparición (FR-012)
  - **Esfuerzo**: 0.5d

**Checkpoint**: Módulo 2 ejecutable y testeado; `BayesFiltroDiscreto` en src/ con cobertura ≥ 80%.

---

## Phase 5: Módulo 3a — Kalman Lineal (US1, US2, P1)

**Goal**: Derivación MMSE del filtro de Kalman; implementación en NumPy; validación contra filterpy.

- [ ] T028 Implementar `src/filtros/kalman_lineal.py` — clase `KalmanLineal` (predict + update + estado + covarianza) con matrices F, H, Q, R
  - **DoD**: mypy --strict pass; residuo vs filterpy < 1e-8 sobre S1; P positiva-definida en cada paso
  - **Esfuerzo**: 0.5d

- [ ] T029 [P] Crear `tests/filtros/test_kalman_lineal.py` — tests: paso estacionario, ganancia de Kalman límite (R→0, R→∞), covarianza positiva-definida
  - **DoD**: pytest pasa; cobertura ≥ 80%; test de R→0 verifica que K→H⁻¹
  - **Esfuerzo**: 0.5d

- [ ] T030 [US1] Crear `cursos/modulo_03_familia_kalman/3a_kalman_lineal/01_teoria.ipynb` — derivación MMSE en ≥4 pasos matriciales, ecuaciones de Riccati, ejemplo 1D pos-vel
  - **DoD**: Ganancia K derivada desde criterio MMSE sin saltos; ecuaciones de Riccati presentes; ejemplo numérico 5 pasos con matrices concretas 2×2; nbval pass
  - **Esfuerzo**: 1.5d

- [ ] T031 [US2] Crear `cursos/modulo_03_familia_kalman/3a_kalman_lineal/02_practica.ipynb` — vehículo 1D S1, ±2σ Plotly, ejercicio Q/R ajustable
  - **DoD**: `|RMSE_student - RMSE_filterpy| < 1e-8`; banda ±2σ cubre ≥95% del estado real; ejes con unidades (eje x=tiempo [pasos], eje y=posición [m]) (Const. XI); reto opcional: implementar Kalman 2D o con R desconocido sin andamiaje (FR-013); smoke-test < 60s; nbval pass
  - **Esfuerzo**: 1d

- [ ] T032 [US1] [US2] QA modulo_3a — nbval + revisión pedagógica
  - **DoD**: nbval pasa; `eigvals(P) > 0` en cada paso; 7 secciones verificadas; Errores comunes incluye "P no positiva-definida"; todos los términos EN (Kalman gain, innovation, state, covariance) definidos en español en su primera aparición (FR-012)
  - **Esfuerzo**: 0.5d

**Checkpoint**: Sub-módulo 3a independientemente completable; `KalmanLineal` en src/ con cobertura ≥ 80%.

---

## Phase 6: Módulo 3b — EKF (US1, US2, P1)

**Goal**: EKF con Jacobiano analítico; demostración de divergencia con no-linealidad fuerte.

- [ ] T033 Implementar `src/filtros/ekf.py` — clase `EKFiltro` que acepta funciones f, h y sus Jacobianos como callables
  - **DoD**: mypy --strict pass; `|RMSE_EKF - RMSE_filterpy.EKF| < 1e-4` en S2; ValueError si P no positiva-definida
  - **Esfuerzo**: 1d

- [ ] T034 [P] Crear `tests/filtros/test_ekf.py` — tests: caso lineal (EKF debe igualar Kalman), S2 no lineal, divergencia detectada
  - **DoD**: pytest pasa; test lineal: `|RMSE_EKF - RMSE_Kalman| < 1e-6`; cobertura ≥ 80%
  - **Esfuerzo**: 0.5d

- [ ] T035 [US1] Crear `cursos/modulo_03_familia_kalman/3b_ekf/01_teoria.ipynb` — recordatorio Jacobiano (≥2 ejemplos), EKF derivación, análisis de error de linealización
  - **DoD**: Recordatorio Jacobiano con 2 ejemplos numéricos concretos ANTES de la derivación del EKF; análisis de divergencia presente; nbval pass
  - **Esfuerzo**: 1.5d

- [ ] T036 [US2] Crear `cursos/modulo_03_familia_kalman/3b_ekf/02_practica.ipynb` — S2 rango 2D, demo de divergencia intencional, ejercicio Jacobiano numérico
  - **DoD**: EKF RMSE < filterpy ± 1e-4 en S2; demo de divergencia documenta síntoma en Errores comunes; `eigvals(P) > 0` assert; ejes con unidades (eje x=tiempo [pasos], eje y=distancia [m]) (Const. XI); reto opcional: calcular Jacobiano numéricamente y comparar con analítico sin andamiaje (FR-013); nbval pass
  - **Esfuerzo**: 1d

- [ ] T037 [US1] [US2] QA modulo_3b — nbval + revisión pedagógica
  - **DoD**: nbval pasa; celda de diagnóstico `eigvals(P) > 0` presente; Errores comunes cubre "Jacobiano incorrecto" y "P no pd"
  - **Esfuerzo**: 0.5d

**Checkpoint**: Sub-módulo 3b completable; `EKFiltro` en src/ con cobertura ≥ 80%.

---

## Phase 7: Módulo 3c — UKF (US1, US2, P1)

**Goal**: Transformada unscented completa con sigma points; comparación directa UKF vs EKF.

- [ ] T038 Implementar `src/filtros/ukf.py` — clase `UKFiltro` con `sigma_points()`, `unscented_transform()`, predict(), update(); parámetros α/β/κ
  - **DoD**: mypy --strict pass; sigma points count = 2n+1 assert; `|RMSE_UKF - RMSE_filterpy.UKF| < 1e-4`; RMSE_UKF ≤ RMSE_EKF en S2
  - **Esfuerzo**: 1d

- [ ] T039 [P] Crear `tests/filtros/test_ukf.py` — tests: sigma points count, pesos suman 1, UKF ≤ EKF en S2 no lineal
  - **DoD**: pytest pasa; `sum(W_m) ≈ 1.0`; cobertura ≥ 80%
  - **Esfuerzo**: 0.5d

- [ ] T040 [US1] Crear `cursos/modulo_03_familia_kalman/3c_ukf/01_teoria.ipynb` — recordatorio esperanza de función no lineal, transformada unscented, derivación sigma points y pesos, UKF predict+update, comparación con EKF
  - **DoD**: Ejemplo 1D con α=1e-3 ANTES de la fórmula general; tabla comparativa UKF vs EKF error de aproximación; pesos Wm y Wc calculados explícitamente; nbval pass
  - **Esfuerzo**: 2d

- [ ] T041 [US2] Crear `cursos/modulo_03_familia_kalman/3c_ukf/02_practica.ipynb` — mismo S2 que 3b, Plotly overlay 3 series (UKF/EKF/real), ejercicio bearing-only
  - **DoD**: `RMSE_UKF ≤ RMSE_EKF` assert en S2; overlay 3 series con leyenda diferenciada; bearing-only ejercicio tiene criterio de éxito; nbval pass
  - **Esfuerzo**: 1d

- [ ] T042 [US3] Crear `cursos/modulo_03_familia_kalman/rubrica.md` — criterios compartidos 3a+3b+3c + sección de comparación de familia Kalman
  - **DoD**: Criterios para cada sub-módulo; sección "Comparación familia Kalman" con tabla esperada (3 métodos × 2 escenarios)
  - **Esfuerzo**: 0.5d

- [ ] T043 [US1] [US2] QA modulo_3c — nbval + revisión pedagógica
  - **DoD**: nbval pasa; sigma points = 2n+1 assert verificable; comparación UKF vs EKF presente; términos alpha/beta/kappa definidos en español
  - **Esfuerzo**: 0.5d

**Checkpoint**: Sub-módulo 3c completable; familia Kalman completa en src/; rubrica del módulo 3 lista.

---

## Phase 8: Módulo 4 — Filtro de Partículas (US1, US2, P2)

**Goal**: SIR con diagnóstico ESS; demo en tiempo real con Rerun; degeneración observable.

- [ ] T044 Implementar `src/filtros/particulas.py` — clase `FiltroPArticulas` (inicializar, propagar, pesar, remuestreo sistemático) con propiedad `ess`
  - **DoD**: mypy --strict pass; `ess` ∈ (0, N]; remuestreo solo cuando ESS < N/2; 1000 partículas convergen en S3
  - **Esfuerzo**: 1d

- [ ] T045 [P] Crear `tests/filtros/test_particulas.py` — tests: ESS > 0, ESS = N para pesos iguales, remuestreo activa cuando ESS < N/2
  - **DoD**: pytest pasa; cobertura ≥ 80%; test de degeneración verifica que ESS < 0.1*N dispara remuestreo
  - **Esfuerzo**: 0.5d

- [ ] T046 [US1] Crear `cursos/modulo_04_particulas/01_teoria.ipynb` — SIR completo con pseudocódigo, ESS derivado, estrategias de remuestreo comparadas, localizador de robots motivación
  - **DoD**: SIR pseudocódigo ANTES de implementación Python; ESS = 1/Σwᵢ² derivado; 3 estrategias comparadas (multinomial, sistemático, residual); nbval pass
  - **Esfuerzo**: 1.5d

- [ ] T047 [US2] Crear `cursos/modulo_04_particulas/02_practica.ipynb` — S3 N=1000, snapshots Plotly t=10/50/100/200, Rerun demo opcional, reto adaptativo
  - **DoD**: `ESS > N*0.1` assert en cada paso de remuestreo; Plotly snapshots con N visible en título; Rerun import con `try/except ImportError` fallback; reto adaptativo tiene criterio de éxito; nbval pass
  - **Esfuerzo**: 1.5d

- [ ] T048 [US3] Crear `cursos/modulo_04_particulas/rubrica.md` — criterios: ESS diagnóstico, convergencia con N=1000, degradación con N=50, reto adaptativo
  - **DoD**: Criterios base verificables con código; reto tiene criterio holístico documentado
  - **Esfuerzo**: 0.5d

- [ ] T049 [US1] [US2] QA modulo_04 — nbval + revisión pedagógica
  - **DoD**: nbval pasa; Rerun fallback funciona sin rerun-sdk; ESS diagnóstico correcto; Errores comunes cubre "degeneración" y "remuestreo excesivo"
  - **Esfuerzo**: 0.5d

**Checkpoint**: Módulo 4 completable; `FiltroPArticulas` en src/ con cobertura ≥ 80%.

---

## Phase 9: US4 — Módulo 5 Proyecto Integrador Comparativo (P4)

**Goal**: Comparación de 5 métodos × 3 escenarios; tabla con ≥3 métricas; justificación guiada + extensión abierta.

**Independent Test**: Guided notebook ejecuta Run All generando tabla 5×3×3; open extension tiene seed válido y template funcional.

- [ ] T050 [US4] Crear `cursos/modulo_05_proyecto_integrador/01_proyecto_guiado.ipynb` — 3 escenarios × 5 métodos, tabla comparativa, sub-análisis familia Kalman, 6 preguntas de justificación guiada
  - **DoD**: Tabla `(5 métodos, 3 métricas, 3 escenarios)` generada por código; sub-análisis Kalman familia explícito; 6 preguntas estructuradas con espacio de respuesta markdown; `tiempo < 120s` assert; nbval pass
  - **Esfuerzo**: 2d

- [ ] T051 [P] [US4] Crear `cursos/modulo_05_proyecto_integrador/02_extension_abierta.ipynb` — plantilla mínima: header, seed, instrucciones sin andamiaje, sección ¿Justificación? sin preguntas guiadas
  - **DoD**: nbval pasa (plantilla no hace nada, solo seed y imports); sin celdas TODO; instrucciones claras en header; **sin preguntas guiadas en ninguna celda** — solo header + instrucciones + `np.random.seed(42)` + sección libre `## Justificación` (FR-010)
  - **Esfuerzo**: 0.5d

- [ ] T052 [US4] Crear `cursos/modulo_05_proyecto_integrador/rubrica.md` — rubrica cuantitativa del notebook guiado (tabla, preguntas) + rubrica holística de 4 dimensiones para extensión abierta
  - **DoD**: Rubrica guiada: cada pregunta tiene respuesta esperada o criterio binario; rubrica holística: 4 dimensiones (coherencia supuestos, corrección técnica, completitud comparación, calidad argumentativa) con escala 1-4
  - **Esfuerzo**: 0.5d

- [ ] T053 [US4] QA modulo_05 — nbval en notebook guiado; verificación manual de extensión abierta
  - **DoD**: nbval pasa en guided; extensión tiene Python válido y `np.random.seed(42)` en celda 2; tabla comparativa generada correctamente
  - **Esfuerzo**: 0.5d

**Checkpoint**: Las 4 user stories completadas independientemente. Todos los notebooks ejecutan Run All.

---

## Phase 10: Polish & Cross-cutting Concerns

**Purpose**: CI verde, exports, glosario completo, revisión pedagógica final.

- [ ] T054 [P] Completar `glosario.md` — definir en español todos los términos EN usados en módulos 1–5: prior, likelihood, posterior, belief, predict, update, Kalman gain, sigma points, ESS, SIR, RMSE, NEES
  - **DoD**: ≥15 términos definidos; notación matemática consistente con los notebooks; paralelo solo dentro de Phase 10 y tras completar notebooks M1–M5
  - **Esfuerzo**: 1d

- [ ] T055 [P] Exportar todos los notebooks a HTML con nbconvert en `docs/notebooks/`
  - **DoD**: 14 archivos HTML generados; `filtros export --all` funciona
  - **Esfuerzo**: 0.5d

- [ ] T056 Ejecutar `make ci` completo y corregir fallos — mypy --strict + ruff check + pytest --cov + nbval
  - **DoD**: `make ci` exits 0; cobertura src/ ≥ 80%; 0 errores nbval; 0 errores mypy
  - **Esfuerzo**: 0.5d

- [ ] T057 Revisión pedagógica final — verificar todos los módulos contra los 10 principios pedagógicos (VII–XVI) de la constitución
  - **DoD**: Checklist en `specs/001-curso-filtros-bayesianos/qa-pedagogico.md`; cada módulo ✅ en los 10 principios; issues abiertos para cualquier ❌
  - **Esfuerzo**: 1d

- [ ] T058 [P] Actualizar `glosario.md` con cualquier término faltante detectado en T057
  - **DoD**: Ningún término EN sin definir en ningún notebook
  - **Esfuerzo**: 0.5d

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: Sin dependencias — empezar inmediatamente
- **Phase 2 (Foundational)**: Depende de Phase 1 — BLOQUEA todas las fases de módulos
- **Phase 3 (M1)**: Depende de Phase 2
- **Phase 4 (M2)**: Depende de Phase 3 (M1 prerequisito pedagógico de M2)
- **Phase 5 (M3a)**: Depende de Phase 4
- **Phase 6 (M3b)**: Depende de Phase 5 (M3a prerequisito de M3b)
- **Phase 7 (M3c)**: Depende de Phase 6 (M3b prerequisito de M3c)
- **Phase 8 (M4)**: Depende de Phase 4; PUEDE ejecutarse en paralelo con Fases 5–7
- **Phase 9 (M5)**: Depende de Phases 3–8 completas
- **Phase 10 (Polish)**: Depende de Phase 9

### User Story Dependencies

- **US1 (Progresión pedagógica)**: Tareas de teoría en cada módulo — secuencial 1→2→3a→3b→3c→4→5
- **US2 (Práctica autoguiada)**: Tareas de práctica — puede ejecutarse en paralelo con US1 dentro del mismo módulo
- **US3 (Autoevaluación)**: Tareas de rúbrica — dependen de US1+US2 del mismo módulo
- **US4 (Proyecto integrador)**: Depende de US1+US2 de todos los módulos anteriores

### Within Each Module Phase

1. Implementar filtro en src/ (si aplica)
2. Tests del filtro en tests/ (en paralelo con T1 si el diseño está claro)
3. Notebook teórico [US1]
4. Notebook práctico [US2] (puede empezar cuando el filtro en src/ está listo)
5. Rúbrica [US3] (cuando notebooks están completos)
6. QA técnico + pedagógico

### Parallel Opportunities

- **Phase 2**: T007, T008, T009, T010, T011, T012, T013, T015, T016 — todos en paralelo
- **Dentro de cada módulo**: Notebook teórico y notebook práctico pueden desarrollarse en paralelo una vez que el filtro en src/ está implementado
- **Módulo 4 vs Módulo 3b/3c**: Pueden producirse en paralelo si hay dos autores disponibles
- **Phase 10**: T054, T055, T058 — en paralelo con T056/T057

---

## Parallel Example: Phase 2 (Foundational)

```bash
# Lanzar en paralelo:
Tarea: "Implementar src/utils/dataset.py"          → T007
Tarea: "Implementar src/utils/metricas.py"         → T008
Tarea: "Implementar src/utils/visualizacion.py"    → T009
Tarea: "Implementar src/db/progreso.py"            → T010
Tarea: "Crear tests/utils/test_dataset.py"         → T011
Tarea: "Crear tests/utils/test_metricas.py"        → T012
Tarea: "Crear tests/db/test_progreso.py"           → T013
Tarea: "Crear plantillas/plantilla_teoria.ipynb"   → T015
Tarea: "Crear plantillas/plantilla_practica.ipynb" → T016
```

---

## Implementation Strategy

### MVP First (US1 P1 — Módulo 1 solamente)

1. Completar Phase 1: Setup
2. Completar Phase 2: Foundational (CRÍTICO — bloquea todo)
3. Completar Phase 3: Módulo 1
4. **PARAR Y VALIDAR**: nbval pass; estudiante puede completar ejercicio base de M1
5. Demo independiente del módulo

### Incremental Delivery

1. Setup + Foundational → infraestructura lista
2. Módulo 1 → test independiente → Demo M1 (MVP)
3. Módulo 2 → test independiente → Demo M2
4. Módulos 3a, 3b, 3c → test de sub-módulo → Demo M3 completo
5. Módulo 4 → test independiente → Demo M4
6. Módulo 5 → validación comparativa completa → Curso completo
7. Polish → CI verde → Publicación

### Parallel Team Strategy (2 autores)

Con 2 autores:
1. Ambos completan Setup + Foundational juntos
2. **Autor A**: Módulos 1 → 2 → 3a → 3b → 3c (cadena secuencial)
3. **Autor B**: Infraestructura extra + Módulo 4 (puede empezar tras M2) → M5

---

## Notes

- `[P]` = archivos distintos, sin dependencias incompletas — ejecutar en paralelo
- Módulo 3 tiene 3 sub-módulos secuenciales (3a → 3b → 3c) — **NO se puede paralelizar dentro del módulo 3**
- Módulo 4 **SÍ puede empezar** cuando Módulos 1–2 están completos (prerequisitos pedagógicos suficientes)
- Cada módulo debe pasar `pytest --nbval-lax` antes de comenzar el siguiente
- Glosario se actualiza al terminar cada módulo, no al final
- `make ci` debe pasar en verde antes de abrir cualquier PR
