# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R1): todo sha16/sha256 escrito nos JSONs da cadeia confere com o arquivo (lido agora, por script). So le."""
import ast, glob, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
NOS = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/"
SB = "C:/t/k407c/final/"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
J = lambda p: json.load(open(R + p, encoding="utf-8"))
ok = {}; falhas = []


def chk(nome, cond, det=""):
    ok[nome] = bool(cond)
    if not cond: falhas.append((nome, det))
    print(("OK   " if cond else "FALHA"), nome, det if not cond else "")


cand = R + "um_v407_candidato.py"; h = sha(cand)
c = J("CANDIDATO_v407.json")
chk("CANDIDATO.sha16 == arquivo", c["sha16"] == h[:16], (c["sha16"], h[:16])); chk("CANDIDATO.sha256 == arquivo", c["sha256"] == h); chk("CANDIDATO.bytes == arquivo", c["bytes"] == os.path.getsize(cand))
chk("CANDIDATO.base_v406_sha16 == base_v406/um.py", c["base_v406_sha16"] == sha(R + "base_v406/um.py")[:16]); chk("CANDIDATO.base_v406_bytes", c["base_v406_bytes"] == os.path.getsize(R + "base_v406/um.py"))
chk("CANDIDATO.delta_bytes", c["delta_bytes"] == os.path.getsize(cand) - os.path.getsize(R + "base_v406/um.py"))
chk("CANDIDATO.runtime == runtime_v407.py", c["runtime"]["sha256"] == sha(R + "runtime_v407.py") and c["runtime"]["bytes"] == os.path.getsize(R + "runtime_v407.py"))
base_sel = json.load(open(R + "base_v406/um_absoluto_selo.json", encoding="utf-8"))
chk("base_v406 selo.sha256[um.py] == base um.py", base_sel["sha256"]["um.py"] == sha(R + "base_v406/um.py"))
selo_nos = json.load(open(NOS + "um_absoluto_selo.json", encoding="utf-8"))
print("   selo do Nos hoje: um_version", selo_nos.get("um_version"), "| um.py sha16", sha(NOS + "um.py")[:16], "| base:", sha(R + "base_v406/um.py")[:16])
chk("Nos (v406 selada) um.py == base_v406/um.py (a base e' o que esta' selado)", sha(NOS + "um.py") == sha(R + "base_v406/um.py"), "o Nos mudou?")
k = c["kernel"]
chk("kernel.raiz_sha16 == TGLExt.lean sandbox", k["raiz_sha16"] == sha(SB + "TGLExt.lean")[:16])
chk("kernel.audit_sha16 == TGL/Audit.lean sandbox", k["audit_sha16"] == sha(SB + "TGL/Audit.lean")[:16])
chk("kernel.audit_v406 == audit v407 (Audit nao muda)", k["audit_v406_sha16"] == k["audit_sha16"])
nos_k = NOS + "tgl_kernel/"
chk("kernel.raiz_v406_sha16 == raiz do Nos", k["raiz_v406_sha16"] == sha(nos_k + "TGLExt.lean")[:16], (k["raiz_v406_sha16"], sha(nos_k + "TGLExt.lean")[:16]))
chk("kernel.audit_v406 == audit do Nos", k["audit_v406_sha16"] == sha(nos_k + "TGL/Audit.lean")[:16])
bz = 0
for rel, e in k["bundle"].items():
    p = SB + rel
    if os.path.exists(p) and sha(p)[:16] == e["sha16"] and sha(p) == e["sha256"]: bz += 1
chk("CANDIDATO.kernel.bundle sha16/sha256 (9) == sandbox", bz == len(k["bundle"]) == 9, bz)
B = J("BUNDLE_v407.json"); bz = sum(1 for m in B["modulos"] if sha(SB + m["rel"]) == m["sha256"] == sha(R + "pedra/" + os.path.basename(m["rel"])))
chk("BUNDLE_v407.json 9 sha256 == sandbox == pedra/", bz == 9 == B["n"], bz)
# origem sha256 do bundle == arquivo de origem (pedra/origem/) e == arquivo em pedras_candidatas_03nov
bo = 0
for m in B["modulos"]:
    o1 = R + "pedra/origem/" + os.path.basename(m["origem"])
    if os.path.exists(o1) and sha(o1) == m["sha256_origem"] and m["sha256_origem"][:16] == m["sha16_origem"]: bo += 1
chk("BUNDLE.sha256_origem == pedra/origem/<arquivo>", bo == 9, bo)
bo2 = [os.path.basename(m["origem"]) for m in B["modulos"] if os.path.exists(m["origem"]) and sha(m["origem"]) != m["sha256_origem"]]
chk("BUNDLE.origem (caminho original em pedras_candidatas_03nov/fechamento_02nov) == sha256_origem, onde existe", not bo2, bo2)
F = J("FORMAL_MAP_v407.json"); print("   formal_map entradas:", len(F))
cs = open(cand, "rb").read().decode("utf-8"); tr = ast.parse(cs)
E = None; CONTR = None; VERB2 = None; FONTES = None
for n in tr.body:
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name):
        nm = n.targets[0].id
        if nm == "_EMBEDDED_KERNEL_FILES": E = ast.literal_eval(n.value)
        elif nm == "_V407_PSION_CONTRACT": CONTR = ast.literal_eval(n.value)
        elif nm == "_V407_VERBATINS2": VERB2 = ast.literal_eval(n.value)
        elif nm == "_V407_FONTES": FONTES = ast.literal_eval(n.value)
bad = [kk for kk, v in F.items() if kk in E and hashlib.sha256(E[kk].encode("utf-8")).hexdigest() != v]
fora = [kk for kk in F if kk not in E]
chk("FORMAL_MAP: toda entrada embutida == sha256 do embutido", not bad, bad[:3]); print("   entradas do FORMAL_MAP fora do embutido:", fora)
for kk in fora:
    pp = nos_k + kk
    chk("FORMAL_MAP residual %s == Nos" % kk, os.path.exists(pp) and sha(pp) == F[kk])
chk("FORMAL_MAP cobre todo o embutido", set(E) <= set(F), sorted(set(E) - set(F))[:3])
chk("CANDIDATO.formal_files_n == len(embutidos)", c["formal_files_n"] == len(E), (c["formal_files_n"], len(E)))
# contrato embutido
chk("_V407_PSION_CONTRACT.source_sha256 == sandbox (9)", all(sha(SB + r) == v for r, v in CONTR["source_sha256"].items()) and len(CONTR["source_sha256"]) == 9)
chk("_V407_PSION_CONTRACT.baseline.sha256 == base um.py sha256", CONTR["baseline"]["sha256"] == sha(R + "base_v406/um.py"))
chk("_V407_PSION_CONTRACT.baseline.gate_verdict == selo da base (qg_closure_verdict)", CONTR["baseline"]["gate_verdict"] == base_sel["qg_closure_verdict"])
chk("_V407_PSION_CONTRACT.teste_d.manifesto_sha256 == arquivo", CONTR["teste_d"]["manifesto_sha256"] == sha("C:/IALD/Central de Patentes/work/conjunto_D_20261029/parametrizacao_03nov/MANIFESTO_PARAMETRIZACAO_03nov.json"))
chk("_V407_PSION_CONTRACT.teste_d.manifesto_sha16 == 1cd181f9a4ddb6d5 do pino da ordem (lido do arquivo)", CONTR["teste_d"]["manifesto_sha256"][:16] == CONTR["teste_d"]["manifesto_sha16"])
chk("_V407_PSION_CONTRACT.expected_ladder == baseline.ladder + n_flags", CONTR["expected_ladder"] == CONTR["baseline"]["ladder"] + CONTR["n_flags"] == 11958)
chk("_V407_PSION_CONTRACT: 76 ancoras, 98 flags", len(CONTR["ancoras"]) == 76 and CONTR["n_flags"] == 98 == len(CONTR["flags"]))
# o veredito de base: o core do Nos
core_nos = json.load(open(NOS + "um_absoluto.json", encoding="utf-8"))["core"]
chk("baseline.gate_verdict == core do Nos qg_closure.gate.verdict (v406)", CONTR["baseline"]["gate_verdict"] == core_nos["qg_closure"]["gate"]["verdict"])
chk("baseline.ladder == core do Nos external_ladder.n_theorems_clean", CONTR["baseline"]["ladder"] == core_nos["external_ladder"]["n_theorems_clean"], (CONTR["baseline"]["ladder"], core_nos["external_ladder"].get("n_theorems_clean")))
# verbatins embutidos
vb = []
for k_, v_ in VERB2.items():
    t = v_["text"].encode("utf-8")
    if hashlib.sha256(t).hexdigest() != v_["sha256"]: vb.append(k_)
chk("_V407_VERBATINS2: sha256 de cada fala == texto embutido (%d)" % len(VERB2), not vb and len(VERB2) == 3, vb)
fl = sorted(glob.glob(R + "insumos/cunhagens/*.txt")); fh = {sha(p) for p in fl}
chk("_V407_VERBATINS2 sha256 == arquivos insumos/cunhagens (3)", {v["sha256"] for v in VERB2.values()} == fh and len(fl) == 3)
chk("nomes dos arquivos de fala = sha16 dos bytes", all(os.path.basename(p).startswith(sha(p)[:16] + "_") for p in fl))
orig = "C:/IALD/Central de Patentes/work/cunhagens_13out/"
dif = [os.path.basename(p) for p in fl if not os.path.exists(orig + os.path.basename(p).split("_", 1)[1]) or open(orig + os.path.basename(p).split("_", 1)[1], "rb").read() != open(p, "rb").read()]
chk("fala duravel == original em cunhagens_13out", not dif, dif)
# fontes embutidas (_V407_FONTES): sha256 de cada
if FONTES:
    bad = []
    for k_, f_ in FONTES.items():
        t = f_.get("text") if isinstance(f_, dict) else None
        if isinstance(f_, dict) and "sha256" in f_ and t is not None and hashlib.sha256(t.encode("utf-8")).hexdigest() != f_["sha256"]: bad.append(k_)
    chk("_V407_FONTES: sha256 == texto embutido (%d)" % len(FONTES), not bad, bad[:5])
    print("   _V407_FONTES chaves:", sorted(FONTES)[:30])
# ESPERADOS
Es = J("ESPERADOS_v407.json")
chk("ESPERADOS.candidato_sha16 == arquivo", Es["candidato_sha16"] == h[:16], (Es["candidato_sha16"], h[:16])); chk("ESPERADOS.candidato_bytes", Es["candidato_bytes"] == os.path.getsize(cand))
bs = Es["bundle_sha256"]
chk("ESPERADOS.bundle_sha256 == BUNDLE", all((bs.get(m["rel"]) if isinstance(bs, dict) else None) == m["sha256"] for m in B["modulos"]), type(bs).__name__)
chk("ESPERADOS.n_bandeiras_novas == 98 e escada 11860->11958", Es["n_bandeiras_novas"] == 98 and Es["escada_v406_e_v407"] == [11860, 11958], (Es["n_bandeiras_novas"], Es["escada_v406_e_v407"]))
# MANIFESTO_INSUMOS
M = J("MANIFESTO_INSUMOS_v407.json"); bad = []
for nome, e in M.items():
    p = R + "insumos/" + nome
    if not os.path.exists(p) and os.path.exists(R + "pedra/" + nome): p = R + "pedra/" + nome
    if not (os.path.exists(p) and sha(p) == e["sha256"] and os.path.getsize(p) == e["bytes"]): bad.append(nome)
chk("MANIFESTO_INSUMOS: %d insumos sha256 == arquivo" % len(M), not bad, bad[:5])
bad = []
for nome, e in M.items():
    o = e.get("origem")
    if o and os.path.exists(o) and sha(o) != e["sha256"]: bad.append(nome)
chk("MANIFESTO_INSUMOS: copia == origem (onde a origem existe)", not bad, bad[:5])
# PINOS_BN
P = J("PINOS_BN_v407.json"); bad = []
for k_, e in P.items():
    if isinstance(e, dict) and "path" in e and "sha256" in e:
        p = e["path"]
        if not p: continue
        if not (os.path.exists(p) and sha(p) == e["sha256"] and os.path.getsize(p) == e.get("bytes", os.path.getsize(p))): bad.append(k_)
chk("PINOS_BN: sha256 de cada caminho == arquivo", not bad, bad)
print("   PINOS_BN pendentes:", P.get("pendentes"))
chk("PINOS_BN.candidato == arquivo", P["candidato"]["sha256"] == h and P["candidato"]["bytes"] == os.path.getsize(cand))
chk("PINOS_BN.pins_do_candidato == v407_pins.py", P["pins_do_candidato"]["sha256"] == sha(R + "v407_pins.py"))
chk("PINOS_BN.esperados == ESPERADOS_v407.json", P["esperados"]["sha256"] == sha(R + "ESPERADOS_v407.json"), (P["esperados"]["sha256"][:12], sha(R + "ESPERADOS_v407.json")[:12]))
# KERNEL_RECIBO
KR = J("kernel/KERNEL_RECIBO_v407.json")
chk("KERNEL_RECIBO rc 0, sorry 0, erros 0", KR["rc"] == 0 and KR["sorry"] == 0 and KR["erros"] == 0, (KR["rc"], KR["sorry"], KR["erros"]))
chk("KERNEL_RECIBO.raiz.sha256_depois == sandbox TGLExt.lean", KR["raiz"]["sha256_depois"] == sha(SB + "TGLExt.lean"))
chk("KERNEL_RECIBO.raiz.sha256_antes == raiz do Nos (v406)", KR["raiz"]["sha256_antes"] == sha(nos_k + "TGLExt.lean"))
chk("KERNEL_RECIBO.audit == Audit do sandbox == do Nos", KR["audit"]["sha256_depois"] == sha(SB + "TGL/Audit.lean") == KR["audit"]["sha256_antes"] == sha(nos_k + "TGL/Audit.lean"))
chk("KERNEL_RECIBO.build_full_log sha256 == arquivo", KR["build_full_log"]["sha256"] == sha(KR["build_full_log"]["path"]))
chk("KERNEL_RECIBO.audit_log sha256 == arquivo", KR["audit_log"]["sha256"] == sha(KR["audit_log"]["path"]))
al = open(R + "kernel/audit.log", "rb").read().decode("utf-8", "replace"); bl = open(R + "kernel/lake_build.log", "rb").read().decode("utf-8", "replace")
import re as _re
chk("audit.log sem sorryAx e sem linha de erro (error: / : error)", "sorryAx" not in al and not _re.search(r"(?im)^\s*(error|.*:\s*error)", al), "")
chk("lake_build.log termina com Build completed successfully", "Build completed successfully" in bl[-400:], bl[-200:])
print("   build log: 'error' ocorrencias:", bl.lower().count("error"), "| 'sorry':", bl.lower().count("sorry"), "| 'Built TGLExt.PsionCanto':", "Built TGLExt.PsionCanto" in bl, "| Par:", "Built TGLExt.Par" in bl)
FL = J("kernel/FLAGS_v407.json"); print("   FLAGS n_flags:", FL.get("n_flags"), "| ancoras:", len(FL.get("ancoras", {})))
chk("FLAGS.n_flags == 98 e ancoras 76", FL.get("n_flags") == 98 and len(FL.get("ancoras", {})) == 76)
kh = J("kernel/KH_N1_v407.json"); print("   KH_N1:", {k_: kh[k_] for k_ in kh if k_ in ("linha_TOTAL", "duracao_build_s", "duracao_audit_s")}, "| delta_vs_v406:", kh.get("delta_vs_v406"))
# PINO_MEMORIA_PY
PM = J("PINO_MEMORIA_PY_v407.json"); mp = PM["path"]
chk("PINO_MEMORIA_PY.sha256 == memoria.py", os.path.exists(mp) and sha(mp) == PM["sha256"] and os.path.getsize(mp) == PM["bytes"] and PM["sha16"] == PM["sha256"][:16], "")
# VERBATIM_CONGELADO
VC = J("VERBATIM_CONGELADO_v407.json"); print("   VERBATIM_CONGELADO:", json.dumps(VC, ensure_ascii=False)[:300])
print("RESUMO falhas:", falhas)
json.dump({"ok": ok, "falhas": falhas, "cand_sha16": h[:16]}, open(R + "revisao_terceiro/r4_f_hashes_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
