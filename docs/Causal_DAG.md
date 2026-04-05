# Causal DAG — Regimes de Incerteza e Catastrofes Regulatorias

> Grafo aciclico direcionado (DAG) mostrando relacoes causais entre condicoes e outcome.
> Base: modelo teorico do Capitulo 2 da tese.

---

## 1. DAG Principal

```
  DIV ─────────────┐
  (Diversidade      │
   Institucional)   │
                    ▼
  REG ──────────► FRAGMENTACAO ──► EROSAO ──► NORMALIZACAO ──► CAT
  (Complexidade     INFORMACIONAL   ENFORCEMENT  DO DESVIO     (Catastrofe)
   Regulatoria)     (P1)            (P2)         (P3)
                                      ▲
  ~ENF ────────────────────────────────┘
  (Ausencia de
   Enforcement)

  ORG ──────────► CAPTURA ──────► NORMALIZACAO ──► FALHA ──► CAT
  (Capacidade      REGULATORIA     DO DESVIO        NAO-LINEAR
   Organizacional)                 (P3)             (P4)

  POL ──────────► PRESSAO ──────► EROSAO ──────────────────► CAT
  (Politizacao)    POR RESULTADOS  ENFORCEMENT (P2)
```

## 2. Relacoes Causais

| De | Para | Tipo | Mecanismo |
|----|------|------|-----------|
| DIV | P1 | Direta | Multiplas agencias fragmentam informacao |
| REG | P1 | Direta | Complexidade regulatoria gera opacidade |
| ~ENF | P2 | Direta | Ausencia de fiscalizacao permite erosao |
| ORG | P3 | Direta | Capacidade organizacional facilita captura |
| POL | P2 | Direta | Pressao politica compromete rigor tecnico |
| P1 | P2 | Sequencial | Fragmentacao informacional enfraquece enforcement |
| P2 | P3 | Sequencial | Erosao do enforcement permite normalizacao |
| P3 | P4 | Sequencial | Normalizacao acumula risco ate falha nao-linear |
| P4 | CAT | Direta | Falha catastrofica e o outcome |

## 3. Independencia das Condicoes

| Par | Independentes? | Justificativa |
|-----|---------------|---------------|
| DIV-REG | Sim | DIV mede fragmentacao; REG mede complexidade (dimensoes diferentes) |
| DIV-ENF | Sim | Fragmentacao institucional != capacidade de fiscalizacao |
| DIV-ORG | Sim | Estrutura regulatoria != capacidade do regulado |
| REG-ENF | Parcial | Complexidade pode dificultar enforcement, mas sao construtos separados |
| REG-ORG | Sim | Framework regulatorio != capacidade organizacional |
| ENF-ORG | Sim | Enforcement e do regulador; ORG e do regulado |
| POL-todos | Sim | Politizacao e contextual, independente das demais |

## 4. Exclusao de GRAV

**GRAV** (Gravidade das consequencias) e excluida porque:
1. Sobrepoe-se conceitualmente ao outcome CAT (Schneider & Wagemann 2012, p.94)
2. GRAV alto -> CAT alto e quase tautologico (mais mortes = mais catastrofico)
3. GRAV e usada como variavel descritiva (SFC, DELTA), nao como condicao causal

## 5. QCA Pathway Derivado

Do DAG, o pathway esperado e:
```
DIV * ~ENF * ORG -> CAT
```

Onde:
- DIV contribui via P1 (fragmentacao)
- ~ENF contribui via P2 (ausencia de enforcement)
- ORG contribui via P3 (captura regulatoria)
- A cadeia P1->P2->P3->P4 opera como mecanismo causal testado pelo PT

## 6. Temporalidade

O DAG implica ordem temporal:
```
Condicoes estruturais (DIV, REG, ORG, POL)
  -> Instaladas ANTES do periodo de analise
  -> Path-dependent (Pierson 1997)

Condicao processual (~ENF)
  -> Opera DURANTE o periodo de analise
  -> Erosao gradual do enforcement

Mecanismo (P1->P2->P3->P4)
  -> Verificado pelo PT com evidencias temporalmente ordenadas
```
