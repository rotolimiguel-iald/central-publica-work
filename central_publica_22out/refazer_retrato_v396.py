# -*- coding: utf-8 -*-
"""Refaz o RETRATO público do cockpit para o site com o estado da v396 (22/10/2026, custódia v396: «Atualize tudo com a nova versão do
um.py»), pela MESMA sequência que montou o retrato da abertura (de 22/10): exportar (só GET na Central local) -> aparar 1 e 2 (o critério
do operador) -> vínculo patentário -> reexportar os mascarados (máscara única e filtro das notas) numa pasta NOVA; troca de pastas (a
anterior fica ao lado, com data); remáscara ampliada; conferência de identificadores de terceiros (a lista privada; só contagens).
Uso: refazer_retrato_v396.py"""
import os, re, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))
PY, PYB = r"C:\Python314\python.exe", r"C:\IALD\Central de Patentes\backend\.venv\Scripts\python.exe"
BASE = Path(r"C:\IALD\Site\tgl\v3.0_bancada\central_publica")
S, S6 = BASE / "snapshot", BASE / "snapshot_v396"
TS = time.strftime("%Y%m%d_%H%M%S")
assert S.is_dir() and not S6.exists(), "estado inesperado das pastas do retrato — PARAR"


def rodar(py, args, cwd=None):
    t0 = time.time()
    r = subprocess.run([py, "-X", "utf8"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd,
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    linhas = [l for l in (r.stdout or "").splitlines() if l.strip()]
    print("  [%s] rc=%d %.0f s | %s" % (Path(args[0]).name, r.returncode, time.time() - t0, (linhas[-1] if linhas else "")[:300]), flush=True)
    if r.returncode != 0:
        print((r.stderr or "")[-1500:])
        raise SystemExit("FALHOU: %s" % args[0])


rodar(PY, [str(W / "exportar_cockpit_publico.py"), str(S6)])
rodar(PY, [str(W / "aparar_retrato_publico.py"), str(S6)])
rodar(PY, [str(W / "aparar_retrato_publico2.py"), str(S6)])
rodar(PYB, [str(W / "vinculo_patentario.py"), str(S6)], cwd=str(W))
rodar(PYB, [str(W / "reexportar_mascarados.py"), str(S6)], cwd=str(W))
os.rename(S, BASE / ("snapshot_v395_" + TS))
os.rename(S6, S)
print("  troca: snapshot -> snapshot_v395_%s; snapshot_v396 -> snapshot" % TS)
rodar(PY, [str(W / "remascarar_retrato.py")])
from mascara_pii import TERCEIROS  # noqa: E402
n = 0
for p in S.rglob("*"):
    if p.is_file() and p.suffix.lower() in (".json", ".txt", ".md", ".html", ".py", ".yaml", ".yml", ".csv", ".tex", ".lean", ".log"):
        try:
            if TERCEIROS is not None and TERCEIROS.search(p.read_text(encoding="utf-8", errors="replace")):
                n += 1
        except OSError:
            pass
print("arquivos do retrato com identificador de terceiro:", n)
assert n == 0, "identificador de terceiro no retrato — PARAR"
print("RETRATO v396 PRONTO")
