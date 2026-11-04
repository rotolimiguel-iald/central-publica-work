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
import TGLExt.HorizonAreaScale
import Mathlib.Data.Real.Sign
import Mathlib.Tactic

set_option autoImplicit false

namespace ChatgptAudit.Orbit052
open Matrix ChatgptAudit ChatgptAudit.Area045
noncomputable section

abbrev OrbitPlane := Fin 2 → ℝ

def orbitBasisX : OrbitPlane := ![1, 0]
def orbitBasisY : OrbitPlane := ![0, 1]

def orbitQuarterTurn : OrbitPlane →ₗ[ℝ] OrbitPlane where
  toFun v := ![-v 1, v 0]
  map_add' u v := by
    ext i
    fin_cases i
    · simp
      ring
    · simp
  map_smul' c v := by
    ext i
    fin_cases i <;> simp

def orbitDotForm : OrbitPlane →ₗ[ℝ] OrbitPlane →ₗ[ℝ] ℝ where
  toFun u :=
    { toFun := fun v => u 0 * v 0 + u 1 * v 1
      map_add' := by
        intro v w
        change u 0 * (v 0 + w 0) + u 1 * (v 1 + w 1) =
          (u 0 * v 0 + u 1 * v 1) + (u 0 * w 0 + u 1 * w 1)
        ring
      map_smul' := by
        intro c v
        change u 0 * (c * v 0) + u 1 * (c * v 1) =
          c * (u 0 * v 0 + u 1 * v 1)
        ring }
  map_add' := by
    intro u v
    apply LinearMap.ext
    intro w
    change (u 0 + v 0) * w 0 + (u 1 + v 1) * w 1 =
      (u 0 * w 0 + u 1 * w 1) + (v 0 * w 0 + v 1 * w 1)
    ring
  map_smul' := by
    intro c u
    apply LinearMap.ext
    intro v
    change (c * u 0) * v 0 + (c * u 1) * v 1 =
      c * (u 0 * v 0 + u 1 * v 1)
    ring

/-- Alternating form in the generator coordinates of one unitary orbit. -/
def orbitSymplectic (r : ℝ) (u v : OrbitPlane) : ℝ :=
  r * (u 0 * v 1 - u 1 * v 0)

def orbitOrientedTurn (r : ℝ) : OrbitPlane →ₗ[ℝ] OrbitPlane :=
  Real.sign r • orbitQuarterTurn

/-- The chosen symplectic calibration, distinct from trace-one normalization. -/
def orbitCalibratedForm (r : ℝ) : OrbitPlane →ₗ[ℝ] OrbitPlane →ₗ[ℝ] ℝ :=
  |r| • orbitDotForm

theorem orbit_basis_decomposition (u : OrbitPlane) :
    u = u 0 • orbitBasisX + u 1 • orbitBasisY := by
  ext i
  fin_cases i <;> simp [orbitBasisX, orbitBasisY]

theorem orbit_quarter_basis_x : orbitQuarterTurn orbitBasisX = orbitBasisY := by
  ext i
  fin_cases i <;> simp [orbitQuarterTurn, orbitBasisX, orbitBasisY]

theorem orbit_quarter_basis_y : orbitQuarterTurn orbitBasisY = -orbitBasisX := by
  ext i
  fin_cases i <;> simp [orbitQuarterTurn, orbitBasisX, orbitBasisY]

theorem orbit_quarter_square (u : OrbitPlane) :
    orbitQuarterTurn (orbitQuarterTurn u) = -u := by
  ext i
  fin_cases i <;> simp [orbitQuarterTurn]

theorem orbit_dot_apply (u v : OrbitPlane) :
    orbitDotForm u v = u 0 * v 0 + u 1 * v 1 := rfl

theorem orbit_bilinear_expansion
    (b : OrbitPlane →ₗ[ℝ] OrbitPlane →ₗ[ℝ] ℝ) (u v : OrbitPlane) :
    b u v =
      u 0 * v 0 * b orbitBasisX orbitBasisX +
      u 0 * v 1 * b orbitBasisX orbitBasisY +
      u 1 * v 0 * b orbitBasisY orbitBasisX +
      u 1 * v 1 * b orbitBasisY orbitBasisY := by
  conv_lhs => rw [orbit_basis_decomposition u, orbit_basis_decomposition v]
  simp only [map_add, map_smul, LinearMap.add_apply, LinearMap.smul_apply, smul_eq_mul]
  ring

/-- A real symmetric form invariant under this actual quarter turn is isotropic. -/
theorem orbit_quarter_invariant_form
    (b : OrbitPlane →ₗ[ℝ] OrbitPlane →ₗ[ℝ] ℝ)
    (hsym : FormSymmetric b)
    (hinv : ∀ u v, b (orbitQuarterTurn u) (orbitQuarterTurn v) = b u v) :
    b = b orbitBasisX orbitBasisX • orbitDotForm := by
  have hdiag : b orbitBasisY orbitBasisY = b orbitBasisX orbitBasisX := by
    simpa only [orbit_quarter_basis_x] using hinv orbitBasisX orbitBasisX
  have hc := hinv orbitBasisX orbitBasisY
  rw [orbit_quarter_basis_x, orbit_quarter_basis_y, map_neg] at hc
  have hcross : b orbitBasisX orbitBasisY = 0 := by
    rw [hsym orbitBasisY orbitBasisX] at hc
    linarith
  apply LinearMap.ext
  intro u
  apply LinearMap.ext
  intro v
  rw [orbit_bilinear_expansion b u v]
  change _ = b orbitBasisX orbitBasisX * (u 0 * v 0 + u 1 * v 1)
  rw [hdiag, hsym orbitBasisY orbitBasisX, hcross]
  ring

theorem orbit_trace_one_selection
    (b : OrbitPlane →ₗ[ℝ] OrbitPlane →ₗ[ℝ] ℝ)
    (hsym : FormSymmetric b)
    (hinv : ∀ u v, b (orbitQuarterTurn u) (orbitQuarterTurn v) = b u v)
    (htrace : b orbitBasisX orbitBasisX + b orbitBasisY orbitBasisY = 1) :
    b = (1 / 2 : ℝ) • orbitDotForm := by
  have h := orbit_quarter_invariant_form b hsym hinv
  have hdiag : b orbitBasisY orbitBasisY = b orbitBasisX orbitBasisX := by
    simpa only [orbit_quarter_basis_x] using hinv orbitBasisX orbitBasisX
  rw [hdiag] at htrace
  have hc : b orbitBasisX orbitBasisX = (1 / 2 : ℝ) := by linarith
  simpa only [hc] using h

theorem orbit_scalar_gram (c : ℝ) :
    formGram (c • orbitDotForm) orbitBasisX orbitBasisY = !![c, 0; 0, c] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [formGram, orbitDotForm, orbitBasisX, orbitBasisY]

theorem orbit_scalar_area (c : ℝ) (hc : 0 ≤ c) :
    formArea (c • orbitDotForm) orbitBasisX orbitBasisY = c := by
  rw [formArea, orbit_scalar_gram]
  change Real.sqrt ((!![c, 0; 0, c] : ScreenMatrix).det) = c
  rw [Matrix.det_fin_two]
  change Real.sqrt (c * c - 0 * 0) = c
  rw [mul_zero, sub_zero, ← pow_two, Real.sqrt_sq_eq_abs, abs_of_nonneg hc]

theorem orbit_trace_one_area
    (b : OrbitPlane →ₗ[ℝ] OrbitPlane →ₗ[ℝ] ℝ)
    (hsym : FormSymmetric b)
    (hinv : ∀ u v, b (orbitQuarterTurn u) (orbitQuarterTurn v) = b u v)
    (htrace : b orbitBasisX orbitBasisX + b orbitBasisY orbitBasisY = 1) :
    formArea b orbitBasisX orbitBasisY = 1 / 2 := by
  rw [orbit_trace_one_selection b hsym hinv htrace]
  exact orbit_scalar_area (1 / 2) (by norm_num)

/-- The diagonal sum for unit vectors; in particular for every orthonormal basis. -/
theorem orbit_selected_trace_in_orthonormal_pair (c : ℝ) (u v : OrbitPlane)
    (hu : orbitDotForm u u = 1) (hv : orbitDotForm v v = 1) :
    (c • orbitDotForm) u u + (c • orbitDotForm) v v = 2 * c := by
  change c * orbitDotForm u u + c * orbitDotForm v v = 2 * c
  rw [hu, hv]
  ring

theorem orbit_sign_times_self (r : ℝ) : Real.sign r * r = |r| := by
  rcases lt_trichotomy r 0 with h | rfl | h
  · rw [Real.sign_of_neg h, abs_of_neg h]
    ring
  · simp
  · rw [Real.sign_of_pos h, abs_of_pos h, one_mul]

theorem orbit_calibration_identity (r : ℝ) (u v : OrbitPlane) :
    orbitSymplectic r u (orbitOrientedTurn r v) = orbitCalibratedForm r u v := by
  change r * (u 0 * (Real.sign r * v 0) - u 1 * (Real.sign r * (-v 1))) =
    |r| * (u 0 * v 0 + u 1 * v 1)
  rw [← orbit_sign_times_self r]
  ring

theorem orbit_oriented_square (r : ℝ) (hr : r ≠ 0) (u : OrbitPlane) :
    orbitOrientedTurn r (orbitOrientedTurn r u) = -u := by
  rcases Real.sign_apply_eq_of_ne_zero r hr with hs | hs
  · ext i
    fin_cases i <;> simp [orbitOrientedTurn, orbitQuarterTurn, hs]
  · ext i
    fin_cases i <;> simp [orbitOrientedTurn, orbitQuarterTurn, hs]

/-- With g(u,v)=Omega(u,Qv), compatibility has the negative sign on g(u,Qv). -/
theorem orbit_calibration_compatibility (r : ℝ) (hr : r ≠ 0) (u v : OrbitPlane) :
    orbitSymplectic r u v = -orbitCalibratedForm r u (orbitOrientedTurn r v) := by
  rw [← orbit_calibration_identity, orbit_oriented_square r hr]
  unfold orbitSymplectic
  simp only [Pi.neg_apply]
  ring

theorem orbit_calibrated_symmetric (r : ℝ) : FormSymmetric (orbitCalibratedForm r) := by
  intro u v
  change |r| * (u 0 * v 0 + u 1 * v 1) = |r| * (v 0 * u 0 + v 1 * u 1)
  ring

theorem orbit_calibrated_positive (r : ℝ) (hr : r ≠ 0) :
    FormPositive (orbitCalibratedForm r) := by
  intro u hu
  have hsum : 0 < u 0 ^ 2 + u 1 ^ 2 := by
    have hx := sq_nonneg (u 0)
    have hy := sq_nonneg (u 1)
    by_contra hn
    have hx0 : u 0 = 0 := sq_eq_zero_iff.mp (by nlinarith)
    have hy0 : u 1 = 0 := sq_eq_zero_iff.mp (by nlinarith)
    apply hu
    ext i
    fin_cases i <;> assumption
  change 0 < |r| * (u 0 * u 0 + u 1 * u 1)
  exact mul_pos (abs_pos.mpr hr) (by simpa only [pow_two] using hsum)

theorem orbit_calibrated_area (r : ℝ) :
    formArea (orbitCalibratedForm r) orbitBasisX orbitBasisY = |r| :=
  orbit_scalar_area |r| (abs_nonneg r)

theorem orbit_zero_calibration :
    orbitCalibratedForm 0 = 0 ∧ orbitOrientedTurn 0 = 0 := by
  simp [orbitCalibratedForm, orbitOrientedTurn]

#print axioms OrbitPlane
#print axioms orbitBasisX
#print axioms orbitBasisY
#print axioms orbitQuarterTurn
#print axioms orbitDotForm
#print axioms orbitSymplectic
#print axioms orbitOrientedTurn
#print axioms orbitCalibratedForm
#print axioms orbit_basis_decomposition
#print axioms orbit_quarter_basis_x
#print axioms orbit_quarter_basis_y
#print axioms orbit_quarter_square
#print axioms orbit_dot_apply
#print axioms orbit_bilinear_expansion
#print axioms orbit_quarter_invariant_form
#print axioms orbit_trace_one_selection
#print axioms orbit_scalar_gram
#print axioms orbit_scalar_area
#print axioms orbit_trace_one_area
#print axioms orbit_selected_trace_in_orthonormal_pair
#print axioms orbit_sign_times_self
#print axioms orbit_calibration_identity
#print axioms orbit_oriented_square
#print axioms orbit_calibration_compatibility
#print axioms orbit_calibrated_symmetric
#print axioms orbit_calibrated_positive
#print axioms orbit_calibrated_area
#print axioms orbit_zero_calibration

end
end ChatgptAudit.Orbit052
