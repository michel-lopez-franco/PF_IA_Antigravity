"""Persistencia local de progreso del estudiante en SQLite."""

import sqlite3
from pathlib import Path
from typing import Optional

_DB_PATH = Path(__file__).parent.parent.parent / "filtros.db"
_MIGRATION = Path(__file__).parent.parent.parent / "db" / "migrations" / "001_initial.sql"


def _connect(db_path: Path = _DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    _aplicar_migracion(conn)
    return conn


def _aplicar_migracion(conn: sqlite3.Connection) -> None:
    if _MIGRATION.exists():
        conn.executescript(_MIGRATION.read_text())
        conn.commit()


class ProgresoEstudiante:
    """CRUD de progreso del estudiante sobre SQLite local."""

    def __init__(self, db_path: Path = _DB_PATH) -> None:
        self._db_path = db_path

    def marcar_completado(
        self,
        modulo_id: str,
        notebook: str,
        rmse_ultimo: Optional[float] = None,
    ) -> None:
        """Marca un notebook como completado, actualizando rmse si se provee."""
        with _connect(self._db_path) as conn:
            conn.execute(
                """INSERT INTO progreso (modulo_id, notebook, completado, rmse_ultimo)
                   VALUES (?, ?, 1, ?)
                   ON CONFLICT(modulo_id, notebook)
                   DO UPDATE SET completado=1, rmse_ultimo=excluded.rmse_ultimo,
                                 ts_ultimo=datetime('now')""",
                (modulo_id, notebook, rmse_ultimo),
            )

    def consultar_rmse(self, modulo_id: str, notebook: str) -> Optional[float]:
        """Devuelve el último RMSE registrado o None si no existe."""
        with _connect(self._db_path) as conn:
            row = conn.execute(
                "SELECT rmse_ultimo FROM progreso WHERE modulo_id=? AND notebook=?",
                (modulo_id, notebook),
            ).fetchone()
        return float(row["rmse_ultimo"]) if row and row["rmse_ultimo"] is not None else None

    def listar_progreso(self) -> list[dict[str, object]]:
        """Devuelve lista de todos los registros de progreso."""
        with _connect(self._db_path) as conn:
            rows = conn.execute(
                "SELECT modulo_id, notebook, completado, rmse_ultimo, ts_ultimo "
                "FROM progreso ORDER BY modulo_id, notebook"
            ).fetchall()
        return [dict(r) for r in rows]

    def registrar_metrica(
        self,
        modulo_id: str,
        filtro: str,
        escenario: str,
        rmse: Optional[float] = None,
        varianza: Optional[float] = None,
        tiempo_s: Optional[float] = None,
    ) -> None:
        """Registra una métrica de ejecución de filtro."""
        with _connect(self._db_path) as conn:
            conn.execute(
                "INSERT INTO metrica_run (modulo_id, filtro, escenario, rmse, varianza, tiempo_s) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (modulo_id, filtro, escenario, rmse, varianza, tiempo_s),
            )
