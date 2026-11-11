import TGLExt.IALDGraviton
import TGLExt.PostoAdendo

/-!
# Candidata v394: ponte matricial da fonte ao setor de helicidade
[DERIVED/REAL apos build] Calculo exato no M2 concreto do kernel. A porta C e
star(IALDGraviton.phaseGate). O Hamiltoniano Hlig=-V0 sigma_x e transportado,
nao suposto igual ao gerador. Eg e pinching de DOIS blocos; nao e a compressao
PXP, nem o consumidor M4. As identificacoes fisicas dos parametros e unidades
permanecem contratos proprios. Nao se afirma atrator universal unico, rede
continua global, propagador avancado, observacao empirica ou mudanca de gate.
-/
set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000
open Matrix Complex
namespace TGLExt.TimeGravitonMatrix
noncomputable section
abbrev M2 := Matrix (Fin 2) (Fin 2) ℂ

def C : M2 := star IALDGraviton.phaseGate
def sigmaY : M2 := !![0, -Complex.I; Complex.I, 0]
def Px : M2 := (1/2 : ℂ) • (1+hCrossC)
def PxMinus : M2 := (1/2 : ℂ) • (1-hCrossC)
def Hlig (V0 : ℝ) : M2 := (-(V0 : ℂ)) • hCrossC
def Hg (V0 : ℝ) : M2 := C * Hlig V0 * star C
def omega (V0 hbar : ℝ) : ℝ := V0/hbar

def Eg : M2 →ₗ[ℂ] M2 where
  toFun X := projPlus * X * projPlus + projMinus * X * projMinus
  map_add' X Y := by simp only [mul_add, add_mul]; noncomm_ring
  map_smul' c X := by simp only [mul_smul_comm, smul_mul_assoc, smul_add, RingHom.id_apply]

def blockPM : M2 →ₗ[ℂ] M2 where
  toFun X := projPlus * X * projMinus
  map_add' X Y := by simp only [mul_add, add_mul]
  map_smul' c X := by simp only [mul_smul_comm, smul_mul_assoc, RingHom.id_apply]

def blockMP : M2 →ₗ[ℂ] M2 where
  toFun X := projMinus * X * projPlus
  map_add' X Y := by simp only [mul_add, add_mul]
  map_smul' c X := by simp only [mul_smul_comm, smul_mul_assoc, RingHom.id_apply]

theorem Eg_apply (X : M2) : Eg X = projPlus*X*projPlus + projMinus*X*projMinus := rfl
theorem blockPM_apply (X : M2) : blockPM X = projPlus*X*projMinus := rfl
theorem blockMP_apply (X : M2) : blockMP X = projMinus*X*projPlus := rfl

macro "matrix_calc" : tactic =>
 `(tactic| (ext i j; fin_cases i <;> fin_cases j <;>
  simp [C, IALDGraviton.phaseGate, sigmaY, Px, PxMinus, Hlig, Hg,
    Eg, blockPM, blockMP, hPlusC, hCrossC, rootPlus, rootMinus, genK, projPlus,
    projMinus, Matrix.mul_apply, Fin.sum_univ_two, Matrix.star_apply,
    Matrix.diagonal, Matrix.one_apply, Matrix.add_apply, Matrix.sub_apply,
    Matrix.smul_apply, Matrix.of_apply, Matrix.vecMul, dotProduct,
    Matrix.vecHead, Matrix.vecTail, pow_two, Complex.ext_iff] <;>
    (repeat' constructor) <;> (first | ring | trivial)))

theorem C_entries : C = !![1,0;0,Complex.I] := by matrix_calc
theorem C_unitary : C * star C = 1 ∧ star C * C = 1 := by constructor <;> matrix_calc
theorem C_sigmaX : C * hCrossC * star C = sigmaY := by matrix_calc
theorem C_Px : C * Px * star C = projPlus := by matrix_calc
theorem C_Hlig (V0 : ℝ) : Hg V0 = (Complex.I * (V0 : ℂ)) • genK := by matrix_calc
theorem hamiltonian_spectral (V0 : ℝ) :
    Hg V0 = (-(V0 : ℂ)) • projPlus + (V0 : ℂ) • projMinus := by matrix_calc
theorem hamiltonian_selfadjoint (V0 : ℝ) : star (Hg V0) = Hg V0 := by matrix_calc

theorem hamiltonian_generator (V0 hbar : ℝ) :
    (-Complex.I/(hbar : ℂ)) • Hg V0 = ((V0/hbar : ℝ) : ℂ) • genK := by
  rw [C_Hlig, smul_smul]
  congr 1
  push_cast
  simp only [div_eq_mul_inv]
  ring_nf
  simp [Complex.I_sq]

theorem pm_orthogonal : projMinus*projPlus = 0 := by matrix_calc
theorem projMinus_star : star projMinus = projMinus := by matrix_calc

theorem Eg_idem (X : M2) : Eg (Eg X) = Eg X := by matrix_calc
theorem Eg_projPlus : Eg projPlus = projPlus := by matrix_calc
theorem Eg_projMinus : Eg projMinus = projMinus := by matrix_calc
theorem Eg_rootPlus : Eg rootPlus = 0 := by matrix_calc
theorem Eg_rootMinus : Eg rootMinus = 0 := by matrix_calc
theorem Eg_one : Eg 1 = 1 := by matrix_calc
theorem Eg_trace (X : M2) : Matrix.trace (Eg X) = Matrix.trace X := by
  simp [Eg, projPlus, projMinus, genK, Matrix.trace_fin_two, Matrix.mul_apply,
    Fin.sum_univ_two, Matrix.smul_apply, Matrix.one_apply, Complex.ext_iff] <;>
    (repeat' constructor) <;> (first | ring | trivial)

theorem four_blocks (X : M2) : Eg X + blockPM X + blockMP X = X := by matrix_calc
theorem blockPM_rootPlus : blockPM rootPlus = rootPlus := by matrix_calc
theorem blockMP_rootPlus : blockMP rootPlus = 0 := by matrix_calc
theorem blockPM_rootMinus : blockPM rootMinus = 0 := by matrix_calc
theorem blockMP_rootMinus : blockMP rootMinus = rootMinus := by matrix_calc

def sourceG : Fin 2 → ℂ := ((Real.sqrt 2)⁻¹ : ℝ) • lightPlus
def transportedG : Fin 2 → ℂ := ((Real.sqrt 2)⁻¹ : ℝ) • (![1,-1] : Fin 2 → ℂ)
def sourceRho : M2 := projPlus
def transportedRho : M2 := C * sourceRho * star C

theorem C_state : C.mulVec sourceG = transportedG := by
  funext i
  fin_cases i <;> simp [C, IALDGraviton.phaseGate, sourceG, transportedG, lightPlus,
    Matrix.mulVec, dotProduct, Fin.sum_univ_two, Matrix.star_apply,
    Matrix.diagonal, Complex.ext_iff] <;> ring

theorem density_transport : transportedRho = PxMinus := by
  unfold transportedRho sourceRho
  matrix_calc

theorem transported_reading : Eg transportedRho = (1/2 : ℂ) • (1:M2) := by
  rw [density_transport]
  matrix_calc

theorem parity_preserved : C * hPlusC * star C = hPlusC := by matrix_calc

theorem angFamily_star (θ : ℝ) : star (angFamily θ) = (angFamily θ).transpose := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [angFamily, genK, Matrix.star_apply, Matrix.transpose_apply,
      Matrix.one_apply, Complex.ext_iff]

theorem rootPlus_phase (θ : ℝ) :
    angFamily θ * rootPlus * star (angFamily θ) =
      Complex.exp ((2*θ : ℝ) * Complex.I) • rootPlus := by
  rw [angFamily_star, the_tensor_squares_the_phase]
  congr 1
  rw [pow_two, ← Complex.exp_add]
  congr 1
  push_cast
  ring

theorem rootMinus_phase (θ : ℝ) :
    angFamily θ * rootMinus * star (angFamily θ) =
      Complex.exp ((-2*θ : ℝ) * Complex.I) • rootMinus := by
  have hp : Complex.exp (((-2*θ : ℝ) : ℂ) * Complex.I) =
      ((Real.cos θ : ℂ) - (Real.sin θ : ℂ)*Complex.I)^2 := by
    have h : Complex.exp (-(θ : ℂ)*Complex.I) =
        (Real.cos θ : ℂ) - (Real.sin θ : ℂ)*Complex.I := by
      simpa [sub_eq_add_neg] using (Complex.exp_mul_I (-(θ : ℂ)))
    rw [← h, pow_two, ← Complex.exp_add]
    congr 1
    push_cast
    ring
  rw [hp, angFamily_star]
  faces

theorem phase_frequency (V0 hbar t : ℝ) :
    angFamily (omega V0 hbar*t) * rootPlus * star (angFamily (omega V0 hbar*t)) =
      Complex.exp ((2*(V0/hbar)*t : ℝ) * Complex.I) • rootPlus := by
  simpa [omega, mul_assoc] using rootPlus_phase (omega V0 hbar*t)

theorem concrete_nonzero_modes : rootPlus ≠ 0 ∧ projPlus ≠ projMinus := by
  constructor
  · intro h
    have h00 := congrFun (congrFun h 0) 0
    norm_num [rootPlus, hPlusC, hCrossC] at h00
  · intro h
    have h01 := congrFun (congrFun h 0) 1
    norm_num [projPlus, projMinus, genK, Complex.ext_iff] at h01


/-! Exact bridges to the canonical diagonal expectation and positive-energy branch. -/
def spectralBasis : M2 := !![1,1;Complex.I,-Complex.I]
def toSpectral (X : M2) : M2 := (1/2 : ℂ) • (star spectralBasis * X * spectralBasis)
def fromSpectral (X : M2) : M2 := (1/2 : ℂ) • (spectralBasis * X * star spectralBasis)

theorem spectralBasis_normalization :
    spectralBasis * star spectralBasis = (2 : ℂ) • (1:M2) ∧
    star spectralBasis * spectralBasis = (2 : ℂ) • (1:M2) := by
  constructor <;> unfold spectralBasis <;> matrix_calc

theorem spectral_roundtrip (X : M2) : fromSpectral (toSpectral X) = X := by
  unfold fromSpectral toSpectral spectralBasis
  matrix_calc

theorem Eg_as_diagExpect (X : M2) :
    Eg X = fromSpectral (TGLExt.diagExpect (toSpectral X)) := by
  unfold fromSpectral toSpectral spectralBasis TGLExt.diagExpect
  matrix_calc

theorem Eg_as_nameOp (X : M2) :
    Eg X = fromSpectral (TGLExt.nameOp TGLExt.Posto.rhoStar (toSpectral X)) := by
  rw [PostoAdendo.A1c_nameOp_rhoStar_eq_diagExpect]
  exact Eg_as_diagExpect X

theorem sourceG_density : Matrix.vecMulVec sourceG (star sourceG) = sourceRho := by
  have hs : (Real.sqrt 2)^2 = 2 := Real.sq_sqrt (by norm_num)
  have h0 : Real.sqrt 2 ≠ 0 := by positivity
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [sourceG, sourceRho, lightPlus, Matrix.vecMulVec, projPlus, genK,
      Matrix.one_apply, Complex.ext_iff] <;>
    (repeat' constructor) <;> (first | (field_simp; nlinarith [hs]) | trivial)

def Hpos (V0 : ℝ) : M2 := (V0 : ℂ) • 1 + Hg V0

theorem Hpos_spectral (V0 : ℝ) : Hpos V0 = (2*(V0 : ℂ)) • projMinus := by
  unfold Hpos
  matrix_calc

def singleJump (a : ℝ) (X : M2) : M2 :=
  let L := (a : ℂ) • projMinus
  L * X * star L - (1/2 : ℂ) • (star L*L*X + X*star L*L)

theorem singleJump_rate (a : ℝ) (X : M2) :
    singleJump a X = ((a : ℂ)^2/2) • (Eg X-X) := by
  unfold singleJump
  matrix_calc

theorem positive_parameters_inhabited : ∃ V0 hbar : ℝ, 0 < V0 ∧ 0 < hbar :=
  ⟨1, 1, by norm_num, by norm_num⟩

end
end TGLExt.TimeGravitonMatrix

#print axioms TGLExt.TimeGravitonMatrix.Eg_apply
#print axioms TGLExt.TimeGravitonMatrix.blockPM_apply
#print axioms TGLExt.TimeGravitonMatrix.blockMP_apply
#print axioms TGLExt.TimeGravitonMatrix.C_entries
#print axioms TGLExt.TimeGravitonMatrix.C_unitary
#print axioms TGLExt.TimeGravitonMatrix.C_sigmaX
#print axioms TGLExt.TimeGravitonMatrix.C_Px
#print axioms TGLExt.TimeGravitonMatrix.C_Hlig
#print axioms TGLExt.TimeGravitonMatrix.hamiltonian_spectral
#print axioms TGLExt.TimeGravitonMatrix.hamiltonian_selfadjoint
#print axioms TGLExt.TimeGravitonMatrix.hamiltonian_generator
#print axioms TGLExt.TimeGravitonMatrix.pm_orthogonal
#print axioms TGLExt.TimeGravitonMatrix.projMinus_star
#print axioms TGLExt.TimeGravitonMatrix.Eg_idem
#print axioms TGLExt.TimeGravitonMatrix.Eg_projPlus
#print axioms TGLExt.TimeGravitonMatrix.Eg_projMinus
#print axioms TGLExt.TimeGravitonMatrix.Eg_rootPlus
#print axioms TGLExt.TimeGravitonMatrix.Eg_rootMinus
#print axioms TGLExt.TimeGravitonMatrix.Eg_one
#print axioms TGLExt.TimeGravitonMatrix.Eg_trace
#print axioms TGLExt.TimeGravitonMatrix.four_blocks
#print axioms TGLExt.TimeGravitonMatrix.blockPM_rootPlus
#print axioms TGLExt.TimeGravitonMatrix.blockMP_rootPlus
#print axioms TGLExt.TimeGravitonMatrix.blockPM_rootMinus
#print axioms TGLExt.TimeGravitonMatrix.blockMP_rootMinus
#print axioms TGLExt.TimeGravitonMatrix.C_state
#print axioms TGLExt.TimeGravitonMatrix.density_transport
#print axioms TGLExt.TimeGravitonMatrix.transported_reading
#print axioms TGLExt.TimeGravitonMatrix.parity_preserved
#print axioms TGLExt.TimeGravitonMatrix.angFamily_star
#print axioms TGLExt.TimeGravitonMatrix.rootPlus_phase
#print axioms TGLExt.TimeGravitonMatrix.rootMinus_phase
#print axioms TGLExt.TimeGravitonMatrix.phase_frequency
#print axioms TGLExt.TimeGravitonMatrix.concrete_nonzero_modes
#print axioms TGLExt.TimeGravitonMatrix.spectralBasis_normalization
#print axioms TGLExt.TimeGravitonMatrix.spectral_roundtrip
#print axioms TGLExt.TimeGravitonMatrix.Eg_as_diagExpect
#print axioms TGLExt.TimeGravitonMatrix.Eg_as_nameOp
#print axioms TGLExt.TimeGravitonMatrix.sourceG_density
#print axioms TGLExt.TimeGravitonMatrix.Hpos_spectral
#print axioms TGLExt.TimeGravitonMatrix.singleJump_rate
#print axioms TGLExt.TimeGravitonMatrix.positive_parameters_inhabited
