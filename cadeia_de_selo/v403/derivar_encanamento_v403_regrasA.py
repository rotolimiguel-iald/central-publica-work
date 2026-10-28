# -*- coding: utf-8 -*-
# regras (lote A) de derivar_encanamento_v403.py: o KERNEL (copiar a base, preparar o sandbox, construir, pos-build, insumos). ORIGEM v402. Mapa: 401 -> 402 (a base selada), 402 -> 403 (esta rodada).
# Escrito pela ferramenta Write (nunca por heredoc: as barras invertidas). Cada regra tem contagem exata; nada e' executado. copiar_pedras_v403.py, gerar_pino_das_pedras_v403.py e copiar_logs_do_kernel_v403.py sao ESCRITOS A MAO.

entrada("copiar_base_v402.py", autoral=True, regras=[
    ("A Bancada de producao JA pina a v402 (B10): nao ha salto de versoes.", "A Bancada de producao JA pina a v402 (B11): nao ha salto de versoes.", 1),
    ("(1925cb691e933ae8; o arquivo manda)", "(6a5033dc3f29324c; o arquivo manda)", 1),
])

_DOC_PK = '''"""preparar_kernel_v403.py -- monta o SANDBOX do kernel da v403 em C:\\\\t\\\\k403c\\\\final (nunca toca o Nos nem C:\\\\t\\\\k402c).
Parte de C:\\\\t\\\\k402c\\\\final (um projeto lake: o kernel do Nos v402 SELADO compilado em .lake/build, com as tres pedras da v402 dentro; sem a pasta probe\\\\ nem os .bak_), e GERA (nao copia) a RAIZ TGLExt.lean a partir da v402 embutida: raiz = v402 + os tres imports das pedras novas
(Caminho, Vida, VerdadeAdendo). O Audit NAO muda nesta versao (AUDIT_PREFIX vazio no delta: ele ja' faz `import TGLExt`, a raiz, que traz os modulos novos; o build de 27/10/2026 foi feito com o Audit inalterado). As pedras sao a fonte do PLANO (v403\\\\pedra\\\\*.lean, copias de bytes das de
v403_kernel\\\\pedras; o sha16 de cada uma e' LIDO na hora da geracao e conferido contra o que o plano deu), copiadas para o sandbox quando diferem. Molde: preparar_kernel_v402.py.
uso: python -I -B -X utf8 preparar_kernel_v403.py [copiar|gerar|conferir]   (copiar = robocopy; gerar = pedras + raiz [+ Audit se o prefixo nao for vazio]; conferir = so' verifica e escreve kernel_modulos_novos_v403.json)"""
'''
entrada("preparar_kernel_v402.py", autoral=True, regras=[
    entre('"""preparar_kernel_v403.py', "import ast, hashlib, json, os, subprocess, sys", _DOC_PK, "docstring do preparar_kernel"),
    ('"/XF", "*.bak_*", "PonteDaEscalaDual*.bak_*", "QuedaSemGeometria*.bak_*", "EsperancaCondicional*.bak_*", "TGLExt.lean.bak_*",', '"/XF", "*.bak_*", "Caminho*.bak_*", "Vida*.bak_*", "VerdadeAdendo*.bak_*", "TGLExt.lean.bak_*", "TGLExt.lean.k403_antes",', 1),
])

_HDR_CK = '''#!/bin/sh
# Constroi o kernel do SANDBOX da v403 (C:\\t\\k403c\\final; nunca o do Nos nem C:\\t\\k402c): um `lake build` INCREMENTAL (a v402 selada, com as tres pedras da v402, ja' esta compilada em .lake/build; as TRES pedras novas, Caminho, Vida e VerdadeAdendo, compilam agora; muda a raiz TGLExt; o Audit e' o da v402, inalterado) + `lake env lean TGL/Audit.lean`.
# Molde: construir_kernel_v402.sh. Logs crus (redirecionamento do bash, UTF-8) em kernel/; pos_build_kernel_v403.py monta o build_full.log no formato do molde e o recibo. A construcao de 27/10/2026 (08:43 a 08:53, rc 0) foi feita no sandbox pela gerencia c1 e os logs dela
# estao em ..\\v403_kernel\\ (copiados em bytes para kernel\\ por copiar_logs_do_kernel_v403.py); este script e' o mesmo comando, para refazer.
'''
entrada("construir_kernel_v402.sh", autoral=True, regras=[
    entre("#!/bin/sh\n", 'K="/c/t/k403c/final"', _HDR_CK, "cabecalho do construir"),
])

_DOC_PB = '''"""pos_build_kernel_v403.py -- DEPOIS de construir_kernel_v403.sh: (1) monta kernel/build_full.log no formato do molde; (2) confere o build (rc, zero erro, zero sorry nas 3 formas do contrato R3.2, 'Build completed successfully',
linha Built/Replayed de cada pedra (Caminho, Vida, VerdadeAdendo), da raiz e do Audit, axiomas no trio, cabecalho dos .olean = Lean 4.31.0); (3) le do log do Audit (SO' dele) as linhas TGL_DECL_SOURCE (declaracao -> modulo emitido
pelo compilador) e o axiom_report EFETIVO com as funcoes do PROPRIO um.py v402 selado (parse_lean_axioms_v394/parse_lean_provenance_v394, extraidas por ast de base_v402\\\\um.py: a MESMA logica que o um.py v403 usara), e deriva
FLAGS_v403.json (as declaracoes NOMEADAS publicas dos modulos novos, na politica da v394, uma serie de chaves por pedra: ext_cam403_NNNN, ext_vid403_NNNN, ext_vad403_NNNN); (4) copia a ARVORE so-fontes para C:\\\\t\\\\k403c\\\\arvore e varre os tokens
proibidos RECURSIVAMENTE com a funcao de varredura do PROPRIO um.py v402 (por ast); (5) mede os criterios; (6) escreve KH_N1_v403.json, KERNEL_RECIBO_v403.json (contrato KERNEL_RECIBO_R3_2: cada pedra tem declaracoes nomeadas, entao nao ha
modulo de auditoria sem declaracao) e vinculo/CRITERIOS_v403.json (x19 = 'nao': as pedras do recibo sao as TRES novas, nao a LightNetStandardWedgeDataBGL). A Bancada JA pina a v402 (B11): o ANTES do recibo e' o kernel da v402. Molde: pos_build_kernel_v402.py.   Uso: python -I -B -X utf8 pos_build_kernel_v403.py"""
'''
entrada("pos_build_kernel_v402.py", autoral=True, regras=[
    entre('"""pos_build_kernel_v403.py', "import ast, datetime, hashlib, json, os, re, shutil, subprocess, sys, unicodedata", _DOC_PB, "docstring do pos_build"),
    ("a lista dos modulos novos (preparar_kernel_v403.py) tem de ser so' as TRES pedras (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional), na ordem do delta", "a lista dos modulos novos (preparar_kernel_v403.py) tem de ser so' as TRES pedras (Caminho, Vida, VerdadeAdendo), na ordem do delta", 1),
    ("mantida na ordem da v403 de 24/10/2026: bandeiras so' nomeadas;", "mantida desde a v401: bandeiras so' nomeadas;", 1),
    ("(preparacao, 26/10/2026); NAO conferido por verificar_kernel_recibo", "(preparacao, 27/10/2026); NAO conferido por verificar_kernel_recibo", 1),
    ("o build do sandbox e' INCREMENTAL (as pedras podem ja' estar compiladas em C:/t/k403/final e C:/t/k402x/final, isoladas; o rito real do Nos compila a frio)", "o build do sandbox C:/t/k403c/final foi INCREMENTAL (copia do kernel v402 compilado + as tres pedras novas; a construcao de 27/10/2026 e' da gerencia c1, logs em v403_kernel; o rito real do Nos compila a frio)", 1),
    ("x19='nao': o recibo v403 lista so' as TRES pedras NOVAS (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) e a LightNetStandardWedgeDataBGL.lean ", "x19='nao': o recibo v403 lista so' as TRES pedras NOVAS (Caminho, Vida, VerdadeAdendo) e a LightNetStandardWedgeDataBGL.lean ", 1),
])

_DOC_CI = '''"""copiar_insumos_v403.py -- copia de BYTES, para a pasta DURAVEL v403\\\\insumos, das fontes que os registros da v403 pinam por sha256: as TRES pedras (Caminho, Vida, VerdadeAdendo), a medida do Audit (KH_N1_v403.json)
e as DUAS falas de 27/10/2026 (ambas do operador; insumos\\\\cunhagens\\\\<sha16>_<nome>). (Nao ha insumo de adendo nesta versao: o ADENDO de 03-04/09 e' da v402.)
Grava MANIFESTO_INSUMOS_v403.json (sha256, origem). As fontes do ACOM (selo pela propria tecnologia) seguem em v399\\\\insumos (o um.py v402 selado as pina por esse caminho). Reexecutavel: o que ja existe e e' igual fica; o que difere aborta.
Roda DEPOIS do pos_build_kernel_v403.py (que gera kernel\\\\KH_N1_v403.json). uso: python -I -B -X utf8 copiar_insumos_v403.py"""
'''
entrada("copiar_insumos_v402.py", autoral=True, regras=[
    entre('"""copiar_insumos_v403.py', "import hashlib, json, os, sys", _DOC_CI, "docstring do copiar_insumos"),
    ('INS = os.path.join(HERE, "insumos"); CUN = os.path.join(INS, "cunhagens"); ADD = os.path.join(INS, "adendo")', 'INS = os.path.join(HERE, "insumos"); CUN = os.path.join(INS, "cunhagens")', 1),
    ("for d in (CUN, ADD):", "for d in (CUN,):", 1),
    entre("# o adendo de 03-04/09: o sha16 que a ORDEM deu", "json.dump(man, open(os.path.join(HERE, \"MANIFESTO_INSUMOS_v403.json\")", "", "o adendo da v402 nao entra nos insumos da v403"),
])
entrada("purga_v402.py", autoral=True, regras=[])
