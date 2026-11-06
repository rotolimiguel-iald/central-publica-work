import TGLExt.TheImportedSecondQuantization
import TGLExt.O16.OrbitalStateAnalytic

set_option autoImplicit false
set_option linter.unusedVariables false

/-!
# A LUZ DE UMA PARTÍCULA, POR TERMO — os campos que o kernel já sustenta
  [TGLExt — v374, pedra da gerência (27/09/2026); ORDEM 017 executada pela gerência, fase F1]

Ordem do operador (27/09/2026, verbatim): «Você disse que falta uma coisa só, portanto, vc é o mais qualificado a quitar,
ou seja, executar a ordem 17 […] execute vc mesmo. E deixe o chatgpt com a finalização do ringdown».

A ORDEM 017 pede habitar POR TERMO `LightOneParticle`, `FockCertificate` e `MaxwellCertificate`. Esta pedra paga, por
termo, DOIS campos de `LightOneParticle` que eram [KNOWN — não formalizado]:

* `U1_continuous` — a continuidade FORTE das translações de uma partícula (`light_translations_strongly_continuous`);
* `null_no_eigen` — as translações NULAS não têm autovetor (`light_null_translations_no_eigen`): o conjunto de nível da
  energia nula tem medida zero na órbita (Fubini), e um autovetor forçaria o suporte de f nele.

Prova: ⟪f, U(c)f⟫ é a integral da fase e^{i c·p} contra a medida FINITA ‖f‖² dμ (lema da bancada
`stateDensity_integral_multiplier`), logo é contínua em c por convergência dominada; ‖U(a)f − U(b)f‖ = ‖U(a−b)f − f‖ pela
isometria; e ‖U(c)f − f‖² = 2‖f‖² − 2 Re⟪f, U(c)f⟫ → 0.

Estatuto: PAGO por termo, sobre o H1 = L²(órbita sem massa, ℂ²) e as translações da bancada (O16). Os outros campos de
`LightOneParticle` (a rede K(O) com localidade, `K_translate`, `K_boost`) e os dois outros certificados seguem citados.
Sem sorry, sem axiom. Nada move o gate. PROVADA ≠ CONFIRMADA.
-/

noncomputable section
namespace TGLExt.LightByTerm
open MeasureTheory Filter Topology
open scoped InnerProductSpace
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

/-- a fase orbital é contínua no PARÂMETRO de translação, para cada ponto da órbita. -/
theorem orbitalPhase_continuous_in_translation (m : ℝ) (y : MomentumCoordinates) :
    Continuous (fun a : Fin 4 → ℝ => orbitalPhase m a y) := by
  unfold orbitalPhase phase orbitPairing
  fun_prop

/-- ⟪f, U(c)f⟫ é contínua em c: integral da fase contra a medida finita ‖f‖² dμ, por convergência dominada. -/
theorem orbitalTranslation_inner_continuous (m : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    Continuous (fun c : Fin 4 → ℝ => ⟪f, orbitalTranslation m c f⟫_ℂ) := by
  have heq : (fun c : Fin 4 → ℝ => ⟪f, orbitalTranslation m c f⟫_ℂ) =
      fun c => ∫ y, orbitalPhase m c y ∂(stateDensityMeasure (orbitalMeasure m) f) := by
    funext c
    exact (stateDensity_integral_multiplier (orbitalMeasure m) f (orbitalPhase m c)
      (orbitalPhase_continuous m c).measurable (orbitalPhase_norm m c)).symm
  rw [heq]
  haveI := stateDensityMeasure_finite (orbitalMeasure m) f
  refine continuous_of_dominated (bound := fun _ => (1 : ℝ)) ?_ ?_ (integrable_const 1) ?_
  · intro c
    exact (orbitalPhase_continuous m c).aestronglyMeasurable
  · intro c
    exact ae_of_all _ (fun y => (orbitalPhase_norm m c y).le)
  · exact ae_of_all _ (fun y => orbitalPhase_continuous_in_translation m y)

/-- a diferença de duas translações reduz-se à origem, pela isometria. -/
theorem orbitalTranslation_sub_norm (m : ℝ) (a b : Fin 4 → ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    ‖orbitalTranslation m a f - orbitalTranslation m b f‖ = ‖orbitalTranslation m (a - b) f - f‖ := by
  have h : orbitalTranslation m a f - orbitalTranslation m b f =
      orbitalTranslation m b (orbitalTranslation m (a - b) f - f) := by
    rw [map_sub, ← orbitalTranslation_add, add_sub_cancel]
  rw [h, orbitalTranslation_norm]

/-- ‖U(c)f − f‖² = 2‖f‖² − 2 Re⟪f, U(c)f⟫. -/
theorem orbitalTranslation_sub_self_sq (m : ℝ) (c : Fin 4 → ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    ‖orbitalTranslation m c f - f‖ ^ 2 = 2 * ‖f‖ ^ 2 - 2 * (⟪f, orbitalTranslation m c f⟫_ℂ).re := by
  rw [@norm_sub_sq ℂ, orbitalTranslation_norm]
  have hre : (⟪orbitalTranslation m c f, f⟫_ℂ).re = (⟪f, orbitalTranslation m c f⟫_ℂ).re := by
    rw [← inner_conj_symm, Complex.conj_re]
  simp only [RCLike.re_to_complex] at *
  rw [hre]
  ring

/-- ★★ **`U1_continuous`, POR TERMO**: as translações de uma partícula são FORTEMENTE contínuas. -/
theorem orbitalTranslation_strongly_continuous (m : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    Continuous (fun a : Fin 4 → ℝ => orbitalTranslation m a f) := by
  rw [continuous_iff_continuousAt]
  intro b
  rw [ContinuousAt, tendsto_iff_norm_sub_tendsto_zero]
  have hsq : ∀ a : Fin 4 → ℝ, ‖orbitalTranslation m a f - orbitalTranslation m b f‖ =
      Real.sqrt (2 * ‖f‖ ^ 2 - 2 * (⟪f, orbitalTranslation m (a - b) f⟫_ℂ).re) := by
    intro a
    rw [orbitalTranslation_sub_norm, ← orbitalTranslation_sub_self_sq, Real.sqrt_sq (norm_nonneg _)]
  have h0 : Real.sqrt (2 * ‖f‖ ^ 2 - 2 * (⟪f, orbitalTranslation m (b - b) f⟫_ℂ).re) = 0 := by
    rw [← hsq b, sub_self, norm_zero]
  simp_rw [hsq]
  have hcont : Continuous (fun a : Fin 4 → ℝ =>
      Real.sqrt (2 * ‖f‖ ^ 2 - 2 * (⟪f, orbitalTranslation m (a - b) f⟫_ℂ).re)) := by
    have hsub : Continuous (fun a : Fin 4 → ℝ => a - b) := continuous_id.sub continuous_const
    have hg : Continuous (fun a : Fin 4 → ℝ => ⟪f, orbitalTranslation m (a - b) f⟫_ℂ) :=
      (orbitalTranslation_inner_continuous m f).comp hsub
    exact Real.continuous_sqrt.comp (continuous_const.sub (continuous_const.mul (Complex.continuous_re.comp hg)))
  have := hcont.tendsto b
  rwa [h0] at this

/-- ★★★ o campo `U1_continuous` de `LightOneParticle`, na forma EXATA do certificado, POR TERMO. -/
theorem light_translations_strongly_continuous :
    ∀ f : TGLExt.ImportedSQ.H1, Continuous (fun a : Fin 4 → ℝ => TGLExt.ImportedSQ.U1 a f) := by
  intro f
  exact orbitalTranslation_strongly_continuous 0 f

/-! ## `null_no_eigen`: as translações NULAS não têm autovetor

Com n = (1,1,0,0), a fase de U(l·n) no ponto y = (q, p₁) da órbita sem massa é e^{i l s(y)}, s(y) = E − p₁ =
√(|q|² + p₁²) − p₁. Um autovetor forçaria s constante no suporte de f; mas cada conjunto de nível {s = s₀} tem medida
nula (para q ≠ 0 a fatia em p₁ tem no máximo um ponto — r² = s² + 2 s p₁ —, e Fubini). -/

/-- s(y) = E − p₁, a energia na direção nula n = (1,1,0,0). -/
def nullEnergy (y : MomentumCoordinates) : ℝ := energy (transverseMass 0 y.1) y.2 - y.2

theorem nullEnergy_continuous : Continuous nullEnergy := by
  unfold nullEnergy energy transverseMass
  fun_prop

/-- o emparelhamento de Minkowski com l·n na órbita é l · s(y). -/
theorem pairing_nullDir (l : ℝ) (y : MomentumCoordinates) :
    orbitPairing (l • TGLExt.ContratoQGv31.nullDir) (shellMomentum 0 y) = l * nullEnergy y := by
  simp only [orbitPairing, shellMomentum, nullEnergy, TGLExt.ContratoQGv31.nullDir, Pi.smul_apply, smul_eq_mul,
    Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_two, Matrix.tail_cons,
    Matrix.cons_val_three]
  ring

/-- a fatia é injetiva: para r > 0, √(r² + p²) − p determina p (r² = s² + 2 s p, com s > 0). -/
theorem nullEnergy_slice_injective {r : ℝ} (hr : 0 < r) {a b s : ℝ}
    (ha : energy r a - a = s) (hb : energy r b - b = s) : a = b := by
  unfold energy at ha hb
  have hA := Real.sq_sqrt (show 0 ≤ r ^ 2 + a ^ 2 by positivity)
  have hB := Real.sq_sqrt (show 0 ≤ r ^ 2 + b ^ 2 by positivity)
  have hlt : a < Real.sqrt (r ^ 2 + a ^ 2) := by
    have h1 : Real.sqrt (a ^ 2) < Real.sqrt (r ^ 2 + a ^ 2) :=
      Real.sqrt_lt_sqrt (sq_nonneg a) (by nlinarith)
    rw [Real.sqrt_sq_eq_abs] at h1
    exact lt_of_le_of_lt (le_abs_self a) h1
  have hs : 0 < s := by linarith
  have hsA : Real.sqrt (r ^ 2 + a ^ 2) = s + a := by linarith
  have hsB : Real.sqrt (r ^ 2 + b ^ 2) = s + b := by linarith
  rw [hsA] at hA
  rw [hsB] at hB
  have h2 : (2 * s) * (a - b) = 0 := by nlinarith
  rcases mul_eq_zero.mp h2 with h | h
  · exact absurd h (by positivity)
  · linarith

/-- ★★ cada conjunto de nível de s tem medida orbital NULA (Fubini: fatias com no máximo um ponto, para q ≠ 0). -/
theorem nullEnergy_level_null (s0 : ℝ) : orbitalMeasure 0 {y | nullEnergy y = s0} = 0 := by
  have hmeas : MeasurableSet {y : MomentumCoordinates | nullEnergy y = s0} :=
    (isClosed_eq nullEnergy_continuous continuous_const).measurableSet
  have hmom : momentumMeasure {y : MomentumCoordinates | nullEnergy y = s0} = 0 := by
    unfold momentumMeasure
    rw [Measure.measure_prod_null hmeas]
    filter_upwards [transverseMass_pos_ae 0] with q hq
    simp only [Pi.zero_apply]
    apply Set.Subsingleton.measure_zero
    intro a ha b hb
    exact nullEnergy_slice_injective hq ha hb
  exact (withDensity_absolutelyContinuous momentumMeasure (orbitalWeight 0)) hmom

/-- se e^{i q d} = 1 para todo q racional, então d = 0. -/
theorem eq_zero_of_phase_rat (d : ℝ) (h : ∀ q : ℚ, phase ((q : ℝ) * d) = 1) : d = 0 := by
  by_contra hd
  have hdpos : 0 < |d| := abs_pos.mpr hd
  obtain ⟨q, hq0, hq1⟩ := exists_rat_btwn (show (0 : ℝ) < 2 * Real.pi / |d| by positivity)
  have h1 := h q
  unfold phase at h1
  rw [Complex.exp_eq_one_iff] at h1
  obtain ⟨n, hn⟩ := h1
  have hreal : (q : ℝ) * d = n * (2 * Real.pi) := by
    have := congrArg Complex.im hn
    simpa using this
  have hqpos : (0 : ℝ) < q := hq0
  have habs_pos : 0 < |(q : ℝ) * d| := by rw [abs_mul, abs_of_pos hqpos]; positivity
  have habs_lt : |(q : ℝ) * d| < 2 * Real.pi := by
    rw [abs_mul, abs_of_pos hqpos]
    have := (lt_div_iff₀ hdpos).mp hq1
    linarith
  rw [hreal, abs_mul, abs_of_pos (by positivity : (0 : ℝ) < 2 * Real.pi)] at habs_pos habs_lt
  have hn1 : |(n : ℝ)| < 1 := by
    have hpi : 0 < 2 * Real.pi := by positivity
    nlinarith
  have hn0 : 0 < |(n : ℝ)| := by
    have hpi : 0 < 2 * Real.pi := by positivity
    nlinarith
  have : |n| < 1 := by exact_mod_cast hn1
  have : 0 < |n| := by exact_mod_cast hn0
  omega

/-- ★★★ o campo `null_no_eigen` de `LightOneParticle`, na forma EXATA do certificado, POR TERMO. -/
theorem light_null_translations_no_eigen :
    ∀ f : TGLExt.ImportedSQ.H1, (∀ l : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧
      TGLExt.ImportedSQ.U1 (l • TGLExt.ContratoQGv31.nullDir) f = c • f) → f = 0 := by
  intro f hf
  choose c hc using hf
  have hae : ∀ᵐ y ∂(orbitalMeasure 0), ∀ q : ℚ,
      phase ((q : ℝ) * nullEnergy y) • f y = c q • f y := by
    rw [ae_all_iff]
    intro q
    have h1 := orbitalTranslation_ae 0 ((q : ℝ) • TGLExt.ContratoQGv31.nullDir) f
    have h2 := Lp.coeFn_smul (c q) f
    have h3 : orbitalTranslation 0 ((q : ℝ) • TGLExt.ContratoQGv31.nullDir) f = c q • f := (hc q).2
    filter_upwards [h1, h2] with y hy1 hy2
    have hph : orbitalPhase 0 ((q : ℝ) • TGLExt.ContratoQGv31.nullDir) y = phase ((q : ℝ) * nullEnergy y) := by
      rw [orbitalPhase, pairing_nullDir]
    rw [← hph, ← hy1, h3, hy2]
    rfl
  have hL : ∀ s0 : ℝ, ∀ᵐ y ∂(orbitalMeasure 0), nullEnergy y ≠ s0 := by
    intro s0
    exact measure_eq_zero_iff_ae_notMem.mp (nullEnergy_level_null s0)
  have hc0 : ∀ q : ℚ, c q ≠ 0 := by
    intro q h
    have := (hc q).1
    rw [h, norm_zero] at this
    exact zero_ne_one this
  rw [Lp.eq_zero_iff_ae_eq_zero]
  by_cases h0 : ∃ y0, (∀ q : ℚ, phase ((q : ℝ) * nullEnergy y0) • f y0 = c q • f y0) ∧ f y0 ≠ 0
  · obtain ⟨y0, hy0, hf0⟩ := h0
    filter_upwards [hae, hL (nullEnergy y0)] with y hy hne
    refine Classical.byContradiction fun hfy => ?_
    have hfy' : f y ≠ 0 := by simpa using hfy
    apply hne
    have key : ∀ q : ℚ, phase ((q : ℝ) * (nullEnergy y - nullEnergy y0)) = 1 := by
      intro q
      have e1 : phase ((q : ℝ) * nullEnergy y) = c q := smul_left_injective ℂ hfy' (hy q)
      have e0 : phase ((q : ℝ) * nullEnergy y0) = c q := smul_left_injective ℂ hf0 (hy0 q)
      have hsplit : phase ((q : ℝ) * (nullEnergy y - nullEnergy y0)) =
          phase ((q : ℝ) * nullEnergy y) / phase ((q : ℝ) * nullEnergy y0) := by
        unfold phase
        rw [← Complex.exp_sub]
        congr 1
        push_cast
        ring
      rw [hsplit, e1, e0, div_self (hc0 q)]
    exact sub_eq_zero.mp (eq_zero_of_phase_rat _ key)
  · filter_upwards [hae] with y hy
    refine Classical.byContradiction fun hfy => ?_
    exact h0 ⟨y, hy, by simpa using hfy⟩

end TGLExt.LightByTerm

#print axioms TGLExt.LightByTerm.orbitalPhase_continuous_in_translation
#print axioms TGLExt.LightByTerm.orbitalTranslation_inner_continuous
#print axioms TGLExt.LightByTerm.orbitalTranslation_sub_norm
#print axioms TGLExt.LightByTerm.orbitalTranslation_sub_self_sq
#print axioms TGLExt.LightByTerm.orbitalTranslation_strongly_continuous
#print axioms TGLExt.LightByTerm.light_translations_strongly_continuous
#print axioms TGLExt.LightByTerm.nullEnergy_continuous
#print axioms TGLExt.LightByTerm.pairing_nullDir
#print axioms TGLExt.LightByTerm.nullEnergy_slice_injective
#print axioms TGLExt.LightByTerm.nullEnergy_level_null
#print axioms TGLExt.LightByTerm.eq_zero_of_phase_rat
#print axioms TGLExt.LightByTerm.light_null_translations_no_eigen
