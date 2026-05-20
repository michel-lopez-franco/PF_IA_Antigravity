"""CLI del curso de filtros — comandos cortos (máx 3 tokens por comando)."""

from pathlib import Path
from typing import Annotated, Optional

import typer

app = typer.Typer(
    name="filtros",
    help="Herramientas CLI para el Curso de Filtros Bayesianos.",
    no_args_is_help=True,
)

_CURSOS_DIR = Path(__file__).parent.parent.parent / "cursos"
_DOCS_DIR = Path(__file__).parent.parent.parent / "docs" / "notebooks"

_MODULO_MAP: dict[str, str] = {
    "1": "modulo_01_probabilidad",
    "2": "modulo_02_bayes_discreto",
    "3a": "modulo_03_familia_kalman/3a_kalman_lineal",
    "3b": "modulo_03_familia_kalman/3b_ekf",
    "3c": "modulo_03_familia_kalman/3c_ukf",
    "4": "modulo_04_particulas",
    "5": "modulo_05_proyecto_integrador",
}


def _resolver_modulo(modulo: str) -> Path:
    key = modulo.strip().lower()
    if key not in _MODULO_MAP:
        raise typer.BadParameter(
            f"Módulo '{modulo}' no reconocido. Opciones: {', '.join(_MODULO_MAP)}"
        )
    return _CURSOS_DIR / _MODULO_MAP[key]


@app.command()
def run(
    modulo: Annotated[str, typer.Option("--modulo", "-m", help="ID del módulo (1,2,3a,3b,3c,4,5)")],
    notebook: Annotated[
        Optional[str],
        typer.Option("--notebook", "-n", help="Nombre del notebook (default: 02_practica.ipynb)"),
    ] = None,
) -> None:
    """Ejecuta el notebook práctico de un módulo con nbconvert."""
    import subprocess

    modulo_path = _resolver_modulo(modulo)
    nb_name = notebook or "02_practica.ipynb"
    nb_path = modulo_path / nb_name

    if not nb_path.exists():
        typer.echo(f"Error: notebook no encontrado en {nb_path}", err=True)
        typer.echo("Verifica que el módulo esté creado. Ejecuta: filtros --help", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Ejecutando {nb_path} …")
    result = subprocess.run(
        ["jupyter", "nbconvert", "--to", "notebook", "--execute",
         "--inplace", str(nb_path)],
        capture_output=False,
    )
    if result.returncode != 0:
        typer.echo("Error durante la ejecución. Revisa la salida anterior.", err=True)
        raise typer.Exit(code=result.returncode)
    typer.echo("✓ Notebook ejecutado correctamente.")


@app.command()
def plot(
    modulo: Annotated[str, typer.Option("--modulo", "-m", help="ID del módulo")],
    scenario: Annotated[
        str,
        typer.Option("--scenario", "-s", help="Escenario del dataset (S1, S2, S3)"),
    ] = "S1",
    output: Annotated[
        Optional[Path],
        typer.Option("--output", "-o", help="Ruta de salida HTML (default: stdout)"),
    ] = None,
) -> None:
    """Genera figura Plotly del dataset y estimación del módulo."""
    import numpy as np

    from src.utils.dataset import generar_dataset
    from src.utils.visualizacion import plot_estimacion

    modulo_path = _resolver_modulo(modulo)
    typer.echo(f"Generando gráfica para módulo {modulo}, escenario {scenario} …")

    estados, _ = generar_dataset(scenario, T=200, seed=42)
    fig = plot_estimacion(
        estados_reales=estados,
        estimados=estados + np.random.default_rng(0).normal(0, 0.1, estados.shape),
        titulo=f"Módulo {modulo} — Escenario {scenario}",
    )

    out_path = output or Path(f"modulo_{modulo}_{scenario}.html")
    fig.write_html(str(out_path))
    typer.echo(f"✓ Figura guardada en {out_path}")


@app.command()
def export(
    modulo: Annotated[str, typer.Option("--modulo", "-m", help="ID del módulo o 'all'")],
    formato: Annotated[
        str,
        typer.Option("--formato", "-f", help="Formato de exportación: html, pdf"),
    ] = "html",
) -> None:
    """Exporta notebooks del módulo con nbconvert (html o pdf)."""
    import subprocess

    _DOCS_DIR.mkdir(parents=True, exist_ok=True)

    modulos = list(_MODULO_MAP.keys()) if modulo.lower() == "all" else [modulo]

    for mod in modulos:
        modulo_path = _resolver_modulo(mod)
        notebooks = sorted(modulo_path.glob("*.ipynb"))
        if not notebooks:
            typer.echo(f"Sin notebooks en {modulo_path} — saltando.")
            continue
        for nb in notebooks:
            typer.echo(f"Exportando {nb.name} …")
            result = subprocess.run(
                ["jupyter", "nbconvert", "--to", formato,
                 "--output-dir", str(_DOCS_DIR), str(nb)],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                typer.echo(f"Error exportando {nb.name}: {result.stderr}", err=True)
            else:
                typer.echo(f"  ✓ {nb.stem}.{formato}")

    typer.echo("Exportación completa.")


if __name__ == "__main__":
    app()
