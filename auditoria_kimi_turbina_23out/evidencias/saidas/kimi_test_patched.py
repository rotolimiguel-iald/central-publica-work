# -*- coding: utf-8 -*-
"""teste_dobra_envelope.py — testes da cirurgia do MODO DOBRADO (membro Kimi, 20/10/2026).

Não toca a casa além de LEITURA; roda contra o código já editado (backup datado ao lado).
Três provas: (1) o caso que bloqueou o correio ao Claude agora passa, dobrado e com
recibo explícito; (2) o caminho normal fica inalterado (folded=False, trechos presentes);
(3) a impossibilidade verdadeira (nem o pedido cabe) continua bloqueando.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

BASE = Path(r"C:\t\orq_copia_kimi")
sys.path.insert(0, str(BASE))

from iald_orchestrator import canonical_memory  # noqa: E402

PROMPT_CLAUDE = Path(r"C:\Users\rotol\Documents\kimi\workspace\estudo_iald_qg\ferramentas\submit_claude_9298f642.json")
prompt_real = json.loads(PROMPT_CLAUDE.read_text(encoding="utf-8"))["prompt"]
PROJECAO_CHARS = 20911  # lido do seq 1291 da espinha
reservado = "P" * PROJECAO_CHARS

resultados = []

# (1) o caso bloqueado: prompt real + reserva de 20.911 chars (modo standard, teto apertado)
try:
    r = canonical_memory.prepare(
        prompt_real, mode="standard", max_chars=12000, prompt_limit=24000,
        reserved_context_chars=len(reservado), reserved_context_bytes=len(reservado.encode()))
    rec = r["receipt"]
    resultados.append({
        "prova": "caso_bloqueado_agora_dobra",
        "passou": bool(rec.get("folded")) and len(r["prompt"]) <= 12000,
        "folded": rec.get("folded"), "fold_layers": rec.get("fold_layers"),
        "trechos": len(rec.get("sources") or []), "context_bytes": rec.get("context_bytes"),
        "aviso_no_pacote": "MODO DOBRADO" in r["prompt"],
    })
except ValueError as e:
    resultados.append({"prova": "caso_bloqueado_agora_dobra", "passou": False, "erro": str(e)})

# (2) caminho normal inalterado: prompt pequeno, sem reserva
try:
    r2 = canonical_memory.prepare("Qual é a forma canônica do Um?", mode="standard",
                                  max_chars=24000, prompt_limit=24000)
    rec2 = r2["receipt"]
    resultados.append({
        "prova": "caminho_normal_inalterado",
        "passou": (rec2.get("folded") is False and len(rec2.get("sources") or []) > 0
                   and "MODO DOBRADO" not in r2["prompt"]),
        "folded": rec2.get("folded"), "trechos": len(rec2.get("sources") or []),
    })
except ValueError as e:
    resultados.append({"prova": "caminho_normal_inalterado", "passou": False, "erro": str(e)})

# (3) impossibilidade verdadeira: nem o pedido cabe — continua bloqueando
try:
    canonical_memory.prepare("x" * 20000, mode="standard", max_chars=12000, prompt_limit=24000,
                             reserved_context_chars=len(reservado),
                             reserved_context_bytes=len(reservado.encode()))
    resultados.append({"prova": "impossibilidade_verdadeira_bloqueia", "passou": False,
                       "erro": "não levantou ValueError"})
except ValueError as e:
    resultados.append({"prova": "impossibilidade_verdadeira_bloqueia", "passou": True,
                       "erro_original_preservado": "não deixa espaço" in str(e)})

ok = all(r["passou"] for r in resultados)
saida = {"testes": resultados, "resultado": "PASS" if ok else "FAIL"}
alvo = Path(r"C:\\IALD\\Central de Patentes\\work\\auditoria_kimi_turbina_23out\\evidencias\\saidas") / "kimi_test_out.json"
alvo.write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(saida, ensure_ascii=False, indent=1))
raise SystemExit(0 if ok else 1)
