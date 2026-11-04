# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R1): o kernel do bundle. 9 embutidos == sandbox C:/t/k407c/final == pedra/ == BUNDLE_v407.json (sha256);
pedra/<Nome>.lean vs pedra/origem/<Candidata>.lean (diff: so' cabecalho/nome/namespace e #print axioms finais); raiz = raiz v406 + 9 imports; Audit identico; as 1746 herdadas == base v406. So le."""
import ast, difflib, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
SB = "C:/t/k407c/final/"
sha = lambda b: hashlib.sha256(b).hexdigest()


def embutidos(p):
    s = open(p, "rb").read().decode("utf-8"); tr = ast.parse(s)
    for n in tr.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_EMBEDDED_KERNEL_FILES":
            return ast.literal_eval(n.value)


E6 = embutidos(R + "base_v406/um.py"); E7 = embutidos(R + "um_v407_candidato.py")
print("embutidos v406:", len(E6), " v407:", len(E7))
BJ = json.load(open(R + "BUNDLE_v407.json", encoding="utf-8")); LJ = json.load(open(R + "kernel_modulos_novos_v407.json", encoding="utf-8"))
mods = {b["rel"]: b for b in BJ["modulos"]}
print("bundle n:", BJ["n"], len(mods), "lista novos:", LJ["n"], "ordem igual:", [b["rel"] for b in BJ["modulos"]] == LJ["novos"])
res = {"modulos": {}}
ok = 0; falhas = []
for rel, b in mods.items():
    nome = os.path.basename(rel)
    body = E7.get(rel)
    sbp = SB + rel; pp = R + "pedra/" + nome
    sb = open(sbp, "rb").read() if os.path.exists(sbp) else None
    pd = open(pp, "rb").read() if os.path.exists(pp) else None
    e = body.encode("utf-8") if isinstance(body, str) else None
    cond = e is not None and sb is not None and pd is not None and sha(e) == sha(sb) == sha(pd) == b["sha256"] and len(e) == b["bytes"]
    res["modulos"][rel] = {"embutido": sha(e)[:12] if e else None, "sandbox": sha(sb)[:12] if sb else None, "pedra": sha(pd)[:12] if pd else None, "bundle": b["sha256"][:12], "ok": cond}
    if cond: ok += 1
    else: falhas.append(rel)
print("9: embutido == sandbox == pedra == BUNDLE:", ok, "falhas:", falhas)
# arquivos novos no embutido
novas = sorted(set(E7) - set(E6)); sumidas = sorted(set(E6) - set(E7))
print("novas:", novas == sorted(mods), len(novas), "sumidas:", sumidas)
dif = [k for k in E6 if k in E7 and E6[k] != E7[k]]
print("herdadas que mudaram:", dif)
r6 = E6["TGLExt.lean"]; r7 = E7["TGLExt.lean"]; suf = BJ["root_suffix"]
print("raiz v407 == raiz v406 + 9 imports:", r7 == r6 + suf, "| prefixo:", r7.startswith(r6), "| sufixo:", repr(r7[len(r6):]))
aud = [k for k in E7 if "udit" in k]
print("audit chaves:", aud, [E6.get(k) == E7.get(k) for k in aud])
for nome in ("TGLExt.lean", "TGL/Audit.lean"):
    p = SB + nome
    if os.path.exists(p):
        b = open(p, "rb").read(); print("sandbox", nome, sha(b)[:16], "== embutido?", (E7.get(nome) or "").encode("utf-8") == b)
n_eq = 0; n_dif = []
for k, v in E7.items():
    p = SB + k
    if os.path.exists(p) and open(p, "rb").read() == v.encode("utf-8"): n_eq += 1
    else: n_dif.append(k)
print("embutidos == sandbox:", n_eq, "de", len(E7), "dif/ausentes:", n_dif[:5])
# tokens suspeitos nos 9
pro = re.compile(r"\bsorry\b|^\s*axiom\b|\bnative_decide\b|\bunsafe\b|#eval|\bofReduceBool\b|\bimplemented_by\b|\bextern\b|@\[csimp\]|\bopaque\b", re.M)
achados = {}
for rel in mods:
    ms = [m.group(0).strip() for m in pro.finditer(E7[rel])]
    if ms: achados[rel] = sorted(set(ms))
print("tokens suspeitos nos 9:", achados)
# diff pedra x origem
ORIG = {os.path.basename(b["origem"]): b for b in BJ["modulos"]}
print("\n=== pedra/<Nome>.lean vs origem (diff de linhas) ===")
for rel, b in mods.items():
    nome = os.path.basename(rel); on = os.path.basename(b["origem"])
    po = R + "pedra/origem/" + on
    if not os.path.exists(po): print("ORIGEM AUSENTE:", on); continue
    ob = open(po, "rb").read(); okh = sha(ob) == b["sha256_origem"]
    a = ob.decode("utf-8").split("\n"); c = E7[rel].split("\n")
    d = [l for l in difflib.unified_diff(a, c, "origem", "norm", lineterm="", n=0)]
    nlin = [l for l in d if (l.startswith("+") or l.startswith("-")) and not l.startswith("+++") and not l.startswith("---")]
    print("---", nome, "origem sha ok:", okh, "| linhas diferentes:", len(nlin), "| linhas origem/norm:", len(a), len(c))
    for l in nlin[:60]: print("    ", l[:220])
    res["modulos"][rel]["diff_n"] = len(nlin); res["modulos"][rel]["origem_sha_ok"] = okh
res["ok"] = ok; res["falhas"] = falhas
json.dump(res, open(R + "revisao_terceiro/r3_d_kernel_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
