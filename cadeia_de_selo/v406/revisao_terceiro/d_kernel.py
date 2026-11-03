# -*- coding: utf-8 -*-
"""Revisor terceiro v406: o kernel do bundle. embutidos (301) == sandbox C:/t/k406c/final == BUNDLE_v406.json (sha256); raiz = raiz v405 + 2 imports; Audit identico;
as 1745 fontes herdadas == base v405 embutida; nada novo alem dos 301 + raiz. So le."""
import hashlib, importlib.util, json, os, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v406/"
SB = "C:/t/k406c/final/"
def load(p, nome):
    spec = importlib.util.spec_from_file_location(nome, p); m = importlib.util.module_from_spec(spec); sys.modules[nome] = m; spec.loader.exec_module(m); return m
# base v405: so' o dict de fontes embutidas, por AST (nao importar a base)
import ast
def embutidos(p):
    s = open(p, "rb").read().decode("utf-8"); tr = ast.parse(s)
    for n in tr.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_EMBEDDED_KERNEL_FILES":
            return ast.literal_eval(n.value)
E405 = embutidos(R + "base_v405/um.py"); E406 = embutidos(R + "um_v406_candidato.py")
print("embutidos v405:", len(E405), " v406:", len(E406))
BJ = json.load(open(R + "BUNDLE_v406.json", encoding="utf-8")); LJ = json.load(open(R + "kernel_modulos_novos_v406.json", encoding="utf-8"))
mods = {b["rel"]: b for b in BJ["modulos"]}
print("bundle n:", BJ["n"], len(mods), "lista novos:", LJ["n"])
sha = lambda b: hashlib.sha256(b).hexdigest()
ok301 = 0; falhas = []
for rel, b in mods.items():
    body = E406.get(rel)
    sb_path = SB + rel
    sb = open(sb_path, "rb").read() if os.path.exists(sb_path) else None
    e = body.encode("utf-8") if isinstance(body, str) else None
    cond = e is not None and sb is not None and sha(e) == sha(sb) == b["sha256"]
    if cond: ok301 += 1
    else: falhas.append((rel, None if e is None else sha(e)[:12], None if sb is None else sha(sb)[:12], b["sha256"][:12]))
print("301: embutido == sandbox == BUNDLE:", ok301, "falhas:", falhas[:5])
# glob do sandbox: ha' arquivos no sandbox F1Fecho394 que nao estao no bundle?
dd = SB + "TGLExt/F1Fecho394/"
no_sb = sorted(f for f in os.listdir(dd) if f.endswith(".lean")); rels_sb = {"TGLExt/F1Fecho394/" + f for f in no_sb}
print("arquivos .lean no sandbox F1Fecho394:", len(no_sb), "| no bundle:", len(set(mods)), "| so no sandbox:", sorted(rels_sb - set(mods))[:5], "| so no bundle:", sorted(set(mods) - rels_sb)[:5])
# chaves novas no E406 em relacao ao E405
novas = sorted(set(E406) - set(E405)); sumidas = sorted(set(E405) - set(E406))
print("novas em E406:", len(novas), "(todas no bundle?)", set(novas) == set(mods), "| sumidas:", sumidas)
diff_herdadas = [k for k in E405 if k in E406 and E405[k] != E406[k]]
print("herdadas que mudaram:", diff_herdadas)
# a raiz
r5 = E405["TGLExt.lean"]; r6 = E406["TGLExt.lean"]
suf = LJ["root_suffix"]
print("raiz v406 == raiz v405 + 2 imports:", r6 == r5 + suf or r6.replace("\r\n", "\n") == (r5 + suf).replace("\r\n", "\n"), "| prefixo igual:", r6.startswith(r5), "| sufixo:", repr(r6[len(r5):]))
# Audit: idêntico? (procurar o nome nas chaves)
aud = [k for k in E406 if "udit" in k]
print("audit chaves:", aud, [E405.get(k) == E406.get(k) for k in aud])
# o sandbox: raiz e Audit em disco
for nome in ("TGLExt.lean", "Audit.lean", "TGLExt/Audit.lean"):
    p = SB + nome
    if os.path.exists(p):
        b = open(p, "rb").read(); print("sandbox", nome, sha(b)[:16], "== embutido?", (E406.get(nome) or "").encode("utf-8") == b)
# tudo que e' do sandbox e' do embutido? (1746 arquivos)
n_eq = 0; n_dif = []
for k, v in E406.items():
    p = SB + k
    if os.path.exists(p) and open(p, "rb").read() == v.encode("utf-8"): n_eq += 1
    else: n_dif.append(k)
print("embutidos == sandbox:", n_eq, "de", len(E406), "dif/ausentes:", n_dif[:5])
# nenhum token proibido nos 301 (sorry, axiom, #eval, native_decide, unsafe)
import re
pro = re.compile(r"\bsorry\b|^\s*axiom\b|\bnative_decide\b|\bunsafe\b|#eval|\bofReduceBool\b|\bimplemented_by\b|\bextern\b|@\[csimp\]|\bopaque\b", re.M)
achados = {}
for rel in mods:
    body = E406[rel]; ms = [m.group(0).strip() for m in pro.finditer(body)]
    if ms: achados[rel] = sorted(set(ms))
print("tokens suspeitos nos 301:", len(achados));
for k, v in list(achados.items())[:15]: print("  ", k.split("/")[-1], v)
json.dump({"ok301": ok301, "falhas": falhas, "n_embutidos_v405": len(E405), "n_embutidos_v406": len(E406), "novas": len(novas), "tokens_suspeitos": achados}, open(R + "revisao_terceiro/d_kernel_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
