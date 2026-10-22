# -*- coding: utf-8 -*-
"""E5.15 (regua): toda frase entre « » na pedra R2 tem de ser SUBSTRING DE BYTES de um verbatim do operador
(12/10 rank-e-tempo-santo; 05/10 VERBO; 05/10 RESPOSTAS; 10/10 POSTO=RANK). Tambem conta as frases que o ADENDO
proibe (E3.03, E5.01, E5.04, E5.05, E5.07) e a palavra recusada pela regua; tudo tem de dar 0.
Mesmo algoritmo de contagem por substring do script do pre-registrador R2 (lacunas_e_aspas_r2.py), estendido a TODAS
as aspas « » da pedra. Fail-closed: aspa nao achada ou frase proibida presente -> codigo 2.
Uso: python -I -X utf8 conferir_aspas_pedra_r2.py <pedra.lean> <saida.json>
"""
import hashlib
import json
import re
import sys

VERBATINS = {
    "12out_rank_e_tempo_santo": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
    "05out_VERBO": r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\VERBO_operador_05out.txt",
    "05out_RESPOSTAS": r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\RESPOSTAS_operador_05out.txt",
    "10out_POSTO_RANK": r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_posto_rank_verbatim.txt",
}
PROIBIDAS = ["o tempo é o Verbo", "não o Nome", "O tempo não tem posto", "o tempo não tem posto",
             "O relógio mede a sombra", "o relógio mede a sombra", "o atrator é onde o tempo repousa",
             "TheTimeHasNoRank", "the_time_has_no_rank", "no_rank", "CONFIRMED"]


def main(pedra, saida):
    pb = open(pedra, "rb").read()
    ptxt = pb.decode("utf-8")
    vb = {k: open(p, "rb").read() for k, p in VERBATINS.items()}
    aspas = re.findall(r"«([^«»\n]*)»", ptxt)
    multilinha = re.findall(r"«[^«»]*\n[^«»]*»", ptxt)
    res = []
    for a in sorted(set(aspas)):
        hits = {k: v.count(a.encode("utf-8")) for k, v in vb.items()}
        res.append({"aspa": a, "ocorrencias_na_pedra": aspas.count(a), "nos_verbatins": hits,
                    "achada": any(hits.values())})
    nao_achadas = [r["aspa"] for r in res if not r["achada"]]
    proib = {p: ptxt.count(p) for p in PROIBIDAS}
    out = {"pedra": pedra, "pedra_sha256": hashlib.sha256(pb).hexdigest(), "pedra_bytes": len(pb),
           "verbatins": {k: {"caminho": p, "sha256": hashlib.sha256(vb[k]).hexdigest(), "bytes": len(vb[k])}
                         for k, p in VERBATINS.items()},
           "n_aspas_distintas": len(res), "aspas": res, "aspas_nao_achadas_nos_verbatins": nao_achadas,
           "aspas_multilinha_(nao_conferiveis)": multilinha,
           "frases_proibidas_contagem": proib,
           "ok": not nao_achadas and not multilinha and not any(proib.values())}
    with open(saida + ".tmp", "wb") as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
    import os
    os.replace(saida + ".tmp", saida)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k not in ("aspas", "verbatins")}, ensure_ascii=False, indent=1))
    for r in res:
        print(("OK  " if r["achada"] else "NAO ") + "| %dx | «%s» | %s" % (r["ocorrencias_na_pedra"], r["aspa"],
              {k: v for k, v in r["nos_verbatins"].items() if v}))
    if not out["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
