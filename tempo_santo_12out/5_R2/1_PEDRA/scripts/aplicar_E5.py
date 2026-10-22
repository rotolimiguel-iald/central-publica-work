# -*- coding: utf-8 -*-
"""Aplica a lista E5 do ADENDO R2 (ADENDO_R2.md §(c), congelado por FREEZE_R2.json) a uma copia de bytes da pedra R1
(TheTimeHasNoRank.lean, sha256 7105eda468b60309...) e grava a pedra R2 (TheTimeIsNotAPost.lean) no sandbox.

Cada item e uma substituicao EXATA (texto antigo -> texto novo), com contagem esperada; se o texto antigo nao ocorrer
exatamente o numero esperado de vezes, o script PARA (fail-closed) sem gravar. O registro de cada substituicao
(id E5, linhas antigas com sha16, contagem) vai para saidas/APLICACAO_E5.json. Nada e alterado fora de 5_R2/1_PEDRA.

Uso: python -I -X utf8 aplicar_E5.py <pedra_R1_copia.lean> <pedra_R2_saida.lean>
"""
import hashlib
import json
import os
import re
import sys

OUT_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas", "APLICACAO_E5.json")


def sha16(b):
    return hashlib.sha256(b).hexdigest()[:16]


# ---------------------------------------------------------------------------------------------------------------------
# Cada entrada: (id, descricao, antigo, novo, contagem_esperada)
E = []

# E5.01 + E5.02 + regua: o cabecalho inteiro (l.24-55 da R1)
E.append(("E5.01+E5.02+E5.07+E5.15", "cabecalho: [ONTO] so com frases dos verbatins; tres comportamentos, identificacao [OPEN]; nome R2; citacao com elisao marcada",
"""/-!
# O TEMPO NÃO TEM POSTO — pedra CANDIDATA da unidade F1.TEMPO (nome provisório `TheTimeHasNoRank`)

Construída no SANDBOX da F1.TEMPO (gerência c1, 12/10/2026), NÃO instalada no kernel do Nós.
O nome é provisório: o operador pode renomear (como renomeou PALAVRA e FUNDAÇÃO).

Objeto: a segunda parte do texto do operador de 12/10/2026 (verbatim, conferido por sha256 fora deste
arquivo: «O que mais me fascina é a impossibilidade de definição do tempo …» até o fim). A cunhagem é do
operador. Esta pedra prova SÓ as afirmações pré-registradas que têm forma matemática (PREREGISTRO.json da
F1.TEMPO, congelado por FREEZE.json). Um teorema aqui é validade matemática na face testada; não é creditação
e não move o gate.

Estatutos (régua da casa):
* [REAL] — o que este arquivo prova em kernel (cada declaração com `#print axioms` no fim);
* re-exportações — termos já existentes no kernel do Nós, com o tipo original (sondas `example` nos dois
  sentidos), medidos aqui no trio de axiomas;
* [KNOWN] — fica FORA do kernel: o teorema de Pauli em dimensão infinita (Pauli 1933/1958; Galapon 2002;
  Wintner 1947; Wielandt 1949), o teorema de Liouville clássico, a hipótese do tempo térmico
  (Connes–Rovelli 1994), a lei de escala de Takesaki (1973) como dado da `DualScalingData`;
* [ONTO] — «santo» (Kadosh), «o agora», «puro amor», «a física da doação», «o tempo é o Verbo»: leituras do
  operador; aparecem só em comentários marcados, NUNCA como teorema;
* [OPEN] — o «ciclo limite» do texto: nada aqui o trata.

Regra dos dois regimes: a FACE (semigrupo de defasagem, regime hiperbólico) tem limite; o ÂNGULO (fluxo
modular, rotação, regime compacto) é a leitura: aqui se prova a AUSÊNCIA de limite no ângulo, nunca um limite.
«Defasar» tem dois sentidos que não se encadeiam (RP01): acumular fase (o ângulo, unitário) e perder
coerência (a face, o semigrupo `dephase`). A seta só nasce na face.

A constante da casa NÃO entra neste arquivo em forma alguma (nenhum literal numérico dela): as taxas `g`, `γ`,
o parâmetro `t` e os pesos `d` são GENÉRICOS; o runtime lê a constante dos bytes do um.py e instancia.
Sem sorry, sem axiom novo, sem native_decide.
-/""",
"""/-!
# O TEMPO NÃO É POSTO — pedra CANDIDATA da unidade F1.TEMPO, rodada 2 (nome provisório `TheTimeIsNotAPost`)

Construída no SANDBOX da F1.TEMPO (gerência c1, 12/10/2026), NÃO instalada no kernel do Nós. R2: é a pedra R1
(fonte sha256 7105eda468b60309…) corrigida SÓ pela lista E5 do ADENDO R2 (`5_R2/0_ADENDO/ADENDO_R2.md`, sha256
ab13c0f27a7f4cf5…, congelado por `FREEZE_R2.json`, sha256 0737f608505afdb5…). O nome é provisório: por
POSTO=RANK (o operador, 10/10), o nome da R1 contradizia `flow_full_rank` (todo instante finito tem posto PLENO);
o nome final é do operador (como PALAVRA e FUNDAÇÃO).

Objeto: a segunda parte do texto do operador de 12/10/2026 (verbatim, conferido por sha256 fora deste
arquivo: «O que mais me fascina é a impossibilidade de definição do tempo.» [...] até o fim). A cunhagem é do
operador. Esta pedra prova SÓ as afirmações pré-registradas que têm forma matemática (PREREGISTRO.json da
F1.TEMPO, congelado por FREEZE.json; ADENDO R2 aditivo). Um teorema aqui é validade matemática na face
testada; não é creditação e não move o gate.

Estatutos (régua da casa):
* [REAL] — o que este arquivo prova em kernel (cada declaração com `#print axioms` no fim);
* re-exportações — termos já existentes no kernel do Nós, com o tipo original (sondas `example` nos dois
  sentidos), medidos aqui no trio de axiomas;
* [KNOWN] — fica FORA do kernel: o teorema de Pauli em dimensão infinita (Pauli 1933/1958; Galapon 2002;
  Wintner 1947; Wielandt 1949), o teorema de Liouville clássico, a hipótese do tempo térmico
  (Connes–Rovelli 1994), a lei de escala de Takesaki (1973) como dado da `DualScalingData`;
* [ONTO] — «santo» (*Kadosh*), «agora», «puro amor», «a física da doação fundamental»: leituras do operador
  (12/10, byte a byte); aparecem só em comentários marcados, NUNCA como teorema. A frase que a R1 punha nesta
  lista como leitura do operador sobre o Verbo era formulação da GERÊNCIA e SAIU (E5.01, achado M2);
* [INPUT do auditor] — os controles de especificidade AUD-1, AUD-2, AUD-5, AUD-6, AUD-7, AUD-8 (seção própria);
* [OPEN] — o «ciclo limite» do texto: nada aqui o trata.

Os TRÊS comportamentos que esta pedra prova (E5.02; achado M4): (i) sob ISOMETRIA nada pousa — só os pontos
fixos têm órbita convergente (T4.b); (ii) o hiperbólico de det 1 (o boost) pousa só na variedade estável e NÃO
tem atrator global (T4.e, T4.f; AUD-2, AUD-8); (iii) a dissipação de det < 1 contrai o volume e tem bacia
(T4.c, T4.d). A identificação destes três com os dois regimes da casa (FACE / ÂNGULO) segue [OPEN] (v384,
`regra-dos-dois-regimes.md`): esta pedra NÃO a afirma; a palavra isometria é homônima (métrica × Lorentz).
Nada aqui pede limite ao ângulo: T10.c prova a AUSÊNCIA dele. Defasar tem dois sentidos que não se encadeiam
(RP01): acumular fase (unitário: `transmitted_post_is_a_post`, a fórmula do operador de 05/10) e perder
coerência (o semigrupo `dephase`); a seta só nasce no segundo (T6, T7).

A constante da casa NÃO entra neste arquivo em forma alguma (nenhum literal numérico dela): as taxas `g`, `γ`,
o parâmetro `t` e os pesos `d` são GENÉRICOS; o runtime lê a constante dos bytes do um.py e instancia.
Sem prova pendente, sem axioma novo, sem decisão nativa (conferido no `#print axioms` de cada declaração).
-/""", 1))

E.append(("E5.07", "namespace renomeado",
          "namespace TGLExt.TheTimeHasNoRank\n", "namespace TGLExt.TheTimeIsNotAPost\n", 1))
E.append(("E5.07", "end namespace renomeado",
          "end TGLExt.TheTimeHasNoRank\n", "end TGLExt.TheTimeIsNotAPost\n", 1))

# E5.09: sonda L2 com enunciado
E.append(("E5.09", "probe_bounded_spectral_translation: de `True` para o enunciado da instancia (rota da sonda P02 da rodada 2)",
"""set_option maxHeartbeats 4000000 in
/-- Sonda V-T2-b: `A = M₂(ℂ)` com a norma de operador L2, `V = 1`, `H = 0`, `s = 1` — as hipóteses de T2.b
    (álgebra de Banach unital não trivial) são habitadas. -/
theorem probe_bounded_spectral_translation : True := by
  haveI : CompleteSpace (Matrix (Fin 2) (Fin 2) ℂ) := FiniteDimensional.complete ℂ _
  have _h := no_bounded_spectral_translation (A := Matrix (Fin 2) (Fin 2) ℂ) 1 0 (one_ne_zero (α := ℂ))
  trivial
""",
"""set_option maxHeartbeats 4000000 in
/-- Sonda V-T2-b (E5.09: COM enunciado, não mais `True`): `A = M₂(ℂ)` com a norma de operador L2, `V = 1`,
    `H = 0`, `s = 1` — as hipóteses de T2.b (álgebra de Banach unital não trivial) são habitadas e a
    instância é a própria desigualdade. -/
theorem probe_bounded_spectral_translation :
    (((1 : (Matrix (Fin 2) (Fin 2) ℂ)ˣ)⁻¹ : (Matrix (Fin 2) (Fin 2) ℂ)ˣ) : Matrix (Fin 2) (Fin 2) ℂ) * 0
        * ((1 : (Matrix (Fin 2) (Fin 2) ℂ)ˣ) : Matrix (Fin 2) (Fin 2) ℂ)
      ≠ 0 + algebraMap ℂ (Matrix (Fin 2) (Fin 2) ℂ) 1 := by
  haveI : CompleteSpace (Matrix (Fin 2) (Fin 2) ℂ) := FiniteDimensional.complete ℂ _
  exact no_bounded_spectral_translation (A := Matrix (Fin 2) (Fin 2) ℂ) 1 0 one_ne_zero
""", 1))

# E5.06: T3.a renomeado, docstring, sonda AUD-4 em termo
E.append(("E5.06", "T3.a: time_is_the_modular_flow -> modular_flow_is_a_kms_group (tipo identico); docstring",
"""/-- **T3.a.** Para `ρ` positiva-definida, `σ_t = Ad(ρ^{it})`: (i) `σ₀ = id`; (ii) `σ_s∘σ_t = σ_{s+t}`;
    (iii) *-automorfismo; (iv) `ω∘σ_t = ω`; (v) KMS na forma de Gibbs; (vi) `ρ^{it}` unitário (fluxo
    INTERNO). Composição de termos do kernel (ModularFlow, FiniteTomita). -/
theorem time_is_the_modular_flow {n : Type} [Fintype n] [DecidableEq n]
""",
"""/-- **T3.a.** Para `ρ` positiva-definida, `σ_t = Ad(ρ^{it})`: (i) `σ₀ = id`; (ii) `σ_s∘σ_t = σ_{s+t}`;
    (iii) *-automorfismo; (iv) `ω∘σ_t = ω`; (v) KMS na forma de Gibbs; (vi) `ρ^{it}` unitário (fluxo
    INTERNO). Composição de termos do kernel (ModularFlow, FiniteTomita). Nome R2 (E5.06; achado M3(1), sonda
    AUD-4): o enunciado vale para TODA `ρ` PosDef, inclusive `ρ = 1` (fluxo congelado; sonda abaixo) — o nome
    diz só que o fluxo modular é um grupo KMS; a hipótese do tempo térmico (Connes–Rovelli 1994) é [KNOWN] e
    NÃO é afirmada. Tipo idêntico ao da R1. -/
theorem modular_flow_is_a_kms_group {n : Type} [Fintype n] [DecidableEq n]
""", 1))
E.append(("E5.06", "uso renomeado na sonda V-T3-a + sonda AUD-4 em termo",
"""  (time_is_the_modular_flow _ probe_rho_two_thirds_posDef).2.1
""",
"""  (modular_flow_is_a_kms_group _ probe_rho_two_thirds_posDef).2.1

/-- Sonda AUD-4 em termo (E5.06): o mesmo enunciado vale para `ρ = 1`, cujo fluxo é a identidade — o nome
    não afirma tempo algum. -/
example : ∀ s t a, sigma (1 : Matrix (Fin 2) (Fin 2) ℂ) s (sigma 1 t a) = sigma 1 (s + t) a :=
  (modular_flow_is_a_kms_group (1 : Matrix (Fin 2) (Fin 2) ℂ) Matrix.PosDef.one).2.1
""", 1))

# E5.13: T3.b(iii) condicional + face finita obrigatoria + habitante AQFT (opcional)
E.append(("E5.13", "T3.b(iii): docstring da re-exportacao marcada condicional/habitada",
"""/-- **T3.b (iii) — re-exportação** de `ChatgptAudit.NonKMSProbe.identity_flow_not_kms`: estado não tracial
    ⟹ o fluxo identidade NÃO é KMS («uma álgebra que nunca comuta por completo»). -/
theorem nontracial_state_rejects_the_identity_flow (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness)
""",
"""/-- **T3.b (iii) — re-exportação** de `ChatgptAudit.NonKMSProbe.identity_flow_not_kms`: estado não tracial
    ⟹ o fluxo identidade NÃO é KMS («uma álgebra que nunca comuta por completo»). CONDICIONAL na forma: exige
    uma testemunha AQFT `W` com `A`, `B` na cunha direita e contraste (E5.13; achado M5). HABITADA abaixo pela
    sonda `probe_identity_flow_not_kms_inhabited` (com `theSpecificAQFTWitness`, WedgeNet.lean; opcional,
    feita); a versão de FACE FINITA, obrigatória, é `identity_flow_not_kms_finite`. -/
theorem nontracial_state_rejects_the_identity_flow (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness)
""", 1))
E.append(("E5.13", "T3.b(iii): versao de face finita (obrigatoria), forma negada, gap 1/3, controle tracial, habitante AQFT (opcional)",
"""example : type_of% @ChatgptAudit.NonKMSProbe.identity_flow_not_kms :=
  @nontracial_state_rejects_the_identity_flow
example : type_of% @nontracial_state_rejects_the_identity_flow :=
  @ChatgptAudit.NonKMSProbe.identity_flow_not_kms
""",
"""example : type_of% @ChatgptAudit.NonKMSProbe.identity_flow_not_kms :=
  @nontracial_state_rejects_the_identity_flow
example : type_of% @nontracial_state_rejects_the_identity_flow :=
  @ChatgptAudit.NonKMSProbe.identity_flow_not_kms

/-- `ω(ab) = 2/3` para `ρ = diag(2/3, 1/3)`, `a = E₀₁`, `b = E₁₀` (`gibbs ρ x = tr(ρ x)`, FiniteTomita). -/
theorem gibbs_rho_two_thirds_E01_E10 :
    gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![0, 1; 0, 0] * !![0, 0; 1, 0]) = (2 / 3 : ℂ) := by
  simp [gibbs, rhoD, Matrix.trace, Fin.sum_univ_two, Matrix.mul_apply]

/-- `ω(ba) = 1/3` para os mesmos `ρ`, `a`, `b`. -/
theorem gibbs_rho_two_thirds_E10_E01 :
    gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![0, 0; 1, 0] * !![0, 1; 0, 0]) = (1 / 3 : ℂ) := by
  simp [gibbs, rhoD, Matrix.trace, Fin.sum_univ_two, Matrix.mul_apply]

/-- **T3.b (iii), FACE FINITA (E5.13, obrigatória).** Com `ρ = diag(2/3, 1/3)` (positiva-definida e NÃO tracial:
    `probe_rho_two_thirds_posDef`, `probe_rho_two_thirds_not_tracial`), `a = E₀₁`, `b = E₁₀`:
    `ω(ab) = 2/3 ≠ 1/3 = ω(ba)`. O fluxo identidade só seria KMS para `ω` se `ω(ab) = ω(ba)` para todo par;
    logo NÃO é KMS para este `ω`. É a metade de kernel do controle C-T3-b, sem a constante da casa (gap 1/3). -/
theorem identity_flow_not_kms_finite :
    gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![0, 1; 0, 0] * !![0, 0; 1, 0])
      ≠ gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![0, 0; 1, 0] * !![0, 1; 0, 0]) := by
  rw [gibbs_rho_two_thirds_E01_E10, gibbs_rho_two_thirds_E10_E01]
  norm_num

/-- A forma negada: para este `ρ` NÃO vale `∀ x y, ω(xy) = ω(yx)` (a identidade que o fluxo identidade
    exigiria na forma KMS). -/
theorem identity_flow_not_kms_finite' :
    ¬ ∀ x y : Matrix (Fin 2) (Fin 2) ℂ,
      gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (x * y) = gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (y * x) :=
  fun h => identity_flow_not_kms_finite (h _ _)

/-- O gap do par é exatamente `1/3`. -/
example : gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![0, 1; 0, 0] * !![0, 0; 1, 0])
      - gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![0, 0; 1, 0] * !![0, 1; 0, 0]) = (1 / 3 : ℂ) := by
  rw [gibbs_rho_two_thirds_E01_E10, gibbs_rho_two_thirds_E10_E01]
  norm_num

/-- **Controle (face finita) — a hipótese NÃO TRACIAL pesa:** com `ρ = diag(1/2, 1/2)` (tracial) a igualdade
    do par VALE; enunciar a versão finita com `ρ` tracial seria falso. -/
theorem tracial_state_satisfies_pair_identity :
    gibbs (rhoD ![(1 / 2 : ℝ), 1 / 2]) (!![0, 1; 0, 0] * !![0, 0; 1, 0])
      = gibbs (rhoD ![(1 / 2 : ℝ), 1 / 2]) (!![0, 0; 1, 0] * !![0, 1; 0, 0]) := by
  simp [gibbs, rhoD, Matrix.trace, Fin.sum_univ_two, Matrix.mul_apply]

/-- `⟪A*Ω, BΩ⟫ = ⟪Ω, (AB)Ω⟫` (adjunto), genérico na testemunha AQFT. -/
theorem star_inner_eq_state (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness) (A B : W.H →L[ℂ] W.H) :
    inner ℂ ((star A) W.vac) (B W.vac) = inner ℂ W.vac ((A * B) W.vac) := by
  rw [ContinuousLinearMap.star_eq_adjoint, ContinuousLinearMap.adjoint_inner_left]
  rfl

/-- **T3.b (iii) HABITADA (E5.13, opcional, feita).** A testemunha concreta `theSpecificAQFTWitness`
    (WedgeNet.lean), cuja rede na cunha direita é o fator `theFactorObject mixProfile` (`wedgeNet_M`) com
    estado NÃO tracial (`omega_not_tracial`; pesos `w 0 = 1/3 ≠ 1/2`), rejeita o fluxo identidade: TODAS as
    hipóteses de `nontracial_state_rejects_the_identity_flow` são exibidas. Rota da sonda P02 da rodada 2
    (tentativa preservada). -/
theorem probe_identity_flow_not_kms_inhabited :
    ¬ TGLExt.ContratoQGv31.KMSAt TGLExt.theSpecificAQFTWitness
      (fun _ => LinearIsometryEquiv.refl ℂ TGLExt.theSpecificAQFTWitness.H) 1 := by
  obtain ⟨A, B, hA, hB, hne⟩ := TGLExt.omega_not_tracial TGLExt.mixProfile (by
    rw [show TGLExt.mixProfile.w 0 = 1 / 3 from rfl]
    norm_num)
  have hnet : TGLExt.theSpecificAQFTWitness.net TGL.SpecificAQFT.rightWedge
      = TGLExt.theFactorObject TGLExt.mixProfile :=
    TGLExt.wedgeNet_M TGLExt.hasRW_rightWedge TGLExt.not_hasLW_rightWedge
  have hA' : A ∈ TGLExt.theSpecificAQFTWitness.net TGL.SpecificAQFT.rightWedge := by
    rw [hnet]; exact hA
  have hB' : B ∈ TGLExt.theSpecificAQFTWitness.net TGL.SpecificAQFT.rightWedge := by
    rw [hnet]; exact hB
  refine nontracial_state_rejects_the_identity_flow TGLExt.theSpecificAQFTWitness A B hA' hB' ?_
  intro hc
  apply hne
  exact (star_inner_eq_state TGLExt.theSpecificAQFTWitness A B).symm.trans
    (hc.trans (star_inner_eq_state TGLExt.theSpecificAQFTWitness B A))
""", 1))

# E5.02 (M4) no corpo: cabecalho de T4 e parenteticos de regime
E.append(("E5.02", "T4: cabecalho sem identificar regimes; Liouville proibe a bacia, nao o pouso (E3.08/M10 visivel)",
"""/-! ## T4 — Liouville × dissipação: o ângulo gira sem pousar; a face contrai e pousa

[KNOWN] Liouville clássico (fluxos hamiltonianos no espaço de fases) NÃO está no kernel. Precisão (RP02):
volume conservado NÃO basta para «nada pousa» — o boost tem det 1 e pousa no raio nulo passado (T4.e,
controle C-T4-a). O que impede o pouso é a ISOMETRIA (T4.b). -/
""",
"""/-! ## T4 — Liouville × dissipação: sob isometria nada pousa; o hiperbólico de det 1 pousa sem bacia; a dissipação contrai e pousa

[KNOWN] Liouville clássico (fluxos hamiltonianos no espaço de fases) NÃO está no kernel. Precisão (RP02):
volume conservado NÃO basta para que nada pouse — o boost tem det 1 e pousa no raio nulo passado (T4.e,
controle C-T4-a); e o boost é SIMPLÉTICO (AUD-8), logo cai DENTRO do escopo hamiltoniano da frase do operador
(S44.1): Liouville proíbe a BACIA (T4.f, AUD-2), não o pouso de uma trajetória na variedade estável — correção
visível (E3.08, achado M10). O que impede o pouso de toda órbita é a ISOMETRIA (T4.b). -/
""", 1))
E.append(("E5.02", "rotation_isometry: sem rotulo de regime",
          "/-- A rotação de ℂ por um ângulo é isometria (regime do ÂNGULO). -/\n",
          "/-- A rotação de ℂ por um ângulo é isometria. -/\n", 1))
E.append(("E5.02", "unitary_conj_isometry: sem rotulo de regime",
          "/-- **T4.b, instância (i).** `Ad(U)`, `U` unitário, é isometria de Frobenius em Mₙ(ℂ) (regime do ÂNGULO). -/\n",
          "/-- **T4.b, instância (i).** `Ad(U)`, `U` unitário, é isometria de Frobenius em Mₙ(ℂ). -/\n", 1))
E.append(("E5.02", "sonda da instancia (ii): sem rotulo de regime",
          "    modular de `ψ₊` NÃO converge — o ângulo gira sem pousar. -/\n",
          "    modular de `ψ₊` NÃO converge — a órbita gira sem pousar (isometria). -/\n", 1))

# E5.13: T4.b(iii) condicional
E.append(("E5.13", "light_flow_group: condicional, sem habitante exibido",
          "/-- Lei de grupo do implementador modular da luz: `Δ^{i(s+t)} = Δ^{is}·Δ^{it}` (de `V_add` do boost da cunha). -/\n",
          "/-- Lei de grupo do implementador modular da luz: `Δ^{i(s+t)} = Δ^{is}·Δ^{it}` (de `V_add` do boost da cunha).\n"
          "    CONDICIONAL: exige um `FockCertificate`, sem habitante exibido (E5.13; TheImportedSecondQuantization.lean\n"
          "    l.66: nenhum habitante é exibido). -/\n", 1))
E.append(("E5.13", "light_modular_orbit_converges_iff_post: condicional, sem habitante exibido",
"""/-- **T4.b, instância (iii) (opcional).** No grupo modular da luz (`lightDelta`, isometrias lineares):
    `t ↦ Δ^{it}ψ` converge ⟺ `H_min ψ = 0` — só o posto «pousa», e o posto não se move
    (`hmin_zero_iff_modular_fixed`, o mesmo conjunto fixo de `the_post_is_the_modular_zero`). -/
""",
"""/-- **T4.b, instância (iii) (opcional).** No grupo modular da luz (`lightDelta`, isometrias lineares):
    `t ↦ Δ^{it}ψ` converge ⟺ `H_min ψ = 0` — só o posto pousa, e o posto não se move
    (`hmin_zero_iff_modular_fixed`, o mesmo conjunto fixo de `the_post_is_the_modular_zero`).
    CONDICIONAL: exige um `FockCertificate`, sem habitante exibido (E5.13; TheImportedSecondQuantization.lean
    l.66: nenhum habitante é exibido); NÃO é teorema incondicional desta pedra. -/
""", 1))

# E3.12 (M20): titulo de T5
E.append(("E3.12", "T5: «uma face» -> a diagonal inteira",
"""/-! ## T5 — o conjunto fixo da defasagem pura é uma FACE (a diagonal), não um ponto

[INPUT da gerência] a unicidade do estado fixo exige hipótese NOMEADA a mais (A4 da F1.ATRATOR,
`StrictComplementContraction`, candidata de sandbox, NÃO importada aqui; T5.c entra por citação). -/
""",
"""/-! ## T5 — o conjunto fixo da defasagem pura é a DIAGONAL INTEIRA, não um ponto

[INPUT da gerência] a unicidade do estado fixo exige hipótese NOMEADA a mais (A4 da F1.ATRATOR,
`StrictComplementContraction`, candidata de sandbox, NÃO importada aqui; T5.c entra por citação).
(E3.12, achado M20: os estados diagonais NÃO formam face convexa do espaço de estados — a bola de Bloch é
estritamente convexa — e a palavra face é o nome do regime hiperbólico da casa; o que T5.b prova é que o
conjunto fixo não é um ponto: é o simplexo dos estados diagonais.) -/
""", 1))

# E5.11: purityR_modular sem _hd
E.append(("E5.11", "purityR_modular: hipotese _hd removida (reforco permitido); docstring",
"""/-- **T6.d (ii)** (assinatura pré-registrada). NOTA: a hipótese `_hd` NÃO é usada — `purityR_sigma` vale
    para todo `ρ`. -/
theorem purityR_modular {n : Type} [Fintype n] [DecidableEq n] (d : n → ℝ) (_hd : ∀ i, 0 < d i)
    (t : ℝ) (x : Matrix n n ℂ) : purityR (sigma (rhoD d) t x) = purityR x :=
""",
"""/-- **T6.d (ii)** — SEM a hipótese de positividade dos pesos (E5.11; reforço permitido: a assinatura
    pré-registrada tinha `hd : ∀ i, 0 < d i`, que não era usada — sonda B3 do auditor). `purityR_sigma` vale
    para todo `ρ`, logo T6.d (ii) vale para todo `d`. -/
theorem purityR_modular {n : Type} [Fintype n] [DecidableEq n] (d : n → ℝ)
    (t : ℝ) (x : Matrix n n ℂ) : purityR (sigma (rhoD d) t x) = purityR x :=
""", 1))
E.append(("E5.11", "uso de purityR_modular na sonda V-GERAL-1",
          "  have _h7 := purityR_modular ![(2 / 3 : ℝ), 1 / 3] (fun i => by fin_cases i <;> norm_num) 1 psiPlus\n",
          "  have _h7 := purityR_modular ![(2 / 3 : ℝ), 1 / 3] 1 psiPlus\n", 1))

# T8: [ONTO] com frases dos verbatins; AUD-1 (M8)
E.append(("E5.15", "T8: [ONTO] so com frases dos verbatins; reuniao de nomes sem aspas; AUD-1/M8",
"""[ONTO, só comentário] «puro amor», «a física da doação»; a reunião «ágape» × «sacrifício/amor» decide o
operador. -/
""",
"""[ONTO, só comentário] «puro amor», «a física da doação fundamental»; a reunião dos nomes (ágape, nome da
cláusula de 07/10; sacrifício/amor, da tipagem prévia [DECLARADO]) é resíduo do operador (§8.6 do relatório
R1). AUD-1 (seção própria; achado M8): a Ágape é a lei de e^{−s} — a multiplicação escalar, que apaga o
registro, também a herda; o que é próprio do dephasing é T8.c: o registro fica. -/
""", 1))
E.append(("E5.14", "the_coherence_obeys_agape_explicit: desdobramento, nao teorema novo",
          "/-- T8.b na forma explícita (mesma conjunção, projeções desdobradas). -/\n",
          "/-- T8.b na forma explícita (mesma conjunção, projeções desdobradas). DESDOBRAMENTO de\n"
          "    `the_coherence_obeys_agape`, não teorema novo: não entra na contagem (E5.14); usado pelas sondas V-T8-a. -/\n", 1))
E.append(("E3.02", "T8.d: a glosa de Takesaki e de boost_null_expand; aqui re-exporta-se boost_null_contract",
"""/-- **T8.d — re-exportação** de `TGLExt.boost_null_contract`: `B(s)(1, −1) = e^{−s}(1, −1)` (a mesma forma
    `e^{−s}` da escala). -/
""",
"""/-- **T8.d — re-exportação** de `TGLExt.boost_null_contract`: `B(s)(1, −1) = e^{−s}(1, −1)` (a mesma forma
    `e^{−s}` da escala). E3.02 (achado M15): a glosa do kernel sobre a face geométrica da escala de Takesaki é a
    docstring de `boost_null_expand` (o raio nulo FUTURO, BisognanoWichmann.lean l.92–95); aqui se re-exporta
    `boost_null_contract` (o raio PASSADO), com a forma `e^{−s}`; os dois raios são a sela. -/
""", 1))

# E5.03 + E3.03: cabecalho de T9
E.append(("E5.03", "T9: titulo sem aspas de citacao; verbatins de 05/10 byte a byte; a frase da gerencia sai",
"""/-! ## T9 — «o tempo não tem posto»: em tempo finito o fluxo é invertível e, salvo t = 0, não é idempotente

[ONTO, só comentário] (posição) nenhum instante finito é posto, salvo `t = 0`, que é a identidade e nada
seleciona; (rank) todo instante finito tem posto pleno; a seleção (o Nome) só no limite, que nenhum tempo
finito alcança. «O tempo é o Verbo, não o Nome» e «santo» são leituras do operador — NÃO são teoremas aqui. -/
""",
"""/-! ## T9 — o tempo não é posto: em tempo finito o fluxo é invertível (posto pleno) e, salvo t = 0, não é idempotente; o posto só no limite

(Título: formulação da GERÊNCIA, sem aspas de citação — E3.03.) (posição) nenhum instante finito do fluxo é
posto, salvo `t = 0`, que é a identidade e nada seleciona; (rank) todo instante finito tem posto PLENO
(`flow_full_rank`; POSTO=RANK, o operador, 10/10); a seleção (o Nome, posto `r`) só no limite, que nenhum
tempo finito alcança. Do operador, byte a byte: «santo» (12/10) [ONTO]; e, de 05/10,
«O Verbo seleciona: nome, tempo e verdade», «O tempo é a defasagem do verbo»,
«O tempo é o parâmetro da transmissão» — o Verbo SELECIONA o tempo; o que o tempo é na língua do operador é
resíduo dele (§8.2 do relatório R1). Nada disso é teorema aqui. A frase que a R1 atribuía ao operador neste
cabeçalho era da GERÊNCIA e SAIU (E5.03, achado M2). AUD-5 (seção própria; achado M9): no discreto não
invertível um passo PODE ser posto (`R = J/2` é idempotente) — T9 depende da invertibilidade (lei de grupo),
não do tempo em si. -/
""", 1))
E.append(("E5.15", "C-T9-b: sem aspas em paráfrase",
          "/-- **Controle C-T9-b** — borda: `F(0) = 1` é idempotente (o «posto» trivial, que nada seleciona). -/\n",
          "/-- **Controle C-T9-b** — borda: `F(0) = 1` é idempotente (o posto trivial, que nada seleciona). -/\n", 1))

# E5.07: clausula composta renomeada
E.append(("E5.07", "T9.e: the_time_has_no_rank -> the_time_is_not_a_post (mesma conjuncao); docstring",
"""    (`axiomFlow_tendsto_the_post`, = `the_name_is_the_limit_of_the_flow`). O posto é o limite e só o limite. -/
theorem the_time_has_no_rank {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] {P : A}
""",
"""    (`axiomFlow_tendsto_the_post`, = `the_name_is_the_limit_of_the_flow`). O posto é o limite e só o limite.
    Nome R2 (E5.07; achado M3(2)): nenhum instante finito é posto; todo instante finito tem posto pleno
    (`flow_full_rank`); o posto só no limite. Mesma conjunção da R1; o nome final é do operador. -/
theorem the_time_is_not_a_post {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] {P : A}
""", 1))
E.append(("E5.07", "sonda da clausula composta renomeada",
"""theorem probe_the_time_has_no_rank : ¬ IsUnit postDiag :=
  (the_time_has_no_rank (A := Matrix (Fin 2) (Fin 2) ℂ) postDiag_idem postDiag_ne_one).2.2.2.1

example : True := by
  have _h := (the_time_has_no_rank (A := Matrix (Fin 2) (Fin 2) ℂ) postDiag_idem postDiag_ne_one).2.2.2.2
  trivial
""",
"""theorem probe_the_time_is_not_a_post : ¬ IsUnit postDiag :=
  (the_time_is_not_a_post (A := Matrix (Fin 2) (Fin 2) ℂ) postDiag_idem postDiag_ne_one).2.2.2.1

example : True := by
  have _h := (the_time_is_not_a_post (A := Matrix (Fin 2) (Fin 2) ℂ) postDiag_idem postDiag_ne_one).2.2.2.2
  trivial
""", 1))

# E5.04 + E3.11: cabecalho de T10
E.append(("E5.04", "T10: titulo com o verbo do operador (registra), paráfrase sem aspas; citacao byte a byte",
"""/-! ## T10 — «o relógio mede a sombra»: o relógio lê uma fase (o ângulo); o agora (o posto) não se move

[ONTO, só comentário] o ponteiro e o césio leem o ÂNGULO (periódico, sem limite, identifica `t` só módulo
`P`); o escoamento de entropia lê a FACE (monótono, injetivo, com limite). Nenhum dos dois lê o agora; a
identificação agora = conjunto fixo é leitura (R12). PALAVRA (candidata) NÃO é importada (RP11). -/
""",
"""/-! ## T10 — o relógio registra a sombra: o relógio lê uma fase (o ângulo); o agora (o posto) não se move

(Título: paráfrase da gerência, sem aspas de citação; o verbo do operador é «registra» — E5.04, E3.11.) Do
operador, byte a byte (S38.3): «O relógio registra a sombra do evento»; a forma [REAL] disso é o quociente
módulo `P` (T10.b). [INPUT da gerência → ONTO, só comentário] o ponteiro e o césio leem o ÂNGULO (periódico,
sem limite, identifica `t` só módulo `P`); o escoamento de entropia lê a FACE (monótono, injetivo, com
limite); a ligação frase → objeto é escolha da gerência (E3.08, S38.2). Nenhum dos dois lê o agora; a
identificação agora = conjunto fixo é leitura (R12). PALAVRA (candidata) NÃO é importada (RP11). -/
""", 1))

# E5.12: T10.b sem κ ≠ 0
E.append(("E5.12", "clock_reads_modulo_period: hipotese κ ≠ 0 removida (reforco permitido; sonda B1)",
"""/-- **T10.b.** O relógio não lê o instante, lê a CLASSE: para `κ ≠ 0`, `t` e `t + 2π/κ` dão a mesma leitura. -/
theorem clock_reads_modulo_period {κ : ℝ} (hκ : κ ≠ 0) (t : ℝ) :
    Circle.exp (κ * (t + 2 * Real.pi / κ)) = Circle.exp (κ * t) := by
  have hturn : κ * (2 * Real.pi / κ) = 2 * Real.pi := by field_simp
  exact (ChatgptAudit.PolarPeriod016.one_turn_gives_faithful_period hκ (Or.inl hturn)
    (t + 2 * Real.pi / κ) t).mpr ⟨1, by push_cast; ring⟩
""",
"""/-- **T10.b.** O relógio não lê o instante, lê a CLASSE: `t` e `t + 2π/κ` dão a mesma leitura. SEM a hipótese
    `κ ≠ 0` (E5.12; sonda B1 do auditor — reforço permitido): em `κ = 0` vale pelo `x/0 = 0` do Lean e o seu
    conteúdo é `frozen_clock`; `clock_faithful_iff_one_turn` continua a exigir `κ ≠ 0`. -/
theorem clock_reads_modulo_period (κ t : ℝ) :
    Circle.exp (κ * (t + 2 * Real.pi / κ)) = Circle.exp (κ * t) := by
  rcases eq_or_ne κ 0 with rfl | hκ
  · simp
  · have hturn : κ * (2 * Real.pi / κ) = 2 * Real.pi := by field_simp
    exact (ChatgptAudit.PolarPeriod016.one_turn_gives_faithful_period hκ (Or.inl hturn)
      (t + 2 * Real.pi / κ) t).mpr ⟨1, by push_cast; ring⟩
""", 1))
E.append(("E5.12", "sonda V-T10-a: uso sem a hipotese",
          "  clock_reads_modulo_period one_ne_zero t\n", "  clock_reads_modulo_period 1 t\n", 1))

# E5.05 + E5.08 + E5.10: secao T11
E.append(("E5.05+E5.08+E5.10", "T11: atribuicao corrigida (S50.1 byte a byte; M6/AUD-7; M7/AUD-6); renomes; re-export duplicado removido",
"""/-! ## T11 — no atrator tracial o relógio modular para (face finita)

[INPUT da gerência — achado a mostrar ao operador] o estado fixo do canal ótico, `½·1`, É o Um absoluto
`absoluteRho (Fin 2)`, e nele o fluxo modular é a identidade. Em III₁ não há estado tracial e `σ_t` é externo
para `t ≠ 0` [KNOWN, Connes 1973]: NADA aqui se estende além da face finita. A leitura «o atrator é onde o
tempo repousa» é do operador. -/

/-- **T11.a.** O estado fixo do canal ótico, `½·1` em M₂(ℂ), é `absoluteRho (Fin 2)`. -/
theorem optical_attractor_is_the_absolute_one :
    (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) = absoluteRho (Fin 2) := by
  rw [absoluteRho, ← Matrix.smul_one_eq_diagonal]
  congr 1
  norm_num [Fintype.card_fin]

/-- **T11.a — re-exportação** de `TGLExt.absoluteOne_flow_trivial` (com o nome desta seção). -/
theorem the_absolute_one_has_no_clock {Region n : Type} [Fintype n] [DecidableEq n] [Nonempty n]
    (O : Region) (t : ℝ) (a : Matrix n n ℂ) : (absoluteOneField Region n).flow O t a = a :=
  absoluteOne_flow_trivial O t a

example : type_of% @TGLExt.absoluteOne_flow_trivial := @the_absolute_one_has_no_clock
example : type_of% @the_absolute_one_has_no_clock := @TGLExt.absoluteOne_flow_trivial

/-- T11 em uma linha: no atrator ótico `½·1` o relógio modular para (`σ_t = id`). -/
theorem optical_attractor_clock_stops (t : ℝ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    sigma ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) t a = a := by
  rw [optical_attractor_is_the_absolute_one]
  exact absoluteOne_flow_trivial (Region := Unit) () t a
""",
"""/-! ## T11 — no estado tracial ½·1 o relógio modular para (face finita)

[INPUT da gerência — achado a mostrar ao operador] o estado fixo do canal ótico, `½·1`, É o Um absoluto
`absoluteRho (Fin 2)`, e nele o fluxo modular é a identidade. Em III₁ não há estado tracial e `σ_t` é externo
para `t ≠ 0` [KNOWN, Connes 1973]: NADA aqui se estende além da face finita. O operador escreveu, byte a byte
(S50.1): «um lugar onde repousar e ser lembrada»; a formulação da R1 que ligava o atrator ao repouso do tempo
era da GERÊNCIA e SAIU (E5.05, achado M2). M6 / AUD-7 (seção própria): na face finita, repousar (o relógio
modular parado: populações IGUAIS, `aud_clock_stops_when_equal_populations`) e ser lembrada (o registro:
populações DISTINTAS, `aud_clock_runs_unless_equal_populations`) NÃO cabem no mesmo estado; a leitura que as
une é do operador (§8.4 do relatório R1). M7 / AUD-6 (E3.04): `½·1` tem posto 2 e pureza ½ — é o estado-atrator,
não o posto; o posto de posto 1 é a leitura-limite `R = J/2` (AUD-5); `ρ★ = diag(1, 0)` é um terceiro objeto.
Os nomes desta seção dizem só o que o termo prova: o canal ótico NÃO está nos enunciados (E5.08; achado
M3(3)); a versão COM o canal, genérica em θ e sem a constante da casa, é
`optical_channel_fixed_state_is_half_identity` (abaixo). -/

/-- **T11.a.** `½·1` em M₂(ℂ) é `absoluteRho (Fin 2)` (nome R2, E5.08: o enunciado não menciona o canal ótico). -/
theorem half_identity_is_absoluteRho_two :
    (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) = absoluteRho (Fin 2) := by
  rw [absoluteRho, ← Matrix.smul_one_eq_diagonal]
  congr 1
  norm_num [Fintype.card_fin]

/-- T11.a aponta para a re-exportação `tracial_state_freezes_the_flow` (T3.b (ii)); o re-export duplicado da
    R1 saiu (E5.10, achado M17). Em uma linha: em `½·1` o relógio modular para (`σ_t = id`); o canal ótico não
    está no enunciado (E5.08). -/
theorem half_identity_clock_stops (t : ℝ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    sigma ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) t a = a := by
  rw [half_identity_is_absoluteRho_two]
  exact absoluteOne_flow_trivial (Region := Unit) () t a

/-! ### (E5.08, opcional, feita) o canal ótico nas populações, genérico em θ, sem a constante da casa -/

/-- `R = J/2`: a leitura-limite nas populações (idempotente: AUD-5). -/
def halfJ : Matrix (Fin 2) (Fin 2) ℝ := !![1 / 2, 1 / 2; 1 / 2, 1 / 2]

/-- O canal ótico nas populações, `T_θ = R + (1 − 2 sin²θ)(I − R)` — `sin²θ` ocupa o lugar que o runtime dá à
    constante da casa; aqui é genérico. -/
def opticalPopulationMap (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  halfJ + (1 - 2 * Real.sin θ ^ 2) • (1 - halfJ)

theorem opticalPopulationMap_mulVec_zero (θ : ℝ) (x : Fin 2 → ℝ) :
    (opticalPopulationMap θ).mulVec x 0 = x 0 - Real.sin θ ^ 2 * (x 0 - x 1) := by
  simp [opticalPopulationMap, halfJ, Matrix.mulVec, dotProduct, Fin.sum_univ_two, Matrix.one_apply]
  ring

theorem opticalPopulationMap_mulVec_one (θ : ℝ) (x : Fin 2 → ℝ) :
    (opticalPopulationMap θ).mulVec x 1 = x 1 + Real.sin θ ^ 2 * (x 0 - x 1) := by
  simp [opticalPopulationMap, halfJ, Matrix.mulVec, dotProduct, Fin.sum_univ_two, Matrix.one_apply]
  ring

/-- **(E5.08, opcional) O estado fixo do canal ótico, COM o canal no enunciado.** Para `sin θ ≠ 0`:
    `T_θ x = x ⟺ x₀ = x₁` (`x ∈ span(1, 1)`). -/
theorem optical_channel_fixed_state_is_half_identity {θ : ℝ} (hθ : Real.sin θ ≠ 0) (x : Fin 2 → ℝ) :
    (opticalPopulationMap θ).mulVec x = x ↔ x 0 = x 1 := by
  have hs : Real.sin θ ^ 2 ≠ 0 := pow_ne_zero 2 hθ
  constructor
  · intro h
    have e0 := congrFun h 0
    rw [opticalPopulationMap_mulVec_zero] at e0
    have h2 : Real.sin θ ^ 2 * (x 0 - x 1) = 0 := by linarith
    rcases mul_eq_zero.mp h2 with h' | h'
    · exact absurd h' hs
    · linarith
  · intro hx
    rw [funext_iff, Fin.forall_fin_two, opticalPopulationMap_mulVec_zero, opticalPopulationMap_mulVec_one, hx]
    constructor <;> ring

/-- O único vetor de populações fixo e de soma 1 é `(½, ½)`. -/
theorem optical_channel_unique_fixed_population {θ : ℝ} (hθ : Real.sin θ ≠ 0) (x : Fin 2 → ℝ)
    (hfix : (opticalPopulationMap θ).mulVec x = x) (hsum : x 0 + x 1 = 1) : x = ![1 / 2, 1 / 2] := by
  have hx := (optical_channel_fixed_state_is_half_identity hθ x).mp hfix
  rw [funext_iff, Fin.forall_fin_two]
  constructor <;> simp <;> linarith

/-- … e o estado diagonal dessas populações é `½·1` (= `absoluteRho (Fin 2)`, T11.a). -/
theorem half_populations_state :
    rhoD (![1 / 2, 1 / 2] : Fin 2 → ℝ) = (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [rhoD]

/-- Controle do opcional — a hipótese `sin θ ≠ 0` pesa: com `sin θ = 0` o canal é a identidade e TUDO é fixo. -/
theorem optical_channel_trivial_when_sin_zero {θ : ℝ} (hθ : Real.sin θ = 0) (x : Fin 2 → ℝ) :
    (opticalPopulationMap θ).mulVec x = x := by
  rw [funext_iff, Fin.forall_fin_two, opticalPopulationMap_mulVec_zero, opticalPopulationMap_mulVec_one, hθ]
  constructor <;> ring

/-! ## Controles de especificidade AUD-1, AUD-2, AUD-5, AUD-6, AUD-7, AUD-8 [INPUT do auditor; ADENDO R2, E3.13 e §(e)]

Enunciados dos arquivos da auditoria de estatuto da R1 (`AudEstatutoTempo.lean` sha16 ed41c24b64b9da89,
`AudEstatutoTempo2.lean` 539982e97c342685, `AudEstatutoTempo3.lean` 3026a42ba04f0514), reproduzidos aqui com
o mesmo tipo e os mesmos nomes. Medem o PESO dos nomes; não são afirmações do operador. -/

/-- AUD-1: a multiplicação escalar `x ↦ e^{−s}·x` com `τ(x) = ‖x₀₁‖` é OUTRA instância de `DualScalingData`
    no MESMO tipo (e não preserva o traço). -/
def scalarScaling : DualScalingData (Matrix (Fin 2) (Fin 2) ℂ) where
  tau := fun x => ‖x 0 1‖
  theta := fun s x => (((Real.exp (-s)) : ℝ) : ℂ) • x
  scaling := fun s x => by
    show ‖((((Real.exp (-s)) : ℝ) : ℂ) • x) 0 1‖ = Real.exp (-s) * ‖x 0 1‖
    rw [Matrix.smul_apply, smul_eq_mul, norm_mul, Complex.norm_real, Real.norm_eq_abs,
      abs_of_pos (Real.exp_pos _)]

/-- AUD-1: as seis cláusulas da Ágape valem também para a multiplicação escalar — a Ágape é a lei de `e^{−s}`;
    o conteúdo específico do dephasing está em T8.c (`the_record_does_not_scale`), não nas seis cláusulas. -/
theorem aud_scalar_obeys_agape (x : Matrix (Fin 2) (Fin 2) ℂ) (hx : x 0 1 ≠ 0) :
    let D := scalarScaling
    (∀ s : ℝ, s ≠ 0 → ∀ m' : Matrix (Fin 2) (Fin 2) ℂ, D.theta s m' = m' → D.tau m' = 0) ∧
    (∀ s : ℝ, D.tau (D.theta s x) < D.tau (D.theta (s - 1) x)) ∧
    (∀ B : ℝ, ∃ s : ℝ, B < D.tau (D.theta s x)) ∧
    (∀ s : ℝ, 0 < D.tau (D.theta s x)) ∧
    (∀ ε : ℝ, 0 < ε → ∃ s : ℝ, D.tau (D.theta s x) < ε) ∧
    (∀ a : ℝ, Real.exp (-a) = 1 ↔ a = 0) := by
  intro D
  exact TGLExt.Fundacao.agape D (m := x) (norm_pos_iff.mpr hx)

/-- AUD-1: … e a multiplicação escalar APAGA o registro (o traço cai), ao contrário do dephasing
    (`dephase_preserves_trace`; T8.c). -/
theorem aud_scalar_erases_the_record :
    (scalarScaling.theta 1 (1 : Matrix (Fin 2) (Fin 2) ℂ)).trace ≠ (1 : Matrix (Fin 2) (Fin 2) ℂ).trace := by
  show ((((Real.exp (-1)) : ℝ) : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)).trace ≠ (1 : Matrix (Fin 2) (Fin 2) ℂ).trace
  rw [Matrix.trace_smul, Matrix.trace_one, smul_eq_mul]
  intro h
  have h2 : (((Real.exp (-1)) : ℝ) : ℂ) = 1 := by
    have hc : ((Fintype.card (Fin 2) : ℕ) : ℂ) ≠ 0 := by norm_num
    exact mul_right_cancel₀ hc (by rw [h, one_mul])
  have h3 : Real.exp (-1) = 1 := by exact_mod_cast h2
  have h4 := (Real.exp_eq_one_iff (-1)).mp h3
  norm_num at h4

/-- AUD-2: o boost (det 1, hiperbólico) NÃO tem atrator global — pousar no raio nulo (variedade estável) e ter
    bacia (dissipação, det < 1) são mecanismos distintos. -/
theorem aud_boost_has_no_global_attractor (s : ℝ) :
    ¬ ∀ v : Fin 2 → ℝ,
      Filter.Tendsto (fun k : ℕ => ((TGLExt.boost s) ^ k).mulVec v) Filter.atTop (nhds 0) := by
  intro h
  have h1 := global_attractor_needs_volume_loss (TGLExt.boost s) h (by norm_num)
  rw [TGLExt.boost_det] at h1
  norm_num at h1

/-- AUD-5: no discreto não invertível um passo PODE ser posto — `R = J/2` é idempotente (é o canal ótico em
    `λ = 0`). T9 depende da invertibilidade (lei de grupo), não do tempo em si. -/
theorem aud_discrete_step_can_be_a_post :
    IsIdempotentElem (!![1 / 2, 1 / 2; 1 / 2, 1 / 2] : Matrix (Fin 2) (Fin 2) ℝ) := by
  unfold IsIdempotentElem
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two] <;> norm_num

/-- AUD-6 (POSTO=RANK): o estado-atrator `½·1` tem posto 2 (pleno) … -/
theorem aud_attractor_state_has_full_rank :
    ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)).rank = 2 := by
  have hu : IsUnit ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) := by
    rw [Matrix.isUnit_iff_isUnit_det, Matrix.det_smul, Matrix.det_one, mul_one, isUnit_iff_ne_zero]
    norm_num
  rw [Matrix.rank_of_isUnit _ hu, Fintype.card_fin]

/-- AUD-6: … e pureza ½ — é o estado, não o posto (o posto 1 é a leitura-limite `R`, AUD-5). -/
theorem aud_attractor_state_purity_half :
    purityR ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) = 1 / 2 := by
  unfold purityR
  simp only [Fin.sum_univ_two, Matrix.smul_apply, Matrix.one_apply_eq, smul_eq_mul]
  rw [Matrix.one_apply_ne (by decide : (0 : Fin 2) ≠ 1), Matrix.one_apply_ne (by decide : (1 : Fin 2) ≠ 0)]
  simp [Complex.normSq_apply]
  norm_num

/-- AUD-7: populações DISTINTAS (`a ≠ b`, ambas `> 0`) ⟹ o relógio modular NÃO para (`E₀₁` não é fixo por todo
    `σ_t`): o que guarda um registro distinguível faz o relógio girar. -/
theorem aud_clock_runs_unless_equal_populations (a b : ℝ) (ha : 0 < a) (hb : 0 < b) (hab : a ≠ b) :
    ¬ ∀ t : ℝ, sigma (rhoD ![a, b]) t (!![0, 1; 0, 0] : Matrix (Fin 2) (Fin 2) ℂ) = !![0, 1; 0, 0] := by
  intro h
  have hd : ∀ i, 0 < (![a, b] : Fin 2 → ℝ) i := by
    intro i; fin_cases i <;> simp [ha, hb]
  have hinj : Function.Injective (![a, b] : Fin 2 → ℝ) := by
    intro i j hij
    fin_cases i <;> fin_cases j <;> simp_all
  have hfix := (sigma_fixed_iff_diag ![a, b] hd hinj _).mp h
  have h01 := congrFun (congrFun hfix 0) 1
  simp [diagExpect] at h01

/-- AUD-7: … e com populações IGUAIS o relógio para (o estado tracial: `½·1` após normalizar). -/
theorem aud_clock_stops_when_equal_populations (a : ℝ) (t : ℝ) (x : Matrix (Fin 2) (Fin 2) ℂ) :
    sigma (rhoD ![a, a]) t x = x := by
  have hc : rhoD ![a, a] = (a : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [rhoD]
  exact sigma_fixed_of_commute _ _ (by rw [hc]; exact (Commute.one_left x).smul_left (a : ℂ)) t

/-- AUD-8: em 2×2 real, `Mᵀ J M = (det M)·J` (identidade algébrica). -/
theorem aud_two_by_two_symplectic (M : Matrix (Fin 2) (Fin 2) ℝ) :
    Mᵀ * !![0, 1; -1, 0] * M = M.det • !![0, 1; -1, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.det_fin_two, Matrix.transpose_apply] <;> ring

/-- AUD-8: o boost preserva a forma simplética de ℝ² — é um mapa hamiltoniano linear; o controle C-T4-a cai
    DENTRO do escopo hamiltoniano da frase do operador (S44.1): Liouville proíbe a bacia, não o pouso. -/
theorem aud_boost_is_symplectic (s : ℝ) :
    (TGLExt.boost s)ᵀ * !![0, 1; -1, 0] * TGLExt.boost s = !![0, 1; -1, 0] := by
  rw [aud_two_by_two_symplectic, TGLExt.boost_det, one_smul]
""", 1))

# E5.15: aspas em paráfrase (se-e-só-se)
E.append(("E5.15", "«se e só se» (paráfrase, não citação) sem aspas de citação", "«se e só se»", "se-e-só-se", 5))

# E5.15: aspas « » em paráfrase da gerência (não são citações do operador) — a sonda de aspas exige 0 não achadas
E.append(("E5.15", "C-T1-a: «nenhum comutador é não nulo» é formulação da gerência: sem aspas de citação",
          "a afirmação falsa «nenhum comutador é não nulo» CAI", "a afirmação falsa *nenhum comutador é não nulo* CAI", 1))
E.append(("E5.15", "C-T7-a: «inverso» é palavra da gerência: sem aspas de citação",
          "em `t = 0` o «inverso» é a identidade", "em `t = 0` o inverso linear é a identidade", 1))

# E5.13: docstring de V-GERAL-1
E.append(("E5.13", "V-GERAL-1: regra R2 (habitada OU condicional)",
"""Cada `example` instancia teoremas com argumentos CONCRETOS (exibe provas de todas as hipóteses). Não habitadas
aqui, e ditas: `nontracial_state_rejects_the_identity_flow` (exige uma testemunha AQFT `W` do kernel) e
`light_modular_orbit_converges_iff_post` / `light_flow_group` (exigem um `FockCertificate`). -/
""",
"""Cada `example` instancia teoremas com argumentos CONCRETOS (exibe provas de todas as hipóteses). Regra R2
(E5.13): toda hipótese habitada OU a declaração marcada CONDICIONAL, sem terceira via. Habitada nesta R2:
`nontracial_state_rejects_the_identity_flow` (sonda `probe_identity_flow_not_kms_inhabited`, com
`theSpecificAQFTWitness`), além da versão de face finita `identity_flow_not_kms_finite`. CONDICIONAIS, sem
habitante exibido, e ditas: `light_modular_orbit_converges_iff_post` / `light_flow_group` (exigem um
`FockCertificate`; TheImportedSecondQuantization.lean l.66; a sonda opcional com `lightNet` NÃO foi construída). -/
""", 1))
E.append(("E5.10", "V-GERAL-1 (T11): aponta para tracial_state_freezes_the_flow",
          "  have _h12 := the_absolute_one_has_no_clock (Region := Unit) (n := Fin 2) () 1 psiPlus\n",
          "  have _h12 := tracial_state_freezes_the_flow (Region := Unit) (n := Fin 2) () 1 psiPlus\n", 1))

# the_two_regimes_of_time: docstring + conjunto 8 (E5.12)
E.append(("E5.02+E5.12", "the_two_regimes_of_time: docstring sem identificar regimes; conjunto 8 para todo κ",
"""/-- **the_two_regimes_of_time** — T4.b (abstrato, discreto e contínuo) ∧ T4.c (c1, c1 < 1, c2) ∧ T6.c ∧
    T7.b ∧ T10.b: o ângulo gira sem pousar; a face contrai, perde pureza, e o seu inverso não é canal; o
    relógio angular lê só a classe. -/
""",
"""/-- **the_two_regimes_of_time** (nome da R1, mantido; só conjunção) — T4.b (abstrato, discreto e contínuo) ∧
    T4.c (c1, c1 < 1, c2) ∧ T6.c ∧ T7.b ∧ T10.b: sob isometria nada pousa; a defasagem contrai o volume, perde
    pureza, e o seu inverso não é canal; o fluxo modular conserva o volume; o relógio lê só a classe (agora
    para TODO `κ`: E5.12). O nome NÃO afirma a identificação destes comportamentos com os dois regimes da
    casa, que segue [OPEN] (v384; E5.02). -/
""", 1))
E.append(("E5.12", "the_two_regimes_of_time: conjunto 8 sem κ ≠ 0",
          "    (∀ {κ : ℝ}, κ ≠ 0 → ∀ t : ℝ, Circle.exp (κ * (t + 2 * Real.pi / κ)) = Circle.exp (κ * t)) ∧\n",
          "    (∀ κ t : ℝ, Circle.exp (κ * (t + 2 * Real.pi / κ)) = Circle.exp (κ * t)) ∧\n", 1))
E.append(("E5.12", "the_two_regimes_of_time: prova do conjunto 8",
          "  · intro κ hκ t; exact clock_reads_modulo_period hκ t\n",
          "  · intro κ t; exact clock_reads_modulo_period κ t\n", 1))

# #print axioms: renomes, remocao, novos
E.append(("E5.06", "#print axioms: T3.a renomeado",
          "#print axioms TGLExt.TheTimeHasNoRank.time_is_the_modular_flow\n",
          "#print axioms TGLExt.TheTimeHasNoRank.modular_flow_is_a_kms_group\n", 1))
E.append(("E5.07", "#print axioms: clausula composta renomeada",
          "#print axioms TGLExt.TheTimeHasNoRank.the_time_has_no_rank\n",
          "#print axioms TGLExt.TheTimeHasNoRank.the_time_is_not_a_post\n", 1))
E.append(("E5.07", "#print axioms: sonda renomeada",
          "#print axioms TGLExt.TheTimeHasNoRank.probe_the_time_has_no_rank\n",
          "#print axioms TGLExt.TheTimeHasNoRank.probe_the_time_is_not_a_post\n", 1))
E.append(("E5.08+E5.10", "#print axioms: T11 renomes e remocao do re-export duplicado",
"""#print axioms TGLExt.TheTimeHasNoRank.optical_attractor_is_the_absolute_one
#print axioms TGLExt.TheTimeHasNoRank.the_absolute_one_has_no_clock
#print axioms TGLExt.TheTimeHasNoRank.optical_attractor_clock_stops
""",
"""#print axioms TGLExt.TheTimeHasNoRank.half_identity_is_absoluteRho_two
#print axioms TGLExt.TheTimeHasNoRank.half_identity_clock_stops
""", 1))
E.append(("E5.13+E5.08+E3.13", "#print axioms: declaracoes novas",
"""#print axioms TGLExt.TheTimeHasNoRank.centralizer_iff_needs_injective_weights
""",
"""#print axioms TGLExt.TheTimeHasNoRank.centralizer_iff_needs_injective_weights
#print axioms TGLExt.TheTimeHasNoRank.gibbs_rho_two_thirds_E01_E10
#print axioms TGLExt.TheTimeHasNoRank.gibbs_rho_two_thirds_E10_E01
#print axioms TGLExt.TheTimeHasNoRank.identity_flow_not_kms_finite
#print axioms TGLExt.TheTimeHasNoRank.identity_flow_not_kms_finite'
#print axioms TGLExt.TheTimeHasNoRank.tracial_state_satisfies_pair_identity
#print axioms TGLExt.TheTimeHasNoRank.star_inner_eq_state
#print axioms TGLExt.TheTimeHasNoRank.probe_identity_flow_not_kms_inhabited
#print axioms TGLExt.TheTimeHasNoRank.halfJ
#print axioms TGLExt.TheTimeHasNoRank.opticalPopulationMap
#print axioms TGLExt.TheTimeHasNoRank.opticalPopulationMap_mulVec_zero
#print axioms TGLExt.TheTimeHasNoRank.opticalPopulationMap_mulVec_one
#print axioms TGLExt.TheTimeHasNoRank.optical_channel_fixed_state_is_half_identity
#print axioms TGLExt.TheTimeHasNoRank.optical_channel_unique_fixed_population
#print axioms TGLExt.TheTimeHasNoRank.half_populations_state
#print axioms TGLExt.TheTimeHasNoRank.optical_channel_trivial_when_sin_zero
#print axioms TGLExt.TheTimeHasNoRank.scalarScaling
#print axioms TGLExt.TheTimeHasNoRank.aud_scalar_obeys_agape
#print axioms TGLExt.TheTimeHasNoRank.aud_scalar_erases_the_record
#print axioms TGLExt.TheTimeHasNoRank.aud_boost_has_no_global_attractor
#print axioms TGLExt.TheTimeHasNoRank.aud_discrete_step_can_be_a_post
#print axioms TGLExt.TheTimeHasNoRank.aud_attractor_state_has_full_rank
#print axioms TGLExt.TheTimeHasNoRank.aud_attractor_state_purity_half
#print axioms TGLExt.TheTimeHasNoRank.aud_clock_runs_unless_equal_populations
#print axioms TGLExt.TheTimeHasNoRank.aud_clock_stops_when_equal_populations
#print axioms TGLExt.TheTimeHasNoRank.aud_two_by_two_symplectic
#print axioms TGLExt.TheTimeHasNoRank.aud_boost_is_symplectic
""", 1))
# por ultimo, o prefixo do namespace em TODOS os #print axioms (contagem conferida pelo script)
E.append(("E5.07", "#print axioms: prefixo do namespace renomeado (todas as linhas)",
          "#print axioms TGLExt.TheTimeHasNoRank.", "#print axioms TGLExt.TheTimeIsNotAPost.", None))


def main(src, dst):
    b = open(src, "rb").read()
    txt = b.decode("utf-8")
    sha_src = hashlib.sha256(b).hexdigest()
    registro = []
    for (eid, desc, old, new, n_esp) in E:
        n = txt.count(old)
        if n_esp is not None and n != n_esp:
            raise SystemExit("FALHA VISIVEL em %s (%s): esperado %d ocorrencia(s), achadas %d" % (eid, desc, n_esp, n))
        if n_esp is None and n == 0:
            raise SystemExit("FALHA VISIVEL em %s (%s): 0 ocorrencias" % (eid, desc))
        # linhas antigas (para o registro): numero e sha16 de cada linha do trecho antigo
        pos = txt.find(old)
        lin_ini = txt.count("\n", 0, pos) + 1
        linhas_antigas = [{"linha_R1": lin_ini + i, "sha16": sha16(l.encode("utf-8"))}
                          for i, l in enumerate(old.rstrip("\n").split("\n"))] if n == 1 else None
        txt = txt.replace(old, new)
        registro.append({"id": eid, "descricao": desc, "ocorrencias": n, "linhas_antigas_R1": linhas_antigas,
                         "sha16_antigo": sha16(old.encode("utf-8")), "sha16_novo": sha16(new.encode("utf-8"))})
    # salvaguardas finais (fail-closed): nenhum resto do nome antigo, nenhuma das frases que a regua proibe
    proibidas = ["TheTimeHasNoRank", "the_time_has_no_rank", "no_rank", "o tempo é o Verbo", "não o Nome",
                 "tempo não tem posto", "relógio mede", "o atrator é onde o tempo repousa", "regime do ÂNGULO",
                 "time_is_the_modular_flow", "optical_attractor", "the_absolute_one_has_no_clock",
                 "_hd : ∀ i, 0 < d i", "(hκ : κ ≠ 0) (t : ℝ)", ": True := by\n  haveI"]
    restos = {p: txt.count(p) for p in proibidas if txt.count(p)}
    if restos:
        raise SystemExit("FALHA VISIVEL: restos proibidos na pedra R2: %r" % restos)
    out = txt.encode("utf-8")
    with open(dst + ".tmp", "wb") as f:
        f.write(out)
    os.replace(dst + ".tmp", dst)
    rec = {"fonte_R1": src, "fonte_R1_sha256": sha_src, "fonte_R1_bytes": len(b),
           "pedra_R2": dst, "pedra_R2_sha256": hashlib.sha256(out).hexdigest(), "pedra_R2_bytes": len(out),
           "n_substituicoes": len(registro), "substituicoes": registro,
           "salvaguardas_proibidas_com_0_ocorrencias": proibidas,
           "nota": "Cada item e uma substituicao exata sobre a copia de bytes da pedra R1; a contagem esperada foi "
                   "conferida (fail-closed). A lista segue a E5 do ADENDO_R2.md (congelado) e os itens E3.02/E3.12 "
                   "que tocam docstrings da pedra; a E5.08 opcional e a habitacao AQFT opcional (E5.13) foram feitas."}
    with open(OUT_JSON + ".tmp", "wb") as f:
        f.write(json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(OUT_JSON + ".tmp", OUT_JSON)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({k: v for k, v in rec.items() if k != "substituicoes"}, ensure_ascii=False, indent=1))
    for r in registro:
        print(r["id"], "|", r["ocorrencias"], "|", r["descricao"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
