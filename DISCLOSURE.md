# Disclosure: Uso de Inteligencia Artificial na Pesquisa

> Documento de transparencia conforme:
> - Portaria CNPq n. 2.664/2026 (Politica de Integridade na Atividade Cientifica)
> - Diretrizes CAPES para uso de IA em pesquisa (2025)
> - Diretrizes para Uso Etico de IA Generativa (Sampaio, Sabbatini & Limongi, 2025)
> - ICLR 2026 LLM Policy
> - APSA Guidelines for Reproducibility

## 1. Declaracao de Responsabilidade

O autor assume responsabilidade integral por todo o conteudo desta tese,
incluindo analise, interpretacao e conclusoes. Nenhum modelo de linguagem
(LLM) e co-autor ou contribuinte intelectual autonomo. Todos os outputs
de IA foram revisados, verificados e validados pelo autor antes da inclusao.

## 2. Modelos de IA Utilizados

| Modelo | Provedor | Versao | Funcao no Pipeline | Custo Estimado |
|--------|----------|--------|-------------------|----------------|
| Claude Opus 4.6 | Anthropic | 2026 | Desenvolvimento de codigo, revisao, brainstorming | Assinatura |
| Gemini 2.0 Flash | Google (via OpenRouter) | 2025 | Codificacao intercoder QCA, evidence extraction PT | ~$2.00 |
| DeepSeek V3.2 | DeepSeek (via OpenRouter) | 2025 | Critica adversarial (intercoder debate), judge | ~$1.50 |
| Qwen 3.6 Plus | Alibaba (via OpenRouter) | 2025 | Proposicao de hipoteses rivais (Thompson Sampling) | $0.00 (free) |
| Qwen 3-next 80B | Alibaba (via OpenRouter) | 2025 | Critica de hipoteses rivais | $0.00 (free) |

**Custo total estimado de API:** ~$5.00 USD (OpenRouter)

## 3. Funcoes Especificas de Cada LLM

### 3.1 No Pipeline QCA (qca_pipeline/)

| Etapa | Script | LLM | Funcao |
|-------|--------|-----|--------|
| Intercoder Reliability | intercoder_debate.py | Gemini Flash + DeepSeek V3.2 | Codificacao fuzzy adversarial (Propose-Critique-Resolve-Judge) |
| ML Enhancement | phase04_multi_importance.py | Nenhum (scikit-learn) | Importancia de features via ensemble |
| Condition Selection | contextual_debate.py | 6 modelos (LinUCB bandit) | Selecao adaptativa de modelos para codificacao |

### 3.2 No Pipeline PT (process_tracing/)

| Etapa | Script | LLM | Funcao |
|-------|--------|-----|--------|
| Evidence Collection | pt_auto_evidence.py | Gemini Flash | Sintese de evidencias a partir da bibliografia |
| Rival Hypotheses | pt_09_rival_hypotheses.py | Qwen 3.6 + Qwen 80B + DeepSeek V3.2 | Geracao, critica e julgamento de hipoteses rivais |
| Intercoder Evidence | pt_intercoder_evidence.py | Gemini Flash + DeepSeek V3.2 | Confiabilidade inter-codificador para evidencias PT |
| Evidence Verification | pt_03_evidence_verification.py | Nenhum (hybrid_search local) | Verificacao documental na bibliografia |

### 3.3 Na Redacao da Tese

| Funcao | Ferramenta | Descricao |
|--------|-----------|-----------|
| Revisao de texto | Claude Opus 4.6 | Revisao de estilo, clareza, consistencia |
| Formatacao ABNT | Claude Opus 4.6 | Verificacao de normas bibliograficas |
| Brainstorming | Claude Opus 4.6 | Exploracao de argumentos e contra-argumentos |

## 4. O que NAO foi feito por IA

- Definicao das hipoteses (H1-H5): derivadas da literatura e da qualificacao
- Selecao de condicoes QCA (DIV, REG, ENF, ORG, POL): fundamentacao teorica do autor
- Calibracao fuzzy: codificacao manual com intercoder validation
- Interpretacao dos resultados: analise exclusiva do autor
- Escolhas metodologicas (thresholds, testes de robustez): fundamentadas na literatura
- Redacao final da tese: autoria integral do pesquisador

## 5. Salvaguardas Metodologicas

| Salvaguarda | Descricao |
|-------------|-----------|
| Intercoder Reliability | Kappa = 0.910, Alpha = 0.923 (LLM vs humano, 30% amostra) |
| Rival Hypotheses Testing | 15 rivais geradas por LLM, testadas bayesianamente (Bennett 2010) |
| QC Gate | 7 verificacoes automaticas antes de gerar capitulo |
| Accent Guardrail | 100+ patterns para corrigir acentos em outputs LLM |
| Reproducibility | set.seed(42) documentado em todos os scripts com justificativa |

## 6. Conformidade com Portaria CNPq 2.664/2026

| Requisito CNPq | Atendimento | Evidencia |
|----------------|-------------|-----------|
| Declarar uso de IAG | Sim | Este documento (secoes 2-3) |
| Especificar ferramenta e finalidade | Sim | Tabelas detalhadas por etapa |
| Nao submeter conteudo IAG como autoria humana | Sim | Secao 4 (O que NAO foi feito por IA) |
| Responsabilidade integral do autor | Sim | Secao 1 (Declaracao) |
| Transparencia em todas as etapas | Sim | Pipeline documentado com parametros |
| Nao inserir projetos de terceiros em IAG | Sim | Dados proprios, sem projetos alheios |

## 7. Reproducibilidade e Acesso ao Codigo

O repositorio publico contem: arquitetura do pipeline, parametros metodologicos,
justificativas de cada escolha analitica, e declaracao completa de uso de IA.

O codigo-fonte completo (scripts R e Python) esta disponivel sob solicitacao
ao autor para fins de auditoria e replicacao academica. O codigo esta em
aperfeicoamento continuo como parte da pesquisa de doutorado e sera
disponibilizado integralmente apos a defesa.

**Repositorio publico:** [a ser criado - GitHub]
**Contato para acesso ao codigo:** [email do autor]

### Para replicacao:
1. R 4.5.2 + pacotes: QCA (3.23), cna, ggplot2, cluster, vegan, parallel
2. Python 3.13 + pacotes: scikit-learn (1.8.0), python-docx, openpyxl, requests
3. Dataset: Base_Barragens_v9.xlsx (65 casos, 36 variaveis fuzzy, 7-point scale)
4. Executar: `Rscript run_pipeline.R` (QCA, 33 steps) + `python pt_run_pipeline.py` (PT, 15 phases)

## 8. Referencias Normativas e Metodologicas

- Portaria CNPq n. 2.664/2026: Politica de Integridade na Atividade Cientifica
- CAPES (2025): A inteligencia artificial na pesquisa e no fomento
- Sampaio, R.C., Sabbatini, M. & Limongi, R. (2025): Diretrizes para Uso Etico de IAG
- ICLR 2026 LLM Policy: https://blog.iclr.cc/2025/08/26/policies-on-large-language-model-usage-at-iclr-2026/
- APSA Guidelines for Reproducibility: https://apsanet.org/publications/journals/american-political-science-review/guidelines-for-reproducibility/
- Political Analysis Replication Guidelines (2025): Cambridge University Press
- Schneider & Wagemann (2012): Set-Theoretic Methods, Ch. 10 (Reproducibility)
- Beach & Pedersen (2019): Process-Tracing Methods, Ch. 7-8 (Evidence Coding)
