# -*- coding: utf-8 -*-
"""Auditor cetico de REPRODUCAO (R2, F1.TEMPO): conferencia por script dos FREEZE (R1 e R2), dos anexos, e da
ordem temporal (V2): tudo o que da veredito na R2 tem de ter comecado DEPOIS de FREEZE_R2.congelado_em_utc.
Tambem confere os hashes declarados em RESULTADO_PEDRA_R2.json, nos recibos e no reensaio contra o disco.
So leitura fora de 5_R2/3_AUD_REPRO. Uso: python -I -X utf8 conferir_freezes_aud.py <saida.json>"""
import datetime
import hashlib
import json
import os
import sys

W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
R1F = os.path.join(W, "1_PREREGISTRO", "FREEZE.json")
R2F = os.path.join(W, "5_R2", "0_ADENDO", "FREEZE_R2.json")
EXP_R2 = ("0737f608505afdb5122e9c9154a2d99e18d6fe12a84ead9ab890b825e8065de5", 4982)
EXP_R1 = ("6b29d4c9b09e5553a3d58a3933137bbf73df3d0b6632b036e0a74abef7533c9b", 5986)
EXP_PEDRA = "4d8a82591badd010513c74ec6b5efce6d368f107841007f5be5000c8bc3b60a4"
EXP_OLEAN = "b52382ec16542a84130cdb405dc8a6d0989312857be4487c96601ece43fa046a"
EXP_REENSAIO = "44e745447fae09911059ae7d4504b41b0e980a706e76f0e992b3665a889327e7"
LONG = "\\\\?\\"
CHUNK = 4194304


def sha(p):
    h = hashlib.sha256()
    p = os.path.normpath(p)
    with open(LONG + p if not p.startswith(LONG) else p, "rb") as fh:
        for c in iter(lambda: fh.read(CHUNK), b""):
            h.update(c)
    return h.hexdigest()


def item(nome, lido, esperado):
    return {"item": nome, "lido": lido, "esperado": esperado, "ok": lido == esperado}


out = {"documento": "conferencia dos FREEZE e da ordem temporal (V1/V2) - auditor de reproducao R2",
       "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "itens": []}
it = out["itens"]
# FREEZE R1
it.append(item("FREEZE R1 sha256", sha(R1F), EXP_R1[0]))
it.append(item("FREEZE R1 bytes", os.path.getsize(R1F), EXP_R1[1]))
fz1 = json.load(open(R1F, encoding="utf-8"))
for key in ("preregistro_json", "preregistro_md"):
    p = fz1[key]["arquivo"]
    it.append(item("R1.%s sha256" % key, sha(p), fz1[key]["sha256"]))
    it.append(item("R1.%s bytes" % key, os.path.getsize(p), fz1[key]["bytes"]))
for a in fz1.get("anexos", []):
    p = os.path.join(W, "1_PREREGISTRO", a["caminho"].replace("/", os.sep))
    it.append(item("R1 anexo %s sha256" % a["caminho"], sha(p), a["sha256"]))
    it.append(item("R1 anexo %s bytes" % a["caminho"], os.path.getsize(p), a["bytes"]))
# FREEZE R2
it.append(item("FREEZE_R2 sha256", sha(R2F), EXP_R2[0]))
it.append(item("FREEZE_R2 bytes", os.path.getsize(R2F), EXP_R2[1]))
fz2 = json.load(open(R2F, encoding="utf-8"))
it.append(item("FREEZE_R2.freeze_R1.sha256 == FREEZE R1", fz2["freeze_R1"]["sha256"], EXP_R1[0]))
for key in ("adendo_json", "adendo_md"):
    p = fz2[key]["arquivo"]
    it.append(item("R2.%s sha256" % key, sha(p), fz2[key]["sha256"]))
    it.append(item("R2.%s bytes" % key, os.path.getsize(p), fz2[key]["bytes"]))
for a in fz2["anexos"]:
    p = os.path.join(W, "5_R2", "0_ADENDO", a["caminho"].replace("/", os.sep))
    it.append(item("R2 anexo %s sha256" % a["caminho"], sha(p), a["sha256"]))
    it.append(item("R2 anexo %s bytes" % a["caminho"], os.path.getsize(p), a["bytes"]))
norm = fz2["implementacao_de_referencia_normativa"]
it.append(item("normativa tolerancia_uniforme_r2.py sha256", sha(norm["arquivo"]), norm["sha256"]))
frozen = datetime.datetime.fromisoformat(fz2["congelado_em_utc"])
out["FREEZE_R2_congelado_em_utc"] = fz2["congelado_em_utc"]
mt = datetime.datetime.fromtimestamp(os.stat(R2F).st_mtime, datetime.timezone.utc)
out["FREEZE_R2_mtime_utc"] = mt.isoformat()
out["FREEZE_R2_mtime_dentro_de_5s_do_campo"] = abs((mt - frozen).total_seconds()) < 5
# a pasta 0_ADENDO nao mudou depois do FREEZE (nenhum arquivo com mtime posterior ao FREEZE, salvo o proprio FREEZE)
adendo_dir = os.path.join(W, "5_R2", "0_ADENDO")
posteriores = []
for dp, dn, fn in os.walk(LONG + adendo_dir):
    for f in fn:
        lp = os.path.join(dp, f)
        m = datetime.datetime.fromtimestamp(os.stat(lp).st_mtime, datetime.timezone.utc)
        if m > frozen + datetime.timedelta(seconds=2):
            posteriores.append({"arquivo": os.path.relpath(lp, LONG + adendo_dir), "mtime_utc": m.isoformat()})
out["0_ADENDO_arquivos_com_mtime_posterior_ao_FREEZE"] = posteriores
it.append(item("0_ADENDO sem arquivo alterado depois do FREEZE_R2", len(posteriores), 0))


# V2: mtimes de 1_PEDRA e 2_REENSAIO
def walk(root):
    for dp, dn, fn in os.walk(LONG + root):
        dn.sort()
        for f in sorted(fn):
            yield os.path.join(dp, f)


v2 = {}
for sub in ("1_PEDRA", "2_REENSAIO"):
    root = os.path.join(W, "5_R2", sub)
    antes, depois = [], []
    for lp in walk(root):
        rel = os.path.relpath(lp, LONG + root).replace("\\", "/")
        m = datetime.datetime.fromtimestamp(os.stat(lp).st_mtime, datetime.timezone.utc)
        (depois if m > frozen else antes).append({"arquivo": rel, "mtime_utc": m.isoformat()})
    v2[sub] = {"n_arquivos": len(antes) + len(depois), "n_depois_do_FREEZE_R2": len(depois),
               "n_antes_do_FREEZE_R2": len(antes), "arquivos_antes_do_FREEZE_R2": antes}
out["V2_mtimes"] = v2
# V2: horas de inicio declaradas nos recibos
ped = json.load(open(os.path.join(W, "5_R2", "1_PEDRA", "logs", "R2_T02_recibo.json"), encoding="utf-8"))
ree = json.load(open(os.path.join(W, "5_R2", "2_REENSAIO", "RESULTADO_REENSAIO_R2.json"), encoding="utf-8"))
aud = json.load(open(os.path.join(W, "5_R2", "1_PEDRA", "logs", "R2_AUDIT_TIPOS_recibo.json"), encoding="utf-8"))
t01 = json.load(open(os.path.join(W, "5_R2", "1_PEDRA", "logs", "R2_T01_recibo.json"), encoding="utf-8"))
v4 = json.load(open(os.path.join(W, "5_R2", "2_REENSAIO", "2_OPTICO", "RESULTADO_OPTICO.json"), encoding="utf-8"))
out["V2_inicios"] = []
for nome, s in (("pedra T02 compilacao start_utc", ped["start_utc"]), ("pedra T01 compilacao start_utc", t01["start_utc"]),
                ("pedra AuditTipos start_utc", aud["start_utc"]), ("reensaio tentativa_002 inicio_utc", ree["inicio_utc"])):
    d = datetime.datetime.fromisoformat(s)
    out["V2_inicios"].append({"item": nome, "utc": s, "segundos_depois_do_FREEZE_R2": (d - frozen).total_seconds(),
                              "posterior": d > frozen})
out["V4_RESULTADO_OPTICO_chaves_de_tempo"] = {k: v4.get(k) for k in ("inicio_utc", "inicio_local", "fim_utc", "tentativa", "modo") if k in v4}
# hashes declarados vs disco (pedra)
P = os.path.join(W, "5_R2", "1_PEDRA")
res = json.load(open(os.path.join(P, "RESULTADO_PEDRA_R2.json"), encoding="utf-8"))
it.append(item("pedra R2 .lean sha256 (disco == RESULTADO_PEDRA_R2)", sha(res["pedra_R2"]["arquivo"]), res["pedra_R2"]["sha256"]))
it.append(item("pedra R2 .lean sha256 == enunciado", sha(res["pedra_R2"]["arquivo"]), EXP_PEDRA))
it.append(item("pedra R2 .lean bytes", os.path.getsize(res["pedra_R2"]["arquivo"]), 120054))
it.append(item("pedra R2 .olean sha256 (disco == RESULTADO_PEDRA_R2)", sha(res["pedra_R2"]["olean"]), res["pedra_R2"]["olean_sha256"]))
it.append(item("pedra R2 .olean sha256 == enunciado", sha(res["pedra_R2"]["olean"]), EXP_OLEAN))
it.append(item("pedra R1 fonte sha256 (3_KERNEL/sandbox)", sha(res["pedra_R2"]["fonte_R1"]["arquivo"]), res["pedra_R2"]["fonte_R1"]["sha256"]))
it.append(item("copia T00_R1 == fonte R1", sha(os.path.join(P, "tentativas", "T00_R1_TheTimeHasNoRank.lean")), res["pedra_R2"]["fonte_R1"]["sha256"]))
it.append(item("recibo T02 source_sha256 == pedra", ped["source_sha256"], res["pedra_R2"]["sha256"]))
it.append(item("recibo T02 olean_sha256 == pedra olean", ped.get("olean_sha256"), res["pedra_R2"]["olean_sha256"]))
it.append(item("recibo T02 exit_code", ped["exit_code"], 0))
it.append(item("recibo T02 n_error", ped["n_error"], 0))
it.append(item("recibo T02 n_warning", ped["n_warning"], 0))
it.append(item("recibo T02 n_sorryAx_na_saida", ped["n_sorryAx_na_saida"], 0))
it.append(item("recibo T02 fora_do_trio", ped["fora_do_trio"], []))
it.append(item("recibo T02 n_axiom_lines", ped["n_axiom_lines"], 152))
it.append(item("recibo T02 saida sha256 (disco)", sha(os.path.join(P, ped["output"])), ped["output_sha256"]))
it.append(item("recibo T02 LEAN_PATH so no .lake do Nos (sem sandbox/3_KERNEL)", all(("tgl_kernel\\.lake" in s) for s in ped["LEAN_PATH"].split(";")), True))
it.append(item("recibo T02 -o dentro do sandbox 1_PEDRA", ped["command"][-1].startswith(os.path.join(P, "sandbox")), True))
it.append(item("DIFF.patch sha256", sha(os.path.join(P, "saidas", "DIFF.patch")), res["diff"]["sha256"]))
it.append(item("T01 fonte preservada sha256", sha(os.path.join(P, "tentativas", "T01_R2_TheTimeIsNotAPost.lean")), res["tentativas_preservadas"]["T01"]["sha256"]))
it.append(item("T01 olean preservado sha256", sha(os.path.join(P, "tentativas", "T01_R2_TheTimeIsNotAPost.olean")), res["tentativas_preservadas"]["T01"]["olean_sha256"]))
it.append(item("1_PEDRA sem toolchain restante", os.path.exists(os.path.join(P, "sandbox", "toolchain")), False))
it.append(item("1_PEDRA sem .lake no sandbox", os.path.exists(os.path.join(P, "sandbox", ".lake")), False))
# manifesto da pedra
man = json.load(open(os.path.join(P, "MANIFESTO_1_PEDRA.json"), encoding="utf-8"))
mlist = man.get("arquivos") or man.get("files") or man
out["manifesto_1_PEDRA_tipo"] = type(mlist).__name__
# manifesto do reensaio
R = os.path.join(W, "5_R2", "2_REENSAIO")
rec = json.load(open(os.path.join(R, "RECIBO_REENSAIO_R2.json"), encoding="utf-8"))
out["recibo_reensaio_chaves"] = sorted(rec.keys())
it.append(item("RESULTADO_REENSAIO_R2.json sha256 == enunciado", sha(os.path.join(R, "RESULTADO_REENSAIO_R2.json")), EXP_REENSAIO))
it.append(item("reensaio_r2.py sha256 == declarado", sha(os.path.join(R, "reensaio_r2.py")), ree["runner_r2"]["sha256"]))
it.append(item("T9c_float_E2_por_k.tsv sha256 == declarado", sha(os.path.join(R, "T9c_float_E2_por_k.tsv")), ree["tabela_por_k"]["sha256"]))
it.append(item("tentativa_002 RESULTADO == raiz (bytes)", sha(os.path.join(R, "tentativas", "tentativa_002_ensaio", "RESULTADO_REENSAIO_R2.json")), sha(os.path.join(R, "RESULTADO_REENSAIO_R2.json"))))
it.append(item("reensaio importou normativa congelada (sha)", ree["implementacao_normativa_importada"]["sha256"], norm["sha256"]))
it.append(item("copia da normativa em 2_REENSAIO/scripts == congelada", sha(os.path.join(R, "scripts", "tolerancia_uniforme_r2.py")), norm["sha256"]))
it.append(item("runner R1 copiado == R1 (sha)", sha(os.path.join(R, "2_OPTICO", "run_optico.py")), sha(os.path.join(W, "2_OPTICO", "run_optico.py"))))
it.append(item("runner R1 sha == fcc289889ec418ba...", sha(os.path.join(W, "2_OPTICO", "run_optico.py"))[:16], "fcc289889ec418ba"))
it.append(item("V4 RESULTADO_OPTICO sha == b6cf4e65...", sha(os.path.join(R, "2_OPTICO", "RESULTADO_OPTICO.json"))[:16], "b6cf4e6567f5a863"))
it.append(item("reensaio valido", ree["valido"], True))
it.append(item("reensaio motivos_de_INVALIDO vazio", ree["motivos_de_INVALIDO"], []))
it.append(item("reensaio semente", ree["semente"], 20261012))
# R1 congelada intacta: RESULTADO_OPTICO R1, DIAGNOSTICO, pedra R1 olean
it.append(item("R1 RESULTADO_OPTICO sha == 2c67b7ea6f118630...", sha(os.path.join(W, "2_OPTICO", "RESULTADO_OPTICO.json"))[:16], "2c67b7ea6f118630"))
it.append(item("R1 DIAGNOSTICO_T9c sha == 26a68eff64aeb7e4...", sha(os.path.join(W, "2_OPTICO", "diagnostico", "DIAGNOSTICO_T9c.json"))[:16], "26a68eff64aeb7e4"))
it.append(item("R1 pedra .olean sha == 9f473a088262b073...", sha(os.path.join(W, "3_KERNEL", "sandbox", "TheTimeHasNoRank.olean"))[:16], "9f473a088262b073"))
it.append(item("R1 RELATORIO_FINAL sha == 7b6dcb18a4440be1...", sha(os.path.join(W, "4_RELATORIO", "RELATORIO_FINAL.md"))[:16], "7b6dcb18a4440be1"))
out["n_itens"] = len(it)
out["falhas"] = [x for x in it if not x["ok"]]
out["todos_ok"] = not out["falhas"]
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ("itens", "V2_mtimes")}, ensure_ascii=False, indent=1))
for sub, v in v2.items():
    print(sub, "antes:", v["n_antes_do_FREEZE_R2"], "depois:", v["n_depois_do_FREEZE_R2"])
    for a in v["arquivos_antes_do_FREEZE_R2"]:
        print("   ANTES", a["arquivo"], a["mtime_utc"])
