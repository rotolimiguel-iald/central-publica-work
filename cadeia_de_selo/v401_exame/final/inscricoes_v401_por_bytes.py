# -*- coding: utf-8 -*-
"""inscricoes_v401_por_bytes.py -- exame final v401: as 6 inscricoes de 25/10 embutidas no candidato (_V401_VERBATINS2: text e sha256) == bytes dos arquivos em
work\\cunhagens_13out (e das copias em v401\\insumos\\cunhagens); a 6a (e26364c5) e' o RECORTE e e' dita como recorte no proprio dict/texto; nenhum verbatim da gerencia."""
import ast, hashlib, json, os, glob
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v401"; CU = r"C:\IALD\Central de Patentes\work\cunhagens_13out"
src = open(os.path.join(V, "um_v401_candidato.py"), encoding="utf-8").read()
T = ast.parse(src)
lit = lambda name: next(ast.literal_eval(n.value) for n in T.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == name)
VB = lit("_V401_VERBATINS2"); FO = lit("_V401_FONTES")
R = {"n_verbatins": len(VB), "itens": {}, "fontes": {}}
for k, v in VB.items():
    arq = v.get("arquivo"); orig = v.get("arquivo_original") or v.get("origem") or ""
    t = v.get("text", ""); h = hashlib.sha256(t.encode("utf-8")).hexdigest()
    cand = [p for p in glob.glob(os.path.join(CU, "OPERADOR_25out_*_verbatim.txt")) if hashlib.sha256(open(p, "rb").read()).hexdigest() == h]
    R["itens"][k] = {"arquivo_declarado": os.path.basename(str(arq)), "sha256_declarado16": str(v.get("sha256"))[:16], "sha256_do_texto16": h[:16], "igual_ao_declarado": str(v.get("sha256")) == h,
                     "arquivo_em_cunhagens_13out_com_esses_bytes": [os.path.basename(p) for p in cand], "copia_em_insumos_igual": (os.path.exists(str(arq)) and hashlib.sha256(open(str(arq), "rb").read()).hexdigest() == h) if arq else None,
                     "operador_no_nome": "OPERADOR_" in os.path.basename(str(arq)), "recorte": "RECORTE" in os.path.basename(str(arq)), "chaves": sorted(v.keys()), "estatuto": v.get("estatuto"), "nota": str(v.get("nota") or v.get("recorte") or "")[:200]}
for k, v in FO.items():
    p = v.get("arquivo"); ok = os.path.exists(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() == v.get("sha256")
    R["fontes"][k] = {"arquivo": os.path.basename(p), "sha_confere": ok, "sha16": str(v.get("sha256"))[:16]}
R["todas_iguais_aos_arquivos"] = all(x["igual_ao_declarado"] and x["arquivo_em_cunhagens_13out_com_esses_bytes"] and x["operador_no_nome"] for x in R["itens"].values())
R["recortes"] = [k for k, x in R["itens"].items() if x["recorte"]]
json.dump(R, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "INSCRICOES_v401_POR_BYTES.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1)[:5000])
