# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1] as FONTES pinadas, as CITACOES (as 11 falas de 11 e 12/11, citadas por data e sha256, NAO transcritas: D181) e os registros por SPEC da v411 (cunhagens_v411 e kh_n1_cobertura_v411), no molde de registros_v410.py
"""registros_v411.py -- o que o gerar_candidato_v411.py emite no bloco de runtime da v411 alem do registro com funcao (registros_h0dn_v411): (1) FONTES (_V411_FONTES): as copias duraveis de v411\\insumos (os 18 insumos
embutidos do H0DN, os 7 citados por sha256 e a medida do Audit da v411), cada uma pinada por sha256 LIDO; (2) CITACOES (FALAS_CITADAS): as 11 falas do operador da lista congelada (DESENHO_v411 secao 3 e o AO LADO do topo), citadas por data, sha256 (lido do arquivo da casa na construcao), papel e autor: o programa NAO leva o texto
de nenhuma delas, nem trecho, nem o nome do arquivo (D181); _V411_VERBATINS2 fica vazio; os 6 textos da gerencia entram so' citados por sha256 (nao sao falas do operador); (3) os SPECS: cunhagens_v411 (as falas citadas por sha256, as decisoes D159 a D181,
as erratas E41 a E44 e a do kh_n1_cobertura_v410 a pisos, as sete ressalvas por rotulo; os registros anteriores seguem selados; o gate e a escada da v410) e kh_n1_cobertura_v411 (a cobertura do Audit do sandbox k411c:
os numeros sao os da v410; o pino exato da arvore do Nos). Regra do nome (D122, D123): nenhum texto novo diz “leitura do operador”; leituras_do_operador fica vazia. Validade no kernel nao e' creditacao; o gate nao se move."""
import hashlib, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
import registros_h0dn_v411 as RH  # noqa: E402

INS = os.path.join(HERE, "insumos"); CUNI = os.path.join(INS, "cunhagens")
ASSINA = DL.ASSINA
sha256 = lambda b: hashlib.sha256(b).hexdigest()
CHAVE_KH = "kh_n1_v411"
FONTES = ([{"chave": "h0dn_v411_" + re.sub(r"[^a-z0-9]+", "_", i_["nome"].lower()).strip("_"), "arquivo": os.path.join(INS, "h0dn_" + i_["nome"]),
            "papel": "insumo EMBUTIDO do registro h0dn_bg1_v411 (%s; DESENHO_v411 secao 2; origem work\\%s)%s [REAL: sha256]" % (i_["papel"], i_["rel"], "; reuso do blob da v410, o mesmo sha256" if i_["reuso_v410"] else "")} for i_ in DL.INSUMOS_V411]
          + [{"chave": "citado_v411_" + re.sub(r"[^a-z0-9]+", "_", c_["nome"].lower()).strip("_"), "arquivo": os.path.join(INS, "citado_" + c_["nome"]),
              "papel": "CITADO por sha256, NAO embutido (DESENHO_v411 secao 2; origem %s) [REAL: sha256]" % c_["rel"]} for c_ in DL.CITADOS_V411]
          + [{"chave": CHAVE_KH, "arquivo": os.path.join(HERE, DL.KERNEL_DIR, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox k411c (pos_build_kernel_v411.py): os numeros sao os da v410 (versao sem modulo novo) [REAL]"}])
assert len({f_["chave"] for f_ in FONTES}) == len(FONTES) == 18 + 7 + 1 and all(os.path.exists(f_["arquivo"]) for f_ in FONTES), "fontes repetidas ou copia duravel ausente (rode copiar_insumos_v411.py)"


# (D181) NENHUM texto de fala no programa: as 11 viram itens CITADOS (data, sha256, papel, autor); a chave e' derivada do sha256 (nunca do nome do arquivo, que carrega as primeiras palavras da fala)
VERBATINS = []   # (vazio: o motor v392 so' embute texto; as citacoes entram pelo _v411_rodar_specs, a partir de _V411_FALAS_CITADAS)
FALAS_CITADAS = {"v411_cun_" + c_["sha256"][:16]: dict(c_) for c_ in DL.FALAS_CITADAS_V411}
assert len(FALAS_CITADAS) == DL.N_FALAS_V411 == 11
VERB_CHAVES = []
CH = lambda id_, desc_, onde_, caminho_, op_, valor_=None, cap_=None, est_="[REAL]": dict(id=id_, descricao=desc_, onde=onde_, caminho=caminho_, op=op_, **({"valor": valor_} if valor_ is not None else {}), **({"capturar": cap_} if cap_ else {}), estatuto=est_)
ANTERIORES_SELADOS = list(DL.REGISTROS_FUNCAO_V410) + ["cunhagens_v410", "kh_n1_cobertura_v410", "traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408",
                                                       "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "ponte_da_massa_v405",
                                                       "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405",
                                                       "projecao_transversal_v404", "jo8v32_v404", "caminho_v403", "vida_v403", "ponte_da_escala_dual_v402", "falsidade_da_inercia_v401", "teste_de_veracidade_fase9_v397", "selo_pela_propria_tecnologia_v399"]


def errata_pisos_v410(cov_base):
    return {"ao_lado_de": "kh_n1_cobertura_v410 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
            "dizia": "A v410 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v410 e o hash formal igual ao pino exato da arvore da v410." % (int(cov_base["decl"]), int(cov_base["thm"])),
            "agora": "A v411 nao acrescenta modulo (as contagens sao as mesmas), mas segue a regra das versoes: o registro da v410 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v411. O veredito do registro da v410 NAO muda.",
            "lacuna_de_fidelidade": "um registro preso a igualdades que uma versao seguinte com modulo quebraria (a mesma lacuna desde a v399); a v411 nao a quebra, e a forma fica a mesma das outras versoes", "estatuto": "[REAL: contagens lidas do log do Audit do sandbox k411c]", "assinatura": ASSINA}


def especs(formal_map, khj, h8_map, cov_base, core0):
    """formal_map = {arquivo embutido: sha256} do kernel (o da v410, sem mudanca); khj = KH_N1_v411.json; h8_map = o hash formal que o RITO vai gerar; cov_base = a cobertura da v410 selada {decl, thm}; core0 = o core da v410. Devolve [cunhagens, kh]."""
    T = khj["linha_TOTAL"]
    gate0 = ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict")
    cks = [CH("u1", "o registro h0dn_bg1_v411 selou neste rito (o resultado da abertura RECALCULADO dos bytes embutidos, as %d checagens; o gate)" % DL.N_CHECKS_FECHO, "core", [DL.FECHO_REGISTRO, "all_verified"], "verdadeiro"),
           CH("u2", "o que fica False por teorema: full_static_witness_exists (no gate do fecho)", "core", ["qg_closure", "gate", "full_static_witness_exists"], "falso"),
           CH("u3", "o que fica False por teorema: trivial_inhabitant_exists", "core", ["witness_rigidity", "trivial_inhabitant_exists"], "falso"),
           CH("u4", "o gate deste rito tem o mesmo veredito da v410 selada (o gate nao se move)", "core", ["qg_closure", "gate", "verdict"], "igual", gate0),
           CH("u5", "a escada do kernel fecha (limpos == esperados): a da v410, sem bandeira nova", "core", ["external_ladder", "all_verified"], "verdadeiro"),
           CH("u6", "a escada esperada e' a da v410 (versao sem modulo novo)", "core", ["external_ladder", "n_theorems_expected"], "igual", int(core0["external_ladder"]["n_theorems_expected"])),
           CH("u7", "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro"),
           CH("u8", "o canal vivo do neutrino segue com o mesmo veredito (nada da v411 toca o neutrino)", "core", ["neutrino_mass", "verdict"], "igual", core0["neutrino_mass"]["verdict"])]
    n = 9
    for nome in ANTERIORES_SELADOS:
        cks.append(CH("u%d" % n, "o registro %s segue selado neste rito" % nome, "core", [nome, "all_verified"], "verdadeiro")); n += 1
    for rel_ in sorted(formal_map):
        if rel_.startswith("TGLExt.lean"):
            cks.append(CH("u%d" % n, "a raiz %s do kernel do rito e' EXATAMENTE a da v410 (sha256)" % rel_, "kf", ["formal_files_sha256", rel_], "igual", formal_map[rel_])); n += 1
    dec_tok = DL.DECISOES_TOKEN_V411   # (D159 a D173, lidas do DESENHO e do AO LADO de 12/11)
    cun = {
        "nome": DL.CUNHAGENS_REGISTRO, "veredito_prefixo": DL.CUNHAGENS_PREFIXO,
        "veredito_sufixo": "OPERATOR_ORDERS_OF_11_AND_12_NOV_CITED_BY_DATE_AND_SHA256_NOT_TRANSCRIBED_%d__DECISIONS_%s__ERRATA_%s_BESIDE__THE_SEVEN_RESERVATIONS_STATED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED" % (len(FALAS_CITADAS), dec_tok, DL.ERRATAS_TOKEN_V411),
        "estatuto": "[REAL -- o kernel (o da v410, sem modulo novo), o registro h0dn_bg1_v411 e os registros anteriores lidos a cada rito; INPUT as %d ordens e ratificacoes do operador de 11 e 12/11/2026 (a pergunta que reabre o teste; o desenho ratificado, D159; a emenda da regra, D162; a precisao das tentativas e o portao dos quatro numeros; a forma de selar; a marca da emenda, D168; a ordem de abrir e a ordem da v411, D169; o testemunho e a ordem do topo, D170; a ratificacao da formula do topo e a leitura com o acervo, D172; a ratificacao da redacao do acrescimo, D173), CITADAS por data e sha256 e NAO transcritas (D181: conversa entre os autores nao entra no programa nem no artigo); os textos da gerencia a que ele respondeu, so' citados por sha256; DECLARADO pelo Kimi as tres linhas de covariancia S1, S2 e S4, so' como texto do pre-registro]" % len(FALAS_CITADAS),
        "fontes": [f_["chave"] for f_ in FONTES if f_["chave"] != CHAVE_KH], "verbatins": [], "kernel_flags": [], "kernel_decls": [], "checks": cks,
        "erratas": [{"ao_lado_de": DL.ERRATA_E41["ao_lado_de"], "dizia": "o docstring de veredito_h0dn_v411 descreve o primeiro portao como reproducao, centragem e impressao digital.", "agora": DL.ERRATA_E41["texto"],
                     "lacuna_de_fidelidade": "o comentario do codigo pinado diz o portao 1 com a centragem dentro; o pre-registro e o codigo de abrir a tratam como conferencia interna (falha = recusa)", "estatuto": "[REAL: o codigo de abrir, pinado e executado neste rito dos bytes embutidos; o modulo nao e' tocado]", "assinatura": ASSINA},
                    {"ao_lado_de": DL.ERRATA_E42["ao_lado_de"], "dizia": "um colchete, em duas linhas da v410, que rotula como leitura uma identificacao do operador (contra a regra do nome, D122 e D123).", "agora": DL.ERRATA_E42["texto"],
                     "lacuna_de_fidelidade": "o achado A1 da revisao de terceiro da v410: o artigo, o handoff e o README ja traziam a forma nova; duas linhas-fonte nao", "estatuto": "[REAL: as duas linhas da v410 seladas ficam como estao; a errata vai ao lado]", "assinatura": ASSINA},
                    {"ao_lado_de": DL.ERRATA_E43["ao_lado_de"], "dizia": "a secao 7 do DESENHO_v411 dizia que as seis aberturas da secao da Escala entrariam no artigo regenerado com a troca dita.", "agora": DL.ERRATA_E43["texto"],
                     "lacuna_de_fidelidade": "seis aberturas da secao da Escala, no texto selado da v410, identificam o operador contra a regra do nome; trocar so' na renderizacao faria o artigo divergir do registro selado (decisao da gerencia c1, 12/11)", "estatuto": "[REAL: o texto selado da v410 e o artigo ficam como estao; a errata vai ao lado]", "assinatura": ASSINA},
                    {"ao_lado_de": DL.ERRATA_E44["ao_lado_de"], "dizia": "a secao da v410 sobre o teste pre-registrado da razao de Hubble (H0DN x BG1), que o artigo da v411 traz igual, descreve o estado da v410 (09 a 11/11/2026) no presente: nenhum dado observado lido, a abertura de versao futura, uma leitura do vetor fora do suporte que o achado da gerencia de 11/11 e a emenda superaram, a abertura condicionada a uma certificacao previa as cegas; e dois trechos antigos dizem que beta na natureza a 5 sigma aguarda instrumento.",
                     "agora": DL.ERRATA_E44["texto"], "agora_en": DL.ERRATA_E44["texto_en"],
                     "lacuna_de_fidelidade": "o texto selado da v410 fica como estava e vai igual para o artigo da v411, onde a versao seguinte ja abriu o teste (achados B-03 e B-08 da revisao de terceiro); a errata vai ao lado, nunca por cima", "estatuto": "[REAL: o texto selado da v410 e os dois trechos antigos ficam como estao; a errata vai ao lado]", "assinatura": ASSINA},
                    errata_pisos_v410(cov_base)],
        "limites": ["[INPUT] as %d ordens e ratificacoes de 11 e 12/11/2026 sao do operador e entram so' CITADAS, por data, sha256, papel e autor (D181: sem o texto, sem trecho e sem o nome do arquivo); o texto fica na casa; os textos da gerencia a que ele respondeu entram so' citados por sha256 (nao sao falas dele)" % len(FALAS_CITADAS),
                    "[REAL] o DESENHO_v411 (sha16 %s) fica citado so' por sha16, nao pinado" % DL.DESENHO_SHA16,
                    "[REAL] o registro CONFERE e nao prova nada por si: quem prova e' o kernel; o resultado do teste e' recalculado pelo registro h0dn_bg1_v411; validade no kernel nao e' creditacao; o gate nao se move"],
        "diz": ["as ordens e ratificacoes do operador de 11 e 12/11/2026 estao citadas por data e sha256, sem transcricao", "o registro h0dn_bg1_v411 selou", "os registros da v394 a v410 seguem selados; o neutrino e o gate nao mudam; nenhuma chave antiga muda"],
        "nao_diz": ["que a creditacao tenha sido dada: ela e' de quem tem autoridade para creditar", "que o gate tenha se movido: nao se moveu", "que haja modulo novo no kernel: nao ha'; o kernel e' o da v410"],
        "leituras_do_operador": [],
        "extras": {"n_falas": len(FALAS_CITADAS), "autores": {k_: v_["autor"] for k_, v_ in FALAS_CITADAS.items()}, "falas_citadas": [dict(v_, chave=k_) for k_, v_ in FALAS_CITADAS.items()], "decisoes": dict(DL.DECISOES_V411), "erratas_ids": list(DL.ERRATAS_IDS_V411), "ressalvas_rotulos": list(DL.RESSALVAS_ROTULOS_PT),
                   "textos_da_gerencia_citados": [{"nome": g_["nome"], "sha256": g_["sha256"]} for g_ in DL.TEXTOS_DA_GERENCIA_CITADOS], "assinatura_das_erratas": ASSINA,
                   "topo_ratificado": {"arquivo": os.path.basename(DL.TOPO_RATIFICADO_ARQ), "sha256": DL.TOPO_SHA256, "n_marcadores": len(DL.MARCADORES_V411 or {})} if DL.TOPO_SHA256 else None,
                   "alcance_de_p_igual_np": "P = nP " + DL.D10.FRASE_QUALIFICADOR_PT + " (D64 e D84 da v410)"},
    }
    kh = {
        "nome": DL.KH_REGISTRO, "veredito_prefixo": DL.KH_PREFIXO,
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__NO_NEW_MODULE__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v411 (iguais aos da v410: nenhum modulo novo); o conjunto exato das fontes formais que o hash formal do rito vera e' pinado; a cobertura NAO move o gate",
        "fontes": [CHAVE_KH], "kernel_flags": [], "kernel_decls": [],
        "checks": [CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
                   CH("h2", "constantes cobertas == as do sandbox v411 (KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
                   CH("h3", "teoremas cobertos == os do sandbox v411 (KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
                   CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
                   CH("h5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
                   CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", T["decl"]),
                   CH("h7", "a cobertura da v411 inclui a da v410 selada (constantes)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", int(cov_base["decl"])),
                   CH("h7b", "os teoremas cobertos incluem os da v410 selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", int(cov_base["thm"])),
                   CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", dict(h8_map)),
                   CH("h9", "medida do Audit v411: duracao bem abaixo do timeout de 1800 s", "fonte:" + CHAVE_KH, ["duracao_audit_s"], "menor_igual", 1200, "duracao_do_audit_s"),
                   CH("h10", "medida do Audit v411: sorryAx ausente do log", "fonte:" + CHAVE_KH, ["sorryAx_no_log_do_audit"], "igual", 0),
                   CH("h11", "medida do Audit v411: as entradas estao no trio", "fonte:" + CHAVE_KH, ["novas_no_trio"], "verdadeiro"),
                   CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro")],
        "erratas": [errata_pisos_v410(cov_base)],
        "limites": ["[REAL] os arquivos residuais da pasta do Nos que o hash formal conta (e nao estao embutidos) sao pinados como estao em 12/11/2026; mudar um deles e' mudar o pino, dito; a cobertura mede o Audit, nao a natureza"],
        "diz": ["o Audit do rito cobre todo o fecho TGL/TGLExt, sem modulo novo, nenhuma constante fora do trio; o hash formal da arvore do Nos e' exatamente o pinado"],
        "nao_diz": ["que a cobertura seja prova da teoria: e' a medida de que todo termo no fecho depende so' do trio", "que o gate tenha se movido"],
        "leituras_do_operador": [], "extras": {"delta_vs_v410": khj.get("delta_vs_v410"), "n_bandeiras": 0, "n_modulos": 0, "duracao_build_s_sandbox": khj.get("duracao_build_s"), "duracao_audit_s_sandbox": khj.get("duracao_audit_s")},
    }
    return [cun, kh]
