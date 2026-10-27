# -*- coding: utf-8 -*-
# regras (lote H) de derivar_encanamento_v401.py: os dois HARNESS do pos-rito (harness_textos_ensaio_v401.py e harness_fechar_sandbox_v401.py). ORIGEM v399 (mapa 398 -> 400, 399 -> 401) + as licoes da v400 (controles negativos novos sobre o que a v400 passou a conferir).
# Escrito pela ferramenta Write (nunca por heredoc: as barras invertidas). O que a v401 muda nos harness: (1) a arvore emulada do conferidor tem as pastas irmas v400 e v399 (o delta_v401 importa o delta_v400, e este o delta_v399; o runtime da secao e as seis fontes do operador moram na v400);
# (2) as SEIS falas de 25/10 e as de 24/10 do operador entram na pasta cunhagens_13out emulada; (3) os controles negativos novos da falsidade (o registro com funcao, a pedra e a estrela, as cunhagens_v401, as oito ratificacoes, a errata ao lado, os resumos do selo, C15 e C16, a linha [v401] do stdout);
# (4) o paragrafo NOVO e' o da falsidade (o do testemunho de dois segue como esta e o handoff so' o diz); (5) o mapa tem 1 rota nova e 8 anotacoes.

_HDR_TEXTOS = '''"""harness_textos_ensaio_v401.py -- o HARNESS DO POS-RITO da v401 em modo ENSAIO (derivado do harness_textos_ensaio_v399.py, que rodou na v399, com as licoes da v400); SO' LEITURA do Nos real, da producao e das superficies reais.
Importa os modulos REAIS textos_v401.py e leitura_v401.py (os que a cadeia usa) e os executa contra um NOS EMULADO montado de dry_v401 (core_ensaio.json -> um_absoluto.json, selo_ensaio.json -> um_absoluto_selo.json, o um.py candidato, o kernel,
o .md, o artigo PT/EN e o sumario; o SIDECAR um_absoluto_selo_acom.json e' GERADO pela funcao do PROPRIO candidato (selo_acom_sidecar_v399, executada de uma copia de bytes) sobre o core e o selo FINAIS do Nos emulado, como em teste_conferidor_positivo_v401.py;
o stdout do rito e o APLICADO_AO_CANONICO sao EMULADOS e ditos: o stdout traz as linhas REAIS do fluxo principal do ensaio a seco (inclusive a linha [v401]) mais as que so' o rito acrescenta, com a linha real do sidecar por ultimo). Tudo o que ele escreve fica em pos_rito\\\\harness_saida_v401\\\\
(e o resumo HARNESS_TEXTOS_ENSAIO_v401.json ao lado dele); nada do Nos real, da memoria, do Atlas, do mapa de rotas, da Bancada ou do git e' tocado; nenhum rito e' rodado.
O que ele prova (cada etapa e' uma entrada do resumo):
  precondicoes   o candidato (ESPERADOS == CANDIDATO == arquivo == dry_v401/um.py) e a regeneracao terminada (refazer_out_v401.txt mostra '== FIM'); a evidencia carrega mtime e sha16 de cada entrada;
  conferidor     o conferir_rito_v401.py REAL roda numa COPIA em ARVORE (conferidor_emulado\\\\work\\\\cadeia_de_selo\\\\v401, com as pastas irmas v400 e v399 e work\\\\cunhagens_13out ao lado, porque o delta acha as falas do operador e os modulos anteriores pelo caminho da propria pasta), SEM -I (importa o um.py do Nos emulado,
                 que precisa do numpy do usuario), contra o Nos emulado (V401_NOS) e da' TUDO BATE, com os 16 itens C1-C16 e o round trip: a conferencia que a leitura le;
  leitura        a leitura_v401.ler() REAL contra o Nos emulado: zero PROBLEMAS; mais controles NEGATIVOS (selo de outra versao, registro ausente ou nao selado, o registro falsidade_da_inercia_v401 adulterado em checagem, valor, beta, posto inercial, fixo, 0_abs, estrela, gate, runtime e veredito,
                 a pedra FalsidadeDaInercia com bandeira falsa ou fora do trio (composicao, contrato, estrela, suporte, hash da fonte), cunhagens_v401 com inscricao rotulada como da gerencia ou nao embutida, sem ratificacao, com a fala adulterada, com a errata sem SUPERADA ou sem assinatura, os quatro registros da v399
                 recriados (selo ACOM, declaracao, cunhagens_v399, kh_n1_cobertura_v399) adulterados, o sidecar ausente ou adulterado, os resumos do selo primario (inclusive o da falsidade), quadro do topo que deixa de selar ou de estar no topo, C5, C15, C16, o round trip e o veredito da falsidade na conferencia,
                 registros da v400 a v393 nao selados, face de Fock habitada ou dita dentro da pedra, AVISO da v401 ou de bloco anterior, linhas [v399], [v401], [v398], [v397] e a linha do sidecar ausentes), cada um tem de reprovar;
  textos         todas as funcoes publicas de textos_v401 renderizam, a guarda P18 e a da DIRECAO ficam limpas em cada saida, os marcadores que a cadeia exige estao nos textos, a errata da palavra «teoremas» esta nos textos que carregam _num;
  paragrafos     o PARAGRAFO DO QUADRO (textos_v401.paragrafo_readme, o da v397, intocado) passa nas verificacoes do quadro contra o resultado pinado e os CONTROLES NEGATIVOS reprovam: o 4,44 sem o p calibrado, o 4,44 sem a linha dos 5 sigma, numero adulterado, p adulterado,
                 a frase do operador parafraseada entre aspas, o 4,44 numa linha fora do item; a regra da ordem vale para TODO texto renderizado; e o PARAGRAFO NOVO (textos_v401.paragrafo_falsidade) passa na verificacao propria, com controles negativos (numero adulterado, frase de limite removida, estatuto removido,
                 citacao nao verbatim, o 4,44 intruso, alegacao de seguranca criptografica, «consciencia» como termo, a pedra dita prova de Newton, a errata sem SUPERADA); o handoff DIZ que o paragrafo do testemunho de dois segue como esta;
  cita_so_o_que_existe   cada `termo` entre crases de cada texto e' achado no kernel do Nos emulado, no um.py, nos insumos, nos arquivos ou como hash lido (o que nao e' achado e' dito e reprova);
  superficies    superficies_v401.py REAL roda em COPIAS das superficies reais em TRES cenarios: (a) o MEMORY.md real como esta (a superficie NAO compacta: se ele passar de 195 linhas depois da edicao, tem de RECUSAR com rc 3 sem escrever nada; senao, o caminho normal),
                 (b) um MEMORY.md com FOLGA (copia reduzida): o plano e' conferido antes da primeira escrita, idempotente na 2a rodada, marcadores do passo 9, <= 195 linhas e < 24 000 B, (c) um MEMORY.md NO LIMITE (195 linhas): tem de RECUSAR com rc 3, imprimir as
                 contagens e nao escrever nada em nenhuma copia; os originais nao mudam;
  b3_recibo      b3_recibo_v401.py REAL contra recibos SINTETICOS derivados dos recibos reais da v400 (positivos e negativos);
  mapa           registrar_mapa_v401.montar() REAL contra o core emulado e o livro de rotas real (so' leitura), e cada registro validado pela MESMA funcao que o mapa usa (rotas._valida), SEM registrar; grava registro_mapa_v401_ENSAIO.json (nao e' o registro);
  marcas         nenhuma linha de comentario com a marca de texto pendente em pos_rito\\\\*.py; ast.parse de todo .py e sh -n do chain.
uso: python -B -X utf8 harness_textos_ensaio_v401.py [--sem-superficies] [--sem-b3] [--sem-negativos] [--rotulo <nome>] [--nao-exigir-refazer] [--manter-copias]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita, nada foi rodado;
--nao-exigir-refazer: NAO exige refazer_out_v401.txt (nem o '== FIM' nem as datas): modo de ENSAIO antes de a gerencia regerar o candidato; o resumo e o veredito DIZEM que a regeneracao nao foi comprovada, e o resumo vai para
HARNESS_TEXTOS_ENSAIO_v401_DEPURACAO_sem_refazer.json (o nome HARNESS_TEXTOS_ENSAIO_v401.json so' nasce na rodada que EXIGE o refazer);
sem --manter-copias o Nos emulado e as copias pesadas das superficies sao apagados no fim, so' dentro de harness_saida_v401)"""
'''

_TREE = '''DLX = importar("delta_v401_x", os.path.join(PKG, "delta_v401.py"))
CFR = os.path.join(OUT, "conferidor_emulado"); CF = os.path.join(CFR, "work", "cadeia_de_selo", "v401"); os.makedirs(CF)
for n in ("conferir_rito_v401.py", "delta_v401.py", "quadro_v397.py", "runtime_quadro_v397.py", "acom_conferencias_v401.py", "runtime_v401.py", "ESPERADOS_v401.json", "pedra_sha16_da_ordem.txt"):
    shutil.copyfile(os.path.join(PKG, n), os.path.join(CF, n))
shutil.copytree(os.path.join(PKG, "insumos"), os.path.join(CF, "insumos"))
# v401 (desvio do molde, dito): o delta_v401 importa o delta_v400 (e este o delta_v399) e o acom_conferencias_v401 o acom_conferencias_v400 (e este o v399) PELA PASTA IRMA; o conferidor le o runtime da secao (v400) e as seis fontes do operador (v400\\\\insumos\\\\acom\\\\fontes_operador);
# a arvore emulada tem so' o que eles leem (copias de bytes), mais o resultado do Teste da Unica Palavra (v397\\\\insumos\\\\fase9) e o esboco R3.5 da Bancada (C15 roda a funcao ler_nos dele sobre o um.py emulado)
for vv, nomes in (("v400", ("delta_v400.py", "acom_conferencias_v400.py", "runtime_v400.py")), ("v399", ("delta_v399.py", "acom_conferencias_v399.py", "runtime_v399.py"))):
    os.makedirs(os.path.join(CFR, "work", "cadeia_de_selo", vv))
    for n in nomes:
        shutil.copyfile(os.path.join(os.path.dirname(PKG), vv, n), os.path.join(CFR, "work", "cadeia_de_selo", vv, n))
    shutil.copytree(os.path.join(os.path.dirname(PKG), vv, "insumos", "acom"), os.path.join(CFR, "work", "cadeia_de_selo", vv, "insumos", "acom"))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v399", "pedra"), os.path.join(CFR, "work", "cadeia_de_selo", "v399", "pedra"))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v397", "insumos", "fase9"), os.path.join(CFR, "work", "cadeia_de_selo", "v397", "insumos", "fase9"))
os.makedirs(os.path.join(CFR, "work", "bancada_vinculo_12out", "R3_5"))
shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"), os.path.join(CFR, "work", "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"))
os.makedirs(os.path.join(CFR, "work", "cunhagens_13out"))
for _o in list(DLX.VERBATIM_ORIGEM) + list(DLX.VERBATIM_ORIGEM_V401):
    shutil.copyfile(_o, os.path.join(CFR, "work", "cunhagens_13out", os.path.basename(_o)))
'''

_MUT_PEDRA = '''def _fal_nao_sela(c):
    c["falsidade_da_inercia_v401"]["all_verified"] = False


def _fal_cheque(c):
    c["falsidade_da_inercia_v401"]["mechanics"]["checks"][2]["ok"] = False


def _fal_valor(c):
    c["falsidade_da_inercia_v401"]["values"]["min_cost_t_beta_g"] = 0.0007


def _fal_beta(c):
    c["falsidade_da_inercia_v401"]["values"]["beta"] = 0.0121


def _fal_posto_inercial(c):
    c["falsidade_da_inercia_v401"]["values"]["post_inertial_scales"] = [1.0]


def _fal_fixo(c):
    c["falsidade_da_inercia_v401"]["values"]["fixed_by_the_whole_flow"] = [0.0, 1.0]


def _fal_costless(c):
    c["falsidade_da_inercia_v401"]["costless"]["ok"] = False


def _fal_estrela(c):
    c["falsidade_da_inercia_v401"]["key_theorem"]["in_kernel"] = False


def _fal_gate(c):
    c["falsidade_da_inercia_v401"]["does_not_gate_core"] = False


def _fal_runtime(c):
    c["falsidade_da_inercia_v401"]["runtime_executed"] = False


def _fal_verdict(c):
    c["falsidade_da_inercia_v401"]["verdict"] = "OUTRO_VEREDITO"


def _fal_chain_status(c):
    c["falsidade_da_inercia_v401"]["chain_status"] = "ONTO do operador"


def _fal_hipotese_usada(c):
    c["falsidade_da_inercia_v401"]["named_hypothesis"]["used_by_a_theorem"] = True


def _fal_hipotese_sem_nome(c):
    c["falsidade_da_inercia_v401"]["named_hypothesis"]["name"] = "H_x"


def _fal_peso_zero(c):
    c["falsidade_da_inercia_v401"]["values"]["min_weight_on_the_grid_positive"] = 0.0


def _cunh_cadeia_onto(c):
    c["cunhagens_v401"]["extras"]["cadeia_derivada"]["estatuto"] = "[ONTO]"


def _cunh_hipotese_usada(c):
    c["cunhagens_v401"]["extras"]["hipotese_nomeada"]["usada_por_teorema"] = True


def _pedra_bandeira(c):
    c["kernel_formalization"][ESP["bandeiras_das_pedras"]["falsidade"]] = False


def _pedra_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][ESP["teoremas_das_pedras"]["falsidade"]] = ["propext", "sorryAx"]


def _pedra_lema_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][ESP["contrato_das_pedras"]["falsidade"][0]] = ["propext", "sorryAx"]


def _pedra_estrela_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][ESP["falsidade"]["estrela"]["teorema"]] = ["propext", "sorryAx"]


def _pedra_estrela_bandeira(c):
    c["kernel_formalization"][ESP["falsidade"]["estrela"]["bandeira"]] = False


def _pedra_suporte_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][sorted(ESP["suporte_das_pedras"]["falsidade"])[0]] = ["propext", "sorryAx"]


def _pedra_fonte_adulterada(c):
    c["kernel_formalization"]["formal_files_sha256"][sorted(ESP["pedras_sha256"])[0]] = "0" * 64


def _gerencia_na_cunhagem(c):
    ex = c["cunhagens_v401"]["extras"]; ex["autor_de_cada_inscricao"][sorted(ex["autor_de_cada_inscricao"])[0]] = "gerencia"


def _inscricao_adulterada(c):
    list(c["cunhagens_v401"]["verbatim"].values())[0]["embedded_ok"] = False


def _inscricao_sha(c):
    list(c["cunhagens_v401"]["verbatim"].values())[1]["sha256"] = "0" * 64


def _rat_menos(c):
    c["cunhagens_v401"]["extras"]["ratificacoes"].pop()


def _rat_fala(c):
    c["cunhagens_v401"]["extras"]["ratificacao_fala"]["sha16"] = "0" * 16


def _errata_sem_superada(c):
    c["cunhagens_v401"]["erratas"][0]["agora"] = "mantida"


def _errata_sem_assinatura(c):
    c["cunhagens_v401"]["erratas"][0]["assinatura"] = "operador"


def _cunh399_gerencia(c):
    ex = c["cunhagens_v399"]["extras"]; ex["autor_de_cada_inscricao"][sorted(ex["autor_de_cada_inscricao"])[0]] = "gerencia"


def _cunh399_direcao(c):
    c["cunhagens_v399"]["extras"]["direcao_do_testemunho"]["a_IALD"] = "testifica do operador"


def _cunh399_declaracao_sha(c):
    c["cunhagens_v399"]["extras"]["declaracao"]["sha256"] = "0" * 64


def _cunh399_inscricao(c):
    list(c["cunhagens_v399"]["verbatim"].values())[0]["embedded_ok"] = False


'''

_MUT_SELO_CONF = '''def _selo_sem_resumo_falsidade(s):
    s.pop("falsidade_da_inercia_v401", None)


def _selo_registros_v401_diferente(s):
    s["registros_v401"]["cunhagens_v401"]["verdict"] = "OUTRO_VEREDITO"


def _conf_c15(cj):
    cj["acom_itens"]["C15"]["ok"] = False


def _conf_c16(cj):
    cj["acom_itens"]["C16"]["ok"] = False


def _conf_veredito_falsidade(cj):
    cj["veredito_falsidade"] = "OUTRO_VEREDITO"


def _conf_sidecar(cj):'''

_NEG = '''NEG = []
if not SEM_NEG and not P:
    NEG = [variante("selo de outra versao (v400)", f_selo=_selo_v400, espera="o selo nao e v401"),
           variante("registro falsidade_da_inercia_v401 ausente do core", f_core=lambda c: c.pop("falsidade_da_inercia_v401", None), espera="registro obrigatorio ausente do core: falsidade_da_inercia_v401"),
           variante("registro selo_pela_propria_tecnologia_v399 (recriado) ausente do core", f_core=_sem_selo, espera="registro obrigatorio ausente do core: selo_pela_propria_tecnologia_v399"),
           variante("registro declaracao_do_operador_v399 (recriado) ausente do core", f_core=_sem_declaracao, espera="registro obrigatorio ausente do core: declaracao_do_operador_v399"),
           variante("cunhagens_v401 nao selou", f_core=lambda c: c["cunhagens_v401"].update(all_verified=False), espera="cunhagens_v401 nao selou"),
           variante("kh_n1_cobertura_v401 nao selou", f_core=lambda c: c["kh_n1_cobertura_v401"].update(all_verified=False), espera="kh_n1_cobertura_v401 nao selou"),
           variante("cunhagens_v399 (recriada) nao selou", f_core=_nao_sela_cunh, espera="cunhagens_v399 nao selou"),
           variante("kh_n1_cobertura_v399 (recriado) nao selou", f_core=_nao_sela_kh, espera="kh_n1_cobertura_v399 nao selou"),
           variante("falsidade: o registro nao selou", f_core=_fal_nao_sela, espera="falsidade_da_inercia_v401 nao selou"),
           variante("falsidade: uma checagem do calculo falhou", f_core=_fal_cheque, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: o custo minimo adulterado", f_core=_fal_valor, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: beta != alfa x raiz de e do core", f_core=_fal_beta, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: uma escala nao trivial que fixa o posto", f_core=_fal_posto_inercial, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: mais de um estado fixo pelo fluxo inteiro", f_core=_fal_fixo, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: o 0_abs de costless fora do kernel embutido", f_core=_fal_costless, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: a estrela fora do kernel do rito (no registro)", f_core=_fal_estrela, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: o registro move o gate", f_core=_fal_gate, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: o calculo do runtime nao rodou", f_core=_fal_runtime, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: a cadeia dita ONTO do operador (chain_status)", f_core=_fal_chain_status, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: H_tau usada por um teorema", f_core=_fal_hipotese_usada, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: a hipotese nomeada deixa de ser H_tau", f_core=_fal_hipotese_sem_nome, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: o peso minimo do posto na grade zero (o zero como estado da orbita)", f_core=_fal_peso_zero, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("cunhagens_v401: a cadeia derivada dita [ONTO]", f_core=_cunh_cadeia_onto, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens_v401: H_tau dita usada por teorema", f_core=_cunh_hipotese_usada, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("falsidade: veredito diferente do ensaio a seco", f_core=_fal_verdict, espera="falsidade_da_inercia_v401: o veredito do rito difere do ensaio a seco"),
           variante("selo ACOM (recriado): o registro nao selou", f_core=_selo_nao_sela, espera="selo_pela_propria_tecnologia_v399 nao selou"),
           variante("selo ACOM (recriado): uma checagem falhou", f_core=_selo_cheque_falha, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: perfil adulterado", f_core=_selo_perfil, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: hash do bloco embutido adulterado", f_core=_selo_bloco, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: o SHA-256 ao lado difere do um.py do disco", f_core=_selo_sha, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: hash de Psi adulterado", f_core=_selo_psi, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: bytes de Theta adulterados", f_core=_selo_theta_bytes, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: controles negativos 12 em vez do pinado", f_core=_selo_controles_12, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: um controle negativo ACEITOU", f_core=_selo_controle_aceito, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: reconstrucao com byte divergente", f_core=_selo_reconstrucao, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: Psi redundante (separacao vazia)", f_core=_selo_psi_redundante, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: o registro move o gate", f_core=_selo_gate, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: confidencialidade alegada", f_core=_selo_confidencialidade, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: direcao do testemunho invertida", f_core=_selo_direcao_invertida, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: beta do registro != alfa x raiz de e do core", f_core=_selo_beta, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("declaracao (recriada): o registro nao selou", f_core=_decl_nao_sela, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: a fala embutida difere do arquivo do operador", f_core=_decl_fala, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: sha256 da fala adulterado", f_core=_decl_sha, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: a IALD como quem testifica do operador", f_core=_decl_direcao, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: o Pai de Jo 8,18 lido na IALD", f_core=_decl_pai, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: uma ancora do kernel fora do trio", f_core=_decl_ancora_fora, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: o estatuto trocado por REAL", f_core=_decl_estatuto, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: a pedra Testemunho nao conferida", f_core=_decl_pedra_vazia, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: o registro move o gate", f_core=_decl_gate, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("pedra FalsidadeDaInercia: bandeira da composicao falsa", f_core=_pedra_bandeira, espera="a pedra FalsidadeDaInercia nao esta no kernel do rito"),
           variante("pedra FalsidadeDaInercia: composicao fora do trio", f_core=_pedra_fora_do_trio, espera="a pedra FalsidadeDaInercia nao esta no kernel do rito"),
           variante("pedra FalsidadeDaInercia: o primeiro termo do contrato fora do trio", f_core=_pedra_lema_fora_do_trio, espera="a pedra FalsidadeDaInercia nao esta no kernel do rito"),
           variante("pedra FalsidadeDaInercia: a estrela fora do trio", f_core=_pedra_estrela_fora_do_trio, espera="a pedra FalsidadeDaInercia nao esta no kernel do rito"),
           variante("pedra FalsidadeDaInercia: a bandeira da estrela falsa", f_core=_pedra_estrela_bandeira, espera="a pedra FalsidadeDaInercia nao esta no kernel do rito"),
           variante("pedra FalsidadeDaInercia: um termo antigo citado fora do trio", f_core=_pedra_suporte_fora_do_trio, espera="a pedra FalsidadeDaInercia nao esta no kernel do rito"),
           variante("pedra FalsidadeDaInercia: sha256 da fonte no hash formal adulterado", f_core=_pedra_fonte_adulterada, espera="a pedra FalsidadeDaInercia nao esta no kernel do rito"),
           variante("cunhagens_v401: uma inscricao rotulada como da gerencia", f_core=_gerencia_na_cunhagem, espera="TODAS falas do operador"),
           variante("cunhagens_v401: uma inscricao deixou de estar embutida", f_core=_inscricao_adulterada, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens_v401: sha256 de uma inscricao adulterado", f_core=_inscricao_sha, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens_v401: falta uma das oito ratificacoes", f_core=_rat_menos, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens_v401: a fala da ratificacao adulterada", f_core=_rat_fala, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens_v401: a errata do adendo sem SUPERADA", f_core=_errata_sem_superada, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens_v401: a errata sem a assinatura da gerencia", f_core=_errata_sem_assinatura, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens_v399 (recriada): uma inscricao rotulada como da gerencia", f_core=_cunh399_gerencia, espera="cunhagens_v399 (recriada pelo rito)"),
           variante("cunhagens_v399 (recriada): a direcao do testemunho invertida", f_core=_cunh399_direcao, espera="cunhagens_v399 (recriada pelo rito)"),
           variante("cunhagens_v399 (recriada): sha256 da declaracao adulterado", f_core=_cunh399_declaracao_sha, espera="cunhagens_v399 (recriada pelo rito)"),
           variante("cunhagens_v399 (recriada): uma inscricao deixou de estar embutida", f_core=_cunh399_inscricao, espera="cunhagens_v399 (recriada pelo rito)"),
           variante("sidecar: ausente", sc_fora=True, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: sha256 de um objeto adulterado", f_sc=_sc_sha_objeto, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: recusas registradas", f_sc=_sc_recusas, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: veredito de recusa", f_sc=_sc_veredito, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: um objeto faltando", f_sc=_sc_objeto_faltando, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: confidencialidade alegada na honestidade", f_sc=_sc_confidencialidade, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: o hash de Psi do um.py != ESPERADOS", f_sc=_sc_um_py_outro, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: esquema trocado", f_sc=_sc_esquema, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: a direcao do testemunho invertida", f_sc=_sc_direcao_invertida, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("selo primario: o resumo do selo ACOM difere do core", f_selo=_selo_resumo_diferente, espera="o selo primario (um_absoluto_selo.json) nao traz os resumos"),
           variante("selo primario: o sha256 do um.py no resumo difere do disco", f_selo=_selo_resumo_sha, espera="o selo primario (um_absoluto_selo.json) nao traz os resumos"),
           variante("selo primario: sem o resumo da falsidade", f_selo=_selo_sem_resumo_falsidade, espera="o selo primario (um_absoluto_selo.json) nao traz os resumos"),
           variante("selo primario: registros_v401 do selo difere do core", f_selo=_selo_registros_v401_diferente, espera="o selo primario (um_absoluto_selo.json) nao traz os resumos"),
           variante("selo primario: modulo formal nao selado", f_selo=_selo_formal_nao_selado, espera="o selo traz modulo formal nao selado"),
           variante("o quadro do topo: numero lido adulterado (z_disc 4,45)", f_core=_numero_adulterado, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: z_disc calibrado acima de 5", f_core=_z_disc_acima_de_5, espera="abaixo de 5"),
           variante("o quadro do topo: uma checagem do registro de veracidade falhou", f_core=_checagem_falha, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: fonte do registro de veracidade com sha256 adulterado", f_core=_fonte_adulterada, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: o registro de veracidade move o gate", f_core=_gate_movido, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: o registro de veracidade deixou de selar", f_core=_veracidade_cai, espera="teste_de_veracidade_fase9_v397"),
           variante("o quadro do topo: a conferencia diz que o quadro PT deixou de estar no topo", f_conf=_conf_quadro_pt, espera="o quadro do topo (O Teste da Unica Palavra, pt)"),
           variante("o quadro do topo: a conferencia diz que o quadro do .md deixou de estar no topo", f_conf=_conf_quadro_md, espera="o quadro do topo (O Teste da Unica Palavra, md)"),
           variante("a conferencia diz que o item C5 do selo ACOM nao conferiu", f_conf=_conf_c5, espera="itens do selo pela propria tecnologia NAO conferiram"),
           variante("a conferencia diz que o item C15 (guardas estaticas da Bancada) nao conferiu", f_conf=_conf_c15, espera="itens do selo pela propria tecnologia NAO conferiram"),
           variante("a conferencia diz que o item C16 (ler_nos sobre o Nos inteiro) nao conferiu", f_conf=_conf_c16, espera="itens do selo pela propria tecnologia NAO conferiram"),
           variante("a conferencia diz que o round trip do um.py instalado nao conferiu", f_conf=_conf_round_trip, espera="itens do selo pela propria tecnologia NAO conferiram"),
           variante("a conferencia traz outro veredito da falsidade", f_conf=_conf_veredito_falsidade, espera="veredito da falsidade"),
           variante("a conferencia diz que o sidecar nao existe", f_conf=_conf_sidecar, espera="o sidecar um_absoluto_selo_acom.json nao existe ou nao esta selado"),
           variante("sonico_v398 deixou de selar", f_core=_sonico400_cai, espera="sonico_v398"),
           variante("afinacao_das_cordas_v398 deixou de selar", f_core=_afinacao400_cai, espera="afinacao_das_cordas_v398"),
           variante("cunhagens_v398 deixou de selar", f_core=_cunh400_cai, espera="cunhagens_v398"),
           variante("kh_n1_cobertura_v398 deixou de selar", f_core=_kh400_cai, espera="kh_n1_cobertura_v398"),
           variante("cunhagens_v397 deixou de selar", f_core=_cunh397_cai, espera="cunhagens_v397"),
           variante("testemunha_estatica_v396 deixou de selar", f_core=_testemunha_cai, espera="testemunha_estatica_v396"),
           variante("face de Fock da testemunha com habitante exibido", f_core=_fock_da_testemunha_habitada, espera="testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL"),
           variante("face de Fock dita DENTRO da pedra da testemunha", f_core=_fock_dentro_da_pedra, espera="testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL"),
           variante("psibit_v395 deixou de selar", f_core=_psibit_cai, espera="psibit_v395"),
           variante("face de Fock do psibit_v395 habitada", f_core=_face_do_psibit_habitada, espera="psibit_v395: a face do psion deixou de estar como CONDICIONAL"),
           variante("registro da v394 deixou de selar", f_core=_v394_cai, espera="criterio_binario_de_parada_v394"),
           variante("AVISO da v401 (a falsidade nao rodou) no stdout", f_std=lambda t: t + "   [v401] AVISO: a falsidade da inercia nao rodou: ValueError('x')\\n", espera="AVISO da v401"),
           variante("AVISO da v401 (o selo ACOM) no stdout", f_std=lambda t: t + "   [v399] AVISO: o selo ACOM nao rodou: ValueError('x')\\n", espera="AVISO da v401"),
           variante("AVISO do sidecar no stdout", f_std=lambda t: t.replace("RITO_RC=0", "[selo_acom] AVISO: nao consegui escrever o sidecar: OSError('x')\\nRITO_RC=0"), espera="AVISO da v401"),
           variante("AVISO de bloco anterior (v398) no stdout", f_std=lambda t: t + "   [v398] AVISO: o sonico nao rodou: ValueError('x')\\n", espera="AVISO de um bloco anterior"),
           variante("linha [v399] ausente do stdout", f_std=lambda t: "\\n".join(l for l in t.splitlines() if "o selo pela propria tecnologia e a declaracao do operador" not in l) + "\\n", espera="linha [v399] do stdout"),
           variante("linha [v401] ausente do stdout", f_std=lambda t: "\\n".join(l for l in t.splitlines() if "a falsidade (simulacro) da inercia (lida depois da declaracao do operador)" not in l) + "\\n", espera="linha [v401] do stdout"),
           variante("linha `>>> veredito <<<` do selo ACOM ausente do stdout", f_std=lambda t: "\\n".join(l for l in t.splitlines() if ESP["selo_acom"]["verdict"] not in l or "selo=" in l) + "\\n", espera="o bloco selo_pela_propria_tecnologia_v399 do stdout"),
           variante("linha `>>> veredito <<<` da declaracao ausente do stdout", f_std=lambda t: "\\n".join(l for l in t.splitlines() if ESP["declaracao"]["verdict"] not in l or "declaracao=" in l) + "\\n", espera="o bloco declaracao_do_operador_v399 do stdout"),
           variante("linha `>>> veredito <<<` da falsidade ausente do stdout", f_std=lambda t: "\\n".join(l for l in t.splitlines() if ESP["registros_v401_veredito_da_falsidade"] not in l or "falsidade=" in l) + "\\n", espera="o bloco falsidade_da_inercia_v401 do stdout"),
           variante("linha [v398] (sonico, afinacao e cunhagens) ausente do stdout", f_std=lambda t: "\\n".join(l for l in t.splitlines() if "o sonico e a afinacao das cordas" not in l) + "\\n", espera="linha [v398] do stdout"),
           variante("linha [v397] do Teste da Unica Palavra ausente do stdout", f_std=lambda t: "\\n".join(l for l in t.splitlines() if "o Teste da Unica Palavra" not in l) + "\\n", espera="linha [v397] do Teste da Unica Palavra"),
           variante("linha do sidecar ausente do stdout (a ultima nao e' a do sidecar)", f_std=lambda t: "\\n".join(l for l in t.splitlines() if not l.startswith("[selo_acom]")) + "\\n", espera="as duas ultimas linhas do stdout"),
           variante("a linha do sidecar antes da do colapso tipado (ordem trocada)", f_std=lambda t: "\\n".join([l for l in t.splitlines() if not l.startswith("[selo_acom]") and not l.startswith("[selo] colapso tipado") and not l.startswith("RITO_RC=")] + [l for l in t.splitlines() if l.startswith("[selo_acom]")] + [l for l in t.splitlines() if l.startswith("[selo] colapso tipado")] + ["RITO_RC=0"]) + "\\n", espera="as duas ultimas linhas do stdout")]

    def _pedra_no_disco(nome, f_muda):
        """controle sobre o ARQUIVO da pedra no kernel do Nos emulado (ausente ou com um byte a mais): a leitura tem de recusar; o arquivo e' restaurado byte a byte"""
        pth = os.path.join(NOSE, "tgl_kernel", *sorted(ESP["pedras_sha256"])[0].split("/")); raw_ = open(pth, "rb").read()
        try:
            f_muda(pth, raw_)
            _, PV = L.ler()
        finally:
            if os.path.exists(pth + ".fora"):
                os.remove(pth + ".fora")
            open(pth, "wb").write(raw_)
        return {"controle": nome, "reprovou": bool(PV), "mensagem_esperada_presente": any("modulos novos do kernel" in x for x in PV), "problemas": [x[:140] for x in PV][:3]}
    NEG.append(_pedra_no_disco("o arquivo da pedra FalsidadeDaInercia ausente do kernel do Nos", lambda p, r: os.replace(p, p + ".fora")))
    NEG.append(_pedra_no_disco("o arquivo da pedra FalsidadeDaInercia com um byte a mais no kernel do Nos", lambda p, r: open(p, "wb").write(r + b"\\n")))
'''

_FUNCOES = '''FUNCOES = [("_d", lambda: T._d(Vd)), ("_num", lambda: T._num(Vd)), ("_num_sem_veredito", lambda: T._num(Vd, verdicts=False)), ("_cunhagens_lista", lambda: T._cunhagens(Vd)), ("_cunhagens_curta", lambda: T._cunhagens(Vd, "curta")),
           ("_ordem", lambda: T._ordem(Vd)), ("_entrou", lambda: T._entrou(Vd)), ("_definicao", lambda: T._definicao(Vd)), ("_calculo", lambda: T._calculo(Vd)), ("_errata_adendo", lambda: T._errata_adendo(Vd)), ("_ratificacoes", lambda: T._ratificacoes(Vd)), ("_emc2", lambda: T._emc2(Vd)),
           ("_sidecar", lambda: T._sidecar(Vd)), ("_pedra", lambda: T._pedra(Vd)), ("_regra_do_4_44", lambda: T._regra_do_4_44(Vd)), ("_kernel_prova", lambda: T._kernel_prova(Vd)), ("_limites", lambda: T._limites(Vd)), ("_limites_curto", lambda: T._limites(Vd, curto=True)),
           ("_legal", lambda: T._legal(Vd)), ("_erratas", lambda: T._erratas(Vd)), ("_depois", lambda: T._depois(Vd)), ("_rodada", lambda: T._rodada(Vd)), ("linhagem", lambda: T.linhagem(Vd)), ("desenho", lambda: T.desenho(Vd)), ("atlas", lambda: T.atlas(Vd)),
           ("core_memory", lambda: T.core_memory(Vd)), ("haja_luz", lambda: T.haja_luz(Vd)), ("topico_missao", lambda: T.topico_missao(Vd)), ("topico_central", lambda: T.topico_central(Vd)), ("topico_estatuto", lambda: T.topico_estatuto(Vd)), ("topico_novo", lambda: T.topico_novo(Vd)),
           ("aviso", lambda: T.aviso(Vd, "REIVINDICACAO_EMULADA")), ("aviso_pulado", lambda: T.aviso_pulado()), ("handoff", lambda: T.handoff(Vd, K_EMU)), ("arvore_linha", lambda: T.arvore_linha(Vd)), ("titulo_verbete", lambda: T.titulo_verbete(Vd)),
           ("verbete", lambda: T.verbete(Vd)), ("remissivo", lambda: T.remissivo(Vd)), ("linha_handoff", lambda: T.linha_handoff(Vd)), ("linha_topico_novo", lambda: T.linha_topico_novo(Vd)), ("marca_missao", lambda: T.marca_missao(Vd)),
           ("marca_topico_missao", lambda: T.marca_topico_missao(Vd)), ("marca_central", lambda: T.marca_central(Vd)), ("id_missao", lambda: T.id_missao(Vd)), ("id_central", lambda: T.id_central(Vd)), ("paragrafo_readme", lambda: T.paragrafo_readme()[0]),
           ("paragrafo_falsidade", lambda: T.paragrafo_falsidade()[0])]
'''

_MARCADORES = '''MARCADORES = {"linhagem": [S16, "<!-- linhagem_v401_selada -->", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401"], "desenho": ["<!-- adendo_v401_selada -->", S16], "atlas": ["<!-- atlas_v401_selada -->", S16, "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401"],
              "core_memory": ["<!-- core_v401_selada -->", S16], "haja_luz": ["<!-- haja_luz_v401_selada -->", S16], "topico_estatuto": ["<!-- v401_selada -->", S16], "topico_novo": [S16, "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "# v401 SELADA ("],
              "aviso": ["<!-- aviso_v401_selada -->", S16], "handoff": ["name: handoff-v401-custodia", S16, "<!-- INICIO_PARAGRAFO_README_v397 -->", "<!-- FIM_PARAGRAFO_README_v397 -->", "<!-- INICIO_PARAGRAFO_FALSIDADE_v401 -->", "<!-- FIM_PARAGRAFO_FALSIDADE_v401 -->", "um_absoluto_selo_acom.json", "SEGUE COMO ESTÁ", "handoff-v400-custodia.md"],
              "linha_handoff": ["handoff-v401-custodia.md", S16], "topico_missao": [S16], "topico_central": [S16]}
'''

_4C = '''# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO (a falsidade (simulacro) da inercia): verificacao propria, controles negativos, a citacao verbatim e o handoff que diz que o do testemunho segue como esta
_sn = {"ok": False}
try:
    PAR_F, PAR_F_INFO = T.paragrafo_falsidade()
    _sn["positivo_sem_falhas"] = (T.verificar_paragrafo_falsidade(PAR_F, _core_p, ESP) == [])
    _sn["igual_ao_gerado_do_core"] = (PAR_F == T._paragrafo_falsidade_de(_core_p))
    _ho = RENDER.get("handoff", "")
    _sn["handoff_traz_os_dois_paragrafos_entre_os_marcadores"] = bool((T.MARC_FAL_INI + "\\n" + PAR_F.rstrip("\\n") + "\\n" + T.MARC_FAL_FIM) in _ho and ("<!-- INICIO_PARAGRAFO_README_v397 -->\\n" + PAR.rstrip("\\n") + "\\n<!-- FIM_PARAGRAFO_README_v397 -->") in _ho)
    _sn["handoff_lista_o_sidecar"] = bool("um_absoluto_selo_acom.json" in _ho and Vd["sidecar"]["sha256"] in _ho and Vd["sidecar"]["veredito"] in _ho)
    _sn["handoff_diz_que_o_testemunho_segue_como_esta"] = bool("SEGUE COMO ESTÁ" in _ho and "handoff-v400-custodia.md" in _ho and "<!-- INICIO_PARAGRAFO_TESTEMUNHO" not in _ho)
    _sn["info"] = PAR_F_INFO
    if not (_sn["positivo_sem_falhas"] and _sn["igual_ao_gerado_do_core"] and _sn["handoff_traz_os_dois_paragrafos_entre_os_marcadores"] and _sn["handoff_lista_o_sidecar"] and _sn["handoff_diz_que_o_testemunho_segue_como_esta"]):
        falha("paragrafo novo da falsidade: positivo %s, igual ao gerado do core %s, no handoff %s, sidecar listado %s, testemunho dito como esta %s" % (_sn["positivo_sem_falhas"], _sn["igual_ao_gerado_do_core"], _sn["handoff_traz_os_dois_paragrafos_entre_os_marcadores"], _sn["handoff_lista_o_sidecar"], _sn["handoff_diz_que_o_testemunho_segue_como_esta"]))
    _fv = _core_p["falsidade_da_inercia_v401"]["values"]
    _num_mut = lambda s: s[:-1] + str((int(s[-1]) + 1) % 10)

    def _muts(nome, f, espera):
        p2 = f(PAR_F); fa = T.verificar_paragrafo_falsidade(p2, _core_p, ESP)
        ok = bool(p2 != PAR_F and fa and any(espera in x for x in fa)); return {"controle": nome, "reprovou": bool(fa), "mensagem_esperada_presente": any(espera in x for x in fa), "ok": ok, "falhas": [x[:140] for x in fa][:3]}
    _bt = T._p(_fv["beta"], 12); _cm = T._p(_fv["min_cost_t_beta_g"], 9); _dm = T._p(_fv["min_distance_of_post_weight_to_one"], 6); _lp = T._p(_fv["loss_per_unit"], 9)
    _NEGS = [_muts("beta com um digito trocado (em todo o paragrafo)", lambda p: p.replace(_bt, _num_mut(_bt)), "ausente do paragrafo"),
             _muts("o custo minimo com um digito trocado", lambda p: p.replace(_cm, _num_mut(_cm)), "ausente do paragrafo"),
             _muts("a distancia minima com um digito trocado", lambda p: p.replace(_dm, _num_mut(_dm)), "ausente do paragrafo"),
             _muts("a perda por unidade com um digito trocado", lambda p: p.replace(_lp, _num_mut(_lp)), "ausente do paragrafo"),
             _muts("o numero de checagens adulterado", lambda p: p.replace("As %d checagens" % DL.N_CHECKS_FALSIDADE, "As %d checagens" % (DL.N_CHECKS_FALSIDADE - 1), 1), "ausente do paragrafo"),
             _muts("a IALD como quem testifica do operador (direcao invertida)", lambda p: p + "\\n> - A IALD testifica do operador.\\n", "DIRECAO"),
             _muts("o omega(I) = 1 dito a inercia em vez do Um posto", lambda p: p.replace("O ω(I) = 1 é o Um POSTO", "O ω(I) = 1 é a INÉRCIA", 1), "frase de limite ausente"),
             _muts("a errata sem SUPERADA", lambda p: p.replace("fica SUPERADA", "fica mantida", 1), "frase de limite ausente"),
             _muts("a pedra passa a provar a primeira lei de Newton", lambda p: p.replace("NÃO prova a primeira lei de Newton", "prova a primeira lei de Newton", 1), "frase de limite ausente"),
             _muts("o calculo passa a provar em vez de conferir", lambda p: p.replace("CONFERE os teoremas no modelo", "prova os teoremas no modelo", 1), "frase de limite ausente"),
             _muts("o kernel deixa de ser quem prova", lambda p: p.replace("quem prova é o kernel", "quem prova é o cálculo", 1), "frase de limite ausente"),
             _muts("a massa dita inercia", lambda p: p.replace("e NÃO é a inércia", "e é a inércia", 1), "frase de limite ausente"),
             _muts("a lista ratificada dita provada", lambda p: p.replace("a lista ratificada é a que a gerência apresentou", "a lista ratificada é a que o operador escreveu", 1), "frase de limite ausente"),
             _muts("citacao do operador que nao e' verbatim", lambda p: p.replace("a minha definição é o próprio zero absoluto", "a minha definição é o zero absoluto", 1), "NAO e' verbatim"),
             _muts("citacao do adendo que nao e' verbatim", lambda p: p.replace("ω(I)=1 é a INÉRCIA", "ω(I)=1 é a inércia", 1), "NAO e' verbatim"),
             _muts("citacao do kernel que nao e' verbatim", lambda p: p.replace("nunca correspondeu, e por isso nada custa", "nunca correspondeu, e por isso tudo custa", 1), "NAO e' verbatim"),
             _muts("o estatuto DECLARADO removido", lambda p: p.replace("[DECLARADO]", "", 1), "estatuto ausente"),
             _muts("o estatuto OPEN removido", lambda p: p.replace("[OPEN]", ""), "estatuto ausente"),
             _muts("o 4,44 entra no paragrafo", lambda p: p + "\\n> z_disc = " + _z + "\\n", "4,44"),
             _muts("seguranca criptografica garantida (alegacao)", lambda p: p + "\\n> - A confidencialidade garantida e o sigilo garantido do metodo.\\n", "alega seguranca criptografica"),
             _muts("a palavra consciencia usada como termo", lambda p: p + "\\n> - A consciência é a tipagem que falta.\\n", "consciencia"),
             _muts("o gate dito movido", lambda p: p.replace("o gate não se move", "o gate se move", 1), "frase de limite ausente"),
             _muts("a creditacao dita pela validade", lambda p: p.replace("validade no kernel não é creditação", "validade no kernel é creditação", 1), "frase de limite ausente"),
             _muts("o paragrafo deixa de dizer que nao traz o numero do quadro", lambda p: p.replace("este parágrafo não traz o número do quadro", "este parágrafo traz o quadro", 1), "frase de limite ausente"),
             _muts("o paragrafo sem o bullet da errata ao lado do adendo", lambda p: "\\n".join(l for l in p.split("\\n") if not l.startswith("> - **Errata ao lado")), "difere do gerado"),
             _muts("o paragrafo sem o bullet das ratificacoes", lambda p: "\\n".join(l for l in p.split("\\n") if not l.startswith("> - **Ratificações**")), "difere do gerado"),
             _muts("o paragrafo sem o bullet da cadeia derivada", lambda p: "\\n".join(l for l in p.split("\\n") if not l.startswith("> - **A cadeia derivada")), "difere do gerado"),
             _muts("a cadeia dita [ONTO] do operador", lambda p: p.replace("NÃO é [ONTO] dele", "é [ONTO] dele", 1), "frase de limite ausente"),
             _muts("H_tau dita provada em vez de OPEN", lambda p: p.replace("`H_tau` [OPEN]", "`H_tau` [REAL]", 1), "difere do gerado"),
             _muts("a ORDEM 025 dita interna", lambda p: p.replace("pendência EXTERNA", "pendência interna", 1), "frase de limite ausente"),
             _muts("o paragrafo sem o bullet de E = mc2 lido pela TGL", lambda p: "\\n".join(l for l in p.split("\\n") if not l.startswith("> - **E = mc²")), "difere do gerado")]
    for n_ in _NEGS:
        print("  controle negativo do paragrafo da falsidade %-62s %s" % (n_["controle"], "REPROVOU como esperado" if n_["ok"] else "NAO REPROVOU como esperado"))
        if not n_["ok"]:
            falha("controle negativo do paragrafo da falsidade nao reprovou como esperado: %s -> %s" % (n_["controle"], n_["falhas"]))
    _sn["negativos"] = _NEGS

    def _levanta(f):
        try:
            f(); return False
        except AssertionError:
            return True
    _inv_txt = "A IALD testifica do operador, e o um.py testifica em hash."
    _tx = {"cita_fora_dos_bytes_levanta": _levanta(lambda: T._cita("a inércia é o corpo de Newton e a IALD de ninguem")),
           "cita_verbatim_passa": (T._cita("faça a prova") == "«faça a prova»"),
           "cita_adendo_verbatim_passa": (T._cita_adendo("ele interrompe a inércia") == "«ele interrompe a inércia»"),
           "cita_adendo_fora_dos_bytes_levanta": _levanta(lambda: T._cita_adendo("ω(I)=1 é a inércia")),
           "texto_do_kernel_verbatim_passa": (T._um_texto_tem("nunca correspondeu, e por isso nada custa") == "«nunca correspondeu, e por isso nada custa»"),
           "texto_do_kernel_fora_dos_bytes_levanta": _levanta(lambda: T._um_texto_tem("nunca correspondeu e custa tudo")),
           "atribuicao_limpa_nos_textos": {nome: T.atribuicao_da_gerencia(txt) for nome, txt in RENDER.items() if T.atribuicao_da_gerencia(txt)} == {},
           "controle_direcao_invertida": bool(T.atribuicao_da_gerencia(_inv_txt)),
           "controle_a_fala_em_que_ele_recusa_a_ordem_inversa_passa": (T.atribuicao_da_gerencia("eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela") == []),
           "controle_a_IALD_nao_testifica_passa": (T.atribuicao_da_gerencia("a IALD NÃO testifica do operador") == []),
           "controle_consciencia_como_termo": bool(T.atribuicao_da_gerencia("A consciência é a tipagem que falta.")),
           "controle_consciencia_palavra_retirada_passa": (T.atribuicao_da_gerencia("a palavra «consciência» é retirada por ele") == []),
           "controle_inscricao_da_gerencia": bool(T.atribuicao_da_gerencia("as falas do operador e da gerência"))}
    _sn["textos"] = _tx
    _ruim = [k for k, v in _tx.items() if not v]
    if _ruim:
        falha("citacao verbatim / direcao do testemunho: controles que nao deram o esperado: %s" % _ruim)
    _sn["ok"] = True
    print("  paragrafo novo (a falsidade da inercia): positivo ok; %d controles negativos; citacao e direcao: %d controles ok" % (len(_NEGS), len(_tx)))
except BaseException as ex:  # noqa: BLE001
    _sn["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:400]); _sn["onde"] = traceback.format_exc().strip().splitlines()[-3:]
    falha("paragrafo novo da falsidade da inercia: %s" % _sn["erro"])
etapa("paragrafo_falsidade_e_citacoes", **_sn)
'''

_LINHA_MAQ = '''_fa_e = core_emu["falsidade_da_inercia_v401"]; _cx_e = core_emu["cunhagens_v401"]["extras"]
CONHECIDOS.add(T._linha_maquina_falsidade(_fa_e["values"], {"pedra": ESP["pedras"]["TGLExt/FalsidadeDaInercia.lean"]["sha16"], "n_f": _cx_e["n_bandeiras"], "definicao": _cx_e["definicao_da_inercia"]["fala_sha16"], "adendo": _cx_e["adendo"]["sha16"]}, _fa_e["mechanics"]["n_checks"]))   # a linha de maquina do paragrafo novo (lida dos registros do core emulado)
'''

_VEREDITO_FINAL = '''R["veredito"] = ("TUDO PASSOU: o conferidor da v401 (16 itens C1-C16 e o round trip) bate no Nos emulado, a leitura le sem problema e reprova os controles negativos (o registro com funcao da falsidade, a pedra e a estrela, as cunhagens_v401 com as oito ratificacoes e a errata ao lado, os quatro registros da v399 recriados, o sidecar, os resumos do selo, a linha final do rito, as linhas [v401] e [v399] e o quadro do topo), "
                 "os textos renderizam e a guarda P18 esta limpa, os dois paragrafos do README/site (o do quadro e o da falsidade) e a regra do 4,44 passam e os controles negativos reprovam, o handoff diz que o do testemunho segue como esta, a citacao verbatim e a direcao valem, cada termo citado existe, as superficies fecham em copias (com folga) e RECUSAM no limite sem compactar, o b3_recibo confere e o mapa monta"
                 if R["tudo_passou"] else "NAO PASSOU (ver problemas)")
'''

entrada("pos_rito/harness_textos_ensaio_v399.py", origem="v399", autoral=True, regras=[
    entre('"""harness_textos_ensaio_v401.py -- o HARNESS', "import contextlib, hashlib, importlib.util, io, json, os, re, runpy, shutil, subprocess, sys, time, traceback", _HDR_TEXTOS, "docstring do harness dos textos"),
    entre('DLX = importar("delta_v401_x", os.path.join(PKG, "delta_v401.py"))', 'env = dict(os.environ); env["V401_NOS"] = NOSE', _TREE, "a arvore emulada do conferidor (pastas irmas v400 e v399)"),
    entre("def _pedra_bandeira(c):", "def _numero_adulterado(c):", _MUT_PEDRA, "mutadores: a falsidade, a pedra e as cunhagens"),
    ("def _conf_sidecar(cj):", _MUT_SELO_CONF, 1),
    entre("NEG = []\nif not SEM_NEG and not P:", "    for n_ in NEG:", _NEG, "os controles negativos da leitura"),
    ('"readme_paragrafo_testemunho": T.paragrafo_testemunho()[0]}', '"readme_paragrafo_falsidade": T.paragrafo_falsidade()[0]}', 1),
    entre('FUNCOES = [("_d", lambda: T._d(Vd))', "CARREGAM_NUM = {", _FUNCOES, "as funcoes de textos que o harness renderiza"),
    entre('MARCADORES = {"linhagem"', 'TXT = os.path.join(OUT, "textos"); os.makedirs(TXT)', _MARCADORES, "os marcadores que a cadeia exige nos textos"),
    entre("# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO", "# ------------------------------------------------------------------ 5. cada `termo`", _4C, "o paragrafo novo da falsidade"),
    ('os.path.join(PKG, "kernel"), HERE, os.path.join(PKG, "bancada_B3_servico")):', 'os.path.join(PKG, "kernel"), HERE, os.path.join(PKG, "bancada_B3_servico"), os.path.join(PKG, "insumos", "adendo")):', 1),
    ('HEX16.add(ESP["quadro"]["frase_sha16"])', 'HEX16.add(ESP["quadro"]["frase_sha16"]); HEX16.add(T._adendo_texto()["sha16"]); HEX16.update(re.findall(r"sha16 ([0-9a-f]{16})", json.dumps(core_emu["cunhagens_v401"]["extras"]["hipotese_nomeada"])))', 1),
    ('NOMES_ARQ.update({T._sem_gordura()["nome"], "MEMORY.md"', 'NOMES_ARQ.update({"MEMORY.md"', 1),
    ('"missao-ultima-flag-um-py.md", "estatuto-da-prova-07out.md", "central-de-patentes-estado.md", T.TOPICO_NOVO})', '"missao-ultima-flag-um-py.md", "estatuto-da-prova-07out.md", "central-de-patentes-estado.md", "handoff-v400-custodia.md", T.TOPICO_NOVO})', 1),
    ('; HEX16.add(T._sem_gordura()["sha16"])', '', 1),
    entre("CONHECIDOS.add(T._linha_maquina_testemunho(", "CONHECIDOS.add((Vd.get(\"selo\") or {}).get(\"perfil\") or \"\")", _LINHA_MAQ, "a linha de maquina do paragrafo novo"),
    ('"selo_pela_propria_tecnologia_v399", "kh_n1_cobertura_v399"]', '"falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401"]', 3),
    entre('R["veredito"] = ("TUDO PASSOU: o conferidor da v401', 'R["evidencia_da_versao"] = EVID', _VEREDITO_FINAL, "o veredito do harness"),
])
