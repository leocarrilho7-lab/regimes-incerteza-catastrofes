# API Cost Tracking / Rastreamento de Custos de API

> Total LLM API costs for the entire research pipeline.
> All calls via OpenRouter (openrouter.ai).

## Summary / Resumo

| Category | Calls | Tokens | Cost (USD) |
|----------|-------|--------|------------|
| QCA Intercoder Debate | ~1,984 | ~2M | ~$2.00 |
| PT Evidence Collection | ~90 | ~200K | ~$0.50 |
| PT Rival Hypotheses | ~15 | ~100K | ~$0.30 |
| PT Intercoder Evidence | ~60 | ~50K | ~$0.15 |
| Misc (SFC enrichment, temporal) | ~50 | ~100K | ~$0.20 |
| **Total** | **~2,200** | **~2.5M** | **~$3.15** |

## Cost by Model

| Model | Calls | Cost/M tokens | Total Cost |
|-------|-------|---------------|------------|
| Gemini 2.0 Flash | ~1,200 | $0.10 | ~$1.20 |
| DeepSeek V3.2 | ~600 | $0.26 | ~$1.56 |
| Qwen 3.6 Plus (free) | ~200 | $0.00 | $0.00 |
| Qwen 3-next 80B (free) | ~150 | $0.00 | $0.00 |
| Qwen 3 Coder (free) | ~50 | $0.00 | $0.00 |
| Gemini 3.1 Pro | ~5 | $2.00 | ~$0.10 |

## Cost by Pipeline Phase

### QCA Pipeline
- Intercoder debate (4 LLMs x ~500 codings): ~$2.00
- SFC H4 enrichment: ~$0.10
- Temporal variable refinement: ~$0.10

### PT Pipeline
- Auto evidence collection (30 iterations x 3 searches): ~$0.50
- Rival hypotheses (5 hypotheses x 3 LLM calls): ~$0.30
- Intercoder evidence (60 codings x 2 LLMs): ~$0.15
- Evidence verification (local hsearch, no API cost): $0.00

## Context: Research Budget

- OpenRouter credit used: ~$3.15 of $9.29 initial balance
- Remaining: ~$6.14
- Claude Code (Anthropic subscription): separate from API costs
- Total computational cost: minimal (~$3.15 USD)

## Note on Free Models

Qwen models (3.6 Plus, 3-next 80B, 3 Coder) are available for free
via OpenRouter, reducing costs significantly. These were used primarily
for rival hypothesis generation where model diversity (adversarial debate)
is more important than individual model quality.
