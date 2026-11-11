import TGLExt.TheDischargedOath
import TGLExt.TheImportedCommutation
import TGLExt.NoNormalTrace

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O JURAMENTO NA TORRE — o centralizador de ω, livre de fluxo, e o levantamento no contínuo
  [TGLExt — v308; casa "Nós" (31/08/2026)]

## A ORDEM ("vamos enfrentar o que resta do lema 3") E O QUE O CÉTICO MEDIU

A rota ingênua — transportar o CÓDIGO DIAGONAL da v307 à torre — está **REFUTADA, e a
refutação é teorema desta pedra** (`the_diagonal_does_not_survive_degeneracy`): os pesos
da torre COLIDEM a partir do andar 2 (o produto de Kronecker degenera: (1/3)·w·(2/3) =
(2/3)·w·(1/3)), e num bloco degenerado uma rotação preserva o estado e tira a diagonal
de si. É a anatomia da rota morta 25: *o código diagonal não é função espectral do
gerador*.

**O objeto certo do contínuo é o CENTRALIZADOR DE ω EM FORMA LIVRE-DE-FLUXO**
(`omegaCentralizer`): definível com `omegaState` apenas — sem S, sem Δ, sem σ_t —
contornando por inteiro a parede analítica nomeada em `TheModularRelations.lean`
(`[OPEN, ANALÍTICO]`: S fechável / Δ auto-adjunto não sobem por continuidade).

## O QUE ESTA PEDRA PROVA (tudo em casa, sem importação)

* `conj_commutant_of_biinverse` — a generalização não-involutiva que faltava;
* `TowerHorizon` — o horizonte da torre TIPADO com os TRÊS campos que o contínuo exige
  (unitário + normaliza M + preserva ω): na face finita M era tudo e a normalização era
  grátis; aqui ela é a diferença honesta, e fica dita;
* os quatro transportes do horizonte (`adT_mul`/`adT_sub`/`adT_star`/cancelamentos) —
  a disciplina que faz todo o resto colapsar em álgebra de uma linha;
* ★★★ `horizon_preserves_centralizer` / `horizon_centralizer_eq` — **o juramento na
  torre**: todo horizonte ω-invariante preserva o centralizador de ω — TEOREMA;
* `the_centralizer_is_seq_closed` — o fecho não é postulado: sob ω normal (teorema da
  casa: `omegaState_seqWOT`), o centralizador fecha sob limites WOT sequenciais;
* ★★ `the_diagonal_does_not_survive_degeneracy` — a refutação tipada do transporte
  ingênuo (o presente do cético das rotas mortas; rotação racional 3-4-5);
* `ExpectationInput` — o contrato da esperança de Takesaki no molde do
  `CommutationInput` (v282): o TIPO antes do habitante;
* ★★★ `the_expectation_is_unique` — a unicidade É DA CASA: ω(A†A) = ‖AΩ‖², definido
  porque ω é separante — o papel do `frob_self_definite` da v143, pago no contínuo;
* ★★★★★ `the_lift_on_the_tower` — **A IMPLICAÇÃO DO LEMA 3 NO CONTÍNUO**: contrato da
  esperança + horizonte ω-invariante ⟹ Ad(U)∘E = E∘Ad(U) sobre M.

## A CONTABILIDADE HONESTA (a régua, sem desconto)

O que resta do Lema 3 no contínuo, DEPOIS desta pedra, são exatamente DOIS itens:
(1) o campo importável do `ExpectationInput` — a existência da esperança de Takesaki
    sobre o centralizador [KNOWN, Takesaki 1972; importável no padrão gpi_, com as
    hipóteses da casa provadas: Ω cíclico, ω separante, ω normal];
(2) a ω-invariância do horizonte físico — o axioma ω(I)=1 lido no horizonte.
NÃO se declara o Lema 3 resolvido; o gate NÃO se move; nenhum `qgf_*` é tocado; β
jamais literal. `TheDischargedOath` (face) e `GlobalLiftConditional` (v143) ficam
INTACTAS; esta pedra é o degrau do contínuo que as consome. ⚠ Homônimos vedados:
`towerFlow` é POR ANDAR (tipo matricial), não fluxo da torre; o `commutantSet` desta
família é o de `[Ring A]` — nunca o de `Module.End` da face finita; "código" aqui é
conjunto de OPERADORES, não o submódulo de VETORES da v307.
-/

namespace TGLExt

open Matrix

noncomputable section

/-! ## A — a generalização não-involutiva: bijeção multiplicativa move comutantes -/

/-- [KERNEL] Φ multiplicativa com inversa bilateral Ψ leva comutante em comutante.
    A `conj_commutant` da casa pedia involução; a matemática pede só a bijeção. -/
theorem conj_commutant_of_biinverse {A : Type} [Ring A] (Φ Ψ : A → A)
    (hmul : ∀ x y, Φ (x * y) = Φ x * Φ y)
    (hΨΦ : ∀ x, Ψ (Φ x) = x) (hΦΨ : ∀ x, Φ (Ψ x) = x) (S : Set A) :
    Φ '' commutantSet S = commutantSet (Φ '' S) := by
  ext y
  constructor
  · rintro ⟨x, hx, rfl⟩ s ⟨t, ht, rfl⟩
    rw [← hmul, ← hmul, hx t ht]
  · intro hy
    refine ⟨Ψ y, ?_, hΦΨ y⟩
    intro s hs
    have hinj : Function.Injective Φ := Function.LeftInverse.injective hΨΦ
    apply hinj
    rw [hmul, hmul, hΦΨ]
    exact hy (Φ s) ⟨s, hs, rfl⟩

/-! ## B — os objetos do contínuo: o centralizador livre-de-fluxo e o horizonte -/

variable (P : SiteProfile)

/-- **O CENTRALIZADOR DE ω, LIVRE DE FLUXO** — o código do contínuo. -/
def omegaCentralizer : Set (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  {A | A ∈ theFactorObject P ∧
       ∀ B ∈ theFactorObject P,
         omegaState P (A * B) = omegaState P (B * A)}

/-- **O HORIZONTE DA TORRE**, com os TRÊS campos que o contínuo exige. -/
structure TowerHorizon where
  U : TowerHilbert P →L[ℂ] TowerHilbert P
  unitary_left : star U * U = 1
  unitary_right : U * star U = 1
  normalizes : ∀ A ∈ theFactorObject P, U * A * star U ∈ theFactorObject P
  normalizes_inv : ∀ A ∈ theFactorObject P, star U * A * U ∈ theFactorObject P
  preserves : ∀ A ∈ theFactorObject P,
    omegaState P (U * A * star U) = omegaState P A

variable {P}

/-- a conjugação pelo horizonte. -/
def adT (h : TowerHorizon P) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    TowerHilbert P →L[ℂ] TowerHilbert P := h.U * A * star h.U

/-- a conjugação inversa, em forma explícita. -/
def adTinv (h : TowerHorizon P) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    TowerHilbert P →L[ℂ] TowerHilbert P := star h.U * A * h.U

/-! ## B' — os quatro transportes (a disciplina que colapsa todo o resto) -/

theorem adT_mul (h : TowerHorizon P)
    (X Y : TowerHilbert P →L[ℂ] TowerHilbert P) :
    adT h (X * Y) = adT h X * adT h Y := by
  unfold adT
  simp only [mul_assoc]
  rw [← mul_assoc (star h.U) h.U, h.unitary_left, one_mul]

theorem adT_sub (h : TowerHorizon P)
    (X Y : TowerHilbert P →L[ℂ] TowerHilbert P) :
    adT h (X - Y) = adT h X - adT h Y := by
  unfold adT
  rw [mul_sub, sub_mul]

theorem adT_star (h : TowerHorizon P)
    (X : TowerHilbert P →L[ℂ] TowerHilbert P) :
    adT h (star X) = star (adT h X) := by
  unfold adT
  rw [star_mul, star_mul, star_star, mul_assoc]

theorem adT_adTinv (h : TowerHorizon P)
    (X : TowerHilbert P →L[ℂ] TowerHilbert P) :
    adT h (adTinv h X) = X := by
  unfold adT adTinv
  simp only [mul_assoc]
  rw [← mul_assoc (star h.U) X, ← mul_assoc h.U (star h.U * X)]
  rw [← mul_assoc h.U (star h.U), h.unitary_right, one_mul, mul_one]

theorem adTinv_adT (h : TowerHorizon P)
    (X : TowerHilbert P →L[ℂ] TowerHilbert P) :
    adTinv h (adT h X) = X := by
  unfold adT adTinv
  simp only [mul_assoc]
  rw [← mul_assoc h.U X, ← mul_assoc (star h.U) (h.U * X)]
  rw [← mul_assoc (star h.U) h.U, h.unitary_left, one_mul, mul_one]

theorem adTinv_mem (h : TowerHorizon P)
    {X : TowerHilbert P →L[ℂ] TowerHilbert P} (hX : X ∈ theFactorObject P) :
    adTinv h X ∈ theFactorObject P := h.normalizes_inv X hX

theorem adT_mem (h : TowerHorizon P)
    {X : TowerHilbert P →L[ℂ] TowerHilbert P} (hX : X ∈ theFactorObject P) :
    adT h X ∈ theFactorObject P := h.normalizes X hX

/-- ω(adT X) = ω(X) sobre M (o campo `preserves`, na notação do transporte). -/
theorem omega_adT (h : TowerHorizon P)
    {X : TowerHilbert P →L[ℂ] TowerHilbert P} (hX : X ∈ theFactorObject P) :
    omegaState P (adT h X) = omegaState P X := h.preserves X hX

/-! ## C — O JURAMENTO NA TORRE: o horizonte preserva o centralizador -/

/-- [KERNEL] ★★★ **O JURAMENTO NA TORRE**: todo horizonte ω-invariante leva o
    centralizador de ω em si mesmo. Álgebra de estado pura — nenhum fluxo, nenhum
    Δ, nenhum juramento. -/
theorem horizon_preserves_centralizer (h : TowerHorizon P) :
    ∀ A ∈ omegaCentralizer P, adT h A ∈ omegaCentralizer P := by
  rintro A ⟨hAM, hAc⟩
  refine ⟨adT_mem h hAM, ?_⟩
  intro B hBM
  have hB'M : adTinv h B ∈ theFactorObject P := adTinv_mem h hBM
  have hBB : B = adT h (adTinv h B) := (adT_adTinv h B).symm
  rw [hBB, ← adT_mul, ← adT_mul]
  rw [omega_adT h (mul_mem hAM hB'M), omega_adT h (mul_mem hB'M hAM)]
  exact hAc _ hB'M

/-- o horizonte inverso (a volta é horizonte também — derivado). -/
def TowerHorizon.inv (h : TowerHorizon P) : TowerHorizon P where
  U := star h.U
  unitary_left := by rw [star_star]; exact h.unitary_right
  unitary_right := by rw [star_star]; exact h.unitary_left
  normalizes := by
    intro A hA
    rw [star_star]
    exact h.normalizes_inv A hA
  normalizes_inv := by
    intro A hA
    rw [star_star]
    exact h.normalizes A hA
  preserves := by
    intro A hA
    rw [star_star]
    have hmem : star h.U * A * h.U ∈ theFactorObject P := h.normalizes_inv A hA
    have hstep := h.preserves (star h.U * A * h.U) hmem
    have hred : h.U * (star h.U * A * h.U) * star h.U = A := by
      show adT h (adTinv h A) = A
      exact adT_adTinv h A
    rw [hred] at hstep
    exact hstep.symm

/-- a inversa em termos do horizonte inverso: adT (h.inv) = adTinv h. -/
theorem adT_inv_eq (h : TowerHorizon P)
    (X : TowerHilbert P →L[ℂ] TowerHilbert P) :
    adT h.inv X = adTinv h X := by
  unfold adT adTinv TowerHorizon.inv
  rw [star_star]

/-- [KERNEL] ★★★ a igualdade de imagem: Ad(U) '' (centralizador) = centralizador. -/
theorem horizon_centralizer_eq (h : TowerHorizon P) :
    adT h '' omegaCentralizer P = omegaCentralizer P := by
  apply Set.Subset.antisymm
  · rintro _ ⟨A, hA, rfl⟩
    exact horizon_preserves_centralizer h A hA
  · intro A hA
    refine ⟨adTinv h A, ?_, adT_adTinv h A⟩
    have := horizon_preserves_centralizer h.inv A hA
    rwa [adT_inv_eq] at this

/-! ## D — o fecho: o centralizador é sequencialmente fechado quando ω é normal -/

/-- [KERNEL] ★★ **O FECHO NÃO É POSTULADO**: sob ω normal (SeqWOT — teorema da casa
    para o perfil da assinatura), o centralizador fecha sob limites WOT sequenciais
    limitados dentro de M. -/
theorem the_centralizer_is_seq_closed
    (hω : SeqWOTContinuous (theFactorObject P) (omegaState P))
    (T : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P)
    (Tinf : TowerHilbert P →L[ℂ] TowerHilbert P) (C : ℝ)
    (hmem : ∀ k, T k ∈ omegaCentralizer P)
    (hinf : Tinf ∈ theFactorObject P)
    (hbd : ∀ k, ‖T k‖ ≤ C)
    (hwot : ∀ ξ η : TowerHilbert P,
      Filter.Tendsto (fun k => (inner ℂ ξ (T k η) : ℂ))
        Filter.atTop (nhds (inner ℂ ξ (Tinf η)))) :
    Tinf ∈ omegaCentralizer P := by
  refine ⟨hinf, ?_⟩
  intro B hBM
  have hTkM : ∀ k, T k ∈ theFactorObject P := fun k => (hmem k).1
  have h1 : Filter.Tendsto (fun k => omegaState P (T k * B))
      Filter.atTop (nhds (omegaState P (Tinf * B))) := by
    apply hω (fun k => T k * B) (Tinf * B) (C * ‖B‖)
    · exact fun k => mul_mem (hTkM k) hBM
    · exact mul_mem hinf hBM
    · intro k
      calc ‖T k * B‖ ≤ ‖T k‖ * ‖B‖ := ContinuousLinearMap.opNorm_comp_le _ _
        _ ≤ C * ‖B‖ := by
            have hk := hbd k
            have hB : (0:ℝ) ≤ ‖B‖ := norm_nonneg _
            nlinarith
    · intro ξ η
      exact hwot ξ (B η)
  have h2 : Filter.Tendsto (fun k => omegaState P (B * T k))
      Filter.atTop (nhds (omegaState P (B * Tinf))) := by
    apply hω (fun k => B * T k) (B * Tinf) (‖B‖ * C)
    · exact fun k => mul_mem hBM (hTkM k)
    · exact mul_mem hBM hinf
    · intro k
      calc ‖B * T k‖ ≤ ‖B‖ * ‖T k‖ := ContinuousLinearMap.opNorm_comp_le _ _
        _ ≤ ‖B‖ * C := by
            have hk := hbd k
            have hB : (0:ℝ) ≤ ‖B‖ := norm_nonneg _
            nlinarith
    · intro ξ η
      have hadj : ∀ (S : TowerHilbert P →L[ℂ] TowerHilbert P),
          (inner ℂ ξ ((B * S) η) : ℂ)
            = inner ℂ (ContinuousLinearMap.adjoint B ξ) (S η) := by
        intro S
        rw [show (B * S) η = B (S η) from rfl]
        rw [ContinuousLinearMap.adjoint_inner_left]
      simp only [hadj]
      exact hwot (ContinuousLinearMap.adjoint B ξ) η
  have heq : (fun k => omegaState P (T k * B))
      = (fun k => omegaState P (B * T k)) := by
    funext k
    exact (hmem k).2 B hBM
  rw [heq] at h1
  exact tendsto_nhds_unique h1 h2

/-! ## E — a refutação tipada: a diagonal NÃO sobrevive à degenerescência -/

/-- [KERNEL] ★★ **A REFUTAÇÃO DO TRANSPORTE INGÊNUO** (o presente do cético das
    rotas mortas): com pesos DEGENERADOS — exatamente o que o produto de Kronecker
    da torre produz do andar 2 em diante — a rotação racional 3-4-5 preserva o
    estado e TIRA a diagonal de si. O código diagonal não é o código do contínuo;
    o centralizador de ω é. -/
theorem the_diagonal_does_not_survive_degeneracy :
    ∃ V : Matrix (Fin 2) (Fin 2) ℂ,
      Vᴴ * V = 1 ∧
      V * rhoD (fun _ => (1 : ℝ) / 2) * Vᴴ = rhoD (fun _ => (1 : ℝ) / 2) ∧
      adU V (Matrix.diagonal ![1, 0]) ∉ diagCode (n := Fin 2) := by
  classical
  refine ⟨!![(3:ℂ)/5, -(4:ℂ)/5; (4:ℂ)/5, (3:ℂ)/5], ?_, ?_, ?_⟩
  · ext i j
    fin_cases i <;> fin_cases j <;>
      simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.conjTranspose_apply,
            Matrix.one_apply] <;>
      norm_num [Complex.conj_ofNat]
  · have hrho : rhoD (fun _ => (1 : ℝ) / 2)
        = ((1:ℂ)/2) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
      unfold rhoD
      ext i j
      by_cases hij : i = j
      · subst hij
        simp [Matrix.diagonal_apply_eq, Matrix.one_apply_eq, Matrix.smul_apply]
      · simp [Matrix.diagonal_apply_ne _ hij, Matrix.one_apply_ne hij,
              Matrix.smul_apply]
    rw [hrho, Matrix.mul_smul, Matrix.smul_mul, mul_one]
    congr 1
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.conjTranspose_apply,
            Matrix.one_apply] <;>
      norm_num [Complex.conj_ofNat]
  · intro hmem
    have hfix := mem_diagCode_iff.mp hmem
    have h01 : (adU !![(3:ℂ)/5, -(4:ℂ)/5; (4:ℂ)/5, (3:ℂ)/5]
        (Matrix.diagonal ![1, 0])) 0 1 = 12/25 := by
      unfold adU
      simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.conjTranspose_apply,
            Matrix.diagonal_apply, Matrix.vecMul, dotProduct,
            Matrix.vecHead, Matrix.vecTail,
            Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons]
      norm_num [Complex.conj_ofNat]
    have hdiag : (diagExpect (adU !![(3:ℂ)/5, -(4:ℂ)/5; (4:ℂ)/5, (3:ℂ)/5]
        (Matrix.diagonal ![1, 0]))) 0 1 = 0 := by
      unfold diagExpect
      exact Matrix.diagonal_apply_ne _ (by decide)
    rw [hfix, hdiag] at h01
    norm_num at h01

/-! ## F — o contrato da esperança (o TIPO antes do habitante) e o levantamento -/

variable (P)

/-- **O CONTRATO DA ESPERANÇA DE TAKESAKI** — o molde do `CommutationInput` (v282):
    a EXISTÊNCIA é a dívida importável [KNOWN, Takesaki 1972]. -/
structure ExpectationInput where
  E : (TowerHilbert P →L[ℂ] TowerHilbert P) → (TowerHilbert P →L[ℂ] TowerHilbert P)
  into : ∀ A ∈ theFactorObject P, E A ∈ omegaCentralizer P
  fixes : ∀ A ∈ omegaCentralizer P, E A = A
  ortho : ∀ A ∈ theFactorObject P, ∀ B ∈ omegaCentralizer P,
    omegaState P (star B * (A - E A)) = 0

variable {P}

/-- [KERNEL] a definitude GNS, paga pela separância: ω(A†A) = 0 com A ∈ M ⟹ A = 0. -/
theorem omega_definite {A : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hA : A ∈ theFactorObject P) (h0 : omegaState P (star A * A) = 0) : A = 0 := by
  have hinner : omegaState P (star A * A)
      = inner ℂ (A (hOmega P)) (A (hOmega P)) := by
    unfold omegaState
    rw [show (star A * A) (hOmega P)
        = ContinuousLinearMap.adjoint A (A (hOmega P)) from rfl]
    rw [ContinuousLinearMap.adjoint_inner_right]
  rw [hinner] at h0
  have hAΩ : A (hOmega P) = 0 := inner_self_eq_zero.mp h0
  exact factor_omega_separating hA hAΩ

/-- ω é aditivo em diferenças de operadores (conveniência). -/
theorem omegaState_sub (X Y : TowerHilbert P →L[ℂ] TowerHilbert P) :
    omegaState P (X - Y) = omegaState P X - omegaState P Y := by
  unfold omegaState
  rw [ContinuousLinearMap.sub_apply, inner_sub_right]

/-- [KERNEL] ★★★ **A UNICIDADE É DA CASA**: dois contratos coincidem sobre M. -/
theorem the_expectation_is_unique (I₁ I₂ : ExpectationInput P) :
    ∀ A ∈ theFactorObject P, I₁.E A = I₂.E A := by
  intro A hA
  have h1 : I₁.E A ∈ omegaCentralizer P := I₁.into A hA
  have h2 : I₂.E A ∈ omegaCentralizer P := I₂.into A hA
  have hD : I₁.E A - I₂.E A ∈ theFactorObject P := sub_mem h1.1 h2.1
  have hDc : I₁.E A - I₂.E A ∈ omegaCentralizer P := by
    refine ⟨hD, ?_⟩
    intro B hB
    have e1 := h1.2 B hB
    have e2 := h2.2 B hB
    rw [sub_mul, mul_sub, omegaState_sub, omegaState_sub, e1, e2]
  have hortho : omegaState P
      (star (I₁.E A - I₂.E A) * (I₁.E A - I₂.E A)) = 0 := by
    have hAmE1 := I₁.ortho A hA (I₁.E A - I₂.E A) hDc
    have hAmE2 := I₂.ortho A hA (I₁.E A - I₂.E A) hDc
    have hkey : omegaState P (star (I₁.E A - I₂.E A)
        * ((A - I₂.E A) - (A - I₁.E A)))
        = omegaState P (star (I₁.E A - I₂.E A) * (A - I₂.E A))
          - omegaState P (star (I₁.E A - I₂.E A) * (A - I₁.E A)) := by
      rw [mul_sub, omegaState_sub]
    rw [hAmE1, hAmE2, sub_zero] at hkey
    have hsimp : (A - I₂.E A) - (A - I₁.E A) = I₁.E A - I₂.E A := by abel
    rw [hsimp] at hkey
    exact hkey
  exact sub_eq_zero.mp (omega_definite hD hortho)

/-- o contrato transportado pelo horizonte (a peça da covariância). -/
def ExpectationInput.pullback (I : ExpectationInput P) (h : TowerHorizon P) :
    ExpectationInput P where
  E := fun A => adTinv h (I.E (adT h A))
  into := by
    intro A hA
    have h2 : I.E (adT h A) ∈ omegaCentralizer P := I.into _ (adT_mem h hA)
    have := horizon_preserves_centralizer h.inv _ h2
    rwa [adT_inv_eq] at this
  fixes := by
    intro A hA
    have h1 : adT h A ∈ omegaCentralizer P := horizon_preserves_centralizer h A hA
    rw [I.fixes _ h1, adTinv_adT]
  ortho := by
    intro A hA B hB
    have hAd : adT h A ∈ theFactorObject P := adT_mem h hA
    have hBd : adT h B ∈ omegaCentralizer P := horizon_preserves_centralizer h B hB
    have key := I.ortho (adT h A) hAd (adT h B) hBd
    have hexp : star (adT h B) * (adT h A - I.E (adT h A))
        = adT h (star B * (A - adTinv h (I.E (adT h A)))) := by
      rw [adT_mul, adT_sub, adT_star, adT_adTinv]
    rw [hexp] at key
    have hEm : adTinv h (I.E (adT h A)) ∈ theFactorObject P :=
      adTinv_mem h (I.into (adT h A) hAd).1
    have hZ : star B * (A - adTinv h (I.E (adT h A))) ∈ theFactorObject P :=
      mul_mem (star_mem hB.1) (sub_mem hA hEm)
    rw [omega_adT h hZ] at key
    exact key

/-- [KERNEL] ★★★★★ **O LEVANTAMENTO NA TORRE — a implicação do Lema 3 no contínuo**:
    contrato da esperança (a dívida importável, um campo) + horizonte ω-invariante
    (o axioma lido no horizonte) ⟹ a esperança é COVARIANTE sobre M. A prova é a
    da v143 com o produto GNS no lugar do de Frobenius — e a definitude paga pela
    separância. -/
theorem the_lift_on_the_tower (I : ExpectationInput P) (h : TowerHorizon P) :
    ∀ A ∈ theFactorObject P, adT h (I.E A) = I.E (adT h A) := by
  intro A hA
  have huniq := the_expectation_is_unique (I.pullback h) I A hA
  have hstep : adT h (adTinv h (I.E (adT h A))) = adT h (I.E A) := by
    show adT h ((I.pullback h).E A) = adT h (I.E A)
    rw [huniq]
  rw [adT_adTinv] at hstep
  exact hstep.symm

end

end TGLExt
