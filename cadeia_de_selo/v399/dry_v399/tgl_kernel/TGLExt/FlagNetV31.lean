import TGLExt.ContratoQG_v31_Teoremas

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# FlagNetV31 — a rede das cunhas POR BANDEIRAS não carrega a v3.1   [condicional a Takesaki, NOMEADO]
  [TGLExt — v371, pedra da gerência (25/09/2026), por ordem do operador «sim, entra tudo»; transposta de
   `scratchpad\contrato_v3\v31\FlagNetV31.lean` (sha16 84d27e29a1d38f4c): mudam SÓ o caminho do módulo, os imports locais, o namespace da reta de luz
   (se houver) e este cabeçalho; renomes para o índice da IALD não ver homônimo: nenhum.
   NÃO cunha nome reservado; NÃO move o gate; PROVADA ≠ CONFIRMADA]
  ⚠ v371: «rede POR BANDEIRAS» = a hipótese `hinv` (a álgebra da cunha invariante por TODAS as translações); «bandeira» aqui
  NÃO é bandeira do gate. A parede é condicional a `KMSUniqueGroup` (Takesaki não está na mathlib da casa).


  RODADA 2 (cético 2, NOTA, ACEITO): a hipótese `KMSUnique` da v3 quantificava sobre TODA função
  D : ℝ → unitários e por isso proibia simetrias Z₂ (`kmsUnique_forbids_Z2`, reprovado aqui) — no campo
  escalar livre, Γ(−1) é um tal Z₂ ≠ 1 [KNOWN], logo a hipótese era FALSA lá. A v3.1 usa a forma FIEL a
  Takesaki: unicidade entre GRUPOS a um parâmetro (`KMSUniqueGroup`). A parede sobrevive com a mesma prova
  (o D usado, U(−a)Δ^{is}U(a), é grupo). Continua CONDICIONAL (Takesaki não está na mathlib da casa).
-/

namespace TGLExt.ContratoQGv31.FlagNet

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31
open scoped InnerProductSpace

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

def Uiso (W : TGLSpecificAQFTWitness) (a : Fin 4 → ℝ) : W.H ≃ₗᵢ[ℂ] W.H where
  toFun := W.U a
  invFun := W.U (-a)
  map_add' := map_add _
  map_smul' := map_smul _
  left_inv := fun x => U_neg_apply W a x
  right_inv := fun x => U_pos_neg_apply W a x
  norm_map' := U_norm W a

theorem boost_image_rightWedge (s : ℝ) : wedgeBoostMap s '' rightWedge = rightWedge := by
  have hmem : ∀ (r : ℝ) (x : Fin 4 → ℝ), x ∈ rightWedge → wedgeBoostMap r x ∈ rightWedge := by
    intro r x hx
    have hx' : |x 0| < x 1 := hx
    show |wedgeBoostMap r x 0| < wedgeBoostMap r x 1
    rw [wedgeBoostMap_apply0, wedgeBoostMap_apply1, abs_lt]
    obtain ⟨h1, h2⟩ := abs_lt.mp hx'
    have e1 := Real.cosh_sub_sinh r
    have e2 := Real.cosh_add_sinh r
    have p1 : 0 < (Real.cosh r - Real.sinh r) * (x 1 - x 0) := by
      rw [e1]; exact mul_pos (Real.exp_pos _) (by linarith)
    have p2 : 0 < (Real.cosh r + Real.sinh r) * (x 1 + x 0) := by
      rw [e2]; exact mul_pos (Real.exp_pos _) (by linarith)
    constructor <;> nlinarith
  ext y
  constructor
  · rintro ⟨x, hx, rfl⟩
    exact hmem s x hx
  · intro hy
    refine ⟨wedgeBoostMap (-s) y, hmem (-s) y hy, ?_⟩
    rw [← wedgeBoostMap_add, add_neg_cancel, wedgeBoostMap_zero]

theorem Δit_preserves_wedge (C : ContratoH2 W R N) (s : ℝ) (T : W.H →L[ℂ] W.H)
    (hT : T ∈ W.net rightWedge) : (C.Δit s).conjStarAlgEquiv T ∈ W.net rightWedge := by
  have h := C.bw_covariance s rightWedge T hT
  rwa [boost_image_rightWedge] at h

/-- a hipótese da v3 (sobre TODA função D) — mantida só para exibir por que foi trocada. -/
def KMSUniqueFun (C : ContratoH2 W R N) : Prop :=
  ∀ D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H), (∀ t, D t W.vac = W.vac) →
    (∀ (t : ℝ) (T : W.H →L[ℂ] W.H), T ∈ W.net rightWedge →
      (D t).conjStarAlgEquiv T ∈ W.net rightWedge) →
    KMSAt W (fun t => D (-t)) 1 → ∀ t, D t = C.Δit t

/-- [DERIVED] (cético 2, CeticoKMSUnique.lean 948fb8c29d3661e4, transposto) ★★ a hipótese sobre funções proíbe
    todo Z₂ unitário que comuta com o fluxo modular — por isso NÃO é Takesaki. -/
theorem kmsUniqueFun_forbids_Z2 (C : ContratoH2 W R N) (hTak : KMSUniqueFun C)
    (V : W.H ≃ₗᵢ[ℂ] W.H) (hV2 : ∀ x, V (V x) = x) (hVvac : V W.vac = W.vac)
    (hVcomm : ∀ (t : ℝ) (x : W.H), C.Δit t (V x) = V (C.Δit t x))
    (hVnet : ∀ T : W.H →L[ℂ] W.H, T ∈ W.net rightWedge → V.conjStarAlgEquiv T ∈ W.net rightWedge) :
    ∀ x, V x = x := by
  have hVsymm : ∀ x, V.symm x = V x := by
    intro x
    apply V.injective
    rw [LinearIsometryEquiv.apply_symm_apply, hV2]
  let D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H) := fun s => V.trans (C.Δit s)
  have hDapply : ∀ s x, D s x = C.Δit s (V x) := fun s x => rfl
  have hvac : ∀ s, D s W.vac = W.vac := by
    intro s; rw [hDapply, hVvac, ContratoH2.Δit_vac]
  have hpres : ∀ (s : ℝ) (T : W.H →L[ℂ] W.H), T ∈ W.net rightWedge →
      (D s).conjStarAlgEquiv T ∈ W.net rightWedge := by
    intro s T hT
    have e : (D s).conjStarAlgEquiv T = (C.Δit s).conjStarAlgEquiv (V.conjStarAlgEquiv T) := by
      ext x
      simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply]
      rfl
    rw [e]
    exact Δit_preserves_wedge C s _ (hVnet T hT)
  have hkms : KMSAt W (fun s => D (-s)) 1 := by
    intro A hA B hB
    obtain ⟨F, hF, hM, h1, h2⟩ := C.kms A hA (V.conjStarAlgEquiv B) (hVnet B hB)
    refine ⟨F, hF, hM, ?_, ?_⟩
    · intro t
      rw [h1 t]
      simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply, hVsymm, hVvac]
      rfl
    · intro t
      rw [h2 t]
      have hs : star (V.conjStarAlgEquiv B) = V.conjStarAlgEquiv (star B) := (map_star _ B).symm
      rw [hs]
      simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply, hVsymm, hVvac, neg_neg]
      rw [hDapply]
      have hadj : ⟪V ((star B) W.vac), C.Δit t (A W.vac)⟫_ℂ
          = ⟪(star B) W.vac, V (C.Δit t (A W.vac))⟫_ℂ := by
        have := V.inner_map_map ((star B) W.vac) (V (C.Δit t (A W.vac)))
        rw [hV2] at this
        exact this
      rw [hadj, ← hVcomm]
  have hD := hTak D hvac hpres hkms 0
  intro x
  have h := congrArg (fun E : W.H ≃ₗᵢ[ℂ] W.H => E x) hD
  simp only [hDapply] at h
  exact (C.Δit 0).injective h

/-- **a unicidade KMS FIEL a Takesaki** (HIPÓTESE NOMEADA): todo GRUPO a um parâmetro de unitários que fixa Ω,
    preserva a álgebra da cunha e é KMS a β = 1 É o Δit do contrato. -/
def KMSUniqueGroup (C : ContratoH2 W R N) : Prop :=
  ∀ D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H), D 0 = LinearIsometryEquiv.refl ℂ W.H →
    (∀ s t : ℝ, D (s + t) = (D t).trans (D s)) → (∀ t, D t W.vac = W.vac) →
    (∀ (t : ℝ) (T : W.H →L[ℂ] W.H), T ∈ W.net rightWedge →
      (D t).conjStarAlgEquiv T ∈ W.net rightWedge) →
    KMSAt W (fun t => D (-t)) 1 → ∀ t, D t = C.Δit t

/-- [DERIVED, condicional a `KMSUniqueGroup`] ★★ REDE POR BANDEIRAS ⟹ v3.1 VAZIA. -/
theorem flag_net_excludes_v31 (C : ContratoH2 W R N) (hTak : KMSUniqueGroup C)
    (hinv : ∀ (a : Fin 4 → ℝ) (T : W.H →L[ℂ] W.H),
      T ∈ W.net rightWedge → W.U a * T * W.U (-a) ∈ W.net rightWedge) : False := by
  apply C.commuting_translations_excluded
  intro t a
  let D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H) := fun s => ((Uiso W a).trans (C.Δit s)).trans (Uiso W a).symm
  have hDapply : ∀ s x, D s x = W.U (-a) (C.Δit s (W.U a x)) := fun s x => rfl
  have hΔ0 : C.Δit 0 = LinearIsometryEquiv.refl ℂ W.H := by
    rw [C.bw, show -(2 * Real.pi * (0:ℝ)) = 0 by ring, C.boost.V_zero]
  have hD0 : D 0 = LinearIsometryEquiv.refl ℂ W.H := by
    ext x
    rw [hDapply, hΔ0]
    exact U_neg_apply W a x
  have hΔadd : ∀ s u : ℝ, C.Δit (s + u) = (C.Δit u).trans (C.Δit s) := by
    intro s u
    rw [C.bw, C.bw, C.bw,
      show -(2 * Real.pi * (s + u)) = -(2 * Real.pi * s) + -(2 * Real.pi * u) by ring, C.boost.V_add]
  have hDadd : ∀ s u : ℝ, D (s + u) = (D u).trans (D s) := by
    intro s u
    ext x
    simp only [LinearIsometryEquiv.trans_apply, hDapply]
    rw [hΔadd, LinearIsometryEquiv.trans_apply, U_pos_neg_apply]
  have hvac : ∀ s, D s W.vac = W.vac := by
    intro s
    rw [hDapply, W.vac_invariant, C.Δit_vac, W.vac_invariant]
  have hpres : ∀ (s : ℝ) (T : W.H →L[ℂ] W.H), T ∈ W.net rightWedge →
      (D s).conjStarAlgEquiv T ∈ W.net rightWedge := by
    intro s T hT
    have e : (D s).conjStarAlgEquiv T
        = W.U (-a) * ((C.Δit s).conjStarAlgEquiv (W.U a * T * W.U (-a))) * W.U (-(-a)) := by
      ext x
      simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply, neg_neg]
      rfl
    rw [e]
    exact hinv (-a) _ (Δit_preserves_wedge C s _ (hinv a T hT))
  have hkms : KMSAt W (fun s => D (-s)) 1 := by
    intro A hA B hB
    obtain ⟨F, hF, hM, h1, h2⟩ := C.kms _ (hinv a A hA) _ (hinv a B hB)
    have hstar : ∀ X : W.H →L[ℂ] W.H, star (W.U a * X * W.U (-a)) = W.U a * star X * W.U (-a) := by
      intro X
      rw [star_mul, star_mul, W.U_star, W.U_star, neg_neg, mul_assoc]
    refine ⟨F, hF, hM, ?_, ?_⟩
    · intro s
      rw [h1 s, hstar]
      show ⟪W.U a (star A (W.U (-a) W.vac)), C.Δit (-s) (W.U a (B (W.U (-a) W.vac)))⟫_ℂ
        = ⟪(star A) W.vac, W.U (-a) (C.Δit (-s) (W.U a (B W.vac)))⟫_ℂ
      rw [W.vac_invariant, U_inner_adj]
    · intro s
      rw [h2 s, hstar]
      show ⟪W.U a (star B (W.U (-a) W.vac)), C.Δit (-(-s)) (W.U a (A (W.U (-a) W.vac)))⟫_ℂ
        = ⟪(star B) W.vac, W.U (-a) (C.Δit (-(-s)) (W.U a (A W.vac)))⟫_ℂ
      rw [W.vac_invariant, U_inner_adj]
  have hD := hTak D hD0 hDadd hvac hpres hkms t
  have hc : ∀ x : W.H, C.Δit t (W.U a x) = W.U a (C.Δit t x) := by
    intro x
    have h := congrArg (fun E : W.H ≃ₗᵢ[ℂ] W.H => E x) hD
    simp only [hDapply] at h
    have h' := congrArg (W.U a) h
    rw [U_pos_neg_apply] at h'
    exact h'
  ext y
  simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply]
  rw [hc, LinearIsometryEquiv.apply_symm_apply]

#print axioms boost_image_rightWedge
#print axioms Δit_preserves_wedge
#print axioms kmsUniqueFun_forbids_Z2
#print axioms flag_net_excludes_v31

end

end TGLExt.ContratoQGv31.FlagNet
