# -*- coding: utf-8 -*-
"""Revisor terceiro v409 (R1): importa o CANDIDATO (sem executar o main) e testa, sobre o core do ensaio a seco (dry_v409/core_ensaio.json), que traducao_turing_v409 e' fail-closed:
nega UMA condicao por vez e confere que o registro RECUSA (all_verified False, veredito de recusa). Confere que cada uma das 20 checagens reprova quando a sua condicao e' negada
(i.e. le o kernel/o core/o contrato e nao um literal) e como a guarda das frases (F35-F43) se comporta em positivos e negativos. Nao escreve nada fora desta pasta."""
import copy, hashlib, importlib.util, json, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
t0 = time.time()
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v409_candidato.py")
m = importlib.util.module_from_spec(spec)
sys.modules["um_cand_rev"] = m
spec.loader.exec_module(m)
print("import ok", round(time.time() - t0, 1), "s;  UM_VERSION", m.UM_VERSION)
core0 = json.load(open(R + "dry_v409/core_ensaio.json", encoding="utf-8"))["core"]
kf0 = core0["kernel_formalization"]
C = m._V409_TRADUCAO_CONTRACT
F = m.traducao_turing_v409
OKV = "TGL_TRADUCAO_TURING_V409__THE_DICTIONARY_REACHES_TURING_RELATIVE_TO_THE_READER"
REFV = "TGL_TRADUCAO_TURING_V409__REFUSED_FORMAL_OR_SOURCE_EVIDENCE"
res = {}


def f(nome_, core, quer_ok, ids_que_devem_reprovar=None):
    c = copy.deepcopy(core)
    try:
        r = F(c)
    except Exception as e:   # noqa: BLE001
        res[nome_] = {"excecao": repr(e)[:200], "esperado_ok": quer_ok, "ok": False}
        print("EXCECAO", nome_, repr(e)[:200]); return None
    v = r["verdict"]; ok_ = v.startswith(OKV) and r["all_verified"] is True
    certo = (ok_ is quer_ok)
    falhos = [c_["id"] for c_ in (r.get("mechanics") or {}).get("checks", []) if not c_["ok"]]
    if ids_que_devem_reprovar is not None:
        recusa_formal = v.startswith(REFV)   # recusada ANTES das checagens: tambem e' fail-closed
        certo = certo and (recusa_formal or all(i in falhos for i in ids_que_devem_reprovar))
    res[nome_] = {"verdict": v[:100], "all_verified": r["all_verified"], "esperado_ok": quer_ok, "checks_falhos": falhos, "ok": certo}
    print(("OK   " if certo else "FALHA"), nome_, "->", v[:90], r["all_verified"], falhos)
    return r


r0 = f("base", core0, True)
print("   checks:", [(c_["id"], c_["ok"]) for c_ in r0["mechanics"]["checks"]])
print("   n_ancoras_ok", r0["values"]["n_ancoras_ok"], "/", r0["values"]["n_ancoras"], "n_modulos_ok", r0["values"]["n_modulos_ok"], "n_flags_true", r0["values"]["n_flags_true"], "escada", r0["values"]["escada"], "respostas_ok", r0["values"]["respostas_ok"])
print("   keys:", sorted(r0.keys()))
print("   contrato: n_ancoras", len(C["ancoras"]), "n_flags", len(C["flags"]), "modulos", list(C["source_sha256"]), "verbatins", len(C["verbatins"]), "expected_ladder", C["expected_ladder"])
# ---- as 82 ancoras: ausente (todas) e as principais com variantes
n_rej = 0
for anc in C["ancoras"]:
    c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"].pop(anc, None); r = F(c); n_rej += (r["all_verified"] is False)
print("82 ancoras, uma por vez AUSENTE do axiom_report: recusadas", n_rej, "de", len(C["ancoras"])); res["82 ancoras ausentes recusadas"] = {"n": n_rej, "ok": n_rej == len(C["ancoras"]) == 82}
n_rej = 0
for anc in C["ancoras"]:
    c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"][anc] = ["propext", "sorryAx"]; r = F(c); n_rej += (r["all_verified"] is False)
print("82 ancoras, uma por vez com sorryAx: recusadas", n_rej, "de", len(C["ancoras"])); res["82 ancoras com sorryAx recusadas"] = {"n": n_rej, "ok": n_rej == len(C["ancoras"])}
n_rej = 0
for anc in C["ancoras"]:
    c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"][anc] = ["Lean.ofReduceBool"]; r = F(c); n_rej += (r["all_verified"] is False)
print("82 ancoras, uma por vez com ofReduceBool: recusadas", n_rej, "de", len(C["ancoras"])); res["82 ancoras com ofReduceBool recusadas"] = {"n": n_rej, "ok": n_rej == len(C["ancoras"])}
n_rej = 0
for anc in C["ancoras"]:
    c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"][anc] = []; r = F(c); n_rej += (r["all_verified"] is False)
print("82 ancoras, uma por vez com lista vazia: recusadas", n_rej, "de", len(C["ancoras"])); res["82 ancoras lista vazia recusadas"] = {"n": n_rej, "ok": n_rej == len(C["ancoras"])}
n_rej = 0
for anc in C["ancoras"]:
    c = copy.deepcopy(core0); c["kernel_formalization"]["declaration_sources_v394"][anc] = "x.lean"; r = F(c); n_rej += (r["all_verified"] is False)
print("82 ancoras, proveniencia errada: recusadas", n_rej, "de", len(C["ancoras"])); res["82 ancoras proveniencia errada recusadas"] = {"n": n_rej, "ok": n_rej == len(C["ancoras"])}
n_rej = 0; n_com_flag = 0
for anc, a in C["ancoras"].items():
    if a.get("flag"):
        n_com_flag += 1
        c = copy.deepcopy(core0); c["kernel_formalization"][a["flag"]] = False; r = F(c); n_rej += (r["all_verified"] is False)
print("ancoras com bandeira (%d), bandeira False uma por vez: recusadas" % n_com_flag, n_rej); res["ancoras com bandeira False recusadas"] = {"n": n_rej, "ok": n_rej == n_com_flag}
c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"][C["ancora_principal"]] = "propext"; f("axiom nao-lista", c, False)
# o trio subconjunto: custoCNF_cons so' propext e' ACEITO (subconjunto do trio)
c = copy.deepcopy(core0); print("   custoCNF_cons axiomas no core:", c["kernel_formalization"]["axiom_report"].get("TGLExt.TraducaoTuring.custoCNF_cons"))
n_rej = 0
for fl in C["flags"]:
    c = copy.deepcopy(core0); c["kernel_formalization"][fl] = False; r = F(c); n_rej += (r["all_verified"] is False)
print("158 bandeiras, uma por vez False: recusadas", n_rej, "de", len(C["flags"])); res["158 bandeiras False recusadas"] = {"n": n_rej, "ok": n_rej == len(C["flags"])}
n_rej = 0
for fl in C["flags"]:
    c = copy.deepcopy(core0); c["kernel_formalization"].pop(fl, None); r = F(c); n_rej += (r["all_verified"] is False)
print("158 bandeiras, uma por vez AUSENTE: recusadas", n_rej, "de", len(C["flags"])); res["158 bandeiras ausentes recusadas"] = {"n": n_rej, "ok": n_rej == len(C["flags"])}
# ---- as fontes
for r_ in C["source_sha256"]:
    c = copy.deepcopy(core0); c["kernel_formalization"]["formal_files_sha256"][r_] = "1" * 64; f("sha256 formal errado: " + r_.split("/")[-1], c, False)
    c = copy.deepcopy(core0); c["kernel_formalization"]["formal_files_sha256"].pop(r_); f("sha256 formal ausente: " + r_.split("/")[-1], c, False)
    orig = m._EMBEDDED_KERNEL_FILES[r_]
    m._EMBEDDED_KERNEL_FILES[r_] = orig + "\n-- adulterado"; f("fonte EMBUTIDA adulterada: " + r_.split("/")[-1], core0, False)
    del m._EMBEDDED_KERNEL_FILES[r_]; f("fonte EMBUTIDA ausente: " + r_.split("/")[-1], core0, False)
    m._EMBEDDED_KERNEL_FILES[r_] = orig
raiz0 = m._EMBEDDED_KERNEL_FILES["TGLExt.lean"]
for nm in ("TraducaoTuring", "ParNaFaceDeFock"):
    m._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = raiz0.replace("import TGLExt.%s\n" % nm, "").replace("import TGLExt.%s\r\n" % nm, "")
    f("raiz embutida sem o import %s" % nm, core0, False, ["c2"])
m._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = raiz0
# ---- escada, gate, kernel
c = copy.deepcopy(core0); c["external_ladder"]["n_theorems_clean"] = 12186; f("escada 12186", c, False, ["c15"])
c = copy.deepcopy(core0); c["external_ladder"]["n_theorems_expected"] = 12029; f("escada esperada 12029 (a da v408)", c, False, ["c15"])
c = copy.deepcopy(core0); c["external_ladder"]["n_theorems_clean"] = "12187"; f("escada string", c, False, ["c15"])
c = copy.deepcopy(core0); c["qg_closure"]["gate"]["verdict"] = "OUTRO"; f("gate com outro veredito", c, False, ["c14"])
c = copy.deepcopy(core0); del c["qg_closure"]; f("qg_closure ausente", c, False, ["c14"])
c = copy.deepcopy(core0); c["kernel_formalization"]["all_verified"] = False; f("kernel recusado (all_verified False)", c, False)
c = copy.deepcopy(core0); del c["kernel_formalization"]["all_verified"]; f("kernel sem all_verified", c, False)
c = copy.deepcopy(core0); c["kernel_formalization"]["all_verified"] = "True"; f("all_verified string", c, False)
f("core vazio", {}, False)
# ---- beta
c = copy.deepcopy(core0); c["beta"] = c["beta"] * 1.001; f("beta do core divergente", c, False)
c = copy.deepcopy(core0); c.pop("beta"); f("beta do core ausente", c, False)
# ---- contrato: mutacoes
sv = m._V409_TRADUCAO_CONTRACT


def mut(nome_, fn, quer_ids=None, quer_ok=False):
    c2 = copy.deepcopy(sv); fn(c2); m._V409_TRADUCAO_CONTRACT = c2
    try: f(nome_, core0, quer_ok, quer_ids)
    finally: m._V409_TRADUCAO_CONTRACT = sv


mut("contrato: sha256 do TraducaoTuring errado", lambda c_: c_["source_sha256"].__setitem__("TGLExt/TraducaoTuring.lean", "0" * 64))
mut("contrato: sha256 do ParNaFaceDeFock errado", lambda c_: c_["source_sha256"].__setitem__("TGLExt/ParNaFaceDeFock.lean", "0" * 64))
mut("contrato: escada 12186", lambda c_: c_.__setitem__("expected_ladder", 12186), ["c15"])
mut("contrato: baseline do gate diferente", lambda c_: c_["baseline"].__setitem__("gate_verdict", "OUTRO"), ["c14"])
mut("contrato: n_ancoras 81", lambda c_: c_.__setitem__("n_ancoras", 81), ["c1"])
mut("contrato: n_flags 157", lambda c_: c_.__setitem__("n_flags", 157), ["c15"])
mut("contrato: ancora_por_modulo vazia", lambda c_: c_["ancoras_por_modulo"].__setitem__("TGLExt/ParNaFaceDeFock.lean", []), ["c1"])
# c20: instancia SIM trocada por uma insatisfazivel: a leitura nao decide mais SAT na SIM
mut("contrato: instancia SIM insatisfazivel (c4/c20)", lambda c_: c_["instancia_sim"].__setitem__("clausulas", [[1], [-1], [2]]), ["c4", "c20"])
mut("contrato: instancia NAO satisfazivel (c10/c20)", lambda c_: c_["instancia_nao"].__setitem__("clausulas", [[1]]), ["c10", "c20"])
mut("contrato: inscricao s vazio (c19)", lambda c_: c_["inscricao_brinquedo"].__setitem__("s", []), ["c19"])
m._V409_TRADUCAO_CONTRACT = sv
f("restaurado", core0, True)
# ---- respostas do operador: tira um teorema que ja' existia
for r_ in C["respostas"]:
    for t_ in r_["teoremas"]:
        c = copy.deepcopy(core0); c["kernel_formalization"]["axiom_report"].pop(t_["completo"]); f("resposta %s: teorema %s ausente" % (r_["id"], t_["curto"]), c, False)
# ---- falas do operador adulteradas
ver = m._V409_VERBATINS2
n = 0
for k in C["verbatins"]:
    sv_t = ver[k]["text"]; ver[k]["text"] = sv_t + " "; r = F(copy.deepcopy(core0)); n += (r["all_verified"] is False); ver[k]["text"] = sv_t
print("14 falas, uma por vez adulterada: recusadas", n, "de", len(C["verbatins"])); res["falas adulteradas recusadas"] = {"n": n, "ok": n == len(C["verbatins"]) == 14}
n = 0
for k in C["verbatins"]:
    tr_ = ver[k]["trechos"]; ver[k]["trechos"] = list(tr_) + ["trecho que nao esta na fala"]; r = F(copy.deepcopy(core0)); n += (r["all_verified"] is False); ver[k]["trechos"] = tr_
print("14 falas, um trecho inexistente acrescentado: recusadas", n); res["falas com trecho inexistente recusadas"] = {"n": n, "ok": n == len(C["verbatins"])}
# ---- texto do registro com frase proibida => c16 e recusa
tx = m._V409_TRADUCAO_TEXT; sv_d = list(tx["diz"])
for frase in ("a TGL prova P = NP de Turing (Cook-Levin)", "P = NP está provado", "a TGL resolve o problema do milênio", "o problema do Clay está resolvido", "a TGL não tem terminal", "há relação sem peso", "TURING_SOLVED",
              "Ω é o uniforme da instância", "o par na face de Fock segue [OPEN]", "isso passa à v410"):
    tx["diz"] = sv_d + [frase]; f("texto com frase proibida: %s" % frase, core0, False, ["c16"])
tx["diz"] = sv_d
tx["diz"] = sv_d + ["P = nP é teorema, ponto"]; f("texto com 'P = nP' sem Turing (F37 nao se aplica; so' P18?)", core0, None if False else True)   # informativo: nao e' obrigatorio reprovar
tx["diz"] = sv_d + ["P = nP é teorema, e a máquina de Turing decide"]; f("texto com 'P = nP' e Turing sem o qualificador local (F37b)", core0, False, ["c16"])
tx["diz"] = sv_d
f("restaurado 2", core0, True)
# ---- guarda de frases: positivos e negativos
G = m._v409_guarda_frases
E28 = "com o leitor que só conta, NP contido em P numa só leitura; a igualdade completa só para o leitor que se lê (E28)"
casos = [
    ("a TGL prova P = NP de Turing (Cook–Levin)", True), ("A TGL decide P = NP das máquinas de Turing", True), ("P = NP está provado", True), ("P = NP é teorema", True),
    ("a TGL resolve o problema do milênio", True), ("o problema do Clay está resolvido", True), ("Clay resolved", True), ("the TGL solves the Millennium Problem", True),
    ("CLAY_SOLVED", True), ("TURING_SOLVED", True), ("P_EQUALS_NP", True), ("MILLENNIUM", True),
    ("a tradução às classes de Turing segue [OPEN]", True), ("the translation to Turing classes stays [OPEN]", True),
    ("Ω é o uniforme", True), ("Omega is the uniform state", True), ("o Ω do psíon é o estado uniforme", True),
    ("o par na face de Fock segue [OPEN]", True), ("o par de psíons na face de Fock fica em aberto", True), ("isso passa à v410", True), ("passes to v410", True),
    ("a máquina de Turing com oráculo: uma leitura decide SAT", True),                                                    # F43 sem a E28
    ("o sistema precisa saber o Nome a cada passo", True),                                                                   # F39 (E25)
    ("a TGL não tem terminal", True), ("há relação sem peso", True),
    ("P = nP é teorema da TGL no modo seleção, relativo ao leitor (o psíon); a máquina sem leitor fica fora: Turing", False),
    ("a máquina sem leitor fica fora; P = nP não é o P = NP de Turing", False),
    ("a identidade de vetores Ω = uniforme fica podada", False), ("«Ω é o uniforme» fica podada", False),
    ("o par na face de Fock está ligado nesta versão", False), ("the pair on the Fock face is linked in this version", False),
    ("a TGL não resolve o problema do Clay", False), ("this does not solve the Clay problem", False),
    ("o terminal é a leitura, não o fim do decaimento", False),
    (E28 + "; o oráculo de contagem", False),
    # R2: as quatro sondas da R1 (MEDIO) agora devem REPROVAR; as frases certas (R2) devem PASSAR
    ("nem o par na face de Fock, que segue [OPEN].", True), ("[OPEN] o par na face de Fock como ligacao;", True), ("[OPEN] o Ω do psíon da luz como o uniforme da instância", True), ("a ligação do par de Fock segue em aberto", True),
    ("nem que o par finito de Bell e o par de Fock sejam o mesmo objeto (espaços distintos, a MESMA Meia-Nat); o par na face de Fock está ligado nesta versão", False),
    ("[REAL] o par na face de Fock LIGADO (ParNaFaceDeFock); PODADA a identidade de vetores Omega = uniforme (a ponte e' a inscricao); [OPEN] a independencia de P vs NP dos axiomas; a igualdade com o leitor que so' conta (E28); o teste com a natureza", False),
    ("a E21 dizia que o par de psions na face de Fock ficava [OPEN] como LIGACAO a fazer; a ligacao foi feita na v409", False),
    ("a ligacao do [OPEN] da v407: o par de psions no setor 2 do Fock concreto da luz tem norma 1", False),
    ("the pair on the Fock face stays [OPEN]", True), ("the pair on the Fock face is linked in this version", False),
    ("a igualdade completa vale so' para o leitor que le tambem as maquinas que o usam (Baker-Gill-Solovay; E28)", False),
    # R3: a forma do MEDIO da R2 e as paraphrases; a frase nova do leitor
    ("[REAL: os termos do kernel do rito · OPEN: o par na face de Fock como ligação, a independência da pergunta da máquina sem leitor, o teste com a natureza]", True),
    ("o par na face de Fock ainda não foi ligado", True), ("a ligação do par na face de Fock fica para a v411", True), ("a ligação passa à v412", True), ("a ligação do par na face de Fock segue aberta", True), ("a ligação do par na face de Fock permanece pendente", True), ("o resto fica para a v411", True),
    ("[INPUT: a ordem · OPEN: o Ω do psíon da luz como o uniforme da instância · KNOWN: x]", True), ("the pair on the Fock face is still pending", True),
    ("[REAL: x, o par na face de Fock LIGADO (`ParNaFaceDeFock`) · PODADA: a identidade de vetores Ω = uniforme (a ponte é a inscrição) · OPEN: a independência da pergunta da máquina sem leitor, a igualdade com o leitor que só conta (E28), o teste com a natureza]", False),
    ("a igualdade completa está provada para o leitor que lê também as máquinas que o usam (Baker–Gill–Solovay 1975 [KNOWN], validade na literatura, não creditação); para o leitor que só conta, não está provada (E28, validade não afirmada)", False),
]
for frase, deve in casos:
    g = G(frase); from_p18 = m._v392_guarda_texto(frase)
    reprovou = bool(g) or bool(from_p18)
    print("guarda:", repr(frase[:80]), "->", [x[0] for x in (g + from_p18)][:3], "(esperado reprovar)" if deve else "(esperado passar)")
    res["guarda: " + frase[:90]] = {"reprovou": reprovou, "esperado": deve, "ok": reprovou == deve}
# SONDAS do revisor: afirmacoes da E28 violada que a guarda talvez nao pegue (informativo: se passam, e' limite da guarda, nao defeito de texto)
sondas = [
    "com o leitor que só conta, a igualdade P = NP vale; " + E28,
    "com o leitor que devolve Z a igualdade vale relativa a ele; " + E28,
    "P^leitor = NP^leitor para o leitor que só conta; " + E28,
    "the counting reader gives P = NP relative to the reader",
]
sond = {}
for s_ in sondas:
    g = G(s_) + m._v392_guarda_texto(s_)
    sond[s_[:100]] = [x[0] for x in g][:3]
    print("SONDA (E28 violada):", repr(s_[:90]), "->", [x[0] for x in g][:3])
res["_sondas_e28_violada"] = {"ok": None, "resultado": sond}
n_ok = sum(1 for v in res.values() if v.get("ok") is True); n_f = sum(1 for v in res.values() if v.get("ok") is False)
print("RESUMO: ok", n_ok, "falha", n_f)
for k, v in res.items():
    if v.get("ok") is False: print("  FALHOU:", k, v)
json.dump(res, open(R + "revisao_terceiro/c_fail_closed_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
