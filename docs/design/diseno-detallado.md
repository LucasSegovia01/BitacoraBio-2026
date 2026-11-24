# BitacoraBio 2026 — Diseño detallado, implementación y pruebas (HU-01.A1)

**Materia:** Ingeniería del Software 2026 (FIUNER) · **Trabajo práctico:** TP4 — Diseño detallado, implementación y testing unitario
**Integrantes:** Nuñez Juliana, Segovia Lucas

> **Versión unificada.** Parte de dos borradores del grupo (el de Juliana y el de Lucas). De cada uno se conservó lo que estaba mejor resuelto; las decisiones del grupo están marcadas en 5.1 y las diferencias con el TP3, en 8.2.

---

## 1. Introducción

### 1.1 Propósito

Este documento baja a diseño detallado, código y pruebas una historia de usuario (HU) del sistema, partiendo de la arquitectura del TP3 (`docs/architecture/arquitectura.md`). Se trabaja **una sola HU de punta a punta**: análisis en tres dimensiones, diagrama de robustez, diagramas de secuencia, modelo de clases, implementación con interfaz gráfica mínima y pruebas unitarias con reporte de cobertura.

### 1.2 HU elegida

**HU-01.A1 · Continuar registro pese a coincidencia detectada** (deriva de CU-01, slice A1).

> Como investigador/a, quiero poder registrar igual mi experimento aunque el sistema encuentre uno similar ya cargado, para dejar constancia de una repetición intencional (por ejemplo, replicar un resultado o validar con otro software).

Criterio de aceptación:

- *Given* una coincidencia detectada por CU-00 y mostrada al investigador/a, *When* elige continuar de todos modos, *Then* el sistema registra el experimento como uno nuevo (autor, fecha, documento de notas propio), sin sobrescribir ni vincular el experimento existente.

**Alcance.** HU-01.A1 se trabaja con **HU-01.B1.1 (registrar experimento) incluida por completo como base**: A1 solo existe como una variante del registro, de modo que el diseño cubre el camino sin coincidencias de B1.1 (con sus tres criterios), el corte por coincidencia (punto de partida de A1 y de E3) y la continuación de A1. Criterios de B1.1 que se incluyen:

1. Proyecto existente, campos obligatorios válidos y sin coincidencias: se registran autor y fecha/hora y se guarda el experimento.
2. Un experimento previo con la misma molécula/ligando pero "inválido" no se reporta como coincidencia.
3. Con los campos opcionales vacíos, el experimento se guarda sin exigirlos.

**Google Docs, simulado por defecto.** El criterio de A1 pide un *documento de notas propio*, así que la operación de vincular el documento (`GestorDeRegistro.vincular_documento`) **sí se diseña y se ejecuta**, usando una interfaz `ClienteGoogleDocs` con una implementación simulada (`ClienteGoogleDocsSimulado`: no se conecta a ningún servicio, devuelve un enlace ficticio y recuerda lo creado) y otra real y opcional (`ClienteGoogleDocsReal`, que crea en una carpeta de Drive un documento con formato —título y apartados predefinidos— y solo se usa si se definen las variables de entorno; se prueba a mano). Con eso el criterio de A1 se cumple completo. Quedan **fuera de alcance**: el reintento cuando falla el vínculo (`HU-01.E1`) y el resto de `HU-01.B1.2`.

### 1.3 Por qué esta HU

| Condición de la consigna | Cómo se cumple |
|---|---|
| Asociada a un escenario de calidad | `EC-07` (principal del TP3): el registro es donde cada técnica aporta lo propio, y A1 usa la clave de coincidencia que define cada técnica. También se relaciona con `EC-11` (varias coincidencias sin perder lo cargado) |
| Atraviesa la estructura | Recorre las cuatro capas: Carga de experimentos (presentación) → Ejecutor de registro (servicios) → Gestor de registro, Detector de duplicados, Registro de técnicas y Técnica Docking (dominio) → Repositorio de experimentos, Almacenamiento de archivos y Cliente de Google Docs (acceso a datos y servicios externos) |
| Una decisión de arquitectura la afecta | `DA-02` (microkernel en el registro), `DA-03` (parámetros nombre-valor-unidad) y `DA-01` (capas) citan sus componentes |

Además de cumplir la consigna, A1 es relevante para el proyecto: la detección de duplicados es la razón de ser de BitacoraBio (evitar que el laboratorio repita un ensayo sin saberlo) y A1 es la salida cuando la repetición es **intencional**. Es la HU donde se juntan la regla central del negocio (qué es una coincidencia), el microkernel (la clave de coincidencia la define la técnica) y una decisión de flujo difícil de resolver bien: cortar el registro, pedir una confirmación y retomarlo sin pedir de nuevo los datos.

### 1.4 Siglas

HU: historia de usuario · CU: caso de uso · EC: escenario de calidad · DA: decisión de arquitectura · RF: requerimiento funcional · GRASP: patrones generales para asignar responsabilidades · CP: caso de prueba · PDB: formato de archivo de estructura molecular · C4: modelo de documentación de arquitectura en cuatro niveles.

---

## 2. Relación con la arquitectura

### 2.1 Tabla de coherencia

| Dimensión | Contenido |
|---|---|
| Funcionalidad | `HU-01.A1`, que incluye `HU-01.B1.1` como base. Slice de `CU-01` (con `CU-00`). Caminos: registro sin coincidencias (B1.1); coincidencias que dejan el registro pendiente de confirmación; continuar de todos modos (A1) o cancelar; rechazo por datos inválidos; falla al guardar archivos (se revierte). Realiza `RF-01`, `RF-02`, `RF-03`, `RF-04` y `RF-08` |
| Estructura | Contenedor *Aplicación del catálogo* (Python/Flask). Estilo: cliente-servidor como base y microkernel en el registro. Patrón: capas relajadas (presentación, servicios, dominio, acceso a datos y servicios externos). Componentes: **Carga de experimentos** (presentación; en el TP3 se llama *Rutas de registro*); **Ejecutor de registro** (servicios); **Gestor de registro** (agrupa lo que el TP3 llamaba Validar datos, Guardar experimento y Vincular documento), **Detector de duplicados, Registro de técnicas y Técnica Docking** (dominio); **Repositorio de experimentos, Almacenamiento de archivos** (en el TP3, *Acceso a archivos*) **y Cliente de Google Docs** (acceso a datos y servicios externos); **Gestión de excepciones** (transversal). Componente principal: *Detector de duplicados*. Diferencias con el TP3 en 8.2 |
| Calidad | `EC-07`: agregar una técnica nueva sin modificar el núcleo ni columnas existentes. Tácticas: diferir el enlace (plug-ins) y parametrización (parámetros nombre-valor-unidad). Respaldo: `DA-02` y `DA-03` (con `DA-01`). También `EC-11` (varias coincidencias sin recargar lo cargado), que se resuelve conservando en el servidor la solicitud ya validada hasta que el investigador confirma o cancela |
| Dominio | `Experimento`, `ParametroExperimento`, `ArchivoResultado` y `DocumentoNotas` (se crean); `CapturaResultado` (si vienen, se guardan); `Proyecto` (se consulta su existencia) y `Usuario` (solo el autor). Ver 3.2 |
| Verificación | `CP-11`: se agrega una técnica de prueba (dinámica molecular) solo con registrarla; el registro, la detección con su clave y el guardado funcionan sin tocar el núcleo ni la entidad `Experimento` (medida de `DA-02` y de `EC-07`). `CP-05` y `CP-05b` para el criterio de A1 |

### 2.2 Estilo y patrones que rigen y cómo se respetan

| Restricción del TP3 | Cómo se respeta en el diseño |
|---|---|
| Capas: una capa no depende de las superiores; las flechas van hacia abajo | La carga de experimentos llama al servicio; el servicio, al dominio; el dominio, a las interfaces del acceso a datos. Ningún módulo importa uno de una capa superior |
| La capa de servicios no tiene lógica | `EjecutorDeRegistro` pide la técnica, crea la solicitud, llama al gestor y decide qué operación sigue según su resultado. No implementa validaciones, comparaciones ni persistencia |
| Microkernel: los plug-ins no se comunican entre sí ni modifican el núcleo | `TecnicaDocking` solo implementa la interfaz `Tecnica`; no conoce otros plug-ins ni el gestor |
| Microkernel: lo propio de la técnica está en el plug-in | Parámetros, validaciones propias y clave de coincidencia están en `TecnicaDocking`; el gestor y el detector las piden a través de la solicitud y no nombran ninguna técnica |
| Las operaciones del gestor no se llaman entre sí | Las llama `EjecutorDeRegistro` en el orden que corresponde; `GestorDeRegistro` no tiene un método que haga todo el registro |

---

## 3. Diseño de la HU

### 3.1 Enunciado y criterios

Ver 1.2. Los criterios de aceptación de B1.1 y de A1 son la fuente de los casos de prueba (sección 7). Tres caminos:

| Camino | Criterios | Resultado |
|---|---|---|
| **A.** Sin coincidencia (incluye el previo inválido y los opcionales vacíos) | B1.1 c1, c2, c3 | Se guarda el experimento y se crea su documento de notas |
| **B.** Con coincidencia | La parte "mostrada" de A1 | El registro se detiene antes de guardar, queda pendiente y se muestra la lista de coincidencias con "Realizar el registro de todas formas" o "Cancelar" |
| **C.** Con coincidencia, confirmada | A1 | Se guarda como experimento nuevo, con su propio documento de notas, **sin repetir la validación ni la búsqueda** |

Además: **D** (datos faltantes o inválidos) y **E** (falla al guardar los archivos), que son rechazos de B1.1. Si el investigador cancela, no se guarda nada y se descarta lo pendiente. El camino A se muestra en la **secuencia 1**, los B y C (con la cancelación) en la **secuencia 2** y los rechazos D y E en la **secuencia 3** (3.5).

### 3.2 Entidades del modelo de dominio que intervienen

Se marcaron los sustantivos de los criterios (proyecto, campos obligatorios, molécula/ligando, coincidencia, experimento previo, estado de validez, autor, fecha/hora, campos opcionales, capturas, documento de notas) y se buscaron en el modelo de dominio del TP1.

| Entidad del modelo (TP1) | ¿Interviene? | Qué usa la HU de ella | La HU la... | ¿Se dibuja? |
|---|---|---|---|---|
| `Experimento` | Sí | Tipo, autor, fecha de carga, estado de validez, campos opcionales, parámetros, "Similar a", rutas y enlace al documento | **Crea** (el nuevo) y **consulta** (los previos) | Sí |
| `ParametroExperimento` | Sí | Nombre, valor y unidad. La molécula/proteína y el ligando son parámetros (`DA-03`) y forman la clave de coincidencia del docking | Crea (los del nuevo) y consulta (los de los previos) | Sí |
| `ArchivoResultado` (la *estructura* PDB) | Sí | El PDB es obligatorio; se guarda en el almacén y el experimento conserva su ruta (`DA-04`) | Crea | Sí (robustez); en el código es la ruta guardada en `Experimento` (`ruta_pdb`) |
| `CapturaResultado` | Sí, de forma mínima | Las capturas son opcionales; si vienen se guardan igual que el PDB | Crea | Sí (robustez); en el código, rutas en `Experimento` (`rutas_capturas`). Con PostgreSQL (proyectado) irían en una tabla aparte relacionada por `experimento_id` |
| `DocumentoNotas` | Sí, simulado | El documento de notas propio de cada experimento (criterio de A1). Se guarda su enlace | Crea | Sí (robustez); en el código, el enlace en `Experimento` |
| `Proyecto` | Referencia | Solo su identificador: `GestorDeRegistro` comprueba que existe | Consulta la existencia; no lo modifica | No: no hay comportamiento que mostrar |
| `Usuario` | Referencia | Solo la identidad del autor (relación "registra"). La autenticación está fuera del desarrollo (RA-01): el sistema recibe el identificador del usuario identificado y lo guarda como autor | No lo consulta ni lo modifica | No: viaja como `autor` dentro de la solicitud, igual que el identificador de `Proyecto` |

**Por qué `Usuario` y `Proyecto` no aparecen como entidades en los diagramas.** Ninguna regla de esta HU necesita sus datos, solo sus identificadores. Dibujarlos como entidades sugeriría una interacción que no existe. `ArchivoResultado`, `CapturaResultado` y `DocumentoNotas` sí se dibujan en la robustez porque se crean, pero en el diagrama de clases no son clases propias: no tienen comportamiento en esta HU y el `Experimento` conserva solo su ruta o su enlace.

**Cambios y decisiones sobre el modelo.**

| Cambio o decisión | Motivo |
|---|---|
| `Experimento` tiene los atributos `tipo` y `fecha_de_carga` (cambio al modelo del TP1, ya agregado a `srs.md`) | `RF-02` y `RF-03` hablan de la fecha de carga y de comparar "el mismo tipo"; el modelo no los mostraba. El autor ya está en la relación `Usuario "registra" Experimento` |
| Molécula/proteína, ligando y software **no** son atributos de `Experimento`: son parámetros de la técnica | Es lo que dice `DA-03` y lo que permite que `EC-07` cumpla "0 columnas modificadas" |
| **"Similar a" se conserva en el dominio** (`Experimento.similar_a`, lista de identificadores) | Está en el formulario del TP1/TP2 y ahora también en el SRS (modelo de dominio y `RF-03`). Sirve para marcar réplicas: **un experimento declarado en "Similar a" no se cuenta como coincidencia**. No se vincula nada al continuar (A1 pide "sin vincular el existente"): el campo lo declara el usuario antes |

### 3.3 Análisis tridimensional

| Dimensión | Elemento | Detalle |
|---|---|---|
| Funcionalidad | B1.1 c1 | Con proyecto existente, campos válidos y sin coincidencias, registrar autor y fecha/hora y guardar el experimento (secuencia 1) |
| Funcionalidad | B1.1 c2 | Un experimento previo inválido no se reporta como coincidencia |
| Funcionalidad | B1.1 c3 | Los campos opcionales vacíos no impiden guardar |
| Funcionalidad | A1 (parte "mostrada") | Con coincidencia, no guardar nada, dejar la solicitud pendiente y mostrar los experimentos coincidentes (secuencia 2) |
| Funcionalidad | A1 | Con confirmación, guardar como nuevo, con su propio documento de notas, sin tocar el existente y sin repetir la validación ni la búsqueda; si cancela, no se guarda nada (secuencia 2) |
| Funcionalidad | Rechazos | Datos faltantes o inválidos: informar y no guardar. Falla al guardar archivos: revertir y no dejar un experimento a medias (secuencia 3) |
| Estructura | Frontera | `PantallaRegistro` (formulario), `PantallaCoincidencias` (tabla con "Realizar el registro de todas formas" y "Cancelar") y `ClienteGoogleDocs` (interfaz hacia el servicio externo, simulado) |
| Estructura | Control | Los cinco controllers de la robustez: `CargaDeExperimentos`, `GestionDeExcepciones`, `EjecutorDeRegistro` (coordina el proceso; el gestor y el detector concentran las operaciones), `RegistroDeTecnicas` (con el plug-in Docking) y `RepositorioDeExperimentos` (experimentos, estructuras y capturas) |
| Estructura | Dominio | `Experimento`, `ParametroExperimento`, las estructuras (PDB), las capturas y el documento de notas |
| Calidad | `EC-07` | La clave de coincidencia, las validaciones y los parámetros los define el plug-in: una técnica nueva no cambia el núcleo ni la entidad |
| Calidad | `EC-11` | Al continuar de todos modos no hay que volver a cargar ningún dato: el Ejecutor conserva la solicitud ya validada (con su PDB) hasta que se confirma o se cancela |

### 3.4 Diagrama de robustez

Leyenda: borde punteado = actor; rectángulo redondeado azul = boundary; círculo naranja = controller; rectángulo con barras verde = entity.

```mermaid
flowchart LR
    inv["Investigador/a<br/>(actor)"]
    pf(["«boundary»<br/>PantallaRegistro"])
    pc(["«boundary»<br/>PantallaCoincidencias"])
    cg(["«boundary»<br/>ClienteGoogleDocs"])
    ce(("«controller»<br/>CargaDeExperimentos"))
    gx(("«controller»<br/>GestionDeExcepciones"))
    er(("«controller»<br/>EjecutorDeRegistro"))
    rt(("«controller»<br/>RegistroDeTecnicas"))
    rx(("«controller»<br/>RepositorioDeExperimentos"))
    ex[["«entity»<br/>Experimento"]]
    pa[["«entity»<br/>ParametroExperimento"]]
    es[["«entity»<br/>Estructura<br/>(ArchivoResultado)"]]
    ca[["«entity»<br/>CapturaResultado"]]
    dn[["«entity»<br/>DocumentoNotas"]]
    inv --> pf
    inv --> pc
    pf --> ce
    pc --> ce
    ce --> er
    ce --> gx
    er --> rt
    er --> rx
    er --> cg
    er --> ex
    er --> pa
    er --> dn
    rx --> ex
    rx --> pa
    rx --> es
    rx --> ca
    classDef actor fill:#f3f4f6,stroke:#4b5563,color:#111827,stroke-dasharray: 4 3
    classDef boundary fill:#dbeafe,stroke:#1d4ed8,color:#0f172a
    classDef controller fill:#ffedd5,stroke:#c2410c,color:#0f172a
    classDef entity fill:#dcfce7,stroke:#15803d,color:#0f172a
    class inv actor
    class pf,pc,cg boundary
    class ce,gx,er,rt,rx controller
    class ex,pa,es,ca,dn entity
```

**Reglas de conexión.** El actor solo toca las pantallas; las pantallas solo tocan a `CargaDeExperimentos`; ninguna frontera toca una entidad; los controllers se coordinan entre sí y manipulan las entidades; el único acceso a un sistema externo (Google Docs) pasa por una frontera, `ClienteGoogleDocs`, a la que el proceso de registro llega a través de `GestorDeRegistro.vincular_documento`, que pide `EjecutorDeRegistro`. Este diagrama es de análisis y no dibuja al gestor: la flecha `EjecutorDeRegistro` → `ClienteGoogleDocs` representa ese paso, y en el diagrama de clases y en las secuencias la llamada la hace el gestor. Como es una frontera, no se conecta con `DocumentoNotas`: esa entidad la maneja el ejecutor. El repositorio se dibuja como controller, igual que en el ejemplo resuelto de la cátedra. Las entidades salen de la tabla 3.2. `SolicitudRegistro` no se dibuja: es el objeto de datos que viaja entre el ejecutor y el gestor (TP3, 5.2.2), no una frontera, un controlador ni una entidad del TP1; por eso no es participante de las secuencias y se ve en el diagrama de clases.

**Criterio de este diagrama: pocos controllers, cada uno con una responsabilidad principal.** El profesor indicó que con 8 controllers ya eran demasiados, y la referencia pide evitar controllers que concentren demasiado y también uno por cada paso. Quedan cinco, que representan las **responsabilidades principales** de la HU. Algunos **agrupan** responsabilidades que el diseño detallado delega en clases especializadas: agrupar en la robustez evita un controller por paso, pero **no elimina la separación de responsabilidades** del modelo de clases. Los cinco controllers no son uno por capa: el TP3 tiene cuatro capas más una responsabilidad transversal, y el reparto es otro (presentación → `CargaDeExperimentos`; servicios y las operaciones del dominio → `EjecutorDeRegistro`; microkernel de técnicas → `RegistroDeTecnicas`; acceso a datos → `RepositorioDeExperimentos`; transversal → `GestionDeExcepciones`). `GestionDeExcepciones` se mantiene por indicación del profesor.

| Controller | Responsabilidad principal | Clases del diseño detallado que lo componen | Capa del TP3 | Criterio GRASP |
|---|---|---|---|---|
| `CargaDeExperimentos` | Recibir el formulario y armar la respuesta | `CargaDeExperimentos` | Presentación | Controlador de entrada: traduce entre el usuario y el servicio, sin reglas |
| `GestionDeExcepciones` | Traducir los errores previstos en respuestas | `GestionDeExcepciones` | Transversal | Aspecto transversal (TP3, 5.4) |
| `EjecutorDeRegistro` | **Coordinar el proceso de registro** | `EjecutorDeRegistro` **coordina**: pide la técnica, crea la solicitud, llama al gestor, decide si continúa, espera una confirmación o termina y conserva la solicitud pendiente. Las operaciones concretas son de `GestorDeRegistro` (validar, guardar el experimento y sus archivos, vincular el documento), que usa a `DetectorDeDuplicados` para la búsqueda | Servicios (el coordinador) y dominio (el gestor y el detector) | Controlador: un solo punto de coordinación. Alta cohesión: el gestor agrupa operaciones relacionadas y delega la que tiene lógica propia |
| `RegistroDeTecnicas` | Entregar la técnica del tipo elegido | `RegistroDeTecnicas`, que administra al plug-in `TecnicaDocking` (el plug-in no es controller ni participante propio) | Dominio (microkernel) | Variaciones protegidas (`EC-07`) |
| `RepositorioDeExperimentos` | Guardar y recuperar lo que produce el registro | Dos interfaces separadas: `RepositorioExperimentos` (`proyectos`, `todos`, `existe_proyecto`, `existe_experimento`, `con_parametros`, `guardar`, `actualizar_rutas`, `eliminar`), única y compartida por el gestor y el detector, y `AlmacenamientoArchivos` (`guardar`, `eliminar_archivos`) | Acceso a datos | Bajo acoplamiento: el dominio no sabe cómo se guarda. Alta cohesión: solo guarda y recupera |

**Cómo se bajan los controllers agrupados a las secuencias.** La robustez se mantiene en el nivel de las responsabilidades principales (cinco controllers, por el límite que indicó el profesor). Las secuencias bajan un nivel y muestran la clase concreta que hace cada trabajo: `GestorDeRegistro` y `DetectorDeDuplicados` (que componen a `EjecutorDeRegistro`), `TecnicaDocking` (que administra `RegistroDeTecnicas`) y la entidad `Experimento`. Los mensajes hacia `RepositorioDeExperimentos` agrupan las operaciones de sus dos interfaces (`RepositorioExperimentos` y `AlmacenamientoArchivos`).

**Qué pasó con los controllers de la versión anterior.** Las clases `ValidarDatos`, `DetectarDuplicados`, `GuardarExperimento`, `VincularDocumento` y la interfaz `PasoDeRegistro` dejaron de existir: sus operaciones son ahora métodos de `GestorDeRegistro` (validar, guardar y vincular) y de `DetectorDeDuplicados` (buscar). `ClienteGoogleDocs` se reclasifica como boundary porque es la interfaz hacia un sistema externo.

**Regla "lo que no aparece en las secuencias no aparece en las clases".** Se cumple así: todas las clases con comportamiento propio de esta HU (`EjecutorDeRegistro`, `GestorDeRegistro`, `DetectorDeDuplicados`, `RegistroDeTecnicas`, `TecnicaDocking`, `Experimento` y las dos interfaces de acceso, agrupadas en `RepositorioDeExperimentos`) son participantes de al menos una secuencia. Lo que sigue agrupado solo es la robustez (sus controllers). Queda registrado en 4.1.

**Dónde vive cada regla de negocio.**

| Regla | Dónde vive | Por qué |
|---|---|---|
| Qué parámetros son obligatorios y su formato | `TecnicaDocking` los declara; `GestorDeRegistro.preparar` los aplica | Cambian con la técnica (`EC-07`) y aplicarlos es igual para todas. La pantalla no decide: solo muestra los errores |
| Qué identifica una coincidencia (en docking: mismo tipo, molécula/proteína y ligando) | `TecnicaDocking.clave_de_coincidencia(parametros)` | Es lo que cambia con un tipo de ensayo nuevo, y por eso el detector no se toca |
| Saber si un experimento coincide con un tipo y una clave | `Experimento.coincide_con(tipo, clave)` | Experto en información: el experimento tiene sus parámetros. Compara sin distinguir mayúsculas ni espacios |
| Un experimento inválido no cuenta como duplicado | `Experimento.es_candidato_a_duplicado()` | Depende solo del estado del propio experimento (`RF-03`) |
| Un experimento declarado en "Similar a" no cuenta como coincidencia | `SolicitudRegistro.declara_similar(experimento)` | Depende de la solicitud en curso, no del candidato |
| Buscar los candidatos con ese tipo y esa clave | `RepositorioExperimentos.con_parametros` | Recorre lo guardado y le pregunta a cada `Experimento`; no decide reglas |
| Una réplica no se informa si ya se informa su original | `Experimento.es_replica_de_alguno(otros)` | Experto en información: la relación está en el `similar_a` del propio experimento. Evita que, a gran escala, cada réplica sume una coincidencia más: se informa el original (`RF-03`) |
| Reunir las coincidencias | `DetectorDeDuplicados.buscar` | Pide la clave a la técnica, pide los candidatos y se queda con los que cuentan (las reglas anteriores); no escribe nada |
| Con coincidencias, el registro no se guarda hasta que el investigador confirme | `GestorDeRegistro.preparar` informa `REQUIERE_CONFIRMACION`; `EjecutorDeRegistro` decide detenerse y esperar | El gestor conoce el resultado de la validación y la detección; el ejecutor decide cómo sigue (`RF-04`) |
| La solicitud validada se conserva hasta confirmar o cancelar, y al confirmar no se repite nada | `EjecutorDeRegistro` | Es estado del proceso, no una regla del negocio; la solicitud es inmutable, así los datos no cambian entre la detección y la confirmación |
| Siempre se crea un experimento nuevo; nunca se toca el existente | `GestorDeRegistro.guardar_experimento` | No recibe ni modifica los experimentos de las coincidencias |
| Autor y fecha de carga se asignan solos | `GestorDeRegistro.guardar_experimento` | Construye el experimento (`RF-02`) |
| Cada experimento tiene su propio documento de notas | `GestorDeRegistro.vincular_documento` | Crea un documento por experimento, con apartados predefinidos, y nunca reutiliza el de otro |
| Si falla el guardado de archivos se revierte el experimento | `GestorDeRegistro.guardar_experimento` | Cierra la consistencia entre los dos almacenes (TP3, 5.6) |
| Qué operación sigue y en qué orden | `EjecutorDeRegistro` | Es una regla de servicio, no del negocio |

**Elemento → componente del TP3 → capa.**

| Elemento | Componente del TP3 | Capa |
|---|---|---|
| `PantallaRegistro`, `PantallaCoincidencias` | Rutas de registro (plantillas HTML) | Presentación |
| `CargaDeExperimentos` | Rutas de registro (renombrado, ver 8.2) | Presentación |
| `GestionDeExcepciones` | Gestión de excepciones | Transversal |
| `EjecutorDeRegistro` | Ejecutor de registro; Gestor de registro (reúne Validar datos, Guardar experimento y Vincular documento del TP3) y Detector de duplicados | Servicios y dominio (núcleo) |
| `RegistroDeTecnicas` | Registro de técnicas y Técnica Docking | Dominio (microkernel) |
| `RepositorioDeExperimentos` | Repositorio de experimentos y Almacenamiento de archivos (en el TP3, Acceso a archivos; ver 8.2) | Acceso a datos |
| `ClienteGoogleDocs` (boundary) | Cliente de Google Docs (simulado, o real si se configura) | Acceso a datos y servicios externos |
| `Experimento`, `ParametroExperimento`, estructuras, capturas, `DocumentoNotas` | Entidades del modelo de dominio (no son un componente del TP3) | Dominio |

### 3.5 Diagramas de secuencia

Se dibujan **tres secuencias cortas**: (1) registro sin coincidencias, (2) registro con coincidencias, con la cancelación y la confirmación (HU-01.A1) y (3) excepciones. Los participantes son los elementos del diagrama de robustez más el actor, y el actor solo interactúa con las pantallas. Los diagramas muestran **los mensajes clave entre participantes**, no el detalle interno de cada operación.

**Cómo se comporta el registro.** `EjecutorDeRegistro` recibe los datos y crea la solicitud, y pide a `GestorDeRegistro` que **prepare** el registro: validar los datos y buscar coincidencias con `DetectorDeDuplicados`. El gestor devuelve un resultado y el ejecutor decide:
- *Sin coincidencias* (`LISTO_PARA_GUARDAR`): el ejecutor sigue de inmediato con el guardado y la vinculación del documento. La pantalla se queda en el formulario y muestra debajo el aviso de que no hubo coincidencias y el experimento se registró. No hay pantalla intermedia.
- *Con coincidencias* (`REQUIERE_CONFIRMACION`): el ejecutor no guarda. Conserva la solicitud ya validada con un identificador y devuelve las coincidencias para que la presentación muestre la pantalla de coincidencias. Si el investigador confirma, el ejecutor recupera la solicitud y sigue con el guardado **sin repetir la validación ni la búsqueda**; si cancela, la descarta.
- *Datos inválidos*: la validación lanza `ErrorValidacion` y no se busca ni se guarda nada.

Encontrar coincidencias es un resultado normal del registro y no una excepción. Las excepciones se reservan para los rechazos: `ErrorValidacion`, `ErrorAlmacenamiento` y `SolicitudNoPendiente`.

**Convención.** `EjecutorDeRegistro` coordina el proceso y le pide el trabajo a `GestorDeRegistro`, que usa a `DetectorDeDuplicados`, a la técnica y a `Experimento`. Los mensajes hacia `RepositorioDeExperimentos` agrupan operaciones de sus dos interfaces del mismo momento (por ejemplo, guardar el experimento y sus archivos). Los participantes son los elementos de la robustez bajados a las clases que los componen (3.4).

**Qué se omite en los diagramas** (existe en el código y en el modelo de clases, sección 4):
- La creación de `SolicitudRegistro` (el DTO que lleva datos, autor y técnica).
- Las operaciones de la técnica que no cambian el flujo (`definiciones`, `parametros_resumen`).
- Las consultas de la validación al repositorio (`existe_proyecto`, `existe_experimento`).
- El detalle del guardado de archivos (una llamada por archivo) y de `actualizar_rutas`: se resumen en un mensaje de guardado.
- Las respuestas intermedias que no aportan.


**Secuencia 1. Registro sin coincidencias (HU-01.B1.1)**

```mermaid
sequenceDiagram
    actor Inv as Investigador/a
    participant PR as PantallaRegistro
    participant CE as CargaDeExperimentos
    participant E as EjecutorDeRegistro
    participant RT as RegistroDeTecnicas
    participant GR as GestorDeRegistro
    participant DD as DetectorDeDuplicados
    participant TD as TecnicaDocking
    participant RX as RepositorioDeExperimentos
    participant EX as Experimento
    participant CG as ClienteGoogleDocs
    Inv->>PR: confirmar()
    PR->>CE: registrar_experimento(formulario, pdb)
    CE->>E: registrar(datos, autor)
    E->>RT: tecnica(tipo)
    RT-->>E: TecnicaDocking
    E->>GR: preparar(solicitud)
    GR->>TD: validar(parametros)
    TD-->>GR: sin errores
    GR->>DD: buscar(solicitud)
    DD->>TD: clave_de_coincidencia(parametros)
    TD-->>DD: clave
    DD->>RX: con_parametros(tipo, clave)
    RX->>EX: coincide_con(tipo, clave)
    RX-->>DD: sin candidatos
    DD-->>GR: sin coincidencias
    GR-->>E: LISTO_PARA_GUARDAR
    E->>GR: guardar_experimento(solicitud)
    GR->>EX: crear (autor, fecha de carga y parámetros)
    GR->>RX: guardar el experimento y sus archivos
    RX-->>GR: experimento guardado
    GR-->>E: experimento
    E->>GR: vincular_documento(experimento, tecnica)
    GR->>CG: crear_documento(titulo, apartados)
    CG-->>GR: enlace
    GR->>RX: guardar el enlace
    E-->>CE: Resultado(registrado)
    CE-->>PR: mostrar(formulario con aviso)
    PR-->>Inv: debajo del formulario, aviso de que no hubo coincidencias y se registró
```

**Secuencia 2. Registro con coincidencias (HU-01.A1)**

```mermaid
sequenceDiagram
    actor Inv as Investigador/a
    participant PR as PantallaRegistro
    participant PC as PantallaCoincidencias
    participant CE as CargaDeExperimentos
    participant E as EjecutorDeRegistro
    participant GR as GestorDeRegistro
    participant DD as DetectorDeDuplicados
    participant RX as RepositorioDeExperimentos
    participant EX as Experimento
    participant CG as ClienteGoogleDocs
    Inv->>PR: confirmar()
    PR->>CE: registrar_experimento(formulario, pdb)
    CE->>E: registrar(datos, autor)
    E->>GR: preparar(solicitud)
    Note over GR,DD: valida y arma la clave con la técnica, como en la secuencia 1
    GR->>DD: buscar(solicitud)
    DD->>RX: con_parametros(tipo, clave)
    RX->>EX: coincide_con(tipo, clave)
    RX-->>DD: candidatos
    DD->>EX: es_candidato_a_duplicado()
    DD-->>GR: coincidencias
    GR-->>E: REQUIERE_CONFIRMACION
    E->>E: conserva la solicitud pendiente con un identificador
    E-->>CE: Resultado(no registrado, coincidencias, pendiente_id)
    CE-->>PC: mostrar(coincidencias, pendiente_id)
    PC-->>Inv: Realizar el registro de todas formas o Cancelar
    alt el investigador cancela
        Inv->>PC: cancelar()
        PC->>CE: cancelar_registro(pendiente_id)
        CE->>E: cancelar(pendiente_id)
        Note over E: descarta la solicitud pendiente
        CE-->>PR: mostrar(registro cancelado)
        PR-->>Inv: no se guardó ningún dato
    else el investigador confirma
        Inv->>PC: continuar()
        PC->>CE: continuar_pese_a_coincidencia(pendiente_id)
        CE->>E: confirmar(pendiente_id)
        Note over E: recupera la solicitud, no repite la validación ni la búsqueda
        E->>GR: guardar_experimento(solicitud)
        GR->>EX: crear (experimento nuevo, el existente no se toca)
        GR->>RX: guardar el experimento y sus archivos
        E->>GR: vincular_documento(experimento, tecnica)
        GR->>CG: crear_documento(titulo, apartados) propio
        GR->>RX: guardar el enlace
        E-->>CE: Resultado(registrado)
        CE-->>PR: mostrar(resultado)
        PR-->>Inv: experimento nuevo con su documento, el existente no se toca
    end
```

**Secuencia 3. Excepciones**

```mermaid
sequenceDiagram
    actor Inv as Investigador/a
    participant PR as PantallaRegistro
    participant CE as CargaDeExperimentos
    participant GX as GestionDeExcepciones
    participant E as EjecutorDeRegistro
    participant GR as GestorDeRegistro
    participant RX as RepositorioDeExperimentos
    Inv->>PR: confirmar()
    PR->>CE: registrar_experimento(formulario, pdb)
    CE->>E: registrar(datos, autor)
    E->>GR: preparar(solicitud)
    alt datos faltantes o inválidos
        GR--xE: ErrorValidacion(errores)
        E--xCE: ErrorValidacion
        CE->>GX: respuesta_para(error)
        GX-->>CE: mensajes de validación
        CE-->>PR: mostrar(formulario con errores)
        PR-->>Inv: errores informados, no se buscó ni se guardó nada
    else falla el almacenamiento
        E->>GR: guardar_experimento(solicitud)
        GR->>RX: guardar el experimento y sus archivos
        RX--xGR: falla el guardado
        GR->>RX: eliminar el experimento y sus archivos
        GR--xE: ErrorAlmacenamiento
        E--xCE: ErrorAlmacenamiento
        CE->>GX: respuesta_para(error)
        GX-->>CE: mensaje de falla
        CE-->>PR: mostrar(aviso)
        PR-->>Inv: el registro no pudo completarse, no queda nada a medias
    end
```

En la rama de falla de almacenamiento se asume que la validación y la detección ya pasaron (no se repiten en el diagrama); la misma falla puede ocurrir al confirmar una solicitud pendiente, con el mismo tratamiento (la solicitud pendiente se consume al confirmar, de modo que hay que cargar el formulario de nuevo). Confirmar una solicitud que ya no está pendiente (ya procesada, cancelada o inexistente) lanza `SolicitudNoPendiente`, que `GestionDeExcepciones` traduce igual que los demás errores. La reversión se resuelve con la compensación del diagrama (el gestor elimina el experimento y sus archivos). Cómo se cubre que falle la propia compensación queda como sacrificio ya declarado en el TP3 (5.6).

**Entidades.** `Experimento` es participante: lo crea el gestor y responde `coincide_con`, `es_candidato_a_duplicado` y `apartados_de_notas` (el contenido de su documento), que son reglas propias (no es una entidad anémica). `ParametroExperimento` forma parte del experimento y no tiene mensajes propios. `Estructura`, `CapturaResultado` y `DocumentoNotas` se representan por la ruta o el enlace que el almacenamiento y `ClienteGoogleDocs` devuelven: no tienen reglas en esta HU (ver 4). Es una diferencia con la referencia, registrada en 4.1.

**Asignación de responsabilidades (GRASP).** Se detalla por clase del diseño. `GestorDeRegistro` y `DetectorDeDuplicados` pertenecen al controller `EjecutorDeRegistro`; `TecnicaDocking`, a `RegistroDeTecnicas`; y `RepositorioExperimentos` y `AlmacenamientoArchivos`, a `RepositorioDeExperimentos`.

| Responsabilidad | Quién | Criterio |
|---|---|---|
| Recibir el formulario y armar la respuesta | `CargaDeExperimentos` | Controlador de entrada: traduce entre el usuario y el servicio; no decide reglas |
| Obtener la técnica, crear la solicitud, decidir cómo sigue y conservar lo pendiente | `EjecutorDeRegistro` | Controlador: coordina sin hacer el trabajo (bajo acoplamiento) |
| Entregar la técnica del tipo elegido | `RegistroDeTecnicas` | Variaciones protegidas: es el único que sabe qué técnicas existen |
| Declarar parámetros, reglas propias y clave de coincidencia | `TecnicaDocking` | Experto en información + variaciones protegidas (`EC-07`) |
| Validar los datos, guardar el experimento y sus archivos, vincular el documento | `GestorDeRegistro` | Alta cohesión: operaciones del registro que comparten los mismos colaboradores. Creador del `Experimento`. No decide el orden |
| Decidir si un experimento coincide con una clave y si puede contar como duplicado | `Experimento` | Experto en información: tiene los parámetros y el estado de validez. Evita una entidad anémica |
| Reunir las coincidencias de una solicitud | `DetectorDeDuplicados` | Alta cohesión: es todo lo que hace. No las muestra ni decide si el registro sigue |
| Traer los candidatos con un tipo y una clave | `RepositorioExperimentos` | Bajo acoplamiento: el dominio no sabe cómo se guarda; compartido por el gestor y el detector. Pregunta a cada `Experimento` si coincide |
| Guardar y eliminar archivos sin distinguir su tipo | `AlmacenamientoArchivos` | Variaciones protegidas: un formato o un almacén nuevo no cambia la interfaz |
| Crear el documento de notas | `ClienteGoogleDocs` | El servicio externo queda detrás de una interfaz |
| Traducir errores previstos en respuestas | `GestionDeExcepciones` | Aspecto transversal (TP3, 5.4) |

---

## 4. Modelo de clases

Un solo diagrama, organizado por capas del TP3 y contrastado con el código implementado (se extrajeron las clases y operaciones públicas del código y se compararon con este diagrama). Muestra lo **actual** (implementaciones `<<actual>>`, que existen en el código) separado de lo **proyectado** (`<<proyectada>>`, que no existe todavía). Las pantallas son plantillas HTML de la presentación y no son clases del modelo; en las secuencias participan como boundaries de la robustez. `CargaDeExperimentos` (módulo `carga_experimentos.py`, con funciones de Flask) se muestra como clase porque participa en las secuencias.

```mermaid
classDiagram
    namespace Presentacion {
        class CargaDeExperimentos {
            <<modulo>>
            +formulario()
            +registrar_experimento(formulario, pdb)
            +continuar_pese_a_coincidencia(pendiente_id)
            +cancelar_registro(pendiente_id)
        }
    }
    namespace Servicios {
        class EjecutorDeRegistro {
            -pendientes: dict
            +registrar(datos, autor) Resultado
            +confirmar(pendiente_id) Resultado
            +cancelar(pendiente_id)
        }
        class ServicioConsulta {
            +proyectos() tuple[]
            +experimentos() Experimento[]
            +resumen_de_proyectos() dict[]
            +experimento(id) Experimento
            +experimentos_de(proyecto_id) Experimento[]
            +contenido_pdb(experimento) str
            +de_autor(autor, estado) Experimento[]
            +buscar(texto, proyecto, autor, estado) Experimento[]
            +autores() str[]
        }
        class Resultado {
            +registrado: bool
            +experimento: Experimento
            +coincidencias: Experimento[]
            +pendiente_id: str
        }
    }
    namespace Dominio {
        class GestorDeRegistro {
            +preparar(solicitud) ResultadoPreparacion
            +guardar_experimento(solicitud) Experimento
            +vincular_documento(experimento, tecnica)
        }
        class ResultadoPreparacion {
            +estado: EstadoPreparacion
            +coincidencias: Experimento[]
        }
        class EstadoPreparacion {
            <<enumeration>>
            LISTO_PARA_GUARDAR
            REQUIERE_CONFIRMACION
        }
        class DetectorDeDuplicados {
            +buscar(solicitud) Experimento[]
        }
        class RegistroDeTecnicas {
            +registrar(tecnica)
            +tecnica(tipo) Tecnica
            +disponibles() Tecnica[]
        }
        class Tecnica {
            <<interface>>
            +definiciones() DefinicionDeParametro[]
            +validar(parametros) str[]
            +clave_de_coincidencia(parametros) dict
            +parametros_resumen() str[]
        }
        class TecnicaDocking
        class DefinicionDeParametro {
            +nombre
            +etiqueta
            +unidad
            +obligatorio: bool
            +max_largo: int
            +grupo: str
            +componentes: int
        }
        class DatosRegistro {
            +proyecto_id
            +tipo
            +fecha_realizacion
            +valores: dict
            +extras: tuple[]
            +hardware
            +tiempo_procesamiento
            +objetivo
            +hipotesis
            +notas
            +similar_a: str[]
            +estado_validez
            +pdb: bytes
            +capturas
        }
        class SolicitudRegistro {
            +datos: DatosRegistro
            +autor
            +tecnica: Tecnica
            +parametros() ParametroExperimento[]
            +declara_similar(experimento) bool
        }
        class Experimento {
            +id
            +proyecto_id
            +tipo
            +autor
            +fecha_de_carga
            +fecha_realizacion
            +estado_validez
            +similar_a: str[]
            +parametros: ParametroExperimento[]
            +ruta_pdb
            +rutas_capturas: str[]
            +documento_notas
            +valor_de(nombre) str
            +coincide_con(tipo, clave) bool
            +es_candidato_a_duplicado() bool
            +apartados_de_notas(etiquetas) list
            +es_replica_de_alguno(otros) bool
        }
        class ParametroExperimento {
            +nombre
            +valor
            +unidad
        }
        class RepositorioExperimentos {
            <<interface>>
            +proyectos() tuple[]
            +todos() Experimento[]
            +existe_proyecto(id) bool
            +existe_experimento(id) bool
            +con_parametros(tipo, clave) Experimento[]
            +guardar(experimento) str
            +actualizar_rutas(experimento)
            +eliminar(id)
        }
        class AlmacenamientoArchivos {
            <<interface>>
            +guardar(experimento_id, nombre, contenido) str
            +leer(ruta) bytes
            +eliminar_archivos(experimento_id)
        }
        class ClienteGoogleDocs {
            <<interface>>
            +crear_documento(titulo, apartados) str
        }
    }
    namespace AccesoADatos {
        class RepositorioExperimentosEnMemoria {
            <<actual>>
        }
        class RepositorioExperimentosSQLite {
            <<actual>>
        }
        class RepositorioExperimentosPostgreSQL {
            <<proyectada>>
        }
        class AlmacenamientoArchivosEnMemoria {
            <<actual>>
        }
        class AlmacenamientoArchivosLocal {
            <<proyectada>>
        }
        class ClienteGoogleDocsSimulado {
            <<actual>>
        }
        class ClienteGoogleDocsReal {
            <<actual, opcional>>
        }
    }
    namespace Transversal {
        class GestionDeExcepciones {
            <<modulo>>
            +respuesta_para(error) dict
        }
        class ErrorPrevisto {
            <<excepcion>>
        }
        class ErrorValidacion {
            +errores: str[]
        }
        class ErrorAlmacenamiento {
            +detalle
        }
        class SolicitudNoPendiente
    }
    CargaDeExperimentos --> EjecutorDeRegistro
    CargaDeExperimentos ..> ServicioConsulta : arma el formulario y las pantallas de consulta
    ServicioConsulta ..> RepositorioExperimentos : usa
    CargaDeExperimentos ..> GestionDeExcepciones
    CargaDeExperimentos ..> DatosRegistro : arma
    EjecutorDeRegistro --> RegistroDeTecnicas
    EjecutorDeRegistro --> GestorDeRegistro
    EjecutorDeRegistro ..> SolicitudRegistro : crea
    EjecutorDeRegistro ..> Resultado : devuelve
    EjecutorDeRegistro ..> SolicitudNoPendiente : lanza
    GestorDeRegistro --> DetectorDeDuplicados
    GestorDeRegistro --> RepositorioExperimentos
    GestorDeRegistro --> AlmacenamientoArchivos
    ServicioConsulta ..> AlmacenamientoArchivos : lee el PDB para el visor
    GestorDeRegistro --> ClienteGoogleDocs
    GestorDeRegistro ..> Tecnica : pide reglas
    GestorDeRegistro ..> Experimento : crea
    GestorDeRegistro ..> ResultadoPreparacion : devuelve
    GestorDeRegistro ..> ErrorValidacion : lanza
    GestorDeRegistro ..> ErrorAlmacenamiento : lanza
    DetectorDeDuplicados --> RepositorioExperimentos
    DetectorDeDuplicados ..> Tecnica : pide la clave
    DetectorDeDuplicados ..> Experimento : pregunta
    RepositorioExperimentos ..> Experimento : devuelve
    SolicitudRegistro ..> ParametroExperimento : arma
    ResultadoPreparacion --> EstadoPreparacion
    RegistroDeTecnicas "1" --> "*" Tecnica
    TecnicaDocking ..|> Tecnica
    Tecnica ..> DefinicionDeParametro
    SolicitudRegistro --> DatosRegistro
    SolicitudRegistro --> Tecnica
    Experimento "1" --> "*" ParametroExperimento
    RepositorioExperimentosEnMemoria ..|> RepositorioExperimentos
    RepositorioExperimentosSQLite ..|> RepositorioExperimentos
    RepositorioExperimentosPostgreSQL ..|> RepositorioExperimentos
    AlmacenamientoArchivosEnMemoria ..|> AlmacenamientoArchivos
    AlmacenamientoArchivosLocal ..|> AlmacenamientoArchivos
    ClienteGoogleDocsSimulado ..|> ClienteGoogleDocs
    ClienteGoogleDocsReal ..|> ClienteGoogleDocs
    ErrorValidacion --|> ErrorPrevisto
    ErrorAlmacenamiento --|> ErrorPrevisto
    SolicitudNoPendiente --|> ErrorPrevisto
    GestionDeExcepciones ..> ErrorPrevisto
```

**Lo actual y lo proyectado.** Hoy existen `RepositorioExperimentosEnMemoria` (por defecto), `RepositorioExperimentosSQLite` (opcional, con `python run.py --db`), `AlmacenamientoArchivosEnMemoria`, `ClienteGoogleDocsSimulado` (por defecto) y `ClienteGoogleDocsReal` (opcional, con `BITACORABIO_GOOGLE_CREDENCIALES`). `RepositorioExperimentosPostgreSQL` (metadatos y rutas, con las capturas en una tabla aparte relacionada por `experimento_id`) y `AlmacenamientoArchivosLocal` (archivos en el sistema de archivos) están previstas y **no están implementadas**.

**Dónde están los puertos.** `RepositorioExperimentos`, `AlmacenamientoArchivos` y `ClienteGoogleDocs` son interfaces que define el dominio (`dominio/puertos.py`): el gestor y el detector dependen de ellas y el acceso a datos las implementa. Por eso están en el namespace `Dominio` del diagrama y sus implementaciones, en `AccesoADatos`. Es la inversión de dependencias de 2.2: el dominio no conoce al acceso a datos.

**Lo que se dejó afuera a propósito:** `Usuario` y `Proyecto` (solo viajan como identificadores), las entidades `ArchivoResultado`, `CapturaResultado` y `DocumentoNotas` como clases (el `Experimento` conserva sus rutas y su enlace), las pantallas y un patrón formal para la cadena de operaciones (alcanza con que `EjecutorDeRegistro` llame a las del gestor).

### 4.1 Validación del diagrama de clases contra la robustez y las secuencias

La consigna pide contrastar el diagrama con el diseño y anotar cada diferencia con su resolución.

| Diferencia encontrada | Qué estaba mal | Qué se hizo |
|---|---|---|
| `GestorDeRegistro`, `DetectorDeDuplicados` y `TecnicaDocking` eran clases y no participantes de las secuencias; `Experimento` tampoco lo era | La referencia dice que lo que no aparece en las secuencias no aparece en las clases | **Resuelto:** las tres secuencias muestran ahora a `RegistroDeTecnicas`, `GestorDeRegistro`, `DetectorDeDuplicados`, `TecnicaDocking` y `Experimento` como participantes. La robustez sigue con cinco controllers (límite del profesor) y las secuencias bajan un nivel (3.4) |
| `Experimento` solo guardaba datos (entidad anémica) y las reglas de coincidencia estaban en el repositorio y en el detector | La consigna pide entidades con comportamiento | **Resuelto:** `coincide_con` y `es_candidato_a_duplicado` pasaron a `Experimento`; "Similar a" queda en `SolicitudRegistro.declara_similar` porque depende de la solicitud |
| Los puertos (`RepositorioExperimentos`, `AlmacenamientoArchivos`, `ClienteGoogleDocs`) figuraban en el namespace de acceso a datos y en el código están en `dominio/puertos.py` | El diagrama no coincidía con el código ni con la inversión de dependencias | **Resuelto:** los puertos se dibujan en `Dominio` y las implementaciones en `AccesoADatos` |
| La presentación importaba `ParametroExperimento` y `ServicioConsulta` dependía del repositorio concreto | Capas relajadas: la presentación no debe usar entidades, y los servicios, los puertos | **Resuelto:** `DatosRegistro.extras` pasó a ser una lista de tuplas `(nombre, valor, unidad)` y `ServicioConsulta` usa el puerto (con `proyectos` y `todos`) |
| `Tecnica.parametros_resumen` está en el código y no lo llama ninguna operación de esta HU | Es parte del plug-in del TP3 (resumen del experimento en listados) | Se agregó al diagrama; queda para la consulta (fuera de alcance) y solo tiene prueba propia |
| `RepositorioExperimentos` y `AlmacenamientoArchivos` son interfaces separadas pero un solo controller en robustez | Solo la agrupación de la robustez | Las secuencias agrupan sus mensajes hacia el controller. Las operaciones de archivos (`guardar`, `eliminar_archivos`) son de `AlmacenamientoArchivos` y las de experimentos (incluidas `actualizar_rutas` y `eliminar`) son de `RepositorioExperimentos` |
| `existe_proyecto`, `existe_experimento` y el guardado archivo por archivo están en el código y en las clases, pero no en las secuencias | No es un error: son detalle interno | Se omiten de las secuencias, que muestran solo los mensajes clave (3.5) |
| `Estructura`, `CapturaResultado` y `DocumentoNotas` son entidades en la robustez y no son clases del código | No tienen reglas ni comportamiento en esta HU: son una ruta o un enlace dentro de `Experimento` | Se dejan como atributos. **A confirmar con el grupo:** mantenerlas en la robustez (modelo del TP1) o sacarlas |
| `PantallaRegistro` y `PantallaCoincidencias` participan en las secuencias pero no son clases del diagrama | Son plantillas HTML, no clases | Se quitaron del modelo de clases; siguen como boundaries de la robustez. Las rutas del código se llaman como en las secuencias (`registrar_experimento`, `continuar_pese_a_coincidencia`, `cancelar_registro`) |
| La solicitud pendiente vive en un diccionario de `EjecutorDeRegistro` y no hay una clase `RegistroPendiente` | Una clase solo con un identificador y una solicitud no aporta | Se conserva el mecanismo en memoria dentro del ejecutor. Con varios procesos del servidor o reinicios se perdería: queda como limitación (7 y 8.2) |
| `Resultado` ahora distingue "registrado" de "requiere confirmación" y `ResultadoPreparacion` es un resultado del dominio | Antes `registrado` era siempre verdadero | El dominio no puede depender de `Resultado` (está en servicios); por eso el gestor devuelve su propio resultado y el ejecutor arma el suyo |
| Los datos inválidos son una excepción (`ErrorValidacion`) y no un estado más del resultado de preparación | El enunciado pensaba tres estados | Son un rechazo y no un camino que continúe o espere; así se conserva `GestionDeExcepciones` para los rechazos. **A confirmar con el grupo** |
| `ErrorPrevisto` está en el diagrama; `CoincidenciasSinConfirmar` se eliminó | Encontrar coincidencias es un resultado normal | Se reemplazó por el estado `REQUIERE_CONFIRMACION`. Se agregó `SolicitudNoPendiente` para confirmar algo que ya no está pendiente |
| `ServicioConsulta` estaba en el código y no en el diagrama | La consigna pide que el diagrama salga del código | **Resuelto:** se agregó al diagrama. No figura en las secuencias porque solo lee (listas del formulario, y las pantallas de proyectos, experimentos, detalle y búsqueda, que no son parte de HU-01.A1) y no participa de la HU; depende del puerto `RepositorioExperimentos` |
| `CargaDeExperimentos` y `GestionDeExcepciones` figuran como clases y en el código son módulos de funciones (en Flask, un controlador web es una función de ruta) | La consigna dice que cada participante es una clase y cada mensaje, una operación | **Se mantiene, con el estereotipo `<<modulo>>` en el diagrama.** Cada mensaje de la secuencia es una función con el mismo nombre (`registrar_experimento`, `continuar_pese_a_coincidencia`, `cancelar_registro`) y el rol es el mismo que el de un controlador de la robustez. Justificación: Flask registra las rutas como funciones con decoradores, y `respuesta_para` no tiene estado, así que envolverlas en una clase sin atributos agregaría una clase que no aporta responsabilidad (la consigna advierte contra diseños con más clases de las necesarias) y no cambiaría las dependencias ni los mensajes. Si hiciera falta, se pasan a clases sin tocar el resto del diseño |

---

## 5. Justificación del diseño

### 5.1 Responsabilidades y decisiones

| Decisión | Por qué | Costo |
|---|---|---|
| **La técnica arma la clave de coincidencia:** `Tecnica.clave_de_coincidencia(parametros)` devuelve un diccionario nombre → valor | Se comparó con la alternativa de que la técnica solo devolviera los *nombres* y la solicitud armara el diccionario. Se eligió la primera: la regla completa queda en el plug-in (`EC-07`), `SolicitudRegistro` sigue siendo un portador de datos sin reglas, `DetectorDeDuplicados` no nombra "proteína" ni "ligando", y la clave se prueba sola | La técnica recibe los parámetros ya armados en cada llamada |
| **Las reglas de un experimento viven en `Experimento`; las de la solicitud, en la solicitud; el detector las combina.** `Experimento.coincide_con(tipo, clave)` y `Experimento.es_candidato_a_duplicado()` son de la entidad; `SolicitudRegistro.declara_similar(e)`, de la solicitud. El repositorio recorre lo guardado y pregunta a cada experimento (`con_parametros`); el detector se queda con los que cuentan | La entidad deja de ser anémica (la consigna lo pide) y el acceso a datos no decide reglas (Tabla 6 del TP3). "Similar a" no va en la entidad porque depende de la solicitud en curso, no del candidato | El detector sigue dependiendo de dos objetos (candidato y solicitud). El repositorio en memoria llama a un método de la entidad; un repositorio SQL tendría que traducir la clave a una consulta y confirmar con la entidad |
| `Tecnica` es una interfaz con `definiciones()` y `validar(parametros)` | `GestorDeRegistro` aplica obligatoriedad y formato a partir de las definiciones (un solo lugar para todas las técnicas) y la técnica aporta solo sus reglas propias. Evita duplicar la obligatoriedad | Dos operaciones donde una "validar" podría hacerlo todo |
| **`GestorDeRegistro` reúne validar, guardar y vincular, y `EjecutorDeRegistro` decide el orden.** El gestor no tiene un método que haga todo el registro | Se evitan tres clases pequeñas con los mismos colaboradores y se evita que el gestor sea otro ejecutor. La división es: el ejecutor decide *qué sigue*, el gestor *hace* cada operación | El gestor tiene cuatro colaboradores; se acepta porque son cohesivos y la búsqueda de duplicados, que tiene lógica propia, está aparte |
| **`DetectorDeDuplicados` es una clase aparte** | Tiene lógica propia (clave, consulta y filtros) y se prueba sola. Solo devuelve coincidencias: no decide si el registro sigue | Una clase más que si fuera un método del gestor |
| **Encontrar coincidencias es un resultado, no una excepción:** `preparar` devuelve `LISTO_PARA_GUARDAR` o `REQUIERE_CONFIRMACION` | Es un camino normal del negocio. El ejecutor decide si continúa, espera o termina sin que el flujo se corte con una excepción | Dos clases de resultado (`ResultadoPreparacion` en el dominio y `Resultado` en servicios), porque el dominio no puede depender de la capa de servicios |
| **Los datos inválidos siguen siendo una excepción** (`ErrorValidacion`) | Es un rechazo de la entrada, no una situación que continúe o espere; mantiene los rechazos en `GestionDeExcepciones` | El enunciado habla de tres estados (el tercero, `DATOS_INVALIDOS`); queda a confirmar con el grupo |
| **La solicitud validada queda pendiente en el ejecutor** con un identificador, y al confirmar no se repite nada | El servidor recibe dos pedidos distintos. La solicitud es inmutable (los datos no cambian entre la detección y la confirmación) y no se agregan atributos permanentes a `SolicitudRegistro`. Cumple `EC-11` sin reenviar el PDB | El estado vive en memoria del proceso: no sobrevive a un reinicio ni a varios servidores. Se consume al confirmar: si el guardado falla hay que cargar de nuevo |
| **Mecanismo de la solicitud pendiente: un diccionario en el ejecutor y no una clase `RegistroPendiente` ni la sesión de Flask** | La solicitud incluye el PDB y las capturas, que no entran en una cookie de sesión; y una clase solo para guardar un identificador y una solicitud no aporta | Si la aplicación creciera se reemplazaría por un almacenamiento temporal compartido |
| **`SolicitudRegistro` es un DTO inmutable y reducido:** datos, autor y técnica | Ya no lleva `confirmada`, `coincidencias` ni `experimento`: los devuelven las operaciones | — |
| **`AlmacenamientoArchivos` con `guardar(experimento_id, nombre, contenido)`, `leer(ruta)` y `eliminar_archivos`** | El gestor no conoce el almacén y no hay una operación por tipo de archivo; un formato nuevo no cambia la interfaz. La presentación ya separa el PDB de las capturas, y el gestor asigna cada ruta a `ruta_pdb` o a `rutas_capturas` | El nombre del PDB (`estructura.pdb`) es una constante del gestor |
| Una única interfaz `RepositorioExperimentos`, compartida por el gestor y el detector | No hay una responsabilidad que justifique separarla ahora | Habría que dividirla si creciera |
| Las interfaces `RepositorioExperimentos`, `AlmacenamientoArchivos` y `ClienteGoogleDocs` | Se cambian la persistencia, el almacén o el servicio externo sin tocar el dominio; las pruebas usan versiones en memoria y un doble que falla. Google Docs queda simulado sin cambiar el diseño | El repositorio tiene dos implementaciones actuales (memoria y SQLite); las otras interfaces, una. Se justifican por el cambio previsto a PostgreSQL y al sistema de archivos, por la conexión real a Google Docs y por las pruebas |
| `guardar_experimento` guarda el experimento y después los archivos, y revierte si falla | Los dos almacenes no comparten transacción (TP3, 5.6) | Si falla el propio `eliminar`, queda un residuo; se acepta para el alcance |
| `vincular_documento` va después de guardar | El documento necesita el id del experimento. Si el vínculo falla, el experimento ya existe (es el escenario `E1`, fuera de alcance) | El reintento no está implementado |

### 5.2 Patrones de diseño usados

No se usaron patrones por obligación. Aparecen dos por el problema concreto que resuelven:

| Patrón | Problema que resuelve | Dónde está |
|---|---|---|
| Strategy (la interfaz `Tecnica` con sus implementaciones) | Variar parámetros, validaciones y clave de coincidencia según el tipo de ensayo sin condicionales en el núcleo (`EC-07`) | `Tecnica`, `TecnicaDocking` y `RegistroDeTecnicas` |
| Repository (`RepositorioExperimentos`) | Que el dominio no conozca cómo se guardan los datos | `RepositorioExperimentos` y sus implementaciones en memoria y SQLite |

No se usó Factory para elegir la técnica: un diccionario en `RegistroDeTecnicas` alcanza.

---

## 6. Implementación

### 6.1 Estructura del código

```text
src/
├── dominio/          # entidades, solicitud, GestorDeRegistro, DetectorDeDuplicados, técnica (interfaz y plug-in Docking), Registro de técnicas, puertos
├── servicios/        # EjecutorDeRegistro y Resultado (y ServicioConsulta, apoyo de la interfaz)
├── acceso_datos/     # repositorio, almacenamiento de archivos y Google Docs: implementaciones en memoria, SQLite (repositorio) y simuladas
├── presentacion/     # CargaDeExperimentos (rutas de Flask) y plantillas HTML
├── transversal/      # Gestión de excepciones
└── arranque.py       # único lugar que arma los objetos concretos
tests/
```

Las cuatro capas del TP3 se ven como carpetas. Las dependencias van en un solo sentido: presentación → servicios → dominio; el acceso a datos implementa los puertos del dominio y solo usa sus entidades. La presentación solo usa del dominio los datos del formulario (`DatosRegistro`) y el registro de técnicas, que es el salto justificado del TP3; no importa entidades. Se verificó leyendo los `import` de `src/`.

### 6.2 Cómo se ejecuta

Las instrucciones completas están en el `README.md`: instalar con `pip install -r requirements.txt`, abrir la interfaz con `python run.py` (en `http://localhost:5000/registro`) y correr las pruebas con `pytest`.

### 6.3 Cómo se reemplazan la persistencia y los servicios externos

- **Persistencia:** por defecto, `RepositorioExperimentosEnMemoria`. Con `python run.py --db bitacorabio.db`, `arranque.py` usa `RepositorioExperimentosSQLite` (módulo estándar `sqlite3`, sin dependencias nuevas): es la única línea que cambia; ni el gestor, ni el detector, ni el ejecutor, ni la presentación se modifican (se verifica con `CP-24`, que corre el núcleo real sobre SQLite). El archivo y las tablas se crean solos la primera vez; el esquema sigue el modelo del TP3 (una fila por experimento y una por parámetro nombre-valor-unidad, con un índice sobre nombre y valor normalizado). Para PostgreSQL se escribiría otra clase que cumpla el mismo puerto. Los archivos PDB siguen en el almacén simulado en memoria, y la solicitud pendiente de una confirmación sigue en memoria del ejecutor: si se reinicia el servidor, se pierde la que esté esperando, pero no los experimentos guardados.
- **Archivos:** `AlmacenamientoArchivosEnMemoria` simula el almacén. Para guardar en el sistema de archivos se escribe `AlmacenamientoArchivosLocal` (proyectada) con la misma interfaz.
- **Google Docs:** `ClienteGoogleDocsSimulado` y `ClienteGoogleDocsReal` cumplen `ClienteGoogleDocs`. `arranque.crear_cliente_docs` elige el real solo si está definida `BITACORABIO_GOOGLE_CREDENCIALES` (con `BITACORABIO_GOOGLE_CARPETA` y, opcional, `BITACORABIO_GOOGLE_TOKEN`); `GestorDeRegistro` no cambia. El documento se crea con apartados predefinidos (fecha de realización, autor, técnica, hipótesis, objetivo, parámetros, hardware, tiempo de procesamiento y un apartado «Notas» para completar): el experimento los arma (`apartados_de_notas`, con las etiquetas que da la técnica) y el cliente real los sube como HTML para que Drive lo convierta en un Google Doc, con la misma librería y el mismo alcance. Si Google falla, el error no se captura (queda dentro de lo que dejamos fuera con `HU-01.E1`): el experimento queda guardado sin documento y la pantalla muestra un error interno.
- **Autenticación:** fuera del desarrollo (TP3): el autor se toma de un usuario identificado fijo (`investigadora.demo`).

---

## 7. Pruebas

### 7.1 Estrategia

Pruebas unitarias con pytest sobre el dominio y la capa de servicios, **sin pasar por la interfaz gráfica**. Los colaboradores son implementaciones en memoria, y para la falla de archivos se usa un doble de prueba (`ArchivosQueFallan`). Se usaron las técnicas de la referencia: caja negra (criterios de aceptación; clases de equivalencia; valores límite) y caja blanca (cada rama del gestor, el detector y el ejecutor: sin y con coincidencias, confirmar y cancelar, inválido y válido, falla y éxito del guardado). Las rutas de Flask se prueban con un cliente de prueba, solo para el flujo visible de la HU.

### 7.2 Tabla de casos de prueba

| ID | Técnica | Origen | Dado (entrada y estado) | Resultado esperado | Archivo de prueba |
|---|---|---|---|---|---|
| CP-01 | Caja negra | B1.1 c1 | Proyecto existente, datos válidos y sin coincidencias | Se registra con autor y fecha de carga; el experimento y el PDB quedan guardados | `test_ejecutor_registro.py` |
| CP-02 | Caja negra | B1.1 c2 | Existe un experimento con la misma molécula/ligando pero inválido | No se reporta como coincidencia; se guarda como el camino normal | `test_ejecutor_registro.py` |
| CP-03 | Caja negra | B1.1 c3 | Campos opcionales vacíos | Se guarda sin exigirlos | `test_ejecutor_registro.py` |
| CP-04 | Caja negra | A1, parte "mostrada" | Existe un coincidente | El resultado no está registrado, trae las coincidencias y un identificador pendiente; no se guardó nada | `test_ejecutor_registro.py` |
| CP-05 | Caja negra | **A1** | Existe un coincidente y se confirma lo pendiente | Se registra un experimento nuevo (id distinto) con documento de notas propio; el existente no cambia ni se vincula | `test_ejecutor_registro.py` |
| CP-05b | Caja negra | **A1**, documento propio | Dos registros iguales, el segundo confirmado | Cada uno tiene un documento de notas distinto | `test_ejecutor_registro.py` |
| CP-06 | Caja negra | EC-11 | Se confirma lo pendiente | No se vuelve a buscar (se cuentan las consultas) y se usan los datos originales sin recargarlos | `test_ejecutor_registro.py` (2) |
| CP-06c | Caja negra | A1, cancelar | Se cancela lo pendiente | No se guarda nada y confirmar después se rechaza con `SolicitudNoPendiente` | `test_ejecutor_registro.py` |
| CP-06d | Caja negra | Robustez | Confirmar dos veces o con un identificador desconocido | `SolicitudNoPendiente`; no se guarda dos veces | `test_ejecutor_registro.py` |
| CP-07 | Caja negra, partición | A1 | Dos experimentos coincidentes | Se informan los dos | `test_ejecutor_registro.py` |
| CP-08 | Caja blanca | Orden de las operaciones | Datos sin PDB y existe un coincidente | `ErrorValidacion` y no se pide confirmación; no se guarda nada | `test_ejecutor_registro.py` |
| CP-09 | Caja negra | Tipo | Tipo "cristalografia" | `ErrorValidacion` | `test_ejecutor_registro.py` |
| CP-10 | Caja blanca | Ejecutor | Gestor espía: pide confirmación o queda listo | Con confirmación solo prepara; si está listo prepara, guarda y vincula, en ese orden | `test_ejecutor_registro.py` |
| CP-11 | Calidad (`EC-07`, `DA-02`) | Medida de `DA-02` | Se registra una técnica de prueba (dinámica molecular) con `paso_tiempo` en fs y otra clave de coincidencia, y se corre el registro completo | Funciona sin modificar el núcleo; el parámetro tiene unidad; el duplicado se detecta con la clave nueva; docking sigue funcionando | `test_ejecutor_registro.py` |
| CP-12 | Caja negra | B1.1 | Fecha de realización 2/11 | Se conserva | `test_ejecutor_registro.py` |
| CP-13 | Caja negra | B1.1, validaciones | Proyecto inexistente; fecha vacía o futura (límite: hoy sí, mañana no); sin PDB; parámetro obligatorio vacío; largo 100 (pasa) y 101 (falla); extra sin nombre; "Similar a" inexistente y existente; proteína igual a ligando; con coincidencia pide confirmación; inválido no busca | Cada una devuelve su error o pasa; si hay varios, se informan juntos | `test_gestor_preparar.py` (16) |
| CP-14 | Caja blanca | RF-03 | Sin candidatos; con coincidencia; inválido; en "Similar a"; otro ligando; otro tipo; inválido y válido a la vez; buscar no escribe | Ver el archivo | `test_detector_de_duplicados.py` (8) |
| CP-15 | Caja blanca | Guardado y documento | Guardado exitoso; opcionales vacíos; capturas; dos registros iguales; falla de archivos; vincular un documento propio; dos documentos distintos | Se guarda con autor, fecha y parámetros con unidad; si falla el guardado de archivos se revierte todo; cada experimento tiene su documento y el enlace queda guardado | `test_gestor_guardado.py` (7) |
| CP-16 | Caja blanca | Entidades | Comparación de valores sin distinguir mayúsculas; estados de validez; `valor_de`; `coincide_con` (coincide sin distinguir mayúsculas ni espacios, otro tipo, parámetro ausente, valor distinto); `es_candidato_a_duplicado` (inválido y no inválido) | Responden según la regla | `test_entidades.py` (9) |
| CP-17 | Caja blanca | Técnica y registro | Obligatorios del docking; proteína igual a ligando; clave de coincidencia armada por la técnica; resumen; registrar y obtener; tipo desconocido | Ver el archivo | `test_tecnicas.py` (7) |
| CP-18 | Caja blanca | Gestión de excepciones | Cada tipo de error previsto | Respuesta con tipo y mensajes para el usuario | `test_gestion_excepciones.py` (4) |
| CP-20 | Caja blanca | RF-03, candidatos | Mismo tipo y clave; otro tipo; otro ligando; sin el parámetro; inválidos | El repositorio trae los candidatos (incluidos los inválidos: no decide reglas) y guarda el enlace del documento | `test_repositorio_en_memoria.py` (6) |
| CP-22 | Caja blanca | Ramas y caminos de la tabla 7.4 | Parámetro adicional con nombre; parámetro opcional vacío; falla del PDB (no de una captura); eliminar archivos o experimentos inexistentes; cancelar un id inexistente; falla de almacenamiento al confirmar; docking sin proteína o sin ligando; clave con parámetros ausentes; clave vacía en el repositorio; `valor_de` con valor | Cada camino da su resultado y, en las fallas, se revierte todo | `test_caminos_independientes.py` (12) |
| CP-21 | Caja negra | Presentación | Sin coincidencias; con coincidencias; confirmar; cancelar; datos inválidos; confirmar algo inexistente | Sin coincidencias sigue en el formulario con el aviso debajo; con coincidencias muestra la pantalla y no guarda; confirmar registra sin volver al formulario; cancelar no guarda; los errores se muestran | `test_carga_experimentos.py` (6) |
| CP-23 | Caja negra | Persistencia (puerto `RepositorioExperimentos`) | Las mismas situaciones que `CP-20` sobre la base SQLite, más: ida y vuelta de todos los campos, orden de los parámetros, ids desde el 101, borrado en cascada y datos que sobreviven a cerrar y abrir la base | Mismo contrato que el repositorio en memoria | `test_repositorio_sqlite.py` (16) |
| CP-25 | Caja negra | Réplicas en las coincidencias (`RF-03`) | Original más réplica: se informa solo el original; réplica de réplica; declarar el original cubre a sus réplicas; original inválido: la réplica válida sí se informa | El usuario ve una sola coincidencia por familia de réplicas | `test_detector_de_duplicados.py` (4), `test_entidades.py` (1) |
| CP-26 | Caja negra y blanca | Parámetros opcionales del docking | Centro y tamaño de la caja ("x, y, z"), exhaustividad, número de poses y mejor afinidad: bien formados, vacíos (no se guardan) y mal formados (casilla incompleta, texto, cero, negativo); se guardan como un parámetro nombre-valor-unidad y no entran en la clave de coincidencia | Valores válidos se aceptan; inválidos dan un mensaje por campo y no guardan | `test_tecnicas.py` (10), `test_carga_experimentos.py` (3) |
| CP-27 | Caja negra | Google Docs real (con un servicio de Drive falso) | Sube el HTML con título y apartados (escapados), crea el documento dentro de la carpeta y devuelve el enlace; sin carpeta no envía `parents`; sin `webViewLink` arma el enlace con el id; `arranque` elige el simulado sin variable de entorno y el real con ella | No se conecta a Google; la autorización con OAuth (`desde_credenciales`) se prueba a mano | `test_google_docs_real.py` (7), `test_entidades.py`, `test_gestor_guardado.py` |
| CP-24 | Caja negra | Cambio de repositorio | El núcleo real registra, detecta una coincidencia y continúa pese a ella, y respeta "Similar a", sobre SQLite | Sin modificar ninguna otra clase | `test_repositorio_sqlite.py` (2) |

En total hay **145 pruebas** (también hay seis casos de `ServicioConsulta` y las de las pantallas, de apoyo). La numeración salta de `CP-18` a `CP-20` porque `CP-19` se retiró al unir casos; `CP-22` se agregó con la tabla de complejidad y `CP-23` y `CP-24`, con el repositorio SQLite. La prueba de calidad de `EC-07` es `CP-11`; la del criterio de A1 es `CP-05` junto con `CP-05b`, `CP-06` y `CP-06c`.

### 7.3 Resultados y cobertura

145 pruebas, todas pasan. Con `pytest --cov=src --cov-branch`: **535 sentencias, 0 sin cubrir; 82 ramas, 0 parciales; 100 %**. El análisis (qué mide y qué no) está en `docs/design/cobertura.md`.

### 7.4 Complejidad ciclomática y caminos independientes

Complejidad = decisiones + 1, medida con `radon cc src -s` (cuenta cada `if`, `for`, `except`, comprensión y operador `and`/`or`). Se prueba un camino independiente por unidad de complejidad; la cobertura de ramas confirma que no quedó ninguna sin recorrer. Se listan las operaciones de la HU con complejidad mayor que 1; el resto (complejidad 1) se ejecuta en cualquier camino.

| Operación | CC | Decisiones | Caminos independientes → prueba |
|---|---|---|---|
| `EjecutorDeRegistro.registrar` | 2 | `if` pide confirmación | (1) sin coincidencias, guarda → `CP-01`; (2) con coincidencias, queda pendiente → `CP-04` |
| `EjecutorDeRegistro.confirmar` | 2 | `if` no hay solicitud pendiente | (1) pendiente → `CP-05`; (2) inexistente o ya usada → `CP-06d` |
| `GestorDeRegistro.preparar` | 3 | `if` errores; `if` coincidencias | (1) datos inválidos → `CP-13` (inválido no busca); (2) con coincidencias → `CP-13`; (3) listo para guardar → `CP-13` |
| `GestorDeRegistro.guardar_experimento` | 3 | `except`; comprensión de capturas | (1) éxito sin capturas → `CP-15`; (2) éxito con capturas → `CP-15`; (3) falla y revierte → `CP-15` (captura) y `CP-22` (PDB, y al confirmar) |
| `GestorDeRegistro._errores_de` | 14 | proyecto; fecha vacía; fecha futura; PDB; `for` definiciones; obligatorio **y** vacío (2); largo; `for` extras; extra sin nombre; `for` similar; similar inexistente; sin errores previos → regla de la técnica | 14 caminos → `CP-13` (proyecto, fecha vacía, fecha futura, PDB, obligatorio vacío, largo 100/101, extra sin nombre, similar inexistente y existente, regla de la técnica, varios errores juntos) y `CP-22` (extra con nombre) |
| `DetectorDeDuplicados.buscar` | 6 | comprensión y `if` de candidatos válidos; comprensión y `if` que excluye; `and` | (1) sin candidatos; (2) coincide; (3) inválido excluido; (4) en "Similar a" excluido → `CP-14`; (5) réplica de otro candidato excluida; (6) réplica de un original inválido sí se informa → `CP-25` |
| `Experimento.apartados_de_notas` | 3 | comprensión de parámetros; `if` unidad | sin parámetros; con parámetro sin unidad; con unidad → `CP-27` |
| `armar_html` | 3 | `for`; `or` del texto vacío | sin apartados; con texto; texto vacío → `CP-27` |
| `Experimento.es_replica_de_alguno` | 2 | `any` con condición | es réplica; no lo es (incluye lista vacía) → `CP-25` |
| `SolicitudRegistro.parametros` | 4 | `for`; `if` valor no vacío; comprensión de extras | (1) con valor → `CP-01`; (2) opcional vacío → `CP-22`; (3) con extras → `CP-22`; (4) sin extras → `CP-01` |
| `TecnicaDocking.validar` | 8 | comprensión; `and` proteína; `and` ligando; `==`; `for` de opcionales; `if` del opcional que viene `and` no tiene el formato | (1) iguales → `CP-17`; (2) distintos → `CP-17`; (3) sin proteína → `CP-22`; (4) sin ligando → `CP-22`; (5) sin parámetros → `CP-22`; (6) opcional ausente, no se valida → `CP-26`; (7) opcional bien formado → `CP-26`; (8) opcional mal formado (cada uno de los cinco) → `CP-26` |
| `TecnicaDocking.clave_de_coincidencia` | 3 | dos comprensiones | (1) con parámetros → `CP-17`; (2) sin parámetros → `CP-22` |
| `Experimento.coincide_con` | 7 | `if` otro tipo; `for` clave; búsqueda del parámetro (comprensión con `if`); `if` falta el parámetro **o** valor distinto | otro tipo, sin el parámetro, valor distinto y coincide → `CP-16`; clave vacía → `CP-22`; un parámetro propio que no es el buscado → `CP-16` |
| `Experimento.es_candidato_a_duplicado` / `SolicitudRegistro.declara_similar` | 1 / 1 | ninguna | un camino cada una → `CP-16`, `CP-14` |
| `RepositorioExperimentosEnMemoria.con_parametros` | 3 | comprensión; `if` coincide | ninguno coincide; coincide → `CP-20` |
| `RepositorioExperimentosSQLite.con_parametros` | 4 | `for` por cada parámetro de la clave; comprensión; `if` que confirma con `Experimento.coincide_con` | clave vacía y clave con parámetros → `CP-23`. El `if` de confirmación no descarta nada con datos reales (la base ya filtró con la misma normalización): es una garantía de que la regla la decide `Experimento` |
| `Experimento.valor_de` | 3 | `for`; `if` nombre | (1) sin parámetros → `CP-16`; (2) con el parámetro → `CP-22` |
| `RegistroDeTecnicas.tecnica` | 2 | `if` tipo no registrado | (1) registrado; (2) desconocido → `CP-17`, `CP-09` |
| `respuesta_para` (excepciones) | 4 | tres tipos de error previsto | un camino por tipo y el genérico → `CP-18` |
| `AlmacenamientoArchivosEnMemoria.eliminar_archivos` | 4 | `for`; `if` | con archivos → `CP-15`; sin archivos → `CP-22` |
| `ClienteGoogleDocsReal.crear_documento` | 3 | `if` carpeta; `or` del enlace | (1) con carpeta → `CP-27`; (2) sin carpeta → `CP-27`; (3) sin `webViewLink` → `CP-27` |

`_errores_de` es el punto de mayor complejidad (14, nivel "C" de radon): concentra todas las validaciones de la solicitud. Se aceptó porque cada regla es una condición simple e independiente y está cubierta una por una; si se agregan más reglas conviene partirla en una función por grupo. `construir_nucleo` (CC 4) está en `arranque.py`, que se excluye de la medición.

---

## 8. Trazabilidad y coherencia con la arquitectura

### 8.1 Tabla de verificación de coherencia

| Verificación | ¿Se cumple? | Evidencia |
|---|---|---|
| Cada participante de las secuencias pertenece a un componente de la ficha | Sí | Tabla "Elemento → componente del TP3 → capa" (3.4) |
| Cada mensaje entre componentes está en el catálogo de relaciones del TP3 | Sí, con las diferencias de 8.2 | `CE → E` y `CE → GX` están tal cual. Los mensajes de `E` a `RX` y `CG` corresponden a las relaciones de las operaciones del gestor y del detector (Gestor de registro y Detector de duplicados → Repositorio, Almacenamiento de archivos y Cliente de Google Docs), porque el controller `EjecutorDeRegistro` representa al proceso y a esas clases. Las llamadas a la técnica y a `Experimento` se ven en las secuencias porque ahora son participantes. Las relaciones nuevas del catálogo están en 8.2 |
| El diseño respeta las restricciones del estilo y del patrón | Sí | 2.2 y la tabla de "cómo se agrupó en la robustez" (3.4). Las dependencias del código van hacia abajo; el ejecutor no tiene lógica |
| La táctica del escenario de calidad aparece como operación o mensaje | Sí | Operaciones `RegistroDeTecnicas.tecnica(tipo)`, `Tecnica.definiciones()`, `validar()` y `clave_de_coincidencia()` del modelo de clases (4), no mensajes de las secuencias, y la prueba CP-11. Es "diferir el enlace" y "parametrización" de `EC-07` |
| Cada entidad del diagrama de robustez está en el modelo de dominio del TP1 | Sí | Tabla 3.2 |
| Cada entidad que interviene según 3.2 aparece en el diseño, o se explica por qué no | Sí | `Usuario` y `Proyecto` se explican en 3.2 (viajan como identificadores); las demás están en la robustez |
| La medida del escenario tiene una prueba que la verifica | Sí | `CP-11` (`EC-07`) y `CP-06` (`EC-11`) |

### 8.2 Diferencias entre el TP3 y este diseño

La consigna pide decir qué cambió al bajar al detalle. Hay cambios ya aplicados a `arquitectura.md` y cambios **pendientes de decidir y aplicar**:

| Diferencia | Estado | Motivo |
|---|---|---|
| Falta la relación "Validar datos → Repositorio de experimentos" | Aplicado al TP3 | La validación necesita saber si el proyecto y los experimentos de "Similar a" existen (hoy la hace el Gestor de registro) |
| Falta la relación "Rutas de registro → Servicio de consulta" | Aplicado al TP3 | El formulario necesita la lista de proyectos y de experimentos |
| Quién excluye los inválidos y los declarados en "Similar a" | Aplicado al TP3 | Es una regla de negocio: el repositorio trae candidatos y el *Detector de duplicados* los filtra. En el TP4 cada regla vive donde están sus datos: el estado, en `Experimento`; "Similar a", en la solicitud |
| `Experimento` tiene reglas propias (`coincide_con`, `es_candidato_a_duplicado`) | Nuevo detalle del TP4 | Evita una entidad anémica |
| El SRS incorpora `tipo`, `fecha_de_carga` y "Similar a" en el modelo de dominio y en `RF-03` | Aplicado al SRS | Ya estaban en el formulario y en el texto de `RF-02`; faltaban en el modelo |
| Las entidades no son un componente y el acceso a datos usa las entidades, pero no el dominio ni los plug-ins | Aplicado al TP3 | Inversión de dependencias: el dominio define los puertos |
| *Rutas de registro* pasa a llamarse **Carga de experimentos** | **Pendiente en el TP3** | Nombre más explícito (decisión del grupo) |
| *Acceso a archivos* pasa a llamarse **Almacenamiento de archivos**, con una interfaz genérica (`guardar`, `leer`, `eliminar_archivos`) | **Pendiente en el TP3** | Antes se había propuesto *Acceso a capturas y estructuras*; se cambia porque no hace falta una operación por tipo de archivo y admite formatos nuevos |
| La técnica arma la clave de coincidencia: `clave_de_coincidencia(parametros)` | Nuevo detalle del TP4 | El TP3 dice solo que la técnica la define |
| *Validar datos*, *Guardar experimento* y *Vincular documento* pasan a ser operaciones de un único componente de dominio, **Gestor de registro**, y la detección queda en **Detector de duplicados** | **Pendiente en el TP3** | Cuatro componentes pequeños con los mismos colaboradores eran demasiados. El TP3 dice que los pasos no se llaman entre sí: se respeta, el gestor no llama a sus operaciones entre sí y el Ejecutor las ordena |
| La obligatoriedad y el formato salen de `definiciones()` y las reglas propias de `validar()` | Nuevo detalle del TP4 | Un solo lugar para la obligatoriedad |
| El registro con coincidencias queda **pendiente** en el Ejecutor hasta confirmar o cancelar | **Pendiente en el TP3** | El TP3 decía que el servidor no guarda nada entre solicitudes y que se repetía el registro con la confirmación. Se cambia para no repetir la validación ni la búsqueda y para no reenviar el PDB. Es estado en memoria; limitación: no sobrevive a un reinicio ni a varios servidores |
| Encontrar coincidencias es un resultado y no un error previsto | **Pendiente en el TP3** | Ya no existe `CoincidenciasSinConfirmar`. Se agrega el error `SolicitudNoPendiente` |
| *Vincular documento* corre con un cliente de Google Docs **simulado** | Nuevo detalle del TP4 | Para cumplir el criterio de A1 sin conexión real |
| Robustez y secuencias | Sin diferencias de fondo | La robustez mantiene cinco controllers y tres fronteras. Las secuencias bajan los controllers agrupados a sus clases (gestor, detector, plug-in) y agregan la entidad `Experimento` (3.4 y 4.1) |

### 8.3 Trazabilidad

| HU / escenario | Componente C4 | Clases | Archivo | Pruebas |
|---|---|---|---|---|
| B1.1 c1 (registrar) | Carga de experimentos → Ejecutor de registro → Gestor de registro | `CargaDeExperimentos`, `EjecutorDeRegistro`, `GestorDeRegistro` | `src/presentacion/carga_experimentos.py`, `src/servicios/ejecutor_registro.py`, `src/dominio/gestor_registro.py` | CP-01, CP-12, CP-13, CP-15, CP-21 |
| B1.1 c2 (excluir inválidos) | Detector de duplicados, Repositorio de experimentos | `DetectorDeDuplicados`, `RepositorioExperimentos` | `src/dominio/detector_de_duplicados.py`, `src/acceso_datos/repositorio_en_memoria.py` | CP-02, CP-14, CP-20 |
| B1.1 c3 (opcionales vacíos) | Gestor de registro | `GestorDeRegistro` | `src/dominio/gestor_registro.py` | CP-03, CP-15 |
| A1, parte "mostrada" | Gestor de registro, Detector de duplicados, Ejecutor de registro | `GestorDeRegistro`, `DetectorDeDuplicados`, `EjecutorDeRegistro`, `Resultado` | `src/dominio/gestor_registro.py`, `src/dominio/detector_de_duplicados.py`, `src/servicios/ejecutor_registro.py` | CP-04, CP-07, CP-14, CP-21 |
| A1 (continuar de todos modos) | Carga de experimentos, Ejecutor de registro, Gestor de registro | `EjecutorDeRegistro`, `GestorDeRegistro`, `SolicitudRegistro`, `ClienteGoogleDocs` | `src/servicios/ejecutor_registro.py`, `src/dominio/gestor_registro.py`, `src/acceso_datos/google_docs_simulado.py` | CP-05, CP-05b, CP-06, CP-06c, CP-06d, CP-15, CP-21 |
| Rechazos (datos, tipo, almacenamiento) | Gestor de registro, Gestión de excepciones | `GestorDeRegistro`, `GestionDeExcepciones` | `src/dominio/gestor_registro.py`, `src/transversal/gestion_excepciones.py` | CP-08, CP-09, CP-13, CP-15, CP-18, CP-21 |
| Persistencia reemplazable (puerto `RepositorioExperimentos`) | Repositorio de experimentos | `RepositorioExperimentos`, `RepositorioExperimentosEnMemoria`, `RepositorioExperimentosSQLite` | `src/dominio/puertos.py`, `src/acceso_datos/repositorio_en_memoria.py`, `src/acceso_datos/repositorio_sqlite.py` | CP-20, CP-23, CP-24 |
| EC-07 | Registro de técnicas, Técnica Docking | `RegistroDeTecnicas`, `Tecnica`, `TecnicaDocking` | `src/dominio/registro_tecnicas.py`, `src/dominio/tecnica.py`, `src/dominio/tecnica_docking.py` | CP-10, CP-11, CP-17 |
| EC-11 | Ejecutor de registro, Carga de experimentos | `EjecutorDeRegistro`, `CargaDeExperimentos` | `src/servicios/ejecutor_registro.py`, `src/presentacion/carga_experimentos.py`, plantilla `coincidencias.html` | CP-06, CP-21 |

Todo criterio de aceptación llega al menos a una prueba. Las clases con comportamiento del diagrama aparecen en las secuencias como participantes; las dos interfaces de acceso se muestran juntas como `RepositorioDeExperimentos` (4.1).

---

## 9. Glosario y bibliografía

**Glosario.** *Solicitud de registro*: objeto inmutable que lleva los datos, el autor y la técnica del registro. *Solicitud pendiente*: solicitud validada con coincidencias que el Ejecutor conserva, con un identificador, hasta que se confirma o se cancela. *Plug-in de técnica*: componente que declara lo propio de un tipo de ensayo (parámetros, validaciones, clave de coincidencia). *Clave de coincidencia*: parámetros que, junto con el tipo, definen que dos experimentos son "el mismo". *Candidato*: experimento previo con el mismo tipo y la misma clave, antes de aplicar las reglas del negocio. *Error previsto*: excepción que el sistema espera y traduce en una respuesta para el usuario. *Doble de prueba*: implementación simulada de un colaborador, usada en las pruebas.

**Bibliografía.**

- Valotto, V. *Diseño tridimensional de software*. 2025.
- Larman, C. *Applying UML and Patterns*. Prentice Hall (criterios GRASP).
- Gamma, E., Helm, R., Johnson, R. y Vlissides, J. *Design Patterns*. Addison-Wesley.
- Rosenberg, D. y Stephens, K. *Use Case Driven Object Modeling with UML*. Apress, 2007.
- Bass, L., Clements, P. y Kazman, R. *Software Architecture in Practice* (tácticas).
- Documentación de pytest y de Flask.
