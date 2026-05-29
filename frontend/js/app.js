/* ================================================================
   app.js — Lógica principal de resume-expedientes
   GovLab · Universidad de La Sabana
   ================================================================ */

// ---- Estado global ----
const AppState = {
  IDLE: 'idle',
  LOADING: 'loading',
  RESULT: 'result',
  ERROR: 'error',
};

let currentState = AppState.IDLE;
let selectedFile = null;
let lastResultHTML = '';

// ---- Mensajes rotativos de carga ----
const LOADING_MESSAGES = [
  'Leyendo el expediente...',
  'Analizando el contexto institucional...',
  'Consultando referencias externas...',
  'Elaborando el resumen ejecutivo...',
];

let loadingMsgIndex = 0;
let loadingMsgInterval = null;

// ---- Referencias DOM ----
const stateIdle    = document.getElementById('state-idle');
const stateLoading = document.getElementById('state-loading');
const stateResult  = document.getElementById('state-result');
const stateError   = document.getElementById('state-error');

const dropzone          = document.getElementById('dropzone');
const fileInput         = document.getElementById('file-input');
const btnSelectMobile   = document.getElementById('btn-select-mobile');
const fileSelectedInfo  = document.getElementById('file-selected-info');
const fileNameDisplay   = document.getElementById('file-name-display');
const btnAnalyze        = document.getElementById('btn-analyze');
const toastError        = document.getElementById('toast-error');
const toastMessage      = document.getElementById('toast-message');

const loadingMessageEl  = document.getElementById('loading-message');
const resultContent     = document.getElementById('result-content');
const errorMessageEl    = document.getElementById('error-message');

const btnNewQuery       = document.getElementById('btn-new-query');
const btnDownloadPdf    = document.getElementById('btn-download-pdf');
const btnShare          = document.getElementById('btn-share');
const btnRetry          = document.getElementById('btn-retry');

const footerYear        = document.getElementById('footer-year');

// ---- Inicialización ----
document.addEventListener('DOMContentLoaded', () => {
  footerYear.textContent = new Date().getFullYear();
  setupDropzone();
  setupButtons();
  
  const savedApiKey = localStorage.getItem('anthropic_api_key');
  const apiKeyInput = document.getElementById('api-key-input');
  if (savedApiKey && apiKeyInput) {
    apiKeyInput.value = savedApiKey;
  }

  setState(AppState.IDLE);
});

// ---- Cambio de estado ----
function setState(state) {
  currentState = state;

  // Quitar .active de todos los estados — el CSS base `.app-state { display:none !important }` los oculta
  [stateIdle, stateLoading, stateResult, stateError].forEach(el => {
    el.classList.remove('active');
  });

  // Activar solo el estado deseado
  const stateMap = {
    [AppState.IDLE]:    stateIdle,
    [AppState.LOADING]: stateLoading,
    [AppState.RESULT]:  stateResult,
    [AppState.ERROR]:   stateError,
  };

  const activeEl = stateMap[state];
  if (activeEl) {
    activeEl.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Gestionar mensajes de loading y countdown
  if (state === AppState.LOADING) {
    startLoadingMessages();
    startCountdown();
  } else {
    stopLoadingMessages();
    stopCountdown();
  }
}

// ---- Mensajes rotativos ----
function startLoadingMessages() {
  loadingMsgIndex = 0;
  loadingMessageEl.textContent = LOADING_MESSAGES[0];

  loadingMsgInterval = setInterval(() => {
    loadingMsgIndex = (loadingMsgIndex + 1) % LOADING_MESSAGES.length;
    loadingMessageEl.style.opacity = '0';
    setTimeout(() => {
      loadingMessageEl.textContent = LOADING_MESSAGES[loadingMsgIndex];
      loadingMessageEl.style.opacity = '1';
    }, 300);
  }, 5000);
}

function stopLoadingMessages() {
  if (loadingMsgInterval) {
    clearInterval(loadingMsgInterval);
    loadingMsgInterval = null;
  }
}

// ---- Countdown timer (60 → 0) ----
let countdownInterval = null;
const COUNTDOWN_TOTAL = 60;
// Circunferencia real del arco SVG: 2π × r=20 mapeado al viewBox 48px → escala 80/48
// stroke-dasharray en el CSS = 125.66 (≈ 2π × 20 × 80/48)
const DASH_TOTAL = 125.66;

const countdownNumberEl = document.getElementById('countdown-number');
const countdownArcEl    = document.getElementById('countdown-progress');

function startCountdown() {
  stopCountdown();
  let remaining = COUNTDOWN_TOTAL;

  // Estado inicial
  _updateCountdown(remaining);

  countdownInterval = setInterval(() => {
    remaining -= 1;

    if (remaining < 0) {
      // El proceso tardó más de 60 s — seguimos en 0 sin detenernos
      remaining = 0;
    }

    _updateCountdown(remaining);
  }, 1000);
}

function stopCountdown() {
  if (countdownInterval) {
    clearInterval(countdownInterval);
    countdownInterval = null;
  }
}

function _updateCountdown(remaining) {
  // Número
  countdownNumberEl.textContent = remaining;

  // Arco SVG: lleno al inicio, vacío al final
  const fraction = remaining / COUNTDOWN_TOTAL;
  const offset   = DASH_TOTAL * (1 - fraction); // 0 = lleno, DASH_TOTAL = vacío
  countdownArcEl.style.strokeDashoffset = offset;

  // Cambiar a rojo en los últimos 10 segundos
  const urgent = remaining <= 10;
  countdownArcEl.classList.toggle('urgent', urgent);
  countdownNumberEl.classList.toggle('urgent', urgent);
}

// ---- Setup Dropzone ----
function setupDropzone() {
  // Click en dropzone abre selector de archivo
  dropzone.addEventListener('click', (e) => {
    if (e.target === btnSelectMobile || btnSelectMobile.contains(e.target)) return;
    fileInput.click();
  });

  // Enter / Space en dropzone para accesibilidad
  dropzone.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      fileInput.click();
    }
  });

  // Drag events
  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
  });

  dropzone.addEventListener('dragleave', (e) => {
    if (!dropzone.contains(e.relatedTarget)) {
      dropzone.classList.remove('dragover');
    }
  });

  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelection(files[0]);
    }
  });

  // File input change
  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
      handleFileSelection(fileInput.files[0]);
    }
  });
}

// ---- Setup botones ----
function setupButtons() {
  // Mobile upload button
  btnSelectMobile.addEventListener('click', (e) => {
    e.stopPropagation();
    fileInput.click();
  });

  // Analizar
  btnAnalyze.addEventListener('click', () => {
    if (selectedFile) {
      analyzeFile(selectedFile);
    }
  });

  // Nueva consulta
  btnNewQuery.addEventListener('click', () => {
    resetToIdle();
  });

  // Reintentar desde error
  btnRetry.addEventListener('click', () => {
    if (selectedFile) {
      analyzeFile(selectedFile);
    } else {
      resetToIdle();
    }
  });

  // Descargar PDF
  btnDownloadPdf.addEventListener('click', () => {
    exportToPDF(resultContent, lastResultHTML);
  });

  // Compartir
  btnShare.addEventListener('click', () => {
    shareResult(lastResultHTML);
  });
}

// ---- Validación y selección de archivo ----
const ALLOWED_EXTENSIONS = ['pdf', 'docx', 'doc', 'png', 'jpg', 'jpeg'];
const MAX_SIZE_BYTES = 20 * 1024 * 1024; // 20 MB

function handleFileSelection(file) {
  // Limpiar errores previos
  hideToast();

  const ext = file.name.split('.').pop().toLowerCase();

  if (!ALLOWED_EXTENSIONS.includes(ext)) {
    showToast('Formato no soportado. Usa PDF, Word o imagen (PNG, JPG).');
    return;
  }

  if (file.size > MAX_SIZE_BYTES) {
    showToast('El archivo es muy grande. Máximo 20 MB.');
    return;
  }

  // Archivo válido
  selectedFile = file;
  fileNameDisplay.textContent = file.name;
  fileSelectedInfo.classList.remove('hidden');
}

// ---- Llamada a la API ----
async function analyzeFile(file) {
  setState(AppState.LOADING);
  hideToast();

  const formData = new FormData();
  formData.append('file', file);

  const apiKeyInput = document.getElementById('api-key-input');
  if (apiKeyInput && apiKeyInput.value.trim() !== '') {
    formData.append('api_key', apiKeyInput.value.trim());
    localStorage.setItem('anthropic_api_key', apiKeyInput.value.trim());
  }

  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      const errMsg = data?.detail?.message || data?.message || 'Ocurrió un error al procesar el expediente.';
      showError(errMsg);
      return;
    }

    if (data.status === 'ok' && data.html) {
      lastResultHTML = data.html;
      resultContent.innerHTML = data.html;
      setState(AppState.RESULT);
    } else {
      showError('No se pudo generar el resumen. Intenta de nuevo.');
    }
  } catch (err) {
    console.error('Error de red:', err);
    showError('No se pudo conectar con el servidor. Verifica tu conexión e intenta de nuevo.');
  }
}

// ---- Helpers de estado ----
function resetToIdle() {
  selectedFile = null;
  lastResultHTML = '';
  fileInput.value = '';
  fileNameDisplay.textContent = '';
  fileSelectedInfo.classList.add('hidden');
  resultContent.innerHTML = '';
  hideToast();
  setState(AppState.IDLE);
}

function showError(message) {
  errorMessageEl.textContent = message;
  setState(AppState.ERROR);
}

function showToast(message) {
  toastMessage.textContent = message;
  toastError.classList.remove('hidden');
}

function hideToast() {
  toastError.classList.add('hidden');
  toastMessage.textContent = '';
}
