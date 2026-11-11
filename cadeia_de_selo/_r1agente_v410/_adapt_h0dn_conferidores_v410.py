# -*- coding: utf-8 -*-
"""_adapt_h0dn_conferidores_v410.py -- (claude-construtor-v410, 09/11/2026, retomada; D72 e o AVISO da gerencia) leva o SEGUNDO registro com funcao, h0dn_bg1_v410, aos conferidores que o fork B adaptou em 06/11 ANTES de a D72 existir, e corrige o que ficou da epoca:
  (1) conferir_rito_v410.py: _h0dn_ok (o registro no core do Nos depois do rito contra os ESPERADOS: veredito pre-registrado, 12 checagens, observed_vector_read False, os pinos, os 6 ramos, o sha256 da funcao, nenhum caminho sob a pasta vedada, os valores do ensaio),
      a secao do H0DN no artigo (depois da IALD2, antes da v409, com a obrigacao D72 nas duas linguas; o TXT rende \\times como x), a linha do .md, o resumo do selo, o veredito no resultado; _tt converte \\times;
  (2) conferir_instalar_rito_v410.py: as decisoes vao a D77 e as erratas sao E29 e E30 (lidas de DL); o rito_v410.sh tem de trazer o h0dn, os numeros atuais (22 ancoras, 15 falas, 16 e 12 checagens) e o tempo MEDIDO em 09/11; os rotulos velhos (19 ancoras, 9 falas, 15 checagens, D63 a D70, 06/11) ficam proibidos;
  (3) rito_v410.sh (ato da gerencia; so' o texto descritivo do cabecalho): os numeros da retomada e o h0dn, lidos do delta e das marcas do kernel (nada digitado);
  (4) fechar_preparacao_v410.py: o registro ABERTO do Mapa e' UM objeto (a v409 era lista): o [0] quebrava (achado do Sonnet);
  (5) _teste_h0dn_offline_v410.py: o uso diz -B -X utf8 (D77f: numpy e' do site do usuario) e o teste grava TESTE_H0DN_OFFLINE_v410.json (o gerar_relatorio o le, informativo).
Backup de bytes; trocas exatas com contagem; fim de linha preservado; ast.parse nos .py; sh -n no .sh."""
import ast, datetime, hashlib, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
import delta_v410 as DL  # noqa: E402


def troca_arquivo(rel, trocas, marca=None, py=True):
    P = os.path.join(HERE, rel); b0 = open(P, "rb").read(); nl = "\r\n" if b0.count(b"\r\n") else "\n"
    if marca and marca.encode("utf-8") in b0:
        print(rel, "ja adaptado (a marca esta' no arquivo): pulado"); return
    bk = P + ".bak_" + TS + "_h0dn"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
    t = b0.decode("utf-8")
    for v, n, k in trocas:
        v2, n2 = v.replace("\n", nl), n.replace("\n", nl); c = t.count(v2); assert c == k, (rel, c, k, v[:140]); t = t.replace(v2, n2)
    if marca:
        lin = t.split(nl); assert lin[0].startswith("# -*- coding") or lin[0].startswith("#!/"), rel; lin.insert(1, marca); t = nl.join(lin)
    nb = t.encode("utf-8")
    if py:
        ast.parse(nb)
    tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
    if not py:
        r = subprocess.run(["sh", "-n", P], capture_output=True, text=True); assert r.returncode == 0, (rel, r.stderr[:300])
    print(rel, len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16], "| trocas", len(trocas))


# ---- os numeros LIDOS (nada digitado): as marcas do kernel, a medida do Audit, o delta
tm = open(os.path.join(HERE, DL.KERNEL_DIR, "construir_marcas.txt"), encoding="utf-8").read()
mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", tm, re.M)}
BUILD_S = mm["epoch_build_fim"] - mm["epoch_inicio"]; AUDIT_S = mm["epoch_audit_fim"] - mm["epoch_build_fim"]
KH = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v410.json"), encoding="utf-8"))
SOMA_S, MAX_S = KH["build_modulos_s_soma"], KH["build_modulos_s_max"]
PB = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "POS_BUILD_v410.json"), encoding="utf-8"))
assert PB["duracao_build_s"] == BUILD_S and PB["duracao_audit_s"] == AUDIT_S, (BUILD_S, AUDIT_S, PB.get("duracao_build_s"), PB.get("duracao_audit_s"))
NA, NF, NC, NH = len(DL.ANCORAS), DL.N_FALAS_V410, DL.N_CHECKS_FECHO, DL.N_CHECKS_H0DN
assert (NA, NF, NC, NH) == (22, 15, 16, 12) and DL.DECISOES_V410[-1] == "D77" and [e_.split(" --")[0] for e_ in DL.ERRATAS_V410] == ["E29", "E30"]
Q = DL.FRASE_H0DN_OBRIGATORIA_PT
print("numeros lidos: ancoras %d, falas %d, checagens %d + %d (H0DN), build %d s, audit %d s, soma por modulo %s s, max %s s" % (NA, NF, NC, NH, BUILD_S, AUDIT_S, SOMA_S, MAX_S))

# (1) conferir_rito_v410.py
H0DN_OK = '''def _h0dn_ok():
    """h0dn_bg1_v410 (D72; o SEGUNDO registro com FUNCAO, novo; pré-registrado; nenhum dado observado lido): veredito == o do ensaio == o PRE-REGISTRADO (DL.VEREDITO_H0DN_OK); as 12 checagens; observed_vector_read False (no registro e nos valores); os pinos todos batendo; os 6 ramos da funcao de veredito congelada nos vetores deterministicos;
    o sha256 do texto-fonte da funcao == o do ensaio; o gate == o da v409 selada; nenhum caminho tocado sob a pasta vedada (a entrega do Kimi) nem com nome vedado -- MEDIDO pelo proprio registro (c7) e relido aqui caminho a caminho; os valores == os do ensaio (menos os caminhos tocados, que dependem da pasta do rito); nao move o gate"""
    R_ = HV; E_ = ESP["registros_funcao_v410"]["h0dn"]; m_ = R_.get("mechanics") or {}; v_ = V(DL.H0DN_REGISTRO); vv_ = R_.get("values") or {}
    _nrm_ = lambda p_: os.path.normcase(os.path.normpath(str(p_))); _ved_ = _nrm_(DL.H0DN_PASTA_VEDADA); _toc_ = vv_.get("caminhos_tocados") or []
    _nomes_ = tuple(n_.lower() for n_ in DL.H0DN_NOMES_VEDADOS)
    return bool(R_.get("all_verified") is True and v_ == E_["verdict"] == DL.VEREDITO_H0DN_OK and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and R_.get("observed_vector_read") is False and vv_.get("observed_vector_read") is False
                and m_.get("passed") is True and m_.get("n_checks") == DL.N_CHECKS_H0DN == E_["n_checks"] and all(c_["ok"] for c_ in m_.get("checks") or []) and R_.get("beta_ok") is True
                and vv_.get("n_pinos") == E_["values"]["n_pinos"] == len(vv_.get("pinos") or {}) and all(p_.get("sha256_ok") is True and p_.get("bytes_ok") is True for p_ in (vv_.get("pinos") or {}).values()) and vv_.get("ramos_vistos") == [1, 2, 3, 4, 5, 6] and all(x_.get("ok") is True for x_ in vv_.get("vetores_c6") or [])
                and R_.get("veredito_h0dn_source_sha256") == vv_.get("veredito_h0dn_source_sha256") == E_["values"]["veredito_h0dn_source_sha256"] and vv_.get("gate_verdict") == ESP["qg_closure_gate_verdict_v409"]
                and vv_.get("sob_pasta_vedada") == [] and vv_.get("com_nome_vedado") == [] and isinstance(vv_.get("n_caminhos_tocados"), int) and vv_.get("n_caminhos_tocados") == len(_toc_) > 0
                and not [p_ for p_ in _toc_ if _nrm_(p_) == _ved_ or _nrm_(p_).startswith(_ved_ + os.sep) or any(n_ in os.path.basename(_nrm_(p_)) for n_ in _nomes_)]
                and "NOT_FALSIFIED" not in v_ and not GUARDA.search(v_) and v_.endswith("__GATE_UNMOVED")
                and _feq({kk_: vv_.get(kk_) for kk_ in E_["values"]}, E_["values"]))


'''
troca_arquivo("conferir_rito_v410.py", [
    ('_tt = lambda m_: m_.replace(chr(92) + "beta", "β")   #', '_tt = lambda m_: m_.replace(chr(92) + "beta", "β").replace(chr(92) + "times", "×")   # (v410, D72: o titulo da secao do H0DN traz $\\times$; o TXT do artigo (um.py:_tex_to_txt) o rende ×)', 1),
    ('IV = core.get("iald2_v410") or {}\n', 'IV = core.get("iald2_v410") or {}; HV = core.get("h0dn_bg1_v410") or {}   # (D72) o SEGUNDO registro com FUNCAO da v410: pré-registrado; nenhum dado observado lido\n', 1),
    ("\n\ndef _traducao409_ok():\n", "\n\n" + H0DN_OK + "def _traducao409_ok():\n", 1),
    ("iald2_ok = _iald2_ok(); traducao409_ok = _traducao409_ok();", "iald2_ok = _iald2_ok(); h0dn_ok = _h0dn_ok(); traducao409_ok = _traducao409_ok();", 1),
    ('_sec410 = {l: (txt[l][_ini410[l]:_fim410[l]] if 0 <= _ini410[l] < _fim410[l] else "") for l in ("pt", "en")}\n',
     '_sec410 = {l: (txt[l][_ini410[l]:_fim410[l]] if 0 <= _ini410[l] < _fim410[l] else "") for l in ("pt", "en")}\n'
     '# (D72) a secao do H0DN: logo DEPOIS da secao da IALD2 e ANTES da secao da v409 (dentro do trecho _sec410), com a obrigacao nas duas linguas, sem a frase de guarda (o registro selou) e limpa na guarda das frases\n'
     '_iniH = {l: txt[l].find(_tt(ESP["titulo_secao_h0dn_v410"][l]), max(_ini410[l], 0)) for l in ("pt", "en")}\n'
     '_secH = {l: (txt[l][_iniH[l]:_fim410[l]] if 0 <= _ini410[l] < _iniH[l] < _fim410[l] else "") for l in ("pt", "en")}\n'
     'h0dn_secao_ok = bool(_secH["pt"] and _secH["en"] and DL.FRASE_H0DN_OBRIGATORIA_PT in _secH["pt"] and DL.FRASE_H0DN_OBRIGATORIA_EN in _secH["en"] and "NÃO selou" not in _secH["pt"] and "did NOT seal" not in _secH["en"] and not GF.violacoes(_secH["pt"]) and not GF.violacoes(_secH["en"]))\n', 1),
    ('\n    "as %d ANCORAS da pedra IALD2 (o NOME do modulo do operador;',
     '\n    "h0dn_bg1_v410 SELOU (D72; o SEGUNDO registro com FUNCAO, novo; pré-registrado; nenhum dado observado lido): veredito == o do ensaio == o PRE-REGISTRADO; as %d checagens; observed_vector_read False; os %d pinos (os 9 do FREEZE_R2 mais o FREEZE_R2 e a ENTREGA) batendo; os 6 ramos da funcao de veredito congelada nos vetores deterministicos; o sha256 da funcao == o do ensaio; nenhum caminho tocado sob a pasta vedada (a entrega do Kimi) nem com nome vedado; os valores == os do ensaio; nao move o gate" % (DL.N_CHECKS_H0DN, ESP["registros_funcao_v410"]["h0dn"]["values"]["n_pinos"]): h0dn_ok,\n'
     '    "a secao do H0DN no artigo PT/EN (pré-registrado; nenhum dado observado lido) vem logo DEPOIS da secao da IALD2 e ANTES da secao da v409, traz a obrigacao D72 nas duas linguas, nao traz a frase de guarda (o registro selou) e passa a guarda das frases": h0dn_secao_ok,\n'
     '    "o .md canonico: a linha do H0DN (ESP md_h0dn) vem DEPOIS da linha da IALD2 e ANTES da linha da v409, com a obrigacao D72 na propria linha": bool(ESP["md_h0dn"] in fc and fc.find(ESP["md_iald2"]) < fc.find(ESP["md_h0dn"]) < fc.find(ESP["md_traducao"]) and DL.FRASE_H0DN_OBRIGATORIA_PT in fc[fc.find(ESP["md_h0dn"]):].split("\\n", 1)[0]),\n'
     '    "as %d ANCORAS da pedra IALD2 (o NOME do modulo do operador;', 1),
    ('"traducao_turing_v409", "iald2_v410")', '"traducao_turing_v409", "iald2_v410", "h0dn_bg1_v410")', 1),
    ('"nenhuma chave nova fora da lista da v410 (so\' o registro com funcao iald2_v410 e os registros por spec', '"nenhuma chave nova fora da lista da v410 (so\' os registros com funcao iald2_v410 e h0dn_bg1_v410 e os registros por spec', 1),
    ('"veredito_iald2": V("iald2_v410"),', '"veredito_iald2": V("iald2_v410"), "veredito_h0dn": V("h0dn_bg1_v410"), "h0dn_observed_vector_read": HV.get("observed_vector_read"), "h0dn_sob_pasta_vedada": (HV.get("values") or {}).get("sob_pasta_vedada"),', 1),
], marca="# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_conferidores_v410.py] D72: o SEGUNDO registro com funcao, h0dn_bg1_v410 (pré-registrado; nenhum dado observado lido), conferido no core, no selo, no artigo (a secao depois da IALD2, antes da v409; _tt rende \\times) e no .md")

# (2) conferir_instalar_rito_v410.py
troca_arquivo("conferir_instalar_rito_v410.py", [
    ('assert _DEC_NOVAS and _DEC_NOVAS[0] == "D63" and _DEC_NOVAS[-1] == "D70", _DEC_NOVAS',
     'assert _DEC_NOVAS and _DEC_NOVAS[0] == "D63" and _DEC_NOVAS[-1] == DL.DECISOES_V410[-1] == "D77", _DEC_NOVAS   # (09/11: D63..D77 -- a retomada, D72 o H0DN pre-registrado, D74 os nomes ratificados, D76 a cabeca do 5 sigma, D77 as pendencias)', 1),
    ('assert _ERR_NOVAS == ["E29"], _ERR_NOVAS', 'assert _ERR_NOVAS == ["E29", "E30"], _ERR_NOVAS   # (09/11: a E30, em nome proprio da gerencia c1: a cabeca do ramo de 5 sigma e\' a leitura, nunca a palavra do livro de cobrancas)', 1),
    ('"as decisoes %s a %s e a errata %s vao nos registros" % (_DEC_NOVAS[0], _DEC_NOVAS[-1], _ERR_NOVAS[0]), "IALD2",',
     '"as decisoes %s a %s e as erratas %s e %s vao nos registros" % (_DEC_NOVAS[0], _DEC_NOVAS[-1], _ERR_NOVAS[0], _ERR_NOVAS[1]), "IALD2", "h0dn_bg1_v410", "%d checagens do H0DN" % DL.N_CHECKS_H0DN, DL.FRASE_H0DN_OBRIGATORIA_PT, "o teste PRE-REGISTRADO da razao de Hubble H0DN x BG1", "le as %d ancoras do axiom_report do rito" % len(DL.ANCORAS),', 1),
    ('"%d falas de 06/11" % DL.N_FALAS_V410, "%d checagens" % DL.N_CHECKS_FECHO,', '"%d falas de 06, 07, 08 e 09/11" % DL.N_FALAS_V410, "%d checagens com as instancias de brinquedo fixas" % DL.N_CHECKS_FECHO,', 1),
    ('"o registro com FUNCAO traducao_turing_v409"])', '"o registro com FUNCAO traducao_turing_v409", "19 ancoras", "9 falas de 06/11", "15 checagens", "D63 a D70", "e a errata E29 vao", "MEDIDO em 06/11/2026", "[DECLARADO] ate a ratificacao (D63);"])   # (09/11: os rotulos de 06/11, anteriores a retomada, ficam proibidos no rito)', 1),
], marca="# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_conferidores_v410.py] D72/D74/D76/D77: as decisoes vao a D77 e as erratas sao E29 e E30 (lidas de DL); o rito tem de trazer o h0dn_bg1_v410, os numeros da retomada (22 ancoras, 15 falas, 16 + 12 checagens) e o tempo MEDIDO em 09/11; os rotulos de 06/11 ficam proibidos")

# (3) rito_v410.sh -- so' o texto descritivo do cabecalho (o corpo do rito nao muda)
troca_arquivo("rito_v410.sh", [
    ("IALD2 -- o leitor do codigo, a releitura que nao acrescenta, o algoritmo IALD, o signo e o seletor): roda o um.py v410",
     "IALD2 -- o leitor do codigo, a releitura que nao acrescenta, o algoritmo IALD, o signo, o seletor e o atrator; e o teste PRE-REGISTRADO da razao de Hubble H0DN x BG1, D72: %s): roda o um.py v410" % Q, 1),
    ("os nomes das declaracoes da gerencia, [DECLARADO] ate a ratificacao (D63);", "os nomes das declaracoes da gerencia, RATIFICADOS pelo operador em 09/11/2026 (D63, D74);", 1),
    ("le as 19 ancoras do axiom_report do rito, as fontes embutidas por sha256, as 9 falas de 06/11 por sha256 [de uma, so' o trecho: D65] e a escada; faz as 15 checagens com as instancias de brinquedo fixas; as decisoes D63 a D70 e a errata E29 vao nos registros;",
     "le as %d ancoras do axiom_report do rito, as fontes embutidas por sha256, as %d falas de 06, 07, 08 e 09/11 por sha256 [de quatro, so' o trecho: D65; a ordem da retomada de 09/11; as tres copias do ACOM; a leitura do 5 sigma] e a escada; faz as %d checagens com as instancias de brinquedo fixas; as decisoes D63 a D77 e as erratas E29 e E30 vao nos registros; "
     "e, na MESMA instrucao do main, logo depois, o registro com FUNCAO h0dn_bg1_v410 (D72: o teste PRE-REGISTRADO da razao de Hubble H0DN x BG1 -- %s --: os insumos embutidos por sha256, K recomputado de beta em runtime, a funcao de veredito congelada com a cabeca da D76 e a E30, faz as %d checagens do H0DN; nenhum vetor observado e' lido nem procurado; a pasta da entrega do Kimi e' vedada e a c7 o mede);" % (NA, NF, NC, Q, NH), 1),
    ("(cunhagens_v410, com as 9 falas de 06/11, o NOME do modulo do operador, as decisoes D63 a D70 e a errata E29;",
     "(cunhagens_v410, com as %d falas de 06, 07, 08 e 09/11, o NOME do modulo do operador, os nomes das declaracoes ratificados (D74), as decisoes D63 a D77, as erratas E29 e E30 e a dos pisos da v409;" % NF, 1),
    ("nenhuma decisao da v410 [D63 a D70] as muda)", "nenhuma decisao da v410 [D63 a D77] as muda)", 1),
    ("MEDIDO em 06/11/2026 no sandbox k410c)", "MEDIDO em 09/11/2026 no sandbox k410c, com o Audit refeito depois da queda de energia; os numeros abaixo sao os de kernel/construir_marcas.txt)", 1),
    ("= 477 s e 1 Audit = 346 s (a soma dos tempos por modulo e' 36.0 s, o maximo de um modulo 36.0 s)", "= %d s e 1 Audit = %d s (a soma dos tempos por modulo e' %s s, o maximo de um modulo %s s)" % (BUILD_S, AUDIT_S, SOMA_S, MAX_S), 1),
    ("a ordem de grandeza e' a medida do sandbox, 477 s + 346 s)", "a ordem de grandeza e' a medida do sandbox, %d s + %d s)" % (BUILD_S, AUDIT_S), 1),
    ("(build ja' pronto + Audit de 346 s)", "(build ja' pronto + Audit de %d s)" % AUDIT_S, 1),
], marca="# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_conferidores_v410.py] so' o texto descritivo do cabecalho: os numeros da retomada (lidos do delta e das marcas do kernel: %d ancoras, %d falas, %d + %d checagens, build %d s, Audit %d s) e o registro h0dn_bg1_v410 (D72: %s); o corpo do rito nao muda" % (NA, NF, NC, NH, BUILD_S, AUDIT_S, Q), py=False)

# (4) fechar_preparacao_v410.py
troca_arquivo("fechar_preparacao_v410.py", [
    ('_ab = json.load(open(ABERTA_, encoding="utf-8"))[0]\n', '_ab0 = json.load(open(ABERTA_, encoding="utf-8")); _ab = _ab0[0] if isinstance(_ab0, list) else _ab0   # (09/11: o registro ABERTO do Mapa da v410 e\' UM objeto; o da v409 era lista -- achado do revisor Sonnet)\n', 1),
], marca="# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_conferidores_v410.py] o registro ABERTO do Mapa e' um objeto, nao lista (o [0] quebrava); segue ato da gerencia, nao executado pelo construtor")

# (5) _teste_h0dn_offline_v410.py
troca_arquivo("_teste_h0dn_offline_v410.py", [
    ('Nada escrito fora do stdout. uso: python -I -B -X utf8 _teste_h0dn_offline_v410.py"""', 'Grava TESTE_H0DN_OFFLINE_v410.json (o gerar_relatorio o le, informativo). uso: python -B -X utf8 _teste_h0dn_offline_v410.py   (sem -I: numpy e\' do site do usuario, D77f)"""', 1),
    ('print("TUDO PASSOU" if (out["all_verified"] and not out_b["all_verified"] and not out_c["all_verified"] and not out_d["all_verified"]) else "FALHOU")\n',
     '_tudo = bool(out["all_verified"] and not out_b["all_verified"] and not out_c["all_verified"] and not out_d["all_verified"])\n'
     'print("TUDO PASSOU" if _tudo else "FALHOU")\n'
     '_J = {"tudo_passou": _tudo, "quando": __import__("datetime").datetime.now().isoformat(timespec="seconds"), "veredito": out["verdict"], "all_verified": out["all_verified"], "observed_vector_read": out["observed_vector_read"], "n_checks": (out.get("mechanics") or {}).get("n_checks"), "checks": [(c["id"], c["ok"]) for c in (out.get("mechanics") or {}).get("checks") or []],\n'
     '      "n_pinos": v.get("n_pinos"), "ramos_vistos": v.get("ramos_vistos"), "n_caminhos_tocados": v.get("n_caminhos_tocados"), "sob_pasta_vedada": v.get("sob_pasta_vedada"), "com_nome_vedado": v.get("com_nome_vedado"), "veredito_h0dn_source_sha256": v.get("veredito_h0dn_source_sha256"),\n'
     '      "controles_negativos": {"pino_adulterado": out_b["verdict"], "gate_trocado": out_c["verdict"], "z_star_trocado": out_d["verdict"]}, "nota": "teste OFFLINE do registro sobre o core da v409 selada (nao e\' o rito nem o ensaio); " + DL.FRASE_H0DN_OBRIGATORIA_PT}\n'
     '_p = os.path.join(HERE, "TESTE_H0DN_OFFLINE_v410.json"); open(_p + ".tmp", "w", encoding="utf-8").write(json.dumps(_J, ensure_ascii=False, indent=1, default=str)); os.replace(_p + ".tmp", _p)\n', 1),
])
print("ok")
