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
import TGLExt.EulerMetricPullback
import TGLExt.GeneralMetricEinstein

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit.FiniteCoordinates
open Matrix Filter Topology Set TGLExt ChatgptAudit.Boost044
  ChatgptAudit.MetricLie ChatgptAudit.EulerPullback ChatgptAudit.GeneralMetric
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section
variable {U W : Set Coordinate4}

structure SmoothCoordinateChange (U W : Set Coordinate4) where
  forward : VectorField4
  inverse : VectorField4
  source_open : IsOpen U
  target_open : IsOpen W
  forward_maps : MapsTo forward U W
  inverse_maps : MapsTo inverse W U
  left_inverse : ∀ x ∈ U, inverse (forward x) = x
  right_inverse : ∀ y ∈ W, forward (inverse y) = y
  forward_smooth : SmoothVectorOn U forward
  inverse_smooth : SmoothVectorOn W inverse

def changeJacobian (C : SmoothCoordinateChange U W) : TensorField4 :=
  vectorJacobian C.forward

def inverseChangeJacobian (C : SmoothCoordinateChange U W) : TensorField4 :=
  fun x => vectorJacobian C.inverse (C.forward x)

def pullbackMetric (C : SmoothCoordinateChange U W) (g : TensorField4) : TensorField4 :=
  fun x => (changeJacobian C x)ᵀ * g (C.forward x) * changeJacobian C x

def pullbackInverse (C : SmoothCoordinateChange U W) (g : TensorField4) : TensorField4 :=
  fun x => inverseChangeJacobian C x * metricInverse g (C.forward x) *
    (inverseChangeJacobian C x)ᵀ

theorem matrix_action_mul (A B : Tensor4) :
    boostMatrixAction (A*B) = (boostMatrixAction A).comp (boostMatrixAction B) := by
  ext v
  simp only [ContinuousLinearMap.comp_apply,boost_matrix_action_apply,Matrix.mulVec_mulVec]

theorem coordinate_jacobian_comp (f h : VectorField4) (x : Coordinate4)
    (hf : ∀ a, DifferentiableAt ℝ (fun y => f y a) (h x))
    (hh : ∀ a, DifferentiableAt ℝ (fun y => h y a) x) :
    vectorJacobian (fun y => f (h y)) x = vectorJacobian f (h x) * vectorJacobian h x := by
  have hff : HasFDerivAt f (boostMatrixAction (vectorJacobian f (h x))) (h x) := by
    rw [← vector_fderiv_is_jacobian f (h x) hf]
    exact (differentiableAt_pi.mpr hf).hasFDerivAt
  have hhh : HasFDerivAt h (boostMatrixAction (vectorJacobian h x)) x := by
    rw [← vector_fderiv_is_jacobian h x hh]
    exact (differentiableAt_pi.mpr hh).hasFDerivAt
  have hd := hff.comp x hhh
  rw [← matrix_action_mul] at hd
  simp only [Function.comp_def] at hd
  ext a b
  have hda := hasFDerivAt_pi'.mp hd a
  change fderiv ℝ (fun y => f (h y) a) x (Pi.single b 1) = _
  rw [hda.fderiv]
  change (boostMatrixAction (vectorJacobian f (h x) * vectorJacobian h x)
    (Pi.single b 1)) a = _
  rw [boost_matrix_action_apply,Matrix.mulVec_single_one]
  rfl

theorem coordinate_jacobian_congr_on (S : Set Coordinate4) (hS : IsOpen S)
    (f h : VectorField4) (he : EqOn f h S) (x : Coordinate4) (hx : x ∈ S) :
    vectorJacobian f x = vectorJacobian h x := by
  ext a b
  have he' : (fun y => f y a) =ᶠ[𝓝 x] (fun y => h y a) := by
    filter_upwards [hS.mem_nhds hx] with y hy
    rw [he hy]
  exact congrArg (fun L : Coordinate4 →L[ℝ] ℝ => L (Pi.single b 1)) he'.fderiv_eq

theorem coordinate_jacobian_identity (x : Coordinate4) :
    vectorJacobian (fun y : Coordinate4 => y) x = 1 := by
  ext a b
  change fderiv ℝ (fun y : Coordinate4 => y a) x (Pi.single b 1) = (1 : Tensor4) a b
  rw [(hasFDerivAt_apply a x).fderiv]
  simp only [ContinuousLinearMap.proj_apply,Pi.single_apply,Matrix.one_apply]

theorem change_hasFDerivAt (C : SmoothCoordinateChange U W) (x : Coordinate4)
    (hx : x ∈ U) :
    HasFDerivAt C.forward (boostMatrixAction (changeJacobian C x)) x := by
  have hd := smooth_vector_differentiableAt U C.source_open C.forward C.forward_smooth x hx
  rw [changeJacobian,← vector_fderiv_is_jacobian C.forward x hd]
  exact (differentiableAt_pi.mpr hd).hasFDerivAt

theorem inverse_change_hasFDerivAt (C : SmoothCoordinateChange U W) (x : Coordinate4)
    (hx : x ∈ U) :
    HasFDerivAt C.inverse (boostMatrixAction (inverseChangeJacobian C x)) (C.forward x) := by
  have hd := smooth_vector_differentiableAt W C.target_open C.inverse C.inverse_smooth
    (C.forward x) (C.forward_maps hx)
  rw [inverseChangeJacobian,← vector_fderiv_is_jacobian C.inverse (C.forward x) hd]
  exact (differentiableAt_pi.mpr hd).hasFDerivAt

theorem inverse_jacobian_mul_jacobian (C : SmoothCoordinateChange U W)
    (x : Coordinate4) (hx : x ∈ U) :
    inverseChangeJacobian C x * changeJacobian C x = 1 := by
  have he := coordinate_jacobian_congr_on U C.source_open
    (fun y => C.inverse (C.forward y)) (fun y => y) C.left_inverse x hx
  rw [coordinate_jacobian_comp C.inverse C.forward x
    (smooth_vector_differentiableAt W C.target_open C.inverse C.inverse_smooth
      (C.forward x) (C.forward_maps hx))
    (smooth_vector_differentiableAt U C.source_open C.forward C.forward_smooth x hx),
    coordinate_jacobian_identity] at he
  exact he

theorem jacobian_mul_inverse_jacobian (C : SmoothCoordinateChange U W)
    (x : Coordinate4) (hx : x ∈ U) :
    changeJacobian C x * inverseChangeJacobian C x = 1 := by
  have hy := C.forward_maps hx
  have he := coordinate_jacobian_congr_on W C.target_open
    (fun y => C.forward (C.inverse y)) (fun y => y) C.right_inverse (C.forward x) hy
  rw [coordinate_jacobian_comp C.forward C.inverse (C.forward x)
    (smooth_vector_differentiableAt U C.source_open C.forward C.forward_smooth
      (C.inverse (C.forward x)) (C.inverse_maps hy))
    (smooth_vector_differentiableAt W C.target_open C.inverse C.inverse_smooth
      (C.forward x) hy),coordinate_jacobian_identity,C.left_inverse x hx] at he
  exact he

theorem change_jacobian_det_ne_zero (C : SmoothCoordinateChange U W)
    (x : Coordinate4) (hx : x ∈ U) : (changeJacobian C x).det ≠ 0 := by
  have he := congrArg Matrix.det (inverse_jacobian_mul_jacobian C x hx)
  rw [Matrix.det_mul,Matrix.det_one] at he
  intro hz
  rw [hz,mul_zero] at he
  exact zero_ne_one he

theorem inverse_change_jacobian_eq_matrix_inverse (C : SmoothCoordinateChange U W)
    (x : Coordinate4) (hx : x ∈ U) :
    inverseChangeJacobian C x = (changeJacobian C x)⁻¹ :=
  (Matrix.inv_eq_left_inv (inverse_jacobian_mul_jacobian C x hx)).symm

theorem change_jacobian_smooth (C : SmoothCoordinateChange U W) :
    SmoothMatrixOn U (changeJacobian C) :=
  vector_jacobian_smooth U C.source_open C.forward C.forward_smooth

theorem matrix_composition_smooth (C : SmoothCoordinateChange U W) (g : TensorField4)
    (hg : SmoothMatrixOn W g) : SmoothMatrixOn U (fun x => g (C.forward x)) := by
  have hf : ContDiffOn ℝ ∞ C.forward U := contDiffOn_pi.mpr C.forward_smooth
  intro a b
  exact (hg a b).comp hf C.forward_maps

theorem inverse_change_jacobian_smooth (C : SmoothCoordinateChange U W) :
    SmoothMatrixOn U (inverseChangeJacobian C) :=
  matrix_composition_smooth C (vectorJacobian C.inverse)
    (vector_jacobian_smooth W C.target_open C.inverse C.inverse_smooth)

theorem pullback_metric_smooth (C : SmoothCoordinateChange U W) (g : TensorField4)
    (hg : SmoothMatrixOn W g) : SmoothMatrixOn U (pullbackMetric C g) :=
  SmoothMatrixOn.mul U _ _
    (SmoothMatrixOn.mul U _ _ (SmoothMatrixOn.transpose U _ (change_jacobian_smooth C))
      (matrix_composition_smooth C g hg)) (change_jacobian_smooth C)

theorem pullback_metric_symmetric (C : SmoothCoordinateChange U W) (g : TensorField4)
    (x : Coordinate4) (hg : (g (C.forward x))ᵀ = g (C.forward x)) :
    (pullbackMetric C g x)ᵀ = pullbackMetric C g x :=
  congruence_symmetric _ _ hg

theorem pullback_metric_lorentz (C : SmoothCoordinateChange U W) (g : TensorField4)
    (x : Coordinate4) (hx : x ∈ U) (hg : LorentzByCongruence (g (C.forward x))) :
    LorentzByCongruence (pullbackMetric C g x) := by
  obtain ⟨F,hF,he⟩ := hg
  refine ⟨F * changeJacobian C x, ?_, ?_⟩
  · rw [Matrix.det_mul]
    exact hF.mul (isUnit_iff_ne_zero.mpr (change_jacobian_det_ne_zero C x hx))
  · unfold pullbackMetric
    rw [he,Matrix.transpose_mul]
    simp only [Matrix.mul_assoc]

theorem pullback_inverse_left (C : SmoothCoordinateChange U W) (g : TensorField4)
    (x : Coordinate4) (hx : x ∈ U) (hg : LorentzByCongruence (g (C.forward x))) :
    pullbackInverse C g x * pullbackMetric C g x = 1 := by
  have hDJ := inverse_jacobian_mul_jacobian C x hx
  have hJD := jacobian_mul_inverse_jacobian C x hx
  have ht : (inverseChangeJacobian C x)ᵀ * (changeJacobian C x)ᵀ = 1 := by
    rw [← Matrix.transpose_mul,hJD,Matrix.transpose_one]
  have hi := constructed_metric_inverse_left g (C.forward x) hg
  unfold pullbackInverse pullbackMetric
  calc
    _ = inverseChangeJacobian C x * metricInverse g (C.forward x) *
        ((inverseChangeJacobian C x)ᵀ * (changeJacobian C x)ᵀ) *
        g (C.forward x) * changeJacobian C x := by noncomm_ring
    _ = inverseChangeJacobian C x * (metricInverse g (C.forward x) * g (C.forward x)) *
        changeJacobian C x := by rw [ht]; simp only [mul_one,Matrix.mul_assoc]
    _ = 1 := by rw [hi,mul_one,hDJ]

theorem constructed_pullback_inverse (C : SmoothCoordinateChange U W) (g : TensorField4)
    (x : Coordinate4) (hx : x ∈ U) (hg : LorentzByCongruence (g (C.forward x))) :
    metricInverse (pullbackMetric C g) x = pullbackInverse C g x :=
  Matrix.inv_eq_left_inv (pullback_inverse_left C g x hx hg)

theorem pullback_inverse_smooth (C : SmoothCoordinateChange U W) (g : TensorField4)
    (hg : SmoothMatrixOn W g) (hl : ∀ y ∈ W, LorentzByCongruence (g y)) :
    SmoothMatrixOn U (pullbackInverse C g) :=
  SmoothMatrixOn.mul U _ _
    (SmoothMatrixOn.mul U _ _ (inverse_change_jacobian_smooth C)
      (matrix_composition_smooth C (metricInverse g) (constructed_metric_inverse_smooth W g hg hl)))
    (SmoothMatrixOn.transpose U _ (inverse_change_jacobian_smooth C))

theorem coordinate_partial_comp (f : Coordinate4 → ℝ) (h : VectorField4)
    (x : Coordinate4) (hf : DifferentiableAt ℝ f (h x))
    (hh : ∀ a, DifferentiableAt ℝ (fun y => h y a) x) (i : Fin 4) :
    coordinatePartial (fun y => f (h y)) x i =
      ∑ a : Fin 4, vectorJacobian h x a i * coordinatePartial f (h x) a := by
  have hd := hf.hasFDerivAt.comp x (differentiableAt_pi.mpr hh).hasFDerivAt
  simp only [Function.comp_def] at hd
  unfold coordinatePartial
  rw [hd.fderiv]
  change fderiv ℝ f (h x) (fderiv ℝ h x (Pi.single i 1)) = _
  rw [vector_fderiv_is_jacobian h x hh,boost_matrix_action_apply,Matrix.mulVec_single_one]
  exact (scalarAlong_eq_fderiv (fun _ a => vectorJacobian h x a i) f (h x)).symm

theorem tensor_jet_composition (C : SmoothCoordinateChange U W) (g : TensorField4)
    (hg : SmoothMatrixOn W g) (x : Coordinate4) (hx : x ∈ U) (i : Fin 4) :
    tensorFieldJet (fun y => g (C.forward y)) x i =
      ∑ a : Fin 4, changeJacobian C x a i • tensorFieldJet g (C.forward x) a := by
  ext j k
  exact coordinate_partial_comp (fun y => g y j k) C.forward x
    (smooth_matrix_differentiableAt W C.target_open g hg (C.forward x) (C.forward_maps hx) j k)
    (smooth_vector_differentiableAt U C.source_open C.forward C.forward_smooth x hx) i

theorem change_jacobian_hessian_symmetry (C : SmoothCoordinateChange U W)
    (x : Coordinate4) (hx : x ∈ U) (i a b : Fin 4) :
    tensorFieldJet (changeJacobian C) x i a b = tensorFieldJet (changeJacobian C) x b a i :=
  vector_jacobian_hessian_symmetry U C.source_open C.forward C.forward_smooth x hx i a b

#print axioms SmoothCoordinateChange
#print axioms changeJacobian
#print axioms inverseChangeJacobian
#print axioms pullbackMetric
#print axioms pullbackInverse
#print axioms matrix_action_mul
#print axioms coordinate_jacobian_comp
#print axioms coordinate_jacobian_congr_on
#print axioms coordinate_jacobian_identity
#print axioms change_hasFDerivAt
#print axioms inverse_change_hasFDerivAt
#print axioms inverse_jacobian_mul_jacobian
#print axioms jacobian_mul_inverse_jacobian
#print axioms change_jacobian_det_ne_zero
#print axioms inverse_change_jacobian_eq_matrix_inverse
#print axioms change_jacobian_smooth
#print axioms matrix_composition_smooth
#print axioms inverse_change_jacobian_smooth
#print axioms pullback_metric_smooth
#print axioms pullback_metric_symmetric
#print axioms pullback_metric_lorentz
#print axioms pullback_inverse_left
#print axioms constructed_pullback_inverse
#print axioms pullback_inverse_smooth
#print axioms coordinate_partial_comp
#print axioms tensor_jet_composition
#print axioms change_jacobian_hessian_symmetry
end
end ChatgptAudit.FiniteCoordinates
