"""El repositorio solo trae candidatos por tipo y clave; no aplica reglas de negocio (esas son de el Detector de duplicados)."""
from tests.conftest import experimento_existente


def test_trae_los_de_mismo_tipo_y_misma_clave_sin_distinguir_mayusculas(repo):
    repo.guardar(experimento_existente())
    assert len(repo.con_parametros("docking", {"proteina": "proteasa hiv-1", "ligando": "INDINAVIR"})) == 1


def test_no_trae_los_de_otro_tipo(repo):
    repo.guardar(experimento_existente(tipo="dinamica"))
    assert repo.con_parametros("docking", {"proteina": "Proteasa HIV-1"}) == []


def test_no_trae_los_de_otro_ligando(repo):
    repo.guardar(experimento_existente())
    assert repo.con_parametros("docking", {"proteina": "Proteasa HIV-1", "ligando": "Ritonavir"}) == []


def test_no_trae_los_que_no_tienen_el_parametro_de_la_clave(repo):
    repo.guardar(experimento_existente())
    assert repo.con_parametros("docking", {"software": "Vina"}) == []


def test_trae_tambien_los_invalidos_porque_no_decide_reglas(repo):
    repo.guardar(experimento_existente(estado="invalido"))
    assert len(repo.con_parametros("docking", {"proteina": "Proteasa HIV-1", "ligando": "Indinavir"})) == 1


def test_guarda_y_recupera_el_enlace_del_documento(repo):
    e = experimento_existente()
    e.id = repo.guardar(e)
    e.documento_notas = "https://docs/1"
    repo.actualizar_rutas(e)
    assert repo.todos()[0].documento_notas == "https://docs/1"
