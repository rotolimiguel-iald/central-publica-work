import TGLExt.TheObserverReadsTheAngle
import TGLExt.TheVerbalCoupling

set_option autoImplicit false
set_option maxHeartbeats 400000

namespace ChatgptAudit.SelectionAngle
open Matrix Complex TGLExt
noncomputable section

/-- Complex phase read from the known nonzero entry of the selected face. -/
def phaseReading (A : Matrix (Fin 2) (Fin 2) ℂ) : ℂ :=
  2 * (projPlus * A) 0 0

/-- Decoder for the prescribed angular family with reciprocal phases. -/
def angularDecoder (z : ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  z • projPlus + z⁻¹ • projMinus

theorem phase_reading_is_the_angular_phase (θ : ℝ) :
    phaseReading (angFamily θ) = Complex.exp ((θ : ℂ) * Complex.I) := by
  unfold phaseReading
  rw [the_observer_reads_the_angle]
  simp [Matrix.smul_apply, projPlus, genK, Matrix.one_apply]
  <;> ring

theorem angular_family_reconstructed_from_one_selected_face (θ : ℝ) :
    angularDecoder (phaseReading (angFamily θ)) = angFamily θ := by
  rw [phase_reading_is_the_angular_phase]
  unfold angularDecoder
  rw [the_angle_is_the_projection]
  have hi : (Complex.exp ((θ : ℂ) * Complex.I))⁻¹ =
      Complex.exp (-(θ : ℂ) * Complex.I) := by
    rw [← Complex.exp_neg]
    congr 1
    ring
  rw [hi]

theorem one_selected_face_separates_angular_forms (θ φ : ℝ)
    (h : projPlus * angFamily θ = projPlus * angFamily φ) :
    angFamily θ = angFamily φ := by
  have hp : phaseReading (angFamily θ) = phaseReading (angFamily φ) := by
    unfold phaseReading
    rw [h]
  calc
    angFamily θ = angularDecoder (phaseReading (angFamily θ)) :=
      (angular_family_reconstructed_from_one_selected_face θ).symm
    _ = angularDecoder (phaseReading (angFamily φ)) := congrArg angularDecoder hp
    _ = angFamily φ := angular_family_reconstructed_from_one_selected_face φ

/-- Explicit bridge between the two separately named complex matrix families. -/
theorem angular_form_is_the_boundary_s_matrix (θ : ℝ) :
    angFamily θ = Smat θ := by
  rfl

theorem miguel_boundary_reconstructed_from_its_selected_face (β : ℝ) :
    angularDecoder (phaseReading (Smat (thetaMiguel β))) =
      Smat (thetaMiguel β) := by
  simpa only [angular_form_is_the_boundary_s_matrix] using
    angular_family_reconstructed_from_one_selected_face (thetaMiguel β)

/-- Selection is not injective on the ambient matrix space. -/
theorem ambient_selection_has_distinct_inputs :
    projPlus ≠ (1 : Matrix (Fin 2) (Fin 2) ℂ) ∧
    projPlus * projPlus = projPlus * 1 := by
  constructor
  · intro h
    have h00 := congrFun (congrFun h 0) 0
    norm_num [projPlus, genK, Matrix.one_apply] at h00
  · rw [(spectral_projections_are_idempotent).1, Matrix.mul_one]

/-- A decoder on all inputs would force injectivity on those inputs. -/
theorem reconstruction_on_all_inputs_forces_injectivity
    {X Y : Type} (encode : X → Y) (decode : Y → X)
    (h : ∀ x, decode (encode x) = x) : Function.Injective encode := by
  intro x y hxy
  calc
    x = decode (encode x) := (h x).symm
    _ = decode (encode y) := congrArg decode hxy
    _ = y := h y

#print axioms phaseReading
#print axioms angularDecoder
#print axioms phase_reading_is_the_angular_phase
#print axioms angular_family_reconstructed_from_one_selected_face
#print axioms one_selected_face_separates_angular_forms
#print axioms angular_form_is_the_boundary_s_matrix
#print axioms miguel_boundary_reconstructed_from_its_selected_face
#print axioms ambient_selection_has_distinct_inputs
#print axioms reconstruction_on_all_inputs_forces_injectivity

end
end ChatgptAudit.SelectionAngle
