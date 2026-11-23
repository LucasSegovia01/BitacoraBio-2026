"""Cliente real de Google Docs (vía Google Drive). Crea un documento de notas vacío dentro de una carpeta.

No se usa por defecto: ``arranque.py`` lo elige solo si está definida la variable de entorno
``BITACORABIO_GOOGLE_CREDENCIALES``. Las librerías de Google se importan recién al autorizar, así que el
resto de la aplicación y las pruebas funcionan sin instalarlas.
"""
from __future__ import annotations

from pathlib import Path

from ..dominio.puertos import ClienteGoogleDocs

# Acceso a Drive: hace falta para crear el documento dentro de una carpeta que creó la persona a mano.
ALCANCES = ["https://www.googleapis.com/auth/drive"]
TIPO_DOCUMENTO = "application/vnd.google-apps.document"


class ClienteGoogleDocsReal(ClienteGoogleDocs):
    def __init__(self, servicio_drive, carpeta_id: str | None = None) -> None:
        """``servicio_drive`` es el objeto de la API de Drive (``build("drive", "v3", ...)``); se inyecta para poder probar."""
        self._drive = servicio_drive
        self._carpeta_id = carpeta_id

    @classmethod
    def desde_credenciales(cls, ruta_credenciales: str, ruta_token: str, carpeta_id: str | None = None):  # pragma: no cover
        """Autoriza con OAuth (abre el navegador la primera vez y guarda el token) y arma el cliente."""
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build

        credenciales = None
        if Path(ruta_token).exists():
            credenciales = Credentials.from_authorized_user_file(ruta_token, ALCANCES)
        if not credenciales or not credenciales.valid:
            if credenciales and credenciales.expired and credenciales.refresh_token:
                credenciales.refresh(Request())
            else:
                flujo = InstalledAppFlow.from_client_secrets_file(ruta_credenciales, ALCANCES)
                credenciales = flujo.run_local_server(port=0)
            Path(ruta_token).write_text(credenciales.to_json(), encoding="utf-8")
        servicio = build("drive", "v3", credentials=credenciales)
        return cls(servicio, carpeta_id)

    def crear_documento(self, titulo: str) -> str:
        cuerpo = {"name": titulo, "mimeType": TIPO_DOCUMENTO}
        if self._carpeta_id:
            cuerpo["parents"] = [self._carpeta_id]
        creado = self._drive.files().create(body=cuerpo, fields="id,webViewLink").execute()
        return creado.get("webViewLink") or f"https://docs.google.com/document/d/{creado['id']}/edit"
