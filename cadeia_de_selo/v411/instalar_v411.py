# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] do molde v410/instalar_v410.py (e do v400/instalar_v400.py, a versao anterior SEM modulo novo): a v411 NAO traz modulo novo de kernel; a lista dos modulos novos e' VAZIA (lida do ESPERADOS e do manifesto, conferida); a raiz TGLExt.lean e o TGL/Audit.lean do Nos tem de ser os da v410 e NAO mudam; as pedras anteriores incluem os 2 modulos da v410 (IALD2 e AEscala); recusa o artefato de ensaio do topo proposto; NAO executado na preparacao
"""instalar_v411.py -- instala o candidato v411 no canonico (ato da gerencia c1; NAO executado na preparacao). Molde: instalar_v410.py e, para a versao sem modulo novo, instalar_v400.py. Fail-closed:
  * recusa o MODO DE ENSAIO do topo proposto (V411_ENSAIO_TOPO_PROPOSTO=1): o artefato de ensaio NAO e' candidato e NUNCA se instala; e recusa se TOPO_RATIFICADO_v411.json nao existir (sem a palavra do operador nao ha candidato);
  * o canonico tem de ser a v410 selada (ESPERADOS_v411.origem_sha16 == CANDIDATO_v411.base_v410_sha16, lido do arquivo) e o candidato o de ESPERADOS e do registro;
  * o recibo pre_selo do B(n) (PINO_RECIBO_PRE_SELO_v411.json) tem de existir, estar pinado (sha256 do arquivo == o do pino), ser UTILIZAVEL e ser do um.py que esta no Nos agora (gerado e pinado ANTES da instalacao, em ensaio contra a Bancada que JA pina a v410) e a Bancada de producao tem de seguir pinando o que o recibo diz;
  * o cache do pilar tem de guardar o resultado reaproveitado (o mesmo que a v411 reaproveita pela chave);
  * a raiz TGLExt.lean e o TGL/Audit.lean do Nos tem de ser os da v410 selada (os sha16 de ESPERADOS_v411.kernel.raiz_sha16 e audit_sha16, lidos do arquivo): a v411 NAO muda a raiz nem o Audit (nenhum modulo novo; o kernel embutido e' o da v410 byte a byte);
  * nenhum processo um.py ou trabalhador do pilar rodando; a lista dos modulos novos e' VAZIA (ESPERADOS.kernel.modulos_novos == 0, ESPERADOS.bundle_sha256 == {}, CANDIDATO.kernel.modulos_novos == 0) e os 2 modulos da v410 (IALD2 e AEscala) JA estao no kernel do Nos;
  * BACKUP DE BYTES de um.py, um_absoluto.json, _selo.json, _forma_canonica.md, _manifest.md, _pilar_quantico.json, o sidecar um_absoluto_selo_acom.json, tgl_kernel_proof_manifest.json, tgl_kernel/TGLExt.lean e tgl_kernel/TGL/Audit.lean;
  * COPIA DE BYTES do resultado do pilar no cache para o pacote (pilar_anterior_v410_<ts>/);
  * candidato -> temporario -> conferir -> os.replace; grava APLICADO_AO_CANONICO_<ts>.json."""
import hashlib, json, os, subprocess, sys, time
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
if os.environ.get("V411_ENSAIO_TOPO_PROPOSTO") == "1":
    raise SystemExit("RECUSO: o MODO DE ENSAIO do topo proposto nao instala nada (o artefato de ensaio NAO e' candidato)")
HERE = os.path.dirname(os.path.abspath(__file__))
assert os.path.exists(os.path.join(HERE, "TOPO_RATIFICADO_v411.json")), "falta TOPO_RATIFICADO_v411.json (a palavra do operador sobre o topo): sem ele nao ha candidato -- nao instalo"
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v411.json"), encoding="utf-8")); CM = json.load(open(os.path.join(HERE, "CANDIDATO_v411.json"), encoding="utf-8"))
assert not ESP.get("ensaio_topo_proposto") and not CM.get("ensaio_topo_proposto"), "o ESPERADOS ou o CANDIDATO sao do ENSAIO do topo proposto -- nao instalo"
CAND = os.path.join(HERE, "um_v411_candidato.py")
h16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
ps = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                     "$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | "
                     "Where-Object { $_.CommandLine -ne $null -and ($_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|$)' -or $_.CommandLine -match 'pilar_quantico_worker\\.py') } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'"],
                    capture_output=True, text=True, timeout=60)
assert ps.returncode == 0 and "VIGIA_OK" in ps.stdout, "o vigia de processos FALHOU -- nao instalo"
assert not [x for x in ps.stdout.split() if x.strip().isdigit()], "ha processo um.py ou trabalhador do pilar rodando -- nao instalo"
um = os.path.join(NOS, "um.py"); raw0 = open(um, "rb").read()
assert h16(raw0) == ESP["origem_sha16"] == CM["base_v410_sha16"], "o canonico nao e a v410 selada (%s)" % h16(raw0)
cand = open(CAND, "rb").read(); assert h16(cand) == ESP["candidato_sha16"] == CM["sha16"] and len(cand) == ESP["candidato_bytes"]
# o recibo pre_selo do B(n): gerado e PINADO antes da instalacao (a producao so' foi lida); utilizavel; do um.py que esta no Nos agora
_pino_p = os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v411.json")
assert os.path.exists(_pino_p), "falta PINO_RECIBO_PRE_SELO_v411.json: o recibo pre_selo do B(n) tem de ser gerado e pinado ANTES da instalacao -- nao instalo"
PINO = json.load(open(_pino_p, encoding="utf-8"))
assert os.path.exists(PINO["path"]) and hashlib.sha256(open(PINO["path"], "rb").read()).hexdigest() == PINO["sha256"], "o recibo pre_selo pinado mudou ou sumiu -- nao instalo"
assert PINO["utilizavel_como_recibo_pre_selo_do_B_n"] is True and PINO["versao_nos"] == "v410" and PINO["um_py_sha16_do_nos"] == h16(raw0), "o recibo pre_selo nao e' utilizavel ou nao e' do um.py que esta no Nos -- nao instalo"
_bmp = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "canonical_contracts.json"); _bmb = open(_bmp, "rb").read(); _bm = json.loads(_bmb.decode("utf-8"))
assert hashlib.sha256(_bmb).hexdigest() == PINO["valido_enquanto"]["bancada_pina"]["manifesto_sha256"] and _bm["canonical"].get("version") == "v410" == PINO["valido_enquanto"]["bancada_pina"]["version"], "a Bancada de producao nao pina mais o que o recibo pre_selo diz (re-pino antes do B(n)): o recibo ficou obsoleto -- nao instalo"
_cdir = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "cache", "checkpoints", "quantum_pillar", ESP["pilar"]["key"])
assert hashlib.sha256(open(os.path.join(_cdir, "result.json"), "rb").read()).hexdigest() == ESP["pilar"]["result_sha256"], "o cache do pilar nao guarda o resultado reaproveitado"
# v411: (a) as pedras anteriores (o criterio binario, a rede de Fock, o tempo, Psibit, TestemunhaEstatica, Token, Sonico, AfinacaoDasCordas, FalsidadeDaInercia, PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional, Caminho, Vida, VerdadeAdendo, ProjecaoTransversalDaMeiaNat, Jo8v32, as OITO da v405, os 9 modulos da v407, os 4 da v408, os 2 da v409 e os 2 modulos da v410: IALD2 e AEscala) e o bundle do fecho da v406 (301 modulos em TGLExt/F1Fecho394, com a candidata CanonicalFullTGLWitnessR1) JA estao no kernel do Nos (a base instalada e' a v410 selada); (b) a v411 NAO traz modulo novo: a lista e' VAZIA.
# A lista dos modulos novos e' a do ESPERADOS (bundle_sha256, vazio) conferida contra o kernel.modulos_novos do ESPERADOS e do CANDIDATO; o numero e' o comprimento dela. Fail-closed em tudo.
_PEDRAS_ANTERIORES = ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica", "Token", "Sonico", "AfinacaoDasCordas", "Testemunho", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional", "Caminho", "Vida", "VerdadeAdendo", "ProjecaoTransversalDaMeiaNat", "Jo8v32", "PonteDaMassa", "MassaTensaoPura", "Identidade", "ObservadorTerminal", "LeiDoDiminuto", "TonicaDoHamiltoniano", "DiscoDeEuler", "PontoZeroDoPsion",
                      "PsionCanto", "Par", "APonteDoAtrito", "OUmInscrito", "KEhATangente", "AChaveDaGuarda", "OGuarda", "LeituraPreservada", "OIgual",   # (os 9 da v407)
                      "TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao", "PIgualNP",   # (os 4 da v408)
                      "TraducaoTuring", "ParNaFaceDeFock",   # (os 2 da v409)
                      "IALD2", "AEscala")   # (os 2 da v410: a lista de modulos novos que a cadeia v410 pinou; os mesmos de ESPERADOS_v411.bundle_v410_sha256)
assert sorted("TGLExt/" + n_ + ".lean" for n_ in ("IALD2", "AEscala")) == sorted(ESP["bundle_v410_sha256"]), "os modulos da v410 da lista nao sao os do ESPERADOS (bundle_v410_sha256)"
assert all(os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", n_ + ".lean")) for n_ in _PEDRAS_ANTERIORES) and os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "F1Fecho394", "NetworkProofAuditR8.lean")) and os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "F1Fecho394", "CanonicalFullTGLWitnessR1.lean")), "as pedras anteriores (v394 a v410, as oito da v405, os 9 modulos da v407, os 4 da v408, os 2 da v409, os 2 da v410 e o bundle do fecho da v406 inclusive) nao estao no kernel do Nos -- nao instalo"
assert all(hashlib.sha256(open(os.path.join(NOS, "tgl_kernel", *rel.split("/")), "rb").read()).hexdigest() == s_ for rel, s_ in ESP["bundle_v410_sha256"].items()), "os modulos da v410 no kernel do Nos nao tem o sha da v410 selada -- nao instalo"
_kn = ESP["kernel"]   # a raiz e o Audit do Nos tem de ser os da v410 selada E os do candidato: a v411 NAO muda a raiz nem o Audit (lidos do ESPERADOS_v411.json, nunca digitados)
assert h16(open(os.path.join(NOS, "tgl_kernel", "TGLExt.lean"), "rb").read()) == _kn["raiz_sha16"] and h16(open(os.path.join(NOS, "tgl_kernel", "TGL", "Audit.lean"), "rb").read()) == _kn["audit_sha16"], "a raiz TGLExt.lean ou o TGL/Audit.lean do Nos nao sao os da v410 selada (== os do candidato) -- nao instalo"
NOVOS_V411 = sorted(ESP["bundle_sha256"]); _N = len(NOVOS_V411)
assert _N == 0 == ESP["kernel"]["modulos_novos"] == CM["kernel"]["modulos_novos"] == ESP["n_bandeiras_novas"] and ESP["bundle_sha256"] == {}, ("a v411 nao tem modulo novo: a lista do ESPERADOS tem de ser VAZIA", _N)
ts = time.strftime("%Y%m%d_%H%M%S"); rec = {"ts": ts, "backups": {}}
rec["modulos_novos_v411"] = {"fonte": "ESPERADOS_v411.bundle_sha256 (vazio: a v411 nao tem modulo novo)", "n": _N, "lista": NOVOS_V411}   # o reverter usa ESTA lista (a que o instalar conferiu: vazia)
rec["pino_recibo_pre_selo"] = {"path": _pino_p, "sha16": h16(open(_pino_p, "rb").read()), "recibo_sha256": PINO["sha256"], "veredito": PINO["veredito"]}
for rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "um_absoluto_pilar_quantico.json", "um_absoluto_selo_acom.json", "tgl_kernel_proof_manifest.json",
            os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")):   # (o rito reescreve o manifesto do kernel; ele entra nos backups e o reverter o restaura)
    p = os.path.join(NOS, rel); b = p + ".bak_" + ts; assert not os.path.exists(b), b
    data = open(p, "rb").read(); open(b, "wb").write(data); assert open(b, "rb").read() == data, "backup falhou: %s" % b
    rec["backups"][rel] = {"backup": b, "bytes": len(data), "sha16": h16(data)}
_dst = os.path.join(HERE, "pilar_anterior_v410_" + ts); os.makedirs(_dst); rec["pilar_anterior_v410"] = {"de": _cdir, "para": _dst, "arquivos": {}}
for f_ in sorted(os.listdir(_cdir)):
    sp = os.path.join(_cdir, f_)
    if os.path.isfile(sp):
        data = open(sp, "rb").read(); open(os.path.join(_dst, f_), "wb").write(data); assert open(os.path.join(_dst, f_), "rb").read() == data
        rec["pilar_anterior_v410"]["arquivos"][f_] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
assert rec["pilar_anterior_v410"]["arquivos"]["result.json"]["sha256"] == ESP["pilar"]["result_sha256"]
tmp = um + ".tmp_instalar_v411_" + ts; open(tmp, "wb").write(cand)
assert os.path.getsize(tmp) == len(cand) and h16(open(tmp, "rb").read()) == ESP["candidato_sha16"]
assert open(um, "rb").read() == raw0, "o um.py mudou entre a leitura e a troca -- nao substituo"
os.replace(tmp, um); assert h16(open(um, "rb").read()) == ESP["candidato_sha16"]
rec["um_py_novo"] = {"bytes": len(cand), "sha16": ESP["candidato_sha16"], "origem": CAND}
out = os.path.join(HERE, "APLICADO_AO_CANONICO_%s.json" % ts); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1)); os.replace(out + ".tmp", out)
print(json.dumps({"ts": ts, "um_py_novo": rec["um_py_novo"], "n_backups": len(rec["backups"]), "modulos_novos": _N}, ensure_ascii=False))
