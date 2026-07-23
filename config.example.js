/**
 * Configurações da Extensão LaTeX Explainer
 *
 * Copie este arquivo para 'config.js' e customize conforme necessário
 * ou edite diretamente no background.js
 */

const CONFIG = {
  // Modelo de IA a usar
  MODEL: {
    // Opções recomendadas para matemática:
    // 'Xenova/LLaMA-2-7B-Math-hf'  - Melhor qualidade (~7GB)
    // 'Xenova/Mistral-7B-Math'      - Rápido e preciso (~7GB)
    // 'Xenova/mathberta'            - Compacto (~110MB)
    // 'Xenova/flan-t5-small'        - Rápido, baixa memória (~250MB)
    // 'Xenova/flan-t5-base'         - Bom custo-benefício (~900MB)

    primary: 'Xenova/LLaMA-2-7B-Math-hf',
    fallback: 'Xenova/flan-t5-small',
    task: 'text-generation',  // ou 'text2text-generation' para Flan-T5
    device: 'webgpu',
    quantized: true,  // Usa versão quantizada (mais rápida, menos memória)
  },

  // Configurações de geração de texto
  GENERATION: {
    max_new_tokens: 128,    // Máximo de tokens na resposta
    temperature: 0.5,       // 0.0 = determinístico, 1.0 = criativo
    top_p: 0.9,             // Nucleus sampling
    do_sample: true,        // Use sampling (melhor qualidade)
  },

  // Configurações de LaTeX
  LATEX: {
    // Suportados atualmente
    detect_inline: true,    // Detectar $...$
    detect_display: true,   // Detectar $$...$$

    // Futuro: suporte a \( \) e \begin{equation}
    detect_paren: false,    // \(...\)
    detect_bracket: false,  // \[...\]
  },

  // Cache de explicações
  CACHE: {
    enabled: false,         // ⚠️ Funcionalidade futura
    storage: 'indexeddb',   // Onde armazenar
    max_size: 100,          // Máximo de itens em cache
    ttl: 7 * 24 * 60 * 60,  // 7 dias em segundos
  },

  // Debug
  DEBUG: {
    verbose: false,         // Log detalhado no console
    measure_time: true,     // Mede tempo de explicação
  },

  // Sites suportados (manifest.json)
  SITES: {
    arxiv: '*://*.arxiv.org/*',
    researchgate: '*://*.researchgate.net/*',
    scholar: '*://*.scholar.google.com/*',
    papers: '*://papers.ssrn.com/*',
    generic: '<all_urls>',
  }
};

// Exportar se estiver em um módulo
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CONFIG;
}
