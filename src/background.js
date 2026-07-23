// Background Service Worker - carrega e gerencia o modelo de IA

let model = null;
let isModelLoading = false;

const initModel = async () => {
  if (model || isModelLoading) return;

  isModelLoading = true;
  try {
    // Usando transformers.js com WebGPU
    const { pipeline } = await import('https://cdn.jsdelivr.net/npm/@xenova/transformers');

    // MathBERTa: Especializado em LaTeX, muito compacto (110MB)
    // Treinado especificamente para entender expressões matemáticas
    try {
      model = await pipeline(
        'feature-extraction',
        'Xenova/mathberta',
        { device: 'webgpu', quantized: true }
      );
      console.log('✓ MathBERTa carregado (110MB, ultra-rápido)');
    } catch (err) {
      console.log('MathBERTa indisponível, usando Flan-T5...');
      // Fallback para modelo genérico
      model = await pipeline(
        'text2text-generation',
        'Xenova/flan-t5-small',
        { device: 'webgpu', quantized: true }
      );
      console.log('✓ Flan-T5-small carregado (250MB)');
    }

    chrome.runtime.sendMessage({ type: 'MODEL_READY' });
  } catch (error) {
    console.error('Erro ao carregar modelo:', error);
    isModelLoading = false;
  }
};

// Inicializa o modelo quando a extensão abre
chrome.runtime.onInstalled.addListener(() => {
  initModel();
});

// Listener para requisições de explicação
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'EXPLAIN_LATEX') {
    explainLatex(request.latex).then(sendResponse);
    return true; // Mantém o canal aberto para resposta assíncrona
  }

  if (request.type === 'CHECK_MODEL') {
    sendResponse({ ready: model !== null });
    return true;
  }
});

const explainLatex = async (latexExpr) => {
  if (!model) {
    await initModel();
  }

  if (!model) {
    return {
      error: 'Modelo não carregou. Tente recarregar a página.',
      latex: latexExpr
    };
  }

  try {
    // Prompt otimizado para modelos matemáticos
    const prompt = `Explique brevemente esta expressão LaTeX em português:

LaTeX: ${latexExpr}

Responda em 2-3 linhas:
- Significado
- Componentes principais (se houver)
- Contexto de uso`;

    const result = await model(prompt, {
      max_new_tokens: 128,
      temperature: 0.5, // Mais determinístico para matemática
      do_sample: true
    });

    // Extrair apenas o texto gerado (não incluir prompt)
    const generatedText = typeof result === 'string'
      ? result
      : result[0]?.generated_text || result[0]?.summary_text || JSON.stringify(result);

    return {
      latex: latexExpr,
      explanation: generatedText.trim(),
      error: null
    };
  } catch (error) {
    console.error('Erro ao explicar LaTeX:', error);
    return {
      latex: latexExpr,
      error: 'Erro ao gerar explicação',
      explanation: null
    };
  }
};
