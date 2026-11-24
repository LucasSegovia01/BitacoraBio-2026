"""ClienteGoogleDocsReal con un servicio de Drive falso (no se conecta a Google)."""
from src.acceso_datos.google_docs_real import (
    ESTILO_APARTADO, ESTILO_TEXTO, ESTILO_TITULO, ClienteGoogleDocsReal, TIPO_DOCUMENTO, armar_html,
)

APARTADOS = [("Autor", "ana"), ("Notas", "")]


def _media(contenido):
    return ("media", contenido)


class _Pedido:
    def __init__(self, respuesta):
        self._respuesta = respuesta

    def execute(self):
        return self._respuesta


class _DriveFalso:
    def __init__(self, respuesta):
        self.respuesta = respuesta
        self.llamadas = []

    def files(self):
        return self

    def create(self, body, media_body, fields):
        self.llamadas.append((body, media_body, fields))
        return _Pedido(self.respuesta)


def test_crea_el_documento_dentro_de_la_carpeta_y_devuelve_el_enlace():
    drive = _DriveFalso({"id": "abc", "webViewLink": "https://docs.google.com/document/d/abc/edit"})
    enlace = ClienteGoogleDocsReal(drive, "CARPETA1", _media).crear_documento("Notas del experimento 7", APARTADOS)
    assert enlace == "https://docs.google.com/document/d/abc/edit"
    cuerpo, media, _ = drive.llamadas[0]
    assert cuerpo == {"name": "Notas del experimento 7", "mimeType": TIPO_DOCUMENTO, "parents": ["CARPETA1"]}
    assert media[0] == "media" and b"Notas del experimento 7</h1>" in media[1]


def test_sin_carpeta_no_envia_parents():
    drive = _DriveFalso({"id": "abc", "webViewLink": "x"})
    ClienteGoogleDocsReal(drive, None, _media).crear_documento("T", APARTADOS)
    assert "parents" not in drive.llamadas[0][0]


def test_arma_el_enlace_si_la_respuesta_no_trae_webviewlink():
    drive = _DriveFalso({"id": "xyz"})
    assert ClienteGoogleDocsReal(drive, None, _media).crear_documento("T", APARTADOS) == "https://docs.google.com/document/d/xyz/edit"


def test_el_html_tiene_titulo_apartados_escapados_y_saltos_de_linea():
    html = armar_html("A <b>", [("Hipótesis", "x < y\nz"), ("Notas", "")])
    assert f'<h1 style="{ESTILO_TITULO}">A &lt;b&gt;</h1>' in html
    assert f'<h2 style="{ESTILO_APARTADO}">Hipótesis</h2><p style="{ESTILO_TEXTO}">x &lt; y<br>z</p>' in html
    assert f'<h2 style="{ESTILO_APARTADO}">Notas</h2><p style="{ESTILO_TEXTO}">&nbsp;</p>' in html


def test_sin_variable_de_entorno_se_usa_el_cliente_simulado(monkeypatch):
    from src.acceso_datos.google_docs_simulado import ClienteGoogleDocsSimulado
    from src.arranque import crear_cliente_docs
    monkeypatch.delenv("BITACORABIO_GOOGLE_CREDENCIALES", raising=False)
    assert isinstance(crear_cliente_docs(), ClienteGoogleDocsSimulado)


def test_con_variable_de_entorno_se_arma_el_cliente_real_con_su_carpeta_y_token(monkeypatch):
    from src.acceso_datos.google_docs_real import ClienteGoogleDocsReal
    from src.arranque import crear_cliente_docs
    recibido = {}

    def falso(ruta_credenciales, ruta_token, carpeta_id=None):
        recibido.update(credenciales=ruta_credenciales, token=ruta_token, carpeta=carpeta_id)
        return "cliente real"

    monkeypatch.setattr(ClienteGoogleDocsReal, "desde_credenciales", falso)
    monkeypatch.setenv("BITACORABIO_GOOGLE_CREDENCIALES", "cred.json")
    monkeypatch.setenv("BITACORABIO_GOOGLE_CARPETA", "CARPETA1")
    monkeypatch.delenv("BITACORABIO_GOOGLE_TOKEN", raising=False)
    assert crear_cliente_docs() == "cliente real"
    assert recibido == {"credenciales": "cred.json", "token": "token.json", "carpeta": "CARPETA1"}


def test_un_documento_sin_apartados_tiene_solo_el_titulo():
    assert f'<h1 style="{ESTILO_TITULO}">T</h1></body>' in armar_html("T", [])
