from __future__ import annotations

from .entidades import Experimento
from .puertos import RepositorioExperimentos
from .solicitud import SolicitudRegistro


class DetectorDeDuplicados:
    """Busca los experimentos que coinciden con el que se quiere registrar (RF-03, CU-00).

    Pide la clave de comparación a la técnica, consulta los candidatos al repositorio y aplica los criterios
    del negocio. Solo devuelve las coincidencias: no escribe nada, no las muestra y no decide si el registro sigue.
    """

    def __init__(self, repositorio: RepositorioExperimentos):
        self._repo = repositorio

    def buscar(self, solicitud: SolicitudRegistro) -> list[Experimento]:
        clave = solicitud.tecnica.clave_de_coincidencia(solicitud.parametros())
        candidatos = self._repo.con_parametros(solicitud.datos.tipo, clave)
        validos = [e for e in candidatos if e.es_candidato_a_duplicado()]  # los inválidos no cuentan (regla del experimento)
        # Tampoco cuentan las réplicas de otro candidato (ya lo representa el original) ni los que el usuario declaró en "Similar a".
        return [e for e in validos if not e.es_replica_de_alguno(validos) and not solicitud.declara_similar(e)]
