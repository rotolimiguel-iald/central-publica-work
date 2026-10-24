# -*- coding: utf-8 -*-
"""_patch_v398x.py -- gera simular_arvore_do_nos_v398x.py e exame_pontos_v398x.py a partir dos meus scripts da v397 (exame final v398, 23/10/2026)."""
import os, ast, shutil
F7 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v397_exame\final"
F8 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v398_exame\final"
shutil.copyfile(os.path.join(F7, "simular_arvore_do_nos_v397x.py"), os.path.join(F8, "simular_arvore_do_nos_v398x.py"))
shutil.copyfile(os.path.join(F7, "exame_pontos_v397x.py"), os.path.join(F8, "exame_pontos_v398x.py"))
# --- simular
p = os.path.join(F8, "simular_arvore_do_nos_v398x.py"); s = open(p, encoding="utf-8").read()
rep = [
 ('V = os.path.join(os.path.dirname(os.path.dirname(H)), "v397")   # v397x: a pasta da cadeia v397', 'V = os.path.join(os.path.dirname(os.path.dirname(H)), "v398")   # v398x: a pasta da cadeia v398'),
 ('default=os.path.join(V, "um_v397_candidato.py")', 'default=os.path.join(V, "um_v398_candidato.py")'),
 ("(um.testemunha_estatica_v396(core) if hasattr(um, 'testemunha_estatica_v396') else None)\n",
  "(um.testemunha_estatica_v396(core) if hasattr(um, 'testemunha_estatica_v396') else None)\n(um.sonico_v398(core) if hasattr(um, 'sonico_v398') else None)\n(um.afinacao_das_cordas_v398(core) if hasattr(um, 'afinacao_das_cordas_v398') else None)\n"),
 ("(um._v397_rodar_specs(core) if hasattr(um, '_v397_rodar_specs') else None)",
  "(um._v397_rodar_specs(core) if hasattr(um, '_v397_rodar_specs') else None)\n(um._v398_rodar_specs(core) if hasattr(um, '_v398_rodar_specs') else None)"),
 ('"teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397"):', '"teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398"):'),
 ('um._V397_SPECS if s_["nome"] == "kh_n1_cobertura_v397"', 'um._V398_SPECS if s_["nome"] == "kh_n1_cobertura_v398"'),
 ('"h8_pino_kh_n1_v397_n"', '"h8_pino_kh_n1_v398_n"'),
]
for a, b in rep:
    assert s.count(a) >= 1, a
    s = s.replace(a, b)
s = s.replace('"""simular_arvore_do_nos_v397x.py -- exame final v397 (molde: simular_arvore_do_nos_v396x.py; + o registro de veracidade (spec) e os registros por spec v397).',
              '"""simular_arvore_do_nos_v398x.py -- exame final v398 (molde: simular_arvore_do_nos_v397x.py; + sonico_v398, afinacao_das_cordas_v398 e os registros por spec v398).', 1)
ast.parse(s); open(p + ".tmp", "w", encoding="utf-8").write(s); os.replace(p + ".tmp", p)
# --- exame_pontos
p = os.path.join(F8, "exame_pontos_v398x.py"); s = open(p, encoding="utf-8").read()
rep = [
 ('ap.add_argument("--sandbox", default=os.path.join(C_, "t", "k397c", "final"))', 'ap.add_argument("--sandbox", default=os.path.join(C_, "t", "k398c", "final"))'),
 ('"""exame_pontos_v397x.py -- exame final v397 (c1, modelo forte, 23/10/2026; molde: exame_pontos_v396x.py,',
  '"""exame_pontos_v398x.py -- exame final v398 (c1, modelo forte, 23/10/2026; molde: exame_pontos_v397x.py, + os registros sonico_v398 e afinacao_das_cordas_v398 pelas instrucoes reais do main, a adjacencia a testemunha, os numeros recalculados e os controles negativos). Texto do molde: exame final v397 (c1, modelo forte, 23/10/2026; molde: exame_pontos_v396x.py,'),
]
for a, b in rep:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
anchor = '# as instrucoes do main da v393 em diante (ate emit_figures), executadas como estao no candidato'
assert s.count(anchor) == 1
bloco = open(os.path.join(F8, "_bloco_pedras_v398.py"), encoding="utf-8").read()
s = s.replace(anchor, bloco + "\n" + anchor, 1)
old = 'if "testemunha_ponto" in R and not ('
assert s.count(old) == 1
s = s.replace(old, 'if "pedras_controles_negativos" in R and not (R["pedras_controles_negativos"].get("todos_recusam") and R["pedras_controles_negativos"].get("positivos_selam")): falsos.append("pedras_controles")\n'
              'if R.get("pedras_mexeu_em_chaves_existentes"): falsos.append("pedras_mexeu")\n'
              'if "pedras_ponto" in R and not all(R["pedras_ponto"][k] for k in ("sonico_imediatamente_depois_da_testemunha", "afinacao_imediatamente_depois_do_sonico", "antes_do_bloco_v393", "testemunha_depois_do_psibit", "try_testemunha_igual_ao_instalado", "try_psibit_igual_ao_instalado")): falsos.append("pedras_ponto")\n'
              'if "sonico" in R and not (R["sonico"].get("all_verified") is True and R["afinacao"].get("all_verified") is True): falsos.append("pedras_registros")\n'
              'if "numeros_independentes" in R and not all(v is True or (isinstance(v, list) and v) for k, v in R["numeros_independentes"]["iguais_aos_do_registro"].items() if k != "kappa_de_teste"): falsos.append("pedras_numeros")\n'
              'if "pedras_instrucao_real" in R and (R["pedras_instrucao_real"]["erro"] or R["pedras_instrucao_real"]["aviso"]): falsos.append("pedras_instrucao_real")\n' + old, 1)
ast.parse(s); open(p + ".tmp", "w", encoding="utf-8").write(s); os.replace(p + ".tmp", p)
print("ok")
