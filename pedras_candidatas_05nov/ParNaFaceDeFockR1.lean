import TGLExt.F1Fecho394.TensorContractionPropertiesR3
import TGLExt.F1Fecho394.BosonicFock
import TGLExt.F1Fecho394.CanonicalWedge
import TGL.GravitonShadow

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-!
# O PAR NA FACE DE FOCK — rodada R1 (parte geral)
  [pedra candidata da gerência c1, 05/11/2026; compilada no sandbox da v408]
-/

noncomputable section
open scoped TensorProduct InnerProductSpace
open UniformSpace

namespace TGLExt.ParNaFaceDeFockR1
open F1Fecho.TensorContraction

section Geral
variable {E G : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [NormedAddCommGroup G] [InnerProductSpace ℂ G]

/-- ★ O ESPELHO CONJUGA O PRODUTO INTERNO: para J antilinear e isométrico, ⟪J x, J y⟫ = conj ⟪x, y⟫ (polarização). -/
theorem inner_espelho (J : E ≃ₗᵢ⋆[ℂ] E) (x y : E) : ⟪J x, J y⟫_ℂ = starRingEnd ℂ ⟪x, y⟫_ℂ := by
  have hI : J (Complex.I • y) = -(Complex.I • J y) := by
    rw [J.map_smulₛₗ, Complex.conj_I, neg_smul]
  have h1 : J x + J y = J (x + y) := (map_add J x y).symm
  have h2 : J x - J y = J (x - y) := (map_sub J x y).symm
  have h3 : J x - (RCLike.I : ℂ) • J y = J (x + Complex.I • y) := by
    rw [map_add, hI, RCLike.I_to_complex, sub_eq_add_neg]
  have h4 : J x + (RCLike.I : ℂ) • J y = J (x - Complex.I • y) := by
    rw [map_sub, hI, RCLike.I_to_complex, sub_neg_eq_add]
  rw [inner_eq_sum_norm_sq_div_four (𝕜 := ℂ) (J x) (J y), inner_eq_sum_norm_sq_div_four (𝕜 := ℂ) x y]
  rw [h1, h2, h3, h4, LinearIsometryEquiv.norm_map, LinearIsometryEquiv.norm_map, LinearIsometryEquiv.norm_map,
    LinearIsometryEquiv.norm_map]
  simp only [RCLike.I_to_complex, map_div₀, map_add, map_sub, map_mul, map_pow, RCLike.conj_ofReal, Complex.conj_I,
    map_ofNat]
  ring

/-- O espelho lido por dentro: ⟪J w, a⟫ = ⟪J⁻¹ a, w⟫. -/
theorem inner_espelho_esq (J : E ≃ₗᵢ⋆[ℂ] E) (w a : E) : ⟪J w, a⟫_ℂ = ⟪J.symm a, w⟫_ℂ := by
  conv_lhs => rw [← J.apply_symm_apply a]
  rw [inner_espelho, inner_conj_symm]

/-- O PROJETOR DE POSTO DOIS sobre o par (a, b): x ↦ ⟪a, x⟫ a + ⟪b, x⟫ b. -/
def projPar (a b : E) : E →L[ℂ] E := (innerSL ℂ a).smulRight a + (innerSL ℂ b).smulRight b

theorem projPar_apply (a b x : E) : projPar a b x = ⟪a, x⟫_ℂ • a + ⟪b, x⟫_ℂ • b := by
  simp [projPar]

/-- O VETOR DO PAR: z = (√2)⁻¹ (f ⊗ u + g ⊗ v), no completamento de E ⊗ G. -/
def vetorPar (f g : E) (u v : G) : Completion (E ⊗[ℂ] G) :=
  (((Real.sqrt 2)⁻¹ : ℝ) : ℂ) • ((f ⊗ₜ[ℂ] u + g ⊗ₜ[ℂ] v : E ⊗[ℂ] G) : Completion (E ⊗[ℂ] G))

theorem contracao_do_par (J : E ≃ₗᵢ⋆[ℂ] E) (f g : E) (u v : G) (x : E) :
    contraction J (vetorPar f g u v) x =
      (((Real.sqrt 2)⁻¹ : ℝ) : ℂ) • (⟪J x, f⟫_ℂ • (u : Completion G) + ⟪J x, g⟫_ℂ • (v : Completion G)) := by
  unfold vetorPar
  rw [map_smul, ContinuousLinearMap.coe_smul', Pi.smul_apply, Completion.coe_add, map_add, ContinuousLinearMap.coe_add',
    Pi.add_apply, contraction_tmul, contraction_tmul]

theorem raiz_meio : (((Real.sqrt 2)⁻¹ : ℝ) : ℂ) * (((Real.sqrt 2)⁻¹ : ℝ) : ℂ) = (2⁻¹ : ℂ) := by
  have h : ((Real.sqrt 2)⁻¹ : ℝ) * ((Real.sqrt 2)⁻¹) = 2⁻¹ := by
    rw [← mul_inv, Real.mul_self_sqrt (by norm_num)]
  rw [← Complex.ofReal_mul, h]
  norm_num

variable [CompleteSpace E]

/-- ★★★ O REDUZIDO DO PAR É A MEIA-NAT: com u, v ortonormais, o reduzido (o traço parcial, `reduced J`) do par é ½ vezes o projetor
    de posto dois sobre J⁻¹ f e J⁻¹ g. -/
theorem reduzido_do_par (J : E ≃ₗᵢ⋆[ℂ] E) (f g : E) (u v : G) (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) (huv : ⟪u, v⟫_ℂ = 0) :
    reduced J (vetorPar f g u v) = (2⁻¹ : ℂ) • projPar (J.symm f) (J.symm g) := by
  apply ContinuousLinearMap.ext
  intro x
  apply ext_inner_left ℂ
  intro y
  have huu : ⟪(u : Completion G), (u : Completion G)⟫_ℂ = 1 := by
    rw [Completion.inner_coe, inner_self_eq_norm_sq_to_K, hu]; simp
  have hvv : ⟪(v : Completion G), (v : Completion G)⟫_ℂ = 1 := by
    rw [Completion.inner_coe, inner_self_eq_norm_sq_to_K, hv]; simp
  have huv' : ⟪(u : Completion G), (v : Completion G)⟫_ℂ = 0 := by rw [Completion.inner_coe, huv]
  have hvu' : ⟪(v : Completion G), (u : Completion G)⟫_ℂ = 0 := by
    rw [Completion.inner_coe, inner_eq_zero_symm.mp huv]
  simp only [reduced, ContinuousLinearMap.comp_apply, ContinuousLinearMap.adjoint_inner_right]
  rw [contracao_do_par, contracao_do_par, inner_espelho_esq J x f, inner_espelho_esq J x g, inner_espelho_esq J y f,
    inner_espelho_esq J y g]
  simp only [inner_smul_left, inner_smul_right, inner_add_left, inner_add_right, huu, hvv, huv', hvu',
    ContinuousLinearMap.coe_smul', Pi.smul_apply, projPar_apply, Complex.conj_ofReal, RCLike.conj_ofReal, inner_conj_symm]
  have hs := raiz_meio
  linear_combination (⟪y, J.symm f⟫_ℂ * ⟪J.symm f, x⟫_ℂ + ⟪y, J.symm g⟫_ℂ * ⟪J.symm g, x⟫_ℂ) * hs

end Geral

end TGLExt.ParNaFaceDeFockR1

#print axioms TGLExt.ParNaFaceDeFockR1.inner_espelho
#print axioms TGLExt.ParNaFaceDeFockR1.reduzido_do_par
