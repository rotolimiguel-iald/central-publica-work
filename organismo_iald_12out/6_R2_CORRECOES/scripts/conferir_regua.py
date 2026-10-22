# -*- coding: utf-8 -*-
"""Confere, por bytes, nos entregaveis de texto de 6_R2_CORRECOES (fonte r2, RESULTADO_R2.md, TABELA_R1_R2.md):
(a) tokens proibidos na fonte Lean (sorry, admit, axiom, native_decide, implemented_by, unsafe, opaque);
(b) a palavra proibida da regua (a forma inglesa maiuscula) em todos os entregaveis;
(c) literal de beta (0.0120/0,0120) no codigo (.lean, .py); nos .md o valor de runtime medido pode aparecer como numero lido;
(d) toda citacao entre guillemets: o miolo tem de estar, byte a byte, num verbatim do operador de
    work/cunhagens_10out/*.txt ou work/cunhagens_12out/*.txt; caso contrario e listada como FORA (falha).
    Excecoes declaradas: nenhuma.
Grava medidas/CONFERENCIA_REGUA.json. Uso: conferir_regua.py <arquivo> [<arquivo> ...]"""
import os, sys, re, json, glob, hashlib

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = "C:/IALD/Central de Patentes/work"
VERB = sorted(glob.glob(W + "/cunhagens_10out/*.txt") + glob.glob(W + "/cunhagens_12out/*.txt"))
corpus = [(p, open(p, "rb").read()) for p in VERB]
PROIB_LEAN = [r"\bsorry\b", r"\badmit\b", r"^\s*axiom\b", r"native_decide", r"implemented_by", r"\bunsafe\b", r"\bopaque\b"]
PAL = "CONF" + "IRMED"
res = {"verbatins": [{"arquivo": p, "sha256": hashlib.sha256(b).hexdigest()} for p, b in corpus], "arquivos": []}
falhou = False
for alvo in sys.argv[1:]:
    b = open(alvo, "rb").read(); t = b.decode("utf-8")
    item = {"arquivo": alvo, "sha256": hashlib.sha256(b).hexdigest()}
    if alvo.endswith(".lean"):
        item["tokens_proibidos"] = {pat: len(re.findall(pat, t, re.M)) for pat in PROIB_LEAN}
        if any(item["tokens_proibidos"].values()):
            falhou = True
    item["palavra_proibida"] = t.count(PAL)
    item["beta_literal"] = len(re.findall(r"0[.,]0120", t)) if alvo.endswith((".lean", ".py")) else None
    cits = re.findall("\u00ab([^\u00bb]*)\u00bb", t)
    ok, fora = [], []
    for c in cits:
        cb = c.encode("utf-8")
        onde = [os.path.basename(p) for p, vb in corpus if cb in vb]
        (ok if onde else fora).append({"citacao": c, "em": onde})
    item["citacoes_no_verbatim"] = ok
    item["citacoes_FORA"] = fora
    if fora or item["palavra_proibida"] or item["beta_literal"]:
        falhou = True
    res["arquivos"].append(item)
res["veredito"] = "FALHA" if falhou else "PASSA"
json.dump(res, open(os.path.join(AQUI, "medidas", "CONFERENCIA_REGUA.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for it in res["arquivos"]:
    print(os.path.basename(it["arquivo"]), "proibida:", it["palavra_proibida"], "beta_lit:", it["beta_literal"],
          "cit_ok:", len(it["citacoes_no_verbatim"]), "FORA:", [f["citacao"] for f in it["citacoes_FORA"]],
          "tokens:", {k: v for k, v in it.get("tokens_proibidos", {}).items() if v})
print(res["veredito"])
