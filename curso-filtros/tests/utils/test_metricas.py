"""Tests para src/utils/metricas.py."""

import numpy as np
import pytest

from src.utils.metricas import ess, nees, rmse


# --- rmse ---

def test_rmse_cero_cuando_iguales() -> None:
    x = np.array([1.0, 2.0, 3.0])
    assert rmse(x, x) == pytest.approx(0.0)


def test_rmse_conocido() -> None:
    estimados = np.array([0.0, 0.0])
    reales = np.array([1.0, 1.0])
    assert rmse(estimados, reales) == pytest.approx(1.0)


def test_rmse_multidimensional() -> None:
    est = np.zeros((10, 2))
    real = np.ones((10, 2))
    assert rmse(est, real) == pytest.approx(1.0)


def test_rmse_retorna_float() -> None:
    result = rmse(np.array([1.0]), np.array([2.0]))
    assert isinstance(result, float)


# --- nees ---

def test_nees_consistente_aprox_n() -> None:
    n = 2
    T = 1000
    rng = np.random.default_rng(42)
    P = np.eye(n)
    estimados = np.zeros((T, n))
    reales = rng.multivariate_normal(np.zeros(n), P, size=T)
    covs = np.tile(P, (T, 1, 1))
    valor = nees(estimados, reales, covs)
    # NEES consistente ≈ n con tolerancia estadística
    assert abs(valor - n) < 0.5, f"NEES={valor:.3f} lejano de n={n}"


def test_nees_retorna_float() -> None:
    est = np.zeros((5, 2))
    real = np.ones((5, 2))
    covs = np.tile(np.eye(2), (5, 1, 1))
    result = nees(est, real, covs)
    assert isinstance(result, float)


# --- ess ---

def test_ess_pesos_uniformes_igual_n() -> None:
    N = 100
    w = np.ones(N) / N
    assert ess(w) == pytest.approx(float(N))


def test_ess_degenerado_igual_uno() -> None:
    N = 50
    w = np.zeros(N)
    w[0] = 1.0
    assert ess(w) == pytest.approx(1.0)


def test_ess_en_rango_0_n() -> None:
    N = 200
    rng = np.random.default_rng(0)
    w_raw = rng.exponential(1.0, size=N)
    w = w_raw / w_raw.sum()
    val = ess(w)
    assert 0.0 < val <= float(N)


def test_ess_retorna_float() -> None:
    w = np.array([0.5, 0.5])
    result = ess(w)
    assert isinstance(result, float)
