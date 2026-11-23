from __future__ import annotations

from ..dominio.puertos import ClienteGoogleDocs


class ClienteGoogleDocsSimulado(ClienteGoogleDocs):
    """Simula Google Docs: no se conecta a ningún servicio; devuelve un enlace ficticio y recuerda lo creado."""

    def __init__(self) -> None:
        self.documentos: dict[str, str] = {}
        self.apartados: dict[str, list[tuple[str, str]]] = {}

    def crear_documento(self, titulo: str, apartados: list[tuple[str, str]]) -> str:
        enlace = f"https://docs.google.com/document/simulado/{len(self.documentos) + 1}"
        self.documentos[enlace] = titulo
        self.apartados[enlace] = list(apartados)
        return enlace
