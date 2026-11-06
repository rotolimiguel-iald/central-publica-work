import json, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
for f in ("ESPERADOS_v409.json", "PINOS_BN_v409.json", "kernel/KERNEL_RECIBO_v409.json", "kernel/FLAGS_v409.json", "kernel/KH_N1_v409.json", "PINO_MEMORIA_PY_v409.json", "MANIFESTO_INSUMOS_v409.json", "FORMAL_MAP_v409.json", "kernel/POS_BUILD_v409.json"):
    d = json.load(open(R + f, encoding="utf-8"))
    print("==", f, type(d).__name__, len(d))
    if isinstance(d, dict):
        for k, v in list(d.items())[:40]:
            s = json.dumps(v, ensure_ascii=False, default=str)
            print("   ", k, ":", s[:170])
