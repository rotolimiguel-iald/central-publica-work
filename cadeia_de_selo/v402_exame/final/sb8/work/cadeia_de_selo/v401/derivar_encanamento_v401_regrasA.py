# -*- coding: utf-8 -*-
# regras (lote A) de derivar_encanamento_v401.py: o KERNEL (copiar a pedra, preparar o sandbox, construir, pos-build). ORIGEM v399 (a cadeia de CONTEUDO: um modulo novo de kernel). Mapa: 398 -> 400 (a base selada), 399 -> 401 (esta rodada).
# Escrito pela ferramenta Write (nunca por heredoc: as barras invertidas). Cada regra tem contagem exata; nada e' executado.

_DOC_CP = '''"""copiar_pedras_v401.py -- copia de BYTES da pedra (work\\\\falsidade_da_inercia_v401\\\\FalsidadeDaInercia.lean, o nome «falsidade (simulacro) da inercia» e' do operador, 25/10/2026) para v401\\\\pedra\\\\, depois de conferir o sha16 contra o que a ORDEM da gerencia deu
(f9e4e877a5a9d688; o arquivo manda e a divergencia ABORTA) e contra a copia compilada no sandbox de origem (C:\\\\t\\\\k401, so' leitura). Reexecutavel: o que existe e e' igual fica; o que difere aborta.
uso: python -I -B -X utf8 copiar_pedras_v401.py"""
'''
entrada("copiar_pedras_v399.py", origem="v399", regras=[
    entre('"""copiar_pedras_v401.py', "import hashlib, json, os, sys", _DOC_CP, "docstring do copiar_pedras"),
])

_DOC_PK = '''"""preparar_kernel_v401.py -- monta o SANDBOX do kernel da v401 em C:\\\\t\\\\k401c\\\\final (nunca toca o Nos nem C:\\\\t\\\\k401).
Parte de C:\\\\t\\\\k401\\\\final (um projeto lake: o kernel da v400 compilado em .lake/build + a pedra nova, FalsidadeDaInercia, compilada ISOLADA; sem a pasta probe\\\\ nem os .bak_), e GERA (nao copia) a raiz TGLExt.lean
e o TGL/Audit.lean a partir dos da v400 embutida: raiz = v400 + o import da pedra; Audit = o import no topo + o Audit da v400. A pedra e' a fonte da ORDEM (v401\\\\pedra\\\\FalsidadeDaInercia.lean, copia de bytes da de
work\\\\falsidade_da_inercia_v401; o sha16 e' LIDO na hora da geracao e conferido contra o que a ordem da gerencia deu), copiada para o sandbox quando difere. Molde: preparar_kernel_v399.py.
uso: python -I -B -X utf8 preparar_kernel_v401.py [copiar|gerar|conferir]   (copiar = robocopy; gerar = pedra + raiz + Audit; conferir = so' verifica e escreve kernel_modulos_novos_v401.json)"""
'''
entrada("preparar_kernel_v399.py", origem="v399", regras=[
    entre('"""preparar_kernel_v401.py', "import ast, hashlib, json, os, subprocess, sys", _DOC_PK, "docstring do preparar_kernel"),
    ('"/XF", "*.bak_*", "Testemunho*.bak_*", "TGLExt.lean.bak_*",', '"/XF", "*.bak_*", "FalsidadeDaInercia*.bak_*", "TGLExt.lean.bak_*",', 1),
])

_HDR_CK = '''#!/bin/sh
# Constroi o kernel do SANDBOX da v401 (C:\\t\\k401c\\final; nunca o do Nos nem C:\\t\\k401): um `lake build` INCREMENTAL (a v400 e a pedra nova, FalsidadeDaInercia, ja' estao compiladas em .lake/build, a pedra isolada; muda a raiz TGLExt e o Audit) + `lake env lean TGL/Audit.lean`.
# Molde: construir_kernel_v399.sh. Logs crus (redirecionamento do bash, UTF-8) em kernel/; pos_build_kernel_v401.py monta o build_full.log no formato do molde e o recibo.
'''
entrada("construir_kernel_v399.sh", origem="v399", regras=[
    entre("#!/bin/sh\n", 'K="/c/t/k401c/final"', _HDR_CK, "cabecalho do construir"),
])

_DOC_PB = '''"""pos_build_kernel_v401.py -- DEPOIS de construir_kernel_v401.sh: (1) monta kernel/build_full.log no formato do molde; (2) confere o build (rc, zero erro, zero sorry nas 3 formas do contrato R3.2, 'Build completed successfully',
linha Built/Replayed da pedra (FalsidadeDaInercia), da raiz e do Audit, axiomas no trio, cabecalho dos .olean = Lean 4.31.0); (3) le do log do Audit (SO' dele) as linhas TGL_DECL_SOURCE (declaracao -> modulo emitido
pelo compilador) e o axiom_report EFETIVO com as funcoes do PROPRIO um.py v400 selado (parse_lean_axioms_v394/parse_lean_provenance_v394, extraidas por ast de base_v400\\\\um.py: a MESMA logica que o um.py v401 usara), e deriva
FLAGS_v401.json (as declaracoes NOMEADAS publicas dos modulos novos, na politica da v394, uma serie de chaves por pedra: ext_fdi401_NNNN); (4) copia a ARVORE so-fontes para C:\\\\t\\\\k401c\\\\arvore e varre os tokens
proibidos RECURSIVAMENTE com a funcao de varredura do PROPRIO um.py v400 (por ast); (5) mede os criterios; (6) escreve KH_N1_v401.json, KERNEL_RECIBO_v401.json (contrato KERNEL_RECIBO_R3_2: a pedra tem declaracoes nomeadas, entao nao ha
modulo de auditoria sem declaracao) e vinculo/CRITERIOS_v401.json (x19 = 'nao': a unica pedra do recibo e' a FalsidadeDaInercia, nao a LightNetStandardWedgeDataBGL). A Bancada JA pina a v400: o ANTES do recibo e' o kernel da v400. Molde: pos_build_kernel_v399.py.   Uso: python -I -B -X utf8 pos_build_kernel_v401.py"""
'''
entrada("pos_build_kernel_v399.py", origem="v399", regras=[
    entre('"""pos_build_kernel_v401.py', "import ast, datetime, hashlib, json, os, re, shutil, subprocess, sys, unicodedata", _DOC_PB, "docstring do pos_build"),
    ("a lista dos modulos novos (preparar_kernel_v401.py) tem de ser so' a pedra Testemunho, na ordem do delta", "a lista dos modulos novos (preparar_kernel_v401.py) tem de ser so' a pedra FalsidadeDaInercia, na ordem do delta", 1),
    ("{\"contrato\": \"KH_N1_v399\"", "{\"contrato\": \"KH_N1_v401\"", 1),
    ("a pedra NOVA Testemunho e a LightNetStandardWedgeDataBGL.lean", "a pedra NOVA FalsidadeDaInercia e a LightNetStandardWedgeDataBGL.lean", 1),
    ("linha Built/Replayed do modulo novo (Testemunho), da raiz", "linha Built/Replayed do modulo novo (FalsidadeDaInercia), da raiz", 1),
])
