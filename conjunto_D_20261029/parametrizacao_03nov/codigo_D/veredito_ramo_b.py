# -*- coding: utf-8 -*-
"""veredito_ramo_b.py -- a FUNCAO DE VEREDITO do V1 do ramo B (conjunto D). Puro e deterministico: recebe numeros, devolve o token.

Por que NAO e gw_stack.veredito: aquela funcao consome o rito do ECO (leis MAY/KMS/DEC, recovery_R1/R2, a_on) e o prefixo TGL_ECHO_RADICAL_V3__, e pode devolver
DETECTED_AT_DELAY_LAW, que NAO esta entre os vereditos permitidos do V1. A "mesma funcao" que o V1 manda usar e a ORDEM da regra 2 da Fase 6, com as
constantes de preregistro_fase6.py (min_eventos 10; poder_min 5; z_excl 5; sistematica_max_relativa 0,3), e as 5 classes do V1:
  0 AWAITING_DATA (sem estimador selado por hash rodado sob este registro, sem dado aberto, ou n < 10 => sufixo INSUFFICIENT_SAMPLE)
  1 INCONCLUSIVE_SYSTEMATICS (C1-C9 reprovado, ou sist_rel > 0,3, ou chi2/dof > 3, ou primario x secundario discordam no rotulo)
  2 NOT_FALSIFIED_UNDERPOWERED (poder = |delta_bar_pred|/sigma_usado < 5; sufixo POWER_<x>_OF_5_SIGMA)
  3 FALSIFIED_AT_5SIGMA (z_excl = |delta_bar - delta_bar_pred|/sigma_usado >= 5: falsifica o PAR (k, M_X, identificacao) sob a lei; NAO a lei, NAO beta, NAO a TGL)
  4 NOT_FALSIFIED_POWERED (+ __GR_TENSION_REPORTED se |z_RG| >= 5; a tensao e RELATADA, nao vira CONFIRMED)
Proibidos: CONFIRMED, PROVED, PROVED_BY, QG confirmada.  Nenhum desfecho move o gate.
Escolha do desenho (dita ANTES): controle obrigatorio NOT_RUN (C1, C2, C5, C6, C9) => AWAITING_DATA__CONTROLS_NOT_RUN (fail-closed: nao se emite desfecho fisico sem os controles).
"""
BASE = "TGL_RAMO_B_RINGDOWN_V1__K_2PI_OVER_KAPPA_HAT_KMS__M_F_DET__ENVELOPE_ADDITIVE_RATE"
SET_D = "SET_D_O4_BLIND"
FIM = "GATE_UNTOUCHED"
PROIBIDOS = ("CONFIRMED", "PROVED", "PROVED_BY", "QG confirmada")
OBRIGATORIOS = ("C1", "C2", "C5", "C6", "C9")
STATUS_OK = ("PASS", "NOT_APPLICABLE")


def _p(x):
    return ("%.2f" % x).replace(".", "P").replace("-", "M")


def token(desfecho):
    t = "__".join([BASE, SET_D, desfecho, FIM])
    for pr in ("CONFIRMED", "PROVED"):
        if pr in t:
            raise AssertionError("token com palavra proibida: " + pr)
    return t


def veredito(ent, CR):
    """ent: n_eventos, estimador_selado (bool), dado_aberto (bool), controles {C1..C9: PASS|FAIL|NOT_APPLICABLE|NOT_RUN},
    sist_rel, chi2_dof, kde_discordancias (lista; vazia/None = sem), poder, z_excl, z_RG.   CR: min_eventos, poder_min, z_excl, sistematica_max_relativa.
    Devolve (token, desfecho, razoes)."""
    r = []
    n = ent["n_eventos"]
    if n < CR["min_eventos"]:
        r.append("n_eventos %d < %d" % (n, CR["min_eventos"]))
        return token("AWAITING_DATA__INSUFFICIENT_SAMPLE"), "AWAITING_DATA__INSUFFICIENT_SAMPLE", r
    if not ent["estimador_selado"] or not ent["dado_aberto"]:
        r.append("estimador selado por hash: %s; dado aberto: %s" % (ent["estimador_selado"], ent["dado_aberto"]))
        return token("AWAITING_DATA"), "AWAITING_DATA", r
    ctr = ent["controles"]
    faltam = [c for c in OBRIGATORIOS if ctr.get(c, "NOT_RUN") == "NOT_RUN"]
    if faltam:
        r.append("controles obrigatorios nao rodados: " + ",".join(faltam))
        return token("AWAITING_DATA__CONTROLS_NOT_RUN"), "AWAITING_DATA__CONTROLS_NOT_RUN", r
    # classe 1
    motivos = []
    for c, v in sorted(ctr.items()):
        if v == "FAIL":
            motivos.append("controle %s reprovado" % c)
    if ent["sist_rel"] > CR["sistematica_max_relativa"]:
        motivos.append("sist_rel %.3f > %.1f" % (ent["sist_rel"], CR["sistematica_max_relativa"]))
    if ent["chi2_dof"] > 3:
        motivos.append("chi2/dof %.2f > 3" % ent["chi2_dof"])
    if ent.get("kde_discordancias"):
        motivos.append("primario x secundario discordam no rotulo: " + ",".join(ent["kde_discordancias"]))
    if motivos:
        return token("INCONCLUSIVE_SYSTEMATICS"), "INCONCLUSIVE_SYSTEMATICS", motivos
    # classe 2
    if ent["poder"] < CR["poder_min"]:
        d = "NOT_FALSIFIED_UNDERPOWERED__POWER_%s_OF_5_SIGMA" % _p(ent["poder"])
        return token(d), d, ["poder %.2f < %.0f: o valor central NAO entra (regra 3 antes da 5)" % (ent["poder"], CR["poder_min"])]
    # classe 3
    if ent["z_excl"] >= CR["z_excl"]:
        return token("FALSIFIED_AT_5SIGMA"), "FALSIFIED_AT_5SIGMA", ["z_excl %.2f >= %.0f; poder %.2f; falsifica o PAR, nao a lei, nao beta, nao a TGL" % (ent["z_excl"], CR["z_excl"], ent["poder"])]
    # classe 4
    d = "NOT_FALSIFIED_POWERED"
    if abs(ent["z_RG"]) >= 5:
        d += "__GR_TENSION_REPORTED"
    return token(d), d, ["z_excl %.2f < %.0f; poder %.2f; |z_RG| %.2f" % (ent["z_excl"], CR["z_excl"], ent["poder"], abs(ent["z_RG"]))]
