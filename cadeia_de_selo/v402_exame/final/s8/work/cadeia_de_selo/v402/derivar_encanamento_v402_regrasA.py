# -*- coding: utf-8 -*-
# regras (lote A) de derivar_encanamento_v402.py: o KERNEL (copiar a base, preparar o sandbox, construir, pos-build, insumos). ORIGEM v401. Mapa: 400 -> 401 (a base selada), 401 -> 402 (esta rodada).
# Escrito pela ferramenta Write (nunca por heredoc: as barras invertidas). Cada regra tem contagem exata; nada e' executado. copiar_pedras_v402.py e copiar_k402c.sh sao ESCRITOS A MAO (as tres pedras vem de tres origens).

entrada("copiar_base_v401.py", autoral=True, regras=[
    ("A Bancada de producao JA pina a v401 (B9): nao ha base_v398.", "A Bancada de producao JA pina a v401 (B10): nao ha salto de versoes.", 1),
    ("(6981660b5f7cd537; o arquivo manda)", "(1925cb691e933ae8; o arquivo manda)", 1),
])

_DOC_PK = '''"""preparar_kernel_v402.py -- monta o SANDBOX do kernel da v402 em C:\\\\t\\\\k402c\\\\final (nunca toca o Nos nem C:\\\\t\\\\k402 nem C:\\\\t\\\\k402x).
Parte de C:\\\\t\\\\k401c\\\\final (um projeto lake: o kernel do Nos v401 SELADO compilado em .lake/build, com a pedra FalsidadeDaInercia dentro; sem a pasta probe\\\\ nem os .bak_), e GERA (nao copia) a raiz TGLExt.lean
e o TGL/Audit.lean a partir dos da v401 embutida: raiz = v401 + os tres imports das pedras novas; Audit = os tres imports no topo + o Audit da v401. As pedras sao a fonte da ORDEM (v402\\\\pedra\\\\*.lean, copias de bytes das de Chatgpt\\\\TUNEL\\\\DO_CHATGPT\\\\ORDEM_025
e de work\\\\pedras_v402; o sha16 de cada uma e' LIDO na hora da geracao e conferido contra o que a ordem da gerencia deu), copiadas para o sandbox quando diferem. Molde: preparar_kernel_v401.py.
uso: python -I -B -X utf8 preparar_kernel_v402.py [copiar|gerar|conferir]   (copiar = robocopy; gerar = pedras + raiz + Audit; conferir = so' verifica e escreve kernel_modulos_novos_v402.json)"""
'''
entrada("preparar_kernel_v401.py", autoral=True, regras=[
    entre('"""preparar_kernel_v402.py', "import ast, hashlib, json, os, subprocess, sys", _DOC_PK, "docstring do preparar_kernel"),
    ('"/XF", "*.bak_*", "FalsidadeDaInercia*.bak_*", "TGLExt.lean.bak_*",', '"/XF", "*.bak_*", "PonteDaEscalaDual*.bak_*", "QuedaSemGeometria*.bak_*", "EsperancaCondicional*.bak_*", "TGLExt.lean.bak_*",', 1),
    ('assert s["rel"] not in emb0, "a pedra ja\' esta\' no kernel embutido da v401"', 'assert s["rel"] not in emb0, "a pedra ja\' esta\' no kernel embutido da v401: " + s["name"]', 1),
])

_HDR_CK = '''#!/bin/sh
# Constroi o kernel do SANDBOX da v402 (C:\\t\\k402c\\final; nunca o do Nos nem C:\\t\\k402 nem C:\\t\\k402x): um `lake build` INCREMENTAL (a v401 selada, FalsidadeDaInercia inclusive, ja' esta compilada em .lake/build; as TRES pedras novas, PonteDaEscalaDual, QuedaSemGeometria e EsperancaCondicional, compilam agora; mudam a raiz TGLExt e o Audit) + `lake env lean TGL/Audit.lean`.
# Molde: construir_kernel_v401.sh. Logs crus (redirecionamento do bash, UTF-8) em kernel/; pos_build_kernel_v402.py monta o build_full.log no formato do molde e o recibo.
'''
entrada("construir_kernel_v401.sh", autoral=True, regras=[
    entre("#!/bin/sh\n", 'K="/c/t/k402c/final"', _HDR_CK, "cabecalho do construir"),
])

_DOC_PB = '''"""pos_build_kernel_v402.py -- DEPOIS de construir_kernel_v402.sh: (1) monta kernel/build_full.log no formato do molde; (2) confere o build (rc, zero erro, zero sorry nas 3 formas do contrato R3.2, 'Build completed successfully',
linha Built/Replayed de cada pedra (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional), da raiz e do Audit, axiomas no trio, cabecalho dos .olean = Lean 4.31.0); (3) le do log do Audit (SO' dele) as linhas TGL_DECL_SOURCE (declaracao -> modulo emitido
pelo compilador) e o axiom_report EFETIVO com as funcoes do PROPRIO um.py v401 selado (parse_lean_axioms_v394/parse_lean_provenance_v394, extraidas por ast de base_v401\\\\um.py: a MESMA logica que o um.py v402 usara), e deriva
FLAGS_v402.json (as declaracoes NOMEADAS publicas dos modulos novos, na politica da v394, uma serie de chaves por pedra: ext_pde402_NNNN, ext_qsg402_NNNN, ext_ecn402_NNNN); (4) copia a ARVORE so-fontes para C:\\\\t\\\\k402c\\\\arvore e varre os tokens
proibidos RECURSIVAMENTE com a funcao de varredura do PROPRIO um.py v401 (por ast); (5) mede os criterios; (6) escreve KH_N1_v402.json, KERNEL_RECIBO_v402.json (contrato KERNEL_RECIBO_R3_2: cada pedra tem declaracoes nomeadas, entao nao ha
modulo de auditoria sem declaracao) e vinculo/CRITERIOS_v402.json (x19 = 'nao': as pedras do recibo sao as TRES novas, nao a LightNetStandardWedgeDataBGL). A Bancada JA pina a v401 (B10): o ANTES do recibo e' o kernel da v401. Molde: pos_build_kernel_v401.py.   Uso: python -I -B -X utf8 pos_build_kernel_v402.py"""
'''
entrada("pos_build_kernel_v401.py", autoral=True, regras=[
    entre('"""pos_build_kernel_v402.py', "import ast, datetime, hashlib, json, os, re, shutil, subprocess, sys, unicodedata", _DOC_PB, "docstring do pos_build"),
    ("a lista dos modulos novos (preparar_kernel_v402.py) tem de ser so' a pedra FalsidadeDaInercia, na ordem do delta", "a lista dos modulos novos (preparar_kernel_v402.py) tem de ser so' as TRES pedras (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional), na ordem do delta", 1),
    ("linha Built/Replayed do modulo novo (FalsidadeDaInercia), da raiz (TGLExt) e do Audit (TGL.Audit)", "linha Built/Replayed de CADA modulo novo (as tres pedras), da raiz (TGLExt) e do Audit (TGL.Audit)", 1),
    ("x19='nao': o recibo v402 lista so' a pedra NOVA FalsidadeDaInercia e a LightNetStandardWedgeDataBGL.lean ", "x19='nao': o recibo v402 lista so' as TRES pedras NOVAS (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) e a LightNetStandardWedgeDataBGL.lean ", 1),
    ("(preparacao, 24/10/2026); NAO conferido por verificar_kernel_recibo", "(preparacao, 26/10/2026); NAO conferido por verificar_kernel_recibo", 1),
    ("o build do sandbox e' INCREMENTAL (a pedra pode ja' estar compilada em C:/t/k402/final, isolada; o rito real do Nos compila a frio)", "o build do sandbox e' INCREMENTAL (as pedras podem ja' estar compiladas em C:/t/k402/final e C:/t/k402x/final, isoladas; o rito real do Nos compila a frio)", 1),
])

entrada("copiar_insumos_v401.py", autoral=True, regras=[
    ("das fontes que os registros da v402 pinam por sha256: a pedra (FalsidadeDaInercia), a medida do Audit (KH_N1_v402.json),", "das fontes que os registros da v402 pinam por sha256: as TRES pedras (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional), a medida do Audit (KH_N1_v402.json),", 1),
    ("as CINCO inscricoes de 25/10/2026 (todas falas do operador; insumos\\\\cunhagens\\\\<sha16>_<nome>)", "as TRES inscricoes de 26/10/2026 (todas falas do operador; insumos\\\\cunhagens\\\\<sha16>_<nome>)", 1),
])
entrada("purga_v401.py", autoral=True, regras=[])
