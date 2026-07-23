# Comparação de Modelos para Explicar LaTeX

## 🏆 Recomendação Rápida

**Melhor qualidade**: `Xenova/LLaMA-2-7B-Math-hf`  
**Melhor equilíbrio**: `Xenova/Mistral-7B-Math`  
**Mais compacto**: `Xenova/mathberta` (~110MB)  
**Fallback**: `Xenova/flan-t5-small` (~250MB)  

---

## Modelos Especializados em Matemática ⭐

### LLaMA-2-7B-Math
```
Tamanho:       ~7GB (quantizado: ~2-3GB)
Tempo inicial: 20-30s
Tempo/explicação: 3-8s
VRAM:          ~2GB durante uso
Qualidade:     ⭐⭐⭐⭐⭐ Excelente
Velocidade:    ⭐⭐⭐ Moderado
Foco:          Resolução + explicação de problemas
```

**Vantagens**:
- Entende contexto matemático profundo
- Explica passo a passo
- Suporta múltiplas áreas (Cálculo, Álgebra, Geometria)

**Desvantagens**:
- Arquivo grande (~7GB)
- Mais lento na primeira execução
- Pode usar mais memória

**Melhor para**: Papers complexos com muita matemática avançada

---

### Mistral-7B-Math  
```
Tamanho:       ~7GB (quantizado: ~2-3GB)
Tempo inicial: 15-25s
Tempo/explicação: 2-5s
VRAM:          ~2GB durante uso
Qualidade:     ⭐⭐⭐⭐ Muito bom
Velocidade:    ⭐⭐⭐⭐ Rápido
Foco:          Matemática prática
```

**Vantagens**:
- Mais rápido que LLaMA
- Explicações claras e concisas
- Bom custo-benefício

**Desvantagens**:
- Menos profundo que LLaMA em tópicos avançados
- Ainda é um arquivo grande

**Melhor para**: Uso geral, papers de engenharia/física

---

### DeepSeek-Math-7B
```
Tamanho:       ~7GB (quantizado: ~2-3GB)
Tempo inicial: 20-30s
Tempo/explicação: 4-10s
VRAM:          ~2.5GB durante uso
Qualidade:     ⭐⭐⭐⭐⭐ Excelente
Velocidade:    ⭐⭐ Lento
Foco:          Matemática simbólica + numérica
```

**Vantagens**:
- Melhor em contas exatas
- Entende cálculo simbólico
- Altíssima precisão

**Desvantagens**:
- Mais lento
- Mais verboso nas explicações

**Melhor para**: Verificação de expressões, cálculos exatos

---

## Modelos Compactos

### MathBERTa
```
Tamanho:       ~110MB
Tempo inicial: 3-5s
Tempo/explicação: 0.5-2s
VRAM:          ~300MB
Qualidade:     ⭐⭐⭐ Bom
Velocidade:    ⭐⭐⭐⭐⭐ Muito rápido
Foco:          Entender LaTeX
```

**Vantagens**:
- Carregamento instantâneo
- Usa pouca memória
- Perfeito para análise rápida

**Desvantagens**:
- Menos "conversacional"
- Não explica tão profundamente
- Mais um "entendedor" que "explicador"

**Melhor para**: Navegação rápida, dispositivos com pouca RAM

---

## Modelos Genéricos (Fallback)

### Flan-T5-Small ⭐ (PADRÃO)
```
Tamanho:       ~250MB
Tempo inicial: 5-10s
Tempo/explicação: 2-5s
VRAM:          ~600MB
Qualidade:     ⭐⭐⭐ Bom
Velocidade:    ⭐⭐⭐⭐ Rápido
Foco:          Texto genérico
```

**Vantagens**:
- Rápido e leve
- Funciona bem em geral
- Bom compromisso

**Desvantagens**:
- Não especializado em matemática
- Às vezes erra em notação complexa

**Melhor para**: Teste inicial, máquinas com pouca RAM

---

### Flan-T5-Base
```
Tamanho:       ~900MB
Tempo inicial: 10-15s
Tempo/explicação: 3-6s
VRAM:          ~1GB
Qualidade:     ⭐⭐⭐⭐ Muito bom
Velocidade:    ⭐⭐⭐ Moderado
Foco:          Texto genérico (melhorado)
```

**Vantagens**:
- Melhor qualidade que Small
- Ainda razoavelmente rápido
- Mais detalhado nas explicações

**Desvantagens**:
- Ainda não especializado em matemática
- Um pouco mais lento

**Melhor para**: Usuários que querem mais qualidade sem modelos especializados

---

## Tabela Comparativa

| Modelo | Tamanho | Tempo/expr | Qualidade | Especialização | Recomendação |
|--------|---------|-----------|-----------|----------------|------|
| **LLaMA-2-7B-Math** | 7GB | 3-8s | ⭐⭐⭐⭐⭐ | Matemática | Melhor qualidade |
| **Mistral-7B-Math** | 7GB | 2-5s | ⭐⭐⭐⭐ | Matemática | **Recomendado** |
| **DeepSeek-Math-7B** | 7GB | 4-10s | ⭐⭐⭐⭐⭐ | Simbólico | Precisão máxima |
| **MathBERTa** | 110MB | 0.5-2s | ⭐⭐⭐ | LaTeX | Ultra-rápido |
| **Flan-T5-Base** | 900MB | 3-6s | ⭐⭐⭐⭐ | Genérico | Bom equilíbrio |
| **Flan-T5-Small** | 250MB | 2-5s | ⭐⭐⭐ | Genérico | Leve |

---

## Como Escolher

### 👤 Usuário Casual
→ Use **Flan-T5-Small** (padrão atual)  
Rápido, leve, funciona bem para expressões comuns.

### 📚 Pesquisador
→ Use **Mistral-7B-Math** ou **LLaMA-2-7B-Math**  
Qualidade excelente para papers complexos.

### 💻 Máquina com pouca RAM/GPU
→ Use **MathBERTa** ou **Flan-T5-Small**  
Compacto e rápido.

### 🚀 Precisa de máxima qualidade
→ Use **LLaMA-2-7B-Math**  
Melhor explicações profundas.

### ⚡ Precisa de máxima velocidade
→ Use **MathBERTa**  
Quase instantâneo.

---

## Como Trocar de Modelo

### Opção 1: Editar background.js (Direto)

```javascript
// Em src/background.js, linha 16-23, mude para:
model = await pipeline(
  'text-generation',
  'Xenova/Mistral-7B-Math',  // ← SUA ESCOLHA
  { device: 'webgpu', quantized: true }
);
```

Depois reload a extensão em `chrome://extensions/`

### Opção 2: Usar config.js (Futuro)

```javascript
// Copie config.example.js para config.js
cp config.example.js config.js

// Edite config.js:
MODEL: {
  primary: 'Xenova/Sua-Escolha',
  ...
}
```

---

## Performance Tips

### Para melhorar velocidade:
1. Use `quantized: true` (já no código)
2. Reduzir `max_new_tokens` em background.js
3. Usar modelo menor (MathBERTa)
4. Garantir GPU dedicada ativa

### Para melhorar qualidade:
1. Usar modelo especializado em matemática
2. Aumentar `max_new_tokens` (128 → 256)
3. Reduzir `temperature` (0.5 → 0.3)

### Para economizar memória:
1. Usar `quantized: true`
2. Escolher modelo compacto
3. Limpar cache periodicamente

---

## Testando Modelos

### Script para testar localmente:

```html
<!DOCTYPE html>
<html>
<head>
  <script type="module">
    import { pipeline } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers';

    async function testModel(modelName) {
      console.time(`Loading ${modelName}`);
      const p = await pipeline('text-generation', modelName, {
        device: 'webgpu',
        quantized: true
      });
      console.timeEnd(`Loading ${modelName}`);

      console.time(`Generating`);
      const result = await p('Explain: E=mc^2', {max_new_tokens: 100});
      console.timeEnd(`Generating`);

      console.log(result[0].generated_text);
    }

    testModel('Xenova/LLaMA-2-7B-Math-hf');
  </script>
</head>
<body>
  Abra DevTools (F12) para ver os resultados
</body>
</html>
```

---

## Próximos Passos

- [ ] Interface para trocar modelo sem editar código
- [ ] Auto-detection de GPU disponível
- [ ] Cache persistente de modelos
- [ ] Seleção dinâmica por área (Calculus vs Algebra)
