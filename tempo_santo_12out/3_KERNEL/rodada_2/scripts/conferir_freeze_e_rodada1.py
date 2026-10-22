# -*- coding: utf-8 -*-
"""Rodada 2 do construtor do kernel (F1.TEMPO): conferência por script, SÓ DE LEITURA.

(1) FREEZE.json: os 2 principais + 28 anexos por sha256 e tamanho; nenhum arquivo novo/ausente; mtime <= FREEZE.
(2) Texto do operador de 12/10 e a segunda parte (desde «O que mais me fascina…»).
(3) Rodada 1 do kernel (3_KERNEL fora de rodada_2): cada arquivo do MANIFESTO_3_KERNEL.json confere por sha256 e
    tamanho (prova de que a rodada 2 NÃO sobrescreveu a rodada 1).
Uso: python -I conferir_freeze_e_rodada1.py <saida.json>
"""
import datetime
import hashlib
import json
import os
import sys

BASE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
PRE = os.path.join(BASE, "1_PREREGISTRO")
K1 = os.path.join(BASE, "3_KERNEL")
OPER = r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"
FREEZE_SHA = "6b29d4c9b09e5553a3d58a3933137bbf73df3d0b6632b036e0a74abef7533c9b"
FREEZE_BYTES = 5986


def h(p):
    with open(p, "rb") as f:
        b = f.read()
    return len(b), hashlib.sha256(b).hexdigest()


def main(out):
    res = {"feito_em_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    n, s = h(os.path.join(PRE, "FREEZE.json"))
    res["freeze"] = {"bytes": n, "sha256": s, "confere_com_o_indice": (n == FREEZE_BYTES and s == FREEZE_SHA)}
    fz = json.load(open(os.path.join(PRE, "FREEZE.json"), "rb"))
    itens = []
    for key in ("preregistro_json", "preregistro_md"):
        n, s = h(fz[key]["arquivo"])
        itens.append({"arquivo": fz[key]["arquivo"], "bytes": n, "sha256": s,
                      "confere": n == fz[key]["bytes"] and s == fz[key]["sha256"]})
    for a in fz["anexos"]:
        p = os.path.join(PRE, a["caminho"].replace("/", os.sep))
        n, s = h(p)
        itens.append({"arquivo": a["caminho"], "bytes": n, "sha256": s,
                      "confere": n == a["bytes"] and s == a["sha256"]})
    listed = {a["caminho"].replace("/", os.sep) for a in fz["anexos"]} | {"PREREGISTRO.json", "PREREGISTRO.md", "FREEZE.json"}
    tfz = datetime.datetime.fromisoformat(fz["congelado_em_utc"]).timestamp()
    present, newer = set(), []
    for root, _d, files in os.walk(PRE):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), PRE)
            present.add(rel)
            if os.path.getmtime(os.path.join(root, f)) > tfz + 1.0:
                newer.append(rel)
    res["freeze_itens"] = itens
    res["freeze_conferem"] = sum(1 for i in itens if i["confere"])
    res["freeze_total"] = len(itens)
    res["freeze_nao_listados"] = sorted(present - listed)
    res["freeze_ausentes"] = sorted(listed - present)
    res["freeze_mtime_posterior"] = sorted(newer)
    res["freeze_ok"] = (res["freeze"]["confere_com_o_indice"] and res["freeze_conferem"] == res["freeze_total"]
                        and not res["freeze_nao_listados"] and not res["freeze_ausentes"] and not newer)
    b = open(OPER, "rb").read()
    i0 = b.find("O que mais me fascina".encode("utf-8"))
    res["texto_do_operador"] = {"arquivo": OPER, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(),
                                "segunda_parte_inicio_byte": i0, "segunda_parte_bytes": len(b) - i0,
                                "segunda_parte_sha256": hashlib.sha256(b[i0:]).hexdigest(),
                                "n_crlf": b.count(b"\r\n")}
    res["texto_do_operador"]["confere"] = (
        res["texto_do_operador"]["sha256"] == "2c8b7b712aa9ad7f435f8652d1febdf6fe64d14775e277f2b2d720598135c8c3"
        and res["texto_do_operador"]["segunda_parte_sha256"] == "6dcefdbe5c6a7752766ec9a1aaa2255f9b874fbb2a445925b6c615f1b574dc72")
    man = json.load(open(os.path.join(K1, "MANIFESTO_3_KERNEL.json"), "rb"))
    r1 = []
    for a in man["arquivos"]:
        p = os.path.join(K1, a["arquivo"].replace("/", os.sep))
        if os.path.exists(p):
            n, s = h(p)
            r1.append({"arquivo": a["arquivo"], "confere": n == a["bytes"] and s == a["sha256"]})
        else:
            r1.append({"arquivo": a["arquivo"], "confere": False, "ausente": True})
    nman, sman = h(os.path.join(K1, "MANIFESTO_3_KERNEL.json"))
    res["rodada_1_kernel"] = {"manifesto": {"bytes": nman, "sha256": sman}, "n_arquivos_no_manifesto": len(r1),
                              "n_conferem": sum(1 for x in r1 if x["confere"]),
                              "divergentes": [x for x in r1 if not x["confere"]]}
    with open(out + ".tmp", "w", encoding="utf-8") as fo:
        json.dump(res, fo, ensure_ascii=False, indent=1)
    os.replace(out + ".tmp", out)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"freeze_ok": res["freeze_ok"], "freeze_conferem": res["freeze_conferem"],
                      "freeze_total": res["freeze_total"], "operador_confere": res["texto_do_operador"]["confere"],
                      "rodada_1": [res["rodada_1_kernel"]["n_conferem"], res["rodada_1_kernel"]["n_arquivos_no_manifesto"]],
                      "rodada_1_divergentes": res["rodada_1_kernel"]["divergentes"]}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
