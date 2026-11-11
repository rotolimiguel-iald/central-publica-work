# -*- coding: utf-8 -*-
# [ADAPTADO v410 PARTE 2, 09/11/2026 (~18h), claude-subagente-adaptacao (Sonnet 5.5, A), a servico do construtor claude-construtor-v410] so' texto: o bundle e' de DOIS modulos em TGLExt/ (IALD2 e AEscala; a raiz ganha dois imports); o codigo e' generico (a lista dos modulos novos vem de kernel_modulos_novos_v410.json e e' conferida contra o ESPERADOS), nada de numero digitado
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] instala o candidato v410 (ato da gerencia): a raiz ganha os imports do bundle (um por modulo: IALD2 e AEscala); as pedras anteriores incluem os 9 da v407, os 4 da v408 e os 2 da v409; a lista dos modulos novos lida de kernel_modulos_novos_v410.json; conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
"""instalar_v410.py -- instala o candidato v410 no canonico (ato da gerencia c1; adaptado em 06/11/2026 por claude-construtor-v410 para o BUNDLE PEQUENO de dois modulos em TGLExt/ [IALD2 e AEscala], NAO executado na preparacao). Molde: instalar_v409.py (a lista dos modulos vem de kernel_modulos_novos_v410.json, como no instalar_v394.py). Fail-closed:
  * o canonico tem de ser a v409 selada (ESPERADOS_v410.origem_sha16 == CANDIDATO_v410.base_v409_sha16, lido do arquivo) e o candidato o de ESPERADOS e do registro;
  * o recibo pre_selo do B(n) (PINO_RECIBO_PRE_SELO_v410.json) tem de existir, estar pinado (sha256 do arquivo == o do pino), ser UTILIZAVEL e ser do um.py que esta no Nos agora (a licao da v409: o recibo e' gerado e pinado ANTES da instalacao; aqui GERADO NOVO, em ensaio contra a Bancada que JA pina a v409) e a Bancada de producao tem de seguir pinando o que o recibo diz (o sha256 do manifesto dela == o do pino);
  * o cache do pilar tem de guardar o resultado reaproveitado (o mesmo que a v410 reaproveita pela chave);
  * a raiz TGLExt.lean e o TGL/Audit.lean do Nos tem de ser os da v409 selada (os sha16 de CANDIDATO_v410.kernel.raiz_v409_sha16 e audit_v409_sha16, lidos do arquivo): a v410 so' ACRESCENTA imports na raiz (um por modulo do bundle: IALD2 e AEscala) e nao muda o Audit;
  * nenhum processo um.py ou trabalhador do pilar rodando (a v410 traz dois modulos novos de kernel em TGLExt/ [IALD2, com o NOME do modulo dado pelo operador em 06/11/2026 e os nomes das declaracoes da gerencia, RATIFICADOS pelo operador em 09/11/2026 (D74); e AEscala, com o nome do modulo e os nomes das declaracoes RATIFICADOS em 09/11/2026 (D87); nenhum da bancada do ChatGPT]; o numero e a lista sao lidos de kernel_modulos_novos_v410.json e conferidos contra ESPERADOS.bundle_sha256: o proprio rito os materializa a partir do corpo embutido);
  * BACKUP DE BYTES de um.py, um_absoluto.json, _selo.json, _forma_canonica.md, _manifest.md, _pilar_quantico.json, tgl_kernel/TGLExt.lean e tgl_kernel/TGL/Audit.lean;
  * COPIA DE BYTES do resultado do pilar no cache para o pacote (pilar_anterior_v409_<ts>/);
  * candidato -> temporario -> conferir -> os.replace; grava APLICADO_AO_CANONICO_<ts>.json."""
import hashlib, json, os, subprocess, sys, time
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v410.json"), encoding="utf-8")); CM = json.load(open(os.path.join(HERE, "CANDIDATO_v410.json"), encoding="utf-8"))
CAND = os.path.join(HERE, "um_v410_candidato.py")
h16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
ps = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                     "$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | "
                     "Where-Object { $_.CommandLine -ne $null -and ($_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|$)' -or $_.CommandLine -match 'pilar_quantico_worker\\.py') } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'"],
                    capture_output=True, text=True, timeout=60)
assert ps.returncode == 0 and "VIGIA_OK" in ps.stdout, "o vigia de processos FALHOU -- nao instalo"
assert not [x for x in ps.stdout.split() if x.strip().isdigit()], "ha processo um.py ou trabalhador do pilar rodando -- nao instalo"
um = os.path.join(NOS, "um.py"); raw0 = open(um, "rb").read()
assert h16(raw0) == ESP["origem_sha16"] == CM["base_v409_sha16"], "o canonico nao e a v409 selada (%s)" % h16(raw0)
cand = open(CAND, "rb").read(); assert h16(cand) == ESP["candidato_sha16"] == CM["sha16"] and len(cand) == ESP["candidato_bytes"]
# o recibo pre_selo do B(n): gerado e PINADO antes da instalacao (a producao so' foi lida); utilizavel; do um.py que esta no Nos agora
_pino_p = os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v410.json")
assert os.path.exists(_pino_p), "falta PINO_RECIBO_PRE_SELO_v410.json: o recibo pre_selo do B(n) tem de ser gerado e pinado ANTES da instalacao -- nao instalo"
PINO = json.load(open(_pino_p, encoding="utf-8"))
assert os.path.exists(PINO["path"]) and hashlib.sha256(open(PINO["path"], "rb").read()).hexdigest() == PINO["sha256"], "o recibo pre_selo pinado mudou ou sumiu -- nao instalo"
assert PINO["utilizavel_como_recibo_pre_selo_do_B_n"] is True and PINO["versao_nos"] == "v409" and PINO["um_py_sha16_do_nos"] == h16(raw0), "o recibo pre_selo nao e' utilizavel ou nao e' do um.py que esta no Nos -- nao instalo"
_bmp = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "canonical_contracts.json"); _bmb = open(_bmp, "rb").read(); _bm = json.loads(_bmb.decode("utf-8"))
assert hashlib.sha256(_bmb).hexdigest() == PINO["valido_enquanto"]["bancada_pina"]["manifesto_sha256"] and _bm["canonical"].get("version") == "v409" == PINO["valido_enquanto"]["bancada_pina"]["version"], "a Bancada de producao nao pina mais o que o recibo pre_selo diz (re-pino antes do B(n)): o recibo ficou obsoleto -- nao instalo"
_cdir = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "cache", "checkpoints", "quantum_pillar", ESP["pilar"]["key"])
assert hashlib.sha256(open(os.path.join(_cdir, "result.json"), "rb").read()).hexdigest() == ESP["pilar"]["result_sha256"], "o cache do pilar nao guarda o resultado reaproveitado"
# v410: (a) as pedras anteriores (o criterio binario, a rede de Fock, o tempo, Psibit, TestemunhaEstatica, Token, Sonico, AfinacaoDasCordas, FalsidadeDaInercia, PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional, Caminho, Vida, VerdadeAdendo, ProjecaoTransversalDaMeiaNat, Jo8v32, as OITO da v405: PonteDaMassa, MassaTensaoPura, Identidade, ObservadorTerminal, LeiDoDiminuto, TonicaDoHamiltoniano, DiscoDeEuler e PontoZeroDoPsion, os 9 modulos da v407: PsionCanto, Par, APonteDoAtrito, OUmInscrito, KEhATangente, AChaveDaGuarda, OGuarda, LeituraPreservada, OIgual, os 4 modulos da v408: TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP, e os 2 modulos da v409: TraducaoTuring e ParNaFaceDeFock) e o bundle do fecho da v406 (301 modulos em TGLExt/F1Fecho394, com a candidata CanonicalFullTGLWitnessR1) JA estao no kernel do Nos (a base instalada e' a v409 selada); (b) os modulos novos da v410 (IALD2 e AEscala, em TGLExt/, nao em F1Fecho394) NAO estao la ainda.
# A lista dos modulos novos vem de kernel_modulos_novos_v410.json (campo 'novos', uma LISTA); o numero e' o comprimento dela, conferido contra ESPERADOS. Fail-closed em tudo.
_PEDRAS_ANTERIORES = ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica", "Token", "Sonico", "AfinacaoDasCordas", "Testemunho", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional", "Caminho", "Vida", "VerdadeAdendo", "ProjecaoTransversalDaMeiaNat", "Jo8v32", "PonteDaMassa", "MassaTensaoPura", "Identidade", "ObservadorTerminal", "LeiDoDiminuto", "TonicaDoHamiltoniano", "DiscoDeEuler", "PontoZeroDoPsion",
                      "PsionCanto", "Par", "APonteDoAtrito", "OUmInscrito", "KEhATangente", "AChaveDaGuarda", "OGuarda", "LeituraPreservada", "OIgual",   # (os 9 da v407)
                      "TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao", "PIgualNP",   # (os 4 da v408)
                      "TraducaoTuring", "ParNaFaceDeFock")   # (os 2 da v409: os nomes da lista de modulos novos que a cadeia v409 pinou, conferidos pelo adaptador da v410 contra a lista que a cadeia v409 gravou)
assert all(os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", n_ + ".lean")) for n_ in _PEDRAS_ANTERIORES) and os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "F1Fecho394", "NetworkProofAuditR8.lean")) and os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "F1Fecho394", "CanonicalFullTGLWitnessR1.lean")), "as pedras anteriores (v394 a v409, as oito da v405, os 9 modulos da v407, os 4 da v408, os 2 da v409 e o bundle do fecho da v406 inclusive) nao estao no kernel do Nos -- nao instalo"
_kn = CM["kernel"]   # a raiz e o Audit do Nos tem de ser os da v409 selada: a v410 so' ACRESCENTA imports na raiz (lidos do CANDIDATO_v410.json, nunca digitados)
assert h16(open(os.path.join(NOS, "tgl_kernel", "TGLExt.lean"), "rb").read()) == _kn["raiz_v409_sha16"] and h16(open(os.path.join(NOS, "tgl_kernel", "TGL", "Audit.lean"), "rb").read()) == _kn["audit_v409_sha16"] == _kn["audit_sha16"], "a raiz TGLExt.lean ou o TGL/Audit.lean do Nos nao sao os da v409 selada -- nao instalo"
_nj = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v410.json"), encoding="utf-8"))
assert isinstance(_nj["novos"], list), "kernel_modulos_novos_v410.json tem de trazer a LISTA em 'novos'"
NOVOS_V410 = list(_nj["novos"]); _N = len(NOVOS_V410)
assert _N > 0 and _N == len(set(NOVOS_V410)) == ESP["kernel"]["modulos_novos"] == len(ESP["bundle_sha256"]) and set(NOVOS_V410) == set(ESP["bundle_sha256"]) and all(x_.startswith("TGLExt/") and x_.count("/") == 1 and x_.endswith(".lean") for x_ in NOVOS_V410), ("a lista dos modulos novos nao e' a do ESPERADOS (o bundle de dois modulos em TGLExt/: IALD2 e AEscala)", _N)
assert not [rel for rel in NOVOS_V410 if os.path.exists(os.path.join(NOS, "tgl_kernel", *rel.split("/")))], "algum dos modulos novos (v410) ja esta no kernel do Nos -- nao instalo"
assert _N == CM["kernel"]["modulos_novos"], ("o numero de modulos novos difere do CANDIDATO_v410.json", _N)
ts = time.strftime("%Y%m%d_%H%M%S"); rec = {"ts": ts, "backups": {}}
rec["modulos_novos_v410"] = {"fonte": "kernel_modulos_novos_v410.json[novos]", "n": _N, "lista": NOVOS_V410}   # o reverter usa ESTA lista (a que o instalar conferiu)
rec["pino_recibo_pre_selo"] = {"path": _pino_p, "sha16": h16(open(_pino_p, "rb").read()), "recibo_sha256": PINO["sha256"], "veredito": PINO["veredito"]}
for rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "um_absoluto_pilar_quantico.json", "um_absoluto_selo_acom.json", "tgl_kernel_proof_manifest.json",
            os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")):   # (licao 2 da v409: o rito reescreve o manifesto do kernel; ele entra nos backups e o reverter o restaura)
    p = os.path.join(NOS, rel); b = p + ".bak_" + ts; assert not os.path.exists(b), b
    data = open(p, "rb").read(); open(b, "wb").write(data); assert open(b, "rb").read() == data, "backup falhou: %s" % b
    rec["backups"][rel] = {"backup": b, "bytes": len(data), "sha16": h16(data)}
_dst = os.path.join(HERE, "pilar_anterior_v409_" + ts); os.makedirs(_dst); rec["pilar_anterior_v409"] = {"de": _cdir, "para": _dst, "arquivos": {}}
for f_ in sorted(os.listdir(_cdir)):
    sp = os.path.join(_cdir, f_)
    if os.path.isfile(sp):
        data = open(sp, "rb").read(); open(os.path.join(_dst, f_), "wb").write(data); assert open(os.path.join(_dst, f_), "rb").read() == data
        rec["pilar_anterior_v409"]["arquivos"][f_] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
assert rec["pilar_anterior_v409"]["arquivos"]["result.json"]["sha256"] == ESP["pilar"]["result_sha256"]
tmp = um + ".tmp_instalar_v410_" + ts; open(tmp, "wb").write(cand)
assert os.path.getsize(tmp) == len(cand) and h16(open(tmp, "rb").read()) == ESP["candidato_sha16"]
assert open(um, "rb").read() == raw0, "o um.py mudou entre a leitura e a troca -- nao substituo"
os.replace(tmp, um); assert h16(open(um, "rb").read()) == ESP["candidato_sha16"]
rec["um_py_novo"] = {"bytes": len(cand), "sha16": ESP["candidato_sha16"], "origem": CAND}
out = os.path.join(HERE, "APLICADO_AO_CANONICO_%s.json" % ts); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1)); os.replace(out + ".tmp", out)
print(json.dumps({"ts": ts, "um_py_novo": rec["um_py_novo"], "n_backups": len(rec["backups"]), "modulos_novos": _N}, ensure_ascii=False))
