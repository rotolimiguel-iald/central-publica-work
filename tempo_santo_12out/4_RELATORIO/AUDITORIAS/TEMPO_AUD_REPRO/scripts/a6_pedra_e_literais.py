"""A6 — (i) toda declaracao da pedra tem #print axioms? (ii) V-GERAL-2: cada re-exportacao tem o par de
`example : type_of% ...`; (iii) tokens proibidos na fonte (sorry/admit/axiom/native_decide/...) fora de
comentarios; (iv) literais da constante da casa (beta/alpha e afins) em TODO codigo dos construtores
(2_OPTICO, 3_KERNEL) e na pedra; o caractere β na pedra. So leitura. Saida: JSON."""
import glob
import json
import os
import re
import sys

STONE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\3_KERNEL\sandbox\TheTimeHasNoRank.lean"
BASE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
out = {}
src = open(STONE, encoding="utf-8").read()


def strip_comments(s):
    # remove /- ... -/ (aninhado simples) e -- ... ate o fim da linha
    res, i, depth = [], 0, 0
    while i < len(s):
        if s.startswith("/-", i):
            depth += 1
            i += 2
            continue
        if depth and s.startswith("-/", i):
            depth -= 1
            i += 2
            continue
        if depth:
            i += 1
            continue
        if s.startswith("--", i):
            j = s.find("\n", i)
            i = len(s) if j < 0 else j
            continue
        res.append(s[i])
        i += 1
    return "".join(res)


code = strip_comments(src)
decls = re.findall(r"^(?:noncomputable\s+)?(?:theorem|lemma|def|abbrev|instance|structure)\s+([A-Za-z_][A-Za-z0-9_'.]*)", code, re.M)
printed = re.findall(r"^#print axioms TGLExt\.TheTimeHasNoRank\.([A-Za-z0-9_'.]+)", src, re.M)
out["declaracoes"] = len(decls)
out["print_axioms"] = len(printed)
out["sem_print"] = sorted(set(decls) - set(printed))
out["print_sem_decl"] = sorted(set(printed) - set(decls))
out["examples"] = len(re.findall(r"^example\b", code, re.M))
# re-exportacoes: pares type_of%
pairs = re.findall(r"^example : type_of% @([A-Za-z0-9_.']+) := @([A-Za-z0-9_.']+)", code, re.M)
out["type_of_pares"] = len(pairs)
fwd = {(a, b) for a, b in pairs}
reexp = []
for a, b in pairs:
    if "." in a and "." not in b:   # original -> novo
        reexp.append({"original": a, "novo": b, "volta": (b, a) in fwd or any(x == b and y == a for x, y in fwd)})
out["reexportacoes"] = reexp
out["reexportacoes_sem_volta"] = [r for r in reexp if not r["volta"]]
docs_reexp = re.findall(r"re-exportação\*?\*? de `([^`]+)`|re-citação; tipo original de `([^`]+)`", src)
out["docstrings_que_dizem_reexportacao"] = [a or b for a, b in docs_reexp]
# tokens proibidos fora de comentarios
proib = {}
for tok in ("sorry", "admit", "axiom ", "native_decide", "implemented_by", "unsafe", "opaque", "@[extern", "decide :=",
            "Classical.ofNonempty", "sorryAx", "set_option debug", "maxRecDepth"):
    n = code.count(tok)
    if n:
        proib[tok] = n
out["tokens_suspeitos_fora_de_comentario"] = proib
out["decide_ocorrencias"] = len(re.findall(r"\bdecide\b", code))
out["beta_char_na_pedra"] = src.count("β")
out["alpha_char_na_pedra"] = src.count("α")
# literais numericos da constante em todo codigo dos construtores + pedra
PAT = re.compile(r"0\.0120|0\.01203|1203130|7\.297|0\.0072973|137\.03|0\.9759|4\.4081|1\.4253|0\.05303|0\.8993|0\.9496|1\.6487")
hits = []
files = [STONE] + glob.glob(os.path.join(BASE, "2_OPTICO", "**", "*.py"), recursive=True) + \
    glob.glob(os.path.join(BASE, "3_KERNEL", "**", "*.py"), recursive=True) + \
    glob.glob(os.path.join(BASE, "3_KERNEL", "**", "*.lean"), recursive=True)
for p in files:
    t = open(p, encoding="utf-8", errors="replace").read()
    for i, ln in enumerate(t.splitlines(), 1):
        for m in PAT.finditer(ln):
            hits.append({"arquivo": os.path.relpath(p, BASE), "linha": i, "texto": ln.strip()[:160]})
out["arquivos_varridos"] = len(files)
out["literais_suspeitos"] = hits
tmp = sys.argv[1] + ".tmp"
with open(tmp, "w", encoding="utf-8") as fo:
    json.dump(out, fo, indent=1, ensure_ascii=False)
os.replace(tmp, sys.argv[1])
print(json.dumps({k: v for k, v in out.items() if k not in ("reexportacoes",)}, ensure_ascii=False, indent=1)[:6000])
print("reexportacoes:", len(reexp))
