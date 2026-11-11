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
import TGLExt.ScalarStressConservation
import TGLExt.MicroscopicClausiusBridge

set_option autoImplicit false
set_option maxHeartbeats 8000000
namespace ChatgptAudit.FisherField
open Matrix Filter Topology Set ChatgptAudit.Coherent023 ChatgptAudit.Micro021
open scoped ContDiff
noncomputable section
variable {ι : Type} [Fintype ι]

/-- Information tensor; no Lorentzian metric is asserted. -/
def fisherTensorAt (p : ι → ℝ) (dp : ι → Coordinate4) : Tensor4 :=
  ∑ i, (p i)⁻¹ • Matrix.vecMulVec (dp i) (dp i)

/-- Actual coordinate differential of the probability field. -/
def probabilityDifferential (P : Coordinate4 → ι → ℝ) (x : Coordinate4) (i : ι) : Coordinate4 :=
  potentialCovector (fun y => P y i) x

def directionalVariation (P : Coordinate4 → ι → ℝ) (x v : Coordinate4) : ι → ℝ :=
  fun i => covectorRead (probabilityDifferential P x i) v

def fisherTensorField (P : Coordinate4 → ι → ℝ) : TensorField4 :=
  fun x => fisherTensorAt (P x) (probabilityDifferential P x)

theorem fisher_tensor_entries (p : ι → ℝ) (dp : ι → Coordinate4) (a b : Fin 4) :
    fisherTensorAt p dp a b = ∑ i, dp i a * dp i b / p i := by
  simp only [fisherTensorAt, Matrix.sum_apply, Matrix.smul_apply, Matrix.vecMulVec,
    Matrix.of_apply, smul_eq_mul]
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem fisher_tensor_symmetric (p : ι → ℝ) (dp : ι → Coordinate4) :
    (fisherTensorAt p dp)ᵀ = fisherTensorAt p dp := by
  simp only [fisherTensorAt, Matrix.transpose_sum, Matrix.transpose_smul, outer_tensor_symmetric]

theorem fisher_tensor_directional (p : ι → ℝ) (dp : ι → Coordinate4) (v : Coordinate4) :
    tensorQuad (fisherTensorAt p dp) v =
      diagonalFisher p (fun i => covectorRead (dp i) v) := by
  simp only [fisherTensorAt, tensorQuad, Matrix.sum_mulVec, dotProduct_sum,
    Matrix.smul_mulVec, dotProduct_smul, smul_eq_mul]
  change (∑ i, (p i)⁻¹ * tensorQuad (Matrix.vecMulVec (dp i) (dp i)) v) = _
  simp only [outer_tensor_quad, diagonalFisher]
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem fisher_tensor_nonnegative (p : ι → ℝ) (dp : ι → Coordinate4)
    (hp : ∀ i, 0 < p i) (v : Coordinate4) :
    0 ≤ tensorQuad (fisherTensorAt p dp) v := by
  rw [fisher_tensor_directional]
  exact diagonal_fisher_nonneg _ _ hp

theorem fisher_tensor_null_iff (p : ι → ℝ) (dp : ι → Coordinate4)
    (hp : ∀ i, 0 < p i) (v : Coordinate4) :
    tensorQuad (fisherTensorAt p dp) v = 0 ↔
      (fun i => covectorRead (dp i) v) = 0 := by
  rw [fisher_tensor_directional]
  exact diagonal_fisher_zero_iff _ _ hp

theorem fisher_tensor_positive_iff (p : ι → ℝ) (dp : ι → Coordinate4)
    (hp : ∀ i, 0 < p i) (v : Coordinate4) :
    0 < tensorQuad (fisherTensorAt p dp) v ↔
      (fun i => covectorRead (dp i) v) ≠ 0 := by
  rw [fisher_tensor_directional]
  exact diagonal_fisher_pos_iff _ _ hp

theorem fisher_field_entries (P : Coordinate4 → ι → ℝ) (x : Coordinate4) (a b : Fin 4) :
    fisherTensorField P x a b =
      ∑ i, coordinatePartial (fun y => P y i) x a *
        coordinatePartial (fun y => P y i) x b / P x i :=
  fisher_tensor_entries _ _ a b

theorem fisher_field_symmetric (P : Coordinate4 → ι → ℝ) (x : Coordinate4) :
    (fisherTensorField P x)ᵀ = fisherTensorField P x :=
  fisher_tensor_symmetric _ _

theorem fisher_field_directional (P : Coordinate4 → ι → ℝ) (x v : Coordinate4) :
    tensorQuad (fisherTensorField P x) v =
      diagonalFisher (P x) (directionalVariation P x v) :=
  fisher_tensor_directional _ _ v

theorem fisher_field_nonnegative (P : Coordinate4 → ι → ℝ) (x : Coordinate4)
    (hp : ∀ i, 0 < P x i) (v : Coordinate4) :
    0 ≤ tensorQuad (fisherTensorField P x) v :=
  fisher_tensor_nonnegative _ _ hp v

omit [Fintype ι] in
theorem directional_variation_fderiv (P : Coordinate4 → ι → ℝ)
    (x v : Coordinate4) (i : ι) :
    directionalVariation P x v i = fderiv ℝ (fun y => P y i) x v := by
  rw [← scalarAlong_eq_fderiv (fun _ => v) (fun y => P y i) x]
  simp only [directionalVariation, probabilityDifferential, potentialCovector,
    covectorRead, dotProduct, scalarAlong]
  apply Finset.sum_congr rfl
  intro a _
  ring

theorem fisher_field_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (hp : ∀ x ∈ U, ∀ i, 0 < P x i) :
    SmoothMatrixOn U (fisherTensorField P) := by
  intro a b
  simp only [fisher_field_entries]
  apply ContDiffOn.sum
  intro i _
  exact ((coordinatePartial_smooth U hU _ (hP i) a).mul
    (coordinatePartial_smooth U hU _ (hP i) b)).div (hP i)
      (fun x hx => ne_of_gt (hp x hx i))

theorem probability_line_derivative (x v : Coordinate4) (t : ℝ) :
    HasDerivAt (fun s : ℝ => x + s • v) v t := by
  simpa using ((hasDerivAt_id t).smul_const v).const_add x

theorem probability_line_eventually (U : Set Coordinate4) (hU : IsOpen U)
    (x v : Coordinate4) (hx : x ∈ U) :
    ∀ᶠ t in 𝓝 (0 : ℝ), x + t • v ∈ U := by
  have hc := (probability_line_derivative x v 0).continuousAt
  exact hc.eventually (hU.mem_nhds (by simpa using hx))

omit [Fintype ι] in
theorem probability_weights_derivative (U : Set Coordinate4) (hU : IsOpen U)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (x v : Coordinate4) (t : ℝ) (ht : x + t • v ∈ U) (i : ι) :
    HasDerivAt (fun s => P (x + s • v) i) (directionalVariation P (x + t • v) v i) t := by
  rw [directional_variation_fderiv]
  exact ((hP i).differentiableOn (by simp)).differentiableAt
    (hU.mem_nhds ht) |>.hasFDerivAt.comp_hasDerivAt t (probability_line_derivative x v t)

omit [Fintype ι] in
theorem directional_variation_continuous (U : Set Coordinate4) (hU : IsOpen U)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (x v : Coordinate4) (hx : x ∈ U) (i : ι) :
    ContinuousAt (fun t : ℝ => directionalVariation P (x + t • v) v i) 0 := by
  have hd : ContDiffOn ℝ ∞ (fun y => directionalVariation P y v i) U := by
    simp only [directionalVariation, probabilityDifferential, potentialCovector,
      covectorRead, dotProduct]
    apply ContDiffOn.sum
    intro a _
    exact (coordinatePartial_smooth U hU _ (hP i) a).mul contDiffOn_const
  have hc : ContinuousAt (fun y => directionalVariation P y v i) (x + (0 : ℝ) • v) := by
    simpa using hd.continuousOn.continuousAt (hU.mem_nhds hx)
  exact ContinuousAt.comp (f := fun t : ℝ => x + t • v)
    (g := fun y => directionalVariation P y v i) hc
    (probability_line_derivative x v 0).continuousAt

/-- Affine spacetime sampling of P; no modular-flow identification. -/
def probabilityFieldCurve (U : Set Coordinate4) (hU : IsOpen U)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (htrace : ∀ y, ∑ i, P y i = 1) (x v : Coordinate4) (hx : x ∈ U) :
    DiagonalStateCurve (P x) where
  weights := fun t => P (x + t • v)
  tangent := fun t => directionalVariation P (x + t • v) v
  at_zero := by intro i; simp
  trace_one := fun t => htrace _
  derivative_zero := by
    intro i
    simpa using probability_weights_derivative U hU P hP x v 0 (by simpa using hx) i
  derivative_past := by
    filter_upwards [(probability_line_eventually U hU x v hx).filter_mono nhdsWithin_le_nhds]
      with t ht
    exact probability_weights_derivative U hU P hP x v t ht
  tangent_continuous := directional_variation_continuous U hU P hP x v hx

theorem probability_field_curve_tangent (U : Set Coordinate4) (hU : IsOpen U)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (htrace : ∀ y, ∑ i, P y i = 1) (x v : Coordinate4) (hx : x ∈ U) :
    (probabilityFieldCurve U hU P hP htrace x v hx).tangent 0 =
      directionalVariation P x v := by
  simp [probabilityFieldCurve]

theorem probability_field_curve_fisher (U : Set Coordinate4) (hU : IsOpen U)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (htrace : ∀ y, ∑ i, P y i = 1) (x v : Coordinate4) (hx : x ∈ U) :
    diagonalFisher (P x) ((probabilityFieldCurve U hU P hP htrace x v hx).tangent 0) =
      tensorQuad (fisherTensorField P x) v := by
  rw [probability_field_curve_tangent, fisher_field_directional]



/-- The derivative data of a Bernoulli field at a point. -/
theorem bernoulli_tensor (p : ℝ) (w : Coordinate4) (hp : p ≠ 0) (hq : 1 - p ≠ 0) :
    fisherTensorAt ![1-p, p] ![-w, w] =
      (p*(1-p))⁻¹ • Matrix.vecMulVec w w := by
  ext a b
  simp only [fisher_tensor_entries, Fin.sum_univ_two, Matrix.cons_val_zero,
    Matrix.cons_val_one, Pi.neg_apply, Matrix.smul_apply, Matrix.vecMulVec,
    Matrix.of_apply, smul_eq_mul]
  field_simp
  ring

/-- The pullback coefficient for p=sin²(theta), away from the zero-probability endpoints. -/
theorem angular_bernoulli_tensor (theta : ℝ) (w : Coordinate4)
    (hs : Real.sin theta ≠ 0) (hc : Real.cos theta ≠ 0) :
    fisherTensorAt ![(Real.cos theta)^2, (Real.sin theta)^2]
      ![-((2*Real.sin theta*Real.cos theta) • w),
        (2*Real.sin theta*Real.cos theta) • w] =
      (4 : ℝ) • Matrix.vecMulVec w w := by
  ext a b
  simp only [fisher_tensor_entries, Fin.sum_univ_two, Matrix.cons_val_zero,
    Matrix.cons_val_one, Pi.neg_apply, Pi.smul_apply, Matrix.smul_apply,
    Matrix.vecMulVec, Matrix.of_apply, smul_eq_mul]
  have hfirst : (-(2*Real.sin theta*Real.cos theta*w a)) *
      (-(2*Real.sin theta*Real.cos theta*w b)) / (Real.cos theta)^2 =
      4*(Real.sin theta)^2*w a*w b := by
    field_simp
    ring
  have hsecond : (2*Real.sin theta*Real.cos theta*w a) *
      (2*Real.sin theta*Real.cos theta*w b) / (Real.sin theta)^2 =
      4*(Real.cos theta)^2*w a*w b := by
    field_simp
    ring
  rw [hfirst, hsecond]
  have hunit := congrArg (fun z : ℝ => 4*z*w a*w b) (Real.sin_sq_add_cos_sq theta)
  nlinarith only [hunit]

theorem angular_bernoulli_directional (theta : ℝ) (w v : Coordinate4)
    (hs : Real.sin theta ≠ 0) (hc : Real.cos theta ≠ 0) :
    tensorQuad (fisherTensorAt ![(Real.cos theta)^2, (Real.sin theta)^2]
      ![-((2*Real.sin theta*Real.cos theta) • w),
        (2*Real.sin theta*Real.cos theta) • w]) v =
      4*(covectorRead w v)^2 := by
  rw [angular_bernoulli_tensor theta w hs hc]
  simp only [tensorQuad, Matrix.smul_mulVec, dotProduct_smul, smul_eq_mul]
  change 4*tensorQuad (Matrix.vecMulVec w w) v = _
  rw [outer_tensor_quad]



/-- Microscopic matching retains a field-derived Fisher tensor, without zero tangent. -/
theorem probability_field_geometric_compatibility
    (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (T : TensorField4)
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (htrace : ∀ y, ∑ i, P y i = 1)
    (x v : Coordinate4) (hx : x ∈ U)
    (screen : ChatgptAudit.Flow019.EquilibriumScreenData U g Gamma x v)
    (ht : ∀ i j a, Gamma x i a j = Gamma x j a i)
    (hp : ∀ i, 0 < P x i) (rate eta : ℝ) (hrate : rate ≠ 0)
    (hheat : Tendsto (fun t => microscopicHeatError
      (probabilityFieldCurve U hU P hP htrace x v hx) rate
      (ChatgptAudit.Flow020.constructedHeat screen T rate hU hg hT) t / t^2)
      (𝓝[<] 0) (𝓝 0))
    (harea : Tendsto (fun t => microscopicAreaError
      (probabilityFieldCurve U hU P hP htrace x v hx) eta
      (inducedArea g screen.curve screen.screen.vectors) t / t^2)
      (𝓝[<] 0) (𝓝 0)) :
    eta * tensorQuad (coordinateRicci Gamma x) v =
      2*Real.pi*tensorQuad (T x) v + tensorQuad (fisherTensorField P x) v := by
  have hh := geometric_microscopic_compatibility
    (probabilityFieldCurve U hU P hP htrace x v hx) U hU g Gamma T hg hG hT
    x v screen ht hp rate eta hrate hheat harea
  simpa only [probability_field_curve_fisher] using hh


#print axioms fisherTensorAt
#print axioms probabilityDifferential
#print axioms directionalVariation
#print axioms fisherTensorField
#print axioms fisher_tensor_entries
#print axioms fisher_tensor_symmetric
#print axioms fisher_tensor_directional
#print axioms fisher_tensor_nonnegative
#print axioms fisher_tensor_null_iff
#print axioms fisher_tensor_positive_iff
#print axioms fisher_field_entries
#print axioms fisher_field_symmetric
#print axioms fisher_field_directional
#print axioms fisher_field_nonnegative
#print axioms directional_variation_fderiv
#print axioms fisher_field_smooth
#print axioms probability_line_derivative
#print axioms probability_line_eventually
#print axioms probability_weights_derivative
#print axioms directional_variation_continuous
#print axioms probabilityFieldCurve
#print axioms probability_field_curve_tangent
#print axioms probability_field_curve_fisher
#print axioms bernoulli_tensor
#print axioms angular_bernoulli_tensor
#print axioms angular_bernoulli_directional
#print axioms probability_field_geometric_compatibility
end
end ChatgptAudit.FisherField
