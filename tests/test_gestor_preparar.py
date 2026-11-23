"""GestorDeRegistro.preparar: validación de datos y detección, sin guardar nada."""
from datetime import date

import pytest

from src.dominio.gestor_registro import EstadoPreparacion
from src.transversal.gestion_excepciones import ErrorValidacion
from tests.conftest import HOY, experimento_existente, solicitud_de


def errores_de(gestor, **cambios):
    with pytest.raises(ErrorValidacion) as e:
        gestor.preparar(solicitud_de(**cambios))
    return e.value.errores


def test_datos_validos_y_sin_coincidencias_quedan_listos_para_guardar(gestor):
    r = gestor.preparar(solicitud_de())
    assert r.estado is EstadoPreparacion.LISTO_PARA_GUARDAR and r.coincidencias == []


def test_proyecto_inexistente(gestor):
    assert any("proyecto" in m for m in errores_de(gestor, proyecto_id="PX"))


def test_fecha_vacia(gestor):
    assert any("fecha" in m.lower() for m in errores_de(gestor, fecha_realizacion=None))


def test_fecha_futura_se_rechaza_pero_hoy_se_acepta(gestor):
    assert any("futura" in m for m in errores_de(gestor, fecha_realizacion=date(2026, 11, 11)))
    gestor.preparar(solicitud_de(fecha_realizacion=HOY))


def test_pdb_obligatorio(gestor):
    assert any("PDB" in m for m in errores_de(gestor, pdb=None))


@pytest.mark.parametrize("campo", ["proteina", "ligando", "software"])
def test_parametro_obligatorio_de_la_tecnica_vacio(gestor, campo):
    valores = {"proteina": "A", "ligando": "B", "software": "Vina", campo: "   "}
    assert errores_de(gestor, valores=valores)


def test_largo_maximo_en_el_limite_pasa_y_uno_mas_falla(gestor):
    gestor.preparar(solicitud_de(valores={"proteina": "A" * 100, "ligando": "B", "software": "V"}))
    assert errores_de(gestor, valores={"proteina": "A" * 101, "ligando": "B", "software": "V"})


def test_parametro_extra_sin_nombre(gestor):
    assert any("no tiene nombre" in m for m in errores_de(gestor, extras=[("", "5", None)]))


def test_similar_a_inexistente(gestor):
    assert any("Similar a" in m for m in errores_de(gestor, similar_a=["999"]))


def test_similar_a_existente_pasa(gestor, repo):
    otro_id = repo.guardar(experimento_existente())
    gestor.preparar(solicitud_de(similar_a=[otro_id]))


def test_regla_propia_de_la_tecnica_proteina_igual_a_ligando(gestor):
    assert any("mismo" in m for m in errores_de(gestor, valores={"proteina": "X", "ligando": "x", "software": "V"}))


def test_informa_todos_los_errores_juntos(gestor):
    errores = errores_de(gestor, proyecto_id="PX", pdb=None, valores={"proteina": "", "ligando": "", "software": ""})
    assert len(errores) >= 5


def test_con_coincidencia_requiere_confirmacion_y_no_guarda_nada(gestor, repo, archivos):
    existente_id = repo.guardar(experimento_existente())
    r = gestor.preparar(solicitud_de())
    assert r.estado is EstadoPreparacion.REQUIERE_CONFIRMACION
    assert [c.id for c in r.coincidencias] == [existente_id]
    assert len(repo.todos()) == 1 and archivos.archivos == {}


def test_con_datos_invalidos_no_busca_duplicados(gestor, repo):
    repo.guardar(experimento_existente())
    with pytest.raises(ErrorValidacion):  # y no pide confirmación: validar va antes de detectar
        gestor.preparar(solicitud_de(pdb=None))
