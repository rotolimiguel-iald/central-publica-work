# -*- coding: utf-8 -*-
"""_adapt_ensaio_v411.py -- (claude-construtor-v411, fork C, 12/11/2026) monta ensaio_a_seco_v411.py a partir do ORIGINAL ..\\v410\\ensaio_a_seco_v410.py (NAO da copia bumpada: nela o bump estragou a heranca),
com trocas DITAS e cada ancora unica (a geracao PARA se uma ancora nao casar o numero de vezes esperado):
 (a) as partes gerais passam a v411: o delta da v411 (com as pontes sys.modules delta_v410 -> DL.D10 etc.), a base v410 selada, o manifesto por DL.MANIFESTO_ARQ, o candidato/artefato por DL.CANDIDATO_ARQ, o dry em
     DL.DRY_DIR (fora de work), as saidas por DL.saida(...) com DL.MARCA_ENSAIO, UM_VERSION v411, a escada sem bandeira nova (o kernel e' o da v410), os registros da v410 RECRIADOS e comparados com os selados,
     as chaves novas do core = as da v411 (h0dn_bg1_v411, cunhagens_v411, kh_n1_cobertura_v411), a troca dita vira troca_dita_v411 (nenhuma), o selo com h0dn_bg1_v411 e registros_v411;
 (b) os blocos (6p, 6p-b, 6p-c, 6p-d) da v410 viram HERANCA: DL.X -> DL.D10.X, CM -> _CM10 (o manifesto da v410 selada), KD -> _KD10 (o kernel dir da v410), E409 -> a escada da base da v410 (_E409_10),
     o registros_aescala_v410 e a guarda das frases da v410 carregados por caminho; a checagem do kh_n1_cobertura_v410 passa de «igualdade exata» a «virou piso» (C13 da v411), como a v410 fez com o da v409;
 (c) blocos NOVOS: (5b-v411) a ordem de chamada do h0dn_bg1_v411 por AST com tres controles negativos; (6q) o registro h0dn_bg1_v411 (tudo certo; numeros recalculados por outro caminho; os controles negativos no
     ponto real; o P2 ao lado da v387) e os specs cunhagens_v411 (E41, E42, E43) e kh_n1_cobertura_v411 (a igualdade exata); (8) o artigo da v411 (o quadro acima do da v397, a remissao, o topo, as trocas, a frase ao lado
     do estatuto e do coracao, o P2 ao lado na secao da v387, a secao nova antes da da v410, as duas guardas com a UNICA excecao da P18, sem n/d, o A2) e a variante sem os registros da v411; (9) a linha do .md;
     (11)-(13) os subprocessos da v411 (simular_arvore, exame_pontos, guardas estaticas) com saida em DL.saida.
Backup de BYTES do destino antes. uso: python -B -X utf8 _adapt_ensaio_v411.py"""
import ast, datetime, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "v410", "ensaio_a_seco_v410.py")
DST = os.path.join(HERE, "ensaio_a_seco_v411.py")
t = open(SRC, "rb").read().decode("utf-8"); assert "\r" not in t
LOG = []


def troca(a_, n_, cnt=1):
    global t
    assert t.count(a_) == cnt, ("ancora", a_[:120], t.count(a_), cnt)
    t = t.replace(a_, n_); LOG.append(a_[:60])


def troca_re(rx_, n_, cnt=1, flags=0):
    global t
    m_ = re.findall(rx_, t, flags); assert len(m_) == cnt, ("ancora re", rx_[:120], len(m_), cnt)
    t = re.sub(rx_, n_, t, flags=flags)


def insere_depois_da_linha(prefixo_, novo_):
    global t
    assert t.count("\n" + prefixo_) == 1, ("ancora de linha", prefixo_[:120], t.count("\n" + prefixo_))
    i_ = t.index("\n" + prefixo_) + 1; j_ = t.index("\n", i_) + 1
    t = t[:j_] + novo_ + t[j_:]


# ======================================================== (b) a HERANCA dos blocos da v410 (6p .. 6p-d): a regiao ate' o artigo
I0 = t.index("# (6p) [v410] OS DOIS REGISTROS COM FUNCAO NOVOS (D72)"); I1 = t.index("# (8) o artigo\n")
seg = t[I0:I1]
seg = re.sub(r"\bDL\.(?!D\d+\b|V4\d\d\b)", "DL.D10.", seg)
seg = re.sub(r"\bCM\[", "_CM10[", seg); seg = re.sub(r"\bCM\.get\(", "_CM10.get(", seg)
seg = seg.replace("os.path.join(KD, ", "os.path.join(_KD10, ")
seg = re.sub(r"\bE409\b", "_E409_10", seg)
assert seg.count('_sha_base10 = hashlib.sha256(open(os.path.join(BASE, "um.py"), "rb").read()).hexdigest()') == 1   # (a base DA v410 e' a v409: o contrato da v410 pina o um.py da v409)
seg = seg.replace('_sha_base10 = hashlib.sha256(open(os.path.join(BASE, "um.py"), "rb").read()).hexdigest()', '_sha_base10 = hashlib.sha256(open(os.path.join(DL.V410, DL.D10.BASE_DIR, "um.py"), "rb").read()).hexdigest()   # (v411: a base da v410 e\' a v409 selada, copia em v410\\\\base_v409)')
assert seg.count('__import__("registros_v410")') == 2
seg = seg.replace('__import__("registros_v410")', '_mod410("registros_v410")')   # (v411: o modulo da cadeia da v410, carregado por caminho)
seg = seg.replace('os.path.join(HERE, "ESPERADOS_v410.pre_r1fix.json")', 'os.path.join(DL.V410, "ESPERADOS_v410.pre_r1fix.json")')
assert seg.count("import registros_aescala_v410 as _RAx  # noqa: E402") == 1
seg = seg.replace("import registros_aescala_v410 as _RAx  # noqa: E402",
                  "_spRAx = _ilu8.spec_from_file_location(\"registros_aescala_v410\", os.path.join(DL.V410, \"registros_aescala_v410.py\")); _RAx = _ilu8.module_from_spec(_spRAx); _spRAx.loader.exec_module(_RAx)   # (v411: HERANCA, carregado por caminho da cadeia da v410)\n"
                  "if os.path.join(DL.V410) in sys.path: sys.path.remove(os.path.join(DL.V410))   # (o modulo da v410 poe a pasta dele no sys.path: tirada, para nada da v410 sombrear a v411)")
# a checagem do kh_n1_cobertura_v410: de «igualdade exata» a «virou piso» (C13 da v411; a igualdade exata esta' no kh_n1_cobertura_v411, bloco (6q))
a_ = seg.index('U["kh_n1_cobertura_v410_selou_a_igualdade_exata_e_as_v409_sao_piso"] = bool(')
b_ = seg.index("\n# ---- (6p-b)", a_)
seg = seg[:a_] + (
    '_cov9_10 = {"decl": _KHT10["linha_TOTAL"]["decl"] - _KHT10["delta_vs_v409"]["decl"], "thm": _KHT10["linha_TOTAL"]["thm"] - _KHT10["delta_vs_v409"]["thm"]}   # (v411) a cobertura da v409 selada, recomposta da medida da v410 (o h7/h7b do spec herdado a pinam como piso)\n'
    'U["kh_n1_cobertura_v410_herdado_virou_piso_e_selou_na_v411"] = bool(_kh10x.get("all_verified") is True and _kh9x.get("all_verified") is True and (_kh10x.get("extras") or {}).get("n_modulos") == DL.D10.N_BUNDLE and (_kh10x.get("extras") or {}).get("n_bandeiras") == _CM10["n_bandeiras"]\n'
    '                                                                        and {i_: _ck10[i_]["op"] for i_ in ("h2", "h3", "h6", "h8")} == {"h2": "maior_igual", "h3": "maior_igual", "h6": "tamanho_maior_igual", "h8": "tamanho_maior_igual"} and len(_kh10s["erratas"]) >= 2 and "v411" in str(_kh10s["erratas"][-1].get("agora"))\n'
    '                                                                        and _ck10["h2"]["valor"] == _KHT10["linha_TOTAL"]["decl"] == _ck10["h6"]["valor"] and _ck10["h3"]["valor"] == _KHT10["linha_TOTAL"]["thm"] and _ck10["h8"]["valor"] == CM["h8"]["pino_antigo_v410_entradas"] and len(_kf0["formal_files_sha256"]) >= _ck10["h8"]["valor"]\n'
    '                                                                        and _ck10["h7"]["valor"] == _cov9_10["decl"] and _ck10["h7b"]["valor"] == _cov9_10["thm"] and (_kh10x.get("extras") or {}).get("delta_vs_v409") == _KHT10["delta_vs_v409"]\n'
    '                                                                        and _kf0["axiom_coverage_v392"]["decl"] >= _KHT10["linha_TOTAL"]["decl"] and _kf0["axiom_coverage_v392"]["thm"] >= _KHT10["linha_TOTAL"]["thm"] and _kf0["axiom_coverage_v392"]["fora_do_trio"] == 0)   # (v411, C13) o spec da v410 HERDADO virou piso; o veredito dele nao muda') + seg[b_:]
seg = ("# (v411) OS BLOCOS (6p) A (6p-d) ABAIXO SAO HERANCA da v410 (a v411 os recria e confere como a v410 fez com o (6o) da v409): os nomes da v410 vem do DL.D10, os numeros do candidato da v410 do _CM10, as bandeiras do\n"
       "# FLAGS da v410 (_KD10), a guarda das frases da v410 (_GF5, carregada por caminho); o kh_n1_cobertura_v410 virou piso (C13). Os rotulos [v410] dos comentarios ficam como no molde.\n") + seg
t = t[:I0] + seg + t[I1:]

# ======================================================== (a) as partes gerais
l1 = t.split("\n", 1)[0]; assert l1.startswith("# -*- coding")
troca(l1 + "\n", l1 + "\n# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork C)] montado por _adapt_ensaio_v411.py do ORIGINAL v410/ensaio_a_seco_v410.py (nao da copia bumpada): as partes gerais da v411 (sem modulo novo;"
      " o registro com funcao h0dn_bg1_v411 e os specs cunhagens_v411/kh_n1_cobertura_v411); os blocos (6p..6p-d) da v410 viram HERANCA (DL.D10, _CM10, _KD10); blocos novos (5b-v411), (6q), o artigo, o .md e a variante da v411; saidas em DL.saida e o dry fora de work.\n")
troca('"""ensaio_a_seco_v410.py -- ENSAIO A SECO da v410 (molde:',
      '"""ensaio_a_seco_v411.py -- [v411, 12/11/2026, claude-construtor-v411, fork C] ENSAIO A SECO da v411: a v411 NAO tem modulo novo de kernel (o kernel e\' o da v410 byte a byte, escada lida do core da base, nenhuma bandeira nova);\n'
      'UM registro com FUNCAO, h0dn_bg1_v411 (o teste H0DN x BG1 aberto uma vez, depois do commit publico do pre-registro, RECALCULADO no rito a partir dos bytes embutidos; 16 checagens; o primario sob o modelo de erros publicado\n'
      'e, ao lado, as Cefeidas livres; o P2 ao lado da v387), e os specs cunhagens_v411 (as 9 falas de 11 e 12/11; D159 a D170; E41, E42 e E43) e kh_n1_cobertura_v411; os quatro registros com funcao da v410 e os specs da v410\n'
      'sao HERANCA (recriados e comparados com os da v410 selada). Retrodicao sem ajuste, com emenda posterior a guarda; teste nao cego; provado e\' validade, nao creditacao; o gate nao se move. Com V411_ENSAIO_TOPO_PROPOSTO=1 o\n'
      'ensaio roda sobre o ARTEFATO DE ENSAIO do topo proposto (fora de work; NAO e\' candidato). O texto abaixo e\' o do molde da v410, que fica como registro do que cada secao herdada confere.\n'
      'ensaio_a_seco_v410.py -- ENSAIO A SECO da v410 (molde:')
troca("uso: python -B -X utf8 ensaio_a_seco_v410.py <candidato.py> <rotulo>", "uso: python -B -X utf8 ensaio_a_seco_v411.py [<candidato.py> <rotulo>]")
troca("import delta_v410 as DL  # noqa: E402\n", "import delta_v411 as DL  # noqa: E402\n")
troca('sys.modules.setdefault("delta_v409", DL.D9); sys.modules.setdefault("delta_v408", DL.D8); sys.modules.setdefault("delta_v407", DL.D7)   # (v410)',
      'sys.modules.setdefault("delta_v410", DL.D10); sys.modules.setdefault("delta_v409", DL.D9); sys.modules.setdefault("delta_v408", DL.D8); sys.modules.setdefault("delta_v407", DL.D7)   # (v411: a ponte da v410 tambem, para a HERANCA da v410) (v410)')
troca('BASE = os.path.join(HERE, DL.BASE_DIR); CORE0P = os.path.join(BASE, "um_absoluto.json"); SELO0P = os.path.join(BASE, "um_absoluto_selo.json")   # a v409 SELADA',
      'BASE = os.path.join(HERE, DL.BASE_DIR); CORE0P = os.path.join(BASE, "um_absoluto.json"); SELO0P = os.path.join(BASE, "um_absoluto_selo.json")   # a v410 SELADA')
troca('cand = sys.argv[1] if len(sys.argv) > 1 else DL.CANDIDATO; rot = sys.argv[2] if len(sys.argv) > 2 else "v410"\nDRY = os.path.join(HERE, "dry_" + rot)\n',
      'cand = sys.argv[1] if len(sys.argv) > 1 else DL.CANDIDATO_ARQ; rot = sys.argv[2] if len(sys.argv) > 2 else "v411"\nDRY = DL.DRY_DIR if rot == "v411" else os.path.join(DL.RODADA_PAI, "dry_" + rot)   # (v411, D135: o dry fica FORA de work)\n')
troca('CM = json.load(open(os.path.join(HERE, "CANDIDATO_v410.json"), encoding="utf-8")); assert CM["sha16"] == h16\n',
      'CM = json.load(open(DL.MANIFESTO_ARQ, encoding="utf-8")); assert CM["sha16"] == h16, ("o manifesto nao e\' deste arquivo", CM["sha16"], h16)\n'
      '_CM10 = json.load(open(os.path.join(DL.V410, "CANDIDATO_v410.json"), encoding="utf-8"))   # (v411) o candidato da v410 SELADA: os numeros dos blocos HERDADOS da v410 saem dele e do DL.D10, nunca do DL da v411\n'
      'assert _CM10["sha16"] == DL.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v410.json nao e\' o da v410 selada", _CM10["sha16"])\n'
      '_KD10 = os.path.join(DL.V410, DL.D10.KERNEL_DIR); _E409_10 = int(_CM10["escada"][0])   # (v411) o kernel dir da v410 (FLAGS, KH_N1 da v410) e a escada da base da v410 (a da v409)\n')
troca('assert _CM9["sha16"] == DL.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v409.json nao e\' o da v409 selada", _CM9["sha16"])', 'assert _CM9["sha16"] == DL.D10.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v409.json nao e\' o da v409 selada", _CM9["sha16"])')
troca('"SEM_GPU_SEM_RITO": "o core da v409 selada + o kernel REAL lido pelo verify com os logs crus do sandbox"}', '"SEM_GPU_SEM_RITO": "o core da v410 selada + o kernel REAL lido pelo verify com os logs crus do sandbox", **DL.MARCA_ENSAIO}')
troca('assert um.UM_VERSION == "v410"', 'assert um.UM_VERSION == "v411"')
troca('and "kh_n1_cobertura_v402" in core0 and selo0["um_version"] == "v409"', 'and "kh_n1_cobertura_v402" in core0 and selo0["um_version"] == "v410"')
troca('assert rep["escada_sem_as_bandeiras_novas"][0] == E409 and rep["escada_sem_as_bandeiras_novas"][1] == ESP and _el0.get("all_verified") is not True and ESP == E409 + CM["n_bandeiras"], rep["escada_sem_as_bandeiras_novas"]',
      'assert rep["escada_sem_as_bandeiras_novas"][0] == E409 == ESP and rep["escada_sem_as_bandeiras_novas"][1] == ESP and _el0.get("all_verified") is True and CM["n_bandeiras"] == 0, rep["escada_sem_as_bandeiras_novas"]   # (v411: SEM bandeira nova, o kf da v410 ja\' fecha a escada do candidato: o kernel e\' o da v410)')
troca('tagged = {i + 1 for i, l in enumerate(lines) if "v393" in l', 'tagged = {i + 1 for i, l in enumerate(lines) if "v411" in l or "v393" in l')
troca("+ list(um._V409_REGISTROS_FUNCAO) + list(um._V409_NOMES_REGISTROS)   # (v410) os registros da v407", "+ list(um._V409_REGISTROS_FUNCAO) + list(um._V409_NOMES_REGISTROS) + list(um._V410_REGISTROS_FUNCAO) + list(um._V410_NOMES_REGISTROS)   # (v411: e os da v410, HERANCA) (v410) os registros da v407")
troca("V410N = list(um._V410_REGISTROS_FUNCAO) + list(um._V410_NOMES_REGISTROS)   # os registros NOVOS da v410", "V411N = list(um._V411_REGISTROS_FUNCAO) + list(um._V411_NOMES_REGISTROS)   # (v411) os registros NOVOS da v411: h0dn_bg1_v411, cunhagens_v411, kh_n1_cobertura_v411 (molde v410:)")
t = re.sub(r"\bV410N\b", "V411N", t); t = re.sub(r"\bNOVAS410\b", "NOVAS411", t)
troca('"recriados_v393_a_v409": recriados', '"recriados_v393_a_v410": recriados')
troca('"registros_novos_v410": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in V411N},', '"registros_novos_v411": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in V411N},')
troca('rep["mainflow"].items() if k not in ("stdout", "recriados_v393_a_v409", "veracidade")', 'rep["mainflow"].items() if k not in ("stdout", "recriados_v393_a_v410", "veracidade")')
t = t.replace("troca_dita_v410", "troca_dita_v411")
troca("import guarda_ordem_de_chamada_v410 as _GOC", "import guarda_ordem_de_chamada_v411 as _GOC")
troca("_ordem = _GOC.ordem_de_chamada(src, _GOC.FUNCOES_V410)", "_ordem = _GOC.ordem_de_chamada(src, _GOC.FUNCOES_V411)")
troca('rep["ordem_de_chamada_v410"] = _ordem', 'rep["ordem_de_chamada_v411"] = _ordem')
troca('rep["ordem_de_chamada_v410_controle_negativo"] = _ctl_ordem', 'rep["ordem_de_chamada_v411_controle_negativo"] = _ctl_ordem')
troca('U["v410_ordem_de_chamada_todo_insumo_do_core_pronto_antes_da_leitura_com_controle_negativo"] = bool(_ordem["ok"] and _ctl_ordem["ok"] and all((_ordem["funcoes"].get(n_) or {}).get("n_chaves_lidas", 0) >= 3 for n_ in _GOC.FUNCOES_V410))',
      'U["v411_ordem_de_chamada_todo_insumo_do_core_pronto_antes_da_leitura_com_controle_negativo"] = bool(_ordem["ok"] and _ctl_ordem["ok"] and all((_ordem["funcoes"].get(n_) or {}).get("n_chaves_lidas", 0) >= 3 for n_ in _GOC.FUNCOES_V411))')
troca('tempfile.mkdtemp(prefix="v410_ens_")', 'tempfile.mkdtemp(prefix="v411_ens_")')
troca('tempfile.mkdtemp(prefix="v410_sidecar_")', 'tempfile.mkdtemp(prefix="v411_sidecar_")')
troca("import acom_conferencias_v410 as AC  # noqa: E402", "import acom_conferencias_v411 as AC  # noqa: E402")
troca("import guarda_frases_v410 as _GF5\n",
      "import importlib.util as _ilu8   # (v411) a guarda das frases da v410, por CAMINHO, para os textos HERDADOS (v405 a v410: texto selado; as regras novas da v411, F60 a F67, julgam so' o texto novo, bloco (6q) e o artigo da v411)\n"
      "_sp10r = _ilu8.spec_from_file_location(\"runtime_v410\", os.path.join(DL.V410, \"runtime_v410.py\")); _rt10m = _ilu8.module_from_spec(_sp10r); _sp10r.loader.exec_module(_rt10m); sys.modules.setdefault(\"runtime_v410\", _rt10m)\n"
      "_sp10p = _ilu8.spec_from_file_location(\"guarda_p18_v410\", os.path.join(DL.V410, \"guarda_p18_v410.py\")); _gp10m = _ilu8.module_from_spec(_sp10p); _sp10p.loader.exec_module(_gp10m); sys.modules.setdefault(\"guarda_p18_v410\", _gp10m)\n"
      "_sp10g = _ilu8.spec_from_file_location(\"guarda_frases_v410\", os.path.join(DL.V410, \"guarda_frases_v410.py\")); _GF5 = _ilu8.module_from_spec(_sp10g); _sp10g.loader.exec_module(_GF5)\n"
      "while DL.V410 in sys.path: sys.path.remove(DL.V410)   # (a guarda da v410 poe a pasta dela no sys.path: tirada, para nada da v410 sombrear a v411)\n"
      "_MOD410 = {}\n\n\n"
      "def _mod410(nome_):\n"
      "    \"\"\"(v411) um modulo da cadeia da v410 (HERANCA), carregado por CAMINHO uma vez, com a pasta da v410 no FIM do sys.path so' durante a carga (os imports dele, *_v410, sao da pasta dele; nada da v410 sombreia a v411).\"\"\"\n"
      "    if nome_ not in _MOD410:\n"
      "        sys.path.append(DL.V410)\n"
      "        try:\n"
      "            sp_ = _ilu8.spec_from_file_location(nome_, os.path.join(DL.V410, nome_ + \".py\")); m_ = _ilu8.module_from_spec(sp_); sys.modules.setdefault(nome_, m_); sp_.loader.exec_module(m_); _MOD410[nome_] = m_\n"
      "        finally:\n"
      "            while DL.V410 in sys.path: sys.path.remove(DL.V410)\n"
      "    return _MOD410[nome_]\n\n\n"
      "import guarda_frases_v411 as _GF11  # noqa: E402   (a guarda das frases da v411, com a UNICA excecao da P18: _GF11.p18_sem_cabeca)\n")
# a escada pinada pelos contratos: a v411 nao traz contrato novo com expected_ladder (o do H0DN v411 pina baseline.escada); os contratos da v410 (IALD2, AEscala) seguem pinando a mesma escada
troca('and um._V409_TRADUCAO_CONTRACT["expected_ladder"] == ESP and _n_esc_base >= 1 and _n_esc_cand == _n_esc_base + 2 and not re.search(r"\'expected_ladder\': %d\\b" % E409, src))',
      'and um._V409_TRADUCAO_CONTRACT["expected_ladder"] == ESP and um._V410_IALD2_CONTRACT["expected_ladder"] == ESP and um._V410_AESCALA_CONTRACT["expected_ladder"] == ESP and _n_esc_base >= 1 and _n_esc_cand == _n_esc_base and E409 == ESP\n'
      '                                                          and um._V411_H0DN_CONTRACT["baseline"]["escada"] == ESP)   # (v411: sem bandeira nova a escada nao muda; nenhum contrato novo com expected_ladder: o do H0DN v411 pina baseline.escada)')
troca('rep["contratos_pinam_a_escada"] = {"expected_ladder_no_selado_da_v409": _n_esc_base, "expected_ladder_no_candidato": _n_esc_cand, "escada_da_v409": E409, "escada_da_v410": ESP}',
      'rep["contratos_pinam_a_escada"] = {"expected_ladder_no_selado_da_v410": _n_esc_base, "expected_ladder_no_candidato": _n_esc_cand, "escada_da_v410": E409, "escada_da_v411": ESP}')
troca('_KHT6 = json.load(open(os.path.join(KD, "KH_N1_v410.json"), encoding="utf-8"))["linha_TOTAL"]   # a linha TOTAL do Audit DA v410', '_KHT6 = json.load(open(os.path.join(KD, "KH_N1_v411.json"), encoding="utf-8"))["linha_TOTAL"]   # (v411) a linha TOTAL do Audit DA v411 (a da v410: nenhum modulo novo)')
troca('and _ck9["h8"]["valor"] == CM["h8"]["pino_antigo_v409_entradas"]', 'and _ck9["h8"]["valor"] == _CM10["h8"]["pino_antigo_v409_entradas"]')
# ---- (7) o selo
troca('"difere_do_selo_v409": mud_selo,', '"difere_do_selo_v410": mud_selo,')
troca('_selo_inexplicado = sorted(k_ for k_ in mud_selo if k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "registros_v410") + tuple(um._V410_REGISTROS_FUNCAO) and not _selo_explica(k_))',
      '_selo_inexplicado = sorted(k_ for k_ in mud_selo if k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "registros_v411") + tuple(um._V411_REGISTROS_FUNCAO) and not _selo_explica(k_))   # (v411: as chaves NOVAS do selo sao h0dn_bg1_v411 e registros_v411)')
troca('           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V410_REGISTROS_FUNCAO) and all(((seal.get("registros_v410") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V410_NOMES_REGISTROS)\n',
      '           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V410_REGISTROS_FUNCAO) and all(((seal.get("registros_v410") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V410_NOMES_REGISTROS)\n'
      '           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V411_REGISTROS_FUNCAO) and all(((seal.get("registros_v411") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V411_NOMES_REGISTROS)\n'
      '           and isinstance((seal.get(DL.FECHO_REGISTRO) or {}).get("p2_ao_lado_da_v387"), dict) and all(k_ in (seal.get(DL.FECHO_REGISTRO) or {}) for k_ in ("verdict", "all_verified", "cabeca_do_teste", "outcome", "linha_ao_lado_cefeidas_livres"))\n')
troca('(({"selo_pela_propria_tecnologia_v399", "um_version", "registros_v410"} | set(um._V410_REGISTROS_FUNCAO)) <= set(mud_selo) and not _selo_inexplicado',
      '(({"selo_pela_propria_tecnologia_v399", "um_version", "registros_v411"} | set(um._V411_REGISTROS_FUNCAO)) <= set(mud_selo) and not _selo_inexplicado')
troca('"traducao_turing_v409", "registros_v406", "registros_v407", "registros_v408", "registros_v409"} & set(mud_selo)))',
      '"traducao_turing_v409", "registros_v406", "registros_v407", "registros_v408", "registros_v409", "registros_v410"} & set(mud_selo)) and not (set(um._V410_REGISTROS_FUNCAO) & set(mud_selo)))   # (v411: o resumo do selo dos registros da v410, HERDADOS, NAO muda)')

# ======================================================== (c) (5b-v411) a ordem de chamada do h0dn_bg1_v411
B5 = r'''# (5b-v411) [v411] A ORDEM DE CHAMADA DO h0dn_bg1_v411, medida por AST (nao depende de a guarda_ordem_de_chamada_v411 conhecer a funcao): as chaves que ele le (qg_closure, external_ladder e h0dn_bg1_v410) prontas ANTES da instrucao
# que o chama; a instrucao e' a SEGUINTE a do recibo HMS/13 e dos specs da v410 (o bloco da v410 INTEIRO ja' rodou) e IMEDIATAMENTE antes de emit_figures; nela ele vem ANTES dos specs da v411.
# Controles negativos: (a) as instrucoes da v410 (hms13) e da v411 TROCADAS (o insumo exigido some); (b) a chamada retirada (chamada ausente: nunca ok por omissao); (c) a chamada do h0dn_bg1_v410 retirada (o insumo exigido some).
_FN_H11 = ("h0dn_bg1_v411", "v411_h0dn_mechanics", "_v398_beta")
_EXIG_H11 = tuple(_EXIG_HMS13) + ("h0dn_fontes_hms13_v410",)
_opV11 = _ordem_psion(src, fns_=_FN_H11, exig_=_EXIG_H11, chamada_="h0dn_bg1_v411(core)")
_icV11 = [i_ for i_, st_ in enumerate(_main0.body) if "h0dn_bg1_v411(core)" in ast.unparse(st_)]
_st2 = _main0.body[_ic0 + 2]; _u2 = ast.unparse(_st2); _st3 = _main0.body[_ic0 + 3]
_logoV11 = bool(len(_icV11) == 1 and _icV11[0] == _ic0 + 2 and 0 <= _u2.find("h0dn_bg1_v411(core)") < _u2.find("_v411_rodar_specs(core)") and isinstance(_st3, ast.Assign) and "emit_figures(core)" in ast.unparse(_st3)
                and "h0dn_bg1_v411(core)" not in _u0 and "h0dn_bg1_v411(core)" not in _u1)
_bloco2 = _lin[_st2.lineno - 1:_st2.end_lineno]
_neg_V11a = _ordem_psion("\n".join(_lin[:_st1.lineno - 1] + _bloco2 + _lin[_st1.lineno - 1:_st2.lineno - 1] + _lin[_st2.end_lineno:]), fns_=_FN_H11, exig_=_EXIG_H11, chamada_="h0dn_bg1_v411(core)")   # (a) a instrucao da v411 ANTES da do hms13
_lin_V11b = list(_lin); _ln_V11b = [i_ for i_, l_ in enumerate(_lin_V11b) if re.match(r"\s+_h411 = h0dn_bg1_v411\(core\)", l_)]
assert len(_ln_V11b) == 1, ("a linha da chamada do h0dn_bg1_v411 nao foi achada uma vez", _ln_V11b)
_lin_V11b[_ln_V11b[0]] = _lin_V11b[_ln_V11b[0]].replace("h0dn_bg1_v411(core)", "{}", 1)
_neg_V11b = _ordem_psion("\n".join(_lin_V11b), fns_=_FN_H11, exig_=_EXIG_H11, chamada_="h0dn_bg1_v411(core)")   # (b) a chamada retirada
_neg_V11c = _ordem_psion("\n".join(_lin_Hb), fns_=_FN_H11, exig_=_EXIG_H11, chamada_="h0dn_bg1_v411(core)")   # (c) a chamada do h0dn_bg1_v410 retirada (o _lin_Hb do bloco (5b''))
rep["ordem_de_chamada_h0dn_bg1_v411"] = {"real": _opV11, "na_instrucao_seguinte_a_do_hms13_e_logo_antes_de_emit_figures": _logoV11, "controle_negativo_instrucoes_trocadas": {k_: _neg_V11a.get(k_) for k_ in ("ok", "lidos_antes_da_atribuicao", "insumos_exigidos_ausentes", "erro")},
                                         "controle_negativo_sem_a_chamada": {k_: _neg_V11b.get(k_) for k_ in ("ok", "erro", "indices")}, "controle_negativo_sem_a_chamada_do_h0dn_v410": {k_: _neg_V11c.get(k_) for k_ in ("ok", "lidos_antes_da_atribuicao", "lidas_sem_origem", "insumos_exigidos_ausentes", "erro")}}
U["v411_ordem_de_chamada_do_h0dn_bg1_v411_medida_por_ast_depois_do_bloco_da_v410_e_antes_de_emit_figures_com_tres_controles_negativos"] = bool(_opV11["ok"] and {"h0dn_bg1_v410", "qg_closure", "external_ladder"} <= set(_opV11.get("chaves_lidas") or []) and _logoV11
    and _neg_V11a["ok"] is False and "h0dn_fontes_hms13_v410" in (_neg_V11a.get("insumos_exigidos_ausentes") or []) and _neg_V11b["ok"] is False and _neg_V11b.get("erro") == "chamada no main ausente ou nao unica"
    and _neg_V11c["ok"] is False and "h0dn_bg1_v410" in (_neg_V11c.get("insumos_exigidos_ausentes") or []))
print("ordem de chamada do h0dn_bg1_v411 (AST propria):", _opV11["ok"], "| lidas:", sorted(_opV11.get("chaves_lidas") or []), "| depois do bloco da v410, antes de emit_figures:", _logoV11, "| controles negativos:", _neg_V11a["ok"] is False, _neg_V11b["ok"] is False, _neg_V11c["ok"] is False)
'''
insere_depois_da_linha('print("ordem de chamada do h0dn_fontes_hms13_v410 (AST propria):"', B5)

# ======================================================== (c) (6q) o registro com funcao da v411 e os specs
B6 = r'''# ---- (6q) [v411] O REGISTRO COM FUNCAO NOVO: h0dn_bg1_v411 -- o teste H0DN x BG1 aberto uma vez, depois do commit publico do pre-registro, RECALCULADO dos bytes embutidos (16 checagens; as duas linhas juntas: o primario sob
#      o modelo de erros publicado e, ao lado, as Cefeidas livres; retrodicao sem ajuste, emenda posterior a guarda, teste nao cego; provado e' validade, nao creditacao; o gate nao se move), e os specs cunhagens_v411 e
#      kh_n1_cobertura_v411. Tudo certo; os numeros RECALCULADOS aqui por OUTRO caminho (os insumos decodificados aqui e conferidos contra os ARQUIVOS do DESENHO; K de beta em runtime com a lei do BG1 decodificado aqui;
#      os Z e os ramos lidos do resultado da abertura decodificado aqui; a cabeca montada aqui do literal); NENHUMA chave antiga muda; e cada elo recusa visivelmente (controles negativos no PONTO REAL: o registro do candidato).
import base64 as _b6411
_CP11, _TP11, _IN11 = um._V411_H0DN_CONTRACT, um._V411_H0DN_TEXT, um._V411_H0DN_INSUMOS
rF11 = c.get(DL.FECHO_REGISTRO) or {}   # o do fluxo (o ponto real do main)
_cc11 = cs(); _antes11 = {k_: json.dumps(v_, sort_keys=True, default=str) for k_, v_ in _cc11.items()}
r11 = um.h0dn_bg1_v411(_cc11); _v11 = r11.get("values") or {}; _m11 = r11.get("mechanics") or {}
_mud11 = sorted(k_ for k_ in set(_cc11) | set(_antes11) if k_ != DL.FECHO_REGISTRO and json.dumps(_cc11.get(k_), sort_keys=True, default=str) != _antes11.get(k_))
U["h0dn_bg1_v411_tudo_certo"] = bool(rF11.get("all_verified") is True and r11["all_verified"] is True and r11["verdict"] == rF11.get("verdict") and r11["verdict"].startswith(DL.VEREDITO_OK_PREFIXO) and r11["verdict"].endswith(DL.VEREDITO_SUFIXO)
    and _m11.get("n_checks") == DL.N_CHECKS_FECHO == len(_m11.get("checks") or []) == 16 and [ck_["id"] for ck_ in _m11["checks"]] == ["c%d" % i_ for i_ in range(1, DL.N_CHECKS_FECHO + 1)] and all(ck_["ok"] for ck_ in _m11["checks"])
    and [ck_["descricao"] for ck_ in _m11["checks"]] == [DL.CHECAGENS_DO_DESENHO["c%d" % i_] for i_ in range(1, DL.N_CHECKS_FECHO + 1)]
    and r11["runtime_executed"] is True and r11["does_not_gate_core"] is True and r11["observed_vector_read"] is True and r11["opened_once"] is True and r11["beta_ok"] is True and not _mud11
    and DL.PREFIXO_DA_FAIXA in r11["verdict"] and "PRIMARY_UNDER_THE_PUBLISHED_MODEL_" in r11["verdict"] and "BESIDE_FREE_CEPHEIDS_" in r11["verdict"] and "<" not in r11["verdict"]
    and all(k_ in r11 for k_ in ("verdict", "all_verified", "opened_once", "cabeca_do_teste", "outcome", "linha_ao_lado_cefeidas_livres", "ressalvas_secao8", "o_que_o_teste_nao_decide"))
    and all(k_ in _v11["primario"] for k_ in ("z_null", "z_tgl", "D", "p_unilateral", "ramo", "outcome", "cabeca_do_teste", "t", "modelo")) and all(k_ in _v11["cefeidas_livres"] for k_ in ("z_null", "z_tgl", "D", "ramo", "outcome", "t", "modelo")) and "atos" in _v11
    and len(r11["ressalvas_secao8"]) == 7 and r11["o_que_o_teste_nao_decide"] == list(DL.NAO_DECIDE_RESUMO_PT))
U["h0dn_bg1_v411_veredito_e_textos_sem_palavra_proibida_com_a_unica_excecao_da_p18"] = bool(not _GUARDA98.search(r11["verdict"]) and not any(t_ in r11["verdict"] for t_ in DL.TOKENS_PROIBIDOS_V411) and not _GF11.violacoes(r11["verdict"])
    and not um._v392_guarda_texto(json.dumps(_TP11, ensure_ascii=False)) and not _GF11.violacoes(json.dumps(_TP11, ensure_ascii=False)) and not _GF11.p18_sem_cabeca("a cabeca do teste: " + r11["cabeca_do_teste"], _GF11.RAMOS_V411, _GF11.N_DA_CABECA)
    and bool(um._v392_guarda_texto("a cabeca do teste: " + r11["cabeca_do_teste"])) and bool(_GF11.p18_sem_cabeca("a cabeca do teste: " + r11["cabeca_do_teste"][:-1] + "X", _GF11.RAMOS_V411, _GF11.N_DA_CABECA)))   # (a excecao estreita: a exata e' retirada; um caractere trocado nao; a crua reprova)
# os numeros RECALCULADOS aqui por OUTRO caminho
_bytes11 = {}
for _n11, _p11 in _CP11["insumos"].items():
    _e11 = _IN11[_n11]
    _bytes11[_n11] = _b6411.b64decode((um._V410_H0DN_INSUMOS[_e11["reuso_v410"]] if isinstance(_e11.get("reuso_v410"), str) else _e11)["b64"])
_pinos_ok11 = bool(len(_bytes11) == len(DL.INSUMOS_V411) == 18 and all(hashlib.sha256(_bytes11[n_]).hexdigest() == _CP11["insumos"][n_]["sha256"] == DL.INSUMO_POR_NOME[n_]["sha256"] == hashlib.sha256(open(DL.INSUMO_POR_NOME[n_]["arquivo"], "rb").read()).hexdigest() for n_ in _CP11["insumos"]))
_bg11 = json.loads(_bytes11["BG1.json"].decode("utf-8")); _res11 = json.loads(_bytes11["RESULTADO_DA_ABERTURA_V411.json"].decode("utf-8")); _ram11 = json.loads(_bytes11["RAMOS_V411.json"].decode("utf-8"))
_bf11 = um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e)
_zs11, _Om11, _Or11 = float(_bg11["law"]["z_star"]), float(_bg11["law"]["frozen_Omega_m"]), float(_bg11["law"]["frozen_Omega_r"])
_E11 = _math.sqrt(_Om11 * (1 + _zs11) ** 3 + _Or11 * (1 + _zs11) ** 4 + (1 - _Om11 - _Or11)); _K11 = _E11 ** (2 * _bf11 / 3)
_est11 = _res11["resultado"]["estatistica"]; _n11c = int(_math.floor(float(_est11["z_null"][0]))); _cab11 = "".join(_ram11["vereditos"]["leitura_partes"]) % _n11c
_ok_num11 = {"pinos": _pinos_ok11, "beta": abs(_v11["beta"] - _bf11) <= 1e-15 and abs(c["beta"] / _bf11 - 1.0) <= 1e-9, "K": abs(_v11["K"] / _K11 - 1.0) <= DL.TOL_K and abs(_v11["log10K"] - _math.log10(_K11)) <= 1e-12 and abs(_v11["E_zstar"] / _E11 - 1.0) <= 1e-12,
             "K_igual_ao_do_registro_da_v410": abs(_v11["K"] / core0["h0dn_bg1_v410"]["values"]["K"] - 1.0) <= DL.TOL_K,
             "z_do_primario": abs(_v11["primario"]["z_null"] - float(_est11["z_null"][0])) <= DL.TOL_RECALCULO and abs(_v11["primario"]["z_tgl"] - float(_est11["z_tgl"][0])) <= DL.TOL_RECALCULO,
             "z_das_cefeidas_livres": abs(_v11["cefeidas_livres"]["z_null"] - float(_est11["z_null"][1])) <= DL.TOL_RECALCULO and abs(_v11["cefeidas_livres"]["z_tgl"] - float(_est11["z_tgl"][1])) <= DL.TOL_RECALCULO,
             "ramos": _v11["primario"]["ramo"] == _res11["resultado"]["veredito"]["ramo"] == _CP11["esperado_do_resultado"]["ramo_primario"] and _v11["cefeidas_livres"]["ramo"] == _res11["resultado"]["linha_ao_lado_cefeidas_livres"]["ramo"] == _CP11["esperado_do_resultado"]["ramo_cefeidas_livres"],
             "cabeca_montada_aqui": r11["cabeca_do_teste"] == _cab11 == _v11["primario"]["cabeca_do_teste"] and ("PRIMARY_UNDER_THE_PUBLISHED_MODEL_%dSIGMA_AGAINST_THE_NULL" % _n11c) in r11["verdict"],
             "limiar": float(_v11["primario"]["z_null"]) >= float(_ram11["limiar"]) > float(_v11["cefeidas_livres"]["z_null"]),
             "p_unilateral": abs(_v11["primario"]["p_unilateral"] - 0.5 * _math.erfc(float(_v11["primario"]["z_null"]) / _math.sqrt(2.0))) <= 1e-15,
             "gate_e_escada": _v11["gate_verdict"] == ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict") == selo0.get("qg_closure_verdict") and _v11["escada"] == ESP == CM["escada"][1]}
U["h0dn_bg1_v411_os_numeros_foram_recalculados_aqui"] = bool(all(_ok_num11.values()))
# o P2 AO LADO da v387 (aditivo da gerencia de 12/11): o token selado nao muda; o campo novo so' com o registro passando; o rotulo lido de UM lugar so' (DL.P2_AO_LADO)
_p2_11 = r11.get("p2_ao_lado_da_v387") or {}; _seg387 = [s_ for s_ in str((core0.get(DL.P2_REGISTRO_SELADO) or {}).get("verdict")).split("__") if DL.P2_TOKEN_SELADO in s_]
U["h0dn_bg1_v411_o_p2_vai_ao_lado_da_v387_e_o_token_selado_nao_muda"] = bool(isinstance(r11.get("p2_ao_lado_da_v387"), dict) and _p2_11.get("rotulo") == DL.P2_ROTULO and _p2_11.get("rotulo_e_proposta") is DL.P2_ROTULO_E_PROPOSTA and len(_seg387) == 1 and _p2_11.get("rotulo_selado_da_v387") == _seg387[0]
    and _p2_11.get("canal") == DL.P2_CANAL and _p2_11.get("nota") == DL.P2_NOTA and DL.P2_TOKEN_SELADO in str((c.get(DL.P2_REGISTRO_SELADO) or {}).get("verdict")) and DL.P2_TOKEN_SELADO not in str(_p2_11.get("rotulo")) and (_v11.get("c14_inclui_o_p2_da_v387") or {}).get("ok") is True
    and rF11.get("p2_ao_lado_da_v387") == r11.get("p2_ao_lado_da_v387"))
# os controles negativos no PONTO REAL (o registro do candidato): cada elo tirado recusa, e pela checagem esperada
def _rodar11(core_=None, contr_=None, txt_=None, ins_=None):
    _s11 = (um._V411_H0DN_CONTRACT, um._V411_H0DN_TEXT, um._V411_H0DN_INSUMOS)
    try:
        um._V411_H0DN_CONTRACT = contr_ or _s11[0]; um._V411_H0DN_TEXT = txt_ or _s11[1]; um._V411_H0DN_INSUMOS = ins_ or _s11[2]
        return um.h0dn_bg1_v411(core_ if core_ is not None else cs())
    finally:
        um._V411_H0DN_CONTRACT, um._V411_H0DN_TEXT, um._V411_H0DN_INSUMOS = _s11


_falhas11 = lambda r_: [ck_["id"] for ck_ in ((r_.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]
_neg11 = {}
_cg11 = cs(); _cg11["qg_closure"]["gate"]["verdict"] = "TGL_OUTRO_GATE"; _o11 = _rodar11(_cg11); _neg11["gate_trocado"] = (_o11["all_verified"] is False and "c14" in _falhas11(_o11), _falhas11(_o11))
_ce11 = cs(); _ce11["external_ladder"]["n_theorems_expected"] = int(_ce11["external_ladder"]["n_theorems_expected"]) + 1; _o11 = _rodar11(_ce11); _neg11["escada_trocada"] = (_o11["all_verified"] is False and "c15" in _falhas11(_o11), _falhas11(_o11))
_c387 = cs(); _c387[DL.P2_REGISTRO_SELADO]["verdict"] = _c387[DL.P2_REGISTRO_SELADO]["verdict"].replace(DL.P2_TOKEN_SELADO, "P2_OUTRA_COISA"); _o11 = _rodar11(_c387)
_neg11["v387_sem_o_token_selado"] = (_o11["all_verified"] is False and _falhas11(_o11) == ["c14"] and _o11.get("p2_ao_lado_da_v387") is None, _falhas11(_o11))
_ck11 = cs(); _ck11["h0dn_bg1_v410"]["values"]["K"] = _ck11["h0dn_bg1_v410"]["values"]["K"] * (1 + 1e-9); _o11 = _rodar11(_ck11); _neg11["K_da_v410_trocado"] = (_o11["all_verified"] is False and "c10" in _falhas11(_o11), _falhas11(_o11))
_ib11 = copy.deepcopy(_IN11); _bv11 = _b6411.b64decode(_ib11["vetor_y255.npz"]["b64"]); _ib11["vetor_y255.npz"]["b64"] = _b6411.b64encode(_bv11[:-1] + bytes([_bv11[-1] ^ 1])).decode("ascii")
_o11 = _rodar11(ins_=_ib11); _neg11["insumo_adulterado"] = (_o11["all_verified"] is False and "REFUSED" in _o11["verdict"] and _o11.get("p2_ao_lado_da_v387") is None, _o11["verdict"][:120])
_rr11 = copy.deepcopy(_res11); _rr11["resultado"]["estatistica"]["z_null"][0] += 1e-6; _rb11 = (json.dumps(_rr11, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
_ir11 = copy.deepcopy(_IN11); _ir11["RESULTADO_DA_ABERTURA_V411.json"] = {"b64": _b6411.b64encode(_rb11).decode("ascii")}
_cr11 = copy.deepcopy(_CP11); _cr11["insumos"]["RESULTADO_DA_ABERTURA_V411.json"].update(sha256=hashlib.sha256(_rb11).hexdigest(), bytes=len(_rb11))
_o11 = _rodar11(contr_=_cr11, ins_=_ir11); _neg11["resultado_adulterado_1e-6_no_z_e_repinado"] = (_o11["all_verified"] is False and "c6" in _falhas11(_o11), _falhas11(_o11))
_tb11 = copy.deepcopy(_TP11); _tb11["diz"] = list(_tb11["diz"]) + ["o teste tem poder certificado e e' um teste cego"]; _o11 = _rodar11(txt_=_tb11); _neg11["texto_com_frase_proibida"] = (_o11["all_verified"] is False and "c16" in _falhas11(_o11), _falhas11(_o11))
_m11k = um.v411_h0dn_mechanics(um._v398_beta(cs())[0], cs(), _CP11, _TP11, _IN11, None, [os.path.join(DL.H0DN_PASTA_VEDADA_V410, "qualquer.json")]); _neg11["caminho_na_pasta_do_kimi"] = (_m11k["passed"] is False and "c1" in [ck_["id"] for ck_ in _m11k["checks"] if not ck_["ok"]], None)
_m11b = um.v411_h0dn_mechanics(um._v398_beta(cs())[0] * 1.01, cs(), _CP11, _TP11, _IN11, None, []); _neg11["beta_errado"] = (_m11b["passed"] is False and "c10" in [ck_["id"] for ck_ in _m11b["checks"] if not ck_["ok"]], None)
_fin11 = {}
for _nm11, _a11, _b11 in (("nan", float("nan"), 0.0), ("inf", 1.0, float("inf")), ("menos_inf", float("-inf"), 0.0)):
    try:
        um._v411_h0dn_guarda_finitude(_a11, _b11); _fin11[_nm11] = False
    except ValueError:
        _fin11[_nm11] = True
_neg11["z_nao_finito_no_involucro"] = (all(_fin11.values()), _fin11)
_cb11 = cs(); _cb11["beta"] = _cb11["beta"] * 1.01; _o11 = _rodar11(_cb11); _neg11["beta_do_core_adulterado"] = (_o11["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _o11["verdict"], _o11["verdict"][:120])
U["h0dn_bg1_v411_cada_elo_recusa_no_ponto_real"] = bool(all(v_[0] is True for v_ in _neg11.values()) and len(_neg11) == 11 and um.h0dn_bg1_v411(cs())["all_verified"] is True)
# os specs da v411: cunhagens_v411 (as falas, D159 a D170, E41, E42 e E43, as sete ressalvas) e kh_n1_cobertura_v411 (a IGUALDADE exata; o kh da v410 virou piso, C13)
_cn11 = c.get(DL.CUNHAGENS_REGISTRO) or {}; _kh11 = c.get(DL.KH_REGISTRO) or {}
_sp11c = [s_ for s_ in um._V411_SPECS if s_["nome"] == DL.CUNHAGENS_REGISTRO][0]; _sp11k = [s_ for s_ in um._V411_SPECS if s_["nome"] == DL.KH_REGISTRO][0]
_ck11k = {ck_["id"]: ck_ for ck_ in _sp11k["checks"]}; _KHT11 = json.load(open(os.path.join(KD, DL.KH_N1_INSUMO), encoding="utf-8"))
U["cunhagens_v411_falas_decisoes_e_as_erratas_e41_e42_e43_ao_lado"] = bool(_cn11.get("all_verified") is True and _cn11.get("verdict", "").startswith(DL.CUNHAGENS_PREFIXO + "__") and ("ERRATA_%s_BESIDE" % DL.ERRATAS_TOKEN_V411) in _cn11.get("verdict", "")
    and [e_.get("agora") for e_ in _sp11c["erratas"][:3]] == [e_["texto"] for e_ in DL.ERRATAS_V411] and len(_sp11c["erratas"]) == len(DL.ERRATAS_V411) + 1 and len(_sp11c["verbatins"]) == DL.N_FALAS_V411 == 9
    and (_sp11c.get("extras") or {}).get("erratas_ids") == list(DL.ERRATAS_IDS_V411) == ["E41", "E42", "E43"] and (_sp11c.get("extras") or {}).get("decisoes") == dict(DL.DECISOES_V411) and _sp11c.get("leituras_do_operador") == []
    and not _GF11.violacoes(json.dumps({k_: _sp11c.get(k_) for k_ in ("erratas", "limites", "diz", "nao_diz", "extras")}, ensure_ascii=False)) and not um._v392_guarda_texto(json.dumps({k_: _sp11c.get(k_) for k_ in ("erratas", "limites", "diz", "nao_diz")}, ensure_ascii=False)))
U["kh_n1_cobertura_v411_cobra_a_igualdade_exata"] = bool(_kh11.get("all_verified") is True and _kh11.get("verdict", "").startswith(DL.KH_PREFIXO + "__") and {i_: _ck11k[i_]["op"] for i_ in ("h2", "h3", "h6", "h8")} == {"h2": "igual", "h3": "igual", "h6": "tamanho_igual", "h8": "igual"}
    and _ck11k["h2"]["valor"] == _KHT11["linha_TOTAL"]["decl"] == _kf0["axiom_coverage_v392"]["decl"] == len(_kf0["axiom_report"]) and _ck11k["h3"]["valor"] == _KHT11["linha_TOTAL"]["thm"] == _kf0["axiom_coverage_v392"]["thm"]
    and dict(_ck11k["h8"]["valor"]) == dict(_kf0["formal_files_sha256"]) and len(_ck11k["h8"]["valor"]) == CM["h8"]["entradas"] and _KHT11["linha_TOTAL"] == json.load(open(os.path.join(_KD10, "KH_N1_v410.json"), encoding="utf-8"))["linha_TOTAL"])
rep[DL.FECHO_REGISTRO] = r11; rep[DL.CUNHAGENS_REGISTRO] = _cn11; rep[DL.KH_REGISTRO] = _kh11
rep["h0dn_bg1_v411_controles_negativos"] = {k_: {"recusou": v_[0], "detalhe": v_[1]} for k_, v_ in _neg11.items()}; rep["h0dn_bg1_v411_numeros_recalculados"] = _ok_num11; rep["h0dn_bg1_v411_chaves_antigas_mexidas"] = _mud11
print("h0dn_bg1_v411:", r11["all_verified"], "|", r11["verdict"][:110], "| numeros:", {k_: v_ for k_, v_ in _ok_num11.items() if not v_} or "todos", "| controles negativos:", {k_: v_[0] for k_, v_ in _neg11.items() if not v_[0]} or "todos recusam")
'''
troca("# (8) o artigo\n", B6 + "# (8) o artigo\n")
# os specs da v411 no laco (6b) dos registros por spec (cada um recusa visivelmente)
troca("+ list(um._V407_SPECS) + list(um._V408_SPECS) + list(um._V409_SPECS):\n    n_ = sp_[\"nome\"]; r_ = {}", "+ list(um._V407_SPECS) + list(um._V408_SPECS) + list(um._V409_SPECS) + list(um._V411_SPECS):   # (v411: e os specs da v411)\n    n_ = sp_[\"nome\"]; r_ = {}")
troca("+ len(um._V406_SPECS) + len(um._V407_SPECS) + len(um._V408_SPECS) + len(um._V409_SPECS)\n", "+ len(um._V406_SPECS) + len(um._V407_SPECS) + len(um._V408_SPECS) + len(um._V409_SPECS) + len(um._V411_SPECS)\n")

# ======================================================== (8) o artigo: os nomes de arquivo, o TOC, as checagens da v411 e a variante
t = t.replace("dry_v410_", "dry_v411_")
troca('TOC = {"pt": [TI410, TA410, TH410, TT409,', 'TOC = {"pt": [um._v411_tex_unicode(DL.TITULO_SECAO_PT), TI410, TA410, TH410, TT409,')
troca('T409, T404, "v384 a v410"], "en": [TI410E, TA410E, TH410E, TT409E,', 'T409, T404, "v384 a v411"], "en": [um._v411_tex_unicode(DL.TITULO_SECAO_EN), TI410E, TA410E, TH410E, TT409E,')
troca('T409E, T404E, "v384 to v410"]}', 'T409E, T404E, "v384 to v411"]}')
F8 = r'''def _checagens_v411_do_artigo(tex_, txt_, lang_):
    """(v411) o que o artigo da v411 tem de trazer, conferido contra as funcoes do PROPRIO candidato sobre o core do ensaio (o quadro, a remissao, o topo, as duas trocas e a do metodo, a frase ao lado do estatuto e do coracao,
    o P2 ao lado na secao da v387, a secao nova ANTES da da v410), as duas guardas linha a linha com a UNICA excecao da P18 (_GF11.p18_sem_cabeca), sem n/d, sem beta/alfa/sigma Unicode no LaTeX novo, e o A2 no TXT."""
    r_ = c.get(DL.FECHO_REGISTRO) or {}

    def _seq(ls_, ini_=0):   # (o artigo junta as linhas de s com uma linha em branco entre elas: cada linha, em ORDEM, contigua; devolve (inicio, fim) ou (-1, -1))
        p0_, p_ = -1, ini_
        for k_, l_ in enumerate(ls_):
            j_ = tex_.find(l_, p_)
            if j_ < 0 or (k_ and tex_[p_:j_].strip()):
                return -1, -1
            p0_ = j_ if k_ == 0 else p0_; p_ = j_ + len(l_)
        return p0_, p_
    ql_ = um._v411_quadro_tex(r_, lang_, um._V411_TITULO_QUADRO_PT); q7l_ = um._v397_quadro_tex(c.get("teste_de_veracidade_fase9_v397"), lang_); rem_ = um._v411_remissao_tex(lang_)
    q_ = "\n".join(ql_); iq_, fq_ = _seq(ql_); i7_, f7_ = _seq(q7l_, max(fq_, 0))   # (o quadro da v397 comeca pela MESMA primeira linha do da v411: procurado DEPOIS do fim do quadro da v411)
    _gap_ = tex_[fq_:i7_] if 0 <= fq_ <= i7_ else "x"
    top_ = um._v411_topo_texto(c, lang_); ef_ = um._v411_efeitos_tex(c, lang_); efm_ = um._v411_efeitos_tex(c, lang_, "metodo"); es_ = um._v411_estatuto_tex(c, lang_); p2_ = um._v411_p2_ao_lado_tex(c, lang_)
    sl_ = um._v411_secao_tex(c, lang_, um._V411_TITULO_SECAO[lang_]); sec_ = "\n".join(sl_); t410_ = "section*{" + (TI410 if lang_ == "pt" else TI410E) + "}"
    s387_ = "section*{" + ("Os três testes de estresse, conjuntos (v387)" if lang_ == "pt" else "The three stress tests, taken together (v387)") + "}"; i387_ = tex_.find(s387_)
    novos_ = um._v411_quadro_tex(r_, lang_, um._V411_TITULO_QUADRO_PT) + sl_ + [rem_, top_, ef_, efm_, es_, p2_]
    viol_ = [(i_, (l_ or "")[:90], _GF11.p18_sem_cabeca(l_, _GF11.RAMOS_V411, _GF11.N_DA_CABECA), _GF11.violacoes(l_)) for i_, l_ in enumerate(novos_)]
    viol_ = [x_ for x_ in viol_ if x_[2] or x_[3]]
    is_, fs_ = _seq(sl_)
    out_ = {"registro_selado": r_.get("all_verified") is True, "quadro_no_tex": iq_ >= 0, "quadro_acima_do_da_v397": 0 <= iq_ < fq_ <= i7_ and not _gap_.strip(), "quadro_antes_do_resumo": 0 <= iq_ < tex_.find(r"\begin{abstract}"),
            "remissao_logo_depois_do_quadro_da_v397": f7_ >= 0 and tex_.find(rem_, f7_) >= 0 and not tex_[f7_:tex_.find(rem_, f7_)].strip(), "topo_abre_o_paragrafo_de_apresentacao": (r"{\large\itshape " + top_) in tex_, "efeitos_trocados": ef_ in tex_, "efeitos_no_metodo": efm_ in tex_,
            "estatuto_ao_lado_e_no_coracao": tex_.count(es_) >= 2, "p2_ao_lado_na_secao_da_v387": 0 <= i387_ < tex_.find(p2_), "secao_nova_antes_da_v410": 0 <= is_ < fs_ <= tex_.find(t410_), "numeros_no_topo": "⟨" not in top_ and "⟩" not in top_,
            "sem_n_d": "n/d" not in q_ + sec_ + top_ + p2_ + efm_, "sem_unicode_no_latex_novo": not any(0x370 <= ord(ch_) <= 0x3FF for ch_ in q_ + sec_ + rem_ + es_ + p2_ + efm_ + top_ + ef_),
            "a2_no_conversor": "^(" in inspect.getsource(um._tex_to_txt) and txt_.count("^(") >= 100, "violacoes": viol_[:4]}
    out_["ok"] = bool(all(v_ is True for k_, v_ in out_.items() if k_ != "violacoes") and not viol_)
    return out_


'''
troca("def compilar(cv, nome, lang, duas=True):", F8 + "def compilar(cv, nome, lang, duas=True):")
insere_depois_da_linha('    rep["artigo"][lang]["r5"] = _checagens_r5_do_artigo(tex, lang)', '    rep["artigo"][lang]["v411"] = _checagens_v411_do_artigo(tex, txt, lang)   # (v411) o artigo da v411 (o quadro, o topo, as trocas, o P2 ao lado, a secao nova), as guardas com a UNICA excecao da P18\n')
troca('       or not all(v["r5"][k_] for k_ in ("tetelestai", "reconstroi", "e36", "dispositivo", "ratificacao", "clausula_logo_depois_da_frase", "piloto_sim_na_secao", "falas_verbatim_pt")) or v["r5"]["unicode_cru_r5_na_secao"]]',
      '       or not all(v["r5"][k_] for k_ in ("tetelestai", "reconstroi", "e36", "dispositivo", "ratificacao", "clausula_logo_depois_da_frase", "piloto_sim_na_secao", "falas_verbatim_pt")) or v["r5"]["unicode_cru_r5_na_secao"] or not v["v411"]["ok"]]')
V11 = r'''# (v411) a VARIANTE sem os registros da v411: as frases de guarda da v411 (o quadro, o topo, a frase dos efeitos) aparecem; no texto completo, nao
cv11 = dict(copy.deepcopy(c)); [cv11.pop(k, None) for k in V411N]
rep["variante_v411"] = {}
for lang in ("pt", "en"):
    _t11v, _x11v, _r211v, _l11v = compilar(cv11, "dry_v411_var11_%s" % lang, lang, duas=False); fl11 = re.sub(r"\s+", " ", _x11v)
    flc11 = re.sub(r"\s+", " ", open(os.path.join(DRY, "dry_v411_%s.txt" % lang), encoding="utf-8").read())
    _g11 = {"pt": ["registro do H0DN v411 NÃO selou", "(v411) NÃO selou nesta rodada", "o registro do H0DN v411 não selou nesta rodada"], "en": ["v411 H0DN record did NOT seal", "(v411) did NOT seal this round", "the v411 H0DN record did not seal this round"]}[lang]
    rep["variante_v411"][lang] = {"rc": _r211v, "frases_de_guarda_na_variante": {g_: g_ in fl11 for g_ in _g11}, "frases_de_guarda_ausentes_no_texto_completo": {g_: g_ not in flc11 for g_ in _g11}}
mau_var11 = [l for l, v in rep["variante_v411"].items() if v["rc"] != [0] or not all(v["frases_de_guarda_na_variante"].values()) or not all(v["frases_de_guarda_ausentes_no_texto_completo"].values())]
print("variante v411:", rep["variante_v411"])
'''
troca("# (9) md e manifesto\n", V11 + "# (9) md e manifesto\n")
troca('    _sn7 = open(os.path.join(HERE, _sn_), encoding="utf-8").read()', '    _sn7 = open(os.path.join(DL.V410, _sn_), encoding="utf-8").read()   # (v411: os snippets da v410 sao da cadeia da v410: HERANCA)')
# ---- (9) o .md e o manifesto
troca('rep["markdown"] = {"carimbo": "**Versão v410**" in md, ', 'rep["markdown"] = {"carimbo": "**Versão v411**" in md, "h0dn_v411": DL.MD_ROTULO_H0DN_V411 in md and 0 <= md.find(DL.MD_ROTULO_H0DN_V411) < md.find("**IALD2 (v410, 06/11/2026):**") and (DL.MD_ROTULO_H0DN_V411 + " " + um._v411_linha_md(c.get(DL.FECHO_REGISTRO))) in md,\n'
      '                   "h0dn_v411_quadro_md_acima_do_da_v397": (lambda q_, q7_: bool(q_ in md and 0 <= md.find(q_) < md.find(q7_)))("\\n".join(um._v411_quadro_md(c.get(DL.FECHO_REGISTRO), um._V411_TITULO_QUADRO_PT)), "\\n".join(um._v397_quadro_md(c.get("teste_de_veracidade_fase9_v397")))),\n'
      '                   "h0dn_v411_linhas_do_md_com_as_duas_guardas": not any(_GF11.p18_sem_cabeca(l_, _GF11.RAMOS_V411, _GF11.N_DA_CABECA) or _GF11.violacoes(l_) for l_ in um._v411_quadro_md(c.get(DL.FECHO_REGISTRO), um._V411_TITULO_QUADRO_PT) + [um._v411_linha_md(c.get(DL.FECHO_REGISTRO))]), ')
troca('rep["manifest"] = "**Versão v410**" in open(mani, encoding="utf-8").read()', 'rep["manifest"] = "**Versão v411**" in open(mani, encoding="utf-8").read()')
troca('os.path.join(HERE, "conferir_citacoes_v410.py")', 'os.path.join(HERE, "conferir_citacoes_v411.py")')
# ---- (11) simular_arvore_do_nos, (12) exame_pontos, (13) as guardas estaticas: os scripts da v411, saidas em DL.saida
troca("_cand_p = os.path.join(HERE, cand); _sha_full", "_cand_p = os.path.join(HERE, cand); _sha_full")
troca('_kh = [s_ for s_ in um._V410_SPECS if s_["nome"] == "kh_n1_cobertura_v410"][0]; _h8 = [ck_ for ck_ in _kh["checks"] if ck_["id"] == "h8"][0]["valor"]   # (v410:',
      '_kh = [s_ for s_ in um._V411_SPECS if s_["nome"] == DL.KH_REGISTRO][0]; _h8 = [ck_ for ck_ in _kh["checks"] if ck_["id"] == "h8"][0]["valor"]   # (v411: o pino exato da arvore esta\' no spec kh_n1_cobertura_v411; o h8 da v410 virou piso) (v410:')
troca('_sp = _pyr([os.path.join(HERE, "simular_arvore_do_nos_v410.py"), "--candidato", _cand_p, "--logs", KD])', '_sp = _pyr([os.path.join(HERE, "simular_arvore_do_nos_v411.py"), "--candidato", _cand_p, "--logs", KD])')
troca('_sj = json.load(open(os.path.join(HERE, "SIMULACAO_ARVORE_NOS_%s.json" % _sha_full[:16]), encoding="utf-8"))', '_sj = json.load(open(DL.saida("SIMULACAO_ARVORE_NOS_%s.json" % _sha_full[:16]), encoding="utf-8"))')
troca("_regs_sim = tuple(um._V410_REGISTROS_FUNCAO) + tuple(um._V410_NOMES_REGISTROS) + ", "_regs_sim = tuple(um._V411_REGISTROS_FUNCAO) + tuple(um._V411_NOMES_REGISTROS) + tuple(um._V410_REGISTROS_FUNCAO) + tuple(um._V410_NOMES_REGISTROS) + ")
troca('"formal_map_v410": _sj.get("formal_map_v410"),', '"formal_map_v411": _sj.get("formal_map_v411"),')
troca('(_sj.get("formal_map_v410") or {}).get("ok") is True', '(_sj.get("formal_map_v411") or {}).get("ok") is True and isinstance(_sj.get("p2_ao_lado_da_v387"), dict)')
troca('_ep = _pyr([os.path.join(HERE, "exame_pontos_v410.py"), "--candidato", _cand_p, "--logs", KD, "--flags", os.path.join(KD, "FLAGS_v410.json"), "--sandbox", KB, "--sha256", _sha_full])',
      '_ep = _pyr([os.path.join(HERE, "exame_pontos_v411.py"), "--candidato", _cand_p, "--logs", KD, "--flags", os.path.join(KD, "FLAGS_v411.json"), "--sandbox", KB, "--sha256", _sha_full])')
troca('_ej = json.load(open(os.path.join(HERE, "EXAME_PONTOS_%s.json" % _sha_full[:16]), encoding="utf-8"))', '_ej = json.load(open(DL.saida("EXAME_PONTOS_%s.json" % _sha_full[:16]), encoding="utf-8"))')
troca('"ponto_iald2": _ej.get("ponto_iald2"), "ponto_h0dn": _ej.get("ponto_h0dn"),', '"ponto_h0dn_v411": _ej.get("ponto_h0dn_v411"), "troca_dita_v411": _ej.get("troca_dita_v411"), "ponto_iald2": _ej.get("ponto_iald2"), "ponto_h0dn": _ej.get("ponto_h0dn"),')
troca("exame_ok = bool(_ep.returncode == 0 and _ej.get(\"algum_falso\") == [] and (_ej.get(\"ponto_iald2\") or {}).get(\"all_verified\") is True",
      "exame_ok = bool(_ep.returncode == 0 and _ej.get(\"algum_falso\") == [] and (_ej.get(\"ponto_h0dn_v411\") or {}).get(\"all_verified\") is True and isinstance((_ej.get(\"ponto_h0dn_v411\") or {}).get(\"p2_ao_lado_da_v387\"), dict) and (_ej.get(\"ponto_iald2\") or {}).get(\"all_verified\") is True")
troca('print("exame_pontos_v410:", exame_ok,', 'print("exame_pontos_v411:", exame_ok,')
troca('_gb_p = os.path.join(HERE, "GUARDAS_ESTATICAS_BANCADA_v410.json")\n_gb = _pyr([os.path.join(HERE, "guardas_estaticas_bancada_v410.py"), _cand_p, _gb_p])',
      '_gb_p = DL.saida("GUARDAS_ESTATICAS_BANCADA_v411.json")\n_gb = _pyr([os.path.join(HERE, "guardas_estaticas_bancada_v411.py"), _cand_p, _gb_p])')
troca('"candidato_passa": (_gj.get("candidato_v410") or {}).get("passou"), "alfa": (_gj.get("candidato_v410") or {}).get("alpha"),', '"candidato_passa": (_gj.get("candidato_v411") or {}).get("passou"), "alfa": (_gj.get("candidato_v411") or {}).get("alpha"),')
troca('_gj.get("contagem_direta") == (CM.get("guardas_estaticas_da_bancada") or {}).get("candidato_v410")', '_gj.get("contagem_direta") == (CM.get("guardas_estaticas_da_bancada") or {}).get("candidato_v411")')
# ---- (0, no fim) o veto: o registro da v411 tambem mede
troca('                            "registro_hms13_tambem_mediu": {',
      '                            "registro_h0dn_v411_tambem_mediu": {"n_caminhos_tocados": ((rep.get(DL.FECHO_REGISTRO) or {}).get("values") or {}).get("n_caminhos_tocados"), "sob_pasta_vedada": ((rep.get(DL.FECHO_REGISTRO) or {}).get("values") or {}).get("sob_pasta_vedada")},\n'
      '                            "registro_hms13_tambem_mediu": {')
# ---- o veredito e a saida
troca("ok = (guardas_ok and viz_ok and mf_ok and all(U.values()) and selo_ok and not mau and not mau_var and ", "ok = (guardas_ok and viz_ok and mf_ok and all(U.values()) and selo_ok and not mau and not mau_var and not mau_var11 and ")
troca('"artigo": mau, "variante": mau_var,', '"artigo": mau, "variante": mau_var, "variante_v411": mau_var11,')
troca('json.dump(rep, open(os.path.join(HERE, "ensaio_a_seco_v410.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)',
      'rep.update(DL.MARCA_ENSAIO); rep["dry"] = DRY\n_pE = DL.saida("ensaio_a_seco_v411.json"); open(_pE + ".tmp", "w", encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1, default=str)); os.replace(_pE + ".tmp", _pE)')
t = t.replace('"\\nVEREDITO DO ENSAIO A SECO (%s): %s"', '"\\nVEREDITO DO ENSAIO A SECO (%s): %s"')
ast.parse(t)
for rx_ in (r"CANDIDATO_v410\.json\"\)\)", r"ensaio_a_seco_v410\.json", r"exame_pontos_v410\.py", r"simular_arvore_do_nos_v410\.py", r"guardas_estaticas_bancada_v410\.py"):
    assert not re.search(rx_, t.replace('os.path.join(DL.V410, "CANDIDATO_v410.json")', "")), ("sobrou referencia da v410 corrente", rx_)
b0 = open(DST, "rb").read()
bak = DST + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_forkc"; open(bak, "wb").write(b0); assert open(bak, "rb").read() == b0
nb = t.encode("utf-8"); open(DST + ".tmp", "wb").write(nb); assert os.path.getsize(DST + ".tmp") == len(nb); os.replace(DST + ".tmp", DST)
print("ok", DST, len(b0), "->", len(nb), "| trocas:", len(LOG))
