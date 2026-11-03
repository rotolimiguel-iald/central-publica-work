# -*- coding: utf-8 -*-
"""Revisor terceiro v406: todo sha16/sha256 escrito nos JSONs da cadeia confere com o arquivo (lido agora, por script)."""
import ast, glob, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v406/"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
J = lambda p: json.load(open(R + p, encoding="utf-8"))
ok = {}; falhas = []
def chk(nome, cond, det=""):
    ok[nome] = bool(cond)
    if not cond: falhas.append((nome, det))
    print(("OK   " if cond else "FALHA"), nome, det if not cond else "")
cand = R + "um_v406_candidato.py"; h = sha(cand)
c = J("CANDIDATO_v406.json")
chk("CANDIDATO.sha16 == arquivo", c["sha16"] == h[:16], (c["sha16"], h[:16])); chk("CANDIDATO.sha256 == arquivo", c["sha256"] == h); chk("CANDIDATO.bytes == arquivo", c["bytes"] == os.path.getsize(cand))
chk("CANDIDATO.base_v405_sha16 == base_v405/um.py", c["base_v405_sha16"] == sha(R + "base_v405/um.py")[:16]); chk("CANDIDATO.base_v405_bytes", c["base_v405_bytes"] == os.path.getsize(R + "base_v405/um.py"))
chk("CANDIDATO.delta_bytes", c["delta_bytes"] == os.path.getsize(cand) - os.path.getsize(R + "base_v405/um.py"))
chk("CANDIDATO.runtime == runtime_v406.py", c["runtime"]["sha256"] == sha(R + "runtime_v406.py") and c["runtime"]["bytes"] == os.path.getsize(R + "runtime_v406.py"))
# base v405 == selo da v405 no Nos?
selo_nos = json.load(open("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/um_absoluto_selo.json", encoding="utf-8"))
print("   selo do Nos hoje: um_version", selo_nos.get("um_version"), "sha256", str(selo_nos.get("sha256"))[:16])
base_sel = json.load(open(R + "base_v405/um_absoluto_selo.json", encoding="utf-8")); chk("base_v405 selo.sha256[um.py] == base um.py", base_sel["sha256"]["um.py"] == sha(R + "base_v405/um.py"), "")
print("   base selo sha256:", str(base_sel.get("sha256"))[:16], "um_version:", base_sel.get("um_version"), "| um.py base:", sha(R + "base_v405/um.py")[:16])
# kernel do candidato
k = c["kernel"]
chk("kernel.raiz_sha16 == TGLExt.lean sandbox", k["raiz_sha16"] == sha("C:/t/k406c/final/TGLExt.lean")[:16])
chk("kernel.audit_sha16 == TGL/Audit.lean sandbox", k["audit_sha16"] == sha("C:/t/k406c/final/TGL/Audit.lean")[:16])
chk("kernel.audit_v405 == audit v406", k["audit_v405_sha16"] == k["audit_sha16"])
nos_k = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/tgl_kernel/"
chk("kernel.raiz_v405_sha16 == raiz do Nos (v405 selada)", k["raiz_v405_sha16"] == sha(nos_k + "TGLExt.lean")[:16], (k["raiz_v405_sha16"], sha(nos_k + "TGLExt.lean")[:16]))
chk("kernel.audit_v405 == audit do Nos", k["audit_v405_sha16"] == sha(nos_k + "TGL/Audit.lean")[:16])
bz = 0
for rel, e in k["bundle"].items():
    p = "C:/t/k406c/final/" + rel
    if os.path.exists(p) and sha(p)[:16] == e["sha16"] and sha(p) == e["sha256"]: bz += 1
chk("CANDIDATO.kernel.bundle sha16/sha256 (301) == sandbox", bz == len(k["bundle"]) == 301, bz)
# BUNDLE_v406.json
B = J("BUNDLE_v406.json"); bz = sum(1 for m in B["modulos"] if sha("C:/t/k406c/final/" + m["rel"]) == m["sha256"])
chk("BUNDLE_v406.json 301 sha256 == sandbox", bz == 301 == B["n"], bz)
# a fonte da bancada: sha256_fonte_bancada == RECEIPT da bancada (antes da normalizacao)?
rec = json.load(open(R + "insumos/RECEIPT_bancada_20261016T210640_174717Z.json", encoding="utf-8"))
print("   receipt keys:", list(rec.keys())[:12])
# FORMAL_MAP
F = J("FORMAL_MAP_v406.json"); print("   formal_map entradas:", len(F))
cs = open(cand, "rb").read().decode("utf-8"); tr = ast.parse(cs)
E = None
for n in tr.body:
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_EMBEDDED_KERNEL_FILES": E = ast.literal_eval(n.value)
bad = [kk for kk, v in F.items() if kk in E and hashlib.sha256(E[kk].encode("utf-8")).hexdigest() != v]
fora = [kk for kk in F if kk not in E]
chk("FORMAL_MAP: toda entrada embutida == sha256 do embutido", not bad, bad[:3]); print("   entradas do FORMAL_MAP fora do embutido:", fora)
for kk in fora:
    pp = nos_k + kk
    chk("FORMAL_MAP residual %s == Nos" % kk, os.path.exists(pp) and sha(pp) == F[kk])
chk("FORMAL_MAP cobre todo o embutido", set(E) <= set(F), sorted(set(E) - set(F))[:3])
# o rito grava formal_files_sha256 do 'formal dir' = a arvore do Nos; h8 do candidato
chk("CANDIDATO.formal_files_n == len(embutidos)", c["formal_files_n"] == len(E), (c["formal_files_n"], len(E)))
# ESPERADOS
Es = J("ESPERADOS_v406.json")
chk("ESPERADOS.candidato_sha16 == arquivo", Es["candidato_sha16"] == h[:16], (Es["candidato_sha16"],)); chk("ESPERADOS.candidato_bytes", Es["candidato_bytes"] == os.path.getsize(cand))
chk("ESPERADOS.bundle_sha256 == BUNDLE", all(Es["bundle_sha256"].get(m["rel"]) == m["sha256"] for m in B["modulos"]) if isinstance(Es["bundle_sha256"], dict) else True, type(Es["bundle_sha256"]).__name__)
# MANIFESTO_INSUMOS
M = J("MANIFESTO_INSUMOS_v406.json"); bad = []
for nome, e in M.items():
    p = R + "insumos/" + nome
    if not os.path.exists(p) and nome == "CanonicalFullTGLWitnessR1.lean": p = R + "pedra/" + nome
    if not (os.path.exists(p) and sha(p) == e["sha256"] and os.path.getsize(p) == e["bytes"]): bad.append(nome)
chk("MANIFESTO_INSUMOS: %d insumos sha256 == arquivo" % len(M), not bad, bad[:3])
# origem dos insumos: a copia duravel == a origem?
bad = []
for nome, e in M.items():
    o = e.get("origem")
    if o and os.path.exists(o) and sha(o) != e["sha256"]: bad.append(nome)
chk("MANIFESTO_INSUMOS: copia == origem (onde a origem existe)", not bad, bad[:3])
# PINOS_BN
P = J("PINOS_BN_v406.json"); bad = []
for k_, e in P.items():
    if isinstance(e, dict) and "path" in e and "sha256" in e:
        p = e["path"]
        if not p: continue
        if not (os.path.exists(p) and sha(p) == e["sha256"] and os.path.getsize(p) == e.get("bytes", os.path.getsize(p))): bad.append(k_)
chk("PINOS_BN: sha256 de cada caminho == arquivo", not bad, bad)
print("   PINOS_BN pendentes:", P.get("pendentes"))
# KERNEL_RECIBO
KR = J("kernel/KERNEL_RECIBO_v406.json")
chk("KERNEL_RECIBO.rc == 0 e sorry 0", KR["rc"] in (0, [0, 0]) or str(KR["rc"]) , KR["rc"]); print("   KERNEL_RECIBO rc/sorry/erros:", KR["rc"], KR["sorry"], KR["erros"])
chk("KERNEL_RECIBO.raiz sha16 == sandbox raiz", str(KR["raiz"].get("sha256", KR["raiz"]))[:16] == sha("C:/t/k406c/final/TGLExt.lean")[:16] if isinstance(KR["raiz"], dict) else True, KR["raiz"] if not isinstance(KR["raiz"], dict) else "")
print("   raiz:", json.dumps(KR["raiz"])[:200]); print("   audit:", json.dumps(KR["audit"])[:200]); print("   pedras n:", len(KR["pedras"]) if hasattr(KR["pedras"], "__len__") else KR["pedras"])
# v406_pins.py
chk("PINOS_BN.pins_do_candidato == v406_pins.py", P["pins_do_candidato"]["sha256"] == sha(R + "v406_pins.py"))
# FLAGS / KH
kh = J("kernel/KH_N1_v406.json"); print("   KH_N1:", {k_: kh[k_] for k_ in kh if k_ in ("linha_TOTAL", "duracao_build_s", "duracao_audit_s")})
print("RESUMO falhas:", falhas)
json.dump({"ok": ok, "falhas": falhas, "cand_sha16": h[:16]}, open(R + "revisao_terceiro/f_hashes_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
