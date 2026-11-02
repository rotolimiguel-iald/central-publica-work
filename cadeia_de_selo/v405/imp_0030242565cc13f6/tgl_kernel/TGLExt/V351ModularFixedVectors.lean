import TGLExt.V351AverageFixedPair
import TGLExt.V351ResolventImaginaryIntertwining
import TGLExt.V351ScalarTomitaImaginaryPowers
import Mathlib.Analysis.InnerProductSpace.LinearMap

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section

/-- Read the existing damped functional calculus on a half-eigenvector.
The rank-one map is only an intertwiner, not a replacement representation. -/
private theorem phase_at_half {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (x : H)
    (hx : T x = (1/2 : ℂ) • x) (t : ℝ) :
    resolventPhaseOperator T t x = (1/4 : ℂ) • x := by
  by_cases hz : x = 0
  · simp [hz]
  let L : H →L[ℂ] H := InnerProductSpace.rankOne ℂ x x
  let Q : H →L[ℂ] H := algebraMap ℂ (H →L[ℂ] H) (1/2)
  have hQ : IsSelfAdjoint Q := by
    change star (algebraMap ℂ (H →L[ℂ] H) (1/2)) = _
    rw [← algebraMap_star_comm]
    norm_num [Q]
  have hL : T*L = L*Q := by
    ext1 y
    change T ((inner ℂ x y) • x) =
      (inner ℂ x ((1/2 : ℂ) • y)) • x
    rw [map_smul,hx,inner_smul_right,smul_smul]
    congr 1
    ring
  have hp : resolventPhaseOperator Q t =
      algebraMap ℂ (H →L[ℂ] H) (1/4) := by
    change cfc (fun z : ℂ => resolventPhaseFunction t z.re)
      (algebraMap ℂ (H →L[ℂ] H) (1/2)) = _
    rw [cfc_algebraMap]
    congr 1
    norm_num [resolventPhaseFunction,resolventDamping,modularPhase]
  have he := congrArg (fun B : H →L[ℂ] H => B x)
    (resolventPhaseOperator_intertwines T Q L hT hQ hL t)
  rw [hp] at he
  change resolventPhaseOperator T t ((inner ℂ x x) • x) =
    (inner ℂ x ((1/4 : ℂ) • x)) • x at he
  rw [map_smul,inner_smul_right] at he
  apply smul_right_injective H (inner_self_ne_zero.mpr hz : inner ℂ x x ≠ 0)
  calc
    _ = ((1/4 : ℂ) * inner ℂ x x) • x := he
    _ = _ := by
      dsimp only
      rw [smul_smul,mul_comm]

/-- Actual simultaneous fixed vectors of S and F are fixed by the already
constructed imaginary powers of their composition, with both domains checked. -/
theorem scalarTomitaImaginaryPower_fixed_of_fixed_pair (P : SiteProfile)
    (x : ScalarGNSHilbert P)
    (hS : x ∈ scalarClosedTomitaDomain P)
    (hF : x ∈ scalarTomitaAdjointDomain P)
    (hxS : scalarClosedTomita P ⟨x,hS⟩ = x)
    (hxF : scalarTomitaAdjoint P ⟨x,hF⟩ = x) (t : ℝ) :
    scalarTomitaImaginaryPower P t x = x := by
  have hD : x ∈ (scalarTomitaSquare P).domain :=
    (scalarTomitaSquare_domain_iff P x).mpr ⟨hS,hxS.symm ▸ hF⟩
  have hDelta : scalarTomitaSquare P ⟨x,hD⟩ = x := by
    have hinput : scalarClosedTomita P (scalarTomitaSquareInput P ⟨x,hD⟩) = x := hxS
    have heq : (⟨scalarClosedTomita P (scalarTomitaSquareInput P ⟨x,hD⟩),
        scalarTomitaSquareInput_image_mem P ⟨x,hD⟩⟩ : scalarTomitaAdjointDomain P) =
        ⟨x,hF⟩ := Subtype.ext hinput
    exact (scalarTomitaSquare_apply P ⟨x,hD⟩).trans
      ((congrArg (scalarTomitaAdjoint P) heq).trans hxF)
  have hinv : scalarTomitaResolvent P (x+x) = x :=
    (congrArg (fun y => scalarTomitaResolvent P (x+y)) hDelta).symm.trans
      (scalarTomitaResolvent_inverse P ⟨x,hD⟩)
  have hx : scalarTomitaResolvent P x = (1/2 : ℂ) • x := by
    have hh := congrArg (fun y : ScalarGNSHilbert P => (1/2 : ℂ) • y) hinv
    rw [map_add,← two_smul ℂ,smul_smul] at hh
    norm_num at hh
    exact hh
  have hd : resolventDampingOperator (scalarTomitaResolvent P) x =
      (1/4 : ℂ) • x := by
    change scalarTomitaResolvent P (x-scalarTomitaResolvent P x) = _
    rw [map_sub,hx,map_smul,hx,smul_smul,← sub_smul]
    norm_num
  have hp := phase_at_half (scalarTomitaResolvent P)
    (scalarTomitaResolvent_selfadjoint P) x hx t
  have he := scalarTomitaImaginaryPower_damping P t x
  rw [hd,hp,map_smul] at he
  exact smul_right_injective (ScalarGNSHilbert P) (by norm_num : (1/4 : ℂ) ≠ 0) he

/-- The existing squares of one-sided averages give fixed vectors for the
same modular group. This does not assert cyclicity of any single vector. -/
theorem regularAverage_square_modular_fixed (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    ∃ A : scalarWeightStarCore P,
      A.val.val = star (regularAverage P δ)*regularAverage P δ ∧
      ∀ t : ℝ, scalarTomitaImaginaryPower P t (scalarWeightStarEmbedding P A) =
        scalarWeightStarEmbedding P A := by
  obtain ⟨A,hA,hS,hF,hxF⟩ := regularAverage_square_fixed_pair P δ hδ
  refine ⟨A,hA,fun t => ?_⟩
  exact scalarTomitaImaginaryPower_fixed_of_fixed_pair P (scalarWeightStarEmbedding P A)
    (scalarWeightStar_mem_closedTomitaDomain P A) hF hS hxF t

end
end TGLV350.Regular
