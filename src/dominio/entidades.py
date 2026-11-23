"""Entidades del modelo de dominio (TP1) que intervienen en HU-01.A1: Experimento y ParametroExperimento."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

ESTADOS_VALIDEZ = ("en_curso", "finalizado", "invalido")


def normalizar(texto: str) -> str:
    """Forma comparable de un valor: sin espacios de más y sin distinguir mayúsculas. La usa también quien guarda los datos."""
    return " ".join(texto.split()).casefold()


@dataclass(frozen=True)
class ParametroExperimento:
    """ParametroExperimento: un dato nombre-valor-unidad de un experimento (DA-03)."""

    nombre: str
    valor: str
    unidad: Optional[str] = None

    def mismo_valor_que(self, otro_valor: str) -> bool:
        """Compara sin distinguir mayúsculas ni espacios de más."""
        return normalizar(self.valor) == normalizar(otro_valor)


@dataclass
class Experimento:
    """Un experimento del catálogo. Guarda sus datos y conoce las reglas que dependen solo de sí mismo:
    si coincide con una clave de técnica y si puede contar como duplicado de otro (RF-03)."""

    proyecto_id: str
    tipo: str
    autor: str
    fecha_de_carga: datetime
    fecha_realizacion: date
    parametros: list[ParametroExperimento] = field(default_factory=list)
    hardware: str = ""
    tiempo_procesamiento: str = ""
    objetivo: str = ""
    hipotesis: str = ""
    notas: str = ""
    estado_validez: str = "en_curso"
    estado_analisis: str = "pendiente"
    similar_a: list[str] = field(default_factory=list)
    id: Optional[str] = None
    ruta_pdb: Optional[str] = None
    rutas_capturas: list[str] = field(default_factory=list)
    documento_notas: Optional[str] = None  # enlace al documento de notas propio (Google Docs, simulado)

    def __post_init__(self) -> None:
        if self.estado_validez not in ESTADOS_VALIDEZ:
            raise ValueError(f"estado de validez desconocido: {self.estado_validez}")

    def valor_de(self, nombre: str) -> Optional[str]:
        for p in self.parametros:
            if p.nombre == nombre:
                return p.valor
        return None

    def coincide_con(self, tipo: str, clave: dict[str, str]) -> bool:
        """Mismo tipo y mismo valor en cada parámetro de la clave de coincidencia (sin distinguir mayúsculas ni espacios)."""
        if self.tipo != tipo:
            return False
        for nombre, valor in clave.items():
            propio = next((p for p in self.parametros if p.nombre == nombre), None)
            if propio is None or not propio.mismo_valor_que(valor):
                return False
        return True

    def apartados_de_notas(self, etiquetas: dict[str, str]) -> list[tuple[str, str]]:
        """Apartados del documento de notas: datos del experimento y un apartado "Notas" para completar.

        ``etiquetas`` traduce el nombre interno de cada parámetro a su etiqueta legible (la da la técnica).
        """
        parametros = "\n".join(
            f"{etiquetas.get(p.nombre, p.nombre)}: {p.valor}" + (f" {p.unidad}" if p.unidad else "")
            for p in self.parametros)
        return [
            ("Fecha de realización", self.fecha_realizacion.isoformat()),
            ("Autor", self.autor),
            ("Técnica", self.tipo),
            ("Hipótesis", self.hipotesis),
            ("Objetivo", self.objetivo),
            ("Parámetros", parametros),
            ("Hardware", self.hardware),
            ("Tiempo de procesamiento", self.tiempo_procesamiento),
            ("Notas", self.notas),
        ]

    def es_replica_de_alguno(self, otros: list["Experimento"]) -> bool:
        """Este experimento se registró como "Similar a" de alguno de los otros: es una réplica, no un caso aparte."""
        return any(otro.id in self.similar_a for otro in otros)

    def es_candidato_a_duplicado(self) -> bool:
        """Un experimento marcado como inválido no cuenta como duplicado (RF-03)."""
        return self.estado_validez != "invalido"

