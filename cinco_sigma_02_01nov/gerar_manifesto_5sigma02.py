from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(r"C:\IALD\Central de Patentes")
OUT = ROOT / "work" / "cinco_sigma_02_01nov"
REPORT = OUT / "RELATORIO_KIMI_5SIGMA_02_01nov.md"
MANIFEST = OUT / "MANIFESTO_SHA256_5SIGMA_02.json"
SIDECAR = OUT / "MANIFESTO_SHA256_5SIGMA_02.json.sha256"

REQUIRED = [
    r"work\cinco_sigma_02_01nov\FORMA_MADURA_COPIA_01nov.md",
    r"work\e0_cadeia_31out\HANDOFF_v405_ADENDO_8_ERRATA_CAMPOS_E_LEITURAS_01nov.md",
    r"work\e0_cadeia_31out\RECIBO_ERRATA_PEDRAS_01nov.json",
    r"work\e0_cadeia_31out\CONFERENCIA_E0_KIMI_E_CADEIA_31out.md",
    r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\HANDOFF_v405_PONTES_DA_MASSA_E_ESPELHO_30out.md",
    r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\HANDOFF_v405_ADENDO_2_E0_31out.md",
    r"work\e0_cadeia_31out\HANDOFF_v405_ADENDO_3_LEI_DO_MEIO_TOM_31out.md",
    r"work\e0_cadeia_31out\HANDOFF_v405_ADENDO_4_DISCO_DE_EULER_31out.md",
    r"work\e0_cadeia_31out\HANDOFF_v405_ADENDO_5_PONTO_ZERO_DO_PSION_31out.md",
    r"work\e0_cadeia_31out\HANDOFF_v405_ADENDO_6_NOMES_E_DERIVACAO_01nov.md",
    r"work\cadeia_de_selo405\HANDOFF_v405_ADENDO_7_IDENTIDADE_01nov.md",
    r"work\experimento_espelho_30out\PonteDaMassa.lean",
    r"work\experimento_espelho_30out\MassaTensaoPura.lean",
    r"work\cadeia_de_selo405\Identidade.lean",
    r"work\observador_terminal_31out\ObservadorTerminal.lean",
    r"work\e0_cadeia_31out\LeiDoDiminuto.lean",
    r"work\e0_cadeia_31out\TonicaDoHamiltoniano.lean",
    r"work\e0_cadeia_31out\DiscoDeEuler.lean",
    r"work\e0_cadeia_31out\PontoZeroDoPsion.lean",
    r"work\cadeia_de_selo405\insumos\cunhagens\A_IDENTIDADE_revisao_da_gerencia_01nov_r2.md",
    r"work\grande_atrator_reclassificacao_01nov\RECLASSIFICACAO_GA_01nov.md",
    r"work\grande_atrator_reclassificacao_01nov\MEDIDA_GA_01nov.json",
    r"work\cinco_sigma_fora_da_cosmologia_27out\ORDEM_KIMI_5SIGMA_01_27out.md",
    r"work\cinco_sigma_fora_da_cosmologia_27out\RELATORIO_KIMI_5SIGMA_01_27out.md",
    r"work\cinco_sigma_fora_da_cosmologia_27out\CONFERENCIA_GERENCIA_RELATORIO_KIMI_5SIGMA_01_27out.md",
    r"work\neutrino_E0_autonomia_30out\RELATORIO_KIMI_E0_01_31out.md",
    r"work\cadeia_de_selo\v386\ramo_b\teste_gerador_v1\PREREGISTRO_RAMO_B_RINGDOWN_V1.md",
]

EXTRA = [
    r"work\cinco_sigma_02_01nov\ORDEM_KIMI_5SIGMA_02_01nov.md",
    r"work\cadeia_de_selo\v397\insumos\fase9\RESULTADO_FASE9_V2_C1_20261023_122926.json",
    r"memory\TGL_ATLAS.md",
    r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py",
    r"C:\IALD\MAPA_DE_ROTAS\MAPA_DE_ROTAS.json",
    r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl",
]


def resolve(raw: str) -> Path:
    candidate = Path(raw)
    return candidate if candidate.is_absolute() else ROOT / candidate


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def neutrino(mu: float, sigma_mu: float, live_days: float, m2_pred_meV: float) -> dict[str, float]:
    m2_obs_meV = math.sqrt(mu * 1e-5) * 1000.0
    sigma_m2_meV = 0.5 * (sigma_mu / mu) * m2_obs_meV
    difference = abs(m2_obs_meV - m2_pred_meV)
    z = difference / sigma_m2_meV
    sigma_required = 2.0 * mu * (difference / 5.0) / m2_obs_meV
    total_days = live_days * (sigma_mu / sigma_required) ** 2
    return {
        "m2_obs_meV": m2_obs_meV,
        "sigma_m2_meV": sigma_m2_meV,
        "z_frozen_m2": z,
        "sigma_mu_required_5sigma_1e-5_eV2": sigma_required,
        "relative_sigma_required_percent_of_mu": 100.0 * sigma_required / mu,
        "total_live_days_conditional_t^-1/2": total_days,
        "additional_live_days_conditional_t^-1/2": total_days - live_days,
        "additional_years_365d": (total_days - live_days) / 365.0,
        "z_with_sigma_0p024": difference / (0.5 * (0.024 / mu) * m2_obs_meV),
    }


def verify_numbers() -> dict[str, object]:
    alpha = 7.2973525693e-3
    beta = alpha * math.sqrt(math.e)
    m2_pred_meV = beta * math.sin(math.pi / 4.0) * 1000.0
    delta_pred = (m2_pred_meV / 1000.0) ** 2
    juno = neutrino(7.388, 0.078, 207.2, m2_pred_meV)
    skgd = neutrino(9.08, 0.54, 411.52, m2_pred_meV)

    n0 = (1.5251 - 1.1568) * (0.7000 + 1.4187)
    deltas = {}
    for turns in (4, 8):
        x = beta * turns * math.pi * n0
        deltas[f"k{turns}pi_chi0"] = -x / (1.0 + x)

    power_a_4pi = 6.145371779227685
    sigma_comb_a = 0.03357378578040692
    delta_a_4pi = -0.20632339565674843
    assert math.isclose(abs(delta_a_4pi) / sigma_comb_a, power_a_4pi, rel_tol=1e-13)
    assert math.isclose(juno["z_frozen_m2"], 1.9379969609, rel_tol=2e-9)
    assert math.isclose(skgd["z_frozen_m2"], 3.605064, rel_tol=2e-6)
    assert math.isclose(juno["sigma_mu_required_5sigma_1e-5_eV2"], 0.03023275259, rel_tol=2e-9)
    assert math.isclose(juno["total_live_days_conditional_t^-1/2"], 1379.188, rel_tol=2e-6)
    assert math.isclose(skgd["additional_live_days_conditional_t^-1/2"], 380.079, rel_tol=2e-6)
    assert math.isclose(deltas["k4pi_chi0"], -0.10552640532180015, rel_tol=1e-13)
    assert math.isclose(deltas["k8pi_chi0"], -0.19090707343364302, rel_tol=1e-13)

    energy_psion_eV = math.sqrt(2.0) * beta
    h_eVs = 4.135667696e-15
    hbarc_eVm = 1.973269804e-7
    hc_eVum = 1.239841984
    curvature = beta / (hbarc_eVm**2)
    psion = {
        "energy_eV": energy_psion_eV,
        "frequency_THz": energy_psion_eV / h_eVs / 1e12,
        "free_wavelength_um": hc_eVum / energy_psion_eV,
        "reduced_length_um": hbarc_eVm / energy_psion_eV * 1e6,
        "curvature_m^-2": curvature,
        "radius_um": 1.0 / math.sqrt(curvature) * 1e6,
    }
    q = {
        "Q_star_omega_over_Gamma": math.sqrt(2.0) / beta,
        "Q_QNM_omega_over_2Gamma": 1.0 / (math.sqrt(2.0) * beta),
    }
    return {
        "convention": "Frozen rite: m2=sqrt(Delta_m21^2); sigma_m2=(1/2)(sigma_Delta/Delta)m2; no D opened.",
        "beta_runtime": beta,
        "m2_pred_meV": m2_pred_meV,
        "delta_m21_pred_1e-5_eV2": delta_pred / 1e-5,
        "JUNO_207p2d": juno,
        "SK_Gd_411p52d_lower_error": skgd,
        "ringdown_chi0": deltas,
        "ringdown_power_check_A31_k4pi": abs(delta_a_4pi) / sigma_comb_a,
        "psion_conditional_u_1eV": psion,
        "quality_factor_conventions": q,
        "status": "ALL_NUMERIC_ASSERTIONS_PASSED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    checks = verify_numbers()
    if args.check_only:
        print(json.dumps(checks, ensure_ascii=False, indent=2))
        return
    if not REPORT.is_file():
        raise FileNotFoundError(REPORT)

    entries = []
    for index, raw in enumerate(REQUIRED + EXTRA + [str(REPORT), str(Path(__file__).resolve())], start=1):
        path = resolve(raw)
        if not path.is_file():
            raise FileNotFoundError(path)
        entries.append({
            "n": index,
            "role": "required_reading" if index <= len(REQUIRED) else "support_or_deliverable",
            "path": str(path.resolve()),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })

    payload = {
        "schema": "IALD/TGL SHA-256 manifest v1",
        "date": "2026-11-01",
        "status": "[DECLARADO pelo Kimi]",
        "required_reading_count": len(REQUIRED),
        "file_count": len(entries),
        "files": entries,
        "numeric_checks": checks,
        "manifest_integrity": {
            "sidecar": SIDECAR.name,
            "algorithm": "SHA-256 of the final manifest bytes; detached to avoid self-reference",
        },
    }
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_hash = sha256(MANIFEST)
    SIDECAR.write_text(f"{manifest_hash}  {MANIFEST.name}\n", encoding="ascii")
    assert sha256(MANIFEST) == SIDECAR.read_text(encoding="ascii").split()[0]
    print(json.dumps({
        "status": "MANIFEST_WRITTEN_AND_VERIFIED",
        "required_reading_count": len(REQUIRED),
        "file_count": len(entries),
        "manifest": str(MANIFEST),
        "manifest_sha256": manifest_hash,
        "sidecar": str(SIDECAR),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
