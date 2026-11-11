# -*- coding: utf-8 -*-
"""Revisor terceiro v410 (R1): (1) sha16 da base e do candidato LIDOS dos arquivos; (2) AST e fonte (byte a byte, por linhas) das funcoes/constantes
que nao podem mudar contra a base v409 (DL.FUNCOES_INTOCADAS herdada + as que o pedido nomeia); (3) o diff de nivel superior (nos nomeados e anonimos)
CONTRA a lista de mudados/novos declarada em COMPARACAO_V409_v410.json; (4) diff por linhas do arquivo inteiro: toda linha mudada cai dentro de um no declarado.
So le; nada executa o candidato."""
import ast, difflib, hashlib, json, sys, time
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
BASE = R + "base_v409/um.py"
CAND = R + "um_v410_candidato.py"
NOMES = ["evaluate_quantum_gravity_closure", "prove_qg_closure_gate", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386",
         "prove_ga_mass_audit", "prove_joint_coincidence_result_v3", "GA_WINDOW_STATUS",
         # registros da v409 e anteriores (devem ficar identicos)
         "traducao_turing_v409", "v409_traducao_mechanics", "_v409_formal", "_v409_guarda_frases", "_v409_rodar_specs", "_v409_sat", "_V409_TRADUCAO_TEXT", "_V409_FONTES", "_V409_VERBATINS2", "_V409_RECUSA", "_V409_NOMES_REGISTROS", "_V409_REGISTROS_FUNCAO",
         "tetelestai_terminal_v408", "v408_terminal_mechanics", "_v408_formal", "_v408_guarda_frases", "_v408_rodar_specs", "_V408_TERMINAL_TEXT", "_V408_FONTES", "_V408_VERBATINS2", "_V408_RECUSA", "_V408_KB_SI_J_PER_K",
         "testemunha_estatica_v396", "v406_fechamento_mechanics", "fechamento_v406", "psibit_v395", "rede_fock_v394", "psion_canto_v407", "v407_psion_mechanics",
         "_v407_elo_lido", "_v407_formal", "_v407_chaves", "_v407_rodar_specs", "_v407_guarda_frases", "_v406_certificado_habitado", "_v406_chaves", "_v406_formal",
         "verify_tgl_kernel_formalization", "run_um", "_V406_FECHO_TEXT", "_V407_PSION_TEXT", "_V407_VERBATINS2"]


def carrega(p):
    b = open(p, "rb").read(); s = b.decode("utf-8"); t = time.time(); tr = ast.parse(s); return b, s, tr, time.time() - t


def acha(tr, nome):
    out = []
    for n in ast.walk(tr):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == nome: out.append(n)
        elif isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == nome for t in n.targets): out.append(n)
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and n.target.id == nome: out.append(n)
    return out


bb, bs, bt, tb = carrega(BASE); cb, cs, ct, tc = carrega(CAND)
cj = json.load(open(R + "CANDIDATO_v410.json", encoding="utf-8")); cmpj = json.load(open(R + "COMPARACAO_V409_v410.json", encoding="utf-8"))
print("base sha16", hashlib.sha256(bb).hexdigest()[:16], len(bb), "| cand sha16", hashlib.sha256(cb).hexdigest()[:16], len(cb), "| json:", cj["sha16"], cj["bytes"], "base_json:", cj.get("base_v409_sha16"))
bl = bs.split("\n"); cl = cs.split("\n")
res = {"nomes": {}}
for n in NOMES:
    a = acha(bt, n); b = acha(ct, n)
    r = {"n_base": len(a), "n_cand": len(b)}
    if len(a) == len(b):
        r["ast_igual"] = all(ast.dump(x) == ast.dump(y) for x, y in zip(a, b))
        r["fonte_igual"] = all("\n".join(bl[x.lineno - 1:x.end_lineno]) == "\n".join(cl[y.lineno - 1:y.end_lineno]) for x, y in zip(a, b))
    res["nomes"][n] = r; print("%-40s" % n, r)


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
dec_mud = sorted(cmpj["mudados"].keys()); dec_nov = sorted(cmpj["novos"])
print("MUDADOS == declarados (26):", mud == dec_mud, "| so meus:", sorted(set(mud) - set(dec_mud)), "| so declarados:", sorted(set(dec_mud) - set(mud)))
print("NOVOS == declarados (38):", nov == dec_nov, "| so meus:", sorted(set(nov) - set(dec_nov)), "| so declarados:", sorted(set(dec_nov) - set(nov)))


def sig(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)): k = ("def", n.name)
    elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): k = ("asg", n.targets[0].id)
    else: k = (type(n).__name__, "")
    return k, hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]


cb_ = Counter(sig(n) for n in bt.body); cc_ = Counter(sig(n) for n in ct.body)
so_base = cb_ - cc_; so_cand = cc_ - cb_
print("corpo: nos so na base:", sum(so_base.values()), "so no cand:", sum(so_cand.values()))
anon_b = [x for x in sorted({k[0] for k in so_base}) if x[0] not in ("def", "asg")]; anon_c = [x for x in sorted({k[0] for k in so_cand}) if x[0] not in ("def", "asg")]
print("anonimos so na base:", anon_b, "| anonimos so no cand:", anon_c)
for n in ct.body:
    k, h = sig(n)
    if k[0] not in ("def", "asg") and (k, h) in so_cand:
        print("   anon novo no cand L%d-%d: %s" % (n.lineno, n.end_lineno, "\n".join(cl[n.lineno - 1:n.end_lineno])[:200]))
decl = set(mud) | set(nov)
iv = []
for n in ct.body:
    nm = None
    if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)): nm = n.name
    elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): nm = n.targets[0].id
    if nm in decl or (nm is None and sig(n) in so_cand): iv.append((n.lineno, n.end_lineno, nm))
iv.sort()
sm = difflib.SequenceMatcher(None, bl, cl, autojunk=False)
fora = []
n_alt = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal": continue
    n_alt += 1
    ok = False
    if j2 == j1:
        ok = any(a <= j1 + 1 <= b or a <= j1 <= b for a, b, _ in iv)
    else:
        ok = all(any(a <= j + 1 <= b for a, b, _ in iv) for j in range(j1, j2))
    if not ok: fora.append((tag, i1 + 1, i2, j1 + 1, j2, "\n".join(cl[j1:min(j2, j1 + 2)])[:200], "\n".join(bl[i1:min(i2, i1 + 2)])[:200]))
print("blocos de diferenca por linhas:", n_alt, "| blocos FORA dos nos declarados:", len(fora))
for f in fora[:15]: print("   FORA", f)
res.update({"mudados": mud, "removidos": rem, "novos": nov, "mud_igual_declarado": mud == dec_mud, "nov_igual_declarado": nov == dec_nov, "anon_base": [list(x) for x in anon_b], "anon_cand": [list(x) for x in anon_c],
            "blocos_diff": n_alt, "blocos_fora": len(fora), "fora": [list(map(str, f)) for f in fora[:15]], "cand_sha16_lido": hashlib.sha256(cb).hexdigest()[:16], "base_sha16_lido": hashlib.sha256(bb).hexdigest()[:16]})
json.dump(res, open(R + "revisao_terceiro/a_intocados_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
