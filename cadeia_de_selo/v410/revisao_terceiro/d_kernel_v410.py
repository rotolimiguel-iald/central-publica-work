# -*- coding: utf-8 -*-
"""Revisor terceiro v409 (R1): o kernel do bundle. 2 embutidos == sandbox C:/t/k409c/final == pedra/ == BUNDLE_v410.json (sha256);
pedra/<Nome>.lean vs pedra/origem/<Candidata>.lean (diff: so' cabecalho/nome/namespace e #print axioms finais); raiz = raiz v408 + 2 imports; Audit identico; as 1746 herdadas == base v408. So le."""
import ast, difflib, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
SB = "C:/t/k410c/final/"
sha = lambda b: hashlib.sha256(b).hexdigest()


def embutidos(p):
    s = open(p, "rb").read().decode("utf-8"); tr = ast.parse(s)
    for n in tr.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_EMBEDDED_KERNEL_FILES":
            return ast.literal_eval(n.value)


Eb = embutidos(R + "base_v409/um.py"); Ec = embutidos(R + "um_v410_candidato.py")
print("embutidos v408:", len(Eb), " v409:", len(Ec))
BJ = json.load(open(R + "BUNDLE_v410.json", encoding="utf-8")); LJ = json.load(open(R + "kernel_modulos_novos_v410.json", encoding="utf-8"))
mods = {b["rel"]: b for b in BJ["modulos"]}
print("bundle n:", BJ["n"], len(mods), "lista novos:", LJ["n"], "ordem igual:", [b["rel"] for b in BJ["modulos"]] == LJ["novos"])
res = {"modulos": {}}
ok = 0; falhas = []
for rel, b in mods.items():
    nome = os.path.basename(rel)
    body = Ec.get(rel)
    sbp = SB + rel; pp = R + "pedra/" + nome
    sb = open(sbp, "rb").read() if os.path.exists(sbp) else None
    pd = open(pp, "rb").read() if os.path.exists(pp) else None
    e = body.encode("utf-8") if isinstance(body, str) else None
    cond = e is not None and sb is not None and pd is not None and sha(e) == sha(sb) == sha(pd) == b["sha256"] and len(e) == b["bytes"]
    res["modulos"][rel] = {"embutido": sha(e)[:12] if e else None, "sandbox": sha(sb)[:12] if sb else None, "pedra": sha(pd)[:12] if pd else None, "bundle": b["sha256"][:12], "ok": cond}
    if cond: ok += 1
    else: falhas.append(rel)
print("2 modulos: embutido == sandbox == pedra == BUNDLE:", ok, "falhas:", falhas)
# arquivos novos no embutido
novas = sorted(set(Ec) - set(Eb)); sumidas = sorted(set(Eb) - set(Ec))
print("novas:", novas == sorted(mods), len(novas), "sumidas:", sumidas)
dif = [k for k in Eb if k in Ec and Eb[k] != Ec[k]]
print("herdadas que mudaram:", dif)
r6 = Eb["TGLExt.lean"]; r7 = Ec["TGLExt.lean"]; suf = BJ["root_suffix"]
print("raiz v409 == raiz v408 + 2 imports:", r7 == r6 + suf, "| prefixo:", r7.startswith(r6), "| sufixo:", repr(r7[len(r6):]))
aud = [k for k in Ec if "udit" in k]
print("audit chaves:", aud, [Eb.get(k) == Ec.get(k) for k in aud])
for nome in ("TGLExt.lean", "TGL/Audit.lean"):
    p = SB + nome
    if os.path.exists(p):
        b = open(p, "rb").read(); print("sandbox", nome, sha(b)[:16], "== embutido?", (Ec.get(nome) or "").encode("utf-8") == b)
n_eq = 0; n_dif = []
for k, v in Ec.items():
    p = SB + k
    if os.path.exists(p) and open(p, "rb").read() == v.encode("utf-8"): n_eq += 1
    else: n_dif.append(k)
print("embutidos == sandbox:", n_eq, "de", len(Ec), "dif/ausentes:", n_dif[:5])
# tokens suspeitos nos 2
pro = re.compile(r"\bsorry\b|^\s*axiom\b|\bnative_decide\b|\bunsafe\b|#eval|\bofReduceBool\b|\bimplemented_by\b|\bextern\b|@\[csimp\]|\bopaque\b", re.M)
achados = {}
for rel in mods:
    ms = [m.group(0).strip() for m in pro.finditer(Ec[rel])]
    if ms: achados[rel] = sorted(set(ms))
print("tokens suspeitos nos 2:", achados)
for rel in mods:
    for i, l in enumerate(Ec[rel].split("\n")):
        if re.search(r"\bsorry\b|^\s*axiom\b|native_decide|\bunsafe\b|#eval|ofReduceBool|implemented_by|\bextern\b|@\[csimp\]|\bopaque\b", l): print("   ", rel, i + 1, l.strip()[:160])
# diff pedra x origem
ORIG = {os.path.basename(b["origem"]): b for b in BJ["modulos"]}
print("\n=== pedra/<Nome>.lean vs origem (diff de linhas) ===")
for rel, b in mods.items():
    nome = os.path.basename(rel); on = os.path.basename(b["origem"])
    po = R + "pedra/origem/" + on
    if not os.path.exists(po): print("ORIGEM AUSENTE:", on); continue
    ob = open(po, "rb").read(); okh = sha(ob) == b["sha256_origem"]
    a = ob.decode("utf-8").replace("\r\n", "\n").split("\n"); c = Ec[rel].split("\n")
    d = [l for l in difflib.unified_diff(a, c, "origem", "norm", lineterm="", n=0)]
    nlin = [l for l in d if (l.startswith("+") or l.startswith("-")) and not l.startswith("+++") and not l.startswith("---")]
    print("---", nome, "origem sha ok:", okh, "| linhas diferentes:", len(nlin), "| linhas origem/norm:", len(a), len(c))
    for l in nlin[:60]: print("    ", l[:220])
    res["modulos"][rel]["diff_n"] = len(nlin); res["modulos"][rel]["origem_sha_ok"] = okh
res["ok"] = ok; res["falhas"] = falhas
json.dump(res, open(R + "revisao_terceiro/d_kernel_v410_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
