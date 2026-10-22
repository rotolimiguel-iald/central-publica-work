# -*- coding: utf-8 -*-
"""instalar_v394.py -- instala o candidato v394 no canonico (ato da gerencia c1, 19/10/2026). Molde: instalar_v393.py. Fail-closed:
  * o canonico tem de ser a v393 selada (ESPERADOS_v394.origem_sha16) e o candidato o de ESPERADOS e do registro;
  * o cache do pilar tem de guardar o resultado reaproveitado (o mesmo que a v394 reaproveita pela chave);
  * nenhum processo um.py ou trabalhador do pilar rodando (a v394 traz 190 modulos novos de kernel: o proprio rito os materializa a partir do corpo embutido);
  * BACKUP DE BYTES de um.py, um_absoluto.json, _selo.json, _forma_canonica.md, _manifest.md, _pilar_quantico.json, tgl_kernel/TGLExt.lean e tgl_kernel/TGL/Audit.lean;
  * COPIA DE BYTES do resultado do pilar no cache para o pacote (pilar_anterior_v393_<ts>/);
  * candidato -> temporario -> conferir -> os.replace; grava APLICADO_AO_CANONICO_<ts>.json."""
import hashlib, json, os, subprocess, sys, time
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v394.json"), encoding="utf-8")); CM = json.load(open(os.path.join(HERE, "CANDIDATO_v394.json"), encoding="utf-8"))
CAND = os.path.join(HERE, "um_v394_candidato_d19.py")
h16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
ps = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                     "$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | "
                     "Where-Object { $_.CommandLine -ne $null -and ($_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|$)' -or $_.CommandLine -match 'pilar_quantico_worker\\.py') } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'"],
                    capture_output=True, text=True, timeout=60)
assert ps.returncode == 0 and "VIGIA_OK" in ps.stdout, "o vigia de processos FALHOU -- nao instalo"
assert not [x for x in ps.stdout.split() if x.strip().isdigit()], "ha processo um.py ou trabalhador do pilar rodando -- nao instalo"
um = os.path.join(NOS, "um.py"); raw0 = open(um, "rb").read()
assert h16(raw0) == ESP["origem_sha16"] == CM["base_v393_sha16"], "o canonico nao e a v393 selada (%s)" % h16(raw0)
cand = open(CAND, "rb").read(); assert h16(cand) == ESP["candidato_sha16"] == CM["sha16"] and len(cand) == ESP["candidato_bytes"]
_cdir = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "cache", "checkpoints", "quantum_pillar", ESP["pilar"]["key"])
assert hashlib.sha256(open(os.path.join(_cdir, "result.json"), "rb").read()).hexdigest() == ESP["pilar"]["result_sha256"], "o cache do pilar nao guarda o resultado reaproveitado"
# v394: (a) as 3 pedras da v393 (a regra) JA estao no kernel do Nos (a base instalada e' a v393 selada); (b) NENHUM dos modulos novos da v394 (os do Codex e a pedra do criterio binario de parada) esta la ainda.
# A lista dos modulos novos: kernel_modulos_novos_v394.json (campo 'novos', gerado por preparar_kernel_v394.py) se vier como LISTA; se vier so' a contagem (defeito conhecido do json.dump), a lista de
# kernel_modulos_novos_v394.lista.json (derivar_instalar_rito_v394.py: sandbox x Nos); por fim ESPERADOS.pedras_sha256 / ESPERADOS.kernel.new. Fail-closed em tudo.
_PEDRAS_V393 = ("RuleTruthContract", "TheRuleAndTheFigureOfTruth", "TheRuleInTheContinuousMotor")
assert all(os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", n_ + ".lean")) for n_ in _PEDRAS_V393), "as pedras da v393 (RuleTruthContract, TheRuleAndTheFigureOfTruth, TheRuleInTheContinuousMotor) nao estao no kernel do Nos -- nao instalo"


def _modulos_novos():
    nj = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v394.json"), encoding="utf-8"))
    n_dito = nj["novos"] if isinstance(nj["novos"], int) else len(nj["novos"])
    if isinstance(nj["novos"], list):
        return list(nj["novos"]), n_dito, "kernel_modulos_novos_v394.json[novos]"
    pl = os.path.join(HERE, "kernel_modulos_novos_v394.lista.json")
    if os.path.exists(pl):
        return list(json.load(open(pl, encoding="utf-8"))["novos"]), n_dito, "kernel_modulos_novos_v394.lista.json[novos]"
    return list(ESP.get("pedras_sha256") or ESP["kernel"]["new"]), n_dito, "ESPERADOS_v394(pedras_sha256|kernel.new)"


NOVOS_V394, _N_DITO, _FONTE_NOVOS = _modulos_novos()
assert len(NOVOS_V394) == _N_DITO and len(set(NOVOS_V394)) == _N_DITO and ESP["kernel"]["modulos_novos"] == _N_DITO and all(x_.startswith("TGLExt/") and x_.endswith(".lean") for x_ in NOVOS_V394), ("a lista dos modulos novos nao e' a do ESPERADOS (.lean de TGLExt/)", len(NOVOS_V394), _N_DITO, _FONTE_NOVOS)
assert set(NOVOS_V394) == set(ESP.get("pedras_sha256") or NOVOS_V394), "a lista dos modulos novos difere de ESPERADOS.pedras_sha256 -- nao instalo"
assert not [rel for rel in NOVOS_V394 if os.path.exists(os.path.join(NOS, "tgl_kernel", *rel.split("/")))], "algum dos modulos novos (v394) ja esta no kernel do Nos -- nao instalo"
ts = time.strftime("%Y%m%d_%H%M%S"); rec = {"ts": ts, "backups": {}}
rec["modulos_novos_v394"] = {"fonte": _FONTE_NOVOS, "n": len(NOVOS_V394), "lista": NOVOS_V394}   # o reverter usa ESTA lista (a que o instalar conferiu)
for rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "um_absoluto_pilar_quantico.json",
            os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")):
    p = os.path.join(NOS, rel); b = p + ".bak_" + ts; assert not os.path.exists(b), b
    data = open(p, "rb").read(); open(b, "wb").write(data); assert open(b, "rb").read() == data, "backup falhou: %s" % b
    rec["backups"][rel] = {"backup": b, "bytes": len(data), "sha16": h16(data)}
_dst = os.path.join(HERE, "pilar_anterior_v393_" + ts); os.makedirs(_dst); rec["pilar_anterior_v393"] = {"de": _cdir, "para": _dst, "arquivos": {}}
for f_ in sorted(os.listdir(_cdir)):
    sp = os.path.join(_cdir, f_)
    if os.path.isfile(sp):
        data = open(sp, "rb").read(); open(os.path.join(_dst, f_), "wb").write(data); assert open(os.path.join(_dst, f_), "rb").read() == data
        rec["pilar_anterior_v393"]["arquivos"][f_] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
assert rec["pilar_anterior_v393"]["arquivos"]["result.json"]["sha256"] == ESP["pilar"]["result_sha256"]
tmp = um + ".tmp_instalar_v394_" + ts; open(tmp, "wb").write(cand)
assert os.path.getsize(tmp) == len(cand) and h16(open(tmp, "rb").read()) == ESP["candidato_sha16"]
assert open(um, "rb").read() == raw0, "o um.py mudou entre a leitura e a troca -- nao substituo"
os.replace(tmp, um); assert h16(open(um, "rb").read()) == ESP["candidato_sha16"]
rec["um_py_novo"] = {"bytes": len(cand), "sha16": ESP["candidato_sha16"], "origem": CAND}
out = os.path.join(HERE, "APLICADO_AO_CANONICO_%s.json" % ts); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1)); os.replace(out + ".tmp", out)
print(json.dumps({"ts": ts, "um_py_novo": rec["um_py_novo"], "n_backups": len(rec["backups"])}, ensure_ascii=False))
