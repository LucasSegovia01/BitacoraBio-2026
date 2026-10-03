# Perfil de usuario — Investigador/a (becario/a)

## Perfil de usuario

- **Quién es:** investigador/a o becario/a de un grupo de investigación en bioinformática (rol definido en el SRS, sección "Stakeholders y Usuarios" / "Stakeholders y roles").
- **Objetivo con el sistema:** mantenerse organizado y al día con el estado de la investigación grupal que se lleva a cabo en el proyecto — tanto de sus propias partes como de lo realizado por sus compañeros/as. *(Supuesto del grupo, aportado al definir la interfaz — no está redactado literalmente en el TP1, pero se deriva directamente del "Valor" del SRS: evitar repetir ensayos y tener el catálogo consultable para cualquier integrante.)*
- **Contexto de uso:** cualquier entorno con computadora — laboratorio, oficina, casa. *(Supuesto del grupo.)*
- **Nivel de conocimiento técnico:** alto. Es investigador/a bioinformático/a: si sabe usar herramientas de docking molecular por consola, puede usar una interfaz suficientemente clara sin curva de aprendizaje adicional. *(Supuesto del grupo, consistente con el perfil que ya describe el TP1 para este rol.)*
- **Limitaciones o frustraciones:** la principal limitación esperable no es de conocimiento técnico, sino de no encontrar algo puntual en las pestañas de la interfaz si esta no es lo suficientemente clara. *(Supuesto del grupo.)*

## Escenario de uso

*(Tomado de HU-01.B1.1 y HU-01.B1.2 del TP1.)*

> Investigado/a X termina de correr un ensayo de docking en su laptop del laboratorio. Entra a BitacoraBio 2026, va a Inicio, y completa el formulario de carga con los datos del experimento: proyecto, molécula/proteína, ligando, software usado y los parámetros clave de la corrida. Como está repitiendo el ensayo a propósito, variando parámetros para un estudio de sensibilidad, usa el campo "Similar a" para dejar esa relación registrada desde el principio. Al confirmar, el sistema verifica que no haya una coincidencia no reconocida, guarda el experimento, crea automáticamente el documento de notas en Google Docs, y Juliana ve el resumen con el enlace a la bitácora — sin haber tenido que enviar ningún archivo por mail ni avisarle a nadie manualmente.

## Flujo de navegación

Pantallas que recorre el/la investigador/a para completar la tarea anterior (definen qué se maquetó):

1. **Inicio** (`HU-01.B1.1-B1.2-cargar-experimento.html`) — completa el formulario de carga.
2. **Posibles coincidencias** (`HU-01.A1-E3-posibles-coincidencias.html`) — solo si CU-00 detecta una coincidencia no declarada de antemano; decide continuar o cancelar.
3. **Detalle de experimento** (`HU-02.B2-detalle-experimento.html`) — ve el resumen del experimento recién guardado, con el enlace a Google Docs.

Flujos adicionales del mismo actor, también cubiertos por el maquetado:

- **Buscar** (`HU-02.B1-A1-busqueda-filtros.html`) → **Detalle de experimento** — para chequear si un ensayo similar ya existe antes de correrlo.
- **Experimentos** (`HU-02.B1-mis-experimentos.html`) → **Detalle de experimento** — para revisar su propio historial.

