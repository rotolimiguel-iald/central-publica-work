# -*- coding: utf-8 -*-
"""_adapt_exame_pontos_v411.py -- (claude-construtor-v411, fork C, 12/11/2026) monta exame_pontos_v411.py a partir do ORIGINAL ..\\v410\\exame_pontos_v410.py (nao da copia bumpada), com trocas DITAS:
(a) o delta da v411; o candidato/artefato por DL.CANDIDATO_ARQ; imp_<sha16> FORA de work (DL.RODADA_PAI); a saida EXAME_PONTOS_<sha16>.json em DL.saida; a base e' a v410 selada;
(b) os pontos da v410 (4g iald2, 4h h0dn_bg1_v410, 4h2 a_escala, 4h3 hms13) e os falsos deles viram HERANCA: os nomes da v410 por DL.D10.*, as bandeiras pelo FLAGS da v410 (a v411 nao tem bandeira nova);
(c) a ordem do main ganha a instrucao da v411 (h0dn_bg1_v411 + _v411_rodar_specs) LOGO DEPOIS da do hms13 e IMEDIATAMENTE antes de emit_figures; (d) o ponto NOVO (4i) do h0dn_bg1_v411 (16 checagens; as duas linhas;
o campo p2_ao_lado_da_v387; o veto medido; o gate); (e) o selo com h0dn_bg1_v411 e registros_v411; os nao-verdes da v411; a troca dita vira troca_dita_v411 (nada declarado, nada mudado em texto).
Backup de BYTES do destino antes; cada ancora unica. uso: python -B -X utf8 _adapt_exame_pontos_v411.py"""
import ast, datetime, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "v410", "exame_pontos_v410.py")
DST = os.path.join(HERE, "exame_pontos_v411.py")
t = open(SRC, "rb").read().decode("utf-8"); assert "\r" not in t


def troca(a_, n_, cnt=1):
    global t
    assert t.count(a_) == cnt, (a_[:110], t.count(a_))
    t = t.replace(a_, n_)


# ---- (b) as regioes da v410 viram heranca (DL.X -> DL.D10.X; A.flags -> o FLAGS da v410)
def heranca(ini_, fim_):
    global t
    i_ = t.index(ini_); j_ = t.index(fim_, i_)
    seg_ = t[i_:j_]
    seg_ = re.sub(r"\bDL\.(?!D\d+\b|V4\d\d\b)", "DL.D10.", seg_)
    seg_ = seg_.replace("A.flags", "_FLAGS10")
    t = t[:i_] + seg_ + t[j_:]


heranca("# (4g) [v410] o PONTO DE CHAMADA REAL do iald2_v410", 'R["chaves_novas_no_core"] = sorted(set(core) - set(antes))')
heranca('pia = R["ponto_iald2"]   # (4g) o ponto NOVO da v410', 'if (R.get("pasta_vedada_kimi_no_exame")')
l1 = t.split("\n", 1)[0]; assert l1.startswith("# -*- coding")
troca(l1 + "\n", l1 + "\n# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork C)] montado por _adapt_exame_pontos_v411.py do ORIGINAL v410/exame_pontos_v410.py: o ponto NOVO e' o do h0dn_bg1_v411 (4i), na instrucao do main LOGO DEPOIS da do hms13 e"
      " IMEDIATAMENTE antes de emit_figures; os pontos da v410 (4g, 4h, 4h2, 4h3) viram HERDADOS (DL.D10, FLAGS da v410); nenhum modulo novo; imp_ e a saida fora de work.\n")
troca('"""exame_pontos_v410.py -- re-execucao', '"""exame_pontos_v411.py -- (v411: o ponto novo e\' o do h0dn_bg1_v411, depois do bloco da v410; os da v410 herdados) re-execucao')
troca("import delta_v410 as DL  # noqa: E402", "import delta_v411 as DL  # noqa: E402")
troca('ap.add_argument("--candidato", default=os.path.join(H, DL.CANDIDATO))', 'ap.add_argument("--candidato", default=DL.CANDIDATO_ARQ)')
troca('IMP = A.imp or os.path.join(H, "imp_" + SHA[:16]); os.makedirs(IMP, exist_ok=True)', 'IMP = A.imp or os.path.join(DL.RODADA_PAI, "imp_" + SHA[:16]); os.makedirs(IMP, exist_ok=True)   # (v411, D135: fora de work)')
troca('SAIDA = A.saida or os.path.join(H, "EXAME_PONTOS_%s.json" % SHA[:16])', 'SAIDA = A.saida or DL.saida("EXAME_PONTOS_%s.json" % SHA[:16])\n_FLAGS10 = os.path.join(DL.V410, DL.D10.KERNEL_DIR, "FLAGS_v410.json")   # (v411) as bandeiras da v410, para os pontos HERDADOS da v410')
troca('CORE0P = A.core0 or os.path.join(H, DL.BASE_DIR, "um_absoluto.json")   # a v409 SELADA (copia de bytes)', 'CORE0P = A.core0 or os.path.join(H, DL.BASE_DIR, "um_absoluto.json")   # a v410 SELADA (copia de bytes)')
troca('R["witness_layers_canonical_full_witness_term_constructed"] = {"da_base_v409_selada": _wl_antes,', 'R["witness_layers_canonical_full_witness_term_constructed"] = {"da_base_v410_selada": _wl_antes,')
troca("list(um._V409_REGISTROS_FUNCAO) + list(um._V409_NOMES_REGISTROS):", "list(um._V409_REGISTROS_FUNCAO) + list(um._V409_NOMES_REGISTROS) + list(um._V410_REGISTROS_FUNCAO) + list(um._V410_NOMES_REGISTROS) + list(um._V411_REGISTROS_FUNCAO) + list(um._V411_NOMES_REGISTROS):")   # (v411) os da v410 sao RECRIADOS pelo bloco (heranca) e os da v411 sao novos
# ---- (c) a ordem do main
troca('ihm = [i for i, s_ in enumerate(unp) if "h0dn_fontes_hms13_v410(core)" in s_]   # (v410, D80) a SEGUNDA instrucao da v410: o recibo HMS/13 + os specs da v410\n',
      'ihm = [i for i, s_ in enumerate(unp) if "h0dn_fontes_hms13_v410(core)" in s_]   # (v410, D80) a SEGUNDA instrucao da v410: o recibo HMS/13 + os specs da v410\n'
      'ih11 = [i for i, s_ in enumerate(unp) if "h0dn_bg1_v411(core)" in s_]   # (v411) o ponto NOVO: o h0dn_bg1_v411 + os specs da v411, LOGO DEPOIS do bloco da v410\n')
troca(" and len(ihm) == 1 and ihm[0] == iia[0] + 1 and ihm[0] + 1 == i1, (", " and len(ihm) == 1 and ihm[0] == iia[0] + 1 and len(ih11) == 1 and ih11[0] == ihm[0] + 1 and ih11[0] + 1 == i1, (")
troca("-> [h0dn_fontes_hms13_v410, specs v410] -> emit_figures nao e' a das instrucoes do main\", ifch, ipc, itt, itu, iia, ihm, i1)",
      "-> [h0dn_fontes_hms13_v410, specs v410] -> [h0dn_bg1_v411, specs v411] -> emit_figures nao e' a das instrucoes do main\", ifch, ipc, itt, itu, iia, ihm, ih11, i1)")
troca("ihm = ihm[0]\n", "ihm = ihm[0]\nih11 = ih11[0]\n")
troca('"logo_antes_da_instrucao_do_hms13_e_dos_specs": iia + 1 == ihm and ihm + 1 == i1,', '"logo_antes_da_instrucao_do_hms13_e_dos_specs": iia + 1 == ihm and ihm + 1 == ih11,')
troca('"logo_antes_do_emit_figures": ihm + 1 == i1,', '"logo_antes_da_instrucao_da_v411": ihm + 1 == ih11,')
troca('not phf.get("logo_antes_do_emit_figures")', 'not phf.get("logo_antes_da_instrucao_da_v411")')
# ---- (d) o ponto NOVO (4i)
troca('out["core.h0dn_fontes_hms13_v410"] = {"all_verified": hf.get("all_verified"), "verdict": str(hf.get("verdict"))[:300], "falhas": R["ponto_hms13"]["mecanica"]["falhos"]}\n',
      'out["core.h0dn_fontes_hms13_v410"] = {"all_verified": hf.get("all_verified"), "verdict": str(hf.get("verdict"))[:300], "falhas": R["ponto_hms13"]["mecanica"]["falhos"]}\n'
      '# (4i) [v411] o PONTO DE CHAMADA REAL do h0dn_bg1_v411 (executado dentro do bloco acima): a instrucao do main LOGO DEPOIS da do hms13 (o bloco da v410 inteiro ja\' rodou) e IMEDIATAMENTE antes de emit_figures; o teste aberto uma vez,\n'
      '#      RECALCULADO dos bytes embutidos; as duas linhas juntas (o primario sob o modelo de erros publicado e as Cefeidas livres ao lado); o campo p2_ao_lado_da_v387; o veto medido; o gate congelado; nenhuma chave antiga mudada\n'
      'h11 = core.get(DL.FECHO_REGISTRO) or {}; h11v = h11.get("values") or {}; _CP11 = um._V411_H0DN_CONTRACT; _ui11 = unp[ih11]\n'
      '_nc387 = lambda v_: re.sub(r"CORE_\\d+_TGL_VERDICTS_CONTAINING_\\d+_NOT_FALSIFIED_\\d+_INCONCLUSIVE_\\d+_AWAITING_OVERLAPPING_\\d+_FALSIFIED_SUBSTRINGS_NAMED", "<CONTAGENS>", v_)\n'
      'R["ponto_h0dn_v411"] = {"indice_no_main": ih11, "linha": main.body[ih11].lineno, "logo_depois_da_instrucao_do_hms13": ih11 == ihm + 1, "logo_antes_do_emit_figures": ih11 + 1 == i1, "dentro_do_bloco_executado": i0 <= ih11 < i1,\n'
      '                        "chama_tambem_os_specs_v411": "_v411_rodar_specs(core)" in _ui11 and _ui11.find("h0dn_bg1_v411(core)") < _ui11.find("_v411_rodar_specs(core)"), "verdict": h11.get("verdict"), "all_verified": h11.get("all_verified"),\n'
      '                        "runtime_executed": h11.get("runtime_executed"), "observed_vector_read": h11.get("observed_vector_read"), "opened_once": h11.get("opened_once"), "does_not_gate_core": h11.get("does_not_gate_core"), "beta_ok": h11.get("beta_ok"),\n'
      '                        "mecanica": {"passed": (h11.get("mechanics") or {}).get("passed"), "n_checks": (h11.get("mechanics") or {}).get("n_checks"), "falhos": [c_.get("id") for c_ in ((h11.get("mechanics") or {}).get("checks") or []) if not c_.get("ok")]},\n'
      '                        "ramo_primario": (h11v.get("primario") or {}).get("ramo"), "ramo_cefeidas_livres": (h11v.get("cefeidas_livres") or {}).get("ramo"), "cabeca_do_teste": h11.get("cabeca_do_teste"), "outcome": h11.get("outcome"),\n'
      '                        "linha_ao_lado_cefeidas_livres": bool(h11.get("linha_ao_lado_cefeidas_livres")), "n_ressalvas_secao8": len(h11.get("ressalvas_secao8") or []), "gate_verdict": h11v.get("gate_verdict"), "escada": h11v.get("escada"),\n'
      '                        "sob_pasta_vedada": h11v.get("sob_pasta_vedada"), "n_caminhos_tocados": h11v.get("n_caminhos_tocados"), "p2_ao_lado_da_v387": h11.get("p2_ao_lado_da_v387"), "c14_inclui_o_p2_da_v387": h11v.get("c14_inclui_o_p2_da_v387"),\n'
      '                        "v387_veredito_selado_igual_ao_da_base": _nc387(str((core.get(DL.P2_REGISTRO_SELADO) or {}).get("verdict"))) == _nc387(str((core0.get(DL.P2_REGISTRO_SELADO) or {}).get("verdict"))) and DL.P2_TOKEN_SELADO in str((core.get(DL.P2_REGISTRO_SELADO) or {}).get("verdict")),   # (as contagens CORE_n_ do instante normalizadas, como no ensaio)\n'
      '                        "contrato": {"n_checks": _CP11["n_checks"], "ramo_primario": _CP11["esperado_do_resultado"]["ramo_primario"], "ramo_cefeidas_livres": _CP11["esperado_do_resultado"]["ramo_cefeidas_livres"], "gate_verdict": _CP11["baseline"]["gate_verdict"], "escada": _CP11["baseline"]["escada"], "pasta_vedada": _CP11["pasta_vedada"]}}\n'
      'out["core." + DL.FECHO_REGISTRO] = {"all_verified": h11.get("all_verified"), "verdict": str(h11.get("verdict"))[:300], "falhas": R["ponto_h0dn_v411"]["mecanica"]["falhos"]}\n')
# ---- (e) a troca dita, os nao verdes, o selo
troca("# (v410) NAO HA TROCA DITA: o candidato nao declara nenhuma (CANDIDATO_v410.json nao tem `troca_dita_v410`)", "# (v411) NAO HA TROCA DITA: o candidato nao declara nenhuma (o manifesto da v411 nao tem `troca_dita_v411`)")
troca('_CMD = json.load(open(os.path.join(H, "CANDIDATO_v410.json"), encoding="utf-8")); _TROCA = _CMD.get("troca_dita_v410", [])', '_CMD = json.load(open(DL.MANIFESTO_ARQ, encoding="utf-8")); _TROCA = _CMD.get("troca_dita_v411", [])')
troca('R["troca_dita_v410"] = {"declarada_no_candidato": _TROCA, "candidato_declara_a_chave": "troca_dita_v410" in _CMD,', 'R["troca_dita_v411"] = {"declarada_no_candidato": _TROCA, "candidato_declara_a_chave": "troca_dita_v411" in _CMD,')
troca('R["troca_dita_v410"]["ok"] = bool(R["troca_dita_v410"]["mudaram_com_texto"] == sorted(_TROCA) == [] and "troca_dita_v410" not in _CMD and _num(_nc(str(R["troca_dita_v410"]["rede_fock_v394_depois"]))) == _num(_nc(str(_V409_RED))) and "JOINT_CERTIFICATE_INHABITED_V406" in str(R["troca_dita_v410"]["rede_fock_v394_depois"]))',
      'R["troca_dita_v411"]["ok"] = bool(R["troca_dita_v411"]["mudaram_com_texto"] == sorted(_TROCA) == [] and "troca_dita_v411" not in _CMD and _num(_nc(str(R["troca_dita_v411"]["rede_fock_v394_depois"]))) == _num(_nc(str(_V409_RED))) and "JOINT_CERTIFICATE_INHABITED_V406" in str(R["troca_dita_v411"]["rede_fock_v394_depois"]))')
troca('if R["troca_dita_v410"]["ok"] is not True: falsos.append("troca_dita_v410")', 'if R["troca_dita_v411"]["ok"] is not True: falsos.append("troca_dita_v411")')
troca('                   "v410_iald2_e_specs": [k for k in list(um._V410_REGISTROS_FUNCAO) + list(um._V410_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n',
      '                   "v410_iald2_e_specs": [k for k in list(um._V410_REGISTROS_FUNCAO) + list(um._V410_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],   # (os da v410: HERDADOS na v411)\n'
      '                   "v411_h0dn_e_specs": [k for k in list(um._V411_REGISTROS_FUNCAO) + list(um._V411_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n')
troca('                 **{n_: {x: (seal.get(n_) or {}).get(x) for x in ("verdict", "all_verified")} for n_ in DL.REGISTROS_FUNCAO}, "registros_v410": {n_: ((seal.get("registros_v410") or {}).get(n_) or {}).get("all_verified") for n_ in um._V410_NOMES_REGISTROS}}',
      '                 **{n_: {x: (seal.get(n_) or {}).get(x) for x in ("verdict", "all_verified")} for n_ in DL.REGISTROS_FUNCAO_V410}, "registros_v410": {n_: ((seal.get("registros_v410") or {}).get(n_) or {}).get("all_verified") for n_ in um._V410_NOMES_REGISTROS},\n'
      '                 DL.FECHO_REGISTRO: {x: (seal.get(DL.FECHO_REGISTRO) or {}).get(x) for x in ("verdict", "all_verified", "cabeca_do_teste", "outcome", "linha_ao_lado_cefeidas_livres", "p2_ao_lado_da_v387")}, "registros_v411": {n_: ((seal.get("registros_v411") or {}).get(n_) or {}).get("all_verified") for n_ in um._V411_NOMES_REGISTROS}}')
# os falsos do ponto novo
troca('if (R.get("pasta_vedada_kimi_no_exame") or {}).get("lidos_sob_a_pasta")',
      'p11 = R["ponto_h0dn_v411"]   # (4i) o ponto NOVO da v411: o teste aberto, recalculado; as duas linhas; o P2 ao lado; o veto; o gate\n'
      'if (p11.get("all_verified") is not True or p11.get("runtime_executed") is not True or p11.get("observed_vector_read") is not True or p11.get("opened_once") is not True or p11.get("does_not_gate_core") is not True or p11.get("beta_ok") is not True\n'
      '        or not p11.get("dentro_do_bloco_executado") or not p11.get("logo_depois_da_instrucao_do_hms13") or not p11.get("logo_antes_do_emit_figures") or not p11.get("chama_tambem_os_specs_v411")\n'
      '        or not str(p11.get("verdict") or "").startswith(DL.VEREDITO_OK_PREFIXO) or not str(p11.get("verdict") or "").endswith(DL.VEREDITO_SUFIXO) or (p11.get("mecanica") or {}).get("passed") is not True or (p11.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS_FECHO or (p11.get("mecanica") or {}).get("falhos")\n'
      '        or p11.get("ramo_primario") != p11["contrato"]["ramo_primario"] or p11.get("ramo_cefeidas_livres") != p11["contrato"]["ramo_cefeidas_livres"] or not p11.get("cabeca_do_teste") or not p11.get("outcome") or p11.get("linha_ao_lado_cefeidas_livres") is not True or p11.get("n_ressalvas_secao8") != 7\n'
      '        or p11.get("gate_verdict") != p11["contrato"]["gate_verdict"] or p11.get("gate_verdict") != pia.get("gate_verdict") or p11.get("escada") != p11["contrato"]["escada"] or p11.get("sob_pasta_vedada") or p11["contrato"]["pasta_vedada"] != DL.H0DN_PASTA_VEDADA_V410\n'
      '        or not isinstance(p11.get("p2_ao_lado_da_v387"), dict) or DL.P2_TOKEN_SELADO not in str((p11.get("p2_ao_lado_da_v387") or {}).get("rotulo_selado_da_v387")) or DL.P2_TOKEN_SELADO in str((p11.get("p2_ao_lado_da_v387") or {}).get("rotulo"))\n'
      '        or (p11.get("c14_inclui_o_p2_da_v387") or {}).get("ok") is not True or p11.get("v387_veredito_selado_igual_ao_da_base") is not True): falsos.append("ponto_h0dn_v411")\n'
      'if (R.get("pasta_vedada_kimi_no_exame") or {}).get("lidos_sob_a_pasta")')
t = t.replace("python -B -X utf8 exame_pontos_v410.py", "python -B -X utf8 exame_pontos_v411.py")
ast.parse(t)
assert "DL.D10.D10." not in t
b0 = open(DST, "rb").read()
bak = DST + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_forkc"; open(bak, "wb").write(b0); assert open(bak, "rb").read() == b0
nb = t.encode("utf-8"); open(DST + ".tmp", "wb").write(nb); assert os.path.getsize(DST + ".tmp") == len(nb); os.replace(DST + ".tmp", DST)
print("ok", DST, len(b0), "->", len(nb))
