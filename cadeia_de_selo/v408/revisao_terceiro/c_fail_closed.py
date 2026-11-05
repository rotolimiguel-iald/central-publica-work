# -*- coding: utf-8 -*-
"""Revisor terceiro v408 (R1): importa o CANDIDATO (sem executar o main) e testa, sobre o core do ensaio a seco (dry_v408/core_ensaio.json), que tetelestai_terminal_v408 e' fail-closed:
nega UMA condicao por vez e confere que o registro RECUSA (all_verified False, veredito de recusa) e que a base sela. Confere que cada uma das 16 checagens reprova quando a sua condicao e' negada
(i.e. le o kernel/o core e nao um literal). Nao escreve nada fora desta pasta."""
import copy, hashlib, importlib.util, json, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v408/"
t0 = time.time()
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v408_candidato.py")
m = importlib.util.module_from_spec(spec)
sys.modules["um_cand_rev"] = m
spec.loader.exec_module(m)
print("import ok", round(time.time() - t0, 1), "s;  UM_VERSION", m.UM_VERSION)
core0 = json.load(open(R + "dry_v408/core_ensaio.json", encoding="utf-8"))["core"]
kf0 = core0["kernel_formalization"]
C = m._V408_TERMINAL_CONTRACT
F = m.tetelestai_terminal_v408
res = {}


def f(nome_, core, quer_ok, ids_que_devem_reprovar=None):
    c = copy.deepcopy(core)
    try:
        r = F(c)
    except Exception as e:   # noqa: BLE001
        res[nome_] = {"excecao": repr(e)[:200], "esperado_ok": quer_ok, "ok": False}
        print("EXCECAO", nome_, repr(e)[:200]); return None
    v = r["verdict"]; ok_ = v.startswith("TGL_TETELESTAI_TERMINAL_V408__THE_TERMINAL_IS_THE_READING") and r["all_verified"] is True
    certo = (ok_ is quer_ok)
    falhos = [c_["id"] for c_ in (r.get("mechanics") or {}).get("checks", []) if not c_["ok"]]
    if ids_que_devem_reprovar is not None:
        recusa_formal = v.startswith("TGL_TETELESTAI_TERMINAL_V408__REFUSED_FORMAL_OR_SOURCE_EVIDENCE")   # recusada ANTES das 16 checagens: tambem e' fail-closed
        certo = certo and (recusa_formal or all(i in falhos for i in ids_que_devem_reprovar))
    res[nome_] = {"verdict": v[:100], "all_verified": r["all_verified"], "esperado_ok": quer_ok, "checks_falhos": falhos, "ok": certo}
    print(("OK   " if certo else "FALHA"), nome_, "->", v[:90], r["all_verified"], falhos)
    return r


r0 = f("base", core0, True)
print("   checks:", [(c_["id"], c_["ok"]) for c_ in r0["mechanics"]["checks"]])
print("   n_ancoras_ok", r0["values"]["n_ancoras_ok"], "/", r0["values"]["n_ancoras"], "n_modulos_ok", r0["values"]["n_modulos_ok"], "n_flags_true", r0["values"]["n_flags_true"], "escada", r0["values"]["escada"], "respostas_ok", r0["values"]["respostas_ok"])
print("   keys:", sorted(r0.keys()))
# ---- as 42 ancoras: ausente
for anc in C["ancoras"]:
    c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"].pop(anc, None); f("ancora ausente: " + anc.split("TGLExt.")[-1], c, False, ["c1"])
for anc in C["ancoras_principais"]:
    c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"][anc] = ["propext", "sorryAx"]; f("ancora com sorryAx: " + anc.split("TGLExt.")[-1], c, False, ["c1"])
    c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"][anc] = ["Lean.ofReduceBool"]; f("ancora com ofReduceBool: " + anc.split("TGLExt.")[-1], c, False)
    c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"][anc] = []; f("ancora com axiom list vazia: " + anc.split("TGLExt.")[-1], c, False, ["c1"])
    c = copy.deepcopy(core0); c["kernel_formalization"]["declaration_sources_v394"][anc] = "x.lean"; f("proveniencia errada: " + anc.split("TGLExt.")[-1], c, False, ["c1"])
    fl = C["ancoras"][anc]["flag"]; c = copy.deepcopy(core0); c["kernel_formalization"][fl] = False; f("bandeira False: " + anc.split("TGLExt.")[-1], c, False, ["c1"])
c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"][C["ancora_principal"]] = "propext"; f("axiom nao-lista", c, False)
# ---- a ultima ancora (card/classes), por seguranca: todas as 42 com sorryAx
n_rej = 0
for anc in C["ancoras"]:
    c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"][anc] = ["propext", "sorryAx"]
    r = F(c); n_rej += (r["all_verified"] is False)
print("42 ancoras, uma por vez com sorryAx: recusadas", n_rej, "de", len(C["ancoras"])); res["42 ancoras com sorryAx recusadas"] = {"n": n_rej, "ok": n_rej == len(C["ancoras"])}
n_rej = 0
for fl in C["flags"]:
    c = copy.deepcopy(core0); c["kernel_formalization"][fl] = False
    r = F(c); n_rej += (r["all_verified"] is False)
print("44 bandeiras, uma por vez False: recusadas", n_rej, "de", len(C["flags"])); res["44 bandeiras False recusadas"] = {"n": n_rej, "ok": n_rej == len(C["flags"])}
n_rej = 0
for fl in C["flags"]:
    c = copy.deepcopy(core0); c["kernel_formalization"].pop(fl, None)
    r = F(c); n_rej += (r["all_verified"] is False)
print("44 bandeiras, uma por vez AUSENTE: recusadas", n_rej, "de", len(C["flags"])); res["44 bandeiras ausentes recusadas"] = {"n": n_rej, "ok": n_rej == len(C["flags"])}
# ---- as fontes
for r_ in C["source_sha256"]:
    c = copy.deepcopy(core0); c["kernel_formalization"]["formal_files_sha256"][r_] = "1" * 64; f("sha256 formal errado: " + r_.split("/")[-1], c, False)
    c = copy.deepcopy(core0); c["kernel_formalization"]["formal_files_sha256"].pop(r_); f("sha256 formal ausente: " + r_.split("/")[-1], c, False)
    orig = m._EMBEDDED_KERNEL_FILES[r_]
    m._EMBEDDED_KERNEL_FILES[r_] = orig + "\n-- adulterado"; f("fonte EMBUTIDA adulterada: " + r_.split("/")[-1], core0, False)
    del m._EMBEDDED_KERNEL_FILES[r_]; f("fonte EMBUTIDA ausente: " + r_.split("/")[-1], core0, False)
    m._EMBEDDED_KERNEL_FILES[r_] = orig
raiz0 = m._EMBEDDED_KERNEL_FILES["TGLExt.lean"]
for nm in ("PIgualNP", "TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao"):
    m._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = raiz0.replace("import TGLExt.%s\n" % nm, "").replace("import TGLExt.%s\r\n" % nm, "")
    f("raiz embutida sem o import %s" % nm, core0, False, ["c2"])
m._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = raiz0
# ---- escada, gate, kernel
c = copy.deepcopy(core0); c["external_ladder"]["n_theorems_clean"] = 12001; f("escada 12001", c, False, ["c13"])
c = copy.deepcopy(core0); c["external_ladder"]["n_theorems_expected"] = 11958; f("escada esperada 11958 (a da v407)", c, False, ["c13"])
c = copy.deepcopy(core0); c["external_ladder"]["n_theorems_clean"] = "12002"; f("escada string", c, False, ["c13"])
c = copy.deepcopy(core0); c["qg_closure"]["gate"]["verdict"] = "OUTRO"; f("gate com outro veredito", c, False, ["c12"])
c = copy.deepcopy(core0); del c["qg_closure"]; f("qg_closure ausente", c, False, ["c12"])
c = copy.deepcopy(core0); c["kernel_formalization"]["all_verified"] = False; f("kernel recusado (all_verified False)", c, False)
c = copy.deepcopy(core0); del c["kernel_formalization"]["all_verified"]; f("kernel sem all_verified", c, False)
c = copy.deepcopy(core0); c["kernel_formalization"]["all_verified"] = "True"; f("all_verified string", c, False)
f("core vazio", {}, False)
# ---- beta
c = copy.deepcopy(core0); c["beta"] = c["beta"] * 1.001; f("beta do core divergente", c, False)
c = copy.deepcopy(core0); c.pop("beta"); f("beta do core ausente", c, False)
# ---- contrato: sha do contrato errado, bandeira/numero errado
sv = m._V408_TERMINAL_CONTRACT
c2 = copy.deepcopy(sv); c2["source_sha256"]["TGLExt/PIgualNP.lean"] = "0" * 64; m._V408_TERMINAL_CONTRACT = c2; f("contrato: sha256 do PIgualNP errado", core0, False)
c2 = copy.deepcopy(sv); c2["expected_ladder"] = 12001; m._V408_TERMINAL_CONTRACT = c2; f("contrato: escada 12001", core0, False, ["c13"])
c2 = copy.deepcopy(sv); c2["baseline"]["gate_verdict"] = "OUTRO"; m._V408_TERMINAL_CONTRACT = c2; f("contrato: baseline do gate diferente", core0, False, ["c12"])
c2 = copy.deepcopy(sv); c2["insumo_purgado"]["sha256"] = "2" * 64; m._V408_TERMINAL_CONTRACT = c2; f("contrato: sha256 do insumo purgado errado", core0, False, ["c15"])
c2 = copy.deepcopy(sv); c2["insumo_purgado"]["integra_pinada"] = True; m._V408_TERMINAL_CONTRACT = c2; f("contrato: integra do acervo marcada como pinada", core0, False, ["c15"])
m._V408_TERMINAL_CONTRACT = sv
f("restaurado", core0, True)
# ---- respostas do operador: tira um teorema que ja' existia
for r_ in C["respostas"]:
    for t_ in r_["teoremas"]:
        c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"].pop(t_["completo"]); f("resposta %s: teorema %s ausente" % (r_["id"], t_["curto"]), c, False)
# ---- falas do operador adulteradas
ver = m._V408_VERBATINS2
k0 = [k for k in ver if k in C["verbatins"]][0]; sv_t = ver[k0]["text"]; ver[k0]["text"] = sv_t + " x"; f("fala do operador adulterada (sha256 difere)", core0, False); ver[k0]["text"] = sv_t
n = 0
for k in C["verbatins"]:
    sv_t = ver[k]["text"]; ver[k]["text"] = sv_t + " "; r = F(copy.deepcopy(core0)); n += (r["all_verified"] is False); ver[k]["text"] = sv_t
print("15 falas, uma por vez adulterada: recusadas", n, "de", len(C["verbatins"])); res["falas adulteradas recusadas"] = {"n": n, "ok": n == len(C["verbatins"])}
# ---- texto do registro com frase proibida => c14 e recusa
tx = m._V408_TERMINAL_TEXT; sv_d = list(tx["diz"])
for frase in ("a TGL prova P = NP de Turing (Cook-Levin)", "P = NP está provado", "a TGL não tem terminal", "há relação sem peso", "o que resta sem peso é relação"):
    tx["diz"] = sv_d + [frase]; f("texto com frase proibida: %s" % frase, core0, False, ["c14"])
tx["diz"] = sv_d
# P = nP sem a ressalva [OPEN] (F34)
tx["diz"] = sv_d + ["P = nP é teorema, ponto"]; f("texto com 'P = nP' sem qualificador/ressalva (F34)", core0, False, ["c14"])
tx["diz"] = sv_d
# ---- insumo purgado trocado no disco: simula leitura falhando
sv_fn = m._v392_fonte_bytes
m._v392_fonte_bytes = lambda k: (False, "SHA256_DIFERE", b"")
f("insumo purgado: leitura/sha256 falha", core0, False, ["c15"])
m._v392_fonte_bytes = sv_fn
f("restaurado 2", core0, True)
# ---- guarda de frases: positivos e negativos (pedido item 4)
G = m._v408_guarda_frases
casos = [
    ("a TGL prova P = NP de Turing (Cook–Levin)", True), ("A TGL decide P = NP das máquinas de Turing (Cook–Levin)", True), ("provamos que P = NP de Turing", True),
    ("P = NP está provado", True), ("P = NP é teorema", True), ("a igualdade das classes P e NP segue podada", True), ("P = nP não trata das classes", True), ("este P=nP não trata de classes", True),
    ("a TGL não tem terminal", True), ("a TGL has no terminal", True), ("a impedância é um termo do kernel", True), ("há relação sem peso", True), ("relação sem peso existe", True), ("there is a relation without weight", True),
    ("o que resta sem peso é relação", True), ("TERMINAL_CONF" + "IRMED", True), ("P_EQUALS_NP", True), ("tudo derivado", True), ("nenhuma hipótese resta", True), ("é uma pós-dição", True),
    ("PRO" + "VED_BY x", True), ("a luz conf" + "irma a teoria", True),
    ("P = nP é teorema nas classes de computação do dicionário do operador (definidas e provadas na pedra PIgualNP); a tradução para as classes das máquinas de Turing, onde o tamanho se conta em bits = log₂ n, não está no kernel: é a próxima construção, [OPEN], não uma recusa", False),
    ("«P = nP» só no sentido do operador", True),
    ("P = nP é teorema nas classes de computação do dicionário do operador", True),
    ("não há relação sem peso", False), ("there is no relation without weight", False), ("relação sem peso é impossível", False),
    ("o terminal é a leitura, não o fim do decaimento", False), ("a TGL tem terminal: Tetelestai, a poda", False), ("a palavra «impedância» fica podada como termo", False),
]
for frase, deve in casos:
    g = G(frase)
    from_p18 = m._v392_guarda_texto(frase)
    reprovou = bool(g) or bool(from_p18)
    print("guarda:", repr(frase[:80]), "->", [x[0] for x in (g + from_p18)][:3], "(esperado reprovar)" if deve else "(esperado passar)")
    res["guarda: " + frase[:90]] = {"reprovou": reprovou, "esperado": deve, "ok": reprovou == deve}
n_ok = sum(1 for v in res.values() if v.get("ok") is True); n_f = sum(1 for v in res.values() if v.get("ok") is False)
print("RESUMO: ok", n_ok, "falha", n_f)
for k, v in res.items():
    if v.get("ok") is False: print("  FALHOU:", k, v)
json.dump(res, open(R + "revisao_terceiro/c_fail_closed_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
