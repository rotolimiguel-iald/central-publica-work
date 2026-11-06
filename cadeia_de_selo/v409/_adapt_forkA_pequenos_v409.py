# -*- coding: utf-8 -*-
"""_adapt_forkA_pequenos_v409.py -- (claude-construtor-v409, fork A, 05/11/2026) adapta os arquivos PEQUENOS do pos_rito (subida mecanica da v408) a v409, A TRADUCAO AS CLASSES DE TURING:
b3_recibo, fila_memoria e superficies (genericos: so' os cabecalhos que descreviam o conteudo da v408), chain_pos_rito (cabecalho, REGS e o sufixo do backup do inventario) e gerar_derivacao_pos_rito (cabecalho e SUITE).
Trocas por LINHA com o prefixo conferido (aborta se nao casar) e trocas de texto com contagem exata (_adapt_util_v409.Arq: CRLF preservado, backup de BYTES, temporario -> tamanho -> substituicao)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

MARCA = "# [ADAPTADO v409, 05/11/2026, claude-construtor-v409 (fork A), a servico da gerencia c1] "
CONTEUDO = ("A v409 = A TRADUCAO AS CLASSES DE TURING (ordem do operador de 05/11/2026: «Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados»): UM modulo novo em TGLExt/ (TraducaoTuring, nome da gerencia ratificado pelo operador), "
            "o registro com funcao traducao_turing_v409 e os dois por spec (cunhagens_v409, kh_n1_cobertura_v409); P = nP e' teorema da TGL no modo selecao, relativo ao leitor, e a maquina sem leitor fica fora; nenhuma chave antiga muda; erratas E24 a E26 ao lado")


def linhas(a, troca):
    """troca {n_linha (1-based): (prefixo_esperado, texto_novo | None para apagar)} sobre a.t (LF)."""
    ls = a.t.split("\n")
    for n in sorted(troca, reverse=True):
        pref, novo = troca[n]
        assert ls[n - 1].startswith(pref), (os.path.basename(a.p), n, ls[n - 1][:120])
        if novo is None:
            del ls[n - 1]
        else:
            ls[n - 1] = novo
    a.t = "\n".join(ls)


# ---------------------------------------------------------------- b3_recibo (generico)
a = Arq("pos_rito/b3_recibo_v409.py")
linhas(a, {2: ("# [A ADAPTAR v409]", MARCA + "molde v408/pos_rito/b3_recibo_v408.py (rotulos subidos por _bump_copia_v409.py; diff em bump/); o corpo e' GENERICO e foi conferido linha a linha: confere so' o recibo do B(n) (versao alvo v409, fase pos_selo, bateria, B<n> = geracao do recibo + 1, deployment B<n>-v409-)."),
           3: ("# [ADAPTADO v409, 04/11/2026, claude-construtor-v409 (fork B)]", None),
           4: ("# A v409 = Tetelestai e' o terminal", "# " + CONTEUDO + ". Nada disso vem daqui: vem do candidato e dos ESPERADOS; o B(n) da v409 e' B18 (a v408 pinou B17; DESENHO_v409), lido do recibo, nunca digitado.")})
a.grava()

# ---------------------------------------------------------------- fila_memoria (generico)
a = Arq("pos_rito/fila_memoria_v409.py")
linhas(a, {2: ("# [A ADAPTAR v409]", MARCA + "sobre a subida mecanica de rotulo da v408 FINAL (_bump_copia_v409.py): este arquivo e' GENERICO (a fila da memoria: guardas, pausa, pinar, verificar) e nao traz nada do conteudo do bundle; conferido linha a linha: so' rotulos v409 (QUEM «claude-c1 pos-rito v409», PINO_MEMORIA_PY_v409.json, V409_MEMORIA_DIR)."),
           3: ("# [ADAPTADO v409, 04/11/2026, claude-construtor-v409 (fork B)]", None)})
a.grava()

# ---------------------------------------------------------------- superficies (o corpo e' generico: os textos vem do textos_v409.py)
a = Arq("pos_rito/superficies_v409.py")
linhas(a, {2: ("# [A ADAPTAR v409]", MARCA + "sobre a subida mecanica da v408 FINAL (bump/pos_rito__superficies_v409.py.diff fica como registro): o corpo e' generico (os blocos vem do textos_v409.py); muda so' o que o cabecalho descreve. " + CONTEUDO + "."),
           3: ("# [ADAPTADO v409, 04/11/2026, claude-construtor-v409 (fork B)]", None),
           7: ("# SEM erratas inline nesta versao (as erratas E21 a E23 da v409", "# SEM erratas inline nesta versao (as erratas E24 a E26 e a dos pisos, da v409, vao DENTRO dos blocos datados: linhagem, desenho, Atlas, core, topico novo e handoff; o Atlas e o diario sao append-only e a correcao vai AO LADO). A funcao inserir_ao_lado fica disponivel (nao e' chamada)."),
           12: ("# A linha do handoff novo entra ANTES da linha do handoff da v408", "# A linha do handoff novo entra ANTES da linha do handoff da v408 (que a custodia da v408 reescreveu em 05/11 e que segue VERBATIM: a ancora (handoff-v408-custodia.md) e' conferida presente, uma so', no MEMORY.md lido na hora, como a linha da missao); a linha do handoff novo e o gancho da missao sao CURTOS de proposito: o indice tem 24.000 B e 195 linhas de teto.")})
a.grava()

# ---------------------------------------------------------------- chain_pos_rito (cabecalho, REGS, sufixo do backup)
a = Arq("pos_rito/chain_pos_rito_v409.sh")
linhas(a, {2: ("# [A ADAPTAR v409]", MARCA + "sobre a subida mecanica de rotulo da v408 FINAL (bump/pos_rito__chain_pos_rito_v409.sh.diff fica como registro), por _adapt_forkA_pequenos_v409.py: mesma ordem de passos 0..14 e mesmos portoes; muda o conteudo dito, REGS e o sufixo do backup do inventario."),
           3: ("# [ADAPTADO v409, 04/11/2026, claude-construtor-v409 (fork B)]", None),
           4: ("# v409 (TETELESTAI E' O TERMINAL, 04/11/2026): CADEIA POS-RITO", "# v409 (A TRADUCAO AS CLASSES DE TURING, 05/11/2026): CADEIA POS-RITO -- derivada por script (_bump_copia_v409.py, rotulos) do chain_pos_rito_v408.sh FINAL (a cadeia de CONTEUDO que rodou no pos-rito da v408; mesma ordem de passos 0..14 e mesmos portoes) e adaptada por _adapt_forkA_pequenos_v409.py."),
           5: ("# A v409 e' TETELESTAI E' O TERMINAL", "# " + CONTEUDO + "; a escada, as bandeiras e o h8 sao lidos de ESPERADOS_v409.json."),
           6: ("# UM registro COM FUNCAO (tetelestai_terminal_v408", "# UM registro COM FUNCAO (traducao_turing_v409: as 62 ancoras da pedra lidas do kernel do rito, o modulo por sha256, as respostas do operador pelos teoremas da pedra, as 17 checagens com a instancia de brinquedo fixa e beta em runtime, o gate congelado, o pino do acervo da v407 na copia purgada (D57d); lido no main DEPOIS dos registros herdados) e DOIS por spec (cunhagens_v409 e kh_n1_cobertura_v409). NENHUMA chave antiga muda."),
           7: ("# O psion_canto_v407 (e os dois por spec da v408", "# O tetelestai_terminal_v408 (e os dois por spec da v408: cunhagens_v408 com a E26 ao lado, kh_n1_cobertura_v408 com pisos), o psion_canto_v407 (e os dois por spec da v407: cunhagens_v407 com a errata da D57(d) ao lado), o fechamento_v406 (e os dois por spec da v406), os treze registros da v405 selada, os da v404, da v403, da v402, da v401 e da v399 sao RECRIADOS pelo rito (selos iguais a v408 selada) e o SIDECAR um_absoluto_selo_acom.json e' reescrito."),
           9: ("# Estatutos: os termos dos quatro modulos sao [REAL]", "# Estatutos: os termos do modulo sao [REAL] (kernel, no trio); [POSTO] o 1 / u = 1 eV; [MEDIDA] alfa; as falas do operador de 05/11 sao [INPUT]; o alcance (D56) e' relativo ao leitor; a maquina sem leitor, a fisica (a leitura exata num ato), a leitura teologica e o par na face de Fock ficam fora do kernel e ditos; [KNOWN] Baker-Gill-Solovay 1975 e as referencias do alcance; validade no kernel nao e' creditacao; o gate nao se move."),
           14: ("# ENSAIO pos-selo -> 10a parada do servico", "# ENSAIO pos-selo -> 10a parada do servico (AGUARDA_OPERADOR) -> 10b B(n) APLICAR (so com B3_AUTORIZADO=sim e o evento c1) -> 10c religamento (AGUARDA_OPERADOR) -> 11 fechar (o handoff TRAZ os DOIS paragrafos do README e do site: o do quadro do 4,44, intocado, e o NOVO da v409 (a traducao as classes de Turing), mais a NOTA ao lado do paragrafo da v408 (E26: a traducao as classes de Turing, [OPEN] na v408, fica fechada relativa ao leitor); diz que os anteriores seguem como estao;"),
           30: ("# textos_v409.py, fechar_v409.py e registrar_mapa_v409.py RECUSAM rodar", "# textos_v409.py, fechar_v409.py e registrar_mapa_v409.py RECUSAM rodar se tiverem trecho marcado para reescrever: os passos 0 a 2 nao os usam. Os passos 0 a 9, 10a, 10c e 11 a 14 estao como na v408, com os rotulos da v409 (desvios ditos: a fila da memoria nos passos 0, 7 e 9; o passo 3 e o 9 exigem os marcadores da v409 (os tres registros novos: traducao_turing_v409, cunhagens_v409 e kh_n1_cobertura_v409);"),
           31: ("# o passo 11 registra o estado da fila no manifesto", "# o passo 11 registra o estado da fila no manifesto e diz que os paragrafos do testemunho, da falsidade, do fechamento (v406), do psion (v407) e de Tetelestai e' o terminal (v408) seguem como estao).")})
a.troca('REGS="tetelestai_terminal_v408 cunhagens_v408 kh_n1_cobertura_v408"', 'REGS="traducao_turing_v409 cunhagens_v409 kh_n1_cobertura_v409"')
a.troca('B="$ATLD/$f.bak_$(date +%Y%m%d_%H%M%S)_v408"', 'B="$ATLD/$f.bak_$(date +%Y%m%d_%H%M%S)_v409"')
a.grava()

# ---------------------------------------------------------------- gerar_derivacao_pos_rito (cabecalho, SUITE, OPCIONAIS)
a = Arq("pos_rito/gerar_derivacao_pos_rito_v409.py")
linhas(a, {2: ("# [A ADAPTAR v409]", MARCA + "sobre a subida mecanica de rotulo da v408 FINAL (_bump_copia_v409.py): a SUITE descreve a v409 (A TRADUCAO AS CLASSES DE TURING; os papeis, as datas e os autores de 05/11: fork A = o pos_rito inteiro e o orquestrador; os do lote 04/11 do fork B ficam como registro nas notas dos arquivos); o montador, a semente e o fragmento SAO usados na v409 (deixam de ser opcionais). SO' LE; a gerencia revisa antes do rito (nao e' versao selada)."),
           3: ("# [ADAPTADO v409, 04/11/2026, claude-construtor-v409 (fork B)]", None)})
a.troca("A ADAPTACAO (o que o pos-rito diz da v409: Tetelestai e' o terminal, com os numeros lidos do rito) foi feita em 04/11/2026 pela claude-construtor-v409 em tres forks, pelos _adapt_*_v409.py desta pasta (trocas de contagem exata com backup de bytes) e por reescrita integral onde o corpo era o da v408 (registrar_mapa_v409.py, gerar_x_custodia_v409.py, textos_custodia_handoff_v409.py, este com o nome de D52); textos_v409.py, leitura_v409.py e o harness dos textos sao do fork A;",
        "A ADAPTACAO (o que o pos-rito diz da v409: a traducao as classes de Turing, relativa ao leitor, com os numeros lidos do rito) foi feita em 05/11/2026 pela claude-construtor-v409 (fork A), pelos _adapt_*_v409.py desta pasta (trocas de contagem exata com backup de bytes), pelo montador (textos_v409.semente + textos_v409_novo.pysnip -> textos_v409.py) e por reescrita onde o corpo era o da v408 (registrar_mapa_v409.py, gerar_x_custodia_v409.py, textos_custodia_handoff_v409.py);")
VELHA = a.t[a.t.index("SUITE = (\n"):a.t.index("OPCIONAIS = {")]
NOVA = '''SUITE = (
    ("chain_pos_rito_v409.sh", "chain_pos_rito_v408.sh", "fork A, 05/11: a cadeia (passos 0..14) com o passo da fila da memoria; REGS da v409 (traducao_turing_v409, cunhagens_v409, kh_n1_cobertura_v409), o rotulo B18, o sufixo _v409 dos backups do inventario"),
    ("superficies_v409.py", "superficies_v408.py", "fork A, 05/11: as superficies (diretorio de memoria por V409_MEMORIA_DIR; recusa rc 3 acima de 195 linhas ou 24000 B); so' as notas mudaram (os blocos vem do textos_v409.py)"),
    ("fechar_v409.py", "fechar_v408.py", "fork A, 05/11: o fechar (manifesto com registros_v409/v408/v407/v406 e registros_funcao_v409 (traducao)/v408 (tetelestai)/v407 (psion)/v406, arquivo, diffs, handoff)"),
    ("b3_recibo_v409.py", "b3_recibo_v408.py", "fork A, 05/11: o recibo do B(n), passo SIMPLES B17 -> B18; so' as notas mudaram"),
    ("gerar_derivacao_pos_rito_v409.py", "gerar_derivacao_pos_rito_v408.py", "fork A, 05/11: este registro (so' le)"),
    ("harness_fechar_sandbox_v409.py", "harness_fechar_sandbox_v408.py", "fork A, 05/11: o harness do fechar/chain em sandbox, com o ensaio da fila da memoria em COPIA e os controles negativos da v409 (a traducao; o tetelestai, o psion e o fechamento herdados; E26; D59)"),
    ("fila_memoria_v409.py", "fila_memoria_v408.py", "fork A, 05/11: as operacoes da fila da memoria do pos-rito (guardas, pausa, pinar, verificar), chamadas pelo chain e pelo harness; so' as notas mudaram"),
    ("leitura_v409.py", "leitura_v408.py", "fork A, 05/11: a leitura da rodada adaptada a traducao as classes de Turing (o modulo TraducaoTuring, as ancoras lidas de delta_v409, nenhuma chave antiga muda; o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados e os registros anteriores recriados)"),
    ("textos_v409.py", "textos_v408.py", "fork A, 05/11: os textos da v409, MONTADOS (montar_textos_v409.py: semente + fragmento): o paragrafo novo, a nota ao lado do paragrafo da v408 com a E26, o handoff, as superficies, o topico novo"),
    ("harness_textos_ensaio_v409.py", "harness_textos_ensaio_v408.py", "fork A, 05/11: o harness do pos-rito adaptado a traducao (controles negativos dos registros novos e dos herdados, D59)"),
    ("registrar_mapa_v409.py", "registrar_mapa_v408.py", "fork A, 05/11: REESCRITO para a v409: a rota nova (o id esta em registrar_mapa_v409.NOVA), as anotacoes nas rotas de 05/11 e as erratas E24 a E26 ao lado"),
    ("textos_custodia_handoff_v409.py", "textos_custodia_handoff_v408.py", "fork A, 05/11: REESCRITO para a v409: os sete textos da custodia (roda ENCADEADO no fim do S6, pelo orquestrador; a chain nao o chama)"),
    ("gerar_x_custodia_v409.py", "gerar_x_custodia_v408.py", "fork A, 05/11: REESCRITO para a v409: o rascunho do post longo do X (numeros do selo e do core; a ordem e as cunhagens por delta_v409.FRASE_*; sem o 4,44; D59)"),
    ("montar_textos_v409.py", "montar_textos_v408.py", "fork A, 05/11: o montador (semente + fragmento -> textos_v409.py); DELETAR ganha _d51"),
    ("textos_v409_novo.pysnip", "textos_v408_novo.pysnip", "fork A, 05/11: o fragmento da v409 (as definicoes da traducao; __HEADER__)"),
    ("textos_v409.semente", "textos_v408.py", "fork A, 05/11: a semente = textos_v408.py FINAL (montado) com os rotulos subidos, a marca trocada e o fim de linha normalizado para LF"),
    ("adaptar_pos_rito_v409.py", None, "OPCIONAL: o adaptador comum da v408; na v409 cada _adapt_*_v409.py e' autonomo"),
)
'''
a.troca(VELHA, NOVA)
a.troca('OPCIONAIS = {"montar_textos_v409.py", "textos_v409_novo.pysnip", "adaptar_pos_rito_v409.py", "textos_v409.semente"}', 'OPCIONAIS = {"adaptar_pos_rito_v409.py"}')
a.troca('"claude-construtor-v409, 04/11: adaptador do pos-rito (trocas de contagem exata com asserts e backup de bytes)"', '"claude-construtor-v409, 04-05/11: adaptador (trocas de contagem exata com asserts e backup de bytes)"')
a.troca("a adaptacao foi feita pela claude-construtor-v409 em 04/11/2026 (forks A e B) pelos _adapt_*_v409.py desta pasta e por reescrita integral onde o corpo era o da v408 (registrar_mapa, gerar_x_custodia, textos_custodia_handoff)",
        "a adaptacao foi feita pela claude-construtor-v409 (fork A) em 05/11/2026 pelos _adapt_*_v409.py desta pasta, pelo montador dos textos e por reescrita onde o corpo era o da v408 (registrar_mapa, gerar_x_custodia, textos_custodia_handoff)")
a.grava()
