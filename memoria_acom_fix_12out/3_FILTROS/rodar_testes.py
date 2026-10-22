"""Roda todas as suítes (origem + novas) em cópias, sob a guarda sitecustomize da auditoria
(PYTHONPATH=guard_exec, ACOM_AUDIT_ROOT=esta pasta, TEMP/TMP dentro dela), e escreve TESTES.md e
RESULTADOS_TESTES.json com cada teste e o resultado PASSA/FALHA. Nenhuma chamada a provedor.
"""
from __future__ import annotations
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUITE = ROOT / "suite"
PY = r"C:\Python314\python.exe"
SUITES = [
    ("SESSOES (origem)", SUITE / "sessions", ["test_sessions", "test_hooks"]),
    ("SESSOES (novos)", SUITE / "sessions", ["test_filters", "test_guard"]),
    ("APP (origem)", SUITE / "app", ["test_app_memory"]),
    ("APP (novos)", SUITE / "app", ["test_app_filters"]),
    ("FILA (novos)", SUITE / "queue", ["test_filters_queue"]),
    ("BLOCOS (novos)", SUITE / "blocos", ["test_blocks"]),
]
LINE = re.compile(r"^(?P<name>test_\w+) \((?P<cls>[\w.]+)\) \.\.\.(?: (?P<res>ok|FAIL|ERROR|skipped.*|expected failure|unexpected success))?\s*$")
OUTCOME = re.compile(r"^(?P<res>ERROR|FAIL): (?P<name>test_\w+) \((?P<cls>[\w.]+)\)")


def run(label, cwd, modules):
    env = dict(os.environ)
    tmp = ROOT / "tmp" / "run"; tmp.mkdir(parents=True, exist_ok=True)
    # Extended-length TEMP (\\?\): the app outbox paths exceed MAX_PATH (260) under this folder and
    # LongPathsEnabled=0 on this machine. The auditor's guard accepts the \\?\ form of its root.
    ext_tmp = "\\\\?\\" + str(tmp)
    env.update(PYTHONPATH=str(ROOT / "guard_exec"), ACOM_AUDIT_ROOT=str(ROOT), TEMP=ext_tmp, TMP=ext_tmp, TMPDIR=ext_tmp,
               PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    (ROOT / "guard_log").mkdir(exist_ok=True)
    start = time.time()
    proc = subprocess.run([PY, "-X", "utf8", "-m", "unittest", "-v"] + modules, cwd=str(cwd), env=env, capture_output=True, timeout=900)
    err = proc.stderr.decode("utf-8", "replace")
    tests, index = [], {}
    for raw in err.splitlines():
        m = LINE.match(raw.strip())
        if m:
            res = m.group("res")
            item = {"suite": label, "module": m.group("cls").split(".")[0], "class": m.group("cls"), "test": m.group("name"),
                    "result": ("PASSA" if res == "ok" else "PULADO" if res and res.startswith("skipped") else "FALHA" if res else "PENDENTE"),
                    "raw": res or "(subtests)"}
            tests.append(item); index[(m.group("cls"), m.group("name"))] = item
            continue
        o = OUTCOME.match(raw.strip())
        if o and (o.group("cls"), o.group("name")) in index:   # a subTest failure marks its parent test
            item = index[(o.group("cls"), o.group("name"))]
            item["result"] = "FALHA"; item["raw"] = o.group("res") + " (subtest)"
    for item in tests:
        if item["result"] == "PENDENTE":   # subtests all passed: unittest prints no trailing 'ok' in -v mode
            item["result"], item["raw"] = "PASSA", "ok (subtests)"
    ran = re.search(r"Ran (\d+) tests? in ([\d.]+)s", err)
    return {"suite": label, "cwd": str(cwd), "modules": modules, "returncode": proc.returncode, "ran": int(ran.group(1)) if ran else None,
            "seconds": round(time.time() - start, 2), "ok": proc.returncode == 0 and err.rstrip().endswith("OK"),
            "tests": tests, "stderr_tail": err[-6000:], "stdout_tail": proc.stdout.decode("utf-8", "replace")[-2000:]}


def guard_summary():
    folder = ROOT / "guard_log"
    blocks, processes, reads_outside = [], 0, set()
    for path in sorted(folder.glob("guard_*.jsonl")):
        processes += 1
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                item = json.loads(line)
            except ValueError:
                continue
            if item.get("kind", "").startswith("BLOCK"):
                blocks.append({k: item.get(k) for k in ("kind", "event", "path", "src", "dst", "args")})
            elif item.get("kind") == "READ_OUTSIDE":
                reads_outside.add(item.get("path"))
    return {"processes": processes, "blocks": blocks, "n_blocks": len(blocks), "reads_outside_n": len(reads_outside),
            "reads_outside_sample": sorted(reads_outside)[:40]}


def main():
    for old in (ROOT / "guard_log").glob("guard_*.jsonl"):
        old.unlink()
    results = [run(*spec) for spec in SUITES]
    summary = guard_summary()
    total = sum(len(r["tests"]) for r in results)
    passed = sum(t["result"] == "PASSA" for r in results for t in r["tests"])
    failed = sum(t["result"] == "FALHA" for r in results for t in r["tests"])
    skipped = sum(t["result"] == "PULADO" for r in results for t in r["tests"])
    all_ok = all(r["ok"] for r in results)
    report = {"at": datetime.now(timezone.utc).isoformat(), "python": PY, "all_ok": all_ok, "total": total, "passed": passed,
              "failed": failed, "skipped": skipped, "suites": results, "guard": summary}
    (ROOT / "RESULTADOS_TESTES.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# TESTES — frente FILTROS (conserto ACOM 12/10)", "",
             "Rodados em %s com `%s` sobre CÓPIAS (`suite\\`), sob a guarda `sitecustomize.py` da auditoria "
             "(sem rede, sem escrita fora desta pasta, sem sqlite gravável fora dela, sem abrir confidenciais). "
             "Nenhuma chamada a provedor. Resultado medido aqui [REAL]: **%d testes, %d PASSA, %d FALHA, %d pulado(s)** — todas as suítes %s."
             % (report["at"], PY, total, passed, failed, skipped, "OK" if all_ok else "COM FALHA"), "",
             "| suíte | módulo | teste | resultado |", "|---|---|---|---|"]
    for r in results:
        for t in r["tests"]:
            lines.append("| %s | `%s` | `%s` | %s |" % (t["suite"], t["module"], t["test"], t["result"]))
    lines += ["", "## Por suíte", "", "| suíte | módulos | rodados | segundos | returncode | OK |", "|---|---|---|---|---|---|"]
    for r in results:
        lines.append("| %s | %s | %s | %s | %s | %s |" % (r["suite"], ", ".join(r["modules"]), r["ran"], r["seconds"], r["returncode"], "sim" if r["ok"] else "NÃO"))
    lines += ["", "## Guarda de execução (auditoria)", "",
              "processos sob guarda: %d; bloqueios: %d; leituras fora da pasta (só leitura, amostra): %d" % (summary["processes"], summary["n_blocks"], summary["reads_outside_n"]), ""]
    for b in summary["blocks"]:
        lines.append("- BLOQUEIO: `%s`" % json.dumps(b, ensure_ascii=False))
    for r in results:
        if not r["ok"]:
            lines += ["", "## Saída da suíte com falha: %s" % r["suite"], "", "```", r["stderr_tail"], "```"]
    (ROOT / "TESTES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"all_ok": all_ok, "total": total, "passed": passed, "failed": failed, "skipped": skipped,
                      "suites": [(r["suite"], r["ran"], r["ok"]) for r in results], "guard_blocks": summary["n_blocks"]}, ensure_ascii=False))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
