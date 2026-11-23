"""Capa de servicios: intermediaria, sin reglas de negocio ni de ninguna técnica."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4

from ..dominio.entidades import Experimento
from ..dominio.gestor_registro import EstadoPreparacion, GestorDeRegistro
from ..dominio.registro_tecnicas import RegistroDeTecnicas
from ..dominio.solicitud import DatosRegistro, SolicitudRegistro
from ..transversal.gestion_excepciones import SolicitudNoPendiente


@dataclass(frozen=True)
class Resultado:
    """Lo que el Ejecutor devuelve a la presentación.

    Registrado: trae el experimento. No registrado: espera confirmación y trae las coincidencias y el id pendiente.
    """

    registrado: bool
    experimento: Optional[Experimento] = None
    coincidencias: list[Experimento] = field(default_factory=list)
    pendiente_id: Optional[str] = None


class EjecutorDeRegistro:
    """Coordina el proceso: obtiene la técnica, crea la solicitud y decide qué operación del gestor sigue.

    Conserva en memoria, hasta que se confirma o cancela, la solicitud ya validada de los registros con coincidencias.
    """

    def __init__(self, registro_tecnicas: RegistroDeTecnicas, gestor: GestorDeRegistro):
        self._tecnicas = registro_tecnicas
        self._gestor = gestor
        self._pendientes: dict[str, SolicitudRegistro] = {}

    def registrar(self, datos: DatosRegistro, autor: str) -> Resultado:
        tecnica = self._tecnicas.tecnica(datos.tipo)
        solicitud = SolicitudRegistro(datos=datos, autor=autor, tecnica=tecnica)
        preparacion = self._gestor.preparar(solicitud)
        if preparacion.estado is EstadoPreparacion.REQUIERE_CONFIRMACION:
            pendiente_id = uuid4().hex
            self._pendientes[pendiente_id] = solicitud
            return Resultado(registrado=False, coincidencias=preparacion.coincidencias, pendiente_id=pendiente_id)
        return self._completar(solicitud)

    def confirmar(self, pendiente_id: str) -> Resultado:
        """Continúa con la solicitud pendiente sin repetir la validación ni la búsqueda."""
        solicitud = self._pendientes.pop(pendiente_id, None)
        if solicitud is None:
            raise SolicitudNoPendiente()
        return self._completar(solicitud)

    def cancelar(self, pendiente_id: str) -> None:
        self._pendientes.pop(pendiente_id, None)

    def _completar(self, solicitud: SolicitudRegistro) -> Resultado:
        experimento = self._gestor.guardar_experimento(solicitud)
        self._gestor.vincular_documento(experimento, solicitud.tecnica)
        return Resultado(registrado=True, experimento=experimento)
