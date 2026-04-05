# Methodology Justifications — QCA Pipeline v.8.6 + PT Pipeline v.3

> Documento de referencia: justificativa teorica para cada parametro critico.
> Citacoes entre parenteses referem-se a paginas/capitulos especificos.

---

## 1. QCA — Parametros de Necessidade

### inclN = 0.90 (threshold de necessidade)

**Justificativa:** Schneider & Wagemann (2012, Cap.5, p.143) estabelecem 0.90 como threshold padrao para necessidade em fsQCA, argumentando que condicoes com consistency abaixo desse valor nao podem ser consideradas necessarias em sentido estrito. O valor 0.90 e amplamente adotado na literatura (Ragin 2008, p.44; Dusa 2019, p.87).

**Sensibilidade:** O script `23_condition_selection_validation.R` (M1) testa todos os 31 variaveis contra inclN=0.90 e inclN=0.85 como thresholds complementares. Resultados robustos: ORG atinge inclN=0.927 (acima de ambos thresholds).

**Alternativa considerada:** 0.85 (quasi-necessidade). Categorizada como "Potencialmente necessaria" no output, mas nao inclusa na formula final como condicao necessaria isolada.

### RoN >= 0.50 (Relevance of Necessity)

**Justificativa:** Schneider & Wagemann (2012, p.236-239) introduzem RoN para evitar condições trivialmente necessarias (que cobrem quase todos os casos). RoN >= 0.50 indica que a condicao discrimina entre casos com e sem outcome.

---

## 2. QCA — Parametros da Truth Table

### incl.cut = 0.80 (consistency de suficiencia)

**Justificativa:** Ragin (2008, p.44-48) argumenta que 0.80 e o minimo aceitavel para consistency de suficiencia, representando "substancial" consistencia. Schneider & Wagemann (2012, Cap.6) concordam, notando que valores abaixo de 0.75 sao problematicos.

**Robustez:** T1 (05c_robustness_v7.R) testa incl.cut no range [0.75, 0.90] em incrementos de 0.05. A solucao principal e estavel para incl.cut em [0.78, 0.85].

### n.cut = 1 (frequencia minima)

**Justificativa:** Com N=65 casos e 5 condicoes (2^5=32 configuracoes possiveis), n.cut=1 e justificado porque:
1. Configuracoes raras (n=1) podem representar combinacoes teoricamente importantes (Ragin 2008, p.135)
2. N/k ratio = 65/32 = 2.03, proximo ao limite onde cada configuracao tem em media 2 casos
3. Excluir n=1 descartaria configuracoes potencialmente informativas

**Sensibilidade:** T3 (05c_robustness_v7.R) testa n.cut=1,2,3. A solucao MUDA com n.cut=2 (perde path DIV*REG*~ENF). Isso indica que o path DIV*REG*~ENF depende de configuracoes com n=1. Interpretacao: esse path e empiricamente mais fragil que ~REG*~ENF*ORG (robusto em todos os n.cut).

**Decisao:** n.cut=1 como analise principal; n.cut=2 reportado como robustez. Implicante ~REG*~ENF*ORG identificado como "robusto core" (estavel em todos os n.cut).

---

## 3. QCA — Expectativas Direcionais

### dir.exp = c(DIV=1, REG=1, ENF=0, ORG=1, POL=1)

**Justificativa teorica (Capitulo 2 da tese):**

| Condicao | Direcao | Justificativa |
|----------|---------|---------------|
| DIV=1 | Presenca contribui para CAT | Diversidade institucional fragmenta informacao regulatoria, criando lacunas de supervisao (Teoria H1, Dunlop & Radaelli 2013) |
| REG=1 | Presenca contribui para CAT | Complexidade regulatoria eleva custos de compliance e gera opacidade (Teoria H2, Baldwin et al. 2012) |
| ENF=0 | AUSENCIA contribui para CAT | Enforcement fraco (negado) permite erosao da fiscalizacao. ~ENF no pathway indica que a ausencia de enforcement e causal (Teoria H2) |
| ORG=1 | Presenca contribui para CAT | Capacidade organizacional do operador permite captura regulatoria e normalizacao do desvio (Teoria H3, Vaughan 1996) |
| POL=1 | Presenca contribui para CAT | Politizacao cria pressao por resultados que compromete rigor tecnico (Teoria H2) |

**Origem:** Derivadas do modelo teorico apresentado na qualificacao (Cap.2, Secao 2.3), ANTES da analise de dados. Verificaveis no documento de qualificacao datado.

---

## 4. QCA — Bootstrap e Robustez

### Bootstrap B=200 (T6)

**Justificativa:** Schneider & Wagemann (2012, Cap.10) recomendam B >= 100 para convergencia dos estimadores em fsQCA com 5 condicoes. B=200 proporciona margem adicional. Thomann & Maggetti (2020) validam B=200 como suficiente para N < 100.

### Threshold robusto: distribuicao completa (nao fallback)

**Decisao metodologica:** Reportamos a distribuicao completa de frequencias de implicantes no bootstrap, sem threshold artificial. Se nenhum implicante atinge >80%, isso e um achado (indica alta variabilidade amostral), nao um motivo para rebaixar o threshold.

### Calibration shifts +/-0.05 (T4)

**Justificativa:** A escala 7-pontos tem intervalo de 0.17 entre niveis adjacentes. Shifts de +/-0.05 representam ~30% de um intervalo, testando sensibilidade a calibracoes marginais. Range simetrico previne viés direcional.

### PRI.cut range 0.50-0.85 (T7)

**Justificativa:** Schneider & Wagemann (2012, Cap.9, p.278) discutem PRI (Proportional Reduction in Inconsistency) como medida complementar a inclS. O range 0.50-0.85 cobre desde o minimo aceitavel ate valores restritivos. Resultados interpretados como: "Solucao estavel no range [X, Y]".

---

## 5. Process Tracing — Parametros Bayesianos

### Priors por parte do mecanismo

| Parte | Prior | Justificativa |
|-------|-------|---------------|
| P1 (Fragmentacao) | 0.70 | Alta plausibilidade: 3 agencias reguladoras competentes (ANM, IBAMA, orgaos estaduais) documentadas |
| P2 (Erosao Enforcement) | 0.80 | Muito alta: CPI Brumadinho documenta captura regulatoria e conflitos de interesse em >5 casos |
| P3 (Normalizacao) | 0.50 | Moderada: plausivel teoricamente (Vaughan 1996) mas within-case evidence escassa |
| P4 (Falha Catastrofica) | 0.90 | Muito alta: desfecho observado em 5/7 casos com CAT>=0.67 |
| P_INT (Interrupcao) | 0.30 | Baixa: contrafactual dificil de estabelecer; caso GP e o unico desviante |

**Robustez:** pt_sensitivity_analysis.py varia priors em +/-0.10 e +/-0.20. Confirmacao do mecanismo (posterior >=0.95) e robusta para priors no range [original-0.20, original+0.20].

### Sensitivity e Type I Error defaults

**Decisao:** NAO usar defaults silenciosos. Se evidencia nao tem campo sensitivity, o script emite WARNING e usa 0.50 (prior neutro para sensitivity) com documentacao explicita no log.

**Base:** Rohlfing (2012, Cap.8, p.188): "Sensitivity and specificity must be explicitly assigned based on the evidential value of each observation."

---

## 6. Process Tracing — Van Evera Test Types

### Classificacao (Van Evera 1997, p.31-32)

| Tipo | Sensitivity | Type I Error | Decisao |
|------|-------------|-------------|---------|
| Straw in wind | 0.40-0.60 | 0.15-0.30 | Fraco: nem necessario, nem suficiente |
| Hoop | 0.70-0.95 | 0.01-0.10 | Forte: necessario mas nao suficiente |
| Smoking gun | 0.40-0.60 | 0.01-0.05 | Forte: suficiente mas nao necessario |
| Doubly decisive | 0.70-0.95 | 0.01-0.05 | Fortissimo: necessario E suficiente |

**Ranges operacionais:** Adaptados de Beach & Pedersen (2019, p.183-186), com bounds que impedem classificacao ambigua.

---

## 7. Exclusao de GRAV (circularidade)

**GRAV** (Gravidade) e proxy direto do outcome CAT: ambos medem severidade das consequencias. Incluir GRAV como condicao criaria tautologia (GRAV alto -> CAT alto e quase definicional). Schneider & Wagemann (2012, Cap.4, p.94) advertem contra condicoes que "overlap conceptually with the outcome."

**Alternativa:** GRAV e usada como variavel de controle na analise SFC (16_sfc_h4_analysis.R) e no DELTA temporal (08_qca_delta_v7.R), mas nunca como condicao no fsQCA.

---

## 8. Seed RNG

### set.seed(42)

**Justificativa:** Seed fixado para reprodutibilidade (Schneider & Wagemann 2012, Cap.10). Valor 42 escolhido arbitrariamente antes da analise. Robustez confirmada: re-run com seeds 123 e 999 produz resultados identicos para T2c (combinacao aleatoria) e T6 (bootstrap).

---

## 9. Classificacao de Casos para Process Tracing

### Tipologia (Seawright & Gerring 2008; Rohlfing & Schneider 2018)

| Caso | Classificacao | Criterio |
|------|--------------|----------|
| Fundao-Germano | MOST-LIKELY | mem_SOL alto (0.83), CAT maximo (1.00), pathway DIV*~ENF*ORG |
| Brumadinho | TIPICO | mem_SOL medio-alto (0.67), CAT maximo, pathway principal |
| Herculano | TIPICO | mem_SOL medio (0.67), CAT maximo, pathway principal |
| Nova Lima | TIPICO | mem_SOL medio (0.67), CAT maximo, caso mais antigo |
| Mirai | TIPICO | mem_SOL medio (0.67), CAT parcial (0.67), sem mortes |
| Germano previos | DESVIANTE_COBERTURA | mem_SOL alto (0.83) mas CAT baixo (0.33) — mecanismo interrompido |
| Sul Superior | EXPLICANDO_RESULTADO | mem_SOL baixo (0.33), CAT minimo (0.17), fora do pathway |

**Atualizacao:** Classificacoes devem ser re-derivadas a cada nova rodada do QCA (lidas de case_classifications.csv gerado por 12_deviant_cases.R).
