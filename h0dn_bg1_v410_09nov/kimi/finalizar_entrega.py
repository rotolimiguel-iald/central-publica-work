from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREV = Path(r"C:\IALD\Central de Patentes\work\kimi_h0dn_discriminante_06nov")
OUT = HERE
DEPOSIT = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\depositos\kimi")
DEPOSIT.mkdir(parents=True, exist_ok=True)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path: Path) -> dict:
    return {"path": str(path), "sha256": sha(path)}


g1g2 = {
    "status": "G1_DERIVED_STRONG_CANDIDATE__G2_CLOSED_IDENTITY_AND_PROVENANCE",
    "G1": {
        "rule": "unweighted arithmetic mean of light curves within each SH0ES calibrator",
        "R22_calibrators": 42,
        "multi_curve_R22": 25,
        "single_curve_R22": 17,
        "max_mean_error_mag": 0.000499725341796875,
        "candidate_not_final_source_confirmation": True,
        "evidence": pin(PREV / "g1g2/G1_ARITHMETIC_CANDIDATE.json"),
    },
    "G2": {
        "status": "CLOSED_IDENTITY_AND_PROVENANCE",
        "aliases": {"2008fv": "2008fv_comb", "1994D": "1994DRichmond"},
        "eight_absent_IDs": "Separated by provenance; no identity guessed by name similarity",
        "extra_13_covariance": "OPEN: independent original sources or prespecified sensitivity required",
        "evidence": pin(PREV / "g1g2/G2_IDS_PROVENIENCIA_RESOLVIDA.json"),
    },
    "no_repetition": "Existing G1/G2 evidence was validated, not recomputed",
}
validation_path = OUT / "VALIDACAO_G1_G2.json"
validation_path.write_text(json.dumps(g1g2, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

files = {
    "y_obs": OUT / "y_obs.npz",
    "construction": OUT / "CONSTRUCAO_Y_OBS.json",
    "physical_covariance": OUT / "C_fisica_258x258.npz",
    "decomposition": OUT / "DECOMPOSICAO_COVARIANCIA.json",
    "G1G2_validation": validation_path,
    "G1_arithmetic": PREV / "g1g2/G1_ARITHMETIC_CANDIDATE.json",
    "G1_G42_scenarios": PREV / "g1g2/G1_G42_COVARIANCE_SCENARIOS.json",
    "G2_provenance": PREV / "g1g2/G2_IDS_PROVENIENCIA_RESOLVIDA.json",
    "temporal_stone": PREV / "provas/AfixacaoTemporalR1.lean",
    "temporal_receipt": PREV / "provas/AfixacaoTemporalR1_receipt.json",
    "support_test": OUT / "TESTE_CENTRALIZACAO_PUBLICADA.json",
    "HMS_diagnostic": OUT / "DIAGNOSTICO_HMS_COMPLETA.json",
}

result = {
    "tipo": "RESULTADO",
    "rota_id": "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov",
    "dominio": "ESTATISTICA_CONJUNTA",
    "titulo": "Y_obs do H0DN construído; G1/G2 documentados; obstrução exata da covariância física",
    "pergunta": "É possível construir o vetor observado e fechar a covariância física H0DN × BG1 sem duplicação, preservando o suporte e a abertura pré-registrada?",
    "dados": [
        "H0DN upstream public data and baseline configuration, 255 equations",
        "SH0ES R22 and Pantheon+ public covariance components",
        "BG1 covariance with explicit conditional independence, not measured cross-covariance",
        "Published host distances and baseline group parameters for centering",
    ],
    "metodo": "Original upstream through build_equations only; A,C,row_names checked byte-identical to FREEZE_R2; y_uncentered and y-Ax_published; G42 arithmetic aggregation; identity/provenance audit; support and PSD checks only; no solver and no estimator.evaluate",
    "resultado": {
        "rows_built": 255,
        "centered_and_uncentered_identical": False,
        "A_C_identical_to_FREEZE": True,
        "host_rank": 94,
        "host_nullity": 72,
        "published_max_abs_null_projection": 0.09312020264507931,
        "published_support_tolerance": 1e-8,
        "published_support_pass": False,
        "full_HMS_rank": 255,
        "full_HMS_support_pass": True,
        "full_HMS_admitted": False,
        "G1": "DERIVED_STRONG_CANDIDATE",
        "G2": "CLOSED_IDENTITY_AND_PROVENANCE",
        "G3_G4": "OBSTRUCTION_EXACT__PHYSICAL_COVARIANCE_OPEN",
        "opening_allowed": False,
    },
    "veredito": "G1_DERIVED_STRONG_CANDIDATE__G2_CLOSED_IDENTITY_AND_PROVENANCE__G3_G4_OBSTRUCTION_EXACT__OPENING_NOT_ALLOWED",
    "estatuto": "REAL",
    "status": "BLOQUEADA",
    "olhou_dados": True,
    "defeito": "Published covariance has nullity 72 and observed y has nonzero null projection; full HMS restores rank but may duplicate variance already contained in mu_error and is not admitted. Extra 13 covariance and independent/shared HMS decomposition remain open.",
    "nao_refazer": "Do not rerun R2 seeds, do not recompute power, do not change FREEZE_R2, do not use full HMS to force acceptance, do not fit or adjust observed data, do not declare 5 sigma.",
    "proximo_passo": "Obtain source-validated independent/shared HMS decomposition and the extra 13 covariance from original sources; then independently review and rerun the frozen validation before any observed opening.",
    "onde": str(OUT / "construir_y_obs.py"),
    "artefatos": [str(path) for path in files.values()],
    "refs": [
        "estatistica.h0dn_bg1.cov_injecoes_06nov",
        "observavel.bell_fock_tt_astra_05nov",
    ],
    "nota": {
        "scope": "The full HMS diagnostic is not physical admission. No Z, t, h or ratio was computed; no solver or estimator.evaluate was called; no new R2 seed was generated; no gate or publication was touched.",
        "open_items": [
            "Independent/shared HMS decomposition without duplication",
            "Covariance for the 13 additional non-R22 calibrators",
            "Cepheid-host, intrinsic-scatter and peculiar-velocity decomposition",
            "Independent review and route-selection accounting",
        ],
        "questions_four_languages": {
            "TGL": "Qual decomposição de erros independentes e compartilhados, incluindo HMS e os 13 calibradores adicionais, torna a covariância fisicamente completa e aceita o vetor sem duplicação?",
            "Teológica [ONTO]": "Que testemunha externa pode certificar que um termo acrescentado à covariância é informação ausente e não a mesma variância contada duas vezes?",
            "Linguística": "Que Nome deve distinguir a HMS completa, que apenas diagnostica suporte, da covariância física efetivamente admitida, para que 'fechada' e 'diagnóstica' não sejam usados como sinônimos?",
            "Jurídica [ONTO]": "Que prova documental e que ato de revisão independente são necessários para admitir a covariância física e autorizar a abertura observada sem transformar um diagnóstico em prova?",
        },
        "pins": {name: pin(path) for name, path in files.items()},
    },
}
delivery_path = OUT / "ENTREGA_H0DN_Y_OBS.json"
delivery_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

now = datetime.now()
deposit_path = DEPOSIT / f"{now:%Y%m%d_%H%M%S}_h0dn_y_obs_obstrucao_covariancia.md"
deposit_path.write_text(
    "---\n"
    "quem: kimi-k3pro\n"
    "casa: Nós\n"
    "tipo: project\n"
    "estatuto: DECLARADO\n"
    "alvo_sugerido: novo:h0dn_covariancia_y_obs\n"
    "fontes:\n"
    f"  - {delivery_path}  sha256:{sha(delivery_path)}\n"
    f"  - {files['y_obs']}  sha256:{sha(files['y_obs'])}\n"
    f"  - {files['physical_covariance']}  sha256:{sha(files['physical_covariance'])}\n"
    f"  - {files['temporal_stone']}  sha256:{sha(files['temporal_stone'])}\n"
    "---\n"
    "Y_obs do H0DN foi construído com as 255 equações e A,C idênticos ao FREEZE_R2, sem solver e sem estimator.evaluate. G1 é candidata forte com agregação aritmética; G2 fecha identidade/proveniência. A covariância publicada tem nulidade 72 e falha no suporte do vetor (projeção máxima 0,09312020264507931). A forma HMS completa tem posto 255 e passa no suporte, mas não é admitida porque a diagonal já está contida em mu_error e pode duplicar variância. G3/G4 seguem abertos. Não houve cálculo de Z, t, h ou razão, nova semente, gate ou publicação. Entrega e hashes em ENTREGA_H0DN_Y_OBS.json.\n",
    encoding="utf-8",
)

print(json.dumps({
    "delivery": str(delivery_path),
    "delivery_sha256": sha(delivery_path),
    "validation": str(validation_path),
    "validation_sha256": sha(validation_path),
    "deposit": str(deposit_path),
    "deposit_sha256": sha(deposit_path),
    "route_registration_file": str(delivery_path),
}, ensure_ascii=False, indent=2))
