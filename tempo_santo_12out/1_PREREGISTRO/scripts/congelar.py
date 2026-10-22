"""Grava FREEZE.json do pre-registro F1.TEMPO: sha256 e tamanho de PREREGISTRO.json e PREREGISTRO.md (lidos dos
bytes, por script) e a hora UTC; acrescenta os sha256 dos anexos da pasta (scripts, consultas, impressoes digitais).
Depois do FREEZE nada se altera na pasta. Uso: python -X utf8 congelar.py"""
import datetime
import hashlib
import json
import os
import sys

BASE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO"


def ent(rel):
    p = os.path.join(BASE, rel)
    with open(p, "rb") as fh:
        b = fh.read()
    return dict(arquivo=p, sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))


def main():
    alvo = os.path.join(BASE, "FREEZE.json")
    if os.path.exists(alvo):
        print("FALHA_VISIVEL: FREEZE.json ja existe; nao se sobrescreve")
        sys.exit(2)
    anexos = []
    for dp, dn, fn in os.walk(BASE):
        dn.sort()
        for f in sorted(fn):
            rel = os.path.relpath(os.path.join(dp, f), BASE)
            if rel in ("PREREGISTRO.json", "PREREGISTRO.md", "FREEZE.json") or "__pycache__" in rel or rel.endswith(".tmp"):
                continue
            anexos.append(dict(caminho=rel.replace("\\", "/"), **{k: v for k, v in ent(rel).items() if k != "arquivo"}))
    fp_a = json.load(open(os.path.join(BASE, "FINGERPRINT_PREREG_ANTES.json"), encoding="utf-8"))
    fp_d = json.load(open(os.path.join(BASE, "FINGERPRINT_PREREG_DEPOIS.json"), encoding="utf-8"))
    doc = dict(
        congelado_em_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        unidade="F1.TEMPO", trilha="TEMPO", gerencia="c1",
        autor="pré-registrador (subagente do workflow posto-e-tempo da gerência c1)",
        preregistro_json=ent("PREREGISTRO.json"),
        preregistro_md=ent("PREREGISTRO.md"),
        anexos=anexos,
        kernel_impressao_digital=dict(antes=dict(meta=fp_a["meta_sha256"], src=fp_a["src_sha256"]),
                                      depois=dict(meta=fp_d["meta_sha256"], src=fp_d["src_sha256"]),
                                      iguais=(fp_a["meta_sha256"] == fp_d["meta_sha256"] and fp_a["src_sha256"] == fp_d["src_sha256"])),
        congelado_antes_de_qualquer_ensaio=True,
        nenhum_teste_rodado=True,
        regra="Depois deste FREEZE nada se altera na pasta 1_PREREGISTRO. Mudança só por ADENDO aditivo, com razões, congelado por hash ANTES do reensaio afetado; todas as tentativas preservadas. O ensaio confere por script estes sha256 e tamanhos antes de começar; divergência = INVÁLIDO.",
    )
    data = (json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    tmp = alvo + ".tmp"
    with open(tmp, "wb") as fo:
        fo.write(data)
    with open(tmp, "rb") as fh:
        if fh.read() != data:
            print("FALHA_VISIVEL: temporario nao confere")
            sys.exit(2)
    os.replace(tmp, alvo)
    with open(alvo, "rb") as fh:
        if fh.read() != data:
            print("FALHA_VISIVEL: FREEZE final nao confere")
            sys.exit(2)
    print("FREEZE.json", len(data), hashlib.sha256(data).hexdigest())
    print(json.dumps(dict(json_=doc["preregistro_json"], md=doc["preregistro_md"], iguais=doc["kernel_impressao_digital"]["iguais"]), ensure_ascii=False))


if __name__ == "__main__":
    main()
