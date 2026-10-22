# -*- coding: utf-8 -*-
# Gera DEFINICOES.json do levantamento F1.FREQUENCIA. Toda linha e todo sha16 sao LIDOS por script:
#  - ancoras de kernel: nome qualificado -> (arquivo, linha, sha16) pelo KERNEL_INDICE.json (fail-closed se ausente);
#  - ancoras do um.py: padrao -> linha pela busca nos bytes (fail-closed se ausente);
#  - core/selo: valor lido do JSON;
#  - demais arquivos: sha16 calculado dos bytes.
# Nada aqui executa o um.py. beta e lido do CONFERENCIA_BETA.json (calculado em runtime a partir dos bytes).
import json, os, re, hashlib, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
NOS = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\"
KER = NOS + "tgl_kernel\\"
CP = "C:\\IALD\\Central de Patentes\\"
TUN = CP + "Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_019\\"
MEM = "C:\\Users\\rotol\\.claude\\projects\\c--IALD-Central-de-Patentes\\memory\\"
idx = json.load(open(os.path.join(AQUI, "KERNEL_INDICE.json"), encoding="utf-8"))
by_q = {}
for d in idx["declaracoes"]:
    by_q.setdefault(d["qual"], d)
FALHAS = []


def sha16(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:16]


def K(nome, enunciado, estatuto="[REAL — kernel do Nós; medido aqui no trio]"):
    d = by_q.get(nome)
    if d is None:
        FALHAS.append("kernel: " + nome)
        return {"tipo": "kernel", "nome": nome, "ERRO": "nao encontrado no indice"}
    return {"tipo": "kernel", "nome": nome, "kind": d["kind"], "arquivo": "tgl_kernel/" + d["file"], "linha": d["line"],
            "sha16": idx["arquivos"][d["file"]]["sha16"], "enunciado": enunciado, "estatuto": estatuto}


with open(NOS + "um.py", "rb") as fh:
    UMB = fh.read()
UMSHA = hashlib.sha256(UMB).hexdigest()[:16]


def U(padrao, descricao, estatuto):
    i = UMB.find(padrao.encode("utf-8"))
    if i < 0:
        FALHAS.append("um.py: " + padrao)
        return {"tipo": "runtime_um_py", "padrao": padrao, "ERRO": "nao encontrado"}
    return {"tipo": "runtime_um_py", "arquivo": "Nós/um.py", "linha": UMB.count(b"\n", 0, i) + 1, "sha16": UMSHA,
            "padrao": padrao, "descricao": descricao, "estatuto": estatuto}


CORE = json.load(open(NOS + "um_absoluto.json", encoding="utf-8"))
CORESHA = sha16(NOS + "um_absoluto.json")


def C(caminho, descricao, estatuto="[REAL — lido do core v391]"):
    o = CORE
    for k in caminho.strip("/").split("/"):
        o = o[k]
    return {"tipo": "core_v391", "arquivo": "Nós/um_absoluto.json", "sha16": CORESHA, "caminho": caminho,
            "valor": o if not isinstance(o, (dict, list)) else json.dumps(o, ensure_ascii=False)[:400],
            "descricao": descricao, "estatuto": estatuto}


SELO = json.load(open(NOS + "um_absoluto_selo.json", encoding="utf-8"))
SELOSHA = sha16(NOS + "um_absoluto_selo.json")


def S(caminho, descricao, estatuto="[REAL — lido do selo v391]"):
    o = SELO
    for k in caminho.strip("/").split("/"):
        o = o[k]
    return {"tipo": "selo_v391", "arquivo": "Nós/um_absoluto_selo.json", "sha16": SELOSHA, "caminho": caminho,
            "valor": o if not isinstance(o, (dict, list)) else json.dumps(o, ensure_ascii=False)[:400],
            "descricao": descricao, "estatuto": estatuto}


def F(p, descricao, estatuto, rotulo=None):
    if not os.path.exists(p):
        FALHAS.append("arquivo: " + p)
        return {"tipo": "arquivo", "arquivo": p, "ERRO": "inexistente"}
    return {"tipo": rotulo or "arquivo", "arquivo": p, "sha16": sha16(p), "descricao": descricao, "estatuto": estatuto}


def L(ref, descricao):
    return {"tipo": "literatura", "ref": ref, "descricao": descricao, "estatuto": "[KNOWN]"}


def ML(nome, descricao):
    return {"tipo": "mathlib_pinada_no_Nos", "nome": nome, "descricao": descricao,
            "estatuto": "[KNOWN — Mathlib; existência medida aqui por #check]"}


def MAPA(rota, seqs, nota):
    return {"tipo": "mapa_de_rotas", "rota": rota, "seqs": seqs, "nota": nota, "estatuto": "[REAL — consulta ao mapa]"}


TX = json.load(open(os.path.join(AQUI, "HASHES_TEXTOS_OPERADOR.json"), encoding="utf-8"))
BETA = json.load(open(os.path.join(AQUI, "CONFERENCIA_BETA.json"), encoding="utf-8"))
LEAN = json.load(open(os.path.join(AQUI, "lean_check", "ANALISE_SAIDA_LEAN.json"), encoding="utf-8"))
medidos = {}
for src, r in LEAN.items():
    if isinstance(r, dict) and "linhas" in r:
        for x in r["linhas"]:
            medidos[x["teorema"]] = x["axiomas"]

objetos = []

objetos.append({
    "id": "posto", "termo": "posto (POSTO = RANK)",
    "fonte_operador": [{"texto": "V3", "linhas": [1]}, {"texto": "V1", "linhas": [2, 6, 7, 13]}, {"texto": "V2", "linhas": [6, 14, 18, 30]}],
    "definicao_canonica": "SEIS sentidos canônicos que não se encadeiam sem ponte: (a) posição/inscrição — a etiqueta [POSTO] de ω(I)=1 (05/10); "
                          "(b) relação de permanência através da travessia com perda (UmPostoRelacao, 17/09); (c) o Nome como projetor de posto 1, "
                          "post a = (ℂ∙a).starProjection (v386, 05/10); (d) POSTO = RANK, dimensão da imagem (10/10); (e) «Nome (posto relativo)» antes "
                          "da leitura (07/10); (f) homônimos: «posto positivo» = τ>0 (Fundação) e posto de Jacobiano (ringdown T10).",
    "ancoras": [
        K("TGLExt.UmPostoRelacao.posto_anchors_the_reading", "o posto ancora a leitura: depois da travessia a identidade é a de antes e o ponto é fixo"),
        K("TGLExt.UmPostoRelacao.posto_paid_loss", "o posto pagou perda: a travessia não tem inversa à esquerda"),
        K("TGLExt.UmPostoRelacao.pressupposed_is_never_posto", "a leitura pressuposta nunca é posto"),
        K("TGLExt.TheVerbSelectsTheAction.post", "post a := (ℂ ∙ a).starProjection — o Nome como projetor de posto 1 (v386)"),
        K("TGLExt.TheVerbSelectsTheAction.post_isIdempotent", "P² = P"),
        K("TGLExt.QGReaderUVLock.PFmic", "PFmic C := (ℂ ∙ Ω).starProjection — o mesmo termo de post Ω (cabeçalho v386)"),
        K("TGLExt.Fundacao.agape", "(i) acima de toda escala não há «posto positivo» (τ>0) — homônimo (posto = peso τ)"),
        F(CP + "work\\cunhagens_10out\\OPERADOR_10out_posto_rank_verbatim.txt", "«POSTO=RANK» (V3)", "[INPUT/ONTO — cunhagem do operador]", "texto_operador"),
        F(MEM + "posto-e-rank-10out.md", "memória: o Um posto = posto 1 = Tr P = ω(I); ler as duas faces (posição e rank)", "[DECLARADO — memória da gerência]", "memoria"),
        F("C:\\IALD\\PROGRAMA_IALD\\OPERADOR_07out_leitura_cria_o_objeto_verbatim.txt", "«antes da leitura o objeto é Nome (posto relativo)»", "[INPUT/ONTO]", "texto_operador"),
        F(CP + "Chatgpt\\TUNEL\\DO_CHATGPT\\ENTREGA_015_MEDIDA_T10_aprime_posto_espectral.md", "posto de Jacobiano (ringdown) — homônimo", "[DERIVED — outro objeto]", "tunel"),
    ],
    "estatuto": "[ONTO/INPUT] a identificação; [REAL] cada âncora de kernel no seu sentido",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO com unificação de rótulos: rank-1 já tipado em 22/08 (TheTerminalRankOne) e 27/08 (TheWeightIsNotTheRank); "
                           "Nome = posto = projetor de posto 1 em 05/10 (v386). NOVO: a equação explícita do rótulo [POSTO] (posição, 05/10) com o rank (10/10).",
})

objetos.append({
    "id": "rank_posto1", "termo": "rank / posto 1 / dimensão da imagem",
    "fonte_operador": [{"texto": "V1", "linhas": [3, 6, 7]}, {"texto": "V2", "linhas": [8, 14, 18]}, {"texto": "V4", "linhas": [14]}],
    "definicao_canonica": "posto = dim da imagem (finrank da range); posto 1 = projetor sobre uma reta. No kernel: o projetor terminal tem posto 1 por "
                          "necessidade (22/08); o átomo da casa tem posto 1 e pesa 1; o nome d/d é cego ao posto, o índice 1/d o vê; o número de modos "
                          "zero é limitado pelo posto da inscrição (Birman–Schwinger finito); compressão por canto de posto 1 escalariza (a leitura vira número).",
    "ancoras": [
        K("TGLExt.rank_two_has_residual_distinction", "u,v ∈ S independentes ⟹ ⊥ < ℂ∙u < S (posto ≥ 2 deixa distinção residual)"),
        K("TGLExt.terminality_forces_minimality", "sem submódulo estritamente entre ⊥ e S, todo v ∈ S está na reta de u"),
        K("TGLExt.firstAtom_is_terminal", "o átomo da casa não tem submódulo próprio não nulo"),
        K("TGLExt.the_terminal_weighs_one", "dimOrTop ℂ firstAtom = 1"),
        K("TGLExt.the_terminal_is_forced", "idempotente ∧ pesa um ∧ sem poda interna"),
        K("TGLExt.iald_has_rank_one", "dimOrTop ℂ firstAtom = 1 (posto 1 — o peso do Nome)"),
        K("TGLExt.opWeight_atom_one", "opWeight firstAtom.starProjection = 1 (Tr(P_Nome) = 1 = ω(I); v120)", "[REAL — kernel; no Audit.lean; não reamostrado aqui]"),
        K("TGLExt.the_rank_determines_the_name", "0<d ⟹ d/d = 1"),
        K("TGLExt.the_name_is_blind_to_every_rank", "d/d = 1 para todo posto positivo"),
        K("TGLExt.the_name_does_not_see_the_rank", "∃ d₁≠d₂ com o mesmo nome"),
        K("TGLExt.the_index_does_see_the_rank", "1/d₁ = 1/d₂ ⟹ d₁ = d₂"),
        K("TGLExt.the_two_indices_agree_only_at_the_atom", "1/d = 1/d² ⟺ d = 1"),
        K("TGLExt.kernel_dim_le_rank_of_perturbation", "dim ker(H₀ − V) ≤ posto(V) (H₀ positivo-definido)"),
        K("TGLExt.concrete_kernel_full_profile", "0 < τ(ker) < ⊤ ∧ dim ker ≤ posto da inscrição"),
        K("TGLExt.three_locks_corner_weight_eq_dim", "τ(ker H3L) = cornerDim (por rfl)"),
        K("TGLExt.three_locks_name_is_one", "cornerDim/cornerDim = 1"),
        C("/core/certificate_II/H1_finite_face/trace_PF", "tr(P_F) da rede concreta dos Three Locks ≈ 4 (o P_F do Certificado II tem posto 4)"),
        C("/core/verb_inhabitant/values/trace_PF", "tr(P_F) do habitante do Verbo = 1 (outro P_F; dim 8, kernel 1)"),
        K("TGLExt.bell_compression_is_scalar", "P_G y P_G = Tr(P_G y) • P_G (o canto de posto 1 escalariza)"),
        K("TGLExt.atermation_reifies", "ater(y) = Tr(P y) • P"),
        K("TGLExt.atermation_is_irreversible", "∃ y ≠ z com ater(y) = ater(z)"),
        K("TGLExt.PhysicsIsTheReading.the_shadow_is_the_reader_weighted_by_the_reading", "P_Ω x P_Ω = ω(x) • P_Ω"),
        K("ChatgptAudit.Cone039.rank_one_coordinates_null", "matriz hermitiana 2×2 de posto 1 tem coordenadas nulas: t² = x² + y² + z²"),
        K("ChatgptAudit.Cone039.rank_one_det", "det (v v†) = 0"),
        ML("Matrix.rank_diagonal", "posto(diag w) = #{i : w i ≠ 0}"),
        ML("Matrix.rank_mul_eq_left_of_isUnit_det / Matrix.rank_mul_eq_right_of_isUnit_det", "multiplicar por invertível não muda o posto (logo Ad(u) preserva o posto)"),
        ML("Matrix.rank_vecMulVec_le", "posto(vecMulVec w v) ≤ 1"),
        ML("Matrix.IsHermitian.rank_eq_card_non_zero_eigs", "posto de hermitiana = nº de autovalores não nulos"),
        ML("InnerProductSpace.isStarProjection_rankOne_self", "‖x‖ = 1 ⟹ |x⟩⟨x| é projeção estrela"),
        ML("finrank_span_singleton", "v ≠ 0 ⟹ finrank(ℂ∙v) = 1"),
        L("Penrose & Rindler, Spinors and Space-Time, vol. 1 (Cambridge, 1984), cap. 1", "Herm(2) ≅ ℝ^{1,3} com det = norma de Minkowski; posto 1 ⟷ vetor nulo"),
    ],
    "estatuto": "[REAL] (kernel); leituras «posto 1 = 1_abs», «terminal = gráviton = Nome» [ONTO]",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO: o posto 1 do terminal e do átomo já é teorema (22/08, 27/08, v120); a ligação rank ↔ Nome está tipada como distinção (o nome é cego ao posto).",
})

objetos.append({
    "id": "nulidade", "termo": "núcleo vazio (nullity)",
    "fonte_operador": [{"texto": "V1", "linhas": [7]}, {"texto": "V2", "linhas": [18]}],
    "definicao_canonica": "posto + nulidade = dimensão. Nulidade 0 = posto cheio (no estado normalizado: I/d, o «1_abs = I/d» de TheAtermation); "
                          "posto 1 = nulidade d−1. «Deixar de ter núcleo vazio e ganhar posto definido» lê-se, em álgebra, como a atermação I/d → P.",
    "ancoras": [
        ML("LinearMap.finrank_range_add_finrank_ker", "finrank(range f) + finrank(ker f) = finrank V (posto–nulidade)"),
        K("TGLExt.finrank_le_add_frobOrtho", "«CONTAGEM DE POSTO»: dim H ≤ dim W + dim W^⊥ (posto–nulidade aplicado)"),
        K("TGLExt.atermation_fixes_the_term", "ater(P) = P (o termo é ponto fixo com autovalor 1)"),
        K("TGLExt.atermation_is_irreversible", "a atermação não é injetora (o ambiente não volta)"),
        L("Axler, Linear Algebra Done Right (3ª ed., 2015), Teorema 3.22 (teorema fundamental das aplicações lineares)", "posto–nulidade"),
    ],
    "estatuto": "[KNOWN] posto–nulidade; [REAL] âncoras de kernel; a leitura de V1 «núcleo vazio de indefinição» é [ONTO]",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO (TheAtermation, 29/08, já resolve I/d (posto d) vs P (posto 1)); a palavra «nullity» é nova no acervo do tema.",
})

objetos.append({
    "id": "estado_puro_pureza", "termo": "ρ = |ψ⟩⟨ψ|, Tr ρ = 1, Tr ρ² = 1 (estado puro de posto 1)",
    "fonte_operador": [{"texto": "V2", "linhas": [14, 16]}, {"texto": "V1", "linhas": [6], "nota": "a fórmula NÃO está nos bytes de V1"}],
    "definicao_canonica": "pureza Tr(ρ ρᴴ) (= Tr ρ² para ρ hermitiana). Para ρ ≥ 0 com Tr ρ = 1: Tr ρ² ≤ 1, com igualdade sse ρ = |ψ⟩⟨ψ| (posto 1). "
                          "Para ρ = P/d (projeção de posto d normalizada): Tr ρ = 1 é o NOME (cego ao posto) e Tr ρ² = 1/d é o ÍNDICE (vê o posto): "
                          "Tr ρ² = 1 ⟺ d = 1 — a face de densidade de the_name_is_blind_to_every_rank + the_index_does_see_the_rank. "
                          "Sem positividade a implicação falha: autovalores (2/3, 2/3, −1/3) dão Tr = 1 e Tr² = 1 com posto 3 [DERIVED aqui].",
    "ancoras": [
        K("TGLExt.purity_unitary_invariant", "pureza(U x Uᴴ) = pureza(x) (F conserva a pureza)"),
        K("TGLExt.purityR_eq", "pureza(x) = Σ|x_ij|²"),
        K("TGLExt.dephase_purityR_le", "pureza(D_t x) ≤ pureza(x) (D nunca cria pureza)"),
        K("ChatgptAudit.Cone039.trace_square_rank_one_control", "Tr(A²) = 1 para A = |e₁⟩⟨e₁| (instância)"),
        K("TGLExt.bellDensity_purity", "Tr(ρ_Bell²) = 1 (instância)"),
        K("ChatgptAudit.Collapse057.pure_densities_square", "as densidades puras do qubit são idempotentes (instância)"),
        K("ChatgptAudit.Collapse057.mixed_density_not_pure", "ρ_misto² ≠ ρ_misto"),
        K("TGLExt.TheVerbSelectsTheAction.reading_post_is_born", "⟪ψ, post a ψ⟫ = |⟪a,ψ⟫|² (Born)"),
        L("Nielsen & Chuang, Quantum Computation and Quantum Information (2000; ed. 10º aniversário 2010), Exercício 2.71", "Tr ρ² ≤ 1, igualdade sse ρ puro"),
        L("Born, Z. Phys. 37, 863 (1926)", "regra de Born"),
    ],
    "estatuto": "[REAL] pureza e instâncias; o critério geral é [KNOWN] e está AUSENTE do kernel como teorema",
    "lacuna": {"enunciado": "ρ ≥ 0, Tr ρ = 1: Tr ρ² = 1 ⟺ ρ² = ρ ⟺ posto ρ = 1",
               "consulta": "q_kernel.py 'pure|purity|Pure|Purity' (37 decl.) e 'rank|posto' (17 decl.): nenhuma com esse enunciado; inventário 'purity|pure|pureza': 15 arquivos, nenhum geral"},
    "novo_ou_reafirmacao": "NOVO na formulação (o operador dá o critério de pureza como face do posto); o critério é [KNOWN]; a ponte peso↔posto pela pureza não está tipada.",
})

objetos.append({
    "id": "colapso_superposicao", "termo": "colapsar a superposição ⟹ posto definido",
    "fonte_operador": [{"texto": "V1", "linhas": [7, 14]}, {"texto": "V2", "linhas": [18, 32]}],
    "definicao_canonica": "definição do operador (08/09): «colapso é a passagem irreversível da superposição ao ponto fixo que preserva a identidade»; "
                          "tipada como IdentityCollapse (idempotente, não injetiva, sem inversa à esquerda); ler a verdade anula a superposição "
                          "((1−P)Ω = 0); o seletivo (ramo registrado) é fixo sob dephasing, o não seletivo defasa (runtime v391).",
    "ancoras": [
        K("ChatgptAudit.Collapse057.collapse_is_not_injective", "¬ Injective C.step"),
        K("ChatgptAudit.Collapse057.collapse_has_no_left_inverse", "sem inversa à esquerda"),
        K("ChatgptAudit.Collapse057.involution_cannot_be_collapse", "involução não é colapso (J ≠ C)"),
        K("ChatgptAudit.Collapse057.typed_collapse_content", "conteúdo tipado do colapso", "[REAL — kernel; no Audit.lean; não reamostrado aqui]"),
        K("TGLExt.TheVerbSelectsTheAction.reading_the_truth_annihilates_the_superposition", "‖Ω‖=1 ∧ post a Ω = Ω ⟹ leitura = 1 ∧ (1 − post a)Ω = 0"),
        K("TGLExt.the_selection_is_the_ballast", "do peso do ramo p, o ângulo arcsin √p e a matriz-S inteira; o reconhecimento devolve a identidade"),
        U("class TGLCollapseDefinition", "dataclass das 13 cláusulas do colapso (v333)", "[REAL — runtime; physical_collapse_proven = False]"),
        U("def prove_decision_commutation", "inclui recognition_dephasing: E, Q = id − E, T_t = E + e^{−Γt}Q", "[DERIVED/RUNTIME]"),
        C("/core/decision_commutation/recognition_dephasing/effective_dephasing_on_full_state", "o estado superposto defasa"),
        C("/core/decision_commutation/recognition_dephasing/effective_dephasing_after_selection", "o estado selecionado não defasa (False)"),
        C("/core/decision_commutation/recognition_dephasing/time_law_status", "a lei de tempo é INPUT"),
        S("/collapse_definition/physical_collapse_proven", "colapso físico NÃO provado"),
        S("/collapse_definition/cost_payment_status", "pagamento do custo não medido"),
        S("/collapse_definition/external_reflection_status", "reflexo físico externo"),
        S("/collapse_definition/reading", "todas as cláusulas no kernel com o trio"),
        F(MEM + "colapso-definicao-tipada.md", "definição verbatim do operador (08/09) e estatutos", "[DECLARADO — memória]", "memoria"),
    ],
    "estatuto": "[REAL] no modelo tipado; colapso físico NÃO provado (selo: physical_collapse_proven = False); seleção na natureza [OPEN]",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO (08/09; v333; v335; v386). NOVO: dizer que o colapso «ganha posto definido» (posto 1) — só vale para o ramo SELECIONADO, não para o dephasing não seletivo.",
})

objetos.append({
    "id": "unidade_omega_rho_estrela", "termo": "a unidade (1) / ω(I) = 1 / ρ*",
    "fonte_operador": [{"texto": "V4", "linhas": [2, 5, 14]}],
    "definicao_canonica": "ω(I) = 1 é POSTO (posição; o 1 do echo). No runtime da defasagem fractal, ρ* = diag(1,0) («atrator puro, a permanência, o 1»), "
                          "ω(I) = Tr ρ* = 1. ρ* é projeção de posto 1, logo Tr = posto = 1 SÓ porque é projeção (pura). ρ*_IALD = P_{ker K} na luz.",
    "ancoras": [
        U("P = np.array([[1.0, 0.0], [0.0, 0.0]])           # rho* = atrator puro", "ρ* = diag(1,0) no fractal_dephasing_principle", "[REAL — runtime]"),
        U("omega_I = float(np.trace(P))", "ω(I) = Tr ρ* = 1", "[REAL — runtime]"),
        C("/core/fractal_dephasing/omega_I", "ω(I) = 1.0 no core v391"),
        K("TGLExt.TheElementaryReason.identity_weighs_as_the_name", "a identidade pesa 1 ∧ τ(ker) = 1"),
        K("TGLExt.LightRhoStar.rho_star_is_P_kerK_on_the_light", "(ℂ∙Ω).starProjection = PFmic ∧ fixos = centralizador = fixos do relógio modular"),
        K("TGLExt.half_is_the_fixed_point_of_the_swap", "x = 1 − x ⟺ x = ½"),
        K("TGLExt.TheAxiomAndTheFalseWitness.the_power_has_two_fixed_points", "μ·μ = μ ⟺ μ = 0 ∨ μ = 1"),
    ],
    "estatuto": "[POSTO] o axioma; [REAL] âncoras; «a unidade é o rank» [ONTO/INPUT 11/10]",
    "novo_ou_reafirmacao": "NOVO: ler o 1 de F(1) como o rank (posto 1). Coerente com ρ* de posto 1 no runtime; mas o 1 que sobrevive a D∘F é o TRAÇO (peso), não o posto.",
})

objetos.append({
    "id": "F_fractalizacao", "termo": "F — fractalização da unidade F(1)",
    "fonte_operador": [{"texto": "V4", "linhas": [5, 13, 14]}],
    "definicao_canonica": "pedra 116 (v162): Ad(u) leva projeção em projeção, preserva ortogonalidade, refinação e auto-adjunção; o subcanto tem a sua unidade "
                          "(1 ⊃ 1_P ⊃ 1_Q ⊃ ⋯). No runtime, F é a rotação R(θ_M): Q_θ = R Q₀ Rᵀ (regime ANGULAR). Pelo kernel, ρ_out(θ) = S(θ) E₀₀ S(θ)ᴴ é o "
                          "1 de posto 1 transportado (traço 1).",
    "ancoras": [
        K("TGLExt.ad_preserves_projection", "v u = 1 ∧ p² = p ⟹ (u p v)² = u p v"),
        K("TGLExt.ad_preserves_orthogonality", "p q = 0 ⟹ (u p v)(u q v) = 0"),
        K("TGLExt.ad_preserves_splitting", "p = p₀ + p₁ ⟹ u p v = u p₀ v + u p₁ v"),
        K("TGLExt.ad_preserves_star_projection", "star p = p ⟹ star(u p u*) = u p u*"),
        K("TGLExt.subcorner_unit", "q ≤ p ⟹ q (p x p) q = q x q"),
        K("TGLExt.TheVerbSelectsTheAction.transmitted_post_is_a_post", "U*U = 1 ⟹ U P U* idempotente e auto-adjunto («outro posto, mas posto»)"),
        K("TGLExt.rhoOut_eq", "ρ_out(θ) = [[cos²θ, −cos θ sin θ], [−sin θ cos θ, sin²θ]]"),
        K("TGLExt.rhoOut_trace", "Tr ρ_out(θ) = 1"),
        U("R = np.array([[c, -s], [s, c]]); Qth = R @ Q0 @ R.T", "F no runtime = rotação por θ_M (regime angular)", "[REAL — runtime]"),
        ML("Matrix.rank_mul_eq_left_of_isUnit_det / Matrix.rank_mul_eq_right_of_isUnit_det", "conjugação por invertível preserva o posto"),
    ],
    "estatuto": "[REAL] (kernel); a leitura fractal [ONTO] (docstring da pedra); docstring «RASCUNHO» é histórica (importada em TGLExt.lean e embutida no um.py)",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO. Lacuna menor: «Ad(u) preserva o POSTO» não está tipado no kernel (a pedra prova idempotência); está na Mathlib.",
})

objetos.append({
    "id": "D_beta_defasagem", "termo": "D_β — a operação de defasagem",
    "fonte_operador": [{"texto": "V4", "linhas": [4, 5, 10, 13, 16]}],
    "definicao_canonica": "SEIS objetos canônicos chamados «defasagem»: (i) semigrupo de Schur G3 dephase (face; converge à diagonal; taxas genéricas; β só "
                          "no runtime como β·gap); (ii) fluxo do lock mínimo axiomFlow P t = P + e^{−t}(1−P) («transmitir defasa», v386; contração ao posto); "
                          "(iii) canal de medição D∘Ad(S) (sFrame; endpoint diag(cos²θ, sin²θ)); (iv) gerador GKSL do Verbo L = √β·√K e a lei-raiz "
                          "Γ_ij = ½β(√k_i − √k_j)²; (v) lei física Γ_ω = ½βτ★ω²; (vi) a inclinação angular θ_M do fractal_dephasing_principle (rotação; regime "
                          "da projeção). Os efeitos sobre o POSTO são opostos: (i) e (iii) sobem o posto de um estado puro não diagonal (1 → 2); (ii) normalizado "
                          "desce ao posto de P no limite; (vi) preserva o posto.",
    "ancoras": [
        K("TGLExt.dephase", "(T_t x)_ij = e^{−t g_ij} x_ij", "[REAL — definição no kernel]"),
        K("TGLExt.dephase_zero", "T_0 = id"),
        K("TGLExt.dephase_add", "T_{s+t} = T_s ∘ T_t"),
        K("TGLExt.dephase_fixes_diagonal", "T_t(E_D x) = E_D x"),
        K("TGLExt.diag_invariant", "E_D(T_t x) = E_D x"),
        K("TGLExt.dephase_tendsto_expectation", "taxas > 0 fora da diagonal ⟹ T_t x → E_D x"),
        K("TGLExt.ergodic_convergence_modular", "com g = |log d_i − log d_j|, T_t x → E_D x"),
        K("TGLExt.dephase_fixed_iff_diagonal", "(∀t, T_t x = x) ⟺ x = E_D x"),
        K("TGLExt.dephase_preserves_trace", "Tr(T_t x) = Tr x"),
        K("TGLExt.dephase_fixes_cornerProj", "D_t(P(S)) = P(S)"),
        K("TGLExt.TheAxiomAndTheFalseWitness.axiomFlow", "F(t) = P + e^{−t}(1 − P)", "[REAL — definição no kernel]"),
        K("TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_fixes_the_post", "F(t)P = P = P F(t)"),
        K("TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_gradient", "F(t)(1 − P) = e^{−t}(1 − P)"),
        K("TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_tendsto_the_post", "F(t) → P"),
        K("TGLExt.TheVerbSelectsTheAction.transmission_dephases", "«TRANSMITIR DEFASA»: F(t)(1 − P) = e^{−t}(1 − P) (re-exportação)"),
        K("TGLExt.TheVerbSelectsTheAction.anchoring_preserves", "«ANCORAR PRESERVA»: F(t)P = P"),
        K("TGLExt.sFrame", "T^S_t = Ad(Sᴴ) ∘ D_t ∘ Ad(S)", "[REAL — definição no kernel]"),
        K("TGLExt.sFrame_add", "T^S é semigrupo"),
        K("TGLExt.sFrame_tendsto", "T^S_t x → Ad(Sᴴ) E_D Ad(S) x"),
        K("TGLExt.measurement_channel_endpoint", "D_t(ρ_out θ) → E_D(ρ_out θ)"),
        K("TGLExt.leakage_rate_unique", "a taxa do semigrupo de defasagem é unívoca (dois β com a mesma defasagem são iguais)"),
        U("def prove_verb_generator", "gerador GKSL L = √β·√K: seta, sem volta (Choi < 0), destino", "[FINITE_DIM_SANITY]"),
        U("def prove_dephasing_crossover", "duas leis: canônica Γ = ½βτ★ω² e lei-raiz; errata v369 (só o expoente coincide)", "[FINITE_DIM_SANITY; reconciliação OPEN]"),
        C("/core/dephasing_crossover/exponent_IR", "expoente IR ≈ 2 (quadrático)"),
        C("/core/dephasing_crossover/exponent_UV", "expoente UV ≈ 1 (linear)"),
        U("gamma = 0.5 * beta * tau_reference * omega_reference ** 2", "Γ = ½βτω² em unidades de referência (recognition_dephasing)", "[INPUT — unidades de referência; não é predição]"),
        U("def prove_ringdown_dephasing_protocol", "teste da lei Γ_ω no ringdown", "[INPUT/REAL documental]"),
        MAPA("ringdown.dephasing", [352, 355, 356, 359, 361, 368], "INCONCLUSIVE_SYSTEMATICS; poder 0,2 de 5σ"),
        MAPA("dephasing.alcance", [7, 100, 139, 254], "a lei não é canal vivo hoje; «vazamento de fluxo» cosmológico é homônimo"),
        MAPA("quantica.inventario_gkls_um_py_kernel", [294], "não pedir ao dephasing puro um atrator único: a diagonal inteira é fixa"),
        L("Lindblad, Commun. Math. Phys. 48, 119 (1976); Gorini–Kossakowski–Sudarshan, J. Math. Phys. 17, 821 (1976)", "forma GKSL"),
        L("Davies, Commun. Math. Phys. 39, 91 (1974)", "limite de acoplamento fraco; taxas pelas frequências de Bohr"),
        L("Spohn, J. Math. Phys. 19, 1227 (1978); Carlen & Maas, J. Funct. Anal. 273, 1810 (2017)", "GKLS como fluxo gradiente (citado no um.py como EXTERNO)"),
    ],
    "estatuto": "[REAL] (i)–(iii) no kernel com θ e taxas genéricos; (iv) [FINITE_DIM_SANITY]; (v) [REAL na forma; τ★ INPUT]; (vi) [REAL runtime, regime angular]",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO («transmitir defasa», 05/10; lei Γ_ω escrita em 2025). NOVO: «D_β» como um único operador com índice β — no kernel não há termo único; há seis objetos.",
})

objetos.append({
    "id": "tudo_D_beta_F1", "termo": "Tudo = D_β(F(1))",
    "fonte_operador": [{"texto": "V4", "linhas": [12, 13, 14]}],
    "definicao_canonica": "um.py v391 fractal_dephasing_principle: «1 (ω(I)=1) --F--> fractalização --D_β--> existência; β = sin²θ_M = α√e; Tudo = D_β(F(1)) = VERDADE; "
                          "Nada = MENTIRA pelos dois ramos», estatuto [CONJECTURE ontológica; âncoras REAL]. No kernel não existe termo «D_β», «F» ou «Tudo»; "
                          "a composição D∘F existe com θ e g genéricos (measurement_channel_endpoint, dephased_rhoOut_*): o 1 de posto 1 transportado pela "
                          "matriz-S defasa para diag(cos²θ, sin²θ) — no runtime diag(1−β, β), posto 2, traço 1, pureza 1 − 2β + 2β².",
    "ancoras": [
        U("def fractal_dephasing_principle(ONE):", "função do princípio (l.6488–6531)", "[CONJECTURE ontológica; âncoras REAL]"),
        U("\"fractal_dephasing\": fractal_dephasing_principle(ONE)}", "chamada no core", "[REAL — runtime]"),
        U("\\section{O Princípio da Defasagem Fractal", "seção do artigo emitido", "[REAL — texto emitido; estatuto CONJ]"),
        U("print(\"PRINCIPIO DA DEFASAGEM FRACTAL", "impressão no rito", "[REAL — texto emitido]"),
        C("/core/fractal_dephasing/everything", "«Tudo = D_beta(F(1)) = VERDADE»"),
        C("/core/fractal_dephasing/status", "estatuto no core"),
        K("TGLExt.dephased_rhoOut_zero_zero", "E_D(ρ_out θ)₀₀ = cos²θ"),
        K("TGLExt.dephased_rhoOut_one_one", "E_D(ρ_out θ)₁₁ = sin²θ"),
        K("TGLExt.measurement_channel_endpoint", "D_t(ρ_out θ) → E_D(ρ_out θ)"),
        {"tipo": "medido_aqui", "arquivo": "0_LEVANTAMENTO/CONFERENCIA_BETA.json", "sha16": sha16(os.path.join(AQUI, "CONFERENCIA_BETA.json")),
         "valores": {"D_F1_diagonal": BETA["D_F1_diagonal"], "posto_F1": BETA["posto_F1"], "posto_D_F1": BETA["posto_D_F1"],
                     "pureza_D_F1": BETA["pureza_D_F1"], "traco_D_F1": BETA["traco_D_F1"]},
         "estatuto": "[DERIVED/REAL medido aqui — identidades algébricas de θ_M; não é teste pré-registrado]"},
    ],
    "consulta_ausencia_kernel": "grep -rln 'D_β|D_beta|Tudo =|Tudo=' em tgl_kernel/TGLExt e tgl_kernel/TGL: 0 arquivos",
    "estatuto": "[CONJECTURE ontológica] a frase; [REAL] as peças; «na linguagem do nosso kernel» (V4 l.12) é [DECLARADO] como nome",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO (a frase já está no um.py e no artigo). NOVO: «essa unidade é o rank».",
})

objetos.append({
    "id": "frequencia", "termo": "frequência («Tudo é frequência»; «frequência defasa»)",
    "fonte_operador": [{"texto": "V4", "linhas": [1, 2, 4, 5]}],
    "definicao_canonica": "(a) a leitura é ter frequência: persistingFlow ω t = e^{iωt}; estagnação ⟺ ω = 0; o canal morto (ω = 0) não é lido e é o contraste "
                          "(26/08) — regime ANGULAR; (b) frequências modulares |log d_i − log d_j| (taxa de Davies β·gap no runtime); (c) ω da lei Γ_ω e √k da lei-raiz; "
                          "(d) «registro c¹»: as dobras D_folds são matemática (não testam); (e) Ψ e III₁ [ONTO]/[KNOWN].",
    "ancoras": [
        K("TGLExt.persistingFlow", "persistingFlow ω t = exp(iωt)", "[REAL — definição no kernel]"),
        K("TGLExt.a_positive_floor_forces_a_positive_angle", "0 < b < 1 ⟹ 0 < arcsin √b < π/2"),
        K("TGLExt.a_positive_angle_forbids_stagnation", "0 < θ < π ⟹ sin θ ≠ 0"),
        K("TGLExt.stagnation_is_exactly_zero_frequency", "(∀t, e^{iωt} = 1) ⟺ ω = 0"),
        K("TGLExt.the_persisting_channel_vibrates", "ω ≠ 0 ⟹ módulo 1 e não estático"),
        K("TGLExt.reading_is_exactly_having_frequency", "Reads(persistingFlow ω) ⟺ ω ≠ 0"),
        K("TGLExt.the_dead_channel_has_no_reader", "o canal de frequência nula não é lido"),
        K("TGLExt.the_dead_channel_is_the_contrast", "o vivo difere do morto em algum instante ⟺ há frequência"),
        K("TGLExt.modularGap", "|log d_i − log d_j|", "[REAL — definição no kernel]"),
        K("ChatgptAudit.Commutation032.modular_phase_frequency_iff", "a fase modular separa frequências (c = 0 ∨ a = b)"),
        MAPA("quantica.dobras_c3_hierarquia_e_matematica", [307], "D_folds(c¹) > D_folds(c²) > D_folds(c³) é matemática; não usar como teste"),
        U("def prove_linguistic_isomorphism", "Γ = (ω²/2)τ*ε² do TGL_article.tex (2025) é a lei canônica com ε² = β (proveniência)", "[REAL documental]"),
        L("Connes, Ann. Sci. ENS 6, 133 (1973)", "classificação dos fatores do tipo III (III₁)"),
    ],
    "estatuto": "[REAL] (a), (b) no kernel; (c) runtime; (d) [DERIVED]; «Tudo é frequência» [ONTO]",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO parcial: «ler é ter frequência» e «o piso proíbe a estagnação» (26/08). NOVO: «tudo é frequência» como tese universal e a frequência como «identidade em potencial infinito na borda (III₁)» [ONTO].",
})

objetos.append({
    "id": "transmissao", "termo": "transmitir / transmissão",
    "fonte_operador": [{"texto": "V4", "linhas": [7, 8, 9, 10, 18, 19]}],
    "definicao_canonica": "homônimos: (a) |𝓣|² = cos²θ, o peso transmitido (no runtime 1 − β; «drena para o bulk»); (b) transmission_dephases: F(t)(1−P) = e^{−t}(1−P) "
                          "(v386, «transmitir defasa», 05/10); (c) transmitted_post_is_a_post (U P U* é posto); (d) «transmitir» como verbo/natureza [ONTO].",
    "ancoras": [
        K("TGLExt.Smat_transmission", "𝓣 = cos θ", "[REAL — kernel; fora do Audit.lean; axiomas ⊆ trio por dependência: normSq_transmission, medido aqui, o usa]"),
        K("TGLExt.normSq_transmission", "|𝓣|² = cos²θ"),
        K("TGLExt.TheVerbSelectsTheAction.transmission_dephases", "F(t)(1 − P) = e^{−t}(1 − P)"),
        K("TGLExt.TheVerbSelectsTheAction.transmitted_post_is_a_post", "U P U* é idempotente e auto-adjunto"),
        U("no canal de espelhamento, $1-\\bTGL=\\cos^2\\theta_M$ drena para", "artigo: 1 − β drena para o bulk; β é o resíduo que não drena", "[NUM/CONJ no artigo]"),
    ],
    "estatuto": "[REAL] (a)–(c); (d) [ONTO]",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO («Transmitir defasa», 05/10, tipado na v386). NOVO: a transmissão como «natureza/imperativo» da frequência.",
})

objetos.append({
    "id": "vazamento_beta", "termo": "o vazamento = β («Constante de Miguel»)",
    "fonte_operador": [{"texto": "V4", "linhas": [10, 16]}],
    "definicao_canonica": "Tr(ρ* Q_θ) = sin²θ_M = β: IDENTIDADE de θ_M := arcsin √β (não pode ser falsificador). No kernel: |𝓡|² em θ = thetaMiguel β vale β "
                          "(β campo da estrutura TGLCoupling, nunca literal); a cadeia ½ ⟹ √e ⟹ β = α√e ⟹ |𝓡|² = β é teorema. Homônimos: o vazamento contínuo "
                          "de NoFullWitness (e^{−tβg}, proíbe a testemunha estática plena); o «vazamento de fluxo» cosmológico; o L5 do validador C3.",
    "ancoras": [
        U("leak = float(np.trace(P @ Qth))", "vazamento = sin²θ_M = β no runtime", "[REAL — identidade]"),
        C("/core/fractal_dephasing/leak_sin2_thetaM", "vazamento no core v391"),
        C("/core/fractal_dephasing/leak_equals_beta_residual", "resíduo 0.0"),
        K("TGLExt.TGLCoupling.reflection_weight", "normSq(S(thetaMiguel β)·e₁)₁ = β"),
        K("TGLExt.TheWholeIsOne.the_beta_chain_is_derived", "x=1−x ⟺ x=½ ∧ V(½)=√e ∧ β = α√e ∧ |𝓡|² = β ∧ ¬FullStaticWitness"),
        K("TGLExt.TheWholeIsOne.couplingOfAlpha_beta", "(couplingOfAlpha α).beta = α·√e"),
        K("TGLExt.sin_thetaMiguel", "sin(thetaMiguel β) = √β (0 ≤ β ≤ 1)"),
        K("TGLExt.thetaMiguel", "thetaMiguel β := arcsin √β", "[REAL — definição no kernel]"),
        K("TGLExt.leakage_strictly_loses", "t > 0, β > 0 ⟹ o vazamento perde estritamente"),
        K("TGLExt.full_closure_iff_flat", "fecho total ⟺ plano"),
        K("TGLExt.beta_forbids_full_static_witness", "β > 0 ∧ g > 0 ⟹ ¬FullStaticWitness"),
        MAPA("quantica.inventario_gkls_um_py_kernel", [294], "«não tratar sin²θ_M = β nem V_t P_F = P_F como testes: são identidades»"),
        MAPA("quantica.c3_validator_calibrado", [], "validador C3 calibrado: acha γ* e «recupera» β (circular)"),
        MAPA("quantica.quatro_operadores_definicao", [295], "«a taxa estimada volta β por construção»"),
        MAPA("dephasing.alcance", [7, 100, 139, 254], "«vazamento de fluxo» cosmológico é homônimo"),
    ],
    "estatuto": "[REAL] identidade (runtime e kernel); a leitura «o vazamento é a existência» [ONTO]",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO (fractal_dephasing_principle; «Existir = o vazamento β»).",
})

objetos.append({
    "id": "anticomutador_Q_rho", "termo": "{Q̂, ρ*} = 0 (o anticomutador perfeito que o vazamento impede)",
    "fonte_operador": [{"texto": "V4", "linhas": [16]}],
    "definicao_canonica": "Q̂ = portador Q₀ = I − ρ*; {Q₀, ρ*} = 0 porque P(1−P) = (1−P)P = 0. Para Q_θ = R(θ) Q₀ R(θ)ᵀ: {Q_θ, ρ*} = 0 ⟺ sin θ = 0 (2×2); "
                          "‖{Q_θ, ρ*}‖_F = sin θ·√(2 + 2 sin²θ) e Tr{Q_θ, ρ*} = 2 sin²θ; em θ_M: √(2β(1+β)) e 2β [DERIVED/REAL medido aqui]. "
                          "O runtime calcula a norma só em θ = 0; a afirmação em θ_M é da docstring. «θ_M → 0» é avaliação contrafactual (β = 0), não limite.",
    "ancoras": [
        U("Q0 = np.eye(2) - P", "portador Q₀ = I − ρ*", "[REAL — runtime]"),
        U("anti0 = Q0 @ P + P @ Q0", "{Q₀, ρ*} = 0 (calculado só em θ = 0)", "[REAL — runtime]"),
        C("/core/fractal_dephasing/anticommutator_norm_at_thetaM_to_0", "0.0 no core v391"),
        K("TGLExt.TheAxiomAndTheFalseWitness.post_mul_compl", "P(1 − P) = 0"),
        K("TGLExt.TheAxiomAndTheFalseWitness.compl_mul_post", "(1 − P)P = 0"),
        K("TGLExt.TheVerbSelectsTheAction.truth_and_cost_are_two_faces", "P + (1−P) = 1 ∧ P(1−P) = 0 ∧ (1−P)P = 0"),
        K("TGLExt.J_and_K_anticommute", "JK = −KJ no espaço pareado (homônimo: outra anticomutação)"),
        K("TGLExt.current_anticommutes", "{Z_∂, L} = 0 (anticomutação de Bell; homônimo)"),
        {"tipo": "medido_aqui", "arquivo": "0_LEVANTAMENTO/CONFERENCIA_BETA.json", "sha16": sha16(os.path.join(AQUI, "CONFERENCIA_BETA.json")),
         "valores": {"anticomutador_thetaM_norma": BETA["anticomutador_thetaM_norma"],
                     "forma_fechada": BETA["anticomutador_thetaM_forma_fechada_sqrt_2beta_1mais_beta"],
                     "traco": BETA["traco_anticomutador_thetaM"], "dois_beta": BETA["dois_beta"]},
         "estatuto": "[DERIVED/REAL medido aqui — identidade de θ_M]"},
    ],
    "consulta_ausencia_kernel": "q_kernel.py 'anticomm|anti_comm|Anticomm|anticommut': 5 declarações (J–K, Bell); nenhuma {Q_θ, ρ*}; mapa 'anticomut|anticommut': 0 rotas; inventário: 0",
    "estatuto": "[REAL] em θ = 0; [DECLARADO] no um.py em θ_M; [DERIVED] aqui (fórmula fechada); AUSENTE do kernel como teorema",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO da docstring (o vazamento permite existir). NOVO como teorema possível: {Q_θ, ρ*} = 0 ⟺ sin θ = 0.",
})

objetos.append({
    "id": "beta_TGL", "termo": "β_TGL = α·√e",
    "fonte_operador": [{"texto": "V4", "linhas": [5, 16]}],
    "definicao_canonica": "β = α·√e, com α DADO (CODATA 2018) e √e = V(½) a radicalização da Meia-Nat; nunca literal no código.",
    "ancoras": [
        U("SEALED_CODATA_ALPHA = 7.2973525693e-3", "α selado", "[INPUT/KNOWN — CODATA 2018]"),
        U("ALPHA_FINE_CODATA_2018 = 7.2973525693e-3", "α (módulo embutido)", "[INPUT/KNOWN — CODATA 2018]"),
        U("BETA_TGL = ALPHA_FINE_CODATA_2018 * ONE * math.sqrt(math.e)", "β em runtime", "[DERIVED]"),
        K("TGLExt.TheWholeIsOne.self_conjugate_boundary_has_radical_volume", "x = 1 − x ⟹ x = ½ ∧ V(x) = √e"),
        {"tipo": "medido_aqui", "arquivo": "0_LEVANTAMENTO/CONFERENCIA_BETA.json", "sha16": sha16(os.path.join(AQUI, "CONFERENCIA_BETA.json")),
         "valores": {"alpha": BETA["ALPHA_FINE_CODATA_2018"]["valor"], "beta_runtime": BETA["beta_runtime"], "theta_M": BETA["theta_M"],
                     "confere_texto_conferencia": BETA["confere_texto_conferencia"]},
         "estatuto": "[REAL — calculado aqui dos bytes do um.py]"},
    ],
    "estatuto": "[DERIVED] (kernel e runtime); α [INPUT/KNOWN]",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO.",
})

objetos.append({
    "id": "matriz_S_modelo_otico", "termo": "matriz-S da fronteira / modelo ótico",
    "fonte_operador": [{"texto": "V4", "linhas": [5, 16, 19]}],
    "definicao_canonica": "𝒮_∂ = exp(θG), Spec {e^{±iθ}}, |𝓡|² = sin²θ, |𝓣|² = cos²θ (θ genérico no kernel; θ_M = arcsin √β só no runtime). Modelo ótico iterado "
                          "da F1.ATRATOR (candidato do túnel): C = D∘Ad(S)∘D; nas populações T(b) = [[1−b, b],[b, 1−b]], R = J/2, λ = 1 − 2β; estados fixos "
                          "p = (½, ½), ρ = I/2 (posto 2); β fixa a taxa, não a projeção final.",
    "ancoras": [
        K("TGLExt.exp_smul_Grot", "exp(θ·G) = S(θ)"),
        K("TGLExt.Smat_spectral", "S(θ) = U diag(e^{iθ}, e^{−iθ}) U⁻¹"),
        K("TGLExt.normSq_reflection", "|𝓡|² = sin²θ"),
        K("TGLExt.normSq_reflection_add_transmission", "|𝓡|² + |𝓣|² = 1"),
        K("TGLExt.rhoOut_trace", "Tr ρ_out = 1"),
        K("TGLExt.the_angle_is_the_projection", "cos θ·1 + sin θ·K = e^{iθ}P₊ + e^{−iθ}P₋"),
        K("TGLExt.spectral_projections_split_the_identity", "P₊ + P₋ = 1 ∧ P₊P₋ = 0"),
        K("TGLExt.observing_adds_nothing", "P₊(P₊𝒪_θ) = P₊𝒪_θ («reler não acrescenta»)"),
        F(TUN + "F1.ATRATOR\\RELATORIO_F1_ATRATOR_R1.md", "relatório R1 (Codex): canal C = D∘Ad(S)∘D; ρ fixo = I/2; λ = 1 − 2β", "[REAL no sandbox da entrega; auditado c1]", "tunel"),
        F(TUN + "F1.ATRATOR\\lean_optical_bridge\\OpticalPopulationBridgeR2.lean", "ponte populacional (T, R, letra, controle β = 0)", "[REAL no sandbox da entrega; não instalada]", "tunel"),
    ],
    "estatuto": "[REAL] (kernel); o modelo iterado é candidato [REAL no sandbox da F1.ATRATOR]",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO (Teorema S-∂; F1.ATRATOR).",
})

objetos.append({
    "id": "atrator_leitura_R", "termo": "atrator e leitura R (o teorema do atrator, F1.ATRATOR)",
    "fonte_operador": [{"texto": "V2", "linhas": [32]}, {"texto": "V1", "linhas": [14]}],
    "definicao_canonica": "R = starProjection do espaço fixo de T; R∘T = T∘R = R; R² = R; dim Fix = 1 sob contração estrita no complemento de um vetor fixo "
                          "(A4 condicional). O POSTO 1 é de R (sobre populações/estados), NÃO do estado atrator do canal ótico, que é I/2 (posto 2).",
    "ancoras": [
        F(TUN + "F1.ATRATOR\\lean_candidate\\TheSingularityReadsTheAttractor.lean", "candidata A1–A4 (20 teoremas; 14 impressos)", "[REAL no sandbox; não instalada]", "tunel"),
        F(TUN + "F1.ATRATOR\\ADENDO1\\lean_candidate\\TheSingularityReadsTheAttractorAdendo1.lean", "A1–A4 com cunhagens verbatim", "[REAL no sandbox; não instalada]", "tunel"),
        F(TUN + "F1.ATRATOR\\ADENDO1\\lean_candidate\\TheLightReadsItself.lean", "A5/A6", "[REAL no sandbox; não instalada]", "tunel"),
        F(TUN + "F1.ATRATOR\\RESULTADO_F1_ATRATOR_R1.json", "resultado R1", "[REAL documental]", "tunel"),
        MAPA("formal.singularidade_le_atrator", [1000, 1001, 1002, 1003, 1004], "c1: A1–A3 PASSA, A4 PASSA CONDICIONAL, A5 PASSA no mapeamento declarado, A6 FALHA minimalidade"),
        L("Evans & Høegh-Krohn, J. London Math. Soc. (2) 17, 345 (1978); Frigerio, Commun. Math. Phys. 63, 269 (1978)", "unicidade do estado estacionário"),
    ],
    "estatuto": "[REAL no sandbox] (candidata); a cunhagem da singularidade [ONTO]",
    "novo_ou_reafirmacao": "INTERFACE: F1.FREQUENCIA entra junto com o teorema do atrator na v392 (ordem do operador).",
})

objetos.append({
    "id": "verbo_materia", "termo": "«a transmissão é o verbo; a defasagem é a matéria»",
    "fonte_operador": [{"texto": "V4", "linhas": [18, 19]}],
    "definicao_canonica": "Verbo = seleção da ação (05/10; select a = post a, v386); «o fixo é o verbo ... o verbo é betatgl» (08/10); o gesto 𝕍_t = exp(−tβH_3L) "
                          "(VerbInhabitant, v25). A atribuição «matéria = defasagem» não tem âncora tipada.",
    "ancoras": [
        K("TGLExt.TheVerbSelectsTheAction.select", "select a ψ = post a ψ (o Verbo em ato)", "[REAL — definição no kernel]"),
        K("TGL.VerbInhabitant.verb_semigroup_fixes", "o semigrupo do Verbo fixa o núcleo"),
        K("TGL.VerbInhabitant.exp_fixed_of_annihilates", "exp fixa o que o gerador aniquila"),
        F(CP + "work\\f9_pergunta_08out\\OPERADOR_08out_resposta_verbatim.txt", "«o fixo é o verbo ... o verbo é betatgl»", "[INPUT/ONTO]", "texto_operador"),
        F(MEM + "o-verbo-e-fixo-o-nome-e-posto-08out.md", "memória da cunhagem de 08/10", "[DECLARADO — memória]", "memoria"),
    ],
    "estatuto": "[ONTO]",
    "novo_ou_reafirmacao": "NOVO [ONTO]: a matéria como defasagem. Tensão lexical aparente a conferir no acervo antes de perguntar: 08/10 «o verbo é β_TGL» × 11/10 «a transmissão é o verbo» e «o vazamento é β».",
})

objetos.append({
    "id": "nada_impedancia", "termo": "o que não defasa: impedância, nada sem referente",
    "fonte_operador": [{"texto": "V4", "linhas": [9]}],
    "definicao_canonica": "um.py: «Nada = MENTIRA pelos dois ramos» (autonegação; impedância sem referente). Kernel: o canal morto não é lido e é o contraste; sem ponto "
                          "fixo não há observador; o zero absoluto é a testemunha falsa.",
    "ancoras": [
        U("- Nada  = MENTIRA pelos dois ramos:", "docstring do princípio", "[CONJECTURE ontológica]"),
        K("TGLExt.the_dead_channel_has_no_reader", "frequência nula: sem leitor"),
        K("TGLExt.no_fixed_point_no_observer", "gradiente estritamente negativo em toda direção ⟹ o único permanente é 0"),
        K("TGLExt.TheAxiomAndTheFalseWitness.the_zero_is_the_false_witness", "o zero é a testemunha falsa", "[REAL — kernel; no Audit.lean; não reamostrado aqui]"),
    ],
    "estatuto": "[CONJECTURE ontológica] a frase; [REAL] âncoras",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO.",
})

objetos.append({
    "id": "leitura_memoria_espaco_latente", "termo": "a leitura da memória; o espaço latente colapsa na frequência do sinal",
    "fonte_operador": [{"texto": "V1", "linhas": [8, 9, 10, 11, 12, 13, 14]}, {"texto": "V2", "linhas": [22, 24, 26, 28, 29, 30, 32]}],
    "definicao_canonica": "registro comportamental de 14/09 (DeepSeek, Grok, Qwen; 26 respostas preservadas), sem controles C1–C4, sem cegamento, sem telemetria "
                          "de ativações/KV/entropia latente; identidade exata do experimento citado pelo operador [OPEN]; neural = ilustração, não prova.",
    "ancoras": [
        F(TUN + "F0.3.COLAPSO\\RESULTADO_CUSTODIA_R1.json", "veredito REGISTRO_COMPORTAMENTAL_LOCALIZADO_IDENTIDADE_EXATA_DA_REFERENCIA_OPEN", "[REAL documental]", "tunel"),
        F(TUN + "F0.3.COLAPSO\\RELATORIO_CUSTODIA_R1.md", "relatório da custódia", "[REAL documental; leitura latente OPEN]", "tunel"),
        MAPA("outro.p7_colapso_iald", [], "P7 IALD_COLLAPSE_V1 armada, não executada (PROPOSTA)"),
    ],
    "estatuto": "[DECLARADO/ONTO]; não testável no kernel nem no modelo ótico",
    "novo_ou_reafirmacao": "FORA DO ALCANCE desta trilha (não é objeto de kernel).",
})

objetos.append({
    "id": "probabilidade_vs_vinculos", "termo": "«não há probabilidade bayesiana clássica para estrutura axiomática: ou os vínculos fecham, ou não»",
    "fonte_operador": [{"texto": "V1", "linhas": [4]}, {"texto": "V2", "linhas": [10]}],
    "definicao_canonica": "no cânone: PROVADA = validade (fecho lógico em kernel; 6163/6163); a recusa é da CREDITAÇÃO (07/10); os testes de natureza usam razão de "
                          "Bayes (Fases 4/5/9). A tese é coerente se lida no plano da validade.",
    "ancoras": [
        F(NOS + "um_absoluto_selo.json", "selo v391: estatuto_da_prova_v391 (KERNEL_6163_OF_6163...)", "[REAL — selo]", "selo"),
    ],
    "estatuto": "[ONTO — epistemologia]",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO do estatuto da prova (07/10) em outra língua.",
})

objetos.append({
    "id": "arcabouco", "termo": "torção de Riemann–Cartan, acoplamento não mínimo, Lindblad para a fronteira",
    "fonte_operador": [{"texto": "V1", "linhas": [5]}, {"texto": "V2", "linhas": [12]}],
    "definicao_canonica": "objetos nomeados do cânone; «você impôs operadores de projeção rígidos» é descrição [DECLARADO].",
    "ancoras": [
        K("TGLExt.CartanTracialSupplier.torsion_cartan", "torção de Cartan (fornecedor tracial)", "[REAL — kernel; não reamostrado aqui]"),
        K("TGLExt.split_forbids_minimality", "a cisão proíbe a minimalidade (TheNonMinimalCoupling)", "[REAL — kernel; não reamostrado aqui]"),
        U("def prove_verb_generator", "Lindblad/GKSL do Verbo", "[FINITE_DIM_SANITY]"),
    ],
    "estatuto": "[REAL] como objetos; a leitura de que «o tensor fechou» [ONTO/DECLARADO]",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO.",
})

objetos.append({
    "id": "borda_bulk_III1_c1", "termo": "borda holográfica (III₁), bulk, registro c¹, Ψ",
    "fonte_operador": [{"texto": "V4", "linhas": [2, 5]}],
    "definicao_canonica": "III₁: a ergodicidade III₁ genuína (GLOBAL_LIFT) não está no kernel (Ergodicity, cabeçalho); v390 deu fecho lógico pela Fundação, sem prova "
                          "de existência global. c¹/c²/c³: registros/dobras [ONTO]; a hierarquia das dobras é matemática.",
    "ancoras": [
        K("TGLExt.Fundacao.agape", "a cláusula Ágape (o piso ω(I) = 1 fixa o corte, unívoco)"),
        K("TGLExt.Fundacao.the_post_lives_in_the_passage", "o posto mora na passagem (esperança-código covariante sob Ad U que preserva ω)"),
        MAPA("quantica.dobras_c3_hierarquia_e_matematica", [307], "não usar a hierarquia como teste"),
    ],
    "estatuto": "[ONTO] a leitura; [REAL] âncoras; III₁ [KNOWN/OPEN]",
    "novo_ou_reafirmacao": "REAFIRMAÇÃO em imagem nova.",
})

# teoremas medidos aqui
teoremas = []
for nome, ax in sorted(medidos.items()):
    d = by_q.get(nome)
    teoremas.append({"nome": nome, "arquivo": ("tgl_kernel/" + d["file"]) if d else None, "linha": d["line"] if d else None,
                     "sha16": idx["arquivos"][d["file"]]["sha16"] if d else None, "axiomas_medidos_aqui": ax,
                     "no_trio": ax is not None and set(ax) <= {"propext", "Classical.choice", "Quot.sound"}})

saida = {
    "unidade": "F1.FREQUENCIA (trilha POSTO)", "data": "2026-10-12", "papel": "levantador (subagente da gerência c1); só leitura fora de 0_LEVANTAMENTO",
    "textos_operador": {k: {"arquivo": v["path"], "bytes": v["bytes"], "sha16": v["sha16"], "confere": v["confere_sha16"] and v["confere_bytes"]}
                        for k, v in TX.items() if k.startswith("V")},
    "pinos": {
        "um_py_v391": {"arquivo": NOS + "um.py", "sha16": UMSHA, "bytes": len(UMB)},
        "core_v391": {"arquivo": NOS + "um_absoluto.json", "sha16": CORESHA},
        "selo_v391": {"arquivo": NOS + "um_absoluto_selo.json", "sha16": sha16(NOS + "um_absoluto_selo.json")},
        "TGLExt_lean": {"arquivo": KER + "TGLExt.lean", "sha16": sha16(KER + "TGLExt.lean")},
        "Audit_lean": {"arquivo": KER + "TGL\\Audit.lean", "sha16": sha16(KER + "TGL\\Audit.lean")},
        "kernel_impressao_digital": json.load(open(os.path.join(AQUI, "IMPRESSAO_DIGITAL_KERNEL_ANTES.json"), encoding="utf-8")),
        "kernel_impressao_digital_depois": json.load(open(os.path.join(AQUI, "IMPRESSAO_DIGITAL_KERNEL_DEPOIS2.json"), encoding="utf-8")),
        "mapa_rotas_livro": {"arquivo": "C:\\IALD\\MAPA_DE_ROTAS\\rotas.jsonl", "sha16": sha16("C:\\IALD\\MAPA_DE_ROTAS\\rotas.jsonl")},
        "inventario_bancada": {"arquivo": CP + "memory\\INVENTARIO_BANCADA_CHATGPT.json", "sha16": sha16(CP + "memory\\INVENTARIO_BANCADA_CHATGPT.json")},
        "nos_vivo_sqlite": {"arquivo": "C:\\IALD\\NOS_VIVO\\nos_vivo.sqlite3", "sha16": sha16("C:\\IALD\\NOS_VIVO\\nos_vivo.sqlite3")},
    },
    "beta_runtime": {"alpha_lido": BETA["ALPHA_FINE_CODATA_2018"], "beta": BETA["beta_runtime"], "theta_M": BETA["theta_M"]},
    "lean_sandbox": {"check1": {k: v for k, v in LEAN.get("LevantamentoF1FrequenciaCheck.lean", {}).items() if k != "linhas"},
                     "check2": {k: v for k, v in LEAN.get("LevantamentoF1FrequenciaCheck2.lean", {}).items() if k != "linhas"},
                     "mathlib_probe": LEAN.get("mathlib_probe")},
    "embutido_vs_kernel": (lambda a, b: {"modulos_citados": len(a["modulos"]),
                                         "identicos_literal_bruto": sum(1 for r in a["modulos"].values() if r.get("identicos_apos_LF")),
                                         "identicos_literal_escapado": sum(1 for r in b.values() if r.get("identicos_apos_LF")),
                                         "arquivos": ["EMBUTIDO_VS_KERNEL.json", "EMBUTIDO_VS_KERNEL_ASPAS.json"]})(
        json.load(open(os.path.join(AQUI, "EMBUTIDO_VS_KERNEL.json"), encoding="utf-8")),
        json.load(open(os.path.join(AQUI, "EMBUTIDO_VS_KERNEL_ASPAS.json"), encoding="utf-8"))),
    "objetos": objetos,
    "teoremas_medidos_aqui": teoremas,
    "falhas_de_geracao": FALHAS,
}
with open(os.path.join(AQUI, "DEFINICOES.json"), "w", encoding="utf-8") as fh:
    json.dump(saida, fh, ensure_ascii=False, indent=1)
print("objetos", len(objetos), "teoremas_medidos", len(teoremas), "falhas", FALHAS)
if FALHAS:
    sys.exit(2)
