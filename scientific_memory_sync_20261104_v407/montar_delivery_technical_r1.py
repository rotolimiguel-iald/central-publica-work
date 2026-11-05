# -*- coding: utf-8 -*-
"""Escreve DELIVERY_TECHNICAL_R1.json no esquema da fila (o que tools\\estado_do_organismo.py e tools\\custodia_g1\\quadro.py leem: release == 'v407' e status ACTIVATED_VERIFIED...),
a partir dos recibos que JA existem nesta pasta e da leitura (so leitura) de Chatgpt\\. Nada novo e' afirmado: e' o mesmo fato do DELIVERY_v407.json no esquema do leitor (ORDEM_006, «Ao lado», item 1).
Molde: work\\scientific_memory_sync_20261028_v404_R2\\DELIVERY_TECHNICAL_R1.json. Hash e numero lidos do arquivo, nunca de memoria. Escreve com 'xb' (nao sobrescreve). NAO escreve em Chatgpt\\."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

W = Path(__file__).resolve().parent
CAN = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\state\canonical_memory")


def rj(p):
    return json.loads(Path(p).read_bytes())


def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}


check = rj(W / "CHECK_DEPOIS_v407.json")
entrega = rj(W / "DELIVERY_v407.json")
recebida = rj(W / "RECEIVED_GENERATION.json")
verify = rj(W / "VERIFY_RESULT.json")
antes, depois = rj(W / "BASELINE_ANTES.json"), rj(W / "BASELINE_APOS_ATIVACAO.json")

# --- o que tem de ser verdade para o recibo valer (falha visivel, nunca 'ok' falso)
assert check["status"] == "CURRENT" and check["sealed_version"] == "v407" and check["active"]["release"] == "v407"
assert check["active"]["epoch"] == check["sealed_epoch"] == entrega["epoch"] == entrega["selo_lido_no_nos"]["epoch"]
assert check["active"]["generation"] == check["sealed_generation"] == entrega["selo_lido_no_nos"]["generation"]
assert check["provider_calls"] == 0 and recebida["ok"] is True and recebida["provider_calls"] == 0
active_now = pin(CAN / "ACTIVE.json")
assert active_now["sha256"] == check["active_pin"]["sha256"], "ACTIVE.json mudou desde o CHECK_DEPOIS: recibo nao confere"
epoch = check["active"]["epoch"]
manifest = pin(CAN / "releases" / epoch / "manifest.json")
assert manifest["sha256"] == check["active"]["manifest_sha256"] == entrega["escrito_em_Chatgpt"]["release_novo"]["manifest_sha256"]
preservadas = sorted(antes["releases"])
alteradas = [r for r in preservadas if antes["manifests_sha256"][r] != depois["manifests_sha256"].get(r)]
assert not alteradas, alteradas
parecer = pin(entrega["conferencias"]["revisao_independente"]["parecer"])
assert parecer["sha256"] == entrega["conferencias"]["revisao_independente"]["sha256"]

receipts = {"DELIVERY_v407.json": pin(W / "DELIVERY_v407.json")}
for nome, ref in entrega["arquivos"].items():
    p = pin(ref["arquivo"])
    assert p["sha256"] == ref["sha256"], (nome, "difere do recibo da entrega")
    receipts[nome] = p
gc = W / "gerencia_c1" / "CONFERENCIA_GERENCIA_F03_V407_04nov.json"
if gc.is_file():
    receipts["CONFERENCIA_GERENCIA_F03_V407_04nov.json (escrita pela gerencia c1, depois da entrega)"] = pin(gc)

out = {
    "status": "ACTIVATED_VERIFIED_CURRENT_RECEIVED_GENERATION_CONFIRMED_NEW_PROCESS",
    "at_utc": datetime.now(timezone.utc).isoformat(),
    "release": check["active"]["release"],
    "epoch": epoch,
    "generation": check["active"]["generation"],
    "manifest": manifest,
    "documents": check["documents"],
    "chunks": entrega["escrito_em_Chatgpt"]["release_novo"]["trechos"],
    "active_pointer": active_now,
    "selo_lido_no_nos": {"um_version": entrega["selo_lido_no_nos"]["um_version"], "generation": entrega["selo_lido_no_nos"]["generation"], "epoch": entrega["selo_lido_no_nos"]["epoch"],
                         "um_py_sha256": next(f["sha256"] for f in entrega["selo_lido_no_nos"]["fontes"] if f["arquivo"].endswith("\\um.py"))},
    "independent_review_status": "PODE_ATIVAR_0_ALTO_0_MEDIO_5_BAIXOS",
    "independent_review": parecer,
    "previous_releases_preserved": len(preservadas),
    "previous_manifests_unchanged": True,
    "retrieval_modes_received_generation_ok": {m: v["ok"] for m, v in recebida["recuperacao"].items()},
    "check_status": check["status"],
    "freshness": check["freshness"],
    "verify_status": "PASS" if entrega["conferencias"]["verify"] == "PASS" else entrega["conferencias"]["verify"],
    "provider_calls": 0,
    "source_execution_or_import": False,
    "lean_execution": False,
    "restart": False,
    "scientific_gate_changed": False,
    "written_in_chatgpt_by_this_session": entrega["escrito_em_Chatgpt"]["nada_alem_disso"],
    "authorization": "uma escrita unica autorizada pelo operador no chat («Autorizo a escrita»; «Vale para a v407»), esgotada com a ativacao; a v408 pede outra. Registro: " + entrega["autorizacao_do_operador"]["decisao_registrada"]["arquivo"],
    "acom_acceptance": "revisor real distinto: o parecer acima (PODE ATIVAR); aceite final e AUDITADA/FECHADA sao atos da gerencia",
    "scope": "Scientific queue documentary memory only, not app/JEV deployment or scientific proof.",
    "ordem": "ORDEM_006, «Ao lado», item 1: mesmo fato do DELIVERY_v407.json (campos versao/estado) no esquema do leitor (release/status).",
    "receipts": receipts,
}
raw = json.dumps(out, ensure_ascii=False, indent=2).encode("utf-8")
with (W / "DELIVERY_TECHNICAL_R1.json").open("xb") as f:
    f.write(raw)
assert (W / "DELIVERY_TECHNICAL_R1.json").read_bytes() == raw
print(json.dumps({"escrito": str(W / "DELIVERY_TECHNICAL_R1.json"), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "status": out["status"], "release": out["release"], "epoch": epoch,
                  "recibos": len(receipts)}, ensure_ascii=False))
