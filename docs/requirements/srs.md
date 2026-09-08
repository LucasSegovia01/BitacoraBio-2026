# **Canvas de Descubrimiento**

### **Dominio y Problema**
En un grupo de investigacion pequeño (ej. un lab de facultad) que corre experimentos computacionales: docking molecular, MD, ensamblados genomicos. Los registros de lo que se probó, sus parámetros y los resultados queda disperso en diversas carpetas locales, con nombres de archivos poco descriptivos y comunicación informal entre pares. Hoy esto se resuelve (mal) con planillas sueltas o memoria de quien hizo cada cosa. Esto tiene como consecuencia que se suelen repetir ensayos ya hechos, y para revisar un resultado hay que descargar el archivo y abrir un programa para su visualización.

### **Datos**
Metadatos estructurados por experimento: tipo, parámetros de entrada, fecha, autor, hipótesis, resultado/estado. Para el MVP (docking), además el archivo de resultado en formato PDB (estructura de la pose obtenida) para el visor de solo lectura. Los datos son generados por los propios integrantes del grupo por lo que no dependen de ninguna fuente ni API externa para funcionar.

### **Usuarios y Stakeholders**
Investigador/estudiante: cargan experimentos nuevos, buscan si algo similar ya se probó antes de correrlo.
Director/responsable del grupo: consulta el historial completo para tener panorama del avance sin pedirle a cada integrante que le comente absolutamente todo.
No usuario directo pero interesado: la cátedra/docente, en tanto es quien evalúa el proyecto,no interactúa con el sistema en producción. 

### **Valor**
Si el sistema funciona, nadie repite un experimento ya realizado sin saberlo, no hace falta abrir software externo (VMD, PyMOL, etc) solo para mirar el resultado, y por ultimo, el proyecto queda consultable para cualquier duda y para un integrante que se suma al grupo posteriormente.

### **Alcance Realista**
*Adentro del sistema*
* Alta, consulta y filtro de experimentos de un solo tipo: docking.
* Campos: molécula/proteína, ligando, software usado, parámetros clave, sitio activo, autor, fecha, hipótesis, estado (éxito/fallido/en curso).
* campo de notas simple por experimento, de un solo autor por vez, dentro del propio sistema.
* Detección de posible duplicado (mismo tipo + misma molécula/ligando ya cargado antes).
* Visor 3D de solo lectura de la pose resultante (vía 3Dmol.js u otra librería equivalente), sin cálculo ni análisis adicional.
* Vínculo con Google Docs: crear/asociar un documento de notas por experimento.

*Afuera del sistema*
* Dinámica molecular y BLAST/ensamblados. --> Quedan como extensión futura, no en esta entrega.
* Reproducción de trayectorias completas de MD (múltiples frames). --> Solo pose estática.
* Cualquier análisis, cálculo o edición sobre los resultados dentro del sistema. --> Es visualización pura.
* Edición colaborativa en tiempo real de las notas dentro del sistema, eso vive en Google Docs, el sistema solo enlaza/crea.

### **Riesgos de Fracaso** 
El más probable en nuestro caso es el cambio de requerimientos. Si el modelo de datos de docking queda armado con columnas fijas muy específicas de esa técnica, agregar otra técnica después obliga a rehacer el esquema. 
* Mitigación: diseñar la tabla de "parámetros del experimento" como estructura extensible (ej. clave-valor o JSON) en vez de columnas rígidas por técnica, para que sumar dinámica molecular más adelante sea agregar filas de parámetros nuevos, no rediseñar la base.

### **Datos Sensibles**
Los metadatos de experimentos no son datos clínicos ni biológicos de una persona — son datos de investigación (moléculas, parámetros, resultados). El único dato mínimamente personal es el nombre del autor de cada experimento (miembro del propio grupo), que no cae dentro de las categorías que exige proteger el Código de Ética IEEE/ACM (no es dato de salud, no es identificable de un tercero ajeno al proyecto).


# **DFD nivel 0**

```mermaid
flowchart TD
    P((0<br/>Gestionar Catálogo<br/>de Experimentos))
    INV[Investigador / Becario]
    DIR[Director del Grupo]
    GDOCS[Google Docs]

    DIR -->|alta de usuario y asignación de rol| P
    P -->|confirmación de alta de usuario| DIR

    INV -->|alta de experimento, parámetros y archivo PDB| P
    P -->|confirmación de carga y vista 3D| INV
    INV -->|modificación de estado de validez/análisis| P
    P -->|confirmación de actualización de estado| INV
    INV -->|consulta y filtro de experimentos| P
    P -->|resultado de búsqueda| INV

    DIR -->|alta y baja de proyecto| P
    P -->|confirmación de gestión de proyecto| DIR
    DIR -->|eliminación de experimento| P
    P -->|confirmación de eliminación| DIR
    DIR -->|consulta y filtro de experimentos| P
    P -->|historial de experimentos| DIR

    P -->|metadatos del experimento| GDOCS
    GDOCS -->|enlace a la bitácora creada| P
```

# **Descompisición funcional (DFD nivel 1)**

```mermaid
flowchart TD
    INV[Investigador / Becario]
    DIR[Director del Grupo]
    GDOCS[Google Docs]

    P1((1<br/>Registrar<br/>Experimento))
    P2((2<br/>Consultar y<br/>Filtrar Experimentos))
    P3((3<br/>Detectar<br/>Duplicado))
    P4((4<br/>Visualizar<br/>Pose 3D))
    P5((5<br/>Vincular<br/>Documento de Notas))
    P6((6<br/>Gestionar<br/>Proyecto))
    P7((7<br/>Modificar Estado<br/>de Experimento))
    P8((8<br/>Eliminar<br/>Experimento))
    P9((9<br/>Registrar<br/>Usuario))

    D1[(D1 · Experimentos)]
    D2[(D2 · Proyectos)]
    D3[(D3 · Usuarios)]

    DIR -->|alta de usuario y rol| P9
    P9 -->|guarda| D3
    P9 -->|confirmación de alta| DIR

    INV -->|parámetros de docking y archivo PDB| P1
    P1 -->|consulta posible coincidencia| P3
    P3 -->|resultado de la verificación| P1
    P3 -->|lee| D1
    P1 -->|verifica proyecto existente| D2
    P1 -->|guarda| D1
    P1 -->|confirmación de carga| INV
    P1 -->|solicita creación de documento| P5
    P5 -->|metadatos del experimento| GDOCS
    GDOCS -->|enlace a la bitácora creada| P5
    P5 -->|link asociado| P1

    DIR -->|criterios de filtro y búsqueda| P2
    INV -->|criterios de filtro y búsqueda| P2
    P2 -->|lee| D1
    P2 -->|historial de experimentos| DIR
    P2 -->|resultado de búsqueda| INV

    INV -->|solicita ver pose| P4
    P4 -->|lee archivo de resultado| D1
    P4 -->|render 3D| INV

    DIR -->|alta o baja de proyecto| P6
    P6 -->|guarda / elimina| D2
    P6 -->|confirmación de gestión| DIR

    INV -->|nuevo estado de validez/análisis| P7
    P7 -->|actualiza| D1
    P7 -->|confirmación de actualización| INV

    DIR -->|eliminación de experimento| P8
    P8 -->|elimina| D1
    P8 -->|confirmación de eliminación| DIR
```

Los 16 flujos externos del Nivel 0 están todos presentes acá, repartidos entre los nueve procesos — regla de balanceo.


# **Modelo de Dominio Conceptual**

```mermaid
classDiagram
    class Usuario {
        <<Investigador o Director>>
    }
    class Proyecto
    class Experimento {
        <<estado_validez: invalido | finalizado | en_curso>>
        <<estado_analisis: pendiente | en_analisis | analizado>>
    }
    class ParametroExperimento
    class ArchivoResultado
    class DocumentoNotas

    Usuario "1" --> "*" Proyecto : crea (solo Director)
    Proyecto "1" --> "*" Experimento : agrupa
    Usuario "1" --> "*" Experimento : registra
    Experimento "1" --> "*" ParametroExperimento : tiene
    Experimento "1" --> "0..1" ArchivoResultado : produce
    Experimento "1" --> "0..1" DocumentoNotas : enlaza
```

# **Selección de proceso(s) a desarrollar en profundidad**

Se elige **Proceso 1 · Registrar Experimento** (incluyendo su interacción con el Proceso 3 · Detectar Duplicado). Tambien el **Proceso 2. Consulta y Filtro de experimentos**. Consideramos que estos procesos son la base para la visualización mínima de lo que el sistema busca hacer, mostrando el uso básico para el usuario investigador / becario, que será el tipo de usuario mas frecuente.

**Quedan fuera de profundización esta entrega:**
- Proceso 4 (Visualizar Pose 3D): la complejidad la resuelve una librería externa (3Dmol.js).
- Proceso 5 (Vincular Documento de Notas): acoplado al Proceso 1, se documenta como dependencia de su especificación.
- Proceso 6 (Gestionar Proyecto): CRUD simple sin reglas de negocio adicionales — se documenta a nivel de alcance (DFD + modelo de dominio), sin CU propio este cuatrimestre.
- Proceso 7 (Modificar Estado de Experimento): cambio de estado simple; queda como extensión natural de CU-01 a desarrollar en una iteración futura si el tiempo lo permite.
- Proceso 8 (Eliminar Experimento): operación de baja sin lógica compleja, análoga a Proceso 6.
- Proceso 9 (Registrar Usuario): alta simple con asignación de rol, sin reglas de negocio propias más allá de la validación de datos básicos — se documenta a nivel de alcance, sin CU propio este cuatrimestre.

# **Requerimientos funcionales**
## Requerimientos funcionales

RF-01: El sistema debe permitir a un usuario con rol Investigador/a registrar un experimento de docking dentro de un proyecto existente, con los campos: molécula/proteína, ligando, software usado, parámetros clave, sitio activo, hipótesis, notas (vacías por defecto) y estado.

RF-02: El sistema debe registrar automáticamente el autor, la fecha y la hora del experimento al momento de la carga, sin intervención manual del usuario.

RF-03: El sistema debe verificar, antes de confirmar el registro, si existe un experimento previo con el mismo tipo y la misma combinación molécula/ligando, excluyendo de esta verificación los experimentos marcados con estado de validez "inválido".

RF-04: El sistema debe alertar al usuario si detecta una posible coincidencia, mostrando el experimento existente, y permitirle decidir si continúa o cancela el registro.

RF-05: El sistema debe crear y asociar automáticamente un documento de Google Docs de notas al confirmarse el registro de un experimento.

RF-06: El sistema debe permitir consultar el detalle completo de un experimento (todos sus campos, parámetros, resultado principal, estado de validez, estado de análisis).

RF-07: El sistema debe permitir filtrar y buscar experimentos por fecha, autor y proyecto.


# **Stakeholders y roles**
## 2. Stakeholders y roles

| Rol | Tipo | Interacción con el sistema | Permisos |
|---|---|---|---|
| Investigador/a o becario/a | Usuario directo | Carga experimentos de docking, consulta el catálogo antes de correr un ensayo nuevo, visualiza poses 3D, agrega notas |Registra experimentos dentro de un proyecto existente; edita los campos de los experimentos que él/ella cargó; puede modificar el estado de validez (`invalido`/`finalizado`) de **cualquier** experimento del catálogo, no solo el propio; consulta y filtra sobre todo el catálogo. No puede crear ni eliminar proyectos ni experimentos.|
| Director/a del grupo | Usuario directo | Consulta el historial completo del grupo, filtra y busca sin necesidad de pedir el dato a cada integrante | Todo lo anterior, más: crea y elimina proyectos; elimina cualquier experimento del catálogo. |
| Cátedra/docente | Interesado, no usuario | Evalúa el proyecto en las instancias de presentación; no interactúa con el sistema en producción | No aplica — no opera el sistema |

**Nota sobre el diseño de permisos**: la distinción de roles entre investigador/a y director/a evita que la carga de un integrante sea modificada o eliminada por otro sin autorización, preservando la trazabilidad histórica que es el valor central del sistema. Ver bloque "Valor" en la sección 1.

# **CU-00 · Detectar Duplicado (incluido por CU-01)**
```
Actor principal: ninguno — CU de sistema, invocado internamente por CU-01
Realiza: RF-03
Precondición: se recibió el tipo de experimento y la combinación molécula/ligando a verificar.

Flujo:
  1. El sistema busca en el catálogo (D1) experimentos del mismo tipo y la misma combinación molécula/ligando.
  2. El sistema excluye de la búsqueda los experimentos con estado_validez = "inválido".
  3. El sistema retorna el resultado al llamador: "sin coincidencias" o "coincidencia encontrada" junto con el/los experimento(s) hallado(s).

Postcondición: el llamador (CU-01) recibe el resultado de la verificación;
  CU-00 no modifica ningún dato del catálogo.
```

# **CU-01 * Registrar Experimento de Docking (Proceso 1)**
```
Actor principal: Investigador/a
Actor secundario: Google Docs (sistema externo)
Realiza: RF-01, RF-02, RF-03, RF-04, RF-05
Incluye (<<include>>): CU-00 · Detectar Duplicado
  (se factoriza aparte porque es una verificación autocontenida que el flujo principal invoca pero no resuelve inline; mantiene CU-01 enfocado en el registro en sí. Compara tipo + molécula/ligando contra D1, excluyendo inválidos.)

Interesados e intereses:
  - Investigador/a: registrar su experimento rápido y saber si si ya se probó algo similar antes de perder tiempo repitiendo un ensayo.
  - Director/a del grupo: que el catálogo quede consistente y confiable como fuente única de verdad del historial del laboratorio.

Precondición: el/la investigador/a está autenticado/a con rol Investigador/a.
Disparador: el/la investigador/a finaliza un ensayo de docking (o quiere registrar uno en curso) y decide dejarlo asentado en el catálogo.
Garantía de éxito: el experimento queda registrado con autor y fecha asignados automáticamente, sin duplicar sin que el investigador/a lo supiera un ensayo ya existente, y con su documento de notas de Google Docs ya asociado.
Garantía mínima: el sistema nunca confirma un registro sin haber completado la verificación de duplicados, ni deja un experimento a medio guardar por falta de algún campo obligatorio.

Flujo principal:
  1. El/la investigador/a selecciona el proyecto existente y completa los campos del experimento: molécula/proteína, ligando, software usado, parámetros clave, sitio activo e hipótesis (las notas quedan vacías por defecto; define el estado inicial).
  2. El sistema verifica si existe un experimento previo del mismo tipo con la misma combinación molécula/ligando, excluyendo los marcados como inválidos <<include>> CU-00 · Detectar Duplicado.
  3. El sistema no encuentra coincidencias y continúa el registro.
  4. El sistema registra automáticamente el autor y la fecha/hora de carga.
  5. El sistema guarda el experimento en el catálogo.
  6. El sistema crea y asocia automáticamente un documento de Google Docs de notas para el experimento, y guarda el enlace devuelto.
  7. El sistema confirma el registro y muestra el resumen del experimento cargado, incluyendo el enlace a su documento de notas.

Flujos alternativos (nombrados):
  - A1: se detecta posible coincidencia y el/la investigador/a decide continuar el registro de todos modos (diverge en el paso 3, retoma en el paso 4).
  - A2: se detecta posible coincidencia y el/la investigador/a decide cancelar el registro (diverge en el paso 3, sin guardar nada).
  - A3: el proyecto seleccionado ya no existe al momento de confirmar (diverge en el paso 1).
  - A4: el/la investigador/a deja un campo obligatorio vacío (diverge en el paso 1).

Flujos de excepción (nombrados):
  - E1: falla la creación del documento de Google Docs, el servicio no responde (diverge en el paso 6; el experimento queda guardado sin bitácora asociada).
  - E2: se interrumpe la conexión durante el guardado del experimento (pasos 4-6).
```

## **Slices**
```
CU-01
  Slice B1 (básico) — pasos 1-7: completa datos, verifica duplicado (CU-00), registra autor/fecha, guarda el experimento, crea documento de notas y confirma con resumen y el enlace incluido.
  Slice A1 — continuar pese a coincidencia detectada   ——> nombrado, sin desarrollar
  Slice A2 — cancelar por coincidencia detectada       ——> nombrado, sin desarrollar
  Slice A3 — proyecto ya no existe                     ——> nombrado, sin desarrollar
  Slice A4 — campo obligatorio vacío                   ——> nombrado, sin desarrollar
  Slice E1 — falla en creación de documento de notas   ——> nombrado, sin desarrollar
  Slice E2 — conexión interrumpida durante el guardado ——> nombrado, sin desarrollar
  ```

## **Historias de usuario**
```
HU-01.B1 · Registrar experimento de docking
Deriva de: CU-01, slice B1 (básico)
Como investigador/a, quiero registrar un experimento de docking con sus parámetros y saber si ya se probó algo similar, para no repetir un ensayo sin saberlo y dejar el catálogo del grupo actualizado.

Criterios de aceptación:
- Given un proyecto existente, todos los campos obligatorios completos y sin coincidencias previas para esa molécula/ligando, 
When el investigador/a confirma el registro, 
Then el sistema guarda el experimento con autor y fecha asignados automáticamente, crea el documento de notas en Google Docs, y muestra el resumen del experimento con el enlace al documento.
- Given un experimento previo con la misma molécula/ligando pero marcado como estado_validez "inválido",
When el investigador/a confirma el registro,
Then el sistema NO lo reporta como coincidencia y completa el registro como en el camino normal.
  ```

## **CU-02 · Consultar y filtrar experimentos (Proceso 2)**
```
Actor principal: Usuario del sistema (generalización de Investigador/a y
  Director/a — ambos roles ejecutan este caso de uso de forma idéntica,
  sin distinción de permisos)
Realiza: RF-06, RF-07

Precondición: el usuario está autenticado, con rol Investigador/a o Director/a.
  Hay al menos un experimento cargado en el catálogo (postcondición de CU-01).
Disparador: el usuario necesita saber si un experimento ya fue realizado, o
  quiere revisar el historial del catálogo.

Flujo principal:
  1. El usuario selecciona uno o más criterios de filtro: fecha, autor o proyecto.
  2. El sistema busca los experimentos del catálogo que cumplen los criterios.
  3. El sistema muestra la lista de experimentos coincidentes, con sus datos
     principales (tipo, molécula/ligando, autor, fecha, estado).
  4. El usuario selecciona un experimento de la lista.
  5. El sistema muestra el detalle completo del experimento seleccionado.

Flujos alternativos: A1 no hay resultados que cumplan los criterios de
  búsqueda (diverge en el paso 2).

Sin flujos de excepción — a diferencia de CU-01, este proceso no depende de
  ningún servicio externo, por lo que no hay puntos de falla que documentar.
```

