# BitacoraBio-2026 - Catálogo de Experimentos Computacionales
### **Integrantes: Nuñez Juliana, Segovia Lucas.**
Este proyecto se trata de un sistema de gestión y trazabilidad diseñado para investigadores y becarios que trabajen juntos en grupos que corren experimentos bioinformáticos. Su alcance inicial (MVP) se centraliza en el registro, búsqueda y filtrado de metadatos para ensayos de docking molecular, previniendo la repetición accidental de ensayos. 
El sistema también integra una vinculación con bitácoras en Google Docs y un visor 3D (solo en modo lectura) para interpretar las poses estructurales sin necesidad de descargar archivos ni abrir software externo.

Detalle completo del problema, stakeholders y alcance: consultar la sección Visión y Alcance en el [SRS (Software Requirements Specification)](docs/requirements/srs.md).

Para la realización de este proyecto se usara un modelo de ciclo de vida **incremental e iterativo** (es decir, una fusión de ambos). El enfoque incremental permite dividir el proyecto en partes mas manejables, entregando una porción funcional de valor desde una etapa temprana, en este caso, sera enfocada en la trazabilidad del docking molecular. Ademas de esto tomaremos un enfoque iterativo para revisar y ajustar la precisión de los metadatos almacenados en cada ciclo. Esto apoyará a la evolucionalidad del software, dejando la arquitectura preparada para la futura integración de incrementos mayores, enfocados en otros tipos de ensayos (Ej. dinámicas moleculares, ensamblados, etc.)

