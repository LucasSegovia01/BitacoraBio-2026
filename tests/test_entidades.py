import pytest

from src.dominio.entidades import Experimento, ParametroExperimento
from tests.conftest import experimento_existente


def test_parametro_compara_sin_distinguir_mayusculas_ni_espacios_de_mas():
    assert ParametroExperimento("proteina", "Proteasa HIV-1").mismo_valor_que("  proteasa   hiv-1 ")


def test_parametro_con_otro_valor_no_coincide():
    assert not ParametroExperimento("ligando", "Indinavir").mismo_valor_que("Ritonavir")


def test_estado_de_validez_desconocido_se_rechaza():
    with pytest.raises(ValueError):
        experimento_existente(estado="raro")


def test_valor_de_devuelve_none_si_no_hay_parametro():
    assert experimento_existente().valor_de("software") is None


def test_coincide_con_la_clave_sin_distinguir_mayusculas_ni_espacios():
    e = experimento_existente()
    assert e.coincide_con("docking", {"proteina": " proteasa  hiv-1", "ligando": "INDINAVIR"})


def test_no_coincide_si_el_tipo_es_otro():
    assert not experimento_existente(tipo="dinamica").coincide_con("docking", {"ligando": "Indinavir"})


def test_no_coincide_si_falta_un_parametro_de_la_clave():
    assert not experimento_existente().coincide_con("docking", {"software": "Vina"})


def test_no_coincide_si_un_valor_de_la_clave_es_distinto():
    assert not experimento_existente().coincide_con("docking", {"ligando": "Ritonavir"})


def test_un_experimento_invalido_no_es_candidato_a_duplicado():
    assert not experimento_existente(estado="invalido").es_candidato_a_duplicado()
    assert experimento_existente(estado="en_curso").es_candidato_a_duplicado()


def test_es_replica_de_alguno_mira_su_similar_a():
    from tests.conftest import experimento_existente
    original, replica = experimento_existente(), experimento_existente()
    original.id, replica.id, replica.similar_a = "1", "2", ["1"]
    assert replica.es_replica_de_alguno([original, replica])
    assert not original.es_replica_de_alguno([original, replica])
    assert not replica.es_replica_de_alguno([])



def test_los_apartados_de_notas_usan_etiquetas_unidades_y_texto_propio():
    from datetime import date, datetime
    e = Experimento(proyecto_id="1", tipo="docking", autor="ana", fecha_de_carga=datetime(2026, 1, 1),
                    fecha_realizacion=date(2026, 3, 4), hipotesis="H",
                    parametros=[ParametroExperimento("proteina", "P"), ParametroExperimento("caja", "20", "Å"),
                                ParametroExperimento("otro", "x")])
    apartados = dict(e.apartados_de_notas({"proteina": "Proteína", "caja": "Caja"}))
    assert apartados["Fecha de realización"] == "2026-03-04" and apartados["Hipótesis"] == "H"
    assert apartados["Parámetros"] == "Proteína: P\nCaja: 20 Å\notro: x"
    assert apartados["Notas"] == ""
