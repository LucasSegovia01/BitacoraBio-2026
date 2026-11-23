"""Pruebas de HU-01.A1 (con B1.1 como base) y del escenario EC-07 a través del Ejecutor de registro."""
from datetime import date

import pytest

from src.arranque import construir_nucleo
from src.dominio.entidades import ParametroExperimento
from src.dominio.gestor_registro import EstadoPreparacion, ResultadoPreparacion
from src.dominio.registro_tecnicas import RegistroDeTecnicas
from src.dominio.tecnica import DefinicionDeParametro, Tecnica
from src.dominio.tecnica_docking import TecnicaDocking
from src.servicios.ejecutor_registro import EjecutorDeRegistro
from src.transversal.gestion_excepciones import ErrorValidacion, SolicitudNoPendiente
from tests.conftest import datos_validos, experimento_existente


def test_cp01_sin_coincidencias_registra_con_autor_y_fecha(sistema, repo, archivos):
    _, ejecutor = sistema
    e = ejecutor.registrar(datos_validos(), autor="ana").experimento
    assert e.autor == "ana" and e.fecha_de_carga is not None and repo.existe_experimento(e.id)
    assert e.ruta_pdb in archivos.archivos


def test_cp02_un_experimento_previo_invalido_no_se_reporta_y_se_guarda_normal(sistema, repo):
    _, ejecutor = sistema
    repo.guardar(experimento_existente(estado="invalido"))
    e = ejecutor.registrar(datos_validos(), autor="ana").experimento
    assert e.id is not None and len(repo.todos()) == 2


def test_cp03_con_opcionales_vacios_se_guarda_sin_exigirlos(sistema):
    _, ejecutor = sistema
    e = ejecutor.registrar(datos_validos(hardware="", tiempo_procesamiento="", objetivo="", hipotesis="", notas=""), "ana").experimento
    assert e.hardware == "" and e.notas == ""


def test_cp04_con_coincidencia_queda_pendiente_y_no_se_guarda_nada(sistema, repo, archivos):
    _, ejecutor = sistema
    existente_id = repo.guardar(experimento_existente())
    r = ejecutor.registrar(datos_validos(), autor="ana")
    assert not r.registrado and r.pendiente_id and [c.id for c in r.coincidencias] == [existente_id]
    assert len(repo.todos()) == 1 and archivos.archivos == {}


def test_cp05_confirmar_registra_un_experimento_nuevo_sin_tocar_el_existente(sistema, repo):
    _, ejecutor = sistema
    existente_id = repo.guardar(experimento_existente())
    antes = repo.todos()[0]
    pendiente = ejecutor.registrar(datos_validos(), autor="ana")
    nuevo = ejecutor.confirmar(pendiente.pendiente_id).experimento
    assert nuevo.id != existente_id and len(repo.todos()) == 2
    assert nuevo.similar_a == [] and repo.todos()[0] == antes
    assert nuevo.documento_notas and repo.todos()[0].documento_notas is None


def test_cp05b_el_experimento_nuevo_tiene_su_propio_documento_de_notas(sistema, repo):
    _, ejecutor = sistema
    primero = ejecutor.registrar(datos_validos(), autor="ana").experimento
    pendiente = ejecutor.registrar(datos_validos(), autor="ana")
    segundo = ejecutor.confirmar(pendiente.pendiente_id).experimento
    assert segundo.documento_notas and segundo.documento_notas != primero.documento_notas


def test_cp06_confirmar_no_repite_la_validacion_ni_la_deteccion(repo, archivos):
    class RepoContador(type(repo)):
        consultas = 0

        def con_parametros(self, tipo, clave):
            RepoContador.consultas += 1
            return super().con_parametros(tipo, clave)

    contador = RepoContador({"P1": "Proyecto uno"})
    _, ejecutor = construir_nucleo(contador, archivos)
    contador.guardar(experimento_existente())
    pendiente = ejecutor.registrar(datos_validos(), autor="ana")
    assert RepoContador.consultas == 1
    ejecutor.confirmar(pendiente.pendiente_id)
    assert RepoContador.consultas == 1  # no volvió a buscar


def test_cp06b_confirmar_usa_los_datos_originales_sin_recargarlos(sistema, repo):
    _, ejecutor = sistema
    repo.guardar(experimento_existente())
    pendiente = ejecutor.registrar(datos_validos(), autor="ana")
    nuevo = ejecutor.confirmar(pendiente.pendiente_id).experimento
    assert nuevo.valor_de("ligando") == "Indinavir" and nuevo.autor == "ana"


def test_cp06c_cancelar_descarta_la_solicitud_y_no_guarda_nada(sistema, repo, archivos):
    _, ejecutor = sistema
    repo.guardar(experimento_existente())
    pendiente = ejecutor.registrar(datos_validos(), autor="ana")
    ejecutor.cancelar(pendiente.pendiente_id)
    assert len(repo.todos()) == 1 and archivos.archivos == {}
    with pytest.raises(SolicitudNoPendiente):
        ejecutor.confirmar(pendiente.pendiente_id)


def test_cp06d_confirmar_dos_veces_o_un_id_desconocido_se_rechaza(sistema, repo):
    _, ejecutor = sistema
    repo.guardar(experimento_existente())
    pendiente = ejecutor.registrar(datos_validos(), autor="ana")
    ejecutor.confirmar(pendiente.pendiente_id)
    with pytest.raises(SolicitudNoPendiente):
        ejecutor.confirmar(pendiente.pendiente_id)
    with pytest.raises(SolicitudNoPendiente):
        ejecutor.confirmar("no-existe")
    assert len(repo.todos()) == 2


def test_cp07_con_varias_coincidencias_las_informa_todas(sistema, repo):
    _, ejecutor = sistema
    repo.guardar(experimento_existente())
    repo.guardar(experimento_existente(estado="en_curso"))
    assert len(ejecutor.registrar(datos_validos(), autor="ana").coincidencias) == 2


def test_cp08_datos_invalidos_se_rechazan_antes_de_buscar_duplicados(sistema, repo):
    _, ejecutor = sistema
    repo.guardar(experimento_existente())
    with pytest.raises(ErrorValidacion):
        ejecutor.registrar(datos_validos(pdb=None), autor="ana")
    assert len(repo.todos()) == 1


def test_cp09_tipo_desconocido(sistema):
    _, ejecutor = sistema
    with pytest.raises(ErrorValidacion):
        ejecutor.registrar(datos_validos(tipo="cristalografia"), autor="ana")


def test_cp10_el_ejecutor_no_guarda_si_el_gestor_pide_confirmacion_y_guarda_si_esta_listo():
    llamadas = []

    class GestorEspia:
        def __init__(self, estado):
            self.estado = estado

        def preparar(self, solicitud):
            llamadas.append("preparar")
            return ResultadoPreparacion(self.estado, [object()] if self.estado is EstadoPreparacion.REQUIERE_CONFIRMACION else [])

        def guardar_experimento(self, solicitud):
            llamadas.append("guardar_experimento")
            return object()

        def vincular_documento(self, experimento):
            llamadas.append("vincular_documento")

    registro = RegistroDeTecnicas()
    registro.registrar(TecnicaDocking())
    EjecutorDeRegistro(registro, GestorEspia(EstadoPreparacion.REQUIERE_CONFIRMACION)).registrar(datos_validos(), "ana")
    assert llamadas == ["preparar"]
    llamadas.clear()
    EjecutorDeRegistro(registro, GestorEspia(EstadoPreparacion.LISTO_PARA_GUARDAR)).registrar(datos_validos(), "ana")
    assert llamadas == ["preparar", "guardar_experimento", "vincular_documento"]


class TecnicaDinamicaDePrueba(Tecnica):
    """Plug-in de prueba (EC-07): una técnica nueva que se agrega sin modificar el núcleo."""

    tipo = "dinamica_molecular"
    etiqueta = "Dinámica molecular"

    def definiciones(self):
        return [DefinicionDeParametro("sistema", "Sistema", obligatorio=True),
                DefinicionDeParametro("paso_tiempo", "Paso de tiempo", unidad="fs", obligatorio=True)]

    def validar(self, parametros):
        return []

    def clave_de_coincidencia(self, parametros):
        return {p.nombre: p.valor for p in parametros if p.nombre == "sistema"}

    def parametros_resumen(self):
        return ["sistema", "paso_tiempo"]


def test_cp11_ec07_una_tecnica_nueva_se_registra_sin_modificar_el_nucleo(repo, archivos):
    registro, ejecutor = construir_nucleo(repo, archivos)
    registro.registrar(TecnicaDinamicaDePrueba())  # único cambio: sumar el plug-in
    datos = datos_validos(tipo="dinamica_molecular", valores={"sistema": "Lisozima en agua", "paso_tiempo": "2"})
    e = ejecutor.registrar(datos, autor="ana").experimento
    assert e.tipo == "dinamica_molecular"
    assert ParametroExperimento("paso_tiempo", "2", "fs") in e.parametros  # misma entidad, filas de parámetro con unidad
    assert not ejecutor.registrar(datos, autor="ana").registrado  # y la detección usa la clave de la técnica nueva
    assert registro.tecnica("docking").tipo == "docking"  # el docking sigue funcionando


def test_cp12_la_fecha_de_realizacion_se_conserva(sistema):
    _, ejecutor = sistema
    e = ejecutor.registrar(datos_validos(fecha_realizacion=date(2026, 11, 2)), autor="ana").experimento
    assert e.fecha_realizacion == date(2026, 11, 2)
