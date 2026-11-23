"""Gestión de excepciones (aspecto transversal, TP3 sección 5.4).

Define los errores previstos del registro (los rechazos; encontrar coincidencias no es un error) y los traduce en respuestas para el usuario.
"""
from __future__ import annotations


class ErrorPrevisto(Exception):
    """Error que el sistema espera y sabe explicar al usuario."""


class ErrorValidacion(ErrorPrevisto):
    """Faltan datos o tienen un formato inválido (CU-01 E5 y E6)."""

    def __init__(self, errores: list[str]):
        super().__init__("; ".join(errores))
        self.errores = list(errores)


class ErrorAlmacenamiento(ErrorPrevisto):
    """Falló el guardado de archivos; lo guardado se revirtió (CU-01 E2)."""

    def __init__(self, detalle: str):
        super().__init__(detalle)
        self.detalle = detalle


class SolicitudNoPendiente(ErrorPrevisto):
    """Se confirmó una solicitud que ya no está pendiente (ya se procesó, se canceló o no existe)."""

    def __init__(self):
        super().__init__("La solicitud ya no está pendiente.")


def respuesta_para(error: ErrorPrevisto) -> dict:
    """Convierte un error previsto en la respuesta que arma la pantalla: tipo y mensajes."""
    if isinstance(error, ErrorValidacion):
        return {"tipo": "validacion", "mensajes": error.errores}
    if isinstance(error, SolicitudNoPendiente):
        return {"tipo": "pendiente", "mensajes": ["El registro pendiente ya no existe. Completá el formulario de nuevo."]}
    if isinstance(error, ErrorAlmacenamiento):
        return {
            "tipo": "almacenamiento",
            "mensajes": ["No se pudo guardar el archivo; el registro se canceló y no quedó nada guardado."],
        }
    return {"tipo": "desconocido", "mensajes": [str(error)]}
