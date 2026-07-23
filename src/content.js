// Content Script - Detecta e marca LaTeX nos PDFs e páginas HTML

// Regex para detectar expressões LaTeX (inline e display)
const LATEX_INLINE_REGEX = /\$([^\$\n]+?)\$/g;
const LATEX_DISPLAY_REGEX = /\$\$([^\$\n]+?)\$\$/g;

const initializeLatexDetection = () => {
  // Detecta se é um PDF (via PDF.js viewer)
  const isPdfPage = document.querySelector('iframe[src*="viewer.html"]') !== null
    || document.querySelector('#viewer') !== null;

  if (isPdfPage) {
    observePdfContent();
  } else {
    processHtmlContent();
  }
};

// Processa conteúdo HTML regular
const processHtmlContent = () => {
  const walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    null,
    false
  );

  let node;
  const nodesToProcess = [];

  while (node = walker.nextNode()) {
    // Evita script/style tags e já processados
    if (node.parentElement?.classList.contains('latex-processed')) continue;
    if (node.parentElement?.tagName === 'SCRIPT') continue;
    if (node.parentElement?.tagName === 'STYLE') continue;

    if (LATEX_INLINE_REGEX.test(node.textContent) || LATEX_DISPLAY_REGEX.test(node.textContent)) {
      nodesToProcess.push(node);
    }
  }

  nodesToProcess.forEach(node => replaceLatexInNode(node));
};

// Substitui LaTeX por elementos clicáveis
const replaceLatexInNode = (node) => {
  const parent = node.parentElement;
  if (!parent) return;

  let html = parent.innerHTML;
  let modified = false;

  // Processa expressões display ($$...$$ )
  html = html.replace(LATEX_DISPLAY_REGEX, (match, latex) => {
    modified = true;
    return createLatexElement(latex, 'display');
  });

  // Processa expressões inline ($...$)
  html = html.replace(LATEX_INLINE_REGEX, (match, latex) => {
    modified = true;
    return createLatexElement(latex, 'inline');
  });

  if (modified) {
    parent.innerHTML = html;
    parent.classList.add('latex-processed');
    attachLatexListeners(parent);
  }
};

const createLatexElement = (latex, type) => {
  const sanitized = escapeHtml(latex.trim());
  const className = type === 'display' ? 'latex-display' : 'latex-inline';
  return `<span class="latex-expr ${className}" data-latex="${sanitized}" role="button" tabindex="0" title="Clique para explicar">$$${sanitized}$$</span>`;
};

// Anexa listeners aos elementos LaTeX
const attachLatexListeners = (container) => {
  container.querySelectorAll('.latex-expr').forEach(elem => {
    if (elem.hasListener) return;

    elem.addEventListener('click', handleLatexClick);
    elem.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' || e.key === ' ') handleLatexClick.call(elem);
    });

    elem.hasListener = true;
  });
};

const handleLatexClick = async (e) => {
  e.stopPropagation();
  const latex = this.dataset.latex;

  // Mostra estado de carregamento
  this.classList.add('loading');
  this.textContent = '⏳ Explicando...';

  try {
    // Envia mensagem para o background service worker
    chrome.runtime.sendMessage(
      { type: 'EXPLAIN_LATEX', latex },
      (response) => {
        if (response.error) {
          showExplanationPopup(latex, `❌ ${response.error}`, true);
        } else {
          showExplanationPopup(latex, response.explanation);
        }
        this.classList.remove('loading');
        this.innerHTML = `$$${latex}$$`;
      }
    );
  } catch (error) {
    console.error('Erro ao solicitar explicação:', error);
    this.classList.remove('loading');
    this.innerHTML = `$$${latex}$$`;
  }
};

// Cria e exibe popup com explicação
const showExplanationPopup = (latex, explanation, isError = false) => {
  let popup = document.getElementById('latex-explanation-popup');

  if (!popup) {
    popup = document.createElement('div');
    popup.id = 'latex-explanation-popup';
    document.body.appendChild(popup);
  }

  popup.innerHTML = `
    <div class="explanation-content ${isError ? 'error' : ''}">
      <button class="close-btn" aria-label="Fechar">&times;</button>
      <div class="latex-header">$$${escapeHtml(latex)}$$</div>
      <div class="explanation-text">${escapeHtml(explanation)}</div>
    </div>
  `;

  popup.style.display = 'block';
  popup.querySelector('.close-btn').addEventListener('click', () => {
    popup.style.display = 'none';
  });

  // Fecha ao clicar fora
  popup.addEventListener('click', (e) => {
    if (e.target === popup) popup.style.display = 'none';
  });
};

const escapeHtml = (text) => {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
};

// Observer para mudanças dinâmicas no DOM (PDFs com scroll lazy-load)
const observePdfContent = () => {
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.addedNodes.length) {
        mutation.addedNodes.forEach(node => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            processElement(node);
          }
        });
      }
    });
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
    characterData: false
  });

  // Processa conteúdo inicial
  processHtmlContent();
};

const processElement = (element) => {
  if (element.textContent && (LATEX_INLINE_REGEX.test(element.textContent) || LATEX_DISPLAY_REGEX.test(element.textContent))) {
    replaceLatexInNode(element);
  }
};

// Inicia detecção quando DOM está pronto
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeLatexDetection);
} else {
  initializeLatexDetection();
}
