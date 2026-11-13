# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1] o estado MEDIDO no fim da Etapa 2A (sem TOPO_RATIFICADO_v411.json) e a sequencia exata (cadeia_v411.sh)
"""gerar_pronto_para_gerar_v411.py -- escreve PRONTO_PARA_GERAR_v411.json: o que a Etapa 2A fez (as decisoes (a) a (g) da gerencia aplicadas, os dois patches do gerador, o contrato das chaves congeladas com a G1 conferido
no registro do ensaio), o que ficou (os scripts com a marca de copia mecanica, os cinco blocos da custodia no handoff, a troca das seis aberturas) e a sequencia exata. Tudo lido do disco. uso: python -B -X utf8 gerar_pronto_para_gerar_v411.py"""
import datetime, glob, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
s16 = lambda p: hashlib.sha256(open(os.path.join(HERE, p), "rb").read()).hexdigest()[:16]
J = lambda p: json.load(open(os.path.join(HERE, p), encoding="utf-8"))
TO, PV, A2, GFJ, REG = J("TESTE_H0DN_OFFLINE_v411.json"), J("PREVOO_GERADOR_v411.json"), J("A2_MEDIDA_v411.json"), J("GUARDA_FRASES_v411.json"), J("TESTE_H0DN_OFFLINE_v411_registro.json")
# o contrato das chaves congeladas com a G1 (aditivo da gerencia, 12/11): conferido no registro do ensaio
TOPO_K = ["verdict", "all_verified", "opened_once", "cabeca_do_teste", "outcome", "linha_ao_lado_cefeidas_livres", "ressalvas_secao8", "o_que_o_teste_nao_decide"]
PR_K = ["z_null", "z_tgl", "D", "p_unilateral", "ramo", "outcome", "cabeca_do_teste", "t", "modelo"]; CL_K = ["z_null", "z_tgl", "D", "ramo", "outcome", "t", "modelo"]
v = REG.get("values") or {}
chaves = {"topo": {k_: k_ in REG for k_ in TOPO_K}, "values.primario": {k_: k_ in (v.get("primario") or {}) for k_ in PR_K}, "values.cefeidas_livres": {k_: k_ in (v.get("cefeidas_livres") or {}) for k_ in CL_K}, "values.atos": "atos" in v}
chaves_ok = all(all(d_.values()) if isinstance(d_, dict) else d_ for d_ in chaves.values())
_marca = "[A ADAPTAR v" + "411]"
MARCADOS = sorted(os.path.relpath(p_, HERE) for p_ in glob.glob(os.path.join(HERE, "**", "*"), recursive=True) if os.path.isfile(p_) and ".bak_" not in p_ and os.sep + "bump" + os.sep not in p_
                  and not p_.endswith((".json", ".txt", ".diff", ".log", ".npz", ".lean", ".md")) and os.path.basename(p_) not in ("_bump_copia_v411.py", "p00_precondicoes_v411.py", "cadeia_v411.sh") and _marca in open(p_, "rb").read().decode("utf-8", "replace"))
out = {"contrato": "PRONTO_PARA_GERAR_v411", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "agente": "claude-construtor-v411", "topo_ratificado_presente": os.path.exists(DL.TOPO_RATIFICADO_ARQ),
       "estado": "ETAPA 2A PARCIAL: as decisoes da gerencia aplicadas e testadas; os dois patches do gerador feitos (A2 medido; as seis aberturas NAO: estao em textos selados da v410); os scripts com corpo da v410 NAO foram adaptados nesta rodada; o candidato NAO foi gerado (sem topo ratificado)",
       "decisoes_aplicadas": {"a_K_LAW": {"veredito_offline": TO["veredito"], "ao_lado_no_desenho": "fim do DESENHO_v411.md (backup de bytes DESENHO_v411.md.bak_20261112_090215)", "desenho_sha16": DL.DESENHO_SHA16},
                              "b_guarda": "F54 fora; F56 sem o teste aberto; F60 a F67 (como aprovado)",
                              "c_excecao_p18": {"funcao": "_v411_p18_sem_cabeca (runtime_h0dn_v411.py; a mesma no um.py e na cadeia: guarda_frases_v411.p18_sem_cabeca)", "controles": GFJ["controle_negativo"].get("excecao_p18_da_cabeca"),
                                                "na_c16_do_registro": (v.get("excecao_p18_da_cabeca")), "g1": "o portao de textos da G1 nao tem a R1 (medido pela custodia): a excecao fica so' na cadeia; a NOTA do handoff diz isso em uma linha"},
                              "d_e_g": "o resumo do que o teste nao decide; as traducoes EN marcadas para a revisao; tolerancia 1e-9 com 0,0 medido (c6_max_dif %s)" % TO["c6_max_dif"]},
       "registro_offline": {"n_ok": TO["n_ok"], "TUDO_PASSOU": TO["TUDO_PASSOU"], "sha16": s16("TESTE_H0DN_OFFLINE_v411.json")},
       "chaves_congeladas_com_a_g1": {"conferidas_no_registro_do_ensaio": chaves, "ok": chaves_ok, "regra": "nao renomear nenhuma; acrescentar so' se preciso"},
       "patches_do_gerador": {"W12_a2_txt": {"feito": True, "medida": A2["linguas"], "arquivo": "A2_MEDIDA_v411.json", "nota": "mudanca contida no conversor _tex_to_txt: ^{X} (X de 2 ou mais caracteres) vira ^(X) antes de dissolver as chaves; o conversor base reproduz o TXT do Nos (conferido); 261 linhas mudam em cada TXT"},
                              "seis_aberturas_da_escala": {"feito": False, "medido": "os trechos “na leitura do operador ela e' a ...” estao SO' em constantes seladas da v410 (_V410_IALD2_CONTRACT, _V410_IALD2_TEXT, _V410_SPECS, _V410_AESCALA_CONTRACT e _V410_AESCALA_TEXT; 7 ocorrencias), nenhuma no codigo do artigo; trocar o literal mudaria chave selada (INTOCADAS)",
                                                           "proposta": "achar onde o artigo IMPRIME esses campos do core e trocar na RENDERIZACAO (uma funcao de troca dita), sem tocar o registro selado; decisao da gerencia"}},
       "pre_voo": {"sha16_do_texto_com_a_PROPOSTA": PV["sha16"], "n_patches": PV["n_patches"], "bytes": PV["bytes"], "guardas_renderizado": PV["guarda_frases"]["violacoes_no_texto_renderizado"], "nota": "nao e' candidato"},
       "falta": {"scripts_com_corpo_da_v410_a_adaptar": MARCADOS, "n": len(MARCADOS),
                 "blocos_da_custodia_no_handoff": ["NOTA_EN_v411", "README_PAINEL_H0DN_v411 (EN e PT)", "README_PRIMORDIAL_5SIGMA_v411", "README_STATUS_5SIGMA_v411 (EN e PT)", "README_H0DN_v411"],
                 "regra_dos_blocos": "montados do MESMO lugar que a abertura do resumo (TOPO_RATIFICADO_v411.json e o core selado), numeros do core, a F67 no mesmo bloco; moldes da custodia so' lidos (tools\\custodia_g1\\textos.py, readme_pinado.py; the_boundary\\tools\\readme_pinado\\readme_partes\\p_igual_np.md)",
                 "nota_do_handoff": ["a contagem esperada de arquivos da pasta da cadeia", "os contratos de registro fora da escada (_V411_H0DN_CONTRACT)", "a excecao estreita da P18 (so' na cadeia; a G1 nao tem a R1)"]},
       "sequencia_exata": {"script": "cadeia_v411.sh", "sha16": s16("cadeia_v411.sh"), "uso": "sh ./cadeia_v411.sh (exige TOPO_RATIFICADO_v411.json; para, com rc 4, no primeiro script que ainda tenha a marca de copia mecanica)",
                           "passos": ["registro offline", "guarda de frases", "quadro renderizado", "citacoes", "candidato", "comparar v410/v411", "ensaio a seco", "esperados", "conferidor negativo", "conferidor positivo", "citacoes do candidato", "diff e pinos", "conferir_instalar_rito", "p00", "fim_de_cadeia (B20 pre-selo)", "relatorio"]},
       "ensaio_do_topo_proposto": "NAO montado nesta rodada (C:\\t\\k411c\\ensaio_topo_proposto\\ nao existe): fica para quando os scripts do ensaio estiverem adaptados",
       "copias_fora_de_work": ["C:\\t\\k411c\\final", "C:\\t\\k411c\\arvore_simulada_h8"], "tmp_na_pasta": [p_ for p_ in glob.glob(os.path.join(HERE, "**", "*.tmp"), recursive=True)]}
p = os.path.join(HERE, "PRONTO_PARA_GERAR_v411.json")
b = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"); open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print("PRONTO_PARA_GERAR_v411.json", hashlib.sha256(b).hexdigest()[:16], "| chaves congeladas ok:", chaves_ok, "| a adaptar:", len(MARCADOS))
