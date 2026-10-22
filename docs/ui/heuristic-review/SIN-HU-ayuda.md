# Evaluación heurística — Ayuda
**Historias de usuario:** ninguna (pantalla transversal, sin HU asociada; surge de la evaluación de la heurística 10 en las demás pantallas)
**Mockup:** `docs/ui/mockups/SIN-HU-ayuda.html`

## Generación del maquetado

**Prompt utilizado:** mismo contexto general (perfil de investigador/a bioinformático/a, estética de las demás pantallas); se pidió una pantalla de Ayuda con preguntas frecuentes sobre registrar y buscar experimentos y un glosario de los términos técnicos del formulario.

**Resultado:** ver `docs/ui/mockups/SIN-HU-ayuda.html`.

## Evaluación heurística

**Prompt utilizado:** el mismo citado en `HU-01.B1.1-B1.2-cargar-experimento.md`.

| # | Heurística | Hallazgo de la IA | Decisión del grupo | Justificación |
|---|---|---|---|---|
| 1 | Visibilidad del estado del sistema | Cumple — mismo header y menú lateral que el resto | **Aceptado, sin cambios** | — |
| 2 | Coincidencia sistema/mundo real | Cumple — glosario con los términos del docking (exhaustiveness, seed, caja de búsqueda) | **Aceptado, sin cambios** | — |
| 3 | Control y libertad del usuario | Cumple — se vuelve a la pantalla anterior con el menú lateral | **Aceptado, sin cambios** | — |
| 4 | Consistencia y estándares | Cumple | **Aceptado, sin cambios** | — |
| 5 | Prevención de errores | No aplica — no hay formularios | **Aceptado, sin cambios** | — |
| 6 | Reconocimiento antes que recuerdo | Cumple — preguntas y términos visibles sin buscar | **Aceptado, sin cambios** | — |
| 7 | Flexibilidad y eficiencia de uso | Parcial — sin buscador dentro de la ayuda | **Aceptado el hallazgo, sin cambio** | Con pocas secciones el contenido se recorre de un vistazo; un buscador no se justifica por ahora. |
| 8 | Diseño estético y minimalista | Cumple | **Aceptado, sin cambios** | — |
| 9 | Ayudar a reconocer/diagnosticar/recuperarse de errores | Parcial — no explica qué hacer ante errores del sistema (ej. Google Docs caído) | **Aceptado el hallazgo, sin cambio** | Depende de los estados de error, que son parte del manejo de excepciones del sistema final. |
| 10 | Ayuda y documentación | Cumple — es la respuesta a la falta detectada en las demás pantallas | **Aceptado** | Se acepta que faltaba; esta pantalla se agrega a consecuencia. |

## Ajustes implementados

1. Pantalla de Ayuda con preguntas frecuentes (registrar experimentos, buscar y consultar) y glosario.
2. Botón "Ayuda" del header enlazado a esta pantalla desde las 6 pantallas con navegación.
