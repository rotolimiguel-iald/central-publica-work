# -*- coding: utf-8 -*-
"""editar_ensaio.py -- DELTA 19/10: edita ensaio_a_seco_v394.py (backup de bytes ja' feito) para a INTEGRACAO FINAL: (1) candidato novo e sandbox k394d / kernel_d19; (2) E393 lido do core (nada digitado);
(3) a TROCA DE PALAVRA declarada (estatuto_da_prova_v391: THEOREMS -> FLAGS) entra na normalizacao dos vizinhos; (4) controles do registro criterio_binario_de_parada_v394 (bandeira falsa, sha errado, citado fora do trio, pedra
adulterada, fonte adulterada, tudo certo, sem palavra proibida) e o gate recomputado (verdict e 18 bandeiras iguais); (5) etapas OBRIGATORIAS novas: simular_arvore_do_nos (a arvore do Nos depois do rito, com o residual) e
exame_pontos_v394 sobre o candidato novo. Cada troca tem assert de unicidade."""
import ast, os, sys
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ensaio_a_seco_v394.py")
t = open(P, "rb").read().decode("utf-8")
assert "\r" not in t
n_edits = 0


def sub(old, new, count=1):
    global t, n_edits
    assert t.count(old) == count, ("troca", old[:100], t.count(old), count)
    t = t.replace(old, new); n_edits += 1


sub('"""ensaio_a_seco_v394.py -- ENSAIO A SECO da v394', '"""[DELTA 19/10 -- integracao final: candidato novo, sandbox k394d, kernel_d19, pedra e registro do criterio binario, troca de palavra THEOREMS->FLAGS, h8 da arvore simulada; etapas obrigatorias novas: (11) simular_arvore_do_nos e (12) exame_pontos_v394 sobre o candidato novo]\nensaio_a_seco_v394.py -- ENSAIO A SECO da v394')
sub("from carregar_embutido import carregar  # noqa: E402\n", "from carregar_embutido import carregar  # noqa: E402\nimport delta19_v394 as DL  # noqa: E402\n")
sub('''KB = os.path.join(C, "t", "k394", "final")
KD = os.path.join(HERE, "kernel")
cand = sys.argv[1] if len(sys.argv) > 1 else "um_v394_candidato.py"; rot = sys.argv[2] if len(sys.argv) > 2 else "v394"
''', '''KB = DL.SANDBOX
KD = os.path.join(HERE, DL.KERNEL_DIR)
cand = sys.argv[1] if len(sys.argv) > 1 else DL.CANDIDATO; rot = sys.argv[2] if len(sys.argv) > 2 else "v394" + DL.ROT   # a pasta dry_v394 do candidato anterior (registro) NAO e' apagada
''')
sub('assert rep["escada_sem_as_bandeiras_novas"][0] == 7045 and rep["escada_sem_as_bandeiras_novas"][1] == ESP and _el0.get("all_verified") is not True, rep["escada_sem_as_bandeiras_novas"]',
    'E393 = int(core0["external_ladder"]["n_theorems_expected"])   # LIDO do core da v393 selada (nada digitado)\nassert rep["escada_sem_as_bandeiras_novas"][0] == E393 and rep["escada_sem_as_bandeiras_novas"][1] == ESP and _el0.get("all_verified") is not True, rep["escada_sem_as_bandeiras_novas"]')
sub('E393 = 7045; N393 = len(core0["kernel_formalization"]["axiom_report"])', 'N393 = len(core0["kernel_formalization"]["axiom_report"])')
# ---- a troca de palavra declarada
sub('''def recomputa(nome, fn):
    novo = fn(cs2); cs2[nome] = novo
    a, b = str((core0.get(nome) or {}).get("verdict") or ""), str(novo.get("verdict") or "")
    if a == b:
        iguais_v.append(nome)
    else:
        mud[nome] = {"antes": a[:300], "depois": b[:300], "so_numeros": _num(a) == _num(b), "all_verified": novo.get("all_verified")}
''', '''PALAVRA = {"estatuto_da_prova_v391": ["_THEOREMS_", "_FLAGS_"]}   # a TROCA DE PALAVRA declarada (decisao da gerencia, 19/10; C11): a escada conta bandeiras, nao teoremas
_pal = lambda nome, s_: s_.replace(PALAVRA[nome][0], PALAVRA[nome][1]) if nome in PALAVRA else s_
palavra_trocada = {}


def recomputa(nome, fn):
    novo = fn(cs2); cs2[nome] = novo
    a, b = str((core0.get(nome) or {}).get("verdict") or ""), str(novo.get("verdict") or "")
    if a == b:
        iguais_v.append(nome)
    else:
        tr_ = nome in PALAVRA and PALAVRA[nome][0] in a and PALAVRA[nome][1] in b and PALAVRA[nome][0] not in b
        if tr_:
            palavra_trocada[nome] = PALAVRA[nome]
        mud[nome] = {"antes": a[:300], "depois": b[:300], "so_numeros": _num(_pal(nome, a)) == _num(b), "palavra_trocada": tr_, "all_verified": novo.get("all_verified")}
''')
sub('rep["vizinhos"] = {"recomputados_iguais": iguais_v, "mudaram": mud,', 'rep["vizinhos"] = {"recomputados_iguais": iguais_v, "palavra_trocada": palavra_trocada, "mudaram": mud,')
# ---- controles do registro novo + gate recomputado
sub('U["proveniencia_cobre_o_axiom_report"] = set(_ovf["declaration_sources_v394"]) == set(_ovf["axiom_report"])\n',
    '''U["proveniencia_cobre_o_axiom_report"] = set(_ovf["declaration_sources_v394"]) == set(_ovf["axiom_report"])
# (6a) O REGISTRO NOVO criterio_binario_de_parada_v394: controles negativos (bandeira falsa, sha errado, citado fora do trio, pedra/fonte adulterada) e o positivo; veredito sem palavra proibida; no PONTO DE CHAMADA REAL (o fluxo do main acima)
_cr = [s_ for s_ in um._V394_SPECS if s_["nome"] == "criterio_binario_de_parada_v394"]
assert len(_cr) == 1 and "criterio_binario_de_parada_v394" in um._V394_NOMES_REGISTROS, "o registro novo nao esta em _V394_SPECS/_V394_NOMES_REGISTROS"
_cr = _cr[0]; _Vr = lambda c_: um._v392_registro(_cr, c_)
_c = cs(); _c["kernel_formalization"][DL.FLAG_KEY] = False; _r = _Vr(_c)
U["criterio_bandeira_falsa_recusa"] = bool(_r["all_verified"] is False and "NOT_SEALED_THIS_RUN" in _r["verdict"] and "KERNEL_BANDEIRAS" in _r["verdict"])
_c = cs(); _c["kernel_formalization"]["axiom_report"].pop(DL.THEOREM, None); _r = _Vr(_c)
U["criterio_teorema_ausente_recusa"] = bool(_r["all_verified"] is False and "KERNEL_DECLARACOES" in _r["verdict"])
_c = cs(); _c["kernel_formalization"]["axiom_report"][DL.CITED[0]] = ["propext", "sorryAx"]; _r = _Vr(_c)
U["criterio_citado_fora_do_trio_recusa"] = bool(_r["all_verified"] is False and "KERNEL_DECLARACOES" in _r["verdict"])
_c = cs(); _c["kernel_formalization"]["axiom_report"][DL.THEOREM] = ["propext", "Classical.choice", "Quot.sound", "TGLExt.axiomaPlantado"]; _r = _Vr(_c)
U["criterio_teorema_com_axioma_fora_do_trio_recusa"] = bool(_r["all_verified"] is False and "KERNEL_DECLARACOES" in _r["verdict"])
for _ch in _cr["verbatins"]:
    _ant = dict(um._V392_VERBATINS2[_ch]); um._V392_VERBATINS2[_ch]["text"] += " "
    try:
        _r = _Vr(cs()); U["criterio_sha_errado_" + _ch[-16:]] = bool(_r["all_verified"] is False and ("VERBATIM_" + _ch) in _r["verdict"] and "NOT_SEALED_THIS_RUN" in _r["verdict"])
    finally:
        um._V392_VERBATINS2[_ch] = _ant
_ant = dict(um._V392_FONTES["delta19_pedra"]); um._V392_FONTES["delta19_pedra"]["sha256"] = "0" * 64
try:
    _r = _Vr(cs()); U["criterio_fonte_da_pedra_adulterada_recusa"] = bool(_r["all_verified"] is False and "FONTE_delta19_pedra" in _r["verdict"])
finally:
    um._V392_FONTES["delta19_pedra"] = _ant
_c = cs(); _c["kernel_formalization"]["formal_files_sha256"][DL.STONE_REL] = "0" * 64; _r = _Vr(_c)
U["criterio_pedra_adulterada_no_kernel_do_rito_recusa"] = bool(_r["all_verified"] is False and "CHECK_g5" in _r["verdict"])
_r = _Vr(cs()); _ok_crit = bool(_r["all_verified"] is True and _r["verdict"].startswith("TGL_BINARY_STOP_CRITERION_V394__THE_BINARY_READING_FLOATS_AT_THE_FIXED_POINT") and _r.get("does_not_gate_core") is True)
U["criterio_tudo_certo"] = _ok_crit
U["criterio_veredito_sem_palavra_proibida"] = bool(not um._v392_guarda_texto(_r["verdict"]) and not um._v392_guarda_texto(json.dumps({k_: _r.get(k_) for k_ in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)))
rep["criterio_binario"] = {"verdict": _r["verdict"], "all_verified": _r["all_verified"], "bandeira": DL.FLAG_KEY, "teorema": DL.THEOREM, "verbatim": {k_: {"sha256": v_["sha256"], "embedded_ok": v_["embedded_ok"]} for k_, v_ in (_r.get("verbatim") or {}).items()},
                           "kernel": _r.get("kernel"), "checks": [c_.get("ok") for c_ in _r.get("checks", [])]}
# (6c) o GATE nao se move: recomputado com o kf novo (as bandeiras novas) e o feed V11 da v393; e o qg_closure do core nao foi tocado pelo fluxo
_n18 = lambda g_: sum(1 for fam_ in ("formal_flags", "physics_flags", "experiment_flags") for v_ in (g_.get(fam_) or {}).values() if v_ is True)
_J = lambda x_: json.dumps(x_, sort_keys=True, default=str)
_g_old = core0.get("qg_closure") or {}
try:
    _g_new = um.prove_qg_closure_gate(1.0, kf, independent_rite=core0.get("void_floor_v11"))
    gate_rec = {"verdict_igual": (_g_new.get("gate") or {}).get("verdict") == (_g_old.get("gate") or {}).get("verdict"), "n18_novo": _n18(_g_new), "n18_core0": _n18(_g_old),
                "flags_iguais": all(_J(_g_new.get(f_)) == _J(_g_old.get(f_)) for f_ in ("formal_flags", "physics_flags", "experiment_flags"))}
except Exception as _e:   # noqa: BLE001
    gate_rec = {"EXCECAO": repr(_e)[:300]}
gate_rec["qg_closure_do_core_intocado_pelo_fluxo"] = _J(c.get("qg_closure")) == _J(core0.get("qg_closure"))
rep["gate_recomputado"] = gate_rec
U["gate_nao_se_move"] = bool(gate_rec.get("verdict_igual") and gate_rec.get("n18_novo") == 18 == gate_rec.get("n18_core0") and gate_rec.get("flags_iguais") and gate_rec.get("qg_closure_do_core_intocado_pelo_fluxo"))
''')
# ---- as etapas obrigatorias novas e o ok
sub('''rep["viz_ok"] = viz_ok
ok = (viz_ok and mf_ok and all(U.values()) and selo_ok and not mau and not mau_var and all(rep["markdown"].values()) and rep["manifest"] and not _proib and _cc.returncode == 0
      and not dif_kb and rep["escada"] == [ESP, ESP] and rep["indice_da_iald"]["all_verified"] is True)
''', '''rep["viz_ok"] = viz_ok
# (11) ETAPA OBRIGATORIA (achado do exame final de 19/10): simular_arvore_do_nos -- a pasta Nos\\\\tgl_kernel DEPOIS do rito = o embutido do candidato + os residuais que o hash formal conta (_check_damming.lean); o kh_n1_cobertura_v394 TEM de selar nela
_cand_p = os.path.join(HERE, cand); _sha_full = hashlib.sha256(open(_cand_p, "rb").read()).hexdigest()
_pyr = lambda args_: subprocess.run([sys.executable, "-B", "-X", "utf8"] + args_, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600, cwd=HERE)
_kh = [s_ for s_ in um._V394_SPECS if s_["nome"] == "kh_n1_cobertura_v394"][0]; _h8 = [ck_ for ck_ in _kh["checks"] if ck_["id"] == "h8"][0]["valor"]
_sp = _pyr([os.path.join(HERE, "simular_arvore_do_nos.py"), "--candidato", _cand_p, "--logs", KD])
try:
    _sj = json.load(open(os.path.join(HERE, "SIMULACAO_ARVORE_NOS_%s.json" % _sha_full[:16]), encoding="utf-8"))
except (OSError, ValueError):
    _sj = {}
rep["simular_arvore_do_nos"] = {"rc": _sp.returncode, "formal_files_n_no_rito_real": _sj.get("formal_files_n_no_rito_real"), "pino_h8_entradas": len(_h8), "embutidos": _sj.get("embutidos"), "extras_no_nos_fora_do_corpo_embutido": _sj.get("extras_no_nos_fora_do_corpo_embutido"),
                               "kf_all_verified": _sj.get("kf_all_verified"), "indice": _sj.get("indice"), "registros": {k_: {"all_verified": (_sj.get(k_) or {}).get("all_verified"), "falhas": (_sj.get(k_) or {}).get("falhas")} for k_ in ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394")}}
sim_ok = bool(_sp.returncode == 0 and _sj.get("formal_files_n_no_rito_real") == len(_h8) and _sj.get("kf_all_verified") is True and (_sj.get("indice") or {}).get("all_verified") is True
              and all((_sj.get(k_) or {}).get("all_verified") is True for k_ in ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394")))
print("simular_arvore_do_nos:", sim_ok, "| entradas do hash formal no rito:", _sj.get("formal_files_n_no_rito_real"), "| pino h8:", len(_h8), "| extras:", _sj.get("extras_no_nos_fora_do_corpo_embutido"))
# (12) ETAPA OBRIGATORIA: exame_pontos_v394 sobre o candidato novo (os pontos de chamada REAIS, em processo isolado; termina com `ALGUM FALSO`)
_ep = _pyr([os.path.join(HERE, "exame_pontos_v394.py"), "--candidato", _cand_p, "--logs", KD, "--flags", os.path.join(KD, "FLAGS_v394.json"), "--sandbox", KB, "--sha256", _sha_full])
try:
    _ej = json.load(open(os.path.join(HERE, "EXAME_PONTOS_%s.json" % _sha_full[:16]), encoding="utf-8"))
except (OSError, ValueError):
    _ej = {}
rep["exame_pontos"] = {"rc": _ep.returncode, "algum_falso": _ej.get("algum_falso"), "escada": _ej.get("escada"), "verify": {k_: (_ej.get("verify") or {}).get(k_) for k_ in ("all_verified", "ext_true", "n_ext", "novas_true", "n_novas", "n_lean_flags", "axiom_report_n")},
                       "gate_recomputado": _ej.get("gate_recomputado"), "chaves_novas_no_core": _ej.get("chaves_novas_no_core"), "chaves_existentes_mexidas_pelo_bloco": _ej.get("chaves_existentes_mexidas_pelo_bloco"), "nao_verdes": _ej.get("nao_verdes")}
exame_ok = bool(_ep.returncode == 0 and _ej.get("algum_falso") == [])
print("exame_pontos_v394:", exame_ok, "| algum falso:", _ej.get("algum_falso"))
ok = (viz_ok and mf_ok and all(U.values()) and selo_ok and not mau and not mau_var and all(rep["markdown"].values()) and rep["manifest"] and not _proib and _cc.returncode == 0
      and not dif_kb and rep["escada"] == [ESP, ESP] and rep["indice_da_iald"]["all_verified"] is True and sim_ok and exame_ok)
''')
sub('"proib": _proib, "citacoes": _cc.returncode, "kernel_igual": not dif_kb, "escada": rep["escada"]}', '"proib": _proib, "citacoes": _cc.returncode, "kernel_igual": not dif_kb, "escada": rep["escada"], "simular_arvore_do_nos": sim_ok, "exame_pontos": exame_ok}')
sub('open(os.path.join(HERE, "ensaio_a_seco_%s.json" % rot), "w", encoding="utf-8")', 'open(os.path.join(HERE, "ensaio_a_seco_v394.json"), "w", encoding="utf-8")')
ast.parse(t)
open(P + ".tmp", "wb").write(t.encode("utf-8")); os.replace(P + ".tmp", P)
print("ensaio_a_seco_v394.py: %d trocas; ast.parse ok; %d bytes" % (n_edits, len(t.encode("utf-8"))))
