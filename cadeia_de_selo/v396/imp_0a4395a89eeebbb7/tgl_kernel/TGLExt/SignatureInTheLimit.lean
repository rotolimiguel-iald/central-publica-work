import TGLExt.TheFactorObject

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A PEDRA 87 — SignatureInTheLimit: a assinatura tipo-III DENTRO do objeto
  [TGLExt — v131, Bloco A do PLANO_ULTIMA_FLAG, pedra 5 de 5]

A pedra 86 cunhou M_TGL. Esta pedra transporta a ASSINATURA para DENTRO
dele — as testemunhas são elementos de andar finito, que JÁ vivem em M_TGL:

* `tState_kron_split` — o estado fatoriza no produto tensorial (a
  generalização da coerência);
* ★★ `omega_ratio_site0/site1` (e inversos) — AS RAZÕES MODULARES
  REALIZADAS NO OBJETO: ω(AB) = r·ω(BA) com A,B ∈ M_TGL, para os
  geradores r = μ₀/(1−μ₀) e r = μ₁/(1−μ₁) e seus inversos;
* ★★★ `omega_not_tracial_mix` — ω NÃO É TRACIAL sobre M_TGL (perfil com
  μ₀ ≠ ½): o estado do objeto completado carrega a assimetria modular;
* ★★ `ladder_in_object` — A ESCADA INTEIRA NO OBJETO: no perfil constante,
  ω(π(up_N)π(down_N)) = l^{N+1}·ω(π(down_N)π(up_N)) para TODO N — o
  reticulado de razões λ^{N+1} das pedras 71/81/82, agora DENTRO de M_TGL;
* ★★★ `signature_log_dense` — A MARCA DE III₁ NO OBJETO: no perfil
  alternado (⅓,¼), o subgrupo aditivo GERADO pelos log-ratios realizados
  em M_TGL é DENSO em ℝ (via a marca log-densa da pedra 72: os geradores
  ½ e ⅓ estão realizados).

HONESTIDADE (nomeada, sem véu): a densidade é do subgrupo GERADO pelas
razões realizadas (o análogo da S-invariante de Connes); a realização de
CADA elemento do subgrupo por uma palavra explícita multi-sítio fica
nomeada como abertura. "Fator" (centro trivial) e "sem peso normal"
seguem o programa (Bloco B do plano). O gate NÃO se move por esta pedra.
β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Kronecker Matrix
open scoped ComplexConjugate

noncomputable section

variable {P : SiteProfile}

/-! ## A — o estado fatoriza no produto tensorial -/

/-- [KERNEL] ★ a fatorização tensorial do estado (generaliza a coerência:
    B = 1 recupera `tState_towerStep`). -/
theorem tState_kron_split (P : SiteProfile) {N : ℕ}
    (A : Matrix (chainIdx N) (chainIdx N) ℂ)
    (B : Matrix (Fin 2) (Fin 2) ℂ) :
    tState P (N + 1) (A ⊗ₖ B)
      = tState P N A * ∑ s, ((siteW (P.w (N + 1)) s : ℝ) : ℂ) * B s s := by
  unfold tState
  rw [Fintype.sum_prod_type]
  have h : ∀ (k : chainIdx N) (s : Fin 2),
      ((towerW P (N + 1) (k, s) : ℝ) : ℂ) * (A ⊗ₖ B) (k, s) (k, s)
        = (((towerW P N k : ℝ) : ℂ) * A k k)
            * (((siteW (P.w (N + 1)) s : ℝ) : ℂ) * B s s) := by
    intro k s
    rw [kroneckerMap_apply]
    rw [show towerW P (N + 1) (k, s)
        = towerW P N k * siteW (P.w (N + 1)) s from rfl]
    push_cast
    ring
  rw [Finset.sum_congr rfl (fun k _ => Finset.sum_congr rfl (fun s _ => h k s))]
  rw [← Finset.sum_mul_sum]

/-- o estado numa matriz-unidade diagonal: o peso daquele índice. -/
theorem tState_single_diag (P : SiteProfile) (N : ℕ) (i : chainIdx N) :
    tState P N (Matrix.single i i (1 : ℂ)) = ((towerW P N i : ℝ) : ℂ) := by
  unfold tState
  rw [Finset.sum_eq_single i]
  · rw [Matrix.single_apply_same, mul_one]
  · intro k _ hk
    rw [Matrix.single_apply_of_ne _ _ _ _ _
      (fun h => hk (h.1.symm)), mul_zero]
  · intro h
    exact absurd (Finset.mem_univ i) h

/-! ## B — as razões dos geradores realizadas no objeto -/

/-- a razão modular r REALIZADA no objeto M_TGL: elementos A,B ∈ M_TGL
    (imagens π de andares finitos) com ω(AB) = r·ω(BA) e ω(BA) ≠ 0. -/
def objRatio (P : SiteProfile) (r : ℝ) : Prop :=
  ∃ (N : ℕ) (A B : Matrix (chainIdx N) (chainIdx N) ℂ),
    omegaState P (towerPi P A * towerPi P B)
      = ((r : ℝ) : ℂ) * omegaState P (towerPi P B * towerPi P A)
    ∧ omegaState P (towerPi P B * towerPi P A) ≠ 0

/-- o levantamento: ω dos produtos π é o estado dos produtos de andar. -/
theorem omegaState_pi_mul {N : ℕ}
    (A B : Matrix (chainIdx N) (chainIdx N) ℂ) :
    omegaState P (towerPi P A * towerPi P B) = tState P N (A * B) := by
  rw [← towerPi_mul, omegaState_pi]

/-- [KERNEL] ★ o estado dos produtos E01·E10 no sítio 0. -/
theorem tState_E01_E10 (P : SiteProfile) :
    tState P 0 (Matrix.single (0 : Fin 2) 1 (1 : ℂ)
        * Matrix.single (1 : Fin 2) 0 (1 : ℂ))
      = ((P.w 0 : ℝ) : ℂ) := by
  rw [Matrix.single_mul_single_same, one_mul, tState_single_diag]
  rfl

theorem tState_E10_E01 (P : SiteProfile) :
    tState P 0 (Matrix.single (1 : Fin 2) 0 (1 : ℂ)
        * Matrix.single (0 : Fin 2) 1 (1 : ℂ))
      = ((1 - P.w 0 : ℝ) : ℂ) := by
  rw [Matrix.single_mul_single_same, one_mul, tState_single_diag]
  rfl

/-- [KERNEL] ★★ A RAZÃO DO SÍTIO 0 REALIZADA: ω(AB) = (μ₀/(1−μ₀))·ω(BA). -/
theorem omega_ratio_site0 (P : SiteProfile) :
    objRatio P (P.w 0 / (1 - P.w 0)) := by
  have hν : (0 : ℝ) < 1 - P.w 0 := by linarith [P.lt_one 0]
  refine ⟨0, Matrix.single 0 1 1, Matrix.single 1 0 1, ?_, ?_⟩
  · rw [omegaState_pi_mul, omegaState_pi_mul, tState_E01_E10, tState_E10_E01]
    rw [← Complex.ofReal_mul]
    congr 1
    field_simp
  · rw [omegaState_pi_mul, tState_E10_E01]
    exact Complex.ofReal_ne_zero.mpr (ne_of_gt hν)

/-- [KERNEL] ★★ o INVERSO também: ω(BA) = ((1−μ₀)/μ₀)·ω(AB). -/
theorem omega_ratio_site0_inv (P : SiteProfile) :
    objRatio P ((1 - P.w 0) / P.w 0) := by
  have hμ : (0 : ℝ) < P.w 0 := P.pos 0
  refine ⟨0, Matrix.single 1 0 1, Matrix.single 0 1 1, ?_, ?_⟩
  · rw [omegaState_pi_mul, omegaState_pi_mul, tState_E01_E10, tState_E10_E01]
    rw [← Complex.ofReal_mul]
    congr 1
    field_simp
  · rw [omegaState_pi_mul, tState_E01_E10]
    exact Complex.ofReal_ne_zero.mpr (ne_of_gt hμ)

/-- [KERNEL] ★ os produtos do sítio 1 (andar 1: 1 ⊗ E). -/
theorem tState_site1 (P : SiteProfile) :
    tState P 1 (((1 : Matrix (chainIdx 0) (chainIdx 0) ℂ)
        ⊗ₖ Matrix.single (0 : Fin 2) 1 (1 : ℂ))
      * ((1 : Matrix (chainIdx 0) (chainIdx 0) ℂ)
        ⊗ₖ Matrix.single (1 : Fin 2) 0 (1 : ℂ)))
      = ((P.w 1 : ℝ) : ℂ) := by
  rw [← Matrix.mul_kronecker_mul, one_mul, Matrix.single_mul_single_same,
    one_mul, tState_kron_split, tState_one, one_mul]
  rw [Finset.sum_eq_single (0 : Fin 2)]
  · rw [Matrix.single_apply_same, mul_one]
    rfl
  · intro s _ hs
    rw [Matrix.single_apply_of_ne _ _ _ _ _ (fun h => hs h.1.symm), mul_zero]
  · intro h
    exact absurd (Finset.mem_univ (0 : Fin 2)) h

theorem tState_site1_rev (P : SiteProfile) :
    tState P 1 (((1 : Matrix (chainIdx 0) (chainIdx 0) ℂ)
        ⊗ₖ Matrix.single (1 : Fin 2) 0 (1 : ℂ))
      * ((1 : Matrix (chainIdx 0) (chainIdx 0) ℂ)
        ⊗ₖ Matrix.single (0 : Fin 2) 1 (1 : ℂ)))
      = ((1 - P.w 1 : ℝ) : ℂ) := by
  rw [← Matrix.mul_kronecker_mul, one_mul, Matrix.single_mul_single_same,
    one_mul, tState_kron_split, tState_one, one_mul]
  rw [Finset.sum_eq_single (1 : Fin 2)]
  · rw [Matrix.single_apply_same, mul_one]
    rfl
  · intro s _ hs
    rw [Matrix.single_apply_of_ne _ _ _ _ _ (fun h => hs h.1.symm), mul_zero]
  · intro h
    exact absurd (Finset.mem_univ (1 : Fin 2)) h

/-- [KERNEL] ★★ A RAZÃO DO SÍTIO 1 REALIZADA (e o inverso, por simetria). -/
theorem omega_ratio_site1 (P : SiteProfile) :
    objRatio P (P.w 1 / (1 - P.w 1)) := by
  have hν : (0 : ℝ) < 1 - P.w 1 := by linarith [P.lt_one 1]
  refine ⟨1, (1 : Matrix (chainIdx 0) (chainIdx 0) ℂ) ⊗ₖ Matrix.single 0 1 1,
    (1 : Matrix (chainIdx 0) (chainIdx 0) ℂ) ⊗ₖ Matrix.single 1 0 1, ?_, ?_⟩
  · rw [omegaState_pi_mul, omegaState_pi_mul, tState_site1, tState_site1_rev]
    rw [← Complex.ofReal_mul]
    congr 1
    field_simp
  · rw [omegaState_pi_mul, tState_site1_rev]
    exact Complex.ofReal_ne_zero.mpr (ne_of_gt hν)

theorem omega_ratio_site1_inv (P : SiteProfile) :
    objRatio P ((1 - P.w 1) / P.w 1) := by
  have hμ : (0 : ℝ) < P.w 1 := P.pos 1
  refine ⟨1, (1 : Matrix (chainIdx 0) (chainIdx 0) ℂ) ⊗ₖ Matrix.single 1 0 1,
    (1 : Matrix (chainIdx 0) (chainIdx 0) ℂ) ⊗ₖ Matrix.single 0 1 1, ?_, ?_⟩
  · rw [omegaState_pi_mul, omegaState_pi_mul, tState_site1, tState_site1_rev]
    rw [← Complex.ofReal_mul]
    congr 1
    field_simp
  · rw [omegaState_pi_mul, tState_site1]
    exact Complex.ofReal_ne_zero.mpr (ne_of_gt hμ)

/-! ## C — a não-tracialidade de ω sobre o objeto -/

/-- [KERNEL] ★★★ ω NÃO É TRACIAL SOBRE M_TGL: com μ₀ ≠ ½, existem A,B
    (imagens da torre, membros de M_TGL) com ω(AB) ≠ ω(BA) — a assimetria
    modular VIVE no objeto completado. -/
theorem omega_not_tracial (P : SiteProfile) (h : P.w 0 ≠ 1 / 2) :
    ∃ A B : TowerHilbert P →L[ℂ] TowerHilbert P,
      A ∈ theFactorObject P ∧ B ∈ theFactorObject P
      ∧ omegaState P (A * B) ≠ omegaState P (B * A) := by
  refine ⟨towerPi P (N := 0) (Matrix.single (0 : Fin 2) (1 : Fin 2) (1 : ℂ)),
    towerPi P (N := 0) (Matrix.single (1 : Fin 2) (0 : Fin 2) (1 : ℂ)),
    towerPi_mem_factor _, towerPi_mem_factor _, ?_⟩
  rw [omegaState_pi_mul, omegaState_pi_mul, tState_E01_E10, tState_E10_E01]
  intro hc
  have hr : P.w 0 = 1 - P.w 0 := Complex.ofReal_injective hc
  apply h
  linarith

/-! ## D — a ESCADA inteira no objeto (perfil constante) -/

/-- o perfil constante: todo sítio pesa μ = l/(1+l) (a razão é l). -/
def constProfile (l : ℝ) (hl : 0 < l) : SiteProfile where
  w := fun _ => l / (1 + l)
  pos := fun _ => div_pos hl (by linarith)
  lt_one := fun _ => by
    rw [div_lt_one (by linarith : (0 : ℝ) < 1 + l)]
    linarith

theorem tState_chainWord (l : ℝ) (hl : 0 < l) :
    ∀ N : ℕ, tState (constProfile l hl) N (chainUp N * chainDown N)
        = (((l / (1 + l)) ^ (N + 1) : ℝ) : ℂ)
      ∧ tState (constProfile l hl) N (chainDown N * chainUp N)
        = (((1 / (1 + l)) ^ (N + 1) : ℝ) : ℂ)
  | 0 => by
      have h1l : (1 : ℝ) + l ≠ 0 := by linarith
      have hν : (1 : ℝ) - l / (1 + l) = 1 / (1 + l) := by
        field_simp
        ring
      constructor
      · rw [show chainUp 0 = Matrix.single (0 : Fin 2) (1 : Fin 2) (1 : ℂ)
            from rfl,
          show chainDown 0 = Matrix.single (1 : Fin 2) (0 : Fin 2) (1 : ℂ)
            from rfl,
          tState_E01_E10]
        rw [show (constProfile l hl).w 0 = l / (1 + l) from rfl, pow_one]
      · rw [show chainUp 0 = Matrix.single (0 : Fin 2) (1 : Fin 2) (1 : ℂ)
            from rfl,
          show chainDown 0 = Matrix.single (1 : Fin 2) (0 : Fin 2) (1 : ℂ)
            from rfl,
          tState_E10_E01]
        rw [show (constProfile l hl).w 0 = l / (1 + l) from rfl, hν, pow_one]
  | N + 1 => by
      obtain ⟨ih1, ih2⟩ := tState_chainWord l hl N
      constructor
      · rw [show chainUp (N + 1)
            = chainUp N ⊗ₖ Matrix.single (0 : Fin 2) (1 : Fin 2) (1 : ℂ)
            from rfl,
          show chainDown (N + 1)
            = chainDown N ⊗ₖ Matrix.single (1 : Fin 2) (0 : Fin 2) (1 : ℂ)
            from rfl,
          ← Matrix.mul_kronecker_mul, Matrix.single_mul_single_same, one_mul,
          tState_kron_split, ih1]
        rw [Finset.sum_eq_single (0 : Fin 2)]
        · rw [Matrix.single_apply_same, mul_one]
          rw [show ((siteW ((constProfile l hl).w (N + 1)) 0 : ℝ) : ℂ)
              = ((l / (1 + l) : ℝ) : ℂ) from rfl]
          rw [← Complex.ofReal_mul]
          congr 1
        · intro s _ hs
          rw [Matrix.single_apply_of_ne _ _ _ _ _ (fun h => hs h.1.symm),
            mul_zero]
        · intro h
          exact absurd (Finset.mem_univ (0 : Fin 2)) h
      · rw [show chainUp (N + 1)
            = chainUp N ⊗ₖ Matrix.single (0 : Fin 2) (1 : Fin 2) (1 : ℂ)
            from rfl,
          show chainDown (N + 1)
            = chainDown N ⊗ₖ Matrix.single (1 : Fin 2) (0 : Fin 2) (1 : ℂ)
            from rfl,
          ← Matrix.mul_kronecker_mul, Matrix.single_mul_single_same, one_mul,
          tState_kron_split, ih2]
        rw [Finset.sum_eq_single (1 : Fin 2)]
        · rw [Matrix.single_apply_same, mul_one]
          rw [show ((siteW ((constProfile l hl).w (N + 1)) 1 : ℝ) : ℂ)
              = ((1 - l / (1 + l) : ℝ) : ℂ) from rfl]
          rw [show (1 : ℝ) - l / (1 + l) = 1 / (1 + l) by field_simp; ring]
          rw [← Complex.ofReal_mul]
          congr 1
        · intro s _ hs
          rw [Matrix.single_apply_of_ne _ _ _ _ _ (fun h => hs h.1.symm),
            mul_zero]
        · intro h
          exact absurd (Finset.mem_univ (1 : Fin 2)) h

/-- [KERNEL] ★★ A ESCADA NO OBJETO: a razão l^{N+1} realizada em M_TGL
    para TODO andar N — o reticulado das pedras 71/81/82, dentro do
    objeto completado. -/
theorem ladder_in_object (l : ℝ) (hl : 0 < l) (N : ℕ) :
    objRatio (constProfile l hl) (l ^ (N + 1)) := by
  obtain ⟨h1, h2⟩ := tState_chainWord l hl N
  refine ⟨N, chainUp N, chainDown N, ?_, ?_⟩
  · rw [omegaState_pi_mul, omegaState_pi_mul, h1, h2, ← Complex.ofReal_mul]
    congr 1
    rw [← mul_pow]
    congr 1
    field_simp
  · rw [omegaState_pi_mul, h2]
    apply Complex.ofReal_ne_zero.mpr
    apply pow_ne_zero
    positivity

/-! ## E — A MARCA DE III₁ NO OBJETO: o perfil alternado (⅓, ¼) -/

/-- o perfil alternado: sítios pares pesam ⅓ (razão ½), ímpares ¼ (razão ⅓). -/
def mixProfile : SiteProfile where
  w := fun n => if n % 2 = 0 then 1 / 3 else 1 / 4
  pos := fun n => by
    by_cases h : n % 2 = 0
    · rw [if_pos h]; norm_num
    · rw [if_neg h]; norm_num
  lt_one := fun n => by
    by_cases h : n % 2 = 0
    · rw [if_pos h]; norm_num
    · rw [if_neg h]; norm_num

theorem mixProfile_ratio0 : mixProfile.w 0 / (1 - mixProfile.w 0) = 1 / 2 := by
  rw [show mixProfile.w 0 = 1 / 3 from rfl]
  norm_num

theorem mixProfile_ratio1 : mixProfile.w 1 / (1 - mixProfile.w 1) = 1 / 3 := by
  rw [show mixProfile.w 1 = 1 / 4 from rfl]
  norm_num

/-- os log-ratios realizados no objeto do perfil alternado. -/
def realizedLog : Set ℝ :=
  {t : ℝ | ∃ r : ℝ, 0 < r ∧ objRatio mixProfile r ∧ t = Real.log r}

theorem log_half_realized : Real.log ((1 : ℝ) / 2) ∈ realizedLog := by
  refine ⟨1 / 2, by norm_num, ?_, rfl⟩
  rw [← mixProfile_ratio0]
  exact omega_ratio_site0 mixProfile

theorem log_third_realized : Real.log ((1 : ℝ) / 3) ∈ realizedLog := by
  refine ⟨1 / 3, by norm_num, ?_, rfl⟩
  rw [← mixProfile_ratio1]
  exact omega_ratio_site1 mixProfile

/-- [KERNEL] ★★★ A MARCA DE III₁ NO OBJETO COMPLETADO: o subgrupo aditivo
    gerado pelos log-ratios REALIZADOS em M_TGL(⅓,¼) é DENSO em ℝ — a
    S-invariante do objeto toca todo ponto (via a marca da pedra 72). -/
theorem signature_log_dense :
    Dense ((AddSubgroup.closure realizedLog : AddSubgroup ℝ) : Set ℝ) := by
  have hsub : ({Real.log ((1 : ℝ) / 2), Real.log ((1 : ℝ) / 3)} : Set ℝ)
      ⊆ realizedLog := by
    intro t ht
    rcases ht with h | h
    · rw [h]; exact log_half_realized
    · rw [h]; exact log_third_realized
  have hmono := AddSubgroup.closure_mono hsub
  apply Dense.mono _ the_mixing_mark
  exact_mod_cast hmono

/-- [KERNEL] ★★★ A SÍNTESE DA PEDRA 87: a assinatura tipo-III vive DENTRO
    do objeto — ω não-tracial + a escada l^{N+1} em todo andar + o subgrupo
    log-denso dos ratios realizados (perfil ⅓,¼). -/
theorem signature_in_the_limit :
    (∃ A B : TowerHilbert mixProfile →L[ℂ] TowerHilbert mixProfile,
      A ∈ theFactorObject mixProfile ∧ B ∈ theFactorObject mixProfile
      ∧ omegaState mixProfile (A * B) ≠ omegaState mixProfile (B * A))
    ∧ (∀ (l : ℝ) (hl : 0 < l) (N : ℕ),
        objRatio (constProfile l hl) (l ^ (N + 1)))
    ∧ Dense ((AddSubgroup.closure realizedLog : AddSubgroup ℝ) : Set ℝ) :=
  ⟨omega_not_tracial mixProfile (by
      rw [show mixProfile.w 0 = 1 / 3 from rfl]; norm_num),
   fun l hl N => ladder_in_object l hl N,
   signature_log_dense⟩

end

end TGLExt
