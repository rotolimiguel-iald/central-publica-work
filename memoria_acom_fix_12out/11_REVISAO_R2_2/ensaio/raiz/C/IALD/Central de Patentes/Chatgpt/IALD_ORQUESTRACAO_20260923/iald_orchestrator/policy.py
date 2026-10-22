"""Deterministic restrictions precede every semantic/provider decision."""
from __future__ import annotations

import math
import re
from .matrix import select_support

FORBIDDEN = re.compile(r"iald_stack_v7|iald_psion_state|(?:^|[\\/\s])\.env(?:[.\s]|$)|\b(?:sk-|AIza)[A-Za-z0-9_-]{12,}", re.I)


def validate_prompt(prompt, max_chars=24000):
    if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > max_chars:
        raise ValueError(f"Informe uma tarefa de 1 a {max_chars} caracteres.")
    if FORBIDDEN.search(prompt):
        raise ValueError("A tarefa referencia confidenciais bloqueados ou aparenta conter credencial.")
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
