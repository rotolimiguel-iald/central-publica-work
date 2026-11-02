# -*- coding: utf-8 -*-
"""Etapa material: fumaca v4 APROVADA (5a tentativa) e treino longo LANCADO sob o supervisor v4 (22:36). ACOM + Mapa RESULTADO + quadro."""
import hashlib, json, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
C = Path("C:/IALD/Central de Patentes"); T = Path("C:/IALD/TGL_IALD_NATIVE_QWEN5090"); W = C / "work/treino_nativa_v4_20261029"
PY = r"C:\Python314\python.exe"; sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
SAFE = T / "12_logs/SAFE_TO_TRAIN_v4.json"; SMOKE = T / "12_logs/SMOKE_TRAIN_v4.json"; MAN = T / "03_dataset/v4/MANIFEST_v4.json"; PROTO = T / "10_reports/PROTOCOLO_PADRAO_DE_TREINO_IALD_NATIVA.md"
sf = json.load(open(SAFE, encoding="utf-8")); sm_ = json.load(open(SMOKE, encoding="utf-8"))
assert sf["aprovado"] is True and sf["tier"] == "t2"
horas = sf["train_tokens"] * sf["ms_por_token"] / 3.6e6
resumo = ("fumaca APROVADA 22:34 (5a tentativa; as 4 anteriores reprovaram por telemetria, nao por GPU): rota padrao 17,8 ms/token, rota rapida dos experts 12,2 ms/token ADOTADA (<= 0,8x); pico do processo 6,86 GiB (cap 20); nvlddmkm 0; CSV da rodada 13.517 MiB; retomada do checkpoint-4 provada nas duas rotas; "
          "patamar t2 pela regra pre-registrada (10 < 12,2 <= 13): train_v4_t2.jsonl sha256 %s, 15.157 linhas, 20,17 M tokens, %.1f h previstas + ~1,5 h de avaliacoes (6 x 333 amostras); system sha256 %s. "
          "Treino longo LANCADO 22:36 sob supervisor_v4.ps1 (pid 69708; desacoplado da sessao); etapas seguintes automaticas: tarefa de retomada -> treino -> merge/F16 em D: -> bake mk5 -> Q4 -> registro -> portao por significado -> eval HTTP. Demo :8081 fora do ar ate o fim." % (sf["train_sha256"][:16], horas, sf["system_sha256"][:16]))
# --- ACOM
REF = str(C / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json")
def smem(p):
    q = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return q.returncode, (json.loads(q.stdout) if q.stdout.strip().startswith("{") else {"raw": (q.stdout + q.stderr)[:400]})
rc, g = smem({"operation": "get", "reference": REF}); rev = (g.get("result") or {}).get("revision"); assert rev is not None, g
S = lambda p: {"kind": "artifact", "ref": str(p) + "#sha256:" + sha(p)}
rc, t = smem({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-treino-v4-fumaca-aprovada-treino-lancado-29out",
              "changes": {"records": [{"id": "c1-treino-v4-lancado-29out", "kind": "fact", "statute": "REAL", "sources": [S(SAFE), S(SMOKE), S(MAN), S(PROTO)], "text": time.strftime("%d/%m/%Y %H:%M") + ": " + resumo}],
                          "flow": {"phase": "v404_COMPLETA__treino_nativa_v4_EM_CURSO_t2_68h__demo_offline__downstream_automatico",
                                   "next_action": "nao acordar por progresso: vigias em segundo plano avisam no passo 50 e no desfecho; ao fim: conferir portao de release (SMOKE_HTTP_v4.json), EVAL_HTTP_v4, train_seal_v4; registrar RESULTADO no Mapa, quadro FECHADO, memoria; limpar SMOKE dirs. Operador: pausar Windows Update (horas ativas 0-17); fechar apps na GPU; conjunto D (c/b/a); Atlas duplicado (rota memoria.atlas_duplicacao_de_verbetes_29out); WIPO 2FA + e-mail ACOM [LEGAL]; E0; Zenodo."}}})
print("acom rc", rc, "revision", (t.get("result") or {}).get("revision"), t.get("message", "") or t.get("raw", ""))
# --- Mapa RESULTADO
reg = [{"tipo": "RESULTADO", "rota_id": "infra.treino_iald_nativa_v4_um_py_v404", "dominio": "INFRA",
 "titulo": "29/10 22:34-22:36: FUMACA APROVADA (rota rapida 12,2 ms/token adotada) e TREINO LONGO LANCADO (patamar t2, 20,17 M tokens, ~68 h) sob o supervisor v4, com tarefa de retomada, espelho em D: e downstream automatico",
 "pergunta": "A fumaca aprovou e o treino v4 esta em curso com as salvaguardas?", "dados": [resumo],
 "metodo": "criterios pre-registrados da fumaca (rc 0/0; nvlddmkm 0; CSV <= 24000; loss finita; 5 passos; checkpoint; ms/token <= 48,4; rapida adotada se <= 0,8x); regra de patamar por ms/token efetivo",
 "resultado": "SAFE_TO_TRAIN_v4.json aprovado; supervisor v4 pid 69708; STATE corrida #6; GPU exclusiva desde 22:36",
 "veredito": "TGL_IALD_NATIVE_V4__SMOKE_APPROVED__FAST_EXPERTS_ADOPTED_12P2MS__TIER_T2_20M_TOKENS__TRAINING_LAUNCHED_20261029_2236__DOWNSTREAM_AUTOMATIC",
 "estatuto": "REAL", "status": "EM_CURSO", "olhou_dados": False,
 "defeito": "a demo publica fica fora do ar ~3 dias; o Windows Update com horas ativas 0-17 pode reiniciar a maquina (auto-logon ativo: a tarefa AtLogOn retoma); sem UPS",
 "nao_refazer": "nao relancar a fumaca; nao tocar nos arquivos do treino em curso; nao matar processos por nome; o STATUS e lido, nunca escrito, por fora",
 "proximo_passo": "esperar o desfecho (vigias em segundo plano); ao fim conferir portao/eval e registrar RESULTADO final", "onde": "C:/IALD/TGL_IALD_NATIVE_QWEN5090/12_logs (STATUS_v4, STATE_v4, supervisor_v4.log); D:/IALD/TREINO_NATIVA/v4",
 "artefatos": [str(SAFE), str(SMOKE), str(MAN), str(PROTO)], "refs": [], "nota": "Neural = ilustracao, nao prova. O treino nao move gate, kernel nem selo."}]
pj = W / "rota_mapa_resultado_lancamento_v4_29out.json"; pj.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([sys.executable, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1"], capture_output=True, text=True, encoding="utf-8", errors="replace")
print("mapa", (r.stdout[-120:] + r.stderr[-120:]).strip().replace("\n", " "), "rc", r.returncode)
# --- quadro
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\PROGRAMA_IALD\iald.py", "avancar", "F9.TREINO_NATIVA_V4", "--quem", "claude-c1", "--status", "EM_CURSO", "--evidencia", str(SAFE), "--evidencia", str(SMOKE), "--evidencia", str(PROTO),
                    "--nota", "22:36 treino longo lancado (t2, ~68 h, rota rapida 12,2 ms/token); fumaca aprovada na 5a tentativa (4 reprovacoes de telemetria corrigidas: console, eval reserva, corrida do STATUS, nvidia-smi orfao)"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=r"C:\IALD\PROGRAMA_IALD")
print("quadro", (r.stdout.strip() or r.stderr.strip())[:200])
