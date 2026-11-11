-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_011 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.FiniteEntropyAlgebra
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Analysis.Complex.Order

set_option autoImplicit false
set_option maxHeartbeats 2600000
namespace ChatgptAudit
open Matrix
open scoped Kronecker ComplexOrder
noncomputable section
variable {ι : Type} [Fintype ι] [DecidableEq ι]

def schmidtAmplitude (p : ι → ℝ) : ι × ι → ℂ :=
  fun x => if x.1=x.2 then (Real.sqrt (p x.1) : ℂ) else 0

def pureCutDensity (p : ι → ℝ) : Matrix (ι × ι) (ι × ι) ℂ :=
  Matrix.vecMulVec (schmidtAmplitude p) (star (schmidtAmplitude p))

def partialTraceRight (rho : Matrix (ι × ι) (ι × ι) ℂ) : Matrix ι ι ℂ :=
  fun i k => ∑ j, rho (i,j) (k,j)

def partialTraceLeft (rho : Matrix (ι × ι) (ι × ι) ℂ) : Matrix ι ι ℂ :=
  fun j l => ∑ i, rho (i,j) (i,l)

theorem sqrt_weight_product (x : ℝ) (hx : 0≤x) :
    (Real.sqrt x : ℂ)*star (Real.sqrt x : ℂ)=(x:ℂ) := by
  simp only [Complex.star_def,Complex.conj_ofReal,← Complex.ofReal_mul,Real.mul_self_sqrt hx]

omit [Fintype ι] in
theorem schmidt_amplitude_norm (p : ι → ℝ) (hp : ∀ i, 0≤p i) (i j : ι) :
    schmidtAmplitude p (i,j)*star (schmidtAmplitude p (i,j))=
      if i=j then (p i:ℂ) else 0 := by
  by_cases h : i=j
  · subst j
    simpa only [schmidtAmplitude,ite_true] using sqrt_weight_product (p i) (hp i)
  · simp [schmidtAmplitude,h]

theorem schmidt_amplitude_normalized (p : ι → ℝ) (hp : ∀ i, 0≤p i) (hs : ∑ i, p i=1) :
    ∑ x, schmidtAmplitude p x*star (schmidtAmplitude p x)=1 := by
  rw [Fintype.sum_prod_type]
  simp only [schmidt_amplitude_norm p hp]
  simpa [eq_comm,← Complex.ofReal_sum] using congrArg (fun r : ℝ => (r:ℂ)) hs

theorem pure_cut_positive (p : ι → ℝ) : (pureCutDensity p).PosSemidef :=
  Matrix.posSemidef_vecMulVec_self_star _

theorem pure_cut_trace_one (p : ι → ℝ) (hp : ∀ i, 0≤p i) (hs : ∑ i, p i=1) :
    Matrix.trace (pureCutDensity p)=1 := by
  change (∑ x, schmidtAmplitude p x*star (schmidtAmplitude p x))=1
  exact schmidt_amplitude_normalized p hp hs

theorem pure_cut_idempotent (p : ι → ℝ) (hp : ∀ i, 0≤p i) (hs : ∑ i, p i=1) :
    pureCutDensity p*pureCutDensity p=pureCutDensity p := by
  ext a b
  change (∑ c, (schmidtAmplitude p a*star (schmidtAmplitude p c))*
    (schmidtAmplitude p c*star (schmidtAmplitude p b)))=
      schmidtAmplitude p a*star (schmidtAmplitude p b)
  calc
    _=schmidtAmplitude p a*(∑ c, schmidtAmplitude p c*star (schmidtAmplitude p c))*
        star (schmidtAmplitude p b) := by
      simp only [Finset.mul_sum,Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro c _
      ring
    _=_ := by rw [schmidt_amplitude_normalized p hp hs]; ring

theorem pure_cut_right_reduction (p : ι → ℝ) (hp : ∀ i, 0≤p i) :
    partialTraceRight (pureCutDensity p)=Matrix.diagonal (fun i => (p i:ℂ)) := by
  ext i k
  by_cases hik : i=k
  · subst k
    change (∑ j, schmidtAmplitude p (i,j)*star (schmidtAmplitude p (i,j)))=_
    simp only [schmidt_amplitude_norm p hp]
    simp
  · rw [Matrix.diagonal_apply_ne _ hik]
    apply Finset.sum_eq_zero
    intro j _
    change schmidtAmplitude p (i,j)*star (schmidtAmplitude p (k,j))=0
    by_cases hij : i=j
    · subst j
      simp [schmidtAmplitude,Ne.symm hik]
    · simp [schmidtAmplitude,hij]

theorem pure_cut_left_reduction (p : ι → ℝ) (hp : ∀ i, 0≤p i) :
    partialTraceLeft (pureCutDensity p)=Matrix.diagonal (fun i => (p i:ℂ)) := by
  ext j l
  by_cases hjl : j=l
  · subst l
    change (∑ i, schmidtAmplitude p (i,j)*star (schmidtAmplitude p (i,j)))=_
    simp only [schmidt_amplitude_norm p hp]
    simp
  · rw [Matrix.diagonal_apply_ne _ hjl]
    apply Finset.sum_eq_zero
    intro i _
    change schmidtAmplitude p (i,j)*star (schmidtAmplitude p (i,l))=0
    by_cases hij : i=j
    · subst i
      simp [schmidtAmplitude,hjl]
    · simp [schmidtAmplitude,hij]

theorem trace_partial_right (rho : Matrix (ι × ι) (ι × ι) ℂ) (a : Matrix ι ι ℂ) :
    Matrix.trace (rho*(a ⊗ₖ (1:Matrix ι ι ℂ)))=Matrix.trace (partialTraceRight rho*a) := by
  simp only [Matrix.trace,Matrix.diag,Matrix.mul_apply,Fintype.sum_prod_type,
    Matrix.kroneckerMap_apply,Matrix.one_apply,partialTraceRight]
  simp only [mul_ite,mul_one,mul_zero,Finset.sum_ite_eq',Finset.mem_univ,if_true,Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro i _
  exact Finset.sum_comm

theorem pure_cut_left_expectation (p : ι → ℝ) (hp : ∀ i, 0≤p i) (a : Matrix ι ι ℂ) :
    Matrix.trace (pureCutDensity p*(a ⊗ₖ (1:Matrix ι ι ℂ)))=∑ i, (p i:ℂ)*a i i := by
  rw [trace_partial_right,pure_cut_right_reduction p hp]
  simp [Matrix.trace,Matrix.diag,Matrix.diagonal_mul]

omit [Fintype ι] in
theorem pure_cut_off_diagonal_zero (p : ι → ℝ) (i j : ι) (hij : i≠j) :
    pureCutDensity p (i,j) (i,j)=0 := by
  simp [pureCutDensity,Matrix.vecMulVec,schmidtAmplitude,hij]

theorem pure_cut_annihilated_projection (p : ι → ℝ) (i j : ι) (hij : i≠j) :
    (Matrix.single (i,j) (i,j) (1:ℂ) : Matrix (ι × ι) (ι × ι) ℂ)≠0 ∧
    Matrix.trace (pureCutDensity p*Matrix.single (i,j) (i,j) 1)=0 := by
  constructor
  · intro hz
    have he := congrArg (fun A : Matrix (ι × ι) (ι × ι) ℂ => A (i,j) (i,j)) hz
    simp at he
  · rw [Matrix.trace_mul_single,pure_cut_off_diagonal_zero p i j hij]
    simp

#print axioms sqrt_weight_product
#print axioms schmidt_amplitude_norm
#print axioms schmidt_amplitude_normalized
#print axioms pure_cut_positive
#print axioms pure_cut_trace_one
#print axioms pure_cut_idempotent
#print axioms pure_cut_right_reduction
#print axioms pure_cut_left_reduction
#print axioms trace_partial_right
#print axioms pure_cut_left_expectation
#print axioms pure_cut_off_diagonal_zero
#print axioms pure_cut_annihilated_projection
end
end ChatgptAudit
