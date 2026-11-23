"""Punto de arranque: el único lugar que arma los objetos concretos (inyección de dependencias)."""
from __future__ import annotations

from datetime import date, datetime

from .acceso_datos.google_docs_simulado import ClienteGoogleDocsSimulado
from .acceso_datos.almacenamiento_archivos_en_memoria import AlmacenamientoArchivosEnMemoria
from .acceso_datos.repositorio_en_memoria import RepositorioExperimentosEnMemoria
from .acceso_datos.repositorio_sqlite import RepositorioExperimentosSQLite
from .dominio.entidades import Experimento, ParametroExperimento
from .dominio.detector_de_duplicados import DetectorDeDuplicados
from .dominio.gestor_registro import GestorDeRegistro
from .dominio.registro_tecnicas import RegistroDeTecnicas
from .dominio.tecnica_docking import TecnicaDocking
from .servicios.ejecutor_registro import EjecutorDeRegistro
from .servicios.servicio_consulta import ServicioConsulta


def construir_nucleo(repositorio, archivos, registro_tecnicas=None, cliente_docs=None):
    """Arma el núcleo del registro: Ejecutor, Gestor y Detector. Google Docs se simula (ClienteGoogleDocsSimulado)."""
    registro = registro_tecnicas or RegistroDeTecnicas()
    if registro_tecnicas is None:
        registro.registrar(TecnicaDocking())
    cliente_docs = cliente_docs or ClienteGoogleDocsSimulado()
    gestor = GestorDeRegistro(repositorio, archivos, cliente_docs, DetectorDeDuplicados(repositorio))
    return registro, EjecutorDeRegistro(registro, gestor)


def cargar_datos_de_ejemplo(repositorio, archivos) -> None:
    ejemplo = Experimento(
        proyecto_id="P1",
        tipo="docking",
        autor="director.demo",
        fecha_de_carga=datetime(2026, 10, 1, 10, 0),
        fecha_realizacion=date(2026, 10, 1),
        parametros=[ParametroExperimento("proteina", "Proteasa HIV-1"), ParametroExperimento("ligando", "Indinavir"), ParametroExperimento("software", "AutoDock Vina")],
    )
    experimento_id = repositorio.guardar(experimento=ejemplo)
    ejemplo.ruta_pdb = archivos.guardar(experimento_id, "estructura.pdb", b"HEADER EJEMPLO\nEND\n")
    repositorio.actualizar_rutas(ejemplo)


PROYECTOS = {"P1": "Inhibidores de proteasa", "P2": "Lisozima"}


def crear_aplicacion(ruta_db: str | None = None):
    """Sin `ruta_db`, la persistencia es en memoria; con una ruta, es una base SQLite en ese archivo.

    Es el único cambio necesario para reemplazar el repositorio: el resto del sistema usa el puerto."""
    from .presentacion.carga_experimentos import crear_app

    if ruta_db:
        repositorio = RepositorioExperimentosSQLite(ruta_db, PROYECTOS)
    else:
        repositorio = RepositorioExperimentosEnMemoria(PROYECTOS)
    archivos = AlmacenamientoArchivosEnMemoria()
    if not repositorio.todos():  # una base que ya tiene datos no se vuelve a sembrar
        cargar_datos_de_ejemplo(repositorio, archivos)
    registro, ejecutor = construir_nucleo(repositorio, archivos)
    return crear_app(ejecutor, registro, ServicioConsulta(repositorio, archivos), autor="investigadora.demo")
