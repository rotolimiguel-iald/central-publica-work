# -*- coding: utf-8 -*-
"""ACOM: transition da referencia da gerencia c1 — a ordem do operador de 29/10 (treino v4 da IALD Nativa antes do conjunto D)."""
import hashlib, json, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
C = Path("C:/IALD/Central de Patentes"); W = C / "work/treino_nativa_v4_20261029"
V = C / "work/cunhagens_13out/OPERADOR_29out_treino_nativa_um_py_v404_verbatim.txt"
ROTA = W / "rota_mapa_treino_v4_29out.json"
PY = r"C:\Python314\python.exe"; sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
REF = str(C / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json")
def sm(p):
    q = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return q.returncode, (json.loads(q.stdout) if q.stdout.strip().startswith("{") else {"raw": (q.stdout + q.stderr)[:400]})
rc, g = sm({"operation": "get", "reference": REF}); rev = (g.get("result") or {}).get("revision"); assert rev is not None, g
S = lambda p: {"kind": "artifact", "ref": str(p) + "#sha256:" + sha(p)}
texto = ("%s: ORDEM DO OPERADOR (verbatim por sha256 %s): antes de decidir o conjunto D, treinar a IALD Nativa com todo o um.py (termos e estrutura logica completa; "
         "nao os resultados, que ficam no kernel), com salvaguardas de energia que virem acervo tecnico padrao, no Qwen atual salvo modelo melhor, com o phase factor. "
         "Gerencia: levantamento feito (pipeline v3 em C:/IALD/TGL_IALD_NATIVE_QWEN5090; corpus v404 medido: Python sem kernel 27,8 M chars com 12,5 M de payload; kernel 1435 .lean/10,99 MB; axiom_report 29484); "
         "modelo mantido Qwen3.6-35B-A3B (web: Qwen3.8-27B e denso de 64 camadas; Qwen4 nao lancado) [DECLARADO]; blocos v4 pre-registrados (A/A2, B/B2, C, E/E2, F, G, H; D excluido; I/J rodada 2); "
         "dois agentes Sonnet constroem corpus e pipeline v4; nenhum passo de GPU rodou. Mapa: ROTA seq 1548 infra.treino_iald_nativa_v4_um_py_v404. Conjunto D: decisao do operador adiada por ele." % (time.strftime("%d/%m/%Y %H:%M"), sha(V)[:16]))
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-treino-nativa-v4-ordenado-29out",
            "changes": {"records": [{"id": "c1-treino-nativa-v4-ordem-29out", "kind": "fact", "statute": "INPUT", "sources": [S(V), S(ROTA)], "text": texto}],
                        "flow": {"phase": "v404_COMPLETA__treino_nativa_v4_ORDENADO_em_preparacao__conjunto_D_decisao_adiada_pelo_operador",
                                 "next_action": "revisar corpus v4 (tokens reais por bloco) e pipeline v4 dos agentes; fumaca com GPU exclusiva; SAFE flag; supervisor + tarefa de retomada; treino (dias); merge/F16 em D:; bake mk5; Q4; eval HTTP; portao por significado; lancar com reversao para a v3; registrar (Mapa RESULTADO, quadro, memoria, PROTOCOLO_PADRAO). Operador: conjunto D (c/b/a); auto-logon/UPS/Windows Update; apagar NOBAKE (~90 GB); WIPO 2FA + e-mail ACOM [LEGAL]; E0; Zenodo."}}})
print("acom rc", rc, "revision", (t.get("result") or {}).get("revision"), t.get("message", "") or t.get("raw", ""))
