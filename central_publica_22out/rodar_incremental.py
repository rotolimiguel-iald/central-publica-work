# -*- coding: utf-8 -*-
"""Roda a atualização INCREMENTAL de um preparo público (22/10/2026, custódia v396): preparar (já vistos) -> construtor incremental numa
pasta NOVA (a esteira original; pula o já visto que não mudou desde 22/10/2026 00:00) -> mescla no preparo. Uso: rodar_incremental.py
<nucleo|work|Chatgpt>"""
import os, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
PY = r"C:\Python314\python.exe"
TIPO = sys.argv[1]
PREP = {"nucleo": "central-publica", "work": "central-publica-work", "Chatgpt": "central-publica-bancada"}[TIPO]
D = Path(r"C:\IALD\Central_publica") / PREP
# (23/10/2026) generalizado: a pasta da rodada leva a hora; o DESDE vem de --desde "AAAA-MM-DD HH:MM:SS" (o padrão é a hora do último
# commit do preparo, lida do git: tudo o que mudou na origem depois da última publicação)
T = Path(r"C:\IALD\Central_publica") / ("_incr_%s_%s" % (time.strftime("%Y%m%d_%H%M%S"), TIPO))
assert not T.exists(), "a pasta da rodada já existe — PARAR (nada se sobrescreve): %s" % T
if "--desde" in sys.argv:
    DESDE = time.mktime(time.strptime(sys.argv[sys.argv.index("--desde") + 1], "%Y-%m-%d %H:%M:%S"))
else:
    DESDE = float(subprocess.run(["git", "-C", str(D), "log", "-1", "--format=%ct"], capture_output=True, text=True).stdout.strip())
print("  DESDE (origem modificada depois de): %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(DESDE)))


def rodar(args, env=None):
    t0 = time.time()
    r = subprocess.run([PY, "-X", "utf8"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    linhas = [l for l in (r.stdout or "").splitlines() if l.strip()]
    print("  [%s] rc=%d %.0f s | %s" % (Path(args[0]).name, r.returncode, time.time() - t0, (linhas[-1] if linhas else "")[:400]))
    if r.returncode != 0:
        print((r.stderr or "")[-2000:])
        raise SystemExit("FALHOU: %s" % args[0])


rodar([str(W / "mesclar_incremento.py"), "preparar", str(D)])
env = dict(os.environ, IALD_PUBLICO_DESDE=str(DESDE), IALD_PUBLICO_JA_VISTOS=str(W / ("ja_vistos_%s.json" % PREP)), PYTHONIOENCODING="utf-8")
if TIPO == "nucleo":
    rodar([str(W / "construir_nucleo_incremental.py"), str(T)], env)
else:
    rodar([str(W / "construir_regiao_incremental.py"), TIPO, str(T)], env)
rodar([str(W / "mesclar_incremento.py"), "mesclar", str(D), TIPO, str(T)])
