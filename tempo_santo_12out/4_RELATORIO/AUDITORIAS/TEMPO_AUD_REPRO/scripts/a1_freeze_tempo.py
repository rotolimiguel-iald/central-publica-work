"""A1 — Auditor F1.TEMPO (lente REPRODUCAO). Confere, so lendo:
 (1) FREEZE.json: sha256/bytes; cada item congelado (PREREGISTRO.json/.md e anexos) por sha256 e bytes;
 (2) 1_PREREGISTRO: nenhum arquivo fora da lista congelada; nenhum mtime depois do FREEZE;
 (3) 2_OPTICO e 3_KERNEL: TODOS os arquivos (recursivo) com sha256, bytes, mtime e birthtime
     comparados com o instante do FREEZE (congelado_em_utc) e com o mtime/birthtime do proprio FREEZE.json;
 (4) as listas de hash declaradas pelos construtores (RECIBO_OPTICO.arquivos_de_2_OPTICO,
     MANIFESTO_3_KERNEL.arquivos, TENTATIVAS) contra os bytes atuais.
Saida: JSON no caminho dado. Nada e escrito fora da pasta do auditor."""
import datetime as dt
import hashlib
import json
import os
import sys

BASE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
PRE = os.path.join(BASE, "1_PREREGISTRO")
OPT = os.path.join(BASE, "2_OPTICO")
KER = os.path.join(BASE, "3_KERNEL")
FREEZE_SHA = "6b29d4c9b09e5553a3d58a3933137bbf73df3d0b6632b036e0a74abef7533c9b"


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def stamp(p):
    st = os.stat(p)
    bt = getattr(st, "st_birthtime_ns", None)
    return st.st_size, st.st_mtime_ns, bt


def iso(ns):
    if ns is None:
        return None
    return dt.datetime.fromtimestamp(ns / 1e9, tz=dt.timezone.utc).isoformat()


out = {"checks": [], "falhas": 0}


def chk(item, esperado, lido):
    ok = esperado == lido
    out["checks"].append({"item": item, "esperado": esperado, "lido": lido, "ok": ok})
    if not ok:
        out["falhas"] += 1
    return ok


fz = os.path.join(PRE, "FREEZE.json")
fzb = open(fz, "rb").read()
chk("FREEZE.json sha256", FREEZE_SHA, hashlib.sha256(fzb).hexdigest())
chk("FREEZE.json bytes", 5986, len(fzb))
F = json.loads(fzb.decode("utf-8"))
t_freeze = dt.datetime.fromisoformat(F["congelado_em_utc"])
t_freeze_ns = int(round(t_freeze.timestamp() * 1e9))
fz_size, fz_mtime, fz_birth = stamp(fz)
out["freeze"] = {"congelado_em_utc": F["congelado_em_utc"], "t_ns": t_freeze_ns,
                 "FREEZE.json_mtime_utc": iso(fz_mtime), "FREEZE.json_birth_utc": iso(fz_birth)}

# (1) itens congelados
lista = [("PREREGISTRO.json", F["preregistro_json"]["sha256"], F["preregistro_json"]["bytes"]),
         ("PREREGISTRO.md", F["preregistro_md"]["sha256"], F["preregistro_md"]["bytes"])]
for a in F["anexos"]:
    lista.append((a["caminho"], a["sha256"], a["bytes"]))
congelados = set()
for rel, h, b in lista:
    p = os.path.join(PRE, rel.replace("/", os.sep))
    congelados.add(os.path.normcase(os.path.normpath(p)))
    data = open(p, "rb").read()
    chk(f"congelado {rel} sha256", h, hashlib.sha256(data).hexdigest())
    chk(f"congelado {rel} bytes", b, len(data))

# (2) 1_PREREGISTRO: arquivos fora da lista e mtimes
extra, depois = [], []
pre_files = []
for dp, dn, fn in os.walk(PRE):
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, PRE).replace(os.sep, "/")
        s, m, bt = stamp(p)
        pre_files.append({"rel": rel, "bytes": s, "mtime_utc": iso(m), "birth_utc": iso(bt)})
        if os.path.normcase(os.path.normpath(p)) not in congelados and rel != "FREEZE.json":
            extra.append(rel)
        if rel != "FREEZE.json" and m > fz_mtime:
            depois.append({"rel": rel, "mtime_utc": iso(m)})
out["pre"] = {"n_arquivos": len(pre_files), "fora_da_lista_congelada": extra,
              "mtime_depois_do_FREEZE_json": depois,
              "max_mtime_utc_exceto_FREEZE": max((x["mtime_utc"] for x in pre_files if x["rel"] != "FREEZE.json"))}
chk("1_PREREGISTRO: arquivos fora da lista congelada", [], extra)
chk("1_PREREGISTRO: mtime depois do FREEZE.json", [], depois)

# (3) 2_OPTICO e 3_KERNEL
res = {}
for nome, raiz in (("2_OPTICO", OPT), ("3_KERNEL", KER)):
    arqs = []
    for dp, dn, fn in os.walk(raiz):
        for f in fn:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, raiz).replace(os.sep, "/")
            s, m, bt = stamp(p)
            arqs.append({"rel": rel, "sha256": sha(p), "bytes": s, "mtime_ns": m, "birth_ns": bt,
                         "mtime_utc": iso(m), "birth_utc": iso(bt),
                         "mtime_depois_do_freeze": m > t_freeze_ns,
                         "birth_depois_do_freeze": (bt is None) or (bt > t_freeze_ns),
                         "mtime_depois_do_FREEZE_json_mtime": m > fz_mtime})
    arqs.sort(key=lambda x: x["mtime_ns"])
    dirs = []
    for dp, dn, fn in os.walk(raiz):
        s, m, bt = stamp(dp)
        dirs.append({"dir": os.path.relpath(dp, BASE), "birth_utc": iso(bt), "mtime_utc": iso(m),
                     "birth_depois_do_freeze": (bt is None) or (bt > t_freeze_ns)})
    res[nome] = {"n": len(arqs),
                 "min_mtime_utc": arqs[0]["mtime_utc"], "min_mtime_rel": arqs[0]["rel"],
                 "min_birth_utc": iso(min(a["birth_ns"] for a in arqs)),
                 "todos_mtime_depois": all(a["mtime_depois_do_freeze"] for a in arqs),
                 "todos_birth_depois": all(a["birth_depois_do_freeze"] for a in arqs),
                 "folga_min_s_mtime": round((arqs[0]["mtime_ns"] - t_freeze_ns) / 1e9, 3),
                 "folga_min_s_birth": round((min(a["birth_ns"] for a in arqs) - t_freeze_ns) / 1e9, 3),
                 "dirs": dirs, "arquivos": arqs}
    chk(f"{nome}: todos os arquivos com mtime depois do FREEZE", True, res[nome]["todos_mtime_depois"])
    chk(f"{nome}: todos os arquivos com birth depois do FREEZE", True, res[nome]["todos_birth_depois"])
out["pastas"] = res

# (4) listas de hash dos construtores
rec = json.load(open(os.path.join(OPT, "RECIBO_OPTICO.json"), encoding="utf-8"))
atual_opt = {a["rel"]: a for a in res["2_OPTICO"]["arquivos"]}
for rel, d in rec["arquivos_de_2_OPTICO"].items():
    a = atual_opt.get(rel)
    chk(f"RECIBO_OPTICO {rel}", (d["sha256"], d["bytes"]), (a["sha256"], a["bytes"]) if a else None)
nao_listados_opt = sorted(set(atual_opt) - set(rec["arquivos_de_2_OPTICO"]))
out["2_OPTICO_nao_listados_no_RECIBO"] = nao_listados_opt
man = json.load(open(os.path.join(KER, "MANIFESTO_3_KERNEL.json"), encoding="utf-8"))
atual_ker = {a["rel"]: a for a in res["3_KERNEL"]["arquivos"]}
for d in man["arquivos"]:
    a = atual_ker.get(d["arquivo"])
    chk(f"MANIFESTO_3_KERNEL {d['arquivo']}", (d["sha256"], d["bytes"]), (a["sha256"], a["bytes"]) if a else None)
out["3_KERNEL_nao_listados_no_MANIFESTO"] = sorted(set(atual_ker) - {d["arquivo"] for d in man["arquivos"]})

# hashes que os construtores declararam no resultado da tarefa
decl = {
    ("2_OPTICO", "RESULTADO_OPTICO.json"): "2c67b7ea6f118630fd1794099c798d35167c27fd9c93d048b9487315ac50ef26",
    ("2_OPTICO", "run_optico.py"): "fcc289889ec418ba1cebdf132e15e7e61533d0b8466e929cf162996cc0a39406",
    ("3_KERNEL", "sandbox/TheTimeHasNoRank.lean"): "7105eda468b60309fea2084d7068bf86b34d8d3b3785bcdaaa7bd582334eaf5b",
    ("3_KERNEL", "sandbox/TheTimeHasNoRank.olean"): "9f473a088262b0735b14a82d02d7fa387f09ad07731ec90b7196b8341a1f5012",
}
for (pasta, rel), h in decl.items():
    a = (atual_opt if pasta == "2_OPTICO" else atual_ker).get(rel)
    chk(f"declarado na tarefa {pasta}/{rel}", h, a["sha256"] if a else None)

tmp = sys.argv[1] + ".tmp"
with open(tmp, "w", encoding="utf-8") as fo:
    json.dump(out, fo, indent=1, ensure_ascii=False)
os.replace(tmp, sys.argv[1])
print("falhas:", out["falhas"], "de", len(out["checks"]))
print("freeze:", out["freeze"])
print("pre:", {k: v for k, v in out["pre"].items()})
for nome in res:
    r = res[nome]
    print(nome, {k: r[k] for k in ("n", "min_mtime_utc", "min_mtime_rel", "min_birth_utc", "todos_mtime_depois",
                                  "todos_birth_depois", "folga_min_s_mtime", "folga_min_s_birth")})
    for d in r["dirs"]:
        print("   dir", d)
print("2_OPTICO nao listados no RECIBO:", nao_listados_opt)
print("3_KERNEL nao listados no MANIFESTO:", out["3_KERNEL_nao_listados_no_MANIFESTO"])
for c in out["checks"]:
    if not c["ok"]:
        print("FALHA:", c)
