# -*- coding: utf-8 -*-
"""Transition ACOM da sessão c1 (29/10/2026): o operador AUTORIZOU o teste cego do conjunto D; a gerência assume a execução na casa.
Encurta flow.phase/next_action para a projeção voltar ao orçamento (a projeção recusou por overflow: 26414 > 24000). Fail-closed."""
import hashlib, json, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"; sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
CEN = r"C:\IALD\Central de Patentes"
V = CEN + r"\work\cunhagens_13out\OPERADOR_29out_autoriza_conjunto_D_verbatim.txt"; verb = open(V, encoding="utf-8").read().strip()
assert verb == "autorizo a realização do teste do conjunto D", verb
V1 = r"C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_05out\PREREGISTRO_RAMO_B_RINGDOWN_V1.json"; assert sha(V1).startswith("86f98fcc124dd9ca")
MAPA = CEN + r"\work\conjunto_D_20261029\rota_mapa_autorizacao_D_29out.json"
REF = CEN + r"\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
def sm(p):
    r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (json.loads(r.stdout) if r.stdout.strip().startswith("{") else {"raw": (r.stdout + r.stderr)[:400]})
rc, g = sm({"operation": "get", "reference": REF}); rev = (g.get("result") or {}).get("revision"); print("acom get rc", rc, "revision", rev); assert rev is not None, g
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + sha(p)}
agora = time.strftime("%d/%m/%Y %H:%M")
texto = ("%s: ORDEM do operador, verbatim «%s» (sha256 %s). Antes da palavra a gerência disse o que D decide: só o PAR do ramo B (k = 2π/κ̂, M_f,det, envoltória; canal F2b retirado ao lado na v404); "
         "se D se comportar como a calibração A (+0,072 ± 0,034) a função congelada devolve FALSIFIED_AT_5SIGMA do par (z_excl ≈ 7 com 10 eventos); no ramo A D é invisível; nenhum cenário move o gate; rodar não é publicar. "
         "Medido: WSL /opt/lal_env (bilby 2.8.2, dynesty 3.1.0, lalsimulation 6.2.1), 48 núcleos, 125 GB; strain dos 10 sem hold em casa; código da PE controlada da ORDEM 013-bis existe (e2_code). "
         "Quadro: F4.1 e F4.2 reivindicadas e EM_CURSO por claude-c1 (eventos 1360–1363). Mapa: registro na rota ringdown.ramo_b_preregistro_v386. "
         "Ordem do V1: congelar os 10 → F4.1 injeções C2 → PE cega → estágio cego com hash (PODER_RAMO_B_ANTES_DE_ABRIR) → abertura → RESULTADO_RAMO_B_V1 pela mesma função de veredito; fora do um.py. "
         "Nada aberto, nenhuma PE executada. O teste em LLMs (P7) foi respondido: não dá o 5σ de β na natureza (regra do próprio P7, um.py v72); pode dar o veredito POWERED do P7 com controles — aguarda palavra do operador." % (agora, verb, sha(V)))
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-conjunto-d-autorizado-pelo-operador-29out",
            "changes": {"records": [{"id": "c1-conjunto-d-autorizado-29out", "kind": "fact", "statute": "INPUT", "sources": [S(V), S(V1), S(MAPA)], "text": texto}],
                        "flow": {"phase": "v404_COMPLETA__conjunto_D_AUTORIZADO_29out__execucao_em_preparacao_F4_1_F4_2",
                                 "next_action": "conjunto D: plano de execução (estudo Sonnet) → F4.1 injeções C2 → F4.2 PE cega dos 10 → estágio cego com hash → abertura → veredito (work/conjunto_D_20261029). Operador: WIPO 2FA + e-mail ACOM [LEGAL]; E0; D2; iald.ia.br; Zenodo; nome da pedra; P7 com controles (aguarda palavra)."}}})
print("acom rc", rc, "revision", (t.get("result") or {}).get("revision"), t.get("message", "") or t.get("raw", ""))
rc2, pj = sm({"operation": "project", "reference": REF}); print("project rc", rc2, (pj.get("error") or "ok"), (pj.get("message") or "")[:160])
