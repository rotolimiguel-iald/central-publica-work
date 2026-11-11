# -*- coding: utf-8 -*-
"""_adapt_d80_gerador_v410.py -- D80 no gerar_candidato_v410.py: o TERCEIRO registro com FUNCAO (h0dn_fontes_hms13_v410): import de registros_hms13_v410; o contrato/texto/insumos do HMS/13 (os pinos do HANDOFF e da ORDEM do Kimi RELIDOS no build; a guarda numerica);
o runtime emendado (runtime_hms13_v410.py); o RCODE emite _V410_HMS13_CONTRACT/_TEXT/_INSUMOS; o main ganha uma SEGUNDA instrucao try (o hms13 le core["h0dn_bg1_v410"], gravado na instrucao anterior: a guarda de ordem exige a atribuicao ANTES da chamada)
com o hms13 e os registros por spec; o selo ganha o resumo do hms13; a terceira linha do .md; os nomes novos; o manifesto CANDIDATO_v410.json ganha `hms13` e `fontes_hms13_embutidas` (caminho + sha256 + bytes: o controle de que o build leu SO' os seis arquivos documentais da pasta do Kimi).
Backup de bytes; trocas exatas (uma ocorrencia cada); ast.parse; idempotente (pula se ja' aplicado)."""
import ast, datetime, hashlib, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
P = os.path.join(HERE, "gerar_candidato_v410.py"); b0 = open(P, "rb").read()
t = b0.decode("utf-8")
if "registros_hms13_v410 as RF" in t:
    print("gerar_candidato_v410.py: a D80 ja' esta' aplicada"); raise SystemExit(0)
bk = P + ".bak_" + TS + "_d80"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
NL = "\r\n" if b0.count(b"\r\n") > b0.count(b"\n") // 2 else "\n"
assert NL == "\n", "o gerador e' LF"


def troca(a, b, n=1):
    global t
    c = t.count(a); assert c == n, (c, n, a[:140]); t = t.replace(a, b)


# (1) import
troca('import registros_h0dn_v410 as RH  # noqa: E402   (D72: o contrato, o texto e os insumos embutidos do registro H0DN)\n',
      'import registros_h0dn_v410 as RH  # noqa: E402   (D72: o contrato, o texto e os insumos embutidos do registro H0DN)\n'
      'import registros_hms13_v410 as RF  # noqa: E402   (D80: o contrato, o texto e os insumos embutidos do registro documental HMS/13; os pinos do HANDOFF e da ORDEM do Kimi sao RELIDOS aqui, imediatamente antes do build)\n')
# (2) o contrato do HMS/13 (depois do contrato do H0DN, de que e' posterior)
troca('CONTR_H = RH.contrato_h0dn(core0, selo0); TXT_H = RH.texto_h0dn(); INS_H = RH.insumos_embutidos()   # (D72) o registro H0DN: contrato (pinos lidos), texto, insumos embutidos em base64\n',
      'CONTR_H = RH.contrato_h0dn(core0, selo0); TXT_H = RH.texto_h0dn(); INS_H = RH.insumos_embutidos()   # (D72) o registro H0DN: contrato (pinos lidos), texto, insumos embutidos em base64\n'
      'CONTR_F = RF.contrato_hms13(core0, selo0, CONTR_H); TXT_F = RF.texto_hms13(); INS_F = RF.insumos_embutidos_hms13()   # (D80) o registro documental HMS/13: os pinos do HANDOFF e da ORDEM do Kimi RELIDOS agora (fail-closed), os quatro artefatos embutidos em base64, a guarda numerica (BLOQUEIO_HMS13_v410.json se um campo proibido aparecer), a ratificacao por sha256\n'
      'assert CONTR_F["n_checks"] == DL.N_CHECKS_HMS13 == 12 and CONTR_F["baseline"]["gate_verdict"] == selo0.get("qg_closure_verdict") and set(CONTR_F["insumos"]) == set(INS_F) == {n_ for n_, _ in DL.HMS13_EMBUTIDOS} and all(INS_F[k_]["sha256"] == v_["sha256"] and INS_F[k_]["bytes"] == v_["bytes"] for k_, v_ in CONTR_F["insumos"].items())\n'
      'assert CONTR_F["campos"] == DL.HMS13_CAMPOS and CONTR_F["guarda_numerica_no_build"]["ok"] is True and not CONTR_F["guarda_numerica_no_build"]["proibidos"] and not CONTR_F["guarda_numerica_no_build"]["listas_numericas"] and CONTR_F["le_em_rito"] is False and CONTR_F["observed_vector_read"] is False and len(CONTR_F["pinos_build"]) == 6\n'
      'assert CONTR_F["veredito_ok"] == DL.VEREDITO_HMS13_OK and not any(t_ in CONTR_F["veredito_ok"] for t_ in DL.TOKENS_PROIBIDOS_V410 + DL.TOKENS_PROIBIDOS_H0DN) and CONTR_F["aditivo_posterior_ao_freeze_r2"] is True and CONTR_F["h0dn"]["freeze_r2_sha256"] == CONTR_H["insumos"]["FREEZE_R2.json"]["sha256"]\n'
      'assert "vibrato" not in json.dumps([CONTR_F, TXT_F], ensure_ascii=False).lower() and not any(n_ in json.dumps([CONTR_F, TXT_F], ensure_ascii=False) for n_ in DL.H0DN_NOMES_VEDADOS), "D80/D65: o texto do HMS/13 cita o nome do arquivo da fala ou um nome vedado"\n')
# (3) o runtime emendado e o RCODE
troca('RUNTIME_SRC = open(os.path.join(HERE, "runtime_v410.py"), encoding="utf-8").read().rstrip("\\n") + "\\n\\n\\n" + open(os.path.join(HERE, "runtime_h0dn_v410.py"), encoding="utf-8").read()   # (D72) o bloco autoral do H0DN emendado ao runtime da v410\n',
      'assert not _p18_sem_falas(json.dumps(TXT_F, ensure_ascii=False)) and not GUARDA.search(json.dumps(TXT_F, ensure_ascii=False)) and not GP.violacoes(json.dumps({k_: TXT_F[k_] for k_ in ("estatuto", "escopo", "limites", "diz", "nao_diz", "o_que_falta", "ressalvas")}, ensure_ascii=False)), "P18 ou palavra recusada no texto do HMS/13"\n'
      'RUNTIME_SRC = open(os.path.join(HERE, "runtime_v410.py"), encoding="utf-8").read().rstrip("\\n") + "\\n\\n\\n" + open(os.path.join(HERE, "runtime_h0dn_v410.py"), encoding="utf-8").read().rstrip("\\n") + "\\n\\n\\n" + open(os.path.join(HERE, "runtime_hms13_v410.py"), encoding="utf-8").read()   # (D72, D80) os blocos autorais do H0DN e do HMS/13 emendados ao runtime da v410\n')
troca('         "_V410_NOMES_REGISTROS = " + repr(spec_nomes)',
      '         + "_V410_HMS13_CONTRACT = " + pprint.pformat(CONTR_F, width=150, sort_dicts=False) + "\\n_V410_HMS13_TEXT = " + pprint.pformat(TXT_F, width=150, sort_dicts=False) + "\\n_V410_HMS13_INSUMOS = " + repr(INS_F) + "   # (D80) os quatro artefatos documentais HMS/13 EMBUTIDOS em base64, pinados por sha256 lido no build (HANDOFF e ORDEM do Kimi relidos); decodificados e conferidos a cada rito; em rito nada e\' lido da pasta do Kimi\\n"\n'
      '         "_V410_NOMES_REGISTROS = " + repr(spec_nomes)')
# (4) o main: a instrucao do iald2/h0dn fecha; a SEGUNDA instrucao traz o hms13 e os specs
troca("    try:   # v410: IALD2 --", "    try:   # v410: IALD2 e H0DN (os registros por spec da v410 rodam na instrucao SEGUINTE, com o HMS/13: D80) --")
rx = re.compile(r'        _n410 = _v410_rodar_specs\(core\)\n        print\("   \[v410\] os registros com funcao e os por spec da v410: iald2=%s \| h0dn=%s \| specs: %d \(selados %d\)".*?\n    except Exception as _e410:\n        print\("   \[v410\] AVISO: o registro da IALD2, o do H0DN ou os registros por spec da v410 nao rodaram: %r" % \(_e410,\)\)\n', re.S)
assert len(rx.findall(t)) == 1, "o fim do bloco N00 nao foi achado uma vez"
NOVO_FIM = (
    "    except Exception as _e410:\n"
    '        print("   [v410] AVISO: o registro da IALD2 ou o do H0DN nao rodaram: %r" % (_e410,))\n'
    "    try:   # v410 (D80): o recibo DOCUMENTAL HMS/13 do Kimi -- h0dn_fontes_hms13_v410, ADITIVO e POSTERIOR ao FREEZE_R2 (le core[\"h0dn_bg1_v410\"], gravado na instrucao anterior; em rito nada e' lido da pasta do Kimi) -- e os registros por spec da v410 (as falas e a cobertura exata do Audit); excecao vira AVISO visivel, nunca derruba o rito\n"
    "        _f410 = h0dn_fontes_hms13_v410(core)   # D80: cobertura documental de fontes, não covariância física fechada; nada aberto\n"
    '        _f410v = _f410.get("values") or {}; _f410m = (_f410.get("mechanics") or {}).get("checks") or []\n'
    '        print("H0DN FONTES HMS/13 [v410 -- D80, a ratificacao do operador de 09/11 («o kimi fezz o trabalho e já te entregou»): a cobertura documental de %s fontes primarias dos %s calibradores fora do R22, embutida por sha256 (lida no build; nada lido em rito), aditiva e posterior ao FREEZE_R2; fatores de erro parciais; a forma HMS completa e\' diagnostico, nao admitida; covariancia fisica ABERTA; abertura nao permitida; H0DN x BG1 segue pré-registrado; nenhum dado observado lido; o gate nao se move]" % (_f410v.get("n_fontes_primarias"), _f410v.get("n_calibradores")))\n'
    '        print("  artefatos embutidos ok = %s/%s ; checagens ok = %s/%s ; numeros permitidos = %s (proibidos %s) ; caminhos sob a pasta vedada = %s ; gate = %s" % (sum(1 for p_ in (_f410v.get("pinos") or {}).values() if p_.get("sha256_ok") and p_.get("bytes_ok")), _f410v.get("n_embutidos"), sum(1 for c_ in _f410m if c_.get("ok")), len(_f410m) or None, (_f410v.get("numeros") or {}).get("permitidos"), len((_f410v.get("numeros") or {}).get("proibidos") or []), len(_f410v.get("sob_pasta_vedada") or []), "IGUAL" if _f410v.get("gate_verdict") == ((core.get("qg_closure") or {}).get("gate") or {}).get("verdict") else "DIFERENTE"))\n'
    '        print("  >>> %s <<<\\n" % _f410["verdict"])\n'
    "        _n410 = _v410_rodar_specs(core)\n"
    '        print("   [v410] os registros com funcao e os por spec da v410: %s | specs: %d (selados %d)" % (" | ".join("%s=%s" % (k_, "SELOU" if (core.get(k_) or {}).get("all_verified") is True else "NAO") for k_ in _V410_REGISTROS_FUNCAO), len(_n410), sum(1 for k_ in _n410 if (core.get(k_) or {}).get("all_verified") is True)))\n'
    "    except Exception as _e410b:\n"
    '        print("   [v410] AVISO: o registro do HMS/13 ou os registros por spec da v410 nao rodaram: %r" % (_e410b,))\n')
t = rx.sub(lambda m_: NOVO_FIM, t)
troca('"N00_main_iald2_h0dn", "G_RUNTIME", "main: iald2_v410, h0dn_bg1_v410 (D72; try/AVISO) e os registros por spec v410,',
      '"N00_main_iald2_h0dn_hms13", "G_RUNTIME", "main: DUAS instrucoes try/AVISO: iald2_v410 e h0dn_bg1_v410 (D72); depois h0dn_fontes_hms13_v410 (D80, posterior ao FREEZE_R2: le core[h0dn_bg1_v410] da instrucao anterior) e os registros por spec v410,')
# (5) o selo
troca('''        '            "h0dn_bg1_v410": {k_: (core.get("h0dn_bg1_v410") or {}).get(k_) for k_ in ("verdict", "all_verified", "observed_vector_read", "runtime_executed", "does_not_gate_core", "veredito_h0dn_source_sha256", "n_checks_esperadas", "lei", "modelos")},',\n''',
      '''        '            "h0dn_bg1_v410": {k_: (core.get("h0dn_bg1_v410") or {}).get(k_) for k_ in ("verdict", "all_verified", "observed_vector_read", "runtime_executed", "does_not_gate_core", "veredito_h0dn_source_sha256", "n_checks_esperadas", "lei", "modelos")},',\n'''
      '''        '            "h0dn_fontes_hms13_v410": {k_: (core.get("h0dn_fontes_hms13_v410") or {}).get(k_) for k_ in ("verdict", "all_verified", "observed_vector_read", "le_em_rito", "runtime_executed", "does_not_gate_core", "campos", "n_checks_esperadas", "aditivo_posterior_ao_freeze_r2")},',\n''')
troca('"selo: +iald2_v410 (resumo), +h0dn_bg1_v410 (resumo; D72) e registros_v410."', '"selo: +iald2_v410 (resumo), +h0dn_bg1_v410 (resumo; D72), +h0dn_fontes_hms13_v410 (resumo; D80) e registros_v410."')
# (6) controles de caractere e a guarda das frases sobre o texto novo
troca('_controles([CONTR_H, TXT_H], "contrato/texto do H0DN")', '_controles([CONTR_H, TXT_H], "contrato/texto do H0DN"); _controles([CONTR_F, TXT_F], "contrato/texto do HMS/13")')
troca('json.dumps([CONTR, TXT, specs, CONTR_H, TXT_H, ', 'json.dumps([CONTR, TXT, specs, CONTR_H, TXT_H, CONTR_F, TXT_F, ')
# (7) a terceira linha do .md
troca('ast.parse("def _f(core, md):\\n" + MD_LINHA_H); _controles(MD_LINHA_H, "linha do md (H0DN)")\n',
      'ast.parse("def _f(core, md):\\n" + MD_LINHA_H); _controles(MD_LINHA_H, "linha do md (H0DN)")\n'
      "MD_LINHA_F = ('    md.append(\"> **Recibo documental HMS/13 (v410, 09/11/2026; D80):** o registro `h0dn_fontes_hms13_v410` embute por sha256, lidos no build (em rito nenhum arquivo da entrega do Kimi é aberto), quatro artefatos documentais da revisão independente do Kimi: o mapa de fontes e covariância dos ' + str(len(CONTR_F[\"ids_calibradores\"])) + ' calibradores fora do R22, o manifesto das ' + str(len(CONTR_F[\"fontes_primarias\"])) + ' fontes primárias (título, URL, sha256 do arquivo e do texto), a validação e o levantamento legível; '\n"
    "              'aditivo e posterior ao FREEZE_R2 (os ' + str(CONTR_H[\"n_pinos_freeze\"]) + ' pinos do congelamento e os 11 do H0DN não mudam); fatores de erro parciais por linha dos arquivos upstream; a forma HMS completa é diagnóstico, não admitida; os dez campos da ORDEM do Kimi [DECLARADO; ratificada pelo operador por sha256: «' + DL.HMS13_TRECHO_RATIFICACAO + '»]: estatuto ' + DL.HMS13_CAMPOS[\"estatuto\"] + ', fontes_primarias 18, calibradores 13, partial_components_only True, as seis bandeiras de fechamento False. '\n"
    "              + DL.FRASE_HMS13_OBRIGATORIA_PT + '. O registro confere ' + str(CONTR_F[\"n_checks\"]) + ' checagens a cada rito; o gate não se move; H0DN × BG1 segue ' + DL.FRASE_H0DN_OBRIGATORIA_PT + '.\")')\n"
    'assert not GP.violacoes(MD_LINHA_F) and not GUARDA.search(MD_LINHA_F) and not GF.violacoes(MD_LINHA_F), GF.violacoes(MD_LINHA_F)[:3]\n'
    'ast.parse("def _f(core, md):\\n" + MD_LINHA_F); _controles(MD_LINHA_F, "linha do md (HMS/13)")\n')
troca('edit(A_M.start(), A_M.start(), MD_LINHA + CRLF + MD_LINHA_H + CRLF, "W09_md", "G_ARTIGO", "md canonico: as linhas «IALD2 (v410)» e «H0DN × BG1 pré-registrado (v410)», antes da linha da v409.")',
      'edit(A_M.start(), A_M.start(), MD_LINHA + CRLF + MD_LINHA_H + CRLF + MD_LINHA_F + CRLF, "W09_md", "G_ARTIGO", "md canonico: as linhas «IALD2 (v410)», «H0DN × BG1 pré-registrado (v410)» e «Recibo documental HMS/13 (v410)», antes da linha da v409.")')
# (8) os nomes novos
troca('"_V410_H0DN_TEXT", "_V410_H0DN_INSUMOS")   # (D72) o bloco do H0DN',
      '"_V410_H0DN_TEXT", "_V410_H0DN_INSUMOS",   # (D72) o bloco do H0DN\n'
      '               "_v410_hms13_numeros", "_v410_hms13_mechanics", "_V410_HMS13_RECUSA", "h0dn_fontes_hms13_v410", "_V410_HMS13_CONTRACT", "_V410_HMS13_TEXT", "_V410_HMS13_INSUMOS")   # (D80) o bloco do HMS/13')
# (9) o manifesto CANDIDATO_v410.json
troca('       "ponto_de_chamada": {"iald2_v410":',
      '       "hms13": {"registro": DL.HMS13_REGISTRO, "tag": DL.TAG_HMS13, "n_checks": CONTR_F["n_checks"], "veredito_ok": CONTR_F["veredito_ok"], "campos": CONTR_F["campos"], "insumos": CONTR_F["insumos"], "pinos_build": CONTR_F["pinos_build"], "handoff": CONTR_F["handoff"], "ordem": CONTR_F["ordem"], "ratificacao": CONTR_F["ratificacao"],\n'
      '                 "guarda_numerica_no_build": CONTR_F["guarda_numerica_no_build"], "cobertura_extra_no_manifesto": CONTR_F["cobertura_extra_no_manifesto"], "archive_statuses": CONTR_F["archive_statuses"], "ids_calibradores": CONTR_F["ids_calibradores"], "n_fontes_primarias": len(CONTR_F["fontes_primarias"]), "le_em_rito": False, "observed_vector_read": False,\n'
      '                 "bytes_embutidos_b64": sum(len(v_["b64"]) for v_ in INS_F.values()), "nota": "D80: " + DL.FRASE_HMS13_OBRIGATORIA_PT + "; aditivo e posterior ao FREEZE_R2; o BUILD leu os seis arquivos documentais da pasta do Kimi (HANDOFF e ORDEM relidos, sha256 conferidos); o RITO nao abre nada de kimi; a cunhagem da mesma fala do operador entra pela pedra da D82 (parte 2), nao por este registro"},\n'
      '       "fontes_hms13_embutidas": {k_: {"caminho": os.path.join(DL.HMS13_DIR, *v_["rel"].split("/")), "sha256": v_["sha256"], "bytes": v_["bytes"], "embutido_no_um_py": k_ in INS_F, "papel": "artefato documental embutido em base64" if k_ in INS_F else "pino do build (relido imediatamente antes; nao embutido)"} for k_, v_ in CONTR_F["pinos_build"].items()},\n'
      '       "ponto_de_chamada": {"h0dn_fontes_hms13_v410": "main: a instrucao SEGUINTE a\' do iald2/h0dn (D80: posterior ao FREEZE_R2; le core[h0dn_bg1_v410]); antes dos specs da v410, que passam a essa instrucao", "iald2_v410":')
nb = t.encode("utf-8"); ast.parse(nb)
tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
print("gerar_candidato_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16], "| ok")
