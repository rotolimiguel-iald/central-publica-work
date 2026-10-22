import ExchangeEntropyResponse
import ModularCostDerivative

set_option autoImplicit false
set_option maxHeartbeats 5000000

namespace ChatgptAudit.Exchange055
open TGLExt Matrix Filter Topology Set
open ChatgptAudit ChatgptAudit.Observable035 ChatgptAudit.Angular034
  ChatgptAudit.Cocycle030 ChatgptAudit.Density033 ChatgptAudit.Covariant053
  ChatgptAudit.Cost054
open scoped Kronecker
noncomputable section

/-- The specified exchange interaction, on the actual two-site prefix. -/
def exchangeGeneratorMatrix : Matrix (chainIdx 1) (chainIdx 1) ℂ :=
  (1/2 : ℂ) • (pauliXMatrix ⊗ₖ pauliXMatrix + pauliYMatrix ⊗ₖ pauliYMatrix)

/-- The independently chosen energy levels are zero and one. -/
def exchangeNumberMatrix : Matrix (Fin 2) (Fin 2) ℂ := !![0,0;0,1]

def exchangeEnergy0Matrix : Matrix (chainIdx 1) (chainIdx 1) ℂ :=
  exchangeNumberMatrix ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ)

def exchangeEnergy1Matrix : Matrix (chainIdx 1) (chainIdx 1) ℂ :=
  (1 : Matrix (Fin 2) (Fin 2) ℂ) ⊗ₖ exchangeNumberMatrix

theorem exchange_generator_matrix_entry (i j : chainIdx 1) :
    exchangeGeneratorMatrix i j=
      if i=(0,1) ∧ j=(1,0) then 1 else if i=(1,0) ∧ j=(0,1) then 1 else 0 := by
  rcases i with ⟨i0,i1⟩
  rcases j with ⟨j0,j1⟩
  fin_cases i0 <;> fin_cases i1 <;> fin_cases j0 <;> fin_cases j1 <;>
    norm_num [exchangeGeneratorMatrix, pauliXMatrix, pauliYMatrix,
      Matrix.kroneckerMap_apply]

theorem exchange_generator_matrix_hermitian : exchangeGeneratorMatrix.IsHermitian := by
  ext ⟨i0,i1⟩ ⟨j0,j1⟩
  fin_cases i0 <;> fin_cases i1 <;> fin_cases j0 <;> fin_cases j1 <;>
    norm_num [Matrix.conjTranspose_apply, exchange_generator_matrix_entry]

theorem exchange_generator_matrix_cube :
    exchangeGeneratorMatrix*exchangeGeneratorMatrix*exchangeGeneratorMatrix=exchangeGeneratorMatrix := by
  ext ⟨i0,i1⟩ ⟨j0,j1⟩
  fin_cases i0 <;> fin_cases i1 <;> fin_cases j0 <;> fin_cases j1 <;>
    norm_num [Matrix.mul_apply, Fintype.sum_prod_type, Fin.sum_univ_two,
      exchange_generator_matrix_entry]

theorem exchange_energy0_matrix_hermitian : exchangeEnergy0Matrix.IsHermitian := by
  ext ⟨i0,i1⟩ ⟨j0,j1⟩
  fin_cases i0 <;> fin_cases i1 <;> fin_cases j0 <;> fin_cases j1 <;>
    norm_num [Matrix.conjTranspose_apply, exchangeEnergy0Matrix, exchangeNumberMatrix,
      Matrix.kroneckerMap_apply, Matrix.one_apply]

theorem exchange_energy1_matrix_hermitian : exchangeEnergy1Matrix.IsHermitian := by
  ext ⟨i0,i1⟩ ⟨j0,j1⟩
  fin_cases i0 <;> fin_cases i1 <;> fin_cases j0 <;> fin_cases j1 <;>
    norm_num [Matrix.conjTranspose_apply, exchangeEnergy1Matrix, exchangeNumberMatrix,
      Matrix.kroneckerMap_apply, Matrix.one_apply]

theorem exchange_generator_matrix_conserves_energy :
    exchangeGeneratorMatrix*(exchangeEnergy0Matrix+exchangeEnergy1Matrix)=
      (exchangeEnergy0Matrix+exchangeEnergy1Matrix)*exchangeGeneratorMatrix := by
  ext ⟨i0,i1⟩ ⟨j0,j1⟩
  fin_cases i0 <;> fin_cases i1 <;> fin_cases j0 <;> fin_cases j1 <;>
    norm_num [Matrix.mul_apply, Fintype.sum_prod_type, Fin.sum_univ_two,
      exchange_generator_matrix_entry, exchangeEnergy0Matrix, exchangeEnergy1Matrix,
      exchangeNumberMatrix, Matrix.kroneckerMap_apply, Matrix.one_apply]

/-- A polynomial formula, subsequently identified with the same boundedPhase used in 054. -/
def exchangeUnitaryMatrix (t : ℝ) : Matrix (chainIdx 1) (chainIdx 1) ℂ :=
  1+(Real.cos t-1) • (exchangeGeneratorMatrix*exchangeGeneratorMatrix)+
    Real.sin t • (Complex.I • exchangeGeneratorMatrix)

theorem exchange_unitary_matrix_entry (t : ℝ) (i j : chainIdx 1) :
    exchangeUnitaryMatrix t i j=
      if i=j then (if i.1=i.2 then 1 else (Real.cos t : ℂ))
      else if i.1≠i.2 ∧ j=(i.2,i.1) then (Real.sin t : ℂ)*Complex.I else 0 := by
  rcases i with ⟨i0,i1⟩
  rcases j with ⟨j0,j1⟩
  fin_cases i0 <;> fin_cases i1 <;> fin_cases j0 <;> fin_cases j1 <;>
    norm_num [exchangeUnitaryMatrix, Matrix.mul_apply, Fintype.sum_prod_type,
      Fin.sum_univ_two, exchange_generator_matrix_entry, Matrix.one_apply,
      Matrix.smul_apply, Complex.real_smul]
  all_goals push_cast
  all_goals ring

def exchangeGenerator (P : SiteProfile) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  towerPi P exchangeGeneratorMatrix

def exchangeEnergy0 (P : SiteProfile) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  towerPi P exchangeEnergy0Matrix

def exchangeEnergy1 (P : SiteProfile) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  towerPi P exchangeEnergy1Matrix

def exchangeUnitary (P : SiteProfile) (t : ℝ) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  towerPi P (exchangeUnitaryMatrix t)

theorem exchange_generator_selfadjoint (P : SiteProfile) : IsSelfAdjoint (exchangeGenerator P) :=
  tower_local_selfadjoint P 1 exchangeGeneratorMatrix exchange_generator_matrix_hermitian

theorem exchange_generator_mem_factor (P : SiteProfile) : exchangeGenerator P∈theFactorObject P :=
  towerPi_mem_factor _

theorem exchange_energy0_selfadjoint (P : SiteProfile) : IsSelfAdjoint (exchangeEnergy0 P) :=
  tower_local_selfadjoint P 1 exchangeEnergy0Matrix exchange_energy0_matrix_hermitian

theorem exchange_energy1_selfadjoint (P : SiteProfile) : IsSelfAdjoint (exchangeEnergy1 P) :=
  tower_local_selfadjoint P 1 exchangeEnergy1Matrix exchange_energy1_matrix_hermitian

theorem exchange_generator_cube (P : SiteProfile) :
    exchangeGenerator P*exchangeGenerator P*exchangeGenerator P=exchangeGenerator P := by
  simp only [exchangeGenerator, ←towerPi_mul, exchange_generator_matrix_cube]

theorem exchange_generator_conserves_energy (P : SiteProfile) :
    exchangeGenerator P*(exchangeEnergy0 P+exchangeEnergy1 P)=
      (exchangeEnergy0 P+exchangeEnergy1 P)*exchangeGenerator P := by
  simpa only [map_mul, map_add] using
    congrArg (towerPiAlgHom P 1) exchange_generator_matrix_conserves_energy

theorem exchange_pi_real_smul (P : SiteProfile) (r : ℝ)
    (a : Matrix (chainIdx 1) (chainIdx 1) ℂ) : towerPi P (r • a)=r • towerPi P a :=
  ((towerPiLinear P 1).restrictScalars ℝ).map_smul r a

theorem exchange_unitary_formula (P : SiteProfile) (t : ℝ) :
    exchangeUnitary P t=1+(Real.cos t-1) • (exchangeGenerator P*exchangeGenerator P)+
      Real.sin t • (Complex.I • exchangeGenerator P) := by
  simp only [exchangeUnitary, exchangeUnitaryMatrix, towerPi_add, exchange_pi_real_smul,
    towerPi_one, towerPi_mul, towerPi_smul, exchangeGenerator]

theorem exchange_unitary_zero (P : SiteProfile) : exchangeUnitary P 0=1 := by
  simp [exchange_unitary_formula]

theorem exchange_unitary_derivative_polynomial (P : SiteProfile) (t : ℝ) :
    HasDerivAt (exchangeUnitary P)
      ((-Real.sin t) • (exchangeGenerator P*exchangeGenerator P)+
        Real.cos t • (Complex.I • exchangeGenerator P)) t := by
  have h := ((hasDerivAt_const t (1 : TowerHilbert P →L[ℂ] TowerHilbert P)).add
    (((Real.hasDerivAt_cos t).sub_const 1).smul_const
      (exchangeGenerator P*exchangeGenerator P))).add
    ((Real.hasDerivAt_sin t).smul_const (Complex.I • exchangeGenerator P))
  have hf : (fun s : ℝ => 1+(Real.cos s-1) • (exchangeGenerator P*exchangeGenerator P)+
      Real.sin s • (Complex.I • exchangeGenerator P))=exchangeUnitary P := by
    funext s
    exact (exchange_unitary_formula P s).symm
  rw [hf] at h
  simpa only [zero_add] using h

theorem exchange_unitary_velocity (P : SiteProfile) (t : ℝ) :
    (Complex.I • exchangeGenerator P)*exchangeUnitary P t=
      (-Real.sin t) • (exchangeGenerator P*exchangeGenerator P)+
        Real.cos t • (Complex.I • exchangeGenerator P) := by
  have hg : exchangeGenerator P*(exchangeGenerator P*exchangeGenerator P)=exchangeGenerator P := by
    rw [←mul_assoc, exchange_generator_cube]
  have hi : (Complex.I • exchangeGenerator P)*(Complex.I • exchangeGenerator P)=
      -(exchangeGenerator P*exchangeGenerator P) := by
    simp only [smul_mul_assoc, mul_smul_comm, smul_smul, Complex.I_mul_I, neg_one_smul]
  calc
    (Complex.I • exchangeGenerator P)*exchangeUnitary P t=
        Complex.I • exchangeGenerator P+
          (Real.cos t-1) • (Complex.I • exchangeGenerator P)+
          Real.sin t • (-(exchangeGenerator P*exchangeGenerator P)) := by
      rw [exchange_unitary_formula, mul_add, mul_add, mul_one, mul_smul_comm,
        smul_mul_assoc, hg, mul_smul_comm, hi]
    _ = ((1 : ℝ)+(Real.cos t-1)) • (Complex.I • exchangeGenerator P)-
        Real.sin t • (exchangeGenerator P*exchangeGenerator P) := by
      simp only [add_smul, one_smul, smul_neg, sub_eq_add_neg]
    _ = _ := by
      rw [show (1 : ℝ)+(Real.cos t-1)=Real.cos t by ring]
      simp only [neg_smul, sub_eq_add_neg]
      abel

theorem exchange_unitary_derivative (P : SiteProfile) (t : ℝ) :
    HasDerivAt (exchangeUnitary P) ((Complex.I • exchangeGenerator P)*exchangeUnitary P t) t := by
  rw [exchange_unitary_velocity]
  exact exchange_unitary_derivative_polynomial P t

/-- Uniqueness is proved by differentiating the inverse-phase product on the whole real line. -/
theorem exchange_inverse_phase_product (P : SiteProfile) (t : ℝ) :
    boundedPhase P (exchangeGenerator P) (-t)*exchangeUnitary P t=1 := by
  have hd (s : ℝ) : HasDerivAt
      (fun r : ℝ => boundedPhase P (exchangeGenerator P) (-r)*exchangeUnitary P r) 0 s := by
    have h := (negative_phase_derivative P (exchangeGenerator P) s).mul
      (exchange_unitary_derivative P s)
    simpa only [neg_mul, mul_assoc, neg_add_cancel] using h
  have h := is_const_of_deriv_eq_zero (fun s => (hd s).differentiableAt)
    (fun s => (hd s).deriv) t 0
  simpa only [neg_zero, bounded_phase_zero, exchange_unitary_zero, one_mul] using h

theorem exchange_unitary_eq_boundedPhase (P : SiteProfile) (t : ℝ) :
    exchangeUnitary P t=boundedPhase P (exchangeGenerator P) t := by
  have hu := (Unitary.mem_iff.mp
    (bounded_phase_unitary P (exchangeGenerator P) (exchange_generator_selfadjoint P) t)).2
  rw [bounded_phase_star P _ (exchange_generator_selfadjoint P)] at hu
  calc
    exchangeUnitary P t=
        (boundedPhase P (exchangeGenerator P) t*boundedPhase P (exchangeGenerator P) (-t))*
          exchangeUnitary P t := by rw [hu, one_mul]
    _ = boundedPhase P (exchangeGenerator P) t := by
      rw [mul_assoc, exchange_inverse_phase_product, mul_one]

theorem exchange_unitary_unitary (P : SiteProfile) (t : ℝ) : exchangeUnitary P t∈unitary _ := by
  rw [exchange_unitary_eq_boundedPhase]
  exact bounded_phase_unitary P _ (exchange_generator_selfadjoint P) t

theorem exchange_unitary_mem_factor (P : SiteProfile) (t : ℝ) :
    exchangeUnitary P t∈theFactorObject P := towerPi_mem_factor _

/-- The evolved state is evaluated by the actual unitary in the same representation. -/
def exchangeState (P : SiteProfile) (t : ℝ) (B : TowerHilbert P →L[ℂ] TowerHilbert P) : ℂ :=
  omegaState P (star (exchangeUnitary P t)*B*exchangeUnitary P t)

theorem exchange_state_prefix (P : SiteProfile) (t : ℝ)
    (a : Matrix (chainIdx 1) (chainIdx 1) ℂ) :
    exchangeState P t (towerPi P a)=
      tState P 1 ((exchangeUnitaryMatrix t)ᴴ*a*exchangeUnitaryMatrix t) := by
  simp only [exchangeState, exchangeUnitary, ContinuousLinearMap.star_eq_adjoint,
    ←towerPi_star, ←towerPi_mul, omegaState_pi]

theorem exchange_first_site_prefix (P : SiteProfile) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    siteOperator P 0 a=towerPi P (a ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ)) := by
  change towerPi P a=towerPi P (towerStep a)
  exact (towerPi_step a).symm

theorem exchange_second_site_prefix (P : SiteProfile) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    siteOperator P 1 a=towerPi P ((1 : Matrix (Fin 2) (Fin 2) ℂ) ⊗ₖ a) := rfl

/-- The full first-site restriction, including arbitrary off-diagonal matrix entries. -/
theorem exchange_marginal0 (P : SiteProfile) (t : ℝ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    exchangeState P t (siteOperator P 0 a)=
      (exchangeWeight (P.w 0) (P.w 1) t : ℂ)*a 0 0+
        ((1-exchangeWeight (P.w 0) (P.w 1) t : ℝ) : ℂ)*a 1 1 := by
  rw [exchange_first_site_prefix, exchange_state_prefix]
  have hc : (Real.cos t : ℂ)^2=1-(Real.sin t : ℂ)^2 := by
    exact_mod_cast (show Real.cos t^2=1-Real.sin t^2 by
      nlinarith only [Real.sin_sq_add_cos_sq t])
  norm_num [tState, towerW, siteW, Matrix.mul_apply, Matrix.conjTranspose_apply,
    Fintype.sum_prod_type, Fin.sum_univ_two, exchange_unitary_matrix_entry,
    Matrix.kroneckerMap_apply, Matrix.one_apply, exchangeWeight]
  all_goals push_cast
  all_goals ring_nf
  all_goals simp only [hc]
  all_goals ring

/-- The full second-site restriction, not merely its number expectation. -/
theorem exchange_marginal1 (P : SiteProfile) (t : ℝ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    exchangeState P t (siteOperator P 1 a)=
      (exchangeWeight (P.w 1) (P.w 0) t : ℂ)*a 0 0+
        ((1-exchangeWeight (P.w 1) (P.w 0) t : ℝ) : ℂ)*a 1 1 := by
  rw [exchange_second_site_prefix, exchange_state_prefix]
  have hc : (Real.cos t : ℂ)^2=1-(Real.sin t : ℂ)^2 := by
    exact_mod_cast (show Real.cos t^2=1-Real.sin t^2 by
      nlinarith only [Real.sin_sq_add_cos_sq t])
  norm_num [tState, towerW, siteW, Matrix.mul_apply, Matrix.conjTranspose_apply,
    Fintype.sum_prod_type, Fin.sum_univ_two, exchange_unitary_matrix_entry,
    Matrix.kroneckerMap_apply, Matrix.one_apply, exchangeWeight]
  all_goals push_cast
  all_goals ring_nf
  all_goals simp only [hc]
  all_goals ring

/-- The actual probability of the zero-level projection in the first restriction. -/
def exchangeWeight0 (P : SiteProfile) (t : ℝ) : ℝ :=
  (exchangeState P t (siteOperator P 0
    ((1 : Matrix (Fin 2) (Fin 2) ℂ)-exchangeNumberMatrix))).re

/-- The actual probability of the zero-level projection in the second restriction. -/
def exchangeWeight1 (P : SiteProfile) (t : ℝ) : ℝ :=
  (exchangeState P t (siteOperator P 1
    ((1 : Matrix (Fin 2) (Fin 2) ℂ)-exchangeNumberMatrix))).re

theorem exchange_weight0_formula (P : SiteProfile) (t : ℝ) :
    exchangeWeight0 P t=exchangeWeight (P.w 0) (P.w 1) t := by
  unfold exchangeWeight0
  rw [exchange_marginal0]
  norm_num [exchangeNumberMatrix, Matrix.sub_apply, Matrix.one_apply]

theorem exchange_weight1_formula (P : SiteProfile) (t : ℝ) :
    exchangeWeight1 P t=exchangeWeight (P.w 1) (P.w 0) t := by
  unfold exchangeWeight1
  rw [exchange_marginal1]
  norm_num [exchangeNumberMatrix, Matrix.sub_apply, Matrix.one_apply]

theorem exchange_energy0_site (P : SiteProfile) :
    exchangeEnergy0 P=siteOperator P 0 exchangeNumberMatrix :=
  (exchange_first_site_prefix P exchangeNumberMatrix).symm

theorem exchange_energy1_site (P : SiteProfile) :
    exchangeEnergy1 P=siteOperator P 1 exchangeNumberMatrix := rfl

theorem exchange_energy0_expectation (P : SiteProfile) (t : ℝ) :
    (exchangeState P t (exchangeEnergy0 P)).re=1-exchangeWeight (P.w 0) (P.w 1) t := by
  rw [exchange_energy0_site, exchange_marginal0]
  norm_num [exchangeNumberMatrix]

theorem exchange_energy1_expectation (P : SiteProfile) (t : ℝ) :
    (exchangeState P t (exchangeEnergy1 P)).re=1-exchangeWeight (P.w 1) (P.w 0) t := by
  rw [exchange_energy1_site, exchange_marginal1]
  norm_num [exchangeNumberMatrix]

theorem exchange_energy0_reference (P : SiteProfile) :
    (omegaState P (exchangeEnergy0 P)).re=1-P.w 0 := by
  simpa only [exchangeState, exchange_unitary_zero, star_one, one_mul, mul_one,
    exchange_weight_zero] using exchange_energy0_expectation P 0

theorem exchange_energy1_reference (P : SiteProfile) :
    (omegaState P (exchangeEnergy1 P)).re=1-P.w 1 := by
  simpa only [exchangeState, exchange_unitary_zero, star_one, one_mul, mul_one,
    exchange_weight_zero] using exchange_energy1_expectation P 0

def exchangeHeat0 (P : SiteProfile) (t : ℝ) : ℝ :=
  (exchangeState P t (exchangeEnergy0 P)).re-(omegaState P (exchangeEnergy0 P)).re

def exchangeHeat1 (P : SiteProfile) (t : ℝ) : ℝ :=
  (exchangeState P t (exchangeEnergy1 P)).re-(omegaState P (exchangeEnergy1 P)).re

theorem exchange_heat0_formula (P : SiteProfile) (t : ℝ) :
    exchangeHeat0 P t=exchangeHeat (P.w 0) (P.w 1) t := by
  rw [exchangeHeat0, exchange_energy0_expectation, exchange_energy0_reference,
    exchange_heat_eq_displacement]
  ring

theorem exchange_heat1_formula (P : SiteProfile) (t : ℝ) :
    exchangeHeat1 P t=exchangeHeat (P.w 1) (P.w 0) t := by
  rw [exchangeHeat1, exchange_energy1_expectation, exchange_energy1_reference,
    exchange_heat_eq_displacement]
  ring

theorem exchange_heat_total_zero (P : SiteProfile) (t : ℝ) :
    exchangeHeat0 P t+exchangeHeat1 P t=0 := by
  rw [exchange_heat0_formula, exchange_heat1_formula]
  exact exchange_heat_conserved _ _ _

theorem exchange_total_energy_conserved (P : SiteProfile) (t : ℝ) :
    (exchangeState P t (exchangeEnergy0 P)).re+(exchangeState P t (exchangeEnergy1 P)).re=
      (omegaState P (exchangeEnergy0 P)).re+(omegaState P (exchangeEnergy1 P)).re := by
  have h := exchange_heat_total_zero P t
  unfold exchangeHeat0 exchangeHeat1 at h
  linarith

def exchangeCurrent0Matrix : Matrix (chainIdx 1) (chainIdx 1) ℂ :=
  Complex.I • (exchangeEnergy0Matrix*exchangeGeneratorMatrix-
    exchangeGeneratorMatrix*exchangeEnergy0Matrix)

def exchangeCurrent1Matrix : Matrix (chainIdx 1) (chainIdx 1) ℂ :=
  Complex.I • (exchangeEnergy1Matrix*exchangeGeneratorMatrix-
    exchangeGeneratorMatrix*exchangeEnergy1Matrix)

def exchangeCurrent0 (P : SiteProfile) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  towerPi P exchangeCurrent0Matrix

def exchangeCurrent1 (P : SiteProfile) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  towerPi P exchangeCurrent1Matrix

theorem exchange_current0_commutator (P : SiteProfile) :
    exchangeCurrent0 P=Complex.I •
      (exchangeEnergy0 P*exchangeGenerator P-exchangeGenerator P*exchangeEnergy0 P) := by
  change (towerPiAlgHom P 1) exchangeCurrent0Matrix= _
  simp only [exchangeCurrent0Matrix, map_smul, map_sub, map_mul]
  rfl

theorem exchange_current1_commutator (P : SiteProfile) :
    exchangeCurrent1 P=Complex.I •
      (exchangeEnergy1 P*exchangeGenerator P-exchangeGenerator P*exchangeEnergy1 P) := by
  change (towerPiAlgHom P 1) exchangeCurrent1Matrix= _
  simp only [exchangeCurrent1Matrix, map_smul, map_sub, map_mul]
  rfl

theorem exchange_current0_matrix_hermitian : exchangeCurrent0Matrix.IsHermitian := by
  ext ⟨i0,i1⟩ ⟨j0,j1⟩
  fin_cases i0 <;> fin_cases i1 <;> fin_cases j0 <;> fin_cases j1 <;>
    norm_num [exchangeCurrent0Matrix, Matrix.conjTranspose_apply, Matrix.mul_apply,
      Fintype.sum_prod_type, Fin.sum_univ_two, exchange_generator_matrix_entry,
      exchangeEnergy0Matrix, exchangeNumberMatrix, Matrix.kroneckerMap_apply, Matrix.one_apply]

theorem exchange_current_matrices_cancel : exchangeCurrent0Matrix+exchangeCurrent1Matrix=0 := by
  ext ⟨i0,i1⟩ ⟨j0,j1⟩
  fin_cases i0 <;> fin_cases i1 <;> fin_cases j0 <;> fin_cases j1 <;>
    norm_num [exchangeCurrent0Matrix, exchangeCurrent1Matrix, Matrix.mul_apply,
      Fintype.sum_prod_type, Fin.sum_univ_two, exchange_generator_matrix_entry,
      exchangeEnergy0Matrix, exchangeEnergy1Matrix, exchangeNumberMatrix,
      Matrix.kroneckerMap_apply, Matrix.one_apply]

theorem exchange_current1_matrix_hermitian : exchangeCurrent1Matrix.IsHermitian := by
  have h : exchangeCurrent1Matrix= -exchangeCurrent0Matrix := by
    calc
      exchangeCurrent1Matrix= -exchangeCurrent0Matrix+
          (exchangeCurrent0Matrix+exchangeCurrent1Matrix) := by abel
      _ = -exchangeCurrent0Matrix := by rw [exchange_current_matrices_cancel, add_zero]
  rw [h]
  exact exchange_current0_matrix_hermitian.neg

theorem exchange_current0_selfadjoint (P : SiteProfile) : IsSelfAdjoint (exchangeCurrent0 P) :=
  tower_local_selfadjoint P 1 exchangeCurrent0Matrix exchange_current0_matrix_hermitian

theorem exchange_current1_selfadjoint (P : SiteProfile) : IsSelfAdjoint (exchangeCurrent1 P) :=
  tower_local_selfadjoint P 1 exchangeCurrent1Matrix exchange_current1_matrix_hermitian

theorem exchange_currents_cancel (P : SiteProfile) : exchangeCurrent0 P+exchangeCurrent1 P=0 := by
  rw [exchangeCurrent0, exchangeCurrent1, ←towerPi_add, exchange_current_matrices_cancel]
  exact (towerPiLinear P 1).map_zero

theorem exchange_current0_expectation (P : SiteProfile) (t : ℝ) :
    (exchangeState P t (exchangeCurrent0 P)).re=
      2*(P.w 0-P.w 1)*Real.sin t*Real.cos t := by
  rw [exchangeCurrent0, exchange_state_prefix]
  norm_num [tState, towerW, siteW, Matrix.mul_apply, Matrix.conjTranspose_apply,
    Fintype.sum_prod_type, Fin.sum_univ_two, exchange_unitary_matrix_entry,
    exchangeCurrent0Matrix, exchangeEnergy0Matrix, exchangeNumberMatrix,
    exchange_generator_matrix_entry, Matrix.kroneckerMap_apply, Matrix.one_apply,
    Complex.mul_re, Complex.mul_im]
  all_goals ring

theorem exchange_current1_expectation (P : SiteProfile) (t : ℝ) :
    (exchangeState P t (exchangeCurrent1 P)).re=
      2*(P.w 1-P.w 0)*Real.sin t*Real.cos t := by
  have h : exchangeCurrent1 P= -exchangeCurrent0 P := by
    calc
      exchangeCurrent1 P= -exchangeCurrent0 P+(exchangeCurrent0 P+exchangeCurrent1 P) := by abel
      _ = -exchangeCurrent0 P := by rw [exchange_currents_cancel, add_zero]
  rw [h]
  have he : exchangeState P t (-exchangeCurrent0 P)= -exchangeState P t (exchangeCurrent0 P) := by
    simp [exchangeState, omegaState]
  rw [he, Complex.neg_re, exchange_current0_expectation]
  ring

/-- The first microscopic continuity equation, with the current defined independently. -/
theorem exchange_heat0_current_derivative (P : SiteProfile) (t : ℝ) :
    HasDerivAt (exchangeHeat0 P) (exchangeState P t (exchangeCurrent0 P)).re t := by
  have hf : exchangeHeat0 P=exchangeHeat (P.w 0) (P.w 1) :=
    funext (exchange_heat0_formula P)
  rw [hf, exchange_current0_expectation]
  exact exchange_heat_derivative _ _ _

/-- The second current has the opposite sign and the same unitary evolution. -/
theorem exchange_heat1_current_derivative (P : SiteProfile) (t : ℝ) :
    HasDerivAt (exchangeHeat1 P) (exchangeState P t (exchangeCurrent1 P)).re t := by
  have hf : exchangeHeat1 P=exchangeHeat (P.w 1) (P.w 0) :=
    funext (exchange_heat1_formula P)
  rw [hf, exchange_current1_expectation]
  exact exchange_heat_derivative _ _ _

#print axioms exchangeGeneratorMatrix
#print axioms exchangeNumberMatrix
#print axioms exchangeEnergy0Matrix
#print axioms exchangeEnergy1Matrix
#print axioms exchange_generator_matrix_entry
#print axioms exchange_generator_matrix_hermitian
#print axioms exchange_generator_matrix_cube
#print axioms exchange_energy0_matrix_hermitian
#print axioms exchange_energy1_matrix_hermitian
#print axioms exchange_generator_matrix_conserves_energy
#print axioms exchangeUnitaryMatrix
#print axioms exchange_unitary_matrix_entry
#print axioms exchangeGenerator
#print axioms exchangeEnergy0
#print axioms exchangeEnergy1
#print axioms exchangeUnitary
#print axioms exchange_generator_selfadjoint
#print axioms exchange_generator_mem_factor
#print axioms exchange_energy0_selfadjoint
#print axioms exchange_energy1_selfadjoint
#print axioms exchange_generator_cube
#print axioms exchange_generator_conserves_energy
#print axioms exchange_pi_real_smul
#print axioms exchange_unitary_formula
#print axioms exchange_unitary_zero
#print axioms exchange_unitary_derivative_polynomial
#print axioms exchange_unitary_velocity
#print axioms exchange_unitary_derivative
#print axioms exchange_inverse_phase_product
#print axioms exchange_unitary_eq_boundedPhase
#print axioms exchange_unitary_unitary
#print axioms exchange_unitary_mem_factor
#print axioms exchangeState
#print axioms exchange_state_prefix
#print axioms exchange_first_site_prefix
#print axioms exchange_second_site_prefix
#print axioms exchange_marginal0
#print axioms exchange_marginal1
#print axioms exchangeWeight0
#print axioms exchangeWeight1
#print axioms exchange_weight0_formula
#print axioms exchange_weight1_formula
#print axioms exchange_energy0_site
#print axioms exchange_energy1_site
#print axioms exchange_energy0_expectation
#print axioms exchange_energy1_expectation
#print axioms exchange_energy0_reference
#print axioms exchange_energy1_reference
#print axioms exchangeHeat0
#print axioms exchangeHeat1
#print axioms exchange_heat0_formula
#print axioms exchange_heat1_formula
#print axioms exchange_heat_total_zero
#print axioms exchange_total_energy_conserved
#print axioms exchangeCurrent0Matrix
#print axioms exchangeCurrent1Matrix
#print axioms exchangeCurrent0
#print axioms exchangeCurrent1
#print axioms exchange_current0_commutator
#print axioms exchange_current1_commutator
#print axioms exchange_current0_matrix_hermitian
#print axioms exchange_current_matrices_cancel
#print axioms exchange_current1_matrix_hermitian
#print axioms exchange_current0_selfadjoint
#print axioms exchange_current1_selfadjoint
#print axioms exchange_currents_cancel
#print axioms exchange_current0_expectation
#print axioms exchange_current1_expectation
#print axioms exchange_heat0_current_derivative
#print axioms exchange_heat1_current_derivative
end
end ChatgptAudit.Exchange055
