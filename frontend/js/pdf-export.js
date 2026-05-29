/* ================================================================
   pdf-export.js — Exportar resultado como PDF
   Estrategia:
     Desktop → html2pdf.js (conversión en browser)
     Mobile  → window.print() con print.css (nativo del SO)
   GovLab · Universidad de La Sabana
   ================================================================ */

/**
 * Exporta el resumen. Detecta mobile/desktop y elige la mejor estrategia.
 * @param {HTMLElement} containerEl - El elemento con el resumen
 * @param {string} htmlContent      - HTML string del resumen (para fallback)
 */
async function exportToPDF(containerEl, htmlContent) {
  const btnPdf = document.getElementById('btn-download-pdf');
  const originalHTML = btnPdf.innerHTML;

  // UI: estado cargando
  btnPdf.disabled = true;
  btnPdf.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
         fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
         style="animation:spin 0.9s linear infinite">
      <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
    </svg>
    <span class="action-label">Generando...</span>`;

  try {
    if (isMobile()) {
      // En mobile: usar el diálogo de impresión nativo del SO
      // Android Chrome → "Guardar como PDF"
      // iOS Safari    → "Imprimir" (puede enviar a AirPrint o Guardar PDF)
      window.print();
    } else if (typeof html2pdf !== 'undefined') {
      await generateWithHtml2PDF(containerEl);
    } else {
      downloadAsHTML(htmlContent);
    }
  } catch (err) {
    console.warn('Error en exportToPDF, usando fallback HTML:', err);
    downloadAsHTML(htmlContent);
  } finally {
    btnPdf.disabled = false;
    btnPdf.innerHTML = originalHTML;
  }
}

/**
 * Genera y descarga un PDF con html2pdf.js (desktop).
 */
async function generateWithHtml2PDF(containerEl) {
  const filename = `Resumen_Ejecutivo_GovLab_${formatDateForFilename()}.pdf`;

  const options = {
    margin: [12, 12, 12, 12],
    filename,
    image: { type: 'jpeg', quality: 1.0 },
    html2canvas: { scale: 2, useCORS: true, logging: false, backgroundColor: '#dde6f5' },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
    pagebreak: { mode: ['avoid-all', 'css', 'legacy'] },
  };

  // Prevenir que la animación fadeIn cause semitransparencia al tomar la captura
  const oldAnimation = containerEl.style.animation;
  const oldOpacity = containerEl.style.opacity;
  containerEl.style.animation = 'none';
  containerEl.style.opacity = '1';

  try {
    await html2pdf().set(options).from(containerEl).save();
  } catch (e) {
    console.error("Error generating PDF:", e);
    throw e;
  } finally {
    containerEl.style.animation = oldAnimation;
    containerEl.style.opacity = oldOpacity;
  }
}

/**
 * Genera un PDF como Blob (para compartir por Web Share API).
 * Solo disponible en desktop con html2pdf.
 * @returns {Blob|null}
 */
async function generatePDFBlob(containerEl) {
  if (typeof html2pdf === 'undefined') return null;

  const options = {
    margin: [12, 12, 12, 12],
    filename: `Resumen_Ejecutivo_GovLab_${formatDateForFilename()}.pdf`,
    image: { type: 'jpeg', quality: 1.0 },
    html2canvas: { scale: 2, useCORS: true, logging: false, backgroundColor: '#dde6f5' },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
    pagebreak: { mode: ['avoid-all', 'css', 'legacy'] },
  };

  const oldAnimation = containerEl.style.animation;
  const oldOpacity = containerEl.style.opacity;
  containerEl.style.animation = 'none';
  containerEl.style.opacity = '1';

  try {
    const pdf = await html2pdf().set(options).from(containerEl).outputPdf('blob');
    return pdf;
  } catch (e) {
    console.error("Error generating PDF blob:", e);
    return null;
  } finally {
    containerEl.style.animation = oldAnimation;
    containerEl.style.opacity = oldOpacity;
  }
}

/**
 * Descarga el contenido como archivo HTML (último recurso).
 */
function downloadAsHTML(htmlContent) {
  const filename = `Resumen_Ejecutivo_GovLab_${formatDateForFilename()}.html`;
  const fullHTML = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>Resumen Ejecutivo · GovLab</title>
  <link href="https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400;500;600;700&display=swap" rel="stylesheet"/>
  <style>body{margin:2rem auto;max-width:800px;padding:0 1rem;background:#fff;}</style>
</head>
<body>${htmlContent}</body>
</html>`;
  const blob = new Blob([fullHTML], { type: 'text/html;charset=utf-8' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href = url; a.download = filename; a.click();
  URL.revokeObjectURL(url);
}

/** Detecta si es mobile (táctil + ancho < 768px) */
function isMobile() {
  return window.matchMedia('(max-width: 768px)').matches
      || ('ontouchstart' in window);
}

function formatDateForFilename() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}
