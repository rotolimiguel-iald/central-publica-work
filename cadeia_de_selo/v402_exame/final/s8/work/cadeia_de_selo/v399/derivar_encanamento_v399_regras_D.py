# -*- coding: utf-8 -*-
# regras (lote D) de derivar_encanamento_v399.py: os scripts AUTORAIS (a logica muda; a subida mecanica e' so' o ponto de partida, editado a mao depois: o derivador NAO sobrescreve o que ja' existe e difere) e o derivador do rito.
# ESTE ARQUIVO e' escrito pela ferramenta Write (barras invertidas intactas).

# ------------------------------------------------------------------------------------------- derivar_instalar_rito (rito_v399.sh derivado do rito_v398.sh FINAL)
_CAB = r'''CABECALHO = ["# O RITO v399 (ato da gerencia c1, 24/10/2026): roda o um.py v399 instalado no Nos -- %d modulo novo de kernel (TGLExt/Testemunho, nome PROVISORIO: quem nomeia e' o operador; o numero e' lido de kernel_modulos_novos_v399.json) materializado a partir do corpo embutido, kernel e Audit" % N_NOVOS,
             "# construidos pelo proprio um.py, os registros com FUNCAO selo_pela_propria_tecnologia_v399 (o metodo do operador, EMBUTIDO, sela o um.py AO LADO do SHA-256) e declaracao_do_operador_v399 (chamados no main, logo depois da afinacao das cordas), o SIDECAR um_absoluto_selo_acom.json (escrito depois da ultima escrita do selo) e os registros por spec novos do core v399 (cunhagens_v399, com as quatro inscricoes de 24/10; kh_n1_cobertura_v399). O QUADRO do Teste da Unica Palavra segue no topo. O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (_QP_REUSE_V386",
             "# segue no um.py; TGL_RITE_CHECKPOINT DESLIGADO). Molde: rito_v398.sh herdado com as afericoes dele, trocados os nomes, o pacote (a propria pasta da cadeia v399) e a",
             "# guarda do marcador anterior: echo 1 | python um.py no Nos, stdout canonico em rodada_v399_stdout.txt, trailer RITO_RC=<rc>, horarios no pacote. RODADA COMPLETA."]
'''
entrada("derivar_instalar_rito_v398.py", autoral=True, regras=[
    entre("CABECALHO = [", "\n# ============================================================================= rito_v399.sh", _CAB, "cabecalho do rito v399"),
    ("a subida de versao e' v398 -> v399 e v396 -> v398, o 'anterior' da guarda do marcador;", "a subida de versao e' v398 -> v399 e v397 -> v398, o 'anterior' da guarda do marcador;", 1),
    ("\"\"\"v398 -> v399, v396 -> v398 (o 'anterior'), V398 -> V399, V396 -> V398, k398c -> k399c, k396 -> k398.\"\"\"", "\"\"\"v398 -> v399, v397 -> v398 (o 'anterior'), V398 -> V399, V397 -> V398, k398c -> k399c, k397 -> k398.\"\"\"", 1),
    ('.replace("v396", "v398").replace("@@A@@", "v399")', '.replace("v397", "v398").replace("@@A@@", "v399")', 1),
    ('.replace("V396", "V398").replace("@@B@@", "V399")', '.replace("V397", "V398").replace("@@B@@", "V399")', 1),
    ('.replace("k398c", "k399c").replace("k396", "k398")', '.replace("k398c", "k399c").replace("k397", "k398")', 1),
    ('== 1 and "v396" not in RITO', '== 1 and "v397" not in RITO', 1),
    ('for tok in ("k398d", "k396", "work398", "v396"):', 'for tok in ("k398d", "k397", "work398", "v397"):', 1),
    ('"sobe": "v398 -> v399, v396 -> v398 (anterior), V398 -> V399, V396 -> V398, k398c -> k399c, k396 -> k398;', '"sobe": "v398 -> v399, v397 -> v398 (anterior), V398 -> V399, V397 -> V398, k398c -> k399c, k397 -> k398;', 1),
    ("tem de trazer a LISTA com as DUAS pedras (Sonico e AfinacaoDasCordas)", "tem de trazer a LISTA com a pedra Testemunho", 1),
    ("(a v398 e as duas pedras novas ja' estao compiladas em .lake/build, cada pedra isolada; mudam a raiz TGLExt e o Audit)", "(a v398 e a pedra nova, Testemunho, ja' estao compiladas em .lake/build, a pedra isolada; mudam a raiz TGLExt e o Audit)", 1),
    ("no Nos o primeiro build compila as pedras a frio", "no Nos o primeiro build compila a pedra a frio", 1),
])

# ------------------------------------------------------------------------------------------- AUTORAIS: a subida mecanica agora; a edicao a mao depois (o derivador nao os sobrescreve)
entrada("p00_precondicoes_v398.py", autoral=True)
entrada("conferir_rito_v398.py", autoral=True)
entrada("gerar_esperados_v398.py", autoral=True)
entrada("gerar_estado_v398.py", autoral=True)
entrada("gerar_registro_mapa_prep_v398.py", autoral=True)
