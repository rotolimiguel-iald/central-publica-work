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
import TGLExt.AngularAreaObservability
import Mathlib.Analysis.InnerProductSpace.Positive

set_option autoImplicit false
set_option maxHeartbeats 1400000
namespace ChatgptAudit.Observable035
open TGLExt ChatgptAudit ChatgptAudit.Angular034 ChatgptAudit.Cocycle030
  ChatgptAudit.Density033
noncomputable section

local instance inst_UnitaryStateDerivative_normedAlgebra (P : SiteProfile) : NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

local instance inst_UnitaryStateDerivative_scalarTower (P : SiteProfile) : IsScalarTower ℚ ℂ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  IsScalarTower.restrictScalars ℚ ℂ _

def omegaContinuous (P : SiteProfile) :
    (TowerHilbert P →L[ℂ] TowerHilbert P) →L[ℂ] ℂ :=
  (innerSL ℂ (hOmega P)).comp (ContinuousLinearMap.apply ℂ (TowerHilbert P) (hOmega P))

theorem omega_continuous_apply (P : SiteProfile)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P) : omegaContinuous P B=omegaState P B := rfl

theorem bounded_phase_star (P : SiteProfile) (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : IsSelfAdjoint A) (s : ℝ) :
    star (boundedPhase P A s)=boundedPhase P A (-s) := by
  simp only [boundedPhase,NormedSpace.star_exp,star_smul,hA.star_eq,star_mul,Complex.star_def,
    Complex.conj_ofReal,Complex.conj_I,Complex.ofReal_neg,neg_mul]
  congr 1
  congr 1
  ring

theorem bounded_phase_mem_factor (P : SiteProfile) (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A∈theFactorObject P) (s : ℝ) :
    boundedPhase P A s∈theFactorObject P := by
  apply NormedSpace.exp_mem (R := ℂ) (s := (theFactorObject P).toStarSubalgebra)
    (factor_norm_closed P)
  exact (theFactorObject P).toStarSubalgebra.smul_mem hA _

def unitaryConjugation (P : SiteProfile) (A B : TowerHilbert P →L[ℂ] TowerHilbert P) (s : ℝ) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  star (boundedPhase P A s)*B*boundedPhase P A s

theorem unitary_conjugation_derivative_zero (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : IsSelfAdjoint A) :
    HasDerivAt (unitaryConjugation P A B) (Complex.I • (B*A-A*B)) 0 := by
  have hp := bounded_phase_derivative_zero P A
  have hn : HasDerivAt (fun s : ℝ => boundedPhase P A (-s)) (-(Complex.I • A)) 0 := by
    have hf : boundedPhase P (-A)=(fun s : ℝ => boundedPhase P A (-s)) := by
      funext s
      simp only [boundedPhase,Complex.ofReal_neg,neg_mul,neg_smul,smul_neg]
    simpa only [hf,smul_neg] using bounded_phase_derivative_zero P (-A)
  have hh := (hn.mul_const B).mul hp
  have hf : (fun s : ℝ => boundedPhase P A (-s)*B*boundedPhase P A s)=unitaryConjugation P A B := by
    funext s
    simp only [unitaryConjugation,bounded_phase_star P A hA]
  change HasDerivAt (fun s : ℝ => boundedPhase P A (-s)*B*boundedPhase P A s) _ 0 at hh
  rw [hf] at hh
  simpa only [neg_zero,bounded_phase_zero,one_mul,mul_one,neg_mul,smul_mul_assoc,mul_smul_comm,
    smul_sub,sub_eq_add_neg,smul_add,smul_neg,add_comm] using hh

theorem unitary_expectation_derivative_zero (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : IsSelfAdjoint A) :
    HasDerivAt (fun s : ℝ => omegaState P (unitaryConjugation P A B s))
      (Complex.I*omegaState P (B*A-A*B)) 0 := by
  have h := (omegaContinuous P).restrictScalars ℝ |>.hasFDerivAt.comp_hasDerivAt
    0 (unitary_conjugation_derivative_zero P A B hA)
  simpa only [ContinuousLinearMap.coe_comp,ContinuousLinearMap.coe_restrictScalars',
    Function.comp_def,omega_continuous_apply,omega_state_smul] using h

def operatorOrbit (P : SiteProfile) (A C : TowerHilbert P →L[ℂ] TowerHilbert P) (s t : ℝ) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  boundedPhase P A s*boundedPhase P C t

def orbitExpectation (P : SiteProfile) (A C B : TowerHilbert P →L[ℂ] TowerHilbert P) (s t : ℝ) : ℂ :=
  omegaState P (star (operatorOrbit P A C s t)*B*operatorOrbit P A C s t)

theorem orbit_unitary (P : SiteProfile) (A C : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : IsSelfAdjoint A) (hC : IsSelfAdjoint C) (s t : ℝ) :
    operatorOrbit P A C s t∈unitary _ :=
  mul_mem (bounded_phase_unitary P A hA s) (bounded_phase_unitary P C hC t)

theorem orbit_mem_factor (P : SiteProfile) (A C : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A∈theFactorObject P) (hC : C∈theFactorObject P) (s t : ℝ) :
    operatorOrbit P A C s t∈theFactorObject P :=
  (theFactorObject P).mul_mem (bounded_phase_mem_factor P A hA s) (bounded_phase_mem_factor P C hC t)

theorem orbit_origin (P : SiteProfile) (A C : TowerHilbert P →L[ℂ] TowerHilbert P) :
    operatorOrbit P A C 0 0=1 := by simp [operatorOrbit,bounded_phase_zero]

theorem orbit_expectation_origin (P : SiteProfile)
    (A C B : TowerHilbert P →L[ℂ] TowerHilbert P) :
    orbitExpectation P A C B 0 0=omegaState P B := by
  simp [orbitExpectation,orbit_origin]

theorem orbit_expectation_first_derivative (P : SiteProfile)
    (A C B : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : IsSelfAdjoint A) :
    HasDerivAt (fun s : ℝ => orbitExpectation P A C B s 0)
      (Complex.I*omegaState P (B*A-A*B)) 0 := by
  simpa only [orbitExpectation,operatorOrbit,bounded_phase_zero,mul_one,unitaryConjugation] using
    unitary_expectation_derivative_zero P A B hA

theorem orbit_expectation_second_derivative (P : SiteProfile)
    (A C B : TowerHilbert P →L[ℂ] TowerHilbert P) (hC : IsSelfAdjoint C) :
    HasDerivAt (fun t : ℝ => orbitExpectation P A C B 0 t)
      (Complex.I*omegaState P (B*C-C*B)) 0 := by
  simpa only [orbitExpectation,operatorOrbit,bounded_phase_zero,one_mul,unitaryConjugation] using
    unitary_expectation_derivative_zero P C B hC

theorem orbit_vector_state (P : SiteProfile)
    (A C B : TowerHilbert P →L[ℂ] TowerHilbert P) (s t : ℝ) :
    orbitExpectation P A C B s t=
      inner ℂ (operatorOrbit P A C s t (hOmega P)) (B (operatorOrbit P A C s t (hOmega P))) := by
  rw [orbitExpectation,mul_assoc,omega_product_inner,star_star]
  rfl

theorem orbit_vector_norm (P : SiteProfile) (A C : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : IsSelfAdjoint A) (hC : IsSelfAdjoint C) (s t : ℝ) :
    ‖operatorOrbit P A C s t (hOmega P)‖=1 := by
  rw [ContinuousLinearMap.norm_map_of_mem_unitary (orbit_unitary P A C hA hC s t)]
  exact hOmega_norm

theorem orbit_expectation_one (P : SiteProfile) (A C : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : IsSelfAdjoint A) (hC : IsSelfAdjoint C) (s t : ℝ) :
    orbitExpectation P A C 1 s t=1 := by
  rw [orbit_vector_state]
  simp only [one_apply_eq_self,inner_self_eq_norm_sq_to_K,orbit_vector_norm P A C hA hC]
  norm_num

theorem orbit_expectation_nonnegative (P : SiteProfile)
    (A C B : TowerHilbert P →L[ℂ] TowerHilbert P) (hB : B.IsPositive) (s t : ℝ) :
    0≤(orbitExpectation P A C B s t).re := by
  rw [orbit_vector_state]
  exact hB.re_inner_nonneg_right _

theorem orbit_expectation_add (P : SiteProfile)
    (A C B D : TowerHilbert P →L[ℂ] TowerHilbert P) (s t : ℝ) :
    orbitExpectation P A C (B+D) s t=orbitExpectation P A C B s t+orbitExpectation P A C D s t := by
  simp only [orbit_vector_state,_root_.add_apply,inner_add_right]

theorem orbit_expectation_smul (P : SiteProfile)
    (A C B : TowerHilbert P →L[ℂ] TowerHilbert P) (z : ℂ) (s t : ℝ) :
    orbitExpectation P A C (z • B) s t=z*orbitExpectation P A C B s t := by
  simp only [orbit_vector_state,_root_.smul_apply,inner_smul_right]

theorem orbit_expectation_sum (P : SiteProfile)
    (A C : TowerHilbert P →L[ℂ] TowerHilbert P) {ι : Type} [Fintype ι]
    (B : ι → TowerHilbert P →L[ℂ] TowerHilbert P) (s t : ℝ) :
    orbitExpectation P A C (∑ i, B i) s t=∑ i, orbitExpectation P A C (B i) s t := by
  simp only [orbit_vector_state,_root_.sum_apply,inner_sum]

#print axioms omegaContinuous
#print axioms omega_continuous_apply
#print axioms bounded_phase_star
#print axioms bounded_phase_mem_factor
#print axioms unitaryConjugation
#print axioms unitary_conjugation_derivative_zero
#print axioms unitary_expectation_derivative_zero
#print axioms operatorOrbit
#print axioms orbitExpectation
#print axioms orbit_unitary
#print axioms orbit_mem_factor
#print axioms orbit_origin
#print axioms orbit_expectation_origin
#print axioms orbit_expectation_first_derivative
#print axioms orbit_expectation_second_derivative
#print axioms orbit_vector_state
#print axioms orbit_vector_norm
#print axioms orbit_expectation_one
#print axioms orbit_expectation_nonnegative
#print axioms orbit_expectation_add
#print axioms orbit_expectation_smul
#print axioms orbit_expectation_sum
end
end ChatgptAudit.Observable035
