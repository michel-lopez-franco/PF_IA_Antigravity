# Calidad de Módulo — Checklist de Publicación: Curso de Filtros Bayesianos

**Purpose**: Validar que los requisitos de cada módulo están completos, claros y alineados
antes de pasar del estado `en_revision` a `publicado`. Este checklist es un
"test de unidad para los requisitos escritos" — NO verifica si el código funciona,
sino si las especificaciones son suficientemente precisas para que puedan construirse
y evaluarse sin ambigüedad.

**Created**: 2026-05-20
**Feature**: [spec.md](../spec.md) | [plan.md](../plan.md) | [contracts/notebook-contract.md](../contracts/notebook-contract.md)
**Scope**: Aplicar a cada módulo (M1–M5) antes de marcarlo como publicado.

---

## 1. Claridad Conceptual

*¿Están especificados los requisitos de claridad conceptual con criterios objetivos?*

- [ ] CHK001 — ¿Se define en la especificación qué constituye una sección de "Intuición" suficiente antes de presentar la derivación formal (extensión mínima, ejemplos requeridos, prohibición de saltos lógicos)? [Clarity, Spec §FR-002]
- [ ] CHK002 — ¿Están definidos los criterios para que un ejemplo numérico sea considerado "paso a paso" (número mínimo de pasos intermedios, nivel de detalle por paso)? [Clarity, Spec §FR-002]
- [ ] CHK003 — ¿Se especifica qué términos en inglés son admisibles sin traducción y cuáles requieren definición en español en cada módulo? [Completeness, Spec §FR-012]
- [ ] CHK004 — ¿Están definidos los requisitos para la sección "Objetivos": verbos de acción medibles, número mínimo de objetivos (≥3), nivel de especificidad (conductual vs. declarativo)? [Clarity, Spec §FR-002, contracts/notebook-contract.md]
- [ ] CHK005 — ¿Se especifica qué notación matemática DEBE estar definida explícitamente antes de usarse (subíndices de tiempo, dimensiones de vectores, operadores)? [Completeness, Gap]
- [ ] CHK006 — ¿Están definidos los requisitos para que la sección "Prerequisitos" sea autocontenida (qué nivel de granularidad al listar conceptos, si incluye referencias a módulos anteriores o solo nombres de conceptos)? [Clarity, Spec §US1-AC2]

---

## 2. Precisión Matemática

*¿Están las derivaciones y validaciones especificadas con rigor suficiente para ser verificables?*

- [ ] CHK007 — ¿Se especifica el estándar de completitud para las derivaciones: qué pasos pueden omitirse sin violar el principio de "sin saltos lógicos" y cómo se documenta una omisión (cita, referencia a apéndice)? [Clarity, Spec §FR-001]
- [ ] CHK008 — ¿Están definidas las tolerancias numéricas exactas para la celda de validación de cada módulo (`|RMSE_student - RMSE_ref| < TOL`, con el valor de TOL especificado)? [Measurability, Spec §FR-006, FR-008]
- [ ] CHK009 — ¿Se especifica qué supuestos del modelo DEBEN enunciarse explícitamente antes de cada derivación (linealidad, gaussianidad, independencia del ruido, estacionariedad)? [Completeness, Gap]
- [ ] CHK010 — ¿Están definidos los requisitos para la anotación de dimensiones de matrices y vectores en la derivación (e.g., "anotar shape (n×n) al introducir cada matriz")? [Clarity, Gap]
- [ ] CHK011 — ¿Se especifica cómo DEBE verificarse que `covarianza` es positiva-definida y qué excepción lanza el filtro si no lo es (`ValueError`)? [Completeness, Spec §FR-006, contracts/filter-contract.md §Garantías]
- [ ] CHK012 — ¿Están definidos los criterios para determinar si la referencia de validación (filterpy/scipy) está suficientemente documentada en la celda marcada? [Clarity, Spec §FR-006]

---

## 3. Continuidad Narrativa

*¿Están especificados los requisitos de cohesión entre secciones y entre notebooks?*

- [ ] CHK013 — ¿Se especifica qué información DEBE contener la sección "¿Qué sigue?" para ser considerada válida (nombre del módulo siguiente, concepto que el módulo actual habilita, breve descripción del puente conceptual)? [Completeness, Spec §FR-002, contracts/notebook-contract.md]
- [ ] CHK014 — ¿Están definidos los requisitos de transición entre celdas code y markdown dentro del notebook (texto introductorio obligatorio antes de código, texto de interpretación después de cada resultado)? [Completeness, Gap]
- [ ] CHK015 — ¿Se especifica cómo DEBE mantenerse la consistencia terminológica dentro de un notebook y entre el notebook teórico y el práctico del mismo módulo (glosario de referencia, prohibición de sinónimos no definidos)? [Consistency, Spec §FR-012]
- [ ] CHK016 — ¿Están definidos los requisitos de la sección "¿Qué aprendiste?": primera persona plural, número mínimo de ítems (≥5), relación con los objetivos declarados al inicio? [Completeness, Spec §FR-002, contracts/notebook-contract.md]
- [ ] CHK017 — ¿Se especifica la estructura narrativa que vincula la sección de Intuición con la Derivación formal (cómo se introduce la necesidad de la derivación después de la intuición)? [Clarity, Gap]

---

## 4. Reproducibilidad del Notebook

*¿Están especificados los requisitos de ejecución determinista y entorno limpio?*

- [ ] CHK018 — ¿Se especifica en qué celda exacta DEBE aparecer `np.random.seed(42)`, cuáles imports son obligatorios en esa misma celda, y si otros seeds adicionales están prohibidos? [Clarity, Spec §FR-011, contracts/notebook-contract.md §Celda 2/3]
- [ ] CHK019 — ¿Están definidos los requisitos de la celda de verificación de entorno de la práctica: qué versiones DEBE verificar (`assert sys.version_info >= (3, 12)`), qué paquetes, y qué mensaje de error DEBE mostrar si faltan? [Completeness, Spec §FR-004, contracts/notebook-contract.md §Celda 3]
- [ ] CHK020 — ¿Se especifica el comportamiento esperado y el mensaje de fallo cuando el smoke-test de tiempo supera el límite (`assert tiempo < 60.0`)? [Clarity, Spec §FR-004, contracts/notebook-contract.md §Reglas]
- [ ] CHK021 — ¿Están definidos los requisitos para la celda de validación numérica: formato exacto del mensaje de assert, qué variable contiene el resultado del estudiante, qué variable contiene la referencia? [Clarity, Spec §FR-006, contracts/notebook-contract.md §Celda de validación]
- [ ] CHK022 — ¿Se especifica si las figuras Plotly DEBEN guardarse como HTML, solo mostrarse en el notebook, o ambas, y cuál es el nombre de archivo esperado? [Ambiguity, Gap]
- [ ] CHK023 — ¿Están definidos los requisitos para garantizar que el notebook no dependa de estado de sesión anterior al ejecutarse con "Run All" desde cero (variables globales, side effects entre celdas)? [Completeness, Spec §FR-004]
- [ ] CHK024 — ¿Se especifica cómo DEBE estar marcada la "celda de validación" para que nbval y el estudiante puedan identificarla inequívocamente? [Clarity, Spec §FR-006, contracts/notebook-contract.md §Celda 4]

---

## 5. Dificultad Progresiva

*¿Están especificados los criterios de progresión de dificultad dentro y entre módulos?*

- [ ] CHK025 — ¿Se especifica la métrica o criterio para determinar que un ejercicio "base" es completable en ≤30 min por el perfil de estudiante objetivo (carrera, 4°–6° semestre)? [Measurability, Gap]
- [ ] CHK026 — ¿Están definidos los requisitos que distinguen un ejercicio "base" de un ejercicio "reto": grado de andamiaje retirado, complejidad matemática adicional, tiempo estimado diferencial? [Clarity, Spec §FR-002]
- [ ] CHK027 — ¿Se especifica qué porción del código de cada ejercicio guiado DEBE estar pre-llenado (andamiaje) y qué partes son `# TODO`, con criterios para decidir la proporción? [Completeness, Spec §FR-006]
- [ ] CHK028 — ¿Están definidos los parámetros del dataset sintético que DEBEN aumentar en complejidad entre módulos y cuáles DEBEN permanecer constantes para permitir comparación en M5 (T, Q, R, seed, dimensión de estado)? [Completeness, Spec §FR-005, data-model.md §Dataset]
- [ ] CHK029 — ¿Se especifica cómo DEBE evidenciarse la progresión de M1 a M5 en el dataset sintético: qué característica nueva introduce cada escenario (S1, S2, S3)? [Clarity, Spec §FR-005, data-model.md §Progresión]
- [ ] CHK030 — ¿Están definidos los criterios para que la sección de "Ejercicios guiados" sea apropiada para la audiencia de carrera sin penalizar a la audiencia de posgrado (señalización de niveles)? [Completeness, Spec §US2, Clarification C1]

---

## 6. Cobertura de Errores Comunes

*¿Están los requisitos de la sección "Errores comunes" definidos con precisión diagnóstica?*

- [ ] CHK031 — ¿Se especifica qué constituye un "síntoma observable" en el contexto del curso: debe ser detectable por el estudiante sin ver el código interno del filtro, sin usar un debugger avanzado? [Clarity, Spec §FR-007]
- [ ] CHK032 — ¿Están definidos los criterios para seleccionar qué errores incluir en la sección: frecuencia esperada en estudiantes, impacto en la comprensión, errores ya observados en clases piloto o literatura docente? [Completeness, Gap]
- [ ] CHK033 — ¿Se especifica si cada error DEBE reproducirse con código ejecutable en el notebook (celda que genera el error) o basta con descripción en prosa? [Ambiguity, Spec §FR-007]
- [ ] CHK034 — ¿Están definidos los requisitos del procedimiento de diagnóstico para cada error (número mínimo de pasos, tipo de prints o asserts de diagnóstico que el estudiante puede usar)? [Completeness, Spec §FR-007]
- [ ] CHK035 — ¿Se especifica si los errores DEBEN clasificarse por tipo (conceptual, de implementación, numérico) y si cada tipo DEBE estar cubierto en cada módulo? [Clarity, Gap]
- [ ] CHK036 — ¿Están definidos los requisitos de referencia cruzada entre la sección "Errores comunes" y los mensajes de las celdas de validación (el assert DEBE apuntar al error documentado)? [Consistency, Spec §FR-006, FR-007]

---

## 7. Alineación Teoría–Práctica–Evaluación

*¿Están los tres artefactos de cada módulo (teórico, práctico, rúbrica) especificados como un conjunto coherente?*

- [ ] CHK037 — ¿Se especifica la trazabilidad requerida entre secciones del notebook teórico y secciones del notebook práctico: cada derivación formal DEBE tener su ejercicio de implementación correspondiente? [Completeness, Spec §FR-003]
- [ ] CHK038 — ¿Están definidos los requisitos de cobertura de la rúbrica por módulo: número mínimo de criterios, proporción entre criterios numéricos y descriptivos, nivel base vs. reto? [Completeness, Spec §FR-008]
- [ ] CHK039 — ¿Se especifica la trazabilidad entre criterios de rúbrica y celdas del notebook práctico: cada criterio evaluable DEBE referenciar la celda o variable que genera el valor a comparar? [Clarity, Spec §FR-008]
- [ ] CHK040 — ¿Están definidos los requisitos de correspondencia entre la lista de "Objetivos" y la sección de "Evaluación": cada objetivo declarado DEBE tener al menos un criterio evaluable en la rúbrica? [Consistency, Spec §FR-002, FR-008]
- [ ] CHK041 — ¿Se especifica si la rúbrica DEBE incluir criterios que solo son verificables ejecutando el notebook práctico (vs. solo leyendo el notebook teórico), y en qué proporción? [Completeness, Spec §FR-008, Gap]
- [ ] CHK042 — ¿Están definidos los requisitos de consistencia entre la celda de validación numérica del notebook práctico y el criterio numérico correspondiente en la rúbrica (misma tolerancia, misma variable)? [Consistency, Spec §FR-006, FR-008]
- [ ] CHK043 — ¿Se especifica cómo la sección "¿Qué aprendiste?" DEBE reflejar los objetivos declarados al inicio del módulo (correspondencia directa, primera persona plural, ≥5 ítems)? [Consistency, Spec §FR-002, contracts/notebook-contract.md]

---

## 8. Consistencia Entre Módulos

*¿Están especificados los requisitos de coherencia del curso como unidad pedagógica?*

- [ ] CHK044 — ¿Se especifica qué convenciones de notación matemática DEBEN ser uniformes en todos los módulos (x̂ₖ para estado estimado, Pₖ para covarianza, z para observación, F/H para matrices de transición/observación)? [Consistency, Gap]
- [ ] CHK045 — ¿Están definidos los parámetros del dataset sintético que DEBEN permanecer idénticos en todos los módulos para habilitar la comparación en M5 (seed=42, T=200, Q=0.1, R=1.0, estado inicial [0.0, 1.0])? [Completeness, Spec §FR-005, data-model.md §Dataset]
- [ ] CHK046 — ¿Se especifica el mecanismo para verificar que el Módulo N+1 no asume conocimiento no cubierto en M1...MN (revisión de sección "Prerequisitos" contra contenido de módulos anteriores)? [Coverage, Spec §US1-AC2]
- [ ] CHK047 — ¿Están definidos los requisitos de consistencia de las celdas de setup entre todos los notebooks: qué imports, seed y assertions de versión son obligatorios en todos? [Consistency, Spec §FR-011, contracts/notebook-contract.md]

---

## Notas de Uso

- Marcar como completado: `- [x] CHK00N`
- Agregar hallazgos específicos inline después del ítem: `- [x] CHK007 ✓ TOL=1e-6 definida en plan.md §M3a`
- Usar `[BLOQUEANTE]` para ítems que impiden publicación
- Usar `[MENOR]` para ítems que se pueden resolver post-publicación con errata
- Escalar ítems sin respuesta a la tarea QA correspondiente en `tasks.md`
