# -*- coding: utf-8 -*-
"""ajuste unico (v401): o registro falsidade_da_inercia_v401 ganha as 3 checagens da CADEIA DERIVADA (a extensao da pedra de 25/10): f7 (a inercia nao e' causa de si mesma), f8 (o zero e' a consequencia da poda: infimo, nunca estado da orbita; o vazamento fica abaixo de todo epsilon),
f9 (a tensao projetada no atrator: o fluxo diagonal e' a escala dual; a coordenada com gap vai a zero no limite e e' diferente de zero em tempo finito; a sem gap e' o equilibrio), e a hipotese NOMEADA H_tau [OPEN] (nenhum teorema a usa)."""
import ast, sys
sys.stdout.reconfigure(encoding="utf-8")
P = "runtime_v401.py"
t = open(P, encoding="utf-8", newline="").read()
assert "ck_(\"f7\"" not in t


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n)
    t = t.replace(old, new)


sub('    vals_ = {"beta": beta_, "grid_scales": len(esc_),', '''    # ---- a CADEIA DERIVADA (a extensao da pedra, 25/10): nada que porte posto precede a impressao; a inercia nao e' causa de si mesma; o zero e' a consequencia da poda; a tensao projetada no atrator
    neg_ = [s_ for s_ in esc_ if s_ < 0.0]; pos_ = [s_ for s_ in esc_ if s_ > 0.0]
    ck_("f7", "[DERIVED] a inercia NAO e' causa de si mesma (inertia_is_not_its_own_cause; no_post_before_the_impression; the_first_motion_is_the_impression): nos estados de teste nao nulos, NENHUM e' fixo em toda escala negativa (o que seria fixo desde sempre), nem em toda escala positiva; o unico fixo e' o nulo e pesa zero; e o posto se move em TODA escala nao trivial, voltando ao peso 1 so' na impressao (a = 0)",
        all(any(theta_(s_, x_) != x_ for s_ in neg_) and any(theta_(s_, x_) != x_ for s_ in pos_) for x_ in xs_ if x_ != 0.0) and all(theta_(s_, 0.0) == 0.0 for s_ in esc_) and all(theta_(s_, 1.0) != 1.0 for s_ in esc_nz_) and [a_ for a_ in esc_ if peso_(a_) == 1.0] == [0.0], [len(neg_), len(pos_)])
    eps_ = (1e-3, 1e-6, 1e-12, 1e-30)
    queda_ = [(e_, -_m401.log(e_) + 1.0) for e_ in eps_]                               # o testemunho de abismo: o peso e^{-s} fica abaixo de e_ em s = -ln(e_) + 1
    vaza_ = [(e_, (1.0 / e_) / (beta_ * 0.5)) for e_ in (0.5, 0.1, 0.02, 0.01)]                            # o testemunho de leak_below_every_epsilon com g = 1/2: t = (1/e_) / (beta g)
    ck_("f8", "[DERIVED] o ZERO E' A CONSEQUENCIA DA PODA (the_zero_is_the_consequence_of_the_pruning; the_fall_never_lands; abismo; leak_below_every_epsilon): o peso do posto e^{-s} e' estritamente positivo em toda a grade (o zero nunca e' estado da orbita), desce abaixo de todo epsilon testado (%s) em s = -ln(epsilon) + 1, "
        "e o vazamento e^{-t beta g} e' estritamente positivo e fica abaixo de cada epsilon no t = (1/epsilon)/(beta g) do testemunho do kernel (g = 1/2, epsilon em 0,5; 0,1; 0,02; 0,01: abaixo disso e^{-1/epsilon} underflowa em dupla precisao)" % (list(eps_),),
        all(peso_(s_) > 0.0 for s_ in esc_) and all(_m401.exp(-s_) < e_ for e_, s_ in queda_) and all(t_ > 0.0 and 0.0 < _m401.exp(-(t_ * beta_ * 0.5)) < e_ for e_, t_ in vaza_), [len(queda_), len(vaza_)])
    dgap_ = (0.0, 0.5, 1.3); x0_ = (2.0, -1.0, 0.75)
    fluxo_ = lambda t_, i_: _m401.exp(-(t_ * beta_ * dgap_[i_])) * x0_[i_]                 # diagFlow beta d t x i = e^{-t beta d_i} x_i
    ck_("f9", "[DERIVED] a TENSAO PROJETADA NO ATRATOR (the_tension_is_projected_onto_the_attractor; diagFlow_coordinate_is_the_scaling): o fluxo diagonal e' a escala dual na escala s = t.beta.d_i (e^{-t beta d_i} x_i == theta_s x_i); a coordenada com gap d_i != 0 e' podada ate' zero no limite (t = 1e9/beta: |fluxo| < 1e-12) e e' DIFERENTE de zero em todo t finito testado; a coordenada com d_i = 0 e' o equilibrio, fixa em todo t",
        all(fluxo_(t_, i_) == theta_(t_ * beta_ * dgap_[i_], x0_[i_]) for t_ in (0.0, 1.0, 10.0, 100.0) for i_ in range(3)) and all(abs(fluxo_(1e9 / beta_, i_)) < 1e-12 for i_ in (1, 2)) and all(fluxo_(t_, i_) != 0.0 for t_ in (0.0, 1.0, 10.0, 100.0) for i_ in (1, 2))
        and all(fluxo_(t_, 0) == x0_[0] for t_ in (0.0, 1.0, 10.0, 100.0, 1e9)), [dgap_, x0_])
    vals_ = {"beta": beta_, "grid_scales": len(esc_),''')
sub('"dephasing_factor_at_t1_g1": _m401.exp(-beta_), "loss_per_unit": 1.0 - _m401.exp(-beta_)}', '"dephasing_factor_at_t1_g1": _m401.exp(-beta_), "loss_per_unit": 1.0 - _m401.exp(-beta_),\n             "min_weight_on_the_grid_positive": min(peso_(s_) for s_ in esc_), "abyss_witnesses": [[e_, s_] for e_, s_ in queda_], "leak_witnesses_g_half": [[e_, t_] for e_, t_ in vaza_], "diag_flow_gap_zero_is_fixed": fluxo_(1e9, 0) == x0_[0], "diag_flow_gap_pruned_at_1e9_over_beta": [abs(fluxo_(1e9 / beta_, i_)) for i_ in (1, 2)]}')
# a hipotese nomeada H_tau e o estatuto da cadeia
sub('"definition_of_the_operator": "inertia = the absolute zero (0_abs, 1=0); w(I) = 1 is the posted One that interrupts it (1=1)",', '"definition_of_the_operator": "inertia = the absolute zero (0_abs, 1=0); w(I) = 1 is the posted One that interrupts it (1=1)",\n            "chain_status": "DERIVED from the axiom w(I)=1 and Takesaki\'s scaling law (KNOWN, a field of the structure); nothing precedes the impression of the posted One", "named_hypothesis": {"name": "H_tau", "status": "OPEN", "content": "tau is Newton\'s mass and Einstein\'s metric", "used_by_a_theorem": False, "pending_external": "ORDEM 025 to Codex (sha16 3fd2b5a801071343): types it by the Bisognano-Wichmann light front"},', 1)
ast.parse(t)
open(P, "w", encoding="utf-8", newline="").write(t)
print("ok", P)
