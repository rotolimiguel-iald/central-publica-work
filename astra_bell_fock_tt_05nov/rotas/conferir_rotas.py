"""Summarize existing receipts and compute conditional design sensitivity only."""
from pathlib import Path
from statistics import NormalDist
import hashlib
import json
import math


ROOT = Path("C:/IALD")
WORK = ROOT / "Central de Patentes/work"
F9 = WORK / "fase9_v2_c1_23out"
H0DN = ROOT / "Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/h0dn_documentary_review"
SOURCES = {
    "F9_result": F9 / "saidas/RESULTADO_FASE9_V2_C1_20261023_122926.json",
    "F9_power": F9 / "saidas/PODER_FASE9_ANTES_DE_ABRIR.json",
    "F9_freeze": F9 / "freeze/RECIBO_DE_CONGELAMENTO.json",
    "F9_opening": F9 / "freeze/RECIBO_DE_ABERTURA.json",
    "H0DN_design": H0DN / "REVISAO_H0DN_ACT.md",
    "H0DN_audit": H0DN / "STRUCTURE_AUDIT.json",
    "H0DN_screen": WORK / "teste_decisivo_30out/calcular_triagem_hubble.py",
    "H0DN_review": WORK / "teste_decisivo_30out/RELATORIO_TESTE_DECISIVO_30out.md",
    "original_survey": WORK / "cinco_sigma_fora_da_cosmologia_27out/CONFERENCIA_GERENCIA_RELATORIO_KIMI_5SIGMA_01_27out.md",
    "survey_update": WORK / "cinco_sigma_02_01nov/RELATORIO_KIMI_5SIGMA_02_01nov.md",
    "D_plan_V1": WORK / "conjunto_D_20261029/parametrizacao_03nov/PODER_RAMO_B_ANTES_DE_ABRIR.json",
    "D_experiment_scope": WORK / "conjunto_D_20261029/parametrizacao_03nov/PARTITURA_D_03nov.md",
    "Neff": WORK / "neff_02nov/PARTITURA_NEFF_02nov.md",
    "RE": WORK / "rota_RE_dualidade_02nov/DERIVACAO_RE_02nov.md",
    "bench": ROOT / "Bancada_Um/CONTRATO_CANONICO_B17.md",
}


def load_receipt(key):
    return json.loads(SOURCES[key].read_text(encoding="utf-8-sig"))


def main():
    observed = load_receipt("F9_result")
    primary = observed["primario"]
    prospective = load_receipt("F9_power")
    k = prospective["K"]
    background = prospective["fundo_BG1_vivo"]
    # Published scalar error used strictly to reproduce the October 30 design.
    local_sigma = 0.81
    shift = (k - 1) * background["H0"]
    total_sigma = math.hypot(local_sigma, k * background["sigma"])
    d_plan = shift / total_sigma
    normal = NormalDist()
    d90 = 5 + normal.inv_cdf(0.9)
    results = {
        "scope": "Existing F9 receipts and single-reader Gaussian design; no new observational data",
        "F9_primary": {
            "verdict": primary["veredito"],
            "K": k,
            "D_from_prospective_file": prospective["poder"]["P_primaria"]["maximum"]["D_S5_fundo_vivo"],
            "D_from_primary_file": primary["poder_previo_so_sigma"],
            "z_disc": primary["calibracao"]["z_disc_calibrado"],
            "p_disc": primary["calibracao"]["p_calibrado_z_disc_unilateral"],
            "z_delta": primary["calibracao"]["z_delta_calibrado"],
            "ln_B": primary["lnB"]["TGL_vs_LCDM"],
            "D_without_cepheids": prospective["poder"]["N_sem_cefeidas"]["maximum"]["D_S5_fundo_vivo"],
        },
        "H0DN_design": {
            "D_scalar": d_plan,
            "total_sigma": total_sigma,
            "expected_shift_km_s_Mpc": shift,
            "one_sided_detection_probability_under_normal_fixed_width": normal.cdf(d_plan - 5),
            "D_for_90_percent": d90,
            "total_sigma_max_for_median_5": shift / 5,
            "total_sigma_max_for_90_percent": shift / d90,
            "information_retained_for_median_5": (5 / d_plan) ** 2,
            "information_retained_for_90_percent": (d90 / d_plan) ** 2,
        },
        "sources": {
            key: {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for key, path in SOURCES.items()
        },
    }
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
