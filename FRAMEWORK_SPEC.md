# ML Agent Framework Multi-Provider - Specification

**Status**: Draft v1.0  
**Organização**: p7dotorg  
**Propósito**: Framework extensível para workflows de ML com suporte a múltiplos LLM providers  

---

## 📋 Resumo Executivo

Um **framework open-source** que replica a funcionalidade do ml-intern (Hugging Face) mas com suporte a **múltiplos providers de LLM** (Claude, OpenAI, DeepSeek, Mistral, etc). 

Objetivo: Automatizar workflows ML completos (dataset collection → processing → training → deployment) permitindo que equipes treinem modelos especializados sem dependência de um único provider de IA.

**Caso de uso inicial**: Treinar modelo especializado para explicar expressões LaTeX em português.

---

## 🎯 Objetivos

### Primário
- ✅ Replicar funcionalidade do ml-intern
- ✅ Suporte a múltiplos providers (Claude, OpenAI, DeepSeek, Mistral, Groq, etc)
- ✅ Orquestrar workflows ML completos
- ✅ Extensível e reutilizável

### Secundários
- ✅ Open-source em p7dotorg
- ✅ Documentação profissional
- ✅ CLI intuitivo
- ✅ Sistema de plugins
- ✅ Logs e auditoria
- ✅ Tratamento de erros robusto

---

## 🏗️ Arquitetura de Alto Nível

```
┌─────────────────────────────────────────────┐
│         CLI Interface (main.py)             │
│  ml-agent --provider claude --task "..."   │
└────────────────┬────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────┐
│      Agent Orchestrator                     │
│  - Parse task specification                 │
│  - Route to appropriate workflow            │
│  - Manage provider selection               │
└────────────────┬────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────┐
│      Provider Abstraction Layer             │
│  - Unified LLM interface                   │
│  - Auth management (API keys, OAuth)       │
│  - Rate limiting & retry logic             │
└─────┬──────────┬──────────┬────────────────┘
      ↓          ↓          ↓
┌─────────┐ ┌──────────┐ ┌─────────┐
│ Claude  │ │ OpenAI   │ │ DeepSeek│
└─────────┘ └──────────┘ └─────────┘
      ↓          ↓          ↓
┌─────────────────────────────────────────────┐
│      Workflow Modules                       │
│  - Dataset Collection (Scraping)            │
│  - Data Processing & Validation             │
│  - Model Training Orchestration             │
│  - Deployment & Publishing                  │
└─────────────────────────────────────────────┘
```

---

## 🔌 Componentes Principais

### 1. **Provider Registry** (`providers/`)
Define interface unificada para diferentes LLM providers.

**Providers suportados (v1.0)**:
- Claude 3.5 Sonnet (Anthropic)
- GPT-4 Turbo (OpenAI)
- DeepSeek-V2 (DeepSeek)
- Mistral Large (Mistral)

**Extensível para**: Groq, Cohere, Llama API, etc

**Responsabilidade**:
- Abstração de API calls
- Gerenciamento de tokens
- Rate limiting
- Retry logic

### 2. **Auth Manager** (`auth/`)
Gerencia credenciais para múltiplos providers.

**Suporta**:
- Environment variables
- `.env` files
- `auth.json` (encrypted)
- OAuth (se aplicável)
- CLI flags

**Prioridade de resolução**:
1. Flag CLI `--api-key`
2. `auth.json` local
3. Variável de ambiente
4. Prompt interativo

### 3. **Workflow Engine** (`workflows/`)
Orquestra tarefas ML complexas.

**Workflows suportados (v1.0)**:
- `dataset-from-arxiv`: Scraping + processamento
- `fine-tune-model`: Treino com Hugging Face
- `deploy-to-hub`: Upload no Hub
- `evaluate-model`: Validação

**Cada workflow**:
- Quebrado em steps
- Logging detalhado
- Retry automático
- Validation em cada passo

### 4. **CLI Interface** (`cli/`)
Interface intuitiva para usuários.

```bash
# Forma básica
ml-agent \
  --provider claude \
  --workflow dataset-from-arxiv \
  --config config.yaml

# Forma avançada
ml-agent chat --provider openai  # Chat interativo
ml-agent list-workflows          # Listar workflows
ml-agent validate-config config.yaml
```

### 5. **Plugin System** (`plugins/`)
Permite estender com novos providers/workflows.

**Tipos de plugins**:
- `provider_plugin`: Novo LLM provider
- `workflow_plugin`: Novo workflow
- `storage_plugin`: Novo backend de armazenamento

---

## 📊 Fluxo de Execução

```
User Input (CLI)
       ↓
Parse Args & Config
       ↓
Authenticate Provider
       ↓
Initialize Agent
       ↓
Load Workflow Definition
       ↓
LOOP (até completion):
  ├─ Execute Step
  ├─ Get LLM response (via provider abstraction)
  ├─ Validate output
  ├─ Log progress
  ├─ Retry se needed (até 3x)
  └─ Next step
       ↓
Generate Report
       ↓
Save Artifacts (model, dataset, logs)
```

---

## 🔧 Tecnologia Stack

| Componente | Tecnologia | Motivo |
|------------|-----------|--------|
| **Linguagem** | Python 3.11+ | Ecossistema ML |
| **CLI** | Typer | Type-safe, moderna |
| **LLM Calls** | Provider SDKs | Oficiais e confiáveis |
| **Data** | Polars/Pandas | Performance |
| **ML Training** | Hugging Face Transformers | Standard da indústria |
| **Config** | Pydantic + YAML | Type-safe, flexível |
| **Logging** | Structlog | Estruturado e debugável |
| **Storage** | Local FS + S3 (futuro) | Flexível |
| **Testing** | Pytest | Standard |

---

## 📁 Estrutura de Diretórios

```
ml-agent/
├── pyproject.toml              # Deps + metadata
├── README.md                   # Documentação
├── LICENSE                     # Apache 2.0
│
├── src/ml_agent/
│   ├── __init__.py
│   ├── cli.py                  # CLI entry point
│   │
│   ├── providers/              # Provider implementations
│   │   ├── __init__.py
│   │   ├── base.py            # Abstract provider interface
│   │   ├── claude.py           # Claude provider
│   │   ├── openai.py           # OpenAI provider
│   │   ├── deepseek.py         # DeepSeek provider
│   │   ├── mistral.py          # Mistral provider
│   │   └── registry.py         # Provider registry
│   │
│   ├── auth/                   # Authentication
│   │   ├── __init__.py
│   │   ├── manager.py          # Auth manager
│   │   └── strategies.py       # Auth strategies
│   │
│   ├── workflows/              # Workflow definitions
│   │   ├── __init__.py
│   │   ├── base.py             # Workflow base class
│   │   ├── dataset.py          # Dataset workflows
│   │   ├── training.py         # Training workflows
│   │   ├── deployment.py       # Deployment workflows
│   │   └── registry.py         # Workflow registry
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── agent.py            # Main agent class
│   │   ├── config.py           # Configuration management
│   │   ├── logger.py           # Logging setup
│   │   └── exceptions.py       # Custom exceptions
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py       # Input validation
│   │   ├── retry.py            # Retry logic
│   │   └── file_ops.py         # File operations
│   │
│   └── plugins/                # Plugin system
│       ├── __init__.py
│       ├── base.py             # Plugin base class
│       └── loader.py           # Plugin loader
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_providers.py
│   │   ├── test_workflows.py
│   │   ├── test_auth.py
│   │   └── test_cli.py
│   │
│   ├── integration/
│   │   ├── test_end_to_end.py
│   │   └── test_workflows_e2e.py
│   │
│   └── fixtures/
│       ├── configs/
│       ├── responses/          # Mock LLM responses
│       └── datasets/
│
├── examples/
│   ├── latex-explainer/
│   │   ├── config.yaml
│   │   ├── prompts.yaml
│   │   └── README.md
│   │
│   └── simple-workflow/
│
├── docs/
│   ├── architecture.md
│   ├── providers.md            # Como adicionar provider
│   ├── workflows.md            # Como criar workflow
│   ├── cli-reference.md
│   ├── api-reference.md
│   └── examples.md
│
└── scripts/
    ├── setup-env.sh            # Setup script
    └── run-tests.sh            # Test runner
```

---

## 🔐 Autenticação & Credenciais

### Estratégia Multi-camadas

1. **CLI Flag** (mais alta prioridade)
   ```bash
   ml-agent --provider claude --api-key "sk-ant-..."
   ```

2. **Config File** (`auth.json` - encrypted)
   ```json
   {
     "providers": {
       "claude": {"api_key": "..."},
       "openai": {"api_key": "..."}
     }
   }
   ```

3. **Environment Variables**
   ```bash
   CLAUDE_API_KEY=sk-ant-...
   OPENAI_API_KEY=sk-...
   ```

4. **Prompt Interativo**
   ```
   No credentials found for 'claude'
   Enter API key (will be masked): ••••••••
   Save to auth.json? [y/n]:
   ```

---

## 📝 Especificação de Workflow

Cada workflow é definido em YAML + Python:

```yaml
# workflows/dataset-from-arxiv.yaml
name: dataset-from-arxiv
version: "1.0"
description: "Coleta dataset de papers arXiv"

parameters:
  papers_count: 100
  categories: ["math", "cs.AI"]
  max_equations_per_paper: 50
  explanation_model: "claude"

steps:
  - name: download_papers
    provider_task: "download_arxiv_papers"
    
  - name: extract_equations
    provider_task: "extract_latex"
    
  - name: generate_explanations
    provider_task: "generate_text"
    model_config:
      max_tokens: 256
      temperature: 0.7
      
  - name: validate_dataset
    provider_task: "validate_quality"
    
  - name: export_dataset
    output_format: "jsonl"
    destination: "s3://bucket/dataset.jsonl"
```

---

## 🧪 Testes & Validação

### Estratégia de Testes

- **Unit Tests**: Providers, workflows, auth (mocks)
- **Integration Tests**: End-to-end com providers reais (⚠️ caro)
- **E2E Tests**: Workflows completos (local)

### Fixtures
- Mock responses de LLMs
- Test datasets pequenos
- Config de teste

---

## 📦 Versionamento & Release

- **Semantic Versioning**: v1.0.0
- **Release Checklist**: Testes, docs, changelog
- **Distribução**: PyPI + GitHub Releases

---

## 🚀 Roadmap

### v1.0 (MVP)
- ✅ 4 providers (Claude, OpenAI, DeepSeek, Mistral)
- ✅ 3 workflows (dataset, training, deploy)
- ✅ CLI básico
- ✅ Logging

### v1.1
- Plugin system
- Mais workflows
- UI web (opcional)

### v2.0
- Distributed training
- Custom model support
- GraphQL API

---

## ✅ Critérios de Aceitação

- [ ] Todos os providers funcionam com autenticação
- [ ] Workflows completam sem erros
- [ ] CLI é intuitiva e documentada
- [ ] Cobertura de testes > 80%
- [ ] Documentação completa
- [ ] Exemplo funcional (LaTeX dataset)
- [ ] Open-source em p7dotorg

---

## 🤝 Governança & Contribuição

- **Licença**: Apache 2.0
- **Contribuidores**: Bem-vindos via PRs
- **Code Style**: Black, isort, mypy
- **CI/CD**: GitHub Actions

---

Este é o spec v1.0. Pronto para implementação!
