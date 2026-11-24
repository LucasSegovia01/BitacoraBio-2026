"""Cliente real de Google Docs (vía Google Drive). Crea un documento de notas con formato (título y apartados) dentro de una carpeta.

No se usa por defecto: ``arranque.py`` lo elige solo si está definida la variable de entorno
``BITACORABIO_GOOGLE_CREDENCIALES``. Las librerías de Google se importan recién al autorizar, así que el
resto de la aplicación y las pruebas funcionan sin instalarlas.
"""
from __future__ import annotations

from html import escape
from pathlib import Path

from ..dominio.puertos import ClienteGoogleDocs

# Acceso a Drive: hace falta para crear el documento dentro de una carpeta que creó la persona a mano.
ALCANCES = ["https://www.googleapis.com/auth/drive"]
TIPO_DOCUMENTO = "application/vnd.google-apps.document"


ESTILO_TITULO = "font-size:20pt;font-weight:bold;color:#1f3a5f;margin:0 0 6pt 0"
ESTILO_APARTADO = (
    "font-size:12pt;font-weight:bold;color:#2b6a8f;margin:14pt 0 2pt 0;"
    "border-bottom:1px solid #c9d6df;padding-bottom:2pt"
)
ESTILO_TEXTO = "font-size:11pt;font-weight:normal;color:#222222;margin:3pt 0 0 0;line-height:1.35"


def armar_html(titulo: str, apartados: list[tuple[str, str]]) -> str:
    """HTML del documento: un título y, por cada apartado, un subtítulo y su texto (los saltos de línea se conservan).
    Los estilos van en línea, que es lo que Drive respeta al convertirlo en un Google Doc."""
    partes = [f'<h1 style="{ESTILO_TITULO}">{escape(titulo)}</h1>']
    for nombre, texto in apartados:
        cuerpo = escape(texto).replace("\n", "<br>") or "&nbsp;"
        partes.append(f'<h2 style="{ESTILO_APARTADO}">{escape(nombre)}</h2><p style="{ESTILO_TEXTO}">{cuerpo}</p>')
    return f'<html><head><meta charset="utf-8"></head><body>{"".join(partes)}</body></html>'


def _media_html(contenido: bytes):  # pragma: no cover
    from googleapiclient.http import MediaInMemoryUpload

    return MediaInMemoryUpload(contenido, mimetype="text/html")


class ClienteGoogleDocsReal(ClienteGoogleDocs):
    def __init__(self, servicio_drive, carpeta_id: str | None = None, fabrica_media=None) -> None:
        """``servicio_drive`` es el objeto de la API de Drive (``build("drive", "v3", ...)``); se inyecta para poder probar.
        ``fabrica_media`` arma el contenido a subir a partir de bytes HTML (por defecto, el de la librería de Google)."""
        self._drive = servicio_drive
        self._carpeta_id = carpeta_id
        self._fabrica_media = fabrica_media or _media_html

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

    def crear_documento(self, titulo: str, apartados: list[tuple[str, str]]) -> str:
        """Sube el contenido como HTML y pide a Drive que lo convierta en Google Doc (título y apartados con formato)."""
        cuerpo = {"name": titulo, "mimeType": TIPO_DOCUMENTO}
        if self._carpeta_id:
            cuerpo["parents"] = [self._carpeta_id]
        contenido = self._fabrica_media(armar_html(titulo, apartados).encode("utf-8"))
        creado = self._drive.files().create(body=cuerpo, media_body=contenido, fields="id,webViewLink").execute()
        return creado.get("webViewLink") or f"https://docs.google.com/document/d/{creado['id']}/edit"
