import TGLExt.StrongAssembly

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A SOLDA CONTÍNUA: o campo g(x) = E(x)ᵀ η E(x) — e o QUARTO FLIP
  [TGLExt — v107, o incremento 27 do programa SemifiniteAnalysis]

O v63 provou a solda PONTUAL (g = eᵀηe simétrica; det g = −det(e)²).
Esta pedra a eleva a CAMPO sobre o frame CURVO do v104:

* `theSolderField` — g(x) = solderMetric4(E(x)) com E o frame curvo:
  ★ diagonal explícita diag((1+x₀²)², −1, −1, −1);
  ★ SIMÉTRICA em todo ponto; ★ SUAVE (C^∞ entrada a entrada);
  ★ `theSolderField_det_neg` — det g(x) = −(1+x₀²)² < 0 em TODA PARTE:
  o volume lorentziano JAMAIS degenera (a face do sinal, típada);
  ★ NÃO-CONSTANTE (a solda é genuinamente curva — herda o forte);
* `SolderFieldData` — o contrato TIPADO do 4º flip: frame forte +
  g nascida da solda + suavidade + det < 0 + não-constância;
* ★★★ `qgStrongCertificate_solder` — O QUARTO FLIP: o nome reservado
  ganha termo com contrato Σ'. O selo NÃO se move (4 < 6).

HONESTIDADE (a lição do v103 aplicada a nós mesmos): o contrato de
EINSTEIN **não** é tipado nesta pedra — um tipo sem CURVATURA como
estrutura seria mais fraco que o espírito da flag, e flipar sobre ele
seria bancada. A curvatura contínua (geometria riemanniana plena)
não está na mathlib de hoje: o 5º flip fica NOMEADO e reservado;
a assinatura plena (1,3) de Sylvester idem (det < 0 é a metade
honesta tipável em 4D).

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix

noncomputable section

/-- O CAMPO SOLDADO: g(x) = E(x)ᵀ η E(x) sobre o frame curvo. -/
def theSolderField (x : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  solderMetric4 (theCurvedFrame.E x)

/-- [KERNEL] ★ a forma diagonal explícita da solda curva. -/
theorem theSolderField_eq (x : Fin 4 → ℝ) :
    theSolderField x
      = Matrix.diagonal (fun i => if i = 0 then profileFn x ^ 2 else -1) := by
  unfold theSolderField solderMetric4
  rw [curvedFrame_E_apply, Matrix.diagonal_transpose]
  unfold eta4
  rw [Matrix.diagonal_mul_diagonal, Matrix.diagonal_mul_diagonal]
  congr 1
  funext i
  fin_cases i <;> simp <;> ring

/-- [KERNEL] ★ g é simétrica em todo ponto (herdado da solda pontual). -/
theorem theSolderField_symm (x : Fin 4 → ℝ) :
    (theSolderField x)ᵀ = theSolderField x :=
  solderMetric4_symm _

/-- [KERNEL] ★ o determinante do campo: det g(x) = −(1+x₀²)². -/
theorem theSolderField_det (x : Fin 4 → ℝ) :
    (theSolderField x).det = -(profileFn x ^ 2) := by
  have hdet : (theCurvedFrame.E x).det = profileFn x := by
    rw [curvedFrame_E_apply, Matrix.det_diagonal, Fin.prod_univ_four]
    simp
  unfold theSolderField
  rw [solderMetric4_det, hdet]

/-- [KERNEL] ★★ O VOLUME LORENTZIANO JAMAIS DEGENERA: det g(x) < 0 em
    toda parte (a face do sinal em 4D, tipada; Sylvester pleno = nomeado). -/
theorem theSolderField_det_neg (x : Fin 4 → ℝ) :
    (theSolderField x).det < 0 := by
  rw [theSolderField_det]
  have h := profileFn_pos x
  nlinarith

theorem theSolderField_nondegenerate (x : Fin 4 → ℝ) :
    IsUnit (theSolderField x).det :=
  isUnit_iff_ne_zero.mpr (ne_of_lt (theSolderField_det_neg x))

/-- [KERNEL] ★ a solda é SUAVE (C^∞, entrada a entrada). -/
theorem theSolderField_smooth (i j : Fin 4) :
    ContDiff ℝ (⊤ : ℕ∞) (fun x => theSolderField x i j) := by
  have h : (fun x => theSolderField x i j)
      = fun x => Matrix.diagonal
          (fun k : Fin 4 => if k = 0 then profileFn x ^ 2 else -1) i j := by
    funext x
    rw [theSolderField_eq]
  rw [h]
  by_cases hij : i = j
  · subst hij
    by_cases hi : i = 0
    · subst hi
      have h2 : (fun x => Matrix.diagonal
          (fun k : Fin 4 => if k = 0 then profileFn x ^ 2 else -1) 0 0)
          = fun x => profileFn x ^ 2 := by
        funext x
        simp [Matrix.diagonal_apply]
      rw [h2]
      exact profileFn_smooth.pow 2
    · have h2 : (fun x => Matrix.diagonal
          (fun k : Fin 4 => if k = 0 then profileFn x ^ 2 else -1) i i)
          = fun _ => (-1 : ℝ) := by
        funext x
        simp [Matrix.diagonal_apply, hi]
      rw [h2]
      exact contDiff_const
  · have h2 : (fun x => Matrix.diagonal
        (fun k : Fin 4 => if k = 0 then profileFn x ^ 2 else -1) i j)
        = fun _ => (0 : ℝ) := by
      funext x
      simp [Matrix.diagonal_apply, hij]
    rw [h2]
    exact contDiff_const

/-- [KERNEL] ★ a solda é genuinamente CURVA: g NÃO é constante. -/
theorem theSolderField_nonconstant :
    ∃ x y : Fin 4 → ℝ, theSolderField x ≠ theSolderField y := by
  refine ⟨(fun _ => 1), (fun _ => 0), fun h => ?_⟩
  have h00 := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 0 0) h
  rw [theSolderField_eq, theSolderField_eq] at h00
  simp only [Matrix.diagonal_apply, if_pos rfl] at h00
  unfold profileFn at h00
  norm_num at h00

/-! ## O contrato tipado do 4º flip -/

/-- [DATA — o contrato FORTE da solda] frame forte + métrica NASCIDA da
    solda (g = EᵀηE) + suavidade + volume lorentziano nunca-nulo +
    não-constância (a solda plana da bancada NÃO entra). -/
structure SolderFieldData where
  frame : SmoothFrameData
  g : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ
  solder_eq : ∀ x, g x = solderMetric4 (frame.E x)
  g_symm : ∀ x, (g x)ᵀ = g x
  g_smooth : ∀ i j : Fin 4, ContDiff ℝ (⊤ : ℕ∞) (fun x => g x i j)
  lorentz_det : ∀ x, (g x).det < 0
  frame_nonconstant : ∃ x y : Fin 4 → ℝ, frame.E x ≠ frame.E y

/-- [KERNEL] ★★ o habitante: a solda curva completa. -/
def theSolderData : SolderFieldData where
  frame := theCurvedFrame
  g := theSolderField
  solder_eq := fun _ => rfl
  g_symm := theSolderField_symm
  g_smooth := theSolderField_smooth
  lorentz_det := theSolderField_det_neg
  frame_nonconstant := curvedFrame_nonconstant

/-- [KERNEL] ★★★ O QUARTO FLIP: o nome reservado do gate ganha termo —
    solda forte com métrica não-constante. O selo NÃO se move (4 < 6). -/
def qgStrongCertificate_solder :
    Σ' (s : SolderFieldData), ∃ x y : Fin 4 → ℝ, s.g x ≠ s.g y :=
  ⟨theSolderData, theSolderField_nonconstant⟩

/-- [KERNEL — cola] a solda e o certificado forte compartilham o MESMO
    frame (o par é compatível; o mestre contínuo é o 5º flip, nomeado). -/
theorem solder_frame_eq_strong :
    theSolderData.frame = theStrongCertificate.frame := rfl

end

end TGLExt
