"""Tests para src/filtros/bayes_discreto.py."""

import numpy as np
import pytest

from src.filtros.bayes_discreto import BayesFiltroDiscreto


# ──────────────────────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────────────────────

def _make_filtro(n: int = 20, sigma: float = 1.0) -> BayesFiltroDiscreto:
    """Filtro con grilla [0..n-1], transición gaussiana, prior uniforme."""
    grilla = np.arange(n, dtype=np.float64)
    # Matriz de transición: movimiento aleatorio gaussiano de media 1 paso
    T = np.zeros((n, n), dtype=np.float64)
    for j in range(n):
        kernel = np.exp(-0.5 * (grilla - (grilla[j] + 1.0)) ** 2 / 1.0)
        T[:, j] = kernel / kernel.sum()
    return BayesFiltroDiscreto(grilla, T, sigma)


# ──────────────────────────────────────────────────────────────────────────────
# Tests de inicialización
# ──────────────────────────────────────────────────────────────────────────────

def test_prior_uniforme_suma_uno() -> None:
    filtro = _make_filtro()
    assert abs(filtro.belief.sum() - 1.0) < 1e-10


def test_prior_uniforme_distribucion_uniforme() -> None:
    n = 10
    filtro = _make_filtro(n=n)
    expected = 1.0 / n
    assert np.allclose(filtro.belief, expected, atol=1e-10)


def test_prior_personalizado_normalizado() -> None:
    n = 10
    grilla = np.arange(n, dtype=np.float64)
    T = np.eye(n, dtype=np.float64)
    prior = np.ones(n, dtype=np.float64) * 2.0  # no normalizado
    filtro = BayesFiltroDiscreto(grilla, T, sigma_sensor=1.0, prior=prior)
    assert abs(filtro.belief.sum() - 1.0) < 1e-10


def test_prior_todo_cero_lanza_error() -> None:
    n = 5
    grilla = np.arange(n, dtype=np.float64)
    T = np.eye(n, dtype=np.float64)
    prior_cero = np.zeros(n, dtype=np.float64)
    with pytest.raises(ValueError, match="cero"):
        BayesFiltroDiscreto(grilla, T, sigma_sensor=1.0, prior=prior_cero)


def test_dimension_T_incorrecta_lanza_error() -> None:
    n = 5
    grilla = np.arange(n, dtype=np.float64)
    T_mala = np.eye(n + 1, dtype=np.float64)
    with pytest.raises(ValueError, match="T_matrix"):
        BayesFiltroDiscreto(grilla, T_mala, sigma_sensor=1.0)


def test_sigma_cero_lanza_error() -> None:
    n = 5
    grilla = np.arange(n, dtype=np.float64)
    T = np.eye(n, dtype=np.float64)
    with pytest.raises(ValueError, match="sigma_sensor"):
        BayesFiltroDiscreto(grilla, T, sigma_sensor=0.0)


# ──────────────────────────────────────────────────────────────────────────────
# Tests de predict
# ──────────────────────────────────────────────────────────────────────────────

def test_predecir_conserva_normalizacion() -> None:
    filtro = _make_filtro()
    filtro.predecir()
    assert abs(filtro.belief.sum() - 1.0) < 1e-10


def test_predecir_con_identidad_no_cambia_belief() -> None:
    n = 5
    grilla = np.arange(n, dtype=np.float64)
    T_identity = np.eye(n, dtype=np.float64)
    prior = np.array([0.1, 0.2, 0.4, 0.2, 0.1], dtype=np.float64)
    filtro = BayesFiltroDiscreto(grilla, T_identity, sigma_sensor=1.0, prior=prior)
    filtro.predecir()
    assert np.allclose(filtro.belief, prior, atol=1e-12)


# ──────────────────────────────────────────────────────────────────────────────
# Tests de update
# ──────────────────────────────────────────────────────────────────────────────

def test_actualizar_concentra_belief() -> None:
    n = 20
    filtro = _make_filtro(n=n, sigma=0.5)
    # Observación exactamente en posición 10
    z = np.array([10.0], dtype=np.float64)
    filtro.actualizar(z)
    # La creencia debe estar mayoritariamente concentrada alrededor de la posición 10
    assert filtro.estado[0] == pytest.approx(10.0, abs=1.0)
    assert filtro.belief[10] > 0.4, "Creencia debería concentrarse en posición 10"


def test_actualizar_normaliza_posterior() -> None:
    filtro = _make_filtro()
    filtro.actualizar(np.array([5.0], dtype=np.float64))
    assert abs(filtro.belief.sum() - 1.0) < 1e-10


def test_actualizar_con_likelihood_imposible_lanza_error() -> None:
    n = 10
    grilla = np.arange(n, dtype=np.float64)  # posiciones 0..9
    T = np.eye(n, dtype=np.float64)
    prior = np.zeros(n, dtype=np.float64)
    prior[0] = 1.0  # creencia concentrada en posición 0
    filtro = BayesFiltroDiscreto(grilla, T, sigma_sensor=1e-10, prior=prior)
    # Observación muy lejos — likelihood efectivamente cero
    with pytest.raises(ValueError, match="colapsó"):
        filtro.actualizar(np.array([1000.0], dtype=np.float64))


# ──────────────────────────────────────────────────────────────────────────────
# Tests de propiedades estado y covarianza
# ──────────────────────────────────────────────────────────────────────────────

def test_estado_retorna_posicion_maxima() -> None:
    n = 10
    grilla = np.arange(n, dtype=np.float64)
    T = np.eye(n, dtype=np.float64)
    prior = np.zeros(n, dtype=np.float64)
    prior[7] = 1.0  # toda la masa en posición 7
    filtro = BayesFiltroDiscreto(grilla, T, sigma_sensor=1.0, prior=prior)
    assert filtro.estado[0] == pytest.approx(7.0, abs=1e-10)


def test_covarianza_uniforme_correcta() -> None:
    n = 5
    grilla = np.array([0.0, 1.0, 2.0, 3.0, 4.0], dtype=np.float64)
    T = np.eye(n, dtype=np.float64)
    filtro = BayesFiltroDiscreto(grilla, T, sigma_sensor=1.0)
    cov = filtro.covarianza
    assert cov.shape == (1, 1)
    # Varianza de distribución uniforme discreta {0,1,2,3,4}: E[X]=2, Var=2
    assert abs(float(cov[0, 0]) - 2.0) < 1e-10


def test_estado_shape() -> None:
    filtro = _make_filtro()
    assert filtro.estado.shape == (1,)


def test_covarianza_shape() -> None:
    filtro = _make_filtro()
    assert filtro.covarianza.shape == (1, 1)


# ──────────────────────────────────────────────────────────────────────────────
# Test ciclo completo (predict + update repetido)
# ──────────────────────────────────────────────────────────────────────────────

def test_ciclo_completo_convergencia() -> None:
    rng = np.random.default_rng(42)
    n = 20
    filtro = _make_filtro(n=n, sigma=1.5)

    # Simular 30 pasos con estado real en posición 10
    estado_real = 10.0
    errores = []
    for _ in range(30):
        filtro.predecir()
        obs = np.array([estado_real + rng.normal(0, 1.5)], dtype=np.float64)
        filtro.actualizar(obs)
        errores.append(abs(float(filtro.estado[0]) - estado_real))

    # Después de 30 pasos, el error MAP debe ser razonable
    error_final = float(np.mean(errores[-10:]))
    assert error_final < 3.0, f"Error final {error_final:.2f} demasiado alto"
