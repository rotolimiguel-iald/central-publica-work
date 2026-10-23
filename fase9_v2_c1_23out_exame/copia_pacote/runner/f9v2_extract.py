# -*- coding: utf-8 -*-
"""f9v2_extract.py -- E5: os centros locais saem da FONTE (bytes ja' conferidos por sha256), por regra PINADA no registro D-H; nunca de um ALVOS montado a mao.
Regra de extracao = {kind: html|pdf, page (pdf), regex com grupos nomeados, sigma_rule}. Exige UMA ocorrencia. Dado nao confiavel: so regex sobre texto."""
import math
import re

import f9v2_text as T


class ExtractionError(RuntimeError):
    pass


def _num(s):
    return float(s.replace(" ", ""))


def apply_sigma_rule(rule, g):
    kind = rule["kind"]
    if kind == "direct":
        return _num(g[rule["group"]])
    if kind == "quadrature":
        return math.sqrt(sum(_num(g[k]) ** 2 for k in rule["groups"]))
    if kind == "mean_asym":
        return (_num(g[rule["plus"]]) + _num(g[rule["minus"]])) / 2.0
    raise ExtractionError("sigma_rule desconhecida: %r" % kind)


def extract_reader(rule, raw):
    """-> {H0, sigma, matched, groups}. raw = bytes da fonte (ja' conferidos)."""
    if rule["kind"] == "html":
        texts = [("html", T.html_to_text(raw))]
    elif rule["kind"] == "pdf":
        pages = T.pdf_pages_text(raw)
        pg = int(rule["page"])
        if not 1 <= pg <= len(pages):
            raise ExtractionError("pagina %d fora do PDF (%d paginas)" % (pg, len(pages)))
        texts = [("p%d" % pg, pages[pg - 1])]
    else:
        raise ExtractionError("kind desconhecido")
    where, text = texts[0]
    ms = list(re.finditer(rule["regex"], text))
    if len(ms) != 1:
        raise ExtractionError("a regra casou %d vezes em %s (exige exatamente 1)" % (len(ms), where))
    g = ms[0].groupdict()
    H0 = _num(g[rule["H0_group"]])
    sigma = apply_sigma_rule(rule["sigma_rule"], g)
    return {"H0": H0, "sigma": sigma, "onde": where, "trecho": ms[0].group(0)[:400], "grupos": g}
