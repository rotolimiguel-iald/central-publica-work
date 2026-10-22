# -*- coding: utf-8 -*-
"""corrigir_afericao_snips_v387.py -- aplica aos snippets dos tres testes (copiados ao pacote, I3) as correcoes da afericao adversarial de 06/10:
C1 (a frase «Nenhum dos tres falhou» passa a ser CONDICIONADA ao lido: livro sem falsificada, escada limpa = esperada, GPU sem discordancia), C2 (o «sim» da coluna RG?
so vale com o estado lido; AWAITING/recusa/INCONCLUSIVE/ausente viram n/a; a marcacao por linha e' dita leitura da gerencia), A6 (o «Lidos um a um» so sai se as
substrings forem as tres lidas em 05/10). Cada old ocorre UMA vez (assert); idempotente pelo marcador _ok3x; ast.parse ao fim."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PRE = '''
    # v387 (afericao adversarial C1/C2/A6, 06/10): o que a secao afirma em bloco e' CONDICIONADO ao que se le nesta rodada
    import re as _re3x
    _lgx3s = (core.get("the_ledger_of_charges_v383") or {}).get("counts") or {}
    _qsx3s = (core.get("quantum_pillar_v384") or {}).get("summary") or {}
    _elx3s = core.get("external_ladder") or {}
    _t2x3s, _t4x3s, _t1x3s, _cpx3s = (_qsx3s.get("T2") or {}), (_qsx3s.get("T4") or {}), (_qsx3s.get("T1") or {}), (_qsx3s.get("cpuref") or {})
    _ok3x = {"RITOS": _lgx3s.get("FALSIFIED") == 0,
             "KERNEL": _elx3s.get("n_theorems_clean") is not None and _elx3s.get("n_theorems_clean") == _elx3s.get("n_theorems_expected"),
             "GPU": (_t2x3s.get("points") is not None and _t2x3s.get("unique") == _t2x3s.get("points") and _t4x3s.get("instances") is not None and _t4x3s.get("unique") == _t4x3s.get("instances")
                     and _t1x3s.get("errors") == 0 and _cpx3s.get("disagreements") == 0)}
    _falhas3x = [k_ for k_, v_ in _ok3x.items() if not v_]
    _NA3x = ("AWAITING", "INCAPAZ", "NOT_RUN", "INCONCLUSIVE", "AUSENTE", "ABSENT")
    _FAL_ESPERADAS3x = {"d1_camb_result", "bancada_fases_5_6_7_v380", "the_ledger_of_charges_v383"}
    _fal_nomes3x = lambda ps_: {_re3x.sub(r"[/.]verdict$", "", str(p_).replace("core/", "", 1)) for p_ in (ps_ or [])}
'''


def edit(fn, pairs):
    s = open(fn, encoding="utf-8").read()
    if "_ok3x = {" in s:
        print("ja corrigido (idempotente):", fn); return
    for a, b in pairs:
        n = s.count(a); assert n == 1, (fn, a[:80], n); s = s.replace(a, b)
    ast.parse("def _f(core, verdict, data_path, s):\n" + s)
    open(fn + ".tmp", "w", encoding="utf-8", newline="\n").write(s); os.replace(fn + ".tmp", fn); print("ok", fn)


for fn, lang in (("artigo_pt_v387_tres_testes.pysnip", "pt"), ("artigo_en_v387_tres_testes.pysnip", "en")):
    p = os.path.join(HERE, fn); s = open(p, encoding="utf-8").read()
    if "_ok3x = {" in s:
        print("ja corrigido (idempotente):", fn); continue
    anc = [l for l in s.split("\n") if l.startswith('    _t3s = core.get("three_stress_tests_v387") or {}')][0] + "\n"
    yes = "sim" if lang == "pt" else "yes"
    na = 'r"n/a (o estado lido nesta rodada não lê a RG)"' if lang == "pt" else 'r"n/a (the state read in this run does not read GR)"'
    row_old = "        _rows3s.append((canal_, estado_, numero_, rg_, disc_, synth_))"
    row_new = ("        if str(rg_).startswith(%r) and any(t_ in str(estado_).replace(r\"\\_\", \"_\").replace(r\"\\allowbreak{}\", \"\") for t_ in _NA3x):\n"
               "            rg_ = %s   # v387 C2: o «%s» so vale com o estado lido\n" % (yes, na, yes)) + row_old
    pairs = [(anc, anc + PRE), (row_old, row_new)]
    L = s.split("\n")
    if lang == "pt":
        pairs += [('                  r"Nenhum dos três falhou nesta rodada, e nenhum deles falhar',
                   '                  + (r"Nenhum dos três falhou nesta rodada (lido: livro sem falsificada, escada limpa = esperada, GPU sem discordância)" if not _falhas3x else (r"Nesta rodada NEM TODOS os pilares passaram --- falhou: " + ", ".join(_falhas3x))) + r", e nenhum deles falhar'),
                  ('(coluna «RG?» = sim; as duas linhas', '(coluna «RG?» = sim --- leitura da gerência por linha, condicionada ao estado lido: AWAITING, recusa, INCONCLUSIVE ou ausente viram n/a; as duas linhas'),
                  ('nomeados acima --- isto é \\textsf{[REAL]};', 'nomeados acima --- isto é \\textsf{[REAL]} nas linhas em que o estado lido o sustenta (a marcação por linha é leitura da gerência);')]
        lr = [x for x in L if x.startswith('                  r"Lidos um a um:')][0]
        alt = 'r"As substrings desta rodada não são as três lidas em 05/10 --- a leitura de cada uma, uma a uma, fica para a gerência (dito). "'
    else:
        pairs += [('                  r"None of the three failed in this run, and that none of them fails',
                   '                  + (r"None of the three failed in this run (read: ledger without a falsified charge, clean ladder = expected, GPU without disagreement)" if not _falhas3x else (r"In this run NOT ALL pillars passed --- failed: " + ", ".join(_falhas3x))) + r", and that none of them fails'),
                  ('(«GR?» = yes; the two synthesis rows', '(«GR?» = yes --- a per-row reading by the management, conditioned on the state read: AWAITING, refusal, INCONCLUSIVE or absent become n/a; the two synthesis rows'),
                  ('named above --- this is \\textsf{[REAL]};', 'named above --- this is \\textsf{[REAL]} in the rows where the state read sustains it (the per-row marking is the management\'s reading);')]
        lr = [x for x in L if x.startswith('                  r"Read one by one:')][0]
        alt = 'r"The substrings of this run are not the three read on 2026-10-05 --- reading each one is left to the management (stated). "'
    pairs.append((lr, '                  + ((' + lr.strip() + ') if _fal_nomes3x(_c3s["fal_paths"]) == _FAL_ESPERADAS3x else (' + alt + ')) + r""'))
    edit(p, pairs)
