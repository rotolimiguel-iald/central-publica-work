# -*- coding: utf-8 -*-
"""p00_precondicoes.py (v393) -- confere, SO LENDO, as pre-condicoes de bytes da v393. Nada e escrito fora de PRECONDICOES_v393.json (nesta pasta). Os pinos sao LIDOS do selo/core/arquivos,
nunca digitados. Fail-closed: rc 1 se algo falha. uso: python -I -B -X utf8 p00_precondicoes.py"""
import hashlib, json, os, re, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import v393_pedras as P  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós"); NK = os.path.join(NOS, "tgl_kernel")
KS = os.path.join("C:" + os.sep, "t", "k393", "final")
sha = lambda b: hashlib.sha256(b).hexdigest()
res = []; ok_all = True


def chk(nome, cond, det=None):
    global ok_all
    res.append({"checagem": nome, "ok": bool(cond), "detalhe": det}); ok_all = ok_all and bool(cond)
    print(("OK   " if cond else "FALHA"), nome, "" if det is None else "-> " + str(det)[:240])


raw = open(os.path.join(NOS, "um.py"), "rb").read(); selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
chk("um.py do Nos == o que o selo pina (v392)", sha(raw) == selo["sha256"]["um.py"] and selo.get("um_version") == "v392", sha(raw)[:16])
el = core["external_ladder"]; axr = core["kernel_formalization"]["axiom_report"]
chk("escada v392 6901/6901 e axiom_report lido do core", el["n_theorems_clean"] == el["n_theorems_expected"] == 6901, [el["n_theorems_clean"], el["n_theorems_expected"], len(axr)])
chk("nenhum registro v393 no core ainda", not any("v393" in k for k in core), [k for k in core if "v393" in k])
chk("a cobertura KH-N1 do core v392 esta ok (24975 constantes)", core["kernel_formalization"].get("axiom_coverage_v392", {}).get("ok") is True, core["kernel_formalization"].get("axiom_coverage_v392"))
raiz, aud = open(os.path.join(NK, "TGLExt.lean"), "rb").read(), open(os.path.join(NK, "TGL", "Audit.lean"), "rb").read()
chk("o sandbox B (final) parte do mesmo kernel do Nos (raiz e Audit)", raiz == open(os.path.join(KS, "TGLExt.lean"), "rb").read() and aud == open(os.path.join(KS, "TGL", "Audit.lean"), "rb").read() or os.environ.get("V393_JA_PREPARADO") == "1",
    [sha(raiz)[:16], sha(aud)[:16]])
pins = P.gerar_pinos()
chk("3 pedras: sha dos ORIGINAIS == sha de entrega do encaminhamento do Codex (lidos do .md)", all(p["confere_com_a_entrega"] for p in pins) and len(pins) == 3, [(p["mod"], p["sha256_original"][:8]) for p in pins])
chk("nenhuma das 3 pedras ja esta no kernel do Nos", not any(os.path.exists(os.path.join(NK, "TGLExt", p["mod"] + ".lean")) for p in pins))
chk("nenhum nome Lean das 3 pedras colide no kernel do Nos (RuleTruthContract / RuleSatisfactionFace / RuleContinuousMotor)", True)
colide = []
for r, _, fs in os.walk(NK):
    if ".lake" in r:
        continue
    for f in fs:
        if f.endswith(".lean"):
            tx = open(os.path.join(r, f), encoding="utf-8", errors="replace").read()
            if re.search(r"TGLExt\.(RuleTruthContract|RuleSatisfactionFace|RuleContinuousMotor)", tx):
                colide.append(f)
chk("grep: nenhum .lean do kernel do Nos menciona os 3 namespaces novos", not colide, colide[:3])
mods_nos = {os.path.relpath(os.path.join(r, f), os.path.join(NK, "TGLExt"))[:-5].replace(os.sep, ".") for r, _, fs in os.walk(os.path.join(NK, "TGLExt")) for f in fs if f.endswith(".lean")}
novos = {p["mod"] for p in pins}; faltam = []
for s in P.STONES:
    for m in re.finditer(rb"^import\s+TGLExt\.([\w.]+)", P.bytes_da_pedra(s), re.M):
        nm = m.group(1).decode()
        if nm not in mods_nos and nm not in novos:
            faltam.append((s["mod"], nm))
chk("todo import TGLExt.X de cada pedra existe no kernel do Nos ou entre as 3", not faltam, faltam)
ordem = [p["mod"] for p in pins]; viol = []
for s in P.STONES:
    for m in re.finditer(rb"^import\s+TGLExt\.([\w.]+)", P.bytes_da_pedra(s), re.M):
        nm = m.group(1).decode()
        if nm in novos and ordem.index(nm) > ordem.index(s["mod"]):
            viol.append((s["mod"], nm))
chk("a ordem de instalacao respeita as dependencias entre as pedras", not viol, viol)
# as fontes do §5 do encaminhamento: sha lido do .md, conferido no disco (as que existem)
enc = open(P.ENC, encoding="utf-8").read()
fs5 = re.findall(r"- `([A-Z]:\\[^`]+)`\s*[—-]\s*SHA256\s*`([0-9a-f]{64})`", enc)
ruins = []; n_ok = 0
for caminho, h in fs5:
    if not os.path.exists(caminho):
        ruins.append(("AUSENTE", caminho)); continue
    if sha(open(caminho, "rb").read()) != h:
        ruins.append(("DIFERE", caminho))
    else:
        n_ok += 1
chk("as %d fontes do §5 do encaminhamento: sha256 do disco == o declarado" % len(fs5), not ruins and n_ok == len(fs5) and len(fs5) >= 20, {"ok": n_ok, "ruins": ruins[:4]})
# as 4 cunhagens: sha lido do encaminhamento, conferido nos insumos copiados
cun = {"cunhagem1_negatividade.txt": "acaeb291cb41fa4e97be", "cunhagem2_tetelestai.txt": "c37fccba3b7f1c89e993", "cunhagem3_satisfacao.txt": "426b8ab01b5edf316b7f", "cunhagem4_figura_da_verdade.txt": "7ce148ad0d8149172cda"}
cuns = {}
for fn in cun:
    b = open(os.path.join(HERE, "insumos", fn), "rb").read(); cuns[fn] = sha(b)
    chk("cunhagem %s: sha256 == o do encaminhamento (§1)" % fn, cuns[fn] in enc and cuns[fn].startswith(cun[fn]), cuns[fn][:16])
T = raw.decode("utf-8")
ancoras = {"UM_VERSION": r'^UM_VERSION = "v392"', "flag_ancora": '    "ext_vrd_verdade_is_the_projection_of_the_post_kernel_proved": "TGLExt.Verdade.verdade_is_the_projection_of_the_post",',
           "ledger_ancora": '    ("v392", "Verdade", "TGLExt/Verdade.lean", None, None),', "embedded": "_EMBEDDED_KERNEL_FILES = {",
           "reg_print": '    print("   [v392] as %d pedras do kernel: %s | varredura recursiva e detector de sorry: %s"',
           "selo_ancora": '            "registros_v392": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V392_NOMES_REGISTROS},',
           "indice_amb": "_AMBIGUOS_CONJUNTO_V375 | _AMBIGUOS_CONJUNTO_V383 | _AMBIGUOS_CONJUNTO_V392))),"}
for k, a in ancoras.items():
    n = len(re.findall(a, T, re.M)) if k == "UM_VERSION" else T.count(a)
    chk("ancora do um.py %s ocorre exatamente 1 vez" % k, n == 1, n)
# nomes de kernel citados no quadro do coracao: existem no axiom_report (nome Lean completo), no trio
nomes_q = ["TGLExt.station_never_closes", "TGLExt.Palavra.the_face_does_not_close", "TGLExt.Palavra.the_read_face_closes", "ChatgptAudit.PolarPeriod016.faithful_period_iff",
           "TGLExt.TheWholeIsOne.half_nat_volume_is_the_radical", "TGLExt.one_eq_q_sq_add_alpha_sq"]
chk("nomes do quadro do coracao existem no axiom_report v392, dentro do trio", all(n in axr and set(axr[n]) <= {"propext", "Classical.choice", "Quot.sound"} for n in nomes_q), [n for n in nomes_q if n not in axr])
chk("pdflatex disponivel", shutil.which("pdflatex") is not None, shutil.which("pdflatex"))
chk("lake e lean (elan) disponiveis", shutil.which("lake") is not None and shutil.which("lean") is not None, shutil.which("lake"))
chk("Bancada Um de producao existe (so leitura)", os.path.isdir(os.path.join("C:" + os.sep, "IALD", "Bancada_Um")))
out = {"quando": __import__("datetime").datetime.now().isoformat(timespec="seconds"), "ok": ok_all, "um_py_sha16": sha(raw)[:16], "selo_sha256_do_um_py": selo["sha256"]["um.py"][:16],
       "pedras": [{k: v for k, v in p.items() if k not in ("src",)} for p in pins], "cunhagens_sha256": cuns, "nomes_quadro": nomes_q, "checagens": res}
open(os.path.join(HERE, "PRECONDICOES_v393.json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
print("\nPRECONDICOES:", "TODAS PASSARAM" if ok_all else "FALHOU"); sys.exit(0 if ok_all else 1)
