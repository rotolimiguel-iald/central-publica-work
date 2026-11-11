# -*- coding: utf-8 -*-
"""Revisor v410 conferencia unica D109: corpus RENDIDO (so' leitura). Leva: artigo PT/EN (TXT do ensaio a seco), .md embutido, folhas de texto dos registros do core de ensaio, textos do harness, rascunho da custodia, relatorio de preparacao."""
import json, re, sys, os
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"


def ws(s):
    return re.sub(r"\s+", " ", s).strip()


def leaves(x, p=""):
    if isinstance(x, str):
        yield p, x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from leaves(v, p + "." + str(k))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, p + "[%d]" % i)


def rd(p):
    return open(p, "rb").read().decode("utf-8", "replace")


def carregar():
    C = {}
    C["pt"] = ws(rd(R + "dry_v410/dry_v410_pt.txt"))
    C["en"] = ws(rd(R + "dry_v410/dry_v410_en.txt"))
    C["md"] = rd(R + "dry_v410/um_absoluto_forma_canonica.md")
    core = json.load(open(R + "dry_v410/core_ensaio.json", encoding="utf-8"))
    reg = {}
    for k, v in core["core"].items():
        if k.endswith("_v410") or k in ("beta_escala_errata_v392",):
            reg[k] = [(k + p, ws(t)) for p, t in leaves(v) if len(t) > 3]
    C["reg"] = reg  # nome do registro -> lista (caminho, texto)
    C["verdict"] = [("verdict" + p, ws(t)) for p, t in leaves(core["verdict"]) if len(t) > 3]
    H = json.load(open(R + "pos_rito/HARNESS_TEXTOS_ENSAIO_v410.json", encoding="utf-8"))
    C["harness"] = [("harness" + p, ws(t)) for p, t in leaves(H) if len(t) > 3]
    C["custodia"] = rd(R + "pos_rito/CUSTODIA_v410_RASCUNHO.txt")
    C["custodia_ws"] = ws(C["custodia"])
    p = R + "RELATORIO_PREPARACAO_v410.md"
    C["relatorio"] = rd(p) if os.path.exists(p) else ""
    return C


def todos_registros(C):
    out = []
    for k, L in C["reg"].items(): out += L
    return out


def ctx(texto, m, n=130):
    a = max(0, m.start() - n); b = min(len(texto), m.end() + n)
    return texto[a:b]


def achar(texto, rx, flags=0, n=130):
    ms = list(re.finditer(rx, texto, flags))
    return len(ms), (ctx(texto, ms[0], n) if ms else "")


def achar_em_folhas(folhas, rx, flags=0, n=130):
    tot = 0; onde = []
    for p, t in folhas:
        ms = list(re.finditer(rx, t, flags))
        if ms:
            tot += len(ms)
            if len(onde) < 4: onde.append((p, ctx(t, ms[0], n)))
    return tot, onde


if __name__ == "__main__":
    C = carregar()
    print({k: (len(v) if not isinstance(v, dict) else {kk: len(vv) for kk, vv in v.items()}) for k, v in C.items()})
