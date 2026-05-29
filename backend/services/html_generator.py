CSS_INLINE = """<style>
  @import url('https://fonts.googleapis.com/css2?family=Libre+Franklin:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');
  .exec-summary { font-family: 'Libre Franklin', sans-serif; color: #00135B; max-width: 760px; margin: 0 auto; }
  .summary-header { border-bottom: 3px solid #00135B; padding-bottom: 1rem; margin-bottom: 2rem; }
  .doc-type { font-size: 0.75rem; letter-spacing: 0.1em; color: #64748b; text-transform: uppercase; display: block; }
  .doc-title { font-family: 'Publico Banner', 'Playfair Display', serif; font-size: 1.75rem; margin: 0.5rem 0; color: #00135B; line-height: 1.3; }
  .doc-date { font-size: 0.8rem; color: #64748b; margin: 0; }
  .summary-section { margin-bottom: 2rem; }
  .summary-section h2 { font-size: 0.8rem; letter-spacing: 0.08em; text-transform: uppercase; color: #00387D; border-bottom: 1px solid #D9E1EF; padding-bottom: 0.4rem; margin-bottom: 1rem; font-family: 'Libre Franklin', sans-serif; font-weight: 700; }
  .summary-section p { line-height: 1.75; margin-bottom: 0.75rem; font-size: 0.875rem; color: #374151; }
  .risk-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  .risk-card { border-radius: 8px; padding: 1rem; }
  .risk-high { background: #fff0f0; border-left: 4px solid #d51437; }
  .risk-medium { background: #fff8ed; border-left: 4px solid #f8a719; }
  .risk-low { background: #f0fdf4; border-left: 4px solid #2b8d04; }
  .risk-label { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; display: block; margin-bottom: 0.5rem; }
  .risk-high .risk-label { color: #d51437; }
  .risk-medium .risk-label { color: #f8a719; }
  .risk-low .risk-label { color: #2b8d04; }
  .risk-card p { font-size: 0.82rem; line-height: 1.6; margin: 0; color: #374151; }
  .mitigation-list { padding-left: 1.5rem; margin: 0; }
  .mitigation-list li { margin-bottom: 0.75rem; font-size: 0.875rem; color: #374151; line-height: 1.7; }
  .mitigation-note { font-size: 0.8rem; color: #64748b; font-style: italic; margin-top: 0.5rem; }
  .recommendation-section { background: #EEF2F8; border-radius: 12px; padding: 1.5rem; }
  .recommendation-section h2 { border-bottom-color: #93AAC9; }
  .references { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.75rem; }
  .ref-link { background: #D9E1EF; color: #00135B; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.78rem; text-decoration: none; transition: background 0.2s; }
  .ref-link:hover { background: #93AAC9; }
  @media (max-width: 640px) { .risk-grid { grid-template-columns: 1fr; } .doc-title { font-size: 1.4rem; } }
</style>"""


def wrap(html_content: str) -> str:
    """Envuelve el HTML generado por Claude con estilos inline GovLab."""
    return CSS_INLINE + "\n" + html_content
