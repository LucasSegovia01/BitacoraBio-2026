# Perfil de usuario — Director/a del grupo

## Perfil de usuario

- **Quién es:** director/a del grupo de investigación (rol definido en el SRS, sección "Stakeholders y Usuarios" / "Stakeholders y roles").
- **Objetivo con el sistema:** consultar el historial completo del grupo para tener panorama del avance de la investigación, sin pedirle a cada integrante que le comente todo. *(Textual del SRS, sección "Usuarios y Stakeholders".)*
- **Contexto de uso:** no está detallado explícitamente para este actor en el TP1. **Supuesto del grupo:** se asume el mismo contexto flexible que el/la investigador/a (cualquier entorno con computadora), por tratarse del mismo tipo de organización de laboratorio chico. No se verificó este supuesto contra ninguna fuente del TP1.
- **Nivel de conocimiento técnico:** no está especificado en el TP1 para este rol. **Supuesto del grupo:** se asume comparable o mayor al del investigador/a, dado que dirige el mismo tipo de trabajo técnico — sin dato del TP1 que lo confirme.
- **Limitaciones o frustraciones:** no están especificadas en el TP1 para este actor. **Supuesto del grupo**, por extensión del perfil de investigador/a.

> Este perfil se apoya en menos información directa del TP1 que el de investigador/a — el SRS define con precisión el *objetivo* del Director/a (panorama sin pedir reportes manuales) pero no describe su contexto de uso ni su nivel técnico. Se deja constancia de esto en vez de inventar atributos no verificables, tal como pide la consigna.

## Escenario de uso

*(Tomado de HU-02.B1 y HU-02.B2 del TP1, que tienen como actor principal a la generalización Investigador/a-Director/a.)*

> El/la director/a quiere saber en qué está el equipo antes de una reunión semanal. Entra a BitacoraBio 2026, va a Buscar, filtra por proyecto para ver todos los experimentos cargados ese mes, y abre el detalle de los que terminaron en estado "Éxito" para revisar los resultados — sin tener que pedirle a cada investigador/a que se los resuma por mail.

## Flujo de navegación

1. **Buscar** (`HU-02.B1-A1-busqueda-filtros.html`) — filtra por proyecto, fecha o autor.
2. **Detalle de experimento** (`HU-02.B2-detalle-experimento.html`) — revisa el resultado de cada experimento que le interesa.

> **Nota de diseño pendiente, no resuelta en esta entrega:** el Director/a no tiene permiso para registrar experimentos (CU-01 tiene como único actor principal al/la Investigador/a). Sin embargo, la pantalla de Inicio del maquetado actual muestra el formulario de carga de forma fija para cualquier usuario que entre, sin distinguir el rol. Si el/la Director/a navegara a Inicio, vería un formulario que no debería poder usar. Queda señalado para una futura iteración (no forma parte de los cambios de esta entrega).

> La misma salvedad de `investigador.md` aplica acá: el acceso a "Mis proyectos" (listado y detalle) no está respaldado por ninguna historia de usuario del TP1.
