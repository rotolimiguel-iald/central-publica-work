# -*- coding: utf-8 -*-
"""instalar_v386.py -- instala o candidato v386 no canonico (ato da gerencia; decisoes do operador de 05/10/2026 lidas por hash: o Verbo, o ramo B reaberto
por pre-registro, «o resto vc consegue responder tudo agroa»). Molde: instalar_v385.py. Fail-closed:
  * o canonico tem de ser a v385 selada (sha16 lido de ESPERADOS_v386.json.origem_sha16) e o candidato o de ESPERADOS (candidato_sha16) e do registro;
  * o pre-registro V1 do ramo B em disco tem de ser o pinado nos esperados (json, md, hashes, poder, gerador; sha256 e bytes);
  * o cache do pilar tem de guardar o resultado da v385 selada (o que a v386 reaproveita pela chave);
  * nenhum processo um.py ou trabalhador do pilar pode estar rodando (lido por Get-CimInstance, so leitura);
  * BACKUP DE BYTES de um.py, um_absoluto.json, um_absoluto_selo.json, um_absoluto_forma_canonica.md, um_absoluto_manifest.md,
    um_absoluto_pilar_quantico.json, tgl_kernel/TGLExt.lean e tgl_kernel/TGL/Audit.lean (.bak_<ts> na mesma pasta) -- o rito materializa o kernel
    embutido por cima dos dois .lean (e grava a pedra nova) e regrava o resultado do pilar;
  * COPIA DE BYTES do resultado do pilar da v385 (o cache que a v386 reaproveita; se o reuse for recusado, o rito o substitui no fim) para o pacote:
    pilar_anterior_v385_<ts>/;
  * candidato -> temporario na pasta do Nos -> conferir bytes e sha -> os.replace; reconfere o sha no disco;
  * grava APLICADO_AO_CANONICO_<ts>.json no pacote (o registro que a cadeia pos-rito le)."""
import hashlib, json, os, subprocess, sys, time
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v386.json"), encoding="utf-8"))
CAND = os.path.join(HERE, "um_v386_candidato.py")
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
assert h16(raw0) == ESP["origem_sha16"], "o canonico nao e a v385 selada (%s)" % h16(raw0)
cand = open(CAND, "rb").read()
assert h16(cand) == ESP["candidato_sha16"] and len(cand) == ESP["candidato_bytes"], "o candidato mudou (%s != %s)" % (h16(cand), ESP["candidato_sha16"])
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v386.json"), encoding="utf-8"))
assert CM["sha16"] == h16(cand) == ESP["candidato_sha16"], "o registro do candidato nao bate com o arquivo nem com os esperados"
for k, f in ESP["ramo_b_V1"]["files"].items():
    assert os.path.isfile(f["path"]) and hashlib.sha256(open(f["path"], "rb").read()).hexdigest() == f["sha256"] and os.path.getsize(f["path"]) == f["bytes"], "o V1 do ramo B em disco (%s) nao e' o pinado" % k
_cdir = ESP["pilar_v385"]["cache_dir"]
assert os.path.isfile(os.path.join(_cdir, "result.json")) and hashlib.sha256(open(os.path.join(_cdir, "result.json"), "rb").read()).hexdigest() == ESP["pilar_v385"]["result_sha256"], "o cache do pilar nao guarda o resultado da v385 selada"
ts = time.strftime("%Y%m%d_%H%M%S")
rec = {"ts": ts, "backups": {}}
for rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "um_absoluto_pilar_quantico.json",
            os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")):
    p = os.path.join(NOS, rel); b = p + ".bak_" + ts
    assert not os.path.exists(b), b
    data = open(p, "rb").read()
    with open(b, "wb") as f:
        f.write(data)
    assert open(b, "rb").read() == data, "backup de bytes falhou: %s" % b
    rec["backups"][rel] = {"backup": b, "bytes": len(data), "sha16": h16(data)}
assert not os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "TheVerbSelectsTheAction.lean")), "a pedra nova JA existe no kernel do Nos -- nao instalo sem a gerencia olhar"
_dst = os.path.join(HERE, "pilar_anterior_v385_" + ts)
os.makedirs(_dst)
rec["pilar_anterior_v385"] = {"de": _cdir, "para": _dst, "arquivos": {}}
for f_ in sorted(os.listdir(_cdir)):
    sp = os.path.join(_cdir, f_)
    if not os.path.isfile(sp):
        continue
    data = open(sp, "rb").read()
    with open(os.path.join(_dst, f_), "wb") as f:
        f.write(data)
    assert open(os.path.join(_dst, f_), "rb").read() == data, "copia de bytes do pilar anterior falhou: %s" % f_
    rec["pilar_anterior_v385"]["arquivos"][f_] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
assert rec["pilar_anterior_v385"]["arquivos"]["result.json"]["sha256"] == ESP["pilar_v385"]["result_sha256"], "o resultado no cache nao e' o da v385 pinado"
tmp = um + ".tmp_instalar_v386_" + ts
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
