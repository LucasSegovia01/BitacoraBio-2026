import pytest

from src.dominio.detector_de_duplicados import DetectorDeDuplicados
from tests.conftest import experimento_existente, solicitud_de


@pytest.fixture
def detector(repo):
    return DetectorDeDuplicados(repo)


def test_sin_candidatos_devuelve_lista_vacia(detector):
    assert detector.buscar(solicitud_de()) == []


def test_devuelve_la_coincidencia(detector, repo):
    existente_id = repo.guardar(experimento_existente())
    assert [e.id for e in detector.buscar(solicitud_de())] == [existente_id]


def test_un_experimento_invalido_no_es_coincidencia(detector, repo):
    repo.guardar(experimento_existente(estado="invalido"))
    assert detector.buscar(solicitud_de()) == []


def test_un_experimento_declarado_en_similar_a_no_se_reporta(detector, repo):
    otro_id = repo.guardar(experimento_existente())
    assert detector.buscar(solicitud_de(similar_a=[otro_id])) == []


def test_otro_ligando_no_es_coincidencia(detector, repo):
    repo.guardar(experimento_existente(ligando="Ritonavir"))
    assert detector.buscar(solicitud_de()) == []


def test_otro_tipo_de_experimento_no_es_coincidencia(detector, repo):
    repo.guardar(experimento_existente(tipo="dinamica"))
    assert detector.buscar(solicitud_de()) == []


def test_buscar_no_escribe_nada(detector, repo):
    repo.guardar(experimento_existente())
    detector.buscar(solicitud_de())
    assert len(repo.todos()) == 1


def test_el_invalido_y_el_valido_a_la_vez_solo_informa_el_valido(detector, repo):
    repo.guardar(experimento_existente(estado="invalido"))
    valido_id = repo.guardar(experimento_existente())
    assert [e.id for e in detector.buscar(solicitud_de())] == [valido_id]


def _replica_de(repo, original_id, **cambios):
    replica = experimento_existente(**cambios)
    replica.similar_a = [original_id]
    return repo.guardar(replica)


def test_una_replica_no_se_reporta_si_ya_se_reporta_su_original(detector, repo):
    original_id = repo.guardar(experimento_existente())
    _replica_de(repo, original_id)
    assert [e.id for e in detector.buscar(solicitud_de())] == [original_id]


def test_con_muchas_replicas_solo_se_reporta_el_original(detector, repo):
    original_id = repo.guardar(experimento_existente())
    primera = _replica_de(repo, original_id)
    _replica_de(repo, primera)  # réplica de una réplica
    _replica_de(repo, original_id)
    assert [e.id for e in detector.buscar(solicitud_de())] == [original_id]


def test_declarar_el_original_cubre_tambien_a_sus_replicas(detector, repo):
    original_id = repo.guardar(experimento_existente())
    _replica_de(repo, original_id)
    assert detector.buscar(solicitud_de(similar_a=[original_id])) == []


def test_si_el_original_es_invalido_la_replica_valida_si_se_reporta(detector, repo):
    original_id = repo.guardar(experimento_existente(estado="invalido"))
    replica_id = _replica_de(repo, original_id)
    assert [e.id for e in detector.buscar(solicitud_de())] == [replica_id]
