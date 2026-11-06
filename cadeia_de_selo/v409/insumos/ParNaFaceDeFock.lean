import TGLExt.F1Fecho394.TensorContractionPropertiesR3
import TGLExt.F1Fecho394.BosonicFock
import TGLExt.F1Fecho394.CanonicalWedge
import TGL.GravitonShadow
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.MeasureTheory.Function.L2Space

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-!
# O PAR NA FACE DE FOCK — os dois psíons no setor 2 do Fock concreto da luz, e a Meia-Nat da marginal
  [TGLExt — pedra da gerência c1, 05/11/2026; o nome `ParNaFaceDeFock` e os nomes das declarações são da gerência e ficam [DECLARADO] até a
   ratificação (a fala de 05/11, «concordo com todos os nomes que foram dados», é anterior a esta pedra e não a cobre); entra na v409, por
   ordem do operador («eu quero que entre tudo na versão 409 não deixar nada para a v410»)]

A LIGAÇÃO QUE A v407 DEIXOU ABERTA. A pedra `Par` (v407) provou o par de psíons na face FINITA: o canto do psíon é o projetor de Bell 4×4, a
marginal é ½·1 (`bell_reduced_half`) e o CCI é ½ (`bell_cci_half`), a Meia-Nat de emaranhamento; e deixou a face de Fock «[OPEN]: o
`FockCertificate` não tem operadores de criação como termo». A E21 da v408 corrigiu ao lado: o [OPEN] era de LIGAÇÃO (fiação), não de
ausência — o Fock CONCRETO (`F1Rede.BosonicFock`) tem os setores e o traço parcial (`F1Fecho.TensorContraction.reduced`). Esta pedra faz a ligação.

O que esta pedra PROVA:
* `inner_espelho`: para J antilinear e isométrico, ⟪J x, J y⟫ = conj ⟪x, y⟫ (polarização); `espelho_ortonormal`: J⁻¹ leva par ortonormal em
  par ortonormal.
* `reduzido_do_par` ★★★: no completamento de E ⊗ G, o par z = (√2)⁻¹ (f ⊗ u + g ⊗ v), com u, v ortonormais, tem reduzido (o traço parcial,
  `reduced J`) igual a ½ vezes o projetor de posto dois sobre J⁻¹ f e J⁻¹ g; `norma_do_par`: com f, g ortonormais, ‖z‖ = 1.
* `meia_nat_do_projetor` ★★★: para ρ = ½·P(a, b), com a, b ortonormais: ρ a = ½ a e ρ b = ½ b (cada psíon pesa ½); ρ(ρ a) ≠ ρ a (o indivíduo
  não ecoa: a marginal não é projeção); os pesos somam 1; e 1 − pureza = ½ (o CCI da Meia-Nat).
* `par_ortonormal_das_polarizacoes`, `existe_par_ortonormal_em_H1` ★★: a uma-partícula da luz é L²(μ₀; ℂ²); as duas polarizações da fibra
  (a involução D = diag(1, −1) e a troca S, aplicadas ponto a ponto) dão um par ortonormal: um autovetor de D e a sua troca, de autovalor oposto.
* `parFock` ★★: o par de psíons, (√2)⁻¹ (f⊗f + g⊗g), no setor 2 do Fock concreto (`parSetor_mem`: está no setor simétrico de duas
  partículas); `parFock_norma`: norma 1; `parFock_ortogonal_ao_vacuo` e `parFock_ortogonal_a_uma_particula`: é outra coisa que o vácuo e que
  uma partícula.
* `a_marginal_do_par` ★★★: pela conjugação canônica da cunha (`F1Rede.CanonicalWedge.Jcandidate`, o J da luz), a marginal do par é ½ vezes
  o projetor de posto dois.
* `o_par_na_face_de_fock` ★★★: a conjunção — existe o par ortonormal; o par está no setor 2, tem norma 1, é ortogonal ao vácuo e a toda
  uma-partícula; a marginal é ½·P; cada psíon pesa ½; o indivíduo não ecoa; 1 − pureza = ½; e a MESMA Meia-Nat da face finita
  (`bell_reduced_half`, `bell_cci_half`).

O que esta pedra NÃO afirma:
* Não identifica o projetor de Bell da face finita com o par da face de Fock: são espaços distintos (`Fin 2 × Fin 2` e o setor 2 do Fock);
  o que se prova é que a marginal tem o MESMO valor, ½, nas duas faces.
* O traço parcial usado é o do kernel (`reduced J z = C†C`, relativo a uma conjugação J); a escolha J = `Jcandidate` é a conjugação da cunha
  canônica; com outra conjugação o projetor muda de lugar (J⁻¹ f, J⁻¹ g), não de valor.
* A leitura «o par de psíons é o gráviton» segue a da pedra `Par` (justaposição da face de helicidade, não identificação).
* Nada aqui é teste com a natureza; não move o gate; PROVADA = validade no kernel, não creditação; NOT_FALSIFIED nunca é CONFIRMED.
Sem sorry, sem axiom; trio `{propext, Classical.choice, Quot.sound}`.
-/

noncomputable section
open scoped TensorProduct InnerProductSpace
open UniformSpace

namespace TGLExt.ParNaFaceDeFock
open F1Fecho.TensorContraction

/-! ### 1. Geral: o espelho e o reduzido do par -/

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

/-- O espelho leva um par ortonormal num par ortonormal. -/
theorem espelho_ortonormal (J : E ≃ₗᵢ⋆[ℂ] E) (f g : E) (hf : ‖f‖ = 1) (hg : ‖g‖ = 1) (hfg : ⟪f, g⟫_ℂ = 0) :
    ‖J.symm f‖ = 1 ∧ ‖J.symm g‖ = 1 ∧ ⟪J.symm f, J.symm g⟫_ℂ = 0 := by
  refine ⟨by rw [LinearIsometryEquiv.norm_map, hf], by rw [LinearIsometryEquiv.norm_map, hg], ?_⟩
  rw [inner_espelho, hfg, map_zero]

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
  rw [map_smul, smul_apply, Completion.coe_add, map_add, add_apply, contraction_tmul, contraction_tmul]

theorem raiz_meio : (((Real.sqrt 2)⁻¹ : ℝ) : ℂ) * (((Real.sqrt 2)⁻¹ : ℝ) : ℂ) = (2⁻¹ : ℂ) := by
  have h : ((Real.sqrt 2)⁻¹ : ℝ) * ((Real.sqrt 2)⁻¹) = 2⁻¹ := by
    rw [← mul_inv, Real.mul_self_sqrt (by norm_num)]
  rw [← Complex.ofReal_mul, h]
  norm_num

/-- (auxiliar) Norma 1 a partir de ⟪z, z⟫ = 1. -/
theorem norma_um_de_inner {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] (z : H) (h : ⟪z, z⟫_ℂ = 1) :
    ‖z‖ = 1 := by
  have h2 : ‖z‖ ^ 2 = 1 := by
    have := (inner_self_eq_norm_sq (𝕜 := ℂ) z).symm
    rw [h] at this
    simpa using this
  have hn := norm_nonneg z
  have h3 : (‖z‖ - 1) * (‖z‖ + 1) = 0 := by ring_nf; linarith
  rcases mul_eq_zero.mp h3 with h4 | h4
  · linarith
  · linarith

/-- ★★ NORMA DO PAR: com f, g ortonormais e u, v de norma 1, o par tem norma 1. -/
theorem norma_do_par (f g : E) (u v : G) (hf : ‖f‖ = 1) (hg : ‖g‖ = 1) (hfg : ⟪f, g⟫_ℂ = 0) (hu : ‖u‖ = 1)
    (hv : ‖v‖ = 1) : ‖vetorPar f g u v‖ = 1 := by
  apply norma_um_de_inner
  have hff : ⟪f, f⟫_ℂ = 1 := by rw [inner_self_eq_norm_sq_to_K, hf]; simp
  have hgg : ⟪g, g⟫_ℂ = 1 := by rw [inner_self_eq_norm_sq_to_K, hg]; simp
  have huu : ⟪u, u⟫_ℂ = 1 := by rw [inner_self_eq_norm_sq_to_K, hu]; simp
  have hvv : ⟪v, v⟫_ℂ = 1 := by rw [inner_self_eq_norm_sq_to_K, hv]; simp
  have hgf : ⟪g, f⟫_ℂ = 0 := inner_eq_zero_symm.mp hfg
  unfold vetorPar
  simp only [inner_smul_left, inner_smul_right, Completion.inner_coe, inner_add_left, inner_add_right,
    TensorProduct.inner_tmul, hff, hgg, huu, hvv, hfg, hgf, Complex.conj_ofReal]
  linear_combination (2 : ℂ) * raiz_meio

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
    smul_apply, projPar_apply, Complex.conj_ofReal, inner_conj_symm]
  have hs := raiz_meio
  linear_combination (⟪y, J.symm f⟫_ℂ * ⟪J.symm f, x⟫_ℂ + ⟪y, J.symm g⟫_ℂ * ⟪J.symm g, x⟫_ℂ) * hs

omit [CompleteSpace E] in
/-- ★★★ A MEIA-NAT DO PROJETOR: para a, b ortonormais e ρ = ½·P(a, b): ρ a = ½ a, ρ b = ½ b (cada psíon pesa ½); ρ(ρ a) ≠ ρ a
    (o indivíduo não ecoa: ρ não é projeção); os pesos somam 1; e 1 − pureza = ½ (o CCI da Meia-Nat). -/
theorem meia_nat_do_projetor (a b : E) (ha : ‖a‖ = 1) (hb : ‖b‖ = 1) (hab : ⟪a, b⟫_ℂ = 0) :
    ((2⁻¹ : ℂ) • projPar a b) a = (2⁻¹ : ℂ) • a
    ∧ ((2⁻¹ : ℂ) • projPar a b) b = (2⁻¹ : ℂ) • b
    ∧ ((2⁻¹ : ℂ) • projPar a b) (((2⁻¹ : ℂ) • projPar a b) a) ≠ ((2⁻¹ : ℂ) • projPar a b) a
    ∧ ⟪a, ((2⁻¹ : ℂ) • projPar a b) a⟫_ℂ + ⟪b, ((2⁻¹ : ℂ) • projPar a b) b⟫_ℂ = 1
    ∧ 1 - (⟪a, ((2⁻¹ : ℂ) • projPar a b) (((2⁻¹ : ℂ) • projPar a b) a)⟫_ℂ
          + ⟪b, ((2⁻¹ : ℂ) • projPar a b) (((2⁻¹ : ℂ) • projPar a b) b)⟫_ℂ) = 2⁻¹ := by
  have haa : ⟪a, a⟫_ℂ = 1 := by rw [inner_self_eq_norm_sq_to_K, ha]; simp
  have hbb : ⟪b, b⟫_ℂ = 1 := by rw [inner_self_eq_norm_sq_to_K, hb]; simp
  have hba : ⟪b, a⟫_ℂ = 0 := inner_eq_zero_symm.mp hab
  have hPa : ((2⁻¹ : ℂ) • projPar a b) a = (2⁻¹ : ℂ) • a := by
    rw [smul_apply, projPar_apply, haa, hba, one_smul, zero_smul, add_zero]
  have hPb : ((2⁻¹ : ℂ) • projPar a b) b = (2⁻¹ : ℂ) • b := by
    rw [smul_apply, projPar_apply, hab, hbb, one_smul, zero_smul, zero_add]
  have hPPa : ((2⁻¹ : ℂ) • projPar a b) (((2⁻¹ : ℂ) • projPar a b) a) = (4⁻¹ : ℂ) • a := by
    rw [hPa, map_smul, hPa, smul_smul]; norm_num
  have hPPb : ((2⁻¹ : ℂ) • projPar a b) (((2⁻¹ : ℂ) • projPar a b) b) = (4⁻¹ : ℂ) • b := by
    rw [hPb, map_smul, hPb, smul_smul]; norm_num
  have ha0 : a ≠ 0 := by intro h; rw [h, norm_zero] at ha; exact zero_ne_one ha
  refine ⟨hPa, hPb, ?_, ?_, ?_⟩
  · rw [hPPa, hPa]
    intro h
    have h2 : ((4⁻¹ : ℂ) - 2⁻¹) • a = 0 := by rw [sub_smul, h, sub_self]
    rcases smul_eq_zero.mp h2 with h3 | h3
    · norm_num at h3
    · exact ha0 h3
  · rw [hPa, hPb, inner_smul_right, inner_smul_right, haa, hbb]; norm_num
  · rw [hPPa, hPPb, inner_smul_right, inner_smul_right, haa, hbb]; norm_num

end Geral

/-! ### 2. As duas polarizações da fibra: um par ortonormal em L²(μ; ℂ²) -/

section Polarizacoes
open MeasureTheory

/-- D = diag(1, −1) e S = a troca, na fibra ℂ² (as duas polarizações). -/
def matD : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]
def matS : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]

theorem matD_mul_self : matD * matD = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [matD, Matrix.mul_apply, Fin.sum_univ_two]
theorem matS_mul_self : matS * matS = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [matS, Matrix.mul_apply, Fin.sum_univ_two]
theorem matD_matS : matD * matS = -(matS * matD) := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [matD, matS, Matrix.mul_apply, Fin.sum_univ_two]
theorem matD_herm : star matD = matD := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [matD, Matrix.star_apply]
theorem matS_herm : star matS = matS := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [matS, Matrix.star_apply]

def polD : EuclideanSpace ℂ (Fin 2) →L[ℂ] EuclideanSpace ℂ (Fin 2) := Matrix.toEuclideanCLM (𝕜 := ℂ) matD
def polS : EuclideanSpace ℂ (Fin 2) →L[ℂ] EuclideanSpace ℂ (Fin 2) := Matrix.toEuclideanCLM (𝕜 := ℂ) matS

theorem polD_polD (a : EuclideanSpace ℂ (Fin 2)) : polD (polD a) = a := by
  have h : polD * polD = 1 := by
    rw [polD, ← map_mul, matD_mul_self, map_one]
  simpa using congrArg (fun L : EuclideanSpace ℂ (Fin 2) →L[ℂ] EuclideanSpace ℂ (Fin 2) => L a) h

theorem polD_polS (a : EuclideanSpace ℂ (Fin 2)) : polD (polS a) = -(polS (polD a)) := by
  have h : polD * polS = -(polS * polD) := by
    rw [polD, polS, ← map_mul, matD_matS, map_neg, map_mul]
  simpa using congrArg (fun L : EuclideanSpace ℂ (Fin 2) →L[ℂ] EuclideanSpace ℂ (Fin 2) => L a) h

theorem polD_adjoint : ContinuousLinearMap.adjoint polD = polD := by
  rw [← ContinuousLinearMap.star_eq_adjoint, polD, ← map_star, matD_herm]

theorem polS_adjoint : ContinuousLinearMap.adjoint polS = polS := by
  rw [← ContinuousLinearMap.star_eq_adjoint, polS, ← map_star, matS_herm]

theorem polD_autoadjunta (a b : EuclideanSpace ℂ (Fin 2)) : ⟪polD a, b⟫_ℂ = ⟪a, polD b⟫_ℂ := by
  rw [← ContinuousLinearMap.adjoint_inner_left, polD_adjoint]

theorem polS_isometria (a b : EuclideanSpace ℂ (Fin 2)) : ⟪polS a, polS b⟫_ℂ = ⟪a, b⟫_ℂ := by
  have h : polS * polS = 1 := by
    rw [polS, ← map_mul, matS_mul_self, map_one]
  have ha : polS (polS a) = a := by
    simpa using congrArg (fun L : EuclideanSpace ℂ (Fin 2) →L[ℂ] EuclideanSpace ℂ (Fin 2) => L a) h
  rw [← ContinuousLinearMap.adjoint_inner_left, polS_adjoint, ha]

variable {α : Type*} [MeasurableSpace α] {μ : Measure α}

/-- D e S levantados a L²(μ; ℂ²), ponto a ponto. -/
def liftD : Lp (EuclideanSpace ℂ (Fin 2)) 2 μ →L[ℂ] Lp (EuclideanSpace ℂ (Fin 2)) 2 μ := polD.compLpL 2 μ
def liftS : Lp (EuclideanSpace ℂ (Fin 2)) 2 μ →L[ℂ] Lp (EuclideanSpace ℂ (Fin 2)) 2 μ := polS.compLpL 2 μ

theorem liftD_ae (f : Lp (EuclideanSpace ℂ (Fin 2)) 2 μ) : liftD f =ᵐ[μ] fun t => polD (f t) :=
  polD.coeFn_compLpL f
theorem liftS_ae (f : Lp (EuclideanSpace ℂ (Fin 2)) 2 μ) : liftS f =ᵐ[μ] fun t => polS (f t) :=
  polS.coeFn_compLpL f

theorem liftD_autoadjunta (f g : Lp (EuclideanSpace ℂ (Fin 2)) 2 μ) : ⟪liftD f, g⟫_ℂ = ⟪f, liftD g⟫_ℂ := by
  rw [L2.inner_def, L2.inner_def]
  apply integral_congr_ae
  filter_upwards [liftD_ae f, liftD_ae g] with t h1 h2
  rw [h1, h2]
  exact polD_autoadjunta _ _

theorem liftS_isometria (f g : Lp (EuclideanSpace ℂ (Fin 2)) 2 μ) : ⟪liftS f, liftS g⟫_ℂ = ⟪f, g⟫_ℂ := by
  rw [L2.inner_def, L2.inner_def]
  apply integral_congr_ae
  filter_upwards [liftS_ae f, liftS_ae g] with t h1 h2
  rw [h1, h2]
  exact polS_isometria _ _

theorem liftD_liftD (f : Lp (EuclideanSpace ℂ (Fin 2)) 2 μ) : liftD (liftD f) = f := by
  apply Lp.ext
  filter_upwards [liftD_ae (liftD f), liftD_ae f] with t h1 h2
  rw [h1, h2, polD_polD]

theorem liftD_liftS (f : Lp (EuclideanSpace ℂ (Fin 2)) 2 μ) : liftD (liftS f) = -(liftS (liftD f)) := by
  apply Lp.ext
  filter_upwards [liftD_ae (liftS f), liftS_ae f, Lp.coeFn_neg (liftS (liftD f)), liftS_ae (liftD f), liftD_ae f]
    with t h1 h2 h3 h4 h5
  rw [h1, h2, h3, Pi.neg_apply, h4, h5, polD_polS]

/-- ★★ AS DUAS POLARIZAÇÕES DÃO UM PAR ORTONORMAL: de qualquer vetor não nulo de L²(μ; ℂ²) sai um par ortonormal (um autovetor de D
    e a sua troca por S, que tem o autovalor oposto). -/
theorem par_ortonormal_das_polarizacoes (x : Lp (EuclideanSpace ℂ (Fin 2)) 2 μ) (hx : x ≠ 0) :
    ∃ f g : Lp (EuclideanSpace ℂ (Fin 2)) 2 μ, ‖f‖ = 1 ∧ ‖g‖ = 1 ∧ ⟪f, g⟫_ℂ = 0 := by
  have chave : ∀ (f : Lp (EuclideanSpace ℂ (Fin 2)) 2 μ) (e : ℂ), ‖f‖ = 1 → liftD f = e • f → (e = 1 ∨ e = -1) →
      ⟪f, liftS f⟫_ℂ = 0 ∧ ‖liftS f‖ = 1 := by
    intro f e hf hDf he
    have hce : starRingEnd ℂ e = e := by rcases he with rfl | rfl <;> simp
    have he0 : e ≠ 0 := by rcases he with rfl | rfl <;> norm_num
    constructor
    · have h1 : ⟪liftD f, liftS f⟫_ℂ = ⟪f, liftD (liftS f)⟫_ℂ := liftD_autoadjunta f (liftS f)
      rw [liftD_liftS, hDf, map_smul, inner_smul_left, inner_neg_right, inner_smul_right, hce] at h1
      have h2 : e * ⟪f, liftS f⟫_ℂ = 0 := by linear_combination h1 / 2
      exact (mul_eq_zero.mp h2).resolve_left he0
    · apply norma_um_de_inner
      rw [liftS_isometria, inner_self_eq_norm_sq_to_K, hf]; simp
  have normaliza : ∀ (w : Lp (EuclideanSpace ℂ (Fin 2)) 2 μ) (e : ℂ), w ≠ 0 → liftD w = e • w → (e = 1 ∨ e = -1) →
      ∃ f g : Lp (EuclideanSpace ℂ (Fin 2)) 2 μ, ‖f‖ = 1 ∧ ‖g‖ = 1 ∧ ⟪f, g⟫_ℂ = 0 := by
    intro w e hw hD he
    have hf : ‖(((‖w‖)⁻¹ : ℝ) : ℂ) • w‖ = 1 := by
      rw [norm_smul, Complex.norm_real, Real.norm_eq_abs, abs_inv, abs_norm, inv_mul_cancel₀ (norm_ne_zero_iff.mpr hw)]
    have hDf : liftD ((((‖w‖)⁻¹ : ℝ) : ℂ) • w) = e • ((((‖w‖)⁻¹ : ℝ) : ℂ) • w) := by
      rw [map_smul, hD, smul_comm]
    obtain ⟨h0, h1⟩ := chave _ e hf hDf he
    exact ⟨_, _, hf, h1, h0⟩
  by_cases hp : x + liftD x = 0
  · have hm : liftD x = (-1 : ℂ) • x := by
      rw [neg_one_smul]; exact eq_neg_of_add_eq_zero_right hp
    exact normaliza x (-1) hx hm (Or.inr rfl)
  · have hD : liftD (x + liftD x) = (1 : ℂ) • (x + liftD x) := by
      rw [map_add, liftD_liftD, one_smul, add_comm]
    exact normaliza _ 1 hp hD (Or.inl rfl)

end Polarizacoes

/-- ★★ EXISTE UM PAR ORTONORMAL NA UMA-PARTÍCULA DA LUZ (H1 = L²(μ₀; ℂ²)): pelas duas polarizações. -/
theorem existe_par_ortonormal_em_H1 :
    ∃ f g : TGLExt.ImportedSQ.H1, ‖f‖ = 1 ∧ ‖g‖ = 1 ∧ ⟪f, g⟫_ℂ = 0 := by
  haveI := AuditF13v31.H1_nontrivial
  obtain ⟨x, hx⟩ := exists_ne (0 : TGLExt.ImportedSQ.H1)
  exact par_ortonormal_das_polarizacoes x hx

/-! ### 3. A face de Fock concreta: o par de psíons no setor 2 -/

section FaceDeFock
open F1Rede.BosonicSectors F1Rede.SectorDirectSum F1Rede.BosonicFock TGLExt.ImportedSQ F1Rede.CanonicalWedge

/-- O PAR DE PSÍONS: (√2)⁻¹ (f⊗f + g⊗g), escrito no completamento de H1 ⊗ (H1 ⊗ ℂ) — que é o espaço do setor 2 do Fock concreto. -/
def parSetor (f g : H1) : Completion (H1 ⊗[ℂ] Algebraic 1) := vetorPar f g (pureAlgebraic f 1) (pureAlgebraic g 1)

theorem parSetor_eq (f g : H1) :
    (parSetor f g : TensorHilbert 2) = (((Real.sqrt 2)⁻¹ : ℝ) : ℂ) • (pureCompleted 2 f + pureCompleted 2 g) := by
  unfold parSetor vetorPar
  rw [Completion.coe_add]
  rfl

theorem parSetor_mem (f g : H1) : (parSetor f g : TensorHilbert 2) ∈ symmetricSpace 2 := by
  rw [parSetor_eq]
  exact Submodule.smul_mem _ _ (Submodule.add_mem _ (pureCompleted_mem 2 f) (pureCompleted_mem 2 g))

/-- O PAR NO FOCK CONCRETO: o vetor de dois psíons no setor 2 do Fock bosônico da luz (`F1Rede.BosonicFock.F`). -/
def parFock (f g : H1) : F := sectorEmbedding (E := Sectors) 2 ⟨(parSetor f g : TensorHilbert 2), parSetor_mem f g⟩

theorem norma_de_pureAlgebraic_um (f : H1) (hf : ‖f‖ = 1) : ‖pureAlgebraic f 1‖ = 1 := by
  rw [pureAlgebraic_norm, hf, pow_one]

theorem inner_de_pureAlgebraic_um (f g : H1) : ⟪pureAlgebraic f 1, pureAlgebraic g 1⟫_ℂ = ⟪f, g⟫_ℂ := by
  change ⟪(f ⊗ₜ[ℂ] (1 : ℂ) : H1 ⊗[ℂ] ℂ), g ⊗ₜ[ℂ] (1 : ℂ)⟫_ℂ = _
  rw [TensorProduct.inner_tmul]
  simp

/-- ★★ O PAR TEM NORMA 1. -/
theorem parFock_norma (f g : H1) (hf : ‖f‖ = 1) (hg : ‖g‖ = 1) (hfg : ⟪f, g⟫_ℂ = 0) : ‖parFock f g‖ = 1 := by
  unfold parFock
  rw [(sectorEmbedding (E := Sectors) 2).norm_map]
  change ‖(parSetor f g : TensorHilbert 2)‖ = 1
  exact norma_do_par f g _ _ hf hg hfg (norma_de_pureAlgebraic_um f hf) (norma_de_pureAlgebraic_um g hg)

/-- ★★ O PAR É OUTRA COISA QUE O VÁCUO E QUE UMA PARTÍCULA: ortogonal ao vácuo (setor 0) e a toda uma-partícula (setor 1). -/
theorem parFock_ortogonal_ao_vacuo (f g : H1) : ⟪vacuum, parFock f g⟫_ℂ = 0 :=
  different_sectors_orthogonal (E := Sectors) 0 2 (by decide) vacuumSector _

theorem parFock_ortogonal_a_uma_particula (f g x : H1) : ⟪oneParticle x, parFock f g⟫_ℂ = 0 :=
  different_sectors_orthogonal (E := Sectors) 1 2 (by decide) (oneParticleEmbedding x) _

/-- ★★★ A MARGINAL DO PAR É A MEIA-NAT, NA FACE DE FOCK: o reduzido do par (pela conjugação canônica da cunha, `Jcandidate`) é
    ½ vezes o projetor de posto dois sobre J⁻¹ f e J⁻¹ g. -/
theorem a_marginal_do_par (f g : H1) (hf : ‖f‖ = 1) (hg : ‖g‖ = 1) (hfg : ⟪f, g⟫_ℂ = 0) :
    reduced Jcandidate (parSetor f g) = (2⁻¹ : ℂ) • projPar (Jcandidate.symm f) (Jcandidate.symm g) :=
  reduzido_do_par Jcandidate f g _ _ (norma_de_pureAlgebraic_um f hf) (norma_de_pureAlgebraic_um g hg)
    (by rw [inner_de_pureAlgebraic_um, hfg])

/-- ★★★ O PAR NA FACE DE FOCK [a ligação que a v407 deixou aberta (E21 da v408); construção da gerência c1, 05/11/2026]: existe um par
    ortonormal f, g na uma-partícula da luz; o par de psíons está no setor 2 do Fock concreto, tem norma 1 e é ortogonal ao vácuo e a toda
    uma-partícula; a sua marginal (pela conjugação da cunha) é ½ vezes um projetor de posto dois: cada psíon pesa ½, o indivíduo não ecoa,
    os pesos somam 1 e 1 − pureza = ½ — a MESMA Meia-Nat da face finita (`bell_reduced_half`, `bell_cci_half`). -/
theorem o_par_na_face_de_fock :
    ∃ f g : H1, ‖f‖ = 1 ∧ ‖g‖ = 1 ∧ ⟪f, g⟫_ℂ = 0
      ∧ ‖parFock f g‖ = 1
      ∧ ⟪vacuum, parFock f g⟫_ℂ = 0
      ∧ (∀ x : H1, ⟪oneParticle x, parFock f g⟫_ℂ = 0)
      ∧ reduced Jcandidate (parSetor f g) = (2⁻¹ : ℂ) • projPar (Jcandidate.symm f) (Jcandidate.symm g)
      ∧ (reduced Jcandidate (parSetor f g)) (Jcandidate.symm f) = (2⁻¹ : ℂ) • Jcandidate.symm f
      ∧ (reduced Jcandidate (parSetor f g)) ((reduced Jcandidate (parSetor f g)) (Jcandidate.symm f))
          ≠ (reduced Jcandidate (parSetor f g)) (Jcandidate.symm f)
      ∧ 1 - (⟪Jcandidate.symm f, (reduced Jcandidate (parSetor f g)) ((reduced Jcandidate (parSetor f g)) (Jcandidate.symm f))⟫_ℂ
            + ⟪Jcandidate.symm g, (reduced Jcandidate (parSetor f g)) ((reduced Jcandidate (parSetor f g)) (Jcandidate.symm g))⟫_ℂ)
          = 2⁻¹
      ∧ TGL.GravitonShadow.ptr TGL.GravitonShadow.bellProjector = (2⁻¹ : ℂ) • 1
      ∧ 1 - Matrix.trace (TGL.GravitonShadow.ptr TGL.GravitonShadow.bellProjector
            * TGL.GravitonShadow.ptr TGL.GravitonShadow.bellProjector) = 2⁻¹ := by
  obtain ⟨f, g, hf, hg, hfg⟩ := existe_par_ortonormal_em_H1
  obtain ⟨ha, hb, hab⟩ := espelho_ortonormal Jcandidate f g hf hg hfg
  have hm := a_marginal_do_par f g hf hg hfg
  obtain ⟨h1, -, h3, -, h5⟩ := meia_nat_do_projetor _ _ ha hb hab
  refine ⟨f, g, hf, hg, hfg, parFock_norma f g hf hg hfg, parFock_ortogonal_ao_vacuo f g,
    fun x => parFock_ortogonal_a_uma_particula f g x, hm, ?_, ?_, ?_, TGL.GravitonShadow.bell_reduced_half,
    TGL.GravitonShadow.bell_cci_half⟩
  · rw [hm]; exact h1
  · rw [hm]; exact h3
  · rw [hm]; exact h5

end FaceDeFock

end TGLExt.ParNaFaceDeFock

#print axioms TGLExt.ParNaFaceDeFock.inner_espelho
#print axioms TGLExt.ParNaFaceDeFock.reduzido_do_par
#print axioms TGLExt.ParNaFaceDeFock.norma_do_par
#print axioms TGLExt.ParNaFaceDeFock.meia_nat_do_projetor
#print axioms TGLExt.ParNaFaceDeFock.par_ortonormal_das_polarizacoes
#print axioms TGLExt.ParNaFaceDeFock.existe_par_ortonormal_em_H1
#print axioms TGLExt.ParNaFaceDeFock.parFock_norma
#print axioms TGLExt.ParNaFaceDeFock.parFock_ortogonal_ao_vacuo
#print axioms TGLExt.ParNaFaceDeFock.a_marginal_do_par
#print axioms TGLExt.ParNaFaceDeFock.o_par_na_face_de_fock
