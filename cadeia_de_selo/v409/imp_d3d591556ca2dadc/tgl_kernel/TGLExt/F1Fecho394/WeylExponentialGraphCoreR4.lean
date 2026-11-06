import TGLExt.F1Fecho394.PairedExponentialClosureR4
/-! The Weyl exponential pairs form an actual graph core of canonicalLift.
This proves approximation in both coordinates. It does not by itself prove
maximality or equality with the closed Tomita graph of the von Neumann algebra. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open Filter Topology
namespace F1Fecho.WeylExponentialCore
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.ExponentialLift F1Fecho.ExponentialTomita F1Fecho.PairedExponential
open F1Fecho.WedgeExponential F1Rede.CanonicalWedge
open ChatgptAudit.Continuous049 AuditF13v31

abbrev K := KWR.toClosedSubmodule.toSubmodule

theorem J_real (t : ℝ) (x : H1) : Jcandidate (t•x) = t•Jcandidate x := by
  rw [← ofReal_smul_H1,← ofReal_smul_H1,Jcandidate.map_smulₛₗ]
  change ((starRingEnd ℂ) (t:ℂ)) • Jcandidate x = (t:ℂ) • Jcandidate x
  simp

theorem K_domain (x : H1) (hx : x ∈ K) : x ∈ TW.domain := ((KWR_mem x).mp hx).choose

theorem TW_K (x : H1) (hx : x ∈ K) : TW ⟨x,K_domain x hx⟩ = Jcandidate x := by
  have hs := ((KWR_mem x).mp hx).choose_spec
  have h := congrArg Jcandidate hs
  change Jcandidate (Jcandidate (TW ⟨x,K_domain x hx⟩)) = Jcandidate x at h
  exact (Jcandidate_involutive _).symm.trans h

def realCore : Submodule ℂ (F × F) := pairCore K Jcandidate

theorem realCore_le_core : realCore ≤ coreGraph TW := by
  apply Submodule.span_le.mpr
  rintro p ⟨x,hx,rfl⟩
  have h : (exponential x,exponential (TW ⟨x,K_domain x hx⟩)) ∈ coreGraph TW :=
    Submodule.subset_span ⟨⟨x,K_domain x hx⟩,rfl⟩
  rw [TW_K x hx] at h
  exact h

theorem core_le_realClosure : coreGraph TW ≤ realCore.topologicalClosure := by
  apply Submodule.span_le.mpr
  rintro p ⟨f,rfl⟩
  obtain ⟨h,k,hh,hk,hf,hs⟩ :=
    domain_fixed_decomposition TW.domain (SW TW Jcandidate) SW_maps SW_involutive f
  change h ∈ K at hh
  change k ∈ K at hk
  have ht : TW f = Jcandidate h + Complex.I • Jcandidate k := by
    have he : f = (⟨h,K_domain h hh⟩ : TW.domain) + Complex.I • ⟨k,K_domain k hk⟩ :=
      Subtype.ext hf
    rw [he]
    change TW.toFun (⟨h,K_domain h hh⟩ + Complex.I • ⟨k,K_domain k hk⟩) = _
    rw [map_add,map_smul]
    change TW ⟨h,K_domain h hh⟩ + Complex.I • TW ⟨k,K_domain k hk⟩ = _
    rw [TW_K h hh,TW_K k hk]
  have hm := complexification_pair_mem_closure K Jcandidate (fun x y => map_add Jcandidate x y)
    J_real h k hh hk
  change (exponential (h+Complex.I•k),exponential (Jcandidate h+Complex.I•Jcandidate k)) ∈
    realCore.topologicalClosure at hm
  rw [← hf,← ht] at hm
  exact hm

theorem realCore_closure_eq : realCore.topologicalClosure = closedGraph TW := by
  apply le_antisymm
  · exact Submodule.topologicalClosure_mono realCore_le_core
  · exact (coreGraph TW).topologicalClosure_minimal core_le_realClosure realCore.isClosed_topologicalClosure

def weylCore : Submodule ℂ (F × F) :=
  Submodule.span ℂ (Set.range (fun k : K =>
    (exponential (Complex.I•(k:H1)),exponential (Complex.I•Jcandidate k))))

theorem weylCore_le_core : weylCore ≤ coreGraph TW := by
  apply Submodule.span_le.mpr
  rintro p ⟨k,rfl⟩
  let f : TW.domain := Complex.I • ⟨(k:H1),K_domain k k.property⟩
  have ht : TW f = Complex.I • Jcandidate k := by
    change TW (Complex.I • (⟨(k:H1),K_domain k k.property⟩ : TW.domain)) = _
    change TW.toFun (Complex.I • (⟨(k:H1),K_domain k k.property⟩ : TW.domain)) = _
    rw [map_smul]
    change Complex.I • TW ⟨(k:H1),K_domain k k.property⟩ = _
    rw [TW_K (k:H1) k.property]
  have hm : (exponential (f:H1),exponential (TW f)) ∈ coreGraph TW :=
    Submodule.subset_span ⟨f,rfl⟩
  rw [ht] at hm
  exact hm

theorem realCore_le_weylClosure : realCore ≤ weylCore.topologicalClosure := by
  apply Submodule.span_le.mpr
  rintro p ⟨k,hk,rfl⟩
  have hr : ∀ t : ℝ, (exponential ((t:ℂ)•(Complex.I•k)),
      exponential ((t:ℂ)•(Complex.I•Jcandidate k))) ∈ weylCore.topologicalClosure := by
    intro t
    have ht : t•k ∈ K := K.smul_mem t hk
    have hm : (exponential (Complex.I•(t•k)),exponential (Complex.I•Jcandidate (t•k))) ∈ weylCore :=
      Submodule.subset_span ⟨⟨t•k,ht⟩,rfl⟩
    rw [J_real] at hm
    have hswap (x : H1) : Complex.I•(t•x) = (t:ℂ)•(Complex.I•x) := by
      rw [← ofReal_smul_H1,smul_smul,smul_smul,mul_comm]
    rw [hswap,hswap] at hm
    exact weylCore.le_topologicalClosure hm
  have hm := complex_ray_mem_closed weylCore.topologicalClosure weylCore.isClosed_topologicalClosure
    (Complex.I•k) (Complex.I•Jcandidate k) hr (-Complex.I)
  simp only [smul_smul,neg_mul,Complex.I_mul_I,neg_neg,one_smul] at hm
  change (exponential k,exponential (Jcandidate k)) ∈ weylCore.topologicalClosure
  exact hm

theorem weylCore_closure_eq : weylCore.topologicalClosure = closedGraph TW := by
  apply le_antisymm
  · exact Submodule.topologicalClosure_mono weylCore_le_core
  · rw [← realCore_closure_eq]
    exact realCore.topologicalClosure_minimal realCore_le_weylClosure weylCore.isClosed_topologicalClosure

/-- Simultaneous approximation of input and output by Weyl exponential pairs. -/
theorem weyl_graph_core_sequence (x : canonicalLift.domain) :
    ∃ u : ℕ → F × F, (∀ n, u n ∈ weylCore) ∧
      Tendsto u atTop (𝓝 ((x:F),canonicalLift x)) := by
  have h : ((x:F),canonicalLift x) ∈ weylCore.topologicalClosure := by
    rw [weylCore_closure_eq]
    exact closedValue_graph TW x
  apply mem_closure_iff_seq_limit.mp
  rw [← Submodule.topologicalClosure_coe]
  exact h

end F1Fecho.WeylExponentialCore
#print axioms F1Fecho.WeylExponentialCore.realCore_closure_eq
#print axioms F1Fecho.WeylExponentialCore.weylCore_closure_eq
#print axioms F1Fecho.WeylExponentialCore.weyl_graph_core_sequence
