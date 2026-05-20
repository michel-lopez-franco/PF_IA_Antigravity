# Quickstart: Curso de Filtros Bayesianos

## Requisitos previos

- Python 3.12+
- `uv` (recomendado) o `pip`
- Jupyter Notebook o JupyterLab

## Instalación

```bash
# Clonar el repositorio
git clone <repo-url>
cd curso-filtros

# Instalar dependencias (recomendado con uv)
uv sync

# O con pip
pip install -e ".[dev]"
```

## Verificar instalación

```bash
make check        # mypy --strict + ruff check
make test         # pytest --cov --fail-under=80
make nbval        # nbval en todos los notebooks
filtros --help    # verifica que la CLI responde
```

## Comenzar el curso

```bash
# Abrir Jupyter Lab
jupyter lab

# O ir directamente al Módulo 1
jupyter notebook cursos/modulo_01_probabilidad/01_teoria.ipynb
```

**Orden recomendado**:
1. `cursos/modulo_01_probabilidad/` — Teoría → Práctica
2. `cursos/modulo_02_bayes_discreto/` — Teoría → Práctica
3. `cursos/modulo_03_familia_kalman/3a_kalman_lineal/` — Teoría → Práctica
4. `cursos/modulo_03_familia_kalman/3b_ekf/` — Teoría → Práctica
5. `cursos/modulo_03_familia_kalman/3c_ukf/` — Teoría → Práctica
6. `cursos/modulo_04_particulas/` — Teoría → Práctica
7. `cursos/modulo_05_proyecto_integrador/01_proyecto_guiado.ipynb`
8. (Opcional posgrado) `cursos/modulo_05_proyecto_integrador/02_extension_abierta.ipynb`

## Comandos CLI

```bash
filtros run   --modulo 2              # ejecuta notebook práctico M2 con nbconvert
filtros plot  --modulo 3a --scenario S1  # genera figura Plotly HTML
filtros export --modulo 1 --formato pdf  # exporta notebook a PDF con nbconvert
filtros --help                         # lista todos los comandos
```

## Ejecutar pruebas

```bash
# Solo tests unitarios (filtros en src/)
pytest tests/ -v

# Solo validación de notebooks
pytest --nbval-lax cursos/ -v

# Todo junto con cobertura
make ci
```

## Makefile de referencia

```makefile
check:   mypy src/ --strict && ruff check src/ tests/
test:    pytest tests/ --cov=src --cov-fail-under=80
nbval:   pytest --nbval-lax cursos/
ci:      make check && make test && make nbval
```
