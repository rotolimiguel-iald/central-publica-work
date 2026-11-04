import importlib.util, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
spec = importlib.util.spec_from_file_location("pos_treino_rev7", R + "orquestrador/pos_treino_v407.py"); O = importlib.util.module_from_spec(spec); sys.modules["pos_treino_rev7"] = O; spec.loader.exec_module(O)
meu = Path(R + "revisao_terceiro/_orq_sandbox"); O.ORQ = meu; O.LOG = meu / "orq_r4_real.log"; O.ESTADO = meu / "ESTADO_r4_real.json"
O.parar_pedido = lambda: False; O.gravar = lambda e_: None
def _sleep(s): raise SystemExit("FECHADA (ficou esperando)")
O.time.sleep = _sleep
for rot, p in (("REVISAO da R3 (guardada em bytes)", R + "revisao_terceiro/REVISAO_TERCEIRO_v407.R3.json"), ("REVISAO real da R4", R + "revisao_terceiro/REVISAO_TERCEIRO_v407.json")):
    O.REV = Path(p); e = {"passos": {}}
    try: print("S1b com a", rot, "->", "ABRE" if O.s1b_revisao(e) else "retornou False")
    except SystemExit as ex: print("S1b com a", rot, "->", ex)
