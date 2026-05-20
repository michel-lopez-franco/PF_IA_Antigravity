"""Tests para src/filtros/kalman_lineal.py."""

import numpy as np
import pytest

from src.filtros.kalman_lineal import KalmanLineal


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _make_1d_filtro(q: float = 0.1, r: float = 1.0) -> KalmanLineal:
    """Filtro 1D: posición escalar, observación directa."""
    F = np.array([[1.0]])
    H = np.array([[1.0]])
    Q = np.array([[q]])
    R = np.array([[r]])
    return KalmanLineal(F, H, Q, R, x0=np.array([0.0]), P0=np.array([[1.0]]))


def _make_pos_vel_filtro(dt: float = 1.0, q: float = 0.1, r: float = 1.0) -> KalmanLineal:
    """Filtro 2D: [posicion, velocidad], observación de posición."""
    F = np.array([[1.0, dt], [0.0, 1.0]])
    H = np.array([[1.0, 0.0]])
    Q = np.array([[q, 0.0], [0.0, q]])
    R = np.array([[r]])
    return KalmanLineal(
        F, H, Q, R,
        x0=np.array([0.0, 1.0]),
        P0=np.eye(2, dtype=np.float64),
    )


# ──────────────────────────────────────────────────────────────────────────────
# Tests de inicialización
# ──────────────────────────────────────────────────────────────────────────────

def test_estado_inicial_shape() -> None:
    kf = _make_pos_vel_filtro()
    assert kf.estado.shape == (2,)


def test_covarianza_inicial_shape() -> None:
    kf = _make_pos_vel_filtro()
    assert kf.covarianza.shape == (2, 2)


def test_dimension_F_incorrecta_lanza_error() -> None:
    F_mala = np.ones((3, 2), dtype=np.float64)  # F no cuadrada
    H = np.array([[1.0, 0.0]])
    Q = np.eye(2, dtype=np.float64)
    R = np.array([[1.0]])
    with pytest.raises(ValueError, match="F"):
        KalmanLineal(F_mala, H, Q, R)


# ──────────────────────────────────────────────────────────────────────────────
# Tests de predict
# ──────────────────────────────────────────────────────────────────────────────

def test_predecir_con_identidad_propaga_estado() -> None:
    kf = _make_1d_filtro()
    kf._x = np.array([5.0])
    kf.predecir()
    assert kf.estado[0] == pytest.approx(5.0, abs=1e-10)


def test_predecir_incrementa_traza_covarianza() -> None:
    """La traza (incertidumbre total) debe crecer tras predicción con Q > 0."""
    kf = _make_pos_vel_filtro()
    traza_antes = float(np.trace(kf.covarianza))
    kf.predecir()
    traza_despues = float(np.trace(kf.covarianza))
    assert traza_despues > traza_antes, f"Traza no creció: {traza_antes:.4f} → {traza_despues:.4f}"


def test_predecir_preserva_simetria_P() -> None:
    kf = _make_pos_vel_filtro()
    for _ in range(10):
        kf.predecir()
    P = kf.covarianza
    assert np.allclose(P, P.T, atol=1e-12)


# ──────────────────────────────────────────────────────────────────────────────
# Tests de update
# ──────────────────────────────────────────────────────────────────────────────

def test_actualizar_reduce_covarianza() -> None:
    kf = _make_1d_filtro()
    kf.predecir()
    P_antes = kf.covarianza.copy()
    kf.actualizar(np.array([2.0]))
    P_despues = kf.covarianza
    assert P_despues[0, 0] < P_antes[0, 0], "P debería disminuir tras update"


def test_actualizar_mueve_estado_hacia_observacion() -> None:
    kf = _make_1d_filtro()
    kf._x = np.array([0.0])
    kf._P = np.array([[10.0]])  # alta incertidumbre: K ≈ 1
    kf.predecir()
    kf.actualizar(np.array([5.0]))
    assert kf.estado[0] > 3.0, "Con alta incertidumbre, estado debe acercarse bastante a z=5"


def test_actualizar_preserva_simetria_P() -> None:
    kf = _make_pos_vel_filtro()
    for _ in range(20):
        kf.predecir()
        kf.actualizar(np.array([float(np.random.default_rng(42).normal(5, 1))]))
    P = kf.covarianza
    assert np.allclose(P, P.T, atol=1e-10)


def test_P_positiva_definida_tras_ciclo() -> None:
    rng = np.random.default_rng(42)
    kf = _make_pos_vel_filtro()
    for k in range(50):
        kf.predecir()
        z = np.array([k * 1.0 + rng.normal(0, 1)])
        kf.actualizar(z)
        eigvals = np.linalg.eigvalsh(kf.covarianza)
        assert np.all(eigvals > 0), f"P no es positiva definida en paso k={k}"


# ──────────────────────────────────────────────────────────────────────────────
# Tests de ganancia de Kalman en casos límite
# ──────────────────────────────────────────────────────────────────────────────

def test_ganancia_R_tendencia_cero_tiende_H_inv() -> None:
    """Con R→0 (sensor perfecto), K debería → H^{-1} (para H cuadrada)."""
    R_small = 1e-10
    kf = _make_1d_filtro(q=0.1, r=R_small)
    kf.predecir()

    # Calcular K manualmente
    P = kf.covarianza
    H = kf._H
    R = kf._R
    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)

    # Con R→0, K ≈ P H^T (H P H^T)^{-1} → H^{-1} cuando H es cuadrada
    H_inv = np.linalg.inv(H)  # type: ignore[arg-type]
    assert abs(float(K[0, 0]) - float(H_inv[0, 0])) < 0.01, f"K={K[0,0]:.6f} ≠ H^-1={H_inv[0,0]:.6f}"


def test_ganancia_R_grande_tiende_cero() -> None:
    """Con R→∞ (sensor muy ruidoso), K → 0 (ignora la observación)."""
    R_large = 1e8
    kf = _make_1d_filtro(q=0.1, r=R_large)
    kf.predecir()

    P = kf.covarianza
    H = kf._H
    R = kf._R
    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)

    assert abs(float(K[0, 0])) < 1e-6, f"K={K[0,0]:.2e} debería ≈ 0 con R grande"


# ──────────────────────────────────────────────────────────────────────────────
# Test de equivalencia con dataset S1 (vs. filterpy)
# ──────────────────────────────────────────────────────────────────────────────

def test_residuo_vs_filterpy_s1() -> None:
    """Residuo entre KalmanLineal y filterpy.KalmanFilter sobre S1 < 1e-8."""
    try:
        from filterpy.kalman import KalmanFilter as FPKalman
    except ImportError:
        pytest.skip("filterpy no disponible")

    from src.utils.dataset import generar_dataset

    estados, obs = generar_dataset("S1", T=100, seed=42)
    dt = 1.0
    q, r = 0.1, 1.0

    # Nuestro filtro
    F = np.array([[1.0, dt], [0.0, 1.0]])
    H = np.array([[1.0, 0.0]])
    Q = np.eye(2) * q
    R_mat = np.array([[r]])
    kf_nuestro = KalmanLineal(F, H, Q, R_mat, x0=np.array([0.0, 1.0]))

    # filterpy
    kf_fp = FPKalman(dim_x=2, dim_z=1)
    kf_fp.F = F.copy()
    kf_fp.H = H.copy()
    kf_fp.Q = Q.copy()
    kf_fp.R = R_mat.copy()
    kf_fp.x = np.array([[0.0], [1.0]])
    kf_fp.P = np.eye(2, dtype=np.float64)

    estimados_nuestros = np.zeros(100)
    estimados_fp = np.zeros(100)

    for k in range(100):
        kf_nuestro.predecir()
        kf_nuestro.actualizar(obs[k])
        estimados_nuestros[k] = kf_nuestro.estado[0]

        kf_fp.predict()
        kf_fp.update(obs[k : k + 1])
        estimados_fp[k] = float(kf_fp.x[0, 0])

    max_residuo = float(np.max(np.abs(estimados_nuestros - estimados_fp)))
    assert max_residuo < 1e-8, f"Residuo máximo {max_residuo:.2e} ≥ 1e-8"
