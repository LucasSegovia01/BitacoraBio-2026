"""Repositorio SQLite: cumple el mismo contrato que el repositorio en memoria (puerto RepositorioExperimentos).

Son las mismas pruebas de `test_repositorio_en_memoria.py` más las propias de una base real: persistencia en archivo,
ids, ida y vuelta de todos los campos y borrado en cascada. Además, el núcleo real corre sobre SQLite sin cambios (CP-24).
"""
import sqlite3
from contextlib import closing
from datetime import date, datetime

import pytest

from src.acceso_datos.almacenamiento_archivos_en_memoria import AlmacenamientoArchivosEnMemoria
from src.acceso_datos.repositorio_sqlite import RepositorioExperimentosSQLite
from src.arranque import construir_nucleo
from src.dominio.entidades import Experimento, ParametroExperimento
from tests.conftest import datos_validos, experimento_existente


@pytest.fixture
def base():
    repositorio = RepositorioExperimentosSQLite(":memory:", {"P1": "Proyecto uno", "P2": "Proyecto dos"})
    yield repositorio
    repositorio.cerrar()


# --- mismo contrato que el repositorio en memoria --------------------------------------------------------------------
def test_trae_los_de_mismo_tipo_y_misma_clave_sin_distinguir_mayusculas(base):
    base.guardar(experimento_existente())
    assert len(base.con_parametros("docking", {"proteina": "  proteasa   hiv-1", "ligando": "INDINAVIR"})) == 1


def test_no_trae_los_de_otro_tipo(base):
    base.guardar(experimento_existente(tipo="dinamica"))
    assert base.con_parametros("docking", {"proteina": "Proteasa HIV-1"}) == []


def test_no_trae_los_de_otro_ligando(base):
    base.guardar(experimento_existente())
    assert base.con_parametros("docking", {"proteina": "Proteasa HIV-1", "ligando": "Ritonavir"}) == []


def test_no_trae_los_que_no_tienen_el_parametro_de_la_clave(base):
    base.guardar(experimento_existente())
    assert base.con_parametros("docking", {"software": "Vina"}) == []


def test_trae_tambien_los_invalidos_porque_no_decide_reglas(base):
    base.guardar(experimento_existente(estado="invalido"))
    assert len(base.con_parametros("docking", {"proteina": "Proteasa HIV-1", "ligando": "Indinavir"})) == 1


def test_con_clave_vacia_trae_todos_los_del_tipo(base):
    base.guardar(experimento_existente())
    base.guardar(experimento_existente(tipo="dinamica"))
    assert len(base.con_parametros("docking", {})) == 1


def test_guarda_y_recupera_el_enlace_del_documento(base):
    e = experimento_existente()
    e.id = base.guardar(e)
    e.documento_notas = "https://docs/1"
    base.actualizar_rutas(e)
    assert base.todos()[0].documento_notas == "https://docs/1"


# --- propias de una base real ---------------------------------------------------------------------------------------
def test_los_ids_siguen_la_numeracion_del_repositorio_en_memoria(base):
    primero = base.guardar(experimento_existente())
    segundo = base.guardar(experimento_existente())
    assert (primero, segundo) == ("101", "102")


def test_guardar_asigna_el_id_al_experimento(base):
    e = experimento_existente()
    assert base.guardar(e) == e.id == "101"


def test_ida_y_vuelta_conserva_todos_los_campos(base):
    original = Experimento(
        proyecto_id="P2", tipo="docking", autor="ana", fecha_de_carga=datetime(2026, 11, 10, 9, 30),
        fecha_realizacion=date(2026, 11, 1),
        parametros=[ParametroExperimento("proteina", "Lisozima"), ParametroExperimento("temperatura", "300", "K")],
        hardware="GPU", tiempo_procesamiento="2h", objetivo="obj", hipotesis="hip", notas="nota",
        estado_validez="finalizado", estado_analisis="analizado", similar_a=["101", "55"],
        ruta_pdb="101/e.pdb", rutas_capturas=["101/a.png", "101/b.png"], documento_notas="https://docs/9",
    )
    base.guardar(original)
    assert base.todos() == [original]


def test_los_parametros_se_devuelven_en_el_orden_en_que_se_guardaron(base):
    e = experimento_existente()
    e.parametros = [ParametroExperimento(n, "x") for n in ("c", "a", "b")]
    base.guardar(e)
    assert [p.nombre for p in base.todos()[0].parametros] == ["c", "a", "b"]


def test_eliminar_borra_el_experimento_y_sus_parametros(tmp_path):
    ruta = tmp_path / "base.db"
    repositorio = RepositorioExperimentosSQLite(str(ruta), {"P1": "Proyecto uno"})
    experimento_id = repositorio.guardar(experimento_existente())
    repositorio.eliminar(experimento_id)
    assert repositorio.todos() == [] and not repositorio.existe_experimento(experimento_id)
    with closing(sqlite3.connect(ruta)) as directa:
        assert directa.execute("SELECT COUNT(*) FROM parametro_experimento").fetchone()[0] == 0
    repositorio.cerrar()


def test_eliminar_un_id_inexistente_no_falla(base):
    base.eliminar("999")
    assert base.todos() == []


def test_existencia_de_proyectos_y_experimentos(base):
    experimento_id = base.guardar(experimento_existente())
    assert base.existe_proyecto("P1") and not base.existe_proyecto("P9")
    assert base.existe_experimento(experimento_id) and not base.existe_experimento("999")


def test_lista_los_proyectos_en_el_orden_de_alta(base):
    assert base.proyectos() == [("P1", "Proyecto uno"), ("P2", "Proyecto dos")]


def test_los_datos_sobreviven_a_cerrar_y_volver_a_abrir_la_base(tmp_path):
    ruta = str(tmp_path / "base.db")
    primera = RepositorioExperimentosSQLite(ruta, {"P1": "Proyecto uno"})
    primera.guardar(experimento_existente())
    primera.cerrar()
    segunda = RepositorioExperimentosSQLite(ruta, {"P1": "Proyecto uno"})
    assert len(segunda.todos()) == 1 and segunda.guardar(experimento_existente()) == "102"
    assert segunda.proyectos() == [("P1", "Proyecto uno")]
    segunda.cerrar()


# --- CP-24: cambiar el repositorio no obliga a cambiar nada más ------------------------------------------------------
def test_cp24_el_nucleo_real_registra_y_continua_pese_a_coincidencia_sobre_sqlite(base):
    _, ejecutor = construir_nucleo(base, AlmacenamientoArchivosEnMemoria())
    base.guardar(experimento_existente())
    pendiente = ejecutor.registrar(datos_validos(), autor="ana")
    assert not pendiente.registrado and len(pendiente.coincidencias) == 1 and len(base.todos()) == 1
    nuevo = ejecutor.confirmar(pendiente.pendiente_id).experimento
    assert nuevo.id == "102" and len(base.todos()) == 2 and nuevo.documento_notas is not None


def test_cp24b_similar_a_declarado_no_se_reporta_sobre_sqlite(base):
    _, ejecutor = construir_nucleo(base, AlmacenamientoArchivosEnMemoria())
    existente = experimento_existente()
    base.guardar(existente)
    resultado = ejecutor.registrar(datos_validos(similar_a=[existente.id]), autor="ana")
    assert resultado.registrado and base.todos()[-1].similar_a == [existente.id]
