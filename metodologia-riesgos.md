# Cómo se miden los riesgos — Marco metodológico

> Documento de referencia para el módulo de **Análisis de Riesgos** del resumidor de expedientes (GovLab · Universidad de La Sabana).
> Fundamenta la lógica del `SYSTEM_PROMPT` en `backend/services/claude_service.py`.

---

## 1. Para qué sirve este documento

El analizador de expedientes incluye una sección de **Análisis de Riesgos**. Para que esa sección sea creíble a nivel ejecutivo, no basta con "listar cosas que pueden salir mal": hay que **clasificar** los riesgos por tipo y **medirlos** con un criterio consistente. Este documento resume cómo lo hacen los estándares de referencia y cómo se aplica a la herramienta.

Dos problemas que este marco corrige:

1. **Identificar más tipos de riesgo.** No solo riesgos estratégicos o legales, sino también económicos, operativos, administrativos, reputacionales, tecnológicos y de integridad.
2. **No sobredimensionar.** Un mapa donde todo es "alto" no permite priorizar. Medir con probabilidad × impacto obliga a distinguir entre alto, medio y bajo.

---

## 2. Marcos de referencia

Cuatro marcos sustentan la metodología. Los tres primeros son internacionales; el cuarto es la norma de obligatorio referente para el sector público colombiano.

### ISO 31000:2018 — Gestión del riesgo. Directrices
Estándar internacional que ofrece principios, un marco de referencia y un proceso para gestionar cualquier tipo de riesgo, adaptable a organizaciones de cualquier tamaño y sector. Define la **evaluación del riesgo** como el proceso global de **identificación + análisis + valoración**, que debe registrarse, comunicarse y validarse en los niveles pertinentes. No es certificable: es una guía.

### ISO/IEC 31010 — Técnicas de evaluación del riesgo
Norma complementaria a la ISO 31000. Proporciona el catálogo de técnicas concretas para identificar y evaluar riesgos, incluida la **matriz de probabilidad-consecuencia** (matriz de calor) que es la base de la medición práctica.

### COSO ERM (2017) — Enterprise Risk Management
Marco de gestión integral del riesgo empresarial. Integra la gestión del riesgo con la estrategia y el desempeño. Aporta una **taxonomía de categorías de riesgo** (estratégico, operativo, de reportes, cumplimiento, financiero, reputacional, ambiental y social) que es útil para no dejar puntos ciegos.

### DAFP — Guía para la administración del riesgo y el diseño de controles en entidades públicas, V6 (2022)
Es el marco más pertinente para el GovLab por el contexto público colombiano. Toma como base ISO 31000 y COSO, y define con detalle: la **clasificación de riesgos**, los **factores de contexto** (interno, externo y del proceso), los **criterios para calificar probabilidad e impacto**, y la **zona de riesgo** que resulta de cruzar ambas variables. Está articulada con el Modelo Integrado de Planeación y Gestión (MIPG) y el esquema de líneas de defensa.

---

## 3. El proceso de gestión del riesgo

Tanto ISO 31000 como la guía del DAFP describen un proceso iterativo. En forma resumida:

1. **Establecer el contexto** — Entender el entorno interno, externo y del proceso, y los objetivos que el riesgo podría afectar.
2. **Identificar** — Reconocer los eventos que pueden ocurrir, sus causas (inmediatas y raíz) y las áreas de impacto.
3. **Analizar** — Estimar la probabilidad de ocurrencia y el nivel de impacto de cada riesgo.
4. **Valorar (evaluar)** — Cruzar probabilidad e impacto para ubicar el riesgo en una zona (baja, media, alta) y decidir prioridad. Esto produce el **riesgo inherente**.
5. **Tratar** — Definir controles y medidas de mitigación. Al aplicarlos se obtiene el **riesgo residual**.
6. **Monitorear, comunicar y consultar** — Actividades transversales a todo el proceso.

> En el resumidor de expedientes la herramienta cubre principalmente los pasos 2, 3 y 4 (identificar, analizar y valorar) y propone el paso 5 en la sección "Alternativas de Mitigación".

---

## 4. Tipos de riesgo (taxonomía)

Identificar **más de un tipo** de riesgo es lo que distingue un análisis superficial de uno completo. Combinando las categorías de COSO ERM y la clasificación del DAFP, estas son las categorías que la herramienta debe considerar:

| Categoría | Qué cubre | Ejemplo institucional |
|---|---|---|
| **Estratégico** | Direccionamiento, planeación, liderazgo, posicionamiento | Una iniciativa que desalinea a la universidad de su misión o de los benchmarks |
| **Operativo / De operación** | Ejecución de procesos, capacidad, proveedores, logística | Dependencia de un único proveedor o cuello de botella en un proceso clave |
| **Económico / Financiero** | Presupuesto, costos, sostenibilidad, retorno, liquidez | Sobrecostos o dependencia de una sola fuente de financiación |
| **Legal / Regulatorio / De cumplimiento** | Normativa, contratación, habeas data, propiedad intelectual | Incumplir requisitos del CNA o de protección de datos |
| **Reputacional** | Percepción de stakeholders, prensa, marca, alumni | Manejo mediático adverso que afecta la imagen Unisabana |
| **Administrativo / De gestión** | Estructura, roles, gobernanza, documentación, trazabilidad | Falta de claridad en responsabilidades o de soporte documental |
| **Tecnológico / De información** | Disponibilidad e integridad de datos, seguridad, continuidad | Pérdida de información o caída de una plataforma crítica |
| **De integridad / Corrupción** | Conflictos de interés, discrecionalidad, fraude | Discrecionalidad excesiva en una decisión sin controles |
| **Ambiental / Social (ESG)** | Impacto en comunidad, sostenibilidad, equidad | Efectos sociales no previstos de un proyecto |

> La guía del DAFP también clasifica los riesgos operativos por su origen: ejecución y administración de procesos, fraude interno, fraude externo y fallas tecnológicas. Esa subdivisión es útil cuando el expediente trata de un proceso operativo concreto.

---

## 5. Cómo se mide un riesgo: Probabilidad × Impacto

La medición práctica descansa en dos variables que se estiman para **cada** riesgo y luego se cruzan en una **matriz de calor**.

### 5.1 Probabilidad
Qué tan factible es que el riesgo ocurra. Puede expresarse en frecuencia (cuántas veces al año) o en porcentaje. Para la herramienta usamos una escala simple de tres niveles:

| Nivel | Lectura |
|---|---|
| **Baja** | Improbable; rara vez o nunca ha ocurrido en contextos similares |
| **Media** | Posible; podría ocurrir en algún momento |
| **Alta** | Probable; ocurre con frecuencia o las condiciones para que ocurra ya están presentes |

> La guía del DAFP utiliza cinco niveles (de "rara vez" hasta "casi seguro", con frecuencias asociadas). Para un resumen ejecutivo de dos páginas, tres niveles son suficientes y más legibles.

### 5.2 Impacto
Las consecuencias para la organización si el riesgo se materializa. El DAFP destaca dos grandes tipos de consecuencia: **económicas/presupuestales** y **reputacionales**, pero el impacto puede ser también operativo, legal o estratégico.

| Nivel | Lectura |
|---|---|
| **Bajo** | Consecuencias menores, absorbibles sin afectar objetivos |
| **Medio** | Consecuencias relevantes que exigen gestión, pero manejables |
| **Alto** | Consecuencias graves que amenazan la viabilidad o el cumplimiento de objetivos |

### 5.3 La matriz de calor
El **nivel del riesgo** (la "zona") resulta de cruzar probabilidad e impacto. Con una matriz 3×3:

| | Impacto Bajo | Impacto Medio | Impacto Alto |
|---|---|---|---|
| **Probabilidad Alta** | Medio | Alto | Alto |
| **Probabilidad Media** | Bajo | Medio | Alto |
| **Probabilidad Baja** | Bajo | Bajo | Medio |

Interpretación:
- **Riesgo Alto** — Amenaza la viabilidad o el logro de objetivos. Requiere acción y mitigación explícita.
- **Riesgo Medio** — Manejable, pero requiere atención y monitoreo.
- **Riesgo Bajo** — Tolerable; se monitorea sin acción inmediata.

> **Riesgo inherente vs. residual.** El nivel calculado antes de aplicar controles es el riesgo *inherente*. Tras aplicar controles eficaces, el riesgo baja a su nivel *residual*. La herramienta reporta el inherente y propone controles en la sección de mitigación.

---

## 6. Regla de calibración (clave para la herramienta)

El error más común es clasificar **todo** como alto o medio. Eso destruye el valor del análisis: si todo es prioritario, nada lo es.

Buenas prácticas que el `SYSTEM_PROMPT` aplica:

- Estimar **siempre** probabilidad e impacto antes de asignar el nivel; no asignar "alto" por inercia.
- **Declarar los riesgos bajos como bajos.** Identificar un riesgo bajo demuestra rigor, no debilidad.
- Buscar **diversidad de categorías**: un buen análisis toca 3-4 tipos distintos, no solo uno.
- Un expediente típico bien analizado suele mostrar una **mezcla** (p. ej. 1 alto, 2 medios, 1-2 bajos), no una columna uniforme.
- **Justificar** el nivel con una frase de probabilidad × impacto.

---

## 7. Cómo se refleja en el código

En `backend/services/claude_service.py`, el `SYSTEM_PROMPT`:

- Incluye una sección **"METODOLOGÍA DE ANÁLISIS DE RIESGOS"** con la taxonomía (sección 4) y la matriz probabilidad × impacto (sección 5).
- Indica al modelo identificar entre **3 y 6 riesgos de categorías distintas**.
- La plantilla HTML usa tres clases CSS ya existentes en `html_generator.py`: `risk-high` (rojo), `risk-medium` (ámbar) y `risk-low` (verde). Antes solo se usaban las dos primeras.
- Cada tarjeta muestra **`[CATEGORÍA] · RIESGO [NIVEL]`** y cierra con la valoración `(Probabilidad · Impacto)`.

---

## 8. Bibliografía

- Organización Internacional de Normalización. (2018). *ISO 31000:2018 — Gestión del riesgo. Directrices*. ISO/TC 262.
- Organización Internacional de Normalización. (2019). *ISO/IEC 31010 — Gestión del riesgo. Técnicas de evaluación del riesgo*.
- Committee of Sponsoring Organizations of the Treadway Commission. (2017). *Enterprise Risk Management — Integrating with Strategy and Performance (COSO ERM)*.
- Departamento Administrativo de la Función Pública (DAFP). (2022). *Guía para la administración del riesgo y el diseño de controles en entidades públicas — Versión 6*. Bogotá: DAFP, MINTIC y Secretaría de Transparencia. https://www.funcionpublica.gov.co/web/eva/biblioteca-virtual
- Departamento Administrativo de la Función Pública (DAFP). (2020). *Guía para la administración del riesgo y el diseño de controles en entidades públicas — Versión 5*. https://www.funcionpublica.gov.co/documents/418548/34150781/
- Superintendencia de Sociedades. (s. f.). *Guía de administración de riesgos institucionales (GC-G-002)*. https://www.supersociedades.gov.co
- Ley 1474 de 2011 (Estatuto Anticorrupción) y Ley 87 de 1993 (Sistema de Control Interno), Colombia.

---

*Laboratorio de Gobierno · Universidad de La Sabana — Documento metodológico del módulo de análisis de riesgos.*
