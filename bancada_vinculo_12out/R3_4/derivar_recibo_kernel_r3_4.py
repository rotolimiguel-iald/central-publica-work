# -*- coding: utf-8 -*-
"""derivar_recibo_kernel_r3_4.py (R3.4, 19/10/2026) -- deriva, POR SCRIPT, o recibo do kernel no contrato KERNEL_RECIBO_R3_4 a partir de um recibo KERNEL_RECIBO_R3_2: o contrato muda e
`modulos_de_auditoria` lista as pedras SEM declaracoes (os modulos de auditoria da versao, ex.: NetworkProofAuditR3/R7/R8 da v394). Antes de escrever, cada fonte listada (lida da
`arvore` do recibo e conferida pelo sha256 do recibo) passa pela varredura do esboco (auditar_fonte_de_auditoria: so import, open, #print axioms e run_cmd, lista fechada de palavras no
corpo): a pedra sem declaracoes cuja fonte nao passa NAO entra na lista e o script recusa (nao se lista o que declara). Nada mais do recibo muda (logs, hashes, criterios).
PROPOSTA: o pino do recibo derivado e da gerencia; o recibo original fica como esta. Escreve UM arquivo NOVO.
uso: python -I -B -X utf8 derivar_recibo_kernel_r3_4.py --recibo <KERNEL_RECIBO_vNNN.json> --saida <novo.json>"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, importlib.util, json
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--recibo", required=True)
ap.add_argument("--saida", required=True)
a = ap.parse_args()
AQUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("sync_r34_derivar", AQUI / "sincronizar_bancada.py")
MOD = importlib.util.module_from_spec(spec)
sys.modules["sync_r34_derivar"] = MOD
spec.loader.exec_module(MOD)
raw = Path(a.recibo).read_bytes()
k = MOD.json_estrito(raw)
if k.get("contrato") != MOD.KERNEL_CONTRATO_R3_2:
    raise SystemExit("CONTRATO_DE_ORIGEM: o recibo e %r (exigido %s)" % (k.get("contrato"), MOD.KERNEL_CONTRATO_R3_2))
if "modulos_de_auditoria" in k:
    raise SystemExit("JA_TEM_MODULOS_DE_AUDITORIA")
arvore = Path(k["arvore"])
sem = [p for p in k["pedras"] if not p.get("declaracoes")]
if not sem:
    raise SystemExit("NENHUMA_PEDRA_SEM_DECLARACOES: nada a listar (o recibo ja serve ao contrato R3_2)")
lista, contagens = [], {}
for p in sem:
    fp = arvore / p["path"]
    b = fp.read_bytes()
    if hashlib.sha256(b).hexdigest() != p["sha256"].lower():
        raise SystemExit("FONTE_NAO_E_A_DO_RECIBO: %s" % p["path"])
    v = MOD.auditar_fonte_de_auditoria(b.decode("utf-8-sig"))
    if not v["ok"]:
        raise SystemExit("PEDRA_SEM_DECLARACOES_QUE_NAO_E_DE_AUDITORIA: %s: %s" % (p["path"], v["motivo"]))
    lista.append(p["path"])
    contagens[p["path"]] = v["contagem"]
novo = {}
for chave, valor in k.items():
    novo[chave] = valor
    if chave == "pedras":
        novo["modulos_de_auditoria"] = sorted(lista)
novo["contrato"] = MOD.KERNEL_CONTRATO
novo["derivado_de"] = dict(contrato=MOD.KERNEL_CONTRATO_R3_2, sha256=hashlib.sha256(raw).hexdigest(), por="derivar_recibo_kernel_r3_4.py (R3.4)",
                           nota="so o contrato e modulos_de_auditoria mudam; os modulos listados sao as pedras sem declaracoes, com a fonte conferida pela varredura do esboco")
p = Path(a.saida)
with open(p, "xb") as f:
    f.write((json.dumps(novo, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
print(json.dumps(dict(saida=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest(), modulos_de_auditoria=sorted(lista), contagens=contagens), ensure_ascii=False))
