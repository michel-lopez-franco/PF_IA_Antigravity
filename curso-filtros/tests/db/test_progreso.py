"""Tests de integración para src/db/progreso.py — usa SQLite en memoria."""

from pathlib import Path

import pytest

from src.db.progreso import ProgresoEstudiante


@pytest.fixture
def progreso(tmp_path: Path) -> ProgresoEstudiante:
    """ProgresoEstudiante apuntando a base de datos temporal."""
    return ProgresoEstudiante(db_path=tmp_path / "test.db")


def test_marcar_completado_nuevo(progreso: ProgresoEstudiante) -> None:
    progreso.marcar_completado("modulo_01", "01_teoria.ipynb")
    rows = progreso.listar_progreso()
    assert len(rows) == 1
    assert rows[0]["completado"] == 1


def test_marcar_completado_con_rmse(progreso: ProgresoEstudiante) -> None:
    progreso.marcar_completado("modulo_02", "02_practica.ipynb", rmse_ultimo=0.034)
    rmse = progreso.consultar_rmse("modulo_02", "02_practica.ipynb")
    assert rmse == pytest.approx(0.034)


def test_consultar_rmse_no_existe_devuelve_none(progreso: ProgresoEstudiante) -> None:
    result = progreso.consultar_rmse("modulo_99", "no_existe.ipynb")
    assert result is None


def test_actualizar_registro_existente(progreso: ProgresoEstudiante) -> None:
    progreso.marcar_completado("modulo_01", "02_practica.ipynb", rmse_ultimo=0.1)
    progreso.marcar_completado("modulo_01", "02_practica.ipynb", rmse_ultimo=0.05)
    rows = progreso.listar_progreso()
    assert len(rows) == 1
    assert progreso.consultar_rmse("modulo_01", "02_practica.ipynb") == pytest.approx(0.05)


def test_listar_progreso_vacio(progreso: ProgresoEstudiante) -> None:
    assert progreso.listar_progreso() == []


def test_listar_multiples_modulos(progreso: ProgresoEstudiante) -> None:
    progreso.marcar_completado("modulo_01", "01_teoria.ipynb")
    progreso.marcar_completado("modulo_01", "02_practica.ipynb")
    progreso.marcar_completado("modulo_02", "01_teoria.ipynb")
    rows = progreso.listar_progreso()
    assert len(rows) == 3


def test_registrar_metrica(progreso: ProgresoEstudiante) -> None:
    progreso.registrar_metrica(
        modulo_id="modulo_03",
        filtro="KalmanLineal",
        escenario="S1",
        rmse=0.023,
        varianza=0.005,
        tiempo_s=0.12,
    )
    # Verificar que no lanza error y la tabla acepta la inserción
    rows = progreso.listar_progreso()
    assert len(rows) == 0  # progreso vacío, metrica_run tiene el dato
