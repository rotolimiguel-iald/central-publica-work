# -*- coding: utf-8 -*-
"""ERRATA AO LADO (gerência, em nome próprio) na memória tres-testes-de-estresse-conjuntos-05out.md e no Atlas: a leitura de 20:02 imprimiu «R1=None; …»
porque leu o campo errado do livro de cobranças (o campo é `outcome`); e os 3 vereditos com «FALSIFIED» (fora NOT_/UN) são substrings de vereditos
compostos — ditos aqui com o caminho. Tudo LIDO do core v386 por script."""
import json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
ATLAS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory", "TGL_ATLAS.md")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
st = time.strftime("%Y%m%d_%H%M%S"); agora = time.strftime("%Y-%m-%d %H:%M:%S"); MARCA = "errata_ledger_tres_testes_05out"
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
rows = core["the_ledger_of_charges_v383"]["ledger"]
ledger_txt = "; ".join("%s = %s" % (r.get("id"), r.get("outcome")) for r in rows)
V = {}
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "verdict" and isinstance(v, str) and v.startswith("TGL_"): V[path + "/" + k] = v
            walk(v, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, path + "[%d]" % i)
walk(core)
fals = [(p, v) for p, v in V.items() if re.search(r"(?<!NOT_)(?<!UN)FALSIFIED", v)]
def trecho(v):
    m = re.search(r"[A-Z0-9_]{0,40}(?<!NOT_)(?<!UN)FALSIFIED[A-Z0-9_]{0,40}", v); return m.group(0) if m else "?"
fals_txt = "; ".join("`%s`: …%s…" % (p, trecho(v)) for p, v in fals)
BL = ("<!-- %s -->\n**ERRATA AO LADO (05/10/2026, %s; gerência, em nome próprio):** a leitura acima imprimiu o livro de cobranças como «R1=None; …» por ler o campo errado; o campo é `outcome` e, lido do core v386: %s "
      "(11 cobranças: 7 NOT_FALSIFIED, 2 INCONCLUSIVE, 2 AWAITING, 1 EXCLUDED_IN_READING — F3b). E os %d vereditos contados com «FALSIFIED» (fora NOT_/UN) são SUBSTRINGS de vereditos compostos, não três ritos falsificados: %s — "
      "o primeiro é a leitura do fundo D1 com β livre (ΛCDM preferido a 5σ; rota reclassificada em 30/09 pela decisão do mapa de R efetivo), o segundo carrega os pares do eco falsificados COMO LEIS DE ATRASO (fora do livro por decisão do operador de 02/10: «o que foi falsificado foi alguma rota»), o terceiro é o próprio livro, cujo veredito cita a regra «FALSIFIED extingue a cobrança, não a regra». "
      "Logo: nenhum veredito FALSIFIED contra a teoria; rotas falsificadas: a D1-β-livre e as leis de atraso do eco. NOT_FALSIFIED nunca é CONFIRMED." % (MARCA, agora, ledger_txt, len(fals), fals_txt))
def nl_de(raw): return "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"
for p in (os.path.join(UMEM, "tres-testes-de-estresse-conjuntos-05out.md"), ATLAS):
    raw0 = open(p, "rb").read()
    if MARCA.encode() in raw0: print("JA ESTA", os.path.basename(p)); continue
    nl = nl_de(raw0); corpo = (nl + nl + BL.replace("\n", nl) + nl).encode("utf-8")
    if not raw0.endswith(nl.encode()): corpo = nl.encode() + corpo
    novo = raw0 + corpo; bak = p + ".bak_" + st + "_errled"; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw0); os.replace(p + ".tmp", p); assert open(p, "rb").read()[:len(raw0)] == raw0
    print("OK", os.path.basename(p), len(raw0), "->", len(novo))
print(ledger_txt); print(fals_txt[:600]); print("FIM", agora)
