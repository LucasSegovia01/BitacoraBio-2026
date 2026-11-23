# BitacoraBio-2026 - Catálogo de Experimentos Computacionales
### **Integrantes: Nuñez Juliana, Segovia Lucas.**
Este proyecto se trata de un sistema de gestión y trazabilidad diseñado para investigadores y becarios que trabajen juntos en grupos que corren experimentos bioinformáticos. Su alcance inicial (MVP) se centraliza en el registro, búsqueda y filtrado de metadatos para ensayos de docking molecular, previniendo la repetición accidental de ensayos. 
El sistema también integra una vinculación con bitácoras en Google Docs y un visor 3D (solo en modo lectura) para interpretar las poses estructurales sin necesidad de descargar archivos ni abrir software externo.

Detalle completo del problema, stakeholders y alcance: consultar la sección Visión y Alcance en el [SRS (Software Requirements Specification)](docs/requirements/srs.md).

Para la realización de este proyecto se usara un modelo de ciclo de vida **incremental e iterativo** (es decir, una fusión de ambos). El enfoque incremental permite dividir el proyecto en partes mas manejables, entregando una porción funcional de valor desde una etapa temprana, en este caso, sera enfocada en la trazabilidad del docking molecular. Ademas de esto tomaremos un enfoque iterativo para revisar y ajustar la precisión de los metadatos almacenados en cada ciclo. Esto apoyará a la evolucionalidad del software, dejando la arquitectura preparada para la futura integración de incrementos mayores, enfocados en otros tipos de ensayos (Ej. dinámicas moleculares, ensamblados, etc.)


## Cómo ejecutar (TP4 · HU-01.A1)

Implementación de la HU-01.A1 (continuar el registro pese a una coincidencia), con HU-01.B1.1 como base. Google Docs se simula detrás de la interfaz `ClienteGoogleDocs`. Requiere Python 3.10 o superior.

    python -m venv .venv
    .venv\Scripts\activate          # en Linux o macOS: source .venv/bin/activate
    pip install -r requirements.txt
    python run.py                   # abrir http://localhost:5000
    pytest                          # pruebas

Por defecto los datos viven en memoria. Con `python run.py --db bitacorabio.db` se guardan en una base SQLite que se crea sola. Hay un experimento de ejemplo cargado (#101, Proteasa HIV-1 / Indinavir): cargar otro igual lleva a la pantalla de coincidencias.

Diseño detallado: [`docs/design/diseno-detallado.md`](docs/design/diseno-detallado.md) · Cobertura y complejidad: [`docs/design/cobertura.md`](docs/design/cobertura.md)

### Cómo usar la página

1. **Registrar** (`/registro`): elegí el proyecto y la técnica, completá la fecha de realización, proteína, ligando y software, y adjuntá el archivo PDB (se ve en el visor 3D). Hipótesis, objetivo, hardware, tiempo, notas, capturas y los parámetros del docking son opcionales.
2. **Coincidencias.** Si ya existe un experimento con la misma proteína y el mismo ligando, aparece la lista de coincidencias. Podés **Cancelar** (no se guarda nada) o **Realizar el registro de todas formas**.
3. **Réplicas.** Marcá «Similar a» para declarar que el experimento es una réplica de otro: se guarda y se muestra un aviso, y no se vuelve a informar como coincidencia.
4. **Resultado.** Al guardar se muestra el id del experimento y el enlace a su **documento de notas** (uno por experimento).
5. **Consultar.** `/proyectos`, `/experimentos` (los tuyos), `/experimentos/<id>` (detalle con parámetros, visor 3D y enlace al documento) y `/buscar`. Con `python run.py --db bitacora.db` los datos quedan guardados al cerrar.
6. La pantalla `/ayuda` resume lo anterior dentro de la aplicación.

### Vincular con Google Docs

Por defecto el enlace al documento es **simulado** (no se crea nada en Google). Para crear documentos reales:

**Una sola vez, en Google Cloud**
1. En [console.cloud.google.com](https://console.cloud.google.com) creá un proyecto y activá la **Google Drive API**.
2. Pantalla de consentimiento OAuth: tipo «Externo» y, en *Usuarios de prueba*, agregá tu cuenta de Google.
3. Credenciales → *Crear credenciales* → **ID de cliente de OAuth**, tipo **Aplicación de escritorio**. Descargá el JSON (`credentials.json`).
4. En tu Drive creá una carpeta para las notas y copiá su id: es lo que va después de `/folders/` en la dirección.

**En tu computadora**
```powershell
pip install -r requirements-google.txt
$env:BITACORABIO_GOOGLE_CREDENCIALES = "C:\ruta\a\credentials.json"   # usá dir para confirmar el nombre exacto
$env:BITACORABIO_GOOGLE_CARPETA = "ID_DE_LA_CARPETA"
python run.py
```
(en bash: `export BITACORABIO_GOOGLE_CREDENCIALES=...`; en cmd: `set ...`). Si no definís `BITACORABIO_GOOGLE_CARPETA`, el documento se crea en la raíz de tu Drive.

La **primera vez** que registres un experimento se abre el navegador para que autorices el acceso; se guarda un `token.json` (cambiá el lugar con `BITACORABIO_GOOGLE_TOKEN`) y no vuelve a pedirse. Las variables valen solo para esa ventana de PowerShell.

**Cómo queda el documento.** Se crea «Notas del experimento N» con un título y los apartados: *Fecha de realización, Autor, Técnica, Hipótesis, Objetivo, Parámetros, Hardware, Tiempo de procesamiento* y *Notas* (para seguir escribiendo). El enlace se ve en el resultado del registro y en el detalle del experimento.

**Problemas comunes**
- *Error 403 / «access_denied»*: tu cuenta no está como usuario de prueba, o la Drive API no está activada.
- *No se abre el navegador o falla la autorización*: borrá `token.json` y repetí.
- *Aparece un enlace `.../document/simulado/...`*: la variable `BITACORABIO_GOOGLE_CREDENCIALES` no está definida en esa ventana.
- Si Google falla, el experimento queda guardado sin documento (el reintento es `HU-01.E1`, fuera de alcance).

**Seguridad.** `credentials.json` y `token.json` dan acceso a tu cuenta: **no los subas al repositorio**. Guardalos fuera de la carpeta del proyecto o agregá `credentials.json` y `token.json` al `.gitignore`.
