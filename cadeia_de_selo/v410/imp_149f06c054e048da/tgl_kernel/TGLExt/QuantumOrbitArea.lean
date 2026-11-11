-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_052 (06-07/09/2026), transposta em 07/09/2026
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
import TGLExt.LocalHorizontalPauli
import TGLExt.ModularHorizontalRotation
import TGLExt.HorizontalAreaSelection

set_option autoImplicit false
set_option maxHeartbeats 1400000

namespace ChatgptAudit.Orbit052
open TGLExt ChatgptAudit ChatgptAudit.Observable035 ChatgptAudit.Area045
noncomputable section

theorem quantum_horizontal_re_pairing (P : SiteProfile) (u v : OrbitPlane) :
    (omegaState P (star (pauliHorizontal P u) * pauliHorizontal P v)).re =
      orbitDotForm u v :=
  pauli_horizontal_re_pairing P u v

theorem quantum_horizontal_im_pairing (P : SiteProfile) (u v : OrbitPlane) :
    (omegaState P (star (pauliHorizontal P u) * pauliHorizontal P v)).im =
      orbitSymplectic (2 * P.w 0 - 1) u v :=
  pauli_horizontal_im_pairing P u v

theorem quantum_horizontal_quarter_action (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2)
    (v : OrbitPlane) :
    adT (modularHorizon P (modularQuarterTurnTime P)) (pauliHorizontal P v) =
      pauliHorizontal P (orbitQuarterTurn v) := by
  have hx := modular_quarter_horizon_x P hp
  have hy := modular_quarter_horizon_y P hp
  rw [adT_modularHorizon] at hx hy ⊢
  simp only [pauliHorizontal, map_add, map_smul, hx, hy]
  simp [orbitQuarterTurn, neg_smul, smul_neg]
  abel

theorem quantum_horizontal_oriented_action (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2)
    (v : OrbitPlane) :
    adT (modularHorizon P (modularOrientedQuarterTime P)) (pauliHorizontal P v) =
      pauliHorizontal P (orbitOrientedTurn (2 * P.w 0 - 1) v) := by
  have hx := modular_oriented_horizon_x P hp
  have hy := modular_oriented_horizon_y P hp
  rw [adT_modularHorizon] at hx hy ⊢
  simp only [pauliHorizontal, map_add, map_smul, hx, hy]
  have hr : 2 * P.w 0 - 1 ≠ 0 := by intro h; apply hp; linarith
  rcases Real.sign_apply_eq_of_ne_zero (2 * P.w 0 - 1) hr with hs | hs
  · simp [hs, orbitOrientedTurn, orbitQuarterTurn, neg_smul, smul_neg]
    abel
  · simp [hs, orbitOrientedTurn, orbitQuarterTurn, neg_smul, smul_neg]
    abel

theorem quantum_horizontal_tracial_action (P : SiteProfile) (hp : P.w 0 = 1 / 2)
    (t : ℝ) (v : OrbitPlane) :
    adT (modularHorizon P t) (pauliHorizontal P v) = pauliHorizontal P v := by
  have hx := modular_horizon_pauli_x_tracial P hp t
  have hy := modular_horizon_pauli_y_tracial P hp t
  rw [adT_modularHorizon] at hx hy ⊢
  simp only [pauliHorizontal, map_add, map_smul, hx, hy]

theorem quantum_orbit_asymmetry_ne_zero (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    2 * P.w 0 - 1 ≠ 0 := by
  intro h
  apply hp
  linarith

/-- The calibration is evaluated on the actual horizon and actual state of the tower. -/
def quantumOrbitPairing (P : SiteProfile) (u v : OrbitPlane) : ℝ :=
  (omegaState P (star (pauliHorizontal P u) *
    adT (modularHorizon P (modularOrientedQuarterTime P)) (pauliHorizontal P v))).im

theorem quantum_orbit_pairing_eq (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2)
    (u v : OrbitPlane) :
    quantumOrbitPairing P u v = orbitCalibratedForm (2 * P.w 0 - 1) u v := by
  unfold quantumOrbitPairing
  rw [quantum_horizontal_oriented_action P hp, quantum_horizontal_im_pairing,
    orbit_calibration_identity]

/-- Bilinearity is proved for the state-and-horizon expression, not postulated. -/
def quantumOrbitForm (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    OrbitPlane →ₗ[ℝ] OrbitPlane →ₗ[ℝ] ℝ where
  toFun u :=
    { toFun := quantumOrbitPairing P u
      map_add' := by
        intro v w
        simp only [quantum_orbit_pairing_eq P hp, map_add]
      map_smul' := by
        intro a v
        simp only [quantum_orbit_pairing_eq P hp, map_smul, RingHom.id_apply] }
  map_add' := by
    intro u v
    apply LinearMap.ext
    intro w
    change quantumOrbitPairing P (u + v) w =
      quantumOrbitPairing P u w + quantumOrbitPairing P v w
    simp only [quantum_orbit_pairing_eq P hp, map_add, LinearMap.add_apply]
  map_smul' := by
    intro a u
    apply LinearMap.ext
    intro v
    change quantumOrbitPairing P (a • u) v = a • quantumOrbitPairing P u v
    simp only [quantum_orbit_pairing_eq P hp, map_smul, LinearMap.smul_apply]

theorem quantum_orbit_form_apply (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2)
    (u v : OrbitPlane) :
    quantumOrbitForm P hp u v =
      (omegaState P (star (pauliHorizontal P u) *
        adT (modularHorizon P (modularOrientedQuarterTime P))
          (pauliHorizontal P v))).im := rfl

theorem quantum_orbit_form_eq (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    quantumOrbitForm P hp = orbitCalibratedForm (2 * P.w 0 - 1) := by
  apply LinearMap.ext
  intro u
  apply LinearMap.ext
  intro v
  exact quantum_orbit_pairing_eq P hp u v

theorem quantum_orbit_form_symmetric (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    FormSymmetric (quantumOrbitForm P hp) := by
  rw [quantum_orbit_form_eq]
  exact orbit_calibrated_symmetric _

theorem quantum_orbit_form_positive (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    FormPositive (quantumOrbitForm P hp) := by
  rw [quantum_orbit_form_eq]
  exact orbit_calibrated_positive _ (quantum_orbit_asymmetry_ne_zero P hp)

theorem quantum_orbit_form_nondegenerate (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2)
    (u : OrbitPlane) (h : ∀ v, quantumOrbitForm P hp u v = 0) : u = 0 := by
  by_contra hu
  have hpos := quantum_orbit_form_positive P hp u hu
  rw [h u] at hpos
  exact (lt_irrefl 0) hpos

theorem quantum_orbit_form_area (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    formArea (quantumOrbitForm P hp) orbitBasisX orbitBasisY = |2 * P.w 0 - 1| := by
  rw [quantum_orbit_form_eq]
  exact orbit_calibrated_area _

theorem quantum_orbit_form_trace (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    quantumOrbitForm P hp orbitBasisX orbitBasisX +
      quantumOrbitForm P hp orbitBasisY orbitBasisY = 2 * |2 * P.w 0 - 1| := by
  rw [quantum_orbit_form_eq]
  exact orbit_selected_trace_in_orthonormal_pair _ _ _
    (by norm_num [orbitDotForm, orbitBasisX])
    (by norm_num [orbitDotForm, orbitBasisY])

/-- The local modular action is identity here; only its imaginary pairing degenerates. -/
theorem quantum_orbit_pairing_tracial (P : SiteProfile) (hp : P.w 0 = 1 / 2)
    (u v : OrbitPlane) : quantumOrbitPairing P u v = 0 := by
  unfold quantumOrbitPairing
  rw [quantum_horizontal_tracial_action P hp, quantum_horizontal_im_pairing]
  simp [orbitSymplectic, hp]

theorem quantum_orbit_directions_effective (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2)
    (u : OrbitPlane) (hu : u ≠ 0) :
    horizontalResponse P u ≠ horizontalResponse P 0 := by
  intro h
  exact hu (horizontal_response_injective P hp h)

/-- Positive calibrated length is attached to distinguishable derivatives of state readings. -/
theorem quantum_orbit_effective_positive (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2)
    (u : OrbitPlane) (hu : u ≠ 0) :
    0 < quantumOrbitForm P hp u u ∧
      horizontalResponse P u ≠ horizontalResponse P 0 :=
  ⟨quantum_orbit_form_positive P hp u hu, quantum_orbit_directions_effective P hp u hu⟩

theorem quantum_centralizer_imaginary_zero (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ omegaCentralizer P) (hAsa : IsSelfAdjoint A)
    (hB : B ∈ theFactorObject P) (hBsa : IsSelfAdjoint B) :
    (omegaState P (star A * B)).im = 0 := by
  rw [hAsa.star_eq]
  apply Complex.conj_eq_iff_im.mp
  change star (omegaState P (A * B)) = omegaState P (A * B)
  rw [← ChatgptAudit.Expectation047.omega_state_star, star_mul,
    hBsa.star_eq, hAsa.star_eq]
  exact (hA.2 B hB).symm

/-- This is the density on the normalized Pauli pair, not the area of another screen. -/
theorem quantum_orbit_third_reference_area :
    formArea (quantumOrbitForm ChatgptAudit.Thermal025.thirdThermalReference
      (by norm_num [ChatgptAudit.Thermal025.thirdThermalReference]))
      orbitBasisX orbitBasisY = 1 / 3 := by
  rw [quantum_orbit_form_area]
  norm_num [ChatgptAudit.Thermal025.thirdThermalReference]

section Selection

variable (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2)
variable (F : (TowerHilbert P →L[ℂ] TowerHilbert P) →
  (TowerHilbert P →L[ℂ] TowerHilbert P) → ℝ)
variable (b : OrbitPlane →ₗ[ℝ] OrbitPlane →ₗ[ℝ] ℝ)
variable (hrepr : ∀ u v, b u v = F (pauliHorizontal P u) (pauliHorizontal P v))
variable (hinv : ∀ u v,
  F (adT (modularHorizon P (modularQuarterTurnTime P)) (pauliHorizontal P u))
    (adT (modularHorizon P (modularQuarterTurnTime P)) (pauliHorizontal P v)) =
  F (pauliHorizontal P u) (pauliHorizontal P v))

include hp hrepr hinv

/-- The invariance hypothesis mentions the actual horizon before passing to coordinates. -/
theorem quantum_candidate_quarter_invariant :
    ∀ u v, b (orbitQuarterTurn u) (orbitQuarterTurn v) = b u v := by
  intro u v
  rw [hrepr, hrepr, ← quantum_horizontal_quarter_action P hp u,
    ← quantum_horizontal_quarter_action P hp v]
  exact hinv u v

theorem quantum_candidate_isotropic (hsym : FormSymmetric b) :
    b = b orbitBasisX orbitBasisX • orbitDotForm :=
  orbit_quarter_invariant_form b hsym
    (quantum_candidate_quarter_invariant P hp F b hrepr hinv)

/-- Isotropy is relative to the real GNS pairing of the same tower state. -/
theorem quantum_candidate_gns_restriction (hsym : FormSymmetric b) (u v : OrbitPlane) :
    F (pauliHorizontal P u) (pauliHorizontal P v) =
      F (sitePauliX P 0) (sitePauliX P 0) *
        (omegaState P (star (pauliHorizontal P u) * pauliHorizontal P v)).re := by
  rw [quantum_horizontal_re_pairing]
  have hc : b orbitBasisX orbitBasisX = F (sitePauliX P 0) (sitePauliX P 0) := by
    simpa only [orbitBasisX, pauli_horizontal_basis_x] using hrepr orbitBasisX orbitBasisX
  calc
    F (pauliHorizontal P u) (pauliHorizontal P v) = b u v := (hrepr u v).symm
    _ = (b orbitBasisX orbitBasisX • orbitDotForm) u v :=
      congrArg (fun q : OrbitPlane →ₗ[ℝ] OrbitPlane →ₗ[ℝ] ℝ => q u v)
        (quantum_candidate_isotropic P hp F b hrepr hinv hsym)
    _ = F (sitePauliX P 0) (sitePauliX P 0) * orbitDotForm u v := by
      change b orbitBasisX orbitBasisX * orbitDotForm u v = _
      rw [hc]

/-- Trace is measured on the existing GNS orthonormal Pauli pair. -/
theorem quantum_candidate_trace_one (hsym : FormSymmetric b)
    (htrace : F (sitePauliX P 0) (sitePauliX P 0) +
      F (sitePauliY P 0) (sitePauliY P 0) = 1) :
    b = (1 / 2 : ℝ) • orbitDotForm := by
  apply orbit_trace_one_selection b hsym
    (quantum_candidate_quarter_invariant P hp F b hrepr hinv)
  simpa only [hrepr, orbitBasisX, orbitBasisY,
    pauli_horizontal_basis_x, pauli_horizontal_basis_y] using htrace

theorem quantum_candidate_trace_one_area (hsym : FormSymmetric b)
    (htrace : F (sitePauliX P 0) (sitePauliX P 0) +
      F (sitePauliY P 0) (sitePauliY P 0) = 1) :
    formArea b orbitBasisX orbitBasisY = 1 / 2 := by
  rw [quantum_candidate_trace_one P hp F b hrepr hinv hsym htrace]
  exact orbit_scalar_area (1 / 2) (by norm_num)

end Selection

#print axioms quantum_horizontal_re_pairing
#print axioms quantum_horizontal_im_pairing
#print axioms quantum_horizontal_quarter_action
#print axioms quantum_horizontal_oriented_action
#print axioms quantum_horizontal_tracial_action
#print axioms quantum_orbit_asymmetry_ne_zero
#print axioms quantumOrbitPairing
#print axioms quantum_orbit_pairing_eq
#print axioms quantumOrbitForm
#print axioms quantum_orbit_form_apply
#print axioms quantum_orbit_form_eq
#print axioms quantum_orbit_form_symmetric
#print axioms quantum_orbit_form_positive
#print axioms quantum_orbit_form_nondegenerate
#print axioms quantum_orbit_form_area
#print axioms quantum_orbit_form_trace
#print axioms quantum_orbit_pairing_tracial
#print axioms quantum_orbit_directions_effective
#print axioms quantum_orbit_effective_positive
#print axioms quantum_centralizer_imaginary_zero
#print axioms quantum_orbit_third_reference_area
#print axioms quantum_candidate_quarter_invariant
#print axioms quantum_candidate_isotropic
#print axioms quantum_candidate_gns_restriction
#print axioms quantum_candidate_trace_one
#print axioms quantum_candidate_trace_one_area

end
end ChatgptAudit.Orbit052
