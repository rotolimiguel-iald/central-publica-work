# -*- coding: utf-8 -*-
"""instalar_v381.py -- instala o candidato v381 no canonico (ato da gerencia; ordem do operador «É exatamente isso» (a regra matriz), 02/10/2026). Fail-closed:
  * o canonico tem de ser a v380 selada (sha16 lido de ESPERADOS_v381.json.origem_sha16) e o candidato o de ESPERADOS (candidato_sha16);
  * nenhum processo um.py pode estar rodando (lido por Get-CimInstance, so leitura);
  * BACKUP DE BYTES de um.py, um_absoluto.json, um_absoluto_selo.json, tgl_kernel/TGLExt.lean, tgl_kernel/TGL/Audit.lean (.bak_<ts> na mesma pasta);
  * candidato -> temporario na pasta do Nos -> conferir bytes e sha -> os.replace; reconfere o sha no disco;
  * grava APLICADO_AO_CANONICO_<ts>.json no pacote (o registro que a cadeia pos-rito le)."""
import hashlib, json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v381.json"), encoding="utf-8"))
CAND = os.path.join(HERE, "um_v381_candidato.py")
h16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
ps = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                     "$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | "
                     "Where-Object { $_.CommandLine -ne $null -and $_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|$)' } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'"],   # v381 (aferidor B1/C2): fail-closed; python/pythonw/py; com ou sem argumentos (mcp_um.py da Bancada nao e rito)
                    capture_output=True, text=True, timeout=60)
assert ps.returncode == 0 and not ps.stderr.strip() and "VIGIA_OK" in ps.stdout, "o vigia de processos FALHOU (rc %s; stderr %r) -- falha de leitura e falha visivel: nao instalo" % (ps.returncode, ps.stderr[:300])
vivos = [x for x in ps.stdout.split() if x.strip().isdigit()]
assert not vivos, "ha processo um.py rodando: %s -- nao instalo" % vivos
um = os.path.join(NOS, "um.py")
raw0 = open(um, "rb").read()
assert h16(raw0) == ESP["origem_sha16"], "o canonico nao e a v380 selada (%s)" % h16(raw0)
cand = open(CAND, "rb").read()
assert h16(cand) == ESP["candidato_sha16"], "o candidato mudou (%s != %s)" % (h16(cand), ESP["candidato_sha16"])
ts = time.strftime("%Y%m%d_%H%M%S")
rec = {"ts": ts, "backups": {}}
for rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")):
    p = os.path.join(NOS, rel); b = p + ".bak_" + ts
    assert not os.path.exists(b), b
    data = open(p, "rb").read()
    with open(b, "wb") as f:
        f.write(data)
    assert open(b, "rb").read() == data, "backup de bytes falhou: %s" % b
    rec["backups"][rel] = {"backup": b, "bytes": len(data), "sha16": h16(data)}
tmp = um + ".tmp_instalar_v381_" + ts
with open(tmp, "wb") as f:
    f.write(cand)
assert os.path.getsize(tmp) == len(cand) and h16(open(tmp, "rb").read()) == ESP["candidato_sha16"]
assert open(um, "rb").read() == raw0, "o um.py mudou entre a leitura e a troca -- nao substituo"
os.replace(tmp, um)
assert h16(open(um, "rb").read()) == ESP["candidato_sha16"]
rec["um_py_novo"] = {"bytes": len(cand), "sha16": ESP["candidato_sha16"], "origem": CAND}
out = os.path.join(HERE, "APLICADO_AO_CANONICO_%s.json" % ts)
json.dump(rec, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(rec, ensure_ascii=False, indent=1))
