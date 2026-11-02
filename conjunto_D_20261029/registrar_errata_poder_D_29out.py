# -*- coding: utf-8 -*-
"""ERRATA ao lado (Mapa de Rotas, rota ringdown.ramo_b_preregistro_v386, corrige o seq 1545 de 29/10/2026), em nome próprio da gerência c1:
o «z_excl ≈ 7 → FALSIFIED_AT_5SIGMA» supunha informação média do A31; com o SNR dos 10 de D (12,1–16,8) o poder de planejamento é 3,7–3,9σ
(D10) e 4,4–4,6σ (D14), e a regra 2 congelada devolve NOT_FALSIFIED_UNDERPOWERED antes de qualquer FALSIFIED. Números lidos do plano do
estudo técnico (Sonnet, 29/10), que calibrou o ajuste σ(SNR) no próprio A31 (0,0355 vs 0,0336; 6 %). Transition ACOM na sequência."""
import glob, hashlib, json, os, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
C = Path("C:/IALD/Central de Patentes"); W = C / "work/conjunto_D_20261029"
PL = W / "PLANO_EXECUCAO_D_29out.md"; INV = W / "INVENTARIO_D_29out.json"; assert PL.is_file() and INV.is_file()
txt = PL.read_text(encoding="utf-8")
for frase in ("3,7–3,9σ (10 eventos) e 4,4–4,6σ (14, com os 4 holds)", "NOT_FALSIFIED_UNDERPOWERED", "0,0355", "121–140 h", "425,3", "177,0"):
    assert frase in txt, frase
arts = [str(PL), str(INV)] + [p for p in glob.glob(str(W / "*PODER*planejamento*.json"))] + [p for p in glob.glob(str(W / "**/*PODER*planejamento*.json"), recursive=True)]
arts = list(dict.fromkeys(arts))
reg = [{
 "tipo": "ERRATA", "corrige": 1545, "rota_id": "ringdown.ramo_b_preregistro_v386", "dominio": "RINGDOWN",
 "titulo": "ERRATA ao lado do seq 1545 (29/10, gerência c1 em nome próprio): o poder de planejamento do conjunto D é 3,7–3,9σ (D10) e 4,4–4,6σ (D14) — abaixo de 5σ; a regra congelada devolve NOT_FALSIFIED_UNDERPOWERED antes de qualquer FALSIFIED; o «z_excl ≈ 7» supunha informação média do A31",
 "pergunta": "Com o SNR real dos 10 eventos de D, a função de veredito congelada pode devolver FALSIFIED_AT_5SIGMA do par?",
 "dados": ["SNR de rede GWOSC dos 10 sem hold: 12,1–16,8 (plano §4.1) [REAL, metadados; nenhum valor de deformação lido]",
           "ajuste σ_τ(SNR) da bancada nos 31 do GWTC-5.0 (ln σ = 1,4166 − 0,9450 ln ρ), calibrado: σ_comb(A31) 0,0355 vs 0,0336 do V1 (6 %) [REAL, planejamento NOT_BLIND]",
           "conjunto B do V1 (10 do GWTC-3: GW150914, GW200129, …) tem SNR 20–26 e poder 6,37σ: a diferença para D é o SNR, não o método [REAL, lido do PODER_CEGO v2 e do V1]"],
 "metodo": "projeção de planejamento [DERIVED]: σ_i(SNR) por evento, σ_comb em quadratura com σ_sys ∈ {0; 0,029; 0,038}, poder = |δ̄_pred|/σ_comb; sem jackknife (só piora) e sem a diferença v4HM_PA × v5PHM; as σ_i reais nascem na PE (estágio cego do V1)",
 "resultado": "poder D10 3,73–3,93σ (σ_comb ≈ 0,10; δ̄_pred −0,3985); D14 4,39–4,64σ; cenário «D como A» (δ̄ = +0,072): z_excl ≈ 4,4–4,6 (D10) e 5,2–5,5 (D14), mas a regra 3 (poder < 5) vem antes da 5: NOT_FALSIFIED_UNDERPOWERED qualquer que seja δ̂; fator de informação que falta para 5σ em D10: 1,78×. Custo: 170 CPU-h por PE (central; faixa 51–517; as 2 PE reais da casa pararam em maxcall com Δlogz 425 e 177, nenhuma convergiu); D10 só: 55–63 h de parede; cadeia F4.1 + D10 + C2 mínima: 121–140 h (5–6 dias; pessimista 15–17 dias). Falta código: guarda novo pinado ao V1 (a cadeia 013-bis/015 está vencida, prazo 03/10, recibo de auditoria ausente), semente de cegueira, injeções C2 em off-source de D, estimador do ramo B + estágio cego + abertura + veredito (gw_stack.veredito é do eco e devolve DETECTED, que o V1 não permite); o prior d_L [100, 2000] Mpc dos jobs existentes truncaria 5 dos 10 (D_L até 4,9 Gpc).",
 "veredito": "TGL_RAMO_B_SET_D__PLANNING_POWER_3P7_TO_3P9_SIGMA_D10__4P4_TO_4P6_D14__BELOW_5__FROZEN_RULE_RETURNS_UNDERPOWERED__COST_5_TO_6_DAYS__CODE_MISSING__DECISION_RETURNED_TO_OPERATOR__NOTHING_OPENED__GATE_UNTOUCHED",
 "estatuto": "DERIVED (o poder de planejamento); REAL (SNR, strain, ambiente, teste de fumaça 0,065 s/forma de onda); DECLARADO (tempos das PE da GW250114); OPEN (custo até convergir)",
 "status": "EM_CURSO", "olhou_dados": False,
 "defeito": "a gerência disse ao operador «z_excl ≈ 7 → FALSIFIED_AT_5SIGMA» antes da palavra dele; o número corrige a frase: com o SNR de D o teste, como congelado, não alcança 5σ no par; a autorização foi dada sobre premissa corrigida e volta ao operador como decisão (rodar até o estágio cego e decidir a abertura com as σ_i reais; não rodar e fechar o ramo B como parede medida; ou rodar tudo)",
 "nao_refazer": "não refazer a projeção de poder (plano §4.3; script no inventário); não redigir segundo pré-registro; não abrir dado; não reaproveitar guardas vencidas da 013-bis",
 "proximo_passo": "decisão do operador entre: (c) PE cega dos 10 até o estágio cego (σ_i reais, PODER_RAMO_B_ANTES_DE_ABRIR com hash) e decidir a abertura ali; (b) não rodar e registrar parede medida, D fica cego para E (GWTC-5 final/O5) com combinação pré-registrada; (a) cadeia completa. Antes de qualquer PE: guarda novo pinado ao V1, prior d_L alargado e escrito antes, semente de cegueira, estimador e veredito do ramo B escritos a partir da regra 2 do V1",
 "onde": "work/conjunto_D_20261029/PLANO_EXECUCAO_D_29out.md (§0, §4.3, §6, §7, §8); INVENTARIO_D_29out.json",
 "artefatos": arts,
 "refs": ["ringdown.dephasing", "natureza.5sigma_fora_da_cosmologia_poder_27out"],
 "nota": "Errata em nome próprio da gerência c1 (lei da assinatura da errata). NOT_FALSIFIED nunca é CONFIRMED; UNDERPOWERED não é «a natureza decidiu»; o gate não se move."}]
pj = W / "rota_mapa_errata_poder_D_29out.json"; pj.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([sys.executable, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1"], capture_output=True, text=True, encoding="utf-8", errors="replace")
print(r.stdout[-500:], r.stderr[-400:], "rc", r.returncode); assert r.returncode == 0
# ---- ACOM (rev 14 -> 15)
PY = r"C:\Python314\python.exe"; sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
REF = str(C / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json")
def sm(p):
    q = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return q.returncode, (json.loads(q.stdout) if q.stdout.strip().startswith("{") else {"raw": (q.stdout + q.stderr)[:400]})
rc, g = sm({"operation": "get", "reference": REF}); rev = (g.get("result") or {}).get("revision"); assert rev is not None, g
S = lambda p: {"kind": "artifact", "ref": str(p) + "#sha256:" + sha(p)}
texto = ("%s: CORREÇÃO em nome próprio da gerência c1 — o estudo técnico (Sonnet, só leitura; plano e inventário com hashes) mediu: SNR dos 10 de D 12,1–16,8; poder de planejamento 3,7–3,9σ (D10) e 4,4–4,6σ (D14) [DERIVED, ajuste calibrado no A31 a 6 %%]; "
         "pela regra 2 congelada (regra 3 antes da 5) o veredito seria NOT_FALSIFIED_UNDERPOWERED qualquer que seja δ̂; o «z_excl ≈ 7 → FALSIFIED» dito ao operador supunha informação média do A31 e está corrigido ao lado (Mapa, ERRATA do seq 1545). "
         "Custo: 170 CPU-h por PE (central), D10 55–63 h de parede, cadeia completa 121–140 h (5–6 dias); as 2 PE reais da casa nunca convergiram (Δlogz 425/177). Falta código: guarda novo pinado ao V1, semente de cegueira, C2 off-source, estimador/estágio cego/abertura/veredito do ramo B; prior d_L truncaria 5/10. "
         "A autorização de 29/10 foi dada sobre premissa agora corrigida: a decisão volta ao operador (quadro F4.1/F4.2 AGUARDA_OPERADOR) com três opções: (c) PE cega até o estágio cego e decidir a abertura com σ_i reais; (b) não rodar, parede medida, D cego para E; (a) cadeia completa. Nada aberto; gate intocado." % time.strftime("%d/%m/%Y %H:%M"))
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-conjunto-d-poder-abaixo-de-5sigma-decisao-devolvida-29out",
            "changes": {"records": [{"id": "c1-conjunto-d-poder-planejamento-29out", "kind": "fact", "statute": "DERIVED", "sources": [S(PL), S(INV), S(pj)], "text": texto}],
                        "flow": {"phase": "v404_COMPLETA__conjunto_D_AUTORIZADO__poder_projetado_3p7_a_3p9_sigma__decisao_do_operador_pendente",
                                 "next_action": "aguardar a decisão do operador sobre o conjunto D (c/b/a); se rodar: escrever guarda pinado ao V1, prior d_L, semente de cegueira, estimador e veredito do ramo B ANTES de qualquer PE (work/conjunto_D_20261029). P7 com controles aguarda palavra. Operador: WIPO 2FA + e-mail ACOM [LEGAL]; E0; D2; iald.ia.br; Zenodo; nome da pedra."}}})
print("acom rc", rc, "revision", (t.get("result") or {}).get("revision"), t.get("message", "") or t.get("raw", ""))
