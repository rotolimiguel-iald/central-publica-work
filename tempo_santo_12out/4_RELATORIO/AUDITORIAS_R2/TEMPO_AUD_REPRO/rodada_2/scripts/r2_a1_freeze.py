"""Auditor de reproducao F1.TEMPO, rodada 2 -- item (1): o FREEZE e anterior a TODO arquivo de 2_OPTICO e 3_KERNEL?
Somente leitura na casa. Saida: um JSON na pasta do auditor (argv[1]).
Confere: sha256/bytes do FREEZE e dos 30 itens que ele lista; mtime e birthtime (UTC) de todo arquivo e pasta
de 2_OPTICO e 3_KERNEL contra congelado_em_utc; quais arquivos a jusante citam o sha256 do FREEZE / PREREGISTRO
(compromisso por hash: quem cita um hash so pode ter sido escrito depois de existir o conteudo).
"""
import hashlib, json, os, sys, datetime as dt

BASE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
LONG = "\\\\?\\"
FREEZE = os.path.join(BASE, "1_PREREGISTRO", "FREEZE.json")
FREEZE_SHA_ESPERADO = "6b29d4c9b09e5553a3d58a3933137bbf73df3d0b6632b036e0a74abef7533c9b"


def sha(p):
    h = hashlib.sha256()
    with open(LONG + p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def utc(ts):
    return dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc)


def walk(root):
    for dp, dn, fn in os.walk(LONG + root):
        dn.sort()
        yield ("dir", dp[len(LONG):])
        for f in sorted(fn):
            yield ("file", os.path.join(dp, f)[len(LONG):])


out = {"o_que": "item (1) da auditoria de reproducao, rodada 2", "quando_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
fb = open(FREEZE, "rb").read()
fsha = hashlib.sha256(fb).hexdigest()
fz = json.loads(fb.decode("utf-8"))
t_freeze = dt.datetime.fromisoformat(fz["congelado_em_utc"])
st = os.stat(FREEZE)
out["freeze"] = {"sha256": fsha, "bytes": len(fb), "sha_confere": fsha == FREEZE_SHA_ESPERADO, "bytes_confere": len(fb) == 5986,
                 "congelado_em_utc": fz["congelado_em_utc"], "mtime_utc": utc(st.st_mtime).isoformat(),
                 "birth_utc": utc(st.st_birthtime).isoformat(),
                 "mtime_menos_congelado_s": (utc(st.st_mtime) - t_freeze).total_seconds()}

# 30 itens do FREEZE
itens = [("PREREGISTRO.json", fz["preregistro_json"]["sha256"], fz["preregistro_json"]["bytes"]),
         ("PREREGISTRO.md", fz["preregistro_md"]["sha256"], fz["preregistro_md"]["bytes"])]
itens += [(a["caminho"], a["sha256"], a["bytes"]) for a in fz["anexos"]]
conf = []
for rel, h, b in itens:
    p = os.path.join(BASE, "1_PREREGISTRO", rel.replace("/", "\\"))
    ok = os.path.exists(LONG + p)
    hh = sha(p) if ok else None
    bb = os.path.getsize(LONG + p) if ok else None
    stp = os.stat(LONG + p) if ok else None
    conf.append({"rel": rel, "sha_ok": hh == h, "bytes_ok": bb == b,
                 "mtime_utc": utc(stp.st_mtime).isoformat() if ok else None,
                 "mtime_antes_ou_igual_freeze": (utc(stp.st_mtime) <= utc(st.st_mtime)) if ok else None})
out["itens_freeze"] = {"n": len(conf), "todos_sha_ok": all(c["sha_ok"] for c in conf), "todos_bytes_ok": all(c["bytes_ok"] for c in conf),
                       "todos_mtime_ate_o_freeze": all(c["mtime_antes_ou_igual_freeze"] for c in conf), "lista": conf}

# 1_PREREGISTRO: nada novo, nada depois do FREEZE
pre = []
listados = {os.path.normcase(os.path.join(BASE, "1_PREREGISTRO", r.replace("/", "\\"))) for r, _, _ in itens}
listados.add(os.path.normcase(FREEZE))
for kind, p in walk(os.path.join(BASE, "1_PREREGISTRO")):
    s = os.stat(LONG + p)
    pre.append({"tipo": kind, "rel": os.path.relpath(p, BASE), "mtime_utc": utc(s.st_mtime).isoformat(),
                "depois_do_freeze_file": utc(s.st_mtime) > utc(st.st_mtime),
                "nao_listado": (kind == "file" and os.path.normcase(p) not in listados)})
out["pasta_1_PREREGISTRO"] = {"arquivos": sum(1 for x in pre if x["tipo"] == "file"),
                              "arquivos_nao_listados_no_freeze": [x["rel"] for x in pre if x["nao_listado"]],
                              "itens_com_mtime_posterior_ao_FREEZE_json": [x for x in pre if x["depois_do_freeze_file"]]}

# 2_OPTICO e 3_KERNEL (e, informativo, 4_RELATORIO e 5_R2)
PRE_SHA = fz["preregistro_json"]["sha256"]
for pasta in ["2_OPTICO", "3_KERNEL", "4_RELATORIO", "5_R2"]:
    root = os.path.join(BASE, pasta)
    files, dirs = [], []
    for kind, p in walk(root):
        s = os.stat(LONG + p)
        rec = {"rel": os.path.relpath(p, BASE), "mtime_utc": utc(s.st_mtime).isoformat(), "birth_utc": utc(s.st_birthtime).isoformat()}
        rec["mtime_depois"] = utc(s.st_mtime) > t_freeze
        rec["birth_depois"] = utc(s.st_birthtime) > t_freeze
        if kind == "file":
            rec["bytes"] = s.st_size
            rec["sha256"] = sha(p)
            try:
                with open(LONG + p, "rb") as f:
                    data = f.read()
                rec["cita_sha_freeze"] = FREEZE_SHA_ESPERADO.encode() in data or FREEZE_SHA_ESPERADO[:16].encode() in data
                rec["cita_sha_preregistro"] = PRE_SHA.encode() in data or PRE_SHA[:16].encode() in data
            except Exception as e:
                rec["erro_leitura"] = repr(e)
            files.append(rec)
        else:
            dirs.append(rec)
    antes_m = [r for r in files if not r["mtime_depois"]]
    antes_b = [r for r in files if not r["birth_depois"]]
    dantes_b = [r for r in dirs if not r["birth_depois"]]
    out["pasta_" + pasta] = {
        "arquivos": len(files), "pastas": len(dirs),
        "mtime_min_utc": min((r["mtime_utc"] for r in files), default=None),
        "mtime_max_utc": max((r["mtime_utc"] for r in files), default=None),
        "birth_min_utc": min((r["birth_utc"] for r in files), default=None),
        "arquivos_com_mtime_ate_o_freeze": [(r["rel"], r["mtime_utc"]) for r in antes_m],
        "arquivos_com_birth_ate_o_freeze": [(r["rel"], r["birth_utc"]) for r in antes_b],
        "pastas_com_birth_ate_o_freeze": [(r["rel"], r["birth_utc"]) for r in dantes_b],
        "arquivos_que_citam_sha_do_freeze": sum(1 for r in files if r.get("cita_sha_freeze")),
        "arquivos_que_citam_sha_do_preregistro": sum(1 for r in files if r.get("cita_sha_preregistro")),
        "primeiro_que_cita_freeze_por_mtime": min(((r["mtime_utc"], r["rel"]) for r in files if r.get("cita_sha_freeze")), default=None),
        "lista": files}

out["veredito_item_1"] = {
    "freeze_sha_e_bytes": out["freeze"]["sha_confere"] and out["freeze"]["bytes_confere"],
    "30_itens_conferem": out["itens_freeze"]["todos_sha_ok"] and out["itens_freeze"]["todos_bytes_ok"] and out["itens_freeze"]["n"] == 30,
    "1_PREREGISTRO_sem_arquivo_novo_nem_posterior": (not out["pasta_1_PREREGISTRO"]["arquivos_nao_listados_no_freeze"]) and (not out["pasta_1_PREREGISTRO"]["itens_com_mtime_posterior_ao_FREEZE_json"]),
    "2_OPTICO_todos_depois": not out["pasta_2_OPTICO"]["arquivos_com_mtime_ate_o_freeze"] and not out["pasta_2_OPTICO"]["arquivos_com_birth_ate_o_freeze"],
    "3_KERNEL_todos_depois": not out["pasta_3_KERNEL"]["arquivos_com_mtime_ate_o_freeze"] and not out["pasta_3_KERNEL"]["arquivos_com_birth_ate_o_freeze"],
}
with open(sys.argv[1], "w", encoding="utf-8") as fo:
    json.dump(out, fo, indent=1, ensure_ascii=False)
v = out["veredito_item_1"]
print(json.dumps(v, ensure_ascii=False))
for pasta in ["2_OPTICO", "3_KERNEL", "4_RELATORIO", "5_R2"]:
    q = out["pasta_" + pasta]
    print(pasta, q["arquivos"], "arq;", q["pastas"], "pastas; mtime", q["mtime_min_utc"], "->", q["mtime_max_utc"], "; birth_min", q["birth_min_utc"],
          "; cita FREEZE:", q["arquivos_que_citam_sha_do_freeze"], "; cita PRE:", q["arquivos_que_citam_sha_do_preregistro"],
          "; primeiro a citar:", q["primeiro_que_cita_freeze_por_mtime"])
    print("   antes(m):", q["arquivos_com_mtime_ate_o_freeze"][:5], " antes(b):", q["arquivos_com_birth_ate_o_freeze"][:5], " pastas antes(b):", q["pastas_com_birth_ate_o_freeze"][:5])
print("freeze:", out["freeze"])
print("1_PRE nao listados:", out["pasta_1_PREREGISTRO"]["arquivos_nao_listados_no_freeze"])
print("1_PRE posteriores:", [(x["rel"], x["mtime_utc"]) for x in out["pasta_1_PREREGISTRO"]["itens_com_mtime_posterior_ao_FREEZE_json"]])
