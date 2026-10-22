# -*- coding: utf-8 -*-
"""instalar_v384.py -- instala o candidato v384 no canonico (ato da gerencia; ordens do operador de 02-03/10/2026: o pilar quantico na GPU; «Agora vamos ter
que rodar ela completa uma primeira vez»). Molde: instalar_v383.py. Fail-closed:
  * o canonico tem de ser a v383 selada (sha16 lido de ESPERADOS_v384.json.origem_sha16) e o candidato o de ESPERADOS (candidato_sha16);
  * nenhum processo um.py pode estar rodando (lido por Get-CimInstance, so leitura);
  * BACKUP DE BYTES de um.py, um_absoluto.json, um_absoluto_selo.json, um_absoluto_forma_canonica.md, um_absoluto_manifest.md (.bak_<ts> na mesma pasta);
  * candidato -> temporario na pasta do Nos -> conferir bytes e sha -> os.replace; reconfere o sha no disco;
  * grava APLICADO_AO_CANONICO_<ts>.json no pacote (o registro que a cadeia pos-rito le). O kernel nao muda (nenhuma pedra nova)."""
import hashlib, json, os, subprocess, sys, time
if sys.flags.optimize:   # as guardas sao assert: com -O elas sumiriam sem aviso (9a afericao)
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v384.json"), encoding="utf-8"))
CAND = os.path.join(HERE, "um_v384_candidato.py")
h16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
ps = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                     "$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | "
                     "Where-Object { $_.CommandLine -ne $null -and ($_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|$)' -or $_.CommandLine -match 'pilar_quantico_worker\\.py') } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'"],
                    capture_output=True, text=True, timeout=60)
assert ps.returncode == 0 and not ps.stderr.strip() and "VIGIA_OK" in ps.stdout, "o vigia de processos FALHOU (rc %s; stderr %r) -- nao instalo" % (ps.returncode, ps.stderr[:300])
vivos = [x for x in ps.stdout.split() if x.strip().isdigit()]
assert not vivos, "ha processo um.py ou trabalhador do pilar rodando: %s -- nao instalo" % vivos
um = os.path.join(NOS, "um.py")
raw0 = open(um, "rb").read()
assert h16(raw0) == ESP["origem_sha16"], "o canonico nao e a v383 selada (%s)" % h16(raw0)
cand = open(CAND, "rb").read()
assert h16(cand) == ESP["candidato_sha16"], "o candidato mudou (%s != %s)" % (h16(cand), ESP["candidato_sha16"])
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v384.json"), encoding="utf-8"))
assert CM["sha16"] == h16(cand) == ESP["candidato_sha16"], "o registro do candidato nao bate com o arquivo nem com os esperados"
# a guarda da ratificacao (3a afericao): candidato de ENSAIO ou sem a ratificacao do operador NAO passa daqui
PRP_V1 = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "PREREGISTRO_PILAR_QUANTICO_20261003_V1.json")
assert CM.get("ensaio") is False, "o candidato e' de ENSAIO -- nao sigo"
_RAT = CM.get("ratificacao_do_operador") or {}
assert _RAT.get("verbatim") and _RAT.get("quando"), "o candidato nao traz a ratificacao do operador -- nao sigo"
assert (_RAT.get("transcrito") or {}).get("de_teste") is False, "a ratificacao do candidato veio de transcrito de TESTE (ou nao diz qual) -- nao sigo"   # 8a afericao
_PJ = json.load(open(PRP_V1, encoding="utf-8"))
assert hashlib.sha256(open(PRP_V1, "rb").read()).hexdigest() == (CM.get("prereg_sha256") or {}).get("json"), "o pre-registro do candidato nao e' o V1 do lugar permanente"
assert _PJ["spec_sha256"] == CM["spec_sha256"] and _PJ["spec"]["worker_sha256"] == CM["worker_sha256"] and (_PJ.get("ratificacao_do_operador") or {}).get("verbatim") == _RAT["verbatim"], \
    "o trabalhador, a especificacao ou a ratificacao do candidato nao sao os do pre-registro V1"
ts = time.strftime("%Y%m%d_%H%M%S")
rec = {"ts": ts, "backups": {}}
for rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md"):
    p = os.path.join(NOS, rel); b = p + ".bak_" + ts
    assert not os.path.exists(b), b
    data = open(p, "rb").read()
    with open(b, "wb") as f:
        f.write(data)
    assert open(b, "rb").read() == data, "backup de bytes falhou: %s" % b
    rec["backups"][rel] = {"backup": b, "bytes": len(data), "sha16": h16(data)}
tmp = um + ".tmp_instalar_v384_" + ts
with open(tmp, "wb") as f:
    f.write(cand)
assert os.path.getsize(tmp) == len(cand) and h16(open(tmp, "rb").read()) == ESP["candidato_sha16"]
assert open(um, "rb").read() == raw0, "o um.py mudou entre a leitura e a troca -- nao substituo"
os.replace(tmp, um)
assert h16(open(um, "rb").read()) == ESP["candidato_sha16"]
rec["um_py_novo"] = {"bytes": len(cand), "sha16": ESP["candidato_sha16"], "origem": CAND}
out = os.path.join(HERE, "APLICADO_AO_CANONICO_%s.json" % ts)
with open(out + ".tmp", "w", encoding="utf-8") as fh:
    json.dump(rec, fh, ensure_ascii=False, indent=1)
os.replace(out + ".tmp", out)
print(json.dumps(rec, ensure_ascii=False, indent=1))
