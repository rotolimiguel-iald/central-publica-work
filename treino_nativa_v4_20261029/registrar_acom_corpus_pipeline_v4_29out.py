# -*- coding: utf-8 -*-
"""ACOM: etapa material — pipeline v4 escrito e revisado pela gerencia; corpus v4 construido e medido (34,8 M tokens = 165 h); decisao de empacotar/system curto/patamares."""
import hashlib, json, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
C = Path("C:/IALD/Central de Patentes"); T = Path("C:/IALD/TGL_IALD_NATIVE_QWEN5090")
PY = r"C:\Python314\python.exe"; sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
REF = str(C / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json")
def sm(p):
    q = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return q.returncode, (json.loads(q.stdout) if q.stdout.strip().startswith("{") else {"raw": (q.stdout + q.stderr)[:400]})
rc, g = sm({"operation": "get", "reference": REF}); rev = (g.get("result") or {}).get("revision"); assert rev is not None, g
S = lambda p: {"kind": "artifact", "ref": str(p) + "#sha256:" + sha(p)}
srcs = [S(T / "11_scripts/run_total_v4.py"), S(T / "11_scripts/02_train_lora_v4.py"), S(T / "11_scripts/01_build_dataset_v4.py"), S(T / "10_reports/PROTOCOLO_PADRAO_DE_TREINO_IALD_NATIVA.md"), S(T / "03_dataset/v4/BLOCOS_v4.json")]
texto = ("%s: ETAPA MATERIAL — (1) pipeline v4 escrito (Sonnet) e REVISADO pela gerencia: GPU exclusiva por tarefa, retomada pelo ultimo checkpoint integro (caminho explicito), espelho assincrono em D:, SAFE_TO_TRAIN_v4 conferido contra o sha256 do corpus, tarefa de retomada so apos a fumaca, bake mk5 sem teclado (block_count lido do GGUF, journal), portao de release por significado com reversao para a v3, registro sem default antes do portao; eval HTTP com 9 perguntas fixas (6 nucleo + 2 bancada + 1 memoria em camadas); protocolo padrao escrito (secoes 0-9). "
         "(2) corpus v4 construido (Sonnet; determinístico; 1.540 fontes com sha256; nenhuma linha acima de ctx 2048): 41.459 linhas, 34,76 M tokens = 165 h a 17,1 ms/token — INVIAVEL; causa medida: 28.286 cartoes B2 repetindo o system de 379 tokens (12,0 M de prompt para 4,4 M de completion); blocos K (Bancada Um, 0,28 M) e L (memoria em camadas, 0,37 M) dentro dos tetos. "
         "(3) DECISAO: empacotar os cartoes pequenos por modulo (completion <= 1.500 tokens por lote), system de treino curto a partir de 'identity:' do reflect kernel (400 chars, ~150 tokens) identico no construtor/treinador/portao/eval por sha256, e tres patamares pre-registrados pelo ms/token da fumaca (t1 A,A2,B2,C,E,E2,F,G,H,K,L; t2 +B; t3 +C2,F2; regra ms<=10 t3, <=13 t2, senao t1); estimativa t1 ~15,6 M tokens (~74 h a 17,1 ms; ~52 h a 12 ms). "
         "ACHADOS COLATERAIS: TGL_ATLAS.md com duplicacao massiva de verbetes e secoes (a medir e tratar a parte); /api/gw/resultados da Bancada devolve HTTP 422 NONFINITE_OR_INVALID_OUTPUT. Nenhum passo de GPU rodou; demo v3 no ar. Estacao: auto-logon ativo; sem UPS; Windows Update com horas ativas 0-17 (pode reiniciar a noite: pausar e ato do operador)." % time.strftime("%d/%m/%Y %H:%M"))
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-treino-v4-pipeline-revisado-corpus-medido-29out",
            "changes": {"records": [{"id": "c1-treino-v4-pipeline-e-corpus-29out", "kind": "fact", "statute": "REAL", "sources": srcs, "text": texto}],
                        "flow": {"phase": "v404_COMPLETA__treino_nativa_v4__pipeline_revisado__corpus_em_reempacotamento__fumaca_pendente",
                                 "next_action": "agentes refazem corpus (empacotado, system curto, t1/t2/t3) e orquestrador (hash do system, escolha do patamar); gerencia confere hashes; fumaca com GPU exclusiva (demo offline); SAFE; supervisor + tarefa; treino; downstream automatico. Operador: pausar Windows Update; fechar apps na GPU; decisao do conjunto D (c/b/a); WIPO 2FA + e-mail ACOM [LEGAL]; E0; Zenodo."}}})
print("acom rc", rc, "revision", (t.get("result") or {}).get("revision"), t.get("message", "") or t.get("raw", ""))
