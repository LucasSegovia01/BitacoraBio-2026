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
   criterio de división explícito (no solo "son dos tareas"), una historia
   de usuario para el flujo de excepción E1 (falla de Google Docs), y un
   slice adicional para formato de dato inválido.
   **Generó:** el criterio de división (valor central sin dependencias
   externas B1, vs. funcionalidad dependiente de un servicio externo B2),
   la HU-01.E1 con criterios Given/When/Then, y el slice A5 propuesto.
   **Resultado:** se aceptó el criterio de división B1/B2 y la HU-01.E1.

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

5. **Consulta:** se pidió una revisión de consistencia general del
   documento antes de la entrega, más la trazabilidad completa.
   **Generó:** detectó tres inconsistencias introducidas por ediciones
   sucesivas: RF-08 no figuraba en el "Realiza" de CU-01 pese a estar
   referenciado en el paso 2 del flujo; la historia de usuario HU-01.B1
   citaba una slice ("B1") que ya había sido dividida en B1.1/B1.2 en una
   edición posterior, sin actualizarse; y un encabezado duplicado con
   contenido de una versión anterior del bloque de Fiabilidad.
   **Resultado:** se corrigió el "Realiza" de CU-01; se decidió partir
   HU-01.B1 en HU-01.B1.1 y HU-01.B1.2 para que coincida con la división
   de slices ya adoptada; se eliminó el encabezado duplicado.

**Qué se descartó y por qué:**
- No se agregó un paso explícito de verificación de "proyecto existente"
  al flujo de CU-01 (propuesta de la IA en el punto 1): el grupo consideró
  que ya quedaba suficientemente claro en el paso 1 y en el alternativo A3.

**Errores o imprecisiones detectadas:** ninguno relevante en esta etapa —
las correcciones fueron ajustes de precisión y alcance, no errores de
contenido.

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