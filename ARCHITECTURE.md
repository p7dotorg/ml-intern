# Arquitetura da Extensão LaTeX Explainer

## Visão Geral

```
┌─────────────────────────────────────────────────────────┐
│                    Chrome Browser                        │
├────────────────────────────┬────────────────────────────┤
│                            │                             │
│   Content Script           │  Service Worker             │
│   (content.js)             │  (background.js)            │
│   ┌──────────────────┐     │  ┌───────────────────┐     │
│   │ • Detecta LaTeX  │     │  │ • transformers.js │     │
│   │ • Cria elements  │ ←───┼→ │ • WebGPU Runtime  │     │
│   │ • Listeners      │     │  │ • Modelo IA       │     │
│   │ • Mostra popup   │     │  │ • Processa texto  │     │
│   └──────────────────┘     │  └───────────────────┘     │
│           │                │           │                 │
│           └────────────────┼───────────┘                 │
│                            │                             │
└────────────────────────────┴────────────────────────────┘
                 ↓ HTML/PDF
        ┌───────────────────┐
        │   Web Pages       │
        │ (arXiv, HTML etc) │
        └───────────────────┘
```

## Componentes

### 1. Manifest (manifest.json)
**Responsabilidade**: Configurar a extensão

- Define permissões
- Registra content scripts
- Configura background service worker
- Define ícones e popup

**Alterações futuras**:
- Suporte a Firefox (Manifest V2)
- Configurações do usuário (storage)
- Ícone dinâmico baseado em status

### 2. Content Script (content.js)
**Responsabilidade**: Interagir com a página

```
Página HTML → Walker (TreeWalker)
            → Detecta LaTeX (regex)
            → Substitui HTML
            → Anexa listeners
            → Mostra popup
```

**Fluxo**:
1. Detecta mutações no DOM (PDFs com lazy-load)
2. Procura por padrões LaTeX ($...$ e $$...$$)
3. Substitui por `<span class="latex-expr">`
4. Listeners on click enviam para background
5. Popup mostra explicação

**Performance**:
- TreeWalker eficiente (não reprocessa)
- Regex compilado globalmente
- MutationObserver com throttling (futuro)

**Limitações**:
- Não funciona com LaTeX renderizado como SVG/imagem
- PDFs com múltiplas páginas podem ser lentos

### 3. Service Worker (background.js)
**Responsabilidade**: Processamento de IA

```
Request "EXPLAIN_LATEX"
        ↓
Load Model (primeira vez)
  ├─ transformers.js
  ├─ WebGPU backend
  └─ ~200MB download
        ↓
Generate Explanation
  ├─ Prompt: "Explique esta expressão LaTeX..."
  ├─ Model.generate()
  └─ Retorna texto
        ↓
Response enviado para content.js
```

**Modelo**: Flan-T5 Small
- Tamanho: ~200MB
- Tempo: 2-5s por explicação
- VRAM: ~800MB

**Cache**: Futuro - store explicações visitadas

### 4. UI Components

#### Popup (popup.html/js)
- Mostra status do modelo
- Informações de uso
- Sem interação (informativa)

#### Overlay (content.css)
- Elementos LaTeX com gradiente roxo
- Hover effects
- Modal com explicação
- Dark mode support

## Fluxo de Dados

```
User clica em LaTeX
  ↓
content.js::handleLatexClick()
  ├─ Extrai latex do data-attribute
  ├─ Mostra "⏳ Explicando..."
  └─ chrome.runtime.sendMessage()
  ↓
background.js::onMessage listener
  ├─ Verifica se modelo está carregado
  ├─ Se não: initModel()
  └─ Chama explainLatex(latex)
  ↓
transformers.js + WebGPU
  ├─ Cria prompt
  ├─ Executa pipeline
  └─ Retorna explicação
  ↓
background.js retorna response
  ↓
content.js::sendResponse()
  ├─ Esconde "⏳"
  ├─ Mostra explicação em popup
  └─ Adiciona event listeners (close)
  ↓
User lê explicação e clica close
```

## Otimizações

### Já Implementadas
✓ Regex compilado globalmente  
✓ TreeWalker para eficiência  
✓ Lazy load do modelo (primeiro uso)  
✓ WebGPU aceleração  
✓ CSS otimizado (sem layout trashing)  

### Futuras
- [ ] Cache de explicações (IndexedDB)
- [ ] Throttle de detecção (MutationObserver)
- [ ] Worker threads para modelo
- [ ] Compressão GZIP do modelo
- [ ] Preload em background
- [ ] Service worker persistent

## Extensibilidade

### Adicionar Suporte a MathML
```javascript
// content.js
const MATHML_SELECTOR = 'math[display="block"]';
document.querySelectorAll(MATHML_SELECTOR).forEach(el => {
  // Converter MathML → LaTeX
  // Ou explicar diretamente
});
```

### Adicionar Novo Modelo
```javascript
// background.js linha 13
const MODEL_CONFIG = {
  'small': 'Xenova/flan-t5-small',      // Padrão
  'large': 'Xenova/flan-t5-large',      // Lento
  'math': 'Xenova/math-llm-7b',         // Hipotético
};

const selectedModel = MODEL_CONFIG[chrome.storage.sync.get('model')] || 'small';
model = await pipeline('text2text-generation', selectedModel, {device: 'webgpu'});
```

### Adicionar Backend Remoto
```javascript
// background.js - fallback para API
if (!model || modelError) {
  const response = await fetch('https://seu-api.com/explain', {
    method: 'POST',
    body: JSON.stringify({ latex })
  });
  return response.json();
}
```

## Segurança

### Já Implementadas
✓ Sanitização de HTML (escapeHtml)  
✓ Nenhuma eval() ou innerHTML inseguro  
✓ CSP headers respeitados  
✓ Sem comunicação com servidor externo  
✓ LocalStorage isolado por origem  

### Considerar
- [ ] Validação rigorosa de entrada LaTeX
- [ ] Timeout de requisições
- [ ] Rate limiting de requisições
- [ ] Validação de CORS

## Performance Targets

| Métrica | Target | Atual |
|---------|--------|-------|
| Carregamento modelo | < 30s | 15-30s |
| Explicação | < 5s | 2-5s |
| Memória | < 1GB | ~800MB |
| CPU (explicação) | < 50% | 30-40% |
| Detecção LaTeX | < 500ms | 50-200ms |

## Roadmap

### v1.0 ✓
- Detecção básica de LaTeX
- Explicações via modelo local
- WebGPU acelerado
- Popup informativa

### v1.1
- [ ] Cache de explicações
- [ ] Histórico de buscas
- [ ] Seleção de modelo do usuário
- [ ] Melhor suporte a PDFs

### v2.0
- [ ] Suporte a MathML
- [ ] Firefox support
- [ ] Cloud sync de preferências
- [ ] Exportar explicações

### v2.1+
- [ ] Modelos especializados por área
- [ ] Detecção de linguagem e tradução
- [ ] Integração com Zotero/Mendeley
- [ ] Editor LaTeX com pré-visualização
