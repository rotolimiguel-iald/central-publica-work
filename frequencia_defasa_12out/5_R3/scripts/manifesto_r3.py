# -*- coding: utf-8 -*-
r"""RODADA 3 — manifesto final: sha256 e bytes de TODO arquivo de 5_R3 (gravado por ultimo; nao inclui a si mesmo porque e
calculado antes de gravar). Confere que nao restou toolchain, build nem .lake dentro de 5_R3 e que as pastas 0-4 da unidade
nao foram tocadas depois do inicio da rodada (mtime < inicio da rodada 3, lido do IMPRESSAO_DIGITAL_KERNEL_ANTES.json).
Grava 5_R3\MANIFESTO_R3.json (recusa sobrescrever)."""
import hashlib, json, os, time, datetime

R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNID = os.path.dirname(R3)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


dst = os.path.join(R3, "MANIFESTO_R3.json")
if os.path.exists(dst):
    raise SystemExit("FALHA VISIVEL: MANIFESTO_R3.json ja existe (nao sobrescrevo)")
itens, restos, total = {}, [], 0
for dp, dns, fns in os.walk(R3):
    for d in dns:
        if d in ("toolchain_v4.31.0", "build", ".lake"):
            restos.append(os.path.join(dp, d))
    for fn in fns:
        p = os.path.join(dp, fn)
        rel = os.path.relpath(p, R3).replace("\\", "/")
        if rel == "MANIFESTO_R3.json":
            continue
        itens[rel] = {"bytes": os.path.getsize(p), "sha256": sha(p)}
        total += itens[rel]["bytes"]
# inicio da rodada 3 = mtime do IMPRESSAO_DIGITAL_KERNEL_ANTES.json (primeiro artefato gravado)
ini = os.path.getmtime(os.path.join(R3, "IMPRESSAO_DIGITAL_KERNEL_ANTES.json"))
tocados = []
for pasta in ("0_LEVANTAMENTO", "1_PREREGISTRO", "2_OPTICO", "3_KERNEL", "4_RELATORIO"):
    for dp, dns, fns in os.walk(os.path.join(UNID, pasta)):
        for fn in fns:
            p = os.path.join(dp, fn)
            if os.path.getmtime(p) >= ini - 60:
                tocados.append(os.path.relpath(p, UNID))
out = {"documento": "MANIFESTO da RODADA 3 (5_R3) — sha256 de todo arquivo da pasta, gravado por ultimo",
       "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "inicio_rodada3_local": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ini)),
       "n_arquivos": len(itens), "bytes_total": total, "restos_toolchain_build_lake": restos,
       "arquivos_das_pastas_0_a_4_modificados_depois_do_inicio": tocados, "arquivos": itens}
tmp = dst + ".tmp"
with open(tmp, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
os.replace(tmp, dst)
print(json.dumps({k: out[k] for k in out if k != "arquivos"}, ensure_ascii=False, indent=1))
