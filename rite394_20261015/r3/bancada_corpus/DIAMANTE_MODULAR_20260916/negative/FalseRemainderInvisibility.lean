import TGLExt.EquivariantSection

open Matrix
-- Negative control only. The full spectral reading for weights [1,2] erases
-- this R and retains this p, but that does not imply [R,p]=0.
example : Commute (!![0, 1; 1, 0] : Matrix (Fin 2) (Fin 2) ℂ)
    (!![1, 0; 0, 0] : Matrix (Fin 2) (Fin 2) ℂ) := by
  change _ * _ = _ * _
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply, Fin.sum_univ_two]
