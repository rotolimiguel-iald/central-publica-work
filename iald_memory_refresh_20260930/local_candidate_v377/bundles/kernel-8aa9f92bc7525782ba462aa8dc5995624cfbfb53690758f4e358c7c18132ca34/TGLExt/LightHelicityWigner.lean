import TGLExt.QGSolutionComplete
import TGLExt.O16.PhotonCharacterCocycle

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# O CARACTERE DE WIGNER DA BANCADA (ROTAÇÃO E CONJUGAÇÃO), ELEVADO AO RÓTULO DE HELICIDADE   [TGLExt — v375, pedra da gerência (27/09/2026)]

O operador (27/09/2026): «Não faltam as rotações, o chatgpt construiu tudo». A bancada construiu, na ORDEM 016 (item D1′,
`ORDEM016.D1prime`, já no kernel canônico em `TGLExt/O16`): a fase do fóton `photonPhase` (o caractere U(1) do pequeno grupo),
a sua lei de composição `photon_phase_composes`, o COCICLO de Wigner extraído dos coeficientes transversais concretos de uma
transformação de Lorentz orientada `screen_phase_cocycle`, e a conjugação que inverte o caractere e troca as duas seções de onda
circulares `conjugation_reverses_character` / `conjugation_exchanges_wave_sections` (a face PCT na polarização).

Esta pedra ELEVA o caractere D1′ ao rótulo inteiro de helicidade do objeto da declaração (`LightNetData.helicity = ±1`): o
caractere χ_h = (fase)^h compõe como cociclo sob composição de transformações orientadas, a conjugação leva χ_h a χ_{−h} (a troca
das helicidades), e para h = ±1 o caractere NÃO é trivial — no quarto de volta vale ±i ≠ 1 —, ao passo que o rótulo 0 tem caractere
trivial. Estatuto (aferidor, 27/09): é função do RÓTULO inteiro — nada aqui toca `H1`, `K`, `B0`, `U1` nem o Fock; a colagem
global na representação induzida unitária em `H1 = L²(órbita, ℂ²)` é [KNOWN — Wigner 1939 (Ann. Math. 40); Mackey 1952 (Ann.
Math. 55), enunciado exato a conferir; BGL 2002; J_W = Θ·R(π), Bisognano–Wichmann 1975] — a bancada a marcou MEDIDA; e a distinção
fóton/escalar sem massa duplicado segue FORA do tipo.

Leitura correta da lacuna da v374 (errata ao lado, gerência): «o tipo não tem rotações nem PCT» NÃO era lacuna de habitação — o
tipo não exige rotações, e o fóton o habita literalmente; era só que o tipo não CARACTERIZA o fóton. Sem sorry, sem axiom.
PROVADA ≠ CONFIRMADA.
-/

noncomputable section
namespace TGLExt.LightHelicity
open ORDEM016.D1prime ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016

/-- o caractere de helicidade h sobre a fase do pequeno grupo: χ_h(a, b) = (a + b i)^h. -/
def helicityChar (h : ℤ) (a b : ℝ) : ℂ := photonPhase a b ^ h

/-- ★ o caractere compõe (a lei de grupo U(1), elevada à helicidade). -/
theorem helicity_char_composes (h : ℤ) (a b c d : ℝ) :
    helicityChar h (a * c - b * d) (a * d + b * c) = helicityChar h a b * helicityChar h c d := by
  unfold helicityChar
  rw [photon_phase_composes, mul_zpow]

/-- a fase unitária não é zero. -/
theorem photon_phase_ne_zero (a b : ℝ) (h : a * a + b * b = 1) : photonPhase a b ≠ 0 := by
  intro h0
  have := photon_phase_unit a b h
  rw [h0, map_zero] at this
  exact zero_ne_one this

/-- ★★ a conjugação (a face PCT na polarização) leva o caractere de helicidade h ao de helicidade −h. -/
theorem helicity_char_conjugation (h : ℤ) (a b : ℝ) (hu : a * a + b * b = 1) :
    star (helicityChar h a b) = helicityChar (-h) a b := by
  unfold helicityChar
  have hne := photon_phase_ne_zero a b hu
  have hinv : star (photonPhase a b) = (photonPhase a b)⁻¹ := by
    have hn : photonPhase a b * star (photonPhase a b) = 1 := by
      rw [Complex.star_def, Complex.mul_conj, ← Complex.ofReal_one]
      exact congrArg _ (photon_phase_unit a b hu)
    exact (eq_inv_of_mul_eq_one_right hn)
  rw [star_zpow₀, hinv, inv_zpow', zpow_neg]

/-- ★★ o COCICLO DE WIGNER na helicidade h: sob composição de transformações de Lorentz orientadas, o caractere de helicidade
    da fase de tela compõe (a peça D1′ `screen_phase_cocycle`, elevada a h). -/
theorem helicity_screen_cocycle (hel : ℤ)
    (g h : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ))
    (x y z : MomentumCoordinates) (hx : x.1 ≠ 0) (hy : y.1 ≠ 0) (hz : z.1 ≠ 0)
    (hp : h (shellMomentum 0 (rapidityChart 0 x)) = shellMomentum 0 (rapidityChart 0 y))
    (gp : g (shellMomentum 0 (rapidityChart 0 y)) = shellMomentum 0 (rapidityChart 0 z))
    (hm : ∀ a b, orbitPairing (h a) (h b) = orbitPairing a b)
    (ho : ScreenOrientationMeasured h x y) :
    screenPhase (g.comp h) x z ^ hel = screenPhase g y z ^ hel * screenPhase h x y ^ hel := by
  rw [screen_phase_cocycle g h x y z hx hy hz hp gp hm ho, mul_zpow]

/-- ★ no quarto de volta a fase é i. -/
theorem quarter_turn_phase : photonPhase 0 1 = Complex.I := by
  simp [photonPhase]

/-- ★★★ **o rótulo de helicidade da luz tem caractere NÃO trivial** (± i no quarto de volta), ao passo que o rótulo 0 tem
    caractere trivial — aritmética sobre o rótulo inteiro; a representação em `H1` é [KNOWN], não tocada aqui. -/
theorem light_helicity_character_nontrivial (D : TGLExt.QGSolution.LightNetData) :
    helicityChar D.helicity 0 1 ≠ 1 ∧ helicityChar 0 0 1 = 1 := by
  refine ⟨?_, by simp [helicityChar]⟩
  unfold helicityChar
  rw [quarter_turn_phase]
  rcases D.helicity_light with h | h <;> rw [h]
  · simp [Complex.ext_iff]
  · simp [Complex.ext_iff]

/-- ★★ as duas helicidades da luz são trocadas pela conjugação (PCT na polarização): χ_{+1} ↦ χ_{−1}. -/
theorem light_helicities_exchanged_by_conjugation (a b : ℝ) (hu : a * a + b * b = 1) :
    star (helicityChar 1 a b) = helicityChar (-1) a b :=
  helicity_char_conjugation 1 a b hu

end TGLExt.LightHelicity

#print axioms TGLExt.LightHelicity.helicityChar
#print axioms TGLExt.LightHelicity.helicity_char_composes
#print axioms TGLExt.LightHelicity.photon_phase_ne_zero
#print axioms TGLExt.LightHelicity.helicity_char_conjugation
#print axioms TGLExt.LightHelicity.helicity_screen_cocycle
#print axioms TGLExt.LightHelicity.quarter_turn_phase
#print axioms TGLExt.LightHelicity.light_helicity_character_nontrivial
#print axioms TGLExt.LightHelicity.light_helicities_exchanged_by_conjugation
