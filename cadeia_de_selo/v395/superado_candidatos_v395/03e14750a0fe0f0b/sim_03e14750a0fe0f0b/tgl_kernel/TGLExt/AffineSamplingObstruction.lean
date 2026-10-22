-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — LOTE 058..062 (09/09/2026), transposta em 10/09/2026 (ENTREGA_062 = elo do lote)
-- Os 77 modulos da sessao de 09/09 da bancada (cadeia de copias integradas 63 -> 72 -> 77 sobre a base v337 lida),
--   1065 teoremas declarados pela bancada. Cinco entregas espontaneas:
--   058: ATLAS GRAVITACIONAL SELECIONADO — continuidade + amostras densas + cortes racionais determinam o registro em U;
--     a leitura geometricLogReading caracteriza a sequencia booleana; a selecao por classe instancia IALDState e os
--     teoremas do Nome; o decodificador devolve classe, g, T e os pesos; Einstein do registro decodificado decorre das
--     leis de area e conservacao do registro original (jets, Levi-Civita, Ricci, Einstein preservados).
--   059: caracter completo reconstroi g/T/Einstein condicionado a area e conservacao; COLAGEM da Lambda unico nas
--     cartas compativeis; naturalidade infinitesimal de Ricci/escalar/Einstein em carta curva; potencial XX somavel
--     auto-adjunto com cauda em norma; exemplo de acoplamento atestado.
--   060: COCICLO UNITARIO INFINITO do potencial XX somavel na acao modular canonica; controle uniforme dos cortes;
--     gerador iV e ODE; grupo beta_t = Ad_u(t) o alpha_t que preserva o fator; transformacao finita de
--     Levi-Civita/Ricci/escalar/Einstein e lei de transformacao de Einstein nas sobreposicoes metricas abertas.
--   061: interacao local somavel com termos NAO comutativos (testemunha explicita); unicidade potencial <-> cociclo;
--     fase central Z^{-it} (gerador i(V - logZ I)); colagem suave selecionada -> Lambda global unico; estado perturbado
--     de Araki [DERIVED + KNOWN, analitico — NAO Lean].
--   062: seletor canonico e Born; reconstrucao do registro pelo seletor; entrelacamento angular; caracter da fase
--     relativa (duas probabilidades de interferencia recuperam a fase); estimativas de localidade de vinculo.
--   Estatuto: [REAL] o compilado; [DERIVED + KNOWN] Araki; [INPUT] R (o registro) e a origem fisica; [OPEN]
--   correspondencia fisica seletor-registro, materia/conservacao/area para os mesmos dados, atlas fisico compativel,
--   alem da classe globalmente limitada, anomalias e UV. Nenhum nome ligado a H3, area fisica ou gate.
-- Auditoria da gerencia (sessao d554e796, 10/09/2026): lote montado da CADEIA de recibos (INTEGRATION_RESULT 77 -> 72
--   -> 63); 77/77 hashes lidos dos bytes contra os recibos; zero proibidos; guarda de colisao; recompilacao INDEPENDENTE
--   77/77 contra o kernel v337, axiomas no trio; a copia integrada da bancada NAO foi usada (so as fontes congeladas).
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.FisherInformationTensor

set_option autoImplicit false
set_option maxHeartbeats 8000000
namespace ChatgptAudit.AffineObstruction
open Matrix Filter Topology Set TGLExt ChatgptAudit.Coherent023
open ChatgptAudit.Micro021 ChatgptAudit.Flow019 ChatgptAudit.Flow020 ChatgptAudit.FisherField
open scoped ContDiff
noncomputable section

/-- A covector is fixed by its values on the Minkowski null cone. -/
theorem linear_map_zero_of_eta_null
    (L : Coordinate4 →ₗ[ℝ] ℝ)
    (hL : ∀ v, tensorQuad eta4 v = 0 → L v = 0) : L = 0 := by
  let e (i : Fin 4) : Coordinate4 := Pi.single i 1
  have hp (i : Fin 4) (hi : i ≠ 0) : tensorQuad eta4 (e 0 + e i) = 0 := by
    fin_cases i <;> simp [e, tensorQuad, eta4, Matrix.mulVec, dotProduct,
      Pi.single_apply, Fin.sum_univ_four] at *
  have hm (i : Fin 4) (hi : i ≠ 0) : tensorQuad eta4 (e 0 - e i) = 0 := by
    fin_cases i <;> simp [e, tensorQuad, eta4, Matrix.mulVec, dotProduct,
      Pi.single_apply, Fin.sum_univ_four] at *
  have he0 : L (e 0) = 0 := by
    have h1 := hL (e 0 + e 1) (hp 1 (by decide))
    have h2 := hL (e 0 - e 1) (hm 1 (by decide))
    simp only [map_add, map_sub] at h1 h2
    linarith
  have he (i : Fin 4) : L (e i) = 0 := by
    by_cases hi : i = 0
    · simpa only [hi] using he0
    · have hh := hL (e 0 + e i) (hp i hi)
      simpa only [map_add, he0, zero_add] using hh
  apply LinearMap.ext
  intro v
  have hv : v = ∑ i : Fin 4, v i • e i := by
    ext j
    simp [e, Pi.single_apply]
  rw [hv, map_sum]
  simp only [map_smul, he, smul_zero, Finset.sum_const_zero, LinearMap.zero_apply]

/-- The null generators are used pointwise; no smooth tetrad is required. -/
theorem linear_map_zero_of_lorentz_null (g : Tensor4) (hg : LorentzByCongruence g)
    (L : Coordinate4 →ₗ[ℝ] ℝ)
    (hL : ∀ v, tensorQuad g v = 0 → L v = 0) : L = 0 := by
  obtain ⟨E, hE, hg⟩ := hg
  let D := E⁻¹
  have hED : E*D = 1 := Matrix.mul_nonsing_inv E hE
  have hDE : D*E = 1 := Matrix.nonsing_inv_mul E hE
  let K : Coordinate4 →ₗ[ℝ] ℝ := L.comp (Matrix.mulVecLin D)
  have hK : K = 0 := linear_map_zero_of_eta_null K (by
    intro v hv
    change L (D *ᵥ v) = 0
    apply hL
    rw [hg, tensorQuad_congruence, Matrix.mulVec_mulVec, hED, Matrix.one_mulVec]
    exact hv)
  apply LinearMap.ext
  intro v
  have hh := congrArg (fun f : Coordinate4 →ₗ[ℝ] ℝ => f (E *ᵥ v)) hK
  simpa only [K, LinearMap.comp_apply, Matrix.mulVecLin_apply,
    Matrix.mulVec_mulVec, hDE, Matrix.one_mulVec, LinearMap.zero_apply] using hh

theorem quadratic_limit_forces_zero_derivative (f : ℝ → ℝ) (d c : ℝ)
    (hd : HasDerivAt f d 0)
    (hq : Tendsto (fun t => (f t - f 0)/t^2) (𝓝[<] 0) (𝓝 c)) : d = 0 := by
  have ht : Tendsto (fun t : ℝ => t) (𝓝[<] 0) (𝓝 0) :=
    continuousAt_id.tendsto.mono_left nhdsWithin_le_nhds
  have he : (fun t => ((f t - f 0)/t^2)*t) =ᶠ[𝓝[<] (0 : ℝ)]
      (fun t => (f t - f 0)/t) := by
    filter_upwards [self_mem_nhdsWithin] with t ht
    have hn : t ≠ 0 := ne_of_lt ht
    field_simp
  have hz : Tendsto (fun t => (f t - f 0)/t) (𝓝[<] 0) (𝓝 0) := by
    simpa using (hq.mul ht).congr' he
  have hder : Tendsto (fun t => (f t - f 0)/t) (𝓝[<] 0) (𝓝 d) := by
    simpa only [zero_add, smul_eq_mul, div_eq_mul_inv, mul_comm] using hd.tendsto_slope_zero_left
  exact tendsto_nhds_unique hder hz

variable {ι : Type} [Fintype ι]

def probabilityEntropyField (P : Coordinate4 → ι → ℝ) : Coordinate4 → ℝ :=
  fun x => finiteEntropy (P x)

theorem probability_entropy_smooth (U : Set Coordinate4)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (hp : ∀ x ∈ U, ∀ i, 0 < P x i) :
    ContDiffOn ℝ ∞ (probabilityEntropyField P) U := by
  unfold probabilityEntropyField finiteEntropy entropyAtom
  apply ContDiffOn.sum
  intro i _
  exact ((hP i).mul ((hP i).log (fun x hx => ne_of_gt (hp x hx i)))).neg

theorem affine_area_matching_entropy_quadratic_limit
    (U : Set Coordinate4) (hU : IsOpen U) (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (htrace : ∀ y, ∑ i, P y i = 1)
    (x v : Coordinate4) (hx : x ∈ U) (screen : EquilibriumScreenData U g Gamma x v)
    (ht : ∀ i j a, Gamma x i a j = Gamma x j a i) (eta : ℝ)
    (harea : Tendsto (fun t => microscopicAreaError
      (probabilityFieldCurve U hU P hP htrace x v hx) eta
      (inducedArea g screen.curve screen.screen.vectors) t / t^2)
      (𝓝[<] 0) (𝓝 0)) :
    Tendsto (fun t => (probabilityEntropyField P (x + t • v) -
      probabilityEntropyField P x)/t^2) (𝓝[<] 0)
      (𝓝 (eta * (-tensorQuad (coordinateRicci Gamma x) v / 2))) := by
  have hA := screen_area_quadratic_limit U hU g Gamma hg hG x v screen ht
  have hh := harea.add (hA.const_mul eta)
  have he : (fun t => microscopicAreaError
      (probabilityFieldCurve U hU P hP htrace x v hx) eta
      (inducedArea g screen.curve screen.screen.vectors) t / t^2 +
      eta * ((inducedArea g screen.curve screen.screen.vectors t - 1)/t^2)) =
      (fun t => (probabilityEntropyField P (x + t • v) - probabilityEntropyField P x)/t^2) := by
    funext t
    dsimp [microscopicAreaError, probabilityFieldCurve, probabilityEntropyField]
    rw [equilibrium_screen_area_initial U g Gamma x v screen]
    ring
  simpa only [he, zero_add] using hh

theorem affine_area_matching_entropy_derivative_zero
    (U : Set Coordinate4) (hU : IsOpen U) (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (htrace : ∀ y, ∑ i, P y i = 1) (hp : ∀ x ∈ U, ∀ i, 0 < P x i)
    (x v : Coordinate4) (hx : x ∈ U) (screen : EquilibriumScreenData U g Gamma x v)
    (ht : ∀ i j a, Gamma x i a j = Gamma x j a i) (eta : ℝ)
    (harea : Tendsto (fun t => microscopicAreaError
      (probabilityFieldCurve U hU P hP htrace x v hx) eta
      (inducedArea g screen.curve screen.screen.vectors) t / t^2)
      (𝓝[<] 0) (𝓝 0)) :
    fderiv ℝ (probabilityEntropyField P) x v = 0 := by
  have hq := affine_area_matching_entropy_quadratic_limit U hU g Gamma hg hG
    P hP htrace x v hx screen ht eta harea
  have hd := ((probability_entropy_smooth U P hP hp).differentiableOn
    (by simp)).differentiableAt (hU.mem_nhds hx)
  have hl : HasDerivAt (fun t : ℝ => probabilityEntropyField P (x + t • v))
      (fderiv ℝ (probabilityEntropyField P) x v) 0 :=
    hd.hasFDerivAt.comp_hasDerivAt_of_eq 0 (probability_line_derivative x v 0) (by simp)
  apply quadratic_limit_forces_zero_derivative _ _ _ hl
  simpa only [zero_smul, add_zero] using hq

/-- Matching of the same affine probability sampling on every null pencil. -/
def UniversalAffineAreaMatching
    (U : Set Coordinate4) (hU : IsOpen U) (g : TensorField4) (Gamma : ConnectionField4)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (htrace : ∀ y, ∑ i, P y i = 1) (eta : ℝ) : Prop :=
  ∀ x (hx : x ∈ U) v, v ≠ 0 → tensorQuad (g x) v = 0 →
    ∃ screen : EquilibriumScreenData U g Gamma x v,
      Tendsto (fun t => microscopicAreaError
        (probabilityFieldCurve U hU P hP htrace x v hx) eta
        (inducedArea g screen.curve screen.screen.vectors) t / t^2)
        (𝓝[<] 0) (𝓝 0)

theorem universal_affine_area_matching_entropy_fderiv_zero
    (U : Set Coordinate4) (hU : IsOpen U) (g : TensorField4) (Gamma : ConnectionField4)
    (hLor : ∀ x ∈ U, LorentzByCongruence (g x))
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (ht : ∀ x ∈ U, ∀ i j a, Gamma x i a j = Gamma x j a i)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (htrace : ∀ y, ∑ i, P y i = 1) (hp : ∀ x ∈ U, ∀ i, 0 < P x i)
    (eta : ℝ) (hmatch : UniversalAffineAreaMatching U hU g Gamma P hP htrace eta) :
    ∀ x ∈ U, fderiv ℝ (probabilityEntropyField P) x = 0 := by
  intro x hx
  have hL := linear_map_zero_of_lorentz_null (g x) (hLor x hx)
    (fderiv ℝ (probabilityEntropyField P) x).toLinearMap (by
      intro v hn
      by_cases hv : v = 0
      · simp [hv]
      · obtain ⟨screen, harea⟩ := hmatch x hx v hv hn
        exact affine_area_matching_entropy_derivative_zero U hU g Gamma hg hG
          P hP htrace hp x v hx screen (ht x hx) eta harea)
  apply ContinuousLinearMap.ext
  intro v
  exact congrArg (fun L : Coordinate4 →ₗ[ℝ] ℝ => L v) hL

theorem universal_affine_area_matching_entropy_constant
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hLor : ∀ x ∈ U, LorentzByCongruence (g x))
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (ht : ∀ x ∈ U, ∀ i j a, Gamma x i a j = Gamma x j a i)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (htrace : ∀ y, ∑ i, P y i = 1) (hp : ∀ x ∈ U, ∀ i, 0 < P x i)
    (eta : ℝ) (hmatch : UniversalAffineAreaMatching U hU g Gamma P hP htrace eta) :
    ∃ entropy : ℝ, ∀ x ∈ U, probabilityEntropyField P x = entropy := by
  apply hU.exists_is_const_of_fderiv_eq_zero hconn
    ((probability_entropy_smooth U P hP hp).differentiableOn (by simp))
  exact universal_affine_area_matching_entropy_fderiv_zero U hU g Gamma hLor hg hG ht
    P hP htrace hp eta hmatch



theorem constant_entropy_affine_area_matching_ricci_null_zero
    (U : Set Coordinate4) (hU : IsOpen U) (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (htrace : ∀ y, ∑ i, P y i = 1)
    (hconst : ∃ entropy : ℝ, ∀ y ∈ U, probabilityEntropyField P y = entropy)
    (x v : Coordinate4) (hx : x ∈ U) (screen : EquilibriumScreenData U g Gamma x v)
    (ht : ∀ i j a, Gamma x i a j = Gamma x j a i) (eta : ℝ) (heta : eta ≠ 0)
    (harea : Tendsto (fun t => microscopicAreaError
      (probabilityFieldCurve U hU P hP htrace x v hx) eta
      (inducedArea g screen.curve screen.screen.vectors) t / t^2)
      (𝓝[<] 0) (𝓝 0)) :
    tensorQuad (coordinateRicci Gamma x) v = 0 := by
  obtain ⟨entropy, he⟩ := hconst
  have hq := affine_area_matching_entropy_quadratic_limit U hU g Gamma hg hG
    P hP htrace x v hx screen ht eta harea
  have hzfun : (fun t => (probabilityEntropyField P (x + t • v) -
      probabilityEntropyField P x)/t^2) =ᶠ[𝓝[<] (0 : ℝ)] (fun _ => 0) := by
    filter_upwards [(probability_line_eventually U hU x v hx).filter_mono nhdsWithin_le_nhds]
      with t ht
    rw [he _ ht, he x hx, sub_self, zero_div]
  have hz : Tendsto (fun t => (probabilityEntropyField P (x + t • v) -
      probabilityEntropyField P x)/t^2) (𝓝[<] 0) (𝓝 0) :=
    tendsto_const_nhds.congr' hzfun.symm
  have hh := tendsto_nhds_unique hq hz
  have hr := (mul_eq_zero.mp hh).resolve_left heta
  linarith

theorem universal_affine_area_matching_ricci_null_zero
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hLor : ∀ x ∈ U, LorentzByCongruence (g x))
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (ht : ∀ x ∈ U, ∀ i j a, Gamma x i a j = Gamma x j a i)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (htrace : ∀ y, ∑ i, P y i = 1) (hp : ∀ x ∈ U, ∀ i, 0 < P x i)
    (eta : ℝ) (heta : eta ≠ 0)
    (hmatch : UniversalAffineAreaMatching U hU g Gamma P hP htrace eta) :
    ∀ x ∈ U, ∀ v, tensorQuad (g x) v = 0 →
      tensorQuad (coordinateRicci Gamma x) v = 0 := by
  have hconst := universal_affine_area_matching_entropy_constant U hU hconn g Gamma
    hLor hg hG ht P hP htrace hp eta hmatch
  intro x hx v hn
  by_cases hv : v = 0
  · simp [hv, tensorQuad]
  · obtain ⟨screen, harea⟩ := hmatch x hx v hv hn
    exact constant_entropy_affine_area_matching_ricci_null_zero U hU g Gamma hg hG
      P hP htrace hconst x v hx screen (ht x hx) eta heta harea

/-- At zero Ricci contraction, nonnegative matter cannot compensate positive Fisher. -/
theorem zero_ricci_nonnegative_matter_forces_zero_variation
    (p : ι → ℝ) (dp : ι → Coordinate4) (hp : ∀ i, 0 < p i)
    (v : Coordinate4) (eta ricci matter : ℝ)
    (hr : ricci = 0) (hm : 0 ≤ matter)
    (hbalance : eta * ricci =
      2*Real.pi*matter + tensorQuad (fisherTensorAt p dp) v) :
    matter = 0 ∧ (fun i => covectorRead (dp i) v) = 0 := by
  have hf := fisher_tensor_nonnegative p dp hp v
  have hprod : 0 ≤ 2*Real.pi*matter := mul_nonneg (by positivity) hm
  rw [hr, mul_zero] at hbalance
  have hfzero : tensorQuad (fisherTensorAt p dp) v = 0 := by linarith
  have hmzero : matter = 0 := by nlinarith [Real.pi_pos]
  exact ⟨hmzero, (fisher_tensor_null_iff p dp hp v).mp hfzero⟩


#print axioms linear_map_zero_of_eta_null
#print axioms linear_map_zero_of_lorentz_null
#print axioms quadratic_limit_forces_zero_derivative
#print axioms probabilityEntropyField
#print axioms probability_entropy_smooth
#print axioms affine_area_matching_entropy_quadratic_limit
#print axioms affine_area_matching_entropy_derivative_zero
#print axioms UniversalAffineAreaMatching
#print axioms universal_affine_area_matching_entropy_fderiv_zero
#print axioms universal_affine_area_matching_entropy_constant
#print axioms constant_entropy_affine_area_matching_ricci_null_zero
#print axioms universal_affine_area_matching_ricci_null_zero
#print axioms zero_ricci_nonnegative_matter_forces_zero_variation
end
end ChatgptAudit.AffineObstruction
