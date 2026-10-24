# -*- coding: utf-8 -*-
"""_gerar_scripts_v398.py -- gera, a partir dos meus scripts do exame v397, os do exame v398: comparar_v397_v398_exame.py e verificar_quadro_v398.py
(as substituicoes sao conferidas uma a uma: count == 1)."""
import os, ast
F7 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v397_exame\final"
F8 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v398_exame\final"
# ---------------- comparar
src = open(os.path.join(F7, "comparar_v396_v397_exame.py"), encoding="utf-8").read()
rep = [
 ('"""comparar_v395_v396_exame.py -- exame final v396 (c1, modelo forte, 22/10/2026): comparacao ESTRUTURAL (AST/literal_eval) entre a v395\ninstalada (A = Nos) e o candidato v396 (B).',
  '"""comparar_v397_v398_exame.py -- exame final v398 (c1, modelo forte, 23/10/2026): comparacao ESTRUTURAL (AST/literal_eval) entre a v397\ninstalada (A = Nos) e o candidato v398 (B). Molde: comparar_v396_v397_exame.py.'),
 ('"acrescentadas_fora_da_pedra": sorted(v for v in add.values() if not v.startswith("TGLExt.Token.")),',
  '"acrescentadas_fora_da_pedra": sorted(v for v in add.values() if not v.startswith(("TGLExt.Sonico.", "TGLExt.AfinacaoDasCordas."))),\n                  "acrescentadas_por_pedra": {"Sonico": sum(1 for v in add.values() if v.startswith("TGLExt.Sonico.")), "AfinacaoDasCordas": sum(1 for v in add.values() if v.startswith("TGLExt.AfinacaoDasCordas."))},'),
 ('for nm in ("_V392_SPECS", "_V393_SPECS", "_V394_SPECS", "_V395_SPECS", "_V396_SPECS"):', 'for nm in ("_V392_SPECS", "_V393_SPECS", "_V394_SPECS", "_V395_SPECS", "_V396_SPECS", "_V397_SPECS"):'),
 ('sp6 = {s["nome"]: s for s in lit(dB, "_V397_SPECS")}\nR["v397_specs"]', 'sp6 = {s["nome"]: s for s in lit(dB, "_V398_SPECS")}\nR["v398_specs"]'),
 ('kh6 = sp6.get("kh_n1_cobertura_v397") or {}', 'kh6 = sp6.get("kh_n1_cobertura_v398") or {}'),
 ('R["h8_v397"] =', 'R["h8_v398"] ='),
 ('R["pedra_sha16_embutida"] = hashlib.sha256(embB.get("TGLExt/Token.lean", "").encode("utf-8")).hexdigest()[:16]',
  'R["pedras_sha16_embutidas"] = {k: hashlib.sha256(embB.get(k, "").encode("utf-8")).hexdigest()[:16] for k in ("TGLExt/Sonico.lean", "TGLExt/AfinacaoDasCordas.lean")}'),
 ('"_V395_PSIBIT_CONTRACT", "_V396_SPECS", "_V396_TESTEMUNHA_CONTRACT", "build_en", "build_pt", "emit_canonical_md", "main", "prove_external_ladder"}',
  '"_V395_PSIBIT_CONTRACT", "_V397_SPECS", "_V396_TESTEMUNHA_CONTRACT", "build_en", "build_pt", "emit_canonical_md", "main", "prove_external_ladder"}'),
 ('"_V396_FONTES", "_V397_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2", "_V395_VERBATINS2", "_V396_VERBATINS2", "_V397_VERBATINS2")}',
  '"_V396_FONTES", "_V397_FONTES", "_V398_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2", "_V395_VERBATINS2", "_V396_VERBATINS2", "_V397_VERBATINS2", "_V398_VERBATINS2")}'),
 ('R["colisoes_v397"] = {"fontes": sorted(FB["_V397_FONTES"] & (FB["_V392_FONTES"] | FB["_V393_FONTES"] | FB["_V394_FONTES"] | FB["_V395_FONTES"] | FB["_V396_FONTES"])),\n                      "falas": sorted(FB["_V397_VERBATINS2"] & (FB["_V392_VERBATINS2"] | FB["_V393_VERBATINS2"] | FB["_V394_VERBATINS2"] | FB["_V395_VERBATINS2"] | FB["_V396_VERBATINS2"]))}',
  'R["colisoes_v398"] = {"fontes": sorted(FB["_V398_FONTES"] & (FB["_V392_FONTES"] | FB["_V393_FONTES"] | FB["_V394_FONTES"] | FB["_V395_FONTES"] | FB["_V396_FONTES"] | FB["_V397_FONTES"])),\n                      "falas": sorted(FB["_V398_VERBATINS2"] & (FB["_V392_VERBATINS2"] | FB["_V393_VERBATINS2"] | FB["_V394_VERBATINS2"] | FB["_V395_VERBATINS2"] | FB["_V396_VERBATINS2"] | FB["_V397_VERBATINS2"]))}'),
 ('"hubble_ratio_opening_v388", "v396_static_witness_mechanics", "rede_fock_v394", "regra_quadratica_v394", "tempo_frequencia_v394"):\n    if f in dA and f in dB:\n        R.setdefault("funcoes_seladas_iguais", {})[f] = ast.dump(dA[f]) == ast.dump(dB[f])',
  '"hubble_ratio_opening_v388", "v396_static_witness_mechanics", "rede_fock_v394", "regra_quadratica_v394", "tempo_frequencia_v394",\n          "_v397_rodar_specs", "_v397_quadro_tex", "_v397_quadro_md", "_v397_atomos", "_v397_linha_de_maquina", "_v397_fmt", "_v397_num", "_v394_rodar_specs"):\n    if f in dA and f in dB:\n        R.setdefault("funcoes_seladas_iguais", {})[f] = ast.dump(dA[f]) == ast.dump(dB[f])\nfor f in ("_V397_VERACIDADE_SPEC", "_V397_FONTES", "_V397_VERBATINS2", "_V397_FRASE_444", "_V397_CHAVES_NUM", "_V396_SPECS", "_V395_SPECS", "_V394_SPECS", "_V393_SPECS", "_V392_SPECS", "_V392_FONTES", "_V392_VERBATINS2"):\n    if f in dA and f in dB:\n        R.setdefault("dados_selados_iguais", {})[f] = ast.dump(dA[f]) == ast.dump(dB[f])'),
]
for a, b in rep:
    assert src.count(a) == 1, a[:90]
    src = src.replace(a, b)
ast.parse(src); open(os.path.join(F8, "comparar_v397_v398_exame.py"), "w", encoding="utf-8").write(src)
# ---------------- verificar_quadro
src = open(os.path.join(F7, "verificar_quadro.py"), "rb").read().decode("utf-8")
rep = [('cadeia_de_selo\\v397"', 'cadeia_de_selo\\v398"'),
       ('for lang, fn in (("pt", "dry_v397_pt.txt"), ("en", "dry_v397_en.txt")):', 'for lang, fn in (("pt", "dry_v398_pt.txt"), ("en", "dry_v398_en.txt")):'),
       ('"dry_v397_var_%s.txt" % lang', '"dry_v398_var_%s.txt" % lang'),
       ('"harness_saida_v397", "fechar_sandbox_resultado", "handoff-v397-custodia.md")', '"harness_saida_v398", "fechar_sandbox_resultado", "handoff-v398-custodia.md")'),
       ('"VERIFICACAO_QUADRO.json"', '"VERIFICACAO_QUADRO_v398.json"')]
for a, b in rep:
    assert src.count(a) >= 1, a[:90]
    src = src.replace(a, b)
ast.parse(src); open(os.path.join(F8, "verificar_quadro_v398.py"), "w", encoding="utf-8").write(src)
print("ok")
