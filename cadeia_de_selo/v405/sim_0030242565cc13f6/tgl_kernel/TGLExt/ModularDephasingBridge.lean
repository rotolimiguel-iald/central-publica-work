import TGLExt.EquivariantSection
import TGLExt.CentralizerLocal
import Mathlib.Tactic.NoncommRing

set_option autoImplicit false
set_option maxHeartbeats 1000000

/-! Reuses the tower's spectral expectation and modular flow. The exact spectral
expectation of the full modular density has stationary range. A coarser
expectation can retain a nontrivial common flow when the relative generator is
constant on each retained block. No spacetime localization is asserted here. -/
namespace ModularDephasingBridge
open TGLExt Matrix
noncomputable section
variable {n : Type} [Fintype n] [DecidableEq n]

omit [Fintype n] in
theorem spectral_preserves_every_diagonal (d : n → ℝ) (v : n → ℂ) :
    specExpect d (diagonal v) = diagonal v := by
  ext i j
  by_cases h : i = j
  · subst h; simp
  · simp [diagonal_apply_ne _ h]

omit [Fintype n] in
theorem spectral_preserves_density (d : n → ℝ) :
    specExpect d (rhoD d) = rhoD d :=
  spectral_preserves_every_diagonal d _

theorem spectral_preserves_modular_generator (d : n → ℝ) (hd : ∀ i, 0 < d i) :
    specExpect d (-logRho (rhoD d)) = -logRho (rhoD d) := by
  rw [logRho_diagonal d hd, diagonal_neg]
  exact spectral_preserves_every_diagonal d _

theorem spectral_reading_is_stationary (d : n → ℝ) (hd : ∀ i, 0 < d i)
    (alpha : ℝ → Matrix n n ℂ → Matrix n n ℂ) :
    (∀ t x, sigma (rhoD d) t (specExpect d x) = alpha t (specExpect d x)) ↔
    (∀ t x, alpha t (specExpect d x) = specExpect d x) := by
  simp only [sigma_fixed_specExpect d hd]
  exact forall_congr' fun t => forall_congr' fun x => eq_comm

theorem spectral_preserves_remainder_balance (d : n → ℝ) (hd : ∀ i, 0 < d i)
    (Q R : Matrix n n ℂ) (h : -logRho (rhoD d) = Q + R) :
    -logRho (rhoD d) = specExpect d Q + specExpect d R := by
  have hp := spectral_preserves_modular_generator d hd
  rw [h] at hp
  rw [h, ← hp]
  ext i j
  by_cases he : d i = d j <;> simp [he]

theorem stationary_generator_balance {A : Type*} [Ring A] (K Q R X : A)
    (h : K = Q + R) (hK : Commute K X) :
    Q * X - X * Q = -(R * X - X * R) := by
  have hc : (Q + R) * X = X * (Q + R) := by simpa [h] using hK.eq
  rw [neg_sub, sub_eq_sub_iff_add_eq_add]
  simpa only [add_mul, mul_add, add_comm] using hc

/-- The same equality on observables, without assuming K stationary. -/
theorem generator_bridge_iff {A : Type*} [Ring A] (K Q R X : A)
    (h : K = Q + R) :
    K * X - X * K = Q * X - X * Q ↔ Commute R X := by
  rw [h]
  change (Q + R) * X - X * (Q + R) = Q * X - X * Q ↔ R * X = X * R
  have hi : (Q + R) * X - X * (Q + R) =
      (Q * X - X * Q) + (R * X - X * R) := by noncomm_ring
  rw [hi, add_eq_left, sub_eq_zero]

/-- Normalization is explicit; the densities need not share a partition function. -/
theorem coarse_dephasing_flow_bridge (q r : n → ℝ) (Z Y : ℝ)
    (hZ : 0 < Z) (hY : 0 < Y) (x : Matrix n n ℂ) (t : ℝ) :
    sigma (rhoD (fun i => Real.exp (-(q i + r i)) / Z)) t (specExpect r x) =
    sigma (rhoD (fun i => Real.exp (-q i) / Y)) t (specExpect r x) := by
  ext i j
  rw [sigma_diagonal_apply _ (fun _ => div_pos (Real.exp_pos _) hZ),
      sigma_diagonal_apply _ (fun _ => div_pos (Real.exp_pos _) hY)]
  by_cases h : r i = r j
  · simp only [specExpect_apply, if_pos h]
    rw [Real.log_div (ne_of_gt (Real.exp_pos _)) (ne_of_gt hZ),
        Real.log_div (ne_of_gt (Real.exp_pos _)) (ne_of_gt hZ),
        Real.log_div (ne_of_gt (Real.exp_pos _)) (ne_of_gt hY),
        Real.log_div (ne_of_gt (Real.exp_pos _)) (ne_of_gt hY)]
    simp only [Real.log_exp]
    congr 2
    push_cast
    rw [h]
    ring
  · simp [h]

omit [Fintype n] in
theorem coarse_preserves_vacuum (q r : n → ℝ) (Z : ℝ) :
    specExpect r (rhoD (fun i => Real.exp (-(q i + r i)) / Z)) =
      rhoD (fun i => Real.exp (-(q i + r i)) / Z) :=
  spectral_preserves_every_diagonal r _

omit [Fintype n] in
theorem coarse_remainder_survives (r : n → ℝ) :
    specExpect r (rhoD r) = rhoD r := spectral_preserves_density r

theorem coarse_remainder_is_invisible (r : n → ℝ) (x : Matrix n n ℂ) :
    Commute (rhoD r) (specExpect r x) := rhoD_commute_specExpect r x

/-- This applies the existing pinching to the actual finite prefixes of the tower. -/
theorem tower_prefix_reading_stationary (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (t : ℝ) :
    sigma (rhoD (towerW P N)) t (specExpect (towerW P N) a) =
      specExpect (towerW P N) a :=
  sigma_fixed_specExpect _ (towerW_pos P N) a t

/-- Multiplicative version for the already constructed product densities. -/
theorem product_dephasing_flow_bridge (a b : n → ℝ)
    (ha : ∀ i, 0 < a i) (hb : ∀ i, 0 < b i) (Y : ℝ) (hY : 0 < Y)
    (x : Matrix n n ℂ) (t : ℝ) :
    sigma (rhoD (fun i => a i * b i)) t (specExpect b x) =
    sigma (rhoD (fun i => a i / Y)) t (specExpect b x) := by
  ext i j
  rw [sigma_diagonal_apply _ (fun i => mul_pos (ha i) (hb i)),
      sigma_diagonal_apply _ (fun i => div_pos (ha i) hY)]
  by_cases h : b i = b j
  · simp only [specExpect_apply, if_pos h]
    rw [Real.log_mul (ne_of_gt (ha i)) (ne_of_gt (hb i)),
        Real.log_mul (ne_of_gt (ha j)) (ne_of_gt (hb j)),
        Real.log_div (ne_of_gt (ha i)) (ne_of_gt hY),
        Real.log_div (ne_of_gt (ha j)) (ne_of_gt hY)]
    congr 2
    push_cast
    rw [h]
    ring
  · simp [h]

/-- Exact restriction on every actual next level of PRODUCT_TOWER. The reading
only dephases the last site. The reference retains the previous level and makes
the last site tracial. It is not the full spectral expectation of the vacuum. -/
theorem tower_last_site_flow_bridge (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx (N+1)) (chainIdx (N+1)) ℂ) (t : ℝ) :
    sigma (rhoD (towerW P (N+1))) t
        (specExpect (fun i : chainIdx (N+1) => siteW (P.w (N+1)) i.2) a) =
    sigma (rhoD (fun i : chainIdx (N+1) => towerW P N i.1 / 2)) t
        (specExpect (fun i : chainIdx (N+1) => siteW (P.w (N+1)) i.2) a) := by
  exact product_dephasing_flow_bridge (n := chainIdx (N+1))
    (fun i => towerW P N i.1) (fun i => siteW (P.w (N+1)) i.2)
    (fun i => towerW_pos P N i.1)
    (fun i => siteW_pos (P.pos (N+1)) (P.lt_one (N+1)) i.2)
    2 (by norm_num) a t

/-- Both densities in the tower bridge are normalized, not arbitrary weights. -/
theorem tower_last_site_reference_normalized (P : SiteProfile) (N : ℕ) :
    (∑ i : chainIdx (N+1), towerW P N i.1 / 2) = 1 := by
  change (∑ i : chainIdx N × Fin 2, towerW P N i.1 / 2) = 1
  rw [Fintype.sum_prod_type]
  have h (i : chainIdx N) : (∑ _ : Fin 2, towerW P N i / 2) = towerW P N i := by
    rw [Fin.sum_univ_two]
    ring
  simp only [h]
  exact towerW_sum P N

/-- Full spectral erasure of R does not erase its commutator action on a
retained observable. The proposed universal shortcut is false already in M2. -/
theorem erased_remainder_counterexample :
    let d : Fin 2 → ℝ := ![1, 2]
    let R : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]
    let p : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, 0]
    specExpect d R = 0 ∧ specExpect d p = p ∧ ¬Commute R p := by
  dsimp
  constructor
  · ext i j
    fin_cases i <;> fin_cases j <;> norm_num [specExpect]
  constructor
  · ext i j
    fin_cases i <;> fin_cases j <;> norm_num [specExpect]
  · intro he
    have hc := congrArg (fun a : Matrix (Fin 2) (Fin 2) ℂ => a 0 1) he.eq
    norm_num [Matrix.mul_apply, Fin.sum_univ_two] at hc

#print axioms spectral_preserves_every_diagonal
#print axioms spectral_preserves_density
#print axioms spectral_preserves_modular_generator
#print axioms spectral_reading_is_stationary
#print axioms spectral_preserves_remainder_balance
#print axioms stationary_generator_balance
#print axioms generator_bridge_iff
#print axioms coarse_dephasing_flow_bridge
#print axioms coarse_preserves_vacuum
#print axioms coarse_remainder_survives
#print axioms coarse_remainder_is_invisible
#print axioms tower_prefix_reading_stationary
#print axioms product_dephasing_flow_bridge
#print axioms tower_last_site_flow_bridge
#print axioms tower_last_site_reference_normalized
#print axioms erased_remainder_counterexample
end
end ModularDephasingBridge
