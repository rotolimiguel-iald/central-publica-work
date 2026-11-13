# -*- coding: utf-8 -*-
"""_adapt_conferir_rito_v411.py -- (claude-construtor-v411, retomada, fork A, 12/11/2026) MONTA o conferir_rito_v411.py a partir do conferir_rito_v410.py ORIGINAL (a versao FINAL que conferiu o rito selado da v410; so' leitura),
para uma versao SEM modulo novo: (1) os rotulos e os caminhos (delta/guarda/acom da v411, V411_NOS, ESPERADOS_v411 em DL.saida, rodada_v411_stdout, as copias de import FORA de work\\); (2) as chaves de ESTADO DA BASE do
ESPERADOS sobem (vereditos_v409 -> vereditos_v410 etc., o esquema do gerar_esperados_v411); (3) os QUATRO registros com funcao da v410 viram HERANCA (as funcoes deles leem os nomes do DL.D10, o delta da v410); (4) as conferencias
NOVAS da v411: o registro h0dn_bg1_v411 (16 checagens, as chaves congeladas com a custodia, os valores do ensaio), os specs cunhagens_v411/kh_n1_cobertura_v411, a secao nova do artigo antes da da v410, o quadro H0DN x BG1 antes do
da v397, o topo do resumo, a linha do .md antes da da IALD2, o selo e o stdout; (5) nenhum modulo novo (bundle vazio; os modulos da v410 como registro); (6) `--controle-negativo` (rc 0 so' se NAO bate, com o Nos ainda na v410).
Cada troca ocorre EXATAMENTE as vezes declaradas (senao PARA). Backup de BYTES do destino antes; ast.parse depois. uso: python -B -X utf8 _adapt_conferir_rito_v411.py"""
import ast, datetime, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "v410", "conferir_rito_v410.py")
DST = os.path.join(HERE, "conferir_rito_v411.py")
T = open(SRC, "rb").read().decode("utf-8"); assert "\r" not in T


def troca(a_, n_, cont=1):
    global T
    assert T.count(a_) == cont, ("ancora", a_[:120], T.count(a_), cont)
    T = T.replace(a_, n_)


def troca_linha(prefixo_, nova_):
    """troca a linha INTEIRA que comeca por prefixo_ (exatamente uma)."""
    global T
    ls_ = T.split("\n"); ix_ = [i_ for i_, l_ in enumerate(ls_) if l_.startswith(prefixo_)]
    assert len(ix_) == 1, ("linha", prefixo_[:100], len(ix_))
    ls_[ix_[0]] = nova_; T = "\n".join(ls_)


def no_trecho(ini_, fim_, f_):
    """aplica f_ ao trecho [ini_, fim_) do texto (ancoras unicas)."""
    global T
    a_ = T.index(ini_); b_ = T.index(fim_, a_); assert T.count(ini_) == 1
    T = T[:a_] + f_(T[a_:b_]) + T[b_:]


# ---- (1) o cabecalho
_i = T.index("# [v410-patch]\n")
CAB = ('# -*- coding: utf-8 -*-\n'
       '# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] MONTADO por _adapt_conferir_rito_v411.py a partir do conferir_rito_v410.py ORIGINAL: versao SEM modulo novo; o registro com funcao h0dn_bg1_v411 e os specs cunhagens_v411/kh_n1_cobertura_v411 NOVOS; os quatro registros com funcao da v410 e os specs da v410 HERDADOS (nomes do DL.D10); a secao, o quadro, o topo, a linha do .md, o selo e o stdout da v411; --controle-negativo\n'
       '"""conferir_rito_v411.py -- confere, DEPOIS do rito v411, o que tinha de mudar e o que NAO podia (ESPERADOS_v411.json; so' + "'" + ' leitura do Nos). Molde: conferir_rito_v410.py (a cadeia de CONTEUDO), montado por _adapt_conferir_rito_v411.py.\n'
       'A v411 NAO tem modulo novo no kernel (o da v410, byte a byte; a escada e a cobertura iguais; nenhuma bandeira nova; o bundle da v410 -- IALD2 e AEscala -- fica no kernel como registro). Mudancas ditas: as chaves novas no core (o registro com\n'
       'FUNCAO h0dn_bg1_v411: o teste H0DN x BG1 aberto uma vez, RECALCULADO no rito a partir dos bytes embutidos; e os registros por spec cunhagens_v411 e kh_n1_cobertura_v411) e o resumo delas no selo (h0dn_bg1_v411 e registros_v411);\n'
       'o selo pela propria tecnologia (v399) muda so' + "'" + ' nos hashes do novo um.py; a versao (um_version v411, sha256); o artigo PT/EN ganha o QUADRO H0DN x BG1 acima do quadro da v397 (que fica, com a linha de remissao), o topo do resumo,\n'
       'as duas trocas ditas, a frase ao lado do estatuto da prova e do coracao e a secao «O teste decisivo» ANTES da secao da v410; o .md ganha o quadro e a linha da v411 antes da linha da IALD2. NENHUMA chave antiga muda: os registros\n'
       'com funcao da v410 (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410) e os anteriores sao RECRIADOS e seguem selados (kh_n1_cobertura_v410 ganha pisos pela C13, o veredito igual). O GATE NAO SE MOVE.\n'
       'A guarda dos textos novos e' + "'" + ' a da v411 (guarda_frases_v411: as quatro obrigacoes F67 no mesmo bloco do resultado; a P18 com a UNICA excecao _v411_p18_sem_cabeca: so' + "'" + ' a cabeca pre-registrada exata). O primario nunca sem as Cefeidas livres,\n'
       '«sob o modelo de erros publicado», «retrodicao», «nao cego» e «validade, nao creditacao»; provado e' + "'" + ' validade, nao creditacao; o gate nao se move.\n'
       'uso: python -B -X utf8 conferir_rito_v411.py [sufixo | --controle-negativo]   (SEM -I: importa o um.py instalado, que precisa do numpy do usuario; o sufixo vai no nome do JSON; `--controle-negativo` = o sufixo _CONTROLE_NEGATIVO_PRE_RITO\n'
       'com o Nos ainda na v410: rc 0 SO' + "'" + ' se NAO bate; _POSITIVO_FALSO_NOS e' + "'" + ' o do teste do caminho positivo). Variavel opcional para o TESTE contra um Nos FALSO (nunca o real): V411_NOS=<pasta>. Com V411_ENSAIO_TOPO_PROPOSTO=1 o ESPERADOS e o JSON\n'
       'de saida sao os da pasta de ensaio (fora de work\\\\; o artefato de ensaio NAO e' + "'" + ' candidato)."""\n'
       '# [v411-patch]\n')
T = CAB + T[_i + len("# [v410-patch]\n"):]
# ---- (2) imports, caminhos e saida
troca('import delta_v410 as DL  # noqa: E402\nimport quadro_v397 as QV  # noqa: E402\nimport acom_conferencias_v410 as AC  # noqa: E402\n',
      'import delta_v411 as DL  # noqa: E402\nsys.modules.setdefault("delta_v410", DL)   # (a ponte por sys.modules: a copia do quadro_v397.py importa o delta pelo nome antigo; usa so\' F9_CAMINHOS e lido(), herdados)\nimport quadro_v397 as QV  # noqa: E402\nimport acom_conferencias_v411 as AC  # noqa: E402\n'
      'CN = "--controle-negativo" in sys.argv   # o controle negativo da cadeia (o Nos ainda na v410): rc 0 so\' se NAO bate\nSUFIXO = "_CONTROLE_NEGATIVO_PRE_RITO" if CN else (sys.argv[1] if len(sys.argv) > 1 else "")\n')
troca('NOS = os.environ.get("V410_NOS") or DL.NOS;', 'NOS = os.environ.get("V411_NOS") or DL.NOS;')
troca('ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v410.json"), encoding="utf-8"))', 'ESP = json.load(open(DL.saida("ESPERADOS_v411.json"), encoding="utf-8"))')
troca('"rodada_v410_stdout.txt"', '"rodada_v411_stdout.txt"', 2)
for _k in ("vereditos", "qg_closure_gate_verdict", "flags_true", "axiom_report", "runtime_seals", "what_remains", "neutrino_frozen_hash", "selo_registros", "veredito_da_falsidade"):
    T = T.replace('ESP["%s_v409"]' % _k, 'ESP["%s_v410"]' % _k)
T = T.replace('ESP["qg_closure_v409_checks"]', 'ESP["qg_closure_v410_checks"]').replace('ESP["qg_closure_v409_sem_checks_json_sha256"]', 'ESP["qg_closure_v410_sem_checks_json_sha256"]').replace('ESP["axiom_report_v410_n"]', 'ESP["axiom_report_v410_n"]')
troca('ESP["the_iald_index_v410"]', 'ESP["the_iald_index_v411"]')
_sobra = sorted(set(re.findall(r'ESP\["([a-z_0-9]*_v409)"\]', T)) - {"estrelas_v409", "registros_funcao_v409", "registros_v409", "titulo_secao_v409", "bundle_v409", "chaves_v409"})
assert not _sobra, ("chave de ESTADO DA BASE da v409 que nao subiu", _sobra)
# ---- (5) o kernel: NENHUM modulo novo; o bundle da v410 como registro
troca_linha('bundle_ok = all(_sha_k(rel) == s for rel, s in ESP["bundle_sha256"].items())',
            'bundle_ok = bool(ESP["bundle_sha256"] == {} and ESP["kernel"]["modulos_novos"] == 0 and ESP["n_bandeiras_novas"] == 0)   # v411: NENHUM modulo novo, nenhuma bandeira nova\n'
            'bundle_v410_ok = bool(len(ESP["bundle_v410_sha256"]) == len(DL.D10.BUNDLE_RELS) > 0 and sorted(ESP["bundle_v410_sha256"]) == sorted(DL.D10.BUNDLE_RELS) and all(_sha_k(rel) == s and (kf.get("formal_files_sha256") or {}).get(rel) == s for rel, s in ESP["bundle_v410_sha256"].items()))   # os modulos da v410 (IALD2 e AEscala): no kernel do Nos e no hash formal do rito, como registro')
troca('; RN410 = sorted(ESP["registros_v410"])   #', '; RN410 = sorted(ESP["registros_v410"]); RN411 = sorted(ESP["registros_v411"])   # (v411: RN410 = os da v410, HERDADOS; RN411 = os desta versao, NOVOS)')
troca_linha('CG10 = core.get("cunhagens_v410") or {};', 'CG10 = core.get("cunhagens_v410") or {}; KH10 = core.get("kh_n1_cobertura_v410") or {}; IV = core.get("iald2_v410") or {}; HV = core.get("h0dn_bg1_v410") or {}; AEV = core.get("a_escala_v410") or {}; HMV = core.get("h0dn_fontes_hms13_v410") or {}   # os quatro registros com funcao da v410 (HERDADOS)\n'
            'CG11 = core.get(DL.CUNHAGENS_REGISTRO) or {}; KH11 = core.get(DL.KH_REGISTRO) or {}; HV11 = core.get(DL.FECHO_REGISTRO) or {}   # v411: o registro com funcao h0dn_bg1_v411 e os specs da v411 (NOVOS)')
troca('_td_txt = ESP.get("troca_dita_textual") or {}', 'V398_NOMES = V398_NOMES + list(DL.D10.REGISTROS_FUNCAO) + [DL.D10.CUNHAGENS_REGISTRO, DL.D10.KH_REGISTRO]   # v411: os da v410, HERDADOS (recriados; o veredito e\' o selado)\n_td_txt = ESP.get("troca_dita_textual") or {}')
troca('_cp = os.path.join(HERE, "conferidor_import_" + umsha)', '_cp = os.path.join(DL.RODADA_PAI, "conferidor_import_" + umsha)   # (D135: a copia de import do um.py por rodada fica FORA de work\\)')
troca('json.dump({"um_version": "v410", "sha256"', 'json.dump({"um_version": DL.UM_VERSION, "sha256"')
troca('_ni = _esb.ler_nos(_pl.Path(_sd), "v410")', '_ni = _esb.ler_nos(_pl.Path(_sd), DL.UM_VERSION)')
troca('if os.environ.get("V410_NOS"):', 'if os.environ.get("V411_NOS"):')
troca('"emulacao (V410_NOS):', '"emulacao (V411_NOS):')
troca('_nr = _esb.ler_nos(_pl.Path(NOS), "v410")', '_nr = _esb.ler_nos(_pl.Path(NOS), DL.UM_VERSION)')
T = re.sub(r"(# C16 \[v400\]:[^\n]*?)V410_NOS", r"\1V411_NOS", T)   # (o comentario do C16 diz a variavel)
assert '"v410")' not in T and "V410_NOS" not in T, [m_ for m_ in re.findall(r'.{40}"v410"\).{10}|V410_NOS', T)]
# ---- (3) os quatro registros com funcao da v410: HERANCA (os nomes do DL.D10)
no_trecho("def _iald2_ok():", "def _traducao409_ok():", lambda s_: re.sub(r"\bDL\.(?!D10\.)", "DL.D10.", s_).replace('ESP["n_bandeiras_por_grupo"]["aescala"]', 'ESP["aescala"]["n_flags"]')
          .replace("(o registro com FUNCAO, novo)", "(HERDADO da v410, RECRIADO na v411)").replace("o SEGUNDO registro com FUNCAO, novo;", "HERDADO da v410, RECRIADO na v411;"))
troca_linha("estrela_ok = len(ESP[\"estrelas_v410\"]) == len(DL.ANCORAS)", re.sub(r"\bDL\.(?!D10\.)", "DL.D10.", [l_ for l_ in T.split("\n") if l_.startswith('estrela_ok = len(ESP["estrelas_v410"]) == len(DL.ANCORAS)')][0]))
troca_linha("estrelaA_ok = len(ESP[\"estrelas_aescala_v410\"])", re.sub(r"\bDL\.(?!D10\.)", "DL.D10.", [l_ for l_ in T.split("\n") if l_.startswith('estrelaA_ok = len(ESP["estrelas_aescala_v410"])')][0]))
# ---- (4) as conferencias NOVAS da v411 (antes da linha que chama as funcoes)
NOVO = r'''

def _sob_ved_(p_):
    _nrm_ = lambda x_: os.path.normcase(os.path.normpath(str(x_))); _ved_ = _nrm_(DL.H0DN_PASTA_VEDADA)
    return _nrm_(p_) == _ved_ or _nrm_(p_).startswith(_ved_ + os.sep) or any(n_.lower() in os.path.basename(_nrm_(p_)) for n_ in DL.H0DN_NOMES_VEDADOS)


_CONG_TOPO = ("verdict", "all_verified", "opened_once", "cabeca_do_teste", "outcome", "linha_ao_lado_cefeidas_livres", "ressalvas_secao8", "o_que_o_teste_nao_decide")   # as chaves CONGELADAS com a custodia (PRONTO_PARA_GERAR_v411.json)
_CONG_LINHAS = {"primario": ("z_null", "z_tgl", "D", "p_unilateral", "ramo", "outcome", "cabeca_do_teste", "t", "modelo"), "cefeidas_livres": ("z_null", "z_tgl", "D", "ramo", "outcome", "t", "modelo")}


def _h0dn411_ok():
    """h0dn_bg1_v411 (o registro com FUNCAO, NOVO: o teste H0DN x BG1 aberto uma vez, RECALCULADO no rito a partir dos bytes embutidos): veredito == o do ensaio (o prefixo, o meio montado com a faixa K_LAW_, as duas linhas
    PRIMARY_/BESIDE_FREE_CEPHEIDS_, o sufixo); as 16 checagens; as chaves congeladas com a custodia no topo e nas duas linhas de values; aberto uma vez; os valores == os do ensaio (menos os caminhos tocados, que dependem da pasta);
    o gate e a escada da v410; nenhum caminho tocado sob a pasta vedada (o veto do Kimi); nenhum token proibido; a guarda das frases limpa no veredito; nao move o gate"""
    R_ = HV11; E_ = ESP["registros_funcao_v411"]["h0dn"]; m_ = R_.get("mechanics") or {}; v_ = V(DL.FECHO_REGISTRO); vv_ = R_.get("values") or {}
    return bool(R_.get("all_verified") is True and v_ == E_["verdict"] and v_.startswith(DL.VEREDITO_OK_PREFIXO) and v_.endswith(DL.VEREDITO_SUFIXO) and DL.PREFIXO_DA_FAIXA in v_ and "PRIMARY_UNDER_THE_PUBLISHED_MODEL_" in v_ and "BESIDE_FREE_CEPHEIDS_" in v_
                and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and R_.get("opened_once") is True
                and m_.get("n_checks") == DL.N_CHECKS_FECHO == E_["n_checks"] and [c_.get("id") for c_ in m_.get("checks") or []] == ["c%d" % i_ for i_ in range(1, DL.N_CHECKS_FECHO + 1)] and all(c_.get("ok") is True for c_ in m_.get("checks") or [])
                and all(k_ in R_ for k_ in _CONG_TOPO) and all(_feq(R_.get(k_), E_["topo"].get(k_)) for k_ in _CONG_TOPO) and all(all(k_ in (vv_.get(l_) or {}) for k_ in ks_) for l_, ks_ in _CONG_LINHAS.items()) and isinstance(vv_.get("atos"), dict)
                and vv_.get("gate_verdict") == ESP["qg_closure_gate_verdict_v410"] == selo.get("qg_closure_verdict") and vv_.get("escada") == ESP["escada"][0] and vv_.get("sob_pasta_vedada") == [] and not [p_ for p_ in (vv_.get("caminhos_tocados") or []) if _sob_ved_(p_)]
                and not any(t_ in v_ for t_ in DL.TOKENS_PROIBIDOS_V411) and not GUARDA.search(v_) and not GF.violacoes(v_)
                and _feq({kk_: vv_.get(kk_) for kk_ in E_["values"]}, E_["values"]))


def _spec411_ok():
    """os registros por spec da v411 (cunhagens_v411, kh_n1_cobertura_v411): selados, o veredito == o do ensaio; as falas de 11 e 12/11 por sha256 (embedded_ok); as erratas E41, E42 e E43 ao lado, em nome proprio da gerencia c1; as decisoes D159 a D170"""
    _vb = CG11.get("verbatim") or {}; _ex = CG11.get("extras") or {}
    return bool(set(ESP["registros_v411"]) == {DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO} and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v411"].items())
                and len(ESP["cunhagens"]) == DL.N_FALAS_V411 and all(((_vb.get(k_) or {}).get("embedded_ok") is True) and ((_vb.get(k_) or {}).get("sha256") == v_["sha256"]) for k_, v_ in ESP["cunhagens"].items())
                and list(_ex.get("erratas_ids") or []) == list(DL.ERRATAS_IDS_V411) and len(CG11.get("erratas") or []) >= len(DL.ERRATAS_IDS_V411) and all(str(e_.get("assinatura", "")).startswith("gerencia c1") for e_ in (CG11.get("erratas") or []))
                and set(_ex.get("decisoes") or {}) >= set(ESP["decisoes_v411_ids"]) and ("ERRATA_%s_BESIDE" % DL.ERRATAS_TOKEN_V411) in V(DL.CUNHAGENS_REGISTRO) and not GF.violacoes(V(DL.CUNHAGENS_REGISTRO)) and not GF.violacoes(V(DL.KH_REGISTRO)))


def _limpo411(t_):
    """um bloco de texto NOVO da v411: as duas guardas limpas (a P18 com a UNICA excecao da cabeca pre-registrada exata; as frases da v411, com as quatro obrigacoes F67 no bloco)"""
    return bool(t_) and not GF.p18_sem_cabeca(t_, GF.RAMOS_V411, GF.N_DA_CABECA) and not GF.violacoes(t_)


# (as quatro obrigacoes do bloco sao cobradas pela guarda da v411 -- a F67 aceita as formas que a regra define, ex. «o teste nao e' cego» --; aqui so' a presenca da linha das Cefeidas livres e' cobrada a mais)
_OBRIG = {"pt": (DL.OBRIG_MODELO_PT, DL.OBRIG_CEFEIDAS_PT, DL.OBRIG_VALIDADE_PT, DL.OBRIG_RETRO_PT, DL.OBRIG_NAO_CEGO_PT), "en": (DL.OBRIG_MODELO_EN, DL.OBRIG_CEFEIDAS_EN, DL.OBRIG_VALIDADE_EN, DL.OBRIG_RETRO_EN, DL.OBRIG_NAO_CEGO_EN)}
_ini411 = {l: txt[l].find(_tt(ESP["titulo_secao_v411"][l])) for l in ("pt", "en")}
_ini410b = {l: txt[l].find(_tt(ESP["titulo_secao_v410"][l])) for l in ("pt", "en")}
_sec411 = {l: (txt[l][_ini411[l]:_ini410b[l]] if 0 <= _ini411[l] < _ini410b[l] else "") for l in ("pt", "en")}
secao411_ok = bool(all(_sec411[l] and _OBRIG[l][1] in _sec411[l] and _limpo411(_sec411[l]) and not any(m_ in _sec411[l] for m_ in ESP["artigo_nao"][l]) for l in ("pt", "en")))
# o QUADRO H0DN x BG1 no topo (antes do quadro da v397) e o resumo que abre com o topo do candidato (o texto do _V411_TOPO ate' o primeiro numero ou formula; os numeros sao do core)
_tq = {"pt": _tt(ESP["titulo_quadro_v411"].split(" [")[0]), "en": _tt(re.search(r"H0DN \$\\times\$ BG1", ESP["titulo_quadro_v411"]).group(0))}   # (o titulo na forma LaTeX ate' o colchete do estatuto, rendido como o TXT o rende ($×$); no EN, o trecho H0DN x BG1 do mesmo titulo)
_iq = {l: txt[l].find(_tq[l]) for l in ("pt", "en")}; _i397 = {l: txt[l].find(EQ["titulo_" + l]) for l in ("pt", "en")}
_topo_c = getattr(um_c, "_V411_TOPO", None) if um_c is not None else None
_topo_pref = {l: re.sub(r"\s+", " ", re.split(r"[$⟨]", (_topo_c or {}).get(l, ""))[0]).strip() for l in ("pt", "en")}
_it = {l: (txt[l].find(_topo_pref[l]) if len(_topo_pref[l]) >= 40 else -1) for l in ("pt", "en")}
_bloco_q = {l: (txt[l][_iq[l]:_i397[l]] if 0 <= _iq[l] < _i397[l] else "") for l in ("pt", "en")}
_bloco_t = {l: (txt[l][_it[l]:_iq[l]] if 0 <= _it[l] < _iq[l] else "") for l in ("pt", "en")}
quadro411_ok = bool(_topo_c is not None and all(0 <= _it[l] < _iq[l] < _i397[l] and _limpo411(_bloco_q[l]) and _OBRIG[l][1] in _bloco_q[l] and _limpo411(_bloco_t[l]) for l in ("pt", "en")))
# o .md canonico: o quadro antes do quadro da v397 e a linha da v411 antes da linha da IALD2 (v410)
_lmd = [l_ for l_ in fc.split("\n") if l_.startswith("> **" + ESP["md_h0dn_v411"] + ":**")]
md411_ok = bool(len(_lmd) == 1 and 0 <= fc.find(ESP["md_quadro_v411"].split(" [")[0]) < fc.find(EQ["md_titulo"]) and fc.find(_lmd[0]) < fc.find("> **" + ESP["md_iald2"] + ":**") and _limpo411(_lmd[0]) and _OBRIG["pt"][1] in _lmd[0])
# o selo: o resumo do h0dn_bg1_v411 (com a cabeca do teste e a linha ao lado) e registros_v411 == o core
_s411 = selo.get(DL.FECHO_REGISTRO) or {}; _sr411 = selo.get("registros_v411") or {}
selo411_ok = bool(_s411.get("verdict") == V(DL.FECHO_REGISTRO) and _s411.get("all_verified") is True and all(_feq(_s411.get(k_), HV11.get(k_)) for k_ in ("cabeca_do_teste", "outcome", "linha_ao_lado_cefeidas_livres", "opened_once"))
                  and set(_sr411) == set(RN411) and all((_sr411.get(n) or {}).get("verdict") == V(n) and (_sr411.get(n) or {}).get("all_verified") is True for n in RN411))
# o stdout do rito: a linha do bloco da v411 e o veredito do registro, sem o AVISO do bloco
std411_ok = bool("H0DN x BG1 ABERTO [v411" in std and V(DL.FECHO_REGISTRO) and V(DL.FECHO_REGISTRO) in std and "[v411] AVISO" not in std)
'''
troca("\niald2_ok = _iald2_ok(); aescala_ok = _aescala_ok();", NOVO.rstrip("\n") + "\n\n\nh0dn411_ok = _h0dn411_ok(); spec411_ok = _spec411_ok(); iald2_ok = _iald2_ok(); aescala_ok = _aescala_ok();")
# a guarda das frases e' a da v411 (precisa estar importada ANTES do bloco novo): sobe o import para junto dos outros
troca("import guarda_frases_v410 as GF\n", "")
troca("import acom_conferencias_v411 as AC  # noqa: E402\n", "import acom_conferencias_v411 as AC  # noqa: E402\nimport guarda_frases_v411 as GF  # noqa: E402   # (a guarda das frases da v411: a mesma funcao do um.py; a P18 com a UNICA excecao da cabeca)\n")
troca("for n_ in list(DL.REGISTROS_FUNCAO) + RN410}, ensure_ascii=False)", "for n_ in list(DL.REGISTROS_FUNCAO) + RN411}, ensure_ascii=False)")
troca('and "o gate não se move" in fc and DL.FRASE_DA_MOLDURA_V410_PT and DL.FRASE_DA_MOLDURA_V410_EN)', 'and "o gate não se move" in fc and DL.D10.FRASE_DA_MOLDURA_V410_PT and DL.D10.FRASE_DA_MOLDURA_V410_EN)')
troca('and _frase_no_artigo and (GF.controle_negativo() or {}).get("ok") is True)', 'and _frase_no_artigo and secao411_ok and (GF.controle_negativo() or {}).get("ok") is True)')
# ---- DEVE
troca('": selo.get("um_version") == "v410"', '": selo.get("um_version") == DL.UM_VERSION and selo411_ok')
troca('"selo um_version v410;', '"selo um_version v411; o resumo h0dn_bg1_v411 (com a cabeca do teste e a linha ao lado) e registros_v411;')
troca('"fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408", "traducao_turing_v409") + tuple(DL.REGISTROS_FUNCAO))', '"fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408", "traducao_turing_v409") + tuple(DL.D10.REGISTROS_FUNCAO) + tuple(DL.REGISTROS_FUNCAO))')
troca('for n in RN410)\n', 'for n in RN410)\n        and all(((selo.get("registros_v411") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v411") or {}).get(n) or {}).get("all_verified") is True for n in RN411)\n')
no_trecho('    "iald2_v410 SELOU (o registro com FUNCAO, novo)', '    "traducao_turing_v409 (HERDADO da v409', lambda s_: re.sub(r"\bDL\.(?!D10\.)", "DL.D10.", s_).replace("(o registro com FUNCAO, novo)", "(HERDADO da v410, RECRIADO na v411)").replace("o registro com FUNCAO da pedra AEscala, novo;", "HERDADO da v410, RECRIADO na v411;")
          .replace("o registro com FUNCAO do teste da razao de Hubble, novo;", "HERDADO da v410, RECRIADO na v411;")
          + '    "h0dn_bg1_v411 SELOU (o registro com FUNCAO, NOVO: o teste H0DN x BG1 aberto uma vez, RECALCULADO no rito a partir dos bytes embutidos; sob o modelo de erros publicado o primario e, ao lado, as Cefeidas livres; retrodicao, nao cego; validade, nao creditacao): veredito == o do ensaio; as %d checagens; as chaves congeladas com a custodia; os valores == os do ensaio (menos os caminhos tocados); o veto a pasta do Kimi; nao move o gate" % DL.N_CHECKS_FECHO: h0dn411_ok,\n'
          + '    "os registros por spec v411 (cunhagens_v411, kh_n1_cobertura_v411) SELARAM com o veredito do ensaio; as %d falas de 11 e 12/11 embutidas por sha256; as erratas %s ao lado, em nome proprio da gerencia c1; as decisoes %s" % (len(ESP["cunhagens"]), ", ".join(DL.ERRATAS_IDS_V411), ", ".join(ESP["decisoes_v411_ids"])): spec411_ok,\n'
          + '    "a secao v411 no artigo PT/EN («%s») vem ANTES da secao da v410, com as quatro obrigacoes (o modelo publicado, as Cefeidas livres, validade e nao creditacao, retrodicao e nao cego) e limpa nas duas guardas (a P18 so\' com a excecao da cabeca pre-registrada exata)" % ESP["titulo_secao_v411"]["pt"]: secao411_ok,\n'
          + '    "o QUADRO H0DN x BG1 (v411) no TOPO do artigo PT/EN, ANTES do quadro da v397 (que fica), com as quatro obrigacoes e limpo; o resumo abre com o texto do topo do candidato (_V411_TOPO; os numeros do core), limpo nas duas guardas": quadro411_ok,\n'
          + '    "o .md canonico: o quadro H0DN x BG1 antes do quadro da v397 e a linha «%s» ANTES da linha da IALD2 (v410), com as quatro obrigacoes e limpa nas duas guardas" % ESP["md_h0dn_v411"]: md411_ok,\n'
          + '    "o stdout do rito traz a linha do bloco H0DN x BG1 ABERTO [v411 e o veredito do registro, sem o AVISO do bloco da v411": std411_ok,\n')
troca('    "os %d modulos novos (o bundle da v410 em TGLExt/: IALD2 e AEscala) no kernel do Nos com o sha do candidato" % len(ESP["bundle_sha256"]): bundle_ok and len(ESP["bundle_sha256"]) == ESP["kernel"]["modulos_novos"] == DL.N_BUNDLE and sorted(ESP["bundle_sha256"]) == sorted(DL.BUNDLE_RELS),',
      '    "NENHUM modulo novo no kernel (a v411 e\' o kernel da v410): bundle_sha256 vazio, nenhuma bandeira nova; os %d modulos da v410 (IALD2 e AEscala) no kernel do Nos e no hash formal do rito, com o sha da v410" % len(ESP["bundle_v410_sha256"]): bundle_ok and bundle_v410_ok,')
troca('{DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO}\n', '{DL.D10.CUNHAGENS_REGISTRO, DL.D10.KH_REGISTRO}\n')
troca('len(ESP["cunhagens"]) == len(DL.VERBATIM_ORIGEM_V410) and all((((CG10.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True) and (((CG10.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"]) for k_, v_ in ESP["cunhagens"].',
      'len(ESP["cunhagens_v410"]) == len(DL.D10.VERBATIM_ORIGEM_V410) and all((((CG10.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True) and (((CG10.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"]) for k_, v_ in ESP["cunhagens_v410"].')
troca('not any(str(v_.get("papel", "")).startswith("leitura da gerencia") for v_ in ESP["cunhagens"].values())', 'not any(str(v_.get("papel", "")).startswith("leitura da gerencia") for v_ in ESP["cunhagens_v410"].values())')
troca('"os registros por spec v410 (cunhagens_v410, kh_n1_cobertura_v410) SELARAM', '"(v411: HERDADOS, recriados) os registros por spec v410 (cunhagens_v410, kh_n1_cobertura_v410) SELARAM')
troca('% len(ESP["cunhagens"]): all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v410"].items())', '% len(ESP["cunhagens_v410"]): all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v410"].items())')
troca('"os registros da v409 e as anteriores (', '"os registros da v410 e as anteriores (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410, cunhagens e kh_n1 da v410; ')
troca('"o artigo PT/EN: a secao v410 (', '"o artigo PT/EN: a secao v411 (O teste decisivo) antes da secao v410 (')
troca('": all(_tt(m) in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l]) and not any(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_nao"][l]),',
      '": all(0 <= _ini411[l] < _ini410b[l] for l in ("pt", "en")) and all(_tt(m) in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l]) and not any(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_nao"][l]),')
troca('"o sumario lista as secoes v410, v409,', '"o sumario lista as secoes v411, v410, v409,')
troca('e o titulo v384 a v410":', 'e o titulo v384 a v411":')
troca('"o .md canonico: carimbo v410 e as linhas da v410 (ESP md_iald2, ANTES da linha da v409)', '"o .md canonico: carimbo v411, a linha da v411 (ESP md_h0dn_v411, ANTES da linha da IALD2) e as linhas da v410 (ESP md_iald2, ANTES da linha da v409)')
troca('": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_iald2"] in fc', '": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_h0dn_v411"] in fc and fc.find(ESP["md_h0dn_v411"]) < fc.find(ESP["md_iald2"]) and ESP["md_iald2"] in fc')
troca('"nenhuma chave nova fora da lista da v410 (so\' os registros com funcao iald2_v410, a_escala_v410, h0dn_bg1_v410 e h0dn_fontes_hms13_v410 e os registros por spec cunhagens_v410 e kh_n1_cobertura_v410; os da v399 a v409, fechamento_v406, psion_canto_v407, tetelestai_terminal_v408 e traducao_turing_v409 inclusive, sao recriados e iguais)"',
      '"nenhuma chave nova fora da lista da v411 (so\' o registro com funcao h0dn_bg1_v411 e os registros por spec cunhagens_v411 e kh_n1_cobertura_v411; os da v399 a v410 -- os quatro com funcao da v410 inclusive -- sao recriados e iguais)"')
troca('or str(k).endswith("_v409") or str(k).endswith("_v410"))) == sorted(list(DL.REGISTROS_FUNCAO) + RN410),', 'or str(k).endswith("_v409") or str(k).endswith("_v410") or str(k).endswith("_v411"))) == sorted(list(DL.REGISTROS_FUNCAO) + RN411),')
troca('"h0dn_fontes_hms13_v410", "cunhagens_v410", "kh_n1_cobertura_v410")) and gate_igual_ok,', '"h0dn_fontes_hms13_v410", "cunhagens_v410", "kh_n1_cobertura_v410") + tuple(DL.REGISTROS_FUNCAO) + tuple(RN411)) and gate_igual_ok,')
# rotulos que diziam a base v409 (so' texto)
no_trecho("DEVE = {", "res = {", lambda s_: s_.replace("da v409 selada", "da v410 selada").replace("RECRIADO na v410", "RECRIADO na v411").replace("RECRIADOS na v410", "RECRIADOS na v411").replace("RECRIADAS na v410", "RECRIADAS na v411")
          .replace("toda bandeira True da v409", "toda bandeira True da v410").replace("o axiom_report da v409", "o axiom_report da v410").replace("NENHUM veredito da v409", "NENHUM veredito da v410").replace("IDENTICO ao da v409", "IDENTICO ao da v410")
          .replace("o veredito do gate == o da v409", "o veredito do gate == o da v410").replace("NENHUMA chave antiga muda na v410", "NENHUMA chave antiga muda na v411"))
# ---- (6) a saida e o controle negativo
troca('p = os.path.join(HERE, "conferencia_rito_v410%s.json" % (sys.argv[1] if len(sys.argv) > 1 else ""))', 'res.update(DL.MARCA_ENSAIO); res["controle_negativo"] = CN\np = DL.saida("conferencia_rito_v411%s.json" % SUFIXO)')
troca('print("TUDO BATE" if ok else "NAO BATE"); sys.exit(0 if ok else 1)',
      'print("TUDO BATE" if ok else "NAO BATE")\nif CN:   # o controle negativo da cadeia: o Nos ainda e\' a v410 selada; o conferidor TEM de dizer que NAO bate (senao a conferencia e\' tautologica)\n'
      '    _nos_e_a_v410 = umsha == ESP["origem_sha16"] and umsha != ESP["candidato_sha16"]\n    print("controle negativo: %s (o Nos %s a v410 selada)" % ("NAO bate (esperado)" if not ok else "BATEU (FALHA do controle)", "e\'" if _nos_e_a_v410 else "NAO e\'"))\n'
      '    sys.exit(0 if (not ok and _nos_e_a_v410) else 1)\nsys.exit(0 if ok else 1)')
ast.parse(T)
if os.path.exists(DST):
    _b = open(DST, "rb").read(); _bk = DST + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_adapt"; open(_bk, "wb").write(_b); assert open(_bk, "rb").read() == _b
nb = T.encode("utf-8"); open(DST + ".tmp", "wb").write(nb); assert os.path.getsize(DST + ".tmp") == len(nb); os.replace(DST + ".tmp", DST)
print("conferir_rito_v411.py montado:", len(nb), "B,", T.count("\n"), "linhas")
