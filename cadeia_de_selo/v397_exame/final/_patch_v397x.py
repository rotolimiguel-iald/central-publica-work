# -*- coding: utf-8 -*-
"""_patch_v397x.py -- gera simular_arvore_do_nos_v397x.py e exame_pontos_v397x.py a partir dos meus scripts da v396 (exame final v397, 23/10/2026)."""
import os, ast, shutil
F6 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v396_exame\final"
F7 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v397_exame\final"
shutil.copyfile(os.path.join(F6, "simular_arvore_do_nos_v396x.py"), os.path.join(F7, "simular_arvore_do_nos_v397x.py"))
shutil.copyfile(os.path.join(F6, "exame_pontos_v396x.py"), os.path.join(F7, "exame_pontos_v397x.py"))
# --- simular
p = os.path.join(F7, "simular_arvore_do_nos_v397x.py"); s = open(p, encoding="utf-8").read()
rep = [
 ('V = os.path.join(os.path.dirname(os.path.dirname(H)), "v396")   # v396x: a pasta da cadeia v396', 'V = os.path.join(os.path.dirname(os.path.dirname(H)), "v397")   # v397x: a pasta da cadeia v397'),
 ('default=os.path.join(V, "um_v396_candidato.py")', 'default=os.path.join(V, "um_v397_candidato.py")'),
 ("(um.testemunha_estatica_v396(core) if hasattr(um, 'testemunha_estatica_v396') else None)",
  "(um.testemunha_estatica_v396(core) if hasattr(um, 'testemunha_estatica_v396') else None)\n(core.__setitem__('teste_de_veracidade_fase9_v397', um._v392_registro(um._V397_VERACIDADE_SPEC, core)) if hasattr(um, '_V397_VERACIDADE_SPEC') else None)"),
 ("(um._v396_rodar_specs(core) if hasattr(um, '_v396_rodar_specs') else None)",
  "(um._v396_rodar_specs(core) if hasattr(um, '_v396_rodar_specs') else None)\n(um._v397_rodar_specs(core) if hasattr(um, '_v397_rodar_specs') else None)"),
 ('"testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396"):', '"testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397"):'),
 ('um._V396_SPECS if s_["nome"] == "kh_n1_cobertura_v396"', 'um._V397_SPECS if s_["nome"] == "kh_n1_cobertura_v397"'),
 ('"h8_pino_kh_n1_v396_n"', '"h8_pino_kh_n1_v397_n"'),
]
for a, b in rep:
    assert s.count(a) >= 1, a
    s = s.replace(a, b)
s = s.replace('"""simular_arvore_do_nos_v396x.py -- exame final v396 (molde: simular_arvore_do_nos_v395x.py; + testemunha_estatica_v396 e os registros por spec v396).',
              '"""simular_arvore_do_nos_v397x.py -- exame final v397 (molde: simular_arvore_do_nos_v396x.py; + o registro de veracidade (spec) e os registros por spec v397).', 1)
ast.parse(s); open(p + ".tmp", "w", encoding="utf-8").write(s); os.replace(p + ".tmp", p)
# --- exame_pontos
p = os.path.join(F7, "exame_pontos_v397x.py"); s = open(p, encoding="utf-8").read()
rep = [
 ('ap.add_argument("--sandbox", default=os.path.join(C_, "t", "k396c", "final"))', 'ap.add_argument("--sandbox", default=os.path.join(C_, "t", "k397c", "final"))'),
 ('"""exame_pontos_v396x.py -- exame final v396 (c1, modelo forte, 22/10/2026; molde: exame_pontos_v395x.py',
  '"""exame_pontos_v397x.py -- exame final v397 (c1, modelo forte, 23/10/2026; molde: exame_pontos_v396x.py, + o registro teste_de_veracidade_fase9_v397 pela instrucao real do main, a adjacencia ao V1 e os controles negativos dele). Texto do molde: exame final v396 (c1, modelo forte, 22/10/2026; molde: exame_pontos_v395x.py'),
]
for a, b in rep:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
anchor = '# as instrucoes do main da v393 em diante (ate emit_figures), executadas como estao no candidato'
assert s.count(anchor) == 1
bloco = open(os.path.join(F7, "_bloco_veracidade.py"), encoding="utf-8").read()
s = s.replace(anchor, bloco + "\n" + anchor, 1)
old = 'if "testemunha_ponto" in R and not ('
assert s.count(old) == 1
s = s.replace(old, 'if "veracidade_controles_negativos" in R and not (R["veracidade_controles_negativos"].get("todos_os_negativos_recusam") and R["veracidade_controles_negativos"].get("positivo_sela_de_novo")): falsos.append("veracidade_controles")\n'
              'if R.get("veracidade_mexeu_em_chaves_existentes"): falsos.append("veracidade_mexeu")\n'
              'if "veracidade_ponto" in R and not all(R["veracidade_ponto"][k] for k in ("imediatamente_depois_do_print_do_v1", "print_proprio_logo_depois", "antes_do_v389", "v1_try_igual_ao_instalado", "v1_print_igual_ao_instalado")): falsos.append("veracidade_ponto")\n'
              'if "veracidade" in R and not (R["veracidade"]["all_verified"] is True and R["veracidade"]["lido_igual_ao_resultado_original"]): falsos.append("veracidade_registro")\n'
              'if "veracidade_instrucao_real" in R and (R["veracidade_instrucao_real"]["erro"] or R["veracidade_instrucao_real"]["aviso"]): falsos.append("veracidade_instrucao_real")\n' + old, 1)
ast.parse(s); open(p + ".tmp", "w", encoding="utf-8").write(s); os.replace(p + ".tmp", p)
print("ok")
