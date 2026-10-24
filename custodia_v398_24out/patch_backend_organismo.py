# -*- coding: utf-8 -*-
"""A rota /api/organismo no backend privado da Central (FastAPI): devolve o quadro medido por tools/estado_do_organismo.py
(organismo/ESTADO_DO_ORGANISMO.json) com a idade da medição; 404 visível quando ainda não há quadro. Só leitura; sem credencial;
o painel do cockpit (frontend/src/pages/Organismo.tsx, Kimi 23/10) lê esta rota. POST /api/organismo/medir (admin) roda o medidor
--sem-rede (rápido) em processo novo e devolve o quadro novo. Troca contada; backup de bytes; py_compile."""
import os, py_compile, time
from pathlib import Path

P = Path("C:/IALD/Central de Patentes/backend/app/main.py")
raw = P.read_bytes(); s = raw.decode("utf-8")
if '"/api/organismo"' in s:
    raise SystemExit("ja aplicado")
A = '@app.get("/api/iald/orquestracao")\n'
B = '''@app.get("/api/organismo")
def organismo_quadro():
    """O QUADRO DO ORGANISMO (24/10/2026): a medida de cada superfície da IALD contra o selo corrente do um.py, feita por
    tools/estado_do_organismo.py (organismo/ESTADO_DO_ORGANISMO.json, fora do git). Só leitura; devolve o documento inteiro mais a idade
    da medição em minutos; 404 visível quando ainda não há quadro (o painel mostra a falha, não inventa)."""
    p = C.CENTRAL / "organismo" / "ESTADO_DO_ORGANISMO.json"
    if not p.is_file():
        raise HTTPException(404, "quadro ainda não medido: rode tools/estado_do_organismo.py")
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise HTTPException(500, "quadro ilegível: %r" % (e,))
    doc["idade_min"] = round((time.time() - p.stat().st_mtime) / 60, 1)
    doc["arquivo"] = str(p)
    return doc


@app.post("/api/organismo/medir")
def organismo_medir(request: Request, body: dict = Body(default={})):
    """AÇÃO (admin): mede o organismo de novo em processo novo (tools/estado_do_organismo.py; --sem-rede por padrão, ~1 min;
    com {"rede": true} mede também o ar, ~3 min) e devolve o quadro novo. Nunca mata processo; nunca chama provedor."""
    _require_admin(request)
    import subprocess as _sp
    args = ["C:/Python314/python.exe", "-X", "utf8", str(C.CENTRAL / "tools" / "estado_do_organismo.py")]
    if not bool(body.get("rede")):
        args.append("--sem-rede")
    try:
        r = _sp.run(args, capture_output=True, timeout=900, cwd=str(C.CENTRAL))
    except _sp.TimeoutExpired:
        raise HTTPException(504, "a medição não terminou em 15 min")
    doc = organismo_quadro()
    doc["medicao"] = {"rc": r.returncode, "ultima_linha": (r.stdout or b"").decode("utf-8", "replace").strip().splitlines()[-1:] }
    return doc


''' + A
assert s.count(A) == 1, s.count(A)
assert "import time" in s or "\nimport time\n" in s or True
s = s.replace(A, B)
if "\nimport time\n" not in s and "import time\n" not in s.split("from fastapi")[0]:
    s = s.replace("import re\n", "import re\nimport time\n", 1)
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, P)
print("backend: /api/organismo e /api/organismo/medir instalados | %d -> %d bytes" % (len(raw), P.stat().st_size))
