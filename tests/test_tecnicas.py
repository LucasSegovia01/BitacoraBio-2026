import pytest

from src.dominio.entidades import ParametroExperimento
from src.dominio.registro_tecnicas import RegistroDeTecnicas
from src.dominio.tecnica_docking import TecnicaDocking
from src.transversal.gestion_excepciones import ErrorValidacion


def test_docking_define_proteina_ligando_y_software_como_obligatorios():
    obligatorios = {d.nombre for d in TecnicaDocking().definiciones() if d.obligatorio}
    assert obligatorios == {"proteina", "ligando", "software"}


def test_docking_rechaza_proteina_y_ligando_iguales():
    errores = TecnicaDocking().validar([ParametroExperimento("proteina", "Indinavir"), ParametroExperimento("ligando", " indinavir ")])
    assert errores and "no pueden ser el mismo" in errores[0]


def test_docking_acepta_proteina_y_ligando_distintos():
    assert TecnicaDocking().validar([ParametroExperimento("proteina", "A"), ParametroExperimento("ligando", "B")]) == []


def test_docking_arma_la_clave_de_coincidencia_con_proteina_y_ligando():
    parametros = [ParametroExperimento("proteina", " Proteasa HIV-1 "), ParametroExperimento("ligando", "Indinavir"),
                  ParametroExperimento("software", "Vina")]
    assert TecnicaDocking().clave_de_coincidencia(parametros) == {"proteina": "Proteasa HIV-1", "ligando": "Indinavir"}


def test_docking_resumen_del_listado():
    assert TecnicaDocking().parametros_resumen() == ["proteina", "ligando"]


def test_el_registro_entrega_la_tecnica_registrada():
    registro = RegistroDeTecnicas()
    docking = TecnicaDocking()
    registro.registrar(docking)
    assert registro.tecnica("docking") is docking and registro.disponibles() == [docking]


def test_el_registro_rechaza_un_tipo_desconocido():
    with pytest.raises(ErrorValidacion) as e:
        RegistroDeTecnicas().tecnica("dinamica")
    assert "no está disponible" in e.value.errores[0]


# --- Parámetros opcionales del docking (caja, exhaustividad, poses, afinidad) ---

def _p(**valores):
    return [ParametroExperimento(n, v) for n, v in valores.items()]


def test_docking_declara_cinco_parametros_opcionales_con_su_unidad_y_sin_entrar_en_la_clave():
    opcionales = {d.nombre: (d.unidad, d.componentes) for d in TecnicaDocking().definiciones() if d.grupo}
    assert opcionales == {"centro_caja": ("Å", 3), "tamano_caja": ("Å", 3), "exhaustividad": (None, 1),
                          "num_poses": (None, 1), "mejor_afinidad": ("kcal/mol", 1)}
    assert not any(d.obligatorio for d in TecnicaDocking().definiciones() if d.grupo)
    clave = TecnicaDocking().clave_de_coincidencia(_p(proteina="A", ligando="B", centro_caja="1, 2, 3", exhaustividad="8"))
    assert clave == {"proteina": "A", "ligando": "B"}


def test_docking_acepta_los_opcionales_bien_formados():
    assert TecnicaDocking().validar(_p(centro_caja="12.5, -3.0, 8.2", tamano_caja="20, 20, 20", exhaustividad="16",
                                       num_poses="10", mejor_afinidad="-9.4")) == []


@pytest.mark.parametrize("nombre, valor, etiqueta", [
    ("centro_caja", "12.5, , 8.2", "Centro de la caja"),
    ("centro_caja", "a, b, c", "Centro de la caja"),
    ("tamano_caja", "20, -5, 20", "Tamaño de la caja"),
    ("tamano_caja", "20, 20", "Tamaño de la caja"),
    ("exhaustividad", "0", "Exhaustividad"),
    ("exhaustividad", "8.5", "Exhaustividad"),
    ("num_poses", "-3", "Número de poses"),
    ("mejor_afinidad", "mucha", "Mejor afinidad"),
])
def test_docking_rechaza_opcionales_mal_formados(nombre, valor, etiqueta):
    errores = TecnicaDocking().validar(_p(**{nombre: valor}))
    assert len(errores) == 1 and errores[0].startswith(etiqueta)
