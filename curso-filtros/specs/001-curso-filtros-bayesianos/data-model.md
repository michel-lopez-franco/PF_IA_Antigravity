# Data Model: Curso de Filtros Bayesianos

**Branch**: `001-curso-filtros-bayesianos` | **Date**: 2026-05-20

---

## Entidades del Dominio

### Módulo

Unidad de aprendizaje completa. Agrupa notebooks, rúbrica y sub-módulos opcionales.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | `str` | Identificador único, e.g. `"modulo_01"`, `"modulo_03_3a"` |
| `titulo` | `str` | Nombre legible, e.g. `"Fundamentos de Probabilidad"` |
| `orden` | `int` | Posición en la secuencia del curso (1–5, sub-módulos 3.1–3.3) |
| `prerequisitos` | `list[str]` | IDs de módulos que deben completarse antes |
| `notebooks` | `list[NotebookRef]` | Referencias a teorico y practico |
| `rubrica_path` | `str` | Ruta relativa a `rubrica.md` |
| `duracion_estimada` | `str` | Descripción textual (variable, sin límite fijo) |

**Restricciones**:
- `prerequisitos` solo puede referenciar módulos con `orden` menor.
- Todo módulo tiene exactamente 1 notebook teórico y 1 práctico, excepto M5 (2 notebooks).

---

### Notebook

Documento Jupyter (.ipynb). Tiene tipo (teórico o práctico) y estructura de secciones obligatorias.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `path` | `str` | Ruta relativa desde raíz del repo |
| `tipo` | `Literal["teorico", "practico", "guiado", "extension"]` | Variante |
| `modulo_id` | `str` | Módulo al que pertenece |
| `seed` | `int` | Semilla fija (siempre 42) |
| `dependencias_py` | `list[str]` | Paquetes requeridos (subset de pyproject.toml) |
| `tiempo_ejecucion_max_s` | `int` | Límite CI: 60 segundos |
| `secciones` | `list[SeccionNotebook]` | Secciones presentes (validadas por nbval) |

**Estados del ciclo de vida**:
`borrador` → `en_revision` → `aprobado` → `publicado`

**Reglas de validación**:
- `tipo == "practico"` requiere celda `[CELDA DE VALIDACIÓN — NO MODIFICAR]`.
- `tipo == "teorico"` requiere sección `## Errores comunes` con ≥ 2 ítems.
- Todos los tipos requieren `## ¿Qué aprendiste?` y `## ¿Qué sigue?` como últimas secciones.

---

### SeccionNotebook

Sección identificada dentro de un notebook (por su encabezado Markdown).

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `nombre` | `str` | Encabezado exacto, e.g. `"## Derivación formal"` |
| `obligatoria` | `bool` | Si su ausencia falla la validación |
| `orden_minimo` | `int` | Índice de celda mínimo donde debe aparecer |

---

### Dataset Sintético

Datos de simulación generados por código, con parámetros fijos y reproducibles.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `escenario_id` | `Literal["S1", "S2", "S3"]` | Escenario de complejidad |
| `T` | `int` | Pasos de tiempo (fijo: 200) |
| `seed` | `int` | Semilla NumPy (fijo: 42) |
| `Q` | `float` | Varianza ruido de proceso (fijo: 0.1) |
| `R` | `float` | Varianza ruido de medición (fijo: 1.0) |
| `estado_inicial` | `np.ndarray` | `[0.0, 1.0]` (posición, velocidad) |
| `estados_verdaderos` | `np.ndarray` | Shape `(T, n_estados)` |
| `observaciones` | `np.ndarray` | Shape `(T, n_obs)` |

**Progresión por módulo**:
- M2: Versión discretizada de S1 (grilla 20 posiciones)
- M3a: S1 continuo
- M3b: S2 (observación no lineal: rango)
- M3c: S2 mismo (para comparación directa EKF vs UKF)
- M4: S3 (dinámica no lineal, ruido no Gaussiano)
- M5: S1 + S2 + S3 juntos

---

### Filtro (implementación Python)

Clase Python tipada que implementa el protocolo de filtrado.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `nombre` | `str` | Nombre canónico del filtro |
| `modulo_origen` | `str` | Módulo donde se deriva y presenta |
| `supuestos` | `list[str]` | Supuestos del modelo (linealidad, Gaussianidad, etc.) |
| `complejidad_O` | `str` | Complejidad por paso de tiempo, e.g. `"O(n^3)"` |
| `ruta_impl` | `str` | Ruta en `src/filtros/` |

**Filtros del curso**:

| Nombre | Módulo | Supuestos clave | Complejidad |
|--------|--------|-----------------|-------------|
| `BayesFiltroDiscreto` | M2 | Estado discreto, modelo de transición finito | O(N²) |
| `KalmanLineal` | M3a | Lineal, Gaussiano | O(n³) |
| `EKFiltro` | M3b | No lineal diferenciable, Gaussiano | O(n³) |
| `UKFiltro` | M3c | No lineal, Gaussiano | O(n³) |
| `FiltroPArticulas` | M4 | Sin supuestos distribucionales (general) | O(N·n) |

---

### RúbricaCriterio

Criterio individual dentro de una rúbrica de evaluación.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | `str` | e.g. `"R-M2-01"` |
| `descripcion` | `str` | Qué se verifica |
| `metodo` | `Literal["assert_numerico", "visual", "prosa"]` | Cómo se verifica |
| `tolerancia` | `float | None` | Solo para `assert_numerico` |
| `nivel` | `Literal["base", "reto"]` | Audiencia objetivo |
| `codigo_verificacion` | `str | None` | Snippet de assert si aplica |

---

### ProgresoEstudiante (SQLite)

Registro local del avance del estudiante. Almacenado en `filtros.db`.

```sql
CREATE TABLE IF NOT EXISTS progreso (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    modulo_id   TEXT    NOT NULL,
    notebook    TEXT    NOT NULL,
    completado  INTEGER NOT NULL DEFAULT 0,  -- 0=no, 1=sí
    rmse_ultimo REAL,
    ts_ultimo   TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

**Restricciones**: `(modulo_id, notebook)` es UNIQUE.

---

## Relaciones

```
Módulo 1──* NotebookRef ──► Notebook
Módulo *──* Módulo (prerequisitos)
Módulo 1──1 Rubrica ──* RúbricaCriterio
Filtro 1──1 Notebook (práctico, celda de validación)
Dataset 1──* Módulo (misma semilla, parámetros compartidos)
Notebook 1──* ProgresoEstudiante (rastrea por notebook)
```

---

## Esquema de Migración SQLite

`db/migrations/001_initial.sql`:
```sql
CREATE TABLE IF NOT EXISTS progreso (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    modulo_id   TEXT    NOT NULL,
    notebook    TEXT    NOT NULL,
    completado  INTEGER NOT NULL DEFAULT 0,
    rmse_ultimo REAL,
    ts_ultimo   TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE(modulo_id, notebook)
);

CREATE TABLE IF NOT EXISTS metrica_run (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    modulo_id   TEXT    NOT NULL,
    filtro      TEXT    NOT NULL,
    escenario   TEXT    NOT NULL,
    rmse        REAL,
    varianza    REAL,
    tiempo_s    REAL,
    ts          TEXT    NOT NULL DEFAULT (datetime('now'))
);
```
