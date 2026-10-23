# -*- coding: utf-8 -*-
"""verificar_extracao.py -- auditoria c1 (23/10/2026), item 2: (a) sha256 de cada fonte == registro D-H == spec; (b) identidade das fontes baixadas
(arXiv id, titulo, autores no HTML); (c) a regra pinada casa UMA vez e devolve o declarado; (d) o declarado da spec V2-c1 == o da R5.2.
Nenhum composto e' calculado. Rodar com python -P -E -B (nao escreve __pycache__ no pacote)."""
import sys, os, json, hashlib, re
sys.dont_write_bytecode = True
PK = r"C:\IALD\Central de Patentes\work\fase9_v2_c1_23out"
sys.path.insert(0, os.path.join(PK, "runner"))
import f9v2_extract as EXT, f9v2_text as T
reg = json.load(open(os.path.join(PK, "spec", "REGISTRO_DH_V2_C1.json"), encoding="utf-8"))
spec = json.load(open(os.path.join(PK, "spec", "PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json"), encoding="utf-8"))["spec"]
r52 = json.load(open(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.1\PREREGISTRO_FASE9_V2_R5_2_F31_LABELS_E1_20261008.json", encoding="utf-8"))["spec"]
out = {}
for rid, r in reg["leitores"].items():
    b = open(os.path.join(PK, *r["file"].split("/")), "rb").read()
    sh = hashlib.sha256(b).hexdigest()
    rule = {k: r[k] for k in ("kind", "regex", "H0_group", "sigma_rule")}
    if "page" in r: rule["page"] = r["page"]
    e = EXT.extract_reader(rule, b)
    # quantas vezes a regra casa (o EXT exige 1)
    sp = spec["leitores"][rid]; s52 = r52["leitores"][rid]
    out[rid] = {"sha_ok": sh == r["sha256"] == sp["documentary_source"]["sha256"], "bytes_ok": len(b) == r["bytes"],
                "extraido": [e["H0"], round(e["sigma"], 12)], "spec_v2": [sp.get("H0"), sp.get("sigma")], "spec_r52": [s52.get("H0"), s52.get("sigma")],
                "igual_spec_v2_1e-9": abs(e["H0"] - sp["H0"]) < 1e-9 and abs(e["sigma"] - sp["sigma"]) < 1e-9,
                "r52_igual_v2": [s52.get("H0"), s52.get("sigma")] == [sp.get("H0"), sp.get("sigma")], "papel_v2": sp.get("papel") or sp.get("role"),
                "trecho": e["trecho"][:160]}
for rid, f in (("L1b", "fontes/L1b_riess2025_arxiv_2509.01667/abs_2509.01667.html"), ("L6", "fontes/L6_lvk_o4a_arxiv_2509.04348/abs_2509.04348v1.html")):
    t = open(os.path.join(PK, *f.split("/")), "rb").read().decode("utf-8", "replace")
    tit = re.search(r'<meta name="citation_title" content="([^"]+)"', t); aut = re.findall(r'<meta name="citation_author" content="([^"]+)"', t)
    aid = re.search(r'<meta name="citation_arxiv_id" content="([^"]+)"', t); dt = re.search(r'<meta name="citation_date" content="([^"]+)"', t)
    vv = re.findall(r"\[v(\d)\]", t)
    out["identidade_" + rid] = {"arxiv_id": aid.group(1) if aid else None, "titulo": tit.group(1) if tit else None, "n_autores": len(aut), "primeiros_autores": aut[:3],
                                "data": dt.group(1) if dt else None, "versoes_listadas": sorted(set(vv))}
print(json.dumps(out, ensure_ascii=False, indent=1))
json.dump(out, open("VERIFICACAO_EXTRACAO.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
