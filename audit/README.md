# LLM Response Audit / Auditoria de Respostas LLM

> Samples of LLM responses for methodological audit.
> CNPq Portaria 2.664/2026: transparency in all research phases.

## Audit Methodology

For each LLM-assisted pipeline phase, we document:
1. **Input prompt** (what was asked)
2. **Raw LLM response** (what was returned)
3. **Human validation** (was the response used, modified, or rejected?)
4. **Quality assessment** (accuracy, relevance, bias detection)

## Sample Categories

### A. QCA Intercoder Coding (intercoder_debate.py)

**Sample size:** 30% of 65 cases x 6 core variables = ~117 codings
**Audit rate:** 10% of codings manually verified (12 samples)

| Case | Variable | Human Score | LLM Debate Score | Match? |
|------|----------|-------------|------------------|--------|
| Fundao-Germano | ENF | 0.17 | 0.17 | Yes |
| Brumadinho | ORG | 1.00 | 1.00 | Yes |
| Sul Superior | ENF | 0.83 | 0.83 | Yes |
| Arcturus | DIV | 0.50 | 0.501 | Yes (crossover adjusted) |

**Agreement rate:** Kappa = 0.910, Alpha = 0.923

### B. PT Evidence Collection (pt_auto_evidence.py)

**Total evidence items generated:** ~90 (6 cases x 5 parts x 3 items)
**Audit rate:** 20% manually verified against bibliography

**Validation criteria:**
- Source exists in bibliography (1,093 PDFs indexed)
- Factual claims match known data (SIGBM/ANM)
- Van Evera classification appropriate for evidence type

### C. Rival Hypothesis Generation (pt_09_rival_hypotheses.py)

**Total rivals generated:** 15 (3 per hypothesis H1-H5)
**Audit:** All 15 reviewed for steel-manning quality (Bennett 2010)

**Quality checks:**
- Priors in valid range [0.20, 0.50]? (no straw men)
- Fingerprints genuinely diagnostic?
- Mutually exclusive?
- At least 1 hoop test per rival? (refutability)

## Rejected LLM Outputs

LLM outputs were rejected when:
1. JSON parsing failed (fallback to structured defaults)
2. Fabricated citations detected (source not in bibliography)
3. Van Evera classification inconsistent with sensitivity/type_i values
4. Rival hypothesis was a trivial variant of main hypothesis

## Human Override Log

| Phase | Override | Reason |
|-------|----------|--------|
| pt_auto_evidence | 3 items removed | Fabricated source names |
| intercoder_debate | 0 overrides | All debate scores within tolerance |
| pt_09_rivals | 2 priors adjusted | Below Bennett (2010) minimum 0.20 |
