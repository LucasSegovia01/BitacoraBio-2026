from src.servicios.servicio_consulta import ServicioConsulta
from tests.conftest import experimento_existente


def test_lista_proyectos_y_experimentos_para_armar_el_formulario(repo):
    repo.guardar(experimento_existente())
    consulta = ServicioConsulta(repo)
    assert consulta.proyectos() == [("P1", "Proyecto uno")]
    assert [e.id for e in consulta.experimentos()] == ["101"]


def _cargar(repo, **cambios):
    e = experimento_existente(**{k: v for k, v in cambios.items() if k in ("proteina", "ligando", "estado")})
    if "autor" in cambios:
        e.autor = cambios["autor"]
    repo.guardar(e)
    return e


def test_resume_los_proyectos_con_cantidad_y_ultima_carga(repo):
    _cargar(repo)
    consulta = ServicioConsulta(repo)
    [resumen] = consulta.resumen_de_proyectos()
    assert (resumen["id"], resumen["cantidad"]) == ("P1", 1) and resumen["ultima"] is not None
    assert consulta.proyecto("P1")["nombre"] == "Proyecto uno"
    assert consulta.proyecto("ZZ") is None
    assert consulta.nombre_de_proyecto("P1") == "Proyecto uno" and consulta.nombre_de_proyecto("ZZ") == "ZZ"


def test_un_proyecto_sin_experimentos_no_tiene_ultima_carga(repo):
    assert ServicioConsulta(repo).resumen_de_proyectos()[0]["ultima"] is None


def test_busca_un_experimento_por_id_y_lista_los_de_un_proyecto(repo):
    _cargar(repo)
    consulta = ServicioConsulta(repo)
    assert consulta.experimento("101").id == "101" and consulta.experimento("999") is None
    assert [e.id for e in consulta.experimentos_de("P1")] == ["101"]
    assert consulta.experimentos_de("P2") == []


def test_filtra_por_texto_proyecto_autor_y_estado(repo):
    _cargar(repo, proteina="Lisozima", autor="ana")
    _cargar(repo, proteina="Tripsina", autor="beto", estado="invalido")
    c = ServicioConsulta(repo)
    assert len(c.buscar()) == 2
    assert [e.autor for e in c.buscar(texto="  LISOZIMA ")] == ["ana"]
    assert [e.autor for e in c.buscar(autor="beto")] == ["beto"]
    assert [e.autor for e in c.de_autor("ana")] == ["ana"]
    assert [e.autor for e in c.buscar(estado="invalido")] == ["beto"]
    assert c.buscar(proyecto="P2") == []
    assert c.buscar(texto="no existe") == []
    assert c.autores() == ["ana", "beto"]


def test_entrega_el_texto_del_pdb_o_nada(repo, archivos):
    e = experimento_existente()
    e.id = repo.guardar(e)
    consulta = ServicioConsulta(repo, archivos)
    assert consulta.contenido_pdb(e) is None  # sin ruta
    e.ruta_pdb = archivos.guardar(e.id, "estructura.pdb", b"ATOM\nEND\n")
    assert consulta.contenido_pdb(e) == "ATOM\nEND\n"
    assert consulta.contenido_pdb(experimento_existente_con_ruta("9/falta.pdb")) is None  # archivo ausente
    assert ServicioConsulta(repo).contenido_pdb(e) is None  # sin almacén


def experimento_existente_con_ruta(ruta):
    e = experimento_existente()
    e.ruta_pdb = ruta
    return e


def test_entrega_los_bytes_de_una_captura_o_nada(repo, archivos):
    e = experimento_existente()
    e.rutas_capturas = [archivos.guardar("101", "1-pose.png", b"PNG1"), "101/borrada.png"]
    repo.guardar(e)
    consulta = ServicioConsulta(repo, archivos)
    assert consulta.contenido_captura(e, 0) == b"PNG1"
    assert consulta.contenido_captura(e, 1) is None  # la ruta existe pero el archivo ya no está
    assert consulta.contenido_captura(e, 2) is None and consulta.contenido_captura(e, -1) is None  # índice fuera de rango
    assert ServicioConsulta(repo).contenido_captura(e, 0) is None  # sin almacenamiento
