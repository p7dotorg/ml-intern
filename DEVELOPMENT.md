# Guia de Desenvolvimento

## Setup Inicial

### 1. Instale dependências
```bash
npm install
```

### 2. Carregue a extensão no Chrome

1. Abra `chrome://extensions/`
2. Ative "Modo de desenvolvedor" (canto superior direito)
3. Clique "Carregar extensão não empacotada"
4. Selecione a pasta do projeto

### 3. Abra DevTools

- Clique ícone da extensão → "Inspecionar visualização de página"
- Ou acesse `chrome://extensions/` → Clique em "inspecionar visualizações" para o Service Worker

## Fluxo de Desenvolvimento

### Edição de Arquivos

A maioria das mudanças requer **reload da extensão**:

1. Edite o arquivo
2. Abra `chrome://extensions/`
3. Clique no ícone ⟲ (reload) na extensão

**Não** precisa de reload:
- Mudanças em CSS (content.css)
- Mudanças em HTML da popup
- Mudanças que não afetam Service Worker

### Debugging

#### Service Worker (background.js)
```bash
# Abra chrome://extensions/
# Clique em "inspecionar visualizações" na extensão
# Console aparecerá - você verá logs de console.log()
```

#### Content Script (content.js)
```bash
# Abra DevTools na página (F12)
# Console mostrará logs do content.js
# Procure por "LaTeX Explainer" ou seus console.log()
```

#### Network Requests
- DevTools → Network tab
- Veja requisições do modelo sendo carregado

## Testes Manuais

### 1. Teste com arXiv
```
1. Abra https://arxiv.org/abs/2301.00000 (qualquer artigo)
2. Role até a seção com equações
3. Clique em uma expressão LaTeX (deve estar destacada)
4. Verifique a popup com explicação
```

### 2. Teste com página HTML local
```bash
# Crie um arquivo test.html com LaTeX
echo '<html>
<body>
  <p>Equação importante: $E = mc^2$</p>
  <p>$$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$</p>
</body>
</html>' > test.html

# Abra em chrome://
# Extensão deve detectar e destacar
```

### 3. Teste de Performance
```bash
# DevTools → Performance tab
# Registre clique em LaTeX
# Analise tempo de explicação
# Deve ser < 5 segundos
```

## Estrutura de Código

### background.js
- Carrega modelo transformers.js
- Processa requisições de explicação
- Gerencia estado do modelo

**Pontos de extensão:**
- Trocar modelo na linha 13
- Adicionar cache de explicações
- Implementar fallback para API externa

### content.js
- Detecta LaTeX via regex
- Substitui por elementos clicáveis
- Gerencia listeners e popups

**Pontos de extensão:**
- Melhorar regex para LaTeX complexo
- Suportar MathML
- Análise de contexto (qual seção do paper)

### content.css
- Estilos dos elementos LaTeX
- Estilos da popup
- Suporte para dark mode

**Pontos de extensão:**
- Temas customizáveis
- Animações mais sofisticadas
- Responsividade melhor

## Regexes para LaTeX

### Atual
```javascript
const LATEX_INLINE = /\$([^\$\n]+?)\$/g;      // $...$
const LATEX_DISPLAY = /\$\$([^\$\n]+?)\$\$/g; // $$...$$
```

### Melhorias possíveis
```javascript
// Suportar \( e \[ para LaTeX em HTML
const LATEX_PAREN = /\\\(([^\)]+?)\\\)/g;
const LATEX_BRACKET = /\\\[([^\]]+?)\\\]/g;

// Suportar \begin{equation}...\end{equation}
const LATEX_ENV = /\\begin\{equation\}([\s\S]*?)\\end\{equation\}/g;
```

## Modelos Alternativos

Atualmente usa **LLaMA-2-Math** com fallback para **Flan-T5-small**.

Você pode trocar em `background.js` para usar outros:

### Modelos Especializados em Matemática ⭐

```javascript
// Melhor qualidade para LaTeX (recomendado)
'Xenova/LLaMA-2-7B-Math-hf'          // ~7GB, muito bom
'Xenova/Mistral-7B-Math'              // ~7GB, rápido
'Xenova/DeepSeek-Math-7B'             // ~7GB, simbólico

// Compacto mas eficiente
'Xenova/mathberta'                    // ~110MB, entende LaTeX
'Xenova/distilbert-base-uncased'      // ~70MB, lightweight
```

### Modelos Genéricos (Fallback)

```javascript
// Se modelo math não carrega, tenta esses:
'Xenova/flan-t5-small'                // ~250MB, rápido
'Xenova/flan-t5-base'                 // ~900MB, melhor
'Xenova/LLaMA-2-13B-hf'               // ~13GB, muito bom
```

### Como Trocar Modelo

```javascript
// Em background.js, linha 12-30:
model = await pipeline(
  'text-generation',
  'Xenova/SUA-ESCOLHA-AQUI',  // ← mude aqui
  { device: 'webgpu', quantized: true }
);
```

⚠️ **Nota**: 
- Modelos > 1GB podem ser lentos na primeira execução
- Use `quantized: true` para economizar memória
- Se falhar, o fallback para Flan-T5-small

## Cache de Explicações

Para evitar re-processar a mesma equação:

```javascript
// Adicione em background.js
const explanationCache = new Map();

const explainLatex = async (latexExpr) => {
  if (explanationCache.has(latexExpr)) {
    return explanationCache.get(latexExpr);
  }
  
  // ... processar ...
  
  explanationCache.set(latexExpr, result);
  return result;
};
```

## Publicar na Chrome Web Store

```bash
# 1. Crie arquivo ZIP
zip -r latex-explainer.zip \
  src/ assets/ manifest.json package.json README.md

# 2. Acesse Chrome Web Store Developer Dashboard
# https://chrome.google.com/webstore/devconsole

# 3. Faça upload do ZIP
# 4. Preencha descrição, screenshots, etc
```

## Troubleshooting

### "transformers.js não está definido"
- Verificar se CDN está acessível
- Tentar com import local: `npm install @xenova/transformers`
- Atualizar manifest.json para servir localmente

### WebGPU não funciona
```javascript
// Verificar suporte em background.js
if (!navigator.gpu) {
  console.warn('WebGPU não disponível, usando CPU');
  // Trocar para { device: 'cpu' }
}
```

### Extension não detecta LaTeX
1. Abra console (F12) na página
2. Cole: `document.body.innerHTML.match(/\$[^\$]+\$/g)`
3. Se retornar nada, LaTeX é renderizado como imagem

## Recursos

- [Chrome Extension Docs](https://developer.chrome.com/docs/extensions/)
- [transformers.js Docs](https://huggingface.co/docs/transformers.js)
- [WebGPU Spec](https://gpuweb.github.io/gpuweb/)
- [Xenova Models](https://huggingface.co/models?library=transformers.js)
