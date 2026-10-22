# -*- coding: utf-8 -*-
"""ERRATA AO LADO, em nome proprio da gerencia (lei da assinatura da errata), da LEITURA [ONTO] gravada em 05/10 (bloco decisoes_operador_05out_b_v385) --
achados da verificacao adversarial (workflow verificar-decisoes-05out-b, 3 lentes): (1) a sub-citacao «a forma falsa deixa de ter conteudo por construcao»
perdeu a virgula do original; (2) o «→ 0» estava colado a axiomFlow_gradient (so a igualdade) -- o limite e' Real.tendsto_exp_neg_atTop_nhds_zero (Mathlib),
e F(t)(1-P) → 0 e' corolario SEM termo proprio na pedra; (3) «o complemento nunca vira posto» nao tem termo: corolario de compl_mul_post + idempotencia com
P != 0 (derivavel; o verificador o compilou como AFER_compl_never_becomes_post); (4) «nao ha posto parcial» nao tem termo e, lido sobre operadores, e' FALSO:
the_power_has_two_fixed_points e' sobre ESCALARES (μ ∈ ℂ); idempotentes intermediarios existem (o proprio PFmic; compl_mul_compl prova que 1-P tambem e'
idempotente) -- «posto parcial» e' leitura [ONTO] sobre o peso; (5) «Logo» apresentava leitura como deducao; (6) «Tornar-se Posto» entre «» no titulo nao
e' verbatim (o de 17/09 e' «tornou-se Posto»); (7) «prova de cada parte» ambiguo; (8) no handoff v384 faltava a etiqueta [INPUT] nas duas decisoes.
So acrescimo; marcador; backup de BYTES; temporario -> conferir -> substituir; idempotente. Reescreve tambem o registro JSON do scratchpad (ao lado)."""
import json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
MP = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes"); UMEM = os.path.join(MP, "memory")
ATLAS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory", "TGL_ATLAS.md")
MARCA = "errata_leitura_05out_b_v385"
J = os.path.join(HERE, "decisoes_operador_05out_b_v385.json")
R = json.load(open(J, encoding="utf-8"))
T3 = R["partes"][2]
assert "a forma falsa, deixa de ter conteúdo por construção" in T3, "a virgula nao esta no verbatim?"
ERRATA = (
    "**ERRATA AO LADO (05/10/2026, tarde; gerência, em nome próprio; achados da verificação adversarial do bloco acima, 3 lentes, verbatim no scratchpad "
    "`v385\\afericao_decisoes_b\\`):** a frase do operador (verbatim, [INPUT/ONTO]) está íntegra; os defeitos são da LEITURA da gerência. "
    "(1) A sub-citação (b) perdeu a vírgula do original: leia-se «a forma falsa, deixa de ter conteúdo por construção». "
    "(2) Em (a), o «→ 0» estava colado a `axiomFlow_gradient`, que é SÓ a igualdade F(t)(1 − P) = e^(−t)(1 − P); que e^(−t) → 0 é `Real.tendsto_exp_neg_atTop_nhds_zero` "
    "(Mathlib, [KNOWN]), e «F(t)(1 − P) → 0» é corolário SEM termo próprio na pedra (derivável; não citar como termo). "
    "(3) «o complemento nunca vira posto» não tem termo na pedra: é corolário de `compl_mul_post` + idempotência, com P ≠ 0 (derivável; o verificador o compilou no sandbox "
    "como `AFER_compl_never_becomes_post`, fora da pedra) — fica como leitura, dita como leitura. "
    "(4) Em (d), «não há terceiro valor nem posto parcial» lê demais: `the_power_has_two_fixed_points` é sobre ESCALARES (μ ∈ ℂ: μ² = μ ⟺ μ ∈ {0, 1}); sobre operadores o "
    "análogo é FALSO — idempotentes intermediários existem (o próprio `PFmic C`; `compl_mul_compl` prova que 1 − P também é idempotente); «posto parcial» é leitura [ONTO] "
    "sobre o peso do Nome, não teorema. "
    "(5) O «Logo» da conclusão apresentava leitura como dedução: leia-se «Leitura:» — a reconciliação das duas frases é do PRÓPRIO operador («em nada se opõe»), não de termo da pedra; "
    "e à lista das leituras [INPUT/ONTO] somam-se «a forma falsa … conteúdo», «o complemento nunca vira posto» e «posto parcial». "
    "(6) No título do bloco, «Tornar-se Posto» entre «» não é verbatim de fonte alguma: o de 17/09 (v365) é «tornou-se Posto»; o de 05/10 é «torna-se» / «tornar». "
    "(7) «o que a pedra prova de cada parte» leia-se «o que a pedra prova, parte a parte, da álgebra que o operador lê». "
    "O que a pedra prova e a leitura cita CERTO: `axiomFlow_fixes_the_post` (F(t)P = P = P·F(t), ∀t), `axiomFlow_gradient` (a igualdade), `compl_mul_post` ((1 − P)P = 0), "
    "`post_mul_compl` (P(1 − P) = 0), `the_reading_has_two_fixed_points` (√x = x ⟺ x ∈ {0, 1}, x ≥ 0), `the_zero_is_the_false_witness` (√0 = 0 ∧ …), "
    "`the_post_is_the_modular_zero`, `axiomFlow_tendsto_the_post` (F(t) → P), `the_power_has_two_fixed_points` (escalares). PROVADA ≠ CONFIRMADA; a leitura segue [ONTO], a ratificar.")
ERRATA_HANDOFF = ("**ERRATA AO LADO (05/10/2026, tarde; gerência, em nome próprio):** as duas decisões verbatim do bloco acima são do operador, [INPUT]; a leitura ontológica da "
                  "terceira está, com a sua própria errata ao lado, em [[um-posto-jamais-pressuposto-e-h2-17set]] (blocos `decisoes_operador_05out_b_v385` e `%s`)." % MARCA)
st = time.strftime("%Y%m%d_%H%M%S")
for p, bloco in ((os.path.join(UMEM, "um-posto-jamais-pressuposto-e-h2-17set.md"), ERRATA), (ATLAS, ERRATA), (os.path.join(UMEM, "handoff-v384-custodia.md"), ERRATA_HANDOFF)):
    raw = open(p, "rb").read()
    if ("<!-- %s -->" % MARCA).encode() in raw:
        print("JA ESTA", os.path.basename(p)); continue
    nl = "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"
    corpo = (nl + nl + "<!-- %s -->" % MARCA + nl + bloco + nl).encode("utf-8")
    if not raw.endswith(nl.encode()):
        corpo = nl.encode() + corpo
    novo = raw + corpo
    bak = p + ".bak_" + st + "_err05b"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw); os.replace(p + ".tmp", p); assert open(p, "rb").read()[:len(raw)] == raw
    print("OK", os.path.basename(p), len(raw), "->", len(novo))
R["leitura_da_gerencia_ONTO__ORIGINAL_COM_DEFEITOS"] = R.pop("leitura_da_gerencia_ONTO")
R["errata_da_leitura"] = ERRATA; R["marca_errata"] = MARCA
open(J + ".bak_" + st, "wb").write(open(J, "rb").read())
json.dump(R, open(J + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(J + ".tmp", J)
print("registro reescrito ao lado:", os.path.basename(J))
