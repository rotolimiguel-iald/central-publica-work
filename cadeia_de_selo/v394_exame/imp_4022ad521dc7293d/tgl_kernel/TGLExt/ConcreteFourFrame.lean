import TGLExt.AQFTCoreInhabitant

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# O FOUR-FRAME DOS BOOSTS: as quatro direções NASCEM da estrutura modular
  [TGLExt — v96b, o incremento 14 do programa SemifiniteAnalysis]

A exigência (H2, TGL_SMOOTH_MODULAR_FOUR_FRAME): as quatro direções
E₀..E₃ devem SURGIR da rede modular — não ser inseridas à mão. Esta
pedra as constrói na face algébrica: a direção fiducial é a do Nome
(ω(I): o tempo modular), e as TRÊS direções espaciais são as ÓRBITAS
DE BOOST — K_i aplicado à fiducial, onde K₁,K₂,K₃ são exatamente os
geradores de boost do v63 (os MESMOS que satisfazem [K₁,K₂] = −J₃:
Lorentz ≠ Euclides em kernel). A matriz E das quatro direções tem
det = 1 ≠ 0 POR TEOREMA (não por hipótese) e o teorema condicional de
H2 (v66) DISPARA: coframe dual E⁻¹E = 1 e métrica soldada lorentziana
por congruência.

O QUE ESTA PEDRA PROVA/CONSTRÓI [KERNEL]:
* ★ `modularFiducial` (DEF) — a direção do Nome;
* ★★ `modularFrame` (DEF) — E = [fiducial | K₁v | K₂v | K₃v]: as
  colunas VÊM dos geradores de boost do v63;
* ★ `modularFrame_col_zero/boost` — as colunas são as órbitas (rfl);
* ★★ `modularFrame_det_isUnit` — det E = 1: a independência das
  quatro direções é TEOREMA;
* ★★★★ `concrete_four_frame_fires` — H2 finito DISPARA no frame
  construído: E⁻¹E = 1 ∧ Lorentz por congruência — a tétrada não é
  mais um dado: é um TERMO derivado dos boosts.

HONESTIDADE: face ALGÉBRICA num ponto — o CAMPO suave E_a(x) com
det ≠ 0 em toda parte (a 1ª equação de estrutura de Cartan sobre o
espaço-tempo) é o conteúdo genuíno de H2 e segue ABERTO; o gate NÃO
se move. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- a direção fiducial: a do Nome (o tempo modular). -/
def modularFiducial : Fin 4 → ℝ := fun i => if i = 0 then 1 else 0

/-- O FOUR-FRAME DOS BOOSTS: coluna 0 = fiducial; coluna i = K_i
    aplicado à fiducial (as órbitas de boost do v63). -/
def modularFrame : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.of fun i b =>
    if b = 0 then modularFiducial i
    else if b = 1 then (K1.mulVec modularFiducial) i
    else if b = 2 then (K2.mulVec modularFiducial) i
    else (K3.mulVec modularFiducial) i

/-- [KERNEL] ★ a coluna 0 é a fiducial (o Nome). -/
theorem modularFrame_col_zero (i : Fin 4) :
    modularFrame i 0 = modularFiducial i := rfl

/-- [KERNEL] ★ as colunas espaciais são as ÓRBITAS DE BOOST. -/
theorem modularFrame_col_boost1 (i : Fin 4) :
    modularFrame i 1 = (K1.mulVec modularFiducial) i := rfl

theorem modularFrame_col_boost2 (i : Fin 4) :
    modularFrame i 2 = (K2.mulVec modularFiducial) i := rfl

theorem modularFrame_col_boost3 (i : Fin 4) :
    modularFrame i 3 = (K3.mulVec modularFiducial) i := rfl

/-- o frame dos boosts, em componentes: é a identidade 4×4 (a
    fiducial gera, pelos boosts, exatamente os quatro eixos). -/
theorem modularFrame_eq_one : modularFrame = 1 := by
  ext i b
  fin_cases i <;> fin_cases b <;>
    simp [modularFrame, modularFiducial, K1, K2, K3, Matrix.mulVec,
      dotProduct, Fin.sum_univ_four, Matrix.one_apply, Matrix.vecHead,
      Matrix.vecTail, Fin.isValue]

/-- [KERNEL] ★★ A INDEPENDÊNCIA DAS QUATRO DIREÇÕES É TEOREMA:
    det E = 1 ≠ 0 — nada foi inserido à mão. -/
theorem modularFrame_det_isUnit : IsUnit modularFrame.det := by
  rw [modularFrame_eq_one, Matrix.det_one]
  exact isUnit_one

/-- [KERNEL] ★★★★ H2 FINITO DISPARA NO FRAME CONSTRUÍDO: coframe
    dual E⁻¹E = 1 e métrica soldada LORENTZIANA por congruência — a
    tétrada deixou de ser hipótese na face algébrica. -/
theorem concrete_four_frame_fires :
    modularFrame⁻¹ * modularFrame = 1
      ∧ LorentzByCongruence (solderMetric4 modularFrame⁻¹) :=
  four_frame_gives_lorentz_metric modularFrame modularFrame_det_isUnit

end

end TGLExt
