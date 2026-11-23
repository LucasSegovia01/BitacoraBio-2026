"""Apoyo de la interfaz: consultas de solo lectura sobre lo guardado (no es parte de HU-01.A1).

Alimenta las pantallas de proyectos, experimentos, detalle y búsqueda. Solo lee a través del puerto
`RepositorioExperimentos`; no escribe nada ni decide reglas de negocio.
"""
from __future__ import annotations

from typing import Optional

from ..dominio.entidades import Experimento, normalizar
from ..dominio.puertos import AlmacenamientoArchivos, RepositorioExperimentos


class ServicioConsulta:
    def __init__(self, repositorio: RepositorioExperimentos, archivos: Optional[AlmacenamientoArchivos] = None):
        self._repo = repositorio
        self._archivos = archivos

    def proyectos(self) -> list[tuple[str, str]]:
        return self._repo.proyectos()

    def experimentos(self) -> list[Experimento]:
        return self._repo.todos()

    def nombre_de_proyecto(self, proyecto_id: str) -> str:
        return dict(self._repo.proyectos()).get(proyecto_id, proyecto_id)

    def resumen_de_proyectos(self) -> list[dict]:
        """Por proyecto: cantidad de experimentos y fecha de la última carga."""
        todos = self._repo.todos()
        resumen = []
        for pid, nombre in self._repo.proyectos():
            propios = [e for e in todos if e.proyecto_id == pid]
            resumen.append({
                "id": pid, "nombre": nombre, "cantidad": len(propios),
                "ultima": max((e.fecha_de_carga for e in propios), default=None),
            })
        return resumen

    def proyecto(self, proyecto_id: str) -> Optional[dict]:
        return next((p for p in self.resumen_de_proyectos() if p["id"] == proyecto_id), None)

    def experimentos_de(self, proyecto_id: str) -> list[Experimento]:
        return self._ordenados([e for e in self._repo.todos() if e.proyecto_id == proyecto_id])

    def experimento(self, experimento_id: str) -> Optional[Experimento]:
        return next((e for e in self._repo.todos() if e.id == experimento_id), None)

    def contenido_pdb(self, experimento: Experimento) -> Optional[str]:
        """Texto del PDB del experimento para el visor, o None si no tiene o ya no está guardado."""
        if not experimento.ruta_pdb or self._archivos is None:
            return None
        contenido = self._archivos.leer(experimento.ruta_pdb)
        return contenido.decode("utf-8", errors="replace") if contenido is not None else None

    def de_autor(self, autor: str, estado: str = "") -> list[Experimento]:
        return self.buscar(autor=autor, estado=estado)

    def autores(self) -> list[str]:
        return sorted({e.autor for e in self._repo.todos()})

    def buscar(self, texto: str = "", proyecto: str = "", autor: str = "", estado: str = "") -> list[Experimento]:
        """Filtra por texto (en los valores de los parámetros), proyecto, autor y estado de validez."""
        buscado = normalizar(texto)
        encontrados = []
        for e in self._repo.todos():
            if proyecto and e.proyecto_id != proyecto:
                continue
            if autor and e.autor != autor:
                continue
            if estado and e.estado_validez != estado:
                continue
            if buscado and not any(buscado in normalizar(p.valor) for p in e.parametros):
                continue
            encontrados.append(e)
        return self._ordenados(encontrados)

    @staticmethod
    def _ordenados(experimentos: list[Experimento]) -> list[Experimento]:
        return sorted(experimentos, key=lambda e: e.fecha_de_carga, reverse=True)
