"""Reproduces the whole audit evidence from scratch. Usage: C:\\Python314\\python.exe -X utf8 run_all.py
Everything that executes code runs in the copy C:\\t\\orq_copia_kimi (no provider CLI on PATH, dead proxy, synthetic sealed memory,
sandboxed ACOM state). Production files are only READ (ledger, board, Nos Vivo backups, Bancada ledger, Kimi notebook)."""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "saidas"
OUT.mkdir(exist_ok=True)
PY = r"C:\Python314\python.exe"
COPY = Path(r"C:\t\orq_copia_kimi")

base_env = dict(os.environ)
base_env["PYTHONDONTWRITEBYTECODE"] = "1"
base_env["PYTHONUTF8"] = "1"


def sandbox_env():
    env = dict(base_env)
    env["PATH"] = r"C:\Python314;C:\Windows\System32;C:\Windows"
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        env[k] = "http://127.0.0.1:9"
    env["NO_PROXY"] = ""
    for k in list(env):
        if re.search(r"(KEY|TOKEN|SECRET|PASSWORD|ANTHROPIC|OPENAI|MIMO|KIMI|DEEPSEEK)", k, re.I):
            env.pop(k, None)
    return env


def run(args, name, cwd=None, env=None, timeout=900):
    p = subprocess.run([PY, "-B", "-X", "utf8", *args], cwd=cwd, env=env or base_env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    (OUT / name).write_text(p.stdout + ("\n--STDERR--\n" + p.stderr if p.stderr.strip() else ""), encoding="utf-8")
    print("%-34s rc=%s" % (name, p.returncode), flush=True)
    return p


def install(variant):
    shutil.copy2(COPY / "_variants" / variant, COPY / "iald_orchestrator" / "canonical_memory.py")
    for pyc in COPY.rglob("__pycache__"):
        shutil.rmtree(pyc, ignore_errors=True)


run([str(HERE / "make_copy.py")], "00_make_copy.txt")
env = sandbox_env()
run([str(HERE / "run_tests.py"), str(OUT / "testes")], "01_testes_resumo.txt", cwd=str(COPY), env=env)
run([str(HERE / "run_fold_cases.py")], "02_fold_tabela.txt", cwd=str(COPY), env=env)
for tag, variant in (("kimi", "cm_kimi.py"), ("producao_atual", "cm_current.py")):
    install(variant)
    run([str(HERE / "attach_check.py")], "03_attach_%s.txt" % tag, cwd=str(COPY), env=env)
run([str(HERE / "run_kimi_test.py")], "04_teste_do_kimi_contra_as_tres_variantes.txt", cwd=str(COPY), env=env)
install("cm_current.py")
run([str(HERE / "rank_counterexample.py")], "05_ranker_contraexemplo.txt", cwd=str(COPY), env=env)
run([str(HERE / "check_descida.py")], "06_descida_prefixo_do_livro.txt")
run([str(HERE / "check_deriva2.py")], "07_deriva_de_gabarito_refutada.txt")
run([str(HERE / "check_pacote.py")], "08_pacote_do_benchmark.txt")
run([str(HERE / "check_manutencao.py")], "09_manutencao_e_fontes.txt")
p = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "verificar"], capture_output=True, text=True, encoding="utf-8")
(OUT / "10_livro_verificar.txt").write_text(p.stdout, encoding="utf-8")
print("10_livro_verificar.txt", p.stdout.strip()[:120].replace("\n", " "))
