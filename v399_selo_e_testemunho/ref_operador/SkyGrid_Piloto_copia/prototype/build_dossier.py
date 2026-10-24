#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_dossier.py — ESTAGIO H. Gera o dossie de engenharia DO CODIGO VIVO.

Forma = conteudo: as especificacoes por componente vem dos .spec() dos modulos
reais e dos manifestos das rodadas — nao de numeros digitados. Escreve:

  prototype/component_specs.json   especificacoes vivas por componente
  prototype/power_budget.json      orcamento de potencia da cadeia (por sat)

O texto humano (DOSSIE_ENGENHARIA.md) referencia estes JSONs.
Tudo [SIM]; specs fisicas de bancada marcadas [HARDWARE]; sem veredito fisico.
"""

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from skygrid_sim import tgl_core                                   # noqa: E402
from skygrid_physics.field_reservoir import FieldReservoir         # noqa: E402
from skygrid_physics.coupling import ResonantCoupler               # noqa: E402
from skygrid_physics.conversion import DipoloConverter             # noqa: E402
from skygrid_physics.transmission import PsiPowerLink              # noqa: E402
from skygrid_physics.storage import ReversalCellStore              # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    res = FieldReservoir()
    cpl = ResonantCoupler()
    cnv = DipoloConverter()
    lnk = PsiPowerLink()
    sto = ReversalCellStore()

    specs = {
        "marker": "[SIM] specs do modelo vivo; bancada = [HARDWARE]",
        "beta_runtime": tgl_core.beta(),
        "theta_M_deg": __import__("math").degrees(tgl_core.theta_m()),
        "ExtractorSat": {
            "reservoir_patch": res.state(),
            "coupler_OH": cpl.spec(),
            "converter_dipolo": cnv.spec(),
            "patents": ["BR 10 2026 003456-8 (Fusao a Frio/OH)",
                        "BR 10 2026 004688-4 (Dipolo Transistor)"],
        },
        "PsiLink": {"spec": lnk.spec(),
                    "patents": ["BR 10 2026 003453-3 (Psi-NET)",
                                "BR 10 2026 003450-9 (Supercondutor) [HARDWARE]",
                                "BR 10 2026 003452-5 (Motor de Dobra) [HARDWARE]"]},
        "GroundBase": {"storage_cell": sto.state(),
                       "patents": ["BR 10 2026 004849-6 (Celula de Reversao)"]},
        "Control": {"iald_budget_steps": int(__import__("math").ceil(
                        100.0 / tgl_core.beta())),
                    "quorum": {"min_validators": 3, "threshold": 0.67},
                    "patents": ["BR 10 2026 003443-6 (IALD/GKSL)",
                                "BR 10 2026 006129-8 (Kernel)",
                                "BR 10 2026 005477-1 (Aprendizado Continuo)"]},
        "physical_verdict_allowed": False,
    }

    # orcamento de potencia por satelite na cadeia default (medio) [SIM]
    P_avail = res.S_field * res.A_cap * 0.8          # disponibilidade media
    eta_c = cpl.eta_couple()
    P_in = eta_c * P_avail
    eta_conv = cnv.eta_conv * cnv.eta_quant
    P_conv = eta_conv * P_in
    eta_link3 = lnk.eta_link(3)
    P_rx = eta_link3 * P_conv
    eta_rt = sto.eta_rt
    budget = {
        "marker": "[SIM] cadeia default por satelite; parametros [CONJ]",
        "P_available_mean_W": P_avail,
        "stages": [
            {"stage": "acoplamento OH", "eta": eta_c,
             "components": {"1-beta": cpl.aperture, "eta_res": 1.0,
                            "eta_geo": cpl.eta_geo},
             "P_out_W": P_in},
            {"stage": "conversao dipolo", "eta": eta_conv, "P_out_W": P_conv},
            {"stage": "enlace Psi (3 hops)", "eta": eta_link3, "P_out_W": P_rx},
            {"stage": "armazenamento (round-trip, fracao armazenada)",
             "eta": eta_rt, "P_out_W_if_stored": P_rx * eta_rt},
        ],
        "halfnat_overhead_W": cpl.halfnat_power_W(),
        "eta_chain_direct": eta_c * eta_conv * eta_link3,
        "physical_verdict_allowed": False,
    }

    with open(os.path.join(HERE, "component_specs.json"), "w",
              encoding="utf-8") as f:
        json.dump(specs, f, indent=1, ensure_ascii=False, default=float)
    with open(os.path.join(HERE, "power_budget.json"), "w",
              encoding="utf-8") as f:
        json.dump(budget, f, indent=1, ensure_ascii=False, default=float)
    print("dossie: component_specs.json + power_budget.json gerados")
    print("cadeia direta por sat: eta=%.4f  P_rx=%.1f W de %.0f W disponiveis"
          % (budget["eta_chain_direct"], P_rx, P_avail))


if __name__ == "__main__":
    main()
