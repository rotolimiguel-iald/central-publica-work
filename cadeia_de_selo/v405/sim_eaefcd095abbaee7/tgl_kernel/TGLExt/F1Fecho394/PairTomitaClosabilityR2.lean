import TGLExt.O16.RecognitionGraph_v2
/-! Generic reuse of the pairing/closure argument in TomitaClosability.lean.
The old proof is for TowerHilbert; this adapter accepts a commuting cyclic pair
and uses exactly the existing pairTomitaGraph. It does not assert its polar data. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
open Set Topology
namespace F1Fecho.PairTomita
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (M N : StarSubalgebra ℂ (H →L[ℂ] H)) (Ω : H)

def orbit : Submodule ℂ H where
  carrier := (fun a : H →L[ℂ] H => a Ω) '' (M : Set (H →L[ℂ] H))
  zero_mem' := ⟨0,M.zero_mem,rfl⟩
  add_mem' := by
    rintro x y ⟨a,ha,rfl⟩ ⟨b,hb,rfl⟩
    exact ⟨a+b,M.add_mem ha hb,rfl⟩
  smul_mem' := by
    rintro c x ⟨a,ha,rfl⟩
    exact ⟨c • a,M.smul_mem ha c,rfl⟩

theorem span_orbit :
    Submodule.span ℂ ((fun a : H →L[ℂ] H => a Ω) '' (M : Set (H →L[ℂ] H))) = orbit M Ω :=
  Submodule.span_eq (orbit M Ω)

theorem dense_orbit_of_dense_span
    (h : Dense ((Submodule.span ℂ ((fun a : H →L[ℂ] H => a Ω) ''
      (M : Set (H →L[ℂ] H)))) : Set H)) :
    Dense ((fun a : H →L[ℂ] H => a Ω) '' (M : Set (H →L[ℂ] H))) := by
  rw [span_orbit] at h
  exact h

abbrev graph := ORDEM016.D6.pairTomitaGraph M Ω

variable (hc : ∀ a ∈ M, ∀ b ∈ N, Commute a b)

include hc in
theorem pairing {a b : H →L[ℂ] H} (ha : a ∈ M) (hb : b ∈ N) :
    inner ℂ ((star a) Ω) (b Ω) = inner ℂ ((star b) Ω) (a Ω) := by
  simp only [ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_inner_left]
  have h := congrArg (fun T : H →L[ℂ] H => T Ω) (hc a ha b hb).eq
  simpa only [ContinuousLinearMap.mul_apply] using congrArg (fun x : H => inner ℂ Ω x) h

include hc in
theorem closure_pairing {p : H × H} (hp : p ∈ closure (graph M Ω))
    {b : H →L[ℂ] H} (hb : b ∈ N) :
    inner ℂ p.2 (b Ω) = inner ℂ ((star b) Ω) p.1 := by
  have hclosed : IsClosed {p : H × H | inner ℂ p.2 (b Ω) = inner ℂ ((star b) Ω) p.1} := by
    apply isClosed_eq <;> fun_prop
  apply closure_minimal (t := {p : H × H | inner ℂ p.2 (b Ω) = inner ℂ ((star b) Ω) p.1}) ?_ hclosed hp
  rintro p ⟨a,ha,rfl⟩
  exact pairing M N Ω hc ha hb

variable (hN : Dense ((fun b : H →L[ℂ] H => b Ω) '' (N : Set (H →L[ℂ] H))))

include hc hN in
theorem closure_functional (x y z : H) (hy : (x,y) ∈ closure (graph M Ω))
    (hz : (x,z) ∈ closure (graph M Ω)) : y = z := by
  apply hN.eq_of_inner_left ℂ
  rintro v ⟨b,hb,rfl⟩
  exact (closure_pairing M N Ω hc hy hb).trans (closure_pairing M N Ω hc hz hb).symm

include hc hN in
theorem closure_vertical (y : H) (hy : (0,y) ∈ closure (graph M Ω)) : y = 0 := by
  apply hN.eq_zero_of_inner_left ℂ
  rintro v ⟨b,hb,rfl⟩
  simpa only [inner_zero_right] using closure_pairing M N Ω hc hy hb

theorem domain_dense (hM : Dense ((fun a : H →L[ℂ] H => a Ω) '' (M : Set (H →L[ℂ] H)))) :
    Dense (Prod.fst '' graph M Ω) := by
  apply Dense.mono ?_ hM
  rintro x ⟨a,ha,rfl⟩
  exact ⟨(a Ω,(star a) Ω),⟨a,ha,rfl⟩,rfl⟩

end F1Fecho.PairTomita
#print axioms F1Fecho.PairTomita.dense_orbit_of_dense_span
#print axioms F1Fecho.PairTomita.pairing
#print axioms F1Fecho.PairTomita.closure_functional
#print axioms F1Fecho.PairTomita.closure_vertical
#print axioms F1Fecho.PairTomita.domain_dense
