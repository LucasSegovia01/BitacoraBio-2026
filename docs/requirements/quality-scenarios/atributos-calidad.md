# Atributos de calidad — escenarios

**Taxonomía utilizada:** ISO/IEC 25010:2023.
**Trazabilidad:** este documento complementa el SRS del TP1 (`docs/requirements/srs.md`); los procesos, RF y CU referenciados se encuentran en ese documento.

## Selección de los 5 atributos y justificación

El grupo eligió **Eficiencia de desempeño, Fiabilidad, Mantenibilidad, Adecuación funcional y Capacidad de interacción** por ser los que más directamente condicionan si BitacoraBio 2026 cumple el propósito por el que se construye, evitar que el laboratorio vuelva a las planillas sueltas y a la memoria informal que el propio SRS identifica como el problema original:

- **Eficiencia de desempeño:** el valor del catálogo crece con el tiempo acumulando experimentos; si el rendimiento se degrada con el volumen, el sistema se vuelve menos útil justo cuando más experimentos tiene para prevenir duplicados — su propósito central.
- **Fiabilidad:** el sistema depende de un servicio externo (Google Docs) fuera del control del equipo; sin un camino de recuperación, una falla temporal de Google Docs dejaría bitácoras permanentemente sin vincular, rompiendo la trazabilidad a largo plazo que es el valor central del proyecto.
- **Mantenibilidad:** el primer riesgo de fracaso identificado en el Canvas de Descubrimiento es el cambio temprano de requerimientos (sumar nuevas técnicas, como una dinámica molecular); el propio SRS declara como parte del "Valor" del proyecto que debe quedar "consultable... para un integrante que se suma al grupo posteriormente"; si esa persona no puede diagnosticar un error sin ayuda externa, ese objetivo no se cumple.
- **Adecuación funcional:** el valor central del sistema es evitar pasos manuales (buscar a mano, abrir software externo), si las funciones agregan pasos innecesarios, el sistema no cumple su propósito aunque no presente errores.
- **Capacidad de interacción:** el perfil de usuario es técnicamente experto pero opera en un laboratorio, con posibles interrupciones; si la pantalla de alerta de duplicados no es operable con varias coincidencias a la vez, el mecanismo de prevención de duplicados se vuelve confuso y empuja al investigador/a a ignorar la alerta sin leerla, el efecto contrario al buscado.

## Atributo: Eficiencia de desempeño

**Entornos:** 2 de 3 escenarios en condiciones de sobrecarga o volumen (mayoría degradada).

**Escenario 1 — entorno normal**

| Campo | Detalle |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Consulta el catálogo filtrando por un solo criterio (ej. proteína) |
| Entorno | Operación normal — 1 usuario conectado, catálogo con volumen típico (~1.000 experimentos) |
| Artefacto | Módulo de consulta y filtro (Proceso 2) |
| Respuesta | El sistema devuelve los experimentos que coinciden con el filtro |
| Medida de respuesta | Se completa en 2 segundos o menos |

**Escenario 2 — entorno de sobrecarga (concurrencia)**

| Campo | Detalle |
|---|---|
| Fuente del estímulo | Múltiples investigadores/as (ej. todo el laboratorio consultando a la vez) |
| Estímulo | Cada uno consulta el catálogo con el mismo tipo de filtro simple del Escenario 1 |
| Entorno | Pico de uso — hasta 20 consultas concurrentes, mismo volumen de catálogo que el Escenario 1 |
| Artefacto | Módulo de consulta y filtro (Proceso 2) |
| Respuesta | El sistema resuelve todas las consultas sin bloquear ni descartar ninguna |
| Medida de respuesta | Cada consulta individual se completa en 5 segundos o menos, con 0% de consultas fallidas o con timeout |

**Escenario 3 — entorno de gran volumen de datos**

| Campo | Detalle |
|---|---|
| Fuente del estímulo | Investigador/a (mismo estímulo que el Escenario 1, sin concurrencia) |
| Estímulo | Consulta el catálogo filtrando por el mismo criterio simple (proteína) |
| Entorno | Catálogo con 100.000 experimentos registrados (en vez de ~1.000), 1 usuario conectado |
| Artefacto | Módulo de consulta y filtro |
| Respuesta | El sistema devuelve los experimentos que coinciden con el filtro |
| Medida de respuesta | Se completa en 5 segundos o menos |

## Atributo: Fiabilidad — Proceso 1 (dependencia de Google Docs)

**Entornos:** 2 de 3 escenarios en condición degradada o de recuperación (mayoría degradada).

**Escenario 1 — entorno normal**

| Campo | Detalle |
|---|---|
| Fuente del estímulo | Investigador/a (vía CU-01) |
| Estímulo | Confirma el registro de un experimento, disparando la creación automática del documento de notas |
| Entorno | Servicio de Google Docs disponible, respondiendo con normalidad |
| Artefacto | Módulo de creación/vinculación de documento de notas |
| Respuesta | El sistema crea el documento y lo asocia al experimento |
| Medida de respuesta | 100% de los registros quedan con el documento vinculado en el primer intento |

**Escenario 2 — entorno degradado (servicio externo no disponible)**

| Campo | Detalle |
|---|---|
| Fuente del estímulo | Investigador/a (mismo estímulo que el Escenario 1) |
| Estímulo | Confirma el registro de un experimento |
| Entorno | El servicio de Google Docs no responde o da timeout |
| Artefacto | Módulo de creación/vinculación de documento de notas, con el mecanismo de recuperación |
| Respuesta | El experimento queda guardado igual, con el documento de notas marcado como "no vinculado"; no se pierde ni se corrompe ningún dato ya guardado |
| Medida de respuesta | 100% de los experimentos quedan en estado consistente (guardados, sin documento) aunque falle Google Docs; 0% de pérdida de datos del registro |

**Escenario 3 — recuperación tras la degradación**

| Campo | Detalle |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Dispara "reintentar vinculación" sobre un experimento en estado "no vinculado" (consecuencia del Escenario 2) |
| Entorno | El servicio de Google Docs vuelve a estar disponible |
| Artefacto | Rama de recuperación de vinculación al documento de notas |
| Respuesta | El sistema crea y asocia el documento sin pedirle al investigador/a ningún dato de nuevo |
| Medida de respuesta | 95% o más de los reintentos se resuelven exitosamente sin intervención adicional |

## Atributo: Mantenibilidad — Modificabilidad y analizabilidad

**Entornos:** 1 de 2 escenarios en condición degradada.

**Escenario 1 — entorno normal (extensión planificada)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Desarrollador/a del equipo |
| Estímulo | Necesita agregar dinámica molecular como nueva técnica de experimento soportada |
| Entorno | Mantenimiento planificado, con acceso completo a la documentación y al modelo de dominio original |
| Artefacto | Modelo de datos de Experimento y ParametroExperimento |
| Respuesta | La nueva técnica se agrega definiendo sus parámetros como nuevas filas de ParametroExperimento, sin modificar el esquema de las tablas ya existentes (Experimento, Proyecto) |
| Medida de respuesta | La extensión no requiere alterar ni una sola columna de las tablas existentes; se implementa en menos de una jornada de trabajo |

**Escenario 2 — entorno degradado (sin el conocimiento del diseño original)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Un/a nuevo/a integrante del equipo, que no participó del diseño original |
| Estímulo | Debe corregir un error reportado en la lógica de detección de duplicados |
| Entorno | Degradado — sin acceso a quienes diseñaron el sistema originalmente, solo con la documentación disponible |
| Artefacto | Detector de Duplicados |
| Respuesta | El/la integrante localiza el módulo responsable apoyándose únicamente en el SRS y en el código, y aplica la corrección sin afectar otros procesos |
| Medida de respuesta | Identifica el módulo responsable en menos de 30 minutos, y la corrección no introduce regresiones verificables en el resto del sistema |

## Atributo: Adecuación funcional — Pertinencia funcional

**Entornos:** los 2 escenarios en condición sobre-estimulada (mayoría degradada).

**Escenario 1 — entorno sobre-estimulado (alto volumen de resultados de búsqueda)**

| Campo | Detalle |
|---|---|
| Subcaracterística | Pertinencia funcional |
| Fuente del estímulo | Investigador/a |
| Estímulo | Revisa las poses de varios experimentos de una misma búsqueda, uno después del otro |
| Entorno | Sobre-estimulado — resultado de búsqueda con alto número de coincidencias (ej. 20 o más experimentos) |
| Artefacto | Visor 3D de solo lectura |
| Respuesta | El investigador/a accede a la pose de cualquier experimento del listado de resultados sin pasos de navegación adicionales a medida que crece la cantidad de resultados — no se le exige paginar, recargar la lista completa, ni salir de la pantalla de resultados para llegar a la pose |
| Medida de respuesta | La cantidad de acciones del usuario para pasar de una fila del resultado a ver su pose se mantiene en 1, verificado sobre conjuntos de resultados de 20, 100 y 500 experimentos |

**Escenario 2 — entorno sobre-estimulado (estudio de sensibilidad de parámetros)**

| Campo | Detalle |
|---|---|
| Subcaracterística | Pertinencia funcional |
| Fuente del estímulo | Investigador/a |
| Estímulo | Registra varios experimentos sucesivos sobre el mismo par molécula/ligando, variando parámetros de la corrida (exhaustividad, función de scoring, software), para verificar la reproducibilidad del resultado |
| Entorno | Sobre-estimulado — ya existen 5 o más experimentos previos cargados para ese mismo par molécula/ligando, producto de un estudio de sensibilidad de parámetros; RF-03 no distingue por parámetro, solo por molécula/ligando |
| Artefacto | Detector de Duplicados |
| Respuesta | Cuando existen coincidencias previas para el par molécula/ligando, el sistema las muestra en una única lista o tabla (una sola pantalla o pop-up), sin abrir una pantalla separada por cada coincidencia encontrada; el investigador/a confirma "continuar" o cancela desde esa misma vista |
| Medida de respuesta | La cantidad de pantallas o pop-ups mostrados para revisar las coincidencias se mantiene en 1, verificado con conjuntos de 1, 5 y 10 coincidencias previas para el mismo par molécula/ligando |

## 6. Atributo: Capacidad de interacción — Operabilidad

**Entornos:** el único escenario en condición sobre-estimulada.

**Escenario 1 — entorno sobre-estimulado (múltiples coincidencias detectadas)**

| Campo | Detalle |
|---|---|
| Subcaracterística | Operabilidad |
| Fuente del estímulo | Investigador/a |
| Estímulo | Al registrar un experimento, CU-00 detecta varias coincidencias posibles a la vez (no una sola) |
| Entorno | Sobre-estimulado — más de una coincidencia mostrada simultáneamente para el mismo intento de registro |
| Artefacto | Interfaz de alerta de duplicado |
| Respuesta | El investigador/a puede revisar cada coincidencia individualmente y decidir continuar o cancelar sin perder de vista los datos que ya había cargado |
| Medida de respuesta | El investigador/a completa la decisión (continuar/cancelar) sin tener que volver a cargar ningún campo del formulario, cualquiera sea la cantidad de coincidencias mostradas |
