# -*- coding: utf-8 -*-
"""Revisor terceiro v406: toda citacao entre « » nos textos publicos NOVOS da v406 e' substring exata de uma das 23 falas do operador (insumos/cunhagens)?
Fontes: artigo PT (pysnip), linha .md (candidato), _V406_FECHO_TEXT e _V406_SPECS (candidato, por AST), textos_v406.py (pos_rito), delta/registros (strings), v406 section renderizada."""
import ast, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v406/"
falas = {}
for p in sorted(glob.glob(R + "insumos/cunhagens/*_verbatim.txt")):
    b = open(p, "rb").read(); falas[os.path.basename(p)] = b.decode("utf-8")
print("falas:", len(falas))
corpus = {k: re.sub(r"\s+", " ", v) for k, v in falas.items()}
# o verbatim tambem em C:/IALD/Central de Patentes/work/cunhagens_13out (origem): conferir sha256 de cada copia contra a origem
orig_dir = "C:/IALD/Central de Patentes/work/cunhagens_13out/"
dif = []
for k, v in falas.items():
    nome_orig = k.split("_", 1)[1]
    po = orig_dir + nome_orig
    if os.path.exists(po):
        if open(po, "rb").read() != open(R + "insumos/cunhagens/" + k, "rb").read(): dif.append(k)
    else: dif.append(k + " (origem ausente)")
print("copias != origem:", dif)
# o prefixo do nome = sha16 dos bytes?
bad = [k for k in falas if not k.startswith(hashlib.sha256(open(R + "insumos/cunhagens/" + k, "rb").read()).hexdigest()[:16] + "_")]
print("nome != sha16 dos bytes:", bad)
q_rx = re.compile(r"«([^»]+)»")
def norm(s): return re.sub(r"\s+", " ", s).strip()
def checa(rotulo, texto):
    out = []
    for m in q_rx.finditer(texto):
        q = norm(m.group(1)); alvo = q.rstrip(".,;:")
        achou = [k for k, c in corpus.items() if q in c or alvo in c]
        out.append((q, bool(achou), achou[0][:16] if achou else None))
    return out
fontes = {}
fontes["artigo_pt_v406.pysnip"] = open(R + "artigo_pt_v406.pysnip", encoding="utf-8").read()
cs = open(R + "um_v406_candidato.py", "rb").read().decode("utf-8"); L = cs.split("\n")
fontes["md_line"] = next(l for l in L if l.lstrip().startswith("md.append(\"> **O fechamento (v406"))
tr = ast.parse(cs)
for n in tr.body:
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("_V406_FECHO_TEXT", "_V406_SPECS", "_V406_FECHO_CONTRACT"):
        try:
            v = ast.literal_eval(n.value); fontes[n.targets[0].id] = json.dumps(v, ensure_ascii=False)
        except Exception as e:
            fontes[n.targets[0].id] = "\n".join(L[n.lineno - 1:n.end_lineno]); print("nao literal:", n.targets[0].id, e)
fontes["textos_v406.py"] = open(R + "pos_rito/textos_v406.py", encoding="utf-8").read()
fontes["registros_v406.py"] = open(R + "registros_v406.py", encoding="utf-8").read()
fontes["delta_v406.py"] = open(R + "delta_v406.py", encoding="utf-8").read()
fontes["runtime_v406.py"] = open(R + "runtime_v406.py", encoding="utf-8").read()
fontes["dry_pt_secao_v406"] = "\n".join(open(R + "dry_v406/dry_v406_pt.txt", encoding="utf-8").read().split("\n")[104:120])
res = {}
for k, t in fontes.items():
    r = checa(k, t); nao = [x for x in r if not x[1]]
    res[k] = {"n": len(r), "nao_substring": [x[0][:150] for x in nao]}
    print("==", k, "citacoes:", len(r), " nao-substring:", len(nao))
    for x in nao[:25]: print("    ?", repr(x[0][:160]))
json.dump(res, open(R + "revisao_terceiro/e_citacoes_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
