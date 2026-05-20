"""Tests para src/utils/dataset.py."""

import numpy as np
import pytest

from src.utils.dataset import generar_dataset


def test_s1_shapes() -> None:
    estados, obs = generar_dataset("S1", T=200, seed=42)
    assert estados.shape == (200, 2)
    assert obs.shape == (200, 1)


def test_s2_shapes() -> None:
    estados, obs = generar_dataset("S2", T=200, seed=42)
    assert estados.shape == (200, 2)
    assert obs.shape == (200, 1)


def test_s3_shapes() -> None:
    estados, obs = generar_dataset("S3", T=200, seed=42)
    assert estados.shape == (200, 2)
    assert obs.shape == (200, 1)


def test_reproducibilidad_mismo_seed() -> None:
    e1, o1 = generar_dataset("S1", T=50, seed=7)
    e2, o2 = generar_dataset("S1", T=50, seed=7)
    np.testing.assert_array_equal(e1, e2)
    np.testing.assert_array_equal(o1, o2)


def test_seed_distinto_produce_datos_distintos() -> None:
    e1, _ = generar_dataset("S1", T=50, seed=1)
    e2, _ = generar_dataset("S1", T=50, seed=2)
    assert not np.allclose(e1, e2)


def test_estado_inicial_s1() -> None:
    estados, _ = generar_dataset("S1", T=1, seed=42)
    # El primer estado debe ser cercano a [0, 1] + ruido de proceso
    assert estados.shape == (1, 2)


def test_s2_observaciones_positivas() -> None:
    # S2 observa rango (sqrt ≥ 0); con ruido puede ser negativo, pero sin ruido siempre > 0
    _, obs = generar_dataset("S2", T=200, seed=42)
    # Rango = sqrt(x^2 + 1) ≥ 1, con R=0.5 casi nunca negativo
    assert obs.dtype == np.float64


def test_dtype_float64() -> None:
    for esc in ("S1", "S2", "S3"):
        e, o = generar_dataset(esc, T=10, seed=42)
        assert e.dtype == np.float64
        assert o.dtype == np.float64


@pytest.mark.parametrize("escenario", ["S1", "S2", "S3"])
def test_tres_escenarios_no_identicos(escenario: str) -> None:
    e, _ = generar_dataset(escenario, T=200, seed=42)
    assert np.all(np.isfinite(e)), f"NaN/inf en escenario {escenario}"
