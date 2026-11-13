# -*- coding: utf-8 -*-
"""_fix_p2_ao_lado_v411.py -- (claude-construtor-v411, retomada, 12/11/2026) o ADITIVO da gerencia c1 de 12/11 (achado da custodia): o token P2_NOT_DETERMINED do veredito SELADO de three_stress_tests_v387 NAO muda;
a leitura nova do P2 vai AO LADO, num campo NOVO do registro h0dn_bg1_v411 (p2_ao_lado_da_v387: rotulo, rotulo_selado_da_v387, canal, nota), preenchido so' quando o registro passa com o ramo primario recalculado
(o do molde do veredito, BRANCH_4); uma checagem DENTRO da c14 (sem mudar N_CHECKS_FECHO): o rotulo selado da v387 lido do core contem P2_NOT_DETERMINED e o campo novo nao o altera. No artigo: a frase AO LADO
(DESENHO 5.1 b) na secao dos tres testes de estresse (v387) e a variante do paragrafo “O metodo”, as duas com as quatro obrigacoes da F67 no mesmo bloco; o texto selado da v387 nao e' reescrito. Toca: registros_h0dn_v411.py,
runtime_h0dn_v411.py, quadro_v411.py, gerar_candidato_v411.py e _teste_h0dn_offline_v411.py. Backup de BYTES antes de cada; ancoras unicas; ast.parse depois. uso: python -B -X utf8 _fix_p2_ao_lado_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca(arq_, pares_):
    p_ = os.path.join(HERE, arq_); b_ = open(p_, "rb").read(); t_ = b_.decode("utf-8"); assert "\r" not in t_, arq_
    for a_, n_ in pares_:
        assert t_.count(a_) == 1, (arq_, a_[:100], t_.count(a_))
        t_ = t_.replace(a_, n_)
    ast.parse(t_)
    bak_ = p_ + ".bak_" + TS + "_p2"; open(bak_, "wb").write(b_); assert open(bak_, "rb").read() == b_
    nb_ = t_.encode("utf-8"); open(p_ + ".tmp", "wb").write(nb_); assert os.path.getsize(p_ + ".tmp") == len(nb_); os.replace(p_ + ".tmp", p_)
    print("ok", arq_, len(b_), "->", len(nb_))


# ---- (1) o contrato leva o p2_ao_lado (lido do delta: o rotulo de UM lugar so')
troca("registros_h0dn_v411.py", [
    ('"textos_da_gerencia_citados": [{"nome": g_["nome"], "sha256": g_["sha256"]} for g_ in DL.TEXTOS_DA_GERENCIA_CITADOS], "desenho_sha16": DL.DESENHO_SHA16}',
     '"textos_da_gerencia_citados": [{"nome": g_["nome"], "sha256": g_["sha256"]} for g_ in DL.TEXTOS_DA_GERENCIA_CITADOS], "desenho_sha16": DL.DESENHO_SHA16,\n'
     '            "p2_ao_lado": dict(DL.P2_AO_LADO)}   # (aditivo da gerencia c1, 12/11: o P2 AO LADO da v387; o token selado nao muda)'),
])

# ---- (2) o runtime: o campo novo e a checagem dentro da c14
troca("runtime_h0dn_v411.py", [
    ('    c14_ok_ = isinstance(gate_, str) and gate_ == c_["baseline"]["gate_verdict"]\n',
     '    c14_ok_ = isinstance(gate_, str) and gate_ == c_["baseline"]["gate_verdict"]\n'
     '    # (aditivo da gerencia c1, 12/11; achado da custodia) DENTRO da c14, sem mudar o numero de checagens: o rotulo SELADO da v387 (o trecho do veredito de three_stress_tests_v387 LIDO do core, nunca digitado)\n'
     '    # traz P2_NOT_DETERMINED e fica como registro; a leitura nova do P2 vai AO LADO, no campo novo p2_ao_lado_da_v387; montar o campo nao altera o veredito selado\n'
     '    p2c_ = c_.get("p2_ao_lado") or {}\n'
     '    v387_antes_ = str((core_.get(p2c_.get("registro") or "") or {}).get("verdict") or "")\n'
     '    seg387_ = [s__ for s__ in v387_antes_.split("__") if p2c_.get("token_selado") and p2c_["token_selado"] in s__]\n'
     '    rot2_ = str(p2c_.get("rotulo") or "")\n'
     '    if "<n>" in rot2_:\n'
     '        rot2_ = rot2_.replace("<n>", str(n_)) if n_ is not None else ""\n'
     '    p2_ = {"rotulo": rot2_ or None, "rotulo_e_proposta": bool(p2c_.get("rotulo_e_proposta")), "rotulo_de": p2c_.get("rotulo_de"), "rotulo_selado_da_v387": seg387_[0] if len(seg387_) == 1 else None,\n'
     '           "registro_selado": p2c_.get("registro"), "canal": p2c_.get("canal"), "nota": p2c_.get("nota")}\n'
     '    v387_depois_ = str((core_.get(p2c_.get("registro") or "") or {}).get("verdict") or "")\n'
     '    c14_p2_ = {"token_no_rotulo_selado": bool(len(seg387_) == 1), "veredito_selado_igual_depois": v387_depois_ == v387_antes_ and bool(v387_antes_), "rotulo_novo_sem_o_token": bool(rot2_) and p2c_.get("token_selado", "") not in rot2_}\n'
     '    c14_p2_["ok"] = bool(p2c_) and all(c14_p2_.values())\n'
     '    c14_ok_ = c14_ok_ and c14_p2_["ok"]\n'),
    ('"veredito_montado": veredito_, "integridade_modelos": integ_.get("model_names") if isinstance(integ_, dict) else None, "pre_registro_estado": c_["estado_do_pre_registro"]}',
     '"veredito_montado": veredito_, "integridade_modelos": integ_.get("model_names") if isinstance(integ_, dict) else None, "pre_registro_estado": c_["estado_do_pre_registro"],\n'
     '               "p2_ao_lado_da_v387": p2_, "c14_inclui_o_p2_da_v387": c14_p2_}'),
    ('            "citados_nao_embutidos": list(c_["citados"]), "contratos_de_registro_fora_da_escada": list(c_["contratos_de_registro_fora_da_escada"])}\n',
     '            "citados_nao_embutidos": list(c_["citados"]), "contratos_de_registro_fora_da_escada": list(c_["contratos_de_registro_fora_da_escada"]), "p2_ao_lado_da_v387": None}\n'),
    ('            out_["verdict"] = (mec_["veredito"] if out_["all_verified"] else _V411_H0DN_RECUSA % "MECHANICS_CHECK_FAILED")\n',
     '            out_["verdict"] = (mec_["veredito"] if out_["all_verified"] else _V411_H0DN_RECUSA % "MECHANICS_CHECK_FAILED")\n'
     '            _r2_ = v_["primario"].get("ramo")   # (o P2 ao lado so\' quando o registro passa e o ramo primario recalculado e\' o do molde do veredito: o BRANCH_ do primario, lido do contrato)\n'
     '            if out_["all_verified"] and _r2_ == c_["esperado_do_resultado"]["ramo_primario"] and ("BRANCH_%s__" % _r2_) in c_["veredito_meio_molde"].split("BESIDE_")[0]:\n'
     '                out_["p2_ao_lado_da_v387"] = dict(v_["p2_ao_lado_da_v387"])\n'),
])

# ---- (3) o quadro: a frase AO LADO da v387 e a variante do metodo, com as quatro obrigacoes da F67 no mesmo bloco
troca("quadro_v411.py", [
    ('    if lang_ == "pt":\n        return r"os efeitos de $\\beta$ na natureza foram lidos acima de $5\\sigma$ num canal, a razão de Hubble, sob o modelo de erros publicado; nos demais canais nenhum discrimina a RG à sensibilidade disponível"\n'
     '    return r"the effects of $\\beta$ in nature were read above $5\\sigma$ in one channel, the Hubble ratio, under the published error model; in the other channels none discriminates GR at the available sensitivity"\n',
     '    if onde_ == "metodo":   # (aditivo da gerencia c1, 12/11) no paragrafo “O metodo” a frase leva as quatro obrigacoes da F67 no mesmo bloco\n'
     '        z_ = _v411_n(((r_.get("values") or {}).get("cefeidas_livres") or {}).get("z_null"), 2, lang_)\n'
     '        if lang_ == "pt":\n'
     '            return (r"os efeitos de $\\beta$ na natureza foram lidos acima de $5\\sigma$ num canal, a razão de Hubble, sob o modelo de erros publicado (ao lado, no mesmo item, as Cefeidas livres dão $" + z_ + r"\\sigma$, abaixo de 5; "\n'
     '                    r"retrodição sem ajuste, com emenda posterior à guarda, teste não cego; provado é validade, não creditação); nos demais canais nenhum discrimina a RG à sensibilidade disponível")\n'
     '        return (r"the effects of $\\beta$ in nature were read above $5\\sigma$ in one channel, the Hubble ratio, under the published error model (beside it, in the same item, the free Cepheids give $" + z_ + r"\\sigma$, below 5; "\n'
     '                r"a retrodiction without fit, with an amendment made after the guard, the test not blind; proved is validity, not creditation); in the other channels none discriminates GR at the available sensitivity")\n'
     '    if lang_ == "pt":\n        return r"os efeitos de $\\beta$ na natureza foram lidos acima de $5\\sigma$ num canal, a razão de Hubble, sob o modelo de erros publicado; nos demais canais nenhum discrimina a RG à sensibilidade disponível"\n'
     '    return r"the effects of $\\beta$ in nature were read above $5\\sigma$ in one channel, the Hubble ratio, under the published error model; in the other channels none discriminates GR at the available sensitivity"\n\n\n'
     'def _v411_p2_ao_lado_tex(core_, lang_):\n'
     '    """(aditivo da gerencia c1, 12/11) a frase AO LADO do P2 na secao dos tres testes de estresse (v387): o texto selado da v387 fica (P2 nao determinada, registro); a leitura nova do P2 vai ao lado, com as quatro\n'
     '    obrigacoes da F67 no mesmo bloco e o rotulo do campo novo do registro (p2_ao_lado_da_v387). So\' se o registro selou; senao, dito."""\n'
     '    r_ = core_.get("h0dn_bg1_v411") or {}; p2_ = r_.get("p2_ao_lado_da_v387") or {}\n'
     '    if r_.get("all_verified") is not True or not p2_:\n'
     '        return (r"\\textbf{(v411, ao lado)} O registro do teste H0DN $\\times$ BG1 não selou nesta rodada: o P2 segue como o registro selado da v387 o diz." if lang_ == "pt"\n'
     '                else r"\\textbf{(v411, beside)} The H0DN $\\times$ BG1 test record did not seal this round: P2 stays as the sealed v387 record says.")\n'
     '    z_ = _v411_n(((r_.get("values") or {}).get("cefeidas_livres") or {}).get("z_null"), 2, lang_)\n'
     '    if lang_ == "pt":\n'
     '        return (r"\\textbf{(v411, ao lado do $P_2$)} Os efeitos de $\\beta$ na natureza foram lidos acima de $5\\sigma$ num canal, a razão de Hubble (H0DN $\\times$ BG1), sob o modelo de erros publicado; ao lado, no mesmo item, "\n'
     '                r"as Cefeidas livres dão $" + z_ + r"\\sigma$, abaixo de 5; é retrodição sem ajuste, com emenda posterior à guarda, e o teste não é cego; provado é validade, não creditação; nos demais canais nenhum discrimina a RG "\n'
     '                r"à sensibilidade disponível. O rótulo selado da v387 (\\texttt{" + _v411_tt(p2_.get("rotulo_selado_da_v387")) + r"}) fica como registro; esta leitura vai ao lado (\\texttt{" + _v411_tt(p2_.get("rotulo")) + r"}"\n'
     '                + (r", rótulo provisório, em proposta" if p2_.get("rotulo_e_proposta") else "") + r").")\n'
     '    return (r"\\textbf{(v411, beside $P_2$)} The effects of $\\beta$ in nature were read above $5\\sigma$ in one channel, the Hubble ratio (H0DN $\\times$ BG1), under the published error model; beside it, in the same item, "\n'
     '            r"the free Cepheids give $" + z_ + r"\\sigma$, below 5; it is a retrodiction without fit, with an amendment made after the guard, and the test is not blind; proved is validity, not creditation; in the other channels none "\n'
     '            r"discriminates GR at the available sensitivity. The sealed v387 label (\\texttt{" + _v411_tt(p2_.get("rotulo_selado_da_v387")) + r"}) stays as record; this reading goes beside it (\\texttt{" + _v411_tt(p2_.get("rotulo")) + r"}"\n'
     '            + (r", provisional label, under proposal" if p2_.get("rotulo_e_proposta") else "") + r").")\n'),
])

# ---- (4) o gerador: a frase ao lado na secao da v387 (PT e EN), o nome novo, o texto renderizado e o selo
troca("gerar_candidato_v411.py", [
    ('_controles(RT_, "runtime_v411"); _controles([CONTR_H, TXT_H, specs, fontes, TOPO], "contrato/texto/specs/fontes/topo")\n',
     '# (aditivo da gerencia c1, 12/11) a frase AO LADO do P2 na secao dos tres testes de estresse (v387), PT e EN: ANTES da linha do veredito da v387 (que fica, selado); o texto selado da v387 nao e\' reescrito\n'
     'for _lg, _sec in (("pt", r\'    _sec3s.append(r"\\section*{Os três testes de estresse, conjuntos (v387)}")\'), ("en", r\'    _sec3s.append(r"\\section*{The three stress tests, taken together (v387)}")\')):\n'
     '    assert T0.count(_sec) == 1, ("a ancora da secao da v387 nao e\' unica", _lg)\n'
     '    _vl = \'    _sec3s.append(r"\\begin{center}\\small\\texttt{" + _tx3s(_t3s.get("verdict") or "TGL_THREE_STRESS_TESTS_V387__NOT_RECORDED_THIS_RUN__SECTION_COUNTED_ALONE__GATE_UNTOUCHED") + r"}\\end{center}")\' + CRLF\n'
     '    _i0 = T0.index(_sec); _i1 = T0.index(_vl, _i0); _prox = [T0.find(x_, _i0 + 1) for x_ in (r\'_sec3s.append(r"\\section*{The three stress tests\', r\'_sec3s.append(r"\\section*{Os três testes de estresse\')]\n'
     '    assert all(p_ < 0 or p_ > _i1 or p_ <= _i0 for p_ in _prox), ("a linha do veredito da v387 achada nao e\' a da secao", _lg)\n'
     '    edit(_i1, _i1, \'    _sec3s.append(_v411_p2_ao_lado_tex(core, "%s"))   # v411 (aditivo da gerencia c1, 12/11): o P2 AO LADO do texto selado da v387, com as quatro obrigacoes da F67\' % _lg + CRLF, "W13_p2_v387_" + _lg, "G_ARTIGO",\n'
     '         "artigo %s: a frase AO LADO do P2 na secao dos tres testes de estresse (v387); o texto selado da v387 fica." % _lg)\n'
     '_controles(RT_, "runtime_v411"); _controles([CONTR_H, TXT_H, specs, fontes, TOPO], "contrato/texto/specs/fontes/topo")\n'),
    ('"_v411_tex_misto", "_v411_topo_texto", "_v411_efeitos_tex", "_v411_estatuto_tex",', '"_v411_tex_misto", "_v411_topo_texto", "_v411_efeitos_tex", "_v411_p2_ao_lado_tex", "_v411_estatuto_tex",'),
    ('"efeitos": [_nsq["_v411_efeitos_tex"](_corq, "pt"), _nsq["_v411_efeitos_tex"](_corq, "en")],',
     '"efeitos": [_nsq["_v411_efeitos_tex"](_corq, "pt"), _nsq["_v411_efeitos_tex"](_corq, "en")], "efeitos_metodo": [_nsq["_v411_efeitos_tex"](_corq, "pt", "metodo"), _nsq["_v411_efeitos_tex"](_corq, "en", "metodo")],\n'
     '          "p2_v387": [_nsq["_v411_p2_ao_lado_tex"](_corq, "pt"), _nsq["_v411_p2_ao_lado_tex"](_corq, "en")],'),
    ('"runtime_executed", "does_not_gate_core", "n_checks_esperadas", "lei", "modelos")},',
     '"runtime_executed", "does_not_gate_core", "n_checks_esperadas", "lei", "modelos", "p2_ao_lado_da_v387")},'),
])

# ---- (5) o teste offline: o campo e o controle negativo da c14 (o veredito da v387 sem o token)
troca("_teste_h0dn_offline_v411.py", [
    ('ce = copy.deepcopy(core0); ce["external_ladder"]["n_theorems_expected"]',
     'c387 = copy.deepcopy(core0); c387["three_stress_tests_v387"]["verdict"] = c387["three_stress_tests_v387"]["verdict"].replace("P2_NOT_DETERMINED", "P2_OUTRA_COISA"); o = rodar(c387)\n'
     'neg["v387_sem_o_token_selado"] = {"recusou": not o["all_verified"] and o.get("p2_ao_lado_da_v387") is None, "falhas": [c["id"] for c in o["mechanics"]["checks"] if not c["ok"]]}\n'
     'ce = copy.deepcopy(core0); ce["external_ladder"]["n_theorems_expected"]'),
    ('tudo = (out["all_verified"] and not falhas and ',
     'P2 = out.get("p2_ao_lado_da_v387") or {}\nprint("p2 ao lado da v387:", P2)\n'
     'p2_ok = bool(P2 and P2.get("rotulo") and "P2_NOT_DETERMINED" in (P2.get("rotulo_selado_da_v387") or "") and "P2_NOT_DETERMINED" not in P2["rotulo"] and P2.get("canal") and P2.get("nota")\n'
     '             and neg["v387_sem_o_token_selado"]["falhas"] == ["c14"] and ((v.get("c14_inclui_o_p2_da_v387") or {}).get("ok") is True))\n'
     'tudo = (p2_ok and out["all_verified"] and not falhas and '),
    ('"controles_negativos": neg, "erro": out.get("error"), "TUDO_PASSOU": bool(tudo)}',
     '"controles_negativos": neg, "erro": out.get("error"), "p2_ao_lado_da_v387": P2, "p2_ok": p2_ok, "TUDO_PASSOU": bool(tudo)}'),
])
print("FEITO")
