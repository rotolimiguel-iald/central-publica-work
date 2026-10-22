# -*- coding: utf-8 -*-
"""verificar_recibo_pre_selo_real.py (R3.4, 19/10/2026) -- SO LEITURA: confere o recibo pre_selo REAL da v394 (o de R3_4, com o salto v392 -> v393) pelo MESMO caminho que o B(n) pos_selo
usara: conferir_recibo_pre_selo(...) do esboco R3.4 contra a Bancada de PRODUCAO (estado_anterior, so leitura), com o sha do recibo pinado, o selo e o manifesto do kernel da v393
(--selo-anterior / --kernel-manifesto-anterior: as copias de bytes v394/base_v393) e a cadeia de selos. Imprime o resultado (ou a recusa) em JSON; nada e escrito.
uso: python -I -B -X utf8 verificar_recibo_pre_selo_real.py <recibo.json>"""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("sync_r34_real", AQUI / "sincronizar_bancada.py")
MOD = importlib.util.module_from_spec(spec)
sys.modules["sync_r34_real"] = MOD
spec.loader.exec_module(MOD)
rec = Path(sys.argv[1])
BASE393 = MOD.WORK / "cadeia_de_selo" / "v394" / "base_v393"
CH = AQUI / "CADEIA_DE_SELOS_v394.json"
cad = MOD.carregar_cadeia_de_selos(CH, hashlib.sha256(CH.read_bytes()).hexdigest())
canon, _ = MOD.carregar_canonical(MOD.PRODUCAO)
ant = MOD.estado_anterior(MOD.PRODUCAO, canon)
try:
    r = MOD.conferir_recibo_pre_selo(rec, ant, MOD.PRODUCAO, False, hashlib.sha256(rec.read_bytes()).hexdigest(), BASE393 / "um_absoluto_selo.json",
                                     BASE393 / "tgl_kernel_proof_manifest.json", cad)
    out = dict(aceito=True, recibo_sha256=r["sha256"], salto=r["salto"], kernel_manifesto_anterior_sha256=r["kernel_manifesto_anterior_sha256"],
               kernel_anterior=r["kernel_anterior"], bateria=r["bateria"], veredito=r["veredito"], versao=r["versao"],
               bancada_pina=dict(version=ant["version"], deployment_id=ant["deployment_id"], um_py_pinado=ant["um_py_pinado"], seal_sha_pinado=ant["seal_sha_pinado"],
                                 estado=ant["estado_do_contrato_instalado"]))
except MOD.Recusa as exc:
    out = dict(aceito=False, recusa=str(exc))
print(json.dumps(out, ensure_ascii=False, indent=1))
sys.exit(0 if out["aceito"] else 2)
