"""Persistencia en SQLite (módulo estándar `sqlite3`, sin dependencias nuevas).

Implementa el mismo puerto que el repositorio en memoria: el dominio, el ejecutor y la presentación no cambian.
Modelo del TP3 (DA-03 y DA-05): una fila por experimento y una fila por parámetro (nombre, valor, unidad),
con un índice sobre (nombre, valor) para buscar coincidencias sin recorrer todo.
"""
from __future__ import annotations

import json
import sqlite3
import threading
from datetime import date, datetime

from ..dominio.entidades import Experimento, ParametroExperimento, normalizar
from ..dominio.puertos import RepositorioExperimentos

_ESQUEMA = """
CREATE TABLE IF NOT EXISTS proyecto (
    id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS experimento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proyecto_id TEXT NOT NULL REFERENCES proyecto(id),
    tipo TEXT NOT NULL,
    autor TEXT NOT NULL,
    fecha_de_carga TEXT NOT NULL,
    fecha_realizacion TEXT NOT NULL,
    hardware TEXT NOT NULL DEFAULT '',
    tiempo_procesamiento TEXT NOT NULL DEFAULT '',
    objetivo TEXT NOT NULL DEFAULT '',
    hipotesis TEXT NOT NULL DEFAULT '',
    notas TEXT NOT NULL DEFAULT '',
    estado_validez TEXT NOT NULL,
    estado_analisis TEXT NOT NULL,
    ruta_pdb TEXT,
    rutas_capturas TEXT NOT NULL DEFAULT '[]',
    documento_notas TEXT
);
CREATE TABLE IF NOT EXISTS parametro_experimento (
    experimento_id INTEGER NOT NULL REFERENCES experimento(id) ON DELETE CASCADE,
    orden INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    valor TEXT NOT NULL,
    valor_normalizado TEXT NOT NULL,
    unidad TEXT
);
CREATE INDEX IF NOT EXISTS idx_parametro_nombre_valor ON parametro_experimento (nombre, valor_normalizado);
CREATE INDEX IF NOT EXISTS idx_parametro_experimento ON parametro_experimento (experimento_id);
CREATE TABLE IF NOT EXISTS similar_a (
    experimento_id INTEGER NOT NULL REFERENCES experimento(id) ON DELETE CASCADE,
    similar_id TEXT NOT NULL
);
"""

# Los ids siguen la numeración del repositorio en memoria: el primero es el 101.
_PRIMER_ID = 100


class RepositorioExperimentosSQLite(RepositorioExperimentos):
    """`ruta` es el archivo de la base (se crea si no existe) o ":memory:" para una base descartable."""

    def __init__(self, ruta: str = ":memory:", proyectos: dict[str, str] | None = None):
        self._conn = sqlite3.connect(ruta, check_same_thread=False)  # Flask atiende cada pedido en un hilo
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._cerrojo = threading.Lock()
        with self._cerrojo, self._conn:
            self._conn.executescript(_ESQUEMA)
            self._conn.execute(
                "INSERT INTO sqlite_sequence (name, seq) SELECT 'experimento', ? "
                "WHERE NOT EXISTS (SELECT 1 FROM sqlite_sequence WHERE name = 'experimento')",
                (_PRIMER_ID,),
            )
            self._conn.executemany("INSERT OR IGNORE INTO proyecto (id, nombre) VALUES (?, ?)", list((proyectos or {}).items()))

    def cerrar(self) -> None:
        self._conn.close()

    # --- consultas ---------------------------------------------------------------------------------------------
    def proyectos(self) -> list[tuple[str, str]]:
        with self._cerrojo:
            return [(f[0], f[1]) for f in self._conn.execute("SELECT id, nombre FROM proyecto ORDER BY rowid")]

    def todos(self) -> list[Experimento]:
        with self._cerrojo:
            return self._cargar("SELECT * FROM experimento ORDER BY id", ())

    def existe_proyecto(self, proyecto_id: str) -> bool:
        with self._cerrojo:
            return self._conn.execute("SELECT 1 FROM proyecto WHERE id = ?", (proyecto_id,)).fetchone() is not None

    def existe_experimento(self, experimento_id: str) -> bool:
        with self._cerrojo:
            return self._conn.execute("SELECT 1 FROM experimento WHERE id = ?", (experimento_id,)).fetchone() is not None

    def con_parametros(self, tipo: str, clave: dict[str, str]) -> list[Experimento]:
        """La base descarta rápido con el índice (nombre, valor); la regla final la confirma `Experimento.coincide_con`."""
        consulta = "SELECT * FROM experimento WHERE tipo = ?"
        argumentos: list[str] = [tipo]
        for nombre, valor in clave.items():
            consulta += (
                " AND EXISTS (SELECT 1 FROM parametro_experimento p"
                " WHERE p.experimento_id = experimento.id AND p.nombre = ? AND p.valor_normalizado = ?)"
            )
            argumentos += [nombre, normalizar(valor)]
        with self._cerrojo:
            candidatos = self._cargar(consulta + " ORDER BY id", tuple(argumentos))
        return [e for e in candidatos if e.coincide_con(tipo, clave)]

    # --- escrituras --------------------------------------------------------------------------------------------
    def guardar(self, experimento: Experimento) -> str:
        with self._cerrojo, self._conn:
            cursor = self._conn.execute(
                "INSERT INTO experimento (proyecto_id, tipo, autor, fecha_de_carga, fecha_realizacion, hardware,"
                " tiempo_procesamiento, objetivo, hipotesis, notas, estado_validez, estado_analisis, ruta_pdb,"
                " rutas_capturas, documento_notas) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (experimento.proyecto_id, experimento.tipo, experimento.autor,
                 experimento.fecha_de_carga.isoformat(), experimento.fecha_realizacion.isoformat(),
                 experimento.hardware, experimento.tiempo_procesamiento, experimento.objetivo, experimento.hipotesis,
                 experimento.notas, experimento.estado_validez, experimento.estado_analisis, experimento.ruta_pdb,
                 json.dumps(experimento.rutas_capturas), experimento.documento_notas),
            )
            nuevo_id = cursor.lastrowid
            self._conn.executemany(
                "INSERT INTO parametro_experimento (experimento_id, orden, nombre, valor, valor_normalizado, unidad)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                [(nuevo_id, i, p.nombre, p.valor, normalizar(p.valor), p.unidad) for i, p in enumerate(experimento.parametros)],
            )
            self._conn.executemany(
                "INSERT INTO similar_a (experimento_id, similar_id) VALUES (?, ?)",
                [(nuevo_id, otro) for otro in experimento.similar_a],
            )
        experimento.id = str(nuevo_id)
        return experimento.id

    def actualizar_rutas(self, experimento: Experimento) -> None:
        with self._cerrojo, self._conn:
            self._conn.execute(
                "UPDATE experimento SET ruta_pdb = ?, rutas_capturas = ?, documento_notas = ? WHERE id = ?",
                (experimento.ruta_pdb, json.dumps(experimento.rutas_capturas), experimento.documento_notas, experimento.id),
            )

    def eliminar(self, experimento_id: str) -> None:
        with self._cerrojo, self._conn:
            self._conn.execute("DELETE FROM experimento WHERE id = ?", (experimento_id,))  # borra también sus parámetros

    # --- apoyo -------------------------------------------------------------------------------------------------
    def _cargar(self, consulta: str, argumentos: tuple) -> list[Experimento]:
        return [self._armar(f) for f in self._conn.execute(consulta, argumentos).fetchall()]

    def _armar(self, fila: sqlite3.Row) -> Experimento:
        identificador = fila["id"]
        parametros = self._conn.execute(
            "SELECT nombre, valor, unidad FROM parametro_experimento WHERE experimento_id = ? ORDER BY orden", (identificador,)
        ).fetchall()
        similares = self._conn.execute("SELECT similar_id FROM similar_a WHERE experimento_id = ?", (identificador,)).fetchall()
        return Experimento(
            proyecto_id=fila["proyecto_id"],
            tipo=fila["tipo"],
            autor=fila["autor"],
            fecha_de_carga=datetime.fromisoformat(fila["fecha_de_carga"]),
            fecha_realizacion=date.fromisoformat(fila["fecha_realizacion"]),
            parametros=[ParametroExperimento(p[0], p[1], p[2]) for p in parametros],
            hardware=fila["hardware"],
            tiempo_procesamiento=fila["tiempo_procesamiento"],
            objetivo=fila["objetivo"],
            hipotesis=fila["hipotesis"],
            notas=fila["notas"],
            estado_validez=fila["estado_validez"],
            estado_analisis=fila["estado_analisis"],
            similar_a=[s[0] for s in similares],
            id=str(identificador),
            ruta_pdb=fila["ruta_pdb"],
            rutas_capturas=json.loads(fila["rutas_capturas"]),
            documento_notas=fila["documento_notas"],
        )
