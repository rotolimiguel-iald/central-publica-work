import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Commute
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Basic
import Mathlib.Analysis.InnerProductSpace.Adjoint
/-! Naturality under a bounded intertwiner, which need not be invertible.
The compact function algebra is generated densely by the coordinate and its
conjugate; no identification of different Hilbert spaces is presumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open Filter Topology
namespace F1Fecho.ContinuousIntertwining
variable {H K:Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
variable {s:Set ℂ} [CompactSpace s]
variable (φ:C(s,ℂ)→⋆ₐ[ℂ](H→L[ℂ]H)) (ψ:C(s,ℂ)→⋆ₐ[ℂ](K→L[ℂ]K))
  (hφ:Continuous φ) (hψ:Continuous ψ) (V:H→L[ℂ]K)

include hφ hψ in
theorem hom_intertwine
    (hgen:V.comp (φ (.restrict s (.id ℂ)))=(ψ (.restrict s (.id ℂ))).comp V)
    (hstar:V.comp (φ (star (.restrict s (.id ℂ))))=(ψ (star (.restrict s (.id ℂ)))).comp V)
    (f:C(s,ℂ)) : V.comp (φ f)=(ψ f).comp V := by
  induction f using ContinuousMap.induction_on_of_compact with
  | const r =>
    change V.comp (φ (algebraMap ℂ C(s,ℂ) r))=(ψ (algebraMap ℂ C(s,ℂ) r)).comp V
    rw [AlgHomClass.commutes,AlgHomClass.commutes]
    ext x
    simp
  | id => exact hgen
  | star_id => exact hstar
  | add f g hf hg =>
    rw [map_add,map_add,ContinuousLinearMap.comp_add,ContinuousLinearMap.add_comp,hf,hg]
  | mul f g hf hg =>
    rw [map_mul,map_mul]
    ext x
    change V (φ f (φ g x))=ψ f (ψ g (V x))
    calc
      _ = ψ f (V (φ g x)) := congrArg (fun M:H→L[ℂ]K=>M (φ g x)) hf
      _ = _ := congrArg (ψ f) (congrArg (fun M:H→L[ℂ]K=>M x) hg)
  | frequently f hf =>
    have hc:IsClosed {g:C(s,ℂ)|V.comp (φ g)=(ψ g).comp V}:=
      isClosed_eq (by fun_prop) (by fun_prop)
    rw [←Set.mem_setOf (p:=fun g:C(s,ℂ)=>V.comp (φ g)=(ψ g).comp V),←hc.closure_eq]
    exact mem_closure_of_frequently_of_tendsto hf tendsto_id

include hφ hψ in
theorem hom_intertwine_selfadjoint
    (hφs:IsSelfAdjoint (φ (.restrict s (.id ℂ))))
    (hψs:IsSelfAdjoint (ψ (.restrict s (.id ℂ))))
    (hgen:V.comp (φ (.restrict s (.id ℂ)))=(ψ (.restrict s (.id ℂ))).comp V)
    (f:C(s,ℂ)) : V.comp (φ f)=(ψ f).comp V := by
  apply hom_intertwine φ ψ hφ hψ V hgen
  rwa [map_star,map_star,hφs.star_eq,hψs.star_eq]

end F1Fecho.ContinuousIntertwining
#print axioms F1Fecho.ContinuousIntertwining.hom_intertwine
#print axioms F1Fecho.ContinuousIntertwining.hom_intertwine_selfadjoint
