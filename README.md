# LaTeX Explainer - Extensão Chrome

Uma extensão Chrome que detecta automaticamente expressões LaTeX em papers acadêmicos e fornece explicações instantâneas usando um modelo de IA rodando localmente no navegador via WebGPU.

## 🎯 Características

- **Detecção Automática**: Identifica expressões LaTeX ($...$ e $$...$$) em artigos
- **Explicações Instantâneas**: Clique em qualquer expressão para obter uma explicação clara
- **Roda Localmente**: Modelo completo executado no navegador com WebGPU (sem servidor)
- **Sem Latência de Rede**: Funciona offline após o carregamento inicial do modelo
- **Suporte Amplo**: Funciona com PDFs embarcados (arXiv, ResearchGate) e páginas HTML
- **Dark Mode**: Suporta tema escuro do sistema operacional

## 📋 Pré-requisitos

- Chrome/Chromium 113+ (com suporte a WebGPU)
- GPU dedicada recomendada (NVIDIA, AMD, Intel Arc)
- ~200MB de espaço para o modelo (primeira execução)
- 8GB+ de RAM recomendado

## 🚀 Instalação em Desenvolvimento

### 1. Clone ou extraia o repositório
```bash
cd /Users/lucianfialho/Code/latex
```

### 2. Instale as dependências (se necessário)
```bash
# Se quiser servir localmente para desenvolvimento
npm install --save-dev http-server
```

### 3. Carregue a extensão no Chrome

1. Abra `chrome://extensions/`
2. Ative o "Modo de desenvolvedor" (canto superior direito)
3. Clique em "Carregar extensão não empacotada"
4. Selecione a pasta `/Users/lucianfialho/Code/latex`

### 4. Teste a extensão

1. Acesse um artigo no [arXiv](https://arxiv.org)
2. Procure por uma expressão LaTeX
3. Clique na expressão destacada com a cor gradiente roxo
4. Uma popup deve aparecer com a explicação

## 🏗️ Estrutura do Projeto

```
latex/
├── manifest.json           # Configuração da extensão
├── src/
│   ├── background.js       # Service Worker (carrega modelo matemático)
│   ├── content.js          # Content Script (detecta LaTeX)
│   ├── content.css         # Estilos para expressões LaTeX
│   ├── popup.html          # Interface da extensão
│   └── popup.js            # Script da popup
├── assets/                 # Ícones da extensão
└── README.md              # Este arquivo
```

## 🔧 Configuração

### Modelo de IA Padrão

Usa **LLaMA-2-Math** (especializado em expressões matemáticas) com fallback para **Flan-T5-small**.

### Trocar o Modelo

No arquivo `src/background.js`, modifique a linha que começa com `await pipeline()`:

```javascript
// Modelos recomendados para matemática:
'Xenova/LLaMA-2-7B-Math-hf'    // ⭐ Melhor qualidade
'Xenova/Mistral-7B-Math'       // ⭐ Rápido e preciso
'Xenova/mathberta'             // Compacto (~110MB)

// Genéricos:
'Xenova/flan-t5-base'          // Bom custo-benefício
'Xenova/flan-t5-small'         // Rápido, baixa memória
```

**Veja DEVELOPMENT.md para lista completa de modelos**

### Ajustar Sites Suportados

No `manifest.json`, ajuste `host_permissions` para mais sites:

```json
"host_permissions": [
  "*://*.arxiv.org/*",
  "*://*.researchgate.net/*",
  "*://*.scholar.google.com/*",
  "*://papers.ssrn.com/*",     // ← adicione sites aqui
  "<all_urls>"
]
```

## 📊 Performance

| Métrica | Valor |
|---------|-------|
| Tamanho do Modelo | ~200MB |
| Primeira Execução | 15-30s |
| Explicação Posterior | 2-5s |
| Memória (em uso) | ~800MB |
| Suporte GPU | WebGPU (NVIDIA, AMD, Intel) |

## 🐛 Troubleshooting

### WebGPU não funciona
- Verifique se seu Chrome suporta WebGPU: `chrome://flags` e procure por "WebGPU"
- Sua GPU pode não ser compatível (verifique drivers)

### Modelo não carrega
1. Abra DevTools (F12) → Console
2. Procure por erros de rede
3. Tente limpar cache: `chrome://settings/siteData`

### Extensão não detecta LaTeX
1. Verifique se o padrão da regex está correto no `content.js`
2. PDFs podem ter LaTeX renderizado como imagens (não textuais)

## 🎨 Customização de Estilos

Para alterar as cores, edite `src/content.css`:

```css
.latex-expr {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  /* ↑ Gradiente roxo padrão - customize aqui */
}
```

## 🔐 Privacidade

- ✅ Todos os dados processados localmente
- ✅ Sem envio de dados para servidor
- ✅ Nenhum rastreamento
- ✅ Modelo roda completamente offline (após primeira execução)

## 📚 Tecnologias Utilizadas

- **transformers.js** - Modelos de IA no navegador
- **WebGPU** - Aceleração GPU
- **ONNX Runtime** - Execução otimizada
- **Manifest V3** - APIs modernas do Chrome

## 🚀 Próximas Melhorias Planejadas

- [ ] Suporte a MathML além de LaTeX
- [ ] Histórico de explicações
- [ ] Temas personalizáveis
- [ ] Suporte a Firefox
- [ ] Sincronização com conta do usuário
- [ ] Modelos especializados por área (Física, Química, etc)

## 📝 Licença

MIT

## 💬 Feedback

Encontrou um bug ou tem uma sugestão? Abra uma issue!

## 🙏 Créditos

- Modelos via [Hugging Face](https://huggingface.co)
- transformers.js via [Xenova](https://github.com/xenova/transformers.js)
- Inspiração em ferramentas como Mathpix e TeX-to-SVG
