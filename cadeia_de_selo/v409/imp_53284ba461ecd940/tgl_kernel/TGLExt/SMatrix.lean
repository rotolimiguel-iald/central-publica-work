import TGLExt.MarkovTower

set_option autoImplicit false

/-!
# A matriz-S da fronteira: 𝒮_∂ = exp(θ·G)   [TGLExt — Teorema S-∂]

O FECHAMENTO DA MATRIZ-S da casa, no kernel, com ângulo θ GENÉRICO:

* (S0) o gerador `G = !![0,1;-1,0]`: `G² = −1` e `Gᴴ = −G` — a estrutura
  complexa real antissimétrica do canal de dois modos;
* (S1) `exp(θ·G) = S(θ) = cos θ·1 + sin θ·G` — a exponencial do gerador
  FECHA na forma cos/sin (diagonalização explícita + fórmula de Euler);
* (S2) unitariedade: `S(θ)ᴴ·S(θ) = 1 = S(θ)·S(θ)ᴴ`;
* (S3) lei de grupo: `S(a)·S(b) = S(a+b)`;
* (S4) espectro EXPLÍCITO: `S(θ) = U·diag(e^{iθ}, e^{−iθ})·U⁻¹` com
  `U = !![1,1;i,−i]` — Spec 𝒮_∂ = {e^{±iθ}} em forma construtiva
  (autovetores explícitos), sem API de spectrum;
* (S5) amplitudes de espalhamento: `𝓣 = cos θ`, `𝓡 = −sin θ`,
  `|𝓡|² = sin²θ`, `|𝓣|² = cos²θ`, `|𝓡|² + |𝓣|² = 1` — o TEOREMA S-∂;
* (S6) leitura de densidade (o canto do v10): `ρ_out = S·E₀₀·Sᴴ` com
  `(ρ_out)₁₁ = sin²θ`, `(ρ_out)₀₀ = cos²θ`, `Tr ρ_out = 1` — a matriz-S
  como CANAL: o peso refletido é `sin²θ`.

θ é GENÉRICO e β JAMAIS aparece neste arquivo: a identificação física
`θ_M = arcsin √β`, `|𝓡|² = β = α·√e`, `|𝓣|² = 1−β` é leitura de RUNTIME
(Python, `tgl_paper_unified.py`) — aqui vive só a estrutura provada.
Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix NormedSpace

noncomputable section

/-- [KERNEL] O GERADOR DA ROTAÇÃO DE ESPALHAMENTO: a estrutura complexa
    real antissimétrica `G = !![0,1;-1,0]` — o "i" matricial do canal de
    dois modos da fronteira (propagação ↔ permanência). -/
def Grot : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; -1, 0]

/-- [KERNEL] A MATRIZ-S DA FRONTEIRA em forma fechada:
    `S(θ) = cos θ·1 + sin θ·G`. No runtime da casa θ = θ_M = arcsin √β;
    AQUI θ é genérico — β jamais entra no Lean. -/
def Smat (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  (Real.cos θ : ℂ) • 1 + (Real.sin θ : ℂ) • Grot

/-! ## S0 — o gerador -/

/-- [KERNEL] `G² = −1`: o gerador é uma estrutura complexa (o "i" do canal). -/
theorem Grot_sq : Grot * Grot = -1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Grot, Matrix.mul_apply, Fin.sum_univ_two]

/-- [KERNEL] `Gᴴ = −G`: o gerador é real antissimétrico (anti-hermitiano),
    logo `θ·G` é skew-adjoint — a raiz da unitariedade de `S(θ)`. -/
theorem Grot_conjTranspose : Grotᴴ = -Grot := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Grot, Matrix.conjTranspose_apply]

/-! ## A forma fechada entrada a entrada -/

/-- A matriz-S em notação explícita: `S(θ) = !![cos θ, sin θ; −sin θ, cos θ]`. -/
theorem Smat_eq (θ : ℝ) :
    Smat θ = !![(Real.cos θ : ℂ), (Real.sin θ : ℂ);
                -(Real.sin θ : ℂ), (Real.cos θ : ℂ)] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Smat, Grot]

/-- `S(0) = 1`: ângulo zero, canal transparente. -/
@[simp] theorem Smat_zero : Smat 0 = 1 := by
  simp [Smat]

/-! ## S3 — lei de grupo -/

/-- [KERNEL] LEI DE GRUPO: `S(a)·S(b) = S(a+b)` — as reflexões modulares
    compõem somando o ângulo de mistura. -/
theorem Smat_mul (a b : ℝ) : Smat a * Smat b = Smat (a + b) := by
  rw [Smat_eq a, Smat_eq b, Smat_eq (a + b)]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, Real.cos_add, Real.sin_add] <;>
    ring

/-! ## S2 — unitariedade -/

/-- `S(θ)ᴴ = S(−θ)`: a adjunta é a rotação reversa. -/
theorem Smat_conjTranspose (θ : ℝ) : (Smat θ)ᴴ = Smat (-θ) := by
  unfold Smat
  rw [Matrix.conjTranspose_add, Matrix.conjTranspose_smul, Matrix.conjTranspose_smul,
    Matrix.conjTranspose_one, Grot_conjTranspose, Complex.star_def,
    Complex.conj_ofReal, Complex.conj_ofReal, Real.cos_neg, Real.sin_neg,
    Complex.ofReal_neg, smul_neg, neg_smul]

/-- [KERNEL] UNITARIEDADE: `S(θ)ᴴ·S(θ) = 1` — nenhum peso se perde na
    fronteira. -/
theorem Smat_conjTranspose_mul (θ : ℝ) : (Smat θ)ᴴ * Smat θ = 1 := by
  rw [Smat_conjTranspose, Smat_mul, neg_add_cancel, Smat_zero]

/-- [KERNEL] UNITARIEDADE (outro lado): `S(θ)·S(θ)ᴴ = 1`. -/
theorem Smat_mul_conjTranspose (θ : ℝ) : Smat θ * (Smat θ)ᴴ = 1 := by
  rw [Smat_conjTranspose, Smat_mul, add_neg_cancel, Smat_zero]

/-- [KERNEL] `S(θ)` é UNITÁRIA (membro de `unitary`). -/
theorem Smat_mem_unitary (θ : ℝ) :
    Smat θ ∈ unitary (Matrix (Fin 2) (Fin 2) ℂ) := by
  rw [Unitary.mem_iff]
  constructor <;> rw [Matrix.star_eq_conjTranspose]
  · exact Smat_conjTranspose_mul θ
  · exact Smat_mul_conjTranspose θ

/-! ## S4 — diagonalização explícita: Spec 𝒮_∂ = {e^{iθ}, e^{−iθ}} -/

/-- A matriz de autovetores `U = !![1,1;i,−i]` (colunas = autovetores de G,
    os modos quirais `(1, ±i)` do canal). -/
def Umat : Matrix (Fin 2) (Fin 2) ℂ := !![1, 1; Complex.I, -Complex.I]

/-- A inversa explícita `U⁻¹ = ½·!![1,−i;1,i]`. -/
def Uinv : Matrix (Fin 2) (Fin 2) ℂ := (2⁻¹ : ℂ) • !![1, -Complex.I; 1, Complex.I]

theorem Umat_mul_Uinv : Umat * Uinv = 1 := by
  have h : Umat * !![1, -Complex.I; 1, Complex.I] = (2 : ℂ) • 1 := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [Umat, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply,
        Complex.I_mul_I]
  rw [Uinv, mul_smul_comm, h, smul_smul]
  norm_num

theorem Uinv_mul_Umat : Uinv * Umat = 1 := by
  have h : !![1, -Complex.I; 1, Complex.I] * Umat = (2 : ℂ) • 1 := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [Umat, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply,
        Complex.I_mul_I]
  rw [Uinv, smul_mul_assoc, h, smul_smul]
  norm_num

/-- O gerador diagonalizado: `U·diag(i,−i)·U⁻¹ = G`. -/
theorem Grot_diagonalized :
    Umat * Matrix.diagonal ![Complex.I, -Complex.I] * Uinv = Grot := by
  have h : Umat * Matrix.diagonal ![Complex.I, -Complex.I]
      * !![1, -Complex.I; 1, Complex.I] = (2 : ℂ) • Grot := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [Umat, Grot, Matrix.diagonal_vec2, Matrix.mul_apply,
        Fin.sum_univ_two, Complex.I_mul_I]
  rw [Uinv, mul_smul_comm, h, smul_smul]
  norm_num

/-- `θ·G` diagonalizada: `θ·G = U·diag(iθ,−iθ)·U⁻¹`. -/
theorem smul_Grot_diagonalized (θ : ℝ) :
    (θ : ℂ) • Grot
      = Umat * Matrix.diagonal ![(θ : ℂ) * Complex.I,
          -((θ : ℂ) * Complex.I)] * Uinv := by
  have h : Matrix.diagonal ![(θ : ℂ) * Complex.I, -((θ : ℂ) * Complex.I)]
      = (θ : ℂ) • Matrix.diagonal ![Complex.I, -Complex.I] := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [Matrix.diagonal_vec2]
  rw [h, mul_smul_comm, smul_mul_assoc, Grot_diagonalized]

/-- O núcleo da diagonalização: `U·diag(cos θ + i·sin θ, cos θ − i·sin θ)·U⁻¹
    = S(θ)` — as duas fases de Euler recombinam na forma fechada cos/sin. -/
theorem Umat_diag_mul_Uinv (θ : ℝ) :
    Umat * Matrix.diagonal ![(Real.cos θ : ℂ) + (Real.sin θ : ℂ) * Complex.I,
        (Real.cos θ : ℂ) - (Real.sin θ : ℂ) * Complex.I] * Uinv = Smat θ := by
  have hsplit : Matrix.diagonal ![(Real.cos θ : ℂ) + (Real.sin θ : ℂ) * Complex.I,
      (Real.cos θ : ℂ) - (Real.sin θ : ℂ) * Complex.I]
      = (Real.cos θ : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)
        + (Real.sin θ : ℂ) • Matrix.diagonal ![Complex.I, -Complex.I] := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [Matrix.diagonal_vec2, sub_eq_add_neg]
  rw [hsplit]
  simp only [mul_add, add_mul, mul_smul_comm, smul_mul_assoc, mul_one]
  rw [Umat_mul_Uinv, Grot_diagonalized]
  simp only [Smat]

/-- A fase reversa de Euler: `e^{−iθ} = cos θ − i·sin θ`. -/
theorem exp_neg_ofReal_mul_I (θ : ℝ) :
    Complex.exp (-((θ : ℂ) * Complex.I))
      = (Real.cos θ : ℂ) - (Real.sin θ : ℂ) * Complex.I := by
  have hneg : -((θ : ℂ) * Complex.I) = ((-θ : ℝ) : ℂ) * Complex.I := by
    push_cast
    ring
  rw [hneg, Complex.exp_ofReal_mul_I, Real.cos_neg, Real.sin_neg,
    Complex.ofReal_neg]
  ring

/-! ## S1 — a exponencial do gerador FECHA na matriz-S -/

/-- [KERNEL] TEOREMA S-∂ (forma exponencial): `exp(θ·G) = S(θ)`.
    A exponencial do gerador antissimétrico é EXATAMENTE a matriz-S em
    forma fechada cos/sin — rota: diagonalização explícita
    (`Matrix.exp_conj` + `Matrix.exp_diagonal` + Euler `e^{±iθ}`).
    θ genérico; a leitura θ_M = arcsin √β é do runtime. -/
theorem exp_smul_Grot (θ : ℝ) : exp ((θ : ℂ) • Grot) = Smat θ := by
  have hU : IsUnit Umat := ⟨⟨Umat, Uinv, Umat_mul_Uinv, Uinv_mul_Umat⟩, rfl⟩
  have hUinv : Umat⁻¹ = Uinv := Matrix.inv_eq_right_inv Umat_mul_Uinv
  rw [smul_Grot_diagonalized θ, ← hUinv, Matrix.exp_conj _ _ hU,
    Matrix.exp_diagonal, hUinv, Pi.exp_def, Matrix.diagonal_fin_two]
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
  rw [← Complex.exp_eq_exp_ℂ, Complex.exp_ofReal_mul_I, exp_neg_ofReal_mul_I,
    ← Matrix.diagonal_vec2]
  exact Umat_diag_mul_Uinv θ

/-- [KERNEL] ESPECTRO EXPLÍCITO: `S(θ) = U·diag(e^{iθ}, e^{−iθ})·U⁻¹` —
    Spec 𝒮_∂ = {e^{±iθ}} na forma construtiva (autovetores explícitos
    `(1, ±i)`), sem API de spectrum. -/
theorem Smat_spectral (θ : ℝ) :
    Smat θ = Umat * Matrix.diagonal ![Complex.exp ((θ : ℂ) * Complex.I),
        Complex.exp (-((θ : ℂ) * Complex.I))] * Uinv := by
  rw [Complex.exp_ofReal_mul_I, exp_neg_ofReal_mul_I]
  exact (Umat_diag_mul_Uinv θ).symm

/-! ## S5 — amplitudes de espalhamento: o TEOREMA S-∂ -/

/-- O modo incidente `e₁ = ![1,0]` (o canal que chega à fronteira). -/
def e1 : Fin 2 → ℂ := ![1, 0]

/-- O modo refletido `e₂ = ![0,1]` (o canal de retorno). -/
def e2 : Fin 2 → ℂ := ![0, 1]

/-- [KERNEL] TRANSMISSÃO: `𝓣 = (S(θ)·e₁)₀ = cos θ`. -/
theorem Smat_transmission (θ : ℝ) :
    (Smat θ).mulVec e1 0 = (Real.cos θ : ℂ) := by
  rw [Smat_eq]
  simp [e1, Matrix.mulVec]

/-- [KERNEL] REFLEXÃO: `𝓡 = (S(θ)·e₁)₁ = −sin θ` — a amplitude que volta. -/
theorem Smat_reflection (θ : ℝ) :
    (Smat θ).mulVec e1 1 = -(Real.sin θ : ℂ) := by
  rw [Smat_eq]
  simp [e1, Matrix.mulVec]

/-- [KERNEL] `|𝓡|² = sin²θ` — o peso refletido. NO RUNTIME (e só lá):
    `sin²θ_M = β = α·√e`. Aqui θ é genérico, β não entra. -/
theorem normSq_reflection (θ : ℝ) :
    Complex.normSq ((Smat θ).mulVec e1 1) = Real.sin θ ^ 2 := by
  rw [Smat_reflection, Complex.normSq_neg, Complex.normSq_ofReal]
  ring

/-- [KERNEL] `|𝓣|² = cos²θ` — o peso transmitido (no runtime: `1 − β`). -/
theorem normSq_transmission (θ : ℝ) :
    Complex.normSq ((Smat θ).mulVec e1 0) = Real.cos θ ^ 2 := by
  rw [Smat_transmission, Complex.normSq_ofReal]
  ring

/-- [KERNEL] O TEOREMA S-∂: `|𝓡|² + |𝓣|² = 1` — a unitariedade das
    amplitudes de espalhamento. No runtime da casa: `β + (1−β) = 1`. -/
theorem normSq_reflection_add_transmission (θ : ℝ) :
    Complex.normSq ((Smat θ).mulVec e1 1)
      + Complex.normSq ((Smat θ).mulVec e1 0) = 1 := by
  rw [normSq_reflection, normSq_transmission, Real.sin_sq_add_cos_sq]

/-! ## S6 — a matriz-S como CANAL: leitura de densidade (o canto do v10) -/

/-- O estado de saída `ρ_out = S(θ)·E₀₀·S(θ)ᴴ` — o canal aplicado ao
    estado puro incidente `E₀₀ = |0⟩⟨0|`. -/
def rhoOut (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  Smat θ * Matrix.single 0 0 1 * (Smat θ)ᴴ

/-- A forma fechada do estado de saída. -/
theorem rhoOut_eq (θ : ℝ) :
    rhoOut θ = !![(Real.cos θ : ℂ) ^ 2, -((Real.cos θ : ℂ) * (Real.sin θ : ℂ));
        -((Real.sin θ : ℂ) * (Real.cos θ : ℂ)), (Real.sin θ : ℂ) ^ 2] := by
  have hE : (Matrix.single 0 0 1 : Matrix (Fin 2) (Fin 2) ℂ) = !![1, 0; 0, 0] := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp
  unfold rhoOut
  rw [Smat_conjTranspose, Smat_eq θ, Smat_eq (-θ), hE]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, Real.cos_neg, Real.sin_neg] <;>
    ring

/-- [KERNEL] LEITURA DE DENSIDADE: o peso REFLETIDO é
    `(ρ_out)₁₁ = sin²θ` — a probabilidade de reflexão do canal.
    NO RUNTIME (e só lá): `sin²θ_M = β`. -/
theorem rhoOut_one_one (θ : ℝ) : rhoOut θ 1 1 = (Real.sin θ : ℂ) ^ 2 := by
  rw [rhoOut_eq]
  simp

/-- [KERNEL] O peso TRANSMITIDO: `(ρ_out)₀₀ = cos²θ` (runtime: `1 − β`). -/
theorem rhoOut_zero_zero (θ : ℝ) : rhoOut θ 0 0 = (Real.cos θ : ℂ) ^ 2 := by
  rw [rhoOut_eq]
  simp

/-- [KERNEL] CONSERVAÇÃO: `Tr ρ_out = 1` — o canal preserva o traço:
    o que não transmite, reflete. -/
theorem rhoOut_trace (θ : ℝ) : (rhoOut θ).trace = 1 := by
  rw [Matrix.trace_fin_two, rhoOut_zero_zero, rhoOut_one_one]
  exact_mod_cast Real.cos_sq_add_sin_sq θ

end

end TGLExt
