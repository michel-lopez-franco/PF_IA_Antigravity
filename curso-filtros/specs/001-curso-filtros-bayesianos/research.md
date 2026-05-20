# Research: Curso de Filtros Bayesianos — Decisiones de Tecnología y Diseño

**Branch**: `001-curso-filtros-bayesianos` | **Date**: 2026-05-20

---

## Decisión 1: Librería de Visualización Estática

**Decision**: Plotly (`plotly` ≥ 5.22) para todas las figuras estáticas en notebooks.

**Rationale**: Genera HTML interactivo que el estudiante puede explorar (zoom, hover) sin
instalar nada adicional. Compatible con Jupyter directamente. Exporta a PNG con un método
(`write_image`) sin dependencias externas adicionales. Alineado con constitution Principio V.

**Alternatives considered**:
- `matplotlib`: Más común académicamente, pero figuras estáticas no interactivas. Descartado
  porque la interactividad tiene valor pedagógico directo (el estudiante puede zoom en la
  convergencia del filtro).
- `bokeh`: Interactivo, pero API más compleja que Plotly para el nivel de audiencia objetivo.

---

## Decisión 2: Librería de Visualización en Tiempo Real

**Decision**: `rerun-sdk` ≥ 0.16 para demo de evolución de partículas en tiempo real (M4).

**Rationale**: Permite visualizar el cloud de partículas convergiendo paso a paso, lo cual
es imposible en un plot estático. Alineado con constitution Principio V (Rerun = tiempo real).
Se usa opcionalmente en M4; si no está instalado, el fallback es un snapshot Plotly.

**Alternatives considered**:
- `matplotlib.animation`: Funciona en notebooks pero produce GIFs pesados, difícil de
  inspeccionar frame a frame. Descartado.
- `dash`: Requiere servidor local, no apto para entorno de notebook estándar.

---

## Decisión 3: Validación de Notebooks en CI

**Decision**: `nbval` para verificar que todos los notebooks ejecutan sin errores.

**Rationale**: `nbval` ejecuta el notebook como lo haría "Run All" y compara outputs (o
solo verifica que no hay errores con `--nbval-lax`). Integra directamente con pytest.
Garantiza constitution Principio X (notebooks autoexplicativos y ejecutables).

**Alternatives considered**:
- `papermill`: Potente para parametrización pero demasiado complejo para verificación simple.
- `nbmake`: Alternativa válida; `nbval` elegido por integración nativa con pytest.

---

## Decisión 4: Librería de Referencia para Validación

**Decision**: `filterpy` ≥ 1.4 como referencia primaria; `pykalman` como alternativa
para Kalman lineal cuando filterpy no tenga implementación equivalente.

**Rationale**: `filterpy` implementa Kalman lineal, EKF, UKF, y partículas con interfaces
limpias y documentación matemática. Es el estándar de facto para filtros educativos en Python.
Usada ÚNICAMENTE en celdas de validación marcadas (FR-006), no en implementaciones.

**Alternatives considered**:
- `scipy.signal.kalman_filter`: No existe; scipy no tiene filtros de Kalman completos.
- Implementación propia de referencia: circular (validamos con la misma lógica que el estudiante).

---

## Decisión 5: Estructura del Módulo 3 (Familia Kalman)

**Decision**: Tres sub-módulos independientes (3a Kalman, 3b EKF, 3c UKF), cada uno con
su propio par de notebooks teórico/práctico.

**Rationale**: Colocar Kalman + EKF + UKF en un solo módulo con 6 notebooks producirían
una unidad de aprendizaje inapropiadamente larga. Los sub-módulos permiten:
1. Progresión incremental: cada sub-módulo construye sobre el anterior
2. Puntos de pausa naturales entre algoritmos
3. Prerequisitos explícitos entre sub-módulos

**Alternatives considered**:
- 1 módulo monolítico con 6 notebooks: Descartado — fatiga cognitiva (riesgo identificado).
- Módulos 3, 4, 5 independientes para Kalman/EKF/UKF: Alteraría la numeración original
  (spec dice 5 módulos) y rompería la coherencia de "Familia Kalman".

---

## Decisión 6: Dataset Sintético — Problema de Seguimiento

**Decision**: Seguimiento de vehículo 1D/2D con tres escenarios de complejidad creciente
(S1 lineal-Gaussiano, S2 no lineal suave, S3 no lineal fuerte), todos generados con
`np.random.seed(42)`, T=200, Q=0.1, R=1.0.

**Rationale**:
- El seguimiento de vehículo es intuitivo para cualquier estudiante de ingeniería.
- Los tres escenarios permiten mostrar exactamente cuándo cada filtro falla vs. prospera.
- Parámetros calibrados para que la convergencia sea observable en < 50 pasos (pedagógicamente
  satisfactorio) pero no trivial.

**Alternatives considered**:
- Problema de localización de robot: Más clásico en literatura SMC, pero requiere mapa 2D
  que añade complejidad de visualización no relacionada con el filtro.
- Péndulo no lineal: Elegante pero difícil de motivar para audiencia mixta sin contexto previo.

---

## Decisión 7: Persistencia SQLite — Scope

**Decision**: SQLite se usa para (a) caché de resultados de simulación y (b) registro de
progreso del estudiante (módulos completados). No se usa para almacenar el dataset sintético
(se genera en cada ejecución del notebook para garantizar reproducibilidad).

**Rationale**: Constitution Principio III exige SQLite para toda persistencia. El caché de
simulaciones acelera re-ejecuciones en clase; el registro de progreso permite al instructor
verificar avance. Ambos son optativos — los notebooks funcionan sin la base de datos.

**Alternatives considered**:
- Almacenar dataset en SQLite: Descartado — la generación en-notebook garantiza reproducibilidad
  y el dataset es pequeño (≤ 1000 puntos).
- JSON para progreso: Descartado — constitution exige SQLite.

---

## Decisión 8: CLI Tool

**Decision**: CLI usando `typer` con subcomandos `filtros run`, `filtros plot`, `filtros export`.

**Rationale**: Constitution Principio IV exige comandos ≤ 3 tokens. `typer` genera help
automático y tiene anotaciones de tipo nativas de Python 3.12. La CLI es conveniente pero
secundaria — el curso vive en notebooks; la CLI es para usuarios avanzados o instructores.

**Alternatives considered**:
- `argparse`: Verboso, sin type hints nativas.
- `click`: Válido, pero `typer` es más ergonómico con type hints de Python 3.12.
