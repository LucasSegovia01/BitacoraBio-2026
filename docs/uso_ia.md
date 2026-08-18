# Bitácora de Uso de IA

**Herramienta utilizada:** Gemini (Google)

### 1. Tareas puntuales
Se utilizó la herramienta a lo largo de varias iteraciones para definir y acotar el proyecto del TP1. Las consultas principales fueron:
1.  **Brainstorming (15/08/26):** Evaluación de viabilidad entre un Motor de Evidencia Oncológica y una Bitácora de Experimentos Computacionales de Laboratorio, luego de presentarle ambas ideas y describir que era lo que se buscaba hacer con cada una.
2.  **Análisis de riesgos críticos (15/08/26):** Consulta específica sobre si existía algún peligro extremo o riesgo oculto al trabajar con la opción oncológica (enfocado al manejo de datos).
3.  **Priorización de alcance (16/08/26):** Consulta sobre si convenía enfocarnos en un ensayo específico (ej. Docking Molecular) o abarcar varios desde el inicio (trabajando con la bitácora).
4.  **Evaluación de ciclos de vida (18/08/26):** Pedimos que nos enumere los pros y contras de los modelos de ciclo de vida (cascada, incremental e iterativo) para poder fundamentar nuestra elección metodológica en el repositorio.
5.  **Sintaxis de diagramado (18/08/26):** Consultamos cómo estructurar visualmente un Diagrama de Contexto (DFD Nivel 0) usando el lenguaje Mermaid, ya que la herramienta no tiene soporte nativo para esto.

### 2. Qué generó la IA
*   **Sobre las ideas:** Recomendó la opción del catálogo de laboratorio, dado que no se estaba seguros de encontrar una fuente de información publica para realizar la otra opción.
*   **Sobre los riesgos críticos:** La IA fue tajante: el fallo de un software médico puede llevar a diagnósticos erróneos, tratamientos incorrectos y daños directos al paciente. También recomendó evitar esta idea ya que se debía tener en cuenta cosas como el manejo de datos sensibles (como los datos de un expediente medico). 
*   **Sobre los ensayos:** Recomendó empezar estrictamente por un solo ensayo (Docking) para evitar el "Desarrollo Acelerado", advirtiendo que el impulso por lanzar productos rápidamente lleva a la omisión de etapas críticas y a fallas graves.
* **Sobre los ciclos de vida (Modelo en Cascada):** detalló que este modelo es muy claro, cada fase tiene identificados los entregables y se revisa cada entregable. Explicó que posee una estructura simple del proceso que facilita la gestión y la planificación. También que la documentación está bien definida, lo que ayuda a la gestión y control del proyecto. En cuanto a las desventajas, mencionó que es muy rígido y es difícil de adecuarse a los cambios.
* **Sobre los ciclos de vida (Modelo Incremental):** La IA generó que una ventaja es la posibilidad de feedback de los clientes ya que se van mostrando y entregando partes funcionales, gracias a esto, inherentemente hay una visión de gestión de riesgo. Destacó que este enfoque permite ir mejorando la satisfacción del usuario al entregar cosas de valor desde etapas tempranas.
* **Sobre Mermaid:** Explicó que se debe usar el tipo de gráfico genérico `flowchart TD` y explicó cómo utilizarlo.

### 3. Modificaciones, decisiones y justificación
*   **Se descartó por completo** la idea del Motor Oncológico. La advertencia sobre el posible daño al paciente hizo notar que el rigor necesario para ese dominio excede los tiempos y objetivos de este trabajo práctico, así como también el conocimiento de los integrantes del grupo, generando cierta incertidumbre sobre la confianza tenida para el manejo de datos como los necesarios para el sistema.
*   **Se aceptó** la recomendación de ir por el Catálogo de Laboratorio y acotar el alcance inicial a un solo ensayo (Docking). Esto nos permite concentrarnos en la calidad de los requerimientos y no caer en la ausencia de pruebas, para que el incremento inicial sea estable y verificable.
* **Ciclos de Vida:** Basándonos en los pros y contras, descartamos el modelo en cascada por su rigidez. Decidimos adoptar el modelo iterativo e incremental para poder entregar nuestro MVP de Docking de manera temprana y adaptarnos a futuros cambios en el dominio.
* **Diagrama:** Se redactó el código mapeando nuestras propias entidades, siguiendo las instrucciones dadas por la IA.

### 4. Errores o imprecisiones detectadas en la IA
* En un inicio la IA utilizada sugirió que, para hacer el catálogo comercialmente mas llamativo, se incluyeran también módulos de Dinámica Molecular y otros tipos de ensayos para la primera entrega. Notamos que se ignoraba la restricción de tiempo y la cantidad de personas que formaban parte del equipo (2 personas). Aceptar eso hubiera empujado a un desarrollo acelerado, saltando fases cruciales para poder llegar a tiempo con las funcionalidades planteadas. Descartamos ese consejo y mantuvimos nuestro alcance acotado.
* Al pedirle ayuda con el código de Mermaid, la IA generó un ejemplo genérico que incluía un "almacén de datos" (una base de datos). Leyendo la teoría de la cátedra, detectamos que esto se trata de un error conceptual: los almacenes de datos no deben graficarse en un DFD de Nivel 0. Descartamos ese ejemplo por completo para no arrastrar el error al trabajo práctico.