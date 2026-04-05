#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Accent Guardrail — Sanitizes Portuguese text before DOCX generation.
Centralizado: importado por generate_v8_report.py, generate_consolidated_chapter.py,
pt_07_generate_chapter.py e qualquer outro gerador DOCX.

Corrige palavras sem acento que o R cat() ou LLM podem produzir.
Regra: patterns mais longos primeiro para evitar substituicoes parciais.
"""

import re

# Comprehensive accent map: (wrong, correct)
# Organized by suffix pattern for maintainability
_ACCENT_PAIRS = [
    # -ção / -ções (most common)
    ("configuracoes", "configurações"), ("configuracao", "configuração"),
    ("explicacoes", "explicações"), ("explicacao", "explicação"),
    ("combinacoes", "combinações"), ("combinacao", "combinação"),
    ("calibracao", "calibração"), ("operacionalizacao", "operacionalização"),
    ("fragmentacao", "fragmentação"), ("normalizacao", "normalização"),
    ("fiscalizacao", "fiscalização"), ("subestimacao", "subestimação"),
    ("regulacao", "regulação"), ("producao", "produção"),
    ("selecao", "seleção"), ("regressao", "regressão"),
    ("investigacao", "investigação"), ("integracao", "integração"),
    ("validacao", "validação"), ("introducao", "introdução"),
    ("solucao", "solução"), ("solucoes", "soluções"),
    ("comparacao", "comparação"), ("avaliacao", "avaliação"),
    ("diversificacao", "diversificação"), ("classificacao", "classificação"),
    ("verificacao", "verificação"), ("intersecao", "interseção"),
    ("variacao", "variação"), ("variacoes", "variações"),
    ("aplicacao", "aplicação"), ("distribuicao", "distribuição"),
    ("correlacao", "correlação"), ("concentracao", "concentração"),
    ("organizacao", "organização"), ("informacao", "informação"),
    ("operacao", "operação"), ("situacao", "situação"),
    ("populacao", "população"), ("educacao", "educação"),
    ("relacao", "relação"), ("secao", "seção"),
    ("dimensao", "dimensão"), ("condicao", "condição"),
    ("condicoes", "condições"),

    # -ência / -ância
    ("inferencia", "inferência"), ("inferencias", "inferências"),
    ("evidencia", "evidência"), ("evidencias", "evidências"),
    ("frequencia", "frequência"), ("frequencias", "frequências"),
    ("suficiencia", "suficiência"), ("consistencia", "consistência"),
    ("equivalencia", "equivalência"), ("potencia", "potência"),
    ("ausencia", "ausência"), ("presenca", "presença"),
    ("consequencia", "consequência"), ("consequencias", "consequências"),
    ("tendencia", "tendência"), ("tendencias", "tendências"),
    ("convergencia", "convergência"), ("divergencia", "divergência"),
    ("transparencia", "transparência"), ("relevancia", "relevância"),
    ("tolerancia", "tolerância"), ("importancia", "importância"),

    # -ário / -ória / -ório
    ("regulatorio", "regulatório"), ("regulatorios", "regulatórios"),
    ("regulatoria", "regulatória"), ("regulatorias", "regulatórias"),
    ("metodologico", "metodológico"), ("metodologica", "metodológica"),
    ("sumario", "sumário"), ("necessario", "necessário"),
    ("contrario", "contrário"), ("ordinario", "ordinário"),

    # -ático / -ética / -ístico
    ("sistematica", "sistemática"), ("sistematico", "sistemático"),
    ("estatistica", "estatística"), ("estatisticas", "estatísticas"),
    ("probabilisticas", "probabilísticas"), ("probabilistica", "probabilística"),
    ("diagnostico", "diagnóstico"), ("diagnosticos", "diagnósticos"),

    # -ável / -ível / -ível
    ("variavel", "variável"), ("variaveis", "variáveis"),
    ("possivel", "possível"), ("possiveis", "possíveis"),
    ("provavel", "provável"), ("provaveis", "prováveis"),

    # -ímico / -ônico / -ético
    ("teorica", "teórica"), ("teorico", "teórico"),
    ("empirica", "empírica"), ("empiricas", "empíricas"),
    ("especifica", "específica"), ("especifico", "específico"),
    ("logica", "lógica"), ("pratica", "prática"), ("praticas", "práticas"),

    # -ítulo / -ênomeno / etc.
    ("capitulo", "capítulo"), ("fenomeno", "fenômeno"), ("fenomenos", "fenômenos"),
    ("hipotese", "hipótese"), ("hipoteses", "hipóteses"),
    ("catastrofe", "catástrofe"), ("catastrofes", "catástrofes"),
    ("indice", "índice"), ("indices", "índices"),

    # -étodo / -ível
    ("metodo", "método"), ("metodos", "métodos"),
    ("analise", "análise"), ("numero", "número"), ("numeros", "números"),
    ("minimo", "mínimo"), ("maximo", "máximo"), ("maxima", "máxima"),
    ("proximo", "próximo"), ("proxima", "próxima"),
    ("tipico", "típico"), ("tipicos", "típicos"),
    ("unica", "única"), ("unico", "único"),
    ("valido", "válido"), ("valida", "válida"),

    # -égia
    ("estrategia", "estratégia"), ("estrategias", "estratégias"),

    # -árias
    ("necessarias", "necessárias"), ("necessaria", "necessária"),

    # Short common words
    ("nao ", "não "), ("Nao ", "Não "),
    ("sao ", "são "), ("Sao ", "São "),
    ("tambem", "também"), ("porem", "porém"),
    ("alem ", "além "), ("atraves", "através"),
    ("ate ", "até "), ("entao", "então"),
    (" e avaliada", " é avaliada"), (" e utilizada", " é utilizada"),
    (" e calculada", " é calculada"), (" e definida", " é definida"),
    ("isto e,", "isto é,"), ("isto e ", "isto é "),
    (" e o ", " é o "), (" e a ", " é a "),
    (" e possivel", " é possível"), (" e necessario", " é necessário"),
]

# Build case-sensitive + capitalized versions
ACCENT_MAP = []
seen = set()
for wrong, right in _ACCENT_PAIRS:
    if wrong not in seen:
        ACCENT_MAP.append((wrong, right))
        seen.add(wrong)
    # Add Capitalized version
    cap_wrong = wrong[0].upper() + wrong[1:]
    cap_right = right[0].upper() + right[1:]
    if cap_wrong not in seen and cap_wrong != wrong:
        ACCENT_MAP.append((cap_wrong, cap_right))
        seen.add(cap_wrong)

# Sort by length descending (longer patterns first to avoid partial matches)
ACCENT_MAP.sort(key=lambda x: -len(x[0]))


def fix_accents(text):
    """Sanitize Portuguese text: restore diacritics stripped by R cat() or LLM output.

    This is a GUARDRAIL — runs before any text is written to DOCX.
    Safe to call multiple times (idempotent: already-correct text is unchanged).
    """
    if not text:
        return text
    for wrong, right in ACCENT_MAP:
        text = text.replace(wrong, right)
    return text


def fix_accents_regex(text):
    """Regex-based version for word-boundary-aware replacement.
    Slower but avoids partial-word matches (e.g., 'analise' inside 'paranalise')."""
    if not text:
        return text
    for wrong, right in ACCENT_MAP:
        text = re.sub(r'\b' + re.escape(wrong) + r'\b', right, text)
    return text


if __name__ == "__main__":
    # Self-test
    test = "A analise sistematica das catastrofes regulatorias nao e possivel sem evidencias empiricas."
    fixed = fix_accents(test)
    print(f"Input:  {test}")
    print(f"Output: {fixed}")
    assert "análise" in fixed
    assert "sistemática" in fixed
    assert "catástrofes" in fixed
    assert "regulatórias" in fixed
    assert "não" in fixed
    assert "evidências" in fixed
    assert "empíricas" in fixed
    print("[OK] All accent guardrail tests pass")
