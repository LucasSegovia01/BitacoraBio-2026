# Reporte de cobertura y análisis (TP4 · HU-01.A1)

## Cómo se midió

- **Comando:** `pytest --cov=src --cov-branch --cov-report=term-missing` (usa `.coveragerc`, que activa ramas y excluye la interfaz gráfica y el arranque).
- **Excluido del cálculo (a propósito):** `src/presentacion/*` (interfaz gráfica; sus rutas se prueban con un cliente de prueba en `test_carga_experimentos.py`) y `src/arranque.py` (arma los objetos y carga datos de ejemplo).

## Resultado

145 pruebas, todas pasan.

| Archivo | Sentencias | Ramas | Cobertura |
|---|---|---|---|
| `acceso_datos/almacenamiento_archivos_en_memoria.py` | 15 | 2 | 100 % |
| `acceso_datos/google_docs_real.py` | 24 | 4 | 100 % |
| `acceso_datos/google_docs_simulado.py` | 11 | 0 | 100 % |
| `acceso_datos/repositorio_en_memoria.py` | 32 | 0 | 100 % |
| `acceso_datos/repositorio_sqlite.py` | 63 | 2 | 100 % |
| `dominio/detector_de_duplicados.py` | 12 | 0 | 100 % |
| `dominio/entidades.py` | 57 | 12 | 100 % |
| `dominio/gestor_registro.py` | 78 | 28 | 100 % |
| `dominio/puertos.py` | 21 | 0 | 100 % |
| `dominio/registro_tecnicas.py` | 15 | 0 | 100 % |
| `dominio/solicitud.py` | 36 | 4 | 100 % |
| `dominio/tecnica.py` | 23 | 0 | 100 % |
| `dominio/tecnica_docking.py` | 29 | 6 | 100 % |
| `servicios/ejecutor_registro.py` | 40 | 4 | 100 % |
| `servicios/servicio_consulta.py` | 53 | 14 | 100 % |
| `transversal/gestion_excepciones.py` | 21 | 6 | 100 % |
| **Total** | **532** | **82** | **100 %** |

## Análisis

### Qué dejó ver la primera medición con ramas

Con las 75 pruebas anteriores la cobertura era de 99 %: dos ramas parciales. Se agregaron pruebas (`CP-22`) para cada una y para las ramas que el análisis manual había anticipado:

- Con el repositorio SQLite se agregaron 18 pruebas (`test_repositorio_sqlite.py`): el mismo contrato del repositorio en memoria, la persistencia en archivo y un caso de punta a punta sobre SQLite.
- Tras pasar las reglas de coincidencia a `Experimento` (`coincide_con` y `es_candidato_a_duplicado`) se agregaron cinco pruebas de la entidad y las ramas quedaron igual de cubiertas.
- `gestor_registro.py` (parámetro adicional **con** nombre, el camino sin error) y `solicitud.py` (parámetro opcional vacío, que no se incluye): eran las dos ramas parciales.
- Falla del guardado del PDB (antes solo se probaba la falla de una captura), eliminar archivos o experimentos inexistentes, cancelar un id inexistente y la falla de almacenamiento al confirmar una solicitud pendiente.

### Lo que la cobertura de ramas no distingue

`coverage` no ve las condiciones dentro de un `and`/`or`: `proteina and ligando and igual` cuenta como una sola decisión. Por eso la tabla de complejidad ciclomática (diseño, 7.4) pide un camino por condición, y se agregaron casos de docking sin proteína y sin ligando. También agrega los bucles que no iteran (clave vacía, sin parámetros).

### Revisión por mutación manual

Se cambió una línea por vez y se volvió a correr la suite. Las diez mutaciones fueron detectadas:

| Mutación | ¿La detectó la suite? |
|---|---|
| `preparar` nunca pide confirmación | Sí |
| Quitar `eliminar` del rollback de `guardar_experimento` | Sí |
| Fecha futura: `>` por `>=` | Sí |
| Quitar la exclusión de "Similar a" en el detector | Sí |
| `confirmar` no consume la solicitud pendiente | Sí |
| `cancelar` no descarta la solicitud | Sí |
| `es_candidato_a_duplicado` siempre verdadero (un inválido contaría como duplicado) | Sí |
| `coincide_con` ignora el tipo | Sí |
| `coincide_con` ignora el valor del parámetro (solo mira que exista) | Sí |
| El detector deja de excluir los declarados en "Similar a" (`declara_similar` reemplazado por una constante) | Sí |

Pruebas débiles que conviene decir en la defensa:

- `CP-10` usa un gestor espía: verifica el orden y la decisión del ejecutor, no el contenido de las operaciones reales (se prueban aparte).
- `CP-21` pasa por las rutas de Flask y compara textos de las páginas: es una prueba de integración del flujo visible, no una prueba unitaria; la consigna pide que las pruebas unitarias no pasen por la interfaz, y por eso `CP-21` no cuenta para la cobertura (`presentacion` está excluida).

### Lo que la cobertura no dice

100 % significa que todo se ejecutó, no que todo se verificó. La medida de `EC-07` (0 columnas modificadas en menos de una jornada) no se puede medir con una prueba unitaria: `CP-11` verifica su condición estructural, pero el tiempo de "una jornada" depende de las personas. Tampoco se probó que la solicitud pendiente se pierda al reiniciar el servidor: es una limitación conocida (diseño, 5.1). La falla de `vincular_documento` (escenario `E1`) está fuera de alcance y no está implementada.

## Demostración

La demostración sigue el criterio de aceptación en la interfaz (`python run.py`, `http://localhost:5000/registro`):

1. Completar el formulario con proteína "Proteasa HIV-1", ligando "Indinavir", software, fecha y un PDB: coincide con el experimento de ejemplo #101 y aparece la pantalla de coincidencias.
2. **Realizar el registro de todas formas:** se registra el experimento nuevo (#102) sin volver al formulario y el #101 no cambia.
3. **Cancelar:** no se guarda nada.
4. Con otra proteína (sin coincidencias): el formulario queda en pantalla y debajo aparece el aviso de que se registró.
5. Dejar la proteína vacía: se rechaza con el mensaje, sin guardar.
