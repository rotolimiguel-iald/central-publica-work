-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_035 (06/09/2026), transposta em 06/09/2026
-- Lote 035..037 (processo da ORDEM_008 cumprido pela bancada: zero instancias anonimas, lote compilado junto
--   num diretorio limpo). 035: DEFORMACOES OBSERVAVEIS e AREA DE FISHER — derivadas da conjugacao unitaria e
--   do estado, observaveis de Pauli por sitio na torre real, duas leituras independentes (jacobiano nao
--   degenerado), medicao conjunta efetiva (sitios distintos), probabilidades normalizadas e suas derivadas,
--   matriz de Fisher na origem, densidade de area de Fisher (4/9 como area de coordenadas). 036: AREA OPTICA e
--   LIBERDADE RADIATIVA — a area induzida dos campos de Jacobi da metrica 029 ligada a curvatura real
--   (A2(0) = -Ric(d,d); A4(0) = 2(tr K)^2 - 2 tr(K_TF^T K_TF)); germes de area distintos para shears
--   distintos. 037: QUARTA ORDEM, AREA e RELOGIO — limites entropicos e de area em 4a ordem; NEGATIVO
--   MEDIDO: o casamento adicional em 4a ordem com parametro comum fixo FALHA (delta4 >= (7/48) B > 0);
--   a reparametrizacao do relogio t + lambda t^3 cancela o defeito ate 4a ordem (controle do relogio relativo).
--   Estatuto [REAL / DERIVED / INPUT / OPEN]: X, Y, sitios e normalizacao sao INPUT; a familia optica
--   lorentziana e INPUT; identificacao da inscricao angular com area fisica, retorno estabilizador, ponte
--   regiao-algebra, escala, assinatura, dinamica gravitacional e H3 geral NAO pagos.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 14/14, 8/8 (via manifesto), 10/10; manifestos
--   1051/977; 3/3 auditores exit 0; recompilacao INDEPENDENTE 15/15, axiomas no trio; guarda de colisao;
--   enunciados lidos. Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito: zero anonimas).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.UnitaryStateDerivative
import TGLExt.SitePauliObservables

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit.Observable035
open Matrix TGLExt ChatgptAudit ChatgptAudit.Angular034 ChatgptAudit.Thermal025
noncomputable section

def pauliOrbit (P : SiteProfile) (n m : ℕ) (s t : ℝ) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  operatorOrbit P (sitePauliX P n) (sitePauliX P m) s t

def pauliExpectation (P : SiteProfile) (n m : ℕ)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P) (s t : ℝ) : ℂ :=
  orbitExpectation P (sitePauliX P n) (sitePauliX P m) B s t

/-- A fixed Y observable is read in the rotated state. -/
def pauliYReading (P : SiteProfile) (n m k : ℕ) (s t : ℝ) : ℝ :=
  (pauliExpectation P n m (sitePauliY P k) s t).re

/-- This Jacobian is defined from derivatives of actual expectation values. -/
def pauliObservableJacobian (P : SiteProfile) (n m : ℕ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![deriv (fun s : ℝ => pauliYReading P n m n s 0) 0,
      deriv (fun t : ℝ => pauliYReading P n m n 0 t) 0;
     deriv (fun s : ℝ => pauliYReading P n m m s 0) 0,
      deriv (fun t : ℝ => pauliYReading P n m m 0 t) 0]

theorem pauli_orbit_unitary (P : SiteProfile) (n m : ℕ) (s t : ℝ) :
    pauliOrbit P n m s t∈unitary _ :=
  orbit_unitary P (sitePauliX P n) (sitePauliX P m)
    (site_pauli_x_selfadjoint P n) (site_pauli_x_selfadjoint P m) s t

theorem pauli_orbit_mem_factor (P : SiteProfile) (n m : ℕ) (s t : ℝ) :
    pauliOrbit P n m s t∈theFactorObject P :=
  orbit_mem_factor P (sitePauliX P n) (sitePauliX P m)
    (site_pauli_x_mem_factor P n) (site_pauli_x_mem_factor P m) s t

theorem pauli_expectation_vector_state (P : SiteProfile) (n m : ℕ)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P) (s t : ℝ) :
    pauliExpectation P n m B s t=
      inner ℂ (pauliOrbit P n m s t (hOmega P))
        (B (pauliOrbit P n m s t (hOmega P))) :=
  orbit_vector_state P (sitePauliX P n) (sitePauliX P m) B s t

theorem pauli_y_reading_origin (P : SiteProfile) (n m k : ℕ) :
    pauliYReading P n m k 0 0=0 := by
  simp only [pauliYReading,pauliExpectation,orbit_expectation_origin,site_pauli_y_state,
    Complex.zero_re]

theorem pauli_y_first_axis_derivative (P : SiteProfile) (n m : ℕ) :
    HasDerivAt (fun s : ℝ => pauliYReading P n m n s 0)
      (2*(2*P.w n-1)) 0 := by
  have hd := orbit_expectation_first_derivative P
    (sitePauliX P n) (sitePauliX P m) (sitePauliY P n) (site_pauli_x_selfadjoint P n)
  rw [site_pauli_y_response] at hd
  change HasDerivAt
    (fun s : ℝ => (orbitExpectation P (sitePauliX P n) (sitePauliX P m)
      (sitePauliY P n) s 0).re) (2*(2*P.w n-1)) 0
  simpa only [Function.comp_def, Complex.reCLM_apply, Complex.ofReal_re] using
    (Complex.reCLM.hasFDerivAt.comp_hasDerivAt 0 hd)

theorem pauli_y_second_axis_derivative (P : SiteProfile) (n m : ℕ) :
    HasDerivAt (fun t : ℝ => pauliYReading P n m m 0 t)
      (2*(2*P.w m-1)) 0 := by
  have hd := orbit_expectation_second_derivative P
    (sitePauliX P n) (sitePauliX P m) (sitePauliY P m) (site_pauli_x_selfadjoint P m)
  rw [site_pauli_y_response] at hd
  change HasDerivAt
    (fun t : ℝ => (orbitExpectation P (sitePauliX P n) (sitePauliX P m)
      (sitePauliY P m) 0 t).re) (2*(2*P.w m-1)) 0
  simpa only [Function.comp_def, Complex.reCLM_apply, Complex.ofReal_re] using
    (Complex.reCLM.hasFDerivAt.comp_hasDerivAt 0 hd)

theorem pauli_y_first_cross_derivative (P : SiteProfile) {n m : ℕ} (h : n≠m) :
    HasDerivAt (fun s : ℝ => pauliYReading P n m m s 0) 0 0 := by
  have hd := orbit_expectation_first_derivative P
    (sitePauliX P n) (sitePauliX P m) (sitePauliY P m) (site_pauli_x_selfadjoint P n)
  have hz : Complex.I*omegaState P
      (sitePauliY P m*sitePauliX P n-sitePauliX P n*sitePauliY P m)=0 := by
    rw [(site_pauli_xy_commute P h).eq,sub_self]
    simp [omegaState]
  rw [hz] at hd
  change HasDerivAt
    (fun s : ℝ => (orbitExpectation P (sitePauliX P n) (sitePauliX P m)
      (sitePauliY P m) s 0).re) 0 0
  simpa only [Function.comp_def, Complex.reCLM_apply, Complex.zero_re] using
    (Complex.reCLM.hasFDerivAt.comp_hasDerivAt 0 hd)

theorem pauli_y_second_cross_derivative (P : SiteProfile) {n m : ℕ} (h : n≠m) :
    HasDerivAt (fun t : ℝ => pauliYReading P n m n 0 t) 0 0 := by
  have hd := orbit_expectation_second_derivative P
    (sitePauliX P n) (sitePauliX P m) (sitePauliY P n) (site_pauli_x_selfadjoint P m)
  have hz : Complex.I*omegaState P
      (sitePauliY P n*sitePauliX P m-sitePauliX P m*sitePauliY P n)=0 := by
    rw [(site_pauli_xy_commute P h.symm).eq,sub_self]
    simp [omegaState]
  rw [hz] at hd
  change HasDerivAt
    (fun t : ℝ => (orbitExpectation P (sitePauliX P n) (sitePauliX P m)
      (sitePauliY P n) 0 t).re) 0 0
  simpa only [Function.comp_def, Complex.reCLM_apply, Complex.zero_re] using
    (Complex.reCLM.hasFDerivAt.comp_hasDerivAt 0 hd)

theorem pauli_observable_jacobian_diagonal (P : SiteProfile) {n m : ℕ} (h : n≠m) :
    pauliObservableJacobian P n m = !![2*(2*P.w n-1),0;0,2*(2*P.w m-1)] := by
  simp only [pauliObservableJacobian,(pauli_y_first_axis_derivative P n m).deriv,
    (pauli_y_second_axis_derivative P n m).deriv,
    (pauli_y_first_cross_derivative P h).deriv,
    (pauli_y_second_cross_derivative P h).deriv]

theorem pauli_observable_jacobian_determinant (P : SiteProfile) {n m : ℕ} (h : n≠m) :
    (pauliObservableJacobian P n m).det=4*(2*P.w n-1)*(2*P.w m-1) := by
  rw [pauli_observable_jacobian_diagonal P h,Matrix.det_fin_two]
  simp
  ring

/-- Nontracial axes ensure invertibility, not a prescribed orientation. -/
theorem pauli_observable_jacobian_nondegenerate (P : SiteProfile) {n m : ℕ} (h : n≠m)
    (hn : P.w n≠1/2) (hm : P.w m≠1/2) :
    (pauliObservableJacobian P n m).det≠0 := by
  rw [pauli_observable_jacobian_determinant P h]
  apply mul_ne_zero
  · apply mul_ne_zero (by norm_num)
    intro hz
    apply hn
    linarith
  · intro hz
    apply hm
    linarith

theorem pauli_observable_jacobian_squared_determinant_positive
    (P : SiteProfile) {n m : ℕ} (h : n≠m)
    (hn : P.w n≠1/2) (hm : P.w m≠1/2) :
    0<((pauliObservableJacobian P n m).det)^2 :=
  sq_pos_of_ne_zero (pauli_observable_jacobian_nondegenerate P h hn hm)

theorem pauli_observable_jacobian_first_tracial (P : SiteProfile) {n m : ℕ} (h : n≠m)
    (hn : P.w n=1/2) : (pauliObservableJacobian P n m).det=0 := by
  rw [pauli_observable_jacobian_determinant P h,hn]
  norm_num

theorem pauli_observable_jacobian_second_tracial (P : SiteProfile) {n m : ℕ} (h : n≠m)
    (hm : P.w m=1/2) : (pauliObservableJacobian P n m).det=0 := by
  rw [pauli_observable_jacobian_determinant P h,hm]
  norm_num

theorem reference_pauli_observable_jacobian :
    pauliObservableJacobian thirdThermalReference 0 1 = !![-2/3,0;0,-2/3] := by
  rw [pauli_observable_jacobian_diagonal thirdThermalReference (by decide)]
  norm_num [thirdThermalReference]

theorem reference_pauli_observable_jacobian_determinant :
    (pauliObservableJacobian thirdThermalReference 0 1).det=4/9 := by
  rw [pauli_observable_jacobian_determinant thirdThermalReference (by decide)]
  norm_num [thirdThermalReference]

theorem tracial_pauli_observable_jacobian {n m : ℕ} (h : n≠m) :
    pauliObservableJacobian halfThermalReference n m=0 := by
  rw [pauli_observable_jacobian_diagonal halfThermalReference h]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [halfThermalReference]

#print axioms pauliOrbit
#print axioms pauliExpectation
#print axioms pauliYReading
#print axioms pauliObservableJacobian
#print axioms pauli_orbit_unitary
#print axioms pauli_orbit_mem_factor
#print axioms pauli_expectation_vector_state
#print axioms pauli_y_reading_origin
#print axioms pauli_y_first_axis_derivative
#print axioms pauli_y_second_axis_derivative
#print axioms pauli_y_first_cross_derivative
#print axioms pauli_y_second_cross_derivative
#print axioms pauli_observable_jacobian_diagonal
#print axioms pauli_observable_jacobian_determinant
#print axioms pauli_observable_jacobian_nondegenerate
#print axioms pauli_observable_jacobian_squared_determinant_positive
#print axioms pauli_observable_jacobian_first_tracial
#print axioms pauli_observable_jacobian_second_tracial
#print axioms reference_pauli_observable_jacobian
#print axioms reference_pauli_observable_jacobian_determinant
#print axioms tracial_pauli_observable_jacobian

end
end ChatgptAudit.Observable035
