# -*- coding: utf-8 -*-
"""Registra no Mapa de Rotas (rota existente ringdown.ramo_b_preregistro_v386) a AUTORIZAÇÃO do operador, 29/10/2026, para executar o teste
cego do conjunto D sob o V1 congelado por hash. Verbatim lido do disco; sha256 por script. A gerência c1 assume a execução na casa."""
import hashlib, json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
C = Path("C:/IALD/Central de Patentes"); W = C / "work/conjunto_D_20261029"
V = C / "work/cunhagens_13out/OPERADOR_29out_autoriza_conjunto_D_verbatim.txt"
verb = V.read_text(encoding="utf-8").strip(); assert verb == "autorizo a realização do teste do conjunto D", verb
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
V1 = Path("C:/IALD/Bancada_Um/investigacao/preregistro_ramo_b_05out/PREREGISTRO_RAMO_B_RINGDOWN_V1.json")
assert sha(V1).startswith("86f98fcc124dd9ca"), "V1 mudou de hash: parar"
REC = C / "work/cadeia_de_selo/v386/ramo_b/pre_registro/RECONCILIACAO_CONJUNTO_D.json"
D10 = json.loads(REC.read_text(encoding="utf-8"))["conjunto_D"]["elegiveis_sem_hold"]["eventos"]; assert len(D10) == 10
reg = [{
 "tipo": "RESULTADO", "rota_id": "ringdown.ramo_b_preregistro_v386", "dominio": "RINGDOWN",
 "titulo": "29/10/2026: o operador AUTORIZOU o teste cego do conjunto D («%s»); a gerência c1 assume a execução na casa sob o V1 congelado (sha16 86f98fcc124dd9ca); F4.1/F4.2 EM_CURSO" % verb,
 "pergunta": "O conjunto D (10 eventos O4 sem hold, PE só-220 cega na casa) decide o PAR do ramo B (k = 2π/κ̂(χ_f), M = M_f,det, envoltória) pela função de veredito congelada?",
 "dados": ["verbatim do operador 29/10 (sha256 %s)" % sha(V), "V1 do ramo B (v386) por hash", "RECONCILIACAO_CONJUNTO_D.json: 10 sem hold: %s" % ", ".join(D10),
           "WSL Ubuntu-24.04 /opt/lal_env: bilby 2.8.2, dynesty 3.1.0, lalsimulation 6.2.1; 48 núcleos; 125 GB [REAL, medido 29/10]",
           "código da PE controlada: Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code (pe_runner, registration_guard, blinding, injection_design, strain_io, pseob_source) [REAL, existe; funcionamento a medir]"],
 "metodo": "ordem do V1 (l.382): congelar os 10 → qualificação F4.1 por injeções C2 (só-RG e dtau220 = δ_pred; |viés| ≤ 0,2|δ_pred|; cobertura) → PE cega dos 10 → estágio cego (σ_i, a_i, N, κ̂, δ_pred, poder, C1, C5 → PODER_RAMO_B_ANTES_DE_ABRIR.json com hash) → abertura → estimador do V1 (δ̄ ponderado com c(σ) profilado; z_RG; z_B; χ²/dof; jackknife) → função de veredito congelada → RESULTADO_RAMO_B_V1.json; fora do um.py (palavra do operador), lido por hash numa versão posterior",
 "resultado": "AUTORIZADO e em preparação: nenhuma PE executada, nenhum dado aberto; quadro F4.1 (evento 1362) e F4.2 (evento 1363) EM_CURSO por claude-c1; plano de execução em elaboração (estudo técnico Sonnet, só leitura e teste de fumaça)",
 "veredito": "TGL_RAMO_B_SET_D__AUTHORIZED_BY_OPERATOR_20261029__EXECUTION_IN_PREPARATION__NOTHING_OPENED__GATE_UNTOUCHED",
 "estatuto": "INPUT (a autorização); REAL (o ambiente e os arquivos, medidos)", "status": "EM_CURSO", "olhou_dados": False,
 "defeito": "o que D pode decidir foi dito ao operador antes da palavra: só o PAR do ramo B (canal F2b retirado ao lado na v404); se D se comportar como a calibração A (+0,072 ± 0,034, 31 eventos) a função devolve FALSIFIED_AT_5SIGMA do par (z_excl ≈ 7 com 10 eventos); no ramo A (τ★ = t_Planck) D é invisível (δ ≈ 3e-42); nenhum cenário move o gate; rodar não é publicar (palavra do operador de 02/10 sobre falsificação segue dele)",
 "nao_refazer": "não redigir segundo pré-registro (o V1 está congelado por hash); não abrir A/B/C como teste (são calibração NOT_BLIND); não computar nem ler posterior de deformação de evento real de D antes do PODER_RAMO_B_ANTES_DE_ABRIR com hash; não reaproveitar a leitura não-cega de A como veredito",
 "proximo_passo": "plano de execução (work/conjunto_D_20261029/PLANO_EXECUCAO_D_29out.md) → F4.1 injeções C2 no WSL → F4.2 PE cega dos 10 → estágio cego com hash → abertura → veredito; custo [DECLARADO] 58–390 CPU-h",
 "onde": "work/conjunto_D_20261029; work/cadeia_de_selo/v386/ramo_b; Chatgpt/ORDEM_013_RINGDOWN/bis/e2_code; C:/IALD/Bancada_Um/investigacao/preregistro_ramo_b_05out",
 "artefatos": [str(V), str(V1), str(REC)],
 "refs": ["ringdown.dephasing", "natureza.5sigma_fora_da_cosmologia_poder_27out", "massa.transicao_beta_para_massa.levantamento_28out"],
 "nota": "NOT_FALSIFIED nunca é CONFIRMED; FALSIFIED do par não é falsificação da lei nem da TGL (V1); PROVADA = validade; o gate não se move."}]
pj = W / "rota_mapa_autorizacao_D_29out.json"; pj.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([sys.executable, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1"], capture_output=True, text=True, encoding="utf-8", errors="replace")
print(r.stdout[-600:], r.stderr[-300:], "rc", r.returncode); assert r.returncode == 0
