import TGLExt.F1Fecho394.FibreRootGraphR3

/-! Domain-exact lifting of a closed positive graph to Lebesgue L2.
Both coefficient functions are required to belong to L2; no domain is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open MeasureTheory
namespace F1Fecho.FibreRootPointwise
open TGLV350.Regular ChatgptAudit.Continuous049
open F1Fecho.FibreModularCalculus F1Fecho.FibreRootGraph
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
local instance operatorRealModule : Module ℝ (RegularHilbert H →L[ℂ] RegularHilbert H) :=
  Module.restrictScalars ℝ ℂ (RegularHilbert H →L[ℂ] RegularHilbert H)

theorem fibre_complement (R:H→L[ℂ]H) : fibre (1-R)=1-fibre R := by
  have h:=map_sub (fibreRepresentation (H:=H)) (1:H→L[ℂ]H) R
  change fibre (1-R)=fibre 1-fibre R at h
  simpa only [fibre_one] using h

theorem root_graph_ae (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1)
    (hi:Function.Injective R) (f g:RegularHilbert H) :
    (f,g)∈(liftedRoot R hR hi).graph ↔
      ∀ᵐ a:ℝ ∂volume,(f a,g a)∈(resolventSquareRoot R hR hi).graph := by
  have hs1 : CFC.sqrt (fibre R)=fibre (CFC.sqrt R) := (fibre_sqrt R hR).symm
  have hs2 : CFC.sqrt (1-fibre R)=fibre (CFC.sqrt (1-R)) := by
    rw [←fibre_complement,←fibre_sqrt _ (sub_nonneg.mpr h1)]
  have he : (f,g)∈(liftedRoot R hR hi).graph ↔
      fibre (CFC.sqrt (1-R)) f=fibre (CFC.sqrt R) g := by
    unfold liftedRoot resolventSquareRoot
    rw [bounded_graph_equation_iff _ _ _ (resolvent_sqrt_pair_commute (fibre R))
      (resolvent_sqrt_pair_square_sum (fibre R) (fibre_nonneg hR) (lifted_le_one R h1)),hs1,hs2]
  rw [he]
  constructor
  · intro h
    filter_upwards [fibre_ae (CFC.sqrt (1-R)) f,fibre_ae (CFC.sqrt R) g] with a hf hg
    apply (bounded_graph_equation_iff _ _ _ (resolvent_sqrt_pair_commute R)
      (resolvent_sqrt_pair_square_sum R hR h1) _ _).mpr
    rw [←hf,←hg,h]
  · intro h
    apply Lp.ext
    filter_upwards [h,fibre_ae (CFC.sqrt (1-R)) f,fibre_ae (CFC.sqrt R) g] with a ha hf hg
    rw [hf,hg]
    exact (bounded_graph_equation_iff _ _ _ (resolvent_sqrt_pair_commute R)
      (resolvent_sqrt_pair_square_sum R hR h1) _ _).mp ha
end F1Fecho.FibreRootPointwise
#print axioms F1Fecho.FibreRootPointwise.fibre_complement
#print axioms F1Fecho.FibreRootPointwise.root_graph_ae
