# -*- coding: utf-8 -*-
# regras (lote A) de derivar_encanamento_v404.py: o KERNEL (copiar a base, preparar o sandbox, construir, pos-build, insumos). ORIGEM v403. Mapa: 402 -> 403 (a base selada), 403 -> 404 (esta rodada).
# Escrito pela ferramenta Write (nunca por heredoc: as barras invertidas). Cada regra tem contagem exata; nada e' executado. copiar_pedras_v404.py, gerar_pino_das_pedras_v404.py e copiar_logs_do_kernel_v404.py sao ESCRITOS A MAO.

entrada("copiar_base_v403.py", autoral=True, regras=[
    ("A Bancada de producao JA pina a v403 (B11): nao ha salto de versoes.", "A Bancada de producao JA pina a v403 (B12): nao ha salto de versoes.", 1),
    ("(6a5033dc3f29324c; o arquivo manda)", "(2ffe9edc7d7545bd; o arquivo manda)", 1),
])

_DOC_PK = '''"""preparar_kernel_v404.py -- monta o SANDBOX do kernel da v404 em C:\\\\t\\\\k404c\\\\final (nunca toca o Nos nem C:\\\\t\\\\k403c).
Parte de C:\\\\t\\\\k403c\\\\final (um projeto lake: o kernel do Nos v403 SELADO compilado em .lake/build, com as tres pedras da v403 dentro; sem a pasta probe\\\\ nem os .bak_), e GERA (nao copia) a RAIZ TGLExt.lean a partir da v403 embutida: raiz = v403 + os dois imports das pedras novas
(ProjecaoTransversalDaMeiaNat, Jo8v32). O Audit NAO muda nesta versao (AUDIT_PREFIX vazio no delta: ele ja' faz `import TGLExt`, a raiz, que traz os modulos novos; a construcao de 28/10/2026 e' feita com o Audit inalterado). As pedras sao a fonte da ORDEM (v404\\\\pedra\\\\*.lean, copias de bytes das de
work\\\\projecao_transversal_28out; o sha16 de cada uma e' LIDO na hora da geracao e conferido contra o que os recibos de 28/10 deram), copiadas para o sandbox quando diferem. Molde: preparar_kernel_v403.py.
uso: python -I -B -X utf8 preparar_kernel_v404.py [copiar|gerar|conferir]   (copiar = robocopy; gerar = pedras + raiz [+ Audit se o prefixo nao for vazio]; conferir = so' verifica e escreve kernel_modulos_novos_v404.json)"""
'''
entrada("preparar_kernel_v403.py", autoral=True, regras=[
    entre('"""preparar_kernel_v404.py', "import ast, hashlib, json, os, subprocess, sys", _DOC_PK, "docstring do preparar_kernel"),
    ('"/XF", "*.bak_*", "Caminho*.bak_*", "Vida*.bak_*", "VerdadeAdendo*.bak_*", "TGLExt.lean.bak_*", "TGLExt.lean.k404_antes",', '"/XF", "*.bak_*", "ProjecaoTransversalDaMeiaNat*.bak_*", "Jo8v32*.bak_*", "TGLExt.lean.bak_*", "TGLExt.lean.k403_antes",', 1),
])

_HDR_CK = '''#!/bin/sh
# Constroi o kernel do SANDBOX da v404 (C:\\t\\k404c\\final; nunca o do Nos nem C:\\t\\k403c): um `lake build` INCREMENTAL (a v403 selada, com as tres pedras da v403, ja' esta compilada em .lake/build; as DUAS pedras novas, ProjecaoTransversalDaMeiaNat e Jo8v32, compilam agora; muda a raiz TGLExt; o Audit e' o da v403, inalterado) + `lake env lean TGL/Audit.lean`.
# Molde: construir_kernel_v403.sh. Logs crus (redirecionamento do bash, UTF-8) em kernel/; pos_build_kernel_v404.py monta o build_full.log no formato do molde e o recibo. Na preparacao de 28/10/2026 a construcao foi feita por este mesmo script (agente claude-prep-v404); as duas pedras ja' tinham sido provadas
# uma a uma por `lake env lean` no k403c (work\\projecao_transversal_28out\\RECIBO_PEDRA_*); copiar_logs_do_kernel_v404.py confere os logs ja' em kernel\\ e grava LOGS_COPIADOS_v404.json; este script e' o mesmo comando, para refazer.
'''
entrada("construir_kernel_v403.sh", autoral=True, regras=[
    entre("#!/bin/sh\n", 'K="/c/t/k404c/final"', _HDR_CK, "cabecalho do construir"),
])

_DOC_PB = '''"""pos_build_kernel_v404.py -- DEPOIS de construir_kernel_v404.sh: (1) monta kernel/build_full.log no formato do molde; (2) confere o build (rc, zero erro, zero sorry nas 3 formas do contrato R3.2, 'Build completed successfully',
linha Built/Replayed de cada pedra (ProjecaoTransversalDaMeiaNat, Jo8v32), da raiz e do Audit, axiomas no trio, cabecalho dos .olean = Lean 4.31.0); (3) le do log do Audit (SO' dele) as linhas TGL_DECL_SOURCE (declaracao -> modulo emitido
pelo compilador) e o axiom_report EFETIVO com as funcoes do PROPRIO um.py v403 selado (parse_lean_axioms_v394/parse_lean_provenance_v394, extraidas por ast de base_v403\\\\um.py: a MESMA logica que o um.py v404 usara), e deriva
FLAGS_v404.json (as declaracoes NOMEADAS publicas dos modulos novos, na politica da v394, uma serie de chaves por pedra: ext_ptm404_NNNN, ext_jo8404_NNNN); (4) copia a ARVORE so-fontes para C:\\\\t\\\\k404c\\\\arvore e varre os tokens
proibidos RECURSIVAMENTE com a funcao de varredura do PROPRIO um.py v403 (por ast); (5) mede os criterios; (6) escreve KH_N1_v404.json, KERNEL_RECIBO_v404.json (contrato KERNEL_RECIBO_R3_2: cada pedra tem declaracoes nomeadas, entao nao ha
modulo de auditoria sem declaracao) e vinculo/CRITERIOS_v404.json (x19 = 'nao': as pedras do recibo sao as DUAS novas, nao a LightNetStandardWedgeDataBGL). A Bancada JA pina a v403 (B12): o ANTES do recibo e' o kernel da v403. Molde: pos_build_kernel_v403.py.   Uso: python -I -B -X utf8 pos_build_kernel_v404.py"""
'''
entrada("pos_build_kernel_v403.py", autoral=True, regras=[
    entre('"""pos_build_kernel_v404.py', "import ast, datetime, hashlib, json, os, re, shutil, subprocess, sys, unicodedata", _DOC_PB, "docstring do pos_build"),
    ("a lista dos modulos novos (preparar_kernel_v404.py) tem de ser so' as TRES pedras (Caminho, Vida, VerdadeAdendo), na ordem do delta", "a lista dos modulos novos (preparar_kernel_v404.py) tem de ser so' as DUAS pedras (ProjecaoTransversalDaMeiaNat, Jo8v32), na ordem do delta", 1),
    ("linha Built/Replayed de CADA modulo novo (as tres pedras), da raiz (TGLExt) e do Audit (TGL.Audit)", "linha Built/Replayed de CADA modulo novo (as duas pedras), da raiz (TGLExt) e do Audit (TGL.Audit)", 1),
    ("(preparacao, 27/10/2026); NAO conferido por verificar_kernel_recibo", "(preparacao, 28/10/2026); NAO conferido por verificar_kernel_recibo", 1),
    ("o build do sandbox C:/t/k404c/final foi INCREMENTAL (copia do kernel v403 compilado + as tres pedras novas; a construcao de 27/10/2026 e' da gerencia c1, logs em v404_kernel; o rito real do Nos compila a frio)", "o build do sandbox C:/t/k404c/final foi INCREMENTAL (copia do kernel v403 compilado + as duas pedras novas; a construcao de 28/10/2026 e' da preparacao, logs em kernel\\\\; o rito real do Nos compila a frio)", 1),
    ("x19='nao': o recibo v404 lista so' as TRES pedras NOVAS (Caminho, Vida, VerdadeAdendo) e a LightNetStandardWedgeDataBGL.lean ", "x19='nao': o recibo v404 lista so' as DUAS pedras NOVAS (ProjecaoTransversalDaMeiaNat, Jo8v32) e a LightNetStandardWedgeDataBGL.lean ", 1),
])

_DOC_CI = '''"""copiar_insumos_v404.py -- copia de BYTES, para a pasta DURAVEL v404\\\\insumos, das fontes que os registros da v404 pinam por sha256: as DUAS pedras (ProjecaoTransversalDaMeiaNat, Jo8v32), a medida do Audit (KH_N1_v404.json), o levantamento «a transicao para a massa» (28/10/2026, fonte
do registro cunhagens_v404) e as NOVE falas de 28/10/2026 (todas do operador; insumos\\\\cunhagens\\\\<sha16>_<nome>). (Nao ha insumo de adendo nesta versao: o ADENDO de 03-04/09 e' da v402.)
Grava MANIFESTO_INSUMOS_v404.json (sha256, origem). As fontes do ACOM (selo pela propria tecnologia) seguem em v399\\\\insumos (o um.py v403 selado as pina por esse caminho). Reexecutavel: o que ja existe e e' igual fica; o que difere aborta.
Roda DEPOIS do pos_build_kernel_v404.py (que gera kernel\\\\KH_N1_v404.json). uso: python -I -B -X utf8 copiar_insumos_v404.py"""
'''
entrada("copiar_insumos_v403.py", autoral=True, regras=[
    entre('"""copiar_insumos_v404.py', "import hashlib, json, os, sys", _DOC_CI, "docstring do copiar_insumos"),
    ('ORIGENS = [(s["insumo"], s["src"]) for s in DL.STONES] + [(DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v404.json"))]',
     'ORIGENS = [(s["insumo"], s["src"]) for s in DL.STONES] + [(DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v404.json")), (os.path.basename(DL.LEVANTAMENTO_ARQ), DL.LEVANTAMENTO_ARQ)]', 1),
])
entrada("purga_v403.py", autoral=True, regras=[])
