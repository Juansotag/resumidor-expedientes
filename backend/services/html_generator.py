CSS_INLINE = """<style>
  @import url('https://fonts.googleapis.com/css2?family=Libre+Franklin:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');
  .exec-summary { font-family: 'Libre Franklin', sans-serif; color: #00135B !important; max-width: 760px; margin: 0 auto; background-color: #dde6f5 !important; padding: 2rem; border-radius: 12px; }
  .summary-header { border-bottom: 3px solid #00135B; padding-bottom: 1rem; margin-bottom: 2rem; }
  .doc-type { font-size: 0.75rem; letter-spacing: 0.1em; color: #64748b !important; text-transform: uppercase; display: block; }
  .doc-title { font-family: 'Publico Banner', 'Playfair Display', serif; font-size: 1.75rem; margin: 0.5rem 0; color: #00135B !important; line-height: 1.3; }
  .doc-date { font-size: 0.8rem; color: #64748b !important; margin: 0; }
  .summary-section { margin-bottom: 2rem; }
  .summary-section h2 { font-size: 0.8rem; letter-spacing: 0.08em; text-transform: uppercase; color: #00387D !important; border-bottom: 1px solid #93AAC9; padding-bottom: 0.4rem; margin-bottom: 1rem; font-family: 'Libre Franklin', sans-serif; font-weight: 700; }
  .summary-section p { line-height: 1.75; margin-bottom: 0.75rem; font-size: 0.875rem; color: #000000 !important; }
  .risk-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  .risk-card { border-radius: 8px; padding: 1rem; }
  .risk-high { background: #fff0f0 !important; border-left: 4px solid #d51437 !important; }
  .risk-medium { background: #fff8ed !important; border-left: 4px solid #f8a719 !important; }
  .risk-low { background: #f0fdf4 !important; border-left: 4px solid #2b8d04 !important; }
  .risk-label { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; display: block; margin-bottom: 0.5rem; }
  .risk-high .risk-label { color: #d51437 !important; }
  .risk-medium .risk-label { color: #f8a719 !important; }
  .risk-low .risk-label { color: #2b8d04 !important; }
  .risk-card p { font-size: 0.82rem; line-height: 1.6; margin: 0; color: #000000 !important; }
  .mitigation-list { padding-left: 1.5rem; margin: 0; }
  .mitigation-list li { margin-bottom: 0.75rem; font-size: 0.875rem; color: #000000 !important; line-height: 1.7; }
  .mitigation-note { font-size: 0.8rem; color: #64748b !important; font-style: italic; margin-top: 0.5rem; }
  .recommendation-section { background: #EEF2F8 !important; border-radius: 12px; padding: 1.5rem; }
  .recommendation-section h2 { border-bottom-color: #93AAC9; }
  .references { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.75rem; }
  .ref-link { background: #D9E1EF !important; color: #00135B !important; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.78rem; text-decoration: none; transition: background 0.2s; }
  .ref-link:hover { background: #93AAC9 !important; }
  @media (max-width: 640px) { .risk-grid { grid-template-columns: 1fr; } .doc-title { font-size: 1.4rem; } }
</style>"""


def wrap(html_content: str) -> str:
    """Envuelve el HTML generado por Claude con estilos inline GovLab."""
    return CSS_INLINE + "\n" + html_content
