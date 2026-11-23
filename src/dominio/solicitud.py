"""Datos y solicitud de registro: lo que viaja entre el Ejecutor y el Gestor de registro (TP3 5.2.2)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from .entidades import ParametroExperimento


@dataclass
class DatosRegistro:
    """Lo que el usuario completó en el formulario."""

    proyecto_id: str
    tipo: str
    fecha_realizacion: Optional[date]
    valores: dict[str, str] = field(default_factory=dict)  # parámetros que define la técnica
    extras: list[tuple[str, str, Optional[str]]] = field(default_factory=list)  # parámetros adicionales libres: (nombre, valor, unidad)
    hardware: str = ""
    tiempo_procesamiento: str = ""
    objetivo: str = ""
    hipotesis: str = ""
    notas: str = ""
    similar_a: list[str] = field(default_factory=list)
    estado_validez: str = "en_curso"
    pdb: Optional[bytes] = None
    capturas: list[tuple[str, bytes]] = field(default_factory=list)


@dataclass(frozen=True)
class SolicitudRegistro:
    """DTO inmutable con lo necesario para iniciar un registro. No guarda resultados: los devuelven las operaciones."""

    datos: DatosRegistro
    autor: str
    tecnica: "object"  # Tecnica elegida por el Ejecutor de registro

    def parametros(self) -> list[ParametroExperimento]:
        """Parámetros del experimento: los que define la técnica (con su unidad) y los extras."""
        lista: list[ParametroExperimento] = []
        for d in self.tecnica.definiciones():
            valor = self.datos.valores.get(d.nombre, "").strip()
            if valor:
                lista.append(ParametroExperimento(d.nombre, valor, d.unidad))
        lista.extend(ParametroExperimento(nombre, valor, unidad) for nombre, valor, unidad in self.datos.extras)
        return lista

    def declara_similar(self, experimento) -> bool:
        """El usuario indicó este experimento en "Similar a": no cuenta como coincidencia."""
        return experimento.id in self.datos.similar_a
