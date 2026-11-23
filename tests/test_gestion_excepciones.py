from src.transversal.gestion_excepciones import (ErrorAlmacenamiento, ErrorPrevisto, ErrorValidacion,
                                                  SolicitudNoPendiente, respuesta_para)


def test_traduce_errores_de_validacion():
    r = respuesta_para(ErrorValidacion(["a", "b"]))
    assert r == {"tipo": "validacion", "mensajes": ["a", "b"]}


def test_traduce_solicitud_no_pendiente():
    assert respuesta_para(SolicitudNoPendiente())["tipo"] == "pendiente"


def test_traduce_falla_de_almacenamiento_con_mensaje_para_el_usuario():
    r = respuesta_para(ErrorAlmacenamiento("disco"))
    assert r["tipo"] == "almacenamiento" and "no quedó nada guardado" in r["mensajes"][0]


def test_traduce_un_error_previsto_generico():
    assert respuesta_para(ErrorPrevisto("x"))["tipo"] == "desconocido"
