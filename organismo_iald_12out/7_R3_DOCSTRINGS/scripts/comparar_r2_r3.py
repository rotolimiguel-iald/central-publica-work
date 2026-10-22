# -*- coding: utf-8 -*-
"""R3: compara r2 x r3 lendo do KERNEL (meta_r2.txt / meta_r3.txt gravados por Meta_TEMPLATE.lean no MESMO sandbox
C:/t/mo3). Para cada constante do modulo TGLExt.IALD: especie, parametros de universo, interna?, hints/safety,
axiomas, TIPO e VALOR em dois modos (SA alfa-invariante; SN com nomes de binder) e o hash da docstring.
Codigo proprio; grava TIPOS_R2_VS_R3.json na raiz da R3. Falha visivel (exit 1) se qualquer tipo ou termo diferir."""
import json, os, re, hashlib, sys, datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M2 = "C:/t/mo3/meta/meta_r2.txt"
M3 = "C:/t/mo3/meta/meta_r3.txt"
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def h(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def ler(p):
    d = {}; ordem = []; cab = None
    with open(p, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.rstrip("\n")
            if not ln:
                continue
            parts = ln.split("\t")
            tag = parts[0]
            if tag == "MODULO":
                cab = parts; continue
            n = parts[1]
            if tag == "DECL":
                kind, internal, lps, extra, axs, doc = parts[2:8]
                d[n] = {"kind": kind, "internal": internal == "true", "lps": lps, "extra": extra,
                        "axiomas": [x for x in axs.split(",") if x], "doc_hash": doc}
                ordem.append(n)
            else:
                d[n][tag] = "\t".join(parts[2:])
    return cab, ordem, d


def cat(n, v):
    if v["internal"]:
        return "interna"
    if re.search(r"\.eq_\d+$", n):
        return "lema_de_equacao"
    if n.startswith("TGLExt.IALD."):
        return "publica"
    return "outra"


c2, o2, d2 = ler(M2)
c3, o3, d3 = ler(M3)
linhas = []
falhas = []
for n in sorted(set(d2) | set(d3)):
    a, b = d2.get(n), d3.get(n)
    if a is None or b is None:
        falhas.append(n); linhas.append({"nome": n, "presente_r2": a is not None, "presente_r3": b is not None}); continue
    reg = {"nome": n, "categoria": cat(n, a), "especie": a["kind"]}
    ok = True
    for campo in ("kind", "internal", "lps", "extra"):
        if a[campo] != b[campo]:
            ok = False; reg[campo + "_difere"] = [a[campo], b[campo]]
    reg["axiomas"] = a["axiomas"]
    reg["axiomas_iguais"] = a["axiomas"] == b["axiomas"]
    reg["axiomas_no_trio"] = set(b["axiomas"]) <= TRIO
    ok = ok and reg["axiomas_iguais"] and reg["axiomas_no_trio"]
    for campo in ("TYPEA", "TYPEN", "VALA", "VALN"):
        reg[campo + "_sha256_r2"] = h(a[campo]); reg[campo + "_sha256_r3"] = h(b[campo])
        reg[campo + "_igual"] = a[campo] == b[campo]
        reg[campo + "_chars"] = len(a[campo])
        ok = ok and reg[campo + "_igual"]
    reg["docstring_mudou"] = a["doc_hash"] != b["doc_hash"]
    reg["docstring_r2_presente"] = a["doc_hash"] != "-"
    reg["IDENTICA_tipo_e_termo"] = ok
    if not ok:
        falhas.append(n)
    linhas.append(reg)
cont = {}
for r in linhas:
    cont[r.get("categoria", "?")] = cont.get(r.get("categoria", "?"), 0) + 1
res = {"quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "metodo": ("Meta_TEMPLATE.lean le, no kernel do MESMO sandbox C:/t/mo3, cada constante do modulo TGLExt.IALD "
                  "(env.header.moduleData[idx].constNames): tipo e valor serializados SA (De Bruijn, sem nomes de binder, "
                  "mdata ignorado) e SN (com nome e info de cada binder e marca de mdata); a comparacao aqui e de "
                  "STRINGS INTEIRAS (os sha256 sao so para leitura humana)."),
       "meta_r2": {"arquivo": M2, "sha256": hashlib.sha256(open(M2, "rb").read()).hexdigest(), "cabecalho": c2},
       "meta_r3": {"arquivo": M3, "sha256": hashlib.sha256(open(M3, "rb").read()).hexdigest(), "cabecalho": c3},
       "n_constantes_r2": len(d2), "n_constantes_r3": len(d3), "mesma_ordem_no_modulo": o2 == o3,
       "contagem_por_categoria": cont,
       "n_identicas_tipo_e_termo_SA": sum(1 for r in linhas if r.get("TYPEA_igual") and r.get("VALA_igual")),
       "n_identicas_tipo_e_termo_SN": sum(1 for r in linhas if r.get("TYPEN_igual") and r.get("VALN_igual")),
       "n_docstring_mudou": sum(1 for r in linhas if r.get("docstring_mudou")),
       "docstring_mudou_em": [r["nome"] for r in linhas if r.get("docstring_mudou")],
       "n_axiomas_fora_do_trio_r3": sum(1 for r in linhas if r.get("axiomas_no_trio") is False),
       "n_sem_axioma": sum(1 for r in linhas if r.get("axiomas") == []),
       "falhas": falhas,
       "VEREDITO": "INVARIANTE_100_POR_CENTO" if not falhas else "DIFERE",
       "constantes": linhas}
json.dump(res, open(os.path.join(AQUI, "TIPOS_R2_VS_R3.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "constantes"}, ensure_ascii=False, indent=1))
sys.exit(0 if not falhas else 1)
