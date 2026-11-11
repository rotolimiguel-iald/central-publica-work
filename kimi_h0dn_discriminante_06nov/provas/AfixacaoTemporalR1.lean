import TGLExt.PsionCanto
import TGLExt.ConjugateAct

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# AFIXAÇÃO TEMPORAL E AGREGAÇÃO ARITMÉTICA — pedra candidata R1, 06/11/2026

Escopo algébrico: um registro clássico `Fin 2` distingue preparo (`n=0`) e
travessia (`n=1`) sem acrescentar outra evolução ao sistema. A pedra prova que
a parte do sistema devolvida é exatamente a entrada ou o canal original, que os
detectores não mudam por causa do registro e que a completeza de Kraus preserva
o traço. Também prova a normalização da média aritmética usada na agregação.

LIMITES: não é implementação física, não é prova de CPTP para um aparelho, não
mede o rival óptico, não fixa o eixo P/Q na natureza e não move o gate. A
conjugação `conjJ` é involutiva e, sozinha, não conta travessias. O modelo de
registro é por setores clássicos, não uma dilatação tensorial completa nova.
-/

noncomputable section
namespace TGLExt.AfixacaoTemporal
open Matrix TGL.GravitonShadow TGLExt.PsionCanto TGLExt

abbrev BellIndex := Fin 2 × Fin 2
abbrev BellMat := Matrix BellIndex BellIndex ℂ
abbrev TaggedBell := Fin 2 → BellMat

/-- Um estado de sistema acompanhado por uma marca clássica `tag`. -/
def tagState (tag : Fin 2) (rho : BellMat) : TaggedBell :=
  fun r => if r = tag then rho else 0

/-- A informação do sistema, somada sobre as duas marcas clássicas. -/
def systemOf (x : TaggedBell) : BellMat := x 0 + x 1

/-- O canal abstrato de duas Kraus cujos resultados ficam na marca `1`. -/
def mirrorChannel (M : Fin 2 → BellMat) (rho : BellMat) : BellMat :=
  M 0 * rho * M 0 + M 1 * rho * M 1

/-- A parte do sistema não depende da marca. -/
lemma system_tagState (tag : Fin 2) (rho : BellMat) :
    systemOf (tagState tag rho) = rho := by
  fin_cases tag <;> simp [systemOf, tagState]

/-- O controle `n=0` devolve a própria entrada. -/
lemma taggedInitial_system (rho : BellMat) :
    systemOf (tagState 0 rho) = rho :=
  system_tagState 0 rho

/-- A travessia devolve exatamente o canal original, sem mapa adicional. -/
lemma taggedTraversal_system (M : Fin 2 → BellMat) (rho : BellMat) :
    systemOf (tagState 1 (mirrorChannel M rho)) = mirrorChannel M rho :=
  system_tagState 1 (mirrorChannel M rho)

/-- O detector lê a mesma intensidade depois de somar a marca temporal. -/
lemma tagged_detector_unchanged (D E : BellMat) :
    (D * systemOf (tagState 1 E)).trace = (D * E).trace := by
  rw [system_tagState]

/-- Completeza das Kraus implica preservação do traço. -/
lemma mirrorChannel_trace (M : Fin 2 → BellMat) (rho : BellMat)
    (hK : M 0 * M 0 + M 1 * M 1 = 1) :
    (mirrorChannel M rho).trace = rho.trace := by
  have h0 : (M 0 * rho * M 0).trace = (rho * (M 0 * M 0)).trace := by
    rw [Matrix.trace_mul_cycle, Matrix.trace_mul_comm]
  have h1 : (M 1 * rho * M 1).trace = (rho * (M 1 * M 1)).trace := by
    rw [Matrix.trace_mul_cycle, Matrix.trace_mul_comm]
  have hsum : rho * (M 0 * M 0) + rho * (M 1 * M 1) = rho := by
    calc
      rho * (M 0 * M 0) + rho * (M 1 * M 1) = rho * (M 0 * M 0 + M 1 * M 1) :=
        (mul_add rho (M 0 * M 0) (M 1 * M 1)).symm
      _ = rho := by rw [hK, Matrix.mul_one]
  rw [mirrorChannel, Matrix.trace_add, h0, h1, ← Matrix.trace_add, hsum]

/-- Com entrada normalizada e completeza, a marca de travessia preserva peso um. -/
lemma taggedTraversal_trace_one (M : Fin 2 → BellMat) (rho : BellMat)
    (hK : M 0 * M 0 + M 1 * M 1 = 1) (hrho : rho.trace = 1) :
    (systemOf (tagState 1 (mirrorChannel M rho))).trace = 1 := by
  rw [system_tagState, mirrorChannel_trace M rho hK, hrho]

/-- O controle também conserva a normalização da entrada. -/
lemma taggedInitial_trace (rho : BellMat) :
    (systemOf (tagState 0 rho)).trace = rho.trace := by
  rw [system_tagState]

/-- A marca lê o próprio registro no setor correspondente. -/
lemma record_tagState (tag : Fin 2) (rho : BellMat) :
    tagState tag rho tag = rho := by
  simp [tagState]

/-- A marca não revela o conteúdo do outro setor. -/
lemma record_other_tagState (tag other : Fin 2) (rho : BellMat) (h : other ≠ tag) :
    tagState tag rho other = 0 := by
  simp [tagState, h]

/-- Preparo e travessia são registros distintos antes do detector. -/
lemma tags_distinguish_control_and_crossing (rho sigma : BellMat) :
    tagState 0 rho 0 = rho ∧ tagState 1 sigma 1 = sigma ∧ (0 : Fin 2) ≠ 1 := by
  simp [tagState]

/-- A conjugação sozinha é involutiva: não é um contador absoluto de travessias. -/
lemma conjugation_is_not_a_counter {n : ℕ}
    (p : (Fin n → ℝ) × (Fin n → ℝ)) : conjJ (conjJ p) = p :=
  J_squared_is_one p

/-- A agregação por média aritmética de `m` entradas. -/
def arithmeticAggregate {m : ℕ} (x : Fin m → ℝ) : ℝ :=
  (m : ℝ)⁻¹ * ∑ i, x i

/-- Os pesos `1/m` são normalizados: a média de um é um. -/
lemma arithmeticAggregate_one (m : ℕ) (hm : 0 < m) :
    arithmeticAggregate (fun _ : Fin m => (1 : ℝ)) = 1 := by
  simp [arithmeticAggregate, Finset.sum_const, nsmul_eq_mul, hm.ne']

/-- A média de qualquer constante é a própria constante. -/
lemma arithmeticAggregate_const (m : ℕ) (hm : 0 < m) (c : ℝ) :
    arithmeticAggregate (fun _ : Fin m => c) = c := by
  simp [arithmeticAggregate, Finset.sum_const, nsmul_eq_mul, hm.ne']

end TGLExt.AfixacaoTemporal

#print axioms TGLExt.AfixacaoTemporal.system_tagState
#print axioms TGLExt.AfixacaoTemporal.taggedInitial_system
#print axioms TGLExt.AfixacaoTemporal.taggedTraversal_system
#print axioms TGLExt.AfixacaoTemporal.tagged_detector_unchanged
#print axioms TGLExt.AfixacaoTemporal.mirrorChannel_trace
#print axioms TGLExt.AfixacaoTemporal.taggedTraversal_trace_one
#print axioms TGLExt.AfixacaoTemporal.taggedInitial_trace
#print axioms TGLExt.AfixacaoTemporal.record_tagState
#print axioms TGLExt.AfixacaoTemporal.record_other_tagState
#print axioms TGLExt.AfixacaoTemporal.tags_distinguish_control_and_crossing
#print axioms TGLExt.AfixacaoTemporal.conjugation_is_not_a_counter
#print axioms TGLExt.AfixacaoTemporal.arithmeticAggregate_one
#print axioms TGLExt.AfixacaoTemporal.arithmeticAggregate_const
