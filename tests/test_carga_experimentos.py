"""Rutas de registro: los dos comportamientos de HU-01.A1 vistos desde la presentación."""
import io

import pytest

from src.arranque import construir_nucleo
from src.presentacion.carga_experimentos import crear_app
from src.servicios.servicio_consulta import ServicioConsulta
from tests.conftest import experimento_existente


@pytest.fixture
def cliente(repo, archivos):
    registro, ejecutor = construir_nucleo(repo, archivos)
    return crear_app(ejecutor, registro, ServicioConsulta(repo, archivos), autor="ana").test_client()


def formulario(**cambios):
    datos = {"tipo": "docking", "proyecto_id": "P1", "fecha_realizacion": "2026-11-01", "v_proteina": "Proteasa HIV-1",
             "v_ligando": "Indinavir", "v_software": "AutoDock Vina", "pdb": (io.BytesIO(b"ATOM\nEND\n"), "a.pdb")}
    datos.update(cambios)
    return datos


def enviar(cliente, **cambios):
    return cliente.post("/registro", data=formulario(**cambios), content_type="multipart/form-data")


def test_sin_coincidencias_sigue_en_el_formulario_con_el_aviso_debajo(cliente, repo):
    r = enviar(cliente)
    html = r.get_data(as_text=True)
    assert r.status_code == 200 and "Registrar experimento" in html
    assert "No se encontraron coincidencias y el experimento se registró correctamente" in html
    assert len(repo.todos()) == 1


def test_con_coincidencias_muestra_la_pantalla_y_no_guarda(cliente, repo):
    repo.guardar(experimento_existente())
    html = enviar(cliente).get_data(as_text=True)
    assert "Posibles coincidencias" in html and "Realizar el registro de todas formas" in html
    assert len(repo.todos()) == 1


def _pendiente_id(html):
    return html.split('name="pendiente_id" value="')[1].split('"')[0]


def test_confirmar_registra_sin_volver_al_formulario(cliente, repo):
    repo.guardar(experimento_existente())
    pid = _pendiente_id(enviar(cliente).get_data(as_text=True))
    r = cliente.post("/registro/confirmar", data={"pendiente_id": pid})
    assert r.status_code == 200 and "Experimento registrado" in r.get_data(as_text=True)
    assert len(repo.todos()) == 2


def test_cancelar_no_guarda_nada(cliente, repo):
    repo.guardar(experimento_existente())
    pid = _pendiente_id(enviar(cliente).get_data(as_text=True))
    assert "Registro cancelado" in cliente.post("/registro/cancelar", data={"pendiente_id": pid}).get_data(as_text=True)
    assert len(repo.todos()) == 1


def test_datos_invalidos_muestran_los_errores_y_no_guardan(cliente, repo):
    r = enviar(cliente, v_ligando="")
    assert r.status_code == 400 and "Ligando es obligatorio" in r.get_data(as_text=True)
    assert repo.todos() == []


def test_confirmar_una_solicitud_inexistente_informa_el_error(cliente):
    r = cliente.post("/registro/confirmar", data={"pendiente_id": "x"})
    assert r.status_code == 400 and "ya no existe" in r.get_data(as_text=True)


def test_registrar_como_similar_a_muestra_un_aviso_propio_y_no_la_pantalla_de_coincidencias(cliente, repo):
    existente = experimento_existente()
    repo.guardar(existente)
    html = enviar(cliente, similar_a=[existente.id]).get_data(as_text=True)
    assert "Registraste el experimento como similar a" in html and f"EXP-{int(existente.id):04d}" in html
    assert "Posibles coincidencias" not in html and "No se encontraron coincidencias" not in html
    assert len(repo.todos()) == 2


def test_el_detalle_ofrece_el_pdb_guardado_para_el_visor(cliente, repo):
    enviar(cliente)
    [e] = repo.todos()
    assert 'id="visor-pdb"' in cliente.get(f"/experimentos/{e.id}").get_data(as_text=True)
    assert cliente.get(f"/experimentos/{e.id}/pdb").get_data(as_text=True).startswith("ATOM")


def test_sin_pdb_o_sin_experimento_el_visor_recibe_404(cliente, repo):
    repo.guardar(experimento_existente())  # guardado sin archivo
    assert cliente.get("/experimentos/101/pdb").status_code == 404
    assert cliente.get("/experimentos/999/pdb").status_code == 404


def test_el_valor_de_tres_casillas_se_guarda_como_un_solo_parametro_con_coma_y_unidad(cliente, repo):
    enviar(cliente, **{"v_centro_caja__1": "12.5", "v_centro_caja__2": "-3.0", "v_centro_caja__3": "8.2",
                       "v_exhaustividad": "16", "v_mejor_afinidad": "-9.4"})
    [e] = repo.todos()
    assert (e.valor_de("centro_caja"), e.valor_de("exhaustividad"), e.valor_de("mejor_afinidad")) == ("12.5, -3.0, 8.2", "16", "-9.4")
    assert next(p.unidad for p in e.parametros if p.nombre == "centro_caja") == "Å"
    assert "Centro de la caja" in cliente.get(f"/experimentos/{e.id}").get_data(as_text=True)


def test_si_las_casillas_estan_vacias_no_se_guarda_el_parametro(cliente, repo):
    enviar(cliente, **{"v_centro_caja__1": "", "v_centro_caja__2": " ", "v_centro_caja__3": ""})
    assert repo.todos()[0].valor_de("centro_caja") is None


def test_casillas_incompletas_o_invalidas_muestran_el_error_y_dejan_el_bloque_abierto(cliente, repo):
    r = enviar(cliente, **{"v_centro_caja__1": "12.5", "v_centro_caja__3": "8.2", "v_exhaustividad": "0"})
    html = r.get_data(as_text=True)
    assert r.status_code == 400 and "Centro de la caja debe ser" in html and "Exhaustividad debe ser un entero positivo" in html
    assert '<details class="grupo-opcional" open' in html and 'value="12.5"' in html
    assert repo.todos() == []
