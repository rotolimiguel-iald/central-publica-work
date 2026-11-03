import TGLExt.F1Fecho394.RealSubspaceTotalityR5
import Mathlib.Topology.Sequences
/-!
Concrete exponential lift of a self-adjoint one-particle operator on the SAME
constructed Fock space. Its closed graph is the closure of the span of
(e(f),e(Tf)); functionality is proved from the exponential inner kernel and
self-adjointness, not assumed. This supplies an actual graph core.
Self-adjointness/positivity of the CLOSED LIFT, tensor spectral identification,
and equality with the algebra-vacuum Tomita polar operator remain unclaimed.
-/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Filter Topology
namespace F1Fecho.ExponentialLift
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.BosonicSectors
open F1Fecho.Exponential F1Fecho.WedgeExponential

variable (T : H1 →ₗ.[ℂ] H1)

def coreGraph : Submodule ℂ (F × F) :=
  Submodule.span ℂ (Set.range (fun f : T.domain => (exponential f, exponential (T f))))

def closedGraph : Submodule ℂ (F × F) := (coreGraph T).topologicalClosure

theorem domain_complex_dense (hT : Dense (T.domain : Set H1)) :
    (Submodule.span ℂ (T.domain.restrictScalars ℝ : Set H1)).topologicalClosure = ⊤ := by
  change (Submodule.span ℂ (T.domain : Set H1)).topologicalClosure = ⊤
  rw [Submodule.span_eq]
  exact Submodule.dense_iff_topologicalClosure_eq_top.mp hT

theorem exponential_domain_total (hT : Dense (T.domain : Set H1)) :
    (Submodule.span ℂ (exponential '' (T.domain : Set H1))).topologicalClosure = ⊤ :=
  exponential_real_subspace_total (T.domain.restrictScalars ℝ) (domain_complex_dense T hT)

theorem one_particle_pairing (hT : IsSelfAdjoint T) (f g : T.domain) :
    inner ℂ (T f) (g : H1) = inner ℂ (f : H1) (T g) := by
  have h := LinearPMap.adjoint_isFormalAdjoint (T := T) hT.dense_domain
  rw [LinearPMap.isSelfAdjoint_def.mp hT] at h
  exact h f g

theorem exponential_pairing (hT : IsSelfAdjoint T) (f g : T.domain) :
    inner ℂ (exponential (T f)) (exponential g) =
      inner ℂ (exponential f) (exponential (T g)) := by
  rw [exponential_inner,exponential_inner,one_particle_pairing T hT f g]

theorem core_pairing (hT : IsSelfAdjoint T) (p : F × F) (hp : p ∈ coreGraph T)
    (g : T.domain) : inner ℂ p.2 (exponential g) = inner ℂ p.1 (exponential (T g)) := by
  induction hp using Submodule.span_induction with
  | mem p hp =>
    obtain ⟨f,rfl⟩ := hp
    exact exponential_pairing T hT f g
  | zero => simp
  | add p q hp hq ihp ihq => simpa only [Prod.snd_add,Prod.fst_add,inner_add_left] using congrArg₂ (·+·) ihp ihq
  | smul c p hp ih =>
    change inner ℂ (c • p.2) (exponential g) = inner ℂ (c • p.1) (exponential (T g))
    rw [inner_smul_left,inner_smul_left,ih]

theorem closed_pairing (hT : IsSelfAdjoint T) (p : F × F) (hp : p ∈ closedGraph T)
    (g : T.domain) : inner ℂ p.2 (exponential g) = inner ℂ p.1 (exponential (T g)) := by
  have hc : IsClosed {q : F × F |
      inner ℂ q.2 (exponential g) = inner ℂ q.1 (exponential (T g))} :=
    isClosed_eq (continuous_snd.inner continuous_const) (continuous_fst.inner continuous_const)
  apply closure_minimal (fun q hq => core_pairing T hT q hq g) hc
  rw [← Submodule.topologicalClosure_coe]
  exact hp

theorem closedGraph_functional (hT : IsSelfAdjoint T) (x y z : F)
    (hy : (x,y) ∈ closedGraph T) (hz : (x,z) ∈ closedGraph T) : y = z := by
  apply sub_eq_zero.mp
  apply exponential_real_subspace_orthogonal_zero (T.domain.restrictScalars ℝ)
    (domain_complex_dense T hT.dense_domain) (y-z)
  intro g hg
  have hp : (0,y-z) ∈ closedGraph T := by simpa only [Prod.mk_sub_mk,sub_self] using (closedGraph T).sub_mem hy hz
  have h := closed_pairing T hT (0,y-z) hp ⟨g,hg⟩
  simpa only [inner_zero_left] using h

def closedDomain : Submodule ℂ F where
  carrier := {x | ∃ y, (x,y) ∈ closedGraph T}
  zero_mem' := ⟨0,(closedGraph T).zero_mem⟩
  add_mem' := by
    rintro x z ⟨y,hy⟩ ⟨w,hw⟩
    exact ⟨y+w,(closedGraph T).add_mem hy hw⟩
  smul_mem' := by
    rintro c x ⟨y,hy⟩
    exact ⟨c•y,(closedGraph T).smul_mem c hy⟩

def closedValue (x : closedDomain T) : F := Classical.choose x.property

theorem closedValue_graph (x : closedDomain T) :
    ((x : F),closedValue T x) ∈ closedGraph T := Classical.choose_spec x.property

def closedLift (hT : IsSelfAdjoint T) : F →ₗ.[ℂ] F where
  domain := closedDomain T
  toFun :=
    { toFun := closedValue T
      map_add' := fun x z => closedGraph_functional T hT _ _ _
        (closedValue_graph T (x+z)) ((closedGraph T).add_mem (closedValue_graph T x) (closedValue_graph T z))
      map_smul' := fun c x => closedGraph_functional T hT _ _ _
        (closedValue_graph T (c•x)) ((closedGraph T).smul_mem c (closedValue_graph T x)) }

theorem closedLift_graph_eq (hT : IsSelfAdjoint T) : (closedLift T hT).graph = closedGraph T := by
  ext p
  rw [LinearPMap.mem_graph_iff']
  constructor
  · rintro ⟨x,rfl⟩
    exact closedValue_graph T x
  · intro hp
    let x : closedDomain T := ⟨p.1,p.2,hp⟩
    refine ⟨x,?_⟩
    apply Prod.ext
    · rfl
    · exact closedGraph_functional T hT p.1 _ p.2 (closedValue_graph T x) hp

theorem closedLift_isClosed (hT : IsSelfAdjoint T) :
    IsClosed ((closedLift T hT).graph : Set (F × F)) := by
  rw [closedLift_graph_eq]
  exact (coreGraph T).isClosed_topologicalClosure

theorem exponential_mem_domain (f : T.domain) : exponential f ∈ closedDomain T := by
  refine ⟨exponential (T f),?_⟩
  exact (coreGraph T).le_topologicalClosure (Submodule.subset_span ⟨f,rfl⟩)

theorem closedLift_exponential (hT : IsSelfAdjoint T) (f : T.domain) :
    closedLift T hT ⟨exponential f,exponential_mem_domain T f⟩ = exponential (T f) := by
  apply closedGraph_functional T hT (exponential f)
  · exact closedValue_graph T ⟨exponential f,exponential_mem_domain T f⟩
  · exact (coreGraph T).le_topologicalClosure (Submodule.subset_span ⟨f,rfl⟩)

theorem closedLift_exponential_sector (hT : IsSelfAdjoint T) (f : T.domain) (n : ℕ) :
    (closedLift T hT ⟨exponential f,exponential_mem_domain T f⟩) n =
      (weight n : ℂ) • pureTensor n (T f) := by
  rw [closedLift_exponential]
  rfl

theorem closedGraph_pairing (hT : IsSelfAdjoint T) (p q : F × F)
    (hp : p ∈ closedGraph T) (hq : q ∈ closedGraph T) :
    inner ℂ p.2 q.1 = inner ℂ p.1 q.2 := by
  have hcore : ∀ z ∈ coreGraph T, inner ℂ p.2 z.1 = inner ℂ p.1 z.2 := by
    intro z hz
    induction hz using Submodule.span_induction with
    | mem z hz =>
      obtain ⟨g,rfl⟩ := hz
      exact closed_pairing T hT p hp g
    | zero => simp
    | add z w hz hw ihz ihw =>
      change inner ℂ p.2 (z.1+w.1) = inner ℂ p.1 (z.2+w.2)
      rw [inner_add_right,inner_add_right,ihz,ihw]
    | smul c z hz ih =>
      change inner ℂ p.2 (c•z.1) = inner ℂ p.1 (c•z.2)
      rw [inner_smul_right,inner_smul_right,ih]
  have hc : IsClosed {z : F × F | inner ℂ p.2 z.1 = inner ℂ p.1 z.2} :=
    isClosed_eq (continuous_const.inner continuous_fst) (continuous_const.inner continuous_snd)
  apply closure_minimal hcore hc
  rw [← Submodule.topologicalClosure_coe]
  exact hq

theorem closedLift_isFormalAdjoint (hT : IsSelfAdjoint T) :
    (closedLift T hT).IsFormalAdjoint (closedLift T hT) := by
  intro x y
  exact closedGraph_pairing T hT ((x : F),closedLift T hT x)
    ((y : F),closedLift T hT y) (closedValue_graph T x) (closedValue_graph T y)

theorem closedDomain_dense (hT : IsSelfAdjoint T) : Dense (closedDomain T : Set F) := by
  have hs : Submodule.span ℂ (exponential '' (T.domain : Set H1)) ≤ closedDomain T := by
    apply Submodule.span_le.mpr
    rintro x ⟨f,hf,rfl⟩
    exact exponential_mem_domain T ⟨f,hf⟩
  apply Submodule.dense_iff_topologicalClosure_eq_top.mpr
  apply le_antisymm le_top
  rw [← exponential_domain_total T hT.dense_domain]
  exact Submodule.topologicalClosure_mono hs

/-- Actual graph-core conclusion: approximation in BOTH graph coordinates. -/
theorem core_graph_sequence (hT : IsSelfAdjoint T) (x : (closedLift T hT).domain) :
    ∃ u : ℕ → F × F, (∀ n, u n ∈ coreGraph T) ∧
      Tendsto u atTop (𝓝 ((x : F),closedLift T hT x)) := by
  have hp : ((x : F),closedLift T hT x) ∈ closedGraph T := closedValue_graph T x
  have hc : ((x : F),closedLift T hT x) ∈ closure (coreGraph T : Set (F × F)) := by
    rw [← Submodule.topologicalClosure_coe]
    exact hp
  exact mem_closure_iff_seq_limit.mp hc

def canonicalLift : F →ₗ.[ℂ] F :=
  closedLift F1Rede.CanonicalWedge.TW F1Rede.CanonicalWedge.TW_selfadjoint

theorem canonicalLift_closed : IsClosed (canonicalLift.graph : Set (F × F)) :=
  closedLift_isClosed _ _

theorem canonicalLift_dense : Dense (canonicalLift.domain : Set F) :=
  closedDomain_dense _ F1Rede.CanonicalWedge.TW_selfadjoint

theorem canonicalLift_exponential (f : F1Rede.CanonicalWedge.TW.domain) :
    canonicalLift ⟨exponential f,exponential_mem_domain _ f⟩ =
      exponential (F1Rede.CanonicalWedge.TW f) := closedLift_exponential _ _ f

end F1Fecho.ExponentialLift
#print axioms F1Fecho.ExponentialLift.closedGraph_functional
#print axioms F1Fecho.ExponentialLift.closedLift
#print axioms F1Fecho.ExponentialLift.closedLift_graph_eq
#print axioms F1Fecho.ExponentialLift.closedLift_isClosed
#print axioms F1Fecho.ExponentialLift.closedLift_exponential
#print axioms F1Fecho.ExponentialLift.closedLift_exponential_sector
#print axioms F1Fecho.ExponentialLift.closedDomain_dense
#print axioms F1Fecho.ExponentialLift.core_graph_sequence
#print axioms F1Fecho.ExponentialLift.canonicalLift_closed
#print axioms F1Fecho.ExponentialLift.canonicalLift_dense
#print axioms F1Fecho.ExponentialLift.canonicalLift_exponential

#print axioms F1Fecho.ExponentialLift.closedLift_isFormalAdjoint
