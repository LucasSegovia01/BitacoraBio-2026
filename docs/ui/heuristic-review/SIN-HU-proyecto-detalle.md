# Evaluación heurística — Detalle de proyecto
**Historia de usuario:** ⚠️ **ninguna — misma salvedad que en `SIN-HU-proyectos-listado.md`** (Proceso 6, fuera de profundización en el TP1, sin CU ni HU propia).
**Mockup:** `docs/ui/mockups/SIN-HU-proyecto-detalle.html`

## Ciclo 1 — Generación del maquetado

**Prompt utilizado:** mismo contexto general; pantalla propuesta por la IA como necesaria para completar el flujo "Mis proyectos → detalle", no pedida explícitamente palabra por palabra por el grupo en un primer momento, sino aceptada como parte del conjunto de pantallas a generar.

**Resultado:** ver `docs/ui/mockups/SIN-HU-proyecto-detalle.html`.

## Ciclo 2 — Evaluación heurística

**Prompt utilizado:** el mismo citado en `HU-01.B1.1-B1.2-cargar-experimento.md`.

**Hallazgos de la IA, revisión del grupo y decisión final:**

| # | Heurística | Hallazgo de la IA | Decisión del grupo | Justificación |
|---|---|---|---|---|
| 1 | Visibilidad del estado del sistema | Cumple — resumen agregado de estados visible | **Aceptado, sin cambios** | — |
| 2 | Coincidencia sistema/mundo real | Cumple | **Aceptado, sin cambios** | — |
| 3 | Control y libertad del usuario | Parcial — sin acción directa de "cargar experimento para este proyecto" | **Aceptado** | Se agrega un botón que redirige al formulario de carga con el proyecto ya preseleccionado. |
| 4 | Consistencia y estándares | Cumple | **Aceptado, sin cambios** | — |
| 5 | Prevención de errores | Cumple (no aplica) | **Aceptado, sin cambios** | — |
| 6 | Reconocimiento antes que recuerdo | Cumple | **Aceptado, sin cambios** | — |
| 7 | Flexibilidad y eficiencia de uso | Incumple — sin filtro de experimentos desde esta misma pantalla | **Rechazado** | El grupo argumenta que agregar filtros acá le quita sentido a la pantalla de Buscar dedicada — mantiene una sola fuente de verdad para esa función. Se deja la pantalla sin cambios en este punto. |
| 8 | Diseño estético y minimalista | Cumple | **Aceptado, sin cambios** | — |
| 9 | Ayudar a reconocer/diagnosticar/recuperarse de errores | Cumple (no aplica) | **Aceptado, sin cambios** | — |
| 10 | Ayuda y documentación | Incumple — sin aclaración de los estados del proyecto | **Rechazado** | Mismo criterio que en `SIN-HU-proyectos-listado.md`: aclaración considerada obvia e innecesaria. |

## Ciclo adicional — ajustes implementados

1. Botón "+ Cargar experimento para este proyecto" agregado junto al badge de estado; redirige al formulario de carga con el campo "Proyecto" ya preseleccionado (vía parámetro en la URL, funcional en el mockup).
2. Botón "❓ Ayuda" sumado al header (cambio transversal).

**Ejemplos de hallazgos rechazados para la bitácora de uso de IA:**
- Heurística 7: se rechazó agregar filtros en esta pantalla, para no duplicar la función de la pantalla de Buscar.
- Heurística 10: se rechazó agregar aclaraciones sobre los estados del proyecto, por el mismo criterio que en Mis proyectos.
