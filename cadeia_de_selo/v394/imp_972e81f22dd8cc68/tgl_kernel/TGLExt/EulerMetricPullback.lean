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
import TGLExt.LieMetricJets
import Mathlib.Topology.Instances.Matrix

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit.EulerPullback
open Matrix Filter Topology Set ChatgptAudit.Boost044 ChatgptAudit.MetricLie
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def eulerMap (V : VectorField4) (t : ℝ) (x : Coordinate4) : Coordinate4 :=
  x + t • V x

def eulerJacobian (V : VectorField4) (t : ℝ) (x : Coordinate4) : Tensor4 :=
  1 + t • vectorJacobian V x

def eulerMetricPullback (g : TensorField4) (V : VectorField4) (t : ℝ)
    (x : Coordinate4) : Tensor4 :=
  (eulerJacobian V t x)ᵀ * g (eulerMap V t x) * eulerJacobian V t x

theorem euler_map_zero (V : VectorField4) (x : Coordinate4) : eulerMap V 0 x = x := by
  simp only [eulerMap,zero_smul,add_zero]

theorem euler_jacobian_zero (V : VectorField4) (x : Coordinate4) :
    eulerJacobian V 0 x = 1 := by
  simp only [eulerJacobian,zero_smul,add_zero]

theorem euler_pullback_zero (g : TensorField4) (V : VectorField4) (x : Coordinate4) :
    eulerMetricPullback g V 0 x = g x := by
  simp only [eulerMetricPullback,euler_map_zero,euler_jacobian_zero,
    Matrix.transpose_one,one_mul,mul_one]

theorem vector_fderiv_is_jacobian (V : VectorField4) (x : Coordinate4)
    (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) x) :
    fderiv ℝ V x = boostMatrixAction (vectorJacobian V x) := by
  have hv : DifferentiableAt ℝ V x := differentiableAt_pi.mpr hV
  ext v a
  have ha := (hasFDerivAt_pi'.mp hv.hasFDerivAt a).fderiv
  change (fderiv ℝ V x v) a = (boostMatrixAction (vectorJacobian V x) v) a
  rw [boost_matrix_action_apply]
  calc
    (fderiv ℝ V x v) a = fderiv ℝ (fun y => V y a) x v :=
      (congrArg (fun L : Coordinate4 →L[ℝ] ℝ => L v) ha).symm
    _ = scalarAlong (fun _ => v) (fun y => V y a) x :=
      (scalarAlong_eq_fderiv (fun _ => v) (fun y => V y a) x).symm
    _ = (vectorJacobian V x *ᵥ v) a := by
      simp only [scalarAlong,vectorJacobian,vectorPartial,Matrix.mulVec,dotProduct]
      apply Finset.sum_congr rfl
      intro i _
      ring

theorem euler_map_hasFDerivAt (V : VectorField4) (x : Coordinate4) (t : ℝ)
    (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) x) :
    HasFDerivAt (eulerMap V t) (boostMatrixAction (eulerJacobian V t x)) x := by
  have hv : DifferentiableAt ℝ V x := differentiableAt_pi.mpr hV
  have hd := (hasFDerivAt_id x).add (hv.hasFDerivAt.const_smul t)
  have he : ContinuousLinearMap.id ℝ Coordinate4 + t • fderiv ℝ V x =
      boostMatrixAction (eulerJacobian V t x) := by
    rw [vector_fderiv_is_jacobian V x hV]
    ext v
    simp only [_root_.add_apply,_root_.smul_apply,
      ContinuousLinearMap.id_apply,boost_matrix_action_apply,eulerJacobian,
      Matrix.add_mulVec,Matrix.one_mulVec,Matrix.smul_mulVec]
  rw [he] at hd
  exact hd

theorem euler_jacobian_is_spatial_derivative (V : VectorField4) (x : Coordinate4)
    (t : ℝ) (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) x) :
    vectorJacobian (eulerMap V t) x = eulerJacobian V t x := by
  ext a b
  have hd := hasFDerivAt_pi'.mp (euler_map_hasFDerivAt V x t hV) a
  change fderiv ℝ (fun y => eulerMap V t y a) x (Pi.single b 1) =
    eulerJacobian V t x a b
  rw [hd.fderiv]
  change (boostMatrixAction (eulerJacobian V t x) (Pi.single b 1)) a = _
  rw [boost_matrix_action_apply,Matrix.mulVec_single_one]
  rfl

theorem euler_map_hasDerivAt (V : VectorField4) (x : Coordinate4) (t : ℝ) :
    HasDerivAt (fun s => eulerMap V s x) (V x) t := by
  apply hasDerivAt_pi.mpr
  intro a
  change HasDerivAt (fun s : ℝ => x a + s * V x a) (V x a) t
  exact (hasDerivAt_mul_const (V x a)).const_add (x a)

theorem euler_jacobian_hasDerivAt (V : VectorField4) (x : Coordinate4) (t : ℝ) :
    HasDerivAt (fun s => eulerJacobian V s x) (vectorJacobian V x) t := by
  apply hasDerivAt_pi.mpr
  intro a
  apply hasDerivAt_pi.mpr
  intro b
  change HasDerivAt (fun s : ℝ => (1 : Tensor4) a b + s * vectorJacobian V x a b)
    (vectorJacobian V x a b) t
  exact (hasDerivAt_mul_const (vectorJacobian V x a b)).const_add ((1 : Tensor4) a b)

theorem euler_metric_transport_derivative (g : TensorField4) (V : VectorField4)
    (x : Coordinate4) (hg : ∀ a b, DifferentiableAt ℝ (fun y => g y a b) x) :
    HasMatrixDerivAt (fun t => g (eulerMap V t x)) (matrixTransport V g x) 0 := by
  intro a b
  have hga : DifferentiableAt ℝ (fun y => g y a b) (eulerMap V 0 x) := by
    rw [euler_map_zero]
    exact hg a b
  have hd := hga.hasFDerivAt.comp_hasDerivAt 0 (euler_map_hasDerivAt V x 0)
  have he : fderiv ℝ (fun y => g y a b) (eulerMap V 0 x) (V x) =
      matrixTransport V g x a b := by
    rw [euler_map_zero,← scalarAlong_eq_fderiv V (fun y => g y a b) x]
    rfl
  rw [he] at hd
  exact hd

theorem euler_metric_pullback_matrix_derivative (g : TensorField4) (V : VectorField4)
    (x : Coordinate4) (hg : ∀ a b, DifferentiableAt ℝ (fun y => g y a b) x) :
    HasMatrixDerivAt (fun t => eulerMetricPullback g V t x)
      (coordinateMetricLie g V x) 0 := by
  have hJ : HasMatrixDerivAt (fun t => eulerJacobian V t x) (vectorJacobian V x) 0 := by
    intro a b
    exact hasDerivAt_pi.mp (hasDerivAt_pi.mp (euler_jacobian_hasDerivAt V x 0) a) b
  have hG := euler_metric_transport_derivative g V x hg
  have hJG := matrix_curve_deriv_mul (fun t => (eulerJacobian V t x)ᵀ)
    (fun t => g (eulerMap V t x)) (vectorJacobian V x)ᵀ (matrixTransport V g x) 0
    (matrix_curve_deriv_transpose _ _ 0 hJ) hG
  have hd := matrix_curve_deriv_mul
    (fun t => (eulerJacobian V t x)ᵀ * g (eulerMap V t x))
    (fun t => eulerJacobian V t x)
    ((vectorJacobian V x)ᵀ * g (eulerMap V 0 x) +
      (eulerJacobian V 0 x)ᵀ * matrixTransport V g x)
    (vectorJacobian V x) 0 hJG hJ
  have he :
      (((vectorJacobian V x)ᵀ * g (eulerMap V 0 x) +
        (eulerJacobian V 0 x)ᵀ * matrixTransport V g x) * eulerJacobian V 0 x +
        ((eulerJacobian V 0 x)ᵀ * g (eulerMap V 0 x)) * vectorJacobian V x) =
      coordinateMetricLie g V x := by
    rw [euler_map_zero,euler_jacobian_zero,Matrix.transpose_one,one_mul,mul_one,one_mul,
      coordinate_metric_lie_matrix_formula]
    abel
  rw [he] at hd
  exact hd

theorem euler_metric_pullback_hasDerivAt (g : TensorField4) (V : VectorField4)
    (x : Coordinate4) (hg : ∀ a b, DifferentiableAt ℝ (fun y => g y a b) x) :
    HasDerivAt (fun t => eulerMetricPullback g V t x) (coordinateMetricLie g V x) 0 := by
  apply hasDerivAt_pi.mpr
  intro a
  apply hasDerivAt_pi.mpr
  exact euler_metric_pullback_matrix_derivative g V x hg a

theorem euler_jacobian_det_positive_near (V : VectorField4) (x : Coordinate4) :
    ∀ᶠ t in 𝓝 (0 : ℝ), 0 < (eulerJacobian V t x).det := by
  have hc : Continuous (fun t : ℝ => eulerJacobian V t x) :=
    continuous_const.add (continuous_id.smul continuous_const)
  exact (isOpen_lt continuous_const hc.matrix_det).mem_nhds
    (by
      change 0 < (eulerJacobian V 0 x).det
      rw [euler_jacobian_zero,Matrix.det_one]
      norm_num)

theorem euler_map_mem_near (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (x : Coordinate4) (hx : x ∈ U) :
    ∀ᶠ t in 𝓝 (0 : ℝ), eulerMap V t x ∈ U := by
  have hc : Continuous (fun t : ℝ => eulerMap V t x) :=
    continuous_const.add (continuous_id.smul continuous_const)
  exact hc.continuousAt.eventually (hU.mem_nhds (by
    change eulerMap V 0 x ∈ U
    rwa [euler_map_zero]))

theorem smooth_euler_pullback_realizes_lie (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x ∈ U) :
    (∀ t, HasFDerivAt (eulerMap V t) (boostMatrixAction (eulerJacobian V t x)) x) ∧
      HasDerivAt (fun t => eulerMetricPullback g V t x) (coordinateMetricLie g V x) 0 := by
  exact ⟨fun t => euler_map_hasFDerivAt V x t (smooth_vector_differentiableAt U hU V hV x hx),
    euler_metric_pullback_hasDerivAt g V x (smooth_matrix_differentiableAt U hU g hg x hx)⟩

theorem smooth_euler_local_certificate (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (hV : SmoothVectorOn U V) (x : Coordinate4) (hx : x ∈ U) :
    ∀ᶠ t in 𝓝 (0 : ℝ), eulerMap V t x ∈ U ∧
      0 < (eulerJacobian V t x).det ∧
      HasFDerivAt (eulerMap V t) (boostMatrixAction (eulerJacobian V t x)) x := by
  filter_upwards [euler_map_mem_near U hU V x hx,euler_jacobian_det_positive_near V x]
    with t ht hd
  exact ⟨ht,hd,euler_map_hasFDerivAt V x t (smooth_vector_differentiableAt U hU V hV x hx)⟩

#print axioms eulerMap
#print axioms eulerJacobian
#print axioms eulerMetricPullback
#print axioms euler_map_zero
#print axioms euler_jacobian_zero
#print axioms euler_pullback_zero
#print axioms vector_fderiv_is_jacobian
#print axioms euler_map_hasFDerivAt
#print axioms euler_jacobian_is_spatial_derivative
#print axioms euler_map_hasDerivAt
#print axioms euler_jacobian_hasDerivAt
#print axioms euler_metric_transport_derivative
#print axioms euler_metric_pullback_matrix_derivative
#print axioms euler_metric_pullback_hasDerivAt
#print axioms euler_jacobian_det_positive_near
#print axioms euler_map_mem_near
#print axioms smooth_euler_pullback_realizes_lie
#print axioms smooth_euler_local_certificate
end
end ChatgptAudit.EulerPullback
