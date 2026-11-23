from __future__ import annotations

import copy

from ..dominio.entidades import Experimento
from ..dominio.puertos import RepositorioExperimentos


class RepositorioExperimentosEnMemoria(RepositorioExperimentos):
    """Persistencia en memoria (opción elegida para este TP). Se reemplaza por PostgreSQL sin tocar el dominio."""

    def __init__(self, proyectos: dict[str, str] | None = None):
        self._proyectos = dict(proyectos or {})
        self._experimentos: dict[str, Experimento] = {}
        self._secuencia = 100

    def proyectos(self) -> list[tuple[str, str]]:
        return list(self._proyectos.items())

    def todos(self) -> list[Experimento]:
        return [copy.deepcopy(e) for e in self._experimentos.values()]

    def existe_proyecto(self, proyecto_id: str) -> bool:
        return proyecto_id in self._proyectos

    def existe_experimento(self, experimento_id: str) -> bool:
        return experimento_id in self._experimentos

    def con_parametros(self, tipo: str, clave: dict[str, str]) -> list[Experimento]:
        """Candidatos: los experimentos que dicen coincidir con la clave. La regla la tiene Experimento; acá solo se recorre."""
        return [copy.deepcopy(e) for e in self._experimentos.values() if e.coincide_con(tipo, clave)]

    def guardar(self, experimento: Experimento) -> str:
        self._secuencia += 1
        experimento_id = str(self._secuencia)
        experimento.id = experimento_id
        self._experimentos[experimento_id] = copy.deepcopy(experimento)
        return experimento_id

    def actualizar_rutas(self, experimento: Experimento) -> None:
        guardado = self._experimentos[experimento.id]
        guardado.ruta_pdb = experimento.ruta_pdb
        guardado.rutas_capturas = list(experimento.rutas_capturas)
        guardado.documento_notas = experimento.documento_notas

    def eliminar(self, experimento_id: str) -> None:
        self._experimentos.pop(experimento_id, None)
