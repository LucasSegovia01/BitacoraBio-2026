"""GestorDeRegistro.guardar_experimento y vincular_documento."""
import pytest

from src.acceso_datos.almacenamiento_archivos_en_memoria import AlmacenamientoArchivosEnMemoria
from src.acceso_datos.google_docs_simulado import ClienteGoogleDocsSimulado
from src.dominio.detector_de_duplicados import DetectorDeDuplicados
from src.dominio.gestor_registro import GestorDeRegistro
from src.transversal.gestion_excepciones import ErrorAlmacenamiento
from tests.conftest import AHORA, solicitud_de


class ArchivosQueFallan(AlmacenamientoArchivosEnMemoria):
    """Doble de prueba: guarda el PDB y falla con la captura (se interrumpe el guardado, CU-01 E2)."""

    def guardar(self, experimento_id, nombre, contenido):
        if nombre.endswith(".png"):
            raise OSError("disco desconectado")
        return super().guardar(experimento_id, nombre, contenido)


def test_guarda_con_autor_fecha_parametros_y_archivo(gestor, repo, archivos):
    e = gestor.guardar_experimento(solicitud_de())
    assert (e.autor, e.fecha_de_carga, e.id) == ("ana", AHORA, "101")
    assert [(p.nombre, p.valor) for p in e.parametros] == [
        ("proteina", "Proteasa HIV-1"), ("ligando", "Indinavir"), ("software", "AutoDock Vina")]
    assert e.ruta_pdb == "101/estructura.pdb" and archivos.archivos[e.ruta_pdb].startswith(b"ATOM")
    assert repo.existe_experimento("101")


def test_los_campos_opcionales_vacios_no_impiden_guardar(gestor):
    e = gestor.guardar_experimento(solicitud_de())
    assert (e.hardware, e.objetivo, e.hipotesis, e.notas, e.rutas_capturas) == ("", "", "", "", [])


def test_guarda_las_capturas_con_la_misma_abstraccion(gestor):
    e = gestor.guardar_experimento(solicitud_de(capturas=[("pose.png", b"png")]))
    assert e.rutas_capturas == ["101/pose.png"]


def test_dos_registros_iguales_crean_dos_experimentos_distintos(gestor, repo):
    e1, e2 = gestor.guardar_experimento(solicitud_de()), gestor.guardar_experimento(solicitud_de())
    assert e1.id != e2.id and len(repo.todos()) == 2


def test_si_falla_el_guardado_de_archivos_se_revierte_todo(repo):
    archivos = ArchivosQueFallan()
    gestor = GestorDeRegistro(repo, archivos, ClienteGoogleDocsSimulado(), DetectorDeDuplicados(repo))
    with pytest.raises(ErrorAlmacenamiento):
        gestor.guardar_experimento(solicitud_de(capturas=[("pose.png", b"png")]))
    assert repo.todos() == [] and archivos.archivos == {}


def test_vincular_crea_un_documento_propio_y_guarda_el_enlace(repo, archivos):
    cliente = ClienteGoogleDocsSimulado()
    gestor = GestorDeRegistro(repo, archivos, cliente, DetectorDeDuplicados(repo))
    e = gestor.guardar_experimento(solicitud_de())
    gestor.vincular_documento(e)
    assert e.documento_notas in cliente.documentos
    assert repo.todos()[0].documento_notas == e.documento_notas


def test_cada_experimento_recibe_un_documento_distinto(gestor):
    e1, e2 = gestor.guardar_experimento(solicitud_de()), gestor.guardar_experimento(solicitud_de())
    gestor.vincular_documento(e1)
    gestor.vincular_documento(e2)
    assert e1.documento_notas != e2.documento_notas
