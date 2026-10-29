import TGLExt.Cocycle

set_option autoImplicit false

/-!
# T1 na face finita: dephasing ergódico → esperança diagonal
  [TGLExt — a sombra finita da ergodicidade]

HONESTIDADE. Este arquivo é a SOMBRA FINITA da ergodicidade (v11 da casa:
`T_t → E_0`, setor fixo = centralizador, o traço emerge). O que fica
provado [KERNEL], com estados e taxas GENÉRICOS:

* (G0) FIXO PELO FLUXO: `Commute ρ x → σₜ(x) = x` — quem comuta com o
  estado é estacionário sob o fluxo modular;
* (G1) O CENTRALIZADOR DA DIAGONAL NÃO-DEGENERADA: `log ρ_D`, `ρ_D^{it}`
  e `σₜ` de `ρ_D = diag(d)` em forma fechada, e o IFF ALGÉBRICO
  `(∀ t, σₜ(x) = x) ↔ x = E_D(x)` — o setor fixo do fluxo É o
  centralizador (sem derivadas: o golpe é `t★ = π/(log dᵢ − log dⱼ)`,
  `e^{iπ} = −1`);
* (G2) O TRAÇO EMERGE NO CENTRALIZADOR: `ω(x·y) = ω(y·x)` para `x` que
  comuta com `ρ` — o selo tracial do setor fixo vira teorema;
* (G3) O SEMIGRUPO DE DEPHASING E A CONVERGÊNCIA ERGÓDICA:
  `(T_t x)ᵢⱼ = e^{−t·g i j}·xᵢⱼ` é semigrupo (`T_0 = id`,
  `T_{s+t} = T_s ∘ T_t`), fixa a diagonal, PRESERVA a diagonal, e
  `T_t(x) → E_D(x)` em `t → ∞` — o TEOREMA ERGÓDICO COM LIMITE; com
  `g := modularGap d = |log dᵢ − log dⱼ|` fecha a LIGAÇÃO MODULAR.

O que NÃO está aqui (e SEGUE onde está): o MIXING FORTE contínuo sob a
classe de Davies (N3) e a ergodicidade III₁ genuína (GLOBAL_LIFT) — o
teorema aberto do programa; a subordinação Poisson–Cauchy segue
certificada FORA do kernel. β JAMAIS entra no Lean: as taxas `g` são
GENÉRICAS — a taxa física `β·|log λᵢ − log λⱼ|` (classe de Davies) é
leitura de RUNTIME. Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix NormedSpace Filter

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ## G0 — fixo pelo fluxo: o comutante do estado é estacionário -/

/-- [KERNEL] FIXO PELO FLUXO: se `x` comuta com `ρ`, então `σₜ(x) = x`
    para todo `t` — o comutante do estado é o setor ESTACIONÁRIO do
    movimento modular. Rota: `Commute ρ x → Commute (log ρ) x`
    (`Commute.cfc_real`) `→ Commute ρ^{it} x` (`smul` + `exp`), e então
    `ρ^{it}·x·ρ^{-it} = x·ρ^{it}·ρ^{-it} = x`. -/
theorem sigma_fixed_of_commute (rho x : Matrix n n ℂ) (h : Commute rho x) (t : ℝ) :
    sigma rho t x = x := by
  have h1 : Commute (logRho rho) x := h.cfc_real Real.log
  have h2 : Commute (modPow rho t) x := by
    unfold modPow
    exact (h1.smul_left ((t : ℂ) * Complex.I)).exp_left
  simp only [sigma]
  rw [h2.eq, mul_assoc, modPow_mul_neg, mul_one]

/-! ## G1 — o centralizador da diagonal não-degenerada -/

/-- O estado diagonal `ρ_D = diag(d)` com pesos reais `d` — o modelo
    finito do estado de referência não-degenerado. -/
def rhoD (d : n → ℝ) : Matrix n n ℂ := diagonal fun i => (d i : ℂ)

section LogDiagonal

open scoped Matrix.Norms.L2Operator

/-- Ancoragem exponencial: `exp(diag(log d)) = ρ_D` para pesos positivos
    (`Matrix.exp_diagonal` + `Real.exp_log`, entrada a entrada). -/
theorem exp_diagonal_log (d : n → ℝ) (hd : ∀ i, 0 < d i) :
    exp (diagonal fun i => (Real.log (d i) : ℂ)) = rhoD d := by
  unfold rhoD
  rw [Matrix.exp_diagonal]
  congr 1
  funext i
  simp only [Pi.coe_exp]
  rw [← Complex.exp_eq_exp_ℂ, ← Complex.ofReal_exp, Real.exp_log (hd i)]

/-- [KERNEL] (G1a) O GERADOR DA DIAGONAL: `log(ρ_D) = diag(log d)` — o
    cálculo funcional contínuo desce à diagonal. Rota inversa por
    exponencial: `log(exp D) = D` (`CFC.log_exp`) com `D = diag(log d)`
    autoadjunta (entradas reais). -/
theorem logRho_diagonal (d : n → ℝ) (hd : ∀ i, 0 < d i) :
    logRho (rhoD d) = diagonal fun i => (Real.log (d i) : ℂ) := by
  have hv : IsSelfAdjoint (fun i => (Real.log (d i) : ℂ)) := by
    rw [isSelfAdjoint_iff]
    funext i
    simp
  have hsa : IsSelfAdjoint (diagonal fun i => (Real.log (d i) : ℂ)) :=
    (isHermitian_diagonal_of_self_adjoint _ hv).isSelfAdjoint
  rw [← exp_diagonal_log d hd]
  exact CFC.log_exp _ hsa

end LogDiagonal

/-- [KERNEL] (G1b) O UNITÁRIO MODULAR DA DIAGONAL:
    `ρ_D^{it} = diag(e^{it·log dᵢ})` — o fluxo da diagonal é fase pura,
    modo a modo (`exp_diagonal` sobre `logRho_diagonal`). -/
theorem modPow_diagonal (d : n → ℝ) (hd : ∀ i, 0 < d i) (t : ℝ) :
    modPow (rhoD d) t
      = diagonal fun i => Complex.exp ((t : ℂ) * Complex.I * (Real.log (d i) : ℂ)) := by
  unfold modPow
  rw [logRho_diagonal d hd, ← diagonal_smul, Matrix.exp_diagonal]
  congr 1
  funext i
  simp only [Pi.coe_exp, Pi.smul_apply, smul_eq_mul, ← Complex.exp_eq_exp_ℂ]

/-- [KERNEL] (G1c) O FLUXO DA DIAGONAL, ENTRADA A ENTRADA:
    `σₜ(x)ᵢⱼ = e^{it(log dᵢ − log dⱼ)}·xᵢⱼ` — cada entrada fora da
    diagonal gira com a DIFERENÇA MODULAR dos pesos; a diagonal não gira. -/
theorem sigma_diagonal_apply (d : n → ℝ) (hd : ∀ i, 0 < d i) (t : ℝ)
    (x : Matrix n n ℂ) (i j : n) :
    sigma (rhoD d) t x i j
      = Complex.exp ((t : ℂ) * Complex.I
          * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ))) * x i j := by
  have harg : (t : ℂ) * Complex.I * (Real.log (d i) : ℂ)
      + ((-t : ℝ) : ℂ) * Complex.I * (Real.log (d j) : ℂ)
      = (t : ℂ) * Complex.I * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ)) := by
    push_cast
    ring
  simp only [sigma, modPow_diagonal d hd, diagonal_mul, mul_diagonal]
  rw [mul_right_comm, ← Complex.exp_add, harg]

/-- [KERNEL] (G1d) O IFF DO CENTRALIZADOR: para a diagonal
    NÃO-DEGENERADA (pesos positivos e injetivos), o setor fixo do fluxo
    modular é EXATAMENTE a subálgebra diagonal:
    `(∀ t, σₜ(x) = x) ↔ x = E_D(x)`.
    (⇒) sem derivadas: para `i ≠ j`, `log dᵢ ≠ log dⱼ` (log injetivo em
    positivos); em `t★ = π/(log dᵢ − log dⱼ)` o fator vira
    `e^{iπ} = −1`, logo `xᵢⱼ = −xᵢⱼ = 0`. (⇐) de G0: a diagonal comuta
    com a diagonal. -/
theorem sigma_fixed_iff_diag (d : n → ℝ) (hd : ∀ i, 0 < d i)
    (hinj : Function.Injective d) (x : Matrix n n ℂ) :
    (∀ t, sigma (rhoD d) t x = x) ↔ x = diagExpect x := by
  constructor
  · intro h
    ext i j
    by_cases hij : i = j
    · subst hij
      simp [diagExpect, diag_apply]
    · have hlog : Real.log (d i) ≠ Real.log (d j) := fun hc =>
        hij (hinj (Real.log_injOn_pos (Set.mem_Ioi.mpr (hd i))
          (Set.mem_Ioi.mpr (hd j)) hc))
      have hr : Real.log (d i) - Real.log (d j) ≠ 0 := sub_ne_zero.mpr hlog
      have hkey : Complex.exp (((Real.pi / (Real.log (d i) - Real.log (d j)) : ℝ) : ℂ)
          * Complex.I * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ))) * x i j
          = x i j := by
        rw [← sigma_diagonal_apply d hd (Real.pi / (Real.log (d i) - Real.log (d j))) x i j]
        exact Matrix.ext_iff.mpr (h _) i j
      have harg : ((Real.pi / (Real.log (d i) - Real.log (d j)) : ℝ) : ℂ)
          * Complex.I * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ))
          = (Real.pi : ℂ) * Complex.I := by
        rw [mul_right_comm, ← Complex.ofReal_sub, ← Complex.ofReal_mul,
          div_mul_cancel₀ _ hr]
      rw [harg, Complex.exp_pi_mul_I, neg_one_mul] at hkey
      have hx0 : x i j = 0 := add_self_eq_zero.mp (neg_eq_iff_add_eq_zero.mp hkey)
      rw [hx0]
      exact (diagonal_apply_ne _ hij).symm
  · intro hx t
    rw [hx]
    exact sigma_fixed_of_commute _ _ (commute_diagonal _ _) t

/-! ## G2 — o traço emerge no centralizador -/

omit [DecidableEq n] in
/-- [KERNEL] (G2) O TRAÇO EMERGE: no centralizador o estado de Gibbs é
    TRACIAL — `ω(x·y) = ω(y·x)` sempre que `x` comuta com `ρ`
    (`Tr(ρxy) = Tr(xρy) = Tr(ρyx)` pelo ciclo do traço). O selo do setor
    fixo vira teorema: sobre o centralizador, ω esquece a modularidade. -/
theorem gibbs_tracial_on_centralizer (rho x y : Matrix n n ℂ) (hx : Commute rho x) :
    gibbs rho (x * y) = gibbs rho (y * x) := by
  simp only [gibbs]
  rw [← mul_assoc, hx.eq, mul_assoc, Matrix.trace_mul_comm, ← mul_assoc]

/-! ## G3 — o semigrupo de dephasing e a convergência ergódica -/

/-- O SEMIGRUPO DE DEPHASING com taxas genéricas `g`:
    `(T_t x)ᵢⱼ = e^{−t·g i j}·xᵢⱼ` — amortecimento entrada a entrada
    (Schur puro; `x` genérico, sem positividade). A taxa FÍSICA da classe
    de Davies é `β·|log λᵢ − log λⱼ|`; β é leitura de runtime, JAMAIS
    entra aqui. -/
def dephase (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) : Matrix n n ℂ :=
  Matrix.of fun i j => (Real.exp (-(t * g i j)) : ℂ) * x i j

omit [Fintype n] [DecidableEq n] in
/-- (G3a) `T_0 = id`: em tempo zero nada amorteceu. -/
theorem dephase_zero (g : n → n → ℝ) (x : Matrix n n ℂ) : dephase g 0 x = x := by
  ext i j
  simp [dephase]

omit [Fintype n] [DecidableEq n] in
/-- [KERNEL] (G3b) LEI DE SEMIGRUPO: `T_{s+t} = T_s ∘ T_t` — o dephasing
    compõe somando tempos (`e^{−(s+t)g} = e^{−sg}·e^{−tg}`). -/
theorem dephase_add (g : n → n → ℝ) (s t : ℝ) (x : Matrix n n ℂ) :
    dephase g (s + t) x = dephase g s (dephase g t x) := by
  ext i j
  have harg : -((s + t) * g i j) = -(s * g i j) + -(t * g i j) := by ring
  simp only [dephase, Matrix.of_apply]
  rw [harg, Real.exp_add, Complex.ofReal_mul, mul_assoc]

omit [Fintype n] in
/-- [KERNEL] (G3c) O SETOR FIXO NÃO MOVE: `T_t(E_D(x)) = E_D(x)` — a
    diagonal é ponto fixo do dephasing (`g i i = 0` na diagonal;
    fora dela já é zero). -/
theorem dephase_fixes_diagonal (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ)
    (x : Matrix n n ℂ) : dephase g t (diagExpect x) = diagExpect x := by
  ext i j
  by_cases hij : i = j
  · subst hij
    simp [dephase, diagExpect, hg0 i, diag_apply]
  · simp [dephase, diagExpect, diagonal_apply_ne _ hij]

omit [Fintype n] in
/-- [KERNEL] (G3d) A DIAGONAL É INVARIANTE: `E_D(T_t(x)) = E_D(x)` — o
    dephasing não transporta peso para dentro nem para fora do setor
    fixo (compatibilidade `T_t`–`E_D`, a face finita da esperança
    condicional invariante). -/
theorem diag_invariant (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ)
    (x : Matrix n n ℂ) : diagExpect (dephase g t x) = diagExpect x := by
  ext i j
  by_cases hij : i = j
  · subst hij
    simp [diagExpect, dephase, hg0 i, diag_apply]
  · simp [diagExpect, diagonal_apply_ne _ hij]

omit [Fintype n] in
/-- [KERNEL] (G3e) O TEOREMA ERGÓDICO COM LIMITE: com taxas positivas
    fora da diagonal, `T_t(x) → E_D(x)` quando `t → ∞` — o dephasing
    CONVERGE para a esperança condicional diagonal. A sombra finita de
    `T_t → E_0` (v11 da casa): decaimento real `e^{−tg} → 0` entrada a
    entrada, levado a ℂ por continuidade. -/
theorem dephase_tendsto_expectation (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0)
    (hgpos : ∀ i j, i ≠ j → 0 < g i j) (x : Matrix n n ℂ) :
    Tendsto (fun t => dephase g t x) atTop (nhds (diagExpect x)) := by
  refine tendsto_pi_nhds.mpr fun i => tendsto_pi_nhds.mpr fun j => ?_
  by_cases hij : i = j
  · subst hij
    have hconst : (fun t : ℝ => dephase g t x i i) = fun _ => x i i := by
      funext t
      simp [dephase, hg0 i]
    have hdiag : diagExpect x i i = x i i := by
      simp [diagExpect, diag_apply]
    rw [hconst, hdiag]
    exact tendsto_const_nhds
  · have hzero : diagExpect x i j = 0 := diagonal_apply_ne _ hij
    rw [hzero]
    have h1 : Tendsto (fun t : ℝ => t * g i j) atTop atTop :=
      Tendsto.atTop_mul_const (hgpos i j hij) tendsto_id
    have h2 : Tendsto (fun t : ℝ => Real.exp (-(t * g i j))) atTop (nhds 0) :=
      Real.tendsto_exp_neg_atTop_nhds_zero.comp h1
    have h3 : Tendsto (fun t : ℝ => (Real.exp (-(t * g i j)) : ℂ)) atTop (nhds 0) := by
      simpa using h2.ofReal
    simpa [dephase] using h3.mul_const (x i j)

/-! ## G3f — a ligação modular: a taxa é o gap dos logaritmos -/

/-- O GAP MODULAR da diagonal: `modularGap d i j = |log dᵢ − log dⱼ|` — a
    forma GENÉRICA da taxa de Davies. A taxa física é `β·modularGap`
    (reparametrização de runtime; β jamais entra no Lean). -/
def modularGap (d : n → ℝ) (i j : n) : ℝ := |Real.log (d i) - Real.log (d j)|

omit [Fintype n] [DecidableEq n] in
/-- O gap modular zera na diagonal. -/
theorem modularGap_diag_zero (d : n → ℝ) (i : n) : modularGap d i i = 0 := by
  simp [modularGap]

omit [Fintype n] [DecidableEq n] in
/-- Para pesos positivos e injetivos, o gap modular é POSITIVO fora da
    diagonal (log é injetivo em positivos). -/
theorem modularGap_pos (d : n → ℝ) (hd : ∀ i, 0 < d i)
    (hinj : Function.Injective d) {i j : n} (hij : i ≠ j) :
    0 < modularGap d i j := by
  unfold modularGap
  rw [abs_pos]
  exact sub_ne_zero.mpr fun hc =>
    hij (hinj (Real.log_injOn_pos (Set.mem_Ioi.mpr (hd i)) (Set.mem_Ioi.mpr (hd j)) hc))

omit [Fintype n] in
/-- [KERNEL] (G3f) CONVERGÊNCIA ERGÓDICA MODULAR: com a taxa
    `g = modularGap d` da diagonal não-degenerada, o dephasing converge
    para a esperança diagonal — G3e com o gap dos logaritmos. A taxa
    física da classe de Davies é `β·modularGap` (β = leitura de runtime). -/
theorem ergodic_convergence_modular (d : n → ℝ) (hd : ∀ i, 0 < d i)
    (hinj : Function.Injective d) (x : Matrix n n ℂ) :
    Tendsto (fun t => dephase (modularGap d) t x) atTop (nhds (diagExpect x)) :=
  dephase_tendsto_expectation (modularGap d) (modularGap_diag_zero d)
    (fun _ _ hij => modularGap_pos d hd hinj hij) x

end

end TGLExt
