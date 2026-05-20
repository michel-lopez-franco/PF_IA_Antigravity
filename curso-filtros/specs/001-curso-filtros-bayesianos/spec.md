# Feature Specification: Curso Completo de Filtros Bayesianos

**Feature Branch**: `001-curso-filtros-bayesianos`

**Created**: 2026-05-20

**Status**: Draft

**Input**: User description: "Quiero construir un curso completo de Filtros Bayesianos desde cero para estudiantes de ingeniería."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Progresión Pedagógica Completa (Priority: P1)

Un estudiante de ingeniería sin conocimiento previo de filtros bayesianos recorre los cinco
módulos en orden, partiendo de fundamentos de probabilidad e inferencia bayesiana hasta llegar
al proyecto integrador comparativo. Cada módulo está diseñado para ser autocontenido dado que
los módulos anteriores se han completado, con prerequisitos explícitos que señalan exactamente
qué conceptos se necesitan.

**Why this priority**: Sin una progresión pedagógica clara y sin saltos lógicos, el estudiante
queda bloqueado antes de llegar a los filtros. Es el flujo principal del curso y la base de todos
los demás.

**Independent Test**: Se puede validar completando únicamente el Módulo 1 (probabilidad e
inferencia bayesiana) y verificando que el estudiante puede resolver los ejercicios de evaluación
con los criterios de éxito definidos en ese módulo — entregando valor de aprendizaje sin necesidad
de los módulos siguientes.

**Acceptance Scenarios**:

1. **Given** el estudiante abre el Módulo 1 sin haber visto material previo del curso,
   **When** sigue las secciones en orden (Objetivos → Prerequisitos → Intuición → Derivación →
   Ejemplo numérico → Ejercicios → Evaluación),
   **Then** puede completar la evaluación del módulo y verificar sus respuestas con los
   criterios de éxito definidos.

2. **Given** el estudiante termina el Módulo N,
   **When** abre el Módulo N+1 y lee la sección "Prerequisitos",
   **Then** todos los conceptos listados como requisito corresponden exactamente a contenido
   cubierto en módulos anteriores — sin referencias a material no enseñado.

3. **Given** el estudiante completa los cinco módulos en orden,
   **When** abre el Módulo 5 (proyecto integrador),
   **Then** puede implementar y comparar los cuatro filtros en un problema de estimación de
   estado común usando únicamente lo aprendido en los módulos 1–4.

---

### User Story 2 - Implementación Práctica Autoguiada (Priority: P2)

Un estudiante abre el notebook práctico de cualquier módulo, ejecuta todas las celdas con
"Run All" en un entorno limpio, y obtiene resultados numéricos que puede verificar contra
los valores de referencia incluidos en el mismo notebook. Completa los ejercicios guiados
con el andamiaje provisto y avanza hacia los retos opcionales si lo desea.

**Why this priority**: La mitad del curso es práctica (principio 50/50). Sin notebooks
funcionales y autoexplicativos, el conocimiento teórico no se consolida en habilidad real.

**Independent Test**: El notebook práctico del Módulo 2 (filtro bayesiano discreto) se puede
ejecutar de inicio a fin sin material externo, generando gráficas verificables con tolerancias
definidas — entregando valor de práctica independientemente de los otros módulos.

**Acceptance Scenarios**:

1. **Given** el estudiante tiene Python y las dependencias instaladas según `pyproject.toml`,
   **When** abre cualquier notebook práctico y ejecuta "Run All",
   **Then** todas las celdas completan sin error y los resultados numéricos están dentro
   de la tolerancia especificada en la celda de validación.

2. **Given** el estudiante lee un ejercicio guiado,
   **When** completa los pasos con el andamiaje provisto (celdas parcialmente llenadas),
   **Then** obtiene un resultado verificable definido en el criterio de éxito del ejercicio.

3. **Given** el estudiante implementa un filtro en el notebook práctico,
   **When** compara su resultado con el valor de referencia (`scipy` o solución analítica),
   **Then** la diferencia es ≤ la tolerancia numérica especificada (e.g., RMSE < 0.05).

---

### User Story 3 - Autoevaluación con Criterios Medibles (Priority: P3)

Un estudiante completa la mini-evaluación de cada módulo y determina por sí mismo si alcanzó
los objetivos de aprendizaje, usando las rúbricas de evaluación que especifican salidas
numéricas esperadas o comportamientos observables concretos.

**Why this priority**: Sin evaluación autoguiada con criterios claros, el estudiante no sabe
cuándo ha dominado un módulo lo suficiente para avanzar al siguiente.

**Independent Test**: El estudiante resuelve la evaluación del Módulo 3 (filtro de Kalman),
compara sus respuestas con la rúbrica, y determina sin ambigüedad si aprobó o qué debe repasar.

**Acceptance Scenarios**:

1. **Given** el estudiante completa la sección "Evaluación" de un módulo,
   **When** consulta la rúbrica correspondiente,
   **Then** cada criterio de la rúbrica tiene una salida esperada concreta (número, gráfica
   con características específicas, o afirmación verificable en código).

2. **Given** el estudiante no pasa un criterio de evaluación,
   **When** consulta la sección "Errores comunes" del mismo módulo,
   **Then** encuentra documentado el síntoma que está experimentando con su procedimiento
   de diagnóstico y resolución.

---

### User Story 4 - Proyecto Integrador Comparativo (Priority: P4)

Un estudiante que completó los módulos 1–4 abre el Módulo 5 y trabaja con un problema unificado
de estimación de estado (seguimiento de posición con ruido gaussiano y no gaussiano) en el que
aplica los cuatro filtros aprendidos, genera métricas comparativas y articula cuándo usar cada
uno.

**Why this priority**: Es el desemboque natural del curso — donde el estudiante demuestra dominio
integrado. Depende de los cuatro módulos anteriores, por eso es P4.

**Independent Test**: Un estudiante con los notebooks 1–4 completos puede ejecutar el Módulo 5
de inicio a fin, obtener la tabla comparativa de métricas y redactar la justificación de
selección de filtro según los supuestos del modelo.

**Acceptance Scenarios**:

1. **Given** el estudiante tiene los resultados numéricos de los módulos 1–4,
   **When** ejecuta el notebook guiado del Módulo 5 con "Run All",
   **Then** obtiene una tabla comparativa con al menos tres métricas para los cinco métodos
   (Bayes discreto, Kalman lineal, EKF, UKF, Partículas) sobre el dataset sintético del curso,
   incluyendo sub-análisis de la familia Kalman.

2. **Given** el estudiante completa la tabla comparativa,
   **When** responde las preguntas de justificación guiada,
   **Then** produce respuestas que identifican correctamente los supuestos de cada método y el
   filtro más adecuado para cada escenario del problema — verificable con la rúbrica del Módulo 5.

3. **Given** el estudiante de posgrado completa el notebook guiado,
   **When** aborda la extensión abierta opcional,
   **Then** aplica al menos tres métodos a un problema distinto elegido libremente y redacta
   una justificación sin preguntas guiadas, argumentando desde los supuestos del modelo.

---

### Edge Cases

- ¿Qué pasa si el estudiante intenta abrir el Módulo 3 sin haber completado el Módulo 2?
  La sección "Prerequisitos" del Módulo 3 lista los conceptos requeridos; el estudiante puede
  volver al módulo correspondiente — el curso no bloquea técnicamente, solo pedagógicamente.
- ¿Qué pasa si el notebook produce resultados numéricos diferentes a los esperados?
  La celda de validación incluye `assert abs(resultado - referencia) < tolerancia` con un
  mensaje de error que apunta a la sección "Errores comunes" relevante.
- ¿Qué pasa si el dataset sintético no se genera (falla el seed o la librería)?
  El notebook incluye una celda de verificación de entorno al inicio con mensajes de error
  accionables si alguna dependencia falta.
- ¿Qué pasa con estudiantes que ya conocen parte del material?
  La sección "Prerequisitos" permite al estudiante evaluar si puede saltar contenido;
  la evaluación de cada módulo puede usarse como diagnóstico de entrada.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El curso DEBE contener exactamente cinco módulos en el siguiente orden:
  (1) Fundamentos de Probabilidad e Inferencia Bayesiana,
  (2) Filtro Bayesiano Discreto,
  (3) Familia Kalman — Filtro de Kalman Lineal + EKF (derivación via Jacobiano) + UKF
      (transformada unscented / sigma points, derivación completa),
  (4) Filtro de Partículas (Sequential Monte Carlo),
  (5) Proyecto Integrador Comparativo.
  El Módulo 3 DEBE derivar formalmente los tres miembros de la familia Kalman sin omitir pasos.

- **FR-002**: Cada módulo DEBE contener las siete secciones de la Estructura de Módulo Estándar
  (Objetivos, Prerequisitos, Intuición, Derivación formal, Ejemplo numérico, Ejercicios guiados,
  Evaluación), más las secciones "Errores comunes" y "Cierre reflexivo" (¿Qué aprendiste? /
  ¿Qué sigue?).

- **FR-003**: Cada módulo DEBE entregar dos artefactos: un notebook teórico (derivaciones,
  intuición, ejemplos numéricos paso a paso) y un notebook práctico (simulaciones, ejercicios
  ejecutables, validación numérica).

- **FR-004**: Todos los notebooks DEBEN ejecutar de inicio a fin con "Run All" en un entorno
  limpio con las dependencias especificadas en `pyproject.toml`, sin intervención manual.

- **FR-005**: El curso DEBE incluir un dataset sintético generado por código dentro de los propios
  notebooks (sin descargas externas). El dataset DEBE aumentar en complejidad de módulo a módulo
  y usarse de forma consistente en el Módulo 5 para la comparación.

- **FR-006**: Cada notebook práctico DEBE incluir una sección de validación numérica que verifique
  el resultado del filtro implementado por el estudiante contra una referencia conocida.
  Las implementaciones del estudiante DEBEN construirse exclusivamente con NumPy y SciPy.
  Las celdas de validación PUEDEN usar `filterpy` o `pykalman` como referencia de librería;
  estas celdas DEBEN estar claramente marcadas como "Celda de validación — no modifiques" y
  DEBEN ejecutar antes que la comparación para que el estudiante vea la diferencia directamente.

- **FR-007**: Cada módulo DEBE documentar al menos dos errores comunes con: (1) síntoma
  observable, (2) procedimiento de diagnóstico, (3) resolución correcta.

- **FR-008**: El curso DEBE incluir una rúbrica de evaluación por módulo con criterios
  expresados como salidas numéricas con tolerancias, características de gráficas, o
  afirmaciones verificables en código.

- **FR-009**: El Módulo 5 DEBE entregar dos artefactos independientes:
  (1) **Notebook guiado (evaluación base)** — estructura fija con andamiaje completo que
      compara los cinco métodos (Bayes discreto, Kalman lineal, EKF, UKF, Partículas) sobre el
      dataset sintético del curso con al menos tres métricas y sección guiada de justificación;
      accesible para la audiencia de carrera.
  (2) **Extensión abierta (reto opcional)** — el estudiante elige un problema de estimación de
      estado distinto, selecciona métricas adicionales, y redacta una justificación no guiada;
      orientado a estudiantes de posgrado o avanzados.

- **FR-010**: La sección de justificación del notebook guiado DEBE incluir preguntas estructuradas
  que lleven al estudiante a articular: (a) los supuestos de cada método, (b) el escenario donde
  cada supuesto se viola, y (c) el método más adecuado para cada variante del problema.
  La extensión abierta NO DEBE incluir preguntas guiadas; el estudiante redacta la justificación
  con libertad de argumentación.

- **FR-011**: Todos los notebooks DEBEN fijar la semilla aleatoria en la primera celda de código
  (`np.random.seed(42)`) para garantizar reproducibilidad total.

- **FR-012**: Todo el contenido DEBE estar escrito en español técnico. Los términos en inglés
  que se usen convencionalmente (e.g., "prior", "likelihood", "belief") DEBEN definirse
  en español en su primera aparición en cada módulo.

- **FR-013**: Los ejercicios de cada módulo DEBEN estar graduados en dos niveles para atender
  la audiencia mixta: (1) un ejercicio base con andamiaje completo, completable en < 30 minutos,
  diseñado para estudiantes de carrera; (2) al menos un reto opcional sin andamiaje, de mayor
  complejidad matemática o computacional, orientado a estudiantes de posgrado o avanzados.

### Key Entities

- **Módulo**: Unidad de aprendizaje completa con nueve secciones obligatorias, dos notebooks
  asociados y una rúbrica de evaluación. Tiene prerequisitos explícitos que referencian módulos
  anteriores.

- **Notebook Teórico**: Documento Jupyter autoexplicativo con derivaciones matemáticas
  paso a paso, intuición narrativa, y ejemplos numéricos trabajados con valores concretos.
  Ejecutable con "Run All".

- **Notebook Práctico**: Documento Jupyter con simulaciones interactivas, ejercicios
  parcialmente andamiados, validación numérica automática y retos opcionales.
  Ejecutable con "Run All".

- **Dataset Sintético**: Serie de datos generada por código (semilla fija) que modela un
  problema de estimación de estado (e.g., seguimiento de posición con ruido gaussiano).
  Se introduce en el Módulo 2 y se reutiliza con extensiones en módulos posteriores.

- **Rúbrica de Evaluación**: Documento por módulo con criterios de éxito medibles
  (valores numéricos con tolerancias, características observables de gráficas, o aserciones
  en código) que permiten autoevaluación sin calificador externo.

- **Filtro**: Modelo probabilístico implementado como clase o función Python tipada, con sus
  supuestos documentados, derivación formal en el notebook teórico, y validación numérica en
  el notebook práctico. El curso incluye cinco implementaciones: Bayes discreto, Kalman lineal,
  EKF (Jacobiano analítico), UKF (sigma points), y Filtro de Partículas (SMC).

- **EKF (Filtro de Kalman Extendido)**: Variante del Kalman para sistemas no lineales que
  linealiza las funciones de transición y observación via Jacobiano en cada paso de tiempo.
  Derivación formal incluida en el Módulo 3.

- **UKF (Filtro de Kalman Unscented)**: Variante del Kalman que propaga sigma points
  deterministas a través de funciones no lineales sin linealizar (transformada unscented).
  Derivación completa de la selección de sigma points y pesos incluida en el Módulo 3.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un estudiante con conocimiento básico de Python y álgebra lineal puede completar
  cada módulo en orden sin necesidad de material externo — el 100% del contenido necesario
  está en los notebooks del curso.

- **SC-002**: El 100% de los notebooks ejecuta sin errores desde la primera celda hasta la
  última en un entorno limpio con las dependencias listadas en `pyproject.toml`.

- **SC-003**: Al final de cada módulo práctico, el estudiante obtiene resultados numéricos
  que coinciden con los valores de referencia dentro de la tolerancia especificada en la
  celda de validación (tolerancia definida por módulo, e.g., RMSE ≤ 0.05 para el
  filtro de Kalman en el dataset sintético estándar).

- **SC-004**: Al completar el notebook guiado del Módulo 5, el estudiante genera una tabla
  comparativa con al menos tres métricas (RMSE, varianza del error, tiempo de cómputo) para
  los cinco métodos sobre el dataset sintético del curso, incluyendo sub-análisis de la
  familia Kalman (lineal vs EKF vs UKF).

- **SC-005**: Al completar la sección de justificación guiada del Módulo 5, el estudiante
  responde correctamente las preguntas estructuradas identificando: supuestos de cada método,
  escenario donde se violan, y método más adecuado para cada variante del problema.

- **SC-008** *(audiencia posgrado)*: Al completar la extensión abierta opcional, el estudiante
  presenta un problema de estimación de estado distinto, aplica al menos tres de los cinco
  métodos, define sus propias métricas de comparación, y redacta una justificación no guiada
  coherente con los supuestos del modelo elegido.

- **SC-006**: Cada módulo contiene al menos un ejercicio base con criterio de éxito verificable
  en código (`assert` o comparación numérica) que un estudiante puede completar en menos
  de 30 minutos usando el andamiaje provisto.

- **SC-007**: La sección "Errores comunes" de cada módulo cubre al menos 2 de los errores que
  un revisor pedagógico identifica como los más frecuentes en estudiantes que aprenden ese
  filtro por primera vez.

## Clarifications

### Session 2026-05-20

- Q: ¿Cuál es el perfil académico objetivo del estudiante? → A: Mixto — estudiantes de carrera (4to–6to semestre) y posgrado en el mismo curso.
- Q: ¿Cuántas horas de trabajo total por módulo? → A: Variable por módulo, determinada por el contenido necesario (sin límite fijo).
- Q: ¿Qué variantes de filtros cubre el curso en sus derivaciones formales? → A: Máxima profundidad — Kalman lineal + EKF (linealización via Jacobiano) + UKF (transformada unscented / sigma points), con derivación completa de cada uno.
- Q: ¿Qué herramientas puede usar el estudiante en los notebooks prácticos? → A: NumPy/SciPy para implementar desde cero; filterpy/pykalman permitidos únicamente en celdas de validación.
- Q: ¿Cuánta autonomía tiene el estudiante en el Módulo 5 (proyecto integrador)? → A: Dos entregables — notebook guiado con andamiaje como evaluación base + extensión abierta opcional orientada a posgrado.

## Assumptions

- El curso atiende una **audiencia mixta**: estudiantes de carrera en ingeniería (4to–6to semestre,
  con cálculo diferencial e integral y álgebra lineal aprobados, sin probabilidad bayesiana formal)
  y estudiantes de posgrado (bases matemáticas sólidas, posiblemente débiles en implementación
  práctica). El andamiaje matemático DEBE ser suficiente para que la audiencia de carrera avance
  sin bloquearse; los retos opcionales de cada módulo (FR-013) DEBEN ser suficientemente
  desafiantes para la audiencia de posgrado. No se asume experiencia previa en filtros bayesianos
  para ninguno de los dos grupos.

- El Módulo 3 (familia Kalman) requiere que el estudiante comprenda derivadas parciales
  (Jacobianos para EKF) y esperanza matemática de funciones no lineales (transformada unscented
  para UKF). El notebook teórico DEBE incluir un recordatorio autocontenido de estos
  prerequisitos matemáticos antes de las derivaciones correspondientes.

- El entorno de trabajo es Jupyter Notebook o JupyterLab ejecutado localmente. No se requiere
  conexión a internet durante las sesiones prácticas.

- Los módulos se estudian en orden secuencial (1 → 2 → 3 → 4 → 5). El curso no está diseñado
  para consumo desordenado, aunque cada módulo indica sus prerequisitos explícitamente.

- El dataset sintético es generado 100% por código en los notebooks (no requiere archivos
  descargados ni bases de datos externas).

- La evaluación es autoguiada: el estudiante usa las rúbricas provistas sin necesidad
  de un calificador externo para los ejercicios guiados. El Módulo 5 puede requerir
  revisión de pares para la sección de justificación cualitativa.

- La duración de cada módulo es variable y está determinada por el contenido necesario para
  cubrir sus objetivos de aprendizaje con rigor, sin imponer un límite de horas fijo. El Módulo 5
  (proyecto integrador) se espera que sea notablemente más largo que los módulos 1–4. El único
  tiempo acotado es el ejercicio base de cada módulo (< 30 minutos, SC-006).

- El tamaño del dataset sintético es deliberadamente pequeño (≤ 1000 puntos por simulación)
  para garantizar tiempos de ejecución de notebook < 60 segundos en hardware estándar
  de estudiante.

- Se asume Python 3.12+ y las dependencias especificadas en `pyproject.toml` del repositorio.
  No se asume disponibilidad de GPU ni entornos de cómputo en la nube.

- Las implementaciones de filtros en los notebooks prácticos usan exclusivamente **NumPy y SciPy**;
  `filterpy` y `pykalman` están permitidos únicamente en celdas de validación explícitamente
  marcadas. Esta restricción garantiza que el estudiante comprenda cada operación del algoritmo
  sin que una librería la oculte.
