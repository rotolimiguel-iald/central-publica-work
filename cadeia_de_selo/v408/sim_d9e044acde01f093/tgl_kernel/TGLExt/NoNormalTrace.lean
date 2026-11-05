import TGLExt.SignatureInTheLimit

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A PEDRA 88 — NoNormalTrace: o assassinato do peso normal no objeto
  [TGLExt — v132, Bloco B do PLANO_ULTIMA_FLAG, pedra 1 de 3]

A pedra 86 cunhou M_TGL; a 87 pôs a assinatura dentro dele. Esta pedra mata
o traço normal DENTRO do objeto completado — a propriedade que o programa
adotou como definição operacional da parede ("matar também o peso", v119/v120):

* `SeqWOTContinuous` — a continuidade WOT-sequencial em sequências limitadas
  de M: a normalidade genuína (σ-fraca) IMPLICA esta propriedade; matá-la
  para todos os traços mata todo traço normal — o teorema fica MAIS FORTE;
* ★ `omegaState_seqWOT` — ω É normal neste sentido: a noção NÃO é vácua no
  objeto (a definição morde só o traço — honestidade estrutural);
* `qMark`/`qMark'`/`uMark` — as marcas de sítio: projeções 1⊗E₀₀, 1⊗E₁₁ e a
  isometria parcial 1⊗E₀₁ que as conjuga; ★ `qMark_partition` — q + q' = 1;
* ★★ `towerPi_qMark_le` — π(marca) é CONTRAÇÃO (projeção: ‖π(q)ξ‖ ≤ ‖ξ‖);
* ★★ `inner_qMark_exact` — A FATORIZAÇÃO EXATA: nos vetores da torre,
  ⟨u, π(q_N) v⟩ = μ_{N+1}·⟨u,v⟩ assim que o sítio marcado passa dos andares
  de u e v — o estado-produto não mistura sítios;
* ★★★ `qMark_wot` — AS MARCAS CONVERGEM WOT A μ·1: exatidão na torre densa
  + contração uniforme ⟹ ⟨ξ, π(q_{s k})η⟩ → μ·⟨ξ,η⟩ em TODO H_φ;
* ★★ `tracial_halves_qMark` — A MEAÇÃO: todo funcional tracial no fator
  divide a marca ao meio — τ(π q) = τ(π q') e q+q'=1 ⟹ τ(π q) = ½;
* ★★★ `no_normal_tracial_state_seq` — O ASSASSINATO: μ ≠ ½ ⟹ NENHUM
  funcional tracial normalizado sobre M_TGL é WOT-sequencialmente contínuo —
  a meação diz ½, o limite diz μ, e o kernel recusa a contradição;
* ★★★ `no_normal_tracial_state_mix` — no OBJETO DA MARCA LOG-DENSA
  (perfil ⅓,¼): M_TGL(⅓,¼) não tem estado tracial normal — o mesmo objeto
  que realiza a S-invariante densa mata o peso;
* ★★ `no_normal_tracial_state_const` — na escada constante (l ≠ 1): III_λ.

HONESTIDADE (nomeada, sem véu): "sem estado tracial normal" NÃO é ainda
"fator III₁ pleno" (centro trivial e ausência de PESO semifinito ilimitado
seguem o programa); é exatamente a definição operacional que o próprio
programa selou ("o único traço é zero" + a marca densa + o objeto). O gate
NÃO se move por esta pedra. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Kronecker Matrix UniformSpace Filter Topology
open scoped ComplexConjugate

noncomputable section

variable {P : SiteProfile}

/-! ## A — a normalidade sequencial (a definição que a régua permite) -/

/-- [DEF] continuidade WOT-sequencial em sequências limitadas de M. A
    normalidade genuína (σ-fraca) implica esta propriedade em qualquer
    álgebra de von Neumann; portanto "nenhum τ com esta propriedade"
    é um teorema MAIS FORTE que "nenhum τ normal". -/
def SeqWOTContinuous {FH : Type} [NormedAddCommGroup FH]
    [InnerProductSpace ℂ FH] [CompleteSpace FH]
    (M : VonNeumannAlgebra FH) (τ : (FH →L[ℂ] FH) → ℂ) : Prop :=
  ∀ (T : ℕ → FH →L[ℂ] FH) (Tinf : FH →L[ℂ] FH) (C : ℝ),
    (∀ k, T k ∈ M) → Tinf ∈ M → (∀ k, ‖T k‖ ≤ C) →
    (∀ ξ η : FH, Tendsto (fun k => (inner ℂ ξ (T k η) : ℂ)) atTop
      (nhds (inner ℂ ξ (Tinf η)))) →
    Tendsto (fun k => τ (T k)) atTop (nhds (τ Tinf))

/-- [KERNEL] ★ ω É NORMAL NESTE SENTIDO: o estado vetorial do Nome satisfaz
    a continuidade WOT-sequencial — a noção não é vácua no objeto. -/
theorem omegaState_seqWOT (P : SiteProfile) :
    SeqWOTContinuous (theFactorObject P) (omegaState P) := by
  intro T Tinf C _ _ _ hwot
  exact hwot (hOmega P) (hOmega P)

/-! ## B — as marcas de sítio e suas leis -/

/-- a marca do sítio N+1: a projeção 1 ⊗ E₀₀ no andar N+1. -/
def qMark (N : ℕ) : Matrix (chainIdx (N + 1)) (chainIdx (N + 1)) ℂ :=
  (1 : Matrix (chainIdx N) (chainIdx N) ℂ) ⊗ₖ Matrix.single 0 0 1

/-- a marca complementar: 1 ⊗ E₁₁. -/
def qMark' (N : ℕ) : Matrix (chainIdx (N + 1)) (chainIdx (N + 1)) ℂ :=
  (1 : Matrix (chainIdx N) (chainIdx N) ℂ) ⊗ₖ Matrix.single 1 1 1

/-- a isometria parcial que conjuga as duas: 1 ⊗ E₀₁. -/
def uMark (N : ℕ) : Matrix (chainIdx (N + 1)) (chainIdx (N + 1)) ℂ :=
  (1 : Matrix (chainIdx N) (chainIdx N) ℂ) ⊗ₖ Matrix.single 0 1 1

theorem single_one_conjT {i j : Fin 2} :
    (Matrix.single i j (1 : ℂ))ᴴ = Matrix.single j i 1 := by
  ext a b
  rw [Matrix.conjTranspose_apply, Matrix.single_apply, Matrix.single_apply]
  by_cases h : i = b ∧ j = a
  · rw [if_pos h, if_pos ⟨h.2, h.1⟩, star_one]
  · rw [if_neg h, if_neg fun hc => h ⟨hc.2, hc.1⟩, star_zero]

/-- [KERNEL] ★ a marca é auto-adjunta. -/
theorem qMark_star (N : ℕ) : (qMark N)ᴴ = qMark N := by
  unfold qMark
  rw [conjTranspose_kronecker, conjTranspose_one, single_one_conjT]

/-- [KERNEL] ★ a marca é idempotente: uma PROJEÇÃO genuína. -/
theorem qMark_mul_self (N : ℕ) : qMark N * qMark N = qMark N := by
  unfold qMark
  rw [← Matrix.mul_kronecker_mul, one_mul, Matrix.single_mul_single_same,
    one_mul]

/-- [KERNEL] ★ u·u† = q: a isometria parcial aterrissa na marca. -/
theorem uMark_mul_star (N : ℕ) : uMark N * (uMark N)ᴴ = qMark N := by
  unfold uMark qMark
  rw [conjTranspose_kronecker, conjTranspose_one, single_one_conjT,
    ← Matrix.mul_kronecker_mul, one_mul, Matrix.single_mul_single_same,
    one_mul]

/-- [KERNEL] ★ u†·u = q': a mesma isometria parte da complementar. -/
theorem star_mul_uMark (N : ℕ) : (uMark N)ᴴ * uMark N = qMark' N := by
  unfold uMark qMark'
  rw [conjTranspose_kronecker, conjTranspose_one, single_one_conjT,
    ← Matrix.mul_kronecker_mul, one_mul, Matrix.single_mul_single_same,
    one_mul]

theorem single_zero_add_single_one :
    Matrix.single (0 : Fin 2) 0 (1 : ℂ) + Matrix.single 1 1 1
      = (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  ext a b
  fin_cases a <;> fin_cases b <;>
    simp [Matrix.single_apply, Matrix.one_apply]

/-- [KERNEL] ★ A PARTIÇÃO: q + q' = 1 — as duas faces do sítio somam o Um. -/
theorem qMark_partition (N : ℕ) :
    qMark N + qMark' N
      = (1 : Matrix (chainIdx (N + 1)) (chainIdx (N + 1)) ℂ) := by
  unfold qMark qMark'
  rw [← Matrix.kronecker_add, single_zero_add_single_one,
    Matrix.one_kronecker_one]

/-! ## C — π é aditiva e homogênea (as leis que faltavam) -/

/-- [KERNEL] ★ π(x+y) = π(x)+π(y): a representação é ADITIVA. -/
theorem towerPi_add {N : ℕ} (x y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P (x + y) = towerPi P x + towerPi P y := by
  ext c
  rw [ContinuousLinearMap.add_apply]
  induction c using Completion.induction_on with
  | hp => apply isClosed_eq <;> fun_prop
  | ih c =>
      obtain ⟨M, b, rfl⟩ := exists_tof c
      have hN : N ≤ N ⊔ M := le_sup_left
      have hM : M ≤ N ⊔ M := le_sup_right
      rw [towerPi_coe, towerPi_coe, towerPi_coe,
        lmulPre_tof_at hN hM, lmulPre_tof_at hN hM, lmulPre_tof_at hN hM,
        tPush_add, add_mul, ← tof_add_same, Completion.coe_add]

/-- [KERNEL] ★ π(c·x) = c·π(x): a representação é HOMOGÊNEA. -/
theorem towerPi_smul {N : ℕ} (c : ℂ)
    (x : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P (c • x) = c • towerPi P x := by
  ext v
  rw [ContinuousLinearMap.smul_apply]
  induction v using Completion.induction_on with
  | hp => apply isClosed_eq <;> fun_prop
  | ih v =>
      obtain ⟨M, b, rfl⟩ := exists_tof v
      have hN : N ≤ N ⊔ M := le_sup_left
      have hM : M ≤ N ⊔ M := le_sup_right
      rw [towerPi_coe, towerPi_coe,
        lmulPre_tof_at hN hM, lmulPre_tof_at hN hM,
        tPush_smul, smul_mul_assoc, ← tof_smul, Completion.coe_smul]

/-! ## D — a contração da projeção -/

/-- [KERNEL] ★ toda projeção da torre age como CONTRAÇÃO no colimite:
    ‖p·v‖² = Re⟨v, p·v⟩ ≤ ‖v‖·‖p·v‖ (Cauchy–Schwarz do pré-Hilbert). -/
theorem lmulPre_proj_le {F : ℕ} {p : Matrix (chainIdx F) (chainIdx F) ℂ}
    (hst : pᴴ = p) (hid : p * p = p) (v : TowerPre P) :
    ‖lmulPre P p v‖ ≤ ‖v‖ := by
  obtain ⟨B, b, rfl⟩ := exists_tof v
  have hF : F ≤ F ⊔ B := le_sup_left
  have hB : B ≤ F ⊔ B := le_sup_right
  rw [lmulPre_tof_at hF hB]
  set K := F ⊔ B with hK
  set p' := tPush hF p with hp'
  set b' := tPush hB b with hb'
  have hst' : p'ᴴ = p' := by rw [hp', ← tPush_star, hst]
  have hid' : p' * p' = p' := by rw [hp', ← tPush_mul, hid]
  have hvb : (tof P B b : TowerPre P) = tof P K b' := by
    rw [hb', tof_tPush]
  rw [hvb]
  have hsq : ‖(tof P K (p' * b') : TowerPre P)‖ ^ 2
      = (tInner P K b' (p' * b')).re := by
    rw [norm_tof_sq]
    congr 1
    unfold tInner
    rw [conjTranspose_mul, hst', mul_assoc, ← mul_assoc p' p' b', hid']
  have hcs : (tInner P K b' (p' * b')).re
      ≤ ‖(tof P K b' : TowerPre P)‖ * ‖(tof P K (p' * b') : TowerPre P)‖ := by
    have h1 : (tInner P K b' (p' * b')).re ≤ ‖tInner P K b' (p' * b')‖ :=
      Complex.re_le_norm _
    have h2 : ‖tInner P K b' (p' * b')‖
        ≤ ‖(tof P K b' : TowerPre P)‖ * ‖(tof P K (p' * b') : TowerPre P)‖ := by
      rw [← innerPre_tof_same, ← towerPre_inner_def]
      exact norm_inner_le_norm _ _
    exact le_trans h1 h2
  set nw : ℝ := ‖(tof P K (p' * b') : TowerPre P)‖ with hnw
  set nv : ℝ := ‖(tof P K b' : TowerPre P)‖ with hnv
  have hnw0 : 0 ≤ nw := norm_nonneg _
  have hnv0 : 0 ≤ nv := norm_nonneg _
  have hkey : nw ^ 2 ≤ nv * nw := le_trans (le_of_eq hsq) hcs
  rcases eq_or_lt_of_le hnw0 with h0 | h0
  · rw [← h0]; exact hnv0
  · have : nw * nw ≤ nv * nw := by
      calc nw * nw = nw ^ 2 := (sq nw).symm
        _ ≤ nv * nw := hkey
    exact le_of_mul_le_mul_right this h0

/-- [KERNEL] ★★ a contração sobe ao completamento: ‖π(p)ξ‖ ≤ ‖ξ‖. -/
theorem towerPi_proj_le {F : ℕ} {p : Matrix (chainIdx F) (chainIdx F) ℂ}
    (hst : pᴴ = p) (hid : p * p = p) (ξ : TowerHilbert P) :
    ‖towerPi P p ξ‖ ≤ ‖ξ‖ := by
  induction ξ using Completion.induction_on with
  | hp => exact isClosed_le (by fun_prop) (by fun_prop)
  | ih v =>
      rw [towerPi_coe, Completion.norm_coe, Completion.norm_coe]
      exact lmulPre_proj_le hst hid v

/-- [KERNEL] ★★ π(marca) é contração. -/
theorem towerPi_qMark_le (N : ℕ) (ξ : TowerHilbert P) :
    ‖towerPi P (qMark N) ξ‖ ≤ ‖ξ‖ :=
  towerPi_proj_le (qMark_star N) (qMark_mul_self N) ξ

/-! ## E — a fatorização exata nos vetores da torre -/

/-- [KERNEL] ★★ A FATORIZAÇÃO EXATA: assim que o sítio marcado (N+1) passa
    dos andares de u e v, ⟨u, π(q_N) v⟩ = μ_{N+1}·⟨u,v⟩ EXATAMENTE — o
    estado-produto não mistura sítios. -/
theorem inner_qMark_exact {A B N : ℕ} (hA : A ≤ N) (hB : B ≤ N)
    (a : Matrix (chainIdx A) (chainIdx A) ℂ)
    (b : Matrix (chainIdx B) (chainIdx B) ℂ) :
    (inner ℂ ((tof P A a : TowerPre P) : TowerHilbert P)
      (towerPi P (qMark N) ((tof P B b : TowerPre P) : TowerHilbert P)) : ℂ)
    = ((P.w (N + 1) : ℝ) : ℂ)
      * inner ℂ ((tof P A a : TowerPre P) : TowerHilbert P)
          ((tof P B b : TowerPre P) : TowerHilbert P) := by
  have hA1 : A ≤ N + 1 := hA.trans (Nat.le_succ N)
  have hB1 : B ≤ N + 1 := hB.trans (Nat.le_succ N)
  rw [towerPi_coe, Completion.inner_coe, Completion.inner_coe]
  rw [show (inner ℂ (tof P A a) (lmulPre P (qMark N) (tof P B b)) : ℂ)
      = innerPre P (tof P A a) (lmulPre P (qMark N) (tof P B b)) from rfl]
  rw [show (inner ℂ (tof P A a) (tof P B b) : ℂ)
      = innerPre P (tof P A a) (tof P B b) from rfl]
  rw [lmulPre_tof_at (le_refl (N + 1)) hB1, tPush_self,
    innerPre_tof_at hA1 (le_refl (N + 1)), tPush_self,
    innerPre_tof_at hA hB]
  rw [tPush_succ hA hA1, tPush_succ hB hB1]
  set ta := tPush hA a with hta
  set tb := tPush hB b with htb
  unfold tInner
  rw [← towerStep_star]
  have hprod : towerStep taᴴ * (qMark N * towerStep tb)
      = (taᴴ * tb) ⊗ₖ Matrix.single 0 0 1 := by
    unfold towerStep qMark
    simp only [← Matrix.mul_kronecker_mul, one_mul, mul_one]
  rw [hprod, tState_kron_split]
  rw [Finset.sum_eq_single (0 : Fin 2)]
  · rw [Matrix.single_apply_same, mul_one]
    rw [show ((siteW (P.w (N + 1)) 0 : ℝ) : ℂ) = ((P.w (N + 1) : ℝ) : ℂ)
      from rfl]
    ring
  · intro s _ hs
    rw [Matrix.single_apply_of_ne _ _ _ _ _ (fun h => hs h.1.symm), mul_zero]
  · intro h
    exact absurd (Finset.mem_univ (0 : Fin 2)) h

/-! ## F — a convergência WOT das marcas -/

/-- [KERNEL] ★★★ AS MARCAS CONVERGEM WOT A μ·1: para qualquer trilha
    estritamente crescente de sítios de peso constante μ, e QUAISQUER
    ξ, η ∈ H_φ, ⟨ξ, π(q_{s k}) η⟩ → μ·⟨ξ,η⟩ — exatidão na torre densa
    + contração uniforme. O limite fraco vive; o forte não existe. -/
theorem qMark_wot (P : SiteProfile) (μ : ℝ) (s : ℕ → ℕ) (hs : StrictMono s)
    (hw : ∀ k, P.w (s k + 1) = μ) (ξ η : TowerHilbert P) :
    Tendsto (fun k => (inner ℂ ξ (towerPi P (qMark (s k)) η) : ℂ)) atTop
      (nhds (((μ : ℝ) : ℂ) * inner ℂ ξ η)) := by
  have hμ0 : 0 < μ := by rw [← hw 0]; exact P.pos _
  have hμ1 : μ < 1 := by rw [← hw 0]; exact P.lt_one _
  rw [Metric.tendsto_atTop]
  intro ε hε
  set D : ℝ := ‖ξ‖ + ‖η‖ + 2 with hDdef
  have hD0 : (0 : ℝ) < D := by positivity
  set δ : ℝ := min 1 (ε / (4 * D)) with hδdef
  have hδ0 : 0 < δ := lt_min one_pos (by positivity)
  have hδ1 : δ ≤ 1 := min_le_left _ _
  have hδε : δ ≤ ε / (4 * D) := min_le_right _ _
  obtain ⟨u, hu⟩ := (towerPre_denseRange (P := P)).exists_dist_lt ξ hδ0
  obtain ⟨v, hv⟩ := (towerPre_denseRange (P := P)).exists_dist_lt η hδ0
  obtain ⟨A, a, rfl⟩ := exists_tof u
  obtain ⟨B, b, rfl⟩ := exists_tof v
  refine ⟨max A B, fun k hk => ?_⟩
  have hAk : A ≤ s k := le_trans (le_trans (le_max_left A B) hk) hs.le_apply
  have hBk : B ≤ s k := le_trans (le_trans (le_max_right A B) hk) hs.le_apply
  set cu : TowerHilbert P := ((tof P A a : TowerPre P) : TowerHilbert P)
    with hcu
  set cv : TowerHilbert P := ((tof P B b : TowerPre P) : TowerHilbert P)
    with hcv
  set Q : TowerHilbert P →L[ℂ] TowerHilbert P := towerPi P (qMark (s k))
    with hQdef
  have hQle : ∀ z, ‖Q z‖ ≤ ‖z‖ := fun z => towerPi_qMark_le (s k) z
  have hex : (inner ℂ cu (Q cv) : ℂ) = ((μ : ℝ) : ℂ) * inner ℂ cu cv := by
    have h := inner_qMark_exact (P := P) hAk hBk a b
    rw [hw k] at h
    exact h
  have hu' : ‖ξ - cu‖ < δ := by rw [← dist_eq_norm]; exact hu
  have hv' : ‖η - cv‖ < δ := by rw [← dist_eq_norm]; exact hv
  have hcu_norm : ‖cu‖ ≤ ‖ξ‖ + 1 := by
    have h1 : ‖cu‖ ≤ ‖ξ‖ + ‖ξ - cu‖ := by
      have h2 := norm_sub_le ξ (ξ - cu)
      simpa using h2
    linarith [hu'.le, hδ1]
  have hcv_norm : ‖cv‖ ≤ ‖η‖ + 1 := by
    have h1 : ‖cv‖ ≤ ‖η‖ + ‖η - cv‖ := by
      have h2 := norm_sub_le η (η - cv)
      simpa using h2
    linarith [hv'.le, hδ1]
  have key : (inner ℂ ξ (Q η) : ℂ) - ((μ : ℝ) : ℂ) * inner ℂ ξ η
      = inner ℂ (ξ - cu) (Q η) + inner ℂ cu (Q (η - cv))
        + ((μ : ℝ) : ℂ) * inner ℂ (cu - ξ) cv
        + ((μ : ℝ) : ℂ) * inner ℂ ξ (cv - η) := by
    simp only [inner_sub_left, inner_sub_right, map_sub]
    rw [hex]
    ring
  rw [dist_eq_norm, key]
  have b1 : ‖(inner ℂ (ξ - cu) (Q η) : ℂ)‖ ≤ δ * ‖η‖ := by
    calc ‖(inner ℂ (ξ - cu) (Q η) : ℂ)‖ ≤ ‖ξ - cu‖ * ‖Q η‖ :=
          norm_inner_le_norm _ _
      _ ≤ δ * ‖η‖ :=
          mul_le_mul hu'.le (hQle η) (norm_nonneg _) hδ0.le
  have b2 : ‖(inner ℂ cu (Q (η - cv)) : ℂ)‖ ≤ (‖ξ‖ + 1) * δ := by
    calc ‖(inner ℂ cu (Q (η - cv)) : ℂ)‖ ≤ ‖cu‖ * ‖Q (η - cv)‖ :=
          norm_inner_le_norm _ _
      _ ≤ (‖ξ‖ + 1) * δ := by
          apply mul_le_mul hcu_norm (le_trans (hQle _) hv'.le)
            (norm_nonneg _) (by positivity)
  have b3 : ‖((μ : ℝ) : ℂ) * inner ℂ (cu - ξ) cv‖ ≤ δ * (‖η‖ + 1) := by
    rw [norm_mul, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hμ0]
    calc μ * ‖(inner ℂ (cu - ξ) cv : ℂ)‖
        ≤ 1 * (‖cu - ξ‖ * ‖cv‖) := by
          apply mul_le_mul hμ1.le (norm_inner_le_norm _ _)
            (norm_nonneg _) zero_le_one
      _ = ‖cu - ξ‖ * ‖cv‖ := one_mul _
      _ ≤ δ * (‖η‖ + 1) := by
          apply mul_le_mul _ hcv_norm (norm_nonneg _) hδ0.le
          rw [norm_sub_rev]
          exact hu'.le
  have b4 : ‖((μ : ℝ) : ℂ) * inner ℂ ξ (cv - η)‖ ≤ ‖ξ‖ * δ := by
    rw [norm_mul, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hμ0]
    calc μ * ‖(inner ℂ ξ (cv - η) : ℂ)‖
        ≤ 1 * (‖ξ‖ * ‖cv - η‖) := by
          apply mul_le_mul hμ1.le (norm_inner_le_norm _ _)
            (norm_nonneg _) zero_le_one
      _ = ‖ξ‖ * ‖cv - η‖ := one_mul _
      _ ≤ ‖ξ‖ * δ := by
          apply mul_le_mul_of_nonneg_left _ (norm_nonneg ξ)
          rw [norm_sub_rev]
          exact hv'.le
  set X1 : ℂ := inner ℂ (ξ - cu) (Q η) with hX1
  set X2 : ℂ := inner ℂ cu (Q (η - cv)) with hX2
  set X3 : ℂ := ((μ : ℝ) : ℂ) * inner ℂ (cu - ξ) cv with hX3
  set X4 : ℂ := ((μ : ℝ) : ℂ) * inner ℂ ξ (cv - η) with hX4
  have habcd : ‖X1 + X2 + X3 + X4‖ ≤ ‖X1‖ + ‖X2‖ + ‖X3‖ + ‖X4‖ := by
    calc ‖X1 + X2 + X3 + X4‖ ≤ ‖X1 + X2 + X3‖ + ‖X4‖ := norm_add_le _ _
      _ ≤ ‖X1 + X2‖ + ‖X3‖ + ‖X4‖ := by
          have h := norm_add_le (X1 + X2) X3
          linarith
      _ ≤ ‖X1‖ + ‖X2‖ + ‖X3‖ + ‖X4‖ := by
          have h := norm_add_le X1 X2
          linarith
  have hδD : δ * (4 * D) ≤ ε := by
    have h4D : (0 : ℝ) < 4 * D := by positivity
    calc δ * (4 * D) ≤ (ε / (4 * D)) * (4 * D) := by
          apply mul_le_mul_of_nonneg_right hδε (le_of_lt h4D)
      _ = ε := by field_simp
  have hfinal : ‖X1‖ + ‖X2‖ + ‖X3‖ + ‖X4‖ < ε := by
    have hξ0 : (0 : ℝ) ≤ ‖ξ‖ := norm_nonneg _
    have hη0 : (0 : ℝ) ≤ ‖η‖ := norm_nonneg _
    nlinarith [b1, b2, b3, b4, hδ0, hδD]
  exact lt_of_le_of_lt habcd hfinal

/-! ## G — a meação tracial -/

/-- [KERNEL] ★★ A MEAÇÃO: todo funcional tracial normalizado sobre o fator
    divide a marca ao meio — u·u† = q e u†·u = q' forçam τ(π q) = τ(π q'),
    e q + q' = 1 força a soma 1: logo τ(π q) = ½, em TODO sítio. -/
theorem tracial_halves_qMark (P : SiteProfile) (N : ℕ)
    (τ : (TowerHilbert P →L[ℂ] TowerHilbert P) → ℂ)
    (hadd : ∀ A B, τ (A + B) = τ A + τ B)
    (hone : τ 1 = 1)
    (htr : ∀ A B, A ∈ theFactorObject P → B ∈ theFactorObject P →
      τ (A * B) = τ (B * A)) :
    τ (towerPi P (qMark N)) = 1 / 2 := by
  have hu := htr (towerPi P (uMark N)) (towerPi P ((uMark N)ᴴ))
    (towerPi_mem_factor _) (towerPi_mem_factor _)
  have heq : towerPi P (uMark N) * towerPi P ((uMark N)ᴴ)
      = towerPi P (qMark N) := by
    rw [← towerPi_mul, uMark_mul_star]
  have heq' : towerPi P ((uMark N)ᴴ) * towerPi P (uMark N)
      = towerPi P (qMark' N) := by
    rw [← towerPi_mul, star_mul_uMark]
  have hhalf : τ (towerPi P (qMark N)) = τ (towerPi P (qMark' N)) := by
    rw [← heq, ← heq']
    exact hu
  have hsum : τ (towerPi P (qMark N)) + τ (towerPi P (qMark' N)) = 1 := by
    rw [← hadd, ← towerPi_add, qMark_partition, towerPi_one, hone]
  rw [← hhalf] at hsum
  linear_combination hsum / 2

/-! ## H — O ASSASSINATO -/

/-- [KERNEL] ★★★ O ASSASSINATO DO PESO NORMAL: numa trilha de sítios de
    peso constante μ ≠ ½, NENHUM funcional tracial normalizado sobre
    M_TGL é WOT-sequencialmente contínuo — a meação diz ½ em todo sítio,
    o limite fraco diz μ, e μ ≠ ½ recusa a coexistência. Como a
    normalidade genuína implica a continuidade sequencial, NÃO EXISTE
    estado tracial normal sobre o objeto completado. -/
theorem no_normal_tracial_state_seq (P : SiteProfile) (μ : ℝ) (s : ℕ → ℕ)
    (hs : StrictMono s) (hw : ∀ k, P.w (s k + 1) = μ) (hμ : μ ≠ 1 / 2)
    (τ : (TowerHilbert P →L[ℂ] TowerHilbert P) → ℂ)
    (hadd : ∀ A B, τ (A + B) = τ A + τ B)
    (hsmul : ∀ (c : ℂ) A, τ (c • A) = c * τ A)
    (hone : τ 1 = 1)
    (htr : ∀ A B, A ∈ theFactorObject P → B ∈ theFactorObject P →
      τ (A * B) = τ (B * A))
    (hnormal : SeqWOTContinuous (theFactorObject P) τ) : False := by
  set Q : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P :=
    fun k => towerPi P (qMark (s k)) with hQ
  set Tinf : TowerHilbert P →L[ℂ] TowerHilbert P := ((μ : ℝ) : ℂ) • 1
    with hT
  have hTpi : towerPi P
      (((μ : ℝ) : ℂ) • (1 : Matrix (chainIdx 0) (chainIdx 0) ℂ)) = Tinf := by
    rw [towerPi_smul, towerPi_one, hT]
  have hmem : ∀ k, Q k ∈ theFactorObject P := fun k => towerPi_mem_factor _
  have hmeminf : Tinf ∈ theFactorObject P := by
    rw [← hTpi]
    exact towerPi_mem_factor _
  have hbound : ∀ k, ‖Q k‖ ≤ 1 := by
    intro k
    refine ContinuousLinearMap.opNorm_le_bound _ zero_le_one (fun ξ => ?_)
    rw [one_mul]
    exact towerPi_qMark_le (s k) ξ
  have hwot : ∀ ξ η : TowerHilbert P,
      Tendsto (fun k => (inner ℂ ξ (Q k η) : ℂ)) atTop
        (nhds (inner ℂ ξ (Tinf η))) := by
    intro ξ η
    have hTη : Tinf η = ((μ : ℝ) : ℂ) • η := by
      simp [hT]
    rw [hTη, inner_smul_right]
    exact qMark_wot P μ s hs hw ξ η
  have hlim := hnormal Q Tinf 1 hmem hmeminf hbound hwot
  have hconst : ∀ k, τ (Q k) = 1 / 2 := fun k =>
    tracial_halves_qMark P (s k) τ hadd hone htr
  have hlim2 : Tendsto (fun k => τ (Q k)) atTop (nhds ((1 : ℂ) / 2)) := by
    rw [tendsto_congr hconst]
    exact tendsto_const_nhds
  have huniq : τ Tinf = (1 : ℂ) / 2 := tendsto_nhds_unique hlim hlim2
  have hτT : τ Tinf = ((μ : ℝ) : ℂ) := by
    rw [hT, hsmul, hone, mul_one]
  rw [hτT] at huniq
  apply hμ
  have hcast : ((μ : ℝ) : ℂ) = ((1 / 2 : ℝ) : ℂ) := by
    rw [huniq]
    norm_num
  exact_mod_cast hcast

/-- [KERNEL] ★★★ O ASSASSINATO NO OBJETO DA MARCA (perfil ⅓,¼): o MESMO
    M_TGL que realiza a S-invariante log-densa (pedra 87) NÃO tem estado
    tracial normal — a assinatura III₁ operacional do programa, completa,
    num único objeto. -/
theorem no_normal_tracial_state_mix
    (τ : (TowerHilbert mixProfile →L[ℂ] TowerHilbert mixProfile) → ℂ)
    (hadd : ∀ A B, τ (A + B) = τ A + τ B)
    (hsmul : ∀ (c : ℂ) A, τ (c • A) = c * τ A)
    (hone : τ 1 = 1)
    (htr : ∀ A B, A ∈ theFactorObject mixProfile →
      B ∈ theFactorObject mixProfile → τ (A * B) = τ (B * A))
    (hnormal : SeqWOTContinuous (theFactorObject mixProfile) τ) : False := by
  refine no_normal_tracial_state_seq mixProfile (1 / 3) (fun k => 2 * k + 1)
    ?_ ?_ ?_ τ hadd hsmul hone htr hnormal
  · intro x y hxy
    dsimp only
    omega
  · intro k
    show mixProfile.w (2 * k + 1 + 1) = 1 / 3
    have hmod : (2 * k + 1 + 1) % 2 = 0 := by omega
    show (if (2 * k + 1 + 1) % 2 = 0 then (1 : ℝ) / 3 else 1 / 4) = 1 / 3
    rw [if_pos hmod]
  · norm_num

/-- [KERNEL] ★★ O ASSASSINATO NA ESCADA CONSTANTE (l ≠ 1): o objeto de
    razão l — a face III_λ — também não tem estado tracial normal. -/
theorem no_normal_tracial_state_const (l : ℝ) (hl : 0 < l) (hl1 : l ≠ 1)
    (τ : (TowerHilbert (constProfile l hl) →L[ℂ]
      TowerHilbert (constProfile l hl)) → ℂ)
    (hadd : ∀ A B, τ (A + B) = τ A + τ B)
    (hsmul : ∀ (c : ℂ) A, τ (c • A) = c * τ A)
    (hone : τ 1 = 1)
    (htr : ∀ A B, A ∈ theFactorObject (constProfile l hl) →
      B ∈ theFactorObject (constProfile l hl) → τ (A * B) = τ (B * A))
    (hnormal : SeqWOTContinuous (theFactorObject (constProfile l hl)) τ) :
    False := by
  refine no_normal_tracial_state_seq (constProfile l hl) (l / (1 + l)) id
    strictMono_id (fun k => rfl) ?_ τ hadd hsmul hone htr hnormal
  intro hc
  apply hl1
  have h1l : (0 : ℝ) < 1 + l := by linarith
  rw [div_eq_div_iff (ne_of_gt h1l) (by norm_num : (2 : ℝ) ≠ 0)] at hc
  linarith

/-- [KERNEL] ★★★ A SÍNTESE DA PEDRA 88: no objeto da marca (⅓,¼) — ω é
    WOT-sequencialmente normal (a noção não é vácua) E nenhum funcional
    tracial normalizado é WOT-sequencialmente normal (o peso está morto).
    O estado do Nome vive; o traço não sobrevive ao limite. -/
theorem the_dead_weight :
    SeqWOTContinuous (theFactorObject mixProfile) (omegaState mixProfile)
    ∧ ∀ τ : (TowerHilbert mixProfile →L[ℂ] TowerHilbert mixProfile) → ℂ,
        (∀ A B, τ (A + B) = τ A + τ B) →
        (∀ (c : ℂ) A, τ (c • A) = c * τ A) →
        τ 1 = 1 →
        (∀ A B, A ∈ theFactorObject mixProfile →
          B ∈ theFactorObject mixProfile → τ (A * B) = τ (B * A)) →
        SeqWOTContinuous (theFactorObject mixProfile) τ → False :=
  ⟨omegaState_seqWOT mixProfile,
   fun τ hadd hsmul hone htr hnormal =>
     no_normal_tracial_state_mix τ hadd hsmul hone htr hnormal⟩

end

end TGLExt
