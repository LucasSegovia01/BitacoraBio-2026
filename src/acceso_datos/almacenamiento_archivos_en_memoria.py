from __future__ import annotations

from typing import Optional

from ..dominio.puertos import AlmacenamientoArchivos


class AlmacenamientoArchivosEnMemoria(AlmacenamientoArchivos):
    """Implementación actual (simulada): guarda los bytes en un diccionario indexado por ruta.

    La implementación proyectada es AlmacenamientoArchivosLocal, sobre el sistema de archivos.
    """

    def __init__(self) -> None:
        self.archivos: dict[str, bytes] = {}

    def guardar(self, experimento_id: str, nombre: str, contenido: bytes) -> str:
        ruta = f"{experimento_id}/{nombre}"
        self.archivos[ruta] = contenido
        return ruta

    def leer(self, ruta: str) -> Optional[bytes]:
        return self.archivos.get(ruta)

    def eliminar_archivos(self, experimento_id: str) -> None:
        for ruta in [r for r in self.archivos if r.startswith(f"{experimento_id}/")]:
            del self.archivos[ruta]
