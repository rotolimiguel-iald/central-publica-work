from __future__ import annotations

import hashlib
import json
from pathlib import Path

OUT = Path(r"C:\IALD\Central de Patentes\work\neff_02nov")
SOURCE = OUT / "fontes" / "Goldstein_Hill_2603.13226v2.pdf"
N_SM = 3.044
DELTA_TGL = 0.11946607525373273
N_TGL = N_SM + DELTA_TGL
SIGMA_5_SEP = DELTA_TGL / 5.0


def metrics(label: str, n_obs: float, sigma: float, role: str) -> dict[str, object]:
    sigma_5_exclusion = abs(N_TGL - n_obs) / 5.0
    return {
        "label": label,
        "role": role,
        "N_obs": n_obs,
        "sigma": sigma,
        "z_TGL_against_center": (N_TGL - n_obs) / sigma,
        "z_SM_against_center": (N_SM - n_obs) / sigma,
        "separation_TGL_SM_sigma": DELTA_TGL / sigma,
        "sigma_for_5sigma_separation": SIGMA_5_SEP,
        "sigma_for_5sigma_exclusion_if_center_persists": sigma_5_exclusion,
        "precision_factor_for_5sigma_separation": sigma / SIGMA_5_SEP,
        "precision_factor_for_5sigma_exclusion": sigma / sigma_5_exclusion,
        "information_factor_for_5sigma_separation": (sigma / SIGMA_5_SEP) ** 2,
        "information_factor_for_5sigma_exclusion": (sigma / sigma_5_exclusion) ** 2,
        "convention": "Gaussian 1D diagnostic only; no TGL likelihood or nature verdict",
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    channels = [
        metrics("He LBT + D, primordial only", 2.976, 0.093, "BACKGROUND_ONLY_CANDIDATE_INDEPENDENT_BLOCK_A"),
        metrics("CMB-PAS + DESI DR2 BAO, without abundances", 3.010, 0.110, "CANDIDATE_INDEPENDENT_BLOCK_B_REQUIRES_PERTURBATIVE_CLOSURE"),
        metrics("He + D + CMB-PAS + DESI DR2 BAO, full baseline", 2.990, 0.070, "FULL_COMBINATION_NOT_INDEPENDENT_OF_SUBSETS"),
    ]
    assert abs(channels[0]["z_TGL_against_center"] - 2.01576425004) < 1e-9
    assert abs(channels[2]["z_TGL_against_center"] - 2.47808678936) < 1e-9
    assert abs(channels[2]["separation_TGL_SM_sigma"] - 1.70665821791) < 1e-9
    assert abs(channels[2]["sigma_for_5sigma_exclusion_if_center_persists"] - 0.03469321505074654) < 1e-12

    payload = {
        "date": "2026-11-02",
        "status": "[DECLARADO pelo Kimi]",
        "N_SM": N_SM,
        "delta_N_eff_TGL": DELTA_TGL,
        "N_eff_TGL": N_TGL,
        "sigma_for_5sigma_model_separation": SIGMA_5_SEP,
        "channels": channels,
        "upper_limit_95_percent": {
            "delta_N_eff_limit": 0.107,
            "delta_TGL_minus_limit": DELTA_TGL - 0.107,
            "delta_TGL_over_limit": DELTA_TGL / 0.107,
            "interpretation": "indicative tension under LambdaCDM+N_eff with DeltaN>0 prior; not a dedicated TGL exclusion",
        },
        "no_verdict_emitted": True,
    }
    (OUT / "CONTAS_PARTITURA_NEFF.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    source_card = {
        "source": "Goldstein & Hill, arXiv:2603.13226v2",
        "version_date_utc": "2026-03-20T03:01:33Z",
        "access_date": "2026-11-02",
        "url": "https://arxiv.org/pdf/2603.13226v2",
        "local_path": str(SOURCE),
        "bytes": SOURCE.stat().st_size,
        "sha256": sha256(SOURCE),
        "admission": "D8_PENDING_OPERATOR_EXPLICIT_DECISION",
        "x16": "OPEN_X16_NO_SELECTION",
        "execution": "E3_AWAITING_OPERATOR",
    }
    (OUT / "FICHA_D8_GOLDSTEIN_HILL.json").write_text(
        json.dumps(source_card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": "NUMERIC_CHECKS_PASSED", "channels": channels, "source_card": source_card}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
