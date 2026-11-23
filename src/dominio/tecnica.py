"""Interfaz de técnica: lo propio de cada ensayo (TP3 5.2.2, DA-02)."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from .entidades import ParametroExperimento


@dataclass(frozen=True)
class DefinicionDeParametro:
    nombre: str
    etiqueta: str
    unidad: Optional[str] = None
    obligatorio: bool = False
    max_largo: int = 100
    grupo: Optional[str] = None  # bloque opcional y plegado del formulario donde se muestra (None: bloque principal)
    componentes: int = 1  # cuántas casillas componen el valor (3 para "x, y, z"); se guarda como un solo valor


class Tecnica(ABC):
    tipo: str
    etiqueta: str

    @abstractmethod
    def definiciones(self) -> list[DefinicionDeParametro]:
        """Parámetros de la técnica: nombre, unidad, obligatoriedad y formato."""

    @abstractmethod
    def validar(self, parametros: list[ParametroExperimento]) -> list[str]:
        """Validaciones propias entre parámetros. Devuelve los errores encontrados."""

    @abstractmethod
    def clave_de_coincidencia(self, parametros: list[ParametroExperimento]) -> dict[str, str]:
        """Parámetros (nombre → valor) que, junto con el tipo, definen que dos experimentos son el mismo (RF-03)."""

    @abstractmethod
    def parametros_resumen(self) -> list[str]:
        """Parámetros que se muestran en el listado."""
