"""Puertos hacia la capa de acceso a datos: el dominio los define y el acceso a datos los implementa."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from .entidades import Experimento


class RepositorioExperimentos(ABC):
    @abstractmethod
    def proyectos(self) -> list[tuple[str, str]]:
        """Pares (id, nombre) de los proyectos, para armar el formulario."""

    @abstractmethod
    def todos(self) -> list[Experimento]:
        """Todos los experimentos, para armar el campo "Similar a"."""

    @abstractmethod
    def existe_proyecto(self, proyecto_id: str) -> bool: ...

    @abstractmethod
    def existe_experimento(self, experimento_id: str) -> bool: ...

    @abstractmethod
    def con_parametros(self, tipo: str, clave: dict[str, str]) -> list[Experimento]:
        """Experimentos del mismo tipo con los mismos valores de la clave (sin excluir ninguno)."""

    @abstractmethod
    def guardar(self, experimento: Experimento) -> str:
        """Guarda el experimento, le asigna un id y lo devuelve."""

    @abstractmethod
    def actualizar_rutas(self, experimento: Experimento) -> None: ...

    @abstractmethod
    def eliminar(self, experimento_id: str) -> None: ...


class ClienteGoogleDocs(ABC):
    """Servicio externo (Google Docs). El dominio lo conoce solo por esta interfaz; en el TP4 hay una versión simulada."""

    @abstractmethod
    def crear_documento(self, titulo: str) -> str:
        """Crea un documento de notas vacío y devuelve su enlace."""


class AlmacenamientoArchivos(ABC):
    """Guarda archivos de un experimento (PDB, capturas, otros formatos futuros) y devuelve sus rutas.

    No distingue tipos de archivo: quien lo usa sabe qué función cumple cada uno.
    """

    @abstractmethod
    def guardar(self, experimento_id: str, nombre: str, contenido: bytes) -> str:
        """Guarda el archivo y devuelve su ruta (por ejemplo, 101/estructura.pdb)."""

    @abstractmethod
    def leer(self, ruta: str) -> Optional[bytes]:
        """Contenido del archivo guardado en esa ruta, o None si no está."""

    @abstractmethod
    def eliminar_archivos(self, experimento_id: str) -> None: ...
