# -*- coding: utf-8 -*-
"""Roda as tres suites da frente HEARTBEAT em processos novos sob a guarda da auditoria (copia byte a byte).

  1. tests\\test_heartbeat_v2.py          — suite nova (req_lib falso em processo)
  2. tests\\test_heartbeat_stub_server.py — servidor de modelo FALSO (adaptador de transporte do requests), 60 batidas
  3. tests\\app\\test_app_memory.py        — suite APP existente de 31 casos (10/10) com 1 caso reescrito

Antes: copia a guarda de C:\\IALD\\PROGRAMA_IALD\\exame_12out\\E_ACOM\\guard\\sitecustomize.py (sha256 conferido) e
copia os dois arquivos modificados de copia\\ para tests\\app\\ (sha256 conferido). Grava tests\\RESULTADOS.json.
Ambiente: PYTHONPATH=tests\\guard, ACOM_AUDIT_ROOT=<pasta da frente>, PYTHONDONTWRITEBYTECODE=1, sem rede.
"""
import hashlib, json, os, re, subprocess, sys, time
from datetime import datetime

FRONT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = os.path.join(FRONT, "tests")
GUARD_SRC = r"C:\IALD\PROGRAMA_IALD\exame_12out\E_ACOM\guard\sitecustomize.py"
GUARD_DST = os.path.join(TESTS, "guard", "sitecustomize.py")
PY = sys.executable


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def copy_verified(src, dst):
    raw = open(src, "rb").read()
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    tmp = dst + ".tmp_copy"
    with open(tmp, "wb") as out:
        out.write(raw); out.flush(); os.fsync(out.fileno())
    if open(tmp, "rb").read() != raw:
        raise OSError("copy did not verify: " + dst)
    os.replace(tmp, dst)
    return hashlib.sha256(raw).hexdigest()


def run_suite(label, path, cwd):
    env = dict(os.environ)
    # Temporarios DENTRO da raiz vigiada, com prefixo \\?\ (LongPathsEnabled=0 nesta maquina [REAL, diagnostico]):
    # os nomes do outbox do app (~190 caracteres) estouram MAX_PATH a partir desta pasta; a guarda ja aceita o prefixo.
    long_tmp = "\\\\?\\" + os.path.join(TESTS, "tmp")
    env.update({"PYTHONPATH": os.path.join(TESTS, "guard"), "ACOM_AUDIT_ROOT": FRONT, "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1", "NO_PROXY": "*", "HTTP_PROXY": "", "HTTPS_PROXY": "",
                "TMP": long_tmp, "TEMP": long_tmp, "TMPDIR": long_tmp})
    t0 = time.time()
    proc = subprocess.run([PY, "-B", "-X", "utf8", "-m", "unittest", "-v", os.path.basename(path)[:-3]],
                          cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800)
    out = proc.stdout + proc.stderr
    cases = {}
    lines = out.splitlines()
    verdict = re.compile(r"^(ok|FAIL|ERROR|skipped.*)$")
    for i, line in enumerate(lines):
        m = re.match(r"^(test_\w+) \(([\w.]+)\) \.\.\. (.*)$", line)
        if not m:
            continue
        rest = m.group(3).strip()
        # um print do codigo testado pode cair entre o nome e o veredito (ex.: test_operator_json_* imprime "[Memoria] ERRO lendo")
        j = i
        while not verdict.match(rest) and j + 1 < len(lines) and j - i < 5:
            j += 1
            rest = lines[j].strip()
        cases[m.group(1)] = "PASSA" if rest == "ok" else "FALHA"
    summary = re.search(r"^(OK|FAILED.*)$", out, re.M)
    ran = re.search(r"^Ran (\d+) tests? in ([\d.]+)s", out, re.M)
    return {"label": label, "file": path, "returncode": proc.returncode, "seconds": round(time.time() - t0, 1),
            "ran": int(ran.group(1)) if ran else None, "summary": summary.group(1) if summary else None,
            "cases": cases, "output": out, "started_at": t0}


def main():
    receipt = {"at": datetime.now().isoformat(timespec="seconds"), "python": sys.version, "statute": "REAL (medido neste processo)",
               "guard": {"source": GUARD_SRC, "sha256_source": sha256(GUARD_SRC)}, "copies": [], "suites": []}
    receipt["guard"]["sha256_copy"] = copy_verified(GUARD_SRC, GUARD_DST)
    assert receipt["guard"]["sha256_copy"] == receipt["guard"]["sha256_source"]
    for name in ("iald_web_server.py", "iald_app_memory.py"):
        src = os.path.join(FRONT, "copia", "projetos_pyhton", "IALD", name)
        dst = os.path.join(TESTS, "app", name)
        s = copy_verified(src, dst)
        receipt["copies"].append({"name": name, "from": src, "to": dst, "sha256": s})
    os.makedirs(os.path.join(TESTS, "tmp"), exist_ok=True)
    os.makedirs(os.path.join(FRONT, "guard_log"), exist_ok=True)
    before_logs = set(os.listdir(os.path.join(FRONT, "guard_log")))
    receipt["suites"].append(run_suite("NOVA — req_lib falso em processo", os.path.join(TESTS, "test_heartbeat_v2.py"), TESTS))
    receipt["suites"].append(run_suite("STUB — servidor de modelo falso, 60 batidas", os.path.join(TESTS, "test_heartbeat_stub_server.py"), TESTS))
    receipt["suites"].append(run_suite("APP 31 (10/10) com 1 caso reescrito", os.path.join(TESTS, "app", "test_app_memory.py"), os.path.join(TESTS, "app")))
    receipt["all_pass"] = all(s["returncode"] == 0 and s["summary"] == "OK" for s in receipt["suites"])
    receipt["total_cases"] = sum(len(s["cases"]) for s in receipt["suites"])
    receipt["failed_cases"] = [c for s in receipt["suites"] for c, v in s["cases"].items() if v != "PASSA"]
    # guarda: resumo dos eventos registrados NESTA rodada = os arquivos guard_<pid>.jsonl que nasceram durante a rodada
    # (logs de rodadas e sondagens anteriores ficam na pasta, mas nao entram na contagem)
    kinds, logs = {}, []
    for name in sorted(set(os.listdir(os.path.join(FRONT, "guard_log"))) - before_logs):
        p = os.path.join(FRONT, "guard_log", name)
        lines = open(p, encoding="utf-8").read().splitlines()
        logs.append(name)
        for line in lines:
            try:
                k = json.loads(line).get("kind")
            except ValueError:
                continue
            kinds[k] = kinds.get(k, 0) + 1
    receipt["guard_events"] = kinds
    receipt["guard_logs_this_run"] = logs
    for s in receipt["suites"]:
        s.pop("started_at", None)
    with open(os.path.join(TESTS, "RESULTADOS.json"), "w", encoding="utf-8") as f:
        json.dump(receipt, f, ensure_ascii=False, indent=1)
    for s in receipt["suites"]:
        print(f"== {s['label']}: ran={s['ran']} summary={s['summary']} rc={s['returncode']} {s['seconds']}s")
        for c, v in s["cases"].items():
            print(f"   {v:6s} {c}")
        if s["summary"] != "OK":
            print(s["output"][-6000:])
    print("guard events:", kinds)
    print("ALL_PASS" if receipt["all_pass"] else "SOME_FAILED")


if __name__ == "__main__":
    main()
