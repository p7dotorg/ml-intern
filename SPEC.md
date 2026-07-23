# Projeto: Dataset + Fine-tuned Model para Explicar LaTeX

## 📋 Visão Geral

Criar um **modelo de IA especializado** que explique expressões LaTeX em português, otimizado para a extensão Chrome. Envolve:
1. Montar dataset de LaTeX + explicações
2. Fine-tunar um modelo Flan-T5-small
3. Integrar na extensão

---

## 🎯 Objetivos

### Objetivo Principal
Construir um modelo de explicação de LaTeX compacto (~250MB), rápido (< 2s/explicação) e especializado em português.

### Objetivos Secundários
- ✅ Dataset escalável e reutilizável
- ✅ Pipeline reproduzível de treino
- ✅ Modelo pronto para produção (quantizado)
- ✅ Integração sem quebrar extensão existente

---

## 📊 Requisitos

### Dataset
- **Fonte**: arXiv papers (scraping automático)
- **Tamanho alvo**: 5k-10k pares (LaTeX, explicação PT)
- **Formato**: JSONL com campos: `latex`, `explanation`, `context`, `difficulty`
- **Cobertura**: Básico até avançado (Cálculo, Álgebra, Probabilidade, etc)

### Modelo
- **Base**: `google/flan-t5-small` (250MB)
- **Idioma**: Português brasileiro
- **Explicações**: Concisas (2-3 linhas max)
- **Saída**: Quantizado para WebGPU

### Integração
- **Compatibilidade**: Chrome Extension V3
- **Runtime**: transformers.js + WebGPU
- **Fallback**: Flan-T5-small original se falhar

---

## 🏗️ Arquitetura

### Subsistema 1: Dataset Builder
```
Dataset Sources
  ├─ arXiv papers (PDF)
  ├─ Wikipedia Math (HTML)
  └─ Manual validation

      ↓

Pipeline:
  1. Download papers
  2. Extrair equações
  3. Extrair contexto (2-3 sentenças)
  4. Gerar explicações (Claude API ou manual)
  5. Validar qualidade
  6. Exportar JSONL

      ↓

Output: `data/latex-explanations-pt.jsonl`
```

### Subsistema 2: Fine-tuning
```
Input Dataset (JSONL)
      ↓
Hugging Face Trainer
  ├─ Model: Flan-T5-small
  ├─ Epochs: 3-5
  ├─ Batch size: 16-32
  └─ Learning rate: 5e-5
      ↓
Trained Model
      ↓
Quantization (ONNX)
      ↓
Output: `models/latex-explainer-pt-v1/`
```

### Subsistema 3: Extension Integration
```
Trained Model
      ↓
Convert para ONNX/WebGPU
      ↓
Update background.js
      ↓
Test na extensão
      ↓
Package final
```

---

## 📁 Estrutura de Arquivos

```
/Users/lucianfialho/Code/latex/
│
├── data/
│   ├── raw/                          # Dados brutos
│   │   ├── arxiv-papers/            # PDFs baixados
│   │   └── sources.json             # Log de fontes
│   │
│   ├── processed/                    # Dados processados
│   │   ├── latex-expressions.jsonl  # Equações extraídas
│   │   ├── with-explanations.jsonl  # Com explicações
│   │   └── validated.jsonl          # Validado
│   │
│   └── splits/
│       ├── train.jsonl              # 80%
│       ├── val.jsonl                # 10%
│       └── test.jsonl               # 10%
│
├── scripts/
│   ├── dataset_builder.py           # Scraper + extrator
│   ├── data_processor.py            # Limpeza e validação
│   ├── generate_explanations.py     # Claude API ou manual
│   ├── train.py                     # Fine-tuning
│   ├── evaluate.py                  # Métricas
│   └── convert_to_onnx.py          # Quantização
│
├── models/
│   ├── latex-explainer-pt-v1/       # Modelo treinado
│   │   ├── pytorch_model.bin
│   │   ├── config.json
│   │   └── tokenizer.json
│   │
│   └── onnx/                         # Versão ONNX
│       └── model.onnx
│
├── notebooks/
│   ├── 01-eda.ipynb                 # Exploração de dados
│   ├── 02-training.ipynb            # Treino interativo
│   └── 03-evaluation.ipynb          # Métricas
│
├── docs/
│   ├── dataset-schema.md            # Formato dos dados
│   ├── training-results.md          # Resultados
│   └── deployment.md                # Como usar
│
└── tests/
    ├── test_dataset.py              # Validação de dados
    └── test_model.py                # Avaliação do modelo
```

---

## 🔄 Workflow

### Week 1: Dataset
- Day 1-2: Scraper de arXiv
- Day 2-3: Parser de LaTeX
- Day 3-4: Gerador de explicações
- Day 4-5: Validação e limpeza

### Week 2: Fine-tuning
- Day 1-2: Setup Hugging Face
- Day 2-3: Fine-tuning
- Day 4: Avaliação
- Day 5: Quantização

### Week 3: Integração
- Day 1-2: Converter para ONNX
- Day 2-3: Integrar na extensão
- Day 4-5: Testes e deploy

---

## 📐 Especificações Técnicas

### Dataset Format (JSONL)
```json
{
  "latex": "E = mc^2",
  "explanation": "Equação de equivalência massa-energia. E é energia, m é massa, c é velocidade da luz.",
  "context": "Einstein provou que massa e energia são conversíveis em sua teoria da relatividade.",
  "source": "arxiv:1905.12345",
  "difficulty": "basic",
  "category": "physics"
}
```

### Model Config
- **Architecture**: Flan-T5-small (encoder-decoder)
- **Tokenizer**: T5TokenizerFast
- **Max input**: 128 tokens
- **Max output**: 128 tokens
- **Precision**: float32 (quantizado para int8 depois)

### Training Hyperparameters
```python
{
  "num_epochs": 3,
  "per_device_train_batch_size": 16,
  "per_device_eval_batch_size": 32,
  "learning_rate": 5e-5,
  "weight_decay": 0.01,
  "warmup_steps": 500,
  "logging_steps": 100,
  "eval_steps": 500,
  "save_steps": 500,
}
```

---

## ✅ Métricas de Sucesso

### Dataset
- ✅ Mínimo 5k pares validados
- ✅ Cobertura de 3+ áreas matemáticas
- ✅ < 5% de duplicatas
- ✅ Distribuição balanceada por dificuldade

### Modelo
- ✅ BLEU score > 0.4 em test set
- ✅ Tempo de explicação < 2s
- ✅ Tamanho quantizado < 300MB
- ✅ Perplexidade < 20 no test set

### Integração
- ✅ Extensão carrega modelo em < 10s
- ✅ Explicações são relevantes (teste manual)
- ✅ Sem crashes ou memory leaks
- ✅ Funciona offline

---

## 🚀 Próximos Passos

1. **Aprovação do Spec** ← Você está aqui
2. **Criar plano de implementação** (3 subsistemas)
3. **Executar incrementalmente**
4. **Validar em produção**

---

## 📝 Notas

- **Dados**: Usar apenas fontes abertas/permitidas (arXiv, Wikipedia)
- **Custo**: Claude API para geração (estimado: $50-100 para 10k pares)
- **Tempo**: ~2-3 semanas com trabalho part-time
- **Risco**: Qualidade de explicações depende de dataset

---

## Aprovação

- [ ] Escopo aprovado
- [ ] Arquitetura aprovada
- [ ] Timeline realista?
- [ ] Recursos disponíveis?

**Próximo passo**: Montar plano de implementação detalhado (superpowers:writing-plans)
