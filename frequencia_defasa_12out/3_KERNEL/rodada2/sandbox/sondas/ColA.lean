/- SONDA de instalação (rodada 2; NÃO é pedra): um módulo vizinho que também gera a equação `TGLExt.rhoOut.eq_1`
   (por `simp [rhoOut]`), sem importar a pedra. -/
import TGLExt.SMatrix

open Matrix

namespace SondaColA

theorem rhoOut_zero_via_unfold : TGLExt.rhoOut 0 = TGLExt.Smat 0 * Matrix.single 0 0 1 * (TGLExt.Smat 0)ᴴ := by
  simp [TGLExt.rhoOut]

end SondaColA

#print axioms SondaColA.rhoOut_zero_via_unfold
