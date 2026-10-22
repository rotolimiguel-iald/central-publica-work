# -*- coding: utf-8 -*-
"""testar_registros_v392.py -- roda o MOTOR dos registros v392 sobre os specs de V\\registros\\grupo_*.py (ou de um so': arg `--grupo <trecho do nome>`), com o core da v391 SELADA
(Nos\\um_absoluto.json) + um kernel SINTETICO (bandeiras e axiom_report lidos de kernel\\FLAGS_v392.json e kernel\\build_full.log, o que ja existir). Nao importa o um.py; nao escreve
nada alem de stdout (e `--json <arquivo>` opcional em V\\registros\\). Para cada registro: all_verified, falhas (checks/fontes/verbatins/kernel/guarda) e os valores `lido`.
Mostra tambem o CONTROLE NEGATIVO: com um sha de fonte adulterado, cada registro com fontes tem de recusar. Uso: python -B -X utf8 testar_registros_v392.py [--grupo G1] [--json saida.json] [--so-falhas]"""
import copy, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import montar_registros_v392 as M  # noqa: E402
import guarda_p18_v392 as G  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
args = sys.argv[1:]; filtro = args[args.index("--grupo") + 1] if "--grupo" in args else None
codigo, info = M.montar(filtro)
ns = {}
exec(compile(G.GUARDA_V392_SRC, "<guarda>", "exec"), ns)
exec(compile(codigo, "<pins>", "exec"), ns)
exec(compile(open(os.path.join(HERE, "registros_motor_v392.py"), encoding="utf-8").read(), "<motor>", "exec"), ns)
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
core = copy.deepcopy(core0); kf = core["kernel_formalization"]
KD = os.path.join(HERE, "kernel"); fj = os.path.join(KD, "FLAGS_v392.json"); lg = os.path.join(KD, "build_full.log"); sintetico = False
if os.path.exists(fj) and os.path.exists(lg):
    LOG = open(lg, encoding="utf-8", errors="replace").read(); AX = {}
    for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", LOG, re.S):
        AX[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
    for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", LOG):
        AX.setdefault(m.group(1), [])
    for f, n, mod, kind in json.load(open(fj, encoding="utf-8"))["flags"]:
        kf[f] = True; kf["axiom_report"][n] = AX.get(n, [])
    sintetico = True
    al = os.path.join(KD, "audit.log")
    if os.path.exists(al):   # a cobertura KH-N1 (a): o axiom_report EFETIVO do rito = o log inteiro do Audit; a checagem de cobertura roda a funcao do runtime
        blob = open(al, encoding="utf-8", errors="replace").read(); AXA = {}
        for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", blob, re.S):
            AXA[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
        for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", blob):
            AXA.setdefault(m.group(1), [])
        kf["axiom_report"].update(AXA)
        rt = open(os.path.join(HERE, "v392_runtime.py"), encoding="utf-8").read(); i0 = rt.index("def _v392_axiom_coverage")
        ns["_V392_KH"] = {"nao_lidas": 4, "decl_minimo": 20000}; exec(compile(rt[i0:], "<cov>", "exec"), ns)
        kf["axiom_coverage_v392"] = ns["_v392_axiom_coverage"](blob, kf["axiom_report"])
core.setdefault("pedras_v392", {"all_verified": True, "_stub": "harness: o ensaio roda o pedras_v392 de verdade"}); core.setdefault("varredura_e_sorry_v392", {"all_verified": True, "_stub": "harness"})
nomes = ns["_v392_rodar_registros"](core)
print("registros:", len(nomes), "| kernel sintetico:", sintetico, "| fontes:", info["n_fontes"], "| verbatins:", info["n_verbatins"])
res = {}; n_ok = 0
for n in nomes:
    r = core[n]; ok = r.get("all_verified") is True; n_ok += ok
    res[n] = {"all_verified": ok, "verdict": r.get("verdict"), "falhas": [c["descricao"] for c in r.get("checks", []) if not c["ok"]] + [f["chave"] for f in r.get("fontes", []) if not f["ok"]]
              + [k for k, v in r.get("verbatim", {}).items() if not v["embedded_ok"]] + (["kernel"] if r.get("kernel") and (r["kernel"]["bandeiras"][0] != r["kernel"]["bandeiras"][1] or r["kernel"]["declaracoes_no_trio"][0] != r["kernel"]["declaracoes_no_trio"][1]) else [])
              + ["guarda:" + str(r.get("guarda_p18_violacoes"))] * bool(r.get("guarda_p18_violacoes")) + (["ERRO:" + r.get("error", "")] if r.get("error") else []), "lido": r.get("lido", {})}
    if "--so-falhas" not in args or not ok:
        print(("OK    " if ok else "FALHA ") + n, "" if ok else res[n]["falhas"][:6])
# controle negativo: adulterar o sha de uma fonte => o registro que a usa recusa; adulterar um trecho do verbatim => recusa
neg = {}
for s in ns["_V392_SPECS"]:
    if s.get("fontes"):
        ch = s["fontes"][0]; antigo = dict(ns["_V392_FONTES"][ch]); ns["_V392_FONTES"][ch]["sha256"] = "0" * 64
        try:
            neg[s["nome"] + ":fonte"] = ns["_v392_registro"](s, core)["all_verified"] is False
        finally:
            ns["_V392_FONTES"][ch] = antigo
    if s.get("verbatins"):
        ch = s["verbatins"][0]; antigo = dict(ns["_V392_VERBATINS2"][ch]); ns["_V392_VERBATINS2"][ch]["text"] = antigo["text"] + " "
        try:
            neg[s["nome"] + ":verbatim"] = ns["_v392_registro"](s, core)["all_verified"] is False
        finally:
            ns["_V392_VERBATINS2"][ch] = antigo
print("sealed: %d de %d | controle negativo (adulterado => recusa): %d de %d" % (n_ok, len(nomes), sum(neg.values()), len(neg)))
if not all(neg.values()):
    print("CONTROLE NEGATIVO FALHOU em:", [k for k, v in neg.items() if not v])
if "--json" in args:
    json.dump({"registros": res, "controle_negativo": neg, "kernel_sintetico": sintetico}, open(os.path.join(HERE, "registros", args[args.index("--json") + 1]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.exit(0 if (n_ok == len(nomes) and all(neg.values())) else 1)
