# -*- coding: utf-8 -*-
r"""conferir_freezes_r2.py -- F1.TEMPO R2, reensaiador otico (regra V1 do ADENDO R2).

ANTES de qualquer ensaio: confere por script (sha256 dos bytes + tamanho) o FREEZE.json da R1 (pelo script da R1
copiado byte a byte: scripts/conferir_freeze_R1_copia.py, 30 itens + texto do operador + um.py) e o FREEZE_R2.json
(o proprio arquivo, ADENDO_R2.md, ADENDO_R2.json, a entrada freeze_R1, os 16 anexos e a implementacao normativa),
e que a hora UTC de agora e POSTERIOR a congelado_em_utc (regra V2). Divergencia = INVALIDO (codigo de saida 2).
Os valores esperados vem do ENUNCIADO da tarefa (a conferencia e contra os BYTES). So biblioteca padrao: python -I.
Escreve so em 5_R2/2_REENSAIO/saidas. Uso: python -I -X utf8 conferir_freezes_r2.py
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.basename(HERE) != "2_REENSAIO":
    sys.exit("RECUSA: fora de 5_R2/2_REENSAIO")
W = os.path.dirname(os.path.dirname(HERE))
ADENDO = os.path.join(W, "5_R2", "0_ADENDO")
FREEZE_R2 = os.path.join(ADENDO, "FREEZE_R2.json")
FREEZE_R1 = os.path.join(W, "1_PREREGISTRO", "FREEZE.json")
SAIDAS = os.path.join(HERE, "saidas")
PY = sys.executable

# esperado (copiado do enunciado da tarefa; a conferencia e contra os bytes)
EXP = {
    "FREEZE_R2.json": ("0737f608505afdb5122e9c9154a2d99e18d6fe12a84ead9ab890b825e8065de5", 4982),
    "ADENDO_R2.json": ("b9568befdcc200f8a3983273a11168fd803a006c04338bd22b6da769bfb3e67f", 60427),
    "ADENDO_R2.md": ("ab13c0f27a7f4cf5e0a568db2fb0f7c5f32fc813a1d735fec9ddd72db38da7e4", 42114),
    "FREEZE_R1": ("6b29d4c9b09e5553a3d58a3933137bbf73df3d0b6632b036e0a74abef7533c9b", 5986),
    "congelado_em_utc": "2026-10-12T23:07:58.201826+00:00",
}


def sha_file(p):
    h = hashlib.sha256()
    n = 0
    with open(p, "rb") as fh:
        while True:
            c = fh.read(1 << 22)
            if not c:
                break
            h.update(c)
            n += len(c)
    return h.hexdigest(), n


def write_json(path, obj):
    assert os.path.commonpath([os.path.abspath(path), HERE]) == HERE
    data = (json.dumps(obj, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    assert os.path.getsize(tmp) == len(data)
    os.replace(tmp, path)
    return hashlib.sha256(data).hexdigest(), len(data)


def main():
    now = datetime.now(timezone.utc)
    out = {"documento": "CONFERENCIA dos FREEZE (R1 e R2) antes do reensaio R2 da face otica (regra V1/V2 do ADENDO R2)",
           "agora_utc": now.isoformat(), "checks": []}

    def chk(item, got, exp):
        ok = (got == exp)
        out["checks"].append({"item": item, "esperado": exp, "lido": got, "ok": ok})
        return ok

    # --- FREEZE R1 pelo script da R1 (copia byte a byte), saida na nossa pasta
    r1_out = os.path.join(SAIDAS, "CONFERENCIA_FREEZE_R1.json")
    r = subprocess.run([PY, "-I", "-X", "utf8", os.path.join(HERE, "scripts", "conferir_freeze_R1_copia.py"), r1_out],
                       capture_output=True, timeout=600)
    r1 = json.load(open(r1_out, encoding="utf-8"))
    chk("FREEZE R1: script da R1 (copia) codigo de saida", r.returncode, 0)
    chk("FREEZE R1: script da R1 (copia) all_ok", r1["all_ok"], True)
    chk("FREEZE R1: script da R1 (copia) n_falhas", r1["n_falhas"], 0)
    out["freeze_R1_conferencia"] = {"arquivo": r1_out, "n_checks": r1["n_checks"], "n_falhas": r1["n_falhas"],
                                    "stdout": r.stdout.decode("utf-8", "replace")[:2000]}
    s, n = sha_file(FREEZE_R1)
    chk("FREEZE R1 sha256 (bytes)", s, EXP["FREEZE_R1"][0])
    chk("FREEZE R1 bytes", n, EXP["FREEZE_R1"][1])

    # --- FREEZE R2
    s, n = sha_file(FREEZE_R2)
    chk("FREEZE_R2.json sha256 (bytes)", s, EXP["FREEZE_R2.json"][0])
    chk("FREEZE_R2.json bytes", n, EXP["FREEZE_R2.json"][1])
    fz = json.load(open(FREEZE_R2, encoding="utf-8"))
    chk("FREEZE_R2 congelado_em_utc == enunciado", fz["congelado_em_utc"], EXP["congelado_em_utc"])
    frozen = datetime.fromisoformat(fz["congelado_em_utc"])
    chk("agora (UTC) e POSTERIOR a congelado_em_utc (V2)", now > frozen, True)
    out["segundos_depois_do_freeze"] = (now - frozen).total_seconds()
    for key, name in (("adendo_json", "ADENDO_R2.json"), ("adendo_md", "ADENDO_R2.md")):
        ent = fz[key]
        chk("FREEZE_R2.%s.sha256 == enunciado" % key, ent["sha256"], EXP[name][0])
        chk("FREEZE_R2.%s.bytes == enunciado" % key, ent["bytes"], EXP[name][1])
        s, n = sha_file(ent["arquivo"])
        chk("%s sha256 (bytes)" % name, s, ent["sha256"])
        chk("%s bytes" % name, n, ent["bytes"])
    fr1 = fz["freeze_R1"]
    chk("FREEZE_R2.freeze_R1.sha256 == enunciado", fr1["sha256"], EXP["FREEZE_R1"][0])
    chk("FREEZE_R2.freeze_R1.bytes == enunciado", fr1["bytes"], EXP["FREEZE_R1"][1])
    chk("FREEZE_R2.freeze_R1.intacto", fr1["intacto"], True)
    s, n = sha_file(fr1["arquivo"])
    chk("FREEZE_R2.freeze_R1.arquivo sha256 (bytes)", s, fr1["sha256"])
    chk("FREEZE_R2.freeze_R1.arquivo bytes", n, fr1["bytes"])
    chk("FREEZE_R2 n_anexos", len(fz["anexos"]), 16)
    for a in fz["anexos"]:
        p = os.path.join(ADENDO, a["caminho"].replace("/", os.sep))
        s, n = sha_file(p)
        chk("anexo %s sha256" % a["caminho"], s, a["sha256"])
        chk("anexo %s bytes" % a["caminho"], n, a["bytes"])
    norm = fz["implementacao_de_referencia_normativa"]
    s, n = sha_file(norm["arquivo"])
    chk("implementacao normativa sha256 (bytes)", s, norm["sha256"])
    chk("implementacao normativa bytes", n, norm["bytes"])
    # a copia da implementacao normativa na nossa pasta e identica
    s, n = sha_file(os.path.join(HERE, "scripts", "tolerancia_uniforme_r2.py"))
    chk("copia local da implementacao normativa sha256", s, norm["sha256"])
    for flag in ("congelado_antes_de_qualquer_reensaio_afetado", "nenhum_teste_rodado", "nenhum_lean_rodado"):
        chk("FREEZE_R2." + flag, fz.get(flag), True)
    chk("FREEZE_R2 kernel antes==depois", fz["kernel_impressao_digital"]["iguais"], True)
    # pasta 0_ADENDO: nenhum arquivo alem dos congelados (FREEZE_R2 + md + json + 16 anexos)
    listed = {"FREEZE_R2.json", "ADENDO_R2.md", "ADENDO_R2.json"} | {a["caminho"] for a in fz["anexos"]}
    ondisk = set()
    for dp, dn, fn in os.walk(ADENDO):
        for f in fn:
            ondisk.add(os.path.relpath(os.path.join(dp, f), ADENDO).replace("\\", "/"))
    chk("pasta 0_ADENDO tem exatamente os arquivos congelados", sorted(ondisk), sorted(listed))

    out["all_ok"] = all(c["ok"] for c in out["checks"])
    out["n_checks"] = len(out["checks"])
    out["n_falhas"] = sum(1 for c in out["checks"] if not c["ok"])
    out["veredito"] = "FREEZES CONFERIDOS (pode ensaiar)" if out["all_ok"] else "INVALIDO: divergencia (nao ensaiar)"
    out["taken_at_local"] = time.strftime("%Y-%m-%d %H:%M:%S")
    sha, nb = write_json(os.path.join(SAIDAS, "CONFERENCIA_FREEZES_R2.json"), out)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"all_ok": out["all_ok"], "n_checks": out["n_checks"], "n_falhas": out["n_falhas"],
                      "segundos_depois_do_freeze": out["segundos_depois_do_freeze"], "sha256": sha, "bytes": nb}))
    for c in out["checks"]:
        if not c["ok"]:
            print("DIVERGENCIA:", json.dumps(c, ensure_ascii=False)[:500])
    sys.exit(0 if out["all_ok"] else 2)


if __name__ == "__main__":
    main()
