import TGLExt.TowerHilbert
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Topology.Algebra.LinearMapCompletion

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A PEDRA 85 — TowerAction: a torre AGE em B(H_φ) — π estendida, Ω cíclico
  [TGLExt — v131, Bloco A do PLANO_ULTIMA_FLAG, pedra 3 de 5]

A pedra 84 deu o Hilbert H_φ. Esta pedra dá a REPRESENTAÇÃO: cada elemento
x da torre age em H_φ como operador LIMITADO, e Ω é CÍCLICO:

* ★★ `lmul_bound_push` — O BOUND UNIFORME DE FROBENIUS: a multiplicação à
  esquerda por x (empurrado a QUALQUER andar) é limitada pela constante
  ‖x‖²_F do andar ORIGINAL — provado por indução de FATIAMENTO
  (`tInner_self_slice`: a norma do andar M+1 é a soma pesada das normas das
  fatias do andar M; `cSlice_towerStep_mul`: a fatia da ação de x⊗1 é a
  ação de x na fatia) — o passo que faz a constante NÃO crescer;
* ★★ `lmulCLM` — a multiplicação à esquerda como operador CONTÍNUO no
  pré-Hilbert (`LinearMap.mkContinuous`);
* ★★★ `towerPi` — A REPRESENTAÇÃO: π(x) ∈ B(H_φ) por extensão ao
  completamento (`ContinuousLinearMap.completion`); com
  `towerPi_compat` (π(empurrado) = π — a UNIÃO é dirigida),
  `towerPi_one` (π(1) = 1), `towerPi_mul` (π(xy) = π(x)π(y)),
  ★★★ `towerPi_star` (π(x†) = π(x)* — a representação é ESTRELADA:
  o adjunto de Hilbert realiza a estrela da torre);
* ★★★ `towerPi_omega` (π(x)Ω = [x]) e `towerPi_orbit_dense` — Ω É CÍCLICO:
  a órbita da torre sobre Ω é DENSA em H_φ — o vetor do Nome gera o espaço.

O QUE RESTA (pedras 86–87): o objeto M_TGL = (π(torre))'' e a assinatura.
β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Kronecker Matrix UniformSpace
open scoped ComplexConjugate

noncomputable section

variable {P : SiteProfile}

/-! ## A — a norma de Frobenius e a desigualdade de Cauchy–Schwarz por linha -/

/-- a norma de Frobenius ao quadrado. -/
def frobSq {N : ℕ} (x : Matrix (chainIdx N) (chainIdx N) ℂ) : ℝ :=
  ∑ j, ∑ i, Complex.normSq (x j i)

theorem frobSq_nonneg {N : ℕ} (x : Matrix (chainIdx N) (chainIdx N) ℂ) :
    0 ≤ frobSq x := by
  apply Finset.sum_nonneg
  intro j _
  apply Finset.sum_nonneg
  intro i _
  exact Complex.normSq_nonneg _

/-- Cauchy–Schwarz por linha: |Σ f·g|² ≤ (Σ|f|²)(Σ|g|²). -/
theorem normSq_sum_mul_le {ι : Type} [Fintype ι] (f g : ι → ℂ) :
    Complex.normSq (∑ i, f i * g i)
      ≤ (∑ i, Complex.normSq (f i)) * (∑ i, Complex.normSq (g i)) := by
  have h1 : ‖∑ i, f i * g i‖ ≤ ∑ i, ‖f i‖ * ‖g i‖ := by
    refine (norm_sum_le _ _).trans (le_of_eq ?_)
    refine Finset.sum_congr rfl fun i _ => ?_
    exact norm_mul _ _
  have h2 : (∑ i, ‖f i‖ * ‖g i‖) ^ 2
      ≤ (∑ i, ‖f i‖ ^ 2) * (∑ i, ‖g i‖ ^ 2) :=
    Finset.sum_mul_sq_le_sq_mul_sq _ _ _
  have h3 : ‖∑ i, f i * g i‖ ^ 2 ≤ (∑ i, ‖f i‖ ^ 2) * (∑ i, ‖g i‖ ^ 2) := by
    have hnn : (0 : ℝ) ≤ ∑ i, ‖f i‖ * ‖g i‖ := by
      apply Finset.sum_nonneg
      intro i _
      exact mul_nonneg (norm_nonneg _) (norm_nonneg _)
    calc ‖∑ i, f i * g i‖ ^ 2 ≤ (∑ i, ‖f i‖ * ‖g i‖) ^ 2 := by
          apply pow_le_pow_left₀ (norm_nonneg _) h1
      _ ≤ _ := h2
  calc Complex.normSq (∑ i, f i * g i) = ‖∑ i, f i * g i‖ ^ 2 :=
        Complex.normSq_eq_norm_sq _
    _ ≤ (∑ i, ‖f i‖ ^ 2) * (∑ i, ‖g i‖ ^ 2) := h3
    _ = (∑ i, Complex.normSq (f i)) * (∑ i, Complex.normSq (g i)) := by
        rw [Finset.sum_congr rfl (fun i _ => (Complex.normSq_eq_norm_sq (f i)).symm),
          Finset.sum_congr rfl (fun i _ => (Complex.normSq_eq_norm_sq (g i)).symm)]

/-! ## B — o bound do andar-base -/

/-- [KERNEL] ★ o bound no andar de origem: ‖x·c‖²_φ ≤ ‖x‖²_F·‖c‖²_φ. -/
theorem lmul_bound_base (P : SiteProfile) (N : ℕ)
    (x c : Matrix (chainIdx N) (chainIdx N) ℂ) :
    (tInner P N (x * c) (x * c)).re ≤ frobSq x * (tInner P N c c).re := by
  rw [tInner_self_eq, tInner_self_eq, Complex.ofReal_re, Complex.ofReal_re,
    Finset.mul_sum]
  apply Finset.sum_le_sum
  intro k _
  rw [← mul_assoc, mul_comm (frobSq x) (towerW P N k), mul_assoc]
  apply mul_le_mul_of_nonneg_left _ (le_of_lt (towerW_pos P N k))
  calc ∑ j, Complex.normSq ((x * c) j k)
      ≤ ∑ j, (∑ i, Complex.normSq (x j i)) * (∑ i, Complex.normSq (c i k)) := by
        apply Finset.sum_le_sum
        intro j _
        rw [show (x * c) j k = ∑ i, x j i * c i k from Matrix.mul_apply]
        exact normSq_sum_mul_le _ _
    _ = (∑ j, ∑ i, Complex.normSq (x j i)) * (∑ i, Complex.normSq (c i k)) :=
        (Finset.sum_mul _ _ _).symm
    _ = frobSq x * ∑ i, Complex.normSq (c i k) := rfl

/-! ## C — o fatiamento: a chave da uniformidade -/

/-- a fatia (t,s) de uma matriz do andar M+1. -/
def cSlice {M : ℕ} (t s : Fin 2)
    (c : Matrix (chainIdx (M + 1)) (chainIdx (M + 1)) ℂ) :
    Matrix (chainIdx M) (chainIdx M) ℂ :=
  Matrix.of fun i k => c (i, t) (k, s)

theorem cSlice_apply {M : ℕ} (t s : Fin 2)
    (c : Matrix (chainIdx (M + 1)) (chainIdx (M + 1)) ℂ)
    (i k : chainIdx M) : cSlice t s c i k = c (i, t) (k, s) := rfl

/-- [KERNEL] ★ a fatia da ação de y⊗1 é a ação de y na fatia. -/
theorem cSlice_towerStep_mul {M : ℕ} (t s : Fin 2)
    (y : Matrix (chainIdx M) (chainIdx M) ℂ)
    (c : Matrix (chainIdx (M + 1)) (chainIdx (M + 1)) ℂ) :
    cSlice t s (towerStep y * c) = y * cSlice t s c := by
  ext j k
  rw [cSlice_apply, Matrix.mul_apply, Matrix.mul_apply]
  rw [Fintype.sum_prod_type]
  have h : ∀ i : chainIdx M,
      ∑ u : Fin 2, towerStep y (j, t) (i, u) * c (i, u) (k, s)
        = y j i * cSlice t s c i k := by
    intro i
    have hstep : ∀ u : Fin 2, towerStep y (j, t) (i, u)
        = y j i * (if t = u then 1 else 0) := by
      intro u
      unfold towerStep
      rw [kroneckerMap_apply, Matrix.one_apply]
    rw [Finset.sum_congr rfl (fun u _ => by rw [hstep u])]
    rw [Finset.sum_congr rfl (fun u _ => by
      rw [mul_assoc, ite_mul, one_mul, zero_mul, mul_ite, mul_zero])]
    rw [Finset.sum_ite_eq]
    rw [if_pos (Finset.mem_univ t)]
    rw [cSlice_apply]
  exact Finset.sum_congr rfl (fun i _ => h i)

/-- [KERNEL] ★★ O FATIAMENTO DA NORMA: a norma-φ do andar M+1 é a soma
    pesada (pelos pesos do sítio novo) das normas-φ das fatias do andar M. -/
theorem tInner_self_slice (P : SiteProfile) {M : ℕ}
    (c : Matrix (chainIdx (M + 1)) (chainIdx (M + 1)) ℂ) :
    (tInner P (M + 1) c c).re
      = ∑ s : Fin 2, ∑ t : Fin 2, siteW (P.w (M + 1)) s
          * (tInner P M (cSlice t s c) (cSlice t s c)).re := by
  rw [tInner_self_eq, Complex.ofReal_re]
  have hW : ∀ (k : chainIdx M) (s : Fin 2),
      towerW P (M + 1) (k, s) = towerW P M k * siteW (P.w (M + 1)) s := by
    intro k s
    rfl
  rw [Fintype.sum_prod_type]
  have hinner : ∀ (k : chainIdx M) (s : Fin 2),
      towerW P (M + 1) (k, s) * ∑ p, Complex.normSq (c p (k, s))
        = siteW (P.w (M + 1)) s * ∑ t : Fin 2,
            towerW P M k * ∑ j, Complex.normSq (cSlice t s c j k) := by
    intro k s
    rw [hW, Fintype.sum_prod_type]
    rw [show (∑ j : chainIdx M, ∑ t : Fin 2, Complex.normSq (c (j, t) (k, s)))
        = ∑ t : Fin 2, ∑ j : chainIdx M, Complex.normSq (cSlice t s c j k) from
      Finset.sum_comm]
    rw [Finset.mul_sum, Finset.mul_sum]
    exact Finset.sum_congr rfl fun t _ => by ring
  rw [Finset.sum_congr rfl (fun k _ => Finset.sum_congr rfl
    (fun s _ => hinner k s))]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun s _ => ?_
  rw [← Finset.mul_sum, Finset.sum_comm, Finset.mul_sum]
  refine Finset.sum_congr rfl fun t _ => ?_
  congr 1
  rw [tInner_self_eq, Complex.ofReal_re]

/-- [KERNEL] ★★ O BOUND UNIFORME: a multiplicação à esquerda pelo x
    EMPURRADO é limitada pela Frobenius do andar ORIGINAL — a constante
    não cresce ao subir a torre (indução de fatiamento). -/
theorem lmul_bound_push (P : SiteProfile) {N : ℕ}
    (x : Matrix (chainIdx N) (chainIdx N) ℂ) :
    ∀ {M : ℕ} (h : N ≤ M) (c : Matrix (chainIdx M) (chainIdx M) ℂ),
      (tInner P M (tPush h x * c) (tPush h x * c)).re
        ≤ frobSq x * (tInner P M c c).re := by
  intro M h
  induction M, h using Nat.le_induction with
  | base =>
      intro c
      rw [tPush_self]
      exact lmul_bound_base P N x c
  | succ M hM ih =>
      intro c
      rw [tPush_succ hM (hM.trans (Nat.le_succ M))]
      rw [tInner_self_slice P (towerStep (tPush hM x) * c), tInner_self_slice P c]
      rw [Finset.mul_sum]
      apply Finset.sum_le_sum
      intro s _
      rw [Finset.mul_sum]
      apply Finset.sum_le_sum
      intro t _
      rw [cSlice_towerStep_mul]
      have hσ : 0 ≤ siteW (P.w (M + 1)) s :=
        le_of_lt (siteW_pos (P.pos (M + 1)) (P.lt_one (M + 1)) s)
      calc siteW (P.w (M + 1)) s
            * (tInner P M (tPush hM x * cSlice t s c)
                (tPush hM x * cSlice t s c)).re
          ≤ siteW (P.w (M + 1)) s
              * (frobSq x * (tInner P M (cSlice t s c) (cSlice t s c)).re) :=
            mul_le_mul_of_nonneg_left (ih (cSlice t s c)) hσ
        _ = frobSq x * (siteW (P.w (M + 1)) s
              * (tInner P M (cSlice t s c) (cSlice t s c)).re) := by ring

/-! ## D — a multiplicação à esquerda no colimite -/

/-- a multiplicação à esquerda por x (andar N) no colimite. -/
def lmulPre (P : SiteProfile) {N : ℕ}
    (x : Matrix (chainIdx N) (chainIdx N) ℂ) :
    TowerPre P → TowerPre P :=
  Quotient.map
    (fun q => ⟨N ⊔ q.1, tPush le_sup_left x * tPush le_sup_right q.2⟩)
    (by
      rintro q q' hq
      have hK : (N ⊔ q.1) ≤ (N ⊔ q.1) ⊔ (N ⊔ q'.1) := le_sup_left
      have hK' : (N ⊔ q'.1) ≤ (N ⊔ q.1) ⊔ (N ⊔ q'.1) := le_sup_right
      have eq := (towerEqv_iff (x := q) (y := q')
        (K := (N ⊔ q.1) ⊔ (N ⊔ q'.1))
        (le_sup_right.trans hK) (le_sup_right.trans hK')).mp hq
      refine (towerEqv_iff hK hK').mpr ?_
      show tPush hK (tPush le_sup_left x * tPush le_sup_right q.2)
        = tPush hK' (tPush le_sup_left x * tPush le_sup_right q'.2)
      rw [tPush_mul, tPush_mul, tPush_trans, tPush_trans, tPush_trans,
        tPush_trans, eq])

theorem lmulPre_tof_at {N M K : ℕ} (hN : N ≤ K) (hM : M ≤ K)
    (x : Matrix (chainIdx N) (chainIdx N) ℂ)
    (b : Matrix (chainIdx M) (chainIdx M) ℂ) :
    lmulPre P x (tof P M b) = tof P K (tPush hN x * tPush hM b) := by
  show tof P (N ⊔ M) (tPush le_sup_left x * tPush le_sup_right b)
    = tof P K (tPush hN x * tPush hM b)
  have hs : N ⊔ M ≤ (N ⊔ M) ⊔ K := le_sup_left
  have hk : K ≤ (N ⊔ M) ⊔ K := le_sup_right
  rw [tof_eq_iff hs hk]
  rw [tPush_mul, tPush_mul, tPush_trans, tPush_trans, tPush_trans, tPush_trans]

/-- π no pré-nível é COMPATÍVEL com o empurrão: a torre age como UNIÃO. -/
theorem lmulPre_compat {N M : ℕ} (h : N ≤ M)
    (x : Matrix (chainIdx N) (chainIdx N) ℂ) (v : TowerPre P) :
    lmulPre P (tPush h x) v = lmulPre P x v := by
  obtain ⟨M', b, rfl⟩ := exists_tof v
  have hM : M ≤ M ⊔ M' := le_sup_left
  have hM' : M' ≤ M ⊔ M' := le_sup_right
  have hN : N ≤ M ⊔ M' := h.trans hM
  rw [lmulPre_tof_at hM hM', lmulPre_tof_at hN hM', tPush_trans]

/-- a multiplicação à esquerda é LINEAR no colimite. -/
def lmulLin (P : SiteProfile) {N : ℕ}
    (x : Matrix (chainIdx N) (chainIdx N) ℂ) :
    TowerPre P →ₗ[ℂ] TowerPre P where
  toFun := lmulPre P x
  map_add' := by
    intro v w
    obtain ⟨A, a, rfl⟩ := exists_tof v
    obtain ⟨B, b, rfl⟩ := exists_tof w
    have hA : A ≤ A ⊔ B := le_sup_left
    have hB : B ≤ A ⊔ B := le_sup_right
    have hN : N ≤ N ⊔ (A ⊔ B) := le_sup_left
    have hAB : A ⊔ B ≤ N ⊔ (A ⊔ B) := le_sup_right
    rw [tof_add_at hA hB, lmulPre_tof_at hN hAB,
      lmulPre_tof_at hN (hA.trans hAB), lmulPre_tof_at hN (hB.trans hAB),
      tof_add_at (le_refl (N ⊔ (A ⊔ B))) (le_refl (N ⊔ (A ⊔ B))),
      tPush_self, tPush_self, tPush_add, mul_add, tPush_trans, tPush_trans]
  map_smul' := by
    intro c v
    obtain ⟨A, a, rfl⟩ := exists_tof v
    have hN : N ≤ N ⊔ A := le_sup_left
    have hA : A ≤ N ⊔ A := le_sup_right
    rw [RingHom.id_apply, tof_smul, lmulPre_tof_at hN hA,
      lmulPre_tof_at hN hA, tof_smul, tPush_smul, mul_smul_comm]

/-- a norma do colimite em coordenadas de andar. -/
theorem norm_tof_sq (K : ℕ) (z : Matrix (chainIdx K) (chainIdx K) ℂ) :
    ‖tof P K z‖ ^ 2 = (tInner P K z z).re := by
  rw [norm_sq_eq_re_inner (𝕜 := ℂ) (tof P K z)]
  rw [show (inner ℂ (tof P K z) (tof P K z) : ℂ) = tInner P K z z from
    innerPre_tof_same K z z]
  rfl

/-- [KERNEL] ★★ A CONTINUIDADE: ‖x·v‖ ≤ ‖x‖_F·‖v‖ em TODO o colimite. -/
theorem lmulPre_norm_le {N : ℕ} (x : Matrix (chainIdx N) (chainIdx N) ℂ)
    (v : TowerPre P) :
    ‖lmulPre P x v‖ ≤ Real.sqrt (frobSq x) * ‖v‖ := by
  obtain ⟨M, b, rfl⟩ := exists_tof v
  have hN : N ≤ N ⊔ M := le_sup_left
  have hM : M ≤ N ⊔ M := le_sup_right
  set K := N ⊔ M
  set b' := tPush hM b with hb'
  have hv : tof P M b = tof P K b' := (tof_tPush hM b).symm
  rw [hv, lmulPre_tof_at hN (le_refl K), tPush_self]
  have hsq : ‖tof P K (tPush hN x * b')‖ ^ 2
      ≤ frobSq x * ‖tof P K b'‖ ^ 2 := by
    rw [norm_tof_sq, norm_tof_sq]
    exact lmul_bound_push P x hN b'
  have h1 : ‖tof P K (tPush hN x * b')‖
      = Real.sqrt (‖tof P K (tPush hN x * b')‖ ^ 2) :=
    (Real.sqrt_sq (norm_nonneg _)).symm
  rw [h1]
  calc Real.sqrt (‖tof P K (tPush hN x * b')‖ ^ 2)
      ≤ Real.sqrt (frobSq x * ‖tof P K b'‖ ^ 2) := Real.sqrt_le_sqrt hsq
    _ = Real.sqrt (frobSq x) * Real.sqrt (‖tof P K b'‖ ^ 2) :=
        Real.sqrt_mul (frobSq_nonneg x) _
    _ = Real.sqrt (frobSq x) * ‖tof P K b'‖ := by
        rw [Real.sqrt_sq (norm_nonneg _)]

/-- ★★ a multiplicação à esquerda como operador CONTÍNUO no pré-Hilbert. -/
def lmulCLM (P : SiteProfile) {N : ℕ}
    (x : Matrix (chainIdx N) (chainIdx N) ℂ) :
    TowerPre P →L[ℂ] TowerPre P :=
  LinearMap.mkContinuous (lmulLin P x) (Real.sqrt (frobSq x))
    (fun v => lmulPre_norm_le x v)

theorem lmulCLM_apply {N : ℕ} (x : Matrix (chainIdx N) (chainIdx N) ℂ)
    (v : TowerPre P) : lmulCLM P x v = lmulPre P x v := rfl

/-! ## E — A REPRESENTAÇÃO π em B(H_φ) -/

/-- ★★★ π(x): a ação de x ∈ torre como operador limitado de H_φ. -/
def towerPi (P : SiteProfile) {N : ℕ}
    (x : Matrix (chainIdx N) (chainIdx N) ℂ) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  (lmulCLM P x).completion

theorem towerPi_coe {N : ℕ} (x : Matrix (chainIdx N) (chainIdx N) ℂ)
    (v : TowerPre P) :
    towerPi P x (v : TowerHilbert P) = ((lmulPre P x v : TowerPre P) : TowerHilbert P) :=
  ContinuousLinearMap.completion_apply_coe _ _

/-- [KERNEL] ★★ π é COMPATÍVEL com o empurrão: π(tPush h x) = π(x) — a
    torre age em H_φ como UNIÃO DIRIGIDA de andares. -/
theorem towerPi_compat {N M : ℕ} (h : N ≤ M)
    (x : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P (tPush h x) = towerPi P x := by
  ext c
  induction c using Completion.induction_on with
  | hp => apply isClosed_eq <;> fun_prop
  | ih c => rw [towerPi_coe, towerPi_coe, lmulPre_compat h x c]

/-- [KERNEL] ★ π(1) = 1: a representação é UNITAL. -/
theorem towerPi_one (N : ℕ) :
    towerPi P (1 : Matrix (chainIdx N) (chainIdx N) ℂ) = 1 := by
  ext c
  induction c using Completion.induction_on with
  | hp => apply isClosed_eq <;> fun_prop
  | ih c =>
      rw [towerPi_coe]
      obtain ⟨M, b, rfl⟩ := exists_tof c
      have hN : N ≤ N ⊔ M := le_sup_left
      have hM : M ≤ N ⊔ M := le_sup_right
      rw [lmulPre_tof_at hN hM, tPush_one, one_mul, tof_tPush]
      rfl

/-- [KERNEL] ★★ π(x·y) = π(x)·π(y): a representação é MULTIPLICATIVA. -/
theorem towerPi_mul (N : ℕ)
    (x y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P (x * y) = towerPi P x * towerPi P y := by
  ext c
  induction c using Completion.induction_on with
  | hp => apply isClosed_eq <;> fun_prop
  | ih c =>
      obtain ⟨M, b, rfl⟩ := exists_tof c
      have hN : N ≤ N ⊔ M := le_sup_left
      have hM : M ≤ N ⊔ M := le_sup_right
      show towerPi P (x * y) ((tof P M b : TowerPre P) : TowerHilbert P)
        = towerPi P x (towerPi P y ((tof P M b : TowerPre P) : TowerHilbert P))
      rw [towerPi_coe, towerPi_coe, towerPi_coe]
      rw [lmulPre_tof_at hN hM, lmulPre_tof_at hN hM,
        lmulPre_tof_at hN (le_refl (N ⊔ M)), tPush_self, tPush_mul, mul_assoc]

/-- a identidade de adjunção por andar: ⟨z·a, b⟩ = ⟨a, z†·b⟩. -/
theorem tInner_mul_left_adjoint (P : SiteProfile) (K : ℕ)
    (z a b : Matrix (chainIdx K) (chainIdx K) ℂ) :
    tInner P K (z * a) b = tInner P K a (zᴴ * b) := by
  unfold tInner
  rw [conjTranspose_mul, mul_assoc]

/-- [KERNEL] ★★★ π(x†) = π(x)*: a representação é ESTRELADA — o adjunto
    de Hilbert realiza a estrela da torre. -/
theorem towerPi_star (N : ℕ) (x : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P xᴴ = ContinuousLinearMap.adjoint (towerPi P x) := by
  refine ((ContinuousLinearMap.eq_adjoint_iff _ _).mpr ?_)
  intro u v
  induction u, v using Completion.induction_on₂ with
  | hp => apply isClosed_eq <;> fun_prop
  | ih u v =>
      rw [towerPi_coe, towerPi_coe, Completion.inner_coe, Completion.inner_coe]
      obtain ⟨A, a, rfl⟩ := exists_tof u
      obtain ⟨B, b, rfl⟩ := exists_tof v
      have hN : N ≤ N ⊔ A ⊔ B := le_sup_left.trans le_sup_left
      have hA : A ≤ N ⊔ A ⊔ B := le_sup_right.trans le_sup_left
      have hB : B ≤ N ⊔ A ⊔ B := le_sup_right
      show innerPre P (lmulPre P xᴴ (tof P A a)) (tof P B b)
        = innerPre P (tof P A a) (lmulPre P x (tof P B b))
      rw [lmulPre_tof_at hN hA, lmulPre_tof_at hN hB,
        innerPre_tof_at (le_refl (N ⊔ A ⊔ B)) hB, tPush_self,
        innerPre_tof_at hA (le_refl (N ⊔ A ⊔ B)), tPush_self,
        tPush_star, tInner_mul_left_adjoint, conjTranspose_conjTranspose]

/-- [KERNEL] ★★★ π(x)Ω = [x]: a órbita do Nome é a própria torre. -/
theorem towerPi_omega (N : ℕ) (x : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P x (hOmega P) = ((tof P N x : TowerPre P) : TowerHilbert P) := by
  unfold hOmega
  rw [show towerOmega P = tof P 0 1 from rfl, towerPi_coe]
  congr 1
  rw [lmulPre_tof_at (le_refl N) (Nat.zero_le N), tPush_self, tPush_one,
    mul_one]

/-- [KERNEL] ★★★ Ω É CÍCLICO: a órbita da torre sobre Ω é DENSA em H_φ —
    o vetor do Nome gera o espaço do fator inteiro. -/
theorem towerPi_orbit_dense :
    DenseRange (fun p : TowerPt => towerPi P p.2 (hOmega P)) := by
  have hr : Set.range (fun p : TowerPt => towerPi P p.2 (hOmega P))
      = Set.range ((↑) : TowerPre P → TowerHilbert P) := by
    ext z
    constructor
    · rintro ⟨⟨N, x⟩, rfl⟩
      exact ⟨tof P N x, (towerPi_omega N x).symm⟩
    · rintro ⟨v, rfl⟩
      obtain ⟨N, a, rfl⟩ := exists_tof v
      exact ⟨⟨N, a⟩, towerPi_omega N a⟩
  have hd : DenseRange ((↑) : TowerPre P → TowerHilbert P) :=
    towerPre_denseRange
  unfold DenseRange at hd ⊢
  rw [hr]
  exact hd

end

end TGLExt
