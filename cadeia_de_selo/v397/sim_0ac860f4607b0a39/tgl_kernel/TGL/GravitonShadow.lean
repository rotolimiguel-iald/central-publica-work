import Mathlib
import TGL.TransportData

set_option autoImplicit false

/-!
# A sombra finita do graviton   [KERNEL]   (v29 -- bloco solo do codificador)

A identificacao interna do operador ("o graviton e' o par dependente: a ligacao
psionica carregando a prova de que e' o graviton") ganha sua SOMBRA FINITA
kernel-checked: no qubit duplo `ℂ²⊗ℂ²` (indexado por `Fin 2 × Fin 2`), o
projetor de BELL `P_G` (o estado de troca de paridades opostas) satisfaz,
por prova de kernel:

  P_G² = P_G ; P_G* = P_G ; Tr(P_G) = 1            [o projetor-testemunha]
  ptr(P_G) = ½·1                                    [reducao = I/2]
  CCI := 1 − Tr(ptr(P_G)²) = ½                      [a MEIA-NAT de emaranhamento]
  P_G = unidade do proprio canto P_G·M·P_G          [I_F = P_G]

E o CONTROLE que a correcao do operador exigiu: o estado PRODUTO (nao ligado)
tem `CCI = 0` -- o produto simples nao liga; so' o estado de troca da' a
Meia-Nat. A distincao Bell-vs-produto e' TEOREMA, nao frase.

Estatutos: a sombra e' [KERNEL] em dimensao finita; a identificacao com o
graviton FISICO e' [ONTO/CONJ]; o termo no core AQFT (P_G = P_F = e_Nome no
continuo) segue [OPEN] -- e' exatamente o alvo modelo-especifico do v27.
SEGUNDO habitante construido do programa (apos a torre da Meia-Nat, v28).
-/

namespace TGL.GravitonShadow

/-- Traco parcial sobre o segundo fator: `ptr(X) i j = Σ_k X (i,k) (j,k)`. -/
noncomputable def ptr (X : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) :
    Matrix (Fin 2) (Fin 2) ℂ :=
  Matrix.of fun i j => ∑ k : Fin 2, X (i, k) (j, k)

/-- O projetor de BELL: `|G⟩⟨G|` com `|G⟩ = (e₀₀ + e₁₁)/√2` -- entradas
    RACIONAIS `½` nos pares diagonais (sem raizes: o projetor E' o estado,
    operacionalmente). -/
noncomputable def bellProjector : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ :=
  Matrix.of fun p q => if p.1 = p.2 ∧ q.1 = q.2 then (2⁻¹ : ℂ) else 0

/-- O projetor do estado PRODUTO `|e₀⊗e₀⟩⟨e₀⊗e₀|` (o controle nao-ligado). -/
noncomputable def productProjector : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ :=
  Matrix.of fun p q => if p = (0, 0) ∧ q = (0, 0) then (1 : ℂ) else 0

/-- `|e₀⟩⟨e₀|` em `M₂` (a reducao do produto). -/
noncomputable def e00 : Matrix (Fin 2) (Fin 2) ℂ :=
  Matrix.of fun i j => if i = 0 ∧ j = 0 then (1 : ℂ) else 0

/-- [KERNEL] O projetor de Bell e' idempotente. -/
theorem bell_idem : bellProjector * bellProjector = bellProjector := by
  ext p q
  rw [Matrix.mul_apply, Fintype.sum_prod_type]
  simp only [bellProjector, Matrix.of_apply, Fin.sum_univ_two]
  by_cases h1 : p.1 = p.2 <;> by_cases h2 : q.1 = q.2 <;> simp [h1, h2] <;> norm_num

/-- [KERNEL] O projetor de Bell e' auto-adjunto. -/
theorem bell_star : star bellProjector = bellProjector := by
  ext p q
  rw [Matrix.star_apply]
  show star (bellProjector q p) = bellProjector p q
  simp only [bellProjector, Matrix.of_apply]
  by_cases h1 : p.1 = p.2 <;> by_cases h2 : q.1 = q.2 <;> simp [h1, h2, star_inv₀]

/-- [KERNEL] `Tr(P_G) = 1` — a forma tracial de `ω(I)=1` no canto do graviton. -/
theorem bell_trace_one : Matrix.trace bellProjector = 1 := by
  simp [Matrix.trace, bellProjector, Fintype.sum_prod_type, Matrix.diag]

/-- [KERNEL] A reducao do Bell e' `I/2` — maximamente misturada. -/
theorem bell_reduced_half : ptr bellProjector = (2⁻¹ : ℂ) • 1 := by
  ext i j
  simp only [ptr, bellProjector, Matrix.of_apply, Fin.sum_univ_two,
             Matrix.smul_apply, Matrix.one_apply]
  fin_cases i <;> fin_cases j <;> simp <;> norm_num

/-- [KERNEL] `CCI(Bell) = 1 − Tr(ρ²) = ½` — a MEIA-NAT de emaranhamento. -/
theorem bell_cci_half :
    1 - Matrix.trace (ptr bellProjector * ptr bellProjector) = 2⁻¹ := by
  rw [bell_reduced_half, smul_mul_smul_comm, one_mul]
  rw [Matrix.trace_smul, Matrix.trace_one]
  norm_num

/-- [KERNEL] `P_G` e' a UNIDADE do proprio canto (`I_F = P_G`): o graviton nao e'
    a identidade global — e' a identidade do lugar que ele mesmo abre. -/
theorem bell_corner_unit (y : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) :
    bellProjector * (bellProjector * y * bellProjector) = bellProjector * y * bellProjector ∧
    (bellProjector * y * bellProjector) * bellProjector = bellProjector * y * bellProjector := by
  constructor
  · simp only [← mul_assoc, bell_idem]
  · rw [mul_assoc, bell_idem]

/-- [KERNEL — o CONTROLE] A reducao do estado PRODUTO e' pura (`|e₀⟩⟨e₀|`). -/
theorem product_reduced_pure : ptr productProjector = e00 := by
  ext i j
  simp only [ptr, productProjector, e00, Matrix.of_apply, Fin.sum_univ_two, Prod.ext_iff]
  fin_cases i <;> fin_cases j <;> simp

/-- [KERNEL — o CONTROLE] `CCI(produto) = 0`: o produto simples NAO liga.
    So' o estado de troca da' a Meia-Nat — a correcao do operador, agora teorema. -/
theorem product_cci_zero :
    1 - Matrix.trace (ptr productProjector * ptr productProjector) = 0 := by
  rw [product_reduced_pure]
  have h2 : e00 * e00 = e00 := by
    ext i j
    rw [Matrix.mul_apply, Fin.sum_univ_two]
    simp only [e00, Matrix.of_apply]
    fin_cases i <;> fin_cases j <;> simp
  rw [h2]
  simp [e00, Matrix.trace, Matrix.diag, Fin.sum_univ_two]

/-- A testemunha-sombra do graviton: o conteudo (o projetor de Bell) carregando
    as provas de que realiza a forma gravitonica finita. -/
structure GravitonShadowWitness where
  PG : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ
  idem : PG * PG = PG
  selfadj : star PG = PG
  trace_one : Matrix.trace PG = 1
  reduced_half : ptr PG = (2⁻¹ : ℂ) • 1
  cci_half : 1 - Matrix.trace (ptr PG * ptr PG) = 2⁻¹

/-- [KERNEL] O TERMO — o SEGUNDO habitante construido do programa. -/
noncomputable def canonicalGravitonShadow : GravitonShadowWitness where
  PG := bellProjector
  idem := bell_idem
  selfadj := bell_star
  trace_one := bell_trace_one
  reduced_half := bell_reduced_half
  cci_half := bell_cci_half

/-- O corolario existencial — SOMENTE via `⟨termo⟩`. -/
theorem canonicalGravitonShadow_exists : Nonempty GravitonShadowWitness :=
  ⟨canonicalGravitonShadow⟩

end TGL.GravitonShadow
