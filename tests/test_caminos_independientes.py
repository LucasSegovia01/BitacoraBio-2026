"""Ramas que la cobertura de ramas (pytest-cov --cov-branch) mostró sin recorrer, más los caminos de la tabla de complejidad."""
import pytest

from src.acceso_datos.almacenamiento_archivos_en_memoria import AlmacenamientoArchivosEnMemoria
from src.acceso_datos.google_docs_simulado import ClienteGoogleDocsSimulado
from src.dominio.detector_de_duplicados import DetectorDeDuplicados
from src.dominio.entidades import ParametroExperimento
from src.dominio.gestor_registro import GestorDeRegistro
from src.dominio.solicitud import SolicitudRegistro
from src.dominio.tecnica import DefinicionDeParametro, Tecnica
from src.transversal.gestion_excepciones import ErrorAlmacenamiento
from tests.conftest import datos_validos, solicitud_de


class TecnicaConOpcional(Tecnica):
    tipo = "con_opcional"
    etiqueta = "Con opcional"

    def definiciones(self):
        return [DefinicionDeParametro("a", "A", obligatorio=True), DefinicionDeParametro("b", "B", unidad="nm")]

    def validar(self, parametros):
        return []

    def clave_de_coincidencia(self, parametros):
        return {}

    def parametros_resumen(self):
        return ["a"]


class ArchivosQueFallanConElPdb(AlmacenamientoArchivosEnMemoria):
    def guardar(self, experimento_id, nombre, contenido):
        raise OSError("disco lleno")


def test_un_parametro_adicional_con_nombre_es_valido(gestor):
    r = gestor.preparar(solicitud_de(extras=[("temperatura", "300", "K")]))
    assert r.coincidencias == []


def test_los_parametros_opcionales_vacios_no_se_incluyen_en_la_solicitud():
    datos = datos_validos(tipo="con_opcional", valores={"a": "x", "b": "  "})
    s = SolicitudRegistro(datos=datos, autor="ana", tecnica=TecnicaConOpcional())
    assert [p.nombre for p in s.parametros()] == ["a"]


def test_si_falla_el_guardado_del_pdb_se_revierte_todo(repo):
    archivos = ArchivosQueFallanConElPdb()
    gestor = GestorDeRegistro(repo, archivos, ClienteGoogleDocsSimulado(), DetectorDeDuplicados(repo))
    with pytest.raises(ErrorAlmacenamiento):
        gestor.guardar_experimento(solicitud_de())
    assert repo.todos() == []


def test_eliminar_archivos_de_un_experimento_sin_archivos_no_falla(archivos):
    archivos.eliminar_archivos("999")
    assert archivos.archivos == {}


def test_eliminar_un_experimento_inexistente_no_falla(repo):
    repo.eliminar("999")
    assert repo.todos() == []


def test_cancelar_un_id_inexistente_no_falla(sistema):
    _, ejecutor = sistema
    ejecutor.cancelar("no-existe")


def test_confirmar_con_falla_de_almacenamiento_revierte_y_consume_lo_pendiente(repo, archivos, monkeypatch):
    from src.arranque import construir_nucleo
    from tests.conftest import experimento_existente

    _, ejecutor = construir_nucleo(repo, archivos)
    repo.guardar(experimento_existente())
    pendiente = ejecutor.registrar(datos_validos(), "ana").pendiente_id
    monkeypatch.setattr(archivos, "guardar", lambda *a, **k: (_ for _ in ()).throw(OSError("disco lleno")))
    with pytest.raises(ErrorAlmacenamiento):
        ejecutor.confirmar(pendiente)
    assert len(repo.todos()) == 1


# --- Caminos que la cobertura de ramas no distingue (condiciones con "and"/"or" y bucles que no iteran) ---

def test_docking_sin_proteina_no_dispara_la_regla_de_igualdad():
    from src.dominio.tecnica_docking import TecnicaDocking
    assert TecnicaDocking().validar([ParametroExperimento("ligando", "X")]) == []


def test_docking_sin_ligando_no_dispara_la_regla_de_igualdad():
    from src.dominio.tecnica_docking import TecnicaDocking
    assert TecnicaDocking().validar([ParametroExperimento("proteina", "X")]) == []


def test_docking_clave_con_parametros_ausentes_queda_vacia():
    from src.dominio.tecnica_docking import TecnicaDocking
    assert TecnicaDocking().clave_de_coincidencia([]) == {"proteina": "", "ligando": ""}


def test_el_repositorio_con_clave_vacia_trae_todos_los_del_tipo(repo):
    from tests.conftest import experimento_existente
    repo.guardar(experimento_existente())
    assert len(repo.con_parametros("docking", {})) == 1


def test_valor_de_devuelve_el_valor_del_parametro_pedido():
    from tests.conftest import experimento_existente
    assert experimento_existente().valor_de("ligando") == "Indinavir"
