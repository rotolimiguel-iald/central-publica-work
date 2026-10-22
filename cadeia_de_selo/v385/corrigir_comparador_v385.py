# -*- coding: utf-8 -*-
"""Disposicoes da afericao de CODIGO da v385 (RELATORIO_AFERIDOR_CODIGO_v385.txt) no comparador da reprodutibilidade (v385_runtime.py):
 1 (CORRIGIR) campo nao finito que difere conta como DIFERENCA (a regra do comparador da bancada v361), nunca como arredondamento;
 2 (CORRIGIR) a escala da tolerancia e' max(1, |a|, |b|) (a da v361): residuo de maquina (1e-16) que muda no ultimo digito fica no arredondamento; contagem
   que muda de 1 continua acusando; o veredito diz MAX_SCALED (e grava, ao lado, a relativa pura so dos finitos, informativa);
 3 (NOTA) o pulo dos campos de tempo e de ambiente por CHAVE DE TEMPO, nunca um booleano (D128.started passa a ser comparado);
 4 (NOTA) D128 que nao rodou NESTA rodada (e rodou na anterior): os campos D128.* saem da comparacao e isso fica DITO no veredito (D128_EXCLUDED);
 5 (NOTA) SAME_V1_SAME_WORKER_SAME_BETA so com a conferencia: a leitura anterior guarda spec/trabalhador/beta/ambiente do resultado; diferentes ->
   NOT_COMPARED_DIFFERENT_INPUTS (e o ambiente, gpu/torch/cuda, e' gravado e comparado, informativo).
Backup de bytes; temporario -> conferir -> substituir; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "v385_runtime.py")
s0 = open(P, encoding="utf-8", newline="").read()
i = s0.index("def quantum_pillar_previous_v385(st):")
NOVO = r'''def quantum_pillar_previous_v385(st):
    """Logo depois de lancar o trabalhador (antes de o calculo novo poder substituir o cache), le o resultado que o cache guardou da rodada anterior com
    a MESMA chave (trabalhador, especificacao, beta) -- o da v384 --, conferido pelo sha256; guarda o resumo (pela MESMA _qp_summary desta rodada), as
    entradas (especificacao, trabalhador, beta) e o ambiente, para medir a reprodutibilidade depois. Nunca levanta: falha de leitura fica dita."""
    out = {"read": False}
    try:
        if not isinstance(st, dict) or st.get("refused") or st.get("mode") != "COMPUTE":
            out["why_not"] = "a rodada desta versao nao CALCULA o pilar (modo %s)" % ((st or {}).get("mode") if isinstance(st, dict) else None)
            return out
        cdir = st.get("cache_dir")
        if not cdir:
            out["why_not"] = "sem pasta de cache"
            return out
        R = _qp_cached_ok(cdir)
        if not R:
            out["why_not"] = "nenhum resultado anterior conferido no cache desta chave"
            return out
        rp = os.path.join(cdir, "result.json")
        out.update({"read": True, "cache_dir": cdir, "key": st.get("key"), "sha256": hashlib.sha256(open(rp, "rb").read()).hexdigest(),
                    "finished": R.get("finished"), "run_id": R.get("run_id"), "verdict": R.get("verdict"), "summary": _qp_summary(R),
                    "inputs": {"spec_sha256": R.get("spec_sha256"), "worker_sha256": R.get("worker_sha256"), "beta_hex": R.get("beta_hex")},
                    "env": {k_: (R.get("env") or {}).get(k_) for k_ in ("gpu", "torch", "cuda")}})
        # o resultado cru nao guarda o resumo: ele e' montado pela MESMA _qp_summary que monta o desta rodada (achado do ensaio a seco, 05/10)
    except Exception as e_:
        out["error"] = repr(e_)
    return out


# os campos que variam legitimamente entre rodadas (tempo e ambiente): pulados por CHAVE DE TEMPO, nunca um booleano (afericao de codigo, nota 3)
_QP_REPRO_SKIP_TOP_V385 = {"phase_seconds", "env"}
_QP_REPRO_SKIP_TIME_V385 = {"cpu_seconds", "elapsed_s", "started", "finished", "spectrum_s", "steady_state_s", "s", "timestamp", "run_id"}
_QP_REPRO_SKIP_V385 = _QP_REPRO_SKIP_TOP_V385 | _QP_REPRO_SKIP_TIME_V385   # (o nome antigo, para quem o le)


def _qp_flat_v385(o, p=""):
    if isinstance(o, dict):
        for k_, v_ in o.items():
            k_ = str(k_)
            if (not p and k_ in _QP_REPRO_SKIP_TOP_V385) or (k_ in _QP_REPRO_SKIP_TIME_V385 and not isinstance(v_, bool)):
                continue
            yield from _qp_flat_v385(v_, (p + "." + k_) if p else k_)
    elif isinstance(o, list):
        for i_, v_ in enumerate(o):
            yield from _qp_flat_v385(v_, "%s[%d]" % (p, i_))
    else:
        yield p, o


def _qp_tok_v385(x_):
    return ("%.1e" % x_).replace(".", "P").replace("-", "M").replace("+", "")


def quantum_pillar_reproducibility_v385(prev, rec):
    """A REPRODUTIBILIDADE (v385): o resumo desta rodada contra o resumo guardado pela anterior (mesma chave), campo a campo, fora os de tempo e de
    ambiente. Igual bit a bit; igual a menos de arredondamento (|a - b| / max(1, |a|, |b|) <= 1e-9, a escala do comparador da bancada v361; campo nao
    finito que difere conta como diferenca); ou diferente (com a lista). So compara se as ENTRADAS forem as mesmas (especificacao, trabalhador, beta);
    se o D128 nao rodou nesta rodada e rodou na anterior, os campos D128.* saem da comparacao e isso fica dito no veredito. [COMPUTED]; nao move o gate."""
    base = {"status": "[COMPUTED]", "does_not_gate_core": True, "skipped_keys": {"top": sorted(_QP_REPRO_SKIP_TOP_V385), "time_keys_not_bool": sorted(_QP_REPRO_SKIP_TIME_V385)},
            "tolerance": "|a-b|/max(1,|a|,|b|) <= 1e-9; non-finite that differs = difference (the v361 bench comparator rule)"}
    if not isinstance(prev, dict) or not prev.get("read"):
        why = (prev or {}).get("why_not") or (prev or {}).get("error") or "sem leitura"
        base.update({"verdict": "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__NO_PREVIOUS_RUN_TO_COMPARE__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED",
                     "compared": False, "why": why})
        return base
    if not isinstance(prev.get("summary"), dict) or not prev.get("summary"):
        base.update({"verdict": "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__NO_PREVIOUS_RUN_TO_COMPARE__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED",
                     "compared": False, "why": "a leitura anterior nao trouxe resumo comparavel"})
        return base
    rec = rec or {}
    if (rec.get("reuse") or {}).get("reused") is True or not rec.get("summary") or not str(rec.get("verdict") or "").startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__"):
        base.update({"verdict": "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED",
                     "compared": False, "why": "esta rodada nao calculou um resultado comparavel (reaproveitado, sem resumo ou fora da arvore)"})
        return base
    # as ENTRADAS: so se compara o que foi calculado das mesmas entradas (nota 5)
    pin = prev.get("inputs") or {}
    rin = {"spec_sha256": rec.get("spec_sha256_in_result"), "worker_sha256": rec.get("worker_sha256"), "beta_hex": rec.get("beta_hex")}
    same_inputs = bool(pin) and all(pin.get(k_) is not None and pin.get(k_) == rin.get(k_) for k_ in rin)
    renv = {k_: ((rec.get("summary") or {}).get("env") or {}).get(k_) for k_ in ("gpu", "torch", "cuda")}
    base.update({"inputs": {"previous": pin, "this_run": rin, "same": same_inputs}, "env": {"previous": prev.get("env"), "this_run": renv, "same": prev.get("env") == renv}})
    if not same_inputs:
        base.update({"verdict": "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__NOT_COMPARED_DIFFERENT_INPUTS__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED",
                     "compared": False, "why": "as entradas da rodada anterior (especificacao/trabalhador/beta) nao sao as desta rodada"})
        return base
    a = dict(_qp_flat_v385(prev.get("summary") or {})); b = dict(_qp_flat_v385(rec.get("summary") or {}))
    # o D128 que nao rodou NESTA rodada (e rodou na anterior): sai da comparacao, dito (nota 4)
    _d_prev = str(((prev.get("summary") or {}).get("D128") or {}).get("status_code")); _d_this = str(((rec.get("summary") or {}).get("D128") or {}).get("status_code"))
    d128_excl = (_d_this != "RAN" and _d_prev == "RAN")
    if d128_excl:
        a = {k_: v_ for k_, v_ in a.items() if not k_.startswith("D128")}; b = {k_: v_ for k_, v_ in b.items() if not k_.startswith("D128")}
    keys = sorted(set(a) | set(b))
    diff = []; maxsc = 0.0; maxrel = 0.0; n_num = 0; n_nonfinite_diff = 0
    for k_ in keys:
        x_, y_ = a.get(k_, "<AUSENTE>"), b.get(k_, "<AUSENTE>")
        num = isinstance(x_, (int, float)) and isinstance(y_, (int, float)) and not isinstance(x_, bool) and not isinstance(y_, bool)
        if num:
            n_num += 1
            fx, fy = float(x_), float(y_)
            if not (math.isfinite(fx) and math.isfinite(fy)):
                if (fx != fx and fy != fy) or fx == fy:          # NaN nos dois, ou o mesmo infinito: igual
                    continue
                n_nonfinite_diff += 1
                diff.append({"field": k_, "previous": str(x_), "this_run": str(y_), "scaled": None, "rel": None}); continue
            if x_ == y_:
                continue
            sc = abs(fx - fy) / max(1.0, abs(fx), abs(fy)); rl = abs(fx - fy) / max(abs(fx), abs(fy), 1e-300)
            maxsc = max(maxsc, sc); maxrel = max(maxrel, rl)
            diff.append({"field": k_, "previous": x_, "this_run": y_, "scaled": sc, "rel": rl})
        elif x_ != y_:
            diff.append({"field": k_, "previous": str(x_)[:200], "this_run": str(y_)[:200], "scaled": None, "rel": None})
    exact_other = all(d_["scaled"] is not None for d_ in diff)
    same_verdict = (prev.get("verdict") == rec.get("verdict"))
    ex = "__D128_EXCLUDED_NOT_RUN_THIS_RUN" if d128_excl else ""
    if not diff:
        v = "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__REPRODUCED_BIT_FOR_BIT__%d_FIELDS%s__SAME_V1_SAME_WORKER_SAME_BETA__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED" % (len(keys), ex)
    elif exact_other and maxsc <= 1e-9:
        v = ("TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__REPRODUCED_WITHIN_ROUNDOFF__%d_FIELDS__%d_DIFFER_MAX_SCALED_%s%s__SAME_V1_SAME_WORKER_SAME_BETA__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED"
             % (len(keys), len(diff), _qp_tok_v385(maxsc), ex))
    else:
        v = "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__NOT_REPRODUCED__%d_OF_%d_FIELDS_DIFFER%s__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED" % (len(diff), len(keys), ex)
    base.update({"verdict": v, "compared": True, "n_fields": len(keys), "n_numeric_fields": n_num, "n_differ": len(diff), "max_scaled_diff": maxsc,
                 "max_rel_diff_finite": maxrel, "n_nonfinite_differ": n_nonfinite_diff, "d128_excluded": d128_excl,
                 "first_differences": diff[:25], "same_pillar_verdict": same_verdict,
                 "previous": {k_: prev.get(k_) for k_ in ("sha256", "finished", "run_id", "verdict", "key")},
                 "this_run": {"result_sha256": rec.get("result_sha256"), "run_id": rec.get("run_id"), "finished": rec.get("finished"), "verdict": rec.get("verdict")}})
    return base
'''
s = s0[:i] + NOVO
ast.parse(s)
st = time.strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + st + "_afer1", "wb").write(s0.encode("utf-8"))
open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); assert os.path.getsize(P + ".tmp") > len(s0.encode("utf-8")); os.replace(P + ".tmp", P)
print("OK v385_runtime.py:", len(s0), "->", len(s))
