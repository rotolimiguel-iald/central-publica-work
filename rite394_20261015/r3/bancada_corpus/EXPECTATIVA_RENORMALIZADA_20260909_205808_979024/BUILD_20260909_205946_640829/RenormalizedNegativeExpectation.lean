import TGLExt.FiniteCoherentSources
import TGLExt.MixedGibbsGravitationalBridge
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.LinearAlgebra.Matrix.PosDef

set_option autoImplicit false
set_option maxHeartbeats 2000000
namespace ChatgptAudit.RenormalizedExpectation
open Matrix Filter Topology Set TGLExt ChatgptAudit
  ChatgptAudit.Coherent023 ChatgptAudit.FiniteCoherentSource
  ChatgptAudit.GravitationalRecord ChatgptAudit.GeneralMetric
  ChatgptAudit.AngularTensorCodec ChatgptAudit.MixedGibbsGravity
noncomputable section

def oscillatorAmplitudes : Fin 2 → ℝ := ![2*Real.sqrt 2/3,-1/3]

def oscillatorVector : EuclideanSpace ℂ (Fin 2) :=
  WithLp.toLp 2 (fun i => (oscillatorAmplitudes i : ℂ))

def oscillatorDensity : Matrix (Fin 2) (Fin 2) ℂ :=
  Matrix.vecMulVec (fun i => (oscillatorAmplitudes i : ℂ))
    (star (fun i => (oscillatorAmplitudes i : ℂ)))

def normalOrderedSquare : Matrix (Fin 2) (Fin 2) ℂ :=
  !![0,(Real.sqrt 2 : ℂ);(Real.sqrt 2 : ℂ),4]

def shiftedSquareFactor : Matrix (Fin 2) (Fin 2) ℂ :=
  !![1,(Real.sqrt 2 : ℂ);0,(Real.sqrt 3 : ℂ)]

theorem amplitudes_square_sum : ∑ i, (oscillatorAmplitudes i)^2=1 := by
  have hs : (Real.sqrt 2)^2=2 := Real.sq_sqrt (by norm_num)
  norm_num [oscillatorAmplitudes,Fin.sum_univ_two]
  nlinarith

theorem oscillator_vector_normalized : ‖oscillatorVector‖=1 := by
  have hs : ‖oscillatorVector‖^2=1 := by
    rw [EuclideanSpace.norm_sq_eq]
    simpa only [oscillatorVector,WithLp.toLp_apply,Complex.norm_real,Real.norm_eq_abs,sq_abs]
      using amplitudes_square_sum
  nlinarith [norm_nonneg oscillatorVector]

theorem oscillator_density_positive : oscillatorDensity.PosSemidef :=
  Matrix.posSemidef_vecMulVec_self_star (fun i => (oscillatorAmplitudes i : ℂ))

theorem oscillator_density_entries :
    oscillatorDensity=!![(8/9:ℂ),-(2*(Real.sqrt 2:ℂ))/9;
      -(2*(Real.sqrt 2:ℂ))/9,(1/9:ℂ)] := by
  have hs : (Real.sqrt 2 : ℂ)^2=2 := by
    exact_mod_cast (Real.sq_sqrt (by norm_num : (0:ℝ)≤2))
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [oscillatorDensity,oscillatorAmplitudes,Matrix.vecMulVec,Pi.star_apply] <;>
    ring_nf <;> simp_all

theorem oscillator_density_trace : Matrix.trace oscillatorDensity=1 := by
  rw [oscillator_density_entries]
  norm_num [Matrix.trace,Fin.sum_univ_two]

theorem oscillator_diagonal_probabilities :
    (oscillatorDensity 0 0).re=8/9 ∧ (oscillatorDensity 1 1).re=1/9 := by
  rw [oscillator_density_entries]
  norm_num

theorem normal_ordered_square_hermitian : normalOrderedSquare.IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [normalOrderedSquare,Matrix.conjTranspose]

theorem negative_normal_ordered_expectation :
    Matrix.trace (oscillatorDensity*normalOrderedSquare)=(-4/9:ℂ) := by
  have hs : (Real.sqrt 2 : ℂ)^2=2 := by
    exact_mod_cast (Real.sq_sqrt (by norm_num : (0:ℝ)≤2))
  rw [oscillator_density_entries]
  norm_num [normalOrderedSquare,Matrix.trace,Matrix.mul_apply,Fin.sum_univ_two]
  ring_nf
  simp_all

theorem positive_shifted_expectation :
    Matrix.trace (oscillatorDensity*(normalOrderedSquare+1))=(5/9:ℂ) := by
  rw [Matrix.mul_add,Matrix.trace_add,Matrix.mul_one,
    negative_normal_ordered_expectation,oscillator_density_trace]
  norm_num

theorem shifted_square_gram :
    normalOrderedSquare+1=shiftedSquareFactor.conjTranspose*shiftedSquareFactor := by
  have h2 : (Real.sqrt 2 : ℂ)^2=2 := by
    exact_mod_cast (Real.sq_sqrt (by norm_num : (0:ℝ)≤2))
  have h3 : (Real.sqrt 3 : ℂ)^2=3 := by
    exact_mod_cast (Real.sq_sqrt (by norm_num : (0:ℝ)≤3))
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [normalOrderedSquare,shiftedSquareFactor,Matrix.conjTranspose,
      Matrix.mul_apply,Fin.sum_univ_two] <;> ring_nf <;> simp_all

theorem shifted_square_positive : (normalOrderedSquare+1).PosSemidef := by
  rw [shifted_square_gram]
  exact Matrix.posSemidef_conjTranspose_mul_self shiftedSquareFactor

theorem negative_expectation_real :
    (Matrix.trace (oscillatorDensity*normalOrderedSquare)).re=(-4/9:ℝ) := by
  rw [negative_normal_ordered_expectation]
  norm_num

variable {J : Type} [Fintype J]

/-- Nonnegative weights and positive Gibbs parameters force nonnegative null source. -/
theorem unsigned_gibbs_null_nonnegative (g gi : TensorField4) (w : J → CovectorField4)
    (weight k : J → ℝ) (hweight : ∀ j, 0≤weight j) (hk : ∀ j, 0<k j)
    (x v : Coordinate4) (hn : tensorQuad (g x) v=0) :
    0≤tensorQuad (finiteCovectorStressField g gi w weight
      (fun j => k j/(Real.pi*Real.cosh (k j)^2)) x) v := by
  apply finite_covector_stress_null_nonnegative g gi w weight _ x v hn
  intro j
  exact mul_nonneg (hweight j) (le_of_lt (div_pos (hk j)
    (mul_pos Real.pi_pos (sq_pos_of_pos (Real.cosh_pos (k j))))))

theorem unsigned_gibbs_excludes_negative_value (g gi : TensorField4) (w : J → CovectorField4)
    (weight k : J → ℝ) (hweight : ∀ j, 0≤weight j) (hk : ∀ j, 0<k j)
    (x v : Coordinate4) (hn : tensorQuad (g x) v=0) :
    tensorQuad (finiteCovectorStressField g gi w weight
      (fun j => k j/(Real.pi*Real.cosh (k j)^2)) x) v ≠ (-4/9:ℝ) := by
  have h := unsigned_gibbs_null_nonnegative g gi w weight k hweight hk x v hn
  intro he
  rw [he] at h
  norm_num at h

theorem unsigned_gibbs_record_null_nonnegative {U : Set Coordinate4}
    (metric : LorentzProbabilityRecord U) (k : J → ℝ) (hk : ∀ j, 0<k j)
    (w : J → CovectorField4) (hw : ∀ j, SmoothVectorOn U (w j))
    (x v : Coordinate4) (hn : tensorQuad (decodeRecord metric.data x) v=0) :
    0≤tensorQuad (recordSource (gibbsRecord metric k w hw) x) v := by
  rw [gibbs_record_source metric k hk w hw]
  exact unsigned_gibbs_null_nonnegative _ _ w (fun _ => 1) k (fun _ => by norm_num) hk x v hn

#print axioms oscillatorAmplitudes
#print axioms oscillatorVector
#print axioms oscillatorDensity
#print axioms normalOrderedSquare
#print axioms shiftedSquareFactor
#print axioms amplitudes_square_sum
#print axioms oscillator_vector_normalized
#print axioms oscillator_density_positive
#print axioms oscillator_density_entries
#print axioms oscillator_density_trace
#print axioms oscillator_diagonal_probabilities
#print axioms normal_ordered_square_hermitian
#print axioms negative_normal_ordered_expectation
#print axioms positive_shifted_expectation
#print axioms shifted_square_gram
#print axioms shifted_square_positive
#print axioms negative_expectation_real
#print axioms unsigned_gibbs_null_nonnegative
#print axioms unsigned_gibbs_excludes_negative_value
#print axioms unsigned_gibbs_record_null_nonnegative
end
end ChatgptAudit.RenormalizedExpectation
