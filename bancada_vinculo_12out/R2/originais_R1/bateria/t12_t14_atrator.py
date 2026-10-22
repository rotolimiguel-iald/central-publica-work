# -*- coding: utf-8 -*-
# T12_ATRATOR_OTICO + T13_ATRATOR_A5_A6 + T14_CONTROLE_AFIM -- replay dos runners CONGELADOS do F1.ATRATOR a partir de copias byte a byte,
# comparando com os resultados arquivados (so carimbos de tempo/ambiente/caminho ignorados). FASE PRE-SELO: os pre-registros pinam o
# um.py vigente; depois do selo eles recusam por desenho. Porte parametrizado de H_BANCADA\scripts\replicar_atrator.py (+ T14).
# uso: t12_t14_atrator.py <dir F1.ATRATOR do tunel> <dir destino (novo)> <saida.json>
import datetime, hashlib, json, subprocess, sys
from pathlib import Path
SRC, DST, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def cp(rel):
    s, d = SRC / rel, DST / rel
    d.parent.mkdir(parents=True, exist_ok=True)
    raw = s.read_bytes()
    with open(d, "xb") as f:
        f.write(raw)
    assert sha(d) == sha(s)
    return {"rel": rel, "sha256": sha(d), "bytes": len(raw)}


VOL = {"started_utc", "finished_utc", "elapsed_seconds", "environment", "began_utc", "ended_utc", "seconds", "created_utc", "python", "platform",
       "numpy", "path", "source_snapshot_before", "source_snapshot_after"}


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in VOL}
    if isinstance(o, list):
        return [strip(x) for x in o]
    return o


def diff(a, b, path="", acc=None):
    acc = acc if acc is not None else {"max_abs": 0.0, "mismatch": []}
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b:
                acc["mismatch"].append(path + "." + k + " (missing)")
                continue
            diff(a[k], b[k], path + "." + k, acc)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            acc["mismatch"].append(path + " (len)")
            return acc
        for i, (x, y) in enumerate(zip(a, b)):
            diff(x, y, path + "[%d]" % i, acc)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        d = abs(float(a) - float(b))
        acc["max_abs"] = max(acc["max_abs"], d)
        if d != 0.0:
            acc["mismatch"].append(path + " (num %.3e)" % d)
    elif a != b:
        acc["mismatch"].append(path + " (value)")
    return acc


copies = [cp(r) for r in ("PREREGISTRO_R1.json", "numerical/run_optical_r3.py", "numerical/RUN_MANIFEST_R3.json", "ADENDO1/PREREGISTRO_ADENDO1_R1.json",
                          "ADENDO1/numerical/run_adendo1_r1.py", "ADENDO1/numerical/RUN_MANIFEST_R1.json", "review/verify_affine_control_r1.py")]
res = dict(teste="T12+T13+T14", quando=datetime.datetime.now().isoformat(timespec="seconds"), copies=copies, runs={})
ok_all = True
for name, rel, outrel in (("T12_optical_r3", "numerical/run_optical_r3.py", "numerical/RESULTADOS_NUMERICOS_R3.json"),
                          ("T13_adendo1_r1", "ADENDO1/numerical/run_adendo1_r1.py", "ADENDO1/numerical/RESULTADOS_ADENDO1_R1.json"),
                          ("T14_controle_afim", "review/verify_affine_control_r1.py", "review/ADENDO_CONTROLE_AFIM_R1.json")):
    script = DST / rel
    t0 = datetime.datetime.now(datetime.timezone.utc)
    r = subprocess.run([sys.executable, "-B", "-X", "utf8", str(script)], cwd=str(script.parent), capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=1800)
    t1 = datetime.datetime.now(datetime.timezone.utc)
    log = DST / (rel + ".vinculo.log")
    with open(log, "x", encoding="utf-8") as f:
        f.write("START %s\nEND %s\nEXIT %d\nSTDOUT:\n%s\nSTDERR:\n%s\n" % (t0.isoformat(), t1.isoformat(), r.returncode, r.stdout, r.stderr))
    new, orig = DST / outrel, SRC / outrel
    e = dict(exit=r.returncode, log=str(log), log_sha256=sha(log), seconds=(t1 - t0).total_seconds())
    if r.returncode == 0 and new.exists():
        a, b = json.loads(new.read_bytes()), json.loads(orig.read_bytes())
        d = diff(strip(a), strip(b))
        e.update(result_new_sha256=sha(new), result_archived_sha256=sha(orig), max_abs_diff=d["max_abs"], n_mismatch=len(d["mismatch"]),
                 mismatch_sample=d["mismatch"][:25], all_expected_outcomes_met_new=a.get("all_expected_outcomes_met"),
                 beta_runtime_new=a.get("beta_runtime") or a.get("beta"), A6=(a.get("A6") or {}).get("status") if isinstance(a.get("A6"), dict) else None)
        e["passa"] = (len(d["mismatch"]) == 0)
    else:
        e["passa"] = False
    ok_all = ok_all and e["passa"]
    res["runs"][name] = e
res["veredito"] = "PASSA" if ok_all else "FALHA"
res["nota"] = "A6 FALHA e o falsificador da minimalidade disparando como pre-registrado (identico ao arquivo), nao defeito"
with out.open("x", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: (v["passa"], v.get("n_mismatch"), v["seconds"]) for k, v in res["runs"].items()}), res["veredito"])
sys.exit(0 if ok_all else 1)
