-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_051 (06-07/09/2026), transposta em 07/09/2026
-- Lote 046..054 (ORDEM_008 cumprida; «tudo o que a bancada podia», 9 entregas, 43 modulos).
--   046: a ESPERANCA APERIODICA — aperiodicExpectationInput P : ExpectationInput P para TODO perfil da torre
--     (media de Cesaro do fluxo modular; limite forte; into/fixes/ortho); o levantamento do Lema 3 dispara para
--     todo perfil e todo horizonte (the_lift_fires_on_the_aperiodic_tower); unicidade; E comuta com sigma_t.
--   047: propriedades da esperanca — linear sobre M, preserva 1/estado/adjunto, bimodular sobre o centralizador,
--     COMPLETAMENTE POSITIVA (CompletelyPositiveMap da mathlib), contracao GNS, NORMAL (supremos positivos dirigidos).
--   048: obstrucoes da identificacao modular/geometrica — Borchers trivial sobrevive ao transporte de estado (027);
--     periodo do fluxo forca retorno de rotulos em localizacao fiel covariante; ligado ao boost 044 (negativos tipados).
--   049-050: SUBESPACO PADRAO CONTINUO em L^2 — T_c = M_exp(-c xi) positivo auto-adjunto (grafo limitado), J
--     antiunitaria, S_c = J T_c involucao fechada, K_c = Fix S_c subespaco padrao; adjunto S_c^dagger = T_c J,
--     Delta_c = S_c^dagger S_c = T_c^2 = T_{2c} com igualdade de dominios, resolvente (I + Delta_c)^{-1}.
--     Identificacao T_c = Delta_c^{1/2} e BW seguem OPEN.
--   051: balanco optico finito — Q - K DeltaA = K E com E >= 0 (integral optica), E/t^4 -> (a^2 + c^2)/12; Riccati;
--     no caso variavel o drift Z_R(s) - s R(s) persiste (controles).
--   052: setor horizontal (plano de Pauli X,Y do 1o sitio) — a esperanca centralizante zera as duas direcoes;
--     o horizonte modular faz o quarto de volta; forma invariante = c x produto GNS real; [INPUT] traco relativo = 1
--     fixa c = 1/2 (densidade de area 1/2); forma efetiva de densidade |2p - 1|. Escala livre sem calibracao por Omega.
--   053: polarizador D = P_R(-i)P_R no Hilbert real; acao GNS de todo TowerHorizon preserva Omega e entrelaca D;
--     radical = centralizador (setor auto-adjunto); CONTRAEXEMPLO: covariancia + calibracao comum NAO da unicidade
--     da area (9/10 vs 1377/1250 no 2o par).
--   054: custo modular do polarizador C_D(x) = sum 2||D^(n+1)x||^2/(2n+1): l.s.c., preservado por todo TowerHorizon,
--     custo zero <=> centralizador; f(0)=0, f(0)=2 localModularCost; C_D(X_1 Omega) = log2/3 na referencia p = 1/3.
--   Estatuto: [REAL] o que esta compilado; [INPUT] calibracao por Omega, traco relativo = 1; [OPEN] H3, selecao
--   fisica da area, escala dimensional, regiao <-> algebra, BW/identificacao T_c = Delta^{1/2}, reconstrucao geral.
-- Auditoria da gerencia (sessao d554e796, 07/09/2026): hashes 185/185 (9 entregas); 9/9 auditores exit 0;
--   recompilacao INDEPENDENTE 43/43, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Analysis.Convex.Basic
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Tactic

set_option autoImplicit false

namespace ChatgptAudit.Optical051
open MeasureTheory Set
noncomputable section

/-- The oriented primitive with base point zero. -/
def opticalPrimitive (f : ℝ → ℝ) (t : ℝ) : ℝ :=
  ∫ s in 0..t, f s

/-- The optical correction, defined independently of heat and entropy. -/
def opticalVolterraCorrection (A F : ℝ → ℝ) (t : ℝ) : ℝ :=
  ∫ s in 0..t, A s * opticalPrimitive F s

/-- Ricci variation remaining even when matter agrees pointwise with Ricci. -/
def opticalCurvatureDrift (R : ℝ → ℝ) (t : ℝ) : ℝ :=
  opticalPrimitive R t - t * R t

theorem optical_primitive_zero (f : ℝ → ℝ) : opticalPrimitive f 0 = 0 := by
  simp [opticalPrimitive]

theorem optical_primitive_const (r t : ℝ) :
    opticalPrimitive (fun _ => r) t = t * r := by
  simp [opticalPrimitive]

theorem optical_primitive_intervalIntegrable (I : Set ℝ) (hI : Convex ℝ I)
    (h0 : 0 ∈ I) (f : ℝ → ℝ) (hf : ContinuousOn f I) (t : ℝ) (ht : t ∈ I) :
    IntervalIntegrable f volume 0 t :=
  (hf.mono (hI.ordConnected.uIcc_subset h0 ht)).intervalIntegrable

theorem optical_primitive_hasDerivAt (I : Set ℝ) (ho : IsOpen I) (hI : Convex ℝ I)
    (h0 : 0 ∈ I) (f : ℝ → ℝ) (hf : ContinuousOn f I) (t : ℝ) (ht : t ∈ I) :
    HasDerivAt (opticalPrimitive f) (f t) t := by
  exact intervalIntegral.integral_hasDerivAt_right
    (optical_primitive_intervalIntegrable I hI h0 f hf t ht)
    (ContinuousOn.stronglyMeasurableAtFilter ho hf t ht)
    ((hf t ht).continuousAt (ho.mem_nhds ht))

theorem optical_primitive_continuousOn (I : Set ℝ) (ho : IsOpen I) (hI : Convex ℝ I)
    (h0 : 0 ∈ I) (f : ℝ → ℝ) (hf : ContinuousOn f I) :
    ContinuousOn (opticalPrimitive f) I := by
  intro t ht
  exact (optical_primitive_hasDerivAt I ho hI h0 f hf t ht).continuousAt.continuousWithinAt

/-- Integrating Raychaudhuri with zero initial expansion, in either time direction. -/
theorem optical_expansion_integral (I : Set ℝ) (hI : Convex ℝ I) (h0 : 0 ∈ I)
    (theta R F : ℝ → ℝ) (hR : ContinuousOn R I) (hF : ContinuousOn F I)
    (htheta : ∀ s ∈ I, HasDerivAt theta (-R s - F s) s)
    (htheta0 : theta 0 = 0) (t : ℝ) (ht : t ∈ I) :
    theta t = -opticalPrimitive R t - opticalPrimitive F t := by
  have hRi := optical_primitive_intervalIntegrable I hI h0 R hR t ht
  have hFi := optical_primitive_intervalIntegrable I hI h0 F hF t ht
  have hFTC := intervalIntegral.integral_eq_sub_of_hasDerivAt
    (fun s hs => htheta s (hI.ordConnected.uIcc_subset h0 ht hs)) (hRi.neg.sub hFi)
  calc
    theta t = ∫ s in 0..t, -R s - F s := by
      simpa only [htheta0, sub_zero] using hFTC.symm
    _ = -opticalPrimitive R t - opticalPrimitive F t := by
      rw [intervalIntegral.integral_sub (f := fun s => -R s) (g := F) hRi.neg hFi,
        intervalIntegral.integral_neg]
      rfl

/-- The exact finite balance, including variable Ricci and matter data. -/
theorem optical_volterra_balance (I : Set ℝ) (ho : IsOpen I) (hI : Convex ℝ I)
    (h0 : 0 ∈ I) (A theta R F M Q : ℝ → ℝ) (K : ℝ)
    (hR : ContinuousOn R I) (hF : ContinuousOn F I) (hM : ContinuousOn M I)
    (hA : ∀ s ∈ I, HasDerivAt A (A s * theta s) s)
    (htheta : ∀ s ∈ I, HasDerivAt theta (-R s - F s) s)
    (htheta0 : theta 0 = 0)
    (hQ : ∀ s ∈ I, HasDerivAt Q (-K * s * M s * A s) s)
    (hQ0 : Q 0 = 0) (t : ℝ) (ht : t ∈ I) :
    Q t - K * (A t - A 0) =
      K * ∫ s in 0..t, A s *
        (opticalPrimitive F s + opticalPrimitive R s - s * M s) := by
  have hAc : ContinuousOn A I := fun s hs =>
    (hA s hs).continuousAt.continuousWithinAt
  have hRc := optical_primitive_continuousOn I ho hI h0 R hR
  have hFc := optical_primitive_continuousOn I ho hI h0 F hF
  have hgc : ContinuousOn
      (fun s => K * (A s * (opticalPrimitive F s + opticalPrimitive R s - s * M s))) I :=
    continuousOn_const.mul (hAc.mul ((hFc.add hRc).sub (continuousOn_id.mul hM)))
  have hd : ∀ s ∈ uIcc 0 t,
      HasDerivAt (fun u => Q u - K * (A u - A 0))
        (K * (A s * (opticalPrimitive F s + opticalPrimitive R s - s * M s))) s := by
    intro s hs
    have hsI := hI.ordConnected.uIcc_subset h0 ht hs
    have he := (hQ s hsI).sub (((hA s hsI).sub_const (A 0)).const_mul K)
    convert he using 1
    all_goals first
      | rfl
      | (rw [optical_expansion_integral I hI h0 theta R F hR hF htheta htheta0 s hsI]; ring)
  have hFTC := intervalIntegral.integral_eq_sub_of_hasDerivAt hd
    ((hgc.mono (hI.ordConnected.uIcc_subset h0 ht)).intervalIntegrable)
  rw [intervalIntegral.integral_const_mul] at hFTC
  simpa only [hQ0, sub_self, mul_zero, sub_zero] using hFTC.symm

/-- Pointwise Ricci--matter matching retains a curvature variation term. -/
theorem optical_volterra_balance_matched (I : Set ℝ) (ho : IsOpen I) (hI : Convex ℝ I)
    (h0 : 0 ∈ I) (A theta R F Q : ℝ → ℝ) (K : ℝ)
    (hR : ContinuousOn R I) (hF : ContinuousOn F I)
    (hA : ∀ s ∈ I, HasDerivAt A (A s * theta s) s)
    (htheta : ∀ s ∈ I, HasDerivAt theta (-R s - F s) s)
    (htheta0 : theta 0 = 0)
    (hQ : ∀ s ∈ I, HasDerivAt Q (-K * s * R s * A s) s)
    (hQ0 : Q 0 = 0) (t : ℝ) (ht : t ∈ I) :
    Q t - K * (A t - A 0) =
      K * ∫ s in 0..t, A s * (opticalPrimitive F s + opticalCurvatureDrift R s) := by
  simpa only [opticalCurvatureDrift, add_sub_assoc] using
    optical_volterra_balance I ho hI h0 A theta R F R Q K
      hR hF hR hA htheta htheta0 hQ hQ0 t ht

/-- Constant Ricci matching removes the drift, leaving the independently defined correction. -/
theorem optical_volterra_balance_constant (I : Set ℝ) (ho : IsOpen I) (hI : Convex ℝ I)
    (h0 : 0 ∈ I) (A theta F Q : ℝ → ℝ) (K r : ℝ)
    (hF : ContinuousOn F I)
    (hA : ∀ s ∈ I, HasDerivAt A (A s * theta s) s)
    (htheta : ∀ s ∈ I, HasDerivAt theta (-r - F s) s)
    (htheta0 : theta 0 = 0)
    (hQ : ∀ s ∈ I, HasDerivAt Q (-K * s * r * A s) s)
    (hQ0 : Q 0 = 0) (t : ℝ) (ht : t ∈ I) :
    Q t - K * (A t - A 0) = K * opticalVolterraCorrection A F t := by
  have h := optical_volterra_balance I ho hI h0 A theta (fun _ => r) F
    (fun _ => r) Q K continuousOn_const hF continuousOn_const
    hA htheta htheta0 hQ hQ0 t ht
  simpa only [optical_primitive_const, add_sub_cancel_right, opticalVolterraCorrection] using h

theorem optical_volterra_correction_zero (A F : ℝ → ℝ) :
    opticalVolterraCorrection A F 0 = 0 := by
  simp [opticalVolterraCorrection]

/-- The double orientation makes the correction nonnegative on both sides of zero. -/
theorem optical_volterra_correction_nonneg (I : Set ℝ) (hI : Convex ℝ I)
    (h0 : 0 ∈ I) (A F : ℝ → ℝ)
    (hA : ∀ s ∈ I, 0 ≤ A s) (hF : ∀ s ∈ I, 0 ≤ F s)
    (t : ℝ) (ht : t ∈ I) : 0 ≤ opticalVolterraCorrection A F t := by
  by_cases hpos : 0 ≤ t
  · apply intervalIntegral.integral_nonneg hpos
    intro s hs
    have hsI : s ∈ I := hI.ordConnected.uIcc_subset h0 ht
      (by simpa only [uIcc_of_le hpos] using hs)
    apply mul_nonneg (hA s hsI)
    apply intervalIntegral.integral_nonneg hs.1
    intro u hu
    exact hF u (hI.ordConnected.uIcc_subset h0 hsI
      (by simpa only [uIcc_of_le hs.1] using hu))
  · have hneg : t ≤ 0 := le_of_not_ge hpos
    have hinner : ∀ s ∈ Icc t 0, opticalPrimitive F s ≤ 0 := by
      intro s hs
      have hsI : s ∈ I := hI.ordConnected.uIcc_subset ht h0
        (by simpa only [uIcc_of_le hneg] using hs)
      have hp : 0 ≤ ∫ u in s..0, F u := by
        apply intervalIntegral.integral_nonneg hs.2
        intro u hu
        exact hF u (hI.ordConnected.uIcc_subset hsI h0
          (by simpa only [uIcc_of_le hs.2] using hu))
      unfold opticalPrimitive
      rw [intervalIntegral.integral_symm]
      exact neg_nonpos.mpr hp
    have hout : 0 ≤ ∫ s in t..0, -(A s * opticalPrimitive F s) := by
      apply intervalIntegral.integral_nonneg hneg
      intro s hs
      have hsI : s ∈ I := hI.ordConnected.uIcc_subset ht h0
        (by simpa only [uIcc_of_le hneg] using hs)
      exact neg_nonneg.mpr (mul_nonpos_of_nonneg_of_nonpos (hA s hsI) (hinner s hs))
    unfold opticalVolterraCorrection
    rw [intervalIntegral.integral_symm]
    simpa only [intervalIntegral.integral_neg] using hout

theorem optical_scaled_correction_nonneg (I : Set ℝ) (hI : Convex ℝ I)
    (h0 : 0 ∈ I) (A F : ℝ → ℝ)
    (hA : ∀ s ∈ I, 0 ≤ A s) (hF : ∀ s ∈ I, 0 ≤ F s)
    (K : ℝ) (hK : 0 ≤ K) (t : ℝ) (ht : t ∈ I) :
    0 ≤ K * opticalVolterraCorrection A F t :=
  mul_nonneg hK (optical_volterra_correction_nonneg I hI h0 A F hA hF t ht)

#print axioms opticalPrimitive
#print axioms opticalVolterraCorrection
#print axioms opticalCurvatureDrift
#print axioms optical_primitive_zero
#print axioms optical_primitive_const
#print axioms optical_primitive_intervalIntegrable
#print axioms optical_primitive_hasDerivAt
#print axioms optical_primitive_continuousOn
#print axioms optical_expansion_integral
#print axioms optical_volterra_balance
#print axioms optical_volterra_balance_matched
#print axioms optical_volterra_balance_constant
#print axioms optical_volterra_correction_zero
#print axioms optical_volterra_correction_nonneg
#print axioms optical_scaled_correction_nonneg

end
end ChatgptAudit.Optical051
