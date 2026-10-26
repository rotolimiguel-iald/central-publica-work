# -*- coding: utf-8 -*-
"""_gerar_scripts_v399.py -- gera, a partir dos meus scripts do exame v398, os do exame v399: comparar_v398_v399_exame.py, verificar_quadro_v399.py, fidelidade_v399.py,
simular_arvore_do_nos_v399x.py e exame_pontos_v399x.py (substituicoes conferidas: count == 1)."""
import os, ast, shutil
F8 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v398_exame\final"
F9 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v399_exame\final"
def sub(src, rep, minimo=1):
    for a, b in rep:
        assert src.count(a) >= minimo and src.count(a) >= 1, a[:100]
        src = src.replace(a, b)
    return src
# ---------------- comparar
src = open(os.path.join(F8, "comparar_v397_v398_exame.py"), encoding="utf-8").read()
src = sub(src, [
 ('"""comparar_v397_v398_exame.py -- exame final v398 (c1, modelo forte, 23/10/2026): comparacao ESTRUTURAL (AST/literal_eval) entre a v397\ninstalada (A = Nos) e o candidato v398 (B). Molde: comparar_v396_v397_exame.py.',
  '"""comparar_v398_v399_exame.py -- exame final v399 (c1, modelo forte, 24/10/2026): comparacao ESTRUTURAL (AST/literal_eval) entre a v398\ninstalada (A = Nos) e o candidato v399 (B). Molde: comparar_v397_v398_exame.py.'),
 ('if not v.startswith(("TGLExt.Sonico.", "TGLExt.AfinacaoDasCordas."))),', 'if not v.startswith("TGLExt.Testemunho.")),'),
 ('"acrescentadas_por_pedra": {"Sonico": sum(1 for v in add.values() if v.startswith("TGLExt.Sonico.")), "AfinacaoDasCordas": sum(1 for v in add.values() if v.startswith("TGLExt.AfinacaoDasCordas."))},',
  '"acrescentadas_por_pedra": {"Testemunho": sum(1 for v in add.values() if v.startswith("TGLExt.Testemunho."))},'),
 ('for c in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT"):',
  'for c in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT"):'),
 ('for nm in ("_V392_SPECS", "_V393_SPECS", "_V394_SPECS", "_V395_SPECS", "_V396_SPECS", "_V397_SPECS"):', 'for nm in ("_V392_SPECS", "_V393_SPECS", "_V394_SPECS", "_V395_SPECS", "_V396_SPECS", "_V397_SPECS", "_V398_SPECS"):'),
 ('sp6 = {s["nome"]: s for s in lit(dB, "_V398_SPECS")}\nR["v398_specs"]', 'sp6 = {s["nome"]: s for s in lit(dB, "_V399_SPECS")}\nR["v399_specs"]'),
 ('kh6 = sp6.get("kh_n1_cobertura_v398") or {}', 'kh6 = sp6.get("kh_n1_cobertura_v399") or {}'),
 ('R["h8_v398"] =', 'R["h8_v399"] ='),
 ('R["pedras_sha16_embutidas"] = {k: hashlib.sha256(embB.get(k, "").encode("utf-8")).hexdigest()[:16] for k in ("TGLExt/Sonico.lean", "TGLExt/AfinacaoDasCordas.lean")}',
  'R["pedras_sha16_embutidas"] = {k: hashlib.sha256(embB.get(k, "").encode("utf-8")).hexdigest()[:16] for k in ("TGLExt/Testemunho.lean",)}'),
 ('"_V395_PSIBIT_CONTRACT", "_V397_SPECS", "_V396_TESTEMUNHA_CONTRACT", "build_en", "build_pt", "emit_canonical_md", "main", "prove_external_ladder"}',
  '"_V395_PSIBIT_CONTRACT", "_V398_SPECS", "_V396_TESTEMUNHA_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V398_SONICO_CONTRACT", "_unified_main", "build_en", "build_pt", "emit_canonical_md", "main", "prove_external_ladder"}'),
 ('"_V396_FONTES", "_V397_FONTES", "_V398_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2", "_V395_VERBATINS2", "_V396_VERBATINS2", "_V397_VERBATINS2", "_V398_VERBATINS2")}',
  '"_V396_FONTES", "_V397_FONTES", "_V398_FONTES", "_V399_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2", "_V395_VERBATINS2", "_V396_VERBATINS2", "_V397_VERBATINS2", "_V398_VERBATINS2", "_V399_VERBATINS2")}'),
 ('R["colisoes_v398"] = {"fontes": sorted(FB["_V398_FONTES"] & (FB["_V392_FONTES"] | FB["_V393_FONTES"] | FB["_V394_FONTES"] | FB["_V395_FONTES"] | FB["_V396_FONTES"] | FB["_V397_FONTES"])),\n                      "falas": sorted(FB["_V398_VERBATINS2"] & (FB["_V392_VERBATINS2"] | FB["_V393_VERBATINS2"] | FB["_V394_VERBATINS2"] | FB["_V395_VERBATINS2"] | FB["_V396_VERBATINS2"] | FB["_V397_VERBATINS2"]))}',
  'R["colisoes_v399"] = {"fontes": sorted(FB["_V399_FONTES"] & (FB["_V392_FONTES"] | FB["_V393_FONTES"] | FB["_V394_FONTES"] | FB["_V395_FONTES"] | FB["_V396_FONTES"] | FB["_V397_FONTES"] | FB["_V398_FONTES"])),\n                      "falas": sorted(FB["_V399_VERBATINS2"] & (FB["_V392_VERBATINS2"] | FB["_V393_VERBATINS2"] | FB["_V394_VERBATINS2"] | FB["_V395_VERBATINS2"] | FB["_V396_VERBATINS2"] | FB["_V397_VERBATINS2"] | FB["_V398_VERBATINS2"]))}'),
 ('"_v397_rodar_specs", "_v397_quadro_tex", "_v397_quadro_md", "_v397_atomos", "_v397_linha_de_maquina", "_v397_fmt", "_v397_num", "_v394_rodar_specs"):',
  '"_v397_rodar_specs", "_v397_quadro_tex", "_v397_quadro_md", "_v397_atomos", "_v397_linha_de_maquina", "_v397_fmt", "_v397_num", "_v394_rodar_specs",\n          "sonico_v398", "afinacao_das_cordas_v398", "v398_sonico_mechanics", "v398_afinacao_mechanics", "_v398_formal", "_v398_beta", "_v398_h2", "_v398_bernoulli", "_v398_bernoulli_poly", "_v398_rodar_specs"):'),
 ('for f in ("_V397_VERACIDADE_SPEC", "_V397_FONTES", "_V397_VERBATINS2", "_V397_FRASE_444", "_V397_CHAVES_NUM", "_V396_SPECS", "_V395_SPECS", "_V394_SPECS", "_V393_SPECS", "_V392_SPECS", "_V392_FONTES", "_V392_VERBATINS2"):',
  'for f in ("_V397_VERACIDADE_SPEC", "_V397_FONTES", "_V397_VERBATINS2", "_V397_FRASE_444", "_V397_CHAVES_NUM", "_V396_SPECS", "_V395_SPECS", "_V394_SPECS", "_V393_SPECS", "_V392_SPECS", "_V392_FONTES", "_V392_VERBATINS2", "_V398_VERBATINS2", "_V398_FONTES", "_V398_SONICO_TEXT", "_V398_AFINACAO_TEXT", "_V397_SPECS"):'),
 ('for f in ("build_pt", "build_en", "emit_canonical_md", "main"):', 'for f in ("build_pt", "build_en", "emit_canonical_md", "main", "_unified_main"):'),
])
ast.parse(src); open(os.path.join(F9, "comparar_v398_v399_exame.py"), "w", encoding="utf-8").write(src)
# ---------------- verificar_quadro
src = open(os.path.join(F8, "verificar_quadro_v398.py"), "rb").read().decode("utf-8")
src = sub(src, [('cadeia_de_selo\\v398"', 'cadeia_de_selo\\v399"'), ('"dry_v398"', '"dry_v399"'), ('"dry_v398_pt.txt"', '"dry_v399_pt.txt"'), ('"dry_v398_en.txt"', '"dry_v399_en.txt"'),
                ('"dry_v398_var_%s.txt" % lang', '"dry_v399_var_%s.txt" % lang'), ('"harness_saida_v398", "fechar_sandbox_resultado", "handoff-v398-custodia.md")', '"harness_saida_v399", "fechar_sandbox_resultado", "handoff-v399-custodia.md")'),
                ('"VERIFICACAO_QUADRO_v398.json"', '"VERIFICACAO_QUADRO_v399.json"')])
ast.parse(src); open(os.path.join(F9, "verificar_quadro_v399.py"), "w", encoding="utf-8").write(src)
# ---------------- simular / exame_pontos
shutil.copyfile(os.path.join(F8, "simular_arvore_do_nos_v398x.py"), os.path.join(F9, "simular_arvore_do_nos_v399x.py"))
shutil.copyfile(os.path.join(F8, "exame_pontos_v398x.py"), os.path.join(F9, "exame_pontos_v399x.py"))
p = os.path.join(F9, "simular_arvore_do_nos_v399x.py"); s = open(p, encoding="utf-8").read()
s = sub(s, [
 ('V = os.path.join(os.path.dirname(os.path.dirname(H)), "v398")   # v398x: a pasta da cadeia v398', 'V = os.path.join(os.path.dirname(os.path.dirname(H)), "v399")   # v399x: a pasta da cadeia v399'),
 ('default=os.path.join(V, "um_v398_candidato.py")', 'default=os.path.join(V, "um_v399_candidato.py")'),
 ("(um.afinacao_das_cordas_v398(core) if hasattr(um, 'afinacao_das_cordas_v398') else None)\n",
  "(um.afinacao_das_cordas_v398(core) if hasattr(um, 'afinacao_das_cordas_v398') else None)\n(um.selo_acom_v399(core) if hasattr(um, 'selo_acom_v399') else None)\n(um.declaracao_do_operador_v399(core) if hasattr(um, 'declaracao_do_operador_v399') else None)\n"),
 ("(um._v398_rodar_specs(core) if hasattr(um, '_v398_rodar_specs') else None)", "(um._v398_rodar_specs(core) if hasattr(um, '_v398_rodar_specs') else None)\n(um._v399_rodar_specs(core) if hasattr(um, '_v399_rodar_specs') else None)"),
 ('"sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398"):', '"sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399"):'),
 ('um._V398_SPECS if s_["nome"] == "kh_n1_cobertura_v398"', 'um._V399_SPECS if s_["nome"] == "kh_n1_cobertura_v399"'),
 ('"h8_pino_kh_n1_v398_n"', '"h8_pino_kh_n1_v399_n"'),
])
s = s.replace('"""simular_arvore_do_nos_v398x.py -- exame final v398 (molde: simular_arvore_do_nos_v397x.py; + sonico_v398, afinacao_das_cordas_v398 e os registros por spec v398).',
              '"""simular_arvore_do_nos_v399x.py -- exame final v399 (molde: simular_arvore_do_nos_v398x.py; + selo_acom_v399, declaracao_do_operador_v399 e os registros por spec v399).', 1)
ast.parse(s); open(p, "w", encoding="utf-8").write(s)
p = os.path.join(F9, "exame_pontos_v399x.py"); s = open(p, encoding="utf-8").read()
s = sub(s, [('ap.add_argument("--sandbox", default=os.path.join(C_, "t", "k398c", "final"))', 'ap.add_argument("--sandbox", default=os.path.join(C_, "t", "k399c", "final"))'),
            ('"""exame_pontos_v398x.py -- exame final v398 (c1, modelo forte, 23/10/2026; molde: exame_pontos_v397x.py,', '"""exame_pontos_v399x.py -- exame final v399 (c1, modelo forte, 24/10/2026; molde: exame_pontos_v398x.py, + o selo ACOM e a declaracao do operador pelas instrucoes reais do main, os controles negativos deles, D4 e o sidecar). Texto do molde: exame final v398 (c1, modelo forte, 23/10/2026; molde: exame_pontos_v397x.py,')])
anchor = '# as instrucoes do main da v393 em diante (ate emit_figures), executadas como estao no candidato'
assert s.count(anchor) == 1
bloco = open(os.path.join(F9, "_bloco_v399.py"), encoding="utf-8").read()
s = s.replace(anchor, bloco + "\n" + anchor, 1)
old = 'if "pedras_controles_negativos" in R and not ('
assert s.count(old) == 1
s = s.replace(old, 'if "v399_controles_negativos" in R and not (R["v399_controles_negativos"].get("todos_recusam") and R["v399_controles_negativos"].get("positivos_selam")): falsos.append("v399_controles")\n'
              'if R.get("v399_mexeu_em_chaves_existentes"): falsos.append("v399_mexeu")\n'
              'if "v399_ponto" in R and not all(R["v399_ponto"][k] for k in ("selo_imediatamente_depois_da_afinacao", "declaracao_imediatamente_depois_do_selo", "antes_do_bloco_v393", "try_afinacao_igual_ao_instalado", "sidecar_no_unified_main_depois_da_ultima_escrita_do_selo")): falsos.append("v399_ponto")\n'
              'if "selo_acom" in R and not (R["selo_acom"].get("all_verified") is True and R["declaracao"].get("all_verified") is True): falsos.append("v399_registros")\n'
              'if "v399_instrucao_real" in R and (R["v399_instrucao_real"]["erro"] or R["v399_instrucao_real"]["aviso"]): falsos.append("v399_instrucao_real")\n'
              'if "v399_d4" in R and not R["v399_d4"].get("ok"): falsos.append("v399_d4")\n'
              'if "v399_sidecar" in R and not R["v399_sidecar"].get("ok"): falsos.append("v399_sidecar")\n' + old, 1)
ast.parse(s); open(p, "w", encoding="utf-8").write(s)
print("ok")
