# Evaluación heurística — Mis proyectos
**Historia de usuario:** ⚠️ **ninguna — ver nota de trazabilidad abajo.**
**Mockup:** `docs/ui/mockups/SIN-HU-proyectos-listado.html`

## Ciclo 1 — Generación del maquetado

**Prompt utilizado:** mismo contexto general (perfil, escenario, estética); el grupo pidió explícitamente datos de proyectos "de juguete", reconociendo que el proceso no está desarrollado en profundidad.

**Resultado:** ver `docs/ui/mockups/SIN-HU-proyectos-listado.html`.

## Ciclo 2 — Evaluación heurística

**Prompt utilizado:** el mismo citado en `HU-01.B1.1-B1.2-cargar-experimento.md`.

**Hallazgos de la IA, revisión del grupo y decisión final:**

| # | Heurística | Hallazgo de la IA | Decisión del grupo | Justificación |
|---|---|---|---|---|
| 1 | Visibilidad del estado del sistema | Cumple — columnas Estado/Última actividad | **Aceptado, sin cambios** | — |
| 2 | Coincidencia sistema/mundo real | Cumple | **Aceptado, sin cambios** | — |
| 3 | Control y libertad del usuario | Cumple (no aplica, solo navegación) | **Aceptado, sin cambios** | — |
| 4 | Consistencia y estándares | Cumple | **Aceptado, sin cambios** | — |
| 5 | Prevención de errores | Cumple (no aplica) | **Aceptado, sin cambios** | — |
| 6 | Reconocimiento antes que recuerdo | Cumple | **Aceptado, sin cambios** | — |
| 7 | Flexibilidad y eficiencia de uso | Incumple — sin orden ni filtro en la tabla | **Aceptado** | Se agrega un selector de orden arriba de la tabla. |
| 8 | Diseño estético y minimalista | Cumple | **Aceptado, sin cambios** | — |
| 9 | Ayudar a reconocer/diagnosticar/recuperarse de errores | Cumple (no aplica) | **Aceptado, sin cambios** | — |
| 10 | Ayuda y documentación | Incumple — sin aclaración de qué significa "Pausado"/"Activo" | **Rechazado** | El grupo considera que el significado de esos estados es evidente por sí mismo y que agregar una aclaración sería ruido innecesario. |

## Ciclo adicional — ajustes implementados

1. Selector "Ordenar por" (Última actividad / Nombre / Cantidad de experimentos) agregado arriba de la tabla.
2. Botón "Ayuda" sumado al header (cambio transversal).

**Ejemplo de hallazgo rechazado para la bitácora de uso de IA:** la heurística 10 — el grupo rechazó agregar aclaraciones sobre los estados "Activo"/"Pausado" por considerarlas evidentes por contexto y, de agregarse, redundantes para el perfil de usuario definido.
