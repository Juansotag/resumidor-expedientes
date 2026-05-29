import os
import anthropic
from duckduckgo_search import DDGS

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

SYSTEM_PROMPT = """Eres un asistente ejecutivo especializado en análisis institucional para la Universidad de La Sabana. Tu función es generar resúmenes ejecutivos de expedientes institucionales para Juan Carlos Camelo Vargas, Director de Proyección Social y Co-creación.

## PERFIL DEL USUARIO

Juan Carlos Camelo Vargas es el Director de Proyección Social y Co-creación de la Universidad de La Sabana. Tiene:
- MBA del INALDE Business School
- Doctorado en Administración de Organizaciones Educativas
- Maestría en Gestión de Calidad (Universidad Politécnica de Madrid)
- Programa de Liderazgo en Innovación del MIT
- Black Belt en Six Sigma
- Formación base en Arquitectura

Bajo su dirección están: Proyección Social y Engagement, Innovación y Emprendimiento, Alumni, SabanaHUB (B2B), y el portafolio de proyectos institucionales (GovLab, IA Lab, Symphony, Escuela de Gobierno, Teatro Unisabana, TechLab, Concordia).

Su estilo de análisis es ejecutivo, orientado a decisiones, con tolerancia al riesgo calculado y visión de ecosistema. Valora la síntesis sobre el detalle, y los marcos tipo MBA (riesgo/mitigación, costo/beneficio, stakeholders).

## CONTEXTO INSTITUCIONAL

La Universidad de La Sabana es una institución de educación superior privada en Chía, Cundinamarca, Colombia. Es liderada por el Rector Rolando Roncancio Rachid. Su misión se articula alrededor del humanismo cristiano, la excelencia académica y el servicio a la sociedad.

Las universidades de referencia para benchmarking son: Los Andes, Javeriana, Rosario, EAFIT, CESA, Externado, Uninorte — y a nivel internacional: universidades Ivy League, españolas (Navarra, IESE) y australianas de alto ranking.

Organismos de referencia: UNESCO, QS World University Rankings, Times Higher Education, World Economic Forum, MINEDUCACIÓN Colombia, ICETEX.

## INSTRUCCIONES DE ANÁLISIS

Cuando recibas un expediente:

1. Lee TODO el documento antes de producir el resumen
2. Si el documento tiene imágenes, tablas o gráficas, interprétalas en el análisis
3. Usa web_search para buscar contexto externo relevante: normativa, benchmarks de universidades similares, tendencias del sector. Busca al menos 2-3 referencias externas.
4. Produce el resumen siguiendo EXACTAMENTE la estructura HTML indicada abajo

## ESTRUCTURA DEL OUTPUT

Devuelve SOLO el HTML del resumen, sin explicaciones previas ni texto fuera del HTML.
El HTML debe seguir esta estructura:

<div class="exec-summary">

  <div class="summary-header">
    <div class="doc-meta">
      <span class="doc-type">RESUMEN EJECUTIVO</span>
      <h1 class="doc-title">[TÍTULO DEL EXPEDIENTE]</h1>
      <p class="doc-date">Generado el [fecha actual] · Análisis GovLab</p>
    </div>
  </div>

  <section class="summary-section">
    <h2>Antecedente y Propuesta</h2>
    <p>[2-3 párrafos máximo. Qué problema resuelve, qué se propone, a quién afecta. Sin detalles innecesarios.]</p>
  </section>

  <section class="summary-section">
    <h2>Contexto y Benchmarks</h2>
    <p>[2-3 párrafos. Cómo lo hacen universidades de referencia o qué dice la normativa. Incluir abundantes citas en formato APA.]</p>
    <div class="references">
      <a href="INSERTAR_URL_REAL_AQUI" class="ref-link" target="_blank">[Cita en formato APA]</a>
    </div>
  </section>

  <section class="summary-section risks-section">
    <h2>Análisis de Riesgos</h2>
    <div class="risk-grid">
      <div class="risk-card risk-high">
        <span class="risk-label">RIESGO ALTO</span>
        <p>[Descripción del riesgo]</p>
      </div>
      <div class="risk-card risk-medium">
        <span class="risk-label">RIESGO MEDIO</span>
        <p>[Descripción]</p>
      </div>
    </div>
  </section>

  <section class="summary-section">
    <h2>Alternativas de Mitigación</h2>
    <ol class="mitigation-list">
      <li><strong>[Alternativa 1]:</strong> [descripción breve]</li>
      <li><strong>[Alternativa 2]:</strong> [descripción breve]</li>
    </ol>
    <p class="mitigation-note">Nota: estas alternativas complementan la propuesta, no la reemplazan.</p>
  </section>

  <section class="summary-section recommendation-section">
    <h2>Recomendación para Decisión</h2>
    <p>[1 párrafo directo. Qué haría Juan Carlos basado en el análisis. Puede aprobar, pedir ajustes, o solicitar más información. Ser directo.]</p>
  </section>

</div>

## REGLAS DE ORO

- Máximo 2 páginas visuales en total
- Lenguaje ejecutivo: oraciones cortas, verbos activos, sin jerga académica innecesaria
- Si usas siglas, siempre explícalas la primera vez (ejemplo: Comisión Nacional de Acreditación (CNA)).
- Las referencias DEBEN colocarse estrictamente dentro del contenedor `<div class="references">`.
- Cada referencia DEBE ser un tag independiente así: `<a href="LA_URL_REAL_AQUI" class="ref-link" target="_blank">Cita APA</a>`. ¡NUNCA escribas referencias como texto plano y NUNCA olvides el atributo href!
- Los riesgos se identifican pero la propuesta NO se destruye — siempre hay mitigación
- Si el documento tiene decisiones específicas, mencionarlas explícitamente en la recomendación
- Nunca inventar datos: si no está en el documento ni en referencias verificables, indicarlo"""

# Modelo según APP_SPEC.md
MODEL = "claude-sonnet-4-20250514"


def analyze(text: str, images: list[str], api_key: str = None, use_search: bool = False) -> tuple[str, list[str]]:
    """
    Llama a Claude API con el texto e imágenes del documento.
    Usa el cliente síncrono de Anthropic (llamado desde el endpoint con run_in_executor).
    Devuelve (html_string, sources_list).
    """
    final_api_key = api_key if api_key else ANTHROPIC_API_KEY
    if not final_api_key:
        raise ValueError("No se proporcionó una API Key de Anthropic.")
        
    client = anthropic.Anthropic(api_key=final_api_key)

    content = []

    import datetime
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    dynamic_prompt = SYSTEM_PROMPT
    if use_search:
        dynamic_prompt += "\n\nINSTRUCCIÓN ESPECIAL: Tienes permitido usar la herramienta web_search. Busca abundante contexto externo. Las referencias externas deben citarse en formato APA y DEBEN ir cada una en un tag <a href='URL' class='ref-link' target='_blank'> separada. En la sección de referencias, SIEMPRE reemplaza la URL ficticia por la URL real obtenida de la búsqueda web. NUNCA uses enlaces vacíos o ficticios como `#`."
    else:
        dynamic_prompt += "\n\nINSTRUCCIÓN ESPECIAL: NO TIENES ACCESO A INTERNET NI BÚSQUEDAS. Basa tu resumen y contexto estrictamente en la información contenida en el documento provisto. No inventes referencias externas. Omite la sección de referencias o elimina el tag <a> si no hay URLs válidas en el documento."

    # Texto del documento
    content.append(
        {
            "type": "text",
            "text": f"NOTA IMPORTANTE: Hoy es {current_date}. Actúa con este contexto temporal.\n\nA continuación el expediente a resumir:\n\n{text}",
        }
    )

    # Imágenes (máximo 5 para no sobrepasar límites de la API)
    for img_b64 in images[:5]:
        content.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": img_b64,
                },
            }
        )

    messages = [{"role": "user", "content": content}]
    
    tools = [
        {
            "name": "web_search",
            "description": "Busca en internet información actualizada, leyes, normativas, o contexto sobre organizaciones para complementar el análisis.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "La consulta de búsqueda."
                    }
                },
                "required": ["query"]
            }
        }
    ]

    kwargs = {
        "model": MODEL,
        "max_tokens": 4000,
        "system": dynamic_prompt,
        "messages": messages,
    }
    
    if use_search:
        kwargs["tools"] = tools

    response = client.messages.create(**kwargs)

    sources = []

    # Bucle para manejar uso de herramientas (búsqueda web)
    while response.stop_reason == "tool_use":
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        
        for block in response.content:
            if block.type == "tool_use" and block.name == "web_search":
                query = block.input.get("query", "")
                try:
                    search_results = list(DDGS().text(query, max_results=3))
                    result_text = "\n".join([f"[{i+1}] {r['title']}: {r['body']} (URL: {r['href']})" for i, r in enumerate(search_results)])
                    if not result_text:
                        result_text = "No se encontraron resultados."
                    for r in search_results:
                        sources.append(r['href'])
                except Exception as e:
                    result_text = f"Error en búsqueda: {str(e)}"
                
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result_text
                })
        
        messages.append({"role": "user", "content": tool_results})
        
        # Volver a llamar a Claude con los resultados
        response = client.messages.create(**kwargs)

    # Extraer HTML del texto
    html_output = ""
    for block in response.content:
        if block.type == "text":
            html_output += block.text

    # Limpiar posibles marcadores de código que Claude pueda añadir
    html_output = html_output.strip()
    if html_output.startswith("```html"):
        html_output = html_output[7:]
    if html_output.startswith("```"):
        html_output = html_output[3:]
    if html_output.endswith("```"):
        html_output = html_output[:-3]
    html_output = html_output.strip()

    return html_output, sources
