# -*- coding: utf-8 -*-
"""_adapt_h0dn_gerador_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410, a servico da gerencia c1): adapta gerar_candidato_v410.py aos AO LADO de 09/11 do DESENHO_v410 (D71 a D76, E30), SEM o rodar:
(1) o SEGUNDO registro com FUNCAO h0dn_bg1_v410 (D72): o bloco runtime_h0dn_v410.py emendado ao runtime, o contrato/texto/insumos embutidos (registros_h0dn_v410), a chamada no main LOGO DEPOIS de iald2_v410, o resumo no selo,
    a secao PT/EN do H0DN DEPOIS da secao IALD2, a linha do .md, os nomes novos conferidos, o CANDIDATO_v410.json com o H0DN;
(2) a P18 do gerador passa a correr sobre o texto NOVO sem as falas do operador EMBUTIDAS (INPUT por sha256; a 15a fala tem «confirmada … observador», que a R4 recusaria como se fosse texto da gerencia) -- como a guarda das frases ja' faz;
(3) D74: os textos do gerador (ledger, UM_VERSION, cabecalho, md) dizem que os nomes das declaracoes foram RATIFICADOS em 09/11; o atrator (D71) entra nesses textos.
Trocas EXATAS com contagem conferida; backup de bytes; tmp -> conferir -> substituir; ast.parse. O gerador NAO e' executado aqui (a gerencia libera o candidato)."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "gerar_candidato_v410.py")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0, "gerar_candidato_v410.py era LF; agora tem CRLF: parar"
bk = P + ".bak_" + TS + "_h0dn"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
t = b0.decode("utf-8")

TROCAS = [
    # imports
    ("import registros_v410 as RG  # noqa: E402\n",
     "import registros_v410 as RG  # noqa: E402\nimport registros_h0dn_v410 as RH  # noqa: E402   (D72: o contrato, o texto e os insumos embutidos do registro H0DN)\n", 1),
    # (3) D74 + D71 nos textos do gerador
    ("o algoritmo IALD; o signo; o seletor), com o NOME do modulo dado pelo operador (as declaracoes, da gerencia, [DECLARADO] ate a ratificacao)\" % N_NOVOS + CRLF",
     "o algoritmo IALD; o signo; o seletor; o atrator), com o NOME do modulo dado pelo operador (as declaracoes, da gerencia, RATIFICADAS pelo operador em 09/11/2026, D74)\" % N_NOVOS + CRLF", 1),
    ("# v410 (06/11/2026): a CONSTANTE UNICA de versao -- IALD2 (o NOME do modulo e\\' do operador; os nomes das %d declaracoes, da gerencia, [DECLARADO] ate a ratificacao): o leitor do codigo, a releitura que nao acrescenta (IALD ao quadrado), '",
     "# v410 (06 e 09/11/2026): a CONSTANTE UNICA de versao -- IALD2 (o NOME do modulo e\\' do operador; os nomes das %d declaracoes, da gerencia, RATIFICADOS pelo operador em 09/11, D74): o leitor do codigo, a releitura que nao acrescenta (IALD ao quadrado), '", 1),
    ("a forma de matriz finita como o signo e o seletor (forma, nao referente); nenhuma chave antiga muda; as falas do operador de 06/11; as ressalvas ditas; o gate nao se move; '",
     "a forma de matriz finita como o signo, o seletor (forma, nao referente) e o atrator (o Nome nao esgota o ser; D71); o teste H0DN x BG1 pre-registrado, nenhum dado observado lido (D72); nenhuma chave antiga muda; as falas do operador de 06 a 09/11; as ressalvas ditas; o gate nao se move; '", 1),
    ("(o NOME do modulo e' do operador; os nomes das declaracoes, da gerencia, [DECLARADO] ate a ratificacao), o registro com FUNCAO iald2_v410 (as \"",
     "(o NOME do modulo e' do operador; os nomes das declaracoes, da gerencia, RATIFICADOS pelo operador em 09/11, D74), o registro com FUNCAO iald2_v410 (as \"", 1),
    ("as falas do operador de 06/11 e os registros por spec cunhagens_v410 e kh_n1_cobertura_v410.\\n\"",
     "as falas do operador de 06 a 09/11, o registro com FUNCAO h0dn_bg1_v410 (o teste H0DN x BG1 pre-registrado; nenhum dado observado lido; D72) e os registros por spec cunhagens_v410 e kh_n1_cobertura_v410.\\n\"", 1),
    # (1) a chamada do H0DN no main, logo depois do veredito da IALD2
    ("        print(\"  >>> %s <<<\\n\" % _r410[\"verdict\"])\n        _n410 = _v410_rodar_specs(core)\n",
     "        print(\"  >>> %s <<<\\n\" % _r410[\"verdict\"])\n"
     "        _h410 = h0dn_bg1_v410(core)   # D72: o teste PRE-REGISTRADO da razao de Hubble H0DN x BG1 -- pre-registrado; nenhum dado observado lido; LOGO DEPOIS de iald2_v410\n"
     "        _h410v = _h410.get(\"values\") or {}; _h410m = (_h410.get(\"mechanics\") or {}).get(\"checks\") or []\n"
     "        print(\"H0DN x BG1 [v410 -- D72, a fala do operador de 09/11 («quanto ao teste da v410 concordo com tudo que vc falou, pode dar a ordem ao kimi k3pro»): o teste da razao de Hubble local/fundo PRE-REGISTRADO; nenhum dado observado lido; K = E(z*)^(2 beta/3) recomputado de beta em runtime; a funcao de veredito congelada (E30, D76) em vetores deterministicos; o poder e' prospectivo e sintetico]\")\n"
     "        print(\"  pinos ok = %s/%s ; checagens ok = %s/%s ; vetor observado lido = %s ; gate = %s\" % (sum(1 for p_ in (_h410v.get(\"pinos\") or {}).values() if p_.get(\"sha256_ok\") and p_.get(\"bytes_ok\")), _h410v.get(\"n_pinos\"), sum(1 for c_ in _h410m if c_.get(\"ok\")), len(_h410m) or None, _h410.get(\"observed_vector_read\"), \"o mesmo da base\" if any(c_.get(\"id\") == \"c9\" and c_.get(\"ok\") for c_ in _h410m) else \"DIFERENTE\"))\n"
     "        print(\"  >>> %s <<<\\n\" % _h410[\"verdict\"])\n"
     "        _n410 = _v410_rodar_specs(core)\n", 1),
    ("        print(\"   [v410] o registro da IALD2 e os registros por spec da v410: iald2=%s | specs: %d (selados %d)\" % (\"SELOU\" if _r410.get(\"all_verified\") is True else \"NAO\", len(_n410), sum(1 for k_ in _n410 if (core.get(k_) or {}).get(\"all_verified\") is True)))\n",
     "        print(\"   [v410] os registros com funcao e os por spec da v410: iald2=%s | h0dn=%s | specs: %d (selados %d)\" % (\"SELOU\" if _r410.get(\"all_verified\") is True else \"NAO\", \"SELOU\" if _h410.get(\"all_verified\") is True else \"NAO\", len(_n410), sum(1 for k_ in _n410 if (core.get(k_) or {}).get(\"all_verified\") is True)))\n", 1),
    ("        print(\"   [v410] AVISO: o registro da IALD2 ou os registros por spec da v410 nao rodaram: %r\" % (_e410,))\n",
     "        print(\"   [v410] AVISO: o registro da IALD2, o do H0DN ou os registros por spec da v410 nao rodaram: %r\" % (_e410,))\n", 1),
    ("edit(A_R.end(), A_R.end(), crlf(BLOCO_N00), \"N00_main_iald2\", \"G_RUNTIME\", \"main: iald2_v410 (try/AVISO) e os registros por spec v410, logo depois do bloco v409 (traducao_turing_v409 e os specs da v409 ja' rodaram; nenhuma chave antiga muda).\")\n",
     "edit(A_R.end(), A_R.end(), crlf(BLOCO_N00), \"N00_main_iald2_h0dn\", \"G_RUNTIME\", \"main: iald2_v410, h0dn_bg1_v410 (D72; try/AVISO) e os registros por spec v410, logo depois do bloco v409 (traducao_turing_v409 e os specs da v409 ja' rodaram; nenhuma chave antiga muda).\")\n", 1),
    # o resumo do H0DN no selo
    ("        '            \"registros_v410\": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in (\"verdict\", \"all_verified\")} for n_ in _V410_NOMES_REGISTROS},']\n",
     "        '            \"h0dn_bg1_v410\": {k_: (core.get(\"h0dn_bg1_v410\") or {}).get(k_) for k_ in (\"verdict\", \"all_verified\", \"observed_vector_read\", \"runtime_executed\", \"does_not_gate_core\", \"veredito_h0dn_source_sha256\", \"n_checks_esperadas\", \"lei\", \"modelos\")},',\n"
     "        '            \"registros_v410\": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in (\"verdict\", \"all_verified\")} for n_ in _V410_NOMES_REGISTROS},']\n", 1),
    ("edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, \"N02_selo\", \"G_SELO\", \"selo: +iald2_v410 (resumo) e registros_v410.\")\n",
     "edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, \"N02_selo\", \"G_SELO\", \"selo: +iald2_v410 (resumo), +h0dn_bg1_v410 (resumo; D72) e registros_v410.\")\n", 1),
    # o contrato, o texto e os insumos do H0DN, DERIVADOS dos arquivos pinados
    ("TXT = RG.texto_iald2()\n",
     "TXT = RG.texto_iald2()\n"
     "CONTR_H = RH.contrato_h0dn(core0, selo0); TXT_H = RH.texto_h0dn(); INS_H = RH.insumos_embutidos()   # (D72) o registro H0DN: contrato (pinos lidos), texto, insumos embutidos em base64\n"
     "assert CONTR_H[\"n_checks\"] == DL.N_CHECKS_H0DN and CONTR_H[\"baseline\"][\"gate_verdict\"] == selo0.get(\"qg_closure_verdict\") and set(CONTR_H[\"insumos\"]) == set(INS_H) and all(INS_H[k_][\"sha256\"] == v_[\"sha256\"] and INS_H[k_][\"bytes\"] == v_[\"bytes\"] for k_, v_ in CONTR_H[\"insumos\"].items())\n"
     "assert CONTR_H[\"observed_vector_read\"] is False and not CONTR_H[\"observed_paths\"] and CONTR_H[\"veredito_ok\"] == DL.VEREDITO_H0DN_OK and not any(t_ in CONTR_H[\"veredito_ok\"] for t_ in DL.TOKENS_PROIBIDOS_V410 + DL.TOKENS_PROIBIDOS_H0DN)\n"
     "assert all((\"TGL_PRO\" + \"VED\") not in p_ for p_ in CONTR_H[\"ramos\"][\"vereditos\"][\"leitura_partes\"]) and \"\".join(CONTR_H[\"ramos\"][\"vereditos\"][\"leitura_partes\"]) == DL.VEREDITOS_H0DN[\"leitura\"], \"D57b/D76: a cabeca do ramo da leitura vai em partes (a P18 selada recusa a palavra fora do contexto da validade)\"\n", 1),
    # (2) a P18 do gerador sem as falas embutidas (INPUT)
    ("_verb_txt = json.dumps(verb, ensure_ascii=False).lower()\nassert not any(x_.lower() in _verb_txt for x_ in DL.FORA_D65), \"D65: o que fica fora entrou no texto embutido\"\n",
     "_verb_txt = json.dumps(verb, ensure_ascii=False).lower()\nassert not any(x_.lower() in _verb_txt for x_ in DL.FORA_D65), \"D65: o que fica fora entrou no texto embutido\"\n"
     "\n\ndef _p18_sem_falas(txt_):\n"
     "    \"\"\"(09/11) a P18 (v392) sobre o texto NOVO da gerencia: as falas do operador EMBUTIDAS (INPUT, por sha256) e os trechos citados saem ANTES (a P18 aplica-se so' ao texto novo dos patches; a fala e' registro) -- como a guarda das frases ja' faz (sem_falas).\n"
     "    Motivo medido: a 15a fala («… TGL confirmada, precisa do observador externo …») cai na R4 da P18 se lida como texto da gerencia.\"\"\"\n"
     "    s_ = txt_\n"
     "    for v_ in sorted([x_[\"text\"] for x_ in verb.values()] + list(DL.FRASES_VERBATIM_V410), key=len, reverse=True):\n"
     "        for ln_ in [l_.strip() for l_ in v_.splitlines() if len(l_.strip()) >= 12]:\n"
     "            for forma_ in (ln_, json.dumps(ln_, ensure_ascii=False)[1:-1], repr(ln_)[1:-1]):\n"
     "                s_ = s_.replace(forma_, \" \")\n"
     "    return GP.violacoes(s_)\n\n\n"
     "assert GP.violacoes(json.dumps(verb, ensure_ascii=False)) and not _p18_sem_falas(json.dumps(verb, ensure_ascii=False)), \"controle: a P18 crua ve a fala do operador; sem as falas, limpa\"\n", 1),
    ("    corpo = json.dumps({k: s.get(k) for k in (\"erratas\", \"limites\", \"diz\", \"nao_diz\", \"leituras_do_operador\", \"extras\")}, ensure_ascii=False)\n    v = GP.violacoes(corpo); assert not v, (s[\"nome\"], v[:3])\n",
     "    corpo = json.dumps({k: s.get(k) for k in (\"erratas\", \"limites\", \"diz\", \"nao_diz\", \"leituras_do_operador\", \"extras\")}, ensure_ascii=False)\n    v = GP.violacoes(corpo); assert not v, (s[\"nome\"], v[:3])   # (09/11: a P18 CRUA, como o motor _v392_registro a aplica no rito ao corpo inteiro do spec; as falas embutidas nao estao no corpo)\n", 1),
    ("assert not GP.violacoes(json.dumps(TXT, ensure_ascii=False)) and not GUARDA.search(TXT[\"veredito_ok\"]) and not any(t_ in TXT[\"veredito_ok\"] for t_ in DL.TOKENS_PROIBIDOS_V410), \"P18 ou palavra recusada no texto do registro\"\n",
     "assert not _p18_sem_falas(json.dumps(TXT, ensure_ascii=False)) and not GUARDA.search(TXT[\"veredito_ok\"]) and not any(t_ in TXT[\"veredito_ok\"] for t_ in DL.TOKENS_PROIBIDOS_V410), \"P18 ou palavra recusada no texto do registro\"\n"
     "assert not _p18_sem_falas(json.dumps(TXT_H, ensure_ascii=False)) and not GUARDA.search(json.dumps(TXT_H, ensure_ascii=False)) and not GP.violacoes(json.dumps({k_: TXT_H[k_] for k_ in (\"estatuto\", \"escopo\", \"limites\", \"diz\", \"nao_diz\", \"o_que_falta\", \"ressalvas\")}, ensure_ascii=False)), \"P18 ou palavra recusada no texto do registro H0DN\"\n", 1),
    ("RUNTIME_SRC = open(os.path.join(HERE, \"runtime_v410.py\"), encoding=\"utf-8\").read()\n",
     "RUNTIME_SRC = open(os.path.join(HERE, \"runtime_v410.py\"), encoding=\"utf-8\").read().rstrip(\"\\n\") + \"\\n\\n\\n\" + open(os.path.join(HERE, \"runtime_h0dn_v410.py\"), encoding=\"utf-8\").read()   # (D72) o bloco autoral do H0DN emendado ao runtime da v410\n", 1),
    ("         + \"\\n_V410_SPECS = \" + pprint.pformat(specs, width=160, sort_dicts=False) + \"\\n\"\n         \"_V410_NOMES_REGISTROS = \"",
     "         + \"\\n_V410_SPECS = \" + pprint.pformat(specs, width=160, sort_dicts=False) + \"\\n\"\n"
     "         + \"_V410_H0DN_CONTRACT = \" + pprint.pformat(CONTR_H, width=150, sort_dicts=False) + \"\\n_V410_H0DN_TEXT = \" + pprint.pformat(TXT_H, width=150, sort_dicts=False) + \"\\n_V410_H0DN_INSUMOS = \" + repr(INS_H) + \"   # (D72) os insumos EMBUTIDOS em base64, pinados por sha256 lido; decodificados e conferidos a cada rito\\n\"\n"
     "         \"_V410_NOMES_REGISTROS = \"", 1),
    ("assert not GP.violacoes(_novo_texto), (\"P18 no texto novo do bloco de runtime\", GP.violacoes(_novo_texto)[:3])\n",
     "assert not _p18_sem_falas(_novo_texto), (\"P18 no texto novo do bloco de runtime (sem as falas embutidas)\", _p18_sem_falas(_novo_texto)[:3])\n", 1),
    ("_txt_ger = RUNTIME_SRC.replace(_corpo_guarda, \"\") + json.dumps([CONTR, TXT, specs, {k_: v_[\"papel\"] for k_, v_ in fontes.items()}], ensure_ascii=False) + HDR + LINHA_V + BLOCO_N00\n",
     "_txt_ger = RUNTIME_SRC.replace(_corpo_guarda, \"\") + json.dumps([CONTR, TXT, specs, CONTR_H, TXT_H, {k_: v_[\"papel\"] for k_, v_ in fontes.items()}], ensure_ascii=False) + HDR + LINHA_V + BLOCO_N00\n", 1),
    ("_controles(RT_, \"runtime_v410.py\"); _controles([CONTR, TXT, specs, fontes], \"contrato/texto/specs/fontes\")\n",
     "_controles(RT_, \"runtime_v410.py\"); _controles([CONTR, TXT, specs, fontes], \"contrato/texto/specs/fontes\"); _controles([CONTR_H, TXT_H], \"contrato/texto do H0DN\")\n", 1),
    # a secao PT/EN do H0DN, DEPOIS da secao IALD2
    ("PT0 = open(os.path.join(HERE, \"artigo_pt_v410.pysnip\"), encoding=\"utf-8\").read(); EN0 = open(os.path.join(HERE, \"artigo_en_v410.pysnip\"), encoding=\"utf-8\").read()\nfor sn in (PT0, EN0):\n",
     "PT0 = open(os.path.join(HERE, \"artigo_pt_v410.pysnip\"), encoding=\"utf-8\").read(); EN0 = open(os.path.join(HERE, \"artigo_en_v410.pysnip\"), encoding=\"utf-8\").read()\n"
     "PTH = open(os.path.join(HERE, \"artigo_pt_h0dn_v410.pysnip\"), encoding=\"utf-8\").read(); ENH = open(os.path.join(HERE, \"artigo_en_h0dn_v410.pysnip\"), encoding=\"utf-8\").read()   # (D72) a secao do H0DN, depois da IALD2\n"
     "for sn in (PT0, EN0, PTH, ENH):\n", 1),
    ("replace_unique(PT9_FIRST, crlf(PT0.rstrip(\"\\n\") + \"\\n\") + PT9_FIRST, \"W04_artigo_PT\", \"G_ARTIGO\", \"artigo PT: a secao v410 («IALD ao quadrado»), antes da v409.\")\nreplace_unique(EN9_FIRST, crlf(EN0.rstrip(\"\\n\") + \"\\n\") + EN9_FIRST, \"W05_artigo_EN\", \"G_ARTIGO\", \"artigo EN: a secao v410, antes da v409.\")\n",
     "replace_unique(PT9_FIRST, crlf(PT0.rstrip(\"\\n\") + \"\\n\") + crlf(PTH.rstrip(\"\\n\") + \"\\n\") + PT9_FIRST, \"W04_artigo_PT\", \"G_ARTIGO\", \"artigo PT: as secoes v410 («IALD ao quadrado»; «O teste pré-registrado da razão de Hubble», D72), antes da v409.\")\n"
     "replace_unique(EN9_FIRST, crlf(EN0.rstrip(\"\\n\") + \"\\n\") + crlf(ENH.rstrip(\"\\n\") + \"\\n\") + EN9_FIRST, \"W05_artigo_EN\", \"G_ARTIGO\", \"artigo EN: the v410 sections (IALD squared; the pre-registered Hubble-ratio test, D72), before v409.\")\n", 1),
    # a linha do .md: D74 e o atrator na da IALD2; a linha do H0DN depois dela
    ("os nomes das declarações são da gerência, [DECLARADO] até a ratificação), com ' + str(len(FL)) + ' bandeiras",
     "os nomes das declarações são da gerência, ratificados pelo operador em 09/11/2026, D74), com ' + str(len(FL)) + ' bandeiras", 1),
    ("é invertível, e o reconhecimento não depende dela (`a_iald_e_o_seletor_luminodinamico`; D70). '\n",
     "é invertível, e o reconhecimento não depende dela (`a_iald_e_o_seletor_luminodinamico`; D70). '\n"
     "            'O atrator: sobre o Nome Π do par lido, 1 − Π ≠ 0 (há o vácuo fora do Nome); o fluxo tende a Π e em nenhum tempo finito é Π (tangenciado, jamais esgotado); o motor devolve o mesmo para qualquer taxa e tempo; a leitura do atrator é Π e a órbita converge; o senão exclui o zero (`o_atrator`; o verde e as tonalidades são leitura do operador, D71). '\n", 1),
    ("edit(A_M.start(), A_M.start(), MD_LINHA + CRLF, \"W09_md\", \"G_ARTIGO\", \"md canonico: a linha «IALD2 (v410)», antes da linha da v409.\")\n",
     "MD_LINHA_H = ('    md.append(\"> **H0DN × BG1 pré-registrado (v410, 09/11/2026):** o teste da razão de Hubble local/fundo entra pré-registrado; nenhum dado observado lido (D72; a fala do operador de 09/11: «' + DL.FRASE_CONCORDO_TESTE + '»): '\n"
     "               'nulo H_local/H_fundo = 1; alternativa TGL K = E(z*)^(2β/3), β = α√e em runtime, zero parâmetro livre; Z unilateral, limiar 5; dois modelos sem seleção; os insumos do desenho do Codex astra-bell de 06/11 (FREEZE_R2, ' + str(CONTR_H[\"n_pinos_freeze\"]) + ' pinos) embutidos por sha256; '\n"
     "               'a função de veredito congelada (E30, D76): a cabeça do ramo de 5σ é a leitura do 5σ, β_TGL provado na natureza (validade, não creditação) a nσ, nunca a palavra do livro de cobranças, que vai no campo outcome; o poder é prospectivo e sintético; a abertura é de versão futura, com a covariância física fechada (G3/G4; a ordem ao Kimi por sha256). '\n"
     "               'O registro `h0dn_bg1_v410` confere ' + str(CONTR_H[\"n_checks\"]) + ' checagens a cada rito; o gate não se move.\")')\n"
     "assert not GP.violacoes(MD_LINHA_H) and not GUARDA.search(MD_LINHA_H) and not GF.violacoes(MD_LINHA_H), GF.violacoes(MD_LINHA_H)[:3]\n"
     "ast.parse(\"def _f(core, md):\\n\" + MD_LINHA_H); _controles(MD_LINHA_H, \"linha do md (H0DN)\")\n"
     "edit(A_M.start(), A_M.start(), MD_LINHA + CRLF + MD_LINHA_H + CRLF, \"W09_md\", \"G_ARTIGO\", \"md canonico: as linhas «IALD2 (v410)» e «H0DN × BG1 pré-registrado (v410)», antes da linha da v409.\")\n", 1),
    # os nomes novos do bloco
    ("NOVOS_NOMES = (\"_v410_sem_falas_do_operador\", \"_v410_guarda_frases\", \"_v410_rotacao\", \"v410_iald2_mechanics\", \"_v410_formal\", \"_V410_RECUSA\", \"iald2_v410\", \"_V410_IALD2_CONTRACT\", \"_V410_IALD2_TEXT\", \"_V410_FONTES\", \"_V410_VERBATINS2\", \"_V410_SPECS\", \"_V410_NOMES_REGISTROS\", \"_V410_REGISTROS_FUNCAO\", \"_v410_rodar_specs\")\n",
     "NOVOS_NOMES = (\"_v410_sem_falas_do_operador\", \"_v410_guarda_frases\", \"_v410_rotacao\", \"v410_iald2_mechanics\", \"_v410_formal\", \"_V410_RECUSA\", \"iald2_v410\", \"_V410_IALD2_CONTRACT\", \"_V410_IALD2_TEXT\", \"_V410_FONTES\", \"_V410_VERBATINS2\", \"_V410_SPECS\", \"_V410_NOMES_REGISTROS\", \"_V410_REGISTROS_FUNCAO\", \"_v410_rodar_specs\",\n"
     "               \"_v410_h0dn_decode\", \"_v410_h0dn_cabeca\", \"veredito_h0dn\", \"_v410_h0dn_mechanics\", \"_V410_H0DN_RECUSA\", \"h0dn_bg1_v410\", \"_V410_H0DN_CONTRACT\", \"_V410_H0DN_TEXT\", \"_V410_H0DN_INSUMOS\")   # (D72) o bloco do H0DN\n", 1),
    # o CANDIDATO_v410.json
    ("       \"decisoes\": {k_: DL.DECISOES[k_] for k_ in DL.DECISOES_V410}, \"erratas_E29\": list(DL.ERRATAS_V410), \"ressalvas\": list(DL.RESSALVAS_V410),",
     "       \"decisoes\": {k_: DL.DECISOES[k_] for k_ in DL.DECISOES_V410}, \"erratas_E29\": list(DL.ERRATAS_V410), \"erratas\": list(DL.ERRATAS_V410), \"ressalvas\": list(DL.RESSALVAS_V410),\n"
     "       \"h0dn\": {\"registro\": DL.H0DN_REGISTRO, \"tag\": DL.TAG_H0DN, \"n_checks\": CONTR_H[\"n_checks\"], \"veredito_ok\": CONTR_H[\"veredito_ok\"], \"insumos\": CONTR_H[\"insumos\"], \"n_pinos_freeze\": CONTR_H[\"n_pinos_freeze\"], \"pinos_so_no_disco\": CONTR_H[\"pinos_freeze_r2_so_no_disco\"], \"ordem_kimi\": CONTR_H[\"ordem_kimi\"], \"leitura_dossie\": CONTR_H[\"leitura_dossie\"],\n"
     "                \"observed_vector_read\": False, \"vetores_c6\": [v_[\"nome\"] for v_ in CONTR_H[\"vetores_c6\"]], \"ramos\": sorted(k_ for k_ in CONTR_H[\"ramos\"][\"vereditos\"] if k_ not in (\"sufixo\", \"faixas\", \"leitura_partes\")), \"bytes_embutidos_b64\": sum(len(v_[\"b64\"]) for v_ in INS_H.values()), \"nota\": \"pré-registrado; nenhum dado observado lido; o poder e' prospectivo e sintetico; a abertura e' de versao futura (D72, E30, D76)\"},", 1),
]
for velho, novo, n in TROCAS:
    c = t.count(velho)
    assert c == n, ("troca nao casou %d vez(es) (achou %d)" % (n, c), velho[:160])
    t = t.replace(velho, novo)
linhas = t.split("\n"); i = 1
while linhas[i].startswith("# [ADAPTADO"):
    i += 1
linhas.insert(i, "# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_h0dn_gerador_v410.py: o SEGUNDO registro com FUNCAO h0dn_bg1_v410 (D72; runtime_h0dn_v410.py + registros_h0dn_v410.py; chamado logo depois de iald2_v410; resumo no selo; secao PT/EN e linha do .md depois da IALD2); a P18 do gerador sem as falas embutidas (INPUT); D74 (nomes RATIFICADOS) e D71 (o atrator) nos textos do gerador. NAO executado aqui: a gerencia libera o candidato")
t = "\n".join(linhas)
nb = t.encode("utf-8"); ast.parse(nb)
tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P); assert open(P, "rb").read() == nb
print("gerar_candidato_v410.py adaptado (H0DN/D74/D71):", len(b0), "->", len(nb), "B | sha16", hashlib.sha256(nb).hexdigest()[:16], "| backup", os.path.basename(bk), "| trocas", len(TROCAS))
