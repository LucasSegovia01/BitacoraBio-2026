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

**Qué se descartó y por qué:**
- No se agregó un paso explícito de verificación de "proyecto existente"
  al flujo de CU-01 (propuesta de la IA en el punto 1): el grupo consideró
  que ya quedaba suficientemente claro en el paso 1 y en el alternativo A3.

**Errores o imprecisiones detectadas:** ninguno relevante en esta etapa —
las correcciones fueron ajustes de precisión y alcance, no errores de
contenido.