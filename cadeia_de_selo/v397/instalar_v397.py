# -*- coding: utf-8 -*-
"""instalar_v397.py -- instala o candidato v397 no canonico (ato da gerencia c1; escrito em 23/10/2026, NAO executado na preparacao). Molde: instalar_v396.py. Fail-closed:
  * o canonico tem de ser a v396 selada (ESPERADOS_v397.origem_sha16 == CANDIDATO_v397.base_v396_sha16, lido do arquivo) e o candidato o de ESPERADOS e do registro;
  * o recibo pre_selo do B(n) (PINO_RECIBO_PRE_SELO_v397.json) tem de existir, estar pinado (sha256 do arquivo == o do pino), ser UTILIZAVEL e ser do um.py que esta no Nos agora (a licao da v396: o recibo e' gerado e pinado ANTES da instalacao);
  * o cache do pilar tem de guardar o resultado reaproveitado (o mesmo que a v397 reaproveita pela chave);
  * nenhum processo um.py ou trabalhador do pilar rodando (a v397 traz UM modulo novo de kernel, o numero lido de kernel_modulos_novos_v397.json: o proprio rito o materializa a partir do corpo embutido);
  * BACKUP DE BYTES de um.py, um_absoluto.json, _selo.json, _forma_canonica.md, _manifest.md, _pilar_quantico.json, tgl_kernel/TGLExt.lean e tgl_kernel/TGL/Audit.lean;
  * COPIA DE BYTES do resultado do pilar no cache para o pacote (pilar_anterior_v396_<ts>/);
  * candidato -> temporario -> conferir -> os.replace; grava APLICADO_AO_CANONICO_<ts>.json."""
import hashlib, json, os, subprocess, sys, time
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v397.json"), encoding="utf-8")); CM = json.load(open(os.path.join(HERE, "CANDIDATO_v397.json"), encoding="utf-8"))
CAND = os.path.join(HERE, "um_v397_candidato.py")
h16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
ps = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                     "$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | "
                     "Where-Object { $_.CommandLine -ne $null -and ($_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|$)' -or $_.CommandLine -match 'pilar_quantico_worker\\.py') } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'"],
                    capture_output=True, text=True, timeout=60)
assert ps.returncode == 0 and "VIGIA_OK" in ps.stdout, "o vigia de processos FALHOU -- nao instalo"
assert not [x for x in ps.stdout.split() if x.strip().isdigit()], "ha processo um.py ou trabalhador do pilar rodando -- nao instalo"
um = os.path.join(NOS, "um.py"); raw0 = open(um, "rb").read()
assert h16(raw0) == ESP["origem_sha16"] == CM["base_v396_sha16"], "o canonico nao e a v396 selada (%s)" % h16(raw0)
cand = open(CAND, "rb").read(); assert h16(cand) == ESP["candidato_sha16"] == CM["sha16"] and len(cand) == ESP["candidato_bytes"]
# o recibo pre_selo do B(n): gerado e PINADO antes da instalacao (a producao so' foi lida); utilizavel; do um.py que esta no Nos agora
_pino_p = os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v397.json")
assert os.path.exists(_pino_p), "falta PINO_RECIBO_PRE_SELO_v397.json: o recibo pre_selo do B(n) tem de ser gerado e pinado ANTES da instalacao -- nao instalo"
PINO = json.load(open(_pino_p, encoding="utf-8"))
assert os.path.exists(PINO["path"]) and hashlib.sha256(open(PINO["path"], "rb").read()).hexdigest() == PINO["sha256"], "o recibo pre_selo pinado mudou ou sumiu -- nao instalo"
assert PINO["utilizavel_como_recibo_pre_selo_do_B_n"] is True and PINO["versao_nos"] == "v396" and PINO["um_py_sha16_do_nos"] == h16(raw0), "o recibo pre_selo nao e' utilizavel ou nao e' do um.py que esta no Nos -- nao instalo"
_cdir = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "cache", "checkpoints", "quantum_pillar", ESP["pilar"]["key"])
assert hashlib.sha256(open(os.path.join(_cdir, "result.json"), "rb").read()).hexdigest() == ESP["pilar"]["result_sha256"], "o cache do pilar nao guarda o resultado reaproveitado"
# v397: (a) as pedras anteriores (o criterio binario, a rede de Fock, o tempo, Psibit e TestemunhaEstatica) JA estao no kernel do Nos (a base instalada e' a v396 selada); (b) o modulo novo da v397 (Token) NAO esta la ainda.
# A lista dos modulos novos vem de kernel_modulos_novos_v397.json (campo 'novos', uma LISTA); o numero e' o comprimento dela, conferido contra ESPERADOS. Fail-closed em tudo.
_PEDRAS_ANTERIORES = ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica")
assert all(os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", n_ + ".lean")) for n_ in _PEDRAS_ANTERIORES) and os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "F1Fecho394", "NetworkProofAuditR8.lean")), "as pedras anteriores (v394 a v396) nao estao no kernel do Nos -- nao instalo"
_nj = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v397.json"), encoding="utf-8"))
assert isinstance(_nj["novos"], list), "kernel_modulos_novos_v397.json tem de trazer a LISTA em 'novos'"
NOVOS_V397 = list(_nj["novos"]); _N = len(NOVOS_V397)
assert _N == len(set(NOVOS_V397)) == ESP["kernel"]["modulos_novos"] == len(ESP["pedras_sha256"]) and set(NOVOS_V397) == set(ESP["pedras_sha256"]) and all(x_.startswith("TGLExt/") and x_.endswith(".lean") for x_ in NOVOS_V397), ("a lista dos modulos novos nao e' a do ESPERADOS", _N)
assert not [rel for rel in NOVOS_V397 if os.path.exists(os.path.join(NOS, "tgl_kernel", *rel.split("/")))], "algum dos modulos novos (v397) ja esta no kernel do Nos -- nao instalo"
ts = time.strftime("%Y%m%d_%H%M%S"); rec = {"ts": ts, "backups": {}}
rec["modulos_novos_v397"] = {"fonte": "kernel_modulos_novos_v397.json[novos]", "n": _N, "lista": NOVOS_V397}   # o reverter usa ESTA lista (a que o instalar conferiu)
rec["pino_recibo_pre_selo"] = {"path": _pino_p, "sha16": h16(open(_pino_p, "rb").read()), "recibo_sha256": PINO["sha256"], "veredito": PINO["veredito"]}
for rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "um_absoluto_pilar_quantico.json",
            os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")):
    p = os.path.join(NOS, rel); b = p + ".bak_" + ts; assert not os.path.exists(b), b
    data = open(p, "rb").read(); open(b, "wb").write(data); assert open(b, "rb").read() == data, "backup falhou: %s" % b
    rec["backups"][rel] = {"backup": b, "bytes": len(data), "sha16": h16(data)}
_dst = os.path.join(HERE, "pilar_anterior_v396_" + ts); os.makedirs(_dst); rec["pilar_anterior_v396"] = {"de": _cdir, "para": _dst, "arquivos": {}}
for f_ in sorted(os.listdir(_cdir)):
    sp = os.path.join(_cdir, f_)
    if os.path.isfile(sp):
        data = open(sp, "rb").read(); open(os.path.join(_dst, f_), "wb").write(data); assert open(os.path.join(_dst, f_), "rb").read() == data
        rec["pilar_anterior_v396"]["arquivos"][f_] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
assert rec["pilar_anterior_v396"]["arquivos"]["result.json"]["sha256"] == ESP["pilar"]["result_sha256"]
tmp = um + ".tmp_instalar_v397_" + ts; open(tmp, "wb").write(cand)
assert os.path.getsize(tmp) == len(cand) and h16(open(tmp, "rb").read()) == ESP["candidato_sha16"]
assert open(um, "rb").read() == raw0, "o um.py mudou entre a leitura e a troca -- nao substituo"
os.replace(tmp, um); assert h16(open(um, "rb").read()) == ESP["candidato_sha16"]
rec["um_py_novo"] = {"bytes": len(cand), "sha16": ESP["candidato_sha16"], "origem": CAND}
out = os.path.join(HERE, "APLICADO_AO_CANONICO_%s.json" % ts); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1)); os.replace(out + ".tmp", out)
print(json.dumps({"ts": ts, "um_py_novo": rec["um_py_novo"], "n_backups": len(rec["backups"]), "modulos_novos": _N}, ensure_ascii=False))
