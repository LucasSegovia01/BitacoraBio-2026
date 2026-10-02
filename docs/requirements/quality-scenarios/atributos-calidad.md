# Atributos de calidad — escenarios

**Taxonomía utilizada:** ISO/IEC 25010:2023.
**Trazabilidad:** este documento complementa el SRS del TP1 (`docs/requirements/srs.md`); los procesos, RF y CU referenciados corresponden a ese documento.

## 1. Selección de los 5 atributos y justificación

El grupo eligió **Eficiencia de desempeño, Fiabilidad, Mantenibilidad, Adecuación funcional y Capacidad de interacción** por ser los que más directamente condicionan si BitacoraBio 2026 cumple el propósito por el que se construye — evitar que el laboratorio vuelva a las planillas sueltas y a la memoria informal que el propio SRS identifica como el problema original:

- **Eficiencia de desempeño:** el valor del catálogo depende de que responda rápido incluso cuando crece; si una consulta simple tarda, el investigador vuelve a la planilla suelta que el sistema busca reemplazar.
- **Fiabilidad:** el sistema depende de un servicio externo (Google Docs) fuera del control del equipo; si una falla ahí hiciera perder el registro del experimento, el sistema sería menos confiable que lo que reemplaza.
- **Mantenibilidad:** el riesgo de fracaso #1 identificado en el Canvas de Descubrimiento es el cambio temprano de requerimientos (sumar nuevas técnicas); sin mantenibilidad, el MVP queda descartable en cuanto el laboratorio quiera crecer.
- **Adecuación funcional:** el valor central del sistema es evitar pasos manuales (buscar a mano, abrir software externo); si las funciones agregan pasos innecesarios, el sistema no cumple su propósito aunque funcione sin errores.
- **Capacidad de interacción:** el perfil de usuario es técnicamente experto pero opera en un laboratorio, con posibles interrupciones; si la interfaz no es operable bajo esas condiciones, no se adopta.

**Atributos considerados y dejados fuera, con motivo:**
- *Seguridad de la información:* el único dato mínimamente personal del sistema es el nombre del autor de cada experimento, ya declarado en el SRS como fuera de las categorías que exige proteger el Código de Ética IEEE/ACM — bajo riesgo real para esta entrega.
- *Compatibilidad:* el sistema interopera con un único servicio externo (Google Docs), ya cubierto por Fiabilidad; no hay otros sistemas con los que deba coexistir en este MVP.
- *Flexibilidad (ex-Portabilidad):* el despliegue multi-entorno no está definido todavía para esta entrega.

## 2. Atributo: Eficiencia de desempeño — Proceso 2

**Entornos:** 2 de 3 escenarios en condiciones de sobrecarga o volumen (mayoría degradada).

### Escenario 1 — entorno normal

| Campo | Detalle |
|---|---|
| Subcaracterística | Comportamiento temporal |
| Fuente del estímulo | Investigador/a |
| Estímulo | Consulta el catálogo filtrando por un solo criterio (ej. proteína) |
| Entorno | Operación normal — 1 usuario conectado, catálogo con volumen típico (~1.000 experimentos) |
| Artefacto | Módulo de consulta y filtro (Proceso 2) |
| Respuesta | El sistema devuelve los experimentos que coinciden con el filtro |
| Medida de respuesta | Se completa en 2 segundos o menos |

**Por qué es crítico:** es la línea base — si el camino más simple de consulta no responde con agilidad, no hay forma de que los casos más exigentes lo hagan.

### Escenario 2 — entorno de sobrecarga (concurrencia)

| Campo | Detalle |
|---|---|
| Subcaracterística | Capacidad |
| Fuente del estímulo | Múltiples investigadores/as (ej. todo el laboratorio consultando a la vez) |
| Estímulo | Cada uno consulta el catálogo con el mismo tipo de filtro simple del Escenario 1 |
| Entorno | Pico de uso — hasta 20 consultas concurrentes, mismo volumen de catálogo que el Escenario 1 |
| Artefacto | Módulo de consulta y filtro (Proceso 2) |
| Respuesta | El sistema resuelve todas las consultas sin bloquear ni descartar ninguna |
| Medida de respuesta | Cada consulta individual se completa en 5 segundos o menos, con 0% de consultas fallidas o con timeout |

**Por qué es crítico:** el escenario de uso real es un laboratorio completo trabajando en simultáneo; si el sistema se degrada con varios usuarios a la vez, deja de servir como fuente única de verdad del grupo.

### Escenario 3 — entorno de gran volumen de datos

| Campo | Detalle |
|---|---|
| Subcaracterística | Capacidad |
| Fuente del estímulo | Investigador/a (mismo estímulo que el Escenario 1, sin concurrencia) |
| Estímulo | Consulta el catálogo filtrando por el mismo criterio simple (proteína) |
| Entorno | Catálogo con 100.000 experimentos registrados (en vez de ~1.000), 1 usuario conectado |
| Artefacto | Módulo de consulta y filtro (Proceso 2) |
| Respuesta | El sistema devuelve los experimentos que coinciden con el filtro |
| Medida de respuesta | Se completa en 5 segundos o menos |

**Por qué es crítico:** el valor del catálogo crece con el tiempo acumulando experimentos; si el rendimiento se degrada con el volumen, el sistema se vuelve menos útil justo cuando más experimentos tiene para prevenir duplicados — su propósito central.

## 3. Atributo: Fiabilidad — Proceso 1 (dependencia de Google Docs)

**Entornos:** 2 de 3 escenarios en condición degradada o de recuperación (mayoría degradada).

### Escenario 1 — entorno normal

| Campo | Detalle |
|---|---|
| Subcaracterística | Disponibilidad |
| Fuente del estímulo | Investigador/a (vía CU-01) |
| Estímulo | Confirma el registro de un experimento, disparando la creación automática del documento de notas |
| Entorno | Servicio de Google Docs disponible, respondiendo con normalidad |
| Artefacto | Módulo de creación/vinculación de documento de notas (paso 7 de CU-01, RF-05) |
| Respuesta | El sistema crea el documento y lo asocia al experimento |
| Medida de respuesta | 100% de los registros quedan con el documento vinculado en el primer intento |

**Por qué es crítico:** confirma que el camino principal funciona — línea base necesaria antes de evaluar la tolerancia a fallos.

### Escenario 2 — entorno degradado (servicio externo no disponible)

| Campo | Detalle |
|---|---|
| Subcaracterística | Tolerancia a fallos |
| Fuente del estímulo | Investigador/a (mismo estímulo que el Escenario 1) |
| Estímulo | Confirma el registro de un experimento |
| Entorno | El servicio de Google Docs no responde o da timeout |
| Artefacto | Mismo módulo (paso 7 de CU-01, RF-05), con el mecanismo de recuperación de RF-09 (excepción E1 de CU-01) |
| Respuesta | El experimento queda guardado igual, con el documento de notas marcado como "no vinculado"; no se pierde ni se corrompe ningún dato ya guardado |
| Medida de respuesta | 100% de los experimentos quedan en estado consistente (guardados, sin documento) aunque falle Google Docs; 0% de pérdida de datos del registro |

**Por qué es crítico:** Google Docs es un servicio externo fuera del control del equipo; si su caída hiciera perder el registro del experimento, el sistema sería menos confiable que las planillas que reemplaza.

### Escenario 3 — recuperación tras la degradación

| Campo | Detalle |
|---|---|
| Subcaracterística | Capacidad de recuperación |
| Fuente del estímulo | Investigador/a |
| Estímulo | Dispara "reintentar vinculación" sobre un experimento en estado "no vinculado" (consecuencia del Escenario 2) |
| Entorno | El servicio de Google Docs vuelve a estar disponible |
| Artefacto | CU-01, excepción E1 — rama de recuperación (RF-09) |
| Respuesta | El sistema crea y asocia el documento sin pedirle al investigador/a ningún dato de nuevo |
| Medida de respuesta | 95% o más de los reintentos se resuelven exitosamente sin intervención adicional |

**Por qué es crítico:** sin un camino de recuperación, una falla temporal de Google Docs dejaría bitácoras permanentemente sin vincular, rompiendo la trazabilidad a largo plazo que es el valor central del proyecto.

## 4. Atributo: Mantenibilidad — Modificabilidad y analizabilidad

**Entornos:** 1 de 2 escenarios en condición degradada.

### Escenario 1 — entorno normal (extensión planificada)

| Campo | Detalle |
|---|---|
| Subcaracterística | Modificabilidad |
| Fuente del estímulo | Desarrollador/a del equipo |
| Estímulo | Necesita agregar dinámica molecular como nueva técnica de experimento soportada |
| Entorno | Mantenimiento planificado, con acceso completo a la documentación y al modelo de dominio original |
| Artefacto | Modelo de datos de Experimento y ParametroExperimento (Proceso 1) |
| Respuesta | La nueva técnica se agrega definiendo sus parámetros como nuevas filas de ParametroExperimento, sin modificar el esquema de las tablas ya existentes (Experimento, Proyecto) |
| Medida de respuesta | La extensión no requiere alterar ni una sola columna de las tablas existentes; se implementa en menos de una jornada de trabajo |

**Por qué es crítico:** es la mitigación directa al riesgo de fracaso #1 identificado en el Canvas de Descubrimiento; si no se cumple, el MVP queda obsoleto en cuanto el laboratorio quiera sumar otra técnica.

### Escenario 2 — entorno degradado (sin el conocimiento del diseño original)

| Campo | Detalle |
|---|---|
| Subcaracterística | Analizabilidad |
| Fuente del estímulo | Un/a nuevo/a integrante del equipo, que no participó del diseño original |
| Estímulo | Debe corregir un error reportado en la lógica de detección de duplicados |
| Entorno | Degradado — sin acceso a quienes diseñaron el sistema originalmente, solo con la documentación disponible |
| Artefacto | CU-00 · Detectar Duplicado y su documentación en el SRS |
| Respuesta | El/la integrante localiza el módulo responsable apoyándose únicamente en el SRS y en el código, y aplica la corrección sin afectar otros procesos |
| Medida de respuesta | Identifica el módulo responsable en menos de 30 minutos, y la corrección no introduce regresiones verificables en el resto del sistema |

**Por qué es crítico:** el propio SRS declara como parte del "Valor" del proyecto que debe quedar "consultable... para un integrante que se suma al grupo posteriormente"; si esa persona no puede diagnosticar un error sin ayuda externa, ese objetivo no se cumple.

## 5. Atributo: Adecuación funcional — Pertinencia funcional

**Entornos:** los 2 escenarios en condición sobre-estimulada (mayoría degradada).

### Escenario A — entorno sobre-estimulado (estudio de sensibilidad de parámetros)

| Campo | Detalle |
|---|---|
| Subcaracterística | Pertinencia funcional |
| Fuente del estímulo | Investigador/a |
| Estímulo | Registra varios experimentos sucesivos sobre el mismo par molécula/ligando, variando parámetros de la corrida (exhaustividad, función de scoring, software), para verificar la reproducibilidad del resultado |
| Entorno | Sobre-estimulado — ya existen 5 o más experimentos previos cargados para ese mismo par molécula/ligando, producto de un estudio de sensibilidad de parámetros; RF-03 no distingue por parámetro, solo por molécula/ligando |
| Artefacto | CU-00 · Detectar Duplicado, integrado en el flujo de CU-01 |
| Respuesta | Cuando existen coincidencias previas para el par molécula/ligando, el sistema las muestra en una única lista o tabla (una sola pantalla o pop-up), sin abrir una pantalla separada por cada coincidencia encontrada; el investigador/a confirma "continuar" o cancela desde esa misma vista |
| Medida de respuesta | La cantidad de pantallas o pop-ups mostrados para revisar las coincidencias se mantiene en 1, verificado con conjuntos de 1, 5 y 10 coincidencias previas para el mismo par molécula/ligando |

**Por qué es crítico:** conecta directo con el "Valor" central del sistema (evitar repetir ensayos sin saberlo); si el mecanismo de prevención de duplicados se vuelve una traba para una práctica legítima y común en docking, el sistema termina estorbando al propio flujo de trabajo que quiere apoyar.

### Escenario C — entorno sobre-estimulado (alto volumen de resultados de búsqueda)

| Campo | Detalle |
|---|---|
| Subcaracterística | Pertinencia funcional |
| Fuente del estímulo | Investigador/a |
| Estímulo | Revisa las poses de varios experimentos de una misma búsqueda, uno después del otro |
| Entorno | Sobre-estimulado — resultado de búsqueda con alto número de coincidencias (ej. 20 o más experimentos) |
| Artefacto | CU-02 (consulta y filtro) integrado con el visor 3D de solo lectura (RF-10) |
| Respuesta | El investigador/a accede a la pose de cualquier experimento del listado de resultados sin pasos de navegación adicionales a medida que crece la cantidad de resultados — no se le exige paginar, recargar la lista completa, ni salir de la pantalla de resultados para llegar a la pose |
| Medida de respuesta | La cantidad de acciones del usuario para pasar de una fila del resultado a ver su pose se mantiene en 1, verificado sobre conjuntos de resultados de 20, 100 y 500 experimentos |

**Por qué es crítico:** es la "alta fricción" descripta textualmente en el problema del SRS ("hay que descargar archivos y abrir software externo para ver un solo resultado"); si esa fricción reaparece al revisar varios resultados seguidos, el visor 3D pierde su razón de ser.

## 6. Atributo: Capacidad de interacción — Operabilidad

**Entornos:** el único escenario en condición sobre-estimulada.

### Escenario A — entorno sobre-estimulado (múltiples coincidencias detectadas)

| Campo | Detalle |
|---|---|
| Subcaracterística | Operabilidad |
| Fuente del estímulo | Investigador/a |
| Estímulo | Al registrar un experimento, CU-00 detecta varias coincidencias posibles a la vez (no una sola) |
| Entorno | Sobre-estimulado — más de una coincidencia mostrada simultáneamente para el mismo intento de registro |
| Artefacto | Interfaz de alerta de duplicado (CU-01, A1/E3) |
| Respuesta | El investigador/a puede revisar cada coincidencia individualmente y decidir continuar o cancelar sin perder de vista los datos que ya había cargado |
| Medida de respuesta | El investigador/a completa la decisión (continuar/cancelar) sin tener que volver a cargar ningún campo del formulario, cualquiera sea la cantidad de coincidencias mostradas |

**Por qué es crítico:** si la pantalla de alerta de duplicados no es operable con varias coincidencias a la vez, el mecanismo de prevención de duplicados —el valor central del sistema— se vuelve confuso y empuja al investigador/a a ignorar la alerta sin leerla, el efecto contrario al buscado.
