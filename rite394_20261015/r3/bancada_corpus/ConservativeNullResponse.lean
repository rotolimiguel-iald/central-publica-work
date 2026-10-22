import NullStressCompletion

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.Completion042
open Matrix Filter Set TGLExt ChatgptAudit ChatgptAudit.Coherent023
open scoped Topology ContDiff
noncomputable section

/-- The covector force that a variable metric trace must cancel. -/
def flatForce (w : CovectorField4) (c : ℝ) : CovectorField4 :=
  fun x j => c*(covectorDivergence flatMetric flatConnection w x*w x j)

theorem coordinate_partial_congr_open (U : Set Coordinate4) (hU : IsOpen U)
    (f g : Coordinate4 → ℝ) (he : Set.EqOn f g U)
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    coordinatePartial f x i=coordinatePartial g x i := by
  have hn : f =ᶠ[𝓝 x] g := by
    filter_upwards [hU.mem_nhds hx] with y hy
    exact he hy
  exact congrArg (fun L : Coordinate4 →L[ℝ] ℝ => L (Pi.single i 1)) hn.fderiv_eq

theorem coordinate_partial_neg_value (f : Coordinate4 → ℝ) (x : Coordinate4)
    (hf : DifferentiableAt ℝ f x) (i : Fin 4) :
    coordinatePartial (fun y => -f y) x i = -coordinatePartial f x i := by
  have h := coordinatePartial_sub (fun _ : Coordinate4 => (0:ℝ)) f x
    (differentiableAt_const 0) hf i
  have hz : coordinatePartial (fun _ : Coordinate4 => (0:ℝ)) x i=0 := by
    simp [coordinatePartial]
  simpa only [zero_sub,hz] using h

/-- Smooth exactness implies closure. No converse on arbitrary domains is asserted. -/
theorem negative_gradient_force_closed (U : Set Coordinate4) (hU : IsOpen U)
    (force : CovectorField4) (f : Coordinate4 → ℝ)
    (hf : ContDiffOn ℝ ∞ f U)
    (hgrad : ∀ x∈U, ∀ j, coordinatePartial f x j = -force x j) :
    ClosedCovectorOn U force := by
  intro x hx i j
  have he (k : Fin 4) : Set.EqOn (fun y => force y k)
      (fun y => -coordinatePartial f y k) U := by
    intro y hy
    have h := hgrad y hy k
    linarith
  have hd (k : Fin 4) : DifferentiableAt ℝ (fun y => coordinatePartial f y k) x :=
    (((coordinatePartial_smooth U hU f hf k).differentiableOn (by simp)).differentiableAt
      (hU.mem_nhds hx))
  rw [coordinate_partial_congr_open U hU _ _ (he j) x hx i,
    coordinate_partial_congr_open U hU _ _ (he i) x hx j,
    coordinate_partial_neg_value _ x (hd j) i,
    coordinate_partial_neg_value _ x (hd i) j,
    coordinate_partials_commute f x (hf.contDiffAt (hU.mem_nhds hx)) i j]

theorem completed_conserved_iff_gradient (U : Set Coordinate4) (hU : IsOpen U)
    (w : CovectorField4) (c : ℝ) (f : Coordinate4 → ℝ)
    (hw : SmoothVectorOn U w) (hclosed : ClosedCovectorOn U w)
    (hf : ContDiffOn ℝ ∞ f U) :
    (∀ x∈U, ∀ j, tensorFieldDivergence flatMetric flatConnection
      (traceCompletedStress w c f) x j=0) ↔
    (∀ x∈U, ∀ j, coordinatePartial f x j = -flatForce w c x j) := by
  constructor
  · intro h x hx j
    have hd := h x hx j
    rw [trace_completed_divergence U hU w c f hw hclosed hf x hx j] at hd
    dsimp [flatForce]
    linarith
  · intro h x hx j
    rw [trace_completed_divergence U hU w c f hw hclosed hf x hx j,h x hx j]
    simp [flatForce]

theorem conserved_null_response_trace_gradient
    (U : Set Coordinate4) (hU : IsOpen U) (w : CovectorField4) (c : ℝ) (T : TensorField4)
    (hw : SmoothVectorOn U w) (hclosed : ClosedCovectorOn U w)
    (hT : SmoothMatrixOn U T) (hs : ∀ x∈U, (T x)ᵀ=T x)
    (hn : ∀ x∈U, ∀ d, tensorQuad eta4 d=0 →
      tensorQuad (T x) d=c*(covectorRead (w x) d)^2)
    (hdiv : ∀ x∈U, ∀ j, tensorFieldDivergence flatMetric flatConnection T x j=0) :
    ∀ x∈U, ∀ j, coordinatePartial (traceCompletion w c T) x j = -flatForce w c x j := by
  have he : Set.EqOn T (traceCompletedStress w c (traceCompletion w c T)) U := by
    intro x hx
    exact null_stress_classification w c T x (hs x hx) (hn x hx)
  apply (completed_conserved_iff_gradient U hU w c (traceCompletion w c T) hw hclosed
    (trace_completion_smooth U w c T hw hT)).1
  intro x hx j
  rw [← tensorFieldDivergence_congr_on U hU flatMetric flatConnection T
    (traceCompletedStress w c (traceCompletion w c T)) he x hx]
  exact hdiv x hx j

/-- Every symmetric smooth realization, including every variable trace, obeys this obstruction. -/
theorem conserved_null_response_closed_force
    (U : Set Coordinate4) (hU : IsOpen U) (w : CovectorField4) (c : ℝ) (T : TensorField4)
    (hw : SmoothVectorOn U w) (hclosed : ClosedCovectorOn U w)
    (hT : SmoothMatrixOn U T) (hs : ∀ x∈U, (T x)ᵀ=T x)
    (hn : ∀ x∈U, ∀ d, tensorQuad eta4 d=0 →
      tensorQuad (T x) d=c*(covectorRead (w x) d)^2)
    (hdiv : ∀ x∈U, ∀ j, tensorFieldDivergence flatMetric flatConnection T x j=0) :
    ClosedCovectorOn U (flatForce w c) :=
  negative_gradient_force_closed U hU (flatForce w c) (traceCompletion w c T)
    (trace_completion_smooth U w c T hw hT)
    (conserved_null_response_trace_gradient U hU w c T hw hclosed hT hs hn hdiv)

/-- Smooth realization of all null responses, with covariant conservation on the same open set. -/
def HasConservedNullRealization (U : Set Coordinate4) (w : CovectorField4) (c : ℝ) : Prop :=
  ∃ T : TensorField4, SmoothMatrixOn U T ∧
    (∀ x∈U, (T x)ᵀ=T x) ∧
    (∀ x∈U, ∀ d, tensorQuad eta4 d=0 → tensorQuad (T x) d=c*(covectorRead (w x) d)^2) ∧
    (∀ x∈U, ∀ j, tensorFieldDivergence flatMetric flatConnection T x j=0)

/-- The exact potential criterion; closure alone is not substituted for global exactness. -/
theorem conserved_null_realization_iff_potential
    (U : Set Coordinate4) (hU : IsOpen U) (w : CovectorField4) (c : ℝ)
    (hw : SmoothVectorOn U w) (hclosed : ClosedCovectorOn U w) :
    HasConservedNullRealization U w c ↔
      ∃ f : Coordinate4 → ℝ, ContDiffOn ℝ ∞ f U ∧
        ∀ x∈U, ∀ j, coordinatePartial f x j = -flatForce w c x j := by
  constructor
  · rintro ⟨T,hT,hs,hn,hdiv⟩
    exact ⟨traceCompletion w c T,trace_completion_smooth U w c T hw hT,
      conserved_null_response_trace_gradient U hU w c T hw hclosed hT hs hn hdiv⟩
  · rintro ⟨f,hf,hgrad⟩
    refine ⟨traceCompletedStress w c f,trace_completed_smooth U w c f hw hf,
      ?_,?_,(completed_conserved_iff_gradient U hU w c f hw hclosed hf).2 hgrad⟩
    · intro x _
      exact trace_completed_symmetric w c f x
    · intro x _ d hd
      exact trace_completed_null w c f x d hd

theorem nonclosed_force_excludes_realization
    (U : Set Coordinate4) (hU : IsOpen U) (w : CovectorField4) (c : ℝ)
    (hw : SmoothVectorOn U w) (hclosed : ClosedCovectorOn U w)
    (hforce : ¬ ClosedCovectorOn U (flatForce w c)) :
    ¬ HasConservedNullRealization U w c := by
  rintro ⟨T,hT,hs,hn,hdiv⟩
  exact hforce (conserved_null_response_closed_force U hU w c T hw hclosed hT hs hn hdiv)

#print axioms flatForce
#print axioms coordinate_partial_congr_open
#print axioms coordinate_partial_neg_value
#print axioms negative_gradient_force_closed
#print axioms completed_conserved_iff_gradient
#print axioms conserved_null_response_trace_gradient
#print axioms conserved_null_response_closed_force
#print axioms HasConservedNullRealization
#print axioms conserved_null_realization_iff_potential
#print axioms nonclosed_force_excludes_realization
end
end ChatgptAudit.Completion042
