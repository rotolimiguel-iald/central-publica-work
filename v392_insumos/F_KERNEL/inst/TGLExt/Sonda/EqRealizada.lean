-- SONDA do exame F_KERNEL (12/10/2026), so no sandbox: um modulo independente que tambem REALIZA o lema
-- equacional TGLExt.conjJ.eq_1 (como TheLightReadsItself faz). Pergunta: dois modulos que realizam o mesmo
-- lema equacional coexistem num mesmo ambiente? (colisao futura possivel na v392 e depois)
import TGLExt.ConjugateAct
set_option autoImplicit false
namespace SondaEqRealizada
theorem conjJ_unfold {n : ℕ} (p : (Fin n → ℝ) × (Fin n → ℝ)) : TGLExt.conjJ p = TGLExt.conjJ p := by
  unfold TGLExt.conjJ
  rfl
end SondaEqRealizada
