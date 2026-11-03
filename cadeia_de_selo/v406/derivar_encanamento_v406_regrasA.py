# -*- coding: utf-8 -*-
# regras (lote A) de derivar_encanamento_v406.py: o KERNEL (pos-build, purga). ORIGEM v405. Mapa: 403 -> 405 (a base selada), 405 -> 406 (esta rodada).
# Escrito pela ferramenta Write (nunca por heredoc: as barras invertidas). Cada regra tem contagem exata; nada e' executado. copiar_base_v406.py, copiar_pedras_v406.py, gerar_pino_das_pedras_v406.py, copiar_insumos_v406.py, copiar_k406c.sh, preparar_kernel_v406.py,
# construir_kernel_v406.sh e copiar_logs_do_kernel_v406.py sao ESCRITOS A MAO (a origem do sandbox mudou: o kernel do Nos, nao o sandbox anterior).

_DOC_PB = '''"""pos_build_kernel_v406.py -- DEPOIS de construir_kernel_v406.sh: (1) monta kernel/build_full.log no formato do molde; (2) confere o build (rc, zero erro, zero sorry nas 3 formas do contrato R3.2, 'Build completed successfully',
linha Built/Replayed de cada pedra (PonteDaMassa, MassaTensaoPura, Identidade, ObservadorTerminal, LeiDoDiminuto, TonicaDoHamiltoniano, DiscoDeEuler, PontoZeroDoPsion), da raiz e do Audit, axiomas no trio, cabecalho dos .olean = Lean 4.31.0); (3) le do log do Audit (SO' dele) as linhas TGL_DECL_SOURCE (declaracao -> modulo emitido
pelo compilador) e o axiom_report EFETIVO com as funcoes do PROPRIO um.py v405 selado (parse_lean_axioms_v394/parse_lean_provenance_v394, extraidas por ast de base_v405\\\\um.py: a MESMA logica que o um.py v406 usara), e deriva
FLAGS_v406.json (as declaracoes NOMEADAS publicas dos modulos novos, na politica da v394, uma serie de chaves por pedra: ext_pdm406_NNNN, ext_mtp406_NNNN, ext_idt406_NNNN, ext_obt406_NNNN, ext_ldd406_NNNN, ext_tdh406_NNNN, ext_dde406_NNNN, ext_pzp406_NNNN); (4) copia a ARVORE so-fontes para C:\\\\t\\\\k406c\\\\arvore e varre os tokens
proibidos RECURSIVAMENTE com a funcao de varredura do PROPRIO um.py v405 (por ast); (5) mede os criterios; (6) escreve KH_N1_v406.json, KERNEL_RECIBO_v406.json (contrato KERNEL_RECIBO_R3_2: cada pedra tem declaracoes nomeadas, entao nao ha
modulo de auditoria sem declaracao) e vinculo/CRITERIOS_v406.json (x19 = 'nao': as pedras do recibo sao as OITO novas, nao a LightNetStandardWedgeDataBGL). A Bancada JA pina a v405 (B13): o ANTES do recibo e' o kernel da v405. Molde: pos_build_kernel_v405.py.   Uso: python -I -B -X utf8 pos_build_kernel_v406.py"""
'''
entrada("pos_build_kernel_v405.py", autoral=True, regras=[
    entre('"""pos_build_kernel_v406.py', "import ast, datetime, hashlib, json, os, re, shutil, subprocess, sys, unicodedata", _DOC_PB, "docstring do pos_build"),
    ("a lista dos modulos novos (preparar_kernel_v406.py) tem de ser so' as DUAS pedras (ProjecaoTransversalDaMeiaNat, Jo8v32), na ordem do delta", "a lista dos modulos novos (preparar_kernel_v406.py) tem de ser so' as OITO pedras (PonteDaMassa, MassaTensaoPura, Identidade, ObservadorTerminal, LeiDoDiminuto, TonicaDoHamiltoniano, DiscoDeEuler, PontoZeroDoPsion), na ordem do delta", 1),
    ("linha Built/Replayed de CADA modulo novo (as duas pedras), da raiz (TGLExt) e do Audit (TGL.Audit)", "linha Built/Replayed de CADA modulo novo (as oito pedras), da raiz (TGLExt) e do Audit (TGL.Audit)", 1),
    ("(preparacao, 28/10/2026); NAO conferido por verificar_kernel_recibo", "(preparacao, 01/11/2026); NAO conferido por verificar_kernel_recibo", 1),
    ("o build do sandbox C:/t/k406c/final foi INCREMENTAL (copia do kernel v405 compilado + as duas pedras novas; a construcao de 28/10/2026 e' da preparacao, logs em kernel\\\\; o rito real do Nos compila a frio)", "o build do sandbox C:/t/k406c/final foi INCREMENTAL (copia do kernel do NOS v405 compilado pelo rito de 28/10 + as oito pedras novas; a construcao de 01/11/2026 e' da preparacao, logs em kernel\\\\; o rito real do Nos compila a frio)", 1),
    ("x19='nao': o recibo v406 lista so' as DUAS pedras NOVAS (ProjecaoTransversalDaMeiaNat, Jo8v32) e a LightNetStandardWedgeDataBGL.lean ", "x19='nao': o recibo v406 lista so' as OITO pedras NOVAS (PonteDaMassa, MassaTensaoPura, Identidade, ObservadorTerminal, LeiDoDiminuto, TonicaDoHamiltoniano, DiscoDeEuler, PontoZeroDoPsion) e a LightNetStandardWedgeDataBGL.lean ", 1),
])
entrada("purga_v405.py", autoral=True, regras=[])
