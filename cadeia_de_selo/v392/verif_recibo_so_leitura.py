import json, sys, hashlib
from pathlib import Path
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\vinculo")
import sincronizar_bancada as S
H = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392"); P = json.load(open(H/"PINOS_BN_v392.json", encoding="utf-8"))
assert hashlib.sha256(open(P["esboco_R3_3"]["path"],"rb").read()).hexdigest()==P["esboco_R3_3"]["sha256"]
nos = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"); bancada = Path(r"C:\IALD\Bancada_Um")
ni = S.ler_nos(nos, "v392")
cri = S.carregar_criterios(P["criterios"]["path"], P["criterios"]["sha256"], "v392")
mod, _ = S.carregar_canonical(bancada); ant = S.estado_anterior(bancada, mod)
ja = (ant["estado_do_contrato_instalado"]=="OK" and ant["version"]=="v392" and ant["um_py_pinado"]==ni["um_py"]["sha256"] and ant["seal_sha_pinado"]==ni["selo"]["sha256"])
rps = S.conferir_recibo_pre_selo(P["recibo_pre_selo"]["path"], ant, bancada, ja, P["recibo_pre_selo"]["sha256"], P["selo_anterior_v391"]["path"], P["kernel_manifesto_anterior_v391"]["path"])
kr = H/"kernel"/"KERNEL_RECIBO_v392.json"; krsha = hashlib.sha256(kr.read_bytes()).hexdigest()
ok, det, pino = S.verificar_kernel_recibo(kr, "v392", ni, krsha, rps, False, cri)
print(ok, krsha[:16]); print(str(det)[:1500])
