"""Grava FREEZE_R2.json do ADENDO R2 da F1.TEMPO: sha256 e tamanho de ADENDO_R2.json e ADENDO_R2.md (lidos dos bytes,
por script), a hora UTC, os sha256 de todos os anexos da pasta (scripts e saidas) e a impressao digital do kernel
antes/depois. Depois do FREEZE nada se altera na pasta 0_ADENDO. Recusa sobrescrever. Mesma forma do congelar.py da R1.
Uso: python -I -X utf8 congelar_r2.py"""
import datetime
import hashlib
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"


def ent(rel):
    p = os.path.join(BASE, rel)
    with open(p, "rb") as fh:
        b = fh.read()
    return dict(arquivo=p, sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))


def main():
    alvo = os.path.join(BASE, "FREEZE_R2.json")
    if os.path.exists(alvo):
        print("FALHA_VISIVEL: FREEZE_R2.json ja existe; nao se sobrescreve")
        sys.exit(2)
    anexos = []
    for dp, dn, fn in os.walk(BASE):
        dn.sort()
        for f in sorted(fn):
            rel = os.path.relpath(os.path.join(dp, f), BASE)
            if rel in ("ADENDO_R2.json", "ADENDO_R2.md", "FREEZE_R2.json") or "__pycache__" in rel or rel.endswith(".tmp"):
                continue
            anexos.append(dict(caminho=rel.replace("\\", "/"), **{k: v for k, v in ent(rel).items() if k != "arquivo"}))
    fp_a = json.load(open(os.path.join(BASE, "saidas", "FINGERPRINT_ADENDO_ANTES.json"), encoding="utf-8"))
    fp_d = json.load(open(os.path.join(BASE, "saidas", "FINGERPRINT_ADENDO_DEPOIS.json"), encoding="utf-8"))
    conf = json.load(open(os.path.join(BASE, "saidas", "CONFERENCIA_ADENDO_R2.json"), encoding="utf-8"))
    if not conf.get("ok"):
        print("FALHA_VISIVEL: a conferencia do ADENDO nao esta ok; nao se congela")
        sys.exit(2)
    fz1 = os.path.join(W, "1_PREREGISTRO", "FREEZE.json")
    with open(fz1, "rb") as fh:
        fz1_b = fh.read()
    doc = dict(
        congelado_em_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        unidade="F1.TEMPO", trilha="TEMPO", gerencia="c1", rodada="R2 — ADENDO aditivo ao pré-registro R1",
        autor="pré-registrador da R2 (subagente do workflow posto-e-tempo da gerência c1)",
        adendo_json=ent("ADENDO_R2.json"),
        adendo_md=ent("ADENDO_R2.md"),
        freeze_R1=dict(arquivo=fz1, sha256=hashlib.sha256(fz1_b).hexdigest(), bytes=len(fz1_b),
                       congelado_em_utc=json.loads(fz1_b.decode("utf-8"))["congelado_em_utc"], intacto=True),
        anexos=anexos,
        implementacao_de_referencia_normativa=ent(os.path.join("scripts", "tolerancia_uniforme_r2.py")),
        conferencia_pre_freeze=dict(arquivo="saidas/CONFERENCIA_ADENDO_R2.json", ok=conf["ok"], n_itens=len(conf["itens"])),
        kernel_impressao_digital=dict(antes=dict(meta=fp_a["meta_sha256"], src=fp_a["src_sha256"], taken_at=fp_a["taken_at"]),
                                      depois=dict(meta=fp_d["meta_sha256"], src=fp_d["src_sha256"], taken_at=fp_d["taken_at"]),
                                      iguais=(fp_a["meta_sha256"] == fp_d["meta_sha256"] and fp_a["src_sha256"] == fp_d["src_sha256"])),
        congelado_antes_de_qualquer_reensaio_afetado=True,
        nenhum_teste_rodado=True,
        nenhum_lean_rodado=True,
        regra="Depois deste FREEZE nada se altera na pasta 5_R2/0_ADENDO. O reensaio afetado (T9.o', O-f', a pedra corrigida e a sua auditoria) só vale se o recibo conferir por script este FREEZE_R2.json e o FREEZE.json da R1 (sha256 e tamanhos) e se começar DEPOIS de congelado_em_utc; divergência = INVÁLIDO. Mudança só por ADENDO R3 aditivo, com razões, congelado por hash ANTES do reensaio afetado; todas as tentativas preservadas. As linhas da R1 nunca se sobrescrevem.",
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
    sys.stdout.reconfigure(encoding="utf-8")
    print("FREEZE_R2.json", len(data), hashlib.sha256(data).hexdigest())
    print(json.dumps(dict(congelado_em_utc=doc["congelado_em_utc"], json_=doc["adendo_json"], md=doc["adendo_md"],
                          n_anexos=len(anexos), kernel_iguais=doc["kernel_impressao_digital"]["iguais"]), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
