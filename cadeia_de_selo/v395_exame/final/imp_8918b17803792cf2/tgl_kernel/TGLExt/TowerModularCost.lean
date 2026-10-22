-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_054 (06-07/09/2026), transposta em 07/09/2026
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
import TGLExt.PolarizerCostSeries
import TGLExt.CovariantAreaCounterexample

set_option autoImplicit false
set_option maxHeartbeats 3200000

namespace ChatgptAudit.Cost054
open TGLExt Matrix Filter Topology Set ClosedSubmodule
open scoped ENNReal NNReal
open ChatgptAudit ChatgptAudit.Covariant053 ChatgptAudit.Observable035
  ChatgptAudit.Orbit052 ChatgptAudit.Density033 ChatgptAudit.Thermal025
noncomputable section

/-- The extended cost of the actual global state polarizer, with no spectral gap assumed. -/
def towerModularCost (P : SiteProfile) (x : TowerHilbert P) : ℝ≥0∞ :=
  polarizerModularCost (statePolarizer P) x

def towerModularCostDomain (P : SiteProfile) : Submodule ℝ (TowerHilbert P) :=
  polarizerCostDomain (statePolarizer P)

theorem tower_modular_cost_domain (P : SiteProfile) (x : TowerHilbert P) :
    x ∈ towerModularCostDomain P ↔ towerModularCost P x < ⊤ :=
  mem_polarizerCostDomain (statePolarizer P) x

theorem tower_modular_cost_zero_iff (P : SiteProfile) (x : TowerHilbert P) :
    towerModularCost P x = 0 ↔ statePolarizer P x = 0 :=
  polarizer_modular_cost_zero_iff (statePolarizer P) x

theorem tower_modular_cost_centralizer (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hsa : IsSelfAdjoint A) :
    towerModularCost P (A (hOmega P)) = 0 ↔ A ∈ omegaCentralizer P :=
  (tower_modular_cost_zero_iff P _).trans (state_polarizer_zero_iff P A hA hsa)

theorem tower_modular_cost_response_kernel (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hsa : IsSelfAdjoint A) :
    towerModularCost P (A (hOmega P)) = 0 ↔
      ∀ B ∈ theFactorObject P, IsSelfAdjoint B → realStateResponse P A B = 0 := by
  rw [tower_modular_cost_centralizer P A hA hsa]
  exact (state_response_kernel P A hA hsa).symm

/-- Scalar restriction of the existing GNS implementation, not a new horizon. -/
def horizonCostIsometry (P : SiteProfile) (h : TowerHorizon P) :
    TowerHilbert P ≃ₗᵢ[ℝ] TowerHilbert P :=
  { (horizonGNSUnitary P h).toLinearEquiv.restrictScalars ℝ with
    norm_map' := (horizonGNSUnitary P h).norm_map }

theorem tower_modular_cost_covariant (P : SiteProfile) (h : TowerHorizon P)
    (x : TowerHilbert P) :
    towerModularCost P (horizonGNSUnitary P h x) = towerModularCost P x :=
  polarizer_modular_cost_covariant (statePolarizer P) (horizonCostIsometry P h)
    (state_polarizer_covariant P h) x

theorem tower_modular_domain_covariant (P : SiteProfile) (h : TowerHorizon P)
    (x : TowerHilbert P) :
    horizonGNSUnitary P h x ∈ towerModularCostDomain P ↔
      x ∈ towerModularCostDomain P := by
  rw [tower_modular_cost_domain, tower_modular_cost_domain, tower_modular_cost_covariant]

theorem tower_modular_cost_factor_invariant (P : SiteProfile) (h : TowerHorizon P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    towerModularCost P (adT h A (hOmega P)) = towerModularCost P (A (hOmega P)) := by
  rw [← horizon_gns_apply_factor P h A hA]
  exact tower_modular_cost_covariant P h _

theorem tower_modular_cost_lowerSemicontinuous (P : SiteProfile) :
    LowerSemicontinuous (towerModularCost P) :=
  polarizer_modular_cost_lowerSemicontinuous (statePolarizer P)

/-- Iteration takes place in the same finite matrix algebra and represents powers of global D. -/
def localPolarizerIterate (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) : ℕ → Matrix (chainIdx N) (chainIdx N) ℂ
  | 0 => a
  | n + 1 => localPolarizerMatrix P N (localPolarizerIterate P N a n)

theorem local_polarizer_iterate_hermitian (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) (n : ℕ) :
    (localPolarizerIterate P N a n).IsHermitian := by
  induction n with
  | zero => exact ha
  | succ n ih => exact local_polarizer_hermitian P N _ ih

theorem local_polarizer_iterate_entry (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (n : ℕ) (i j : chainIdx N) :
    localPolarizerIterate P N a n i j =
      (Complex.I * (((towerW P N i - towerW P N j) /
        (towerW P N i + towerW P N j) : ℝ) : ℂ)) ^ n * a i j := by
  induction n with
  | zero => simp [localPolarizerIterate]
  | succ n ih =>
    simp only [localPolarizerIterate, localPolarizerMatrix, ih, pow_succ]
    ring

theorem state_polarizer_local_power (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) (n : ℕ) :
    (statePolarizer P ^ n) (towerPi P a (hOmega P)) =
      towerPi P (localPolarizerIterate P N a n) (hOmega P) := by
  induction n with
  | zero => simp [localPolarizerIterate]
  | succ n ih =>
    rw [pow_succ', mul_apply_eq_comp, ih,
      state_polarizer_local P N _ (local_polarizer_iterate_hermitian P N a ha n)]
    rfl

theorem local_iterate_normSq (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (n : ℕ) (i j : chainIdx N) :
    Complex.normSq (localPolarizerIterate P N a n i j) =
      ((towerW P N i - towerW P N j) / (towerW P N i + towerW P N j)) ^ (2 * n) *
        Complex.normSq (a i j) := by
  rw [local_polarizer_iterate_entry, Complex.normSq_mul, map_pow,
    Complex.normSq_mul, Complex.normSq_I, Complex.normSq_ofReal, one_mul]
  rw [← pow_two, ← pow_mul]

theorem state_polarizer_local_power_norm (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) (n : ℕ) :
    ‖(statePolarizer P ^ n) (towerPi P a (hOmega P))‖ ^ 2 =
      ∑ j, ∑ i, towerW P N j *
        (((towerW P N i - towerW P N j) / (towerW P N i + towerW P N j)) ^ (2 * n) *
          Complex.normSq (a i j)) := by
  rw [state_polarizer_local_power P N a ha n, norm_sq_eq_re_inner (𝕜 := ℂ),
    local_operator_pairing]
  change (tInner P N (localPolarizerIterate P N a n) (localPolarizerIterate P N a n)).re = _
  rw [tInner_self_eq, Complex.ofReal_re]
  simp only [Finset.mul_sum, local_iterate_normSq]

/-- A finite column-weighted expression, before symmetrizing the ordered pairs. -/
def localModularCost (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) : ℝ :=
  ∑ j, ∑ i, towerW P N j *
    (((towerW P N i - towerW P N j) / (towerW P N i + towerW P N j)) *
      (Real.log (towerW P N i) - Real.log (towerW P N j))) * Complex.normSq (a i j)

theorem tower_local_cost_hasSum (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) :
    HasSum (fun n : ℕ => (2 : ℝ) / (2 * (n : ℝ) + 1) *
      ‖(statePolarizer P ^ (n + 1)) (towerPi P a (hOmega P))‖ ^ 2)
      (localModularCost P N a) := by
  have hs (j i : chainIdx N) :=
    ((polarizer_cost_weights_hasSum (towerW P N i) (towerW P N j)
      (towerW_pos P N i) (towerW_pos P N j)).mul_left (towerW P N j)).mul_right
        (Complex.normSq (a i j))
  have hall := hasSum_sum (s := Finset.univ) (fun j _ =>
    hasSum_sum (s := Finset.univ) (fun i _ => hs j i))
  change HasSum _ (localModularCost P N a) at hall
  apply hall.congr_fun
  intro n
  rw [state_polarizer_local_power_norm P N a ha (n + 1)]
  simp only [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j _
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem tower_local_cost_formula (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) :
    towerModularCost P (towerPi P a (hOmega P)) = ENNReal.ofReal (localModularCost P N a) :=
  polarizer_modular_cost_eq_of_hasSum (statePolarizer P) _ _
    (tower_local_cost_hasSum P N a ha)

theorem tower_local_mem_cost_domain (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) :
    towerPi P a (hOmega P) ∈ towerModularCostDomain P := by
  rw [tower_modular_cost_domain, tower_local_cost_formula P N a ha]
  exact ENNReal.ofReal_lt_top

/-- Local self-adjoint vectors form a Hilbert-dense subset of the real state sector.
This does not claim that they are a core for the cost form. -/
theorem tower_cost_domain_dense_real (P : SiteProfile) :
    (towerModularCostDomain P ⊓ realStateSubspace P).topologicalClosure =
      realStateSubspace P := by
  apply le_antisymm
  · exact Submodule.topologicalClosure_minimal _ inf_le_right (real_state_subspace_closed P)
  · change (Submodule.span ℝ (realStateGenerators P)).topologicalClosure ≤ _
    apply Submodule.topologicalClosure_minimal _ ?_ (Submodule.isClosed_topologicalClosure _)
    apply Submodule.span_le.mpr
    rintro x ⟨A, hA, hsa, hx⟩
    rw [hx]
    apply (Submodule.isClosed_topologicalClosure _).mem_of_tendsto
      (expectation_omega_limit (P := P) A)
    apply Filter.Eventually.of_forall
    intro N
    apply Submodule.le_topologicalClosure
    change towerPi P (expectationMatrix P N A) (hOmega P) ∈
      towerModularCostDomain P ⊓ realStateSubspace P
    have hmat := expectationMatrix_hermitian N A hA hsa
    exact ⟨tower_local_mem_cost_domain P N _ hmat,
      real_state_generator_mem P _ (towerPi_mem_factor _)
        (tower_local_selfadjoint P N _ hmat)⟩

/-- The ordered-pair formula has a factor one half. No choice of ordering on chainIdx is used. -/
theorem local_modular_cost_symmetric (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) :
    localModularCost P N a = (1 / 2 : ℝ) *
      ∑ i, ∑ j, (towerW P N i - towerW P N j) *
        (Real.log (towerW P N i) - Real.log (towerW P N j)) * Complex.normSq (a i j) := by
  let f : chainIdx N → chainIdx N → ℝ := fun i j =>
    towerW P N j * (((towerW P N i - towerW P N j) /
      (towerW P N i + towerW P N j)) *
      (Real.log (towerW P N i) - Real.log (towerW P N j))) * Complex.normSq (a i j)
  have hp (i j : chainIdx N) : f i j + f j i =
      (towerW P N i - towerW P N j) *
        (Real.log (towerW P N i) - Real.log (towerW P N j)) * Complex.normSq (a i j) := by
    have hij : star (a j i) = a i j := congrFun (congrFun ha i) j
    have hn : Complex.normSq (a j i) = Complex.normSq (a i j) := by
      simpa only [Complex.star_def, Complex.normSq_conj] using congrArg Complex.normSq hij
    have hd : towerW P N i + towerW P N j ≠ 0 :=
      ne_of_gt (add_pos (towerW_pos P N i) (towerW_pos P N j))
    dsimp only [f]
    rw [hn, add_comm (towerW P N j) (towerW P N i)]
    field_simp [hd]
    ring
  have hswap : (∑ i, ∑ j, f j i) = ∑ i, ∑ j, f i j := Finset.sum_comm
  have hdef : localModularCost P N a = ∑ i, ∑ j, f i j := by
    unfold localModularCost
    exact Finset.sum_comm
  rw [hdef]
  calc
    (∑ i, ∑ j, f i j) = (1 / 2 : ℝ) *
        ((∑ i, ∑ j, f i j) + (∑ i, ∑ j, f j i)) := by rw [hswap]; ring
    _ = (1 / 2 : ℝ) * ∑ i, ∑ j, (f i j + f j i) := by
      simp only [Finset.sum_add_distrib]
    _ = _ := by simp only [hp]

theorem tower_local_cost_symmetric_formula (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) :
    towerModularCost P (towerPi P a (hOmega P)) = ENNReal.ofReal ((1 / 2 : ℝ) *
      ∑ i, ∑ j, (towerW P N i - towerW P N j) *
        (Real.log (towerW P N i) - Real.log (towerW P N j)) * Complex.normSq (a i j)) := by
  rw [tower_local_cost_formula P N a ha, local_modular_cost_symmetric P N a ha]

section RotatingPair
variable {H : Type*} [NormedAddCommGroup H] [NormedSpace ℝ H]

theorem rotating_pair_norm_powers (D : H →L[ℝ] H) (x y : H) (k : ℝ)
    (hx : D x = k • y) (hy : D y = (-k) • x) (hn : ‖y‖ ^ 2 = ‖x‖ ^ 2) (n : ℕ) :
    ‖(D ^ n) x‖ ^ 2 = k ^ (2 * n) * ‖x‖ ^ 2 ∧
      ‖(D ^ n) y‖ ^ 2 = k ^ (2 * n) * ‖x‖ ^ 2 := by
  induction n with
  | zero => simp [hn]
  | succ n ih =>
    have hp : 2 * (n + 1) = 2 * n + 2 := by omega
    constructor
    · rw [pow_succ D n, mul_apply_eq_comp, hx, map_smul, norm_smul, mul_pow,
        Real.norm_eq_abs, sq_abs, ih.2, hp, pow_add]
      ring
    · rw [pow_succ D n, mul_apply_eq_comp, hy, map_smul, norm_smul, mul_pow,
        Real.norm_eq_abs, abs_neg, sq_abs, ih.1, hp, pow_add]
      ring

end RotatingPair

theorem first_pauli_cost_norm_powers (n : ℕ) :
    ‖(statePolarizer thirdThermalReference ^ n)
      (sitePauliX thirdThermalReference 0 (hOmega _))‖ ^ 2 = (1 / 3 : ℝ) ^ (2 * n) := by
  have hn := first_pair_real_gram
  have hxx : ‖sitePauliX thirdThermalReference 0 (hOmega _)‖ ^ 2 = 1 := by
    simpa only [real_inner_self_eq_norm_sq] using hn.1
  have hyy : ‖sitePauliY thirdThermalReference 0 (hOmega _)‖ ^ 2 = 1 := by
    simpa only [real_inner_self_eq_norm_sq] using hn.2.1
  have h := (rotating_pair_norm_powers (statePolarizer thirdThermalReference) _ _ (1 / 3)
    first_pauli_polarizer_x (by simpa only [neg_div] using first_pauli_polarizer_y)
    (by rw [hxx, hyy]) n).1
  simpa only [hxx, mul_one] using h

theorem double_flip_cost_norm_powers (n : ℕ) :
    ‖(statePolarizer thirdThermalReference ^ n) (doubleFlipX (hOmega _))‖ ^ 2 =
      (3 / 5 : ℝ) ^ (2 * n) * (5 / 9) := by
  have h := (rotating_pair_norm_powers (statePolarizer thirdThermalReference) _ _ (3 / 5)
    double_flip_polarizer_x (by simpa only [neg_div] using double_flip_polarizer_y)
    (by rw [double_flip_norm_squares.1, double_flip_norm_squares.2]) n).1
  simpa only [double_flip_norm_squares.1] using h

/-- The first reference vector is unchanged from the previous construction. -/
theorem first_pauli_modular_cost :
    towerModularCost thirdThermalReference (sitePauliX thirdThermalReference 0 (hOmega _)) =
      ENNReal.ofReal (Real.log 2 / 3) := by
  have hn : ‖sitePauliX thirdThermalReference 0 (hOmega _)‖ ^ 2 = 1 := by
    simpa using first_pauli_cost_norm_powers 0
  have h := polarizer_cost_of_weight_norm_powers (statePolarizer thirdThermalReference)
    (sitePauliX thirdThermalReference 0 (hOmega _)) 2 1 (by norm_num) (by norm_num)
    (fun n => by rw [first_pauli_cost_norm_powers, hn]; norm_num)
  change towerModularCost thirdThermalReference _ = _ at h
  rw [hn] at h
  convert h using 1
  congr 1
  norm_num [Real.log_one]
  ring

/-- The second vector is raw: its squared GNS norm is five ninths, not one. -/
theorem double_flip_modular_cost :
    towerModularCost thirdThermalReference (doubleFlipX (hOmega _)) =
      ENNReal.ofReal (2 * Real.log 2 / 3) := by
  have h := polarizer_cost_of_weight_norm_powers (statePolarizer thirdThermalReference)
    (doubleFlipX (hOmega _)) 4 1 (by norm_num) (by norm_num)
    (fun n => by rw [double_flip_cost_norm_powers, double_flip_norm_squares.1]; norm_num)
  have hlog : Real.log (4 : ℝ) = 2 * Real.log 2 := by
    have he : (4 : ℝ) = 2 ^ 2 := by norm_num
    rw [he, Real.log_pow]
    norm_num
  change towerModularCost thirdThermalReference _ = _ at h
  rw [double_flip_norm_squares.1] at h
  convert h using 1
  congr 1
  norm_num [Real.log_one, hlog]
  ring

#print axioms towerModularCost
#print axioms towerModularCostDomain
#print axioms tower_modular_cost_domain
#print axioms tower_modular_cost_zero_iff
#print axioms tower_modular_cost_centralizer
#print axioms tower_modular_cost_response_kernel
#print axioms horizonCostIsometry
#print axioms tower_modular_cost_covariant
#print axioms tower_modular_domain_covariant
#print axioms tower_modular_cost_factor_invariant
#print axioms tower_modular_cost_lowerSemicontinuous
#print axioms localPolarizerIterate
#print axioms local_polarizer_iterate_hermitian
#print axioms local_polarizer_iterate_entry
#print axioms state_polarizer_local_power
#print axioms local_iterate_normSq
#print axioms state_polarizer_local_power_norm
#print axioms localModularCost
#print axioms tower_local_cost_hasSum
#print axioms tower_local_cost_formula
#print axioms tower_local_mem_cost_domain
#print axioms tower_cost_domain_dense_real
#print axioms local_modular_cost_symmetric
#print axioms tower_local_cost_symmetric_formula
#print axioms rotating_pair_norm_powers
#print axioms first_pauli_cost_norm_powers
#print axioms double_flip_cost_norm_powers
#print axioms first_pauli_modular_cost
#print axioms double_flip_modular_cost

end
end ChatgptAudit.Cost054
