# Bitácora de Uso de IA

## Uso de IA — Definición y acotación del proyecto (TP1)

**Herramienta:** Gemini (Google).

**Registro de intercambios:**

1. **Consulta (15/08/26):** se le presentaron dos ideas de proyecto —un
   Motor de Evidencia Oncológica y una Bitácora de Experimentos
   Computacionales de Laboratorio— describiendo qué se buscaba hacer con
   cada una, para evaluar su viabilidad.
   **Generó:** recomendó la opción del catálogo de laboratorio, dado que no
   había certeza de encontrar una fuente de información pública para la
   otra opción.
   **Resultado:** se descartó por completo la idea del Motor Oncológico.

2. **Consulta (15/08/26):** se preguntó puntualmente si existía algún
   riesgo extremo u oculto en trabajar con la opción oncológica, enfocado
   al manejo de datos.
   **Generó:** advirtió que el fallo de un software médico puede derivar en
   diagnósticos erróneos, tratamientos incorrectos y daño directo al
   paciente, y recomendó evitar esa idea por el manejo de datos sensibles
   (expedientes médicos).
   **Resultado:** la advertencia confirmó que el rigor necesario para ese
   dominio excedía los tiempos, los objetivos del TP y el conocimiento del
   grupo; reforzó la decisión de descartar la opción oncológica.

3. **Consulta (16/08/26):** se preguntó si convenía enfocarse en un solo
   tipo de ensayo (ej. Docking Molecular) o abarcar varios desde el inicio.
   **Generó:** recomendó empezar estrictamente por un solo ensayo (Docking)
   para evitar el "desarrollo acelerado", advirtiendo que el impulso por
   lanzar funcionalidades rápido lleva a omitir etapas críticas y a fallas
   graves.
   **Resultado:** se aceptó acotar el alcance inicial a un solo ensayo
   (Docking), para concentrarse en la calidad de los requerimientos.

4. **Consulta (18/08/26):** se pidió que enumere pros y contras de los
   modelos de ciclo de vida (cascada, incremental, iterativo) para
   fundamentar la elección metodológica.
   **Generó:** sobre cascada, destacó claridad de fases y documentación
   bien definida, pero rigidez frente a cambios; sobre incremental,
   destacó la posibilidad de feedback temprano y entrega de valor desde
   etapas tempranas.
   **Resultado:** se descartó cascada por su rigidez; se adoptó el modelo
   iterativo e incremental para entregar el MVP de Docking tempranamente y
   poder adaptarse a cambios futuros en el dominio.

5. **Consulta (18/08/26):** se consultó cómo estructurar visualmente un
   Diagrama de Contexto (DFD Nivel 0) en Mermaid, por falta de soporte
   nativo de la herramienta de diagramado.
   **Generó:** indicó usar el tipo de gráfico `flowchart TD` y explicó su
   sintaxis.
   **Resultado:** se redactó el código mapeando las entidades propias del
   proyecto, siguiendo la sintaxis indicada.

**Qué se descartó y por qué:**
- Se descartó una sugerencia inicial de la IA de sumar módulos de Dinámica
  Molecular y otros tipos de ensayo a la primera entrega para hacer el
  catálogo "comercialmente más llamativo": ignoraba la restricción de
  tiempo y el tamaño del equipo (2 personas), y hubiera forzado un
  desarrollo acelerado saltando fases críticas.
- Se descartó el ejemplo genérico de Mermaid que la IA generó para el DFD,
  porque incluía un almacén de datos (base de datos) en un diagrama de
  Nivel 0 — un error conceptual detectado al revisar la teoría de la
  cátedra, ya que los almacenes de datos no deben graficarse en ese nivel.

**Errores o imprecisiones detectadas:**
- La sugerencia de ampliar el alcance a varios tipos de ensayo en la
  primera entrega, sin considerar las restricciones reales del equipo.
- La inclusión de un almacén de datos en el ejemplo de DFD Nivel 0,
  contrario a la convención de ese nivel de diagrama.

## Uso de IA — Revisión de Casos de Uso e Historias de Usuario

**Herramienta:** Claude (asistente de IA conversacional).

**Registro de intercambios:**

1. **Consulta:** se le pidió una devolución de CU-01 tal como estaba en el
   SRS.
   **Generó:** detectó ausencia de un CU para el Proceso 2 (elegido pero no
   desarrollado), contradicción entre el campo "estado" singular de
   Alcance/RF-01 y los dos campos separados del modelo de dominio, y el
   archivo PDB mencionado en Datos pero ausente del flujo de CU-01.
   **Resultado:** el CU-02 quedó a cargo de otro integrante del grupo; la
   incorporación del PDB al flujo quedó a cargo del grupo; la
   inconsistencia de "estado" se dejó pendiente, sin resolver por la IA.

2. **Consulta:** se le pidió plantear un CU-00 (Detectar Duplicado) propio,
   indicar dónde ubicarlo en el documento, y armar un cuadro de los slices
   de CU-01 en formato Cockburn.
   **Generó:** un CU-00 compacto (sin interesados ni disparador), con
   recomendación de ubicarlo antes de CU-01, y el cuadro de slices
   solicitado.
   **Resultado:** se aceptó tal cual la propuesta y la ubicación.

3. **Consulta:** se pidió dividir el slice básico de CU-01 en B1/B2, con un
   criterio de división explícito (valor central sin dependencias
   externas B1, vs. funcionalidad dependiente de un servicio externo B2), 
   una historia de usuario para el flujo de excepción E1 (falla de Google 
   Docs), y un slice adicional para formato de dato inválido.
   **Generó:** la HU-01.E1 con criterios Given/When/Then, y el slice A5 
   propuesto.
   **Resultado:** se aceptó la redacción de división B1/B2 y la HU-01.E1.
   **Nota:** la notación utilizada finalmente fue cambiada por el equipo:
   B1/B2 → B1.1/B1.2

4. **Consulta:** se pidió redactar RF-08 y RF-09 e incorporarlos al texto
   del flujo de CU-01, relacionando RF-09 con un caso de uso propio.
   **Generó:** el texto de RF-08 (validación de formato/completitud)
   insertado como paso explícito del flujo, y RF-09 (reintento de
   vinculación) modelado como CU-01b, caso de uso de extensión
   (`<<extend>>` de CU-01).
   **Resultado:** se aceptaron ambos RF y CU-01b tal cual. Se corrigieron
   manualmente los puntos de divergencia exactos de los flujos
   alternativos de CU-01; la renumeración que propuso la IA se usó solo
   como borrador de referencia, marcada para cotejar contra el archivo real
   antes de incorporarla.

5. **Consulta:** el docente recomendó dos correcciones sobre lo anterior:
   (a) un camino solo es "alternativo" si se cumple la función del caso de
   uso — todo lo que no la cumple es "excepción"; (b) CU-01b no debía ser
   un caso de uso aparte, sino una rama de recuperación dentro de la
   excepción E1 de CU-01. Se pidió aplicar ambos cambios y verificar
   consistencia en todo el documento.
   **Generó:** reclasificó los flujos "cancelar registro", "proyecto
   inexistente", "campo vacío" y "formato inválido" —antes A2, A3, A4, A5—
   como excepciones E3, E4, E5, E6, dejando A1 como único alternativo
   (es el único que termina con el experimento registrado). Plegó el
   mecanismo de reintento de RF-09 directamente en el texto de la
   excepción E1, eliminando CU-01b como caso de uso independiente.
   **Resultado:** se aceptaron ambos cambios. Al revisar el resto del
   documento se encontraron y corrigieron referencias que habían quedado
   con el nombramiento viejo: la HU-01.E1 citaba "slice A2" y "paso 6" en
   vez de "slice E3"/"E1" y "paso 7"; la trazabilidad completa seguía
   listando "Slice A2 → HU-01.A2"; y los escenarios de calidad de
   Fiabilidad y Mantenibilidad todavía mencionaban a CU-01b y al slice A2
   como si siguieran existiendo.

6. **Consulta:** se le pidió a la IA que comenzara a redactar las Historias de 
   Usuario (HU) con sus criterios de aceptación (Given/When/Then) a partir 
   de los slices de los casos de uso.
   **Generó:** redactó únicamente las historias correspondientes a los flujos 
   básicos, ignorando por completo los slices secundarios (excepciones y 
   alternativos, se especificó explicitamente cuales seria desarrollados). 
   Además, las historias eran excesivamente largas, incluían detalles técnicos
   de implementación en el "Then" (ej. consultas a la base de datos) o 
   incluyendo detalles correspondientes al Proceso de Gestión de Usuarios, el 
   cual no estaba entre los procesos seleccionados para profundizar.
   **Resultado:** se rechazó la generación inicial. Se le marcaron los errores
   basándonos en la teoría: los criterios de aceptación no deben describir 
   implementación técnica interna y solo se deben redactar HUs para los 
   procesos elegidos en el alcance. Se le escribió manualmente una historia de
   usuario como ejemplo (HU-01.B1.1) y se le pidió a la IA rehacer todo el 
   lote basándose exclusivamente en ese molde.

**Qué se descartó y por qué:**
- No se agregó un paso explícito de verificación de "proyecto existente"
  al flujo de CU-01: el grupo consideró que ya quedaba suficientemente
  claro en el paso 1 y en el alternativo (hoy excepción) E4.
- La incorporación del archivo PDB al flujo de registro quedó a cargo del
  grupo, no de la IA.
- **Se descartó el diseño de CU-01b como caso de uso de extensión**
  (`<<extend>>`), armado en un intercambio anterior con la misma IA: por
  indicación del docente, el reintento de vinculación con Google Docs no
  amerita un caso de uso propio, es la rama de recuperación de la
  excepción E1 de CU-01. Se refactorizó en consecuencia.
- **Se descartó la clasificación original de cuatro flujos como alternativos** 
  (A2-A5: cancelar, proyecto inexistente, campo vacío, formato inválido): 
  con el criterio del docente, ninguno de los cuatro termina con el experimento 
  registrado, así que se reclasificaron como excepciones (E3-E6).
- **Se descartaron todas las Historias de Usuario generadas por la IA con detalle 
  excesivo o detalles de procesos satelitales** (como el CRUD de Usuarios). La 
  justificación es que el alcance de TP1 exige desarrollar en profundidad solo los
  procesos seleccionados en el DFD, y aceptar esas historias hubiera significado 
  inflar el alcance artificialmente.

**Errores o imprecisiones detectadas:**
- Al aplicar la reclasificación A→E, la IA no propagó el cambio de nombre
  a todas las referencias existentes en el documento (trazabilidad, una
  historia de usuario, dos escenarios de calidad): quedaron varias
  menciones sueltas a nombres de slice viejos y a CU-01b, que hubo que
  revisar manualmente en una vuelta aparte hasta encontrarlas todas. Queda
  como aprendizaje: después de un renombrado, conviene pedir explícitamente
  una búsqueda de referencias cruzadas en todo el documento, no asumir que
  el cambio se propaga solo.
- Se detectó que la IA tiene una tendencia a sobre-especificar técnicamente las
  Historias de Usuario, introduciendo lógica de base de datos o código en los 
  criterios "Then". Se corrigió imponiendo un ejemplo manual (Prompt con Few-Shot).

## Uso de IA — Atributos de Calidad

1. **Consulta:** se presentaron seis ideas propias de escenarios de
   calidad (ISO 25010), y se pidió una idea adicional propia de la IA 
   (excluyendo Mantenibilidad, ya tomada por otro integrante).
   **Generó:** señaló que una idea de Rendimiento mezclaba dos variables
   distintas (complejidad de filtro y concurrencia) en un mismo par de
   escenarios; que una idea de Usabilidad sobre duplicados no detectados
   (falso negativo); y que dos ideas (parámetro nuevo vía JSON, nuevo tipo
   de análisis) caían bajo la misma característica ISO 25010
   (Mantenibilidad o Modificabilidad) que ya había elegido el otro
   integrante. Propuso un escenario propio de Seguridad (autorización),
   basado en la tabla de roles ya existente en el SRS.
   **Resultado:** se aceptó la idea de Seguridad propuesta por la IA. Se
   descartó la mitad de la idea de Usabilidad (el caso de falso negativo), 
   dado que al grupo le pareció finalmente que correspondía mas con manejo 
   de excepciones que con un Escenario de un Atributo de Calidad.
   La superposición con Mantenibilidad quedó marcada para coordinar con el
   otro integrante, sin resolver en esta conversación.

2. **Consulta:** se pidió desarrollar los tres escenarios de Rendimiento
   (Proceso 2) y los de Fiabilidad (dependencia de Google Docs), en
   formato de tabla (fuente-estímulo-artefacto-entorno-respuesta-medida),
   como código para pegar en el documento.
   **Generó:** tres escenarios de Rendimiento (normal, sobrecarga por
   concurrencia, gran volumen de datos) y tres de Fiabilidad (normal,
   servicio caído, recuperación vía RF-09/CU-01b), además del escenario de
   Seguridad ya mencionado, todos en el formato de tabla pedido.
   **Resultado:** se aceptaron los seis escenarios.

**Qué se descartó y por qué:**
- Se descartó la mitad de la idea de Usabilidad sobre duplicados no
  detectados (falso negativo): no es un atributo de calidad, es un defecto
  de corrección funcional de RF-03.

**Errores o imprecisiones detectadas:**
- En un primer intento de escenario de Rendimiento, la IA combinó
  complejidad de filtro y concurrencia en el mismo par de escenarios,
  violando el criterio de "una sola variable de entorno por par"; se
  separaron en dos ideas independientes antes de desarrollarlas.

## Uso de IA — Modelo de Dominio, Requerimientos Funcionales y Atributos de Calidad

**Herramienta:** Claude (asistente de IA conversacional).

**Registro de intercambios:**

1. **Consulta:** se pidió una opinión honesta, con ventajas y desventajas,
   entre la idea de catálogo de experimentos y una variante acotada de
   consulta de biomarcadores oncológicos, antes de descartar esta última
   definitivamente.
   **Generó:** comparación de ambas, recomendando el catálogo por no
   depender de servicios externos fuera del control del grupo; sugirió
   sumar integración con Google Docs y un visor 3D de solo lectura
   (3Dmol.js) para darle mayor profundidad de ingeniería sin ampliar el
   alcance a dinámica molecular completa.
   **Resultado:** se aceptó la recomendación y se sumaron ambas
   funcionalidades al alcance del MVP.

2. **Consulta:** se pidió armar el canvas de descubrimiento completo y el
   DFD Nivel 0 a partir de las decisiones ya conversadas.
   **Generó:** el canvas (dominio, datos, usuarios, valor, alcance,
   riesgos, datos sensibles) y el diagrama en Mermaid con las entidades
   externas del sistema.
   **Resultado:** se aceptaron ambos, con correcciones menores de tipeo
   antes de incorporarlos al SRS.

3. **Consulta:** se preguntó si el Director del grupo debía tener permisos
   distintos a los del Investigador/a, o si todos debían tener el mismo
   nivel de acceso.
   **Generó:** argumentos a favor (evitar que un integrante modifique o
   borre la carga de otro sin autorización) y en contra (complejidad
   adicional de control de acceso), dejando ambas opciones como válidas
   según el tiempo disponible.
   **Resultado:** se aceptó diferenciar roles (Investigador/a vs.
   Director/a).

4. **Consulta:** antes de descartar definitivamente la idea de
   biomarcadores oncológicos, se preguntó si era realizable en la vida
   real, con qué variante (epigenética o biomarcador genético clásico) y
   qué fuentes públicas existían.
   **Generó:** casos reales documentados en oncología (HER2/trastuzumab,
   EGFR/inhibidores de tirosina-quinasa, KRAS/cetuximab) y las fuentes
   públicas asociadas (TCGA/GDC, cBioPortal), junto con un análisis de por
   qué el volumen de curación de evidencia necesario excedía el tiempo
   del cuatrimestre.
   **Resultado:** confirmó la decisión de descartar esa idea; se armó
   además una consulta por mail al docente comparando ambas opciones
   finalistas, cuya respuesta (fuente NCCN sin acceso público, riesgo de
   incompatibilidad de vocabularios entre fuentes) reforzó la decisión
   final por el catálogo de experimentos.

5. **Consulta:** se pidió ayuda para redactar los requerimientos
   funcionales a partir de una lista informal de ideas sueltas del grupo
   (usuarios y roles, permisos de "jefes" sobre proyectos, filtros,
   registro automático, enlace a Google Docs, detección de duplicados).
   **Generó:** una primera versión numerada de RF, señalando ambigüedades
   a resolver antes de continuar: si "proyecto" era una entidad nueva del
   modelo de dominio, si "experimento" y "análisis" debían tratarse como
   lo mismo, y una contradicción entre permisos de edición mencionados en
   distintos momentos de la charla.
   **Resultado:** se aceptaron las interpretaciones propuestas como punto
   de partida, y se corrigieron en consultas posteriores a medida que el
   grupo definía mejor el modelo (entidad Proyecto, estados de validez y
   de análisis del experimento).

6. **Consulta:** se pidió actualizar el modelo de dominio y el DFD Nivel 1
   tras incorporar Proyecto y los estados del experimento; más adelante,
   el grupo notó que faltaba un proceso de registro de usuario en ambos
   niveles del DFD.
   **Generó:** el diagrama de clases y el DFD Nivel 1 actualizados; luego,
   el Proceso 9 (Registrar Usuario) y sus flujos correspondientes en el
   DFD Nivel 0 y Nivel 1, junto con la observación de que el primer
   Director del sistema no puede darse de alta a sí mismo por esta vía,
   y requiere un dato de siembra inicial fuera de la interfaz.
   **Resultado:** se aceptaron ambas actualizaciones.

7. **Consulta:** se pidieron los escenarios de calidad (ISO 25010) para el
   atributo de mantenibilidad, en el mismo formato de tabla de 6 campos
   ya usado para fiabilidad y usabilidad.
   **Generó:** dos escenarios (entorno normal de extensión planificada, y
   entorno degradado sin conocimiento del diseño original), conectados
   explícitamente con el riesgo de cambio de requerimientos ya
   documentado en el canvas.
   **Resultado:** se aceptaron ambos escenarios.

**Qué se descartó y por qué:**
- Se descartó por completo la idea de un sistema de consulta biomarcador-
  tratamiento oncológico, pese a confirmarse su viabilidad científica y de
  datos públicos, por exceder el tiempo disponible para curar evidencia
  clínica de calidad en un cuatrimestre con dos personas.

**Errores o imprecisiones detectadas:** ninguna imprecisión factual
relevante de la IA en esta sección; las correcciones fueron ajustes de
alcance y consistencia interna del propio documento en evolución.

## Uso de IA — Corrección de las capas del TP3 (arquitectura)

**Herramienta:** Claude (asistente de IA conversacional).

**Registro de intercambios:**

1. **Consulta (10/11/26):** el docente indicó que la capa de servicios era
   demasiado grande y mezclaba funciones de negocio y de servicio. Se
   pidieron opciones de diseño antes de tocar nada.
   **Generó:** tres opciones: cinco capas (presentación, servicios fina,
   negocio, acceso a datos e integración externa), cuatro capas
   (presentación, servicios fina, negocio y acceso a datos y servicios
   externos) y un esquema de aplicación, dominio e infraestructura.
   Recomendó cinco capas.
   **Resultado:** se descartó la recomendación de la IA. Tras consultar de
   nuevo al docente, este definió cuatro capas: servicios sin lógica
   (Ejecutor de registro, Servicio de consulta y Gestión de capturas), una
   capa de dominio con el resto del núcleo del microkernel (Registro de
   técnicas, los pasos del registro y los plug-ins), y lo demás sin
   cambios. Coincidía con la segunda opción propuesta.

2. **Consulta (10/11/26):** se pidió aplicar el cambio en el documento
   `arquitectura.md`, con el diagrama de componentes del grupo como guía.
   **Generó:** los cambios en 5.2.2, 5.3 (tabla de capas y restricciones),
   5.5, la sección 7 (diagrama y catálogo de componentes) y DA-01. Incluyó
   dos saltos de capa justificados: las rutas de registro piden las
   técnicas directamente al registro de técnicas para armar el formulario,
   y el servicio de consulta y la gestión de capturas llaman directo al
   acceso a datos, porque no ejecutan reglas de negocio. También agregó en
   DA-01 la alternativa descartada de tres capas con las reglas dentro de
   servicios.
   **Resultado:** se aceptó y se incorporó al documento luego de revisión.

**Qué se descartó y por qué:**
- Se descartó la recomendación de cinco capas: el docente fijó cuatro, y
  la integración con servicios externos quedó dentro de la capa de acceso
  a datos.

**Errores o imprecisiones detectadas:**
- La IA dejó que el servicio de consulta y la gestión de capturas llamaran
  al acceso a datos sin pasar por el dominio. Se declaró como salto
  justificado, pero queda una pregunta abierta para el docente: si la
  regla "solo el autor puede modificar las capturas" es una regla de
  servicio o debe pasar a la capa de dominio.

  ## Uso de IA — Revisión del Diseño Detallado y Casos de Prueba (TP4)

**Herramienta:** ChatGPT (asistente de IA conversacional).

**Registro de intercambios:**

1. **Consulta:** se compartió la versión actualizada del diseño detallado de HU-01.A1 para revisar su coherencia con los requisitos, las decisiones previas del grupo y la arquitectura definida. Se pidió analizar los diagramas de robustez, las secuencias, el modelo de clases, las responsabilidades de los componentes y la correspondencia con los casos de prueba.
   **Generó:** observaciones sobre el flujo de registro con y sin coincidencias, la confirmación y cancelación de solicitudes pendientes, las responsabilidades de `EjecutorDeRegistro` y `GestorDeRegistro`, el manejo de excepciones, el almacenamiento de archivos y la integración con Google Docs.
   **Resultado:** se utilizaron las observaciones como puntos de revisión, sin aceptar automáticamente las propuestas. Se mantuvieron como referencia las decisiones ya establecidas por el grupo y las restricciones indicadas por el docente.

2. **Consulta:** se compartieron los archivos de pruebas correspondientes a los distintos módulos para revisar su correspondencia con los criterios de prueba y con el diseño actualizado.
   **Generó:** una revisión de las pruebas de carga de experimentos, detección de duplicados, entidades, gestión de excepciones, repositorio, servicio de consulta, ejecutor, gestor y técnicas. Se señalaron algunos aspectos cuya cobertura convenía comprobar con mayor precisión.
   **Resultado:** se identificaron puntos para revisar, entre ellos la comprobación de que los datos inválidos no lleguen a provocar una búsqueda de duplicados y la cobertura del manejo de errores. No se modificaron los tests en esta etapa.

3. **Consulta:** se volvió a proporcionar el contenido de los archivos `test_gestion_de_excepciones.py` y `test_entidades.py` para precisar qué verificaba cada uno.
   **Generó:** una nueva revisión de ambos archivos a partir del contenido compartido.
   **Resultado:** se confirmó que son archivos diferentes y que cubren responsabilidades distintas: `test_entidades.py` verifica la comparación de parámetros, el rechazo de estados de validez desconocidos y la búsqueda de parámetros; `test_gestion_de_excepciones.py` verifica la traducción de errores de validación, solicitudes no pendientes, errores de almacenamiento y errores previstos genéricos mediante `respuesta_para`.

4. **Consulta:** se pidió realizar una revisión integral del diseño antes de modificar código o pruebas, prestando especial atención a las contradicciones entre diagramas y responsabilidades.
   **Generó:** una lista de cuestiones para contrastar, entre ellas la relación entre el gestor y Google Docs, el guardado del enlace del documento, la compensación ante fallos de almacenamiento, la representación de los componentes en robustez y secuencias, la semántica de `similar_a`, los estados de preparación y las solicitudes pendientes.
   **Resultado:** se preparó una consigna para consolidar primero las decisiones de diseño y corregir la documentación. Se estableció que no debían introducirse abstracciones innecesarias ni darse por implementadas funcionalidades que todavía no se hubieran comprobado en el código.

**Qué se descartó y por qué:**
- Se descartaron las propuestas de agregar controladores para cada paso u operación del registro. La usuaria ya había aclarado reiteradamente que el diseño debía simplificarse y que el docente había cuestionado la cantidad de controladores de la propuesta anterior.
- Se descartaron las modificaciones que suponían agregar clases, interfaces o componentes sin una responsabilidad concreta que las justificara.
- No se aceptaron automáticamente las interpretaciones de la IA sobre decisiones que el grupo ya había definido o que la usuaria había corregido expresamente. Las propuestas debían respetar los requisitos, las decisiones previas y las observaciones del docente.
- No se modificaron el código ni los tests durante esta revisión. Se decidió priorizar la consolidación del diseño detallado antes de pasar a la implementación.
- No se consideró que una funcionalidad estuviera implementada por aparecer en un diagrama, en la documentación o en un caso de prueba. Era necesario comprobarlo en el código y, cuando correspondiera, ejecutar las pruebas.

**Errores o imprecisiones detectadas:**
- ChatGPT insistió en propuestas que no respetaban las restricciones de diseño indicadas por la usuaria. En más de una ocasión fue necesario reiterar que no debía crearse un controlador por cada operación, que la arquitectura debía simplificarse y que no se quería volver a una estructura con una cantidad excesiva de controladores.
- ChatGPT volvió a plantear supuestos sobre responsabilidades y componentes que la usuaria ya había aclarado o rechazado. La usuaria tuvo que corregir esas interpretaciones y señalar que debían tomarse en cuenta las decisiones establecidas en intercambios anteriores, en lugar de volver a proponer soluciones incompatibles con ellas.
- ChatGPT no siempre distinguió entre decisiones de diseño, funcionalidades proyectadas e implementación comprobada. Fue necesario insistir en que no se afirmara que algo estaba implementado sin haber revisado el código correspondiente.

# Uso de IA — TP4 (diseño detallado, implementación y pruebas de HU-01.A1)

**Herramienta:** Claude (Anthropic), en sesiones de chat y de código.

Qué se pidió, qué generó la IA y qué decidió el grupo. Si algo de lo escrito en "Resultado" no coincide con lo que recuerdan, corríjanlo: la consigna pide que refleje lo que realmente pasó.

## Registro de intercambios

1. **Consulta:** se pidieron opciones de estructura en capas para corregir el TP3.
   **Generó:** tres opciones (5 capas, 4 capas, aplicación-dominio-infraestructura) y recomendó 5 capas.
   **Resultado:** se descartó la recomendación. El profesor había indicado 4 capas (presentación, servicios, dominio, acceso a datos y servicios externos) y se aplicó eso.

2. **Consulta:** se pidió recomendar una HU para el TP4.
   **Generó:** recomendó HU-01.A1 con B1.1 como base, y HU-01.E1 como alternativa.
   **Resultado:** se eligió A1 y se dejó la conexión real con Google Docs fuera de alcance.

3. **Consulta:** se pidió aplicar el cambio de capas a `arquitectura.md`.
   **Generó:** redacción de los cambios en las secciones 5.2.2, 5.3, 5.5, 7 y DA-01.
   **Resultado:** se leyó y reviso el texto generado, se confirmo que el mismo no presentaba contradicciones y que representaba efectivamente lo pedido por el grupo.

4. **Consulta:** se pidió un primer diseño detallado de A1 (robustez, secuencias, clases).
   **Generó:** un `EjecutorRegistro` sin lógica, reglas de coincidencia dentro de `Experimento` y la clave de coincidencia en el plug-in.
   **Resultado:** se conservó la clave de coincidencia en la técnica. Se descartó delegar el filtrado en `Experimento` y se dejó en el detector, porque el repositorio no decide reglas (TP3, Tabla 6).

5. **Consulta:** se pidió unificar el diseño con la versión de Lucas y las revisiones del grupo, comprobadas por otra herramienta de IA.
   **Generó:** una versión con `PasoDeRegistro` (cuatro pasos), `Resultado`, `CoincidenciasSinConfirmar`, Google Docs simulado y una robustez con un controller por paso.
   **Resultado:** el grupo rechazó el diseño por ilegible: un controller por paso producía controllers obesos y secuencias largas. Se redujo a cinco controllers y se pidió rehacer las secuencias más cortas. Es un caso real de sugerencia de la IA descartada.

6. **Consulta:** se pidió implementar y probar.
   **Generó:** el código Flask, 66 pruebas (luego 75) y una revisión por mutación manual.
   **Resultado:** se comprobó la funcionalidad del código, buscando los casos de error, recorriendo los distintos caminos posibles. Se hallaron problemas en la resolución de distintos problemas, así como también con distintos pasos de la implementación, que no seguían lo específicado anteriormento por el grupo.

7. **Consulta:** se pidió un nuevo diagrama de clases y, luego, ajustar el flujo (solicitud pendiente, estados de preparación).
   **Generó:** `GestorDeRegistro` y `DetectorDeDuplicados` en lugar de los cuatro pasos, la solicitud pendiente en el ejecutor, `ResultadoPreparacion` en lugar de `CoincidenciasSinConfirmar`, `AlmacenamientoArchivos` y tres secuencias cortas. Adaptó código, pruebas y documento.
   **Resultado:** se aceptó el diseño. Se pidió mantener los cinco controllers y que el actor solo toque fronteras. Un diagrama de clases reducido que generó la IA había perdido atributos del SRS de `Experimento` (estado de análisis, objetivo, hardware, tiempo de procesamiento, hipótesis, notas) y la relación `CargaDeExperimentos → RegistroDeTecnicas`: se detectó en la revisión y se restauraron.

8. **Consulta:** se pidió una revisión integral del diseño (contradicciones, trazabilidad, revisión de pruebas), con la restricción de no modificar código ni pruebas.
   **Generó:** correcciones al documento y una lista de pendientes. Verificó el comportamiento real antes de documentarlo: reportó que la falla de Google Docs hoy produce un error 500 y no lo especificado (E1), y que una afirmación del pedido sobre archivos de prueba duplicados no era cierta.
   **Resultado:** el documento de diseño quedó como versión final salvo errores de consistencia. Los pendientes (E1, ramas, complejidad ciclomática, actualizar SRS y TP3) quedaron registrados y no se tapan.

9. **Consulta:** se pidió conectar Google Docs de verdad y qué hacía falta.
   **Generó:** una explicación de los pasos (proyecto de Google Cloud, APIs, credenciales), una guía detallada para configurarlo y la clase `ClienteGoogleDocsReal` (crea un documento vacío en una carpeta de Drive), activable con variables de entorno; por defecto sigue el cliente simulado. Primero recomendó una cuenta de servicio y, al revisar, se corrigió a sí misma: con una cuenta de Gmail común los archivos de una cuenta de servicio no tienen espacio propio en Drive, y propuso OAuth de aplicación de escritorio. Escribió pruebas con un Drive falso.
   **Resultado:** el grupo creó el proyecto y las credenciales, y lo probó a mano en su máquina, porque la IA no pudo probar la conexión contra Google. Se mantuvo como opcional; el manejo de la falla de Google Docs (E1) sigue sin implementar.

10. **Consulta:** se pidió trabajar sobre una rama alternativa.
   **Qué pasó:** la IA trabajó con una copia desactualizada: había clonado solo la rama `main` y no vio la rama `tp4-hu-01-a1`, que tenía el código, las pruebas y los documentos más recientes. El grupo se lo avisó. Después de avisarle, el grupo resolvió la diferencia por su cuenta y siguió con la versión de la rama.
   **Resultado:** error de la IA, no del grupo, detectado y corregido por el grupo. Por eso los documentos que se generaron antes de ese aviso (discurso, presentación y número de pruebas) conviene contrastarlos con el repositorio.


## Qué se descartó o se corrigió (y por qué)

- Cinco capas (propuesta de la IA): se descartó por indicación del profesor.
- Un controller de robustez por paso y `PasoDeRegistro`: se descartó por obeso e ilegible; quedaron cinco controllers.
- Coincidencias como excepción (`CoincidenciasSinConfirmar`): se reemplazó por un resultado de preparación, porque es un camino normal del negocio.
- Repetir el registro con una marca de confirmada (idea del TP3): se reemplazó por una solicitud pendiente en el ejecutor.
- Filtrado dentro de `Experimento`: se dejó en el detector.
- Atributos del SRS perdidos en un diagrama reducido: se restauraron.
- Cuenta de servicio para Google Docs (primera recomendación de la IA): se cambió a OAuth de escritorio por el problema de espacio en Drive con cuentas comunes.
- Trabajo sobre una copia desactualizada del repositorio (solo `main`): lo detectó el grupo y lo resolvió usando la rama `tp4-hu-01-a1`.
