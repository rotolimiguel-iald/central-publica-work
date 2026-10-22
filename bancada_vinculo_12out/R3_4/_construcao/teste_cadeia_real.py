# -*- coding: utf-8 -*-
"""teste de construcao (R3.4): a cadeia REAL v392 -> v393 contra a Bancada de producao e o Nos reais (SO LEITURA). Importa o esboco como modulo."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("sync_r34", AQUI / "sincronizar_bancada.py")
MOD = importlib.util.module_from_spec(spec)
sys.modules["sync_r34"] = MOD
spec.loader.exec_module(MOD)
CH = AQUI / "CADEIA_DE_SELOS_v394.json"
sha = hashlib.sha256(CH.read_bytes()).hexdigest()
cad = MOD.carregar_cadeia_de_selos(CH, sha)
print("cadeia ok:", cad["versoes"], cad["n_elos"], [l["registro_sha256"][:16] for l in cad["ligacoes"]])
canon, _ = MOD.carregar_canonical(MOD.PRODUCAO)
ant = MOD.estado_anterior(MOD.PRODUCAO, canon)
print("bancada:", ant["version"], ant["um_py_pinado"][:16], ant["seal_sha_pinado"][:16], ant["estado_do_contrato_instalado"])
MOD.conferir_cadeia_com_a_bancada(cad, ant)
print("inicio confere com a Bancada")
nos = MOD.ler_nos(MOD.NOS_PADRAO, "v393")
MOD.conferir_cadeia_com_o_fim(cad, "v393", nos["um_py"]["sha256"], nos["selo"]["sha256"], nos["kernel"]["sha256"], "o Nos lido agora")
print("fim confere com o Nos v393")
salto = MOD.montar_salto(cad, ant)
print(json.dumps(salto, indent=1)[:1800])
