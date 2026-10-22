# -*- coding: utf-8 -*-
"""V1 da regra de decisao R2: confere por script o FREEZE.json da R1 (1_PREREGISTRO) e o FREEZE_R2.json (5_R2/0_ADENDO),
com sha256 e tamanhos de TODOS os itens listados, e registra a hora UTC de inicio deste ensaio (V2: tem de ser
posterior a FREEZE_R2.congelado_em_utc). Fail-closed: qualquer divergencia -> codigo de saida 2 e "ok": false.
Os valores esperados sao LIDOS dos proprios FREEZE (nunca digitados). O sha256 esperado do FREEZE_R2.json e passado na
linha de comando (vem do enunciado da tarefa, nao de memoria) e e comparado ao medido.
Uso: python -I -X utf8 conferir_freezes_pedra_r2.py <sha256_esperado_do_FREEZE_R2_segundo_o_enunciado>
"""
import datetime
import hashlib
import json
import os
import sys

W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
D_R1 = os.path.join(W, "1_PREREGISTRO")
D_R2 = os.path.join(W, "5_R2", "0_ADENDO")
F_R1 = os.path.join(D_R1, "FREEZE.json")
F_R2 = os.path.join(D_R2, "FREEZE_R2.json")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas",
                   "CONFERENCIA_FREEZES_PEDRA_R2.json")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def item(caminho, sha_esp, bytes_esp):
    ok_exist = os.path.exists(caminho)
    s = sha(caminho) if ok_exist else None
    b = os.path.getsize(caminho) if ok_exist else None
    return {"caminho": caminho, "sha256_esperado": sha_esp, "sha256_medido": s, "bytes_esperado": bytes_esp,
            "bytes_medido": b, "confere": bool(ok_exist and s == sha_esp and b == bytes_esp)}


def main(sha_r2_enunciado):
    inicio_utc = datetime.datetime.now(datetime.timezone.utc)
    r1 = json.load(open(F_R1, encoding="utf-8"))
    r2 = json.load(open(F_R2, encoding="utf-8"))
    itens_r1 = [item(r1["preregistro_json"]["arquivo"], r1["preregistro_json"]["sha256"], r1["preregistro_json"]["bytes"]),
                item(r1["preregistro_md"]["arquivo"], r1["preregistro_md"]["sha256"], r1["preregistro_md"]["bytes"])]
    for a in r1["anexos"]:
        itens_r1.append(item(os.path.join(D_R1, a["caminho"]), a["sha256"], a["bytes"]))
    freeze_r1_proprio = item(F_R1, r2["freeze_R1"]["sha256"], r2["freeze_R1"]["bytes"])
    itens_r2 = [item(r2["adendo_json"]["arquivo"], r2["adendo_json"]["sha256"], r2["adendo_json"]["bytes"]),
                item(r2["adendo_md"]["arquivo"], r2["adendo_md"]["sha256"], r2["adendo_md"]["bytes"])]
    for a in r2["anexos"]:
        itens_r2.append(item(os.path.join(D_R2, a["caminho"]), a["sha256"], a["bytes"]))
    sha_r2_medido = sha(F_R2)
    congelado = datetime.datetime.fromisoformat(r2["congelado_em_utc"])
    out = {
        "nota": "V1/V2 da regra de decisao R2 (ADENDO_R2 §d): conferencia por script dos dois FREEZE antes de construir a "
                "pedra corrigida; valores esperados lidos dos FREEZE; divergencia = INVALIDO (fail-closed).",
        "inicio_deste_ensaio_utc": inicio_utc.isoformat(),
        "FREEZE_R1": {"arquivo": F_R1, "congelado_em_utc": r1["congelado_em_utc"], "proprio": freeze_r1_proprio,
                      "n_itens": len(itens_r1), "itens": itens_r1,
                      "todos_conferem": all(x["confere"] for x in itens_r1) and freeze_r1_proprio["confere"]},
        "FREEZE_R2": {"arquivo": F_R2, "congelado_em_utc": r2["congelado_em_utc"],
                      "sha256_medido": sha_r2_medido, "bytes_medido": os.path.getsize(F_R2),
                      "sha256_esperado_pelo_enunciado": sha_r2_enunciado,
                      "sha256_confere_com_o_enunciado": sha_r2_medido == sha_r2_enunciado,
                      "n_itens": len(itens_r2), "itens": itens_r2,
                      "todos_conferem": all(x["confere"] for x in itens_r2),
                      "kernel_impressao_digital_registrada": r2["kernel_impressao_digital"]},
        "inicio_posterior_ao_FREEZE_R2": inicio_utc > congelado,
        "segundos_apos_FREEZE_R2": (inicio_utc - congelado).total_seconds(),
    }
    out["ok"] = bool(out["FREEZE_R1"]["todos_conferem"] and out["FREEZE_R2"]["todos_conferem"]
                     and out["FREEZE_R2"]["sha256_confere_com_o_enunciado"] and out["inicio_posterior_ao_FREEZE_R2"])
    with open(OUT + ".tmp", "wb") as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(OUT + ".tmp", OUT)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k not in ("FREEZE_R1", "FREEZE_R2")}, ensure_ascii=False, indent=1))
    print("R1:", out["FREEZE_R1"]["n_itens"], "itens, todos conferem:", out["FREEZE_R1"]["todos_conferem"],
          "| proprio:", freeze_r1_proprio["confere"])
    print("R2:", out["FREEZE_R2"]["n_itens"], "itens, todos conferem:", out["FREEZE_R2"]["todos_conferem"],
          "| sha256 medido:", sha_r2_medido)
    for x in itens_r1 + itens_r2:
        if not x["confere"]:
            print("DIVERGE:", x)
    if not out["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main(sys.argv[1])
