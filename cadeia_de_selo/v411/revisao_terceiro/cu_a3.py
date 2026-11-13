"""CU-A3: (i) linhas fora dos nos mudados/novos/removidos iguais (comentarios, brancos, nos de topo nao-nomeados); (ii) blobs grandes iguais; (iii) beta literal e numeros do teste nos nos novos/mudados."""
import ast, hashlib, os, re, json
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
OLD = os.path.join(V, "um_v411_candidato.py.bak_20261112_195053")
NEW = os.path.join(V, "um_v411_candidato.py")
def load(p): return open(p, "rb").read().decode("utf-8")
so, sn = load(OLD), load(NEW)
ot, nt = ast.parse(so), ast.parse(sn)
CH = {"_V411_AB","_V411_FE","_v411_fala_do_autor_tex","_v411_fala_do_autor_md","_V411_FALA_DO_AUTOR","_v411_fecho_blocos","_v411_rotulo_agregado","_v411_errata_e44_tex","_V411_FALAS_CITADAS","_V411_TEXTOS_DA_GERENCIA","_v411_citar_falas","_v411_quadro_tex","_v411_quadro_md","_v411_secao_tex","_v411_linha_md","_v411_estatuto_tex","_v411_guarda_frases","h0dn_bg1_v411","_V411_H0DN_CONTRACT","_V411_H0DN_TEXT","_V411_VERBATINS2","_V411_SPECS","_V411_TOPO","_v411_rodar_specs","main"}
def nm(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)): return n.name
    if isinstance(n, ast.Assign): return ",".join(x.id for tg in n.targets for x in ast.walk(tg) if isinstance(x, ast.Name))
    return None
def keep(src, tree):
    L = src.split("\n"); skip = set()
    for n in tree.body:
        if nm(n) in CH:
            # inclui decoradores/comentarios imediatamente nao; so' as linhas do no
            for i in range(n.lineno, n.end_lineno + 1): skip.add(i)
    return [(i+1, l) for i, l in enumerate(L) if (i+1) not in skip]
ko, kn = keep(so, ot), keep(sn, nt)
lo = [l for _, l in ko]; ln = [l for _, l in kn]
print("linhas fora dos nos: old", len(lo), "new", len(ln), "iguais:", lo == ln)
if lo != ln:
    import difflib
    d = list(difflib.unified_diff([x[:200] for x in lo], [x[:200] for x in ln], lineterm="", n=0))
    print(len(d)); print("\n".join(d[:40]))
# blobs: strings > 100KB
def bigs(tree):
    r = {}
    for n in tree.body:
        for x in ast.walk(n):
            if isinstance(x, ast.Constant) and isinstance(x.value, (str, bytes)) and len(x.value) > 100000:
                v = x.value if isinstance(x.value, bytes) else x.value.encode()
                r.setdefault(nm(n) or "?", []).append((len(v), hashlib.sha256(v).hexdigest()[:16]))
    return r
bo, bn = bigs(ot), bigs(nt)
print("blobs old", {k: len(v) for k, v in bo.items()})
print("blobs new", {k: len(v) for k, v in bn.items()})
print("blobs iguais:", bo == bn, "total bytes", sum(a for v in bn.values() for a, _ in v))
# blobs medios (> 5000) nos nos mudados/novos
def meds(tree, only):
    r = []
    for n in tree.body:
        if nm(n) in only:
            for x in ast.walk(n):
                if isinstance(x, ast.Constant) and isinstance(x.value, str) and len(x.value) > 3000:
                    r.append((nm(n), len(x.value), hashlib.sha256(x.value.encode()).hexdigest()[:12]))
    return r
print("strings > 3000 chars nos nos CH, old:", meds(ot, CH)); print("new:", meds(nt, CH))
# beta literal e numeros do teste
pat = re.compile(r"0[.,]0120313|0\.01203|1203130040|0[.,]012031")
nums_novos = []
for n in nt.body:
    if nm(n) in CH:
        seg = ast.get_source_segment(sn, n) or ""
        for m in pat.finditer(seg): nums_novos.append((nm(n), m.group(0)))
print("beta literal nos nos CH:", nums_novos)
json.dump({"fora_dos_nos_iguais": lo == ln, "blobs_iguais": bo == bn}, open(r"C:\t\k411c\revisao_CU\a3.json","w"))
