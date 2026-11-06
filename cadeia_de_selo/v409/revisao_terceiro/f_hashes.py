# -*- coding: utf-8 -*-
"""Revisor terceiro v409 (R1): todo sha16/sha256 escrito nos JSONs da cadeia confere com o arquivo (lido agora, por script). So le.
Conjuntos nominais: CANDIDATO, BUNDLE, KERNEL_RECIBO, PINOS_BN, ESPERADOS, MANIFESTO_INSUMOS, FORMAL_MAP, PINO_MEMORIA_PY, VERBATIM_CONGELADO, o contrato _V409_TRADUCAO_CONTRACT, _V409_VERBATINS2 e _V407_FONTES;
e uma varredura de TODO JSON de nivel superior (e de kernel/, insumos/) por pares {path, sha256[, bytes]} (recursivo)."""
import ast, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
NOS = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/"
SB = "C:/t/k409c/final/"
CU = "C:/IALD/Central de Patentes/work/cunhagens_13out/"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
J = lambda p: json.load(open(R + p, encoding="utf-8"))
ok = {}; falhas = []


def chk(nome, cond, det=""):
    ok[nome] = bool(cond)
    if not cond: falhas.append((nome, det))
    print(("OK   " if cond else "FALHA"), nome, det if not cond else "")


cand = R + "um_v409_candidato.py"; h = sha(cand)
c = J("CANDIDATO_v409.json")
chk("CANDIDATO.sha16 == arquivo", c["sha16"] == h[:16], (c["sha16"], h[:16])); chk("CANDIDATO.sha256 == arquivo", c["sha256"] == h); chk("CANDIDATO.bytes == arquivo", c["bytes"] == os.path.getsize(cand))
chk("CANDIDATO.base_v408_sha16 == base_v408/um.py", c["base_v408_sha16"] == sha(R + "base_v408/um.py")[:16]); chk("CANDIDATO.base_v408_bytes", c["base_v408_bytes"] == os.path.getsize(R + "base_v408/um.py"))
chk("CANDIDATO.delta_bytes", c["delta_bytes"] == os.path.getsize(cand) - os.path.getsize(R + "base_v408/um.py"))
chk("CANDIDATO.runtime == runtime_v409.py", c["runtime"]["sha256"] == sha(R + "runtime_v409.py") and c["runtime"]["bytes"] == os.path.getsize(R + "runtime_v409.py"))
base_sel = json.load(open(R + "base_v408/um_absoluto_selo.json", encoding="utf-8"))
chk("base_v408 selo.sha256[um.py] == base um.py", base_sel["sha256"]["um.py"] == sha(R + "base_v408/um.py"))
chk("base_v408/um.py sha16 == e7bc6b10e8ff76be (a v408 selada, escrita no pedido)", sha(R + "base_v408/um.py")[:16] == "e7bc6b10e8ff76be")
selo_nos = json.load(open(NOS + "um_absoluto_selo.json", encoding="utf-8"))
print("   selo do Nos hoje: um_version", selo_nos.get("um_version"), "| um.py sha16", sha(NOS + "um.py")[:16], "| base:", sha(R + "base_v408/um.py")[:16])
chk("Nos (v408 selada) um.py == base_v408/um.py (a base e' o que esta' selado)", sha(NOS + "um.py") == sha(R + "base_v408/um.py"), "o Nos mudou?")
k = c["kernel"]
chk("kernel.raiz_sha16 == TGLExt.lean sandbox", k["raiz_sha16"] == sha(SB + "TGLExt.lean")[:16])
chk("kernel.audit_sha16 == TGL/Audit.lean sandbox", k["audit_sha16"] == sha(SB + "TGL/Audit.lean")[:16])
chk("kernel.audit_v408 == audit v409 (Audit nao muda)", k["audit_v408_sha16"] == k["audit_sha16"])
nos_k = NOS + "tgl_kernel/"
chk("kernel.raiz_v408_sha16 == raiz do Nos", k["raiz_v408_sha16"] == sha(nos_k + "TGLExt.lean")[:16], (k["raiz_v408_sha16"], sha(nos_k + "TGLExt.lean")[:16]))
chk("kernel.audit_v408 == audit do Nos", k["audit_v408_sha16"] == sha(nos_k + "TGL/Audit.lean")[:16])
bz = 0
for rel, e in k["bundle"].items():
    p = SB + rel
    if os.path.exists(p) and sha(p)[:16] == e["sha16"] and sha(p) == e["sha256"]: bz += 1
chk("CANDIDATO.kernel.bundle sha16/sha256 (2) == sandbox", bz == len(k["bundle"]) == 2, bz)
B = J("BUNDLE_v409.json"); bz = sum(1 for m in B["modulos"] if sha(SB + m["rel"]) == m["sha256"] == sha(R + "pedra/" + os.path.basename(m["rel"])))
chk("BUNDLE_v409.json 2 sha256 == sandbox == pedra/", bz == 2 == B["n"], bz)
bo = 0; bo_ins = 0
for m in B["modulos"]:
    o1 = R + "pedra/origem/" + os.path.basename(m["origem"])
    if os.path.exists(o1) and sha(o1) == m["sha256_origem"] and m["sha256_origem"][:16] == m["sha16_origem"]: bo += 1
    if os.path.exists(m["origem"]) and sha(m["origem"]) == m["sha256_origem"]: bo_ins += 1
chk("BUNDLE.sha256_origem == pedra/origem/<arquivo>", bo == 2, bo)
chk("BUNDLE.origem (insumos\\<Nome>.lean) == sha256_origem", bo_ins == 2, bo_ins)
for m in B["modulos"]:
    oc = m["origem_candidata"]
    print("   origem_candidata:", os.path.basename(oc), "existe:", os.path.exists(oc), "sha256 ==", (sha(oc) == m["sha256_candidata"]) if os.path.exists(oc) else None)
rn = json.load(open(B["recibo_dos_nomes"], encoding="utf-8")); chk("BUNDLE.recibo_dos_nomes_sha256 == arquivo", sha(B["recibo_dos_nomes"]) == B["recibo_dos_nomes_sha256"])
F = J("FORMAL_MAP_v409.json"); print("   formal_map entradas:", len(F))
cs = open(cand, "rb").read().decode("utf-8"); tr = ast.parse(cs)
E = None; CONTR = None; VERB2 = None; FONTES = None; F407 = None
for n in tr.body:
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name):
        nm = n.targets[0].id
        if nm == "_EMBEDDED_KERNEL_FILES": E = ast.literal_eval(n.value)
        elif nm == "_V409_TRADUCAO_CONTRACT": CONTR = ast.literal_eval(n.value)
        elif nm == "_V409_VERBATINS2": VERB2 = ast.literal_eval(n.value)
        elif nm == "_V409_FONTES": FONTES = ast.literal_eval(n.value)
        elif nm == "_V407_FONTES": F407 = ast.literal_eval(n.value)
bad = [kk for kk, v in F.items() if kk in E and hashlib.sha256(E[kk].encode("utf-8")).hexdigest() != v]
fora = [kk for kk in F if kk not in E]
chk("FORMAL_MAP: toda entrada embutida == sha256 do embutido", not bad, bad[:3]); print("   entradas do FORMAL_MAP fora do embutido:", fora)
for kk in fora:
    pp = nos_k + kk
    chk("FORMAL_MAP residual %s == Nos" % kk, os.path.exists(pp) and sha(pp) == F[kk])
chk("FORMAL_MAP cobre todo o embutido", set(E) <= set(F), sorted(set(E) - set(F))[:3])
chk("CANDIDATO.formal_files_n == len(embutidos)", c["formal_files_n"] == len(E), (c["formal_files_n"], len(E)))
chk("_V409_TRADUCAO_CONTRACT.source_sha256 == sandbox (2)", all(sha(SB + r) == v for r, v in CONTR["source_sha256"].items()) and len(CONTR["source_sha256"]) == 2)
chk("_V409_TRADUCAO_CONTRACT.baseline.sha256 == base um.py sha256", CONTR["baseline"]["sha256"] == sha(R + "base_v408/um.py"))
chk("_V409_TRADUCAO_CONTRACT.baseline.gate_verdict == selo da base (qg_closure_verdict)", CONTR["baseline"]["gate_verdict"] == base_sel["qg_closure_verdict"])
chk("_V409_TRADUCAO_CONTRACT.expected_ladder == baseline.ladder + n_flags == 12187", CONTR["expected_ladder"] == CONTR["baseline"]["ladder"] + CONTR["n_flags"] == 12187, (CONTR["expected_ladder"], CONTR["baseline"]["ladder"], CONTR["n_flags"]))
chk("_V409_TRADUCAO_CONTRACT: 82 ancoras, 158 flags", len(CONTR["ancoras"]) == 82 == CONTR["n_ancoras"] and CONTR["n_flags"] == 158 == len(CONTR["flags"]))
core_nos = json.load(open(NOS + "um_absoluto.json", encoding="utf-8"))["core"]
chk("baseline.gate_verdict == core do Nos qg_closure.gate.verdict (v408)", CONTR["baseline"]["gate_verdict"] == core_nos["qg_closure"]["gate"]["verdict"])
chk("baseline.ladder == core do Nos external_ladder.n_theorems_clean", CONTR["baseline"]["ladder"] == core_nos["external_ladder"]["n_theorems_clean"], (CONTR["baseline"]["ladder"], core_nos["external_ladder"].get("n_theorems_clean")))
ip = CONTR["acervo_v407_repinado"]; pur = R + "../v408/insumos/PSION_NO_ACERVO_04nov_purgado.md"
chk("acervo_v407_repinado.sha256 == PSION_NO_ACERVO_04nov_purgado.md (v408/insumos)", sha(pur) == ip["sha256"] and os.path.getsize(pur) == ip["bytes"])
chk("acervo_v407_repinado: integra NAO pinada; sha16 da integra citado", ip["integra_pinada"] is False and ip["integra_fora_do_espelho"] is True and ip["integra_sha16"] == "823206bc6d5a74af")
k7 = F407["psion_no_acervo_do_imac_03nov"]
chk("_V407_FONTES[psion_no_acervo].sha256 == a copia purgada", k7["sha256"] == ip["sha256"] and os.path.exists(k7["arquivo"]) and sha(k7["arquivo"]) == k7["sha256"], k7["arquivo"])
vb = []
for k_, v_ in VERB2.items():
    t = v_["text"].encode("utf-8")
    if hashlib.sha256(t).hexdigest() != v_["sha256"]: vb.append(k_)
chk("_V409_VERBATINS2: sha256 de cada fala == texto embutido (%d)" % len(VERB2), not vb and len(VERB2) == 14, (vb, len(VERB2)))
fl = sorted(glob.glob(R + "insumos/cunhagens/*.txt")); fh = {sha(p) for p in fl}
print("   arquivos em insumos/cunhagens:", len(fl))
chk("_V409_VERBATINS2 sha256 == arquivos insumos/cunhagens (os 14 embutidos estao la')", {v["sha256"] for v in VERB2.values()} <= fh, len({v["sha256"] for v in VERB2.values()} - fh))
# prefixo do nome: sha16 do arquivo (inteiras) OU sha16 do ORIGINAL (trechos)
mal = []
for p in fl:
    nome = os.path.basename(p); pref = nome.split("_", 1)[0]
    if nome.endswith(".trecho_que_fica.txt"):
        # o original esta' em cunhagens_13out com o nome sem o prefixo e com sufixo _verbatim.txt; o trecho tem de ser substring do original
        base = nome.split("_", 1)[1].replace(".trecho_que_fica.txt", "")
        cands = glob.glob(CU + base + "*.txt") or glob.glob(CU + base.replace("_primeira_frase", "") + "*.txt")
        orig = [q for q in glob.glob(CU + "OPERADOR_05nov_*.txt") if hashlib.sha256(open(q, "rb").read()).hexdigest()[:16] == pref]
        if not orig: mal.append((nome, "original com este sha16 nao achado em cunhagens_13out")); continue
        tz = open(p, "rb").read().decode("utf-8").strip(); oz = open(orig[0], "rb").read().decode("utf-8")
        if tz not in oz and re.sub(r"\s+", " ", tz) not in re.sub(r"\s+", " ", oz): mal.append((nome, "o trecho nao e' substring do original"))
    else:
        if pref != sha(p)[:16]: mal.append((nome, "prefixo != sha16 dos bytes"))
chk("nomes dos arquivos de fala: prefixo = sha16 dos bytes (inteiras) ou do ORIGINAL (trechos, substring do original)", not mal, mal)
dif = []
for p in fl:
    nome = os.path.basename(p)
    if nome.endswith(".trecho_que_fica.txt"): continue
    o = CU + nome.split("_", 1)[1]
    if not os.path.exists(o) or open(o, "rb").read() != open(p, "rb").read(): dif.append(nome)
chk("fala duravel (inteira) == original em cunhagens_13out", not dif, dif)
if FONTES:
    bad = []
    for k_, f_ in FONTES.items():
        t = f_.get("text") if isinstance(f_, dict) else None
        if isinstance(f_, dict) and "sha256" in f_ and t is not None and hashlib.sha256(t.encode("utf-8")).hexdigest() != f_["sha256"]: bad.append(k_)
    chk("_V409_FONTES: sha256 == texto embutido (%d)" % len(FONTES), not bad, bad[:5])
Es = J("ESPERADOS_v409.json")
chk("ESPERADOS.candidato_sha16 == arquivo", Es["candidato_sha16"] == h[:16], (Es["candidato_sha16"], h[:16])); chk("ESPERADOS.candidato_bytes", Es["candidato_bytes"] == os.path.getsize(cand))
bs = Es["bundle_sha256"]
chk("ESPERADOS.bundle_sha256 == BUNDLE", all((bs.get(m["rel"]) if isinstance(bs, dict) else None) == m["sha256"] for m in B["modulos"]), type(bs).__name__)
chk("ESPERADOS.n_bandeiras_novas == 158 e escada 12029->12187", Es["n_bandeiras_novas"] == 158 and Es["escada_v408_e_v409"] == [12029, 12187], (Es["n_bandeiras_novas"], Es["escada_v408_e_v409"]))
M = J("MANIFESTO_INSUMOS_v409.json"); bad = []
for nome, e in M.items():
    p = R + "insumos/" + nome
    if not os.path.exists(p) and os.path.exists(R + "pedra/" + nome): p = R + "pedra/" + nome
    if not os.path.exists(p) and nome.endswith("_embutida.lean"): p = R + "pedra/" + nome.replace("_embutida", "")
    if not os.path.exists(p) and nome in ("BUNDLE_v409.json",): p = R + nome
    if not os.path.exists(p) and nome.startswith("KH_N1"): p = R + "kernel/" + nome
    if not (os.path.exists(p) and sha(p) == e["sha256"] and os.path.getsize(p) == e["bytes"]): bad.append(nome)
chk("MANIFESTO_INSUMOS: %d insumos sha256 == arquivo" % len(M), not bad, bad[:6])
bad = []
for nome, e in M.items():
    o = e.get("origem")
    if o and os.path.isabs(o) and os.path.exists(o) and sha(o) != e["sha256"]: bad.append(nome)
chk("MANIFESTO_INSUMOS: copia == origem (onde a origem existe)", not bad, bad[:5])
P = J("PINOS_BN_v409.json"); bad = []
for k_, e in P.items():
    if isinstance(e, dict) and "path" in e and "sha256" in e:
        p = e["path"]
        if not p: continue
        if not (os.path.exists(p) and sha(p) == e["sha256"] and os.path.getsize(p) == e.get("bytes", os.path.getsize(p))): bad.append(k_)
chk("PINOS_BN: sha256 de cada caminho == arquivo", not bad, bad)
print("   PINOS_BN pendentes:", P.get("pendentes"))
chk("PINOS_BN.candidato == arquivo", P["candidato"]["sha256"] == h and P["candidato"]["bytes"] == os.path.getsize(cand))
chk("PINOS_BN.pins_do_candidato == v409_pins.py", P["pins_do_candidato"]["sha256"] == sha(R + "v409_pins.py"))
chk("PINOS_BN.esperados == ESPERADOS_v409.json", P["esperados"]["sha256"] == sha(R + "ESPERADOS_v409.json"), (P["esperados"]["sha256"][:12], sha(R + "ESPERADOS_v409.json")[:12]))
chk("PINOS_BN.selo_anterior_v408 == base_v408/um_absoluto_selo.json", P["selo_anterior_v408"]["sha256"] == sha(R + "base_v408/um_absoluto_selo.json"))
KR = J("kernel/KERNEL_RECIBO_v409.json")
chk("KERNEL_RECIBO rc 0, sorry 0, erros 0", str(KR["rc"]) == "0" and str(KR["sorry"]) == "0" and str(KR["erros"]) == "0", (KR["rc"], KR["sorry"], KR["erros"]))
chk("KERNEL_RECIBO.raiz.sha256_depois == sandbox TGLExt.lean", KR["raiz"]["sha256_depois"] == sha(SB + "TGLExt.lean"))
chk("KERNEL_RECIBO.raiz.sha256_antes == raiz do Nos (v408)", KR["raiz"]["sha256_antes"] == sha(nos_k + "TGLExt.lean"))
chk("KERNEL_RECIBO.audit == Audit do sandbox == do Nos", KR["audit"]["sha256_depois"] == sha(SB + "TGL/Audit.lean") == KR["audit"]["sha256_antes"] == sha(nos_k + "TGL/Audit.lean"))
chk("KERNEL_RECIBO.build_full_log sha256 == arquivo", KR["build_full_log"]["sha256"] == sha(KR["build_full_log"]["path"]))
chk("KERNEL_RECIBO.audit_log sha256 == arquivo", KR["audit_log"]["sha256"] == sha(KR["audit_log"]["path"]))
chk("KERNEL_RECIBO.pedras sha256 == sandbox (2)", len(KR["pedras"]) == 2 and all(sha(SB + p["path"]) == p["sha256"] for p in KR["pedras"]))
chk("KERNEL_RECIBO.axiomas == trio", sorted(KR["axiomas"]) == ["Classical.choice", "Quot.sound", "propext"], KR["axiomas"])
chk("KERNEL_RECIBO.criterios j1: 223 declaracoes, 182 teoremas, 0 fora do trio", KR["criterios"]["j1_declaracoes"]["medido"] == 223 and KR["criterios"]["j1_teoremas"]["medido"] == 182 and KR["criterios"]["j1_fora_do_trio"]["medido"] == 0, KR["criterios"])
al = open(R + "kernel/audit.log", "rb").read().decode("utf-8", "replace"); bl = open(R + "kernel/lake_build.log", "rb").read().decode("utf-8", "replace")
chk("audit.log sem sorryAx e sem linha de erro (error: / : error)", "sorryAx" not in al and not re.search(r"(?im)^\s*(error|.*:\s*error)", al), "")
chk("lake_build.log termina com Build completed successfully", "Build completed successfully" in bl[-400:], bl[-200:])
print("   build log: 'error' ocorrencias:", bl.lower().count("error"), "| 'sorry':", bl.lower().count("sorry"))
FL = J("kernel/FLAGS_v409.json"); print("   FLAGS n_flags:", FL.get("n_flags"), "| ancoras:", len(FL.get("ancoras", {})))
chk("FLAGS.n_flags == 158 e ancoras 82", FL.get("n_flags") == 158 and len(FL.get("ancoras", {})) == 82)
kh = J("kernel/KH_N1_v409.json"); print("   KH_N1:", {k_: kh[k_] for k_ in kh if k_ in ("linha_TOTAL", "duracao_build_s", "duracao_audit_s")}, "| delta_vs_v408:", kh.get("delta_vs_v408"))
PM = J("PINO_MEMORIA_PY_v409.json"); mp = PM["path"]
chk("PINO_MEMORIA_PY.sha256 == memoria.py", os.path.exists(mp) and sha(mp) == PM["sha256"] and os.path.getsize(mp) == PM["bytes"] and PM["sha16"] == PM["sha256"][:16], "")
VC = J("VERBATIM_CONGELADO_v409.json"); print("   VERBATIM_CONGELADO: n =", VC.get("n"), "| registro:", len(VC.get("registro", [])))
bad = [r_["arquivo"] for r_ in VC["registro"] if not (os.path.exists(r_["arquivo"]) and sha(r_["arquivo"]) == r_["sha256"] and os.path.getsize(r_["arquivo"]) == r_["bytes"])]
chk("VERBATIM_CONGELADO: cada arquivo (14) com path+sha256+bytes == disco", not bad and len(VC["registro"]) == 14, bad[:5])


# varredura geral: todo {path, sha256[, bytes]} em todo JSON de nivel superior (e de kernel/, insumos/)
def varre(o, onde, acc):
    if isinstance(o, dict):
        if "sha256" in o and isinstance(o.get("sha256"), str) and len(o["sha256"]) == 64 and isinstance(o.get("path"), str):
            acc.append((onde, o["path"], o["sha256"], o.get("bytes")))
        for kk, vv in o.items(): varre(vv, onde + "/" + str(kk), acc)
    elif isinstance(o, list):
        for i, vv in enumerate(o): varre(vv, onde + "[%d]" % i, acc)


acc = []
for p in sorted(glob.glob(R + "*.json") + glob.glob(R + "kernel/*.json") + glob.glob(R + "insumos/*.json")):
    nm = os.path.basename(p)
    if nm.startswith(("EXAME_PONTOS", "SIMULACAO_ARVORE", "ESPERADOS", "ensaio_a_seco", "conferencia_rito", "FORMAL_MAP", "KERNEL_RECIBO", "CANDIDATO_v409")): continue
    try: d = json.load(open(p, encoding="utf-8"))
    except Exception: continue
    varre(d, nm, acc)
print("   pares {path, sha256} encontrados em JSONs:", len(acc))
mud = []; ause = []
for onde, path, s, b in acc:
    pp = path if os.path.isabs(path) else R + path
    if not os.path.exists(pp): ause.append((onde, path)); continue
    if sha(pp) != s or (b is not None and isinstance(b, int) and os.path.getsize(pp) != b): mud.append((onde, path))
print("   ausentes no disco (nao e' erro se for artefato transitorio):", len(ause)); [print("     ", x) for x in ause[:12]]
chk("varredura geral: todo {path, sha256} existente == disco", not mud, mud[:12])
print("RESUMO falhas:", falhas)
json.dump({"ok": ok, "falhas": falhas, "cand_sha16": h[:16], "pares_varridos": len(acc), "ausentes": [list(x) for x in ause[:40]], "divergentes": [list(x) for x in mud[:40]]}, open(R + "revisao_terceiro/f_hashes_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
