# -*- coding: utf-8 -*-
"""instalar_v406.py -- instala o candidato v406 no canonico (ato da gerencia c1; adaptado em 02/11/2026 para o BUNDLE do fecho, NAO executado na preparacao). Molde: instalar_v405.py (a lista dos modulos e' a do bundle de 301, como no instalar_v394.py). Fail-closed:
  * o canonico tem de ser a v405 selada (ESPERADOS_v406.origem_sha16 == CANDIDATO_v406.base_v405_sha16, lido do arquivo) e o candidato o de ESPERADOS e do registro;
  * o recibo pre_selo do B(n) (PINO_RECIBO_PRE_SELO_v406.json) tem de existir, estar pinado (sha256 do arquivo == o do pino), ser UTILIZAVEL e ser do um.py que esta no Nos agora (a licao da v405: o recibo e' gerado e pinado ANTES da instalacao; aqui GERADO NOVO, em ensaio contra a Bancada que JA pina a v405) e a Bancada de producao tem de seguir pinando o que o recibo diz (o sha256 do manifesto dela == o do pino);
  * o cache do pilar tem de guardar o resultado reaproveitado (o mesmo que a v406 reaproveita pela chave);
  * nenhum processo um.py ou trabalhador do pilar rodando (a v406 traz 301 modulos novos de kernel em TGLExt/F1Fecho394 [o BUNDLE do fecho: os 300 da bancada do ChatGPT e a candidata CanonicalFullTGLWitnessR1 da gerencia; o nome desta e' provisorio, os das pedras sao do operador]; o numero e a lista sao lidos de kernel_modulos_novos_v406.json e conferidos contra ESPERADOS.bundle_sha256: o proprio rito os materializa a partir do corpo embutido);
  * BACKUP DE BYTES de um.py, um_absoluto.json, _selo.json, _forma_canonica.md, _manifest.md, _pilar_quantico.json, tgl_kernel/TGLExt.lean e tgl_kernel/TGL/Audit.lean;
  * COPIA DE BYTES do resultado do pilar no cache para o pacote (pilar_anterior_v405_<ts>/);
  * candidato -> temporario -> conferir -> os.replace; grava APLICADO_AO_CANONICO_<ts>.json."""
import hashlib, json, os, subprocess, sys, time
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v406.json"), encoding="utf-8")); CM = json.load(open(os.path.join(HERE, "CANDIDATO_v406.json"), encoding="utf-8"))
CAND = os.path.join(HERE, "um_v406_candidato.py")
h16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
ps = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                     "$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | "
                     "Where-Object { $_.CommandLine -ne $null -and ($_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|$)' -or $_.CommandLine -match 'pilar_quantico_worker\\.py') } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'"],
                    capture_output=True, text=True, timeout=60)
assert ps.returncode == 0 and "VIGIA_OK" in ps.stdout, "o vigia de processos FALHOU -- nao instalo"
assert not [x for x in ps.stdout.split() if x.strip().isdigit()], "ha processo um.py ou trabalhador do pilar rodando -- nao instalo"
um = os.path.join(NOS, "um.py"); raw0 = open(um, "rb").read()
assert h16(raw0) == ESP["origem_sha16"] == CM["base_v405_sha16"], "o canonico nao e a v405 selada (%s)" % h16(raw0)
cand = open(CAND, "rb").read(); assert h16(cand) == ESP["candidato_sha16"] == CM["sha16"] and len(cand) == ESP["candidato_bytes"]
# o recibo pre_selo do B(n): gerado e PINADO antes da instalacao (a producao so' foi lida); utilizavel; do um.py que esta no Nos agora
_pino_p = os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v406.json")
assert os.path.exists(_pino_p), "falta PINO_RECIBO_PRE_SELO_v406.json: o recibo pre_selo do B(n) tem de ser gerado e pinado ANTES da instalacao -- nao instalo"
PINO = json.load(open(_pino_p, encoding="utf-8"))
assert os.path.exists(PINO["path"]) and hashlib.sha256(open(PINO["path"], "rb").read()).hexdigest() == PINO["sha256"], "o recibo pre_selo pinado mudou ou sumiu -- nao instalo"
assert PINO["utilizavel_como_recibo_pre_selo_do_B_n"] is True and PINO["versao_nos"] == "v405" and PINO["um_py_sha16_do_nos"] == h16(raw0), "o recibo pre_selo nao e' utilizavel ou nao e' do um.py que esta no Nos -- nao instalo"
_bmp = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "canonical_contracts.json"); _bmb = open(_bmp, "rb").read(); _bm = json.loads(_bmb.decode("utf-8"))
assert hashlib.sha256(_bmb).hexdigest() == PINO["valido_enquanto"]["bancada_pina"]["manifesto_sha256"] and _bm["canonical"].get("version") == "v405" == PINO["valido_enquanto"]["bancada_pina"]["version"], "a Bancada de producao nao pina mais o que o recibo pre_selo diz (re-pino antes do B(n)): o recibo ficou obsoleto -- nao instalo"
_cdir = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "cache", "checkpoints", "quantum_pillar", ESP["pilar"]["key"])
assert hashlib.sha256(open(os.path.join(_cdir, "result.json"), "rb").read()).hexdigest() == ESP["pilar"]["result_sha256"], "o cache do pilar nao guarda o resultado reaproveitado"
# v406: (a) as pedras anteriores (o criterio binario, a rede de Fock, o tempo, Psibit, TestemunhaEstatica, Token, Sonico, AfinacaoDasCordas, FalsidadeDaInercia, PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional, Caminho, Vida, VerdadeAdendo, ProjecaoTransversalDaMeiaNat, Jo8v32 e as OITO da v405: PonteDaMassa, MassaTensaoPura, Identidade, ObservadorTerminal, LeiDoDiminuto, TonicaDoHamiltoniano, DiscoDeEuler e PontoZeroDoPsion) JA estao no kernel do Nos (a base instalada e' a v405 selada); (b) os 301 modulos novos da v406 (o bundle do fecho em TGLExt/F1Fecho394) NAO estao la ainda.
# A lista dos modulos novos vem de kernel_modulos_novos_v406.json (campo 'novos', uma LISTA); o numero e' o comprimento dela, conferido contra ESPERADOS. Fail-closed em tudo.
_PEDRAS_ANTERIORES = ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica", "Token", "Sonico", "AfinacaoDasCordas", "Testemunho", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional", "Caminho", "Vida", "VerdadeAdendo", "ProjecaoTransversalDaMeiaNat", "Jo8v32", "PonteDaMassa", "MassaTensaoPura", "Identidade", "ObservadorTerminal", "LeiDoDiminuto", "TonicaDoHamiltoniano", "DiscoDeEuler", "PontoZeroDoPsion")
assert all(os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", n_ + ".lean")) for n_ in _PEDRAS_ANTERIORES) and os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "F1Fecho394", "NetworkProofAuditR8.lean")), "as pedras anteriores (v394 a v405, as oito da v405 inclusive) nao estao no kernel do Nos -- nao instalo"
_nj = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v406.json"), encoding="utf-8"))
assert isinstance(_nj["novos"], list), "kernel_modulos_novos_v406.json tem de trazer a LISTA em 'novos'"
NOVOS_V406 = list(_nj["novos"]); _N = len(NOVOS_V406)
assert _N == len(set(NOVOS_V406)) == ESP["kernel"]["modulos_novos"] == len(ESP["bundle_sha256"]) == 301 and set(NOVOS_V406) == set(ESP["bundle_sha256"]) and all(x_.startswith("TGLExt/F1Fecho394/") and x_.endswith(".lean") for x_ in NOVOS_V406), ("a lista dos modulos novos nao e' a do ESPERADOS (o bundle de 301)", _N)
assert not [rel for rel in NOVOS_V406 if os.path.exists(os.path.join(NOS, "tgl_kernel", *rel.split("/")))], "algum dos modulos novos (v406) ja esta no kernel do Nos -- nao instalo"
ts = time.strftime("%Y%m%d_%H%M%S"); rec = {"ts": ts, "backups": {}}
rec["modulos_novos_v406"] = {"fonte": "kernel_modulos_novos_v406.json[novos]", "n": _N, "lista": NOVOS_V406}   # o reverter usa ESTA lista (a que o instalar conferiu)
rec["pino_recibo_pre_selo"] = {"path": _pino_p, "sha16": h16(open(_pino_p, "rb").read()), "recibo_sha256": PINO["sha256"], "veredito": PINO["veredito"]}
for rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "um_absoluto_pilar_quantico.json", "um_absoluto_selo_acom.json", "tgl_kernel_proof_manifest.json",
            os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")):   # (licao 2 da v405: o rito reescreve o manifesto do kernel; ele entra nos backups e o reverter o restaura)
    p = os.path.join(NOS, rel); b = p + ".bak_" + ts; assert not os.path.exists(b), b
    data = open(p, "rb").read(); open(b, "wb").write(data); assert open(b, "rb").read() == data, "backup falhou: %s" % b
    rec["backups"][rel] = {"backup": b, "bytes": len(data), "sha16": h16(data)}
_dst = os.path.join(HERE, "pilar_anterior_v405_" + ts); os.makedirs(_dst); rec["pilar_anterior_v405"] = {"de": _cdir, "para": _dst, "arquivos": {}}
for f_ in sorted(os.listdir(_cdir)):
    sp = os.path.join(_cdir, f_)
    if os.path.isfile(sp):
        data = open(sp, "rb").read(); open(os.path.join(_dst, f_), "wb").write(data); assert open(os.path.join(_dst, f_), "rb").read() == data
        rec["pilar_anterior_v405"]["arquivos"][f_] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
assert rec["pilar_anterior_v405"]["arquivos"]["result.json"]["sha256"] == ESP["pilar"]["result_sha256"]
tmp = um + ".tmp_instalar_v406_" + ts; open(tmp, "wb").write(cand)
assert os.path.getsize(tmp) == len(cand) and h16(open(tmp, "rb").read()) == ESP["candidato_sha16"]
assert open(um, "rb").read() == raw0, "o um.py mudou entre a leitura e a troca -- nao substituo"
os.replace(tmp, um); assert h16(open(um, "rb").read()) == ESP["candidato_sha16"]
rec["um_py_novo"] = {"bytes": len(cand), "sha16": ESP["candidato_sha16"], "origem": CAND}
out = os.path.join(HERE, "APLICADO_AO_CANONICO_%s.json" % ts); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1)); os.replace(out + ".tmp", out)
print(json.dumps({"ts": ts, "um_py_novo": rec["um_py_novo"], "n_backups": len(rec["backups"]), "modulos_novos": _N}, ensure_ascii=False))
