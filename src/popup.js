// Popup script - Atualiza status do modelo

const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');

// Verifica status inicial
const checkModelStatus = () => {
  chrome.runtime.sendMessage(
    { type: 'CHECK_MODEL' },
    (response) => {
      if (response?.ready) {
        updateStatus(true);
      } else {
        updateStatus(false);
      }
    }
  );
};

// Listener para quando o modelo ficar pronto
chrome.runtime.onMessage.addListener((request) => {
  if (request.type === 'MODEL_READY') {
    updateStatus(true);
  }
});

const updateStatus = (isReady) => {
  if (isReady) {
    statusDot.classList.add('ready');
    statusText.textContent = '✓ Pronto para usar!';
  } else {
    statusDot.classList.remove('ready');
    statusText.textContent = '⏳ Carregando modelo...';
  }
};

// Verifica status quando abre a popup
document.addEventListener('DOMContentLoaded', checkModelStatus);

// Recarrega status a cada 2 segundos enquanto carrega
const statusCheckInterval = setInterval(() => {
  checkModelStatus();
}, 2000);

// Para de verificar depois de 2 minutos
setTimeout(() => {
  clearInterval(statusCheckInterval);
}, 120000);
