import GeneralSourceUnitaryRealization
import JointCoherentGravitation

set_option autoImplicit false
set_option maxHeartbeats 3000000
namespace ChatgptAudit.GeneralSourceEinstein
open Matrix Filter Topology Set TGLExt ChatgptAudit.GeneralMetric
  ChatgptAudit.GeneralClausius ChatgptAudit.Coherent023 ChatgptAudit.Unitary022
  ChatgptAudit.Micro021 ChatgptAudit.Flow019 ChatgptAudit.Flow020
  ChatgptAudit.JointUnitary ChatgptAudit.JointGravitation
  ChatgptAudit.GeneralSourceUnitary
noncomputable section

/-- Heat is built from the supplied total source, not from a sectorwise conservation assumption. -/
theorem general_source_heat_matching
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4}
    {x direction : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x direction) (T : TensorField4) (rate : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hTd : ∀ i j, DifferentiableOn ℝ (fun y => T y i j) U)
    (hLor : LorentzByCongruence (g x)) (hTs : (T x)ᵀ = T x)
    (hn : tensorQuad (g x) direction = 0) :
    Tendsto (fun t => microscopicHeatError (calibrationSourceCurve g T x direction) rate
      (constructedHeat P T rate hU hg hTd) t / t^2) (𝓝[<] 0) (𝓝 0) := by
  have hQ := constructed_heat_quadratic_limit P T rate hU hg hTd
  have hK := calibration_source_modular_null_limit g T x direction hLor hTs hn
  have hl := hQ.sub (hK.const_mul (rate / (2*Real.pi)))
  have he : (fun t => microscopicHeatError (calibrationSourceCurve g T x direction) rate
      (constructedHeat P T rate hU hg hTd) t / t^2) =
      (fun t => constructedHeat P T rate hU hg hTd t / t^2 -
        rate / (2*Real.pi) * (modularIncrement (jointBase calibrationLabelData)
          ((calibrationSourceCurve g T x direction).weights t) / t^2)) := by
    funext t
    unfold microscopicHeatError
    ring
  rw [he]
  have hz : -rate * tensorQuad (T x) direction / 2 -
      rate / (2*Real.pi) * (-Real.pi * tensorQuad (T x) direction) = 0 := by
    field_simp [Real.pi_ne_zero]
    ring
  rw [hz] at hl
  exact hl

/-- The remaining area law is equivalent to null Ricci balance for the supplied T. -/
theorem general_source_area_matching_iff_ricci
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4}
    {x direction : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x direction) (T : TensorField4) (eta : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (ht : ∀ i j k, Gamma x i k j = Gamma x j k i)
    (hLor : LorentzByCongruence (g x)) (hTs : (T x)ᵀ = T x)
    (hn : tensorQuad (g x) direction = 0) :
    Tendsto (fun t => microscopicAreaError (calibrationSourceCurve g T x direction) eta
      (inducedArea g P.curve P.screen.vectors) t / t^2) (𝓝[<] 0) (𝓝 0) ↔
      eta * tensorQuad (coordinateRicci Gamma x) direction =
        2*Real.pi * tensorQuad (T x) direction := by
  have h := joint_area_matching_iff_ricci P calibrationLabelData
    (calibrationSourceCovectors g T) eta hU hg hG ht hn
  change Tendsto (fun t => microscopicAreaError (calibrationSourceCurve g T x direction) eta
    (inducedArea g P.curve P.screen.vectors) t / t^2) (𝓝[<] 0) (𝓝 0) ↔
      eta * tensorQuad (coordinateRicci Gamma x) direction =
        2*Real.pi * tensorQuad (realizedSourceField g T x) direction at h
  rw [realized_source_eq g T x hLor hTs] at h
  exact h

/-- Representation is general; area matching and total conservation remain explicit physical inputs. -/
theorem general_source_einstein_from_area
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (g T : TensorField4) (hg : SmoothMatrixOn U g) (hT : SmoothMatrixOn U T)
    (hLor : ∀ x ∈ U, LorentzByCongruence (g x)) (hTs : ∀ x ∈ U, (T x)ᵀ = T x)
    (screens : MetricScreenFamily U g) (eta : ℝ) (heta : eta ≠ 0)
    (hd : ∀ x ∈ U, ∀ j, tensorFieldDivergence (metricInverse g)
      (leviCivitaField g (metricInverse g)) T x j = 0)
    (harea : ∀ x (hx : x ∈ U) direction (hv : direction ≠ 0)
      (hn : tensorQuad (g x) direction = 0),
      Tendsto (fun t => microscopicAreaError (calibrationSourceCurve g T x direction) eta
        (inducedArea g (screens x hx direction hv hn).curve
          (screens x hx direction hv hn).screen.vectors) t / t^2) (𝓝[<] 0) (𝓝 0)) :
    ∃ cosmological : ℝ, ∀ x ∈ U,
      geometricEinsteinTensor g (metricInverse g) (leviCivitaField g (metricInverse g)) x +
        cosmological • g x = (2*Real.pi/eta) • T x := by
  have hw := calibration_source_covectors_smooth U g T hg hT hLor
  have hc := realized_source_conserved U hU g T
    (leviCivitaField g (metricInverse g)) hLor hTs hd
  obtain ⟨cosmological, hcos⟩ := joint_einstein_from_area U hU hconn calibrationLabelData
    g (calibrationSourceCovectors g T) hg hLor hw screens eta heta hc harea
  refine ⟨cosmological, ?_⟩
  intro x hx
  have h := hcos x hx
  change geometricEinsteinTensor g (metricInverse g) (leviCivitaField g (metricInverse g)) x +
    cosmological • g x = (2*Real.pi/eta) • realizedSourceField g T x at h
  rw [realized_source_eq g T x (hLor x hx) (hTs x hx)] at h
  exact h

#print axioms general_source_heat_matching
#print axioms general_source_area_matching_iff_ricci
#print axioms general_source_einstein_from_area
end
end ChatgptAudit.GeneralSourceEinstein
