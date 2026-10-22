import TGLExt.F1Fecho394.VectorWedge
set_option autoImplicit false
set_option maxHeartbeats 600000
noncomputable section
open MeasureTheory Filter
namespace F1Rede.Wedge
open ChatgptAudit.Continuous049 ChatgptAudit.Continuous050
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem T_apply_ae (c : ℝ) (f : (T (H := H) c).domain) :
    T c f =ᵐ[volume] fun x => (Real.exp (-c*x) : ℂ) • (f : VH H) x :=
  (T_graph c _ _).mp ((T c).mem_graph f)
theorem T_domain (c : ℝ) (f : VH H) : f ∈ (T c).domain ↔
    MemLp (fun x => (Real.exp (-c*x) : ℂ) • f x) 2 (volume : Measure ℝ) := by
  constructor
  · intro hf
    exact (Lp.memLp (T c ⟨f,hf⟩)).ae_eq (T_apply_ae c ⟨f,hf⟩)
  · intro hf
    have hg := (T_graph c f (hf.toLp _)).mpr hf.coeFn_toLp
    exact LinearPMap.mem_domain_of_mem_graph hg

theorem half_norm_le (c x : ℝ) (z : H) : ‖(Real.exp (-c*x) : ℂ) • z‖ ≤
    ‖z‖ + ‖(Real.exp (-(2*c)*x) : ℂ) • z‖ := by
  simp only [norm_smul,Complex.norm_real,Real.norm_eq_abs,Real.abs_exp]
  rw [continuous_weight_double]
  have h : Real.exp (-c*x) ≤ 1 + Real.exp (-c*x)^2 := by
    nlinarith [sq_nonneg (Real.exp (-c*x) - 1/2)]
  calc
    _ ≤ (1 + Real.exp (-c*x)^2) * ‖z‖ := mul_le_mul_of_nonneg_right h (norm_nonneg z)
    _ = ‖z‖ + Real.exp (-c*x)^2 * ‖z‖ := by ring

theorem T_double_domain_le (c : ℝ) : (T (H := H) (2*c)).domain ≤ (T c).domain := by
  intro f hf
  apply (T_domain c f).mpr
  have h2 := (T_domain (2*c) f).mp hf
  have hdom := (Lp.memLp f).norm.add h2.norm
  have hw : AEStronglyMeasurable (fun x : ℝ => (Real.exp (-c*x) : ℂ) • f x) (volume : Measure ℝ) := by
    have hc : Continuous (fun x : ℝ => (Real.exp (-c*x) : ℂ)) := by fun_prop
    exact hc.aestronglyMeasurable.smul (Lp.aestronglyMeasurable f)
  apply hdom.mono' hw
  exact Eventually.of_forall (fun x => half_norm_le c x (f x))

theorem T_double_graph_iff (c : ℝ) (f g : VH H) : (f,g) ∈ (T (2*c)).graph ↔
    ∃ h : VH H, (f,h) ∈ (T c).graph ∧ (h,g) ∈ (T c).graph := by
  constructor
  · intro hfg
    have hf := T_double_domain_le c (LinearPMap.mem_domain_of_mem_graph hfg)
    let h := T c ⟨f,hf⟩
    refine ⟨h,(T c).mem_graph ⟨f,hf⟩,?_⟩
    apply (T_graph c h g).mpr
    have h1 := T_apply_ae c ⟨f,hf⟩
    have h2 := (T_graph (2*c) f g).mp hfg
    filter_upwards [h1,h2] with x hx hy
    change g x = (Real.exp (-c*x) : ℂ) • (T c ⟨f,hf⟩) x
    rw [hy,hx,continuous_weight_double_complex,mul_smul]
  · rintro ⟨h,hfh,hhg⟩
    apply (T_graph (2*c) f g).mpr
    have h1 := (T_graph c f h).mp hfh
    have h2 := (T_graph c h g).mp hhg
    filter_upwards [h1,h2] with x hx hy
    rw [hy,hx,continuous_weight_double_complex,mul_smul]
#print axioms T_domain
#print axioms T_double_graph_iff
end F1Rede.Wedge