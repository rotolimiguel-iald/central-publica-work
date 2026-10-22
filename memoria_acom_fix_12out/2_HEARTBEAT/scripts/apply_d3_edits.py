# -*- coding: utf-8 -*-
"""Aplica as edicoes D3 nas COPIAS (copia\\projetos_pyhton\\IALD\\*.py), preservando CRLF.

Cada ancora tem de aparecer exatamente UMA vez no texto (fail-closed). O arquivo e lido em bytes,
normalizado para \\n so em memoria, editado, devolvido a \\r\\n e conferido (zero LF solto, mesmo BOM).
Nada em producao e tocado.
"""
import hashlib, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPIA = os.path.join(ROOT, "copia", "projetos_pyhton", "IALD")
WEB = os.path.join(COPIA, "iald_web_server.py")
MEM = os.path.join(COPIA, "iald_app_memory.py")


def load(path):
    raw = open(path, "rb").read()
    assert not raw.startswith(b"\xef\xbb\xbf"), "BOM inesperado"
    text = raw.decode("utf-8")
    crlf = text.count("\r\n")
    assert crlf == text.count("\n"), "arquivo nao e CRLF puro"
    return text.replace("\r\n", "\n")


def save(path, text):
    assert "\r" not in text
    raw = text.replace("\n", "\r\n").encode("utf-8")
    tmp = path + ".tmp_edit"
    with open(tmp, "wb") as out:
        out.write(raw); out.flush(); os.fsync(out.fileno())
    assert open(tmp, "rb").read() == raw
    os.replace(tmp, path)
    back = raw.decode("utf-8")
    assert back.count("\r\n") == back.count("\n"), "CRLF nao preservado"
    return hashlib.sha256(raw).hexdigest()


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"ancora '{label}' aparece {n} vez(es); esperado 1")
    return text.replace(old, new)


# ─────────────────────────────────────────────────────────────────────────────
# iald_web_server.py — so o trecho do heartbeat
# ─────────────────────────────────────────────────────────────────────────────

HEADER_OLD = "# β_TGL = α × √e — Zero free parameters.\n# ══════════════════════════════════════════════════════════════\n\n# ── TGL Constants (computed, NEVER hardcoded) ──\n"
HEADER_NEW = """# β_TGL = α × √e — Zero free parameters.
#
# 12/10/2026 — D3 do conserto da memória comum (ordem do operador «resolva a questão da
# memória», sha16 78ef70e6f9868281). A amarração de 10/10 (run_autonomous + projeção da
# memória comum dentro de t0..elapsed + dez tool_result por batida com o corpo das respostas)
# mudou a régua da medida (mediana 88,8 → 14,5 tok/s, logs r60/r61) e alimentou o psion com
# medidas degradadas. Agora: a medida é SÓ de geração (payload idêntico ao r60); o psion só
# recebe medida admissível e é salvo de forma atômica; a telemetria por batida vai para um
# arquivo próprio rotativo; a memória comum recebe no máximo um evento por mudança de classe
# ou por hora; nunca mais run_autonomous nem tool_result no heartbeat.
# ══════════════════════════════════════════════════════════════

# ── TGL Constants (computed, NEVER hardcoded) ──
"""

CONST_OLD = "HEARTBEAT_MAX_TOKENS = 256\nHEARTBEAT_RUNS_PER_PROMPT = 2\n"
CONST_NEW = """HEARTBEAT_MAX_TOKENS = 256
HEARTBEAT_RUNS_PER_PROMPT = 2
# 12/10/2026 — D3: medida só de geração, telemetria própria, memória comum por classe/hora.
HEARTBEAT_SYSTEM_MESSAGE = {"role": "system", "content": "You are IALD. Respond concisely."}
HEARTBEAT_MEASUREMENT_REGIME = "generation_only"      # o único regime admissível para o psion
HEARTBEAT_LOG_DIR = os.path.join(SERVE_DIR, "logs")
HEARTBEAT_TELEMETRY_FILE = os.path.join(HEARTBEAT_LOG_DIR, "iald_heartbeat_telemetry.jsonl")
HEARTBEAT_TELEMETRY_MAX_BYTES = 4 * 1024 * 1024       # teto por arquivo; rotação .1 … .KEEP encadeada
HEARTBEAT_TELEMETRY_KEEP = 5
HEARTBEAT_HEALTH_FILE = os.path.join(HEARTBEAT_LOG_DIR, "iald_heartbeat_health.json")
HEARTBEAT_MEMORY_MIN_INTERVAL = 3600                  # s entre eventos na memória comum sem mudança de classe
HEARTBEAT_ALERT_RATIO = 0.8                           # o mesmo critério do alerta do psion (avg < 0,8 × baseline)
HEARTBEAT_MEMORY_IDENTIFIER = "native-heartbeat"
HEARTBEAT_MEMORY_LINEAGE = "health"                   # livro próprio; o contexto legado de 10/10 fica só-leitura
HEARTBEAT_MEMORY_OBJECTIVE = ("Health ledger of the existing local heartbeat: generation-only tok/s measurement, "
                              "recorded only on health-class change or at most hourly; no response bodies, "
                              "no private service state, no scientific gate decisions.")
HEARTBEAT_PSION_DAILY_BAK = True                      # uma cópia de bytes por dia: <psion>.bak_<AAAAMMDD> (D3c)
"""

SAVE_OLD = '''def _save_psion_state(psion):
    """Save Psion state to JSON."""
    with open(HEARTBEAT_STATE_FILE, "w") as f:
        json.dump(psion, f, indent=2, default=str)
'''
SAVE_NEW = '''def _save_psion_state(psion):
    """Save Psion state to JSON — atomically (12/10/2026, D3c).

    Tempário → fsync → conferência → os.replace: uma escrita que falha nunca deixa o estado
    vazio ou pela metade (regra de 22/08/2026: nunca open(P, "w") direto). Na primeira escrita
    do dia os bytes anteriores vão para <arquivo>.bak_<AAAAMMDD> (cópia opaca; o conteúdo não
    é interpretado aqui). Os bytes gravados são os mesmos que o gravador em modo texto produzia.
    """
    raw = json.dumps(psion, indent=2, default=str).replace("\\n", os.linesep).encode("utf-8")
    target = HEARTBEAT_STATE_FILE
    if HEARTBEAT_PSION_DAILY_BAK and os.path.exists(target):
        bak = target + ".bak_" + datetime.now().strftime("%Y%m%d")
        if not os.path.exists(bak):
            with open(target, "rb") as f:
                old = f.read()
            tmp_bak = bak + ".tmp_" + secrets.token_hex(4)
            with open(tmp_bak, "wb") as out:
                out.write(old)
                out.flush()
                os.fsync(out.fileno())
            with open(tmp_bak, "rb") as chk:
                if chk.read() != old:
                    os.remove(tmp_bak)
                    raise OSError("Psion daily byte copy did not verify")
            os.replace(tmp_bak, bak)
    tmp = target + ".tmp_" + secrets.token_hex(4)
    with open(tmp, "wb") as out:
        out.write(raw)
        out.flush()
        os.fsync(out.fileno())
    with open(tmp, "rb") as chk:
        if chk.read() != raw:
            os.remove(tmp)
            raise OSError("Psion state write did not verify")
    os.replace(tmp, target)
'''

CYCLE_OLD_START = "def heartbeat_cycle():\n    return app_memory.run_autonomous('native-heartbeat',\n"
CYCLE_OLD_END = "    print(f\"[Heartbeat] Gen {gen} | Beat #{beats} | \"\n          f\"{overall_avg:.1f} tok/s | CV={cv:.4f}\", flush=True)\n    return \"ok\"\n\n\nclass PsionHeartbeat:\n"

CYCLE_NEW = '''def _heartbeat_clock():
    """Relógio de parede da cadência da memória (injetável nos testes)."""
    return time.time()


def _heartbeat_payload(sys_msg, prompt):
    """O pedido do micro-benchmark r60, byte a byte o regime medido antes de 10/10/2026: sem bloco de memória."""
    return {
        "model": "qwen3",
        "messages": [sys_msg, prompt],
        "max_tokens": HEARTBEAT_MAX_TOKENS,
        "temperature": 0.7,
        "stream": False,
    }


def _heartbeat_payload_sha256(payload):
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def _heartbeat_tok_s(data, elapsed):
    """tok/s de uma amostra: timings do servidor quando existem (só geração), senão completion_tokens/elapsed."""
    timings = data.get("timings") if isinstance(data, dict) else None
    if isinstance(timings, dict):
        n, ms = timings.get("predicted_n"), timings.get("predicted_ms")
        if (isinstance(n, (int, float)) and isinstance(ms, (int, float)) and not isinstance(n, bool)
                and not isinstance(ms, bool) and n > 0 and ms > 0):
            return n / ms * 1000.0, "timings.predicted_n/predicted_ms"
    usage = data.get("usage", {}) if isinstance(data, dict) else {}
    comp_tokens = usage.get("completion_tokens", 0) if isinstance(usage, dict) else 0
    if isinstance(comp_tokens, (int, float)) and not isinstance(comp_tokens, bool) and comp_tokens > 0 and elapsed > 0.01:
        return comp_tokens / elapsed, "completion_tokens/elapsed"
    return None, None


def _heartbeat_measure():
    """
    Medida pura de geração (12/10/2026, D3a). Envia os prompts do micro-benchmark r60 ao
    llama-server e mede tok/s. A janela cronometrada contém SÓ o post HTTP: nenhuma projeção
    da memória comum, nenhuma contagem de tokens, nenhum tool_result. Amostra que falha é
    pulada (`continue`): o heartbeat é medição local gratuita e nunca bloqueia o ciclo seguinte.
    Devolve: regime, status, results, samples (sem corpos de resposta), formulas.
    """
    measurement = {"regime": HEARTBEAT_MEASUREMENT_REGIME, "status": "no_results",
                   "results": [], "samples": [], "formulas": []}
    # 1. Check idle + health
    if not _heartbeat_is_idle():
        measurement["status"] = "skipped_busy"
        return measurement
    if not _heartbeat_llama_ok():
        measurement["status"] = "skipped_offline"
        return measurement

    # 2. Run micro-benchmark (payload r60; t0/elapsed só em volta do post)
    results, samples, formulas = [], [], []
    for index, prompt in enumerate(HEARTBEAT_PROMPTS):
        runs = []
        for run in range(HEARTBEAT_RUNS_PER_PROMPT):
            # Re-check idle between runs (abort if user appears)
            if not _heartbeat_is_idle():
                if results:
                    break  # Use partial results
                measurement["status"] = "aborted_user"
                return measurement
            payload = _heartbeat_payload(HEARTBEAT_SYSTEM_MESSAGE, prompt)
            payload_sha = _heartbeat_payload_sha256(payload)
            try:
                t0 = time.perf_counter()
                r = req_lib.post(f"{LLAMA_URL}/v1/chat/completions", json=payload, timeout=60)
                elapsed = time.perf_counter() - t0
                if r.status_code != 200:
                    samples.append({"prompt": index, "run": run, "ok": False, "http": r.status_code,
                                    "elapsed_s": round(elapsed, 4)})
                    continue
                data = r.json()
            except Exception as exc:
                samples.append({"prompt": index, "run": run, "ok": False, "error": type(exc).__name__})
                continue
            tok_s, formula = _heartbeat_tok_s(data, elapsed)
            samples.append({"prompt": index, "run": run, "ok": tok_s is not None, "elapsed_s": round(elapsed, 4),
                            "tok_s": round(tok_s, 1) if tok_s is not None else None, "formula": formula,
                            "payload_sha256": payload_sha})
            if tok_s is not None:
                runs.append(round(tok_s, 1))
                if formula not in formulas:
                    formulas.append(formula)
        if runs:
            avg = sum(runs) / len(runs)
            var = sum((x - avg) ** 2 for x in runs) / len(runs)
            results.append({"avg_tok_s": round(avg, 1), "variance": round(var, 2)})
    measurement.update(results=results, samples=samples, formulas=formulas,
                       status="ok" if results else "no_results")
    return measurement


def _heartbeat_aggregate(measurement):
    results = measurement["results"]
    overall_avg = sum(r["avg_tok_s"] for r in results) / len(results)
    overall_var = sum(r["variance"] for r in results) / len(results)
    cv = math.sqrt(overall_var) / max(overall_avg, 0.01)
    return overall_avg, cv


def _heartbeat_psion_admissible(measurement):
    """Só uma medida completa de geração pode tocar o psion (12/10/2026, D3c).

    Admissível = status ok, regime generation_only e toda amostra contada medida por fórmula
    conhecida e enviada com o payload r60 (sha256 recomputado aqui). O resto — regime com a
    memória dentro da janela, payload estranho, amostra sem fórmula — é recusado às claras e
    os bytes do psion ficam como estão.
    """
    if measurement.get("status") != "ok" or measurement.get("regime") != HEARTBEAT_MEASUREMENT_REGIME:
        return False, "status_or_regime"
    counted = [s for s in measurement.get("samples", []) if s.get("ok")]
    if not counted or not measurement.get("results"):
        return False, "no_counted_samples"
    for sample in counted:
        index = sample.get("prompt")
        if type(index) is not int or not 0 <= index < len(HEARTBEAT_PROMPTS):
            return False, "unknown_prompt"
        expected = _heartbeat_payload_sha256(_heartbeat_payload(HEARTBEAT_SYSTEM_MESSAGE, HEARTBEAT_PROMPTS[index]))
        if sample.get("payload_sha256") != expected or not sample.get("formula"):
            return False, "foreign_payload_or_formula"
    return True, "ok"


def _heartbeat_class(avg_tok_s, baseline_tok_s, total_beats):
    """Classe de saúde com o critério do próprio alerta do psion (avg < 0,8 × baseline depois de > 3 batidas)."""
    if avg_tok_s is None:
        return "falha"
    if not isinstance(baseline_tok_s, (int, float)) or type(total_beats) is not int or total_beats <= 3:
        return "ok"
    return "alerta" if avg_tok_s < baseline_tok_s * HEARTBEAT_ALERT_RATIO else "ok"


def _heartbeat_telemetry_rotate(path):
    """Renomeação encadeada path → .1 → … → .KEEP (o mais antigo além de KEEP cai). Nunca trunca."""
    oldest = f"{path}.{HEARTBEAT_TELEMETRY_KEEP}"
    if os.path.exists(oldest):
        os.remove(oldest)
    for i in range(HEARTBEAT_TELEMETRY_KEEP - 1, 0, -1):
        src = f"{path}.{i}"
        if os.path.exists(src):
            os.replace(src, f"{path}.{i + 1}")
    if os.path.exists(path):
        os.replace(path, f"{path}.1")


def _heartbeat_telemetry_append(summary):
    """Uma linha JSON por batida no arquivo rotativo próprio do heartbeat — nunca na memória comum.

    A linha carrega o seu sha256 (calculado sobre a forma canônica sem o campo). A rotação só
    acontece ANTES de acrescentar: a linha corrente nunca é truncada.
    """
    os.makedirs(HEARTBEAT_LOG_DIR, exist_ok=True)
    body = dict(summary)
    body.pop("line_sha256", None)
    canonical = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    body["line_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    raw = (json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str) + "\\n").encode("utf-8")
    path = HEARTBEAT_TELEMETRY_FILE
    try:
        size = os.path.getsize(path)
    except OSError:
        size = 0
    if size and size + len(raw) > HEARTBEAT_TELEMETRY_MAX_BYTES:
        _heartbeat_telemetry_rotate(path)
    with open(path, "ab") as out:
        out.write(raw)
        out.flush()
        os.fsync(out.fileno())
    return body


def _heartbeat_health_load():
    try:
        with open(HEARTBEAT_HEALTH_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        return state if isinstance(state, dict) else {}
    except (OSError, ValueError):
        return {}


def _heartbeat_health_save(state):
    os.makedirs(HEARTBEAT_LOG_DIR, exist_ok=True)
    raw = json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
    tmp = HEARTBEAT_HEALTH_FILE + ".tmp_" + secrets.token_hex(4)
    with open(tmp, "wb") as out:
        out.write(raw)
        out.flush()
        os.fsync(out.fileno())
    os.replace(tmp, HEARTBEAT_HEALTH_FILE)


def _heartbeat_record_memory_if_due(klass, summary, line_sha256, now):
    """No máximo UM evento na memória comum por mudança de classe ou por HEARTBEAT_MEMORY_MIN_INTERVAL.

    O evento é um resumo fact/REAL da medida (sem corpos de resposta), id 'hb.' + sha256 da
    linha de telemetria, fonte 'heartbeat_telemetry:<sha>'. Falha da memória é impressa, fica
    na telemetria e é tentada de novo numa batida futura; nunca bloqueia o ciclo seguinte.
    """
    state = _heartbeat_health_load()
    previous_class, last_at = state.get("class"), state.get("last_memory_event_at")
    due = (klass != previous_class or not isinstance(last_at, (int, float)) or isinstance(last_at, bool)
           or now - last_at >= HEARTBEAT_MEMORY_MIN_INTERVAL)
    if not due:
        return None
    event_id = "hb." + line_sha256
    keys = ("at", "regime", "status", "class", "avg_tok_s", "cv", "n_prompts", "baseline_before",
            "baseline_after", "total_beats", "formula", "psion")
    text = json.dumps({k: summary.get(k) for k in keys}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    flow = {"phase": "heartbeat_" + klass,
            "next_action": "Read the heartbeat telemetry line referenced by the source before any action; no automatic resend."}
    try:
        receipt = app_memory.record_measurement(HEARTBEAT_MEMORY_IDENTIFIER, HEARTBEAT_MEMORY_OBJECTIVE, text,
                                                "heartbeat_telemetry:" + line_sha256, flow=flow,
                                                event_id=event_id, lineage=HEARTBEAT_MEMORY_LINEAGE)
    except Exception as exc:
        print(f"[Heartbeat] memória comum indisponível ({type(exc).__name__}); telemetria preservada, "
              f"sem repetição automática", flush=True)
        _heartbeat_telemetry_append({"kind": "memory_event_failed", "at": summary.get("at"), "class": klass,
                                     "beat_line_sha256": line_sha256, "error": type(exc).__name__})
        return None
    state.update({"class": klass, "since": now if klass != previous_class else state.get("since", now),
                  "last_memory_event_at": now, "last_memory_event_id": event_id,
                  "last_revision": receipt.get("revision"), "context_id": receipt.get("context_id"),
                  "last_line_sha256": line_sha256})
    _heartbeat_health_save(state)
    _heartbeat_telemetry_append({"kind": "memory_event", "at": summary.get("at"), "event_id": event_id,
                                 "revision": receipt.get("revision"), "context_id": receipt.get("context_id"),
                                 "class": klass, "beat_line_sha256": line_sha256})
    return event_id


def heartbeat_cycle():
    """
    One complete heartbeat cycle (12/10/2026, D3): medida só de geração → psion (EMA, taxa β)
    só com medida admissível → uma linha de telemetria → memória comum só por mudança de classe
    ou no máximo 1/hora. Nunca dentro de run_autonomous; falha nunca bloqueia o ciclo seguinte.
    """
    now = _heartbeat_clock()
    measurement = _heartbeat_measure()
    status = measurement["status"]
    summary = {"kind": "beat", "at": datetime.fromtimestamp(now).isoformat(timespec="seconds"),
               "epoch": round(now, 3), "regime": measurement["regime"], "status": status,
               "formula": "+".join(measurement.get("formulas") or []) or None, "class": None,
               "avg_tok_s": None, "cv": None, "n_prompts": len(measurement["results"]),
               "samples": measurement["samples"], "baseline_before": None, "baseline_after": None,
               "total_beats": None, "psion": "untouched"}
    if status in ("skipped_busy", "aborted_user"):
        # Não é sinal de saúde: o servidor está atendendo alguém. Só telemetria.
        _heartbeat_telemetry_append(summary)
        return status

    klass, psion = "falha", None
    if status == "ok":
        admissible, reason = _heartbeat_psion_admissible(measurement)
        if not admissible:
            summary["psion"], status = "refused_" + reason, "inadmissible"
        else:
            overall_avg, cv = _heartbeat_aggregate(measurement)
            summary["avg_tok_s"], summary["cv"] = round(overall_avg, 1), round(cv, 4)
            try:
                with _heartbeat_lock:
                    psion = _load_psion_state()
                    # Verify anchoring
                    stored_beta = psion.get("beta_tgl", _BETA_TGL)
                    if abs(stored_beta - _BETA_TGL) > 1e-10:
                        print(f"[Heartbeat] ANCHORING VIOLATION: stored beta={stored_beta}", flush=True)
                        summary["psion"], status = "anchoring_error", "anchoring_error"
                    else:
                        summary["baseline_before"] = psion.get("heartbeat", {}).get("baseline_tok_s")
                        psion = _update_psion_from_heartbeat(psion, overall_avg, cv, len(measurement["results"]))
                        _save_psion_state(psion)
                        hb = psion.get("heartbeat", {})
                        summary["baseline_after"], summary["total_beats"] = hb.get("baseline_tok_s"), hb.get("total_beats")
                        summary["psion"] = "updated"
                        klass = _heartbeat_class(overall_avg, summary["baseline_after"], summary["total_beats"])
            except Exception as exc:
                print(f"[Heartbeat] psion indisponível ({type(exc).__name__}); medida fica só na telemetria", flush=True)
                summary["psion"], status = "error_" + type(exc).__name__, "psion_error"
    summary["status"], summary["class"] = status, klass
    line = _heartbeat_telemetry_append(summary)
    event_id = _heartbeat_record_memory_if_due(klass, summary, line["line_sha256"], now)
    tail = f" | memória {event_id[:19]}…" if event_id else ""
    if status == "ok":
        print(f"[Heartbeat] Gen {psion.get('generation', '?')} | Beat #{summary['total_beats']} | "
              f"{summary['avg_tok_s']:.1f} tok/s | CV={summary['cv']:.4f} | classe={klass}{tail}", flush=True)
    else:
        print(f"[Heartbeat] {status} | classe={klass}{tail}", flush=True)
    return status


class PsionHeartbeat:
'''

STATUS_OLD = '''                "alerts": hb.get("alerts", [])[-5:],
                "beta_tgl": psion.get("beta_tgl", _BETA_TGL),
            }
'''
STATUS_NEW = '''                "alerts": hb.get("alerts", [])[-5:],
                "beta_tgl": psion.get("beta_tgl", _BETA_TGL),
                "health": _heartbeat_health_load(),   # 12/10/2026 (D3): classe, desde quando, último evento
            }
'''

# ─────────────────────────────────────────────────────────────────────────────
# iald_app_memory.py — record_measurement (após run_autonomous)
# ─────────────────────────────────────────────────────────────────────────────

MEM_OLD = '''            raise


def protected_path(path):
'''
MEM_NEW = '''            raise


def record_measurement(identifier, objective, text, source_ref, *, flow=None, event_id=None, lineage='measurement'):
    """One fact/REAL event for an existing local measurement service (12/10/2026, D3b).

    No run_autonomous (no start/finish pair, no reconciliation lock), no outbox spool and no
    response bodies: the caller passes a canonical summary plus a reference to its own telemetry
    line. Each service/lineage has its own ledger (`app_service_<sha256(identifier:lineage)>`), so
    the legacy heartbeat context of 10/10 stays read-only history. Changing the objective text
    means a new lineage name: the anchor of an existing ledger is immutable. Idempotent by
    event_id; local compare-and-swap only, never a provider call.
    """
    if not isinstance(identifier, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}', identifier):
        raise ValueError('Invalid measurement service identifier')
    if not isinstance(lineage, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}', lineage):
        raise ValueError('Invalid measurement lineage')
    if not isinstance(text, str) or not text or not isinstance(source_ref, str) or not source_ref:
        raise ValueError('Measurement text and source reference are required')
    scope = {'house': 'IALD_APP_SERVICES', 'principal': 'service.' + identifier}
    ident = 'app_service_' + digest(identifier + ':' + lineage)
    actor_id = 'service.' + identifier
    event_id = event_id or ('measurement.' + digest(identifier + ':' + lineage + ':' + source_ref))
    store = MemoryStore(_SHARED_ROOT)
    store.ensure_context(ident, objective=objective, scope=scope,
        actor={'id': actor_id, 'kind': 'system'},
        constraints={'mission_id': ident, 'service': identifier, 'lineage': lineage, 'gate_authority': False,
                     'no_credentials_or_private_service_state_in_memory': True, 'no_response_bodies': True,
                     'cadence': 'class_change_or_hourly'})
    record = {'id': event_id, 'kind': 'fact', 'statute': 'REAL', 'text': text,
              'sources': [{'kind': 'measurement', 'ref': source_ref}]}
    changes = {'records': [record]}
    if flow is not None:
        changes['flow'] = flow
    actor = {'id': actor_id, 'kind': 'measurement'}
    with _LOCK:
        for _ in range(12):
            snapshot = store.get(ident, scope)
            try:
                return store.transition(ident, scope, expected_revision=snapshot['revision'],
                                        event_id=event_id, actor=actor, changes=changes)
            except RevisionConflict:
                continue
    raise RuntimeError('Concurrent memory updates require reconciliation')


def protected_path(path):
'''


def main():
    web = load(WEB)
    web = replace_once(web, HEADER_OLD, HEADER_NEW, "cabeçalho do heartbeat")
    web = replace_once(web, CONST_OLD, CONST_NEW, "constantes do heartbeat")
    web = replace_once(web, SAVE_OLD, SAVE_NEW, "_save_psion_state")
    start = web.count(CYCLE_OLD_START)
    end = web.count(CYCLE_OLD_END)
    if start != 1 or end != 1:
        raise SystemExit(f"ancoras do ciclo: inicio={start} fim={end}; esperado 1/1")
    i = web.index(CYCLE_OLD_START)
    j = web.index(CYCLE_OLD_END) + len(CYCLE_OLD_END)
    assert i < j
    web = web[:i] + CYCLE_NEW + web[j:]
    web = replace_once(web, STATUS_OLD, STATUS_NEW, "get_status")
    for forbidden in ("run_autonomous('native-heartbeat'", "_heartbeat_cycle_with_memory",
                      'app_memory.tool_result("heartbeat_sample"'):
        if forbidden in web:
            raise SystemExit("trecho antigo sobreviveu: " + forbidden)
    sha_web = save(WEB, web)

    mem = load(MEM)
    mem = replace_once(mem, MEM_OLD, MEM_NEW, "record_measurement")
    sha_mem = save(MEM, mem)

    import ast
    for p in (WEB, MEM):
        ast.parse(open(p, "rb").read().decode("utf-8"))
    print("iald_web_server.py", sha_web)
    print("iald_app_memory.py", sha_mem)


if __name__ == "__main__":
    main()
