# -*- coding: utf-8 -*-
# regras (lote E3) de derivar_encanamento_v405.py: a comparacao AST v404 x v405. ORIGEM v404 FINAL (comparar_v403_v404.py). Escrito pela ferramenta Write.
_EXPL = r'''EXPLICACOES = {
    "UM_VERSION": "W01: a constante unica de versao v404 -> v405",
    "_EMBEDDED_KERNEL_FILES": "K00/K01: a raiz TGLExt.lean regenerada (+ os oito imports das pedras; o Audit nao muda) e +8 modulos Lean (as oito pedras com os nomes do operador)",
    "_LEAN_THEOREM_FLAGS": "V01: +%d bandeiras das oito pedras (so' declaracao nomeada)" % NB,
    "prove_external_ladder": "V02: a lista ext_flags ganha as %d bandeiras (a escada %d -> %d)" % (NB, E_ANT, E_NOVA),
    "_ESQUELETO_STONES": "V03: o ledger de pedras ganha as oito pedras da v405",
    "_V404_SPECS": "C13: kh_n1_cobertura_v404 h2/h3/h6 viram pisos e h8 o tamanho minimo (+ errata ao lado); o veredito do registro nao muda",
    "_V394_FORMAL_CONTRACT": EXPL_CONTRATO, "_V394_QUADRATIC_CONTRACT": EXPL_CONTRATO, "_V394_NETWORK_CONTRACT": EXPL_CONTRATO, "_V395_PSIBIT_CONTRACT": EXPL_CONTRATO,
    "_V396_TESTEMUNHA_CONTRACT": EXPL_CONTRATO, "_V398_SONICO_CONTRACT": EXPL_CONTRATO, "_V398_AFINACAO_CONTRACT": EXPL_CONTRATO, "_V401_FALSIDADE_CONTRACT": EXPL_CONTRATO,
    "_V402_CONTRACTS": EXPL_CONTRATO + " nos tres contratos da v402 (ponte, queda, esperanca)", "_V403_CONTRACTS": EXPL_CONTRATO + " nos tres contratos de pedra da v403 (caminho, vida, adendo da verdade; o do gate fica None)",
    "_V404_CONTRACTS": EXPL_CONTRATO + " nos dois contratos de pedra da v404 (projecao, jo8v32; o da errata de F2b fica None)",
    "main": "N00/N01/N02: as chamadas dos oito registros com funcao (depois do jo8v32_v404) e dos specs v405 e as chaves novas do selo (try/AVISO; nada do que existia muda)",
    "build_pt": "W04: as secoes «A massa derivada e a identidade definida» e «A identidade» do artigo PT, antes da secao v404 (o quadro «O Teste da Unica Palavra» do topo NAO muda)",
    "build_en": "W05: the sections «The derived mass and the defined identity» and «The identity» of the EN article, before the v404 section (the box at the top does NOT change)",
    "emit_canonical_md": "W09: a linha «A massa derivada e a identidade definida (v405)» no .md canonico, antes da linha da v404 (o quadro do topo NAO muda)",
}
'''
_NOVOS = r'''NOVOS_ESPERADOS = set(DL.REGISTROS_FUNCAO) | {"v405_ponte_mechanics", "v405_tensao_mechanics", "v405_identidade_mechanics", "v405_observador_mechanics", "v405_diminuto_mechanics", "v405_tonica_mechanics", "v405_disco_mechanics", "v405_psion_mechanics",
                                              "_v405_guarda_frases", "_v405_ensaio_tex", "v405_ga_mechanics", "_v405_ga_registro", "v405_gap_mechanics", "_v405_gap_registro", "_v405_close", "_v405_rel", "_v405_mat_trace", "_v405_mat_mul", "_v405_mat_dagger", "_v405_mat_eye", "_v405_mat_sub", "_v405_mat_norm", "_v405_rot_projector", "_V405_MECANICAS", "_v405_formal", "_v405_registro", "_V405_RECUSA",
                                              "_V405_CONTRACTS", "_V405_TEXTS", "_V405_FONTES", "_V405_VERBATINS2", "_V405_IDENTIDADE_TXT", "_V405_IDENTIDADE_EN_TXT", "_V405_ENSAIO_ORIGINAL_SHA16", "_V405_SPECS", "_V405_NOMES_REGISTROS", "_V405_REGISTROS_FUNCAO", "_v405_rodar_specs"}
'''
entrada("comparar_v403_v404.py", dst="comparar_v404_v405.py", autoral=True, regras=[
    ("Os nos NOVOS esperados sao so' os da v405 (os tres registros com funcao e as duas mecanicas, o leitor da deformacao, o miolo comum, os contratos, os textos, as fontes, as falas, os specs e o rodar_specs).", "Os nos NOVOS esperados sao so' os da v405 (os oito registros com funcao, as oito mecanicas, os auxiliares, a guarda das frases, o renderizador do ensaio, as medidas do Grande Atrator, o miolo comum, os contratos, os textos, as fontes, as falas, o ensaio e a traducao, os specs e o rodar_specs).", 1),
    entre("EXPLICACOES = {\n", "NOVOS_ESPERADOS = {", _EXPL, "as explicacoes da comparacao"),
    entre("NOVOS_ESPERADOS = {", "FUNCOES_QUE_NAO_PODEM_MUDAR = (", _NOVOS, "os nos novos esperados"),
    ('FUNCOES_QUE_NAO_PODEM_MUDAR = ("evaluate_quantum_gravity_closure", "prove_qg_closure_gate", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386")', 'FUNCOES_QUE_NAO_PODEM_MUDAR = ("evaluate_quantum_gravity_closure", "prove_qg_closure_gate", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386", "prove_ga_mass_audit", "prove_joint_coincidence_result_v3", "GA_WINDOW_STATUS")', 1),
    ('# os nos anonimos novos esperados: o `import math as _m404` do bloco da v405', '# os nos anonimos novos esperados: o `import math as _m405` do bloco da v405', 1),
    ('sum("_m404" in x for x in anon_novos_txt) == 1 and sum("_V392_FONTES.update(_V404_FONTES)" in x for x in anon_novos_txt) == 1 and sum("_V392_VERBATINS2.update(_V404_VERBATINS2)" in x for x in anon_novos_txt) == 1', 'sum("_m405" in x for x in anon_novos_txt) == 1 and sum("_V392_FONTES.update(_V405_FONTES)" in x for x in anon_novos_txt) == 1 and sum("_V392_VERBATINS2.update(_V405_VERBATINS2)" in x for x in anon_novos_txt) == 1', 1),
])
