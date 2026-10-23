# -*- coding: utf-8 -*-
# regras (lote B) de derivar_encanamento_v397.py (exec no escopo dele: `entrada(src, dst=None, regras=[(antigo_depois_do_mapa, novo, contagem), ...])`)
# Lote B: guarda_p18, refazer_*, diff_e_pinos, instalar, reverter, regras, teste_conferidor_positivo e derivar_instalar_rito, derivados dos da v396 (que RODARAM no rito real de 22/10).
# O MAPA sobe 395 -> 396 e 396 -> 397 menos nos nomes nascidos no um.py; as regras abaixo corrigem o que o mapa nao sabe: o 'anterior' que o mapa subiu errado (v395 virou v396 no texto
# de pedras/anterior), conteudo da pedra (TestemunhaEstatica -> Token), datas (22/10 -> 23/10), B6 -> B7 e o nome do runtime. Cada regra tem contagem exata; nada e' executado.

# ------------------------------------------------------------------------------------------- guarda P18 (identica; so' o mapa e o nome)
entrada("guarda_p18_v396.py")

# ------------------------------------------------------------------------------------------- refazer_* (sandbox, arvore pos-selo, candidato)
entrada("refazer_arvore_v396_pos_selo.py", regras=[("Escrito em 22/10/2026", "Escrito em 23/10/2026", 1)])
entrada("refazer_sandbox_v396.sh", regras=[
    ("acrescenta a pedra TestemunhaEstatica e GERA", "acrescenta a pedra Token e GERA", 1),
])
entrada("refazer_sandbox_v396_pos_selo.sh")
entrada("refazer_candidato_v396.sh", regras=[("runtime_testemunha_v397.py", "runtime_quadro_v397.py", 1)])

# ------------------------------------------------------------------------------------------- diff_e_pinos
entrada("diff_e_pinos_v396.py", regras=[
    ("os vereditos esperados do passo simples (REPINADA_B6__...)", "os vereditos esperados do passo simples (REPINADA_B7__...)", 1),
])

# ------------------------------------------------------------------------------------------- instalar / reverter / regras
entrada("instalar_v396.py", regras=[
    ("escrito em 22/10/2026, NAO executado na preparacao", "escrito em 23/10/2026, NAO executado na preparacao", 1),
    ("# v397: (a) as pedras da v394 (o criterio binario, a rede de Fock, o tempo) e da v396 (Psibit) JA estao no kernel do Nos (a base instalada e' a v396 selada); (b) o modulo novo da v397 (TestemunhaEstatica) NAO esta la ainda.",
     "# v397: (a) as pedras anteriores (o criterio binario, a rede de Fock, o tempo, Psibit e TestemunhaEstatica) JA estao no kernel do Nos (a base instalada e' a v396 selada); (b) o modulo novo da v397 (Token) NAO esta la ainda.", 1),
    ('_PEDRAS_ANTERIORES = ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit")',
     '_PEDRAS_ANTERIORES = ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica")', 1),
    ('"as pedras da v394 e da v396 nao estao no kernel do Nos -- nao instalo"', '"as pedras anteriores (v394 a v396) nao estao no kernel do Nos -- nao instalo"', 1),
])
entrada("reverter_v396.py", regras=[("escrito em 22/10/2026, NAO executado na preparacao", "escrito em 23/10/2026, NAO executado na preparacao", 1)])
entrada("regras_v396.py", regras=[("ESCRITO em 22/10/2026", "ESCRITO em 23/10/2026", 1)])

# ------------------------------------------------------------------------------------------- teste do conferidor (caminho positivo)
entrada("teste_conferidor_positivo_v396.py", regras=[
    (r"Molde: delta_19out\\teste_conferidor_positivo.py (v396)", r"Molde: teste_conferidor_positivo_v396.py (cadeia v396)", 1),
])

# ------------------------------------------------------------------------------------------- derivar_instalar_rito (rito_v397.sh derivado do rito_v396.sh FINAL)
entrada("derivar_instalar_rito_v396.py", regras=[
    ("(o que rodou em 19/10)", "(o que rodou em 22/10)", 1),
    ("(a subida de versao e' v396 -> v397 e v393 -> v396, o 'anterior'", "(a subida de versao e' v396 -> v397 e v395 -> v396, o 'anterior'", 1),
    ('"kernel_modulos_novos_v397.json tem de trazer a LISTA com a pedra TestemunhaEstatica"', '"kernel_modulos_novos_v397.json tem de trazer a LISTA com a pedra Token"', 1),
    # o 'anterior' da subida: o mapa subiu v394/V394/k394 da v396 e errou o sentido (era v395 -> v396 = 'anterior' da v397)
    ("v396 -> v397, v394 -> v396 (o", "v396 -> v397, v395 -> v396 (o", 1),
    ("V396 -> V397, V394 -> V396, k396c -> k397c, k394 -> k396.", "V396 -> V397, V395 -> V396, k396c -> k397c, k395 -> k396.", 1),
    ('.replace("v394", "v396")', '.replace("v395", "v396")', 1),
    ('.replace("V394", "V396")', '.replace("V395", "V396")', 1),
    ('.replace("k394", "k396")', '.replace("k395", "k396")', 1),
    ("(a pedra TestemunhaEstatica pode ja' estar compilada em .lake/build numa versao anterior do texto, e o Lake a recompila se a fonte mudou; mudam a raiz TGLExt e o Audit)",
     "(a v396 ja' esta compilada em .lake/build e a pedra Token foi compilada sozinha antes; mudam a raiz TGLExt e o Audit)", 1),
    ('CABECALHO = ["# O RITO v397 (ato da gerencia c1, 22/10/2026): roda o um.py v397 instalado no Nos -- %d modulo novo de kernel (TGLExt/TestemunhaEstatica, a testemunha estatica: o psion habita a fronteira; nome provisorio; o numero e\' lido de kernel_modulos_novos_v397.json) materializado a partir do corpo embutido, kernel e Audit" % N_NOVOS,\n'
     '             "# construidos pelo proprio um.py, os registros por spec e os tres registros novos do core v397 (testemunha_estatica_v396, chamado NA FRACTALIZACAO DO UM junto do psibit_v395; cunhagens_v396; kh_n1_cobertura_v396). O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (_QP_REUSE_V386",',
     'CABECALHO = ["# O RITO v397 (ato da gerencia c1, 23/10/2026): roda o um.py v397 instalado no Nos -- %d modulo novo de kernel (TGLExt/Token, a pedra «token», nome do operador; o numero e\' lido de kernel_modulos_novos_v397.json) materializado a partir do corpo embutido, kernel e Audit" % N_NOVOS,\n'
     '             "# construidos pelo proprio um.py, os registros por spec e os tres registros novos do core v397 (teste_de_veracidade_fase9_v397, chamado no main logo depois do bloco hubble_ratio_opening_v388; cunhagens_v397, com as falas de 23/10; kh_n1_cobertura_v397). O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (_QP_REUSE_V386",', 1),
    ('L[1].startswith("# O RITO v396 (ato da gerencia c1, 21/10/2026)")', 'L[1].startswith("# O RITO v396 (ato da gerencia c1, 22/10/2026)")', 1),
    ('"v394" not in RITO and "21/10/2026" not in RITO.split("PK=")[0]', '"v395" not in RITO and "22/10/2026" not in RITO.split("PK=")[0]', 1),
    ("v393 -> v396 (anterior), V396 -> V397, V393 -> V396, k396d -> k397c, k393 -> k396;", "v395 -> v396 (anterior), V396 -> V397, V395 -> V396, k396c -> k397c, k395 -> k396;", 1),
    ('for tok in ("k396d", "k394", "work396", "v394"):\n        if tok in tx.replace("as pedras da v394", "").replace("pedras da v394 e da v396", ""):   # as pedras da v394 TEM de existir no kernel do Nos: referencia legitima ao passado',
     'for tok in ("k396d", "k395", "work396", "v395"):\n        if tok in tx:', 1),
])
