# -*- coding: utf-8 -*-
"""_teste_mecanica_v410.py -- (claude-construtor-v410, 06/11/2026) teste RAPIDO, fora do ensaio: executa o bloco v410_pins.py (o que o candidato embute) com as funcoes herdadas da v409 injetadas e um core FALSO,
para ver os valores CALCULADOS das checagens de brinquedo (c3-c10, c14, c15). As checagens que leem o kernel do rito (c1, c2, c11, c12) falham aqui por construcao: o ensaio a seco as confere de verdade."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guarda_frases_v410 as GF  # noqa: E402
import delta_v410 as DL  # noqa: E402
H = os.path.dirname(os.path.abspath(__file__))
ns = {"_v409_sat": GF._rt9._v409_sat, "_v409_guarda_frases": GF._rt9._v409_guarda_frases, "_v392_guarda_texto": GF.GP.violacoes, "_EMBEDDED_KERNEL_FILES": {},
      "_V392_FONTES": {}, "_V392_VERBATINS2": {}, "_v392_registro": None}
ALFA = DL.D9.D8.D7.ALPHA_FINE_CODATA_2018 if hasattr(DL.D9.D8.D7, "ALPHA_FINE_CODATA_2018") else None
exec(compile(open(os.path.join(H, "v410_pins.py"), encoding="utf-8").read(), "v410_pins.py", "exec"), ns)
c_ = ns["_V410_IALD2_CONTRACT"]
import ast  # noqa: E402
um = open(os.path.join(H, "base_v409", "um.py"), encoding="utf-8").read()
t = ast.parse(um)
alfa = [ast.literal_eval(n.value) for n in t.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "SEALED_CODATA_ALPHA"][0]
ns["SEALED_CODATA_ALPHA"] = alfa
ns["_v376_same_alpha_literal"] = lambda: True
beta = alfa * math.sqrt(math.e)
core = {"beta": beta, "kernel_formalization": {}, "external_ladder": {}, "qg_closure": {"gate": {"verdict": c_["baseline"]["gate_verdict"]}}}
r = ns["v410_iald2_mechanics"](beta, core, c_)
print(json.dumps([(c["id"], c["ok"]) for c in r["checks"]]))
v = r["values"]
print({k: v[k] for k in ("leitor_do_codigo", "iald_ao_quadrado", "reler", "primeira_leitura", "resolver_verificar", "instancia_sim", "instancia_nao", "signo_do_nome", "signo_do_par", "representacao_de_beta")})
print("guarda sobre o texto do registro:", GF.RT._v410_guarda_frases(json.dumps(ns["_V410_IALD2_TEXT"], ensure_ascii=False))[:3])
