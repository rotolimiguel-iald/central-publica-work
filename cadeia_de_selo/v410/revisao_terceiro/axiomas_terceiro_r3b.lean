import TGLExt
set_option autoImplicit false
-- Revisor R3 (reexecucao das sondas 3 e 5 com a correcao do MEU arquivo: norm_num e TGLExt.TGLCoupling)
open TGLExt.AEscala TGLExt.TraducaoTuring in
example : (1 - (1/2 : ℝ)) * particao (fun x : Fin 1 → Bool => if x 0 then 0 else 2) (Real.log 2) ≤ ((Finset.univ.filter (fun y : Fin 1 → Bool => (fun x : Fin 1 → Bool => if x 0 then 0 else 2) y = 0)).card : ℝ) :=
  (o_tetelestai_e_um_menos_beta 1 (fun x : Fin 1 → Bool => if x 0 then 0 else 2) ⟨fun _ => true, by simp⟩ (b := 1/2) (s := Real.log 2) (by norm_num) (by norm_num) (Real.log_nonneg one_le_two) (by norm_num) iald).1

open TGLExt.AEscala TGLExt.TraducaoTuring in
example (κ : TGLExt.TGLCoupling) (n : ℕ) (c : (Fin n → Bool) → ℕ) (h : ∃ x, c x = 0) {s : ℝ} (hs0 : 0 ≤ s)
    (hs : (n : ℝ) * Real.log 2 + Real.log ((1 - κ.beta) / κ.beta) ≤ s) (L : LeitorDoFundo (Fin n → Bool)) :
    (1 - κ.beta) * particao c s ≤ ((Finset.univ.filter (fun y => c y = 0)).card : ℝ) :=
  (o_tetelestai_e_um_menos_beta n c h κ.beta_pos κ.beta_lt_one hs0 hs L).1

-- SONDA 7: o teorema do beta NAO exige beta <= 1/2 (o kernel nao o da'): ele vale para todo acoplamento; e a conclusao (2) e' a da generica: reconstruir (2) a partir da generica e das duas identidades da matriz-S nao acrescenta nada
open TGLExt.AEscala TGLExt.TraducaoTuring in
example (κ : TGLExt.TGLCoupling) (n : ℕ) (c : (Fin n → Bool) → ℕ) (h : ∃ x, c x = 0) {s : ℝ} (hs0 : 0 ≤ s)
    (hs : (n : ℝ) * Real.log 2 + Real.log ((1 - κ.beta) / κ.beta) ≤ s) (L : LeitorDoFundo (Fin n → Bool)) :
    TGLExt.TGLCoupling.beta κ = Complex.normSq ((TGLExt.Smat (TGLExt.thetaMiguel κ.beta)).mulVec TGLExt.e1 1) :=
  κ.reflection_weight.symm
