import PauliInteractionWitness

set_option autoImplicit false
set_option maxHeartbeats 600000

namespace ChatgptAudit.AdmissibleInteraction
open TGLExt ChatgptAudit ChatgptAudit.Observable035
  ChatgptAudit.SummableInteraction ChatgptAudit.InteractionWitness Filter Topology
noncomputable section

/-- Admissible coefficients carry the actual summability proof. -/
structure SummableCouplingData where
  value : ℕ → ℝ
  norm_summable : Summable (fun j => |value j|)

def certifiedInteraction (P : SiteProfile) (c : SummableCouplingData) :
    InteractionOperator P := interactionLimit P c.value

def certifiedPrefix (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) :
    InteractionOperator P := interactionPrefix P c.value N

def singleBondData : SummableCouplingData where
  value := singleBondCoupling
  norm_summable := single_bond_coupling_summable

theorem certified_interaction_selfadjoint (P : SiteProfile) (c : SummableCouplingData) :
    IsSelfAdjoint (certifiedInteraction P c) :=
  interaction_limit_selfadjoint P c.value

theorem certified_interaction_mem_factor (P : SiteProfile) (c : SummableCouplingData) :
    certifiedInteraction P c ∈ theFactorObject P :=
  interaction_limit_mem_factor P c.value

theorem certified_prefix_converges (P : SiteProfile) (c : SummableCouplingData) :
    Tendsto (certifiedPrefix P c) atTop (𝓝 (certifiedInteraction P c)) :=
  interaction_prefix_tendsto P c.value c.norm_summable

theorem certified_interaction_bound (P : SiteProfile) (c : SummableCouplingData) :
    ‖certifiedInteraction P c‖≤∑' j, |c.value j| :=
  interaction_limit_norm_bound P c.value c.norm_summable

theorem certified_cutoff_uniform_bound (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) :
    ‖certifiedPrefix P c N‖≤∑' j, |c.value j| :=
  interaction_prefix_uniform_bound P c.value c.norm_summable N

theorem certified_cutoff_error (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) :
    ‖certifiedInteraction P c-certifiedPrefix P c N‖≤couplingTail c.value N :=
  interaction_tail_bound P c.value c.norm_summable N

theorem certified_tail_vanishes (c : SummableCouplingData) :
    Tendsto (couplingTail c.value) atTop (𝓝 0) :=
  coupling_tail_tendsto_zero c.value c.norm_summable

theorem certified_single_bond (P : SiteProfile) :
    certifiedInteraction P singleBondData=pauliBond P 0 :=
  single_bond_limit P

theorem certified_single_bond_not_centralizer (P : SiteProfile) (hp : P.w 0≠1/2) :
    certifiedInteraction P singleBondData ∉ omegaCentralizer P :=
  single_bond_limit_not_in_centralizer P hp

theorem certified_single_bond_interacts (P : SiteProfile) :
    (certifiedInteraction P singleBondData * sitePauliZ P 0 -
        sitePauliZ P 0 * certifiedInteraction P singleBondData) * sitePauliZ P 1 -
      sitePauliZ P 1 * (certifiedInteraction P singleBondData * sitePauliZ P 0 -
        sitePauliZ P 0 * certifiedInteraction P singleBondData) ≠ 0 :=
  single_bond_limit_interacts P

#print axioms SummableCouplingData
#print axioms certifiedInteraction
#print axioms certifiedPrefix
#print axioms singleBondData
#print axioms certified_interaction_selfadjoint
#print axioms certified_interaction_mem_factor
#print axioms certified_prefix_converges
#print axioms certified_interaction_bound
#print axioms certified_cutoff_uniform_bound
#print axioms certified_cutoff_error
#print axioms certified_tail_vanishes
#print axioms certified_single_bond
#print axioms certified_single_bond_not_centralizer
#print axioms certified_single_bond_interacts
end
end ChatgptAudit.AdmissibleInteraction
