# -*- coding: utf-8 -*-
"""Disposicoes da afericao de CODIGO da v385 no gerador do candidato (gerar_candidato_v385.py):
 nota 10: as linhas W04 (os dois registros novos no main) em try/except -- uma excecao ali vira registro NAO selado/NAO comparado, dito, e o rito segue
   (nunca derruba o rito depois das ~2,5 h do pilar); o balde dos nao selados e o conferidor tornam isso visivel;
 nota 9: a ORDEM DO OPERADOR da v385 gravada no CANDIDATO_v385.json, lida do transcrito por script (mensagem achada pelo comeco), nunca digitada;
 e a escada do registro lida do core da v384 (nao mais o literal 5998).
Backup de bytes; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "gerar_candidato_v385.py")
s0 = open(P, encoding="utf-8", newline="").read(); s = s0
T = []
T.append(("""reg = ['    core["quantum_pillar_reproducibility_v385"] = quantum_pillar_reproducibility_v385(_QP_PREV_V385, core["quantum_pillar_v384"])   # v385: a reprodutibilidade, campo a campo [COMPUTED]',
       '    print("   [v385] a reprodutibilidade do pilar quantico (a rodada desta versao contra a guardada pela anterior, mesma chave): %s" % core["quantum_pillar_reproducibility_v385"]["verdict"])',
       '    core["the_axiom_v385"] = the_axiom_v385(core)   # v385: o Axioma e a testemunha falsa -- as 28 declaracoes verificadas pelo kernel desta rodada e o nome do degrau final lido do kernel',""",
"""reg = ['    try:   # v385 (afericao de codigo, nota 10): uma excecao aqui vira registro NAO comparado, dito -- nunca derruba o rito depois do pilar',
       '        core["quantum_pillar_reproducibility_v385"] = quantum_pillar_reproducibility_v385(_QP_PREV_V385, core["quantum_pillar_v384"])   # v385: a reprodutibilidade, campo a campo [COMPUTED]',
       '    except Exception as _e385:',
       '        core["quantum_pillar_reproducibility_v385"] = {"verdict": "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__NOT_COMPARED_RUNTIME_ERROR__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED", "compared": False, "why": repr(_e385)[:400], "status": "[COMPUTED]", "does_not_gate_core": True}',
       '    print("   [v385] a reprodutibilidade do pilar quantico (a rodada desta versao contra a guardada pela anterior, mesma chave): %s" % core["quantum_pillar_reproducibility_v385"]["verdict"])',
       '    try:   # v385 (afericao de codigo, nota 10): uma excecao aqui vira o Axioma NAO selado, dito (all_verified False: vai ao balde dos nao selados)',
       '        core["the_axiom_v385"] = the_axiom_v385(core)   # v385: o Axioma e a testemunha falsa -- as 28 declaracoes verificadas pelo kernel desta rodada e o nome do degrau final lido do kernel',
       '    except Exception as _e385:',
       '        core["the_axiom_v385"] = {"verdict": "TGL_THE_AXIOM_V385__NOT_SEALED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e385)[:400], "does_not_gate_core": True}',"""))
T.append(("""man = {"candidato": out, "sha16": h16, "bytes": len(b), "base_v384_sha16": SHA0, "kernel": KERNEL_MANIFEST, "escada": [5998, 5998 + len(FLAGS)],""",
"""# a escada da v384, LIDA do core selado (nao mais o literal), e a ORDEM DO OPERADOR da v385, LIDA do transcrito (afericao de codigo, nota 9)
_C384 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]["external_ladder"]
_E384 = int(_C384["n_theorems_expected"]); assert int(_C384["n_theorems_clean"]) == _E384
_TR = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
_ORD = None
for _ln in open(_TR, encoding="utf-8", errors="replace"):
    try:
        _d = json.loads(_ln)
    except ValueError:
        continue
    if _d.get("type") == "user":
        _c = _d.get("message", {}).get("content")
        for _t in ([_c] if isinstance(_c, str) else [x.get("text", "") for x in (_c or []) if isinstance(x, dict) and x.get("type") == "text"]):
            if (_t or "").strip().startswith("agora sim, concordo com tudo, prossiga"):
                _ORD = {"verbatim": _t.strip(), "quando": _d.get("timestamp"), "transcrito": _TR, "lido_por": "gerar_candidato_v385.py (mensagem achada pelo comeco)"}
assert _ORD, "a ordem do operador da v385 nao foi achada no transcrito"
man = {"candidato": out, "sha16": h16, "bytes": len(b), "base_v384_sha16": SHA0, "kernel": KERNEL_MANIFEST, "escada": [_E384, _E384 + len(FLAGS)],
       "ordem_do_operador": _ORD,"""))
for a, b in T:
    n = s.count(a)
    assert n == 1, ("a troca nao e unica", n, a[:100])
    s = s.replace(a, b)
ast.parse(s)
st = time.strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + st + "_afer1", "wb").write(s0.encode("utf-8"))
open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
print("OK gerar_candidato_v385.py:", len(s0), "->", len(s))
