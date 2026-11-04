-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_022 (05-06/09/2026), transposta em 06/09/2026
-- Lote 007..023: habitante GLOBAL periodico da esperanca do centralizador; cauda nao ciclica;
--   obstrucoes de Borchers e da assinatura; e a camada GEOMETRICA GERAL em carta: tensores,
--   conexao de Levi-Civita, curvatura, Bianchi, Einstein geometrico + conservacao, Raychaudhuri,
--   Clausius local <=> balanco nulo de Ricci, telas/congruencias nulas construidas, area e calor,
--   entropia relativa, dinamica unitaria, covetor de materia. Estatuto [REAL / INPUT / OPEN]:
--   Clausius, a metrica lorentziana, H3 dinamico, assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100% nas 17 entregas; 17/17
--   auditores da bancada exit 0; recompilacao INDEPENDENTE 116/116 exit 0, todos os axiomas no
--   trio [propext, Classical.choice, Quot.sound]; zero sorry/warning; enunciados lidos.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports; nada mais.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.TwoLevelSchrodinger

set_option autoImplicit false
set_option maxHeartbeats 8500000
namespace ChatgptAudit.Unitary022
open Matrix Filter Topology Set
open scoped ComplexOrder
noncomputable section

def baseWeights (u v : ℝ) : Fin 2 → ℝ := ![u^2,v^2]
def transferCoefficient (a b u v : ℝ) : ℝ := (a*u+b*v)^2-u^2
def pairWeights (a b frequency u v t : ℝ) : Fin 2 → ℝ :=
  ![u^2+transferCoefficient a b u v*Real.sin (frequency*t)^2,
    v^2-transferCoefficient a b u v*Real.sin (frequency*t)^2]

theorem cartesian_amplitude_square (x y : ℝ) :
    ((x:ℂ)-Complex.I*(y:ℂ))*star ((x:ℂ)-Complex.I*(y:ℂ))=(x^2+y^2:ℝ) := by
  simp only [Complex.star_def,map_sub,map_mul,Complex.conj_ofReal,Complex.conj_I,
    Complex.ofReal_add,Complex.ofReal_pow]
  linear_combination -(y:ℂ)^2*Complex.I_sq

theorem first_weight_square (a b frequency u v t : ℝ) :
    (u*Real.cos (frequency*t))^2+((a*u+b*v)*Real.sin (frequency*t))^2=
      pairWeights a b frequency u v t 0 := by
  simp only [pairWeights,Matrix.cons_val_zero,transferCoefficient]
  linear_combination u^2*(Real.sin_sq_add_cos_sq (frequency*t))

theorem second_weight_square (a b frequency u v t : ℝ) (h : a^2+b^2=1) :
    (v*Real.cos (frequency*t))^2+((b*u-a*v)*Real.sin (frequency*t))^2=
      pairWeights a b frequency u v t 1 := by
  simp only [pairWeights,Matrix.cons_val_one,Matrix.cons_val_zero,transferCoefficient]
  linear_combination (u^2+v^2)*Real.sin (frequency*t)^2*h+
    v^2*(Real.sin_sq_add_cos_sq (frequency*t))

theorem pair_amplitude_weights (a b frequency u v t : ℝ) (h : a^2+b^2=1) (i : Fin 2) :
    evolvedPair a b frequency u v t i*star (evolvedPair a b frequency u v t i)=
      (pairWeights a b frequency u v t i:ℂ) := by
  fin_cases i
  · change evolvedPair a b frequency u v t 0*star (evolvedPair a b frequency u v t 0)=
      (pairWeights a b frequency u v t 0:ℂ)
    rw [evolved_pair_first]
    have hh := cartesian_amplitude_square (u*Real.cos (frequency*t)) ((a*u+b*v)*Real.sin (frequency*t))
    rw [first_weight_square] at hh
    simpa only [Complex.ofReal_mul,Complex.ofReal_add] using hh
  · change evolvedPair a b frequency u v t 1*star (evolvedPair a b frequency u v t 1)=
      (pairWeights a b frequency u v t 1:ℂ)
    rw [evolved_pair_second]
    have hh := cartesian_amplitude_square (v*Real.cos (frequency*t)) ((b*u-a*v)*Real.sin (frequency*t))
    rw [second_weight_square a b frequency u v t h] at hh
    simpa only [Complex.ofReal_mul,Complex.ofReal_sub] using hh

theorem pair_weights_nonnegative (a b frequency u v t : ℝ) (h : a^2+b^2=1) :
    ∀ i, 0≤pairWeights a b frequency u v t i := by
  intro i
  fin_cases i
  · change 0≤pairWeights a b frequency u v t 0
    rw [←first_weight_square]
    positivity
  · change 0≤pairWeights a b frequency u v t 1
    rw [←second_weight_square a b frequency u v t h]
    positivity

theorem pair_weights_normalized (a b frequency u v t : ℝ) (hs : u^2+v^2=1) :
    ∑ i, pairWeights a b frequency u v t i=1 := by
  simp only [Fin.sum_univ_two,pairWeights,Matrix.cons_val_zero,Matrix.cons_val_one]
  linear_combination hs

def correlatedAmplitude (z : Fin 2 → ℂ) : Fin 2 × Fin 2 → ℂ :=
  fun x => if x.1=x.2 then z x.1 else 0
def correlatedDensity (z : Fin 2 → ℂ) : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ :=
  Matrix.vecMulVec (correlatedAmplitude z) (star (correlatedAmplitude z))

def correlatedExtension (A : PairMatrix) : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ :=
  fun x y => if x.1=x.2 then (if y.1=y.2 then A x.1 y.1 else 0)
    else if x=y then 1 else 0

theorem correlated_extension_one : correlatedExtension 1=1 := by
  ext ⟨i,j⟩ ⟨k,l⟩
  fin_cases i <;> fin_cases j <;> fin_cases k <;> fin_cases l <;>
    simp [correlatedExtension]

theorem correlated_extension_product (A B : PairMatrix) :
    correlatedExtension A*correlatedExtension B=correlatedExtension (A*B) := by
  ext ⟨i,j⟩ ⟨k,l⟩
  fin_cases i <;> fin_cases j <;> fin_cases k <;> fin_cases l <;>
    simp [correlatedExtension,Matrix.mul_apply,Fintype.sum_prod_type,Fin.sum_univ_two]

theorem correlated_extension_adjoint (A : PairMatrix) :
    (correlatedExtension A)ᴴ=correlatedExtension Aᴴ := by
  ext ⟨i,j⟩ ⟨k,l⟩
  fin_cases i <;> fin_cases j <;> fin_cases k <;> fin_cases l <;>
    simp [correlatedExtension,Matrix.conjTranspose_apply]

theorem correlated_flow_unitary (a b frequency t : ℝ) (h : a^2+b^2=1) :
    (correlatedExtension (pairFlow a b frequency t))ᴴ*
      correlatedExtension (pairFlow a b frequency t)=1 ∧
    correlatedExtension (pairFlow a b frequency t)*
      (correlatedExtension (pairFlow a b frequency t))ᴴ=1 := by
  constructor
  · rw [correlated_extension_adjoint,correlated_extension_product,
      pair_flow_adjoint_mul a b frequency t h,correlated_extension_one]
  · rw [correlated_extension_adjoint,correlated_extension_product,
      pair_flow_mul_adjoint a b frequency t h,correlated_extension_one]

theorem correlated_extension_action (A : PairMatrix) (z : Fin 2 → ℂ) :
    correlatedExtension A *ᵥ correlatedAmplitude z=correlatedAmplitude (A *ᵥ z) := by
  ext ⟨i,j⟩
  fin_cases i <;> fin_cases j <;>
    simp [correlatedExtension,correlatedAmplitude,Matrix.mulVec,dotProduct,
      Fintype.sum_prod_type,Fin.sum_univ_two]

theorem correlated_state_is_evolved (a b frequency u v t : ℝ) :
    correlatedAmplitude (evolvedPair a b frequency u v t)=
      correlatedExtension (pairFlow a b frequency t) *ᵥ correlatedAmplitude (initialPair u v) := by
  rw [correlated_extension_action]
  rfl

theorem correlated_density_positive (z : Fin 2 → ℂ) : (correlatedDensity z).PosSemidef :=
  Matrix.posSemidef_vecMulVec_self_star _

theorem correlated_amplitude_normalized (z : Fin 2 → ℂ) (r : Fin 2 → ℝ)
    (hz : ∀ i, z i*star (z i)=(r i:ℂ)) (hs : ∑ i, r i=1) :
    ∑ x, correlatedAmplitude z x*star (correlatedAmplitude z x)=1 := by
  rw [Fintype.sum_prod_type]
  have he : ∀ i j, correlatedAmplitude z (i,j)*star (correlatedAmplitude z (i,j))=
      if i=j then (r i:ℂ) else 0 := by
    intro i j
    by_cases h : i=j
    · subst j
      simpa only [correlatedAmplitude,ite_true] using hz i
    · simp [correlatedAmplitude,h]
  simp only [he]
  simpa [eq_comm,←Complex.ofReal_sum] using congrArg (fun x : ℝ => (x:ℂ)) hs

theorem correlated_density_trace (z : Fin 2 → ℂ) (r : Fin 2 → ℝ)
    (hz : ∀ i, z i*star (z i)=(r i:ℂ)) (hs : ∑ i, r i=1) :
    Matrix.trace (correlatedDensity z)=1 := by
  exact correlated_amplitude_normalized z r hz hs

theorem correlated_density_idempotent (z : Fin 2 → ℂ) (r : Fin 2 → ℝ)
    (hz : ∀ i, z i*star (z i)=(r i:ℂ)) (hs : ∑ i, r i=1) :
    correlatedDensity z*correlatedDensity z=correlatedDensity z := by
  ext x y
  change (∑ k, (correlatedAmplitude z x*star (correlatedAmplitude z k))*
    (correlatedAmplitude z k*star (correlatedAmplitude z y)))=
      correlatedAmplitude z x*star (correlatedAmplitude z y)
  calc
    _=correlatedAmplitude z x*(∑ k, correlatedAmplitude z k*star (correlatedAmplitude z k))*
        star (correlatedAmplitude z y) := by
      simp only [Finset.mul_sum,Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro k _
      ring
    _=_ := by rw [correlated_amplitude_normalized z r hz hs]; ring

theorem correlated_right_reduction (z : Fin 2 → ℂ) (r : Fin 2 → ℝ)
    (hz : ∀ i, z i*star (z i)=(r i:ℂ)) :
    partialTraceRight (correlatedDensity z)=Matrix.diagonal (fun i => (r i:ℂ)) := by
  ext i k
  fin_cases i <;> fin_cases k <;>
    simp [partialTraceRight,correlatedDensity,correlatedAmplitude,Matrix.vecMulVec] <;>
      first | exact hz 0 | exact hz 1

theorem evolved_state_valid (a b frequency u v t : ℝ) (h : a^2+b^2=1) (hs : u^2+v^2=1) :
    let z := evolvedPair a b frequency u v t
    let r := pairWeights a b frequency u v t
    (correlatedDensity z).PosSemidef ∧ Matrix.trace (correlatedDensity z)=1 ∧
    correlatedDensity z*correlatedDensity z=correlatedDensity z ∧
    partialTraceRight (correlatedDensity z)=Matrix.diagonal (fun i => (r i:ℂ)) := by
  dsimp only
  exact ⟨correlated_density_positive _,correlated_density_trace _ _
    (pair_amplitude_weights a b frequency u v t h) (pair_weights_normalized a b frequency u v t hs),
    correlated_density_idempotent _ _ (pair_amplitude_weights a b frequency u v t h)
      (pair_weights_normalized a b frequency u v t hs),
    correlated_right_reduction _ _ (pair_amplitude_weights a b frequency u v t h)⟩

#print axioms cartesian_amplitude_square
#print axioms first_weight_square
#print axioms second_weight_square
#print axioms pair_amplitude_weights
#print axioms pair_weights_nonnegative
#print axioms pair_weights_normalized
#print axioms correlated_extension_one
#print axioms correlated_extension_product
#print axioms correlated_extension_adjoint
#print axioms correlated_flow_unitary
#print axioms correlated_extension_action
#print axioms correlated_state_is_evolved
#print axioms correlated_density_positive
#print axioms correlated_amplitude_normalized
#print axioms correlated_density_trace
#print axioms correlated_density_idempotent
#print axioms correlated_right_reduction
#print axioms evolved_state_valid
end
end ChatgptAudit.Unitary022
