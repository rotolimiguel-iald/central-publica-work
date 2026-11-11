# -*- coding: utf-8 -*-
"""_adapt_d72_delta_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410, a servico da gerencia c1): adapta delta_v410.py ao AO LADO das DECISOES de 09/11 do DESENHO_v410 (D72 a D75):
as falas 12 (09/11, as decisoes e a ratificacao dos nomes, inteira) e 13 (08/11, as tres copias do ACOM, so' o trecho); as decisoes D72 (o registro pre-registrado H0DN x BG1), D73 (o treino junto), D74 (os nomes
RATIFICADOS: os textos passam a dize-lo; as docstrings da pedra nao mudam), D75 (as tres copias do ACOM); as frases da obrigacao e da moldura do H0DN. Trocas EXATAS com contagem conferida; backup de bytes; tmp -> conferir -> substituir; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "delta_v410.py")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b0 = open(P, "rb").read()
assert b0.count(b"\r\n") == 0, "delta_v410.py era LF; agora tem CRLF: parar"
bk = P + ".bak_" + TS + "_d72"
open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
t = b0.decode("utf-8")

TROCAS = [
    # (a) as falas 12 e 13
    ('N_CREDITOS = "OPERADOR_09nov_creditos_voltaram_v410_completa_teste_5sigma_qwen_pausar_treino_verbatim.txt"   # (o AO LADO de 09/11: a 11a fala, a ORDEM da retomada; so\' o trecho da retomada e\' citado, o resto e\' operacional)\n',
     'N_CREDITOS = "OPERADOR_09nov_creditos_voltaram_v410_completa_teste_5sigma_qwen_pausar_treino_verbatim.txt"   # (o AO LADO de 09/11: a 11a fala, a ORDEM da retomada; so\' o trecho da retomada e\' citado, o resto e\' operacional)\n'
     'N_RATIFICA = "OPERADOR_09nov_concordo_teste_v410_ordem_ao_kimi_ratifico_os_nomes_treino_acom_fila_verbatim.txt"   # (o AO LADO das DECISOES de 09/11: a 12a fala, inteira; D72 a D75; os nomes RATIFICADOS, D74)\n'
     'N_TRES_COPIAS = "OPERADOR_08nov_acom_so_as_tres_copias_mais_recentes_verbatim.txt"   # (a 13a fala, de 08/11, registrada pela sessao de custodia com a fala dele entre aspas: so\' o trecho das tres copias; D75)\n', 1),
    ('N_SELETOR, N_ATRATOR, N_CREDITOS)   # as ONZE falas: as oito do DESENHO_v410 §3, a do AO LADO de 06/11 (o seletor) e as duas do AO LADO de 09/11 (o atrator, de 07/11; a ordem da retomada, de 09/11); fala que chegar DEPOIS fica fora\n',
     'N_SELETOR, N_ATRATOR, N_CREDITOS, N_RATIFICA, N_TRES_COPIAS)   # as TREZE falas: as oito do DESENHO_v410 §3, a do AO LADO de 06/11 (o seletor), as duas do AO LADO da retomada de 09/11 (o atrator, de 07/11; a ordem da retomada) e as duas do AO LADO das decisoes de 09/11 (as decisoes e a ratificacao dos nomes, inteira; as tres copias do ACOM, de 08/11, so\' o trecho); fala que chegar DEPOIS fica fora\n', 1),
    ('for _m in re.finditer(r"`(OPERADOR_0[679]nov_[A-Za-z0-9_]+_verbatim\\.txt)`[^`\\n]{0,40}`([0-9a-f]{16})`", _DESENHO_TXT):   # (06, 07 e 09/11: o DESENHO e os seus AO LADO)',
     'for _m in re.finditer(r"`(OPERADOR_0[6789]nov_[A-Za-z0-9_]+_verbatim\\.txt)`[^`\\n]{0,40}`([0-9a-f]{16})`", _DESENHO_TXT):   # (06 a 09/11: o DESENHO e os seus AO LADO)', 1),
    ('VERBATIM_PAPEL["operador, so\' o trecho (a ordem da retomada, 09/11)"] = "fala do operador de que se embute e cita SO\' a frase da retomada da v410 (o AO LADO de 09/11 do DESENHO); o resto da fala e\' operacional e entra so\' por sha256 (nao e\' embutido nem publicado)"\n',
     'VERBATIM_PAPEL["operador, so\' o trecho (a ordem da retomada, 09/11)"] = "fala do operador de que se embute e cita SO\' a frase da retomada da v410 (o AO LADO de 09/11 do DESENHO); o resto da fala e\' operacional e entra so\' por sha256 (nao e\' embutido nem publicado)"\n'
     'VERBATIM_PAPEL["operador, so\' o trecho (as tres copias do ACOM, 08/11)"] = "fala do operador de que se embute e cita SO\' a frase das tres copias do ACOM (D75); o arquivo de origem e\' registro da sessao de custodia com a fala dele entre aspas e entra so\' por sha256 (nao e\' embutido nem publicado)"\n', 1),
    ('TRECHO_RETOMADA = "chegou a hora de voltarmos com tudo para confeccionarmos a versão 410 completa do um.py"   # (a ordem de 09/11, AO LADO do DESENHO: so\' este trecho e\' citado; o resto da fala e\' operacional)\n',
     'TRECHO_RETOMADA = "chegou a hora de voltarmos com tudo para confeccionarmos a versão 410 completa do um.py"   # (a ordem de 09/11, AO LADO do DESENHO: so\' este trecho e\' citado; o resto da fala e\' operacional)\n'
     'TRECHO_TRES_COPIAS = "as únicas cópias que merecem ser mantidas são  as três mais recentes que acumulam tudo, as demais tornam-se desncessárias"   # (08/11, D75; com o espaco duplo e a grafia do original)\n', 1),
    ('                        N_CREDITOS: ("meio", TRECHO_RETOMADA, "so\' a frase da retomada da v410 (o AO LADO de 09/11 do DESENHO): o resto da fala e\' operacional e fica fora dos textos do um.py")}\n'
     'VERBATIM_SO_O_TRECHO_PAPEL = {N_SOLUCAO: "operador, so\' o trecho (D65)", N_CREDITOS: "operador, so\' o trecho (a ordem da retomada, 09/11)"}\n'
     'TEXTO_EMBUTIDO_SO_TRECHO = {N_SOLUCAO: "so\' o trecho que a D65 deixa entrar (o nome do algoritmo); o arquivo inteiro entra so\' por sha256",\n'
     '                            N_CREDITOS: "so\' a frase da retomada da v410 (o AO LADO de 09/11); o arquivo inteiro entra so\' por sha256"}\n',
     '                        N_CREDITOS: ("meio", TRECHO_RETOMADA, "so\' a frase da retomada da v410 (o AO LADO de 09/11 do DESENHO): o resto da fala e\' operacional e fica fora dos textos do um.py"),\n'
     '                        N_TRES_COPIAS: ("meio", TRECHO_TRES_COPIAS, "so\' a frase das tres copias do ACOM (D75): o resto do arquivo e\' o registro da sessao de custodia e fica fora dos textos do um.py")}\n'
     'VERBATIM_SO_O_TRECHO_PAPEL = {N_SOLUCAO: "operador, so\' o trecho (D65)", N_CREDITOS: "operador, so\' o trecho (a ordem da retomada, 09/11)", N_TRES_COPIAS: "operador, so\' o trecho (as tres copias do ACOM, 08/11)"}\n'
     'TEXTO_EMBUTIDO_SO_TRECHO = {N_SOLUCAO: "so\' o trecho que a D65 deixa entrar (o nome do algoritmo); o arquivo inteiro entra so\' por sha256",\n'
     '                            N_CREDITOS: "so\' a frase da retomada da v410 (o AO LADO de 09/11); o arquivo inteiro entra so\' por sha256",\n'
     '                            N_TRES_COPIAS: "so\' a frase das tres copias do ACOM (D75); o arquivo inteiro (registro da sessao de custodia) entra so\' por sha256"}\n', 1),
    ('DATA_DA_FALA.update({N_ATRATOR: "07/11/2026", N_CREDITOS: "09/11/2026"})\n',
     'DATA_DA_FALA.update({N_ATRATOR: "07/11/2026", N_CREDITOS: "09/11/2026", N_RATIFICA: "09/11/2026", N_TRES_COPIAS: "08/11/2026"})\n', 1),
    ('VERBATIM_QUANDO_V410 = "06, 07 e 09/11/2026 (o ACOM e\' a segunda quantizacao; a particula e\' o codigo e o funtor o leitor; o nome do algoritmo; nomear o kernel de IALD; o NOME IALD2; a pedra e\' o enunciado; a forma da luz; a ORDEM da v410 e o signo; a IALD e\' a instanciacao do seletor; o atrator: o Nome nao esgota o ser; a ORDEM da retomada da v410)"\n',
     'VERBATIM_QUANDO_V410 = "06, 07, 08 e 09/11/2026 (o ACOM e\' a segunda quantizacao; a particula e\' o codigo e o funtor o leitor; o nome do algoritmo; nomear o kernel de IALD; o NOME IALD2; a pedra e\' o enunciado; a forma da luz; a ORDEM da v410 e o signo; a IALD e\' a instanciacao do seletor; o atrator: o Nome nao esgota o ser; a ORDEM da retomada da v410; as decisoes de 09/11 e a ratificacao dos nomes; as tres copias do ACOM)"\n', 1),
    ('FRASE_RETOMADA = TRECHO_RETOMADA\n',
     'FRASE_RETOMADA = TRECHO_RETOMADA\n'
     '# a 12a fala (09/11/2026, inteira: as decisoes e a ratificacao dos nomes, D72 a D75) e a 13a (08/11/2026, so\' o trecho das tres copias, D75)\n'
     'FRASE_RATIFICO = "os nomes dos teoremas ratifico-os todos"\n'
     'FRASE_CONCORDO_TESTE = "quanto ao teste da v410 concordo com tudo que vc falou, pode dar a ordem ao kimi k3pro"\n'
     'FRASE_TREINO = "o treino concordo com sua proposta"\n'
     'FRASE_APROVO_ACOM = "aprovo o pedido da remoção das cópias desnecessárias do ACOM, pode fazê-lo"\n'
     'FRASE_TRES_COPIAS = TRECHO_TRES_COPIAS\n', 1),
    ('(N_ATRATOR, FRASE_ISSO_E_O_ATRATOR), (N_CREDITOS, FRASE_RETOMADA)]\n',
     '(N_ATRATOR, FRASE_ISSO_E_O_ATRATOR), (N_CREDITOS, FRASE_RETOMADA),\n'
     '               (N_RATIFICA, FRASE_RATIFICO), (N_RATIFICA, FRASE_CONCORDO_TESTE), (N_RATIFICA, FRASE_TREINO), (N_RATIFICA, FRASE_APROVO_ACOM), (N_TRES_COPIAS, FRASE_TRES_COPIAS)]\n', 1),
    ('== len(VERBATIM_SO_O_TRECHO) == 2, "as onze falas (N_FALAS_V410), duas com so\' o trecho (a da D65; a ordem de 09/11), nenhuma repetida"\n',
     '== len(VERBATIM_SO_O_TRECHO) == 3, "as treze falas (N_FALAS_V410), tres com so\' o trecho (a da D65; a ordem de 09/11; as tres copias de 08/11), nenhuma repetida"\n', 1),
    # (b) D74: os nomes RATIFICADOS (os textos passam a dize-lo; as docstrings da pedra, da epoca, nao mudam)
    ('"a_iald_e_o_seletor_luminodinamico, o_atrator e os demais) sao da gerencia c1 e ficam [DECLARADO] ate a ratificacao (D63)" % (_H_NOME, FRASE_NOME_IALD2))}\n',
     '"a_iald_e_o_seletor_luminodinamico, o_atrator e os demais) sao da gerencia c1, RATIFICADOS pelo operador em 09/11/2026 («%s», sha16 %s; D74); as docstrings da pedra dizem [DECLARADO] ate a ratificacao, verdade da epoca da pedra (D63)" % (_H_NOME, FRASE_NOME_IALD2, FRASE_RATIFICO, VERBATIM_PREFIXOS_DA_ORDEM_V410[N_RATIFICA]))}\n', 1),
    ('NOME_DO_OPERADOR = NOMES_DAS_PEDRAS                             # (o nome dos scripts bumpados; na v410 o nome do MODULO e\' do operador e os das declaracoes sao da gerencia, [DECLARADO] ate a ratificacao: D63)\n',
     'NOME_DO_OPERADOR = NOMES_DAS_PEDRAS                             # (o nome dos scripts bumpados; na v410 o nome do MODULO e\' do operador e os das declaracoes sao da gerencia, RATIFICADOS por ele em 09/11: D74)\n'
     'NOMES_RATIFICADOS = True                                        # D74 (09/11/2026): «os nomes dos teoremas ratifico-os todos» cobre TODAS as declaracoes da IALD2 (secoes 1 a 6)\n'
     'FRASE_NOMES_RATIFICADOS_PT = "os nomes das declarações são da gerência c1, ratificados pelo operador em 09/11/2026 («%s», D74); as docstrings da pedra, da época, dizem [DECLARADO] até a ratificação e não mudam" % FRASE_RATIFICO\n'
     'FRASE_NOMES_RATIFICADOS_EN = "the names of the declarations are the management\'s (c1), ratified by the operator on 09/11/2026 (D74); the docstrings of the stone, of their time, say [DECLARADO] until ratification and do not change"\n', 1),
    ('    "o_nome_iald2": "«%s» [INPUT; a fala inteira]: o NOME do modulo e\' do operador; o espelho do nome e\' termo: iald_ao_quadrado (Pi·Pi = Pi), reler_o_par_nao_acrescenta, o_par_lido_le_um; os nomes das declaracoes sao da gerencia, [DECLARADO] ate a ratificacao (D63)" % FRASE_NOME_IALD2,\n',
     '    "o_nome_iald2": "«%s» [INPUT; a fala inteira]: o NOME do modulo e\' do operador; o espelho do nome e\' termo: iald_ao_quadrado (Pi·Pi = Pi), reler_o_par_nao_acrescenta, o_par_lido_le_um; os nomes das declaracoes sao da gerencia, RATIFICADOS pelo operador em 09/11/2026 (D74; D63 e\' a decisao da epoca)" % FRASE_NOME_IALD2,\n', 1),
    ('    "a_ordem_da_retomada": "«%s» [INPUT; so\' este trecho da ordem de 09/11]: a ordem da retomada da v410 (os creditos de volta); o resto da fala e\' operacional e nao entra em texto do um.py (o que dele for objeto de decisao vai em AO LADO proprio)" % FRASE_RETOMADA,\n',
     '    "a_ordem_da_retomada": "«%s» [INPUT; so\' este trecho da ordem de 09/11]: a ordem da retomada da v410 (os creditos de volta); o resto da fala e\' operacional e nao entra em texto do um.py (o que dele for objeto de decisao vai em AO LADO proprio)" % FRASE_RETOMADA,\n'
     '    "a_ratificacao_dos_nomes": "«%s» [INPUT; a 12a fala, inteira, 09/11]: os nomes de TODAS as declaracoes da IALD2 (secoes 1 a 6), dados pela gerencia c1, ficam RATIFICADOS pelo operador (D74); as docstrings da pedra, da epoca, dizem [DECLARADO] ate a ratificacao e nao mudam" % FRASE_RATIFICO,\n'
     '    "as_decisoes_de_09nov": "«%s»; «%s»; «%s» [INPUT; a 12a fala]: o teste H0DN x BG1 entra PRE-REGISTRADO nesta versao (D72: a ordem ao Kimi e\' da gerencia; pré-registrado; nenhum dado observado lido); o treino do Qwen3.8 corre junto com a cadeia (D73); as copias do ACOM alem das tres mais novas sao descartadas (D75)" % (FRASE_CONCORDO_TESTE, FRASE_TREINO, FRASE_APROVO_ACOM),\n'
     '    "as_tres_copias_do_acom": "«%s» [INPUT; so\' o trecho da fala de 08/11, registrada pela sessao de custodia]: a regra das tres copias do banco da memoria ACOM (D75); nao e\' checagem numerica do um.py" % FRASE_TRES_COPIAS,\n', 1),
    # (c) as decisoes D72 a D75 e a D63 com o seu AO LADO
    ('            "sao da gerencia e ficam [DECLARADO] ate a ratificacao; ditos assim em todo texto [decisao da gerencia c1, 06/11/2026]" % (_H_NOME, FRASE_NOME_IALD2)),\n',
     '            "sao da gerencia e ficam [DECLARADO] ate a ratificacao; ditos assim em todo texto [decisao da gerencia c1, 06/11/2026] (AO LADO, 09/11: a ratificacao veio em 09/11/2026, D74; os textos passam a dize-la; as docstrings da pedra nao mudam)" % (_H_NOME, FRASE_NOME_IALD2)),\n', 1),
    ('            + "; a IALD2 nao muda mais nesta versao salvo ordem do operador [decisao da gerencia c1, 09/11/2026, AO LADO do DESENHO]"),\n'
     '})\n'
     'DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71")\n',
     '            + "; a IALD2 nao muda mais nesta versao salvo ordem do operador [decisao da gerencia c1, 09/11/2026, AO LADO do DESENHO]"),\n'
     '    "D72": ("o REGISTRO PRE-REGISTRADO H0DN x BG1, o segundo registro com FUNCAO desta versao (core[h0dn_bg1_v410], chamado no main logo depois de iald2_v410; TAG H0DN_BG1): o teste da razao de Hubble local/fundo (desenho do Codex astra-bell de 06/11, congelado ANTES de qualquer "\n'
     '            "olhar no dado: FREEZE_R2.json, 9 pinos; leitura da gerencia em LEITURA_DOSSIE_5SIGMA_09nov.json) entra pré-registrado; nenhum dado observado lido: nulo H_local/H_fundo = 1; alternativa TGL K = E(z*)^(2 beta/3), com beta = alfa sqrt e em runtime e z*, Omega_m, Omega_r LIDOS da "\n'
     '            "funcao congelada da Fase 9 ja\' no um.py; estatistica Z = (h_hat - log10 H_bg)/sigma_nulo, unilateral, limiar 5; dois modelos (o publicado; o vies diferencial Cefeida livre), nenhum selecionado; os insumos embutidos em base64 e pinados por sha256 lido (estimator_frozen.npz, "\n'
     '            "BG1.json, analysis_plan.json, FREEZE_R2.json, estimator.py, ENTREGA_H0DN_BG1.json; network.npz so\' pinado pelo FREEZE_R2); 12 checagens: os pinos, K e log10 K recomputados de beta, sd_null e sd_tgl reproduzidos do npz, D esperado e o poder analitico conferidos contra a ENTREGA "\n'
     '            "(o poder MC dentro do IC95 dela: conferencia, nao recalculo), a FUNCAO DE VEREDITO CONGELADA veredito_h0dn (INCONCLUSIVE_SYSTEMATICS enquanto a covariancia fisica nao fecha, G3/G4; NOT_FALSIFIED_POWERED, FALSIFIED_AT_SENSITIVITY, NOT_DISCRIMINATED_AT_SENSITIVITY, TENSION_WITH_BOTH) "\n'
     '            "com o sha256 do texto-fonte no registro e 4 vetores deterministicos, observed_vector_read = False (nenhum arquivo observado e\' procurado nesta versao), a guarda (FIVE_SIGMA_OBSERVED, DETECTED, H0DN_CONFIRMS e as frases de 5 sigma atingido proibidos; a aritmetica do agregado "\n'
     '            "publico nao entra em texto), o gate, a rota Kimi espectro x fotometria como NOT_TESTABLE (nao e\' o teste), a regra conjunta congelada e o texto; o que falta (y_obs pelo codigo upstream; a covariancia fisica sem duplicar Cefeida; os IDs) e a ORDEM ao Kimi ficam no spec h0dn_bg1_v410; "\n'
     '            "a ressalva da novidade de uso: o agregado publico e\' conhecido desde out/2025, K nao tem parametro ajustado e o PRE-REGISTRO nesta versao selada e\' o que vale (lei da prova, 05/10); o poder e\' prospectivo e sintetico; a abertura e\' de versao futura, com a covariancia fisica fechada "\n'
     '            "[decisao da gerencia c1, 09/11/2026, AO LADO do DESENHO; a fala do operador: «%s»]" % FRASE_CONCORDO_TESTE),\n'
     '    "D73": ("o treino do Qwen3.8 (CPU, 48 threads, sem GPU) corre JUNTO com a cadeia: o lancador so\' para o servidor da nativa e o trabalhador do pilar quantico; os processos treinar.py/campanha.py nao se tocam; o teto do S4 (5 h) decide: se estourar, a gerencia pausa o treino PELO PID medido "\n'
     '            "(checkpoint a cada passo), roda, e retoma por campanha.py retomar; a duracao do build, do Audit e do rito e\' registrada para medir a contencao [decisao da gerencia c1, 09/11/2026; a fala do operador: «%s»]" % FRASE_TREINO),\n'
     '    "D74": ("NOMES RATIFICADOS: «%s» (a 12a fala, 09/11/2026) cobre TODAS as declaracoes da IALD2 (secoes 1 a 6); as docstrings da pedra nao mudam (dizem [DECLARADO] ate a ratificacao, verdade da epoca); o registro cunhagens_v410 e os textos dizem que a ratificacao aconteceu em 09/11 "\n'
     '            "[decisao da gerencia c1, 09/11/2026]" % FRASE_RATIFICO),\n'
     '    "D75": ("a regra das TRES COPIAS do ACOM no codigo: por ordem de 08/11 («%s»; a 13a fala, so\' o trecho) e aprovacao de 09/11 («%s»), snapshots.py passou a DESCARTAR as copias alem das 3 mais novas, conferindo o sha256 das que ficam antes de apagar; nada mais vai ao D:; as 485 copias "\n'
     '            "ja\' no D: nao foram tocadas (decisao do operador); entra no spec cunhagens_v410 por sha; nao e\' checagem numerica do um.py [decisao da gerencia c1, 09/11/2026]" % (FRASE_TRES_COPIAS, FRASE_APROVO_ACOM)),\n'
     '})\n'
     'DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73", "D74", "D75")\n', 1),
    # (d) as frases do H0DN (D72): a obrigacao onde «H0DN» aparecer e a moldura
    ('FRASE_D71_EN = (',
     'FRASE_H0DN_OBRIGATORIA_PT = "pré-registrado; nenhum dado observado lido"   # D72: OBRIGATORIO onde «H0DN» aparecer\n'
     'FRASE_H0DN_OBRIGATORIA_EN = "pre-registered; no observed data read"\n'
     'FRASE_DA_MOLDURA_H0DN_PT = "pré-registrado nesta versão selada; poder prospectivo sintético de 96,6 % e 62,5 %; nenhum vetor observado lido; a abertura é de versão futura, com a covariância física fechada"\n'
     'FRASE_DA_MOLDURA_H0DN_EN = "pre-registered in this sealed version; synthetic prospective power 96.6% and 62.5%; no observed vector read; the opening belongs to a future version, with the physical covariance closed"\n'
     'FRASE_D71_EN = (', 1),
]
for velho, novo, n in TROCAS:
    c = t.count(velho)
    assert c == n, ("troca nao casou %d vez(es) (achou %d)" % (n, c), velho[:140])
    t = t.replace(velho, novo)
linhas = t.split("\n")
assert linhas[2].startswith("# [ADAPTADO v410, 09/11/2026"), linhas[2][:80]
linhas.insert(3, "# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_d72_delta_v410.py: as falas 12 (as decisoes de 09/11 e a ratificacao dos nomes, inteira) e 13 (as tres copias do ACOM, 08/11, so' o trecho); D72 (o registro pre-registrado H0DN x BG1), D73, D74 (nomes RATIFICADOS: os textos o dizem), D75; as frases da obrigacao e da moldura do H0DN")
t = "\n".join(linhas)
nb = t.encode("utf-8")
ast.parse(nb)
tmp = P + ".tmp_" + TS
open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb)
os.replace(tmp, P)
assert open(P, "rb").read() == nb
print("delta_v410.py adaptado (D72-D75):", len(b0), "->", len(nb), "B | sha16", hashlib.sha256(nb).hexdigest()[:16], "| backup", os.path.basename(bk), "| trocas", len(TROCAS))
