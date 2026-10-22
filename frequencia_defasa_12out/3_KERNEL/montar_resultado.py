# -*- coding: utf-8 -*-
"""Monta RESULTADO_KERNEL.json (face K da F1.FREQUENCIA, trilha POSTO) a partir dos artefatos medidos nesta pasta.
Nada e lido de memoria: todo hash e numero vem dos arquivos (conferencias, recibos, auditoria, varredura).
Escreve SO em 3_KERNEL (temporario -> conferir -> substituir)."""
import datetime, hashlib, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))


def J(nome):
    return json.loads(open(os.path.join(AQUI, nome), "rb").read().decode("utf-8"))


def sha_arq(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


CONF = J("CONFERENCIA_FREEZE.json")
BETA = J("BETA_RUNTIME.json")
ANTES = J("IMPRESSAO_DIGITAL_KERNEL_ANTES.json")
DEPOIS = J("IMPRESSAO_DIGITAL_KERNEL_DEPOIS.json")
REC = J(os.path.join("logs", "final_pedra_RECIBO.json"))
RECA = J(os.path.join("logs", "auditoria_RECIBO.json"))
AUD = J("AUDITORIA_KERNEL.json")
VAR = J("VARREDURA_FONTE.json")
DEC = J("DECLARACOES.json")
PRE = json.loads(open(os.path.join(os.path.dirname(AQUI), "1_PREREGISTRO", "PREREGISTRO.json"), "rb").read().decode("utf-8"))
PEDRA = os.path.join(AQUI, "sandbox", "TGLExt", "TheUnitIsTheRank.lean")
OLEAN = os.path.join(AQUI, "olean", "TheUnitIsTheRank.olean")
NS = "TGLExt.TheUnitIsTheRank."

pedra_sha = sha_arq(PEDRA)
olean_sha = sha_arq(OLEAN)
assert pedra_sha == REC["source_sha256"] == AUD["pedra_sha256_auditada"] == VAR["pedra_sha256"] == DEC["pedra_sha256"], \
    "FALHA VISIVEL: a pedra auditada nao e a compilada"
assert olean_sha == REC["olean_sha256"], "FALHA VISIVEL: olean preservado difere do compilado"
declarados = {d["nome"] for d in DEC["declaracoes"]}
ax_por = {x["nome"]: x for x in AUD["por_declaracao"]}

# ---------------------------------------------------------------- partes (pre-registro, secao c) -> face K
# resultado: PASSA (provada) | FALHA (refutada no kernel: a negacao foi provada) | CITADO | CITADO_REAL |
#            NAO_FORMALIZADA (e por que). «esperado» e o do pre-registro congelado.
P = []


def parte(pid, resultado, decls, estatuto, nota, sem_peso=None, triviais=None):
    for d in decls:
        assert d in declarados, "declaracao inexistente: " + d
    esperado = None
    for a in PRE["c_afirmacoes"]:
        for p in a["partes"]:
            if p[0] == pid:
                esperado = p[6]
    assert esperado is not None, "parte fora do pre-registro: " + pid
    P.append({"id": pid, "resultado_K": resultado, "esperado_preregistro": esperado,
              "conforme_o_esperado": esperado.split(" (")[0] == resultado,
              "declaracoes": [NS + d for d in decls],
              "axiomas": sorted({",".join(ax_por[NS + d]["axiomas"]) for d in decls}) if decls else [],
              "estatuto": estatuto, "nota": nota,
              "hipoteses_sem_peso": sem_peso or [], "triviais_por_desenho": triviais or []})


R = "[REAL no sandbox: termo de kernel; axiomas no trio]"
parte("P1.a", "PASSA", ["pure_iff_rank_one", "pure_iff_idempotent", "pure_core"],
      "[KNOWN — Nielsen & Chuang, Ex. 2.71] o conteudo; " + R + " o TERMO (novo no kernel: levantamento 2.3)",
      "Enunciado literal em M_n(C), n tipo finito qualquer: rho PSD, Tr rho = 1 => (Tr rho^2 = 1 <=> posto rho = 1) e "
      "(Tr rho^2 = 1 <=> rho^2 = rho). Rota: teorema espectral da Mathlib; autovalores em [0,1] com soma 1. As duas "
      "hipoteses tem peso: C1 (sem PSD falha em M_3) e C2 (sem Tr = 1 falha).")
parte("P1.b", "PASSA", ["trace_sq_fin_two", "pure_iff_rank_one_fin_two", "trace_and_purity_one_fin_two"], R,
      "Provado mais do que o pre-registrado: em M_2(C) com Tr M = 1 vale o <=> (Tr M^2 = 1 <=> posto M = 1) SEM "
      "positividade; a implicacao literal (Tr M = Tr M^2 = 1 => det M = 0 e posto M = 1) e corolario.")
parte("P1.d", "PASSA", ["rankOne_density", "rankOne_density_normalized"], R,
      "|psi| = 1 codificado como <psi,psi> = star psi . psi = 1 (em `n -> C` a norma da Mathlib e a do sup, nao a de "
      "Hilbert). psi != 0 => posto |psi><psi| = 1; normalizado => Tr = 1, idempotente, Tr(.^2) = 1.")
parte("P2.lit", "CITADO", ["rank_add_nullity"],
      "[KNOWN — Mathlib LinearMap.finrank_range_add_finrank_ker; Axler, LADR, Teo. 3.22]",
      "Re-exportado para matrizes como termo (posto + nulidade = n); o PASSA e do termo, o conteudo segue KNOWN.")
parte("P2.a", "PASSA", ["rhoStar_rank_nullity", "half_identity_rank_nullity", "zero_rank_nullity"], R,
      "(posto, nulidade): rho* = (1,1), I/2 = (2,0), 0 = (0,2). Leituras R-a / R-b do pre-registro: so os fatos; a "
      "escolha de leitura e do operador [INPUT].")
parte("P2.b", "PASSA", ["trace_one_rank_pos", "rank_one_iff_nullity", "rank_one_iff_nullity_succ"], R,
      "A forma literal com subtracao natural (nulidade = n - 1) usa Tr rho = 1 (que garante n >= 1); a forma sem "
      "subtracao (nulidade + 1 = n) vale sem hipotese nenhuma.")
parte("P3.a", "PASSA", ["compression_by_rank_one", "reading_returns_the_post", "compression_by_rank_one_literal"], R,
      "P X P = <a,Xa> P e Tr(P X) = <a,Xa> valem para TODO vetor a; <a,Xa> != 0 => P X P/<a,Xa> = P. Projetores "
      "especificos ja estavam no kernel (bell_compression_is_scalar, the_shadow_is_the_reader_weighted_by_the_reading); "
      "a forma geral e nova. Luders [KNOWN].",
      sem_peso=["compression_by_rank_one_literal: _ha (<a,a> = 1) nao e usada; so seria necessaria para P^2 = P, que nao "
                "faz parte do enunciado P3.a"])
parte("P3.b", "PASSA", ["reading_of_the_attractor_state", "reading_weights_are_truth_and_cost",
                        "reading_weights_at_theta", "reading_weights_at_thetaMiguel"], R,
      "A leitura de posto 1 aplicada ao estado atrator I/2 devolve rho* (Tr = 1/2); Tr(rho* diag(1-b,b)) = 1-b e "
      "Tr(Q0 diag(1-b,b)) = b; com b = sin^2 th: = |t(th)|^2 e |r(th)|^2; em thetaMiguel: 1-beta e beta (identidades de "
      "theta_M, sem poder discriminante). A pedra NAO identifica P com o R da F1.ATRATOR.")
parte("P4", "PASSA", ["trace_eq_rank_of_projection", "normalized_projection_name", "normalized_projection_index",
                      "name_meets_rank_only_at_the_atom", "normalized_projection_literal"],
      "[DERIVED no levantamento] -> " + R,
      "rho = P/d: Tr rho = 1 (o nome, cego ao posto), Tr rho^2 = 1/d (o indice, ve o posto), Tr rho^2 = Tr rho <=> d = 1. "
      "Face de densidade de TheWeightIsNotTheRank: DISTINCAO, nao ponte; os dois 1 so coincidem no atomo.",
      sem_peso=["normalized_projection_literal: _hH (P^H = P) nao e usada; Tr P = posto P vale para todo idempotente "
                "sobre C (B1.b)"])
parte("B1.a", "PASSA", ["rhoStar_trace", "rhoStar_rank", "rhoStar_idem", "rhoStar_herm", "rhoStar_unit"], R,
      "Tr rho* = posto rho* = 1, rho*^2 = rho* = rho*^H. omega(I) = Tr rho* e [REAL runtime] (um.py l.6513); "
      "posicao <-> rank e [ONTO].")
parte("B1.b", "PASSA", ["trace_eq_rank_of_projection"], R,
      "P^2 = P => Tr P = posto P sobre C, sem hipotese hermitiana (rota IsProj sobre a imagem, Mathlib).")
parte("B1.c", "PASSA", ["range_rhoStar"], R,
      "imagem rho* = span{e1} com e1 = ![1,0] (o `e1` da SMatrix = o «e0» do pre-registro); posto = finrank(span) = 1.")
parte("B2.a", "PASSA", ["Qtheta_eq", "Qtheta_eq_rot", "Rot_eq_conjTranspose", "anticomm_eq", "anticomm_zero_iff",
                        "anticomm_trace", "anticomm_frob"], R,
      "Q_th = [[s^2,-sc],[-cs,c^2]] (e a receita R Q0 R^T do um.py l.6518 e o mesmo objeto que S^H Q0 S); "
      "{Q_th, rho*} = [[2s^2,-sc],[-cs,0]]; = 0 <=> sin th = 0 (avaliacao exata em th em pi*Z, nunca limite no angulo); "
      "Tr = 2s^2; soma |.|^2 = 2s^2(1+s^2) (purityR de PageInformation).")
parte("B2.b", "PASSA", ["anticomm_at_thetaMiguel"], R + "; identidade de theta_M",
      "c : TGLCoupling: {Q_thM, rho*} != 0, Tr = 2 beta, soma |.|^2 = 2 beta(1+beta). Sem poder discriminante.")
parte("B3.a", "PASSA", ["leak_eq", "leak_eq_rhoOut", "leak_eq_reflected_weight"], R,
      "Tr(rho* Q_th) = sin^2 th = Tr(F_th(1) Q0) = (rhoOut th)_11 = |r(th)|^2.")
parte("B3.b", "PASSA", ["leak_at_thetaMiguel"], R + "; identidade de theta_M := arcsin sqrt beta",
      "Tr(rho* Q_thM) = beta para todo c : TGLCoupling. Validade algebrica; nao discrimina beta (mapa seq 294).")
P.append({"id": "B3.d", "resultado_K": "NAO_FORMALIZADA", "esperado_preregistro": "PASSA",
          "conforme_o_esperado": None, "declaracoes": [], "axiomas": [],
          "estatuto": "sem face K no pre-registro (coluna K = '-')",
          "nota": "Conferencia numerica do beta de runtime com o numero escrito pelo operador em V4 l.16: e afirmacao de "
                  "runtime (face O). O numero de beta nunca entra no Lean; pela regra (f) do pre-registro, onde ha uma "
                  "face so, ela decide — aqui decide a face O. (BETA_RUNTIME.json so confere a receita e 0 < beta < 1.)",
          "hipoteses_sem_peso": [], "triviais_por_desenho": []})
parte("B4.a", "PASSA", ["ad_trace", "ad_rank", "ad_projection", "ad_rhoStar"], R,
      "u^H u = 1: Tr e posto preservados (lacuna L4 fechada via Mathlib rank_mul_eq_*_of_isUnit_det); u P u^H e "
      "projecao (re-uso de ad_preserves_projection e ad_preserves_star_projection, pedra 116); em rho*: Tr = posto = 1. "
      "F e angulo: so le.")
parte("B4.b", "PASSA", ["fractal_one_is_rank_one"], R,
      "F_th(1) = rhoOut th: posto 1, Tr 1, idempotente, hermitiana, Tr(.^2) = 1.")
parte("B5.a", "PASSA", ["endpoint_eq", "endpoint_det", "endpoint_trace", "endpoint_rank_two_iff",
                        "endpoint_rank_one_iff", "endpoint_purity"], R,
      "D_inf F_th(1) = diag(c^2, s^2); Tr 1; posto 2 <=> sin 2th != 0 (senao 1); pureza 1 - 2s^2c^2, < 1 <=> sin 2th != 0. "
      "«Tudo = D_beta(F(1))» segue [CONJECTURE ontologica]; aqui so o ponto final e o seu posto.")
parte("B5.b", "PASSA", ["rank_diag_two_iff", "rank_diag_one_at_ends", "endpoint_at_thetaMiguel"], R,
      "b em [0,1]: posto diag(1-b,b) = 2 <=> 0 < b < 1; = 1 em b = 0 e b = 1; c : TGLCoupling: D_inf F_thM(1) = "
      "diag(1-beta, beta), posto 2, pureza 1 - 2beta(1-beta) < 1.")
parte("B5.c", "PASSA", ["dephased_rhoOut_eq", "dephased_det", "dephased_rank_two_iff", "dephased_rank_at_zero",
                        "dephased_trace"], R,
      "g_ii = 0, g01, g10 > 0, t > 0: det D_t F_th(1) = c^2 s^2 (1 - e^{-t(g01+g10)}); posto 2 <=> sin 2th != 0; t = 0: "
      "posto 1; traco preservado em todo t.")
parte("B5.e(i)", "PASSA", ["fractal_one_is_rank_one"], R, "= B4.b: F(1) tem posto 1.")
parte("B5.e(ii)", "FALHA", ["rank_not_preserved_by_dephasing", "trace_survives_dephasing"],
      R + "; negativo honesto",
      "A universal «para todo th, posto D_inf F_th(1) = posto F_th(1)» e REFUTADA no kernel (testemunha thetaMiguel: 2 != 1). "
      "Sobrevive o traco, nao o posto. Conforme o pre-registrado.")
parte("B6.a", "PASSA", ["leak_survives_dephasing"], R, "g_ii = 0: Tr(rho* D_t Q_th) = sin^2 th para todo t.")
parte("B6.b", "PASSA", ["dephased_Qtheta_eq", "anticomm_dephased_eq", "anticomm_dephased_entry00",
                        "anticomm_dephased_zero_iff", "diagExpect_Qtheta", "anticomm_limit"], R,
      "{D_t Q_th, rho*} = [[2s^2, -e^{-t g01} sc],[-e^{-t g10} cs, 0]]; = 0 <=> sin th = 0 (vale para QUAISQUER taxas); "
      "{D_inf Q_th, rho*} = diag(2s^2, 0).")
parte("B7.a1", "PASSA", ["Smat_pow", "leak_after_n_passes"], R,
      "S(th)^n = S(n th): iterar o angulo e girar o angulo; peso refletido apos n passagens = sin^2(n th).")
parte("B7.a2", "PASSA", ["angular_leak_no_limit", "angular_reflected_weight_no_limit", "angular_leak_zero_converges",
                         "sin_sq_shift_identity", "sin_sq_double"], R,
      "sin th != 0 => sin^2(n th) NAO tem limite (prova: um limite L teria L = 1/2 pela recorrencia de tres termos e "
      "L = 4L(1-L) pela duplicacao); sin th = 0 => constante 0. O limite nunca e pedido ao angulo: prova-se que nao existe.")
parte("B7.b", "CITADO_REAL", ["dephasing_has_limit"], "[REAL — ja no kernel: dephase_tendsto_expectation]",
      "Re-exportacao TRIVIAL (a face tem limite).", triviais=["dephasing_has_limit"])
parte("B7.c", "CITADO_REAL", ["spiral_with_rate_converges", "spiral_without_rate_has_no_limit",
                              "spiral_without_rate_is_periodic"],
      "[REAL — ja no kernel: IALDJones.orbit_tendsto_center, angular_orbit_no_limit, angular_orbit_periodic]",
      "Re-exportacoes TRIVIAIS. O decaimento como direcao hiperbolica de SL(2,R) segue [ONTO] e nao e afirmado.",
      triviais=["spiral_with_rate_converges", "spiral_without_rate_has_no_limit", "spiral_without_rate_is_periodic"])
parte("B8.a", "PASSA", ["nothing_branch", "rhoOut_zero", "dephase_rhoStar", "Qtheta_zero"], R,
      "th = 0: Tr(rho* Q0) = 0, {Q0, rho*} = 0, F_0(1) = rho* = D_t rho* para todo t; posto 1; pureza 1. «Nada» nao e termo.")
parte("B8.b", "PASSA", ["rhoOut_eq_diag_iff", "dephasing_trivial_iff", "cos_thetaMiguel",
                        "sin_two_thetaMiguel_eq_zero_iff", "dephasing_trivial_at_thetaMiguel"], R,
      "(para todo t, D_t F_th(1) = F_th(1)) <=> sin 2th = 0; em thetaMiguel(b), b em [0,1]: <=> b = 0 ou b = 1; posto 1 "
      "nos dois ramos.")
parte("B9.a", "FALHA", ["literal_transmission_does_not_force_dephasing"], R + "; negativo honesto",
      "A leitura LITERAL (transmitir = |t|^2 > 0 => D atua) e REFUTADA no kernel, para TODA matriz de taxas com g_ii = 0 "
      "(testemunha th = 0: |t|^2 = 1 e D nao atua). Conforme o pre-registrado.")
parte("B9.a'", "FALHA", ["literal_leak_does_not_force_dephasing"], R + "; controle",
      "A leitura simetrica (vazar = |r|^2 > 0 => D atua) e REFUTADA (testemunha th = pi/2). Conforme o pre-registrado.")
parte("B9.b", "PASSA", ["dephasingActs_iff", "dephasing_acts_iff_transmits_and_leaks", "inscription_at_thetaMiguel"], R,
      "Leitura de INSCRICAO: D atua <=> |t|^2 > 0 E |r|^2 > 0; em thetaMiguel D atua e (D_inf F(1))_11 = beta. "
      "«transmitir» como natureza segue [ONTO].")
parte("B9.c", "CITADO_REAL", ["transmission_dephases_reexport"],
      "[REAL — ja no kernel: TheVerbSelectsTheAction.transmission_dephases (v386)]",
      "Re-exportacao TRIVIAL: F(t)(1-P) = e^{-t}(1-P).", triviais=["transmission_dephases_reexport"])
for pid, oque in (("O1", "[ONTO — epistemologia]: «ou os vinculos fecham, ou nao fecham»; nao e objeto de kernel "
                         "(NAO_TESTAVEL). A validade no kernel e binaria por declaracao — e o que esta auditoria mede."),
                  ("O2", "[OPEN]: a leitura da memoria dos modelos / espaco latente; sem telemetria latente; nao e "
                         "objeto de kernel (ABERTO).")):
    esperado = [p[6] for a in PRE["c_afirmacoes"] for p in a["partes"] if p[0] == pid][0]
    P.append({"id": pid, "resultado_K": "NAO_FORMALIZADA", "esperado_preregistro": esperado,
              "conforme_o_esperado": True, "declaracoes": [], "axiomas": [], "estatuto": oque.split(":")[0],
              "nota": oque, "hipoteses_sem_peso": [], "triviais_por_desenho": []})

ids_pre = [p[0] for a in PRE["c_afirmacoes"] for p in a["partes"]]
ids_res = [x["id"] for x in P]
assert sorted(ids_pre) == sorted(ids_res), ("partes divergentes", sorted(set(ids_pre) ^ set(ids_res)))

# ---------------------------------------------------------------- controles
CTRL = [
    ("C1", "P1.a", ["psd_is_necessary", "psd_is_necessary'"], "diag(2/3,2/3,-1/3) em M_3: Tr 1, Tr(.^2) 1, posto 3, nao PSD"),
    ("C2", "P1.a", ["normalization_is_necessary", "normalization_is_necessary'"], "rho*/2: PSD, posto 1, Tr(.^2) = 1/4"),
    ("C3", "B1, P4", ["trace_one_not_rank_one", "trace_one_not_rank_one'"],
     "I/2: Tr 1, posto 2, PSD (a citacao de runtime tr P_F ~ 4 nao e termo)"),
    ("C4", "P3", ["reading_needs_weight"], "P = rho*, rho = Q0: Tr(P rho) = 0, P rho P = 0; a leitura nao devolve P"),
    ("C5", "P3", ["reading_needs_rank_one"], "P = 1 (posto 2), rho = I/2: a saida tem posto 2"),
    ("C6", "B4", ["nonunitary_changes_trace"], "A = diag(2,1): Tr(A rho* A^H) = 4 e A^H A != 1"),
    ("C7", "B4", ["singular_kills_rank"], "A = Q0: A rho* A^H = 0, posto 0"),
    ("C8", "B5", ["endpoint_rank_one_at_poles", "endpoint_rank_one_iff"], "th em {0, pi/2}: D_inf F_th(1) = F_th(1), posto 1"),
    ("C9", "B5, B7.b", ["zero_rate_no_dephasing"], "g = 0: D_t = id e NAO converge a D_inf (rhoOut(pi/4))"),
    ("C10", "B6", ["plus_reader_value", "nondiagonal_reader_sees_time"],
     "leitor |+><+| em thetaMiguel, gamma = 1: valor 1/2 - e^{-t} sc; t = 0 e t = 1 diferem (o limiar delta >= 1e-3 e da face O)"),
    ("C11", "B7.a2", ["angular_leak_zero_at_pi", "angular_leak_zero_converges"], "th = pi: sin^2(n pi) = 0 para todo n"),
    ("C12", "B9.a", ["literal_transmission_does_not_force_dephasing", "transmission_without_dephasing_at_zero"],
     "th = 0: |t|^2 = 1 e D nao atua"),
    ("C13", "B9.a'", ["literal_leak_does_not_force_dephasing", "leak_without_dephasing_at_half_pi"],
     "th = pi/2: |r|^2 = 1 e D nao atua"),
    ("C14", "B2", ["anticomm_zero_at_zero", "anticomm_zero_iff"], "th = 0: {Q0, rho*} = 0"),
]
controles = []
for cid, origem, decls, oque in CTRL:
    for d in decls:
        assert d in declarados, d
    controles.append({"id": cid, "parte_de_origem": origem, "declaracoes": [NS + d for d in decls],
                      "resultado": "FALHA_SEM_HIPOTESE", "esperado": "FALHA_SEM_HIPOTESE", "conforme": True,
                      "o_que_mostra": oque})

SONDAS = {
    "habitantes": ["probe_states", "probe_e1", "probe_coupling", "probe_angles", "unitRates_spec"],
    "os_dois_lados_de_cada_iff": {
        "pure_iff_rank_one, pure_iff_idempotent (P1.a)": "probe_pure_both_sides (rho* verdadeiro; I/2 falso)",
        "pure_iff_rank_one_fin_two (P1.b)": "probe_fin_two_both_sides",
        "rank_one_iff_nullity(_succ) (P2.b)": "probe_rank_nullity_both_sides",
        "name_meets_rank_only_at_the_atom (P4)": "probe_name_rank_both_sides (rho*; 1 em M_2) e probe_rank_two_projection "
                                                 "(diag(1,1,0,0), lado falso)",
        "anticomm_zero_iff, anticomm_dephased_zero_iff (B2.a, B6.b)": "probe_anticomm_both_sides (th = 0; th = pi/4)",
        "endpoint_rank_two_iff, endpoint_rank_one_iff, dephased_rank_two_iff, dephasing_trivial_iff, "
        "dephasing_acts_iff_transmits_and_leaks (B5, B8.b, B9.b)": "probe_endpoint_both_sides (th = pi/4; th = 0; t = 1; "
                                                                    "taxas unitarias)",
        "endpoint_purity (< 1 <=> sin 2th != 0)": "probe_purity_both_sides",
        "rank_diag_two_iff, sin_two_thetaMiguel_eq_zero_iff (B5.b, B8.b)": "probe_diag_both_sides (b = 1/2; b = 0)",
        "angular_leak_no_limit / angular_leak_zero_converges (B7.a2)": "probe_angular_both_sides (th = 1; th = pi)",
        "auxiliares (rank_two_iff, rank_one_iff_fin_two, nullity_pos_iff_det_eq_zero, rhoOut_eq_diag_iff, "
        "sin_two_mul_eq_zero_iff, cs_sq_eq_zero_iff, conj_diag_eq_iff)": "realizados implicitamente pelas mesmas sondas "
                                                                         "(rho*/I/2; th = 0/pi/4)",
    },
    "TGLCoupling": "probe_coupling habita TGLCoupling com beta = 1/2 SO para mostrar 0 < beta < 1 satisfativel; o beta de "
                   "runtime (BETA_RUNTIME.json) tambem satisfaz 0 < beta < 1",
}
for v in SONDAS["habitantes"]:
    assert v in declarados, v

ACHADOS = [
    "P1.b: em M_2(C), com Tr M = 1, o <=> (Tr M^2 = 1 <=> posto M = 1) vale SEM positividade (o pre-registro tinha so a "
    "implicacao). [REAL no sandbox]",
    "P3.a: a escalarizacao P X P = <a,Xa> P e Tr(P X) = <a,Xa> vale para TODO vetor a; a normalizacao <a,a> = 1 e hipotese "
    "sem peso no enunciado literal. [REAL no sandbox]",
    "P4/B1.b: Tr P = posto P vale para todo idempotente sobre C; P^H = P e hipotese sem peso no enunciado literal de P4. "
    "[REAL no sandbox]",
    "P2.b: a forma literal «nulidade = n - 1» (subtracao natural) precisa de n >= 1 (dado por Tr rho = 1); para n = 0 ela "
    "seria falsa em N (0 = 0 - 1). A forma «nulidade + 1 = n» vale sem hipotese. [REAL no sandbox; nota de formalizacao]",
    "B6.b: {D_t Q_th, rho*} = 0 <=> sin th = 0 vale para QUAISQUER taxas (g_ii = 0 desnecessaria). [REAL no sandbox]",
    "B6.b complemento: o LIMITE da face como Tendsto — com taxas positivas {D_t Q_th, rho*} -> diag(2 s^2, 0) "
    "(anticomm_dephased_tendsto). [REAL no sandbox; fora do pre-registro]",
    "B2.a: o zero do anticomutador e exatamente sin th = 0, isto e th em pi*Z (th = 0 e th = pi), avaliacao exata e nao "
    "«theta_M -> 0» como limite no angulo — coerente com a nota do pre-registro sobre um.py l.6502. [REAL no sandbox]",
    "B9.a: o contraexemplo da leitura literal vale para TODA matriz de taxas com g_ii = 0 (nao usa g_ij > 0). [REAL no sandbox]",
    "Ponte runtime-kernel: Rot_eq_conjTranspose e Qtheta_eq_rot provam que a receita do um.py (R Q0 R^T, l.6518) e o "
    "mesmo objeto que S(th)^H Q0 S(th) do kernel. [REAL no sandbox]",
    "Tecnico: no sandbox o modulo da pedra chama-se `TheUnitIsTheRank` (compilado com --root=TGLExt) porque uma pasta "
    "`TGLExt` dentro de sandbox\\build sombreia o pacote TGLExt do Nos na resolucao do LEAN_PATH (a 1a execucao "
    "'final_pedra', com o modulo TGLExt.TheUnitIsTheRank, falhou com: object file '...sandbox\\build\\TGLExt\\"
    "GlobalLiftLadder.olean' of module TGLExt.GlobalLiftLadder does not exist; o recibo dessa execucao foi sobrescrito "
    "pela 2a). O namespace e TGLExt.TheUnitIsTheRank; instalado no Nos o modulo seria TGLExt.TheUnitIsTheRank com o mesmo "
    "fonte; o sha256 do .olean e o do modulo do sandbox. [REAL — medido aqui]",
]

# ---------------------------------------------------------------- tentativas
tent = []
for tag in ("tentativa01", "tentativa02", "tentativa03", "tentativa04", "tentativa05", "final_pedra", "auditoria"):
    r = J(os.path.join("logs", tag + "_RECIBO.json"))
    tent.append({"tag": tag, "alvo": r["alvo"], "source_sha256": r["source_sha256"], "exit_code": r["exit_code"],
                 "n_erros": r["n_erros"], "n_avisos": r["n_avisos"], "saida": r["saida"], "saida_sha256": r["saida_sha256"]})
snap = {}
for fn in sorted(os.listdir(os.path.join(AQUI, "sandbox", "TGLExt"))):
    snap[fn] = sha_arq(os.path.join(AQUI, "sandbox", "TGLExt", fn))

# ---------------------------------------------------------------- manifesto
manif = {}
for dp, dns, fns in os.walk(AQUI):
    dns.sort()
    for fn in sorted(fns):
        p = os.path.join(dp, fn)
        rel = os.path.relpath(p, AQUI).replace("\\", "/")
        if rel in ("RESULTADO_KERNEL.json",) or rel.endswith(".tmp"):
            continue
        manif[rel] = [os.path.getsize(p), sha_arq(p)]

kernel_intacto = (ANTES["sha256_metadados"] == DEPOIS["sha256_metadados"]
                  and ANTES["sha256_conteudo_lean"] == DEPOIS["sha256_conteudo_lean"]
                  and ANTES["n_arquivos"] == DEPOIS["n_arquivos"])
sandbox_limpo = not any(os.path.exists(os.path.join(AQUI, "sandbox", x)) for x in ("toolchain_v4.31.0", "build"))
lake_no_sandbox = [dp for dp, dns, fns in os.walk(os.path.join(AQUI, "sandbox")) if os.path.basename(dp) == ".lake"]

res = {
    "documento": "RESULTADO_KERNEL — F1.FREQUENCIA (trilha POSTO), face K",
    "gerencia": "c1",
    "autor": "construtor do kernel (subagente)",
    "gerado_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "estatuto_geral": "[REAL no sandbox] termos de kernel compilados e auditados; validade na face testada, nao creditacao; "
                      "nao move o gate; nao fala da natureza; instalar no Nos e ato da v392 (gerencia e operador)",
    "escopo": "escrita so em 3_KERNEL; um.py lido so por busca de linha (nao executado); nada no quadro, mapa (so "
              "consultar), memoria, tunel, Nos, kernel do Nos, Bancada_Um, site ou git; sem dado observado, provedor, "
              "chamada paga ou ferramenta da Bancada",
    "escrita_fora_do_3_KERNEL": "[REAL — dito, nao disfarcado] durante a sonda de nomes (13:56 local) foram criados 3 "
                                "arquivos temporarios fora do 3_KERNEL com a lista de nomes desconhecidos da sonda: "
                                "all.txt e unk.txt no scratchpad da sessao e /tmp/unknown.txt (Git Bash); os tres foram "
                                "APAGADOS ao final (so eles; o scratchpad e compartilhado com a gerencia). Nenhuma outra "
                                "escrita fora do 3_KERNEL.",
    "acom": "[INPUT do construtor] README de C:\\IALD\\MEMORIA_IALD lido; a ordem proibe escrever na memoria e nao ha "
            "referencia propria, por isso NAO houve init; a inscricao desta etapa e ato da gerencia",
    "conferencia_preregistro": {
        "veredito": CONF["veredito"], "divergencias": CONF["divergencias"],
        "PREREGISTRO.json": CONF["freeze"]["PREREGISTRO.json"]["sha256"],
        "PREREGISTRO.md": CONF["freeze"]["PREREGISTRO.md"]["sha256"],
        "FREEZE.json_sha256": CONF["FREEZE.json"]["sha256"],
        "demais_arquivos_do_FREEZE_conferidos": sum(1 for v in CONF["freeze_demais"].values() if v["confere"]),
        "pinos_da_ordem": [[x["arquivo"], x["bytes"], x["sha256"], x["confere_com_a_ordem"]] for x in CONF["pinos"]],
        "pinos_do_preregistro_conferidos": sum(1 for x in CONF["pinos_preregistro"] if x.get("confere")),
        "verbatins": {k: [v["sha256"], v["confere"]] for k, v in CONF["verbatins"].items()},
    },
    "beta_runtime": {k: BETA[k] for k in ("alpha_linha", "alpha_texto", "beta_receita", "beta_repr",
                                          "beta_confere_com_a_conferencia_do_preregistro", "theta_M_repr",
                                          "TGLCoupling_habitado_pelo_beta_de_runtime")},
    "pedra": {
        "nome_provisorio": "TheUnitIsTheRank (o operador pode renomear)",
        "arquivo": PEDRA, "bytes": os.path.getsize(PEDRA), "sha256": pedra_sha,
        "namespace": "TGLExt.TheUnitIsTheRank",
        "modulo_no_sandbox": "TheUnitIsTheRank (lean --root=TGLExt)", "modulo_se_instalada_no_Nos": "TGLExt.TheUnitIsTheRank",
        "imports": ["Mathlib", "TGLExt.GlobalLiftLadder", "TGLExt.TheSingularExpectation", "TGLExt.TheTraceIsNotErasable",
                    "TGLExt.PageInformation", "TGLExt.FractalUnitarity", "TGLExt.TheWeightIsNotTheRank",
                    "TGLExt.TheVerbalCoupling", "TGLExt.TheSameBetaReadsThreeFaces", "TGLExt.IALDJones",
                    "TGLExt.TheVerbSelectsTheAction", "TGLExt.TheAxiomAndTheFalseWitness"],
        "declaracoes": DEC["n"], "teoremas": sum(1 for d in DEC["declaracoes"] if d["tipo"] == "theorem"),
        "defs": sum(1 for d in DEC["declaracoes"] if d["tipo"] != "theorem"),
        "beta_no_lean": "nunca: theta generico ou thetaMiguel c.beta com c : TGLCoupling",
    },
    "compilacao": {
        "toolchain": "Lean 4.31.0 (commit 68218e876d2a38b1985b8590fff244a83c321783), copiado do elan para sandbox\\toolchain_v4.31.0",
        "LEAN_PATH": REC["LEAN_PATH"], "comando": REC["comando"], "cwd": REC["cwd"],
        "exit_code": REC["exit_code"], "n_erros": REC["n_erros"], "n_avisos": REC["n_avisos"], "avisos": [],
        "ocorrencias_sorryAx": REC["ocorrencias_sorryAx"], "declaration_uses_sorry": REC["declaration_uses_sorry"],
        "saida": REC["saida"], "saida_sha256": REC["saida_sha256"],
        "olean": {"gerado_em": REC["olean"], "preservado_em": OLEAN, "bytes": REC["olean_bytes"], "sha256": olean_sha},
    },
    "auditoria_axiomas": {
        "arquivo": os.path.join(AQUI, "sandbox", "AuditTheUnitIsTheRank.lean"),
        "exit_code": RECA["exit_code"], "n_erros": RECA["n_erros"], "n_avisos": RECA["n_avisos"],
        "saida": RECA["saida"], "saida_sha256": RECA["saida_sha256"],
        "print_axioms_respondidos": AUD["print_axioms_respondidos"], "declaracoes_explicitas": AUD["declaracoes_explicitas"],
        "todas_no_trio": AUD["todas_no_trio"], "contagem_por_conjunto": AUD["contagem_por_conjunto_de_axiomas"],
        "varredura_constantes_do_modulo": AUD["varredura_constantes_do_modulo"],
        "varredura_fora_do_trio": AUD["varredura_fora_do_trio"], "varredura_sorryAx": AUD["varredura_sorryAx"],
        "enunciados_literalmente_True": AUD["enunciados_literalmente_True"],
        "veredito": AUD["veredito_auditoria"],
    },
    "nome_sem_peso": {
        "metodo": "termo de prova: para cada teorema do modulo (210 constantes, 197 teoremas incl. auxiliares), os binders "
                  "de tipo Prop que nao ocorrem no corpo da prova (MetaM: forallTelescope + Expr.beta + containsFVar)",
        "hipoteses_nao_usadas": AUD["hipoteses_sem_peso"],
        "leitura": "So as duas formas literais tem hipotese sem peso, ambas por desenho e documentadas (prefixo _): a "
                   "normalizacao <a,a> = 1 em P3.a e P^H = P em P4. Em todos os demais teoremas toda hipotese Prop ocorre "
                   "na prova. Nenhuma prova inteira e «nome sem peso»: nenhum enunciado e True e os controles C1–C14 "
                   "mostram que as hipoteses-chave sao necessarias. Sao TRIVIAIS por desenho (pre-registrado): as "
                   "re-exportacoes de B7.b, B7.c, B9.c; e auxiliares de ponte: rhoOut_eq_ad (rfl), dephasingActs_iff "
                   "(not_forall), rhoStar_unit e as formas *_literal (corolarios).",
    },
    "varredura_fonte": {k: VAR[k] for k in ("tokens_vetados_no_codigo", "tokens_vetados_em_comentarios",
                                            "literais_alpha_beta", "veredito")},
    "varredura_fonte_nota": "as ocorrencias em comentario de 'sorry' e 'axiom' sao a frase convencional «Sem sorry, sem "
                            "axiom.» do cabecalho; vocabulario proibido: 0 ocorrencias (VARREDURA_FONTE.json)",
    "por_parte": P,
    "controles": controles,
    "sondas_de_vacuidade": SONDAS,
    "resumo": {
        "PASSA": sorted(x["id"] for x in P if x["resultado_K"] == "PASSA"),
        "FALHA_negativos_honestos": sorted(x["id"] for x in P if x["resultado_K"] == "FALHA"),
        "CITADO": sorted(x["id"] for x in P if x["resultado_K"] == "CITADO"),
        "CITADO_REAL": sorted(x["id"] for x in P if x["resultado_K"] == "CITADO_REAL"),
        "NAO_FORMALIZADA": sorted(x["id"] for x in P if x["resultado_K"] == "NAO_FORMALIZADA"),
        "todas_conforme_o_esperado_na_face_K": all(x["conforme_o_esperado"] in (True, None) for x in P),
        "controles_FALHA_SEM_HIPOTESE": len(controles),
        "nota": "PASSA aqui e PASSA_K (validade na face K). O veredito da parte, pela regra (f), exige tambem a face O "
                "(outra unidade). FALHA em B5.e(ii), B9.a, B9.a' e o esperado pre-registrado (negativo honesto).",
    },
    "cetico_aferidor": {
        "mapa_de_rotas": "consultas so de leitura (rotas.py consultar); livro sha256 antes = depois",
        "consultas": {
            "k01 'TheUnitIsTheRank|unit.is.the.rank|unidade.e.o.rank'": J(os.path.join("consultas_mapa", "k01.json"))["n"],
            "k02 'F1.FREQUENCIA|frequencia_defasa|trilha POSTO'": J(os.path.join("consultas_mapa", "k02.json"))["n"],
            "k03 'pure_iff|estado puro|Tr.rho.2|pureza.*posto|posto.*pureza'": J(os.path.join("consultas_mapa", "k03.json"))["n"],
        },
        "k03_rota": "quantica.dobras_c3_hierarquia_e_matematica (hierarquia das dobras do validador C3; outro objeto)",
        "registros_no_livro": J(os.path.join("consultas_mapa", "k01.json"))["n_registros"],
        "cabeca": J(os.path.join("consultas_mapa", "k01.json"))["cabeca"],
        "nomes_livres": "env.contains (com os imports da pedra) e grep do kernel: nenhum dos nomes da pedra existia em "
                        "TGLExt, TGL, Matrix, Filter ou na raiz; a unica colisao (raiz: rank_eq_zero_iff, de modulos) foi "
                        "evitada com matrix_rank_eq_zero_iff (logs\\sonda_nomes2_SAIDA.txt)",
        "novidade": "«pureza <=> posto 1» geral, {Q_th, rho*} fora de th = 0, Ad(u) preserva o posto e S(th)^n eram "
                    "ausentes do kernel segundo o levantamento (2.3, 2.12, 2.6) e o pre-registro (cetico_aferidor); "
                    "aqui viram termos.",
    },
    "interface_atrator": "o posto que esta pedra tipa e o da LEITURA (P de posto 1 nos estados: P3, B1); a ponte proposta "
                         "e de estado (P3.b: a leitura de posto 1 aplicada a I/2 devolve rho*); a pedra NAO identifica P "
                         "com o R da F1.ATRATOR e nao refaz formal.singularidade_le_atrator",
    "nao_afirma": PRE["e_pedra"]["nao_afirma"],
    "achados_fora_do_preregistro": ACHADOS,
    "tgl_kernel_impressao_digital": {
        "antes": [ANTES["sha256_metadados"], ANTES["sha256_conteudo_lean"], ANTES["n_arquivos"]],
        "depois": [DEPOIS["sha256_metadados"], DEPOIS["sha256_conteudo_lean"], DEPOIS["n_arquivos"]],
        "igual": kernel_intacto,
    },
    "limpeza": {"toolchain_e_build_apagados": sandbox_limpo, ".lake_no_sandbox": lake_no_sandbox,
                "preservados": "pedra, snapshots das tentativas 02 e 03, auditoria, sondas de API, logs e recibos de "
                               "todas as tentativas, e o .olean final em olean\\ (sha256 acima)"},
    "tentativas": tent,
    "snapshots_sandbox_TGLExt": snap,
    "manifesto_3_KERNEL": manif,
}
dst = os.path.join(AQUI, "RESULTADO_KERNEL.json")
b = json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8") + b"\n"
with open(dst + ".tmp", "wb") as f:
    f.write(b)
assert os.path.getsize(dst + ".tmp") == len(b)
os.replace(dst + ".tmp", dst)
print(json.dumps({"RESULTADO_KERNEL.json": [len(b), hashlib.sha256(b).hexdigest()], "resumo": res["resumo"],
                  "kernel_intacto": kernel_intacto, "sandbox_limpo": sandbox_limpo}, ensure_ascii=False, indent=1))
