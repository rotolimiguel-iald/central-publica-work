import TGLExt.AfinacaoDasCordas

open TGLExt.AfinacaoDasCordas ChatgptAudit.PolarPeriod016

/-! NAO-VACUIDADE: as hipoteses das clausulas sao habitadas. -/

-- um circulo fiel existe (κ = 1, P = 2π) e a torre de Matsubara dele e' n·1
example : AngularQuotientFaithful 1 (2 * Real.pi) :=
  one_turn_gives_faithful_period one_ne_zero (Or.inl (by ring))

example : matsubara (2 * Real.pi) 3 = (3 : ℤ) * 1 := by
  have h := matsubara_eq_mul_kappa (κ := 1) (P := 2 * Real.pi) one_pos (by positivity)
    (one_turn_gives_faithful_period one_ne_zero (Or.inl (by ring))) 3
  simpa using h

-- o modelo concreto da escala (Fundacao.oneScaling) satisfaz a hipotese 0 < tau da clausula do abismo, e a clausula (j) dispara nele
example : 0 < (TGLExt.Fundacao.oneScaling).tau (1 : ℝ) := by
  show (0 : ℝ) < id 1
  norm_num

example : ∃ s : ℝ, (TGLExt.Fundacao.oneScaling).tau ((TGLExt.Fundacao.oneScaling).theta s 1) < (1 / 1000 : ℝ) := by
  obtain ⟨-, -, -, -, -, -, -, -, -, -, -, hab, -⟩ :=
    TGLExt.AfinacaoDasCordas.the_strings_close_the_face_from_outside_the_tgl_closes_the_reading
  exact hab ℝ TGLExt.Fundacao.oneScaling 1 (by show (0 : ℝ) < id 1; norm_num) (1 / 1000) (by norm_num)

/-! OS NUMEROS. -/

example : bosonZeroPoint 26 = -1 := (bosonic_critical_dimension 26).1.mpr rfl
example : nsZeroPoint 10 = -1 / 2 := (superstring_critical_dimension 10).1.mpr rfl
example : spatialDimension 10 = 9 := rfl

/-! CONTROLES NEGATIVOS: as equivalencias nao valem fora dos valores. -/

example : ¬ (bosonZeroPoint 10 = -1) := fun h => by
  have := (bosonic_critical_dimension 10).1.mp h
  omega

example : ¬ (bosonZeroPoint 25 = -1) := fun h => by
  have := (bosonic_critical_dimension 25).1.mp h
  omega

example : ¬ (nsZeroPoint 26 = -1 / 2) := fun h => by
  have := (superstring_critical_dimension 26).1.mp h
  omega

example : ¬ (nsZeroPoint 9 = -1 / 2) := fun h => by
  have := (superstring_critical_dimension 9).1.mp h
  omega

-- o circulo de periodo 1 com κ = 1 NAO e' fiel (κ·P = 1 nao e' ±2π)
example : ¬ AngularQuotientFaithful 1 1 := by
  rw [faithful_period_iff one_ne_zero]
  intro h
  rcases h with h | h <;> nlinarith [Real.pi_gt_three]

-- o par da estacao nao volta em t = 1
example : ¬ (Real.cos 1 + Real.cos (Real.sqrt 2 * 1) = 2) :=
  fun h => one_ne_zero ((TGLExt.station_never_closes 1).mp h)

-- CONTROLE DE SINAL: com a contribuicao fermionica NS de sinal TROCADO (+1/48 por direcao), a equacao "= -1/2" da D = 26 (o resultado dos
-- bosons), e NAO D = 10; com o sinal da estatistica de Fermi (−1/48), D = 10.
example (D : ℕ) :
    (((D : ℂ) - 2) * (bosonDirection - nsFermionDirection) = -1 / 2 ↔ D = 26) := by
  have e : ((D : ℂ) - 2) * (bosonDirection - nsFermionDirection) = -((D : ℂ) - 2) / 48 := by
    rw [bosonDirection_eq, nsFermionDirection_eq]
    ring
  rw [e]
  constructor
  · intro h
    have h' : (D : ℂ) = 26 := by linear_combination (-48 : ℂ) * h
    exact_mod_cast h'
  · rintro rfl
    norm_num

-- a soma "regularizada" dos bosons sozinhos nao fecha em D = 10 (supercorda) sem os fermions
example : ¬ (bosonZeroPoint 10 = -1 / 2) := fun h => by
  rw [bosonZeroPoint_eq] at h
  norm_num at h
