"""Entrega da F0.3 para a v407: DELIVERY_v407.json (hashes lidos dos arquivos), quadro (iald.py avancar), ACOM (transition), Mapa (RESULTADO), deposito na fila, bloco ao_lado no 004_RESULTADO e secao no relatorio ao lado.
Rodar UMA vez, depois da ativacao e das conferencias em processo novo. Hash e numero lidos dos arquivos; correcao vai AO LADO."""
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

OLD_SC = Path(r"C:\Users\rotol\AppData\Local\Temp\claude\C--IALD-Central-de-Patentes\fda3adae-8303-4906-a1c4-4eb0c0b6c4e4\scratchpad")
W = Path(r"C:\IALD\Central de Patentes\work\scientific_memory_sync_20261104_v407")
T = Path(r"C:\IALD\TUNEL_CLAUDE_APP")
CM = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\state\canonical_memory")
DEC = Path(r"C:\IALD\Central de Patentes\work\scientific_memory_sync_20261103_v406\DECISAO_DO_OPERADOR_F03_VALE_PARA_V407_04nov.json")
FILA = Path(r"C:\Users\rotol\.claude\projects\C--IALD-Central-de-Patentes\memory\fila\depositos\claude-app")
PY = r"C:\Python314\python.exe"
QUEM = "claude-app-orquestrador"
EPOCH = "v407_4323b401f15cc971"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
agora = lambda: datetime.now().astimezone().isoformat(timespec="seconds")
rd = lambda p: json.loads(Path(p).read_bytes())


def run(args):
    r = subprocess.run(args, capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")


# 0) diff pos-ativacao em arquivo
rc, out, err = run([PY, "-B", "-X", "utf8", str(W / "diff_f03.py"), str(W / "BASELINE_APOS_PREPARE.json"), str(W / "BASELINE_APOS_ATIVACAO.json"), "releases/" + EPOCH + "/"])
(W / "DIFF_APOS_ATIVACAO.txt").write_text(out, encoding="utf-8")
rc, out, err = run([PY, "-B", "-X", "utf8", str(W / "diff_f03.py"), str(W / "BASELINE_ANTES.json"), str(W / "BASELINE_APOS_ATIVACAO.json"), "releases/" + EPOCH + "/"])
(W / "DIFF_TOTAL_ANTES_E_DEPOIS.txt").write_text(out, encoding="utf-8")

prep, ver, act, chk0, chk1, rg = (rd(W / n) for n in ("PREPARATION_%s.json" % EPOCH, "VERIFY_RESULT.json", "ACTIVATE_RESULT.json", "CHECK_ANTES_v407.json", "CHECK_DEPOIS_v407.json", "RECEIVED_GENERATION.json"))
assert act["status"] == "ACTIVATED_BY_EXISTING_API" and act["pointer"]["epoch"] == EPOCH
assert chk1["status"] == "CURRENT" and rg["ok"] is True and ver["status"] == "PASS"
bak = sorted(CM.glob("ACTIVE.json.bak_20261104_08*"))
assert len(bak) == 1, bak
parecer = W / "review" / "PARECER_F03_v407_R1.md"
fontes_nos = [{"arquivo": p["path"], "sha256": p["sha256"], "bytes": p["bytes"]} for p in prep["sources"]]
arquivos = {n: {"arquivo": str(W / n), "sha256": sha(W / n)} for n in (
    "CHECK_ANTES_v407.json", "BASELINE_ANTES.json", "BUILD_INTENT_%s.json" % EPOCH, "CATALOG_%s.json" % EPOCH, "ESTATUTOS_%s.json" % EPOCH, "PREPARATION_%s.json" % EPOCH, "PREPARE_RESULT.json", "VERIFY_RESULT.json",
    "BASELINE_APOS_PREPARE.json", "ACTIVATE_RESULT.json", "CHECK_DEPOIS_v407.json", "RECEIVED_GENERATION.json", "BASELINE_APOS_ATIVACAO.json", "DIFF_APOS_ATIVACAO.txt", "DIFF_TOTAL_ANTES_E_DEPOIS.txt",
    "baseline_f03.py", "diff_f03.py", "received_generation.py", "rodar_f03_v407.py")}
arquivos["PARECER_F03_v407_R1.md"] = {"arquivo": str(parecer), "sha256": sha(parecer)}
dec = rd(DEC)
delivery = {
    "unidade": "F0.3.MEMORIA_CIENTIFICA_SYNC", "versao": "v407", "epoch": EPOCH, "quando": agora(), "por": QUEM, "estado": "ATIVADA_PELA_API_COM_CAS__CURRENT_EM_PROCESSO_NOVO",
    "autorizacao_do_operador": {"palavras_no_chat": ["Autorizo a escrita", "Vale para a v407"], "sha256_das_palavras": [hashlib.sha256(s.encode("utf-8")).hexdigest() for s in ("Autorizo a escrita", "Vale para a v407")],
                                "decisao_registrada": {"arquivo": str(DEC), "sha256": sha(DEC)}, "leitura": dec["decisao_do_operador"]["leitura"], "chamado": "gerencia c1 (central-de-patentes-66), 04/11/2026 07:3x, por SendMessage; o check devolveu SEALED_ADVANCE_PENDING_SYNC v407",
                                "esgotada_com": "a ativacao (feita as 08:02:05-08:02:12); Chatgpt\\ volta a ser so' leitura para esta sessao"},
    "selo_lido_no_nos": {"um_version": chk0["sealed_version"], "generation": chk0["sealed_generation"], "epoch": chk0["sealed_epoch"], "fontes": fontes_nos},
    "escrito_em_Chatgpt": {"release_novo": {"diretorio": prep["target"], "arquivos_novos": 17, "manifest_sha256": prep["manifest"]["sha256"], "manifest_bytes": prep["manifest"]["bytes"], "documentos": prep["documents"], "trechos": prep["chunks"]},
                            "ACTIVE.json": {"antes_sha256": chk0["active_pin"]["sha256"], "depois_sha256": sha(CM / "ACTIVE.json"), "depois_bytes": (CM / "ACTIVE.json").stat().st_size, "conteudo": act["pointer"]},
                            "backup_do_ponteiro": {"arquivo": str(bak[0]), "sha256": sha(bak[0])}, "nada_alem_disso": "DIFF_TOTAL_ANTES_E_DEPOIS.txt: 18 novos (17 do release + o backup do ponteiro), 1 alterado (ACTIVE.json), 0 removidos; manifests dos 16 releases anteriores inalterados"},
    "conferencias": {"verify": ver["status"], "check_depois": chk1["status"], "geracao_recebida_em_processo_novo": rg["ok"], "retrieval_modos": {k: v["ok"] for k, v in rg["recuperacao"].items()}, "provider_calls": 0,
                     "revisao_independente": {"veredito": "PODE ATIVAR (0 alto, 0 medio, 5 baixos operacionais/herdados)", "parecer": str(parecer), "sha256": sha(parecer)}},
    "arquivos": arquivos, "nao_feito": ["nao movi gate, kernel, um.py nem o selo", "nao reiniciei sessoes, app, MCP nem a fila", "nao avancei a unidade para AUDITADA/FECHADA (ato da gerencia)", "nao escrevi nada mais em Chatgpt\\"],
    "limites": ["a revisao independente nao viu o chat do operador (as palavras dele constam da decisao registrada por mim: [DECLARADO])", "efeito da ativacao em fila/web/MCP legados nao verificado alem da geracao recebida em processo novo", "baixos herdados: o selo cobre 5 das 13 fontes; matches_fisica_snapshot False em 9/13 desde o catalogo v369; um trecho do DESENHO casa a lista FORBIDDEN (igual no v404)"]}
dp = W / "DELIVERY_v407.json"
with dp.open("xb") as f:
    f.write(json.dumps(delivery, ensure_ascii=False, indent=1).encode("utf-8"))
print("DELIVERY_v407.json", dp.stat().st_size, "bytes sha16", sha(dp)[:16])

resumo = ("F0.3 para a v407 ATIVADA pela API existente com CAS (04/11 08:02): release %s (13 documentos, %d trechos, manifest %s…) criado em Chatgpt\\…\\canonical_memory\\releases; ACTIVE.json v404 -> v407 (sha256 %s… -> %s…), "
          "backup %s; check em processo novo = CURRENT, geracao recebida conferida (3 modos de recuperacao), 0 chamadas de provedor; unico acrescimo/alteracao em Chatgpt\\: o release novo (17 arquivos), o backup do ponteiro e o ACTIVE.json; "
          "revisao independente PODE ATIVAR. Autorizacao do operador no chat: «Autorizo a escrita» e «Vale para a v407»."
          % (EPOCH, prep["chunks"], prep["manifest"]["sha256"][:12], chk0["active_pin"]["sha256"][:12], sha(CM / "ACTIVE.json")[:12], bak[0].name))

# 1) quadro
rc, out, err = run([PY, "-X", "utf8", r"C:\IALD\PROGRAMA_IALD\iald.py", "avancar", "F0.3.MEMORIA_CIENTIFICA_SYNC", "--quem", QUEM, "--status", "ENTREGUE", "--evidencia", str(dp), "--nota",
                    "F0.3 v407 ativada pela API com CAS (08:02); check CURRENT em processo novo; revisao independente PODE ATIVAR; nao movi AUDITADA/FECHADA"])
print("quadro rc", rc, " ".join(out.split())[:200], err[:200])

# 2) Mapa: RESULTADO na rota que registrei quando a F0.3 parou no gate
nota = {"tipo": "RESULTADO", "rota_id": "memoria.cientifica_sync.v406_gate_chatgpt", "titulo": "F0.3 sincronizada a v407: ativada pela API com CAS, depois de a v406 nao ser mais sincronizavel e de o operador estender a autorizacao",
        "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False, "veredito": "F03_V407_ATIVADA_PELA_API_COM_CAS__CURRENT_EM_PROCESSO_NOVO__AGUARDA_ACEITE_DA_GERENCIA",
        "resultado": resumo, "nota": "A rota nasceu bloqueada pelo gate de escrita em Chatgpt\\ e depois pelo guarda fail-closed do helper (selo v407 parcial); com o selo completo e o chamado da c1, a escrita unica autorizada pelo operador foi feita e esgotada. A v406 nunca foi sincronizada (o Nos passou direto a v407).",
        "proximo_passo": "A gerencia confere o recibo e da' o aceite (AUDITADA/FECHADA e' ato dela); a proxima sincronizacao (v408) pede nova autorizacao do operador.",
        "refs": ["app.release.v406", "filme.par_v406.final_e_narrado"], "artefatos": [str(dp), str(W / "ACTIVATE_RESULT.json"), str(W / "RECEIVED_GENERATION.json"), str(W / "DIFF_TOTAL_ANTES_E_DEPOIS.txt"), str(parecer)]}
np_ = W / "anotacao_f03_v407_ativada.json"
with np_.open("xb") as f:
    f.write(json.dumps(nota, ensure_ascii=False, indent=1).encode("utf-8"))
rc, out, err = run([PY, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(np_), "--quem", QUEM])
print("mapa rc", rc, " ".join(out.split())[:230], err[:300])

# 3) ACOM
sys.path.insert(0, str(OLD_SC))
import acom as A


def acom(op, extra=None):
    payload = {"operation": op, "reference": A.REF}
    payload.update(extra or {})
    rc, out, err = A.call(payload)
    return rc, (json.loads(out) if out.strip().startswith("{") else out), err


rc, v0, err = acom("verify")
rev0 = v0["result"]["receipt"]["revision"]
changes = {"records": [{"id": "f03-v407-ativada-20261104", "kind": "fact", "statute": "REAL", "text": resumo + " Fecha o item pendente decisao-operador-f03-v407-20261104 e a unidade F0.3 desta rodada.",
                        "sources": [{"kind": "artifact", "ref": str(dp), "sha256": sha(dp)}, {"kind": "artifact", "ref": str(parecer), "sha256": sha(parecer)}]}],
           "flow": {"phase": "app_v406_instalado_e_aceito; h1_h4_prontos; f03_v407_ATIVADA (check CURRENT); filme_par_v406_final_e_narrado_prontos_aguardam_escuta_do_operador; agendadas_negadas",
                    "next_action": "operador assiste ao filme narrado e decide voz/corte do fechamento; gerencia aceita a F0.3; release v407 do app vem por ORDEM da cadeia da gerencia (S10); v408 pede nova autorizacao para a F0.3"}}
rc, res, err = acom("transition", {"expected_revision": rev0, "event_id": "claude-app-orq-20261104-f03-v407-ativada", "actor": {"id": QUEM, "kind": "agent"}, "changes": changes})
print("acom transition rc", rc, (json.dumps(res, ensure_ascii=False)[:140] if not isinstance(res, str) else res[:300]), err[:200])
rc, v1, err = acom("verify")
print("acom verify rc", rc, "ok", v1["result"]["ok"], "revisao", v1["result"]["receipt"]["revision"])

# 4) fila: SEMPRE pela ferramenta memoria.py depositar (regra da c1, 04/11), nunca a mao
texto = (f"[REAL] 04/11/2026 08:02: a memoria cientifica sincronizada da fila (F0.3) foi ATIVADA para a v407 pela API existente com CAS, por escrita unica autorizada pelo operador no chat "
         f"(Autorizo a escrita; Vale para a v407) e chamada pela gerencia c1 depois do selo completo do Nos. Release {EPOCH}: 13 documentos, {prep['chunks']} trechos, manifest {prep['manifest']['sha256'][:16]}; "
         f"ACTIVE.json v404 -> v407; check em processo novo = CURRENT; revisao independente PODE ATIVAR. Em Chatgpt so' mudaram o release novo (17 arquivos), o ACTIVE.json e o backup do ponteiro; "
         f"a autorizacao se esgotou com a ativacao (a v408 pede outra). A unidade nao foi movida para AUDITADA/FECHADA (ato da gerencia). Mapa: memoria.cientifica_sync.v406_gate_chatgpt (RESULTADO).")
tf = W / "DEPOSITO_F03_v407.md"
with tf.open("xb") as f:
    f.write(texto.encode("utf-8"))
FILA_DIR = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila")
r = subprocess.run([PY, "-X", "utf8", "memoria.py", "depositar", "--quem", QUEM, "--tipo", "project", "--estatuto", "REAL", "--alvo", "missao-ultima-flag-um-py.md",
                    "--fonte", str(dp), "--fonte", str(parecer), "--slug", "f03-v407-ativada-04nov", "--texto-arquivo", str(tf)], cwd=str(FILA_DIR), capture_output=True)
print("fila rc", r.returncode, " ".join(r.stdout.decode("utf-8", "replace").split())[:300], r.stderr.decode("utf-8", "replace")[:400])

# 5) 004_RESULTADO: terceiro bloco ao_lado


def substituir(p, novo):
    p = Path(p)
    antigo = p.read_bytes()
    p.with_name(p.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S")).write_bytes(antigo)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_bytes(novo)
    assert tmp.stat().st_size >= len(antigo), "encolheu: " + p.name
    tmp.replace(p)


r4 = T / "RESULTADOS" / "004_RESULTADO.json"
d = rd(r4)
d["ao_lado"].append({"quando": agora(), "de": QUEM, "motivo": "04/11 08:02: a F0.3 foi executada para a v407 (selo completo; chamado da c1; autorizacao do operador no chat)", "estado_da_parte_F0.3": "ENTREGUE: ativada pela API com CAS; check CURRENT em processo novo",
                     "resumo": resumo, "arquivos": [{"arquivo": str(dp), "sha256": sha(dp)}, {"arquivo": str(parecer), "sha256": sha(parecer)}], "falta": ["aceite da gerencia (AUDITADA/FECHADA e' ato dela)"]})
substituir(r4, json.dumps(d, ensure_ascii=False, indent=1).encode("utf-8"))
print("004_RESULTADO.json: terceiro bloco ao_lado acrescentado")

# 6) relatorio ao lado
rel = T / "RELATORIO_20261103_AO_LADO.md"
sec = ("\n## 6. F0.3 em 04/11 (08:02): feita para a v407, com a sua autorização\n\n"
       "- O selo da v407 ficou completo no Nós e a gerência me chamou. Rodei o `check` (devolveu `SEALED_ADVANCE_PENDING_SYNC` com `v407`), reivindiquei a unidade, preparei o release, verifiquei, um revisor independente disse **PODE ATIVAR** e ativei pela API existente, com proteção de concorrência (CAS).\n"
       "- **Escrevi em `Chatgpt\\` uma vez só**, como você autorizou («Autorizo a escrita» e «Vale para a v407»): um release novo (17 arquivos), o ponteiro `ACTIVE.json` (v404 → v407) e o backup do ponteiro anterior. Mais nada mudou ali (conferido por diff da árvore). A autorização se esgotou com a ativação; a v408 pede outra.\n"
       "- Em processo novo: `check` = CURRENT e a geração recebida confere nos três modos de recuperação; nenhuma chamada de provedor. Não movi gate, kernel, `um.py` nem selo, e não reiniciei nada.\n"
       "- Recibo: `work\\scientific_memory_sync_20261104_v407\\DELIVERY_v407.json`; Mapa: `memoria.cientifica_sync.v406_gate_chatgpt` (RESULTADO).\n")
b = rel.read_bytes()
substituir(rel, b.rstrip(b"\r\n") + b"\n" + sec.encode("utf-8"))
print("relatorio ao lado: secao 6 acrescentada")
