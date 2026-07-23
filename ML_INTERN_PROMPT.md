# Prompt para ml-intern: Dataset + Fine-tuned Model para Explicar LaTeX

## Tarefa Principal

Crie um modelo especializado em português para explicar expressões LaTeX, otimizado para uso em uma extensão Chrome. O modelo deve:

1. **Coletar Dataset**: 5k-10k pares de (expressão LaTeX, explicação em português)
2. **Fine-tune**: Treinar Flan-T5-small com este dataset
3. **Publicar**: Fazer upload no Hugging Face Hub
4. **Validar**: Testar qualidade do modelo

---

## Fase 1: Coleta de Dataset

### Estratégia de Dados
- **Fonte primária**: arXiv papers (mathematics, physics, computer science)
- **Fonte secundária**: Wikipedia Math em português
- **Formato esperado**: JSONL com campos: `latex`, `explanation`, `context`, `source`, `difficulty`

### Instruções Específicas

```
Para cada expressão LaTeX encontrada:
1. Extrair a equação (ex: "E = mc^2")
2. Extrair 2-3 sentenças de contexto do paper
3. Gerar explicação concisa em português (2-3 linhas máximo)
4. Classificar dificuldade: "basic", "intermediate", "advanced"

Exemplo esperado:
{
  "latex": "\\int_0^\\infty e^{-x^2} dx",
  "explanation": "Integral definida de e elevado a menos x² de 0 até infinito. Esta é a famosa integral gaussiana, igual a √π/2. Muito usada em probabilidade e estatística.",
  "context": "A distribuição normal depende da integral gaussiana para seu cálculo de probabilidade.",
  "source": "arxiv:1234.56789",
  "difficulty": "intermediate"
}
```

### Requisitos Mínimos
- Mínimo 5000 pares validados
- Máximo 10 minutos de processamento por paper
- Evitar duplicatas
- Balancear entre basic/intermediate/advanced
- Salvar em: `data/latex-explanations-pt.jsonl`

---

## Fase 2: Fine-tuning do Modelo

### Setup
- **Modelo base**: `google/flan-t5-small`
- **Idioma**: Português brasileiro
- **Output tokens**: Máximo 128
- **Dataset split**: 80% train, 10% val, 10% test

### Configuração de Treino

```python
training_args = {
    "num_train_epochs": 3,
    "per_device_train_batch_size": 16,
    "per_device_eval_batch_size": 32,
    "learning_rate": 5e-5,
    "weight_decay": 0.01,
    "warmup_steps": 500,
    "logging_steps": 100,
    "eval_steps": 500,
    "save_steps": 500,
    "output_dir": "models/latex-explainer-pt-v1",
    "overwrite_output_dir": True,
    "save_total_limit": 2,
}
```

### Validação
- Calcular BLEU score no test set
- Gerar 5 exemplos de explicações geradas
- Verificar tamanho final do modelo
- Validação manual de 10 explicações aleatórias

### Output Esperado
- Modelo em: `models/latex-explainer-pt-v1/`
- Config em JSON
- Tokenizer salvo
- Relatório de métricas

---

## Fase 3: Publicação no Hugging Face Hub

### Informações do Repositório
- **Nome**: `seu-usuario/latex-explainer-pt-v1`
- **Tipo**: Model
- **Descrição**: "Modelo Flan-T5-small fine-tuned para explicar expressões LaTeX em português"
- **Licença**: Apache 2.0

### Conteúdo do README
```markdown
# LaTeX Explainer PT v1

Modelo Flan-T5-small fine-tuned para explicar expressões LaTeX em português.

## Uso
\`\`\`python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("seu-usuario/latex-explainer-pt-v1")
model = AutoModelForSeq2SeqLM.from_pretrained("seu-usuario/latex-explainer-pt-v1")

input_text = "Explique: E = mc^2"
input_ids = tokenizer.encode(input_text, return_tensors="pt")
outputs = model.generate(input_ids, max_length=128)
explanation = tokenizer.decode(outputs[0])
print(explanation)
\`\`\`

## Dataset
- 7,500 pares LaTeX ↔ explicação em português
- Coletados de arXiv e Wikipedia
- Split: 80% train, 10% val, 10% test
- Dificuldade: basic até advanced

## Métricas
- BLEU score: (será calculado)
- Tamanho: ~250MB
- Parâmetros: 60M

## Treinamento
- Epochs: 3
- Batch size: 16
- Learning rate: 5e-5
- Hardware: (especificar GPU usada)
```

### Fazer Upload
1. Salvar arquivos do modelo no Hub
2. Incluir dataset processado (opcional)
3. Publicar com versionamento semântico

---

## Fase 4: Validação e Testes

### Testes Automáticos
```python
test_cases = [
    ("E = mc^2", "Equivalência massa-energia"),
    ("∫ sin(x) dx", "Integral indefinida"),
    ("∇·E = ρ/ε₀", "Lei de Gauss"),
    ("P(A|B) = P(B|A)P(A)/P(B)", "Teorema de Bayes"),
]

# Para cada caso, gerar explicação e validar se é relevante
```

### Qualidade Manual
Revisar 10 explicações aleatórias:
- [ ] Explicação é concisa (< 3 linhas)?
- [ ] Usa português correto?
- [ ] Explica significado da expressão?
- [ ] Menciona uso/contexto?

---

## Fase 5: Integração na Extensão (Futuro)

Após validação:
1. Converter modelo ONNX para WebGPU
2. Atualizar `src/background.js` para usar novo modelo
3. Testar na extensão Chrome
4. Versionar como `v1.1` da extensão

---

## Requisitos Globais

- **Idioma**: Português brasileiro obrigatório
- **Formato**: JSONL para dataset, model artifacts para modelo
- **Tamanho máximo**: Dataset < 500MB, modelo < 300MB
- **Disponibilidade**: Dataset + modelo públicos no Hub
- **Documentação**: README em português e inglês
- **Versionamento**: Semantic versioning (v1.0.0)

---

## Checklist Final

- [ ] Dataset coletado e validado (5k+ pares)
- [ ] Fine-tuning completo com métricas
- [ ] Modelo publicado no Hub
- [ ] README com instruções de uso
- [ ] 10 exemplos de explicações testados manualmente
- [ ] Relatório de qualidade gerado
- [ ] Arquivo `latex-explanations-pt.jsonl` salvo localmente
- [ ] Arquivo `models/latex-explainer-pt-v1/` disponível

---

## Notas Importantes

1. **Qualidade é prioridade**: Dataset pequeno mas bom > dataset grande mas ruim
2. **Português correto**: As explicações devem ser naturais e bem escritas
3. **Reproduzibilidade**: Salvar seeds e configurations para reproduzir treino
4. **Segurança**: Usar apenas fontes de dados abertas (CC, arXiv, Wikipedia)
5. **Tempo**: Se exceder 8 horas, pausar e revisar estratégia

---

## Comando para Executar

```bash
ml-intern < ML_INTERN_PROMPT.md

# OU modo direto:
ml-intern "$(cat ML_INTERN_PROMPT.md)"

# OU com aprovação automática (use com cuidado):
ml-intern --auto-approve "$(cat ML_INTERN_PROMPT.md)"
```

---

Boa sorte! 🚀
