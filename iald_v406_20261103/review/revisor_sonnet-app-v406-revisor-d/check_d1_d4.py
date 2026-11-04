# -*- coding: utf-8 -*-
"""Revisor independente da INSTALACAO v406 - D1..D4 e a parte de arquivo de D6. Somente leitura.
Nao importa verify_installed.py; recalcula tudo a partir dos bytes."""
import sys
sys.dont_write_bytecode = True
import json, hashlib, os, time
from pathlib import Path

W = Path("C:/IALD/Central de Patentes/work/iald_v406_20261103")
ROOT = Path("C:/IALD/projetos_pyhton/IALD")
OUT = W / "review/revisor_sonnet-app-v406-revisor-d"
REL = ROOT / "canonical_releases" / "v406_a381c4d14709"
INSTALL_START = time.mktime((2026, 11, 3, 20, 18, 0, 0, 0, -1))  # 03/11/2026 20:18 local


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(p):
    return os.path.normcase(os.path.normpath(str(p)))


R = {"checks": {}, "numbers": {}, "findings": []}

plan_raw = (W / "install_plan.json").read_bytes()
plan_sha = sha_bytes(plan_raw)
plan = json.loads(plan_raw)
files = plan["files"]
rf = json.loads((W / "validation/review_final.json").read_bytes())
dep = json.loads((W / "deployment.json").read_bytes())
fc = json.loads((W / "validation/final_checks.json").read_bytes())

# ---------------- D1 ----------------
tools_now = {n: sha_file(W / n) for n in ("deploy_controlled.py", "transaction.py", "maintenance.py", "verify_installed.py")}
tools_rec = {"deploy_controlled.py": rf["deploy_controlled_sha256"], "transaction.py": rf["transaction_sha256"],
             "maintenance.py": rf["maintenance_sha256"], "verify_installed.py": rf["verify_installed_sha256"]}
d1 = {
    "plan_sha256_recalculado": plan_sha,
    "review_final.plan_sha256": rf["plan_sha256"],
    "deployment.plan_sha256": dep["plan_sha256"],
    "final_checks.plan_sha256": fc["plan_sha256"],
    "tools_recalculados": tools_now,
    "tools_gravados_review_final": tools_rec,
    "review_final_status": rf["status"],
    "review_final_checks_total": len(rf["checks"]),
    "review_final_checks_falsos": sum(1 for c in rf["checks"] if not c.get("pass")),
    "review_final_findings": len(rf["findings"]),
}
d1["PASS"] = (plan_sha == rf["plan_sha256"] == dep["plan_sha256"] == fc["plan_sha256"]
              and all(tools_now[k] == tools_rec[k] for k in tools_now))
R["checks"]["D1"] = d1

# ---------------- D2 ----------------
bad, missing, errs, src_bad, dep_bad = [], [], [], [], []
total_bytes = 0
t0 = time.time()
for it in files:
    dest = Path(it["destination"])
    try:
        if not dest.is_file():
            missing.append(str(dest))
            continue
        h = sha_file(dest)
        total_bytes += dest.stat().st_size
        if h != it["sha256"]:
            bad.append({"dest": str(dest), "disk": h, "plano": it["sha256"]})
        if dep["files"].get(str(dest)) != it["sha256"]:
            dep_bad.append(str(dest))
        src = Path(it["source"])
        if src.is_file():
            if sha_file(src) != it["sha256"]:
                src_bad.append(str(src))
        else:
            src_bad.append("AUSENTE:" + str(src))
    except Exception as e:  # noqa
        errs.append({"dest": str(dest), "err": repr(e)})
d2 = {"arquivos_no_plano": len(files), "ok_no_disco": len(files) - len(bad) - len(missing) - len(errs),
      "divergentes": bad[:10], "n_divergentes": len(bad), "ausentes": missing[:10], "n_ausentes": len(missing),
      "erros": errs[:10], "n_erros": len(errs), "bytes_totais_instalados": total_bytes,
      "deployment.files_entradas": len(dep["files"]), "deployment.files_divergem_do_plano": len(dep_bad),
      "staging_diverge_do_plano": len(src_bad), "staging_exemplos": src_bad[:5], "segundos": round(time.time() - t0, 1)}
d2["PASS"] = (len(files) == 1773 and not bad and not missing and not errs and len(dep["files"]) == len(files) and not dep_bad)
R["checks"]["D2"] = d2

# ---------------- D3 ----------------
back = dep["backups"]
base_items = [it for it in files if it.get("baseline")]
d3_rows, d3_ok = [], True
stamps = set()
for it in base_items:
    dest = it["destination"]
    row = {"dest": dest.replace("C:\\IALD\\projetos_pyhton\\IALD\\", ""), "baseline_plano": it["baseline"][:16],
           "novo_plano": it["sha256"][:16]}
    bp = back.get(dest)
    if not bp:
        row["backup"] = None
        d3_ok = False
    else:
        bpp = Path(bp)
        row["backup_nome"] = bpp.name
        row["ao_lado"] = (norm(bpp.parent) == norm(Path(dest).parent)) and bpp.name.startswith(Path(dest).name + ".bak_")
        stamps.add(bpp.name.split(".bak_")[-1])
        if bpp.is_file():
            hb = sha_file(bpp)
            row["sha_backup"] = hb[:16]
            row["backup_igual_baseline"] = (hb == it["baseline"])
            row["backup_difere_do_novo"] = (hb != it["sha256"])
        else:
            row["backup_existe"] = False
        ok = row.get("ao_lado") and row.get("backup_igual_baseline")
        d3_ok = d3_ok and bool(ok)
    d3_rows.append(row)
extra_backup_keys = [k for k in back if k not in {it["destination"] for it in base_items}]
d3 = {"destinos_com_baseline": len(base_items), "backups_no_deployment": len(back), "carimbos_distintos": sorted(stamps),
      "backups_sem_baseline_no_plano": extra_backup_keys, "linhas": d3_rows}
d3["PASS"] = (len(base_items) == 7 and len(back) == 7 and d3_ok and len(stamps) == 1 and not extra_backup_keys)
R["checks"]["D3"] = d3

# ---------------- D4 ----------------
cats = {"release_v406": 0, "core_packet_raiz": 0, "haiku55": 0, "haiku": 0, "manifesto_ativo": 0, "FORA": []}
for it in files:
    d = Path(it["destination"])
    n = norm(d)
    if n.startswith(norm(REL) + os.sep):
        cats["release_v406"] += 1
    elif n == norm(ROOT / "core_packet_v406_bound.txt"):
        cats["core_packet_raiz"] += 1
    elif norm(d.parent) == norm(ROOT / ".iald_runtime" / "haiku55"):
        cats["haiku55"] += 1
    elif norm(d.parent) == norm(ROOT / ".iald_runtime" / "haiku"):
        cats["haiku"] += 1
    elif n == norm(ROOT / "iald_nucleo_fixo.json"):
        cats["manifesto_ativo"] += 1
    else:
        cats["FORA"].append(str(d))
# arquivos extras/faltando no diretorio da release
plan_rel = {norm(it["destination"]) for it in files if norm(it["destination"]).startswith(norm(REL) + os.sep)}
disk_rel = set()
for dp, dn, fn in os.walk(REL):
    for f in fn:
        disk_rel.add(norm(os.path.join(dp, f)))
extras_rel = sorted(disk_rel - plan_rel)
faltam_rel = sorted(plan_rel - disk_rel)
# restos de escrita atomica
tmp_left = []
for base in (ROOT, ROOT / ".iald_runtime" / "haiku55", ROOT / ".iald_runtime" / "haiku"):
    for p in base.glob("*.tmp_v380_*"):
        tmp_left.append(str(p))
for dp, dn, fn in os.walk(REL):
    for f in fn:
        if ".tmp_v380_" in f:
            tmp_left.append(os.path.join(dp, f))
# RUNTIME_BASELINE
rb = json.loads((W / "app/RUNTIME_BASELINE.json").read_bytes())["files"]
rb_bad, rb_missing, rb_ex = [], [], rb[0]["path"]
for e in rb:
    pth = Path(e["path"])
    if not pth.is_absolute():
        pth = ROOT / pth
    if not pth.is_file():
        rb_missing.append(str(pth))
        continue
    if sha_file(pth) != e["sha256"]:
        rb_bad.append(str(pth))
# varredura de topo: tudo que mudou em ROOT (nao recursivo) apos 20:18 local
top_changed = []
for p in ROOT.iterdir():
    try:
        if p.is_file() and p.stat().st_mtime >= INSTALL_START:
            top_changed.append(p.name)
    except OSError:
        pass
py_changed = [n for n in top_changed if n.endswith(".py")]
rb_names = {Path(e["path"]).name.casefold() for e in rb}
py_top_not_in_baseline = sorted(p.name for p in ROOT.glob("*.py") if p.name.casefold() not in rb_names)
d4 = {"deployment.accounts_modified": dep["accounts_modified"], "deployment.bench_restarted": dep["bench_restarted"],
      "deployment.client_files_changed": dep["client_files_changed"],
      "categorias_dos_destinos": {k: (v if k != "FORA" else len(v)) for k, v in cats.items()},
      "destinos_fora_do_escopo": cats["FORA"][:10],
      "arquivos_extras_no_diretorio_da_release": len(extras_rel), "extras_exemplos": extras_rel[:5],
      "arquivos_do_plano_ausentes_no_diretorio": len(faltam_rel),
      "restos_tmp_v380": tmp_left[:5],
      "RUNTIME_BASELINE_arquivos": len(rb), "RUNTIME_BASELINE_exemplo_caminho": rb_ex,
      "RUNTIME_BASELINE_divergentes": rb_bad[:10], "RUNTIME_BASELINE_ausentes": rb_missing[:10],
      "topo_ROOT_modificados_apos_20h18": sorted(top_changed), "py_topo_modificados_apos_20h18": py_changed,
      "py_topo_fora_do_baseline_informativo": py_top_not_in_baseline[:10], "n_py_topo_fora_do_baseline": len(py_top_not_in_baseline)}
d4["PASS"] = (dep["accounts_modified"] is False and dep["bench_restarted"] is False and dep["client_files_changed"] is False
              and not cats["FORA"] and cats["release_v406"] == 1765 and cats["core_packet_raiz"] == 1
              and cats["haiku55"] == 3 and cats["haiku"] == 3 and cats["manifesto_ativo"] == 1
              and not rb_bad and not rb_missing and len(rb) == 171 and not py_changed and not extras_rel and not faltam_rel and not tmp_left)
R["checks"]["D4"] = d4

# ---------------- D6 (parte de arquivo; o conteudo e' conferido contra manifest_install.json) ----------------
last = files[-1]
mf_disk_raw = (ROOT / "iald_nucleo_fixo.json").read_bytes()
mf_stage = Path(last["source"])
mf = json.loads(mf_disk_raw)
rel_ok = (mf["operational_core"]["current_release"] == "v406" and mf["active_cluster"]["release"] == "v406"
          and mf["jev_control"].get("release") == "v406")
# todos os campos "path" do manifesto
paths = []


def walk(o, trail=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "path" and isinstance(v, str):
                paths.append((trail, v, o.get("sha256") or o.get("public_sha256")))
            else:
                walk(v, trail + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, trail + "[" + str(i) + "]")


walk(mf)
fora, verificados, divergentes_h, nao_existe = [], 0, [], []
for trail, pth, h in paths:
    pp = Path(pth)
    pp_abs = pp if pp.is_absolute() else ROOT / pp
    inside = norm(pp_abs).startswith(norm(REL) + os.sep) or norm(pp_abs) == norm(ROOT / "core_packet_v406_bound.txt")
    if not inside:
        fora.append({"trail": trail, "path": pth})
    if not pp_abs.is_file():
        nao_existe.append(pth)
    elif h and len(h) == 64:
        verificados += 1
        if sha_file(pp_abs) != h:
            divergentes_h.append(pth)
d6 = {"ultimo_do_plano_e_o_manifesto": norm(last["destination"]) == norm(ROOT / "iald_nucleo_fixo.json"),
      "indice_do_manifesto_no_plano": files.index(last), "total_plano": len(files),
      "sha_manifesto_no_disco": sha_bytes(mf_disk_raw), "sha_manifest_install_staging": sha_file(mf_stage),
      "sha_manifesto_no_plano": last["sha256"],
      "operational_core.current_release": mf["operational_core"]["current_release"],
      "active_cluster.release": mf["active_cluster"]["release"], "jev_control.release": mf["jev_control"].get("release"),
      "jev_control.path": mf["jev_control"]["path"],
      "campos_path_no_manifesto": len(paths), "paths_fora_da_release_v406": fora[:10], "n_paths_fora": len(fora),
      "paths_inexistentes": nao_existe[:10], "paths_com_sha_verificados": verificados, "paths_sha_divergentes": divergentes_h[:10]}
d6["PASS"] = (d6["ultimo_do_plano_e_o_manifesto"] and d6["indice_do_manifesto_no_plano"] == len(files) - 1 and rel_ok
              and d6["sha_manifesto_no_disco"] == d6["sha_manifest_install_staging"] == d6["sha_manifesto_no_plano"]
              and not fora and not nao_existe and not divergentes_h)
R["checks"]["D6_arquivo"] = d6

R["hashes_evidencia"] = {n: sha_file(W / n) for n in ("deployment.json", "restart.json", "maintenance.json", "INSTALLED_VERIFICATION.json", "deploy_stdout.txt")}
(OUT / "d1_d4_result.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")

# resumo curto
for k, v in R["checks"].items():
    slim = {kk: vv for kk, vv in v.items() if kk not in ("linhas", "tools_recalculados", "tools_gravados_review_final")}
    print(k, "PASS" if v["PASS"] else "FAIL", json.dumps(slim, ensure_ascii=False)[:1500])
print("hashes", json.dumps(R["hashes_evidencia"]))
