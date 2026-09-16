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