import TGLExt.BenchCertificate

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O FRAME CURVO: a primeira face FORTE alimentada
  [TGLExt — v104, o incremento 21 do programa SemifiniteAnalysis]

O v103 endureceu o certificado e provou que a bancada não o alimenta.
Esta pedra alimenta a PRIMEIRA das três faces fortes — o frame:

* `theCurvedFrame : SmoothFrameData` — E(x) = diag(1+x₀², 1, 1, 1):
  suave (C^∞, polinomial em cada entrada), det = 1+x₀² invertível em
  TODA PARTE (1+x₀² ≥ 1 > 0 — nunca zero, sem hipótese);
* ★ `curvedFrame_nonconstant` — E NÃO é constante (x₀=1 vs x₀=0
  distinguem a entrada (0,0): 2 ≠ 1): o dente `frame_nonconstant` do
  tipo FORTE está SATISFEITO por este termo — a primeira das três
  faces fortes tem habitante;
* ★ `curvedFrame_det_everywhere` — o determinante é unidade em TODO
  ponto (eco explícito do campo, para a escada).

HONESTIDADE: alimentar a face do frame NÃO constrói o certificado
forte — faltam as DUAS faces duras (Dirac genuinamente ILIMITADO;
fibra ∞-dim na rede) e toda a metade v2 (curvatura como estrutura,
covariância, III₁). Nenhum nome reservado é usado; nenhuma flag de
gate se move.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- a função-perfil da entrada (0,0): 1 + x₀². -/
def profileFn (x : Fin 4 → ℝ) : ℝ := 1 + (x 0) ^ 2

theorem profileFn_smooth : ContDiff ℝ (⊤ : ℕ∞) profileFn := by
  unfold profileFn
  exact contDiff_const.add ((contDiff_apply ℝ ℝ 0).pow 2)

theorem profileFn_pos (x : Fin 4 → ℝ) : 0 < profileFn x := by
  unfold profileFn
  positivity

/-- O FRAME CURVO: E(x) = diag(1+x₀², 1, 1, 1). -/
def theCurvedFrame : SmoothFrameData where
  E := fun x => Matrix.diagonal (fun i => if i = 0 then profileFn x else 1)
  smooth := by
    intro i j
    by_cases hij : i = j
    · subst hij
      by_cases hi : i = 0
      · subst hi
        have h : (fun x => Matrix.diagonal
            (fun k : Fin 4 => if k = 0 then profileFn x else 1) 0 0)
            = profileFn := by
          funext x
          simp [Matrix.diagonal_apply]
        rw [h]
        exact profileFn_smooth
      · have h : (fun x => Matrix.diagonal
            (fun k : Fin 4 => if k = 0 then profileFn x else 1) i i)
            = fun _ => (1 : ℝ) := by
          funext x
          simp [Matrix.diagonal_apply, hi]
        rw [h]
        exact contDiff_const
    · have h : (fun x => Matrix.diagonal
          (fun k : Fin 4 => if k = 0 then profileFn x else 1) i j)
          = fun _ => (0 : ℝ) := by
        funext x
        simp [Matrix.diagonal_apply, hij]
      rw [h]
      exact contDiff_const
  det_unit := fun x => by
    have h : (Matrix.diagonal
        (fun i : Fin 4 => if i = 0 then profileFn x else 1)).det
        = profileFn x := by
      rw [Matrix.det_diagonal, Fin.prod_univ_four]
      simp
    rw [h]
    exact isUnit_iff_ne_zero.mpr (ne_of_gt (profileFn_pos x))

theorem curvedFrame_E_apply (x : Fin 4 → ℝ) :
    theCurvedFrame.E x
      = Matrix.diagonal (fun i => if i = 0 then profileFn x else 1) := rfl

/-- [KERNEL] ★ O DENTE SATISFEITO: o frame curvo NÃO é constante —
    a primeira das três faces do tipo FORTE tem habitante. -/
theorem curvedFrame_nonconstant :
    ∃ x y : Fin 4 → ℝ, theCurvedFrame.E x ≠ theCurvedFrame.E y := by
  refine ⟨(fun _ => 1), (fun _ => 0), fun h => ?_⟩
  have h00 := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 0 0) h
  rw [curvedFrame_E_apply, curvedFrame_E_apply] at h00
  simp only [Matrix.diagonal_apply, if_pos rfl] at h00
  unfold profileFn at h00
  norm_num at h00

/-- [KERNEL] ★ o eco explícito: det(E(x)) é unidade em TODO ponto. -/
theorem curvedFrame_det_everywhere :
    ∀ x : Fin 4 → ℝ, IsUnit (theCurvedFrame.E x).det :=
  theCurvedFrame.det_unit

end

end TGLExt
