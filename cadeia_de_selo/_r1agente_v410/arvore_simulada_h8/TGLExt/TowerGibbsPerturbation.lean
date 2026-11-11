-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_024 (06/09/2026), transposta em 06/09/2026
-- Lote 024..026: a perturbacao de GIBBS realizada no mesmo Hilbert da torre (estado fiel,
--   normalizado, distinto da orbita modular; resposta quadratica; calor/fonte por normalizacao);
--   o LIMITE TERMICO: para perfil constante nao tracial a preparacao NAO tem limite em norma
--   (nao-Cauchy) e o acoplamento da torre e ilimitado; corte com escala escolhida; AFINIDADE:
--   criterio exato (Cauchy <=> afinidade-limite > 0), estado global no Hilbert original, fiel e
--   ciclico; perfil gradual (muda em infinitos sitios, ainda fiel). Estatuto [REAL / INPUT / OPEN]:
--   selecao fisica, area, H3 dinamico, dimensao/assinatura, globalizacao e a classificacao geral
--   dos estados normais (disjuncao) seguem INPUT/OPEN — a bancada NAO promoveu nao-Cauchy a teorema
--   geral de disjuncao nem importou Kakutani.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100%; manifestos 202/206/220;
--   3/3 auditores da bancada exit 0; recompilacao INDEPENDENTE 22/22, axiomas no trio; guarda de
--   colisao estatica no ROOT; enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.QuadraticGibbsCurve

set_option autoImplicit false
set_option maxHeartbeats 12000000
namespace ChatgptAudit.Thermal024
open Matrix Filter Topology Set TGLExt ChatgptAudit.Micro021
open scoped ComplexOrder
noncomputable section
variable {ι : Type} [Fintype ι] [DecidableEq ι] [Nonempty ι]

def gibbsFilter (p : ι → ℝ) (s : ℝ) : Matrix ι ι ℂ :=
  Matrix.diagonal (fun i => (Real.sqrt (gibbsWeights p s i/p i) : ℂ))

def gibbsFilterInverse (p : ι → ℝ) (s : ℝ) : Matrix ι ι ℂ :=
  Matrix.diagonal (fun i => ((Real.sqrt (gibbsWeights p s i/p i) : ℂ))⁻¹)

theorem gibbs_filter_positive (p : ι → ℝ) (hp : ∀ i, 0<p i) (s : ℝ) :
    (gibbsFilter p s).PosDef := by
  rw [gibbsFilter,Matrix.posDef_diagonal_iff]
  intro i
  exact Complex.zero_lt_real.mpr (Real.sqrt_pos.mpr (div_pos (gibbs_weights_positive p hp s i) (hp i)))

omit [Nonempty ι] in
theorem gibbs_filter_self_adjoint (p : ι → ℝ) (s : ℝ) : (gibbsFilter p s)ᴴ=gibbsFilter p s := by
  ext i j
  by_cases hij : i=j
  · subst j
    simp [gibbsFilter]
  · simp [gibbsFilter,Matrix.conjTranspose_apply,Matrix.diagonal_apply_ne _ hij,
      Matrix.diagonal_apply_ne _ (Ne.symm hij)]

theorem gibbs_filter_inverse (p : ι → ℝ) (hp : ∀ i, 0<p i) (s : ℝ) :
    gibbsFilter p s*gibbsFilterInverse p s=1 := by
  rw [gibbsFilter,gibbsFilterInverse,Matrix.diagonal_mul_diagonal]
  ext i j
  by_cases hij : i=j
  · subst j
    have hn : (Real.sqrt (gibbsWeights p s i/p i):ℂ)≠0 := by
      exact_mod_cast ne_of_gt (Real.sqrt_pos.mpr (div_pos (gibbs_weights_positive p hp s i) (hp i)))
    simp [hn]
  · simp [Matrix.diagonal_apply_ne _ hij,Matrix.one_apply_ne hij]

omit [DecidableEq ι] in
theorem gibbs_filter_weighted_square (p : ι → ℝ) (hp : ∀ i, 0<p i) (s : ℝ) (i : ι) :
    p i*(Real.sqrt (gibbsWeights p s i/p i))^2=gibbsWeights p s i := by
  rw [Real.sq_sqrt (le_of_lt (div_pos (gibbs_weights_positive p hp s i) (hp i)))]
  field_simp [ne_of_gt (hp i)]

theorem gibbs_filter_local_state (p : ι → ℝ) (hp : ∀ i, 0<p i) (s : ℝ) (a : Matrix ι ι ℂ) :
    (∑ i, (p i:ℂ)*((gibbsFilter p s)ᴴ*a*gibbsFilter p s) i i)=
      ∑ i, (gibbsWeights p s i:ℂ)*a i i := by
  rw [gibbs_filter_self_adjoint]
  apply Finset.sum_congr rfl
  intro i _
  have hc : (p i:ℂ)*(Real.sqrt (gibbsWeights p s i/p i):ℂ)^2=(gibbsWeights p s i:ℂ) := by
    exact_mod_cast gibbs_filter_weighted_square p hp s i
  simp only [gibbsFilter,Matrix.diagonal_mul,Matrix.mul_diagonal]
  calc
    (p i:ℂ)*((Real.sqrt (gibbsWeights p s i/p i):ℂ)*a i i*
        (Real.sqrt (gibbsWeights p s i/p i):ℂ))=
      ((p i:ℂ)*(Real.sqrt (gibbsWeights p s i/p i):ℂ)^2)*a i i := by ring
    _=_ := by rw [hc]

def towerGibbsVector (P : SiteProfile) (N : ℕ) (s : ℝ) : TowerHilbert P :=
  towerPi P (gibbsFilter (towerW P N) s) (hOmega P)

def towerGibbsState (P : SiteProfile) (N : ℕ) (s : ℝ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) : ℂ :=
  inner ℂ (towerGibbsVector P N s) (A (towerGibbsVector P N s))

theorem tower_gibbs_sandwich (P : SiteProfile) (N : ℕ) (s : ℝ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    towerGibbsState P N s A=
      omegaState P (star (towerPi P (gibbsFilter (towerW P N) s))*A*
        towerPi P (gibbsFilter (towerW P N) s)) := by
  unfold towerGibbsState towerGibbsVector omegaState
  change inner ℂ _ _=inner ℂ (hOmega P)
    (ContinuousLinearMap.adjoint (towerPi P (gibbsFilter (towerW P N) s))
      (A (towerPi P (gibbsFilter (towerW P N) s) (hOmega P))))
  rw [ContinuousLinearMap.adjoint_inner_right]

theorem tower_gibbs_local_state (P : SiteProfile) (N : ℕ) (s : ℝ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerGibbsState P N s (towerPi P a)=∑ i, (gibbsWeights (towerW P N) s i:ℂ)*a i i := by
  rw [tower_gibbs_sandwich]
  change omegaState P
    ((ContinuousLinearMap.adjoint (towerPi P (gibbsFilter (towerW P N) s)))*towerPi P a*
      towerPi P (gibbsFilter (towerW P N) s))=_
  rw [←towerPi_star,←towerPi_mul,←towerPi_mul,omegaState_pi]
  exact gibbs_filter_local_state (towerW P N) (towerW_pos P N) s a

theorem tower_gibbs_state_one (P : SiteProfile) (N : ℕ) (s : ℝ) :
    towerGibbsState P N s 1=1 := by
  rw [←towerPi_one (P := P) N,tower_gibbs_local_state]
  simp only [Matrix.one_apply_eq,mul_one,←Complex.ofReal_sum,gibbs_weights_normalized _ (towerW_pos P N),
    Complex.ofReal_one]

theorem tower_gibbs_vector_norm (P : SiteProfile) (N : ℕ) (s : ℝ) :
    ‖towerGibbsVector P N s‖=1 := by
  have hh := tower_gibbs_state_one P N s
  change inner ℂ (towerGibbsVector P N s) (towerGibbsVector P N s)=1 at hh
  have hreal : ‖towerGibbsVector P N s‖^2=1 := by
    rw [norm_sq_eq_re_inner (𝕜 := ℂ),hh]
    rfl
  nlinarith [norm_nonneg (towerGibbsVector P N s)]

theorem tower_gibbs_square_value (P : SiteProfile) (N : ℕ) (s : ℝ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    towerGibbsState P N s (star A*A)=
      inner ℂ (A (towerGibbsVector P N s)) (A (towerGibbsVector P N s)) := by
  change inner ℂ (towerGibbsVector P N s)
    (ContinuousLinearMap.adjoint A (A (towerGibbsVector P N s)))=_
  rw [ContinuousLinearMap.adjoint_inner_right]

theorem tower_gibbs_state_positive (P : SiteProfile) (N : ℕ) (s : ℝ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    0 ≤ (towerGibbsState P N s (star A*A)).re := by
  rw [tower_gibbs_square_value]
  exact inner_self_nonneg (𝕜 := ℂ)

theorem tower_gibbs_vector_separating (P : SiteProfile) (N : ℕ) (s : ℝ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A∈theFactorObject P)
    (hz : A (towerGibbsVector P N s)=0) : A=0 := by
  let F := towerPi P (gibbsFilter (towerW P N) s)
  let R := towerPi P (gibbsFilterInverse (towerW P N) s)
  have hF : F∈theFactorObject P := towerPi_mem_factor _
  have hAF : A*F=0 := factor_omega_separating ((theFactorObject P).mul_mem hA hF) hz
  have hFR : F*R=1 := by
    rw [←towerPi_mul,gibbs_filter_inverse _ (towerW_pos P N),towerPi_one]
  calc
    A=A*(F*R) := by rw [hFR,mul_one]
    _=(A*F)*R := (mul_assoc _ _ _).symm
    _=0 := by rw [hAF,zero_mul]

theorem tower_gibbs_state_faithful (P : SiteProfile) (N : ℕ) (s : ℝ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A∈theFactorObject P)
    (hz : towerGibbsState P N s (star A*A)=0) : A=0 := by
  rw [tower_gibbs_square_value] at hz
  exact tower_gibbs_vector_separating P N s A hA (inner_self_eq_zero.mp hz)

theorem tower_gibbs_state_seqWOT (P : SiteProfile) (N : ℕ) (s : ℝ) :
    SeqWOTContinuous (theFactorObject P) (towerGibbsState P N s) := by
  intro T Tinf C _ _ _ hWOT
  exact hWOT (towerGibbsVector P N s) (towerGibbsVector P N s)

theorem tower_gibbs_inclusion_coherent (P : SiteProfile) (N : ℕ) (s : ℝ)
    {L M : ℕ} (hLM : L≤M) (a : Matrix (chainIdx L) (chainIdx L) ℂ) :
    towerGibbsState P N s (towerPi P (tPush hLM a))=towerGibbsState P N s (towerPi P a) := by
  rw [towerPi_compat]

theorem tower_gibbs_local_generator (P : SiteProfile) (N : ℕ) (s : ℝ) :
    towerGibbsState P N s (towerPi P (diagonalModularGenerator (towerW P N)))=
      (gibbsMean (towerW P N) s:ℂ) := by
  rw [tower_gibbs_local_state]
  simp only [diagonalModularGenerator,Matrix.diagonal_apply_eq,gibbsMean,modularScore,
    Complex.ofReal_sum,Complex.ofReal_mul]


omit [Nonempty ι] in
theorem gibbs_filter_zero (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) :
    gibbsFilter p 0=1 := by
  ext i j
  by_cases hij : i=j
  · subst j
    simp [gibbsFilter,gibbs_weights_zero p hs,ne_of_gt (hp i)]
  · simp [gibbsFilter,Matrix.diagonal_apply_ne _ hij,Matrix.one_apply_ne hij]

theorem tower_gibbs_state_zero (P : SiteProfile) (N : ℕ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    towerGibbsState P N 0 A=omegaState P A := by
  unfold towerGibbsState towerGibbsVector
  rw [gibbs_filter_zero _ (towerW_pos P N) (towerW_sum P N),towerPi_one]
  rfl

theorem tower_gibbs_local_projection (P : SiteProfile) (N : ℕ) (s : ℝ) (i : chainIdx N) :
    towerGibbsState P N s (towerPi P (Matrix.diagonal (Pi.single i (1:ℂ))))=
      (gibbsWeights (towerW P N) s i:ℂ) := by
  rw [tower_gibbs_local_state]
  simp [Pi.single_apply]


theorem tower_gibbs_state_add (P : SiteProfile) (N : ℕ) (s : ℝ)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) :
    towerGibbsState P N s (A+B)=towerGibbsState P N s A+towerGibbsState P N s B := by
  simp [towerGibbsState,inner_add_right]

theorem tower_gibbs_state_smul (P : SiteProfile) (N : ℕ) (s : ℝ)
    (c : ℂ) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    towerGibbsState P N s (c • A)=c*towerGibbsState P N s A := by
  simp [towerGibbsState,inner_smul_right]

theorem tower_gibbs_state_square_nonnegative (P : SiteProfile) (N : ℕ) (s : ℝ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    0 ≤ towerGibbsState P N s (star A*A) := by
  rw [tower_gibbs_square_value,inner_self_eq_norm_sq_to_K]
  positivity

#print axioms tower_gibbs_state_add
#print axioms tower_gibbs_state_smul
#print axioms tower_gibbs_state_square_nonnegative
#print axioms gibbs_filter_zero
#print axioms tower_gibbs_state_zero
#print axioms tower_gibbs_local_projection
#print axioms gibbs_filter_positive
#print axioms gibbs_filter_self_adjoint
#print axioms gibbs_filter_inverse
#print axioms gibbs_filter_weighted_square
#print axioms gibbs_filter_local_state
#print axioms tower_gibbs_sandwich
#print axioms tower_gibbs_local_state
#print axioms tower_gibbs_state_one
#print axioms tower_gibbs_vector_norm
#print axioms tower_gibbs_square_value
#print axioms tower_gibbs_state_positive
#print axioms tower_gibbs_vector_separating
#print axioms tower_gibbs_state_faithful
#print axioms tower_gibbs_state_seqWOT
#print axioms tower_gibbs_inclusion_coherent
#print axioms tower_gibbs_local_generator
end
end ChatgptAudit.Thermal024
