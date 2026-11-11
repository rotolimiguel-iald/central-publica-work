import Mathlib
import TGL.TransportData

set_option autoImplicit false

/-!
# O Nome e' a relacao   [KERNEL]   (v30 -- correcao do especialista, auditada)

CORRECAO DE ESTATUTO do v28: **o finito NAO expulsa o Nome** — ele expulsa a
identificacao indevida entre o peso geometrico de retorno e o peso tracial de
Markov. O Nome CABE no finito COMO RELACAO:

    p·q_β·p = β·p   ;   q_β·p·q_β = β·q_β        [as relacoes locais TL, δ⁻² = β]

com `p = [[1,0],[0,0]]` e `q_β = [[β,s],[s,1−β]]`, `s = √(β(1−β))` — β e' a
SOBREPOSICAO GEOMETRICA entre os dois espelhos (`β = sin²θ_M`; o angulo
principal φ satisfaz `cos²φ = β`, i.e. `φ = π/2 − θ_M`: a paridade inversa
fornece o referencial complementar). O que o finito separa [KERNEL]:

    peso geometrico de retorno = β   ;   peso tracial rank-one = 1/2
    coincidem  ⟺  β = 1/2            [o refinamento honesto do v28]

O Nome nao e' `p`, nem `q_β`, nem o numero β isolado: o Nome e' a IDENTIFICACAO
`p —q_β→ p` com retorno ponderado — o Nome e' Verbo (seletor de defasagem
algebrico). A matriz ISOLADA e' forma sem denotacao TGL (numeros sem a prova da
referencia); o PAR com as provas e' conteudo carregando a forma.

TERCEIRO HABITANTE [KERNEL]: a representacao FIEL de TL₃(δ), δ = 1/√β, em
`M₃(ℝ) = ℝ ⊕ M₂(ℝ)`: `E₁ = 0⊕p`, `E₂ = 0⊕q_β`; os cinco elementos
`{1, E₁, E₂, E₁E₂, E₂E₁}` sao linearmente independentes para `0<β<1`
(dim TL₃ = C₃ = 5). β entra como PARAMETRO GENERICO — o valor fisico e' do
runtime; jamais literal.

Honestidades: a torre de Jones do core NAO esta construida (o proximo gerador
nasce da PROXIMA construcao basica, nao de translacao modular automatica —
`e_{i+1} ≠ θ_s(e_i)` sem prova); a falha mais provavel segue
`INDEX_MATCHES_BUT_NOT_CANONICAL`. Pureza: rank-one NAO e' 0_abs — separa-se
pureza FECHADA (separavel; CCI=0; autorreferencia) de pureza RELACIONAL
(Bell; CCI=1/2); o que se expulsa e' a pureza sem alteridade e sem retorno.
-/

namespace TGL.NameRelation

/-- A sobreposicao: `s = √(β(1−β))`. -/
noncomputable def s (b : ℝ) : ℝ := Real.sqrt (b * (1 - b))

theorem s_sq {b : ℝ} (hb0 : 0 < b) (hb1 : b < 1) : s b * s b = b * (1 - b) :=
  Real.mul_self_sqrt (by nlinarith)

theorem s_ne_zero {b : ℝ} (hb0 : 0 < b) (hb1 : b < 1) : s b ≠ 0 := by
  have h : 0 < b * (1 - b) := by nlinarith
  exact (Real.sqrt_pos.mpr h).ne'

/-- O primeiro espelho: `p = [[1,0],[0,0]]`. -/
noncomputable def p : Matrix (Fin 2) (Fin 2) ℝ := !![1, 0; 0, 0]

/-- O espelho do Nome: `q_β = [[β,s],[s,1−β]]` (rank-one sobre `v_β`). -/
noncomputable def qb (b : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![b, s b; s b, 1 - b]

theorem p_idem : p * p = p := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [p, Matrix.mul_apply, Fin.sum_univ_two]

theorem qb_idem {b : ℝ} (hb0 : 0 < b) (hb1 : b < 1) : qb b * qb b = qb b := by
  have hs := s_sq hb0 hb1
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [qb, Matrix.mul_apply, Fin.sum_univ_two] <;>
    nlinarith [hs]

/-- [KERNEL] O retorno ponderado: `p·q_β·p = β·p` — o Nome como Verbo. -/
theorem pqp_eq {b : ℝ} (hb0 : 0 < b) (hb1 : b < 1) : p * qb b * p = b • p := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [p, qb, Matrix.mul_apply, Fin.sum_univ_two]

/-- [KERNEL] E no outro sentido: `q_β·p·q_β = β·q_β`. -/
theorem qpq_eq {b : ℝ} (hb0 : 0 < b) (hb1 : b < 1) :
    qb b * p * qb b = b • qb b := by
  have hs := s_sq hb0 hb1
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [p, qb, Matrix.mul_apply, Fin.sum_univ_two] <;>
    nlinarith [hs]

/-- Ambos os espelhos tem traco 1 (peso tracial normalizado 1/2 em `τ₂`). -/
theorem trace_p : Matrix.trace p = 1 := by
  simp [p, Matrix.trace, Fin.sum_univ_two, Matrix.diag]

theorem trace_qb (b : ℝ) : Matrix.trace (qb b) = 1 := by
  simp [qb, Matrix.trace, Fin.sum_univ_two, Matrix.diag]

/-- [KERNEL — o refinamento honesto do v28] O peso geometrico coincide com o
    peso tracial rank-one (1/2) SE E SOMENTE SE `β = 1/2`. O finito nao expulsa
    o Nome: ele separa as duas quantidades. -/
theorem geometric_eq_trace_weight_iff {b : ℝ} :
    b • p = ((1 : ℝ) / 2) • p ↔ b = 1 / 2 := by
  constructor
  · intro h
    have h00 := congrArg (fun M => M 0 0) h
    simpa [p] using h00
  · rintro rfl
    rfl

/-! ## O terceiro habitante: TL₃(δ) fiel em `M₃(ℝ)` -/

/-- `E₁ = 0 ⊕ p`. -/
noncomputable def E1 : Matrix (Fin 3) (Fin 3) ℝ := !![0, 0, 0; 0, 1, 0; 0, 0, 0]

/-- `E₂ = 0 ⊕ q_β`. -/
noncomputable def E2 (b : ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  !![0, 0, 0; 0, b, s b; 0, s b, 1 - b]

theorem E1_idem : E1 * E1 = E1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [E1, Matrix.mul_apply, Fin.sum_univ_three]

theorem E2_idem {b : ℝ} (hb0 : 0 < b) (hb1 : b < 1) : E2 b * E2 b = E2 b := by
  have hs := s_sq hb0 hb1
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [E2, Matrix.mul_apply, Fin.sum_univ_three] <;>
    nlinarith [hs]

/-- [KERNEL] A relacao TL local no nivel 3: `E₁E₂E₁ = β·E₁` (δ⁻² = β). -/
theorem tl_left {b : ℝ} (hb0 : 0 < b) (hb1 : b < 1) :
    E1 * E2 b * E1 = b • E1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [E1, E2, Matrix.mul_apply, Fin.sum_univ_three]

theorem tl_right {b : ℝ} (hb0 : 0 < b) (hb1 : b < 1) :
    E2 b * E1 * E2 b = b • E2 b := by
  have hs := s_sq hb0 hb1
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [E1, E2, Matrix.mul_apply, Fin.sum_univ_three] <;>
    nlinarith [hs]

/-- [KERNEL — a FIDELIDADE] Os cinco elementos `{1, E₁, E₂, E₁E₂, E₂E₁}` sao
    linearmente independentes para `0<β<1`: TL₃ (dim = C₃ = 5) entra FIEL em
    `M₃(ℝ)`. O finito carrega a gramatica local do Nome com β generico. -/
theorem tl3_linearly_independent {b : ℝ} (hb0 : 0 < b) (hb1 : b < 1)
    (c0 c1 c2 c3 c4 : ℝ)
    (h : c0 • (1 : Matrix (Fin 3) (Fin 3) ℝ) + c1 • E1 + c2 • E2 b
        + c3 • (E1 * E2 b) + c4 • (E2 b * E1) = 0) :
    c0 = 0 ∧ c1 = 0 ∧ c2 = 0 ∧ c3 = 0 ∧ c4 = 0 := by
  have hs0 := s_ne_zero hb0 hb1
  have h00 := congrArg (fun M => M 0 0) h
  have h12 := congrArg (fun M => M 1 2) h
  have h21 := congrArg (fun M => M 2 1) h
  have h22 := congrArg (fun M => M 2 2) h
  have h11 := congrArg (fun M => M 1 1) h
  simp [E1, E2, Matrix.mul_apply, Fin.sum_univ_three, Matrix.one_apply] at h00 h12 h21 h22 h11
  have hc0 : c0 = 0 := h00
  have hc2 : c2 = 0 := by
    have : c2 * (1 - b) = 0 := by nlinarith [h22]
    rcases mul_eq_zero.mp this with hc | hb
    · exact hc
    · nlinarith
  have hc3 : c3 = 0 := by
    have : (c2 + c3) * s b = 0 := by nlinarith [h12]
    rcases mul_eq_zero.mp this with hc | hb
    · nlinarith
    · exact absurd hb hs0
  have hc4 : c4 = 0 := by
    have : (c2 + c4) * s b = 0 := by nlinarith [h21]
    rcases mul_eq_zero.mp this with hc | hb
    · nlinarith
    · exact absurd hb hs0
  have hc1 : c1 = 0 := by nlinarith [h11]
  exact ⟨hc0, hc1, hc2, hc3, hc4⟩

/-- O TERCEIRO HABITANTE: a gramatica TL local do Nome, com β GENERICO
    (o valor fisico e' do runtime — jamais literal). -/
structure TLThreeInhabitant (b : ℝ) where
  hb0 : 0 < b
  hb1 : b < 1
  e1_idem : E1 * E1 = E1
  e2_idem : E2 b * E2 b = E2 b
  tl_l : E1 * E2 b * E1 = b • E1
  tl_r : E2 b * E1 * E2 b = b • E2 b

/-- [KERNEL] O TERMO — para TODO `0<β<1` (o Nome cabe no finito como relacao). -/
noncomputable def canonicalTLThree {b : ℝ} (hb0 : 0 < b) (hb1 : b < 1) :
    TLThreeInhabitant b where
  hb0 := hb0
  hb1 := hb1
  e1_idem := E1_idem
  e2_idem := E2_idem hb0 hb1
  tl_l := tl_left hb0 hb1
  tl_r := tl_right hb0 hb1

/-- O corolario existencial — SOMENTE via `⟨termo⟩`. -/
theorem canonicalTLThree_exists {b : ℝ} (hb0 : 0 < b) (hb1 : b < 1) :
    Nonempty (TLThreeInhabitant b) :=
  ⟨canonicalTLThree hb0 hb1⟩

end TGL.NameRelation
