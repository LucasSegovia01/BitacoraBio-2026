from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Callable

from ..transversal.gestion_excepciones import ErrorAlmacenamiento, ErrorValidacion
from .detector_de_duplicados import DetectorDeDuplicados
from .entidades import Experimento
from .puertos import AlmacenamientoArchivos, ClienteGoogleDocs, RepositorioExperimentos
from .solicitud import SolicitudRegistro
from .tecnica import Tecnica

NOMBRE_PDB = "estructura.pdb"


class EstadoPreparacion(Enum):
    LISTO_PARA_GUARDAR = "listo_para_guardar"  # datos válidos y sin coincidencias
    REQUIERE_CONFIRMACION = "requiere_confirmacion"  # datos válidos pero con coincidencias


@dataclass(frozen=True)
class ResultadoPreparacion:
    estado: EstadoPreparacion
    coincidencias: list[Experimento] = field(default_factory=list)


class GestorDeRegistro:
    """Operaciones concretas del registro de un experimento. No decide el orden: eso lo hace el Ejecutor.

    Las reglas específicas de cada técnica las aplica la técnica; la búsqueda de duplicados, el detector.
    Datos inválidos es un rechazo (ErrorValidacion); encontrar coincidencias es un resultado normal.
    """

    def __init__(
        self,
        repositorio: RepositorioExperimentos,
        almacenamiento: AlmacenamientoArchivos,
        cliente_docs: ClienteGoogleDocs,
        detector: DetectorDeDuplicados,
        hoy: Callable[[], date] = date.today,
        ahora: Callable[[], datetime] = datetime.now,
    ):
        self._repo = repositorio
        self._archivos = almacenamiento
        self._docs = cliente_docs
        self._detector = detector
        self._hoy = hoy
        self._ahora = ahora

    def preparar(self, solicitud: SolicitudRegistro) -> ResultadoPreparacion:
        """Valida los datos y busca coincidencias. No guarda nada."""
        errores = self._errores_de(solicitud)
        if errores:
            raise ErrorValidacion(errores)
        coincidencias = self._detector.buscar(solicitud)
        if coincidencias:
            return ResultadoPreparacion(EstadoPreparacion.REQUIERE_CONFIRMACION, coincidencias)
        return ResultadoPreparacion(EstadoPreparacion.LISTO_PARA_GUARDAR)

    def guardar_experimento(self, solicitud: SolicitudRegistro) -> Experimento:
        """Guarda un experimento nuevo con autor y fecha, y sus archivos; si algo falla, revierte (HU-01.A1, RF-02)."""
        d = solicitud.datos
        experimento = Experimento(
            proyecto_id=d.proyecto_id,
            tipo=d.tipo,
            autor=solicitud.autor,
            fecha_de_carga=self._ahora(),
            fecha_realizacion=d.fecha_realizacion,
            parametros=solicitud.parametros(),
            hardware=d.hardware.strip(),
            tiempo_procesamiento=d.tiempo_procesamiento.strip(),
            objetivo=d.objetivo.strip(),
            hipotesis=d.hipotesis.strip(),
            notas=d.notas.strip(),
            estado_validez=d.estado_validez,
            similar_a=list(d.similar_a),
        )
        experimento.id = self._repo.guardar(experimento)
        try:
            experimento.ruta_pdb = self._archivos.guardar(experimento.id, NOMBRE_PDB, d.pdb)
            experimento.rutas_capturas = [self._archivos.guardar(experimento.id, n, c) for n, c in d.capturas]
            self._repo.actualizar_rutas(experimento)
        except Exception as causa:
            self._repo.eliminar(experimento.id)
            self._archivos.eliminar_archivos(experimento.id)
            raise ErrorAlmacenamiento(str(causa)) from causa
        return experimento

    def vincular_documento(self, experimento: Experimento, tecnica: Tecnica) -> None:
        """Crea el documento de notas propio del experimento, con apartados predefinidos, y guarda su enlace
        (HU-01.B1.2). El reintento queda fuera de alcance."""
        etiquetas = {d.nombre: d.etiqueta for d in tecnica.definiciones()}
        experimento.documento_notas = self._docs.crear_documento(
            f"Notas del experimento {experimento.id}", experimento.apartados_de_notas(etiquetas))
        self._repo.actualizar_rutas(experimento)

    def _errores_de(self, solicitud: SolicitudRegistro) -> list[str]:
        d = solicitud.datos
        errores: list[str] = []
        if not self._repo.existe_proyecto(d.proyecto_id):
            errores.append("El proyecto elegido no existe.")
        if d.fecha_realizacion is None:
            errores.append("La fecha de realización es obligatoria.")
        elif d.fecha_realizacion > self._hoy():
            errores.append("La fecha de realización no puede ser futura.")
        if not d.pdb:
            errores.append("El archivo PDB es obligatorio.")
        for definicion in solicitud.tecnica.definiciones():
            valor = d.valores.get(definicion.nombre, "").strip()
            if definicion.obligatorio and not valor:
                errores.append(f"{definicion.etiqueta} es obligatorio.")
            elif len(valor) > definicion.max_largo:
                errores.append(f"{definicion.etiqueta} supera los {definicion.max_largo} caracteres.")
        for nombre, _valor, _unidad in d.extras:
            if not nombre.strip():
                errores.append("Un parámetro adicional tiene valor pero no tiene nombre.")
        for otro_id in d.similar_a:
            if not self._repo.existe_experimento(otro_id):
                errores.append(f"El experimento '{otro_id}' indicado en 'Similar a' no existe.")
        if not errores:
            errores.extend(solicitud.tecnica.validar(solicitud.parametros()))
        return errores
