import TGLExt.Cocycle
import TGLExt.TheFlowLawContrast
import TGLExt.LeiDoDiminuto

set_option autoImplicit false

/-!
# Pedra da gerência c1 (02/11/2026), sobre a fala do operador; NOME RATIFICADO pelo operador em 03/11/2026 (verbatim sha16 `73466598d3419fb0`: «concordo com todos os nomes e os ratifico»); entra no kernel na v407; compilada no sandbox da v407 (k407c/final), só no trio.

«É isso mesmo, mas agora o K me pareceu fazer a função do próprio gráviton ( que antes eu disse ser o operador “=“, aquele que criva)» (02/11/2026, verbatim sha16 1c05c03070544839, em work\cunhagens_13out)

`K β E a b = (E b / E a)^(2β/3)` é a razão de Hubble entre dois registros: a forma de `the_derived_kernel_factor`, sem luz na fórmula.
Prova-se que K obedece às três leis do sinal de igual, com holonomia trivial; que sua leitura angular é um cociclo unitário com as leis
de `TGLExt.Cocycle`, e a face K volta em t = −i; que o cociclo do kernel entre dois estados cujos logaritmos diferem por um escalar é
exatamente essa fase; e que o crivo das razões tem testemunha única. Ler K como o gráviton é do operador [ONTO]: não é termo de kernel.
Três homônimos: este K é a razão de Hubble; o K modular é outro objeto, e aqui ele só aparece como diferença de logaritmos; K_β de Cartan não entra.
-/

namespace TGLExt.OIgual
open TGLExt TGLExt.TheFlowLawContrast TGLExt.LeiDoDiminuto

noncomputable section

/-- A razão de Hubble entre os registros `a` e `b`. -/
def K (β : ℝ) (E : ℝ → ℝ) (a b : ℝ) : ℝ := (E b / E a) ^ ((2 / 3 : ℝ) * β)

variable {β : ℝ} {E : ℝ → ℝ} (hpos : ∀ s, 0 < E s) (a b c : ℝ)
include hpos

theorem K_pos : 0 < K β E a b := Real.rpow_pos_of_pos (div_pos (hpos b) (hpos a)) _

/-- Reflexiva. -/
theorem K_refl : K β E a a = 1 := by
  unfold K
  rw [div_self (hpos a).ne', Real.one_rpow]

/-- Simétrica. -/
theorem K_symm : K β E b a = (K β E a b)⁻¹ := by
  unfold K
  rw [← Real.inv_rpow (div_pos (hpos b) (hpos a)).le, inv_div]

/-- Transitiva. -/
theorem K_trans : K β E a b * K β E b c = K β E a c := by
  unfold K
  rw [← Real.mul_rpow (div_pos (hpos b) (hpos a)).le (div_pos (hpos c) (hpos b)).le]
  congr 1
  have ha := (hpos a).ne'
  have hb := (hpos b).ne'
  field_simp

/-- Holonomia trivial: a volta pelo triângulo fecha em 1, como `cocycle_triangle`. O transporte não depende do caminho. -/
theorem K_triangle : K β E a b * K β E b c * K β E c a = 1 := by
  rw [K_trans hpos a b c, K_symm hpos a c, mul_inv_cancel₀ (K_pos hpos a c).ne']

/-- A leitura angular de K. -/
def leitura (β : ℝ) (E : ℝ → ℝ) (a b t : ℝ) : ℂ :=
  Complex.exp (((t : ℂ) * Complex.I) * (Real.log (K β E a b) : ℂ))

omit hpos in
/-- A leitura tem norma 1: só lê. -/
theorem leitura_norm (t : ℝ) : ‖leitura β E a b t‖ = 1 := by
  unfold leitura
  have h : ((t : ℂ) * Complex.I) * (Real.log (K β E a b) : ℂ) = ((t * Real.log (K β E a b) : ℝ) : ℂ) * Complex.I := by
    push_cast
    ring
  rw [h, Complex.norm_exp_ofReal_mul_I]

/-- Colagem: a lei de `cocycle_chain`. -/
theorem leitura_chain (t : ℝ) : leitura β E a b t * leitura β E b c t = leitura β E a c t := by
  unfold leitura
  rw [← Complex.exp_add, ← K_trans hpos a b c, Real.log_mul (K_pos hpos a b).ne' (K_pos hpos b c).ne']
  congr 1
  push_cast
  ring

/-- A face volta em t = −i: o peso K sai da leitura por continuação. -/
theorem a_face_em_menos_i :
    Complex.exp (((-Complex.I) * Complex.I) * (Real.log (K β E a b) : ℂ)) = (K β E a b : ℂ) := by
  have h : (-Complex.I) * Complex.I = 1 := by simp
  rw [h, one_mul, ← Complex.ofReal_exp, Real.exp_log (K_pos hpos a b)]

/-- K é a razão de Hubble do kernel. -/
theorem K_e_a_lei (β Hcmb : ℝ) (N : ℝ) (hN : N ≠ 0)
    (hE : ∀ s ∈ Set.uIcc (0 : ℝ) N, DifferentiableAt ℝ E s)
    (hint : IntervalIntegrable (frwContrast E) MeasureTheory.volume 0 N) :
    H0localContrast β Hcmb (frwContrast E) N = Hcmb * K β E 0 N :=
  the_derived_kernel_factor β Hcmb E N hN hE hpos hint

omit hpos

/-- O crivo tem testemunha única: mesmas razões se e só se há exatamente um fator. Igualdade como seleção única. -/
theorem o_crivo_tem_testemunha_unica (A B : Acorde) (hA : notaPrincipal A ≠ 0) (hB : notaPrincipal B ≠ 0) :
    (∀ i, razao B i = razao A i) ↔ ∃! r : ℝ, r ≠ 0 ∧ B = transpor r A := by
  rw [mesmas_razoes_iff_transposicao A B hA hB]
  constructor
  · rintro ⟨r, hr, h⟩
    refine ⟨r, ⟨hr, h⟩, fun s hs => ?_⟩
    have h1 : notaPrincipal B = r * notaPrincipal A := by rw [h]; rfl
    have h2 : notaPrincipal B = s * notaPrincipal A := by rw [hs.2]; rfl
    exact mul_right_cancel₀ hA (h2.symm.trans h1)
  · rintro ⟨r, h, _⟩
    exact ⟨r, h⟩

section Cociclo
variable {n : Type} [Fintype n] [DecidableEq n]

/-- A ponte com o cociclo do kernel: se os logaritmos diferem por um escalar `c`, o cociclo é a fase pura. O cociclo é gerado pela diferença. -/
theorem cociclo_de_um_escalar (phi psi : Matrix n n ℂ) (c : ℂ) (h : logRho phi = logRho psi + c • 1) (t : ℝ) :
    cocycle phi psi t = Complex.exp ((t : ℂ) * Complex.I * c) • (1 : Matrix n n ℂ) := by
  have hc : Commute (logRho phi) (logRho psi) := by
    rw [h]
    exact (Commute.refl _).add_left ((Commute.one_left _).smul_left c)
  rw [cocycle_of_commute phi psi hc t, h, add_sub_cancel_left, smul_smul]
  have e : ((t : ℂ) * Complex.I * c) • (1 : Matrix n n ℂ) = Matrix.diagonal (fun _ => (t : ℂ) * Complex.I * c) := by
    ext i j
    by_cases hij : i = j
    · subst hij; simp
    · simp [hij]
  rw [e, Matrix.exp_diagonal]
  ext i j
  by_cases hij : i = j
  · subst hij
    simp [Complex.exp_eq_exp_ℂ]
  · simp [hij]

/-- ω(I) = 1 proíbe o fator global: dois estados normalizados não diferem por um escalar `k ≠ 1`. K só pode ser razão entre um setor e o todo. -/
theorem escalar_entre_normalizados_e_um (phi psi : Matrix n n ℂ) (k : ℂ) (h : phi = k • psi)
    (h1 : phi.trace = 1) (h2 : psi.trace = 1) : k = 1 := by
  rw [h, Matrix.trace_smul, h2, smul_eq_mul, mul_one] at h1
  exact h1

end Cociclo

/-- O fundo é a média sobre o peso inteiro; o local é a média condicionada ao que sobreviveu. O que vazou entra no peso com taxa zero, e os pesos somam 1. -/
theorem o_fundo_e_a_media (β Hcmb : ℝ) (g : ℝ → ℝ) (N : ℝ) :
    let w := survivingWeightContrast β g N
    Hcmb = w * H0localContrast β Hcmb g N + (1 - w) * 0 ∧ w + (1 - w) = 1 := by
  intro w
  have h : w ≠ 0 := (survivingWeightContrast_pos β g N).ne'
  refine ⟨?_, by ring⟩
  have e : H0localContrast β Hcmb g N = Hcmb / w := rfl
  rw [e, mul_zero, add_zero]
  field_simp

end

end TGLExt.OIgual
