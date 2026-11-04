import TGLExt.F1Fecho394.WedgeAnalyticR2
import TGLExt.F1Fecho394.StandardComplexSpanR1
/-! Exponential totality over a real subspace is proved from density of its
complex span. This supplies a wedge-specific density theorem; it does not
identify the Tomita operator of a von Neumann algebra. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
set_option synthInstance.maxHeartbeats 100000
noncomputable section
open Filter Topology UniformSpace
namespace F1Fecho.WedgeExponential
open TGLExt.ImportedSQ F1Rede.BosonicSectors F1Rede.BosonicFock
open F1Rede.BosonicSectorContinuity F1Fecho.Exponential

def complexification (K : Submodule ℝ H1) : Submodule ℂ H1 where
  carrier := {z | ∃ x ∈ K, ∃ y ∈ K, z = x + Complex.I • y}
  zero_mem' := ⟨0, K.zero_mem, 0, K.zero_mem, by simp⟩
  add_mem' := by
    rintro a b ⟨x,hx,y,hy,rfl⟩ ⟨u,hu,w,hw,rfl⟩
    refine ⟨x+u,K.add_mem hx hu,y+w,K.add_mem hy hw,?_⟩
    module
  smul_mem' := by
    rintro c z ⟨x,hx,y,hy,rfl⟩
    refine ⟨c.re • x - c.im • y, K.sub_mem (K.smul_mem _ hx) (K.smul_mem _ hy),
      c.im • x + c.re • y, K.add_mem (K.smul_mem _ hx) (K.smul_mem _ hy), ?_⟩
    have h1 : (c.re : ℂ) + Complex.I * (c.im : ℂ) = c := by
      simpa only [mul_comm] using Complex.re_add_im c
    have h2 : -(c.im : ℂ) + Complex.I * (c.re : ℂ) = c * Complex.I := by
      apply Complex.ext <;> simp
    symm
    calc
      _ = ((c.re : ℂ) + Complex.I * (c.im : ℂ)) • x +
          (-(c.im : ℂ) + Complex.I * (c.re : ℂ)) • y := by
        simp only [← ofReal_smul_H1]
        module
      _ = c • x + (c * Complex.I) • y := by rw [h1,h2]
      _ = _ := by module

theorem complexification_eq_span (K : Submodule ℝ H1) :
    complexification K = Submodule.span ℂ (K : Set H1) := by
  apply le_antisymm
  · rintro z ⟨x,hx,y,hy,rfl⟩
    exact Submodule.add_mem _ (Submodule.subset_span hx)
      (Submodule.smul_mem _ _ (Submodule.subset_span hy))
  · apply Submodule.span_le.mpr
    intro x hx
    exact ⟨x,hx,0,K.zero_mem,by simp⟩

theorem pure_inner_zero_on_complexification (K : Submodule ℝ H1) (v : F)
    (hv : ∀ x ∈ K, inner ℂ v (exponential x) = 0) (n : ℕ)
    (z : H1) (hz : z ∈ complexification K) :
    inner ℂ (v n) (pureTensor n z) = 0 := by
  obtain ⟨x,hx,y,hy,rfl⟩ := hz
  let P : ℂ → ℂ := fun c => inner ℂ (v n : TensorHilbert n) (pureCompleted n (x+c•y))
  have ha : AnalyticOnNhd ℂ P Set.univ := by
    intro c _
    have hline : AnalyticAt ℂ (fun d : ℂ => x+d•y) c :=
      analyticAt_const.add (analyticAt_id.smul analyticAt_const)
    exact ((innerSL ℂ (v n : TensorHilbert n)).analyticAt _).comp
      ((analytic_pureCompleted n _).comp hline)
  have hr : ∀ t : ℝ, P t = 0 := by
    intro t
    apply pure_inner_zero_on_real_subspace K v hv
    apply K.add_mem hx
    rw [ofReal_smul_H1]
    exact K.smul_mem t hy
  exact analytic_zero_from_real P ha hr Complex.I

theorem exponential_real_subspace_orthogonal_zero (K : Submodule ℝ H1)
    (hK : (Submodule.span ℂ (K : Set H1)).topologicalClosure = ⊤)
    (v : F) (hv : ∀ x ∈ K, inner ℂ v (exponential x) = 0) : v = 0 := by
  apply lp.ext
  funext n
  apply sector_eq_zero_of_pure_inner_zero n (v n)
  intro x
  let P : H1 → ℂ := fun y => inner ℂ (v n : TensorHilbert n) (pureCompleted n y)
  have hc : Continuous P := (innerSL ℂ (v n : TensorHilbert n)).continuous.comp
    (continuous_pureCompleted id continuous_id n)
  have hz : (complexification K : Set H1) ⊆ {y | P y = 0} :=
    fun y hy => pure_inner_zero_on_complexification K v hv n y hy
  have hcl := closure_minimal hz (isClosed_eq hc continuous_const)
  have hd : closure (complexification K : Set H1) = Set.univ := by
    rw [complexification_eq_span, ← Submodule.topologicalClosure_coe, hK]
    rfl
  exact hcl (hd.symm ▸ Set.mem_univ x)

theorem exponential_real_subspace_total (K : Submodule ℝ H1)
    (hK : (Submodule.span ℂ (K : Set H1)).topologicalClosure = ⊤) :
    (Submodule.span ℂ (exponential '' (K : Set H1))).topologicalClosure = ⊤ := by
  apply Submodule.topologicalClosure_eq_top_iff.mpr
  apply le_antisymm _ bot_le
  intro v hv
  change v = 0
  apply exponential_real_subspace_orthogonal_zero K hK v
  intro x hx
  exact (Submodule.mem_orthogonal' _ v).mp hv (exponential x)
    (Submodule.subset_span ⟨x,hx,rfl⟩)

theorem standard_complex_span_dense (K : StandardSubspace H1) :
    (Submodule.span ℂ (K.toClosedSubmodule : Set H1)).topologicalClosure = ⊤ :=
  F1Fecho.StandardComplexSpan.dense K

theorem standard_exponential_total (K : StandardSubspace H1) :
    (Submodule.span ℂ (exponential '' (K.toClosedSubmodule : Set H1))).topologicalClosure = ⊤ :=
  exponential_real_subspace_total K.toClosedSubmodule.toSubmodule (standard_complex_span_dense K)

theorem canonical_wedge_exponential_total :
    (Submodule.span ℂ (exponential ''
      (F1Rede.CanonicalWedge.spectralOutput.KWR.toClosedSubmodule : Set H1))).topologicalClosure = ⊤ :=
  standard_exponential_total F1Rede.CanonicalWedge.spectralOutput.KWR

end F1Fecho.WedgeExponential

#print axioms F1Fecho.WedgeExponential.complexification_eq_span
#print axioms F1Fecho.WedgeExponential.pure_inner_zero_on_complexification
#print axioms F1Fecho.WedgeExponential.exponential_real_subspace_orthogonal_zero
#print axioms F1Fecho.WedgeExponential.exponential_real_subspace_total

#print axioms F1Fecho.WedgeExponential.standard_complex_span_dense
#print axioms F1Fecho.WedgeExponential.standard_exponential_total
#print axioms F1Fecho.WedgeExponential.canonical_wedge_exponential_total
