from __future__ import annotations

from ..transversal.gestion_excepciones import ErrorValidacion
from .tecnica import Tecnica


class RegistroDeTecnicas:
    """Núcleo del microkernel: conoce los plug-ins y entrega el de cada experimento."""

    def __init__(self) -> None:
        self._tecnicas: dict[str, Tecnica] = {}

    def registrar(self, tecnica: Tecnica) -> None:
        self._tecnicas[tecnica.tipo] = tecnica

    def tecnica(self, tipo: str) -> Tecnica:
        try:
            return self._tecnicas[tipo]
        except KeyError:
            raise ErrorValidacion([f"El tipo de experimento '{tipo}' no está disponible."]) from None

    def disponibles(self) -> list[Tecnica]:
        return list(self._tecnicas.values())
