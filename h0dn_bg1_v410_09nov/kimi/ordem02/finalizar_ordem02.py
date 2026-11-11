from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REVIEW = HERE / "PACOTE_REVISAO_R3"
DEPOSIT = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\depositos\kimi")
OLD = [
    DEPOSIT / "20261109_144204_h0dn_y_obs_obstrucao_covariancia.md",
    DEPOSIT / "20261109_144232_h0dn_y_obs_obstrucao_covariancia.md",
    DEPOSIT / "20261109_145102_hms_13_pacote_revisao_independente.md",
    DEPOSIT / "20261109_152126_claude_incorporar_hms13_um_py.md",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path: Path) -> dict:
    return {"path": str(path), "sha256": sha(path), "bytes": path.stat().st_size}


stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
redeposits = []
for index, old in enumerate(OLD, 1):
    text = old.read_text(encoding="utf-8")
    if "quem: kimi-k3pro" not in text:
        raise RuntimeError(f"Expected rejected frontmatter not found: {old}")
    corrected = text.replace("quem: kimi-k3pro", "quem: kimi", 1)
    corrected += f"\n\nRedepósito de custódia em 10/11/2026, por exigência da ORDEM_KIMI_H0DN_02_10nov.md. Original preservado: `{old.name}`. Correção somente do campo frontmatter para `quem: kimi`, igual ao nome da pasta; nenhum resultado científico foi alterado.\n"
    target = DEPOSIT / f"{stamp}_redeposito_{index:02d}_{old.name}"
    target.write_text(corrected, encoding="utf-8")
    frontmatter = corrected.split("---", 2)[1]
    assert "quem: kimi\n" in frontmatter and "quem: kimi-k3pro" not in frontmatter
    redeposits.append({"original": str(old), "redeposito": pin(target)})

redeposit_receipt = {
    "status": "FOUR_REJECTED_DEPOSITS_REDEPOSITED_WITH_CORRECT_QUEM",
    "original_files_preserved": True,
    "scientific_content_changed": False,
    "frontmatter_correction": "quem: kimi-k3pro -> quem: kimi",
    "items": redeposits,
}
redeposit_path = HERE / "REDEPOSITOS_CUSTODIA.json"
redeposit_path.write_text(json.dumps(redeposit_receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

files = [
    HERE / "SEEDS_R3_REGISTRADAS.json",
    HERE / "C_fisica_R3_A1_REDUCIDA.npz",
    HERE / "A1_HOST_DECOMPOSITION.json",
    HERE / "DECOMPOSICAO_FISICA_R3.json",
    HERE / "CERTIFICADO_DE_PODER_R3.json",
    HERE / "A1_SINTETICOS.json",
    REVIEW / "ORDEM_REVISAO_R3.md",
    REVIEW / "verificar_r3.py",
    REVIEW / "VALIDACAO_R3.json",
    HERE / "preparar_ordem02.py",
    redeposit_path,
]
pins = {p.name: pin(p) for p in files}
validation = json.loads((REVIEW / "VALIDACAO_R3.json").read_text(encoding="utf-8"))
if validation["status"] != "R3_REVIEW_VALIDATED__A1_ALGEBRA_CLOSED__POWER_NOT_EVALUABLE" or not all(validation["checks"].values()):
    raise RuntimeError("Cannot deliver without a valid R3 review receipt")

previous_observed = []
for name in ["CONSTRUCAO_Y_OBS.json", "TESTE_CENTRALIZACAO_PUBLICADA.json", "DIAGNOSTICO_HMS_COMPLETA.json"]:
    previous_observed.append(pin(HERE.parent / name))

delivery = {
    "tipo": "RESULTADO",
    "rota_id": "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov",
    "dominio": "ESTATISTICA_CONJUNTA",
    "titulo": "R3: A1 fecha por redundâncias exatas; covariância completa e poder permanecem bloqueados",
    "pergunta": "É possível fechar a covariância física H0DN × BG1 e certificar poder discriminante real, às cegas, sem abrir o observado?",
    "dados": [
        "H0DN public Appendix B.2/B.3.2: 255 equations, 183 distinct measurements and 72 redundancies",
        "network.npz and public factor matrices; 166 host equations, including 37 R22 triplets",
        "G42 STATONLY, PV, BG1 and 13-calibrator source audits from prior work",
        "No observed vector was read in this order",
    ],
    "metodo": "Exact shared-measurement factorization; explicit 72-constraint basis; covariance reconstruction and eigensupport; deterministic synthetic-only parameter recovery and out-of-support rejection; A2-A6 admission audit; no RNG, no power Monte Carlo and no observed support test",
    "resultado": {
        "veredito_certificado": "COVARIANCE_NOT_CLOSABLE_FROM_PUBLIC_SOURCES",
        "A1": "CLOSABLE_FROM_PUBLIC_SOURCES__EXACT_REDUNDANCIES",
        "A1_host_rank": 94,
        "A1_host_nullity": 72,
        "A1_support_rank": 183,
        "A1_reconstruction_max_abs": validation["metrics"]["host_reconstruction_max_abs"],
        "A1_synthetic_estimator_pass": True,
        "A2": "CLOSED_ALGEBRAIC_CONDITIONAL__PHYSICAL_ERROR_MODEL_OPEN",
        "A3": "CLOSED_FOR_G42_STATONLY_ONLY",
        "A4": "INHERITED_PV_ACCOUNTING_OPEN",
        "A5": "OPEN_NO_TRANSPLANT__EXTRA13_OUT_DESIGN_ONLY__IN_CAP13_ROBUSTNESS_ONLY",
        "A6": "CONDITIONAL_INDEPENDENCE_ONLY",
        "admitted_variants": [],
        "D_conservador": None,
        "D_by_variant_and_model": {},
        "power_gate": "NOT_EVALUABLE",
        "mc_status": "NOT_RUN_NO_ADMITTED_COVARIANCE",
        "new_seed_count": 0,
        "observed_support_tests_now": 0,
        "opening_allowed": False,
    },
    "veredito": "COVARIANCE_NOT_CLOSABLE_FROM_PUBLIC_SOURCES__A1_ALGEBRA_CLOSED__POWER_NOT_EVALUABLE__OPENING_NOT_ALLOWED",
    "estatuto": "DECLARADO",
    "status": "BLOQUEADA",
    "olhou_dados": False,
    "defeito": "A1 fecha algebricamente, mas A2/A3 não provam identidade física dos erros G42, A4 não fecha a contabilidade PV herdada, os 13 não têm covariância completa/cruzamentos e H0DN–BG1 é apenas condicional. Sem variante física completa não há D ou poder certificado.",
    "nao_refazer": "Não usar HMS completa ou jitter; não projetar y; não abrir suporte observado nesta ordem; não gerar sementes R3 sem variante admitida; não tocar R2/FREEZE_R2/v410; não repetir Fase 9 V2 ou rotas mortas; não declarar 5 sigma, detectado ou confirmado.",
    "proximo_passo": "Revisão independente de A1; recuperar produtos internos G42/PV/13 e covariância local–BG1 ou fixar cegamente uma poda admissível; só então registrar sementes novas, calcular D, orçamento e Monte Carlo cruzado. Se H0DN não bastar, avaliar B1/conjunto D apenas como proposta sob seu V1 existente.",
    "onde": str(REVIEW / "ORDEM_REVISAO_R3.md"),
    "artefatos": [str(p) for p in files],
    "refs": [
        "estatistica.h0dn_bg1.cov_injecoes_06nov",
        "d1.fase9.v2_c1_a_unica_palavra_23out",
        "natureza.5sigma_fora_da_cosmologia_poder_27out",
    ],
    "nota": {
        "escopo": "DECLARADO pelo Kimi até conferência da gerência. A1_CLOSABLE não significa covariância completa nem abertura. POWER_NOT_EVALUABLE não é UNDERPOWERED numérico.",
        "pins": pins,
        "B4_summary": "Delta-D não é estimável antes de uma covariância admitida. Faltam centros compartilhados/precisão R22 se a montagem exata falhar, identidade G42, decomposição PV, matrizes/cruzamentos dos 13 ou poda cega admitida e covariância local–BG1.",
        "route_accounting": {
            "previous_observed_receipts_counted": previous_observed,
            "new_observed_routes_in_order02": 0,
            "new_support_tests_in_order02": 0,
        },
        "redepositos": redeposit_receipt,
        "questions_four_languages": {
            "TGL": "Para uma futura variante admitida, o senhor fixa o portão de 90% (D conservador ≥ 6,282) e autoriza EXTRA13_OUT como desenho conservador, ou exige primeiro os produtos internos dos 13?",
            "Teológica [ONTO]": "Que testemunho deve bastar para chamarmos o poder de real: a redução cega dos dados não resolvidos ou a covariância completa dos 13, e sob qual limiar de 90%?",
            "Linguística": "Devemos nomear EXTRA13_OUT como variante conservadora de poder, sem chamá-la covariância física recuperada, e fixar D ≥ 6,282 como significado de poder real?",
            "Jurídica [ONTO]": "Qual decisão pré-registrada o senhor ratifica: exigir os produtos internos ou admitir a poda cega EXTRA13_OUT, sempre com D conservador ≥ 6,282 e revisão independente antes da abertura?",
        },
        "observed_opening_performed": False,
        "gate_or_publication_changed": False,
    },
}
delivery_path = HERE / "ENTREGA_ORDEM02.json"
delivery_path.write_text(json.dumps(delivery, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
delivery_pin = pin(delivery_path)

main_deposit = DEPOSIT / f"{stamp}_ordem02_r3_a1_poder_bloqueado.md"
main_deposit.write_text(f"""---
quem: kimi
casa: Nós
tipo: project
estatuto: DECLARADO
alvo_sugerido: novo:h0dn_r3_poder
fontes:
  - {delivery_path}  sha256:{delivery_pin['sha256']}
  - {HERE / 'CERTIFICADO_DE_PODER_R3.json'}  sha256:{sha(HERE / 'CERTIFICADO_DE_PODER_R3.json')}
  - {HERE / 'DECOMPOSICAO_FISICA_R3.json'}  sha256:{sha(HERE / 'DECOMPOSICAO_FISICA_R3.json')}
  - {REVIEW / 'VALIDACAO_R3.json'}  sha256:{sha(REVIEW / 'VALIDACAO_R3.json')}
---
ORDEM_KIMI_H0DN_02 concluída sem abertura. A1 fecha pela fonte: as 72 direções são redundâncias exatas das 111 linhas R22, tratadas por fatoração compartilhada e redução/pseudoinversa, nunca por HMS completa ou jitter. A reconstrução do host tem erro máximo {validation['metrics']['host_reconstruction_max_abs']}; os testes apenas sintéticos passaram. A2/A3 ficam condicionais, A4 PV e A6 independência empírica seguem abertos, e os 13 ficam OPEN_NO_TRANSPLANT. Logo o certificado é COVARIANCE_NOT_CLOSABLE_FROM_PUBLIC_SOURCES, D_conservador=null, power_gate=NOT_EVALUABLE, Monte Carlo não rodado e zero sementes novas. Não houve leitura de y_obs nem novo teste de suporte. Os quatro depósitos recusados de 09/11 foram redepositados ao lado com quem:kimi e originais preservados. A rota existente recebeu esta entrega para revisão da gerência; nenhum gate, FREEZE_R2, v410 ou publicação foi alterado.
""", encoding="utf-8")

print(json.dumps({"delivery": delivery_pin, "main_deposit": pin(main_deposit), "redeposit_receipt": pin(redeposit_path), "redeposits": redeposits}, ensure_ascii=False, indent=2))
