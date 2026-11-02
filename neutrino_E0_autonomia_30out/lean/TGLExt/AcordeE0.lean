import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Positivity

set_option autoImplicit false

/-!
# Acorde e escala de `E0`

Formalização algébrica de um acorde de cinco notas reais. A nota principal tem
índice `0`; uma transposição multiplica todas as notas pelo mesmo fator. A
preservação das razões exige apenas que esse fator seja não nulo.

`E_pent` permanece um dado independente: este módulo não lhe atribui valor e só
transporta uma avaliação de escala quando recebe um `ScaleEvaluation` separado.
O fator de semitom descendente é opcional e não é premissa de `E0`.
-/

namespace TGLExt.AcordeE0

/-- Um acorde formado por exatamente cinco notas reais. -/
structure Chord where
  notes : Fin 5 → ℝ

/-- O índice da nota principal do acorde. -/
def principalIndex : Fin 5 := 0

/-- A nota principal do acorde. -/
def principal (chord : Chord) : ℝ :=
  chord.notes principalIndex

/-- Transposição multiplicativa de todas as notas pelo fator `r`. -/
def transpose (r : ℝ) (chord : Chord) : Chord where
  notes i := r * chord.notes i

/-- Razão entre uma nota do acorde e sua nota principal. -/
noncomputable def ratioToPrincipal (chord : Chord) (i : Fin 5) : ℝ :=
  chord.notes i / principal chord

/-- Uma transposição por fator não nulo preserva todas as razões à principal. -/
theorem transpose_preserves_every_ratio (r : ℝ) (hr : r ≠ 0)
    (chord : Chord) (i : Fin 5) :
    ratioToPrincipal (transpose r chord) i = ratioToPrincipal chord i := by
  simp only [ratioToPrincipal, principal, transpose]
  exact mul_div_mul_left _ _ hr

/-- Escala declarada: `E0 = r * E_pent`, sem fixar `E_pent`. -/
def E0 (r E_pent : ℝ) : ℝ :=
  r * E_pent

/-- Certificado separado de que um `E_pent`, fornecido independentemente, vale
`target`. Nenhum valor numérico é fornecido por este módulo. -/
structure ScaleEvaluation (E_pent target : ℝ) where
  E_pent_eq_target : E_pent = target

/-- Com um certificado independente para `E_pent`, a definição de `E0` transporta
essa avaliação para o alvo correspondente. -/
theorem E0_eq_target_of_scaleEvaluation (r E_pent target : ℝ)
    (evaluation : ScaleEvaluation E_pent target) :
    E0 r E_pent = r * target := by
  unfold E0
  rw [evaluation.E_pent_eq_target]

/-- Fator opcional de um semitom descendente, `r = 2^(-1/12)`. -/
noncomputable def semitoneRatio : ℝ :=
  (2 : ℝ) ^ (-1 / 12 : ℝ)

/-- O fator opcional de semitom é não nulo, portanto também pode transpor. -/
theorem semitoneRatio_ne_zero : semitoneRatio ≠ 0 := by
  unfold semitoneRatio
  positivity

end TGLExt.AcordeE0
