import TGLExt.F1Fecho394.WeylExponentialGraphCoreR4
import TGLExt.F1Fecho394.WedgePairTomitaR2
/-! One inclusion of ACTUAL graphs: Sexp is a restriction of the closed
Tomita operator of R(KWR), vacuum. Reverse inclusion is not assumed or asserted. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.ExponentialTomitaInclusion
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.ExponentialLift F1Fecho.ExponentialTomita F1Fecho.WeylExponentialCore
open F1Rede.CanonicalWedge F1Fecho.WeylCoefficients F1Fecho.WedgePairTomita

/-- Transport the output of the actual pair Tomita by Gamma(J), producing a linear map. -/
def pairLift : F →ₗ.[ℂ] F where
  domain := domain KWR
  toFun :=
    { toFun := fun x => JF (S KWR x)
      map_add' := by intro x y; rw [map_add,map_add]
      map_smul' := by
        intro c x
        rw [(S KWR).map_smulₛₗ,JF.map_smulₛₗ]
        simp }

theorem pairLift_graph_iff (p : F × F) : p ∈ pairLift.graph ↔
    (p.1,JF p.2) ∈ Set.range (fun x : domain KWR => ((x:F),S KWR x)) := by
  rw [LinearPMap.mem_graph_iff']
  constructor
  · rintro ⟨x,rfl⟩
    refine ⟨x,?_⟩
    apply Prod.ext
    · rfl
    · change S KWR x = JF (JF (S KWR x))
      exact (F1Fecho.Antilinear.canonicalFockJ_involutive _).symm
  · rintro ⟨x,hx⟩
    refine ⟨x,?_⟩
    apply Prod.ext
    · have h1 : (x:F) = p.1 := congrArg Prod.fst hx
      exact h1
    · change JF (S KWR x) = p.2
      have h2 : S KWR x = JF p.2 := congrArg Prod.snd hx
      rw [h2]
      exact F1Fecho.Antilinear.canonicalFockJ_involutive p.2

theorem pairLift_closed : IsClosed (pairLift.graph : Set (F × F)) := by
  have he : (pairLift.graph : Set (F × F)) =
      (fun p : F × F => (p.1,JF p.2)) ⁻¹'
        Set.range (fun x : domain KWR => ((x:F),S KWR x)) := by
    ext p; exact pairLift_graph_iff p
  rw [he]
  exact (S_closed KWR).preimage (continuous_fst.prodMk (JF.continuous.comp continuous_snd))

theorem vacuum_amplitude_star (f : H1) : star (amplitude f 0) = amplitude f 0 := by
  rw [amplitude_norm_form]
  simp only [inner_zero_right,sub_zero,Complex.star_def,← Complex.exp_conj,map_neg,map_div₀,
    map_pow,Complex.conj_ofReal,map_ofNat]

theorem vacuum_amplitude_neg (f : H1) : amplitude (-f) 0 = amplitude f 0 := by
  simp only [amplitude,inner_neg_left,inner_neg_right,neg_neg,inner_zero_right,neg_zero]

theorem weyl_pair_mem (k : K) :
    (exponential (Complex.I•(k:H1)),exponential (Complex.I•Jcandidate k)) ∈ pairLift.graph := by
  let q := amplitude (Complex.I•(k:H1)) 0
  have hq : q ≠ 0 := amplitude_ne_zero _ _
  let u : domain KWR := ⟨FieldWeyl.W k vacuum,
    algebra_vector_domain KWR (FieldWeyl.W k) (FieldWeyl.W_mem_R _ k k.property)⟩
  have hu : (u:F) = q • exponential (Complex.I•(k:H1)) := FieldWeyl.W_vacuum k
  have hg : pairLift u = q • exponential (Complex.I•Jcandidate k) := by
    change JF (S KWR u) = _
    rw [S_Weyl_vector KWR (k:H1) k.property,FieldWeyl.W_vacuum]
    change JF (amplitude (Complex.I•(-(k:H1))) 0 • exponential (Complex.I•(-(k:H1)))) = _
    rw [smul_neg,vacuum_amplitude_neg,JF.map_smulₛₗ]
    change star q • JF (exponential (-(Complex.I•(k:H1)))) = _
    rw [vacuum_amplitude_star,JF_exponential,map_neg,Jcandidate.map_smulₛₗ]
    simp only [Complex.conj_I,neg_smul,neg_neg]
    rfl
  have hm : q • (exponential (Complex.I•(k:H1)),exponential (Complex.I•Jcandidate k)) ∈ pairLift.graph := by
    have h := pairLift.mem_graph u
    rw [hu,hg] at h
    exact h
  have h := pairLift.graph.smul_mem q⁻¹ hm
  simpa only [smul_smul,inv_mul_cancel₀ hq,one_smul] using h

theorem lift_graph_inclusion : closedGraph TW ≤ pairLift.graph := by
  rw [← weylCore_closure_eq]
  apply weylCore.topologicalClosure_minimal _ pairLift_closed
  apply Submodule.span_le.mpr
  rintro p ⟨k,rfl⟩
  exact weyl_pair_mem k

theorem Sexp_domain_inclusion (x : canonicalLift.domain) : (x:F) ∈ domain KWR := by
  have h := lift_graph_inclusion (closedValue_graph TW x)
  obtain ⟨u,hu⟩ := pairLift.mem_graph_iff'.mp h
  have he : (u:F) = (x:F) := congrArg Prod.fst hu
  have hp : (u:F) ∈ domain KWR := u.property
  rw [he] at hp
  exact hp

theorem Sexp_eq_pair_on_domain (x : canonicalLift.domain) :
    S KWR ⟨(x:F),Sexp_domain_inclusion x⟩ = Sexp x := by
  have h := lift_graph_inclusion (closedValue_graph TW x)
  obtain ⟨u,hu⟩ := pairLift.mem_graph_iff'.mp h
  have he : (⟨(x:F),Sexp_domain_inclusion x⟩ : domain KWR) = u :=
    Subtype.ext (congrArg Prod.fst hu).symm
  rw [he]
  apply JF.injective
  change JF (S KWR u) = JF (JF (canonicalLift x))
  rw [F1Fecho.Antilinear.canonicalFockJ_involutive]
  exact congrArg Prod.snd hu

theorem Sexp_graph_subset_pair_graph :
    Set.range (fun x : canonicalLift.domain => ((x:F),Sexp x)) ⊆
      Set.range (fun x : domain KWR => ((x:F),S KWR x)) := by
  rintro p ⟨x,rfl⟩
  refine ⟨⟨(x:F),Sexp_domain_inclusion x⟩,?_⟩
  exact Prod.ext rfl (Sexp_eq_pair_on_domain x)

end F1Fecho.ExponentialTomitaInclusion
#print axioms F1Fecho.ExponentialTomitaInclusion.pairLift_closed
#print axioms F1Fecho.ExponentialTomitaInclusion.weyl_pair_mem
#print axioms F1Fecho.ExponentialTomitaInclusion.lift_graph_inclusion
#print axioms F1Fecho.ExponentialTomitaInclusion.Sexp_domain_inclusion
#print axioms F1Fecho.ExponentialTomitaInclusion.Sexp_eq_pair_on_domain
#print axioms F1Fecho.ExponentialTomitaInclusion.Sexp_graph_subset_pair_graph
