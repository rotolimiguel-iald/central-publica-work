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
import TGLExt.TowerDefinite
import TGLExt.ModularFirstLaw
import Mathlib.Analysis.SpecialFunctions.BinaryEntropy

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit
open Matrix TGLExt
noncomputable section
variable {ι κ : Type} [Fintype ι] [Fintype κ]

def entropyAtom (x : ℝ) : ℝ := -(x*Real.log x)
def finiteEntropy (p : ι → ℝ) : ℝ := ∑ i, entropyAtom (p i)
def productWeights (p : ι → ℝ) (q : κ → ℝ) : ι × κ → ℝ := fun x => p x.1*q x.2

def leftMarginal (w : ι × κ → ℝ) : ι → ℝ := fun i => ∑ j, w (i,j)
def rightMarginal (w : ι × κ → ℝ) : κ → ℝ := fun j => ∑ i, w (i,j)
def diagonalMutualInformation (w : ι × κ → ℝ) : ℝ :=
  finiteEntropy (leftMarginal w)+finiteEntropy (rightMarginal w)-finiteEntropy w

def diagonalModularGenerator [DecidableEq ι] (p : ι → ℝ) : Matrix ι ι ℂ :=
  Matrix.diagonal (fun i => ((-Real.log (p i) : ℝ) : ℂ))

theorem entropyAtom_zero : entropyAtom 0=0 := by simp [entropyAtom]
theorem entropyAtom_one : entropyAtom 1=0 := by simp [entropyAtom]

theorem entropyAtom_mul (x y : ℝ) :
    entropyAtom (x*y)=y*entropyAtom x+x*entropyAtom y := by
  by_cases hx : x=0
  · simp [hx,entropyAtom_zero]
  by_cases hy : y=0
  · simp [hy,entropyAtom_zero]
  unfold entropyAtom
  rw [Real.log_mul hx hy]
  ring

theorem finiteEntropy_neg_sum (p : ι → ℝ) :
    finiteEntropy p= -(∑ i, p i*Real.log (p i)) := by
  simp [finiteEntropy,entropyAtom,Finset.sum_neg_distrib]

theorem product_weights_sum (p : ι → ℝ) (q : κ → ℝ)
    (hp : ∑ i, p i=1) (hq : ∑ j, q j=1) :
    ∑ x, productWeights p q x=1 := by
  simp only [productWeights,Fintype.sum_prod_type,← Finset.mul_sum,hq,mul_one,hp]

theorem finiteEntropy_product (p : ι → ℝ) (q : κ → ℝ)
    (hp : ∑ i, p i=1) (hq : ∑ j, q j=1) :
    finiteEntropy (productWeights p q)=finiteEntropy p+finiteEntropy q := by
  simp only [finiteEntropy,productWeights,Fintype.sum_prod_type,entropyAtom_mul,Finset.sum_add_distrib]
  simp only [← Finset.sum_mul,← Finset.mul_sum,hp,hq,one_mul]

omit [Fintype ι] in
theorem product_left_marginal (p : ι → ℝ) (q : κ → ℝ) (hq : ∑ j, q j=1) :
    leftMarginal (productWeights p q)=p := by
  funext i
  simp only [leftMarginal,productWeights,← Finset.mul_sum,hq,mul_one]

omit [Fintype κ] in
theorem product_right_marginal (p : ι → ℝ) (q : κ → ℝ) (hp : ∑ i, p i=1) :
    rightMarginal (productWeights p q)=q := by
  funext j
  simp only [rightMarginal,productWeights,← Finset.sum_mul,hp,one_mul]

theorem product_mutual_information_zero (p : ι → ℝ) (q : κ → ℝ)
    (hp : ∑ i, p i=1) (hq : ∑ j, q j=1) :
    diagonalMutualInformation (productWeights p q)=0 := by
  rw [diagonalMutualInformation,product_left_marginal p q hq,product_right_marginal p q hp,
    finiteEntropy_product p q hp hq]
  ring

theorem site_entropy_binary (p : ℝ) :
    finiteEntropy (siteW p)=Real.binEntropy p := by
  rw [Real.binEntropy_eq_negMulLog_add_negMulLog_one_sub]
  norm_num [finiteEntropy,siteW,Fin.sum_univ_two,entropyAtom,Real.negMulLog]
  ring

theorem entropy_diagonal_modular_expectation [DecidableEq ι] (p : ι → ℝ) :
    (finiteEntropy p : ℂ)=∑ i, (p i : ℂ)*diagonalModularGenerator p i i := by
  simp only [finiteEntropy,Complex.ofReal_sum,diagonalModularGenerator,Matrix.diagonal_apply_eq]
  apply Finset.sum_congr rfl
  intro i _
  unfold entropyAtom
  push_cast
  ring

theorem finite_entropy_first_law (p q : ι → ℝ) (hp : ∀ i, 0<p i) (hq : ∑ i, q i=0) :
    HasDerivAt (fun e : ℝ => finiteEntropy (fun i => p i+e*q i))
      (∑ i, q i*(-Real.log (p i))) 0 := by
  classical
  simpa only [finiteEntropy_neg_sum] using first_law_diagonal p q hp hq

#print axioms entropyAtom_zero
#print axioms entropyAtom_one
#print axioms entropyAtom_mul
#print axioms finiteEntropy_neg_sum
#print axioms product_weights_sum
#print axioms finiteEntropy_product
#print axioms product_left_marginal
#print axioms product_right_marginal
#print axioms product_mutual_information_zero
#print axioms site_entropy_binary
#print axioms entropy_diagonal_modular_expectation
#print axioms finite_entropy_first_law
end
end ChatgptAudit
