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
import TGLExt.TowerModularCost
import Mathlib.Analysis.Calculus.LHopital

set_option autoImplicit false
set_option maxHeartbeats 3600000

namespace ChatgptAudit.Cost054
open TGLExt Matrix Filter Topology Set
open ChatgptAudit ChatgptAudit.Observable035 ChatgptAudit.Angular034
  ChatgptAudit.Covariant053 ChatgptAudit.Cocycle030 ChatgptAudit.Density033
noncomputable section

/-- The real expectation is a continuous real-linear functional. -/
def omegaRealContinuous (P : SiteProfile) :
    (TowerHilbert P →L[ℂ] TowerHilbert P) →L[ℝ] ℝ :=
  Complex.reCLM.comp ((omegaContinuous P).restrictScalars ℝ)

theorem omega_real_continuous_apply (P : SiteProfile)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P) :
    omegaRealContinuous P B = (omegaState P B).re := rfl

theorem bounded_phase_negative_generator (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (t : ℝ) :
    boundedPhase P (-A) t = boundedPhase P A (-t) := by
  simp only [boundedPhase, Complex.ofReal_neg, neg_mul, neg_smul, smul_neg]

theorem negative_phase_derivative (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (t : ℝ) :
    HasDerivAt (fun s : ℝ => boundedPhase P A (-s))
      (-(boundedPhase P A (-t) * (Complex.I • A))) t := by
  have h := bounded_phase_derivative P (-A) t
  change HasDerivAt (fun s : ℝ => boundedPhase P (-A) s) _ t at h
  simpa only [bounded_phase_negative_generator, smul_neg, mul_neg] using h

/-- Product-rule velocity; no derivative is taken as a definition of the cost. -/
def unitaryConjugationVelocity (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) (t : ℝ) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  -(boundedPhase P A (-t) * (Complex.I • A) * B * boundedPhase P A t) +
    boundedPhase P A (-t) * B * boundedPhase P A t * (Complex.I • A)

theorem unitary_conjugation_has_derivative (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : IsSelfAdjoint A) (t : ℝ) :
    HasDerivAt (unitaryConjugation P A B) (unitaryConjugationVelocity P A B t) t := by
  have h := ((negative_phase_derivative P A t).mul_const B).mul
    (bounded_phase_derivative P A t)
  have hf : (fun s : ℝ => boundedPhase P A (-s) * B * boundedPhase P A s) =
      unitaryConjugation P A B := by
    funext s
    simp only [unitaryConjugation, bounded_phase_star P A hA]
  change HasDerivAt (fun s : ℝ => boundedPhase P A (-s) * B * boundedPhase P A s) _ t at h
  rw [hf] at h
  simpa only [unitaryConjugationVelocity, neg_mul, mul_assoc] using h

/-- Minus the double commutator [A,[A,B]]. -/
def doubleModularCommutator (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  -(A * A * B) + A * B * A + A * B * A - B * (A * A)

theorem unitary_velocity_derivative_zero (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) :
    HasDerivAt (unitaryConjugationVelocity P A B) (doubleModularCommutator P A B) 0 := by
  let C := Complex.I • A
  have hn := negative_phase_derivative P A 0
  have hp := bounded_phase_derivative P A 0
  have hleft := (((hn.mul_const C).mul_const B).mul hp).neg
  have hright := ((hn.mul_const B).mul hp).mul_const C
  have h := hleft.add hright
  change HasDerivAt (unitaryConjugationVelocity P A B) _ 0 at h
  have hsq : C * C = -(A * A) := by
    simp only [C, smul_mul_assoc, mul_smul_comm, smul_smul,
      Complex.I_mul_I, neg_one_smul]
  have hmid : C * B * C = -(A * B * A) := by
    simp only [C, smul_mul_assoc, mul_smul_comm, smul_smul,
      Complex.I_mul_I, neg_one_smul]
  convert h using 1
  simp only [neg_zero, bounded_phase_zero, one_mul, mul_one]
  change doubleModularCommutator P A B =
    -(-C * C * B + C * B * C) + (-C * B + B * C) * C
  calc
    doubleModularCommutator P A B =
        C * C * B - C * B * C - C * B * C + B * (C * C) := by
      rw [hsq, hmid]
      simp only [doubleModularCommutator]
      noncomm_ring
    _ = _ := by noncomm_ring

def unitaryEnergy (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) (t : ℝ) : ℝ :=
  (omegaState P (unitaryConjugation P A B t)).re

def unitaryEnergyVelocity (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) (t : ℝ) : ℝ :=
  (omegaState P (unitaryConjugationVelocity P A B t)).re

theorem unitary_energy_derivative (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : IsSelfAdjoint A) (t : ℝ) :
    HasDerivAt (unitaryEnergy P A B) (unitaryEnergyVelocity P A B t) t := by
  have h := (omegaRealContinuous P).hasFDerivAt.comp_hasDerivAt t
    (unitary_conjugation_has_derivative P A B hA t)
  convert h using 1
  all_goals rfl

theorem unitary_energy_velocity_zero (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) :
    unitaryEnergyVelocity P A B 0 = (Complex.I * omegaState P (B*A-A*B)).re := by
  have h : unitaryConjugationVelocity P A B 0 = Complex.I • (B*A-A*B) := by
    simp only [unitaryConjugationVelocity, neg_zero, bounded_phase_zero, one_mul, mul_one,
      smul_mul_assoc, mul_smul_comm, smul_sub]
    module
  rw [unitaryEnergyVelocity, h, omega_state_smul]

theorem unitary_energy_velocity_derivative (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) :
    HasDerivAt (unitaryEnergyVelocity P A B)
      (omegaState P (doubleModularCommutator P A B)).re 0 := by
  have h := (omegaRealContinuous P).hasFDerivAt.comp_hasDerivAt 0
    (unitary_velocity_derivative_zero P A B)
  convert h using 1
  all_goals rfl

theorem unitary_energy_second_derivative (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : IsSelfAdjoint A) :
    HasDerivAt (deriv (unitaryEnergy P A B))
      (omegaState P (doubleModularCommutator P A B)).re 0 := by
  have he : deriv (unitaryEnergy P A B) = unitaryEnergyVelocity P A B := by
    funext t
    exact (unitary_energy_derivative P A B hA t).deriv
  rw [he]
  exact unitary_energy_velocity_derivative P A B

/-- Second-order response from actual derivatives, with the factor one half explicit. -/
theorem quadratic_response_from_velocity (f v : ℝ → ℝ) (c : ℝ)
    (hf : ∀ t, HasDerivAt f (v t) t) (hv : HasDerivAt v c 0) (hv0 : v 0=0) :
    Tendsto (fun t => (f t-f 0)/t^2) (𝓝[≠] 0) (𝓝 (c/2)) := by
  have hvs : Tendsto (fun t => v t/t) (𝓝[≠] 0) (𝓝 c) := by
    simpa only [zero_add, hv0, sub_zero, smul_eq_mul, div_eq_mul_inv, mul_comm]
      using hv.tendsto_slope_zero
  have hderiv : ∀ᶠ t in 𝓝[≠] (0:ℝ), HasDerivAt (fun s => f s-f 0) (v t) t :=
    Filter.Eventually.of_forall (fun t => (hf t).sub_const (f 0))
  have hg : ∀ᶠ t in 𝓝[≠] (0:ℝ),
      HasDerivAt (fun s : ℝ => s^2) (2*t) t :=
    Filter.Eventually.of_forall (fun t => by
      convert (hasDerivAt_id t).pow 2 using 1
      all_goals norm_num
      all_goals rfl)
  have hgn : ∀ᶠ t in 𝓝[≠] (0:ℝ), 2*t≠0 := by
    filter_upwards [self_mem_nhdsWithin] with t ht
    exact mul_ne_zero (by norm_num) ht
  have hfzero : Tendsto (fun t => f t-f 0) (𝓝[≠] 0) (𝓝 0) := by
    simpa only [sub_self] using ((hf 0).continuousAt.sub_const (f 0)).mono_left
      nhdsWithin_le_nhds
  have hgzero : Tendsto (fun t : ℝ => t^2) (𝓝[≠] 0) (𝓝 0) := by
    simpa using ((continuousAt_id : ContinuousAt (fun t : ℝ => t) 0).pow 2).tendsto.mono_left
      nhdsWithin_le_nhds
  have hratio : Tendsto (fun t => v t/(2*t)) (𝓝[≠] 0) (𝓝 (c/2)) := by
    simpa only [mul_comm (2:ℝ), div_mul_eq_div_div] using hvs.div_const (2:ℝ)
  exact HasDerivAt.lhopital_zero_nhdsNE hderiv hg hgn hfzero hgzero hratio

def localModularMatrix (P : SiteProfile) (N : ℕ) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  Matrix.diagonal (fun i => ((-Real.log (towerW P N i) : ℝ) : ℂ))

def localModularObservable (P : SiteProfile) (N : ℕ) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  towerPi P (localModularMatrix P N)

def finiteModularEnergy (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) : ℝ → ℝ :=
  unitaryEnergy P (towerPi P a) (localModularObservable P N)

theorem local_modular_matrix_hermitian (P : SiteProfile) (N : ℕ) :
    (localModularMatrix P N).IsHermitian := by
  ext i j
  by_cases h : i=j
  · subst j
    simp [localModularMatrix]
  · simp [localModularMatrix, Matrix.diagonal, h, Ne.symm h]

theorem local_modular_commutator_state (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    omegaState P (localModularObservable P N * towerPi P a -
      towerPi P a * localModularObservable P N)=0 := by
  have hm : towerPi P (localModularMatrix P N*a-a*localModularMatrix P N) =
      localModularObservable P N*towerPi P a-towerPi P a*localModularObservable P N := by
    change (towerPiAlgHom P N) (_-_) = _
    simp only [map_sub, map_mul]
    rfl
  rw [← hm, omegaState_pi]
  simp [tState, localModularMatrix, Matrix.sub_apply, Matrix.diagonal_mul,
    Matrix.mul_diagonal, mul_comm]

theorem finite_modular_energy_first_zero (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) :
    HasDerivAt (finiteModularEnergy P N a) 0 0 := by
  have h := unitary_energy_derivative P (towerPi P a) (localModularObservable P N)
    (tower_local_selfadjoint P N a ha) 0
  simpa only [unitary_energy_velocity_zero, local_modular_commutator_state,
    mul_zero, Complex.zero_re, finiteModularEnergy] using h

theorem local_modular_double_coefficient (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) :
    (omegaState P (doubleModularCommutator P (towerPi P a)
      (localModularObservable P N))).re = 2 * localModularCost P N a := by
  let k := localModularMatrix P N
  have hm : towerPi P (-(a*a*k)+a*k*a+a*k*a-k*(a*a)) =
      doubleModularCommutator P (towerPi P a) (localModularObservable P N) := by
    change (towerPiAlgHom P N) (-(a*a*k)+a*k*a+a*k*a-k*(a*a)) = _
    simp only [map_sub, map_add, map_neg, map_mul]
    rfl
  rw [← hm, omegaState_pi]
  have hright (b : Matrix (chainIdx N) (chainIdx N) ℂ) (i j : chainIdx N) :
      (b*k) i j = b i j * ((-Real.log (towerW P N j) : ℝ) : ℂ) := by
    change (b * Matrix.diagonal (fun j =>
      ((-Real.log (towerW P N j) : ℝ) : ℂ))) i j = _
    exact Matrix.mul_diagonal _ _ _ _
  have hleft (b : Matrix (chainIdx N) (chainIdx N) ℂ) (i j : chainIdx N) :
      (k*b) i j = ((-Real.log (towerW P N i) : ℝ) : ℂ) * b i j := by
    change (Matrix.diagonal (fun i =>
      ((-Real.log (towerW P N i) : ℝ) : ℂ)) * b) i j = _
    exact Matrix.diagonal_mul _ _ _ _
  have hmiddle (i : chainIdx N) :
      (a*k*a) i i = ∑ j,
        (a i j * ((-Real.log (towerW P N j) : ℝ) : ℂ)) * a j i := by
    rw [Matrix.mul_apply]
    apply Finset.sum_congr rfl
    intro j _
    rw [hright]
  have hd (i : chainIdx N) :
      (-(a*a*k)+a*k*a+a*k*a-k*(a*a)) i i =
        ∑ j, ((2*(Real.log (towerW P N i)-Real.log (towerW P N j)) : ℝ) : ℂ) *
          (Complex.normSq (a i j) : ℂ) := by
    simp only [Matrix.sub_apply, Matrix.add_apply, Matrix.neg_apply]
    rw [hright, hleft]
    simp only [hmiddle]
    simp only [Matrix.mul_apply]
    rw [Finset.sum_mul, Finset.mul_sum]
    rw [← Finset.sum_neg_distrib, ← Finset.sum_add_distrib,
      ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro j _
    have hji : a j i = star (a i j) := by
      simpa only [Matrix.conjTranspose_apply] using
        (congrFun (congrFun ha j) i).symm
    have hprod : a i j * a j i = (Complex.normSq (a i j) : ℂ) := by
      rw [hji, Complex.star_def, Complex.mul_conj]
    calc
      _ = ((2*(Real.log (towerW P N i)-Real.log (towerW P N j)) : ℝ) : ℂ) *
          (a i j * a j i) := by
        push_cast
        ring
      _ = _ := by rw [hprod]
  have hn (i j : chainIdx N) : Complex.normSq (a j i)=Complex.normSq (a i j) := by
    simpa only [Matrix.conjTranspose_apply, Complex.star_def, Complex.normSq_conj] using
      congrArg Complex.normSq (congrFun (congrFun ha i) j)
  have hswap :
      (∑ i, ∑ j, towerW P N j *
        (Real.log (towerW P N i)-Real.log (towerW P N j))*Complex.normSq (a i j)) =
      -(∑ i, ∑ j, towerW P N i *
        (Real.log (towerW P N i)-Real.log (towerW P N j))*Complex.normSq (a i j)) := by
    rw [Finset.sum_comm]
    simp only [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intro j _
    rw [hn]
    ring
  have he :
      (∑ i, ∑ j, (towerW P N i-towerW P N j) *
        (Real.log (towerW P N i)-Real.log (towerW P N j))*Complex.normSq (a i j)) =
      2 * ∑ i, ∑ j, towerW P N i *
        (Real.log (towerW P N i)-Real.log (towerW P N j))*Complex.normSq (a i j) := by
    simp only [sub_mul, Finset.sum_sub_distrib]
    rw [hswap]
    ring
  have hre (f : chainIdx N → ℂ) : (∑ i, f i).re = ∑ i, (f i).re :=
    map_sum Complex.reAddGroupHom f Finset.univ
  have htrace :
      (tState P N (-(a*a*k)+a*k*a+a*k*a-k*(a*a))).re =
      2 * ∑ i, ∑ j, towerW P N i *
        (Real.log (towerW P N i)-Real.log (towerW P N j))*Complex.normSq (a i j) := by
    simp only [tState, hd, Finset.mul_sum]
    simp only [hre]
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intro j _
    rw [← Complex.ofReal_mul, ← Complex.ofReal_mul, Complex.ofReal_re]
    ring
  rw [htrace, local_modular_cost_symmetric P N a ha, he]
  ring

theorem finite_modular_energy_second (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) :
    HasDerivAt (deriv (finiteModularEnergy P N a)) (2*localModularCost P N a) 0 := by
  simpa only [finiteModularEnergy, local_modular_double_coefficient P N a ha] using
    unitary_energy_second_derivative P (towerPi P a) (localModularObservable P N)
      (tower_local_selfadjoint P N a ha)

theorem finite_modular_energy_quadratic_limit (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) :
    Tendsto (fun t => (finiteModularEnergy P N a t-finiteModularEnergy P N a 0)/t^2)
      (𝓝[≠] 0) (𝓝 (localModularCost P N a)) := by
  have hv := unitary_energy_velocity_derivative P (towerPi P a) (localModularObservable P N)
  rw [local_modular_double_coefficient P N a ha] at hv
  have hv0 : unitaryEnergyVelocity P (towerPi P a) (localModularObservable P N) 0=0 := by
    rw [unitary_energy_velocity_zero, local_modular_commutator_state, mul_zero, Complex.zero_re]
  have h := quadratic_response_from_velocity _ _ _
    (unitary_energy_derivative P (towerPi P a) (localModularObservable P N)
      (tower_local_selfadjoint P N a ha)) hv hv0
  have he : 2*localModularCost P N a/2=localModularCost P N a := by ring
  rw [he] at h
  exact h

/-- The extended global cost equals half the actual local energy second derivative. -/
theorem global_cost_is_modular_response (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) :
    towerModularCost P (towerPi P a (hOmega P)) =
      ENNReal.ofReal (deriv (deriv (finiteModularEnergy P N a)) 0/2) := by
  rw [(finite_modular_energy_second P N a ha).deriv, tower_local_cost_formula P N a ha]
  congr 1
  ring

#print axioms omegaRealContinuous
#print axioms omega_real_continuous_apply
#print axioms bounded_phase_negative_generator
#print axioms negative_phase_derivative
#print axioms unitaryConjugationVelocity
#print axioms unitary_conjugation_has_derivative
#print axioms doubleModularCommutator
#print axioms unitary_velocity_derivative_zero
#print axioms unitaryEnergy
#print axioms unitaryEnergyVelocity
#print axioms unitary_energy_derivative
#print axioms unitary_energy_velocity_zero
#print axioms unitary_energy_velocity_derivative
#print axioms unitary_energy_second_derivative
#print axioms quadratic_response_from_velocity
#print axioms localModularMatrix
#print axioms localModularObservable
#print axioms finiteModularEnergy
#print axioms local_modular_matrix_hermitian
#print axioms local_modular_commutator_state
#print axioms finite_modular_energy_first_zero
#print axioms local_modular_double_coefficient
#print axioms finite_modular_energy_second
#print axioms finite_modular_energy_quadratic_limit
#print axioms global_cost_is_modular_response
end
end ChatgptAudit.Cost054
