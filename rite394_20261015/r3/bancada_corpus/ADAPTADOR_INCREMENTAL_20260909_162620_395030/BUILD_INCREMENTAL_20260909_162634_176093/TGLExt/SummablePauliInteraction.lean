import TGLExt.SitePauliObservables
import TGLExt.SummableLikelihoodGenerator
import Mathlib.Analysis.Normed.Group.InfiniteSum
import Mathlib.Topology.Algebra.InfiniteSum.NatInt
import Mathlib.Tactic.NoncommRing

set_option autoImplicit false
set_option maxHeartbeats 900000

namespace ChatgptAudit.SummableInteraction
open TGLExt ChatgptAudit ChatgptAudit.Observable035
  ChatgptAudit.Cocycle030 Filter Topology
noncomputable section

abbrev InteractionOperator (P : SiteProfile) := TowerHilbert P →L[ℂ] TowerHilbert P

def pauliBond (P : SiteProfile) (j : ℕ) : InteractionOperator P :=
  sitePauliX P j * sitePauliX P (j+1)

def interactionTerm (P : SiteProfile) (c : ℕ → ℝ) (j : ℕ) : InteractionOperator P :=
  (c j : ℂ) • pauliBond P j

def interactionPrefix (P : SiteProfile) (c : ℕ → ℝ) (N : ℕ) : InteractionOperator P :=
  ∑ j ∈ Finset.range N, interactionTerm P c j

def interactionLimit (P : SiteProfile) (c : ℕ → ℝ) : InteractionOperator P :=
  ∑' j, interactionTerm P c j

def couplingTail (c : ℕ → ℝ) (N : ℕ) : ℝ :=
  ∑' j, |c (j+N)|

theorem pauli_bond_selfadjoint (P : SiteProfile) (j : ℕ) :
    IsSelfAdjoint (pauliBond P j) := by
  change star (sitePauliX P j * sitePauliX P (j+1)) = _
  rw [star_mul, (site_pauli_x_selfadjoint P j).star_eq,
    (site_pauli_x_selfadjoint P (j+1)).star_eq]
  exact (site_pauli_xx_commute P (Nat.ne_of_lt (Nat.lt_succ_self j))).eq.symm

theorem pauli_bond_square (P : SiteProfile) (j : ℕ) :
    pauliBond P j * pauliBond P j = 1 := by
  have hc := (site_pauli_xx_commute P (Nat.ne_of_lt (Nat.lt_succ_self j))).eq
  unfold pauliBond
  calc
    sitePauliX P j * sitePauliX P (j+1) * (sitePauliX P j * sitePauliX P (j+1)) =
        sitePauliX P j * (sitePauliX P (j+1) * sitePauliX P j) * sitePauliX P (j+1) := by
          noncomm_ring
    _ = sitePauliX P j * (sitePauliX P j * sitePauliX P (j+1)) * sitePauliX P (j+1) := by rw [← hc]
    _ = (sitePauliX P j * sitePauliX P j) *
        (sitePauliX P (j+1) * sitePauliX P (j+1)) := by noncomm_ring
    _ = 1 := by rw [site_pauli_x_square, site_pauli_x_square, one_mul]

theorem pauli_bond_unitary (P : SiteProfile) (j : ℕ) :
    pauliBond P j ∈ unitary (InteractionOperator P) := by
  rw [Unitary.mem_iff]
  constructor <;> rw [(pauli_bond_selfadjoint P j).star_eq, pauli_bond_square]

theorem selfadjoint_involution_norm_le_one {P : SiteProfile}
    (A : InteractionOperator P) (ha : IsSelfAdjoint A) (hs : A*A=1) : ‖A‖≤1 := by
  have he : ‖A‖*‖A‖=‖(1 : InteractionOperator P)‖ := by
    rw [← CStarRing.norm_star_mul_self, ha.star_eq, hs]
  have ho : ‖(1 : InteractionOperator P)‖≤1 := ContinuousLinearMap.norm_id_le
  nlinarith [norm_nonneg A]

theorem pauli_bond_norm_le_one (P : SiteProfile) (j : ℕ) :
    ‖pauliBond P j‖≤1 :=
  selfadjoint_involution_norm_le_one _ (pauli_bond_selfadjoint P j) (pauli_bond_square P j)

theorem pauli_bond_mem_factor (P : SiteProfile) (j : ℕ) :
    pauliBond P j ∈ theFactorObject P :=
  mul_mem (site_pauli_x_mem_factor P j) (site_pauli_x_mem_factor P (j+1))

theorem interaction_term_selfadjoint (P : SiteProfile) (c : ℕ → ℝ) (j : ℕ) :
    IsSelfAdjoint (interactionTerm P c j) := by
  change star ((c j : ℂ) • pauliBond P j) = (c j : ℂ) • pauliBond P j
  simp only [star_smul, Complex.star_def, Complex.conj_ofReal,
    (pauli_bond_selfadjoint P j).star_eq]

theorem interaction_term_norm_bound (P : SiteProfile) (c : ℕ → ℝ) (j : ℕ) :
    ‖interactionTerm P c j‖≤|c j| := by
  rw [interactionTerm, norm_smul, Complex.norm_real, Real.norm_eq_abs]
  exact mul_le_of_le_one_right (abs_nonneg _) (pauli_bond_norm_le_one P j)

theorem interaction_term_mem_factor (P : SiteProfile) (c : ℕ → ℝ) (j : ℕ) :
    interactionTerm P c j ∈ theFactorObject P :=
  (theFactorObject P).toStarSubalgebra.smul_mem (pauli_bond_mem_factor P j) _

theorem interaction_prefix_selfadjoint (P : SiteProfile) (c : ℕ → ℝ) (N : ℕ) :
    IsSelfAdjoint (interactionPrefix P c N) := by
  change star (∑ j ∈ Finset.range N, interactionTerm P c j) = _
  simp only [star_sum, (interaction_term_selfadjoint P c _).star_eq]
  rfl

theorem interaction_prefix_mem_factor (P : SiteProfile) (c : ℕ → ℝ) (N : ℕ) :
    interactionPrefix P c N ∈ theFactorObject P :=
  sum_mem (fun j _ => interaction_term_mem_factor P c j)

theorem interaction_prefix_norm_bound (P : SiteProfile) (c : ℕ → ℝ) (N : ℕ) :
    ‖interactionPrefix P c N‖≤∑ j ∈ Finset.range N, |c j| := by
  exact (norm_sum_le _ _).trans
    (Finset.sum_le_sum (fun j _ => interaction_term_norm_bound P c j))

theorem interaction_norm_summable (P : SiteProfile) (c : ℕ → ℝ)
    (hc : Summable (fun j => |c j|)) :
    Summable (fun j => ‖interactionTerm P c j‖) :=
  Summable.of_nonneg_of_le (fun _ => norm_nonneg _) (interaction_term_norm_bound P c) hc

theorem interaction_summable (P : SiteProfile) (c : ℕ → ℝ)
    (hc : Summable (fun j => |c j|)) : Summable (interactionTerm P c) :=
  (interaction_norm_summable P c hc).of_norm

theorem interaction_prefix_tendsto (P : SiteProfile) (c : ℕ → ℝ)
    (hc : Summable (fun j => |c j|)) :
    Tendsto (interactionPrefix P c) atTop (𝓝 (interactionLimit P c)) :=
  (interaction_summable P c hc).hasSum.tendsto_sum_nat

theorem interaction_limit_selfadjoint (P : SiteProfile) (c : ℕ → ℝ) :
    IsSelfAdjoint (interactionLimit P c) := by
  change star (∑' j, interactionTerm P c j) = _
  rw [tsum_star]
  simp only [(interaction_term_selfadjoint P c _).star_eq]
  rfl

theorem interaction_limit_mem_factor (P : SiteProfile) (c : ℕ → ℝ) :
    interactionLimit P c ∈ theFactorObject P :=
  tsum_mem (factor_norm_closed P) (fun j => interaction_term_mem_factor P c j)

theorem interaction_limit_norm_bound (P : SiteProfile) (c : ℕ → ℝ)
    (hc : Summable (fun j => |c j|)) :
    ‖interactionLimit P c‖≤∑' j, |c j| :=
  tsum_of_norm_bounded hc.hasSum (interaction_term_norm_bound P c)

theorem coupling_tail_nonnegative (c : ℕ → ℝ) (N : ℕ) : 0≤couplingTail c N :=
  tsum_nonneg (fun _ => abs_nonneg _)

theorem interaction_prefix_add_tail (P : SiteProfile) (c : ℕ → ℝ)
    (hc : Summable (fun j => |c j|)) (N : ℕ) :
    interactionPrefix P c N + (∑' j, interactionTerm P c (j+N)) = interactionLimit P c :=
  (interaction_summable P c hc).sum_add_tsum_nat_add N

theorem interaction_limit_sub_prefix (P : SiteProfile) (c : ℕ → ℝ)
    (hc : Summable (fun j => |c j|)) (N : ℕ) :
    interactionLimit P c - interactionPrefix P c N = ∑' j, interactionTerm P c (j+N) := by
  rw [← interaction_prefix_add_tail P c hc N]
  abel

theorem interaction_tail_bound (P : SiteProfile) (c : ℕ → ℝ)
    (hc : Summable (fun j => |c j|)) (N : ℕ) :
    ‖interactionLimit P c - interactionPrefix P c N‖≤couplingTail c N := by
  rw [interaction_limit_sub_prefix P c hc N]
  exact tsum_of_norm_bounded ((summable_nat_add_iff N).mpr hc).hasSum
    (fun j => interaction_term_norm_bound P c (j+N))

theorem coupling_tail_tendsto_zero (c : ℕ → ℝ) (hc : Summable (fun j => |c j|)) :
    Tendsto (couplingTail c) atTop (𝓝 0) := by
  have he (N : ℕ) : couplingTail c N =
      (∑' j, |c j|) - ∑ j ∈ Finset.range N, |c j| := by
    have h := hc.sum_add_tsum_nat_add N
    change _ + couplingTail c N = _ at h
    linarith
  have heq : couplingTail c = (fun N => (∑' j, |c j|) - ∑ j ∈ Finset.range N, |c j|) := funext he
  rw [heq]
  have ht : Tendsto (fun _ : ℕ => (∑' j, |c j|)) atTop (𝓝 (∑' j, |c j|)) := tendsto_const_nhds
  simpa using ht.sub hc.hasSum.tendsto_sum_nat

theorem interaction_prefix_uniform_bound (P : SiteProfile) (c : ℕ → ℝ)
    (hc : Summable (fun j => |c j|)) (N : ℕ) :
    ‖interactionPrefix P c N‖≤∑' j, |c j| :=
  (interaction_prefix_norm_bound P c N).trans
    (hc.sum_le_tsum _ (fun _ _ => abs_nonneg _))

#print axioms InteractionOperator
#print axioms pauliBond
#print axioms interactionTerm
#print axioms interactionPrefix
#print axioms interactionLimit
#print axioms couplingTail
#print axioms pauli_bond_selfadjoint
#print axioms pauli_bond_square
#print axioms pauli_bond_unitary
#print axioms selfadjoint_involution_norm_le_one
#print axioms pauli_bond_norm_le_one
#print axioms pauli_bond_mem_factor
#print axioms interaction_term_selfadjoint
#print axioms interaction_term_norm_bound
#print axioms interaction_term_mem_factor
#print axioms interaction_prefix_selfadjoint
#print axioms interaction_prefix_mem_factor
#print axioms interaction_prefix_norm_bound
#print axioms interaction_norm_summable
#print axioms interaction_summable
#print axioms interaction_prefix_tendsto
#print axioms interaction_limit_selfadjoint
#print axioms interaction_limit_mem_factor
#print axioms interaction_limit_norm_bound
#print axioms coupling_tail_nonnegative
#print axioms interaction_prefix_add_tail
#print axioms interaction_limit_sub_prefix
#print axioms interaction_tail_bound
#print axioms coupling_tail_tendsto_zero
#print axioms interaction_prefix_uniform_bound
end
end ChatgptAudit.SummableInteraction
