# -*- coding: utf-8 -*-
"""instalar_v388.py -- instala o candidato v388 no canonico (ato da gerencia, 06/10/2026; ordem do operador via c1). Molde: instalar_v387.py. Fail-closed:
  * o canonico tem de ser a v387 selada (ESPERADOS_v388.origem_sha16) e o candidato o de ESPERADOS e do registro;
  * os arquivos da Fase 9 aberta (resultado, runner, V1) em disco tem de ser os pinados (v388_pins_fase9.json, gerado dos pinos);
  * o cache do pilar tem de guardar o resultado reaproveitado (o mesmo que a v388 reaproveita pela chave);
  * nenhum processo um.py ou trabalhador do pilar rodando; a pedra nova AINDA nao esta no kernel do Nos;
  * BACKUP DE BYTES de um.py, um_absoluto.json, _selo.json, _forma_canonica.md, _manifest.md, _pilar_quantico.json, tgl_kernel/TGLExt.lean e tgl_kernel/TGL/Audit.lean;
  * COPIA DE BYTES do resultado do pilar no cache para o pacote (pilar_anterior_v387_<ts>/);
  * candidato -> temporario -> conferir -> os.replace; grava APLICADO_AO_CANONICO_<ts>.json."""
import hashlib, json, os, subprocess, sys, time
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v388.json"), encoding="utf-8")); CM = json.load(open(os.path.join(HERE, "CANDIDATO_v388.json"), encoding="utf-8"))
CAND = os.path.join(HERE, "um_v388_candidato.py")
h16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
ps = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                     "$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | "
                     "Where-Object { $_.CommandLine -ne $null -and ($_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|$)' -or $_.CommandLine -match 'pilar_quantico_worker\\.py') } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'"],
                    capture_output=True, text=True, timeout=60)
assert ps.returncode == 0 and "VIGIA_OK" in ps.stdout, "o vigia de processos FALHOU -- nao instalo"
assert not [x for x in ps.stdout.split() if x.strip().isdigit()], "ha processo um.py ou trabalhador do pilar rodando -- nao instalo"
um = os.path.join(NOS, "um.py"); raw0 = open(um, "rb").read()
assert h16(raw0) == ESP["origem_sha16"] == "64c899f86d8d32e1", "o canonico nao e a v387 selada (%s)" % h16(raw0)
cand = open(CAND, "rb").read(); assert h16(cand) == ESP["candidato_sha16"] == CM["sha16"] and len(cand) == ESP["candidato_bytes"]
F9 = json.load(open(os.path.join(HERE, "v388_pins_fase9.json"), encoding="utf-8"))
for k, f in F9["files"].items():
    assert os.path.isfile(f["path"]) and hashlib.sha256(open(f["path"], "rb").read()).hexdigest() == f["sha256"], "o arquivo da Fase 9 (%s) nao e' o pinado" % k
_cdir = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "cache", "checkpoints", "quantum_pillar", ESP["pilar"]["key"])
assert hashlib.sha256(open(os.path.join(_cdir, "result.json"), "rb").read()).hexdigest() == ESP["pilar"]["result_sha256"], "o cache do pilar nao guarda o resultado reaproveitado"
assert not os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "TheCouplingRunsBoundedBelow.lean")), "a pedra nova JA existe no kernel do Nos -- nao instalo sem a gerencia olhar"
ts = time.strftime("%Y%m%d_%H%M%S"); rec = {"ts": ts, "backups": {}}
for rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "um_absoluto_pilar_quantico.json",
            os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")):
    p = os.path.join(NOS, rel); b = p + ".bak_" + ts; assert not os.path.exists(b), b
    data = open(p, "rb").read(); open(b, "wb").write(data); assert open(b, "rb").read() == data, "backup falhou: %s" % b
    rec["backups"][rel] = {"backup": b, "bytes": len(data), "sha16": h16(data)}
_dst = os.path.join(HERE, "pilar_anterior_v387_" + ts); os.makedirs(_dst); rec["pilar_anterior_v387"] = {"de": _cdir, "para": _dst, "arquivos": {}}
for f_ in sorted(os.listdir(_cdir)):
    sp = os.path.join(_cdir, f_)
    if os.path.isfile(sp):
        data = open(sp, "rb").read(); open(os.path.join(_dst, f_), "wb").write(data); assert open(os.path.join(_dst, f_), "rb").read() == data
        rec["pilar_anterior_v387"]["arquivos"][f_] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
assert rec["pilar_anterior_v387"]["arquivos"]["result.json"]["sha256"] == ESP["pilar"]["result_sha256"]
tmp = um + ".tmp_instalar_v388_" + ts; open(tmp, "wb").write(cand)
assert os.path.getsize(tmp) == len(cand) and h16(open(tmp, "rb").read()) == ESP["candidato_sha16"]
assert open(um, "rb").read() == raw0, "o um.py mudou entre a leitura e a troca -- nao substituo"
os.replace(tmp, um); assert h16(open(um, "rb").read()) == ESP["candidato_sha16"]
rec["um_py_novo"] = {"bytes": len(cand), "sha16": ESP["candidato_sha16"], "origem": CAND}
out = os.path.join(HERE, "APLICADO_AO_CANONICO_%s.json" % ts); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1)); os.replace(out + ".tmp", out)
print(json.dumps({"ts": ts, "um_py_novo": rec["um_py_novo"], "n_backups": len(rec["backups"])}, ensure_ascii=False))
