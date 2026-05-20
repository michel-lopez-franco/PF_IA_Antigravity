# Contrato: Esquema de Celdas de Notebooks

**Branch**: `001-curso-filtros-bayesianos` | **Date**: 2026-05-20

Define la estructura de celdas obligatoria para cada tipo de notebook del curso.
Todo notebook DEBE cumplir este contrato para pasar validación con `nbval`.

## Tipo: Teórico

Secciones en orden obligatorio. La ausencia de cualquier sección bloquea el PR.

```
[CELDA 1]  Markdown — Header con:
           # <Título>
           **Módulo**: <ID> | **Tipo**: TEÓRICO | **Fecha**: YYYY-MM-DD
           > Prerequisitos: <lista>

[CELDA 2]  Markdown — ## Objetivos de aprendizaje
           Lista numerada ≥ 3 ítems, cada uno verbo de acción medible.

[CELDA 3]  Code — Seed + imports + verificación de versión:
           import numpy as np; import sys
           np.random.seed(42)
           assert sys.version_info >= (3, 12)

[CELDAS 4..N-5]  Alternadas Markdown+Code:
           ## Intuición (Markdown)
           ## Derivación formal (Markdown con LaTeX)
           Celdas Code de verificación tras cada derivación
           ## Ejemplo numérico paso a paso (Code+Markdown)

[CELDA N-4]  Markdown — ## Errores comunes
             ≥ 2 subsecciones con: **Síntoma**, **Diagnóstico**, **Solución**

[CELDA N-3]  Markdown — ## Evaluación
             Lista de problemas con criterios de éxito medibles

[CELDA N-2]  Markdown — ## ¿Qué aprendiste?
             Lista ≥ 5 ítems, primera persona plural ("Aprendimos que...")

[CELDA N-1]  Markdown — ## ¿Qué sigue?
             Nombre del siguiente módulo + cómo este habilita al siguiente
```

## Tipo: Práctico

```
[CELDA 1]  Markdown — Header con:
           # <Título> — Práctica
           **Módulo**: <ID> | **Tipo**: PRÁCTICO | **Fecha**: YYYY-MM-DD

[CELDA 2]  Code — Setup obligatorio:
           import numpy as np; import sys; import time
           np.random.seed(42)
           assert sys.version_info >= (3, 12)
           _t0 = time.time()

[CELDA 3]  Code — Generación del dataset:
           from src.utils.dataset import generar_dataset
           estados, observaciones = generar_dataset(escenario="S1", T=200, seed=42)

[CELDA 4]  Code — [CELDA DE VALIDACIÓN — NO MODIFICAR]
           # Referencia filterpy/scipy — resultado de referencia almacenado en rmse_ref
           from filterpy... ; rmse_ref = ...

[CELDAS 5..M]  Code+Markdown — Implementación del estudiante:
           Celdas con comentarios `# TODO: implementar <descripción>`

[CELDA M+1]  Code — Validación numérica automática:
           rmse_student = ...
           assert abs(rmse_student - rmse_ref) < TOL, f"RMSE {rmse_student:.4f} ≠ ref"
           assert np.all(np.isfinite(estado_estimado)), "NaN/inf detectado — ver Errores comunes"

[CELDA M+2]  Code+Markdown — ## Ejercicios guiados (base, ≤ 30 min)

[CELDA M+3]  Code+Markdown — ## Reto (opcional, sin andamiaje)

[CELDA M+4]  Code — Smoke-test de ejecución:
           tiempo = time.time() - _t0
           assert tiempo < 60.0, f"Notebook tardó {tiempo:.1f}s (máx 60s)"

[CELDA M+5]  Markdown — ## ¿Qué aprendiste? + ## ¿Qué sigue?
```

## Tipo: Guiado (Módulo 5 base)

Igual que Práctico pero sin celdas TODO — todas las celdas de implementación tienen
andamiaje completo. Sección adicional obligatoria:

```
[PENÚLTIMA SECCIÓN]  Markdown+Code — ## Justificación guiada
                     Exactamente 6 preguntas estructuradas con espacio de respuesta en Markdown.
                     Cada pregunta referencia la tabla comparativa generada arriba.
```

## Tipo: Extensión Abierta (Módulo 5 posgrado)

```
[CELDA 1]  Markdown — Header + instrucciones mínimas
[CELDA 2]  Code — np.random.seed(42) ÚNICAMENTE — sin más andamiaje
[CELDAS 3+]  El estudiante escribe libremente
[ÚLTIMA CELDA]  Markdown — ## Justificación (sin preguntas guiadas)
```

## Reglas de validación automática (nbval)

| Regla | Cómo se verifica |
|-------|-----------------|
| Celda 2/3 contiene `np.random.seed(42)` | Grep en metadata del notebook |
| Celda de validación presente y marcada | Tag `[CELDA DE VALIDACIÓN — NO MODIFICAR]` en celda |
| Sección `## ¿Qué aprendiste?` presente | nbval verifica que la celda no falla |
| Smoke-test de tiempo pasa | `assert tiempo < 60` en última celda Code |
| Sin NaN/inf en estimación | `assert np.all(np.isfinite(...))` en celda de validación |
