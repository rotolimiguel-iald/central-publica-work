import TGLExt.BisognanoWichmann

/-!
# Auditoria (lente ESTATUTO E REGRA) da F1.TEMPO — sonda AUD-8 (só sandbox do auditor)

S44.1 do operador: «Na mecânica clássica e nos sistemas estritamente hamiltonianos, o volume no espaço de fases
é rigidamente conservado pelo teorema de Liouville: tudo gira indefinidamente sem nunca pousar …». O controle
C-T4-a da pedra (`volume_kept_yet_lands`) usa o boost `B(s)` (det 1), que pousa no raio nulo passado. AUD-8 mostra
que o boost é SIMPLÉTICO em ℝ² (preserva a forma `J = [[0,1],[−1,0]]`): é um mapa hamiltoniano linear. Logo o
controle cai DENTRO do escopo «estritamente hamiltoniano» da frase — uma trajetória pousa (variedade estável,
medida nula); o que Liouville proíbe é a BACIA (atrator com volume), não o pouso de toda trajetória [KNOWN].
Sem sorry, sem axiom, sem native_decide; a constante da casa não entra.
-/

set_option autoImplicit false

open TGLExt
open scoped Matrix

namespace AudEstatutoTempo3

/-- Em 2×2 real: `Mᵀ J M = (det M)·J` (identidade algébrica). -/
theorem aud_two_by_two_symplectic (M : Matrix (Fin 2) (Fin 2) ℝ) :
    Mᵀ * !![0, 1; -1, 0] * M = M.det • !![0, 1; -1, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.det_fin_two, Matrix.transpose_apply] <;> ring

/-- AUD-8: o boost preserva a forma simplética de ℝ² (det 1 em 2×2 ⟺ simplético). -/
theorem aud_boost_is_symplectic (s : ℝ) :
    (TGLExt.boost s)ᵀ * !![0, 1; -1, 0] * TGLExt.boost s = !![0, 1; -1, 0] := by
  rw [aud_two_by_two_symplectic, TGLExt.boost_det, one_smul]

end AudEstatutoTempo3

#print axioms AudEstatutoTempo3.aud_two_by_two_symplectic
#print axioms AudEstatutoTempo3.aud_boost_is_symplectic
