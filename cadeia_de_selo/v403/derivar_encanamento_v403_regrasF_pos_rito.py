# -*- coding: utf-8 -*-
# regras (lote F) de derivar_encanamento_v403.py: a SUITE DO POS-RITO (pos_rito/): a SEMENTE mecanica da v403 sobre os arquivos FINAIS da v402 (os que rodaram no pos-rito real de 27/10/2026). ORIGEM v402 (mapa 401 -> 402 e 402 -> 403; protecao dos nomes nascidos no um.py).
# ESTA E' UMA SEMENTE: o que o pos-rito diz da v403 (handoff, README/site, Atlas, linhagem, topico de memoria, registro no Mapa de Rotas) depende do RESULTADO do rito, que a preparacao nao conhece; por isso cada arquivo que carrega narrativa recebe a linha de comentario
# `# TEXTO_A_REESCREVER_V403` (a marca da cadeia: textos, fechar e registrar_mapa RECUSAM rodar com ela; o p00 reprova enquanto ela existir em qualquer pos_rito/*.py). A gerencia reescreve a narrativa com os numeros do rito e tira as marcas.
# O que a semente JA' muda (mecanico e verificavel): os numeros de versao; os rotulos B(n) (a Bancada de producao pina a v402 em B11, deployment LIDO de C:\IALD\Bancada_Um\canonical_contracts.json [so' leitura]; o passo da v403 e' B11 -> B12); a lista de registros que os passos 3 e 9 exigem nas superficies
# (os seis registros NOVOS da v403); o cabecalho do chain (conteudo da versao lido de CANDIDATO_v403.json); o sufixo dos backups do Atlas. O RESTO (a adaptacao do fechar, das superficies, do harness e da leitura aos registros da v403, e os textos) e' da gerencia: ver o registro DERIVACAO_v403.json de pos_rito.

import json as _json_f

_MARCA_F = "# TEXTO_A_REESCREVER_V403 -- SEMENTE MECANICA da preparacao (27/10/2026): a narrativa abaixo e' a da v402 com os rotulos de versao subidos; a gerencia a reescreve com o resultado do rito e REMOVE esta linha antes de a cadeia usar o arquivo.\n"
_BANC = _json_f.load(open(os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "canonical_contracts.json"), encoding="utf-8"))   # SO' LEITURA: o numero do passo e o deployment que a Bancada pina agora
_PASSO = _BANC["sincronizacao"]["passo"]; _DEPLOY = _BANC["deployment_id"]; _VER_BANC = _BANC["canonical"]["version"]
assert _VER_BANC == "v402" and _PASSO.startswith("B") and _DEPLOY.startswith(_PASSO + "-v402-"), ("a Bancada de producao nao pina a v402 como a preparacao supoe", _VER_BANC, _PASSO, _DEPLOY)
_PROX = "B%d" % (int(_PASSO[1:]) + 1)            # o passo da v403 (B11 -> B12), calculado
_CM_F = _json_f.load(open(os.path.join(HERE, "CANDIDATO_v403.json"), encoding="utf-8"))
_NB_F, _ESC_F = _CM_F["n_bandeiras"], _CM_F["escada"]


def marca_pendente(t):
    """regra por FUNCAO (lote F): insere, logo depois da linha de codificacao, a linha de comentario da marca da cadeia (a ASSERTA: a linha de codificacao tem de ser a primeira)."""
    assert t.startswith("# -*- coding: utf-8 -*-\n"), ("o arquivo nao comeca pela linha de codificacao", t[:60])
    return "# -*- coding: utf-8 -*-\n" + _MARCA_F + t[len("# -*- coding: utf-8 -*-\n"):]


_MP = (marca_pendente, "marca de narrativa pendente (TEXTO_A_REESCREVER_V403)", 1)

_CHAIN_HDR = ('''# v403 (27/10): CADEIA POS-RITO -- SEMENTE MECANICA da preparacao (derivar_encanamento_v403.py, lote F) sobre o chain_pos_rito_v402.sh FINAL (a cadeia de CONTEUDO que rodou em 27/10; mesma ordem de passos 0..14 e mesmos portoes), com as licoes da v402 (o sidecar entra na custodia, a conferencia traz C15 e C16, as guardas estaticas da Bancada)
# e o passo da FILA DA MEMORIA (abaixo). A gerencia a adapta A MAO (narrativa, vereditos esperados e os arquivos marcados com TEXTO_A_REESCREVER_V403) antes do pos-rito. O rito (rito_v403.sh) AINDA NAO rodou (RITO_RC=<rc> no fim do Nos\\rodada_v403_stdout.txt).
# A v403 e' uma versao de CONTEUDO (os nomes do operador, 27/10/2026, e a F8.1): TRES modulos novos de kernel (TGLExt/Caminho, TGLExt/Vida, TGLExt/VerdadeAdendo; %d bandeiras novas; escada %d -> %d; h8 lido de ESPERADOS_v403.json),
# QUATRO registros COM FUNCAO (caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403; lidos no main logo DEPOIS da esperanca_condicional_v402) e DOIS registros por spec (cunhagens_v403: as 2 falas do operador de 27/10 verbatim por sha256, as erratas E5 e E6 em nome da gerencia c1, as decisoes D17 a D22 e a leitura [ONTO] da tripla espectral;
# e kh_n1_cobertura_v403). A F8.1: as tres bandeiras literais do gate (linearized_spin2_finite_face, protocol_pre_registered, null_tests_passed_blind) passam a CALCULADAS; a letra do veredito do gate NAO muda. Os registros da v402, da v401 e da v399 sao RECRIADOS pelo rito (selos iguais ao ensaio a seco) e o SIDECAR um_absoluto_selo_acom.json e' REESCRITO
# (depois da ultima escrita do selo). O QUADRO «O Teste da Unica Palavra» (v397, a regra do 4,44) PERMANECE no topo do artigo e do .md, INTOCADO: o conferidor e a leitura o conferem de novo; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item) segue valendo em TODO texto que o cite. O paragrafo do testemunho de dois (v399) SEGUE COMO ESTA.
# Estatutos: Caminho, Vida e o adendo da Verdade sao [DERIVED] por citacao e composicao de termos de kernel (o teorema novo the_name_reads_the_inscription_as_weights e' [REAL]); a F8.1 e' [REAL] no codigo e no rito; a independencia das 4 experimentais do gate NAO e' resolvida [DECLARADO, GV-03]; a leitura pela tripla espectral e' [ONTO]; o gate nao se move.
''' % (_NB_F, _ESC_F[0], _ESC_F[1])).replace("\\\\", "\\")

entrada("pos_rito/b3_recibo_v402.py", autoral=True, regras=[
    ("Passo simples (a Bancada de producao pina a v402, B10, deployment B10-v402-20261025-R1, e o Nos passou a v403; o rito grava a geracao B11 --",
     "Passo simples (a Bancada de producao pina a v402, %s, deployment %s, e o Nos passou a v403; o rito grava a geracao %s --" % (_PASSO, _DEPLOY, _PROX), 1),
])
entrada("pos_rito/superficies_v402.py", autoral=True, regras=[])
entrada("pos_rito/fila_memoria_v402.py", autoral=True, regras=[])
entrada("pos_rito/montar_textos_v402.py", autoral=True, regras=[])
entrada("pos_rito/fechar_v402.py", autoral=True, regras=[_MP])
entrada("pos_rito/textos_v402.py", autoral=True, regras=[_MP])
entrada("pos_rito/registrar_mapa_v402.py", autoral=True, regras=[_MP])
entrada("pos_rito/leitura_v402.py", autoral=True, regras=[_MP])
entrada("pos_rito/harness_textos_ensaio_v402.py", autoral=True, regras=[_MP])
entrada("pos_rito/harness_fechar_sandbox_v402.py", autoral=True, regras=[
    ("com as licoes da v403 (a ponte, a queda, a esperanca; o passo simples B10 -> B11).", "com as licoes da v403 (o caminho, a vida, o adendo da verdade e as bandeiras do gate; o passo simples %s -> %s)." % (_PASSO, _PROX), 1),
    ("passo SIMPLES B10 (v402) -> B11 (v403)", "passo SIMPLES %s (v402) -> %s (v403)" % (_PASSO, _PROX), 1),
    ("passo SIMPLES B10 -> B11 com recibos SINTETICOS", "passo SIMPLES %s -> %s com recibos SINTETICOS" % (_PASSO, _PROX), 1),
    ("o b3_recibo confere o passo simples B10 -> B11;", "o b3_recibo confere o passo simples %s -> %s;" % (_PASSO, _PROX), 1),
])
entrada("pos_rito/chain_pos_rito_v402.sh", autoral=True, regras=[
    entre("# v403 (26/10): CADEIA POS-RITO", "# ORDEM: 0 guardas", _CHAIN_HDR, "cabecalho do chain (semente da v403)"),
    ('REGS="ponte_da_escala_dual_v402 queda_sem_geometria_v402 esperanca_condicional_v402 cunhagens_v402 kh_n1_cobertura_v402"', 'REGS="caminho_v403 vida_v403 verdade_adendo_v403 bandeiras_do_gate_v403 cunhagens_v403 kh_n1_cobertura_v403"', 1),
    ("a Bancada de producao JA pina a v402 (B10, B10-v402-20261025-R1)", "a Bancada de producao JA pina a v402 (%s, %s)" % (_PASSO, _DEPLOY), 1),
    ("Bancada pina + 1 (B10 -> n = 11;", "Bancada pina + 1 (%s -> n = %s;" % (_PASSO, _PROX[1:]), 1),
    ("(PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) tem declaracoes nomeadas", "(Caminho, Vida, VerdadeAdendo) tem declaracoes nomeadas", 1),
    ("exigem os marcadores da v403 (os cinco registros novos)", "exigem os marcadores da v403 (os seis registros novos)", 1),
    ('%Y%m%d_%H%M%S)_v402"', '%Y%m%d_%H%M%S)_v403"', 1),
])
_DOC_GD = r'''"""gerar_derivacao_pos_rito_v403.py -- REGISTRA (SO' LE; nao deriva, nao sobrescreve nada) a proveniencia dos scripts do pos_rito da v403.
Na v403 a suite do pos_rito e' a SEMENTE mecanica de derivar_encanamento_v403.py (lote F) sobre o arquivo FINAL da cadeia v402 (o que foi USADO no pos-rito real de 27/10/2026): o numero de versao subido por script (401 -> 402 e 402 -> 403, com a protecao dos nomes nascidos no um.py), mais as regras do lote F (os rotulos B(n), a lista de registros do chain,
o cabecalho do chain, o sufixo dos backups do Atlas e a marca TEXTO_A_REESCREVER_V403 nos arquivos de narrativa). A ADAPTACAO A MAO (o que o pos-rito diz da v403, com os numeros do rito) e' da gerencia e AINDA NAO foi feita: os arquivos marcados RECUSAM rodar ate a marca sair.
Este script apenas recalcula, em MEMORIA e com o proprio motor (derivar_v403_motor.bump), a semente PURA de cada arquivo (so' o mapa de versoes) e a compara com o arquivo atual.
Para cada arquivo do pos_rito que tem origem na v402 grava o sha256 da origem, o da semente pura (recalculada agora), o do arquivo atual, o estado (SEMENTE_PURA | DIFERE_DA_SEMENTE_PURA: regras do lote F ou edicao a mao) e o tamanho do diff (linhas trocadas); os que nao tem origem (escritos de novo) ficam listados como tais.
Escreve so' pos_rito/DERIVACAO_v403.json (com backup de bytes do anterior). NUNCA executa nenhum dos scripts; so' ast.parse. Uso: python -I -B -X utf8 gerar_derivacao_pos_rito_v403.py   (rc 0 = gravou; rc 1 = algum arquivo sem origem lida ou com sintaxe invalida)"""
'''
entrada("pos_rito/gerar_derivacao_pos_rito_v402.py", autoral=True, regras=[
    ("B10 -> B11", "%s -> %s" % (_PASSO, _PROX), 1),
    ('("fila_memoria_v403.py", None, "A1 (ARQUIVO NOVO): as operacoes', '("fila_memoria_v403.py", "fila_memoria_v402.py", "A1 (arquivo novo na v402; semente na v403): as operacoes', 1),
    entre('"""gerar_derivacao_pos_rito_v403.py', "import ast, difflib, hashlib, json, os, sys, time", _DOC_GD, "docstring do registro do pos_rito"),
    ('r["estado"] = "SEMENTE_INTACTA"', 'r["estado"] = "SEMENTE_PURA"', 1),
    ('r["estado"] = "EDITADO_A_MAO_SOBRE_A_SEMENTE"', 'r["estado"] = "DIFERE_DA_SEMENTE_PURA__regras_do_lote_F_ou_edicao_a_mao"', 1),
    ('"origem": "pos_rito da v402 FINAL (a cadeia usada no rito real de 25/10), mapa 400 -> 402 e 402 -> 403 por script (semente); depois EDITADO A MAO, arquivo por arquivo (a gerencia mandou nao regerar com derivar_encanamento_v403)",',
     '"origem": "pos_rito da v402 FINAL (a cadeia usada no pos-rito real de 27/10), mapa 401 -> 402 e 402 -> 403 por script (semente pura) mais as regras do lote F de derivar_encanamento_v403.py; a adaptacao a mao e\' da gerencia e AINDA nao foi feita",', 1),
])
