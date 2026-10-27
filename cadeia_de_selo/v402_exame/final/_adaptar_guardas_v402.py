# -*- coding: utf-8 -*-
"""_adaptar_guardas_v402.py -- gera guardas_e_bn_v402.py a partir do molde da v401 (troca de ancoras conferidas uma a uma)."""
import os
H = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(H, "..", "..", "v401_exame", "final", "guardas_e_bn_v401.py"), encoding="utf-8").read()
rep = [
    ('guardas_e_bn_v401.py -- exame final v401 (c1, 25/10/2026).', 'guardas_e_bn_v402.py -- exame final v402 (examinador final unico, 27/10/2026; molde: guardas_e_bn_v401.py).'),
    ('uso: python -I -B -X utf8 guardas_e_bn_v401.py', 'uso: python -I -B -X utf8 guardas_e_bn_v402.py  [v402: Nos real v401; candidato v402; manifesto sintetizado com as 3 pedras e as 146 constantes do meu audit; producao B10-v401; pre_selo 36aaf247; T17 v402]'),
    ('V401 = os.path.join(WK, "cadeia_de_selo", "v401")', 'V401 = os.path.join(WK, "cadeia_de_selo", "v402")   # (nome herdado do molde: aqui e o pacote v402)'),
    ('PINOS_BN_v401.json', 'PINOS_BN_v402.json'),
    ('"esboco_r35_exame_bn401"', '"esboco_r35_exame_bn402"'),
    ('for v in ("v400", "v401"):', 'for v in ("v401", "v402"):'),
    ('selo400_raw', 'seloA_raw'), ('selo400', 'seloA'), ('core400_raw', 'coreA_raw'), ('kman400', 'kmanA'),
    ('nomes_audit = [l.split("\\t")[1] for l in open(os.path.join(HERE, "auditoria_falsidade.log"), encoding="utf-8") if l.startswith("FDI_AX\\t")]\nassert len(nomes_audit) == 22, len(nomes_audit)',
     'nomes_audit = [l.split("\\t")[2] for l in open(os.path.join(HERE, "auditoria_v402.log"), encoding="utf-8") if l.startswith("V402_AX\\t")]\nassert len(nomes_audit) == 146, len(nomes_audit)'),
    ('kman401', 'kmanB'),
    ('ff["TGLExt/FalsidadeDaInercia.lean"] = KR["pedras"][0]["sha256"]; ff["TGLExt.lean"] = KR["raiz"]["sha256_depois"]; ff["TGL/Audit.lean"] = KR["audit"]["sha256_depois"]',
     'for _p, _m in zip(KR["pedras"], ("TGLExt/PonteDaEscalaDual.lean", "TGLExt/QuedaSemGeometria.lean", "TGLExt/EsperancaCondicional.lean")):\n    ff[_m] = _p["sha256"]\nff["TGLExt.lean"] = KR["raiz"]["sha256_depois"]; ff["TGL/Audit.lean"] = KR["audit"]["sha256_depois"]'),
    ('"impressao_antes_v400"', '"impressao_antes_v401"'),
    ('def montar(nome, um_bytes, versao="v401"', 'def montar(nome, um_bytes, versao="v402"'),
    ('def ler(nome, um_bytes, versao="v401"', 'def ler(nome, um_bytes, versao="v402"'),
    ('R["ler_nos_candidato_v401"], NOS_INFO', 'R["ler_nos_candidato_v402"], NOS_INFO'),
    ("b'\\r\\nUM_VERSION = \"v401\"\\r\\n'", "b'\\r\\nUM_VERSION = \"v402\"\\r\\n'"),
    ('s.__setitem__("um_version", "v400")', 's.__setitem__("um_version", "v401")'),
    ('SELO_ANT = PINOS["selo_anterior_v400"]["path"]; KMAN_ANT = PINOS["kernel_manifesto_anterior_v400"]["path"]\nassert shaf(SELO_ANT) == PINOS["selo_anterior_v400"]["sha256"] and shaf(KMAN_ANT) == PINOS["kernel_manifesto_anterior_v400"]["sha256"]\nR["selo_anterior_v400_e_o_do_nos"]',
     'SELO_ANT = PINOS["selo_anterior_v401"]["path"]; KMAN_ANT = PINOS["kernel_manifesto_anterior_v401"]["path"]\nassert shaf(SELO_ANT) == PINOS["selo_anterior_v401"]["sha256"] and shaf(KMAN_ANT) == PINOS["kernel_manifesto_anterior_v401"]["sha256"]\nR["selo_anterior_v401_e_o_do_nos"]'),
    ('("selo_anterior_e_o_da_v399", (rps_p, ant, Path(PROD), False, PINOS["recibo_pre_selo"]["sha256"], os.path.join(V401, "..", "v400", "base_v399", "um_absoluto_selo.json"), KMAN_ANT, None))',
     '("selo_anterior_e_o_da_v400", (rps_p, ant, Path(PROD), False, PINOS["recibo_pre_selo"]["sha256"], os.path.join(V401, "..", "v401", "base_v400", "um_absoluto_selo.json"), KMAN_ANT, None))'),
    ('crit = MOD.carregar_criterios(CRI, PINOS["criterios"]["sha256"], "v401")\nok17, det17, _ = MOD.verificar_kernel_recibo(KRP, "v401"', 'crit = MOD.carregar_criterios(CRI, PINOS["criterios"]["sha256"], "v402")\nok17, det17, _ = MOD.verificar_kernel_recibo(KRP, "v402"'),
    ('ok, det, _ = MOD.verificar_kernel_recibo(p, "v401", NOS_INFO, None, None, True, c)', 'ok, det, _ = MOD.verificar_kernel_recibo(p, "v402", NOS_INFO, None, None, True, c)'),
    ('c["esperados"].__setitem__("j1_teoremas", 19)', 'c["esperados"].__setitem__("j1_teoremas", 105)'),
    ('R["veredito"] = {"nos_real_v400_passa": R["ler_nos_nos_real_v400"]["passou"], "nos_real_como_v401_recusa": not R["ler_nos_nos_real_v401"]["passou"],\n                 "candidato_passa_ler_nos": R["ler_nos_candidato_v401"]["passou"] and R["ler_nos_candidato_v401"]["alpha"]["n_linhas_nao_indentadas"] == 1 and R["ler_nos_candidato_v401"]["alpha"]["n_reatribuicoes_indentadas"] == 0,',
     'R["veredito"] = {"nos_real_v401_passa": R["ler_nos_nos_real_v401"]["passou"], "nos_real_como_v402_recusa": not R["ler_nos_nos_real_v402"]["passou"],\n                 "candidato_passa_ler_nos": R["ler_nos_candidato_v402"]["passou"] and R["ler_nos_candidato_v402"]["alpha"]["n_linhas_nao_indentadas"] == 1 and R["ler_nos_candidato_v402"]["alpha"]["n_reatribuicoes_indentadas"] == 0,'),
    ('"bancada_pina_B9_v400": R["producao"]["deployment_id"] == "B9-v400-20261024-R1" and R["producao"]["version"] == "v400",', '"bancada_pina_B10_v401": R["producao"]["deployment_id"] == "B10-v401-20261025-R1" and R["producao"]["version"] == "v401",'),
    ('GUARDAS_E_BN_v401.json', 'GUARDAS_E_BN_v402.json'),
    ('for k in ("ler_nos_nos_real_v400", "ler_nos_nos_real_v401", "ler_nos_candidato_v401",', 'for k in ("ler_nos_nos_real_v401", "ler_nos_nos_real_v402", "ler_nos_candidato_v402",'),
    ('R["t17_variante_sem_a_pedra_no_recibo"] = variante("sem_pedra", lambda k: k.__setitem__("pedras", []))',
     'R["t17_variante_sem_a_pedra_no_recibo"] = variante("sem_pedra", lambda k: k.__setitem__("pedras", []))\nR["t17_variante_uma_pedra_a_menos"] = variante("uma_pedra_a_menos", lambda k: k["pedras"].pop())'),
    ('"t17_variantes_recusam": not R["t17_variante_declaracao_a_menos"]["passou"] and not R["t17_variante_criterio_esperado_errado"]["passou"] and not R["t17_variante_sem_a_pedra_no_recibo"]["passou"],',
     '"t17_variantes_recusam": not R["t17_variante_declaracao_a_menos"]["passou"] and not R["t17_variante_criterio_esperado_errado"]["passou"] and not R["t17_variante_sem_a_pedra_no_recibo"]["passou"] and not R["t17_variante_uma_pedra_a_menos"]["passou"],'),
    ('"t17_variante_sem_a_pedra_no_recibo", "producao_inalterada_por_este_exame"', '"t17_variante_sem_a_pedra_no_recibo", "t17_variante_uma_pedra_a_menos", "t17_controle_sandbox", "producao_inalterada_por_este_exame"'),
]
for a, b in rep:
    assert s.count(a) >= 1, ("ancora", a[:90])
    s = s.replace(a, b)
open(os.path.join(H, "guardas_e_bn_v402.py"), "w", encoding="utf-8", newline="\n").write(s)
print("ok; linhas com v400 restantes:", [l.strip()[:140] for l in s.splitlines() if "v400" in l])
