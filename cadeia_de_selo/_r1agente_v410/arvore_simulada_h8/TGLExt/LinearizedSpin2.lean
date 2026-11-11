import TGLExt.TriadMaster

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O SETOR SPIN-2 FÍSICO (face finita): hélice ±2, sem ghosts, duas polarizações
  [TGLExt — v75, o item 6 do fecho na face que cede hoje]

O veredito do fechamento definitivo lista o que falta para o selo
TGL_QG_PHYSICAL_MODEL_CONSTRUCTED: "m = 0, s = 2, λ = ±2, sem modos de
norma negativa". Esta pedra fecha a FACE FINITA desse setor:

O QUE ESTA PEDRA PROVA [KERNEL]:

* ★ `rotZ_preserves_eta` — a rotação espacial concreta R(θ) é isometria
  de η₄ (R(θ)ᵀ η R(θ) = η): o gerador compacto do v63 exponenciado, em
  números — R(θ) ∈ SO(1,3) e a métrica soldada fica na classe (v66);
* ★★ `helicity_two_rotation` / `helicity_two_rotation_cross` — **A LEI
  DA DUPLA HÉLICE (λ = ±2)**: sob rotação por θ, o par de polarizações
  TT (e₊, e×) gira por 2θ:
  R(θ)ᵀ e₊ R(θ) = cos(2θ)·e₊ − sin(2θ)·e× ;
  R(θ)ᵀ e× R(θ) = sin(2θ)·e₊ + cos(2θ)·e× —
  a ASSINATURA do spin-2 (helicidade ±2) como identidade de matrizes,
  com o ângulo DOBRADO saindo das fórmulas de arco-duplo;
* ★★ `tt_kinetic_positive` / `tt_no_negative_norm` — **SEM GHOSTS (face
  finita)**: a forma cinética do setor físico é POSITIVA-DEFINIDA:
  tr[(a·e₊ + b·e×)ᵀ(a·e₊ + b·e×)] = 2(a² + b²) ≥ 0, com igualdade sse
  a = b = 0 — nenhum modo de norma negativa no setor TT;
* ★ `polarizations_linearly_independent` — **EXATAMENTE DUAS**: e₊ e e×
  são linearmente independentes (o plano físico tem dimensão 2).

HONESTIDADE: esta é a face FINITA/cinemática do item 6 — a lei de hélice,
a positividade e a contagem no setor TT concreto. O que segue ABERTO do
item 6: a AÇÃO linearizada completa (Fierz–Pauli como equação de
Euler–Lagrange do modelo contínuo concreto) e a ausência de ghosts fora
do gauge TT — dependem do contínuo (itens 1–5 do fecho). β jamais
literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix

noncomputable section

/-- a rotação espacial concreta em torno de z (o gerador compacto J₃ do
    v63, exponenciado em forma fechada). -/
def rotZ (θ : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1, 0, 0, 0;
     0, Real.cos θ, -(Real.sin θ), 0;
     0, Real.sin θ, Real.cos θ, 0;
     0, 0, 0, 1]

/-- a polarização "mais" do gráviton (TT): e₊ = x⊗x − y⊗y. -/
def ePlus : Matrix (Fin 4) (Fin 4) ℝ :=
  !![0, 0, 0, 0;
     0, 1, 0, 0;
     0, 0, -1, 0;
     0, 0, 0, 0]

/-- a polarização "cruz" do gráviton (TT): e× = x⊗y + y⊗x. -/
def eCross : Matrix (Fin 4) (Fin 4) ℝ :=
  !![0, 0, 0, 0;
     0, 0, 1, 0;
     0, 1, 0, 0;
     0, 0, 0, 0]

/-- [KERNEL] ★ R(θ) é isometria de η₄: o gerador compacto do v63 em
    números — a rotação preserva a métrica de Minkowski (e a classe
    lorentziana da solda, v66). -/
theorem rotZ_preserves_eta (θ : ℝ) :
    (rotZ θ)ᵀ * eta4 * rotZ θ = eta4 := by
  have h := Real.sin_sq_add_cos_sq θ
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rotZ, eta4, Matrix.mul_apply, Matrix.transpose_apply,
      Fin.sum_univ_four, Matrix.diagonal_apply] <;>
    nlinarith [h]

/-- [KERNEL] ★★ A LEI DA DUPLA HÉLICE (metade "mais"): sob rotação por
    θ, e₊ gira por 2θ — R(θ)ᵀ e₊ R(θ) = cos(2θ)·e₊ − sin(2θ)·e×.
    O ângulo DOBRADO é a assinatura da helicidade ±2 (spin-2). -/
theorem helicity_two_rotation (θ : ℝ) :
    (rotZ θ)ᵀ * ePlus * rotZ θ
      = Real.cos (2 * θ) • ePlus - Real.sin (2 * θ) • eCross := by
  rw [Real.cos_two_mul', Real.sin_two_mul]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rotZ, ePlus, eCross, Matrix.mul_apply, Matrix.transpose_apply,
      Fin.sum_univ_four, Matrix.smul_apply, Matrix.sub_apply] <;>
    ring

/-- [KERNEL] ★★ A LEI DA DUPLA HÉLICE (metade "cruz"):
    R(θ)ᵀ e× R(θ) = sin(2θ)·e₊ + cos(2θ)·e× — o par (e₊, e×) gira por
    2θ: helicidade ±2 completa. -/
theorem helicity_two_rotation_cross (θ : ℝ) :
    (rotZ θ)ᵀ * eCross * rotZ θ
      = Real.sin (2 * θ) • ePlus + Real.cos (2 * θ) • eCross := by
  rw [Real.cos_two_mul', Real.sin_two_mul]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rotZ, ePlus, eCross, Matrix.mul_apply, Matrix.transpose_apply,
      Fin.sum_univ_four, Matrix.smul_apply, Matrix.add_apply] <;>
    ring

/-- [KERNEL] ★★ SEM GHOSTS (face finita): a forma cinética do setor TT é
    2(a² + b²) — POSITIVA. -/
theorem tt_kinetic_positive (a b : ℝ) :
    Matrix.trace ((a • ePlus + b • eCross)ᵀ * (a • ePlus + b • eCross))
      = 2 * (a ^ 2 + b ^ 2) := by
  simp [ePlus, eCross, Matrix.trace, Matrix.mul_apply, Matrix.transpose_apply,
    Fin.sum_univ_four, Matrix.smul_apply, Matrix.add_apply, Matrix.diag]
  ring

/-- [KERNEL] ★ NENHUM MODO DE NORMA NEGATIVA no setor físico: a forma é
    ≥ 0, e anula-se SÓ no zero (a definição de ghost-free na face TT). -/
theorem tt_no_negative_norm (a b : ℝ) :
    0 ≤ Matrix.trace ((a • ePlus + b • eCross)ᵀ * (a • ePlus + b • eCross)) ∧
      (Matrix.trace ((a • ePlus + b • eCross)ᵀ * (a • ePlus + b • eCross)) = 0
        ↔ a = 0 ∧ b = 0) := by
  rw [tt_kinetic_positive]
  constructor
  · positivity
  · constructor
    · intro h
      constructor <;> nlinarith [sq_nonneg a, sq_nonneg b]
    · rintro ⟨rfl, rfl⟩
      ring

/-- [KERNEL] ★ EXATAMENTE DUAS polarizações: e₊ e e× são linearmente
    independentes — o plano físico do gráviton tem dimensão 2. -/
theorem polarizations_linearly_independent :
    ∀ a b : ℝ, a • ePlus + b • eCross = 0 → a = 0 ∧ b = 0 := by
  intro a b h
  have h11 := congrFun (congrFun h 1) 1
  have h12 := congrFun (congrFun h 1) 2
  constructor
  · simpa [ePlus, eCross, Matrix.smul_apply, Matrix.add_apply] using h11
  · simpa [ePlus, eCross, Matrix.smul_apply, Matrix.add_apply] using h12

end

end TGLExt
