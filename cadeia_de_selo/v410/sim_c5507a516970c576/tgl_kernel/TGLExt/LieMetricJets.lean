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
import TGLExt.MetricRicciVariation
import TGLExt.BoostMetricPullback

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit.MetricLie
open Matrix Filter Topology Set ChatgptAudit.Boost044
  ChatgptAudit.MetricVariation ChatgptAudit.MetricRicci
noncomputable section
open scoped ContDiff

def vectorJacobian (V : VectorField4) : TensorField4 :=
  fun x a b => vectorPartial V x b a

#print axioms vectorJacobian

def matrixTransport (V : VectorField4) (g : TensorField4) : TensorField4 :=
  fun x => ∑ k : Fin 4, V x k • tensorFieldJet g x k

#print axioms matrixTransport

def lieMetricJetDerivative (g : Tensor4) (dg : Fin 4 → Tensor4)
    (ddg : Fin 4 → Fin 4 → Tensor4) (v : Coordinate4)
    (P : Tensor4) (H : Fin 4 → Tensor4) (i : Fin 4) : Tensor4 :=
  (∑ k : Fin 4, P k i • dg k) + (∑ k : Fin 4, v k • ddg i k) +
    (H i)ᵀ*g + Pᵀ*dg i + dg i*P + g*H i

#print axioms lieMetricJetDerivative

theorem vector_jacobian_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (hV : SmoothVectorOn U V) :
    SmoothMatrixOn U (vectorJacobian V) := by
  intro a b
  exact vectorPartial_smooth U hU V hV b a

#print axioms vector_jacobian_smooth

theorem vector_jacobian_hessian_symmetry (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (hV : SmoothVectorOn U V) (x : Coordinate4) (hx : x∈U)
    (i a b : Fin 4) :
    tensorFieldJet (vectorJacobian V) x i a b =
      tensorFieldJet (vectorJacobian V) x b a i := by
  exact congrFun (vectorPartial_commute U hU V hV x hx i b) a

#print axioms vector_jacobian_hessian_symmetry

theorem matrix_transport_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (g : TensorField4)
    (hV : SmoothVectorOn U V) (hg : SmoothMatrixOn U g) :
    SmoothMatrixOn U (matrixTransport V g) := by
  intro a b
  change ContDiffOn ℝ ∞ (fun x => ∑ k : Fin 4, V x k*tensorFieldJet g x k a b) U
  exact ContDiffOn.sum (fun k _ => (hV k).mul (tensorFieldJet_smooth U hU g hg k a b))

#print axioms matrix_transport_smooth

theorem coordinate_metric_lie_matrix_formula (g : TensorField4) (V : VectorField4)
    (x : Coordinate4) :
    coordinateMetricLie g V x = matrixTransport V g x +
      (vectorJacobian V x)ᵀ*g x + g x*vectorJacobian V x := by
  ext a b
  simp only [coordinateMetricLie,scalarAlong,matrixTransport,vectorJacobian,
    Matrix.add_apply,Matrix.mul_apply,Matrix.transpose_apply,
    ]
  congr 1
  congr 1
  apply Finset.sum_congr rfl
  intro k _
  ring

#print axioms coordinate_metric_lie_matrix_formula

theorem coordinate_metric_lie_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (g : TensorField4)
    (hV : SmoothVectorOn U V) (hg : SmoothMatrixOn U g) :
    SmoothMatrixOn U (coordinateMetricLie g V) := by
  have he : coordinateMetricLie g V = fun x => matrixTransport V g x +
      (vectorJacobian V x)ᵀ*g x + g x*vectorJacobian V x := by
    funext x
    exact coordinate_metric_lie_matrix_formula g V x
  rw [he]
  exact SmoothMatrixOn.add U _ _
    (SmoothMatrixOn.add U _ _ (matrix_transport_smooth U hU V g hV hg)
      (SmoothMatrixOn.mul U _ _
        (SmoothMatrixOn.transpose U _ (vector_jacobian_smooth U hU V hV)) hg))
    (SmoothMatrixOn.mul U _ _ hg (vector_jacobian_smooth U hU V hV))

#print axioms coordinate_metric_lie_smooth

theorem tensor_jet_sum (U : Set Coordinate4) (hU : IsOpen U)
    (A : Fin 4 → TensorField4) (hA : ∀ k, SmoothMatrixOn U (A k))
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    tensorFieldJet (fun y => ∑ k : Fin 4, A k y) x i =
      ∑ k : Fin 4, tensorFieldJet (A k) x i := by
  ext a b
  change coordinatePartial (fun y => ∑ k : Fin 4, A k y a b) x i = _
  rw [coordinatePartial_sum _ x
    (fun k => smooth_matrix_differentiableAt U hU (A k) (hA k) x hx a b) i]
  rfl

#print axioms tensor_jet_sum

theorem tensor_jet_scalar_product (U : Set Coordinate4) (hU : IsOpen U)
    (f : Coordinate4 → ℝ) (A : TensorField4)
    (hf : ContDiffOn ℝ ∞ f U) (hA : SmoothMatrixOn U A)
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    tensorFieldJet (fun y => f y • A y) x i =
      coordinatePartial f x i • A x + f x • tensorFieldJet A x i := by
  ext a b
  exact coordinatePartial_mul f (fun y => A y a b) x
    ((hf.differentiableOn (by simp)).differentiableAt (hU.mem_nhds hx))
    (smooth_matrix_differentiableAt U hU A hA x hx a b) i

#print axioms tensor_jet_scalar_product

theorem matrix_transport_jet (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (g : TensorField4)
    (hV : SmoothVectorOn U V) (hg : SmoothMatrixOn U g)
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    tensorFieldJet (matrixTransport V g) x i =
      (∑ k : Fin 4, vectorJacobian V x k i • tensorFieldJet g x k) +
      ∑ k : Fin 4, V x k • tensorFieldJet (fun y => tensorFieldJet g y k) x i := by
  unfold matrixTransport
  have hterm (k : Fin 4) :
      SmoothMatrixOn U (fun y => V y k • tensorFieldJet g y k) := by
    intro a b
    exact (hV k).mul (tensorFieldJet_smooth U hU g hg k a b)
  rw [tensor_jet_sum U hU (fun k y => V y k • tensorFieldJet g y k) hterm x hx i]
  simp only [tensor_jet_scalar_product U hU _ _ (hV _)
    (tensorFieldJet_smooth U hU g hg _) x hx i,Finset.sum_add_distrib,
    vectorJacobian,vectorPartial]

#print axioms matrix_transport_jet

theorem coordinate_metric_lie_jet (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (g : TensorField4)
    (hV : SmoothVectorOn U V) (hg : SmoothMatrixOn U g)
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    tensorFieldJet (coordinateMetricLie g V) x i =
      lieMetricJetDerivative (g x) (tensorFieldJet g x)
        (fun i k => tensorFieldJet (fun y => tensorFieldJet g y k) x i)
        (V x) (vectorJacobian V x) (tensorFieldJet (vectorJacobian V) x) i := by
  have he : coordinateMetricLie g V = fun y => matrixTransport V g y +
      (vectorJacobian V y)ᵀ*g y + g y*vectorJacobian V y := by
    funext y
    exact coordinate_metric_lie_matrix_formula g V y
  have hP := vector_jacobian_smooth U hU V hV
  have hd (A : TensorField4) (hA : SmoothMatrixOn U A) :=
    smooth_matrix_differentiableAt U hU A hA x hx
  rw [he]
  rw [tensorFieldJet_add _ _ x
    (hd _ (SmoothMatrixOn.add U _ _ (matrix_transport_smooth U hU V g hV hg)
      (SmoothMatrixOn.mul U _ _ (SmoothMatrixOn.transpose U _ hP) hg)))
    (hd _ (SmoothMatrixOn.mul U _ _ hg hP))]
  simp only [Pi.add_apply]
  rw [tensorFieldJet_add _ _ x (hd _ (matrix_transport_smooth U hU V g hV hg))
    (hd _ (SmoothMatrixOn.mul U _ _ (SmoothMatrixOn.transpose U _ hP) hg))]
  simp only [Pi.add_apply]
  rw [tensorFieldJet_mul _ _ x (hd _ (SmoothMatrixOn.transpose U _ hP)) (hd _ hg) i,
    tensorFieldJet_mul _ _ x (hd _ hg) (hd _ hP) i,
    tensorFieldJet_transpose,matrix_transport_jet U hU V g hV hg x hx i]
  unfold lieMetricJetDerivative
  abel

#print axioms coordinate_metric_lie_jet

theorem lower_lie_jet_identity (g : Tensor4) (dg : Fin 4 → Tensor4)
    (ddg : Fin 4 → Fin 4 → Tensor4) (v : Coordinate4)
    (P : Tensor4) (H : Fin 4 → Tensor4)
    (hg : ∀ a b, g a b=g b a)
    (hdg : ∀ i a b, dg i a b=dg i b a)
    (hddg : ∀ i k, ddg i k=ddg k i)
    (hH : ∀ i a b, H i a b=H b a i) (i : Fin 4) :
    lowerChristoffelJet (lieMetricJetDerivative g dg ddg v P H) i =
      (∑ k : Fin 4, v k • lowerChristoffelJet (ddg k) i) +
      (∑ k : Fin 4, P k i • lowerChristoffelJet dg k) +
      Pᵀ*lowerChristoffelJet dg i + lowerChristoffelJet dg i*P + g*H i := by
  ext a b
  have hdd (i k a b : Fin 4) : ddg i k a b=ddg k i a b :=
    congrFun (congrFun (hddg i k) a) b
  simp only [lowerChristoffelJet,lieMetricJetDerivative,Matrix.add_apply,Matrix.mul_apply,
    Matrix.transpose_apply,Matrix.smul_apply,smul_eq_mul,
    Fin.sum_univ_four]
  simp only [hg,hdg,hdd,hH]
  ring

#print axioms lower_lie_jet_identity

end
end ChatgptAudit.MetricLie
