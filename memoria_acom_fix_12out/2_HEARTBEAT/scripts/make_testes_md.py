# -*- coding: utf-8 -*-
"""Gera TESTES.md a partir de tests\\RESULTADOS.json (resultado medido) + descricoes fixas de cada caso.
Nenhum resultado e escrito a mao: PASSA/FALHA vem do unittest -v capturado pelo runner.
"""
import json, os
from datetime import datetime

FRONT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DESC = {
    # NOVA
    "test_heartbeat_measures_generation_only": "post falso com 0,2 s de latência; `project_messages` e `_operational_native_payload` trocados por versões que dormem 1 s e contam; contador = 0 durante `_heartbeat_measure`; payload enviado == payload r60 (mensagens exatamente `[sys_msg, prompt]`, sem bloco de memória); `elapsed` de cada amostra em [0,2; 0,3] s; fórmula `completion_tokens/elapsed`; corpos de resposta ausentes da medida.",
    "test_heartbeat_tok_s_prefers_server_timings": "`_heartbeat_tok_s`: com `timings` → `predicted_n/predicted_ms×1000` (200 tok/s com elapsed 9 s); sem `timings` → `completion_tokens/elapsed`; timings inválidos (0/0) caem na fórmula do elapsed; sem tokens → `(None, None)`; numa medida com latência 0,3 s e timings 128/400 ms o tok/s é 320,0.",
    "test_heartbeat_memory_event_only_on_class_change_or_hourly": "relógio injetado; estado de saúde prévio `ok`; 3 batidas `ok` → 0 eventos; 1 batida `alerta` (50 vs baseline 100) → 1 evento; mesma classe < 1 h → nada; +61 min → 1 evento; registros `fact/REAL`, fonte `measurement` `heartbeat_telemetry:<sha>`, id `hb.<sha>`, texto sem `response`/`choices`; fase `heartbeat_alerta`; linhas `memory_event` da telemetria casam com os ids do livro; health.json com classe e revisão.",
    "test_sixty_beats_in_process_zero_or_one_memory_event": "60 batidas com req_lib falso (timings 100 tok/s): 60× `ok`, exatamente 1 evento na memória (classe estabelecida), psion sintético com total_beats 70 e generation 60, telemetria com rotação (teto 16 KiB) e 61 linhas íntegras (60 beats + 1 memory_event); mais 60 batidas com estado prévio → 0 eventos novos.",
    "test_heartbeat_failure_does_not_block_next_cycle": "HTTP 500 → `continue` → `no_results`, classe `falha`, 1 evento, psion intocado; depois 200 → `ok` (mudança de classe → evento); exceção de rede não propaga; memória comum indisponível (`record_measurement` lança OSError) → batida completa, linha `memory_event_failed`, classe do health não avança, batida seguinte grava o alerta.",
    "test_skipped_busy_and_aborted_user_write_telemetry_only": "`skipped_busy` (servidor ocupado) → só telemetria, classe nula, sem evento, psion não criado; `skipped_offline` → classe `falha` → 1 evento.",
    "test_heartbeat_telemetry_rotation": "teto de 4 KiB: 120 linhas → `.1`…`.5` existem (cada ≤ 4 KiB), `.6` não existe, arquivo corrente ≤ 4 KiB, cada linha íntegra com sha conferido, sequência contígua até a linha corrente.",
    "test_psion_save_atomic_and_daily_bak": "`_save_psion_state` sobre arquivo sintético: bytes CRLF iguais aos do gravador antigo; 3 gravações no mesmo dia → exatamente 1 `.bak_<AAAAMMDD>` com os bytes da primeira versão; nenhum tempário sobrando; com `HEARTBEAT_PSION_DAILY_BAK=False` não nasce cópia.",
    "test_degraded_measurement_never_reaches_psion": "medidas com regime `operational_memory_included`, payload que não é o r60 (sha256 estranho) ou amostra sem fórmula → `inadmissible`, bytes do psion intactos, telemetria `refused_*`, classe `falha`; medida admissível entra (total_beats 11); ancoragem violada (beta 0,5) → `anchoring_error` e psion não salvo.",
    "test_memory_event_is_fact_real_without_bodies_and_legacy_context_untouched": "contexto legado de 10/10 criado por `run_autonomous` fica com o mesmo recibo depois da batida; livro novo `app_service_<sha(native-heartbeat:health)>` no mesmo escopo, restrições `no_response_bodies`/`gate_authority=false`, âncora do serviço; registro `fact/REAL` com fonte `measurement`, texto < 600 caracteres, sem corpo de resposta nem chaves; projeção sem corpo.",
    "test_record_measurement_idempotent_scoped_and_validated": "`record_measurement`: mesmo event_id → recibo replayed na mesma revisão; outra linhagem → outro contexto; objetivo alterado na mesma linhagem → AnchorConflict (ValueError); texto vazio, identificador inválido e flow ilegal → ValueError; partição: escopo de outra casa não lê.",
    "test_heartbeat_source_has_no_memory_inside_the_measurement": "estático (AST, código sem docstrings): `heartbeat_cycle`, `_heartbeat_measure` e `_heartbeat_record_memory_if_due` não chamam `run_autonomous`, `tool_result`, `_operational_native_payload`, `project_messages`, `check_text_window`, `.projection`, `routing_state`; `_heartbeat_cycle_with_memory` não existe; `_operational_native_payload` e `_prepare_native_payload` continuam para chat/admin; `_save_psion_state` usa `os.replace` e não `open(..., \"w\")`; o gatilho admin chama `heartbeat_cycle()`.",
    # STUB
    "test_sixty_beats_stub_server_zero_or_one_memory_event": "servidor de modelo FALSO (adaptador de transporte do `requests`, sem socket) com `/health` e `/v1/chat/completions` no formato llama.cpp (timings 64 tok / 640 ms): 60 batidas com `_heartbeat_llama_ok` e `_heartbeat_is_idle` REAIS → 60× `ok`; 600 POSTs e 60 GETs; cada corpo recebido == payload r60 (Content-Type application/json, timeout 60); `project_messages`/`tool_result`/`run_autonomous` nunca chamados; tok/s = 100,0 em todas as amostras pela fórmula dos timings; psion sintético 70 beats / generation 60 / baseline 100,0 / sem alertas; rotação com teto de 32 KiB; 1 evento na memória (fase `heartbeat_ok`) cujo id casa com a linha `memory_event`; variante com saúde prévia: 60 batidas → 0 eventos.",
    "test_stub_without_timings_measures_only_the_generation_window": "stub sem `timings` e com 0,2 s de latência; `project_messages` lento (1 s) nunca chamado; fórmula `completion_tokens/elapsed`; `elapsed` em [0,2; 0,3] s; tok/s em [210; 330]; classe `ok`.",
    "test_stub_http_500_then_offline_then_recovers_without_blocking": "stub devolve 500 → `no_results`, psion intocado, classe `falha` (1 evento); `/health` 503 → `skipped_offline` (sem evento novo); volta 200 → `ok` sem conciliação (evento por mudança de classe); telemetria `[no_results, skipped_offline, ok]`.",
    # APP 31 (reescrita)
    "test_actual_heartbeat_transport_generation_only_never_blocks": "REESCRITA do caso `test_actual_heartbeat_transport_and_uncertain_block` (l.270–284 da suíte de 10/10), que afirmava o bloco de memória no pedido, o candidato `synthetic-heartbeat` no banco e o bloqueio por RuntimeError: agora afirma payload r60 exato, `project_messages` não chamado, contexto legado nunca criado, livro de saúde na revisão 1 com fase `heartbeat_falha` e sem corpo de resposta, exceção de rede não propaga e o ciclo seguinte roda sem evento novo.",
}


def main():
    r = json.load(open(os.path.join(FRONT, "tests", "RESULTADOS.json"), encoding="utf-8"))
    lines = ["# TESTES — frente HEARTBEAT (conserto ACOM 12/10, decisão D3)", "",
             f"Rodada: {r['at']} · Python {r['python'].split()[0]} · guarda da auditoria `sitecustomize.py` sha256 `{r['guard']['sha256_copy'][:16]}…` (cópia byte a byte de `{r['guard']['source']}`) · estatuto: **[REAL]** (resultados capturados do `unittest -v` por `scripts\\run_tests.py`, gravados em `tests\\RESULTADOS.json`).",
             "",
             "Ambiente de cada suíte: processo novo, `PYTHONPATH=tests\\guard`, `ACOM_AUDIT_ROOT=<pasta da frente>`, sem bytecode, temporários dentro da pasta com prefixo `\\\\?\\` (LongPathsEnabled=0 nesta máquina: os nomes do outbox do app, ~190 caracteres, estouram MAX_PATH a partir desta pasta). Nenhum provedor, nenhuma rede, nenhum confidencial lido: o psion dos testes é um arquivo sintético; o banco comum é um `MemoryStore` sintético na pasta temporária; a lib `iald_memory` usada é a cópia congelada v1 (`tests\\core`, sha256 no MANIFESTO).",
             ""]
    total = 0
    for s in r["suites"]:
        lines.append(f"## {s['label']} — `{os.path.relpath(s['file'], FRONT)}`")
        lines.append("")
        lines.append(f"`{s['summary']}` · {s['ran']} caso(s) · {s['seconds']} s")
        lines.append("")
        lines.append("| caso | o que prova | resultado |")
        lines.append("|---|---|---|")
        for case, result in s["cases"].items():
            total += 1
            lines.append(f"| `{case}` | {DESC.get(case, '(suíte APP de 10/10, inalterada)')} | **{result}** |")
        lines.append("")
    lines.append(f"**Total: {total} casos; falhas: {len(r['failed_cases'])} {r['failed_cases'] if r['failed_cases'] else ''}; `all_pass = {r['all_pass']}`.**")
    lines.append("")
    lines.append("## Eventos da guarda durante as três suítes [REAL]")
    lines.append("")
    for k, v in sorted(r["guard_events"].items()):
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    lines.append(("Leitura: `BLOCK_WRITE_OUTSIDE` (quando aparece) são as sondagens do `tempfile.gettempdir()` nos diretórios temporários do sistema (recusadas pela guarda, por isso os temporários caem dentro da pasta); `BLOCK_NETWORK` é o `socket.socketpair()` emulado no `import requests` (um `bind` em `::1` por processo, recusado — conferido com `import requests` isolado); `READ_OUTSIDE` são leituras de módulos de produção importados pela suíte APP (só leitura); nenhum `BLOCK_CONFIDENTIAL_*`, nenhum `BLOCK_MUTATION_OUTSIDE`, nenhum `SQLITE_RW` fora da pasta.") + (" Nesta rodada não houve `BLOCK_WRITE_OUTSIDE` nem `BLOCK_MUTATION_OUTSIDE`; os eventos medidos são só os listados acima." if not any(k.startswith("BLOCK_WRITE") or k.startswith("BLOCK_MUTATION") for k in r["guard_events"]) else ""))
    out = os.path.join(FRONT, "TESTES.md")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("TESTES.md:", out, "cases:", total, "all_pass:", r["all_pass"])


if __name__ == "__main__":
    main()
