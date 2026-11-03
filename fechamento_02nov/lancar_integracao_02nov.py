# -*- coding: utf-8 -*-
"""Lança o driver da integração R3 como processo desacoplado (o Start-Process quebrou o caminho com espaço)."""
import subprocess, sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
drv = AQUI / "integrar_fecho_bancada_02nov.py"
out = open(AQUI / "integracao_stdout.log", "ab")
err = open(AQUI / "integracao_stderr.log", "ab")
flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
p = subprocess.Popen([sys.executable, "-X", "utf8", str(drv)], cwd=r"C:\t\k405c\final", stdout=out, stderr=err, stdin=subprocess.DEVNULL, creationflags=flags, close_fds=True)
(AQUI / "integracao_PID.txt").write_text(str(p.pid), encoding="ascii")
print("PID", p.pid)
