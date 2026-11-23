from __future__ import annotations

import re

from .entidades import ParametroExperimento
from .tecnica import DefinicionDeParametro, Tecnica

GRUPO_DOCKING = "Parámetros del docking"
_NUMERO = r"-?\d+(?:\.\d+)?"
_POSITIVO = r"\d+(?:\.\d+)?"
_ENTERO = r"[1-9]\d*"
# nombre → (formato válido, etiqueta, cómo se describe en el mensaje). Todos son opcionales: solo se validan si vienen.
_FORMATOS = {
    "centro_caja": (re.compile(rf"{_NUMERO}\s*,\s*{_NUMERO}\s*,\s*{_NUMERO}"), "Centro de la caja", "tres números separados por coma (x, y, z)"),
    "tamano_caja": (re.compile(rf"{_POSITIVO}\s*,\s*{_POSITIVO}\s*,\s*{_POSITIVO}"), "Tamaño de la caja", "tres números positivos separados por coma (x, y, z)"),
    "exhaustividad": (re.compile(_ENTERO), "Exhaustividad", "un entero positivo"),
    "num_poses": (re.compile(_ENTERO), "Número de poses", "un entero positivo"),
    "mejor_afinidad": (re.compile(_NUMERO), "Mejor afinidad", "un número"),
}


class TecnicaDocking(Tecnica):
    """Plug-in de docking molecular: la única técnica que se construye en este TP."""

    tipo = "docking"
    etiqueta = "Docking molecular"

    def definiciones(self) -> list[DefinicionDeParametro]:
        return [
            DefinicionDeParametro("proteina", "Molécula / Proteína", obligatorio=True),
            DefinicionDeParametro("ligando", "Ligando", obligatorio=True),
            DefinicionDeParametro("software", "Software utilizado", obligatorio=True, max_largo=60),
            DefinicionDeParametro("centro_caja", "Centro de la caja", unidad="Å", grupo=GRUPO_DOCKING, componentes=3),
            DefinicionDeParametro("tamano_caja", "Tamaño de la caja", unidad="Å", grupo=GRUPO_DOCKING, componentes=3),
            DefinicionDeParametro("exhaustividad", "Exhaustividad", grupo=GRUPO_DOCKING),
            DefinicionDeParametro("num_poses", "Número de poses", grupo=GRUPO_DOCKING),
            DefinicionDeParametro("mejor_afinidad", "Mejor afinidad", unidad="kcal/mol", grupo=GRUPO_DOCKING),
        ]

    def validar(self, parametros: list[ParametroExperimento]) -> list[str]:
        valores = {p.nombre: p.valor for p in parametros}
        errores = []
        proteina, ligando = valores.get("proteina"), valores.get("ligando")
        if proteina and ligando and proteina.strip().casefold() == ligando.strip().casefold():
            errores.append("La molécula/proteína y el ligando no pueden ser el mismo.")
        for nombre, (formato, etiqueta, esperado) in _FORMATOS.items():
            if nombre in valores and not formato.fullmatch(valores[nombre].strip()):
                errores.append(f"{etiqueta} debe ser {esperado}.")
        return errores

    def clave_de_coincidencia(self, parametros: list[ParametroExperimento]) -> dict[str, str]:
        valores = {p.nombre: p.valor.strip() for p in parametros}
        return {n: valores.get(n, "") for n in ("proteina", "ligando")}

    def parametros_resumen(self) -> list[str]:
        return ["proteina", "ligando"]
