# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R1): (1) sha16 do candidato lido do arquivo contra CANDIDATO_v407.json; (2) AST e fonte das funcoes intocadas contra a base v406;
(3) o que mudou no nivel superior (nos nomeados e nao nomeados); (4) diff de fonte das duas funcoes que mudaram. So le; nada executa o candidato."""
import ast, difflib, hashlib, json, sys, time
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
BASE = R + "base_v406/um.py"
CAND = R + "um_v407_candidato.py"
NOMES = ["evaluate_quantum_gravity_closure", "prove_qg_closure_gate", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386", "prove_ga_mass_audit", "prove_joint_coincidence_result_v3", "GA_WINDOW_STATUS"]


def carrega(p):
    b = open(p, "rb").read(); s = b.decode("utf-8"); t = time.time(); tr = ast.parse(s); return b, s, tr, time.time() - t


def acha(tr, nome):
    out = []
    for n in ast.walk(tr):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == nome: out.append(n)
        elif isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == nome for t in n.targets): out.append(n)
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and n.target.id == nome: out.append(n)
    return out


bb, bs, bt, tb = carrega(BASE); cb, cs, ct, tc = carrega(CAND)
cj = json.load(open(R + "CANDIDATO_v407.json", encoding="utf-8"))
print("base sha16", hashlib.sha256(bb).hexdigest()[:16], len(bb)); print("cand sha16", hashlib.sha256(cb).hexdigest()[:16], len(cb), "json:", cj["sha16"], cj.get("bytes"), "base_json:", cj.get("base_v406_sha16"))
bl = bs.split("\n"); cl = cs.split("\n")
res = {}
for n in NOMES:
    a = acha(bt, n); b = acha(ct, n)
    r = {"n_base": len(a), "n_cand": len(b)}
    if len(a) == len(b):
        r["ast_igual"] = all(ast.dump(x) == ast.dump(y) for x, y in zip(a, b))
        r["fonte_igual"] = all("\n".join(bl[x.lineno - 1:x.end_lineno]) == "\n".join(cl[y.lineno - 1:y.end_lineno]) for x, y in zip(a, b))
        r["linhas_base"] = [(x.lineno, x.end_lineno) for x in a]; r["linhas_cand"] = [(y.lineno, y.end_lineno) for y in b]
    res[n] = r; print(n, r)


def top(tr):
    d = {}
    for n in tr.body:
        nm = None
        if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)): nm = n.name
        elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): nm = n.targets[0].id
        if nm: d.setdefault(nm, []).append(hashlib.sha256(ast.dump(n).encode()).hexdigest()[:16])
    return d


tb_ = top(bt); tc_ = top(ct)
mud = sorted(k for k in tb_ if k in tc_ and tb_[k] != tc_[k]); rem = sorted(k for k in tb_ if k not in tc_); nov = sorted(k for k in tc_ if k not in tb_)
print("mudados", len(mud)); print(mud); print("removidos", rem); print("novos", len(nov)); print(nov)


def sig(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)): k = ("def", n.name)
    elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): k = ("asg", n.targets[0].id)
    else: k = (type(n).__name__, "")
    return k, hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]


cb_ = Counter(sig(n) for n in bt.body); cc_ = Counter(sig(n) for n in ct.body)
so_base = cb_ - cc_; so_cand = cc_ - cb_
nomes_b = sorted({k[0] for k in so_base}); nomes_c = sorted({k[0] for k in so_cand})
print("corpo: nos so na base:", sum(so_base.values()), "so no cand:", sum(so_cand.values()))
print("so base nao-nomeados:", [x for x in nomes_b if x[0] not in ("def", "asg")])
print("so cand nao-nomeados:", [x for x in nomes_c if x[0] not in ("def", "asg")])
print("so base nomeados:", [x for x in nomes_b if x[0] in ("def", "asg") and x not in nomes_c])


def fn(tr, lines, nome):
    for n in tr.body:
        if isinstance(n, ast.FunctionDef) and n.name == nome:
            return "\n".join(lines[n.lineno - 1:n.end_lineno])
    return None


for nome in ["testemunha_estatica_v396", "v406_fechamento_mechanics"]:
    a = fn(bt, bl, nome); b = fn(ct, cl, nome)
    print("=" * 30, nome, len(a) if a else None, len(b) if b else None)
    if a is None:
        # pode ser aninhada
        for nn in ast.walk(bt):
            if isinstance(nn, ast.FunctionDef) and nn.name == nome: a = "\n".join(bl[nn.lineno - 1:nn.end_lineno])
        for nn in ast.walk(ct):
            if isinstance(nn, ast.FunctionDef) and nn.name == nome: b = "\n".join(cl[nn.lineno - 1:nn.end_lineno])
        print("(aninhada)", len(a) if a else None, len(b) if b else None)
    for l in difflib.unified_diff(a.split("\n"), b.split("\n"), "base", "cand", lineterm="", n=0):
        print(l[:2500])
json.dump({"res": res, "mudados": mud, "removidos": rem, "novos": nov, "cand_sha16_lido": hashlib.sha256(cb).hexdigest()[:16]}, open(R + "revisao_terceiro/a_intocados_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
