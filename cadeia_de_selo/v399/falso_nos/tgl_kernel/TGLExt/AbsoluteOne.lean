import TGLExt.PsiEmergence

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# Ψ = 1_abs: o campo é o Um absoluto — a construção canônica começa
  [TGLExt — v58, a identificação final do operador]

A identificação canônica: **Ψ = 1_abs** — o campo não "vale 1": é a
seção-unitária originária, `Ψ_abs(𝒪) = 1_{M(𝒪)}`. Consequências
CONSTRUÍDAS nesta pedra (a "construção canônica da dinâmica de Ψ=1_abs"
na face onde ela é hoje demonstrável, sem fabricar):

* ★ `absoluteOneField` — O TERMO CANÔNICO de `PsiHomeData` que a
  identificação seleciona SEM ESCOLHA ALGUMA: `ρ_Ψ(𝒪) = I/n` (o vetor
  GNS é a unidade normalizada: Ω = √(I/n) = I/√n). A subdeterminação do
  v57 fica RESOLVIDA PELA IDENTIFICAÇÃO: dado Ψ = 1_abs, a morada é
  determinada — e `ω_Ψ(I) = 1` segue por `PsiHomeData.name_one`
  (a cadeia do especialista: Ψ = 1_abs ⟹ ω_Ψ(I) = 1);
* ★ `absoluteOne_name_eq_trace` — o NOME do Um é O TRAÇO normalizado
  (o estado canônico; nenhum parâmetro);
* ★ `absoluteOne_flow_trivial` — **O TRANSPORTE DO UM ABSOLUTO É
  TRIVIAL**: σ^Ψ_t = id para Ψ = 1_abs. Sem contraste não há fluxo
  modular, não há dephasing, não há curvatura — a gravidade é a
  curvatura da INSCRIÇÃO (q ≠ 0), não do absoluto. O par exato do
  `excite_holonomy_flat` (v54): "onde o Um cola, não há curvatura;
  onde um patch se recusa ao Um, a holonomia a mede";
* ★ `commutator_locks_annihilate_one` + `commutator_kernel_inhabited` —
  a dinâmica canônica da casa é curvatura-por-comutador (v48/E11); e
  COMUTADORES ANULAM O UM (`δ_A(1) = 0`): logo `𝒟_Ψ(1_abs) = 0`
  canonicamente e o núcleo físico é NÃO-NULO porque o Um o habita —
  a cláusula "ker ≠ 0" de Breuer é DERIVADA, não inserida;
* ★ `corner_fixes_inhabitant` — em Hilbert GENÉRICO (∞-dim): se
  `𝒟 Ω = 0` então `P_F Ω = Ω` — o requisito do operador
  (`P_{F,Ψ}Ω_Ψ = Ω_Ψ`: o Um está no núcleo físico do transporte)
  como teorema de uma linha sobre o v56.

A correspondência final `1 = q² + α²` é a espinha do próprio runtime
(verificada a resíduo 0,0 em cada rodada): a identificação Ψ = 1_abs dá
a ela o estatuto de decomposição pitagórica da inscrição do Um
(α_abs = 1; o observado α_obs = sech(κ/2) entra pelo contraste q).

HONESTIDADE. O que esta pedra NÃO fecha: o pacote CONTÍNUO (o core
III₁/II_∞ com traço de Breuer genuíno e a solda e_Ψ — a face finita do
absoluto é tracial/plana POR TEOREMA; a física observada é a deformação
q ≠ 0, e o III₁ vive no contínuo, v45). `full_TGL_witness = False`
INALTERADO; E7 INALTERADO. β JAMAIS entra. Sem sorry, sem axiom.
Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix
open scoped ComplexOrder MatrixOrder

noncomputable section

variable {Region : Type} {n : Type} [Fintype n] [DecidableEq n]

/-! ## A — o termo canônico: Ψ = 1_abs seleciona a morada sem escolha -/

/-- a densidade do Um absoluto: `ρ_Ψ = I/n` (Ω = I/√n, a unidade
    normalizada como vetor GNS). -/
def absoluteRho (n : Type) [Fintype n] [DecidableEq n] : Matrix n n ℂ :=
  Matrix.diagonal fun _ => (Fintype.card n : ℂ)⁻¹

theorem absoluteRho_posDef [Nonempty n] : (absoluteRho n).PosDef := by
  rw [absoluteRho, Matrix.posDef_diagonal_iff]
  intro i
  have h : (0 : ℝ) < ((Fintype.card n : ℝ))⁻¹ := by
    have : 0 < Fintype.card n := Fintype.card_pos
    positivity
  have := Complex.zero_lt_real.mpr h
  simpa using this

theorem absoluteRho_trace [Nonempty n] : (absoluteRho n).trace = 1 := by
  rw [absoluteRho, Matrix.trace_diagonal]
  have hn : (Fintype.card n : ℂ) ≠ 0 := by
    exact_mod_cast Fintype.card_ne_zero
  simp [Finset.sum_const, Finset.card_univ, hn]

/-- ★ O TERMO CANÔNICO: a identificação `Ψ = 1_abs` seleciona a regra do
    campo SEM ESCOLHA — a subdeterminação (v57) resolvida PELA identificação.
    `ω_Ψ(I) = 1` segue por `PsiHomeData.name_one` aplicado a este termo. -/
noncomputable def absoluteOneField (Region : Type) (n : Type) [Fintype n]
    [DecidableEq n] [Nonempty n] : PsiHomeData Region n where
  rho := fun _ => absoluteRho n
  rho_posDef := fun _ => absoluteRho_posDef
  rho_trace_one := fun _ => absoluteRho_trace

/-- [KERNEL] ★ EXISTÊNCIA CANÔNICA (corolário do termo): o campo absoluto
    habita `PsiHomeData` para toda rede de regiões — sem parâmetro algum. -/
theorem absoluteOneField_exists (Region : Type) (n : Type) [Fintype n]
    [DecidableEq n] [Nonempty n] : Nonempty (PsiHomeData Region n) :=
  ⟨absoluteOneField Region n⟩

/-- [KERNEL] ★ O NOME DO UM É O TRAÇO: `ω_Ψ(a) = Tr(a)/n` — o estado
    canônico, determinado pela identificação (nenhuma escolha). -/
theorem absoluteOne_name_eq_trace [Nonempty n] (O : Region)
    (a : Matrix n n ℂ) :
    (absoluteOneField Region n).name O a = (Fintype.card n : ℂ)⁻¹ * a.trace := by
  show gibbs (absoluteRho n) a = (Fintype.card n : ℂ)⁻¹ * a.trace
  rw [gibbs, absoluteRho]
  rw [← Matrix.smul_one_eq_diagonal]
  rw [Matrix.smul_mul, Matrix.one_mul, Matrix.trace_smul]
  simp

/-! ## B — o transporte do absoluto é trivial: sem contraste, sem curvatura -/

theorem absoluteRho_commute (a : Matrix n n ℂ) :
    Commute (absoluteRho n) a := by
  rw [absoluteRho, ← Matrix.smul_one_eq_diagonal]
  unfold Commute SemiconjBy
  rw [Matrix.smul_mul, Matrix.mul_smul, Matrix.one_mul, Matrix.mul_one]

/-- [KERNEL] ★ O TRANSPORTE DO UM ABSOLUTO É TRIVIAL: `σ^Ψ_t = id` para
    `Ψ = 1_abs` — o absoluto não tem contraste interno: sem fluxo modular,
    sem dephasing, SEM CURVATURA. A gravidade é a curvatura da INSCRIÇÃO
    (`q ≠ 0`), não do Um (o par do `excite_holonomy_flat`, v54). -/
theorem absoluteOne_flow_trivial [Nonempty n] (O : Region) (t : ℝ)
    (a : Matrix n n ℂ) :
    (absoluteOneField Region n).flow O t a = a := by
  show sigma (absoluteRho n) t a = a
  have hlog : Commute a (logRho (absoluteRho n)) :=
    ((absoluteRho_commute a).cfc_real Real.log).symm
  have hmp : Commute a (modPow (absoluteRho n) t) := by
    unfold modPow
    exact (hlog.smul_right _).exp_right
  unfold sigma
  rw [← hmp.eq, mul_assoc, modPow_mul_neg, mul_one]

/-! ## C — a dinâmica canônica anula o Um: ker ≠ 0 DERIVADO -/

/-- [KERNEL] ★ OS LOCKS-COMUTADORES ANULAM O UM: para a dinâmica canônica
    da casa (curvatura-por-comutador, v48), `𝒟_Ψ(1_abs) = 0` — o Um está
    no núcleo físico por construção, não por inserção. -/
theorem commutator_locks_annihilate_one (A B C : Matrix n n ℂ) :
    excite A 1 = 0 ∧ excite B 1 = 0 ∧ excite C 1 = 0 :=
  ⟨excite_one_zero A, excite_one_zero B, excite_one_zero C⟩

/-- [KERNEL] ★ O NÚCLEO FÍSICO É NÃO-NULO PORQUE O UM O HABITA: a cláusula
    "ker 𝒟 ≠ 0" da camada de Breuer é DERIVADA para a dinâmica canônica
    (o habitante que garante a positividade do canto é o próprio 1_abs). -/
theorem commutator_kernel_inhabited [Nonempty n] (A : Matrix n n ℂ) :
    excite A (1 : Matrix n n ℂ) = 0 ∧ (1 : Matrix n n ℂ) ≠ 0 := by
  refine ⟨excite_one_zero A, fun h => ?_⟩
  have := congrFun (congrFun h (Classical.arbitrary n)) (Classical.arbitrary n)
  simp [Matrix.zero_apply] at this

/-! ## D — o canto fixa o habitante: P_F Ω = Ω em Hilbert genérico -/

/-- [KERNEL] ★ O CANTO FIXA O HABITANTE (∞-dim): se `𝒟 Ω = 0` então
    `P_F Ω = Ω` — o requisito do operador (`P_{F,Ψ}Ω_Ψ = Ω_Ψ`: o Um está
    no núcleo físico do transporte) como corolário de uma linha do v56. -/
theorem corner_fixes_inhabitant {H W : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] [NormedAddCommGroup W]
    [NormedSpace ℂ W] (D : H →L[ℂ] W) {u : H} (hu : D u = 0) :
    D.ker.starProjection u = u := by
  rw [Submodule.starProjection_eq_self_iff]
  exact hu

end

end TGLExt
