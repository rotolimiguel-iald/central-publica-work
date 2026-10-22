"""Deterministic restrictions precede every semantic/provider decision."""
from __future__ import annotations

import math
import re
from .matrix import select_support

# D4 (12/10/2026): superset of the previous pattern. Adds any iald_stack_v<N>, GitHub/Slack/Bearer
# tokens, *.key/*.pem names and the Escritório house as a PATH (drive, UNC or slash-delimited
# component; NFC or NFD accent), never the loose word. Fail-closed: a hit refuses, nothing is redacted.
FORBIDDEN = re.compile(
    r"iald_stack_v\d|iald_psion_state|(?:^|[\\/\s])\.env(?:[.\s]|$)|\b(?:sk-|AIza)[A-Za-z0-9_-]{12,}"
    r"|\bgh[pousr]_[A-Za-z0-9]{20,}|\bxox[abposr]-[A-Za-z0-9-]{10,}|\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"
    r"|\b[\w\-]+\.(?:key|pem)\b"
    r"|(?:\b[a-z]:[\\/]+(?:[^\\/\s]+[\\/]+)*|\\\\[^\\/\s]+[\\/]+(?:[^\\/\s]+[\\/]+)*|[\\/])escrit(?:ó|[oó])rio",
    re.I)


def confidential_rules(text):
    """Rule NAMES matched by `text` (never the matched spans).

    The regex above is the always-present shortcut; when the shared memory guard
    (`iald_memory.guard`, installed with the common memory) is importable its rule
    names are added. The shortcut alone already covers every D4 item.
    """
    rules = ["policy.FORBIDDEN"] if isinstance(text, str) and FORBIDDEN.search(text) else []
    try:
        from iald_memory import guard
    except ImportError:
        guard = None
    if guard is not None:
        rules.extend(r for r in guard.scan_text(text) if r not in rules)
    return rules


def validate_prompt(prompt, max_chars=24000):
    if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > max_chars:
        raise ValueError(f"Informe uma tarefa de 1 a {max_chars} caracteres.")
    rules = confidential_rules(prompt)
    if rules:
        raise ValueError("A tarefa referencia confidenciais bloqueados ou aparenta conter credencial: "
                         + ", ".join(rules))
    return prompt.strip()


def classify(prompt):
    text = prompt.casefold()
    complex_terms = ("demonstre", "teorema", "lean", "arquitetura", "refator", "auditor", "gravidade", "prova", "kernel")
    needs_reasoning = len(prompt) > 4000 or any(term in text for term in complex_terms)
    return {"complexity": "deep" if needs_reasoning else "standard",
            "source": "INPUT: initial lexical policy, not measured model quality",
            "capabilities": ["text"], "estimated_input_tokens": math.ceil(len(prompt.encode("utf-8")) / 3),
            "estimate_status": "ESTIMATE_OF_USER_TEXT_ONLY_EXCLUDES_CLIENT_OVERHEAD"}


def route(prompt, providers, counts, *, classification=None, excluded=(), max_prompt_chars=24000):
    validate_prompt(prompt, max_prompt_chars)
    task = classification or classify(prompt)
    rows, weights, mask = [], [], []
    for provider in providers:
        p = dict(provider)
        reasons = []
        if p["id"] in excluded:
            reasons.append("falha nesta tarefa")
        if p.get("status") != "ready":
            reasons.append(p.get("status", "indisponivel"))
        if task["complexity"] == "deep" and p.get("tier") != "advanced":
            reasons.append("política inicial exige raciocínio avançado")
        if p.get("billing") not in ("local", "subscription") and not (p.get("billing") == "authorized_api" and p.get("billing_authorized") is True):
            reasons.append("custo adicional sem teto configurado")
        if p.get("daily_run_limit", 10) is not None and counts.get(p["id"], 0) >= p.get("daily_run_limit", 10):
            reasons.append("limite operacional diário atingido")
        if p.get("quota_remaining") is not None and p["quota_remaining"] <= 0:
            reasons.append("cota do provedor esgotada")
        if task["estimated_input_tokens"] + p.get("output_token_budget", 2048) > p.get("context_budget", 8192):
            reasons.append("texto fornecido excede orçamento estimado de entrada/saída")
        # No invented benchmark: these weights are declared scheduling policy.
        weight = 1.0 / (1.0 + counts.get(p["id"], 0))
        if p.get("billing") == "local" and task["complexity"] == "standard":
            weight *= 2.0
        p.update(eligible=not reasons, exclusion_reasons=reasons, policy_weight=weight)
        rows.append(p)
        weights.append(weight)
        mask.append(not reasons)
    selection = select_support([r["id"] for r in rows], weights, mask)
    return {"task": task, "candidates": rows, "matrix": selection, "selected": selection["selected"],
            "status": selection["status"], "quality_status": "NOT_BENCHMARKED",
            "quota_scope": "Limites operacionais locais; não equivalem às cotas das assinaturas. Consumo completo só é conhecido após a chamada.",
            "reason": "Suporte elegível → preservação matricial → política de custo/cota → maior peso."}
