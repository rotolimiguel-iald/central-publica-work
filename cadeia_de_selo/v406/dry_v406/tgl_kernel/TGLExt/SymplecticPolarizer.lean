-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_053 (06-07/09/2026), transposta em 07/09/2026
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
import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.Analysis.InnerProductSpace.StandardSubspace
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Covariant053

open ClosedSubmodule

noncomputable section

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
variable (R : Submodule ℝ H) [CompleteSpace R]

/-- The ambient real polarizer is the actual compression P_R (-i) P_R.
It is not a modular conjugation or a modular generator. -/
def symplecticPolarizer : H →L[ℝ] H :=
  R.starProjection.comp
    ((((-Complex.I) • ContinuousLinearMap.id ℂ H).restrictScalars ℝ).comp
      R.starProjection)

theorem polarizer_apply (x : H) :
    symplecticPolarizer R x =
      R.starProjection ((-Complex.I) • R.starProjection x) := rfl

theorem polarizer_mem (x : H) : symplecticPolarizer R x ∈ R := by
  rw [polarizer_apply]
  exact R.starProjection_apply_mem _

/-- On the ambient space the imaginary pairing is compressed in both variables. -/
theorem polarizer_pairing (x y : H) :
    inner ℝ x (symplecticPolarizer R y) =
      (inner ℂ (R.starProjection x) (R.starProjection y)).im := by
  rw [polarizer_apply, ← R.inner_starProjection_left_eq_right,
    ClosedSubmodule.inner_real_eq_re_inner, inner_smul_right]
  simp [Complex.mul_re]

theorem polarizer_duality {x y : H} (hx : x ∈ R) (hy : y ∈ R) :
    (inner ℂ x (symplecticPolarizer R y)).re = (inner ℂ x y).im := by
  rw [← ClosedSubmodule.inner_real_eq_re_inner, polarizer_pairing,
    Submodule.starProjection_eq_self_iff.mpr hx,
    Submodule.starProjection_eq_self_iff.mpr hy]

theorem polarizer_norm_le (x : H) : ‖symplecticPolarizer R x‖ ≤ ‖x‖ := by
  rw [polarizer_apply]
  calc
    ‖R.starProjection ((-Complex.I) • R.starProjection x)‖
        ≤ ‖(-Complex.I) • R.starProjection x‖ := R.norm_starProjection_apply_le _
    _ = ‖R.starProjection x‖ := by rw [norm_smul]; simp
    _ ≤ ‖x‖ := R.norm_starProjection_apply_le _

theorem polarizer_opNorm_le : ‖symplecticPolarizer R‖ ≤ 1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ zero_le_one
  intro x
  simpa only [one_mul] using polarizer_norm_le R x

theorem polarizer_antisymmetric (x y : H) :
    inner ℝ x (symplecticPolarizer R y) =
      -inner ℝ (symplecticPolarizer R x) y := by
  rw [real_inner_comm y (symplecticPolarizer R x),
    polarizer_pairing, polarizer_pairing]
  simpa only [RCLike.im_eq_complex_im] using
    (inner_im_symm (𝕜 := ℂ) (R.starProjection x) (R.starProjection y))

/-- Riesz uniqueness within the real subspace, with all domains explicit. -/
theorem polarizer_eq_of_pairing {y z : H} (hy : y ∈ R) (hz : z ∈ R)
    (hp : ∀ x ∈ R, (inner ℂ x z).re = (inner ℂ x y).im) :
    symplecticPolarizer R y = z := by
  have hd : symplecticPolarizer R y - z ∈ R :=
    R.sub_mem (polarizer_mem R y) hz
  have hh : inner ℝ (symplecticPolarizer R y - z)
      (symplecticPolarizer R y - z) = 0 := by
    rw [inner_sub_right, ClosedSubmodule.inner_real_eq_re_inner, ClosedSubmodule.inner_real_eq_re_inner,
      polarizer_duality R hd hy, hp _ hd, sub_self]
  exact sub_eq_zero.mp (inner_self_eq_zero.mp hh)

theorem polarizer_kernel_iff {y : H} (hy : y ∈ R) :
    symplecticPolarizer R y = 0 ↔
      ∀ x ∈ R, (inner ℂ x y).im = 0 := by
  constructor
  · intro h x hx
    rw [← polarizer_duality R hx hy, h, inner_zero_right]
    rfl
  · intro h
    apply polarizer_eq_of_pairing R hy R.zero_mem
    intro x hx
    simp only [inner_zero_right, Complex.zero_re, h x hx]

/-- A quadratic family on the real ambient space. It can have a nontrivial radical. -/
def polarizerForm (epsilon : ℝ) (x y : H) : ℝ :=
  inner ℝ (symplecticPolarizer R x) (symplecticPolarizer R y) +
    epsilon * inner ℝ (symplecticPolarizer R (symplecticPolarizer R x))
      (symplecticPolarizer R (symplecticPolarizer R y))

theorem polarizer_form_re (epsilon : ℝ) (x y : H) :
    polarizerForm R epsilon x y =
      (inner ℂ (symplecticPolarizer R x) (symplecticPolarizer R y)).re +
        epsilon * (inner ℂ (symplecticPolarizer R (symplecticPolarizer R x))
          (symplecticPolarizer R (symplecticPolarizer R y))).re := by
  simp only [polarizerForm, ClosedSubmodule.inner_real_eq_re_inner]

/-- The bilinear bundle has the literal polarizer family as its evaluation. -/
def polarizerFormBilin (epsilon : ℝ) : H →ₗ[ℝ] H →ₗ[ℝ] ℝ where
  toFun x :=
    { toFun := polarizerForm R epsilon x
      map_add' := by
        intro y z
        simp only [polarizerForm, map_add, inner_add_right]
        ring
      map_smul' := by
        intro c y
        change polarizerForm R epsilon x (c • y) = c * polarizerForm R epsilon x y
        simp only [polarizerForm, map_smul, real_inner_smul_right]
        ring }
  map_add' := by
    intro x y
    ext z
    change polarizerForm R epsilon (x+y) z =
      polarizerForm R epsilon x z + polarizerForm R epsilon y z
    simp only [polarizerForm, map_add, inner_add_left]
    ring
  map_smul' := by
    intro c x
    ext y
    change polarizerForm R epsilon (c • x) y = c * polarizerForm R epsilon x y
    simp only [polarizerForm, map_smul, real_inner_smul_left]
    ring

theorem polarizer_form_apply (epsilon : ℝ) (x y : H) :
    polarizerFormBilin R epsilon x y = polarizerForm R epsilon x y := rfl

theorem polarizer_form_symmetric (epsilon : ℝ) (x y : H) :
    polarizerForm R epsilon x y = polarizerForm R epsilon y x := by
  simp only [polarizerForm, real_inner_comm]

theorem polarizer_form_diagonal (epsilon : ℝ) (x : H) :
    polarizerForm R epsilon x x =
      ‖symplecticPolarizer R x‖^2 +
        epsilon * ‖symplecticPolarizer R (symplecticPolarizer R x)‖^2 := by
  simp only [polarizerForm, real_inner_self_eq_norm_sq]

theorem polarizer_form_nonneg (epsilon : ℝ) (he : 0 ≤ epsilon) (x : H) :
    0 ≤ polarizerForm R epsilon x x := by
  rw [polarizer_form_diagonal]
  exact add_nonneg (sq_nonneg _) (mul_nonneg he (sq_nonneg _))

theorem polarizer_form_zero_iff (epsilon : ℝ) (he : 0 ≤ epsilon) (x : H) :
    polarizerForm R epsilon x x = 0 ↔ symplecticPolarizer R x = 0 := by
  rw [polarizer_form_diagonal]
  constructor
  · intro h
    have ht : 0 ≤ epsilon * ‖symplecticPolarizer R (symplecticPolarizer R x)‖^2 :=
      mul_nonneg he (sq_nonneg _)
    have hn : ‖symplecticPolarizer R x‖ = 0 := by nlinarith
    exact norm_eq_zero.mp hn
  · intro h
    simp [h]

/-- An ambient complex isometry preserving R also preserves its real projection. -/
theorem real_projection_covariant (W : H ≃ₗᵢ[ℂ] H)
    (hWR : ∀ x : H, x ∈ R ↔ W x ∈ R) (x : H) :
    R.starProjection (W x) = W (R.starProjection x) := by
  apply Submodule.eq_starProjection_of_mem_of_inner_eq_zero
    ((hWR _).mp (R.starProjection_apply_mem x))
  intro y hy
  have hy' : W.symm y ∈ R := (hWR _).mpr (by simpa only [W.apply_symm_apply] using hy)
  calc
    inner ℝ (W x - W (R.starProjection x)) y =
        inner ℝ (W (x - R.starProjection x)) (W (W.symm y)) := by
      rw [map_sub, W.apply_symm_apply]
    _ = inner ℝ (x - R.starProjection x) (W.symm y) := by
      simp only [ClosedSubmodule.inner_real_eq_re_inner, W.inner_map_map]
    _ = 0 := Submodule.starProjection_inner_eq_zero x (W.symm y) hy'

theorem polarizer_covariant (W : H ≃ₗᵢ[ℂ] H)
    (hWR : ∀ x : H, x ∈ R ↔ W x ∈ R) (x : H) :
    symplecticPolarizer R (W x) = W (symplecticPolarizer R x) := by
  rw [polarizer_apply, real_projection_covariant R W hWR,
    ← W.map_smul (-Complex.I) (R.starProjection x),
    real_projection_covariant R W hWR]
  rfl

theorem polarizer_square_covariant (W : H ≃ₗᵢ[ℂ] H)
    (hWR : ∀ x : H, x ∈ R ↔ W x ∈ R) (x : H) :
    symplecticPolarizer R (symplecticPolarizer R (W x)) =
      W (symplecticPolarizer R (symplecticPolarizer R x)) := by
  rw [polarizer_covariant R W hWR, polarizer_covariant R W hWR]

/-- Covariance requires a genuine complex isometry carrying R onto itself. -/
theorem polarizer_form_covariant (epsilon : ℝ) (W : H ≃ₗᵢ[ℂ] H)
    (hWR : ∀ x : H, x ∈ R ↔ W x ∈ R) (x y : H) :
    polarizerForm R epsilon (W x) (W y) = polarizerForm R epsilon x y := by
  simp only [polarizerForm, polarizer_covariant R W hWR,
    ClosedSubmodule.inner_real_eq_re_inner, W.inner_map_map]

#print axioms symplecticPolarizer
#print axioms polarizer_apply
#print axioms polarizer_mem
#print axioms polarizer_pairing
#print axioms polarizer_duality
#print axioms polarizer_norm_le
#print axioms polarizer_opNorm_le
#print axioms polarizer_antisymmetric
#print axioms polarizer_eq_of_pairing
#print axioms polarizer_kernel_iff
#print axioms polarizerForm
#print axioms polarizer_form_re
#print axioms polarizerFormBilin
#print axioms polarizer_form_apply
#print axioms polarizer_form_symmetric
#print axioms polarizer_form_diagonal
#print axioms polarizer_form_nonneg
#print axioms polarizer_form_zero_iff
#print axioms real_projection_covariant
#print axioms polarizer_covariant
#print axioms polarizer_square_covariant
#print axioms polarizer_form_covariant

end
end ChatgptAudit.Covariant053
