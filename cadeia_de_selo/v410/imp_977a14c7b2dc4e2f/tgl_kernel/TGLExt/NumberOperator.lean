import TGLExt.WitnessV2

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O OPERADOR NÚMERO: o candidato ao Dirac genuinamente ilimitado
  [TGLExt — v105, o incremento 23 do programa SemifiniteAnalysis]

A face do CORNER forte pede um Dirac GENUINAMENTE ilimitado
(`GenuinelyUnboundedDiracData`, v103). O candidato canônico: N e_n = n·e_n
em ℓ²(ℕ,ℂ), domínio D_N = {x | Σ n²|x_n|² < ∞}. Esta pedra prova a METADE
ALCANÇÁVEL HOJE:

* `numberDomain` — D_N como submódulo; ★ `numberDomain_dense` — D_N é
  DENSO (via `lp.hasSum_single`: todo x é limite de somas finitas de
  inscrições, e cada inscrição mora em D_N) — sem densidade, star(N)=N
  nem faz sentido;
* `numberOp : ellTwo →ₗ.[ℂ] ellTwo` — N como operador PARCIAL genuíno
  (domínio próprio, não ⊤);
* ★★ `numberOp_symmetric` — ⟪N x, y⟫ = ⟪x, N y⟫ no domínio
  (`IsFormalAdjoint numberOp numberOp`, termo a termo em ℓ²);
* ★ `numberOp_kills_first` — N e₀ = 0: o átomo do Nome mora no kernel;
* ★★ `numberOp_unbounded` — NENHUMA cota C serve (‖N e_m‖ = m·‖e_m‖):
  o N alimentará `GenuinelyUnboundedDiracData` ASSIM QUE star(N)=N
  fechar — e o Dirac de bancada (v103) jamais poderia.

A PAREDE RESTANTE (nomeada, sem véu): star(N) = N pede a inclusão dura
N†.domain ⊆ D_N — caracterização do domínio do adjunto por truncamento
(S_M ≤ C·√S_M ⟹ S_M ≤ C² uniforme ⟹ Σ n²|y_n|² < ∞). A mathlib não tem
auto-adjunção essencial; será construída à mão (próximas pedras).

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal

noncomputable section

/-- a multiplicação por n nas coordenadas (a função crua). -/
def numberSeq (x : ellTwo) : ℕ → ℂ := fun n => (n : ℂ) * x n

/-- o domínio do operador número: Σ n²|x_n|² < ∞. -/
def numberDomain : Submodule ℂ ellTwo where
  carrier := {x | Memℓp (numberSeq x) 2}
  zero_mem' := by
    have h : numberSeq (0 : ellTwo) = 0 := by
      funext n
      show (n : ℂ) * (0 : ellTwo) n = 0
      rw [lp.coeFn_zero]
      simp
    show Memℓp (numberSeq (0 : ellTwo)) 2
    rw [h]
    exact zero_memℓp
  add_mem' := by
    intro a b ha hb
    have h : numberSeq (a + b) = numberSeq a + numberSeq b := by
      funext n
      show (n : ℂ) * (a + b) n = (n : ℂ) * a n + (n : ℂ) * b n
      rw [lp.coeFn_add]
      simp [mul_add]
    show Memℓp (numberSeq (a + b)) 2
    rw [h]
    exact (ha : Memℓp (numberSeq a) 2).add hb
  smul_mem' := by
    intro c x hx
    have h : numberSeq (c • x) = c • numberSeq x := by
      funext n
      show (n : ℂ) * (c • x) n = c • ((n : ℂ) * x n)
      rw [lp.coeFn_smul]
      simp [smul_eq_mul]
      ring
    show Memℓp (numberSeq (c • x)) 2
    rw [h]
    exact (hx : Memℓp (numberSeq x) 2).const_smul c

theorem mem_numberDomain_iff {x : ellTwo} :
    x ∈ numberDomain ↔ Memℓp (numberSeq x) 2 := Iff.rfl

/-- N como operador PARCIALMENTE definido (o domínio é próprio). -/
def numberOp : ellTwo →ₗ.[ℂ] ellTwo where
  domain := numberDomain
  toFun :=
    { toFun := fun x => (⟨numberSeq (x : ellTwo),
        mem_numberDomain_iff.mp x.2⟩ : ellTwo)
      map_add' := fun x y => by
        apply Subtype.ext
        funext n
        show (n : ℂ) * ((x : ellTwo) + (y : ellTwo)) n
          = ((n : ℂ) * (x : ellTwo) n) + ((n : ℂ) * (y : ellTwo) n)
        rw [lp.coeFn_add]
        simp [mul_add]
      map_smul' := fun c x => by
        apply Subtype.ext
        funext n
        show (n : ℂ) * (c • (x : ellTwo)) n = c • ((n : ℂ) * (x : ellTwo) n)
        rw [lp.coeFn_smul]
        simp [smul_eq_mul]
        ring }

theorem numberOp_apply (x : numberOp.domain) (n : ℕ) :
    (numberOp x : ellTwo) n = (n : ℂ) * (x : ellTwo) n := rfl

/-- [KERNEL] ★★ N É SIMÉTRICO: ⟪N x, y⟫ = ⟪x, N y⟫ para x, y no domínio
    — N é adjunto formal de si mesmo (termo a termo; n é real). -/
theorem numberOp_symmetric : numberOp.IsFormalAdjoint numberOp := by
  intro x y
  rw [lp.inner_eq_tsum, lp.inner_eq_tsum]
  apply tsum_congr
  intro n
  simp only [RCLike.inner_apply, numberOp_apply, map_mul]
  have hconj : (starRingEnd ℂ) ((n : ℕ) : ℂ) = ((n : ℕ) : ℂ) :=
    Complex.conj_natCast n
  rw [hconj]
  ring

/-- [KERNEL] ★ cada inscrição mora no domínio (suporte finito). -/
theorem single_mem_numberDomain (k : ℕ) :
    inscriptions k ∈ numberDomain := by
  show Memℓp (numberSeq (inscriptions k)) 2
  have h : numberSeq (inscriptions k) = (k : ℂ) • ⇑(inscriptions k) := by
    funext n
    show (n : ℂ) * (inscriptions k) n = (k : ℂ) • (inscriptions k) n
    rcases eq_or_ne n k with rfl | hnk
    · simp [smul_eq_mul]
    · unfold inscriptions
      rw [lp.single_apply_ne 2 k 1 hnk]
      simp
  rw [h]
  exact (lp.memℓp (inscriptions k)).const_smul (k : ℂ)

/-- [KERNEL] ★ N e₀ = 0: o átomo do Nome mora no kernel do candidato. -/
theorem numberOp_kills_first :
    numberOp ⟨firstInscription, single_mem_numberDomain 0⟩ = 0 := by
  apply Subtype.ext
  funext n
  show (n : ℂ) * firstInscription n = (0 : ellTwo) n
  rw [lp.coeFn_zero]
  rcases eq_or_ne n 0 with rfl | hn
  · simp
  · unfold firstInscription inscriptions
    rw [lp.single_apply_ne 2 0 1 hn]
    simp

/-- N na inscrição m: N e_m = m·e_m (a lei espectral do candidato). -/
theorem numberOp_single (m : ℕ) :
    numberOp ⟨inscriptions m, single_mem_numberDomain m⟩
      = (m : ℂ) • inscriptions m := by
  apply Subtype.ext
  funext n
  show (n : ℂ) * (inscriptions m) n = ((m : ℂ) • inscriptions m) n
  rw [lp.coeFn_smul]
  rcases eq_or_ne n m with rfl | hnm
  · simp [smul_eq_mul]
  · unfold inscriptions
    rw [lp.single_apply_ne 2 m 1 hnm]
    simp [Pi.single_eq_of_ne hnm]

/-- [KERNEL] ★★ A ILIMITAÇÃO: nenhuma cota C serve — ‖N e_m‖ = m. O N
    alimentará `GenuinelyUnboundedDiracData` assim que star(N)=N fechar;
    o Dirac de bancada (v103) jamais poderia. -/
theorem numberOp_unbounded :
    ¬ ∃ C : ℝ, ∀ x : numberOp.domain,
      ‖numberOp x‖ ≤ C * ‖(x : ellTwo)‖ := by
  rintro ⟨C, hC⟩
  obtain ⟨m, hm⟩ := exists_nat_gt C
  have hnorm := hC ⟨inscriptions m, single_mem_numberDomain m⟩
  rw [numberOp_single m, norm_smul] at hnorm
  have h1 : ‖inscriptions m‖ = 1 := inscriptions_orthonormal.1 m
  simp only [h1, mul_one, Complex.norm_natCast] at hnorm
  exact absurd hnorm (not_le.mpr hm)

/-- [KERNEL] ★ O DOMÍNIO É DENSO: todo x ∈ ℓ² é limite das somas finitas
    de inscrições (lp.hasSum_single), e cada soma finita mora em D_N —
    sem isto, star(N)=N nem faria sentido. -/
theorem numberDomain_dense : Dense (numberDomain : Set ellTwo) := by
  intro f
  have hsum : HasSum (fun k => lp.single 2 k (f k)) f :=
    lp.hasSum_single (by norm_num) f
  refine mem_closure_of_tendsto hsum ?_
  filter_upwards with s
  refine Submodule.sum_mem numberDomain ?_
  intro k _
  have h : lp.single 2 k (f k) = (f k) • inscriptions k := by
    apply Subtype.ext
    funext n
    unfold inscriptions
    rw [lp.coeFn_smul]
    rcases eq_or_ne n k with rfl | hnk
    · simp [lp.single_apply_self, smul_eq_mul]
    · rw [lp.single_apply_ne 2 k _ hnk]
      simp [Pi.single_eq_of_ne hnk]
  rw [h]
  exact Submodule.smul_mem numberDomain (f k) (single_mem_numberDomain k)

end

end TGLExt
