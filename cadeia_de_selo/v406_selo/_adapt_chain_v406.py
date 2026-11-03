# -*- coding: utf-8 -*-
"""_adapt_chain_v406.py -- as edicoes de chain_pos_rito_v406.sh (chamado por adaptar_pos_rito_v406.py)."""

BLOCO_4_9 = """# v406 (O FECHAMENTO, 02/11/2026): CADEIA POS-RITO -- derivada por script (derivar_encanamento_v406.py, lote F) do chain_pos_rito_v405.sh FINAL (a cadeia de CONTEUDO que rodou em 01/11; mesma ordem de passos 0..14 e mesmos portoes), com as licoes da v405 e o passo da FILA DA MEMORIA (abaixo). A narrativa e os vereditos esperados vem de textos_v406.py (montado de textos_v406.semente + textos_v406_novo.pysnip por montar_textos_v406.py), de leitura_v406.py e de ESPERADOS_v406.json (lidos, nunca digitados).
# A v406 e' o FECHAMENTO (as falas do operador de 02/11/2026): UM BUNDLE de 301 modulos novos de kernel (os 300 da bancada do ChatGPT, F1.FECHO_20261015, recompilados do fonte, e a candidata CanonicalFullTGLWitnessR1, de nome PROVISORIO: os nomes das pedras sao do operador; a escada, as bandeiras e o h8 sao lidos de ESPERADOS_v406.json),
# UM registro COM FUNCAO (fechamento_v406; lido no main DEPOIS dos da v405) e DOIS por spec (cunhagens_v406 e kh_n1_cobertura_v406). As QUATRO chaves de testemunha deixam de ser literal False e sao LIDAS do kernel do rito (errata E14). O GATE NAO SE MOVE: o qg_closure e' identico ao da v405; a funcao do neutrino NAO e' reescrita (o angle_status antigo fica); o numero da massa e' o da v405.
# Os treze registros da v405, os da v404, da v403, da v402, da v401 e da v399 sao RECRIADOS pelo rito (selos iguais a v405 selada) e o SIDECAR um_absoluto_selo_acom.json e' REESCRITO (depois da ultima escrita do selo).
# O QUADRO «O Teste da Unica Palavra» (v397, a regra do 4,44) PERMANECE no topo do artigo e do .md, INTOCADO: o conferidor e a leitura o conferem de novo; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item) segue valendo em TODO texto que o cite. Os paragrafos do testemunho, da falsidade, da ponte, de Caminho, Verdade e Vida, de Jo 8,32 e da massa derivada (v405) seguem como estao; os anteriores recebem a NOTA ao lado (E14).
# Estatutos: os termos do fecho sao [REAL] (kernel, no trio); [POSTO] o 1 / u = 1 eV; [MEDIDA] alfa; as leituras do operador de 02/11 entram como [ONTO] e nao sao teoremas; as ressalvas (K(O) != bot so' na cunha; o nucleo II_inf [KNOWN/DECLARADO]; traco ENNReal ciclico; R7 Codex x Codex; R4/R5 fora; o nome provisorio) vao ditas; validade no kernel nao e' creditacao. A guarda das frases (guarda_frases_v406.py) roda sobre todo texto renderizado (superficies, fechar, mapa).
"""


def rodar(A):
    nome = "chain_pos_rito_v406.sh"
    txt, crlf, raw = A.le(nome)
    if A.pula(nome, txt):
        return
    t = A.tira_cabecalho(txt)
    t = A.entre(t, "# v406 (preparacao, 01/11/2026): CADEIA POS-RITO", "# ORDEM: 0 guardas", BLOCO_4_9)
    t = A.sub(t, "o NOVO da v406 (a massa derivada e a identidade definida), mais a NOTA ao lado do paragrafo da v405 (E0 passou de declarado a posto; os nomes foram dados); diz que os anteriores seguem como estao;",
              "o NOVO da v406 (o fechamento), mais a NOTA ao lado dos paragrafos anteriores (E14: as quatro chaves de testemunha eram literal e passaram a leitura do kernel); diz que os anteriores seguem como estao;")
    t = A.sub(t, "a Bancada de producao JA pina a v405 (B13, B13-v405-20261028-R1)", "a Bancada de producao JA pina a v405 (B14, B14-v405-20261102-R1)")
    t = A.sub(t, "o diff v405 -> v406 e' so' as oito pedras novas", "o diff v405 -> v406 e' so' os 301 modulos novos")
    t = A.sub(t, "(B13 -> n = 14;", "(B14 -> n = 15;")
    t = A.sub(t, "o passo 3 e o 9 exigem os marcadores da v406 (os treze registros novos);", "o passo 3 e o 9 exigem os marcadores da v406 (os tres registros novos);")
    t = A.sub(t, 'REGS="ponte_da_massa_v405 massa_tensao_pura_v405 identidade_v405 observador_terminal_v405 lei_do_diminuto_v405 tonica_do_hamiltoniano_v405 disco_de_euler_v405 ponto_zero_do_psion_v405 cunhagens_v405 campos_fechados_e_leituras_v405 ga_reclassificacao_v405 gap_v405 kh_n1_cobertura_v405"',
              'REGS="fechamento_v406 cunhagens_v406 kh_n1_cobertura_v406"')
    t = A.sub(t, "# os registros NOVOS da v406 que as superficies", "# os TRES registros NOVOS da v406 que as superficies")
    t = A.sub(t, "as oito pedras novas tem declaracoes nomeadas", "os 301 modulos novos tem declaracoes nomeadas")
    t = A.sub(t, '.bak_$(date +%Y%m%d_%H%M%S)_v405"', '.bak_$(date +%Y%m%d_%H%M%S)_v406"')
    A.grava(nome, t, crlf, raw)
