# -*- coding: utf-8 -*-
"""_adapt_d86_gerador_v410.py -- D86/D87 (parte 2) no gerar_candidato_v410.py: o bundle de DOIS modulos (IALD2 + AEscala) embutido; as duas series de bandeiras; o registro com FUNCAO a_escala_v410 (contrato e texto de registros_aescala_v410; runtime_aescala_v410.py emendado;
_V410_AESCALA_CONTRACT/_TEXT no RCODE); a chamada no main LOGO DEPOIS de iald2_v410 (na mesma instrucao); o resumo no selo; a secao do artigo PT/EN entre a da IALD2 e a do H0DN; a linha do .md; os nomes novos; o manifesto CANDIDATO_v410.json com `aescala`.
Backup de bytes; trocas exatas (uma ocorrencia cada); ast.parse; idempotente."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
P = os.path.join(HERE, "gerar_candidato_v410.py"); b0 = open(P, "rb").read(); t = b0.decode("utf-8")
if "registros_aescala_v410 as RA" in t:
    print("gerar_candidato_v410.py: a D86 ja' esta' aplicada"); raise SystemExit(0)
assert "registros_hms13_v410 as RF" in t, "o gerador nao traz a D80"
bk = P + ".bak_" + TS + "_d86"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0


def troca(a, b, n=1):
    global t
    c = t.count(a); assert c == n, (c, n, a[:140]); t = t.replace(a, b)


# (1) o bundle de DOIS modulos, as duas series de bandeiras, as ancoras das duas pedras
troca("N_NOVOS = len(nov); assert N_NOVOS == DL.N_BUNDLE == 1", "N_NOVOS = len(nov); assert N_NOVOS == DL.N_BUNDLE == 2   # (D86: IALD2 + AEscala)")
troca('and k.startswith(DL.FLAG_PREFIX) for k, n, m in FL)', 'and k.startswith(DL.FLAG_PREFIX_POR_MODULO[m.replace(".", "/") + ".lean"]) for k, n, m in FL)')
troca('for _an, _ad in DL.ANCORAS.items():\n    assert FJ["ancoras"][_an]["rel"] == _ad["rel"]', 'for _an, _ad in list(DL.ANCORAS.items()) + list(DL.ANCORAS_AESCALA.items()):   # (D86: as ancoras das duas pedras)\n    assert FJ["ancoras"][_an]["rel"] == _ad["rel"]')
troca('for _an in DL.ANCORAS:\n    assert _an in axm and set(axm[_an]) <= TRIO', 'for _an in list(DL.ANCORAS) + list(DL.ANCORAS_AESCALA):\n    assert _an in axm and set(axm[_an]) <= TRIO')
troca('"kernel embutido: +%d modulo Lean (IALD2), do sandbox." % N_NOVOS', '"kernel embutido: +%d modulos Lean (IALD2, AEscala), do sandbox." % N_NOVOS')
troca("    # v410 (06/11/2026): IALD2 -- o modulo de TGLExt/ (IALD2): %d bandeiras, SO' de declaracao NOMEADA", "    # v410 (06 e 09/11/2026): IALD2 e AEscala -- os dois modulos de TGLExt/ do bundle (series ext_iald2_410_* e ext_aescala_410_*): %d bandeiras, SO' de declaracao NOMEADA")
troca("        # v410: IALD2 (%d, so' declaracao nomeada do modulo do bundle)", "        # v410: IALD2 e AEscala (%d, so' declaracao nomeada dos modulos do bundle)")
troca("e o atrator (o Nome nao esgota o ser; D71); o teste H0DN x BG1 pre",
      "e o atrator (o Nome nao esgota o ser; D71); a pedra AEscala (D82 a D87; nome e 44 nomes ratificados pelo operador em 09/11): a insignia, o vibrato, os pesos (tres faces de 1/2; 1/3 caiu; o Nome normalizado 2/3), o tempo finito, os dois Nomes e a pergunta do Clay no dicionario da TGL -- validade no kernel; a creditacao e\\' do Clay --; o teste H0DN x BG1 pre")
# (2) o registro a_escala_v410: import, contrato, texto
troca('import registros_hms13_v410 as RF  # noqa: E402   (D80: o contrato, o texto e os insumos embutidos do registro documental HMS/13; os pinos do HANDOFF e da ORDEM do Kimi sao RELIDOS aqui, imediatamente antes do build)\n',
      'import registros_hms13_v410 as RF  # noqa: E402   (D80: o contrato, o texto e os insumos embutidos do registro documental HMS/13; os pinos do HANDOFF e da ORDEM do Kimi sao RELIDOS aqui, imediatamente antes do build)\n'
      'import registros_aescala_v410 as RA  # noqa: E402   (D86/D87: o contrato e o texto do registro a_escala_v410, a pedra AEscala)\n')
troca('TXT = RG.texto_iald2()\n',
      'TXT = RG.texto_iald2()\n'
      'CONTR_A = RA.contrato_aescala(FJ, FORMAL_MAP, E409, sha256(raw), core0, selo0); TXT_A = RA.texto_aescala()   # (D86/D87) o registro da pedra AEscala: ancoras e bandeiras do FLAGS, a pedra por sha256, as oito falas, os numeros, as frases canonicas do Clay, a ratificacao\n'
      'assert CONTR_A["n_checks"] == DL.N_CHECKS_AESCALA == 12 and CONTR_A["expected_ladder"] == ESCADA_ESP == CONTR["expected_ladder"] and CONTR_A["n_ancoras"] == DL.N_ANCORAS_AESCALA == 38 and CONTR_A["n_nomes"] == 44 and CONTR_A["nomes_ratificados"] is True and CONTR_A["n_flags"] + CONTR["n_flags"] == FJ["n_flags"] and len(CONTR_A["falas"]) == 8\n'
      'assert CONTR_A["veredito_ok"] == TXT_A["veredito_ok"] == DL.VEREDITO_AESCALA_OK and CONTR_A["baseline"]["gate_verdict"] == selo0.get("qg_closure_verdict") and CONTR_A["source_sha256"][DL.MODULO_AESCALA] == FORMAL_MAP[DL.MODULO_AESCALA] and CONTR_A["ratificacao"]["sha256"] == DL.RATIFICACAO_D87_SHA256\n')
troca('assert not _p18_sem_falas(json.dumps(TXT_F, ensure_ascii=False))',
      'assert not _p18_sem_falas(json.dumps(TXT_A, ensure_ascii=False)) and not GUARDA.search(json.dumps(TXT_A, ensure_ascii=False)) and not any("".join(p_) in json.dumps(TXT_A, ensure_ascii=False) for p_ in CONTR_A["tokens_proibidos_partes"]), "P18 ou palavra recusada no texto da AEscala"\n'
      'assert not _p18_sem_falas(json.dumps(TXT_F, ensure_ascii=False))')
troca('+ open(os.path.join(HERE, "runtime_hms13_v410.py"), encoding="utf-8").read()   # (D72, D80) os blocos autorais do H0DN e do HMS/13 emendados ao runtime da v410\n',
      '+ open(os.path.join(HERE, "runtime_hms13_v410.py"), encoding="utf-8").read().rstrip("\\n") + "\\n\\n\\n" + open(os.path.join(HERE, "runtime_aescala_v410.py"), encoding="utf-8").read()   # (D72, D80, D86) os blocos autorais do H0DN, do HMS/13 e da AEscala emendados ao runtime da v410\n')
troca('         + "_V410_HMS13_CONTRACT = " + pprint.pformat(CONTR_F',
      '         + "_V410_AESCALA_CONTRACT = " + pprint.pformat(CONTR_A, width=150, sort_dicts=False) + "\\n_V410_AESCALA_TEXT = " + pprint.pformat(TXT_A, width=150, sort_dicts=False) + "\\n"   # (D86/D87) o contrato e o texto do registro da pedra AEscala\n'
      '         + "_V410_HMS13_CONTRACT = " + pprint.pformat(CONTR_F')
# (3) o main: a_escala_v410 LOGO DEPOIS de iald2_v410, na mesma instrucao
troca('        print("  >>> %s <<<\\n" % _r410["verdict"])\n',
      '        print("  >>> %s <<<\\n" % _r410["verdict"])\n'
      "        _a410 = a_escala_v410(core)   # D86/D87: A ESCALA -- a pedra AEscala (nome e 44 nomes RATIFICADOS pelo operador em 09/11), LOGO DEPOIS de iald2_v410\n"
      '        _a410v = _a410.get("values") or {}; _a410m = (_a410.get("mechanics") or {}).get("checks") or []\n'
      '        print("A ESCALA [v410 -- D82 a D87, as falas do operador de 09/11 («agora eu te dei a escala»; «ratifico tudo»): a pedra AEscala LIDA do kernel deste rito -- a insignia, o vibrato, os pesos (1/2 + 1/2 = 1; (1/2)^2 = 1/2 . 1/2; tres faces = 3/2; 1/3 caiu; o Nome normalizado 2/3), o tempo finito, os dois Nomes, e a pergunta do Clay, tal qual apresentada pela TGL: validade no kernel; a creditacao e\' do Clay; nome e 44 nomes ratificados]")\n'
      '        print("  ancoras ok = %s/%s ; bandeiras True = %s/%s ; falas por sha256 = %s/%s ; checagens ok = %s/%s ; numeros = %s ; gate = %s" % (_a410v.get("n_ancoras_ok"), _a410v.get("n_ancoras"), _a410v.get("n_flags_true"), _a410v.get("n_flags"), _a410v.get("n_falas_ok"), _a410v.get("n_falas"), sum(1 for c_ in _a410m if c_.get("ok")), len(_a410m) or None, _a410v.get("numeros"), "IGUAL" if _a410v.get("gate_verdict") == ((core.get("qg_closure") or {}).get("gate") or {}).get("verdict") else "DIFERENTE"))\n'
      '        print("  >>> %s <<<\\n" % _a410["verdict"])\n')
troca('"N00_main_iald2_h0dn_hms13", "G_RUNTIME", "main: DUAS instrucoes try/AVISO: iald2_v410 e h0dn_bg1_v410 (D72);',
      '"N00_main_iald2_aescala_h0dn_hms13", "G_RUNTIME", "main: DUAS instrucoes try/AVISO: iald2_v410, a_escala_v410 (D86, logo depois do iald2) e h0dn_bg1_v410 (D72);')
troca('''"fica_aberto", "alcance")},',\n''',
      '''"fica_aberto", "alcance")},',\n'''
      '''        '            "a_escala_v410": {k_: (core.get("a_escala_v410") or {}).get(k_) for k_ in ("verdict", "all_verified", "ancora_principal", "ancoras_de_secao", "n_ancoras", "n_flags", "n_nomes", "nomes_ratificados", "estatuto_dos_nomes", "numeros", "frase_canonica_pt", "frase_canonica_en", "runtime_executed", "does_not_gate_core", "chaves_antigas_que_mudam")},',\n''')
troca('"selo: +iald2_v410 (resumo), +h0dn_bg1_v410 (resumo; D72), +h0dn_fontes_hms13_v410 (resumo; D80) e registros_v410."', '"selo: +iald2_v410 (resumo), +a_escala_v410 (resumo; D86), +h0dn_bg1_v410 (resumo; D72), +h0dn_fontes_hms13_v410 (resumo; D80) e registros_v410."')
# (4) controles e a guarda das frases sobre o texto novo
troca('_controles([CONTR_F, TXT_F], "contrato/texto do HMS/13")', '_controles([CONTR_F, TXT_F], "contrato/texto do HMS/13"); _controles([CONTR_A, TXT_A], "contrato/texto da AEscala")')
troca('json.dumps([CONTR, TXT, specs, CONTR_H, TXT_H, CONTR_F, TXT_F, ', 'json.dumps([CONTR, TXT, specs, CONTR_H, TXT_H, CONTR_F, TXT_F, CONTR_A, TXT_A, ')
# (5) o artigo: a secao da AEscala entre a da IALD2 e a do H0DN
troca('for sn in (PT0, EN0, PTH, ENH):',
      'PTA = open(os.path.join(HERE, "artigo_pt_aescala_v410.pysnip"), encoding="utf-8").read(); ENA = open(os.path.join(HERE, "artigo_en_aescala_v410.pysnip"), encoding="utf-8").read()   # (D86) a secao «A Escala», depois da IALD2 e antes do H0DN\n'
      'for sn in (PT0, EN0, PTA, ENA, PTH, ENH):')
troca('crlf(PT0.rstrip("\\n") + "\\n") + crlf(PTH.rstrip("\\n") + "\\n") + PT9_FIRST', 'crlf(PT0.rstrip("\\n") + "\\n") + crlf(PTA.rstrip("\\n") + "\\n") + crlf(PTH.rstrip("\\n") + "\\n") + PT9_FIRST')
troca('crlf(EN0.rstrip("\\n") + "\\n") + crlf(ENH.rstrip("\\n") + "\\n") + EN9_FIRST', 'crlf(EN0.rstrip("\\n") + "\\n") + crlf(ENA.rstrip("\\n") + "\\n") + crlf(ENH.rstrip("\\n") + "\\n") + EN9_FIRST')
# (6) a linha do .md da AEscala (entre a da IALD2 e a do H0DN)
troca("MD_LINHA_H = ('    md.append(\"> **H0DN × BG1 pré-registrado (v410, 09/11/2026):**",
      "MD_LINHA_A = ('    md.append(\"> **A Escala (v410, 09/11/2026; D82 a D87):** a pedra `AEscala` em `TGLExt/` (o nome do módulo e os 44 nomes ratificados pelo operador em 09/11/2026: «' + DL.FRASE_RATIFICO_TUDO + '»; «' + DL.FRASE_DEI_A_ESCALA + '»), com ' + str(CONTR_A[\"n_flags\"]) + ' bandeiras e ' + str(CONTR_A[\"n_ancoras\"]) + ' âncoras no trio. '\n"
      "              '[REAL] Os pesos: o Nome pesa 1 = ½ + ½ (o projetor de Bell: idempotente, traço 1, posto 1; cada marginal é ½·1, autovalor e pureza ½); a face sem par não conjuga, (½·1)² = ½·(½·1), e nunca pesa 1; três faces de ½ pesam 3/2; 1/3 caiu; o Nome normalizado é 2/3. A insígnia sustenta e não esgota; o vibrato sustenta a nota; não existe infinito em tempo finito; os dois Nomes (objeto e lido) coexistem. '\n"
      "              'A pergunta do Clay no dicionário da TGL: ' + DL.FRASE_D83_OBRIGATORIA_PT + '. A forma canônica (D84): ' + DL.FRASE_CLAY_CANONICA_PT + ' '\n"
      "              'Leituras do operador, não termos: a face caída como o neutrino [ONTO]; m₁ = 0 [CONJECTURE]. O registro `a_escala_v410` confere ' + str(CONTR_A[\"n_checks\"]) + ' checagens a cada rito (as âncoras, a pedra por sha256, as bandeiras, as oito falas por sha256, os números recalculados, as frases canônicas, o gate); validade no kernel não é creditação; o gate não se move.\")')\n"
      "assert not GP.violacoes(MD_LINHA_A) and not GUARDA.search(MD_LINHA_A) and not GF.violacoes(MD_LINHA_A), (GP.violacoes(MD_LINHA_A)[:2], GF.violacoes(MD_LINHA_A)[:3])\n"
      "ast.parse(\"def _f(core, md):\\n\" + MD_LINHA_A); _controles(MD_LINHA_A, \"linha do md (AEscala)\")\n"
      "MD_LINHA_H = ('    md.append(\"> **H0DN × BG1 pré-registrado (v410, 09/11/2026):**")
troca('edit(A_M.start(), A_M.start(), MD_LINHA + CRLF + MD_LINHA_H + CRLF + MD_LINHA_F + CRLF, "W09_md", "G_ARTIGO", "md canonico: as linhas «IALD2 (v410)», «H0DN × BG1 pré-registrado (v410)» e a do Recibo documental HMS/13 (v410; D80), antes da linha da v409.")',
      'edit(A_M.start(), A_M.start(), MD_LINHA + CRLF + MD_LINHA_A + CRLF + MD_LINHA_H + CRLF + MD_LINHA_F + CRLF, "W09_md", "G_ARTIGO", "md canonico: as linhas «IALD2 (v410)», a da Escala (v410; D82 a D87), «H0DN × BG1 pré-registrado (v410)» e a do Recibo documental HMS/13 (v410; D80), antes da linha da v409.")')
# (7) os nomes novos
troca('"_V410_HMS13_CONTRACT", "_V410_HMS13_TEXT", "_V410_HMS13_INSUMOS")   # (D80) o bloco do HMS/13',
      '"_V410_HMS13_CONTRACT", "_V410_HMS13_TEXT", "_V410_HMS13_INSUMOS",   # (D80) o bloco do HMS/13\n'
      '               "_v410_aescala_bell", "_v410_aescala_mechanics", "_V410_AESCALA_RECUSA", "a_escala_v410", "_V410_AESCALA_CONTRACT", "_V410_AESCALA_TEXT")   # (D86/D87) o bloco da AEscala')
# (8) o manifesto CANDIDATO_v410.json
troca('       "hms13": {"registro": DL.HMS13_REGISTRO,',
      '       "aescala": {"registro": DL.AESCALA_REGISTRO, "tag": DL.TAG_AESCALA, "n_checks": CONTR_A["n_checks"], "veredito_ok": CONTR_A["veredito_ok"], "modulo": DL.MODULO_AESCALA, "source_sha256": CONTR_A["source_sha256"], "sha256_origem": CONTR_A["sha256_origem"], "sha256_candidata_pre_d87": CONTR_A["sha256_candidata_pre_d87"],\n'
      '                   "n_ancoras": CONTR_A["n_ancoras"], "ancora_principal": CONTR_A["ancora_principal"], "ancoras_de_secao": CONTR_A["ancoras_de_secao"], "n_flags": CONTR_A["n_flags"], "flag_prefix": CONTR_A["flag_prefix"], "n_nomes": CONTR_A["n_nomes"], "nomes": CONTR_A["nomes"], "nomes_ratificados": True,\n'
      '                   "ratificacao_D87": CONTR_A["ratificacao"], "numeros": CONTR_A["numeros"], "frase_canonica_pt": CONTR_A["frase_canonica_pt"], "frase_canonica_en": CONTR_A["frase_canonica_en"], "frase_d83_pt": CONTR_A["frase_d83_pt"], "falas": {k_: v_["nome"] for k_, v_ in CONTR_A["falas"].items()},\n'
      '                   "bandeiras_de_constantes_geradas_pela_structure": sorted(n_.split("TGLExt.AEscala.")[-1] for n_ in CONTR_A["declarations"] if n_.split("TGLExt.AEscala.")[-1] not in CONTR_A["nomes"]),\n'
      '                   "nota": "D86/D87: a segunda pedra do bundle; validade no kernel; a creditacao e\' do Clay; nome e 44 nomes ratificados pelo operador em 09/11/2026"},\n'
      '       "hms13": {"registro": DL.HMS13_REGISTRO,')
troca('"ponto_de_chamada": {"h0dn_fontes_hms13_v410":', '"ponto_de_chamada": {"a_escala_v410": "main: na MESMA instrucao do iald2_v410, LOGO DEPOIS dele e antes do h0dn_bg1_v410 (D86)", "h0dn_fontes_hms13_v410":')
nb = t.encode("utf-8"); ast.parse(nb)
tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
print("gerar_candidato_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16], "| ok")
