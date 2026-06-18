/* ================================================================
   share.js — Compartir el resumen ejecutivo
   Estrategia:
     1. Si mobile + navigator.share con files → comparte PDF como archivo
     2. Si navigator.share sin files       → comparte texto/URL
     3. Fallback desktop                   → copia HTML al portapapeles
   GovLab · Universidad de La Sabana
   ================================================================ */

/**
 * Intenta compartir el resumen de la mejor forma según el dispositivo.
 * @param {string} htmlContent - HTML del resumen
 */
async function shareResult(htmlContent) {
  const feedback = document.getElementById('share-feedback');
  const resultEl = document.getElementById('result-content');

  // --- Opción A: Web Share API con PDF (mobile moderno) ---
  if (navigator.canShare) {
    try {
      // Intentar generar PDF para compartir como archivo
      let pdfBlob = null;
      try { pdfBlob = await generatePDFBlob(resultEl); } catch (_) {}

      if (pdfBlob && navigator.canShare({ files: [new File([pdfBlob], 'resumen.pdf', { type: 'application/pdf' })] })) {
        const filename = typeof getExportFilename !== 'undefined'
          ? getExportFilename(resultEl, 'pdf')
          : `Resumen_Ejecutivo_GovLab_${formatDateForFilename()}.pdf`;
        const file = new File(
          [pdfBlob],
          filename,
          { type: 'application/pdf' }
        );
        await navigator.share({
          title: 'Resumen Ejecutivo — GovLab UniSabana',
          text: 'Adjunto el resumen ejecutivo generado por resume-expedientes · GovLab.',
          files: [file],
        });
        return; // éxito
      }
    } catch (err) {
      if (err.name === 'AbortError') return; // usuario canceló
      // Continuar con siguiente opción
    }
  }

  // --- Opción B: Web Share API sin archivo (mobile básico) ---
  if (navigator.share) {
    try {
      await navigator.share({
        title: 'Resumen Ejecutivo — GovLab UniSabana',
        text: stripHTML(htmlContent).slice(0, 500) + '...',
      });
      return;
    } catch (err) {
      if (err.name === 'AbortError') return;
    }
  }

  // --- Opción C: Copiar HTML al portapapeles (desktop) ---
  try {
    await copyToClipboard(htmlContent);
    showFeedback(feedback, '✓ HTML copiado al portapapeles');
  } catch {
    try {
      await copyToClipboard(stripHTML(htmlContent));
      showFeedback(feedback, '✓ Texto copiado al portapapeles');
    } catch {
      showFeedback(feedback, '✗ No se pudo copiar');
    }
  }
}

async function copyToClipboard(text) {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
  } else {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;opacity:0;pointer-events:none';
    document.body.appendChild(ta);
    ta.focus(); ta.select();
    const ok = document.execCommand('copy');
    document.body.removeChild(ta);
    if (!ok) throw new Error('execCommand falló');
  }
}

function showFeedback(el, message) {
  el.textContent = message;
  el.classList.remove('hidden');
  el.style.animation = 'none';
  el.offsetHeight; // reflow
  el.style.animation = '';
  setTimeout(() => el.classList.add('hidden'), 2500);
}

function stripHTML(html) {
  const tmp = document.createElement('div');
  tmp.innerHTML = html;
  return tmp.textContent || tmp.innerText || '';
}
