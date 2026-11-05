import TGLExt.GeneralMetricEinstein

set_option autoImplicit false
set_option maxHeartbeats 2400000

/-!
Order 012 B2: flat FLRW in the existing Coordinate4 chart. These are definitions
and evaluations of the same metric/inverse/Levi-Civita machinery consumed by
metric_only_einstein_equation. No Ricci or Einstein component is an input field.
-/

namespace ChatgptAudit.FLRW
open Matrix TGLExt ChatgptAudit.GeneralMetric
open scoped ContDiff
noncomputable section

def flrwMetric (a : ℝ → ℝ) : TensorField4 := fun x =>
  Matrix.diagonal ![1, -(a (x 0))^2, -(a (x 0))^2, -(a (x 0))^2]

def flrwInverse (a : ℝ → ℝ) : TensorField4 := fun x =>
  Matrix.diagonal ![1, -((a (x 0))^2)⁻¹, -((a (x 0))^2)⁻¹, -((a (x 0))^2)⁻¹]

def flrwHubble (a : ℝ → ℝ) (t : ℝ) : ℝ := deriv a t / a t

theorem flrw_metric_lorentz (a : ℝ → ℝ) (x : Coordinate4)
    (ha : a (x 0) ≠ 0) : LorentzByCongruence (flrwMetric a x) := by
  refine ⟨Matrix.diagonal ![1, a (x 0), a (x 0), a (x 0)], ?_, ?_⟩
  · apply isUnit_iff_ne_zero.mpr
    simp [Matrix.det_diagonal, Fin.prod_univ_four, ha]
  · ext i j
    fin_cases i <;> fin_cases j <;>
      simp [flrwMetric, eta4, Matrix.mul_apply, Matrix.diagonal] <;> ring

theorem flrw_inverse_left (a : ℝ → ℝ) (x : Coordinate4)
    (ha : a (x 0) ≠ 0) : flrwInverse a x * flrwMetric a x = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [flrwMetric, flrwInverse, Matrix.mul_apply, Matrix.diagonal, ha]

theorem flrw_inverse_right (a : ℝ → ℝ) (x : Coordinate4)
    (ha : a (x 0) ≠ 0) : flrwMetric a x * flrwInverse a x = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [flrwMetric, flrwInverse, Matrix.mul_apply, Matrix.diagonal, ha]

/-- The explicit diagonal inverse is the canonical matrix inverse on the chart. -/
theorem flrw_metric_inverse (a : ℝ → ℝ) (x : Coordinate4)
    (ha : a (x 0) ≠ 0) : metricInverse (flrwMetric a) x = flrwInverse a x :=
  metric_inverse_unique (flrwMetric a x) (metricInverse (flrwMetric a) x)
    (flrwInverse a x)
    (constructed_metric_inverse_left (flrwMetric a) x (flrw_metric_lorentz a x ha))
    (flrw_inverse_right a x ha)

/-- The coordinate derivative of a scalar time function in the existing chart. -/
theorem coordinatePartial_time_function (f : ℝ → ℝ) (f' : ℝ) (x : Coordinate4)
    (hf : HasDerivAt f f' (x 0)) (i : Fin 4) :
    coordinatePartial (fun y => f (y 0)) x i = if i = 0 then f' else 0 := by
  have h := hf.comp_hasFDerivAt (𝕜 := ℝ) (f := fun y : Coordinate4 => y 0)
    x (hasFDerivAt_apply (𝕜 := ℝ) 0 x)
  change (fderiv ℝ (f ∘ (fun y : Coordinate4 => y 0)) x) (Pi.single i 1) = _
  rw [h.fderiv]
  simp [Pi.single_apply, eq_comm]

theorem flrw_metric_smooth (U : Set Coordinate4) (a : ℝ → ℝ)
    (ha : ∀ x∈U, ContDiffAt ℝ ∞ a (x 0)) : SmoothMatrixOn U (flrwMetric a) := by
  intro i j x hx
  have hp : ContDiffAt ℝ ∞ (fun y : Coordinate4 => y 0) x := by fun_prop
  have ht := (ha x hx).comp x hp
  fin_cases i <;> fin_cases j <;> dsimp [flrwMetric, Matrix.diagonal] <;>
    first | exact contDiffWithinAt_const | exact (ht.contDiffWithinAt.pow 2).neg

theorem flrw_inverse_smooth (U : Set Coordinate4) (a : ℝ → ℝ)
    (ha : ∀ x∈U, ContDiffAt ℝ ∞ a (x 0)) (hpos : ∀ x∈U, 0 < a (x 0)) :
    SmoothMatrixOn U (metricInverse (flrwMetric a)) :=
  constructed_metric_inverse_smooth U (flrwMetric a) (flrw_metric_smooth U a ha)
    (fun x hx => flrw_metric_lorentz a x (hpos x hx).ne')

/-- The first jet is computed from the scale factor, not postulated. -/
theorem flrw_metric_jet (a : ℝ → ℝ) (x : Coordinate4)
    (ha : DifferentiableAt ℝ a (x 0)) (i : Fin 4) :
    tensorFieldJet (flrwMetric a) x i = if i = 0 then
      Matrix.diagonal ![0, -2*a (x 0)*deriv a (x 0),
        -2*a (x 0)*deriv a (x 0), -2*a (x 0)*deriv a (x 0)] else 0 := by
  have hd : HasDerivAt (fun t => -(a t)^2)
      (-2*a (x 0)*deriv a (x 0)) (x 0) := by
    simpa [mul_assoc] using! (ha.hasDerivAt.pow 2).neg
  have hs (j : Fin 4) := coordinatePartial_time_function _ _ x hd j
  have hc (c : ℝ) (j : Fin 4) : coordinatePartial (fun _ => c) x j = 0 := by
    simp [coordinatePartial]
  by_cases hi : i = 0 <;> ext j k <;> fin_cases j <;> fin_cases k <;>
    simp [tensorFieldJet, flrwMetric, Matrix.diagonal, hc, hs, hi]

/-- Two scalar coefficients determine the evaluated FLRW connection. -/
def flrwConnectionForm (b h : ℝ) : ConnectionMatrix4 :=
  ![Matrix.diagonal ![0,h,h,h],
    !![0,b,0,0; h,0,0,0; 0,0,0,0; 0,0,0,0],
    !![0,0,b,0; 0,0,0,0; h,0,0,0; 0,0,0,0],
    !![0,0,0,b; 0,0,0,0; 0,0,0,0; h,0,0,0]]

def flrwConnection (a : ℝ → ℝ) : ConnectionField4 := fun x =>
  flrwConnectionForm (a (x 0)*deriv a (x 0)) (flrwHubble a (x 0))

/-- Evaluation of the existing Levi-Civita construction. -/
theorem flrw_connection (a : ℝ → ℝ) (x : Coordinate4)
    (ha : a (x 0) ≠ 0) (hd : DifferentiableAt ℝ a (x 0)) :
    leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a)) x =
      flrwConnection a x := by
  unfold leviCivitaField
  rw [flrw_metric_inverse a x ha]
  have hj := flrw_metric_jet a x hd
  funext i
  ext j k
  fin_cases i <;> fin_cases j <;> fin_cases k <;>
    simp [leviCivitaJet, lowerChristoffelJet, hj, flrwInverse,
      flrwConnection, flrwConnectionForm, flrwHubble, Matrix.mul_apply,
    Matrix.diagonal] <;> field_simp

/-- Differentiating the evaluated connection still uses the chart's first jet. -/
theorem flrw_connection_form_jet (b h : ℝ → ℝ) (db dh : ℝ) (x : Coordinate4)
    (hb : HasDerivAt b db (x 0)) (hh : HasDerivAt h dh (x 0)) (i j : Fin 4) :
    connectionFirstJet (fun y => flrwConnectionForm (b (y 0)) (h (y 0))) x i j =
      if i = 0 then flrwConnectionForm db dh j else 0 := by
  have hbj (j : Fin 4) := coordinatePartial_time_function b db x hb j
  have hhj (j : Fin 4) := coordinatePartial_time_function h dh x hh j
  have hc (c : ℝ) (j : Fin 4) : coordinatePartial (fun _ => c) x j = 0 := by
    simp [coordinatePartial]
  by_cases hi : i = 0 <;> ext k l <;> fin_cases j <;> fin_cases k <;> fin_cases l <;>
    simp [connectionFirstJet, tensorFieldJet, flrwConnectionForm,
      Matrix.diagonal, hbj, hhj, hc, hi]

/-- Ricci is evaluated from the curvature definition for these connection jets. -/
theorem flrw_connection_form_ricci (Gamma : ConnectionField4) (x : Coordinate4)
    (b h db dh : ℝ) (hG : Gamma x = flrwConnectionForm b h)
    (hJ : connectionFirstJet Gamma x = fun i =>
      if i = 0 then flrwConnectionForm db dh else 0) :
    coordinateRicci Gamma x =
      Matrix.diagonal ![-3*(dh+h^2),db+b*h,db+b*h,db+b*h] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [coordinateRicci, coordinateCurvature, connectionCurvatureJet, hG, hJ,
      flrwConnectionForm, Matrix.mul_apply, Fin.sum_univ_four, Matrix.diagonal,
      Matrix.vecHead, Matrix.vecTail] <;> ring

/-- Ricci of the actual metric-generated connection on an open FLRW chart. -/
theorem flrw_ricci (U : Set Coordinate4) (hU : IsOpen U) (a : ℝ → ℝ)
    (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0 < a (y 0))
    (x : Coordinate4) (hx : x∈U) :
    coordinateRicci (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x =
      Matrix.diagonal ![-3*deriv (deriv a) (x 0)/a (x 0),
        a (x 0)*deriv (deriv a) (x 0)+2*(deriv a (x 0))^2,
        a (x 0)*deriv (deriv a) (x 0)+2*(deriv a (x 0))^2,
        a (x 0)*deriv (deriv a) (x 0)+2*(deriv a (x 0))^2] := by
  have hz := (hpos x hx).ne'
  have hda : DifferentiableAt ℝ a (x 0) := (ha x hx).differentiableAt (by simp)
  have hdda : DifferentiableAt ℝ (deriv a) (x 0) :=
    ((ha x hx).derivWithin (m := ∞) (by simp)).differentiableAt (by simp)
  have hb : HasDerivAt (fun t => a t*deriv a t)
      ((deriv a (x 0))^2+a (x 0)*deriv (deriv a) (x 0)) (x 0) := by
    simpa [pow_two] using! hda.hasDerivAt.mul hdda.hasDerivAt
  have hh : HasDerivAt (flrwHubble a)
      ((deriv (deriv a) (x 0)*a (x 0)-(deriv a (x 0))^2)/(a (x 0))^2) (x 0) := by
    simpa [flrwHubble, pow_two] using! hdda.hasDerivAt.div hda.hasDerivAt hz
  have heq : Set.EqOn
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) (flrwConnection a) U := by
    intro y hy
    exact flrw_connection a y (hpos y hy).ne' ((ha y hy).differentiableAt (by simp))
  have hj : connectionFirstJet
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x = fun i =>
      if i = 0 then flrwConnectionForm
        ((deriv a (x 0))^2+a (x 0)*deriv (deriv a) (x 0))
        ((deriv (deriv a) (x 0)*a (x 0)-(deriv a (x 0))^2)/(a (x 0))^2)
      else 0 := by
    funext i j
    change tensorFieldJet (fun y =>
      leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a)) y j) x i = _
    rw [congrArg (fun J => J i) (tensorFieldJet_congr_on U hU _ _
      (fun y hy => congrArg (fun C => C j) (heq hy)) x hx)]
    simpa [flrwConnection, connectionFirstJet, ite_apply] using
      flrw_connection_form_jet _ _ _ _ x hb hh i j
  rw [flrw_connection_form_ricci _ x _ _ _ _ (heq hx) hj]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.diagonal, flrwHubble] <;> field_simp <;> ring

end
end ChatgptAudit.FLRW
