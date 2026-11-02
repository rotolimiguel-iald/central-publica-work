import TGLExt.V354NormalizedSplit
import TGL.CoreSupport
import Mathlib.Analysis.InnerProductSpace.LinearPMap

set_option autoImplicit false

namespace TGLV350.Regular
open TGLExt TGLV351 TGL.CoreSupport
noncomputable section

/-- Actual choices from the constructed normalized split, not witness inputs. -/
def regularNormalizedFaces (P : SiteProfile) :
    {qr : PositiveCoreInput P × PositiveCoreInput P //
      IsStarProjection qr.1.val ∧ IsStarProjection qr.2.val ∧ qr.1.val*qr.2.val=0 ∧
      scalarInverseLimitWeight P (qr.1.add qr.2) = 1 ∧
      scalarInverseLimitWeight P qr.1 = scalarInverseLimitWeight P qr.2} := by
  let q := Classical.choose (scalarTrace_normalized_split_exists P)
  let r := Classical.choose (Classical.choose_spec (scalarTrace_normalized_split_exists P))
  exact ⟨(q,r),Classical.choose_spec
    (Classical.choose_spec (scalarTrace_normalized_split_exists P))⟩

def regularFiniteSupport (P : SiteProfile) : PositiveCoreInput P :=
  (regularNormalizedFaces P).val.1.add (regularNormalizedFaces P).val.2

theorem regularFiniteSupport_projection (P : SiteProfile) :
    IsStarProjection (regularFiniteSupport P).val :=
  (regularNormalizedFaces P).property.1.add
    (regularNormalizedFaces P).property.2.1 (regularNormalizedFaces P).property.2.2.1

theorem regularFiniteSupport_trace (P : SiteProfile) :
    scalarInverseLimitWeight P (regularFiniteSupport P) = 1 :=
  (regularNormalizedFaces P).property.2.2.2.1

theorem regularFiniteSupport_ne_zero (P : SiteProfile) :
    (regularFiniteSupport P).val ≠ 0 := by
  intro hz
  have he : regularFiniteSupport P = PositiveCoreInput.zero P := Subtype.ext hz
  have ht := regularFiniteSupport_trace P
  rw [he,scalarInverseLimitWeight_zero] at ht
  exact zero_ne_one ht

/-- CoreSupport's minimal representative, now with constructed support. This
bounded representative is not identified with an unrelated microscopic operator. -/
def regularMinimalLock (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P) :=
  1-(regularFiniteSupport P).val

theorem regularMinimalLock_mem (P : SiteProfile) :
    regularMinimalLock P ∈ regularCoreAlgebra P :=
  (regularCoreAlgebra P).sub_mem (regularCoreAlgebra P).one_mem
    (regularFiniteSupport P).property.1

theorem regularMinimalLock_selfadjoint (P : SiteProfile) :
    IsSelfAdjoint (regularMinimalLock P) :=
  hmin_selfadjoint _ (regularFiniteSupport_projection P).isSelfAdjoint.star_eq

theorem regularMinimalLock_annihilation (P : SiteProfile) :
    (regularFiniteSupport P).val * regularMinimalLock P = 0 :=
  support_annihilates _ (regularFiniteSupport_projection P).isIdempotentElem

theorem regularMinimalLock_maximal (P : SiteProfile)
    (r : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hr : r * regularMinimalLock P = 0) : r * (regularFiniteSupport P).val = r :=
  support_maximal _ _ hr

theorem regularMinimalLock_ker (P : SiteProfile) :
    (regularMinimalLock P).ker = (regularFiniteSupport P).val.range := by
  let q := (regularFiniteSupport P).val
  have hq : q*q=q := (regularFiniteSupport_projection P).isIdempotentElem
  ext x
  change x-q x=0 ↔ ∃ y, q y=x
  constructor
  · intro hx
    exact ⟨x,(sub_eq_zero.mp hx).symm⟩
  · rintro ⟨y,rfl⟩
    have hh := congrArg (fun A : RegularHilbert (TowerHilbert P) →L[ℂ] _ => A y) hq
    exact sub_eq_zero.mpr hh.symm

/-- Literal Hilbert projection of the zero spectral subspace. -/
theorem regularMinimalLock_spectral_zero (P : SiteProfile) :
    (regularMinimalLock P).ker.starProjection = (regularFiniteSupport P).val := by
  obtain ⟨_,he⟩ := isStarProjection_iff_eq_starProjection_range.mp
    (regularFiniteSupport_projection P)
  simpa only [regularMinimalLock_ker] using he.symm

/-- Unit relative gap on the orthogonal complement of the kernel. -/
theorem regularMinimalLock_relative_gap (P : SiteProfile)
    (x : RegularHilbert (TowerHilbert P)) (hx : x ∈ (regularMinimalLock P).kerᗮ) :
    ‖regularMinimalLock P x‖ = ‖x‖ := by
  rw [regularMinimalLock_ker,ContinuousLinearMap.orthogonal_range] at hx
  have hs : (regularFiniteSupport P).val.adjoint = (regularFiniteSupport P).val :=
    (regularFiniteSupport_projection P).isSelfAdjoint.star_eq
  rw [hs] at hx
  change (regularFiniteSupport P).val x=0 at hx
  change ‖x-(regularFiniteSupport P).val x‖=‖x‖
  rw [hx,sub_zero]

/-- Full-domain graph of the bounded minimal representative. -/
def regularMinimalLockGraph (P : SiteProfile) := (regularMinimalLock P).toPMap ⊤

theorem regularMinimalLockGraph_selfadjoint (P : SiteProfile) :
    IsSelfAdjoint (regularMinimalLockGraph P) := by
  change ((regularMinimalLock P).toPMap ⊤).adjoint = (regularMinimalLock P).toPMap ⊤
  rw [ContinuousLinearMap.toPMap_adjoint_eq_adjoint_toPMap_of_dense _
    (by simpa only [Submodule.top_coe] using (dense_univ : Dense (Set.univ : Set (RegularHilbert (TowerHilbert P)))))]
  exact congrArg (fun A : RegularHilbert (TowerHilbert P) →L[ℂ] _ => A.toPMap ⊤)
    (regularMinimalLock_selfadjoint P).star_eq

theorem regularMinimalLockGraph_closed (P : SiteProfile) :
    (regularMinimalLockGraph P).IsClosed := (regularMinimalLockGraph_selfadjoint P).isClosed

theorem regularMinimalLockGraph_domain (P : SiteProfile) :
    (regularMinimalLockGraph P).domain = ⊤ := rfl

/-- Affiliation by invariance of the actual graph under every bounded member
of the commutant. The domain is all H, explicitly recorded above. -/
theorem regularMinimalLockGraph_affiliated (P : SiteProfile)
    (B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hB : B ∈ (regularCoreAlgebra P).commutant)
    (x y : RegularHilbert (TowerHilbert P))
    (hxy : (x,y) ∈ (regularMinimalLockGraph P).graph) :
    (B x,B y) ∈ (regularMinimalLockGraph P).graph := by
  have he : regularMinimalLock P x=y := by
    rcases (LinearPMap.mem_graph_iff _).mp hxy with ⟨z,hz,hy⟩
    change regularMinimalLock P z.val=y at hy
    rwa [hz] at hy
  have hc := (VonNeumannAlgebra.mem_commutant_iff.mp hB) _ (regularMinimalLock_mem P)
  apply (LinearPMap.mem_graph_iff _).mpr
  refine ⟨⟨B x,Submodule.mem_top⟩,rfl,?_⟩
  change regularMinimalLock P (B x)=B y
  have h := congrArg (fun A : RegularHilbert (TowerHilbert P) →L[ℂ] _ => A x) hc
  change regularMinimalLock P (B x)=B (regularMinimalLock P x) at h
  rwa [he] at h

#print axioms regularNormalizedFaces
#print axioms regularFiniteSupport_trace
#print axioms regularMinimalLock_spectral_zero
#print axioms regularMinimalLock_relative_gap
#print axioms regularMinimalLockGraph_selfadjoint
#print axioms regularMinimalLockGraph_closed
#print axioms regularMinimalLockGraph_affiliated
end
end TGLV350.Regular
