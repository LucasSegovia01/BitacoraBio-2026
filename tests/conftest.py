from datetime import date, datetime

import pytest

from src.acceso_datos.almacenamiento_archivos_en_memoria import AlmacenamientoArchivosEnMemoria
from src.acceso_datos.repositorio_en_memoria import RepositorioExperimentosEnMemoria
from src.arranque import construir_nucleo
from src.dominio.entidades import Experimento, ParametroExperimento
from src.dominio.solicitud import DatosRegistro

HOY = date(2026, 11, 10)
AHORA = datetime(2026, 11, 10, 9, 30)


def datos_validos(**cambios) -> DatosRegistro:
    base = dict(
        proyecto_id="P1",
        tipo="docking",
        fecha_realizacion=date(2026, 11, 1),
        valores={"proteina": "Proteasa HIV-1", "ligando": "Indinavir", "software": "AutoDock Vina"},
        pdb=b"ATOM      1  N   ALA A   1\nEND\n",
    )
    base.update(cambios)
    return DatosRegistro(**base)


def experimento_existente(proteina="Proteasa HIV-1", ligando="Indinavir", estado="finalizado", tipo="docking") -> Experimento:
    return Experimento(
        proyecto_id="P1",
        tipo=tipo,
        autor="otra.persona",
        fecha_de_carga=datetime(2026, 10, 1, 8, 0),
        fecha_realizacion=date(2026, 10, 1),
        parametros=[ParametroExperimento("proteina", proteina), ParametroExperimento("ligando", ligando)],
        estado_validez=estado,
    )


@pytest.fixture
def repo():
    return RepositorioExperimentosEnMemoria({"P1": "Proyecto uno"})


@pytest.fixture
def archivos():
    return AlmacenamientoArchivosEnMemoria()


@pytest.fixture
def sistema(repo, archivos):
    """Núcleo real con persistencia y archivos en memoria."""
    registro, ejecutor = construir_nucleo(repo, archivos)
    return registro, ejecutor


@pytest.fixture
def gestor(repo, archivos):
    from src.acceso_datos.google_docs_simulado import ClienteGoogleDocsSimulado
    from src.dominio.detector_de_duplicados import DetectorDeDuplicados
    from src.dominio.gestor_registro import GestorDeRegistro

    return GestorDeRegistro(repo, archivos, ClienteGoogleDocsSimulado(), DetectorDeDuplicados(repo),
                            hoy=lambda: HOY, ahora=lambda: AHORA)


def solicitud_de(**cambios):
    from src.dominio.solicitud import SolicitudRegistro
    from src.dominio.tecnica_docking import TecnicaDocking

    return SolicitudRegistro(datos=datos_validos(**cambios), autor="ana", tecnica=TecnicaDocking())
