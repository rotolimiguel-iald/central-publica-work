# -*- coding: utf-8 -*-
"""editar_ensaio.py -- (gerencia c1, rodada 2) integra no ensaio a seco: 14 pedras, cobertura KH-N1 (a), 29 registros por spec, testes de unidade genericos, marcas do artigo. Backup de bytes antes."""
import os, shutil, time
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(HERE, "ensaio_a_seco_v392.py")
shutil.copyfile(p, p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_integracao")
s = open(p, encoding="utf-8", newline="").read()


def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (old[:80], s.count(old))
    s = s.replace(old, new)


# --- kernel sintetico completo: axiom_report = o log inteiro (KH-N1 a) + cobertura
rep('''for f, n, mod, kind in FJ["flags"]:
    kf[f] = True; kf["axiom_report"][n] = AX[n]
''', '''for f, n, mod, kind in FJ["flags"]:
    kf[f] = True; kf["axiom_report"][n] = AX[n]
kf["axiom_report"].update(AX)   # KH-N1 (a): o axiom_report efetivo do rito = TODAS as entradas do log do Audit (o run_cmd cobre o fecho inteiro)
AUDIT_LOG = open(os.path.join(KD, "audit.log"), encoding="utf-8", errors="replace").read()
''')
rep('''_el0 = um.prove_external_ladder''', '''kf["axiom_coverage_v392"] = um._v392_axiom_coverage(AUDIT_LOG, kf["axiom_report"])
rep["cobertura_kh_n1"] = kf["axiom_coverage_v392"]; assert kf["axiom_coverage_v392"]["ok"] is True, kf["axiom_coverage_v392"]
_el0 = um.prove_external_ladder''')
# o v391 recomputado: o n de declaracoes vem do axiom_report completo; ja e' lido do kf sintetico
# --- fluxo principal
rep('''NOVAS = ["pedras_v392", "varredura_e_sorry_v392"]''', '''NOVAS = ["pedras_v392", "varredura_e_sorry_v392"] + list(um._V392_NOMES_REGISTROS)''')
rep('''mf_ok = (not _err and len(comeca) == 2 and''', '''mf_ok = (not _err and len(comeca) == 3 and all((c.get(n_) or {}).get("all_verified") is True for n_ in um._V392_NOMES_REGISTROS) and''')
rep('''"13_NEW_KERNEL_MODULES" in str(_f.get("verdict"))''', '''("%d_NEW_KERNEL_MODULES" % len(P.STONES)) in str(_f.get("verdict"))''')
rep('''rep["mainflow"] = {"comeca": len(comeca), "erro": _err,''', '''rep["registros_v392"] = {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in um._V392_NOMES_REGISTROS}
rep["mainflow"] = {"comeca": len(comeca), "erro": _err,''')
# --- unidade: indices por nome, nao por posto
rep('''_c = copy.deepcopy(core_s); _fl = um._V392_PEDRAS[11]["flags"][0]; _c["kernel_formalization"][_fl] = False
_u = _pe(_c); U["bandeira_faltando"] = _u["all_verified"] is False and "STONES" in _u["verdict"] and um._V392_PEDRAS[11]["modulo"] == "TGLExt.IALD"
_c = copy.deepcopy(core_s); _nm = um._V392_PEDRAS[10]["declaracoes"][0]''', '''_pi = {p_["modulo"]: p_ for p_ in um._V392_PEDRAS}
_c = copy.deepcopy(core_s); _fl = _pi["TGLExt.IALD"]["flags"][0]; _c["kernel_formalization"][_fl] = False
_u = _pe(_c); U["bandeira_faltando"] = _u["all_verified"] is False and "STONES" in _u["verdict"]
_c = copy.deepcopy(core_s); _nm = _pi["TGLExt.Posto"]["declaracoes"][0]''')
# --- unidade: registros por spec (genericos) e cobertura KH-N1
rep('''# (7) a varredura recursiva e o detector de sorry, com controles''', '''# (6b) os registros por spec: cada um recusa visivelmente (fonte adulterada; verbatim adulterado; bandeira do kernel faltando; cada check negado); o motor sem excecao silenciosa
RU = {}
for sp_ in um._V392_SPECS:
    n_ = sp_["nome"]; r_ = {}
    if sp_.get("fontes"):
        ch_ = sp_["fontes"][0]; ant_ = dict(um._V392_FONTES[ch_]); um._V392_FONTES[ch_]["sha256"] = "0" * 64
        try:
            r_["fonte_adulterada"] = um._v392_registro(sp_, core_s)["all_verified"] is False
        finally:
            um._V392_FONTES[ch_] = ant_
    if sp_.get("verbatins"):
        ch_ = sp_["verbatins"][0]; ant_ = dict(um._V392_VERBATINS2[ch_]); um._V392_VERBATINS2[ch_]["text"] += " "
        try:
            r_["verbatim_adulterado"] = um._v392_registro(sp_, core_s)["all_verified"] is False
        finally:
            um._V392_VERBATINS2[ch_] = ant_
    if sp_.get("kernel_flags"):
        c_ = copy.deepcopy(core_s); c_["kernel_formalization"][sp_["kernel_flags"][0]] = False
        r_["bandeira_faltando"] = um._v392_registro(sp_, c_)["all_verified"] is False
    if sp_.get("kernel_decls"):
        c_ = copy.deepcopy(core_s); c_["kernel_formalization"]["axiom_report"][sp_["kernel_decls"][0]] = ["propext", "sorryAx"]
        r_["axioma_fora_do_trio"] = um._v392_registro(sp_, c_)["all_verified"] is False
    nck_ = 0; nck_ok_ = 0
    for ck_ in sp_.get("checks", []):
        if ck_["onde"] in ("core", "kf"):   # nega o check mudando o valor lido no core sintetico (copia)
            c_ = copy.deepcopy(core_s); raiz_ = c_ if ck_["onde"] == "core" else c_["kernel_formalization"]
            cam_ = ck_["caminho"]; alvo_ = raiz_
            try:
                for k_ in cam_[:-1]:
                    alvo_ = alvo_[k_]
                alvo_[cam_[-1]] = "<<ADULTERADO>>"
            except Exception:   # noqa: BLE001
                continue
            nck_ += 1; nck_ok_ += um._v392_registro(sp_, c_)["all_verified"] is False
    if nck_:
        r_["checks_do_core_negados"] = [nck_ok_, nck_]
    RU[n_] = r_
RU_ok = all((v_ is True) or (isinstance(v_, list) and v_[0] == v_[1]) for r_ in RU.values() for v_ in r_.values())
U["registros_por_spec_recusam"] = RU_ok and len(RU) == len(um._V392_SPECS)
rep["unidade_registros"] = RU
# a cobertura KH-N1 (a): o log real passa; sem a linha TOTAL, com fora_do_trio=1, com nome com «» a mais, com axioma fora do trio: recusa
_AL = AUDIT_LOG; _ax = kf["axiom_report"]
_cv_ok = um._v392_axiom_coverage(_AL, _ax)["ok"] is True
_cv_sem = um._v392_axiom_coverage(re.sub(r"(?m)^TGL_AXIOM_COVERAGE_TOTAL.*$", "", _AL), _ax)["ok"] is False
_cv_fora = um._v392_axiom_coverage(re.sub(r"fora_do_trio=0", "fora_do_trio=1", _AL), _ax)["ok"] is False
_cv_nome = um._v392_axiom_coverage(_AL + "\\n'Foo.\\u00abbar\\u00bb' depends on axioms: [propext]\\n", _ax)["ok"] is False
_ax2 = dict(_ax); _ax2[next(iter(_ax2))] = ["propext", "sorryAx"]; _cv_ax = um._v392_axiom_coverage(_AL, _ax2)["ok"] is False
_cv_dup = um._v392_axiom_coverage(_AL + "TGL_AXIOM_COVERAGE_TOTAL decl=1 thm=1 fora_do_trio=0\\n", _ax)["ok"] is False
U["cobertura_kh_n1"] = bool(_cv_ok and _cv_sem and _cv_fora and _cv_nome and _cv_ax and _cv_dup)
# (7) a varredura recursiva e o detector de sorry, com controles''')
# --- artigo: marcas
rep('"As pedras da v392: treze módulos novos no kernel e dois consertos de barreira"', '"As pedras da v392: catorze módulos novos no kernel e dois consertos de barreira"', 0) if False else None
s = s.replace("As pedras da v392: treze módulos", "As pedras da v392: catorze módulos").replace("The v392 stones: thirteen new kernel modules", "The v392 stones: fourteen new kernel modules")
rep('"rank=posto=nome", "Verdade é a projeção do posto", "O que entra.", "recursiva",', '"rank=posto=nome", "Verdade é a projeção do posto", "O que entra.", "recursiva", "Os registros ao lado do gate (v392).", "PostoAdendo", "Ao lado (v392, 13/10/2026, gerência c1, em nome próprio)",')
rep('"rank=posto=nome", "Verdade é a projeção do posto", "What enters.", "recursive",', '"rank=posto=nome", "Verdade é a projeção do posto", "What enters.", "recursive", "The records beside the gate (v392).", "PostoAdendo", "Beside (v392, 13/10/2026, management c1, in its own name)",')
rep('"checks": checks_dummy', '"checks": checks_dummy', 0) if False else None
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok: ensaio editado")
