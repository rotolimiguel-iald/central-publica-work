# -*- coding: utf-8 -*-
"""SO SE O RITO v385 PRECISAR SER REPETIDO (afericao de codigo, nota 8): devolve ao cache do pilar o resultado da v384 (a copia de BYTES que o
instalar_v385.py guardou em pilar_anterior_v384_<ts>/), para que a segunda tentativa compare contra a v384 -- e nao contra a primeira tentativa da v385,
que o _qp_save_cache gravou no fim. Fail-closed:
  * nenhum processo um.py nem trabalhador do pilar vivo (Get-CimInstance, so leitura);
  * a copia do pacote tem de ser a pinada nos esperados (sha256 do result.json) e conferir arquivo a arquivo com o APLICADO;
  * se o cache JA e' o da v384, nada a fazer (rc 0);
  * o cache atual NAO e' apagado: vai a <cache>.v385_tentativa_<ts> (renomeado), e a copia entra por temporario -> conferir -> substituir.
Uso: python restaurar_cache_anterior_v385.py  (so com ordem da gerencia, depois de uma tentativa do rito que nao serviu)."""
import glob, hashlib, json, os, shutil, subprocess, sys, time
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
HERE = os.path.dirname(os.path.abspath(__file__))
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v385.json"), encoding="utf-8"))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
ps = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                     "$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | "
                     "Where-Object { $_.CommandLine -ne $null -and ($_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|$)' -or $_.CommandLine -match 'pilar_quantico_worker\\.py') } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'"],
                    capture_output=True, text=True, timeout=60)
assert ps.returncode == 0 and not ps.stderr.strip() and "VIGIA_OK" in ps.stdout, "o vigia de processos falhou (rc %s; stderr %r) -- nao restauro" % (ps.returncode, ps.stderr[:300])
assert not [x for x in ps.stdout.split() if x.strip().isdigit()], "ha um.py ou trabalhador do pilar vivo -- nao restauro"
AP = json.load(open(sorted(glob.glob(os.path.join(HERE, "APLICADO_AO_CANONICO_*.json")))[-1], encoding="utf-8"))
SRC = AP["pilar_anterior_v384"]["para"]; CDIR = AP["pilar_anterior_v384"]["de"]
assert os.path.normcase(CDIR) == os.path.normcase(ESP["pilar_v384"]["cache_dir"]), "o cache do APLICADO nao e' o dos esperados"
for f_, m_ in AP["pilar_anterior_v384"]["arquivos"].items():
    assert sha(os.path.join(SRC, f_)) == m_["sha256"], "a copia do pacote mudou: %s" % f_
assert sha(os.path.join(SRC, "result.json")) == ESP["pilar_v384"]["result_sha256"], "a copia nao e' o resultado pinado da v384"
cur = os.path.join(CDIR, "result.json")
if os.path.exists(cur) and sha(cur) == ESP["pilar_v384"]["result_sha256"]:
    print("o cache JA guarda o resultado da v384 -- nada a fazer"); sys.exit(0)
ts = time.strftime("%Y%m%d_%H%M%S")
tmp = CDIR + ".tmp_restaurar_" + ts
os.makedirs(tmp)
for f_ in AP["pilar_anterior_v384"]["arquivos"]:
    shutil.copyfile(os.path.join(SRC, f_), os.path.join(tmp, f_))
    assert sha(os.path.join(tmp, f_)) == AP["pilar_anterior_v384"]["arquivos"][f_]["sha256"]
old = None
if os.path.isdir(CDIR):
    old = CDIR + ".v385_tentativa_" + ts
    os.replace(CDIR, old)
try:
    os.replace(tmp, CDIR)
except Exception as e1:   # (2a passada, N8) a VOLTA: o cache da tentativa retorna ao lugar; se a volta falhar, isso fica dito
    e2 = None
    if old:
        try:
            os.replace(old, CDIR)
        except Exception as e_r:
            e2 = e_r
    raise SystemExit("a troca falhou: %r; a volta do cache da tentativa: %s; a copia ficou em %s" % (e1, ("FALHOU: %r (ele ficou em %s)" % (e2, old)) if e2 else ("ok" if old else "nao havia"), tmp))
assert sha(os.path.join(CDIR, "result.json")) == ESP["pilar_v384"]["result_sha256"]
rec = {"ts": ts, "cache": CDIR, "restaurado_de": SRC, "cache_da_tentativa_guardado_em": old}
json.dump(rec, open(os.path.join(HERE, "RESTAURADO_CACHE_ANTERIOR_%s.json" % ts), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(rec, ensure_ascii=False, indent=1))
