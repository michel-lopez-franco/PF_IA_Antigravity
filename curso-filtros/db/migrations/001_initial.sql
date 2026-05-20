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
