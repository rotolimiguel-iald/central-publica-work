#!/usr/bin/env python3
"""Inventário reproduzível de escalas de energia para ORDEM_KIMI_E0_01_31out.

Não compara nenhuma escala com um alvo experimental. Os valores de m2 são
somente a transformação aritmética m2 = U*alpha*exp(1/2)*sin(pi/4).
"""

import json
import math
from pathlib import Path


ALPHA = 7.2973525693e-3
H = 6.62607015e-34
HBAR = H / (2.0 * math.pi)
C = 299792458.0
M_EC2_EV = 510998.95
HARTREE_EV = 27.211386245988
RYDBERG_EV = 13.605693122994
A0_M = 5.29177210903e-11
R_E_M = 2.8179403262e-15
KB = 1.380649e-23
E_EV = 1.602176634e-19
G = 6.67430e-11
TP_S = 5.391247e-44

DIRAC_EV = M_EC2_EV * (1.0 - math.sqrt(1.0 - ALPHA**2))
T_U_K = 11604.5181
T_CMB_K = 2.72548
R0_FACTOR = 27.2114
R_FIXO_M = 1.43996e-9

M2_FACTOR = ALPHA * math.exp(0.5) * math.sin(math.pi / 4.0)


def coulomb_ev(radius_m: float) -> float:
    """Energia Coulombiana alpha*hbar*c/r, expressa em eV."""
    return ALPHA * HBAR * C / (radius_m * E_EV)


def entrada_energia(
    identificador: str,
    quantidade: str,
    status: str,
    u_ev: float,
    formula: str,
    **extra: object,
) -> dict[str, object]:
    """Cria uma entrada de energia e aplica a fórmula comum de m2."""
    entrada: dict[str, object] = {
        "id": identificador,
        "quantidade": quantidade,
        "status": status,
        "formula_U_eV": formula,
        "U_eV": u_ev,
        "m2_eV": u_ev * M2_FACTOR,
        "m2_meV": 1000.0 * u_ev * M2_FACTOR,
    }
    entrada.update(extra)
    return entrada


def construir_inventario() -> dict[str, object]:
    """Calcula todas as escalas sem usar qualquer alvo experimental."""
    hartree_calc = ALPHA**2 * M_EC2_EV
    rydberg_calc = hartree_calc / 2.0
    r0_m = R0_FACTOR * A0_M
    planck_energy_j = math.sqrt(HBAR * C**5 / G)
    native_planck_ev = planck_energy_j / (4.0 * math.pi * E_EV)

    # As constantes tabeladas fornecidas servem como controle de precisão,
    # não como alvo de seleção de escala. A tolerância acomoda o arredondamento
    # independente de alpha, m_ec2, Hartree e Rydberg nas entradas fornecidas.
    assert math.isclose(hartree_calc, HARTREE_EV, rel_tol=1.0e-11)
    assert math.isclose(rydberg_calc, RYDBERG_EV, rel_tol=1.0e-11)

    energias = [
        entrada_energia(
            "hartree",
            "Energia de Hartree",
            "derived",
            hartree_calc,
            "alpha^2 * m_ec2",
            valor_tabelado_eV=HARTREE_EV,
        ),
        entrada_energia(
            "rydberg",
            "Energia de Rydberg",
            "derived",
            rydberg_calc,
            "alpha^2 * m_ec2 / 2 = Hartree / 2",
            valor_tabelado_eV=RYDBERG_EV,
        ),
        entrada_energia(
            "repouso_eletron",
            "Energia de repouso do elétron",
            "known",
            M_EC2_EV,
            "m_ec2",
        ),
        entrada_energia(
            "alpha3_mec2",
            "Terceira potência de alpha vezes a energia de repouso do elétron",
            "open",
            ALPHA**3 * M_EC2_EV,
            "alpha^3 * m_ec2",
        ),
        entrada_energia(
            "alpha4_mec2",
            "Quarta potência de alpha vezes a energia de repouso do elétron",
            "open",
            ALPHA**4 * M_EC2_EV,
            "alpha^4 * m_ec2",
        ),
        entrada_energia(
            "dirac",
            "Energia de Dirac fornecida",
            "derived",
            DIRAC_EV,
            "m_ec2 * (1 - sqrt(1 - alpha^2))",
        ),
        entrada_energia(
            "coulomb_a0",
            "Energia Coulombiana no raio de Bohr",
            "derived",
            coulomb_ev(A0_M),
            "alpha * hbar * c / (a0 * E_eV)",
            comprimento_m=A0_M,
        ),
        entrada_energia(
            "coulomb_re",
            "Energia Coulombiana no raio clássico do elétron",
            "derived",
            coulomb_ev(R_E_M),
            "alpha * hbar * c / (r_e * E_eV)",
            comprimento_m=R_E_M,
        ),
        entrada_energia(
            "coulomb_r0",
            "Energia Coulombiana na normalização r0",
            "target-chosen",
            coulomb_ev(r0_m),
            "alpha * hbar * c / (r0 * E_eV), r0 = 27.2114 * a0",
            comprimento_m=r0_m,
            dependencia="r0",
        ),
        entrada_energia(
            "coulomb_1_43996_nm",
            "Energia Coulombiana em 1.43996 nm",
            "target-chosen",
            coulomb_ev(R_FIXO_M),
            "alpha * hbar * c / ((1.43996 nm) * E_eV)",
            comprimento_m=R_FIXO_M,
        ),
        entrada_energia(
            "kB_T_U",
            "Energia térmica na temperatura de Unruh normalizada",
            "target-chosen",
            KB * T_U_K / E_EV,
            "kB * T_U / E_eV",
            temperatura_K=T_U_K,
            normalizacao="T_U fornecida; não derivada neste inventário",
        ),
        entrada_energia(
            "kB_T_CMB",
            "Energia térmica na temperatura CMB fornecida",
            "open",
            KB * T_CMB_K / E_EV,
            "kB * T_CMB / E_eV",
            temperatura_K=T_CMB_K,
        ),
        entrada_energia(
            "landauer_CMB_ln2",
            "Energia de Landauer ln(2) na temperatura CMB fornecida",
            "open",
            KB * T_CMB_K * math.log(2.0) / E_EV,
            "kB * T_CMB * ln(2) / E_eV",
            temperatura_K=T_CMB_K,
        ),
        entrada_energia(
            "planck_nativo_sobre_4pi",
            "Energia de Planck nativa dividida por 4pi",
            "conditional",
            native_planck_ev,
            "sqrt(hbar * c^5 / G) / (4pi * E_eV)",
            condicao="ramo nativo de Planck; não identificado automaticamente a E0",
        ),
    ]

    return {
        "ordem": "ORDEM_KIMI_E0_01_31out",
        "descricao": "Inventário de unidades e escalas candidatas para E0",
        "escopo": {
            "comparacao_com_alvo": "nao_realizada",
            "escala_absoluta_E0": "U_E_NOT_DERIVED",
            "m2_eh_previsao_independente": False,
            "nota": (
                "m2 é calculado apenas pela transformação aritmética de cada U; "
                "nenhuma escala condicional ou escolhida é promovida a derivação de E0."
            ),
        },
        "constantes": {
            "alpha": {"valor": ALPHA, "unidade": "1", "status": "known"},
            "h": {"valor": H, "unidade": "J s", "status": "known"},
            "hbar": {
                "valor": HBAR,
                "unidade": "J s",
                "status": "derived",
                "formula": "h/(2*pi)",
            },
            "c": {"valor": C, "unidade": "m/s", "status": "known"},
            "m_ec2": {"valor": M_EC2_EV, "unidade": "eV", "status": "known"},
            "Hartree": {"valor": HARTREE_EV, "unidade": "eV", "status": "known"},
            "Rydberg": {"valor": RYDBERG_EV, "unidade": "eV", "status": "known"},
            "a0": {"valor": A0_M, "unidade": "m", "status": "known"},
            "r_e": {"valor": R_E_M, "unidade": "m", "status": "known"},
            "kB": {"valor": KB, "unidade": "J/K", "status": "known"},
            "E_eV": {"valor": E_EV, "unidade": "J/eV", "status": "known"},
            "G": {"valor": G, "unidade": "m^3/(kg s^2)", "status": "known"},
            "tP": {"valor": TP_S, "unidade": "s", "status": "known"},
        },
        "convencoes": {
            "energia_coulombiana_J": "alpha * hbar * c / r",
            "formula_m2": "m2 = U * alpha * exp(0.5) * sin(pi/4)",
            "fator_m2_por_U": M2_FACTOR,
            "unidade_de_U_e_m2": "eV",
            "ln2": math.log(2.0),
        },
        "potencias_alpha_adimensionais": {
            "alpha^3": ALPHA**3,
            "alpha^4": ALPHA**4,
        },
        "comprimentos": [
            {
                "id": "r0",
                "quantidade": "Comprimento de normalização r0",
                "status": "target-chosen",
                "formula": "27.2114 * a0",
                "valor_m": r0_m,
                "valor_nm": r0_m * 1.0e9,
            },
            {
                "id": "r_fixo_1_43996_nm",
                "quantidade": "Comprimento fornecido para avaliação Coulombiana",
                "status": "target-chosen",
                "valor_m": R_FIXO_M,
                "valor_nm": R_FIXO_M * 1.0e9,
            },
        ],
        "temperaturas": [
            {
                "id": "T_U",
                "quantidade": "Temperatura de Unruh normalizada",
                "status": "target-chosen",
                "valor_K": T_U_K,
            },
            {
                "id": "T_CMB",
                "quantidade": "Temperatura CMB fornecida",
                "status": "known",
                "valor_K": T_CMB_K,
            },
        ],
        "escalas_energia": energias,
    }


def main() -> None:
    destino = Path(__file__).resolve().with_name("inventario_unidades_e0.json")
    inventario = construir_inventario()
    with destino.open("w", encoding="utf-8", newline="\n") as arquivo:
        json.dump(inventario, arquivo, ensure_ascii=False, indent=2, allow_nan=False)
        arquivo.write("\n")
    print(f"JSON gravado: {destino}")
    print(f"Escalas de energia: {len(inventario['escalas_energia'])}")
    print(f"Fator m2/U: {M2_FACTOR:.15e}")


if __name__ == "__main__":
    main()
