# -*- coding: utf-8 -*-
"""Entradas SINTETICAS (fabricadas) que exercem cada ramo da funcao de veredito V2-c1. Nenhum centro observado."""
import copy
import math

BASE_SUFFIX = "__D1B__FUNDO_BG1__NOT_BLIND_TO_DATA_STATED__NOT_A_CONFIRMATION__GATE_UNTOUCHED"
TB = "TGL_FASE9_V2_A_UNICA_PALAVRA_BETA_TGL__"


def base():
    return {
        "fundo": "BG1", "n_local": 5, "n_alvos_declarados": 0, "required_sources_admitted": True, "beta_livre_no_limite": False,
        "dispersao_endpoints": {"minimum": {"chi2_por_gl": 0.8, "p": 0.5}, "maximum": {"chi2_por_gl": 0.6, "p": 0.7}},
        "minimum": {"z_delta": 0.5, "sigma_z_por_alvo": [(1.04, 0.3), (1.9, -0.2), (2.4, 0.1), (3.05, 0.0), (3.6, 0.2)]},
        "maximum": {"poder_previo": 5.72, "z_disc": 6.2, "lnB_lcdm": 12.0, "lnB_livre": 2.0, "lnB_shift": 3.0, "lnB_fundo_livre": 2.0, "poder_nao_cefeida": 3.9},
        "use_novel_parametros": True,
    }


def mut(f):
    r = base()
    f(r)
    return r


BRANCHES = {
    "baseline_discriminates": (base(), "NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_6SIGMA__ZERO_FREE_PARAMETERS__USE_NOVEL"),
    "inventory_pending": (mut(lambda r: r.update(n_alvos_declarados=2)), "INCONCLUSIVE_SYSTEMATICS"),
    "source_admission_pending": (mut(lambda r: r.update(required_sources_admitted=False)), "INCONCLUSIVE_SYSTEMATICS"),
    "beta_prior_edge": (mut(lambda r: r.update(beta_livre_no_limite=True)), "INCONCLUSIVE_SYSTEMATICS"),
    "dispersion_high_chi2": (mut(lambda r: r["dispersao_endpoints"]["maximum"].update(chi2_por_gl=2.5)), "INCONCLUSIVE_SYSTEMATICS"),
    "dispersion_low_p": (mut(lambda r: r["dispersao_endpoints"]["minimum"].update(p=0.005)), "INCONCLUSIVE_SYSTEMATICS"),
    "dispersion_missing": (mut(lambda r: r.pop("dispersao_endpoints")), "INCONCLUSIVE_SYSTEMATICS"),
    "dispersion_one_endpoint": (mut(lambda r: r["dispersao_endpoints"].pop("maximum")), "INCONCLUSIVE_SYSTEMATICS"),
    "dispersion_missing_p": (mut(lambda r: r["dispersao_endpoints"]["minimum"].pop("p")), "INCONCLUSIVE_SYSTEMATICS"),
    "falsification": (mut(lambda r: r["minimum"].update(z_delta=-5.2)), "FALSIFIED_AT_5SIGMA"),
    "falsification_positive_side": (mut(lambda r: r["minimum"].update(z_delta=5.0)), "FALSIFIED_AT_5SIGMA"),
    "falsification_single_reader": (mut(lambda r: r["minimum"].update(sigma_z_por_alvo=[(0.93, 5.1), (1.9, 0.0)])), "FALSIFIED_AT_5SIGMA"),
    "single_reader_sigma_above_1_no_trigger": (mut(lambda r: r["minimum"].update(sigma_z_por_alvo=[(1.04, 6.0), (1.9, 0.0)])), "DISCRIMINATES"),
    "tension": (mut(lambda r: r["minimum"].update(z_delta=3.5)), "TENSION_3_TO_5_SIGMA"),
    "power_truncation_4.95": (mut(lambda r: r["maximum"].update(poder_previo=4.95)), "NOT_FALSIFIED_UNDERPOWERED__POWER_P4P9_OF_5_SIGMA"),
    "power_truncation_4.9999": (mut(lambda r: r["maximum"].update(poder_previo=4.9999)), "NOT_FALSIFIED_UNDERPOWERED__POWER_P4P9_OF_5_SIGMA"),
    "power_boundary_5": (mut(lambda r: r["maximum"].update(poder_previo=5.0)), "DISCRIMINATES"),
    "free_background_suffix": (mut(lambda r: r["maximum"].update(lnB_fundo_livre=0.5)), "__NOT_DISCRIMINATED_FROM_FREE_BACKGROUND"),
    "ladder_suffix": (mut(lambda r: r["maximum"].update(lnB_shift=-1.0, poder_nao_cefeida=5.1)), "__NOT_DISCRIMINATED_FROM_LADDER_SYSTEMATIC"),
    "z_below_5": (mut(lambda r: r["maximum"].update(z_disc=4.6)), "NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY"),
    "lnB_below_5_at_z6": (mut(lambda r: r["maximum"].update(lnB_lcdm=4.0)), "NOT_DISCRIMINATED_FROM_LCDM_LNB_BELOW_5"),
    "lnB_free_below_minus_1": (mut(lambda r: r["maximum"].update(lnB_livre=-1.5)), "NOT_DISCRIMINATED_FROM_LCDM_BETA_FREE_LNB_BELOW_MINUS_1"),
    "deviation_1_to_3": (mut(lambda r: (r["minimum"].update(z_delta=2.0), r["maximum"].update(z_disc=4.0))), "DEVIATION_1_TO_3_SIGMA"),
    "one_reader_no_dispersion": (mut(lambda r: (r.update(n_local=1), r.pop("dispersao_endpoints"), r["minimum"].update(sigma_z_por_alvo=[(1.9, 0.1)]))), "DISCRIMINATES"),
}

NUMERIC_GUARDS = {
    "poder_previo_nan": lambda r: r["maximum"].update(poder_previo=math.nan),
    "poder_previo_bool": lambda r: r["maximum"].update(poder_previo=True),
    "z_disc_nan": lambda r: r["maximum"].update(z_disc=math.nan),
    "z_disc_bool": lambda r: r["maximum"].update(z_disc=True),
    "lnB_lcdm_nan": lambda r: r["maximum"].update(lnB_lcdm=math.nan),
    "lnB_livre_nan": lambda r: r["maximum"].update(lnB_livre=math.nan),
    "lnB_shift_nan": lambda r: r["maximum"].update(lnB_shift=math.nan),
    "lnB_fundo_livre_nan": lambda r: r["maximum"].update(lnB_fundo_livre=math.nan),
    "poder_nao_cefeida_nan": lambda r: r["maximum"].update(poder_nao_cefeida=math.nan),
    "z_delta_nan": lambda r: r["minimum"].update(z_delta=math.nan),
    "z_delta_bool": lambda r: r["minimum"].update(z_delta=False),
    "power_posinf": lambda r: r["maximum"].update(poder_previo=math.inf),
    "z_disc_neginf": lambda r: r["maximum"].update(z_disc=-math.inf),
    "n_local_bool": lambda r: r.update(n_local=True),
    "n_alvos_bool": lambda r: r.update(n_alvos_declarados=False),
    "chi2_bool": lambda r: r["dispersao_endpoints"]["minimum"].update(chi2_por_gl=True),
    "p_bool": lambda r: r["dispersao_endpoints"]["minimum"].update(p=True),
    "chi2_inf": lambda r: r["dispersao_endpoints"]["minimum"].update(chi2_por_gl=math.inf),
    "sigma_nan": lambda r: r["minimum"].update(sigma_z_por_alvo=[(math.nan, 0.0)]),
    "reader_z_bool": lambda r: r["minimum"].update(sigma_z_por_alvo=[(1.0, True)]),
    "unknown_numeric_inf": lambda r: r.update(extra_campo=math.inf),
    "invalid_p": lambda r: r["dispersao_endpoints"]["minimum"].update(p=1.5),
}


def numeric_case(name):
    r = base()
    NUMERIC_GUARDS[name](r)
    return r


def run_branches(fn):
    out = {}
    for name, (r, _) in BRANCHES.items():
        try:
            out[name] = fn(copy.deepcopy(r))
        except ValueError as e:
            out[name] = "ValueError:" + str(e)
    return out
