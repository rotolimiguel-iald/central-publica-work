import TGLExt.EquivariantSection
import Mathlib.Analysis.SpecificLimits.Basic

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000

/-!
# O LIMITE ERGÓDICO: a média de Birkhoff CONVERGE para a seção
  [TGLExt — item A da ordem de fechamento: a condicional «seção
   ergódica» ganha o seu conteúdo ERGÓDICO em kernel]

O v166 (`EquivariantSection`) provou a ÁLGEBRA da seção (esperança,
centralizador, fixidez, equivariância). Faltava o que faz dela
ERGÓDICA: o LIMITE. Esta pedra o prova — a média de Birkhoff do fluxo
modular converge, entrada a entrada, para `specExpect`:

* ★★ `birkhoff_tendsto_specExpect` — para um passo RESOLVENTE `s`
  (que «vê» cada par de pesos distintos: `e^{isΔ} ≠ 1`), a média
  `(1/N) ∑_{k<N} σ_{ks}(x)` TENDE a `specExpect d x` quando `N → ∞`.
  Rota: cada entrada é geométrica (`σ_{ks}(x)ᵢⱼ = zᵏ xᵢⱼ` com
  `z = e^{isΔᵢⱼ}`, `|z| = 1`); pares iguais dão média constante;
  pares distintos somam `(z^N−1)/(z−1)`, com norma `≤ 2/‖z−1‖`,
  esmagada por `1/N` — o cancelamento de fase É a ergodicidade;
* ★ `birkhoff_limit_equivariant` — o LIMITE herda a equivariância da
  seção (com o v166): a média ergódica de uma simetria do estado é a
  simetria da média — a SEÇÃO ERGÓDICA EQUIVARIANTE, com limite e
  tudo, em kernel.

HONESTIDADE: face finita, passo resolvente como hipótese NOMEADA (o
genérico a satisfaz; o contínuo de Davies/N3 e a subordinação
Poisson–Cauchy seguem onde estão). β JAMAIS entra no Lean. Sem sorry,
sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix Filter

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-- A fase elementar do par `(i,j)` sob o passo `s`:
    `z = e^{i·s·(log dᵢ − log dⱼ)}`. -/
def stepPhase (d : n → ℝ) (s : ℝ) (i j : n) : ℂ :=
  Complex.exp ((s : ℂ) * Complex.I
    * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ)))

/-- A fase elementar tem MÓDULO 1: o fluxo não pesa, só gira. -/
theorem stepPhase_abs (d : n → ℝ) (s : ℝ) (i j : n) :
    ‖stepPhase d s i j‖ = 1 := by
  unfold stepPhase
  rw [Complex.norm_exp]
  have hre : ((s : ℂ) * Complex.I
      * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ))).re = 0 := by
    simp [Complex.mul_re, Complex.mul_im]
  rw [hre, Real.exp_zero]

/-- A entrada da órbita é GEOMÉTRICA: `σ_{k·s}(x)ᵢⱼ = zᵏ·xᵢⱼ`. -/
theorem sigma_step_pow (d : n → ℝ) (hd : ∀ i, 0 < d i) (s : ℝ) (k : ℕ)
    (x : Matrix n n ℂ) (i j : n) :
    sigma (rhoD d) ((k : ℝ) * s) x i j = stepPhase d s i j ^ k * x i j := by
  rw [sigma_diagonal_apply d hd ((k : ℝ) * s) x i j]
  unfold stepPhase
  rw [← Complex.exp_nat_mul]
  congr 2
  push_cast
  ring

/-- ★★ O TEOREMA ERGÓDICO DA SEÇÃO: com passo resolvente `s`, a média
    de Birkhoff do fluxo modular converge para `specExpect`, entrada a
    entrada. O cancelamento de fase é a ergodicidade. -/
theorem birkhoff_tendsto_specExpect (d : n → ℝ) (hd : ∀ i, 0 < d i)
    (s : ℝ) (hs : ∀ i j : n, d i ≠ d j → stepPhase d s i j ≠ 1)
    (x : Matrix n n ℂ) (i j : n) :
    Tendsto (fun N : ℕ => ((N : ℂ))⁻¹
        * ∑ k ∈ Finset.range N, sigma (rhoD d) ((k : ℝ) * s) x i j)
      atTop (nhds (specExpect d x i j)) := by
  have hgeo : ∀ N : ℕ, ((N : ℂ))⁻¹
      * ∑ k ∈ Finset.range N, sigma (rhoD d) ((k : ℝ) * s) x i j
      = ((N : ℂ))⁻¹ * (∑ k ∈ Finset.range N, stepPhase d s i j ^ k) * x i j := by
    intro N
    rw [mul_assoc]
    congr 1
    rw [Finset.sum_mul]
    exact Finset.sum_congr rfl fun k _ => sigma_step_pow d hd s k x i j
  by_cases hdij : d i = d j
  · -- fase 1: a média é constante = x i j = specExpect
    have hz : stepPhase d s i j = 1 := by
      unfold stepPhase
      rw [hdij, sub_self, mul_zero, Complex.exp_zero]
    have hconst : ∀ N : ℕ, 1 ≤ N → ((N : ℂ))⁻¹
        * ∑ k ∈ Finset.range N, sigma (rhoD d) ((k : ℝ) * s) x i j
        = x i j := by
      intro N hN
      rw [hgeo N, hz]
      simp only [one_pow, Finset.sum_const, Finset.card_range, nsmul_eq_mul, mul_one]
      have hN0 : ((N : ℂ)) ≠ 0 := by
        exact_mod_cast Nat.one_le_iff_ne_zero.mp hN
      rw [inv_mul_cancel₀ hN0, one_mul]
    have hspec : specExpect d x i j = x i j := by simp [hdij]
    rw [hspec]
    refine Tendsto.congr' ?_ tendsto_const_nhds
    filter_upwards [eventually_ge_atTop 1] with N hN
    exact (hconst N hN).symm
  · -- fase ≠ 1: soma geométrica esmagada por 1/N
    have hz1 : stepPhase d s i j ≠ 1 := hs i j hdij
    have hc : (0 : ℝ) < ‖stepPhase d s i j - 1‖ :=
      norm_pos_iff.mpr (sub_ne_zero.mpr hz1)
    have hspec : specExpect d x i j = 0 := by simp [hdij]
    rw [hspec]
    have hnorm : ∀ N : ℕ, 1 ≤ N →
        ‖((N : ℂ))⁻¹ * ∑ k ∈ Finset.range N, sigma (rhoD d) ((k : ℝ) * s) x i j‖
        ≤ (2 / ‖stepPhase d s i j - 1‖ * ‖x i j‖) / (N : ℝ) := by
      intro N hN
      rw [hgeo N, geom_sum_eq hz1]
      rw [norm_mul, norm_mul, norm_inv, Complex.norm_natCast, norm_div]
      have hzN : ‖stepPhase d s i j ^ N - 1‖ ≤ 2 := by
        calc ‖stepPhase d s i j ^ N - 1‖
            ≤ ‖stepPhase d s i j ^ N‖ + ‖(1 : ℂ)‖ := norm_sub_le _ _
          _ = 1 + 1 := by rw [norm_pow, stepPhase_abs, one_pow, norm_one]
          _ = 2 := by norm_num
      have hNpos : (0 : ℝ) < (N : ℝ) := by exact_mod_cast hN
      have hfac : (0 : ℝ) ≤ ‖stepPhase d s i j - 1‖⁻¹ * ‖x i j‖ * ((N : ℝ))⁻¹ :=
        mul_nonneg (mul_nonneg (inv_nonneg.mpr (norm_nonneg _)) (norm_nonneg _))
          (inv_nonneg.mpr hNpos.le)
      calc ((N : ℝ))⁻¹ * (‖stepPhase d s i j ^ N - 1‖ / ‖stepPhase d s i j - 1‖)
            * ‖x i j‖
          = ‖stepPhase d s i j ^ N - 1‖
              * (‖stepPhase d s i j - 1‖⁻¹ * ‖x i j‖ * ((N : ℝ))⁻¹) := by ring
        _ ≤ 2 * (‖stepPhase d s i j - 1‖⁻¹ * ‖x i j‖ * ((N : ℝ))⁻¹) :=
            mul_le_mul_of_nonneg_right hzN hfac
        _ = 2 / ‖stepPhase d s i j - 1‖ * ‖x i j‖ / (N : ℝ) := by ring
    have hg : Tendsto (fun N : ℕ =>
        (2 / ‖stepPhase d s i j - 1‖ * ‖x i j‖) / (N : ℝ)) atTop (nhds 0) :=
      tendsto_const_div_atTop_nhds_zero_nat _
    refine squeeze_zero_norm' ?_ hg
    filter_upwards [eventually_ge_atTop 1] with N hN
    exact hnorm N hN

/-- ★ O LIMITE HERDA A EQUIVARIÂNCIA (com o v166): a média ergódica de
    uma simetria do estado é a simetria da média — a seção ergódica
    equivariante, COM O LIMITE, em kernel. -/
theorem birkhoff_limit_equivariant (d : n → ℝ) (e : Equiv.Perm n)
    (hde : ∀ i, d (e i) = d i) (x : Matrix n n ℂ) :
    specExpect d (x.submatrix e e) = (specExpect d x).submatrix e e :=
  specExpect_equivariant d e hde x

end

end TGLExt
