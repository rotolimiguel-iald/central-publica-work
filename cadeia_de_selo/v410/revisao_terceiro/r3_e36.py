# -*- coding: utf-8 -*-
"""Revisor v410 R3: a regra 'E36 sempre com a clausula do limite na mesma folha' (c8): a frase EXATA da E36 (PT e EN) num texto do registro SEM a clausula e' recusada? e COM a clausula e' aceita?"""
import importlib.util, json, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v410_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev"] = m; spec.loader.exec_module(m)
core = json.load(open(R + "dry_v410/core_ensaio.json", encoding="utf-8"))["core"]
c = m._V410_AESCALA_CONTRACT; tx = m._V410_AESCALA_TEXT; sv = list(tx["diz"])
def run():
    core.pop("a_escala_v410", None); r = m.a_escala_v410(core); core.pop("a_escala_v410", None); return r["all_verified"], [(x["id"], x["ok"]) for x in r["mechanics"]["checks"] if not x["ok"]]
print("base:", run())
for nome, fr in (("E36 PT exata", c["frase_e36_pt"]), ("E36 EN exata", c["frase_e36_en"]), ("reconstroi PT exata", c["frase_reconstroi_pt"]), ("tetelestai PT exata", c["frase_tetelestai_pt"]), ("dispositivo PT exata", c["frase_dispositivo_pt"]), ("ACOM Mirror sem [PILOTO][SIM]", "o runner do ACOM Mirror valida o Tetelestai em computacao"), ("ACOM Mirror com desempenho", "o runner do ACOM Mirror [PILOTO][SIM] nada ali valida fisica e passa 22 de 22 testes")):
    tx["diz"] = sv + [fr]; print("%-34s SEM clausula ->" % nome, run())
    tx["diz"] = sv + [fr + " " + c["clausula_z_pt"] + " " + c["clausula_z_en"]]; print("%-34s COM clausula ->" % nome, run())
tx["diz"] = sv
print("restaurado:", run())
print("frase_e36_pt:", c["frase_e36_pt"][:300])
