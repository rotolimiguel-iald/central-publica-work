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
import TGLExt.LeviCivitaLieVariation

set_option autoImplicit false
set_option maxHeartbeats 2200000
namespace ChatgptAudit.RicciLie
open Matrix Filter Topology Set ChatgptAudit.Boost044
  ChatgptAudit.MetricVariation ChatgptAudit.MetricRicci ChatgptAudit.MetricLie
  ChatgptAudit.MetricLieConnection ChatgptAudit.CurvedConnection
noncomputable section
open scoped ContDiff

def baseConnectionLie (Gamma : ConnectionField4) (V : VectorField4) :
    ConnectionField4 := fun x i =>
  matrixTransport V (fun y => Gamma y i) x +
    ∑ k : Fin 4, vectorJacobian V x k i • Gamma x k

#print axioms baseConnectionLie

theorem base_connection_lie_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V) :
    SmoothConnectionOn U (baseConnectionLie Gamma V) := by
  intro i
  apply SmoothMatrixOn.add U _ _ (matrix_transport_smooth U hU V _ hV (hG i))
  intro a b
  change ContDiffOn ℝ ∞ (fun x => ∑ k : Fin 4, vectorJacobian V x k i*Gamma x k a b) U
  exact ContDiffOn.sum (fun k _ =>
    (vector_jacobian_smooth U hU V hV k i).mul (hG k a b))

#print axioms base_connection_lie_smooth

theorem connection_lie_split (Gamma : ConnectionField4) (V : VectorField4) :
    coordinateConnectionLie Gamma V = fun x i =>
      baseConnectionLie Gamma V x i + connectionGaugeDirection Gamma (vectorJacobian V) x i := by
  funext x i
  unfold coordinateConnectionLie baseConnectionLie connectionGaugeDirection mixedCovariantDerivative
  abel

#print axioms connection_lie_split

theorem connection_lie_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V) :
    SmoothConnectionOn U (coordinateConnectionLie Gamma V) := by
  rw [connection_lie_split]
  intro i
  exact SmoothMatrixOn.add U _ _ (base_connection_lie_smooth U hU Gamma V hG hV i)
    (gauge_direction_smooth U hU Gamma (vectorJacobian V) hG
      (vector_jacobian_smooth U hU V hV) i)

#print axioms connection_lie_smooth

theorem curvature_variation_add (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma C D : ConnectionField4)
    (hC : SmoothConnectionOn U C) (hD : SmoothConnectionOn U D)
    (x : Coordinate4) (hx : x∈U) (i j : Fin 4) :
    curvatureVariation Gamma (fun y k => C y k+D y k) x i j =
      curvatureVariation Gamma C x i j + curvatureVariation Gamma D x i j := by
  have hJ (a b : Fin 4) : connectionFirstJet (fun y k => C y k+D y k) x a b =
      connectionFirstJet C x a b+connectionFirstJet D x a b := by
    exact congrArg (fun J => J a) (tensorFieldJet_add _ _ x
      (smooth_matrix_differentiableAt U hU _ (hC b) x hx)
      (smooth_matrix_differentiableAt U hU _ (hD b) x hx))
  unfold curvatureVariation
  rw [hJ i j,hJ j i]
  noncomm_ring

#print axioms curvature_variation_add

theorem base_connection_lie_jet (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x∈U) (i j : Fin 4) :
    connectionFirstJet (baseConnectionLie Gamma V) x i j =
      (∑ k : Fin 4, vectorJacobian V x k i • connectionFirstJet Gamma x k j) +
      (∑ k : Fin 4, V x k • connectionSecondJet Gamma x i k j) +
      (∑ k : Fin 4, tensorFieldJet (vectorJacobian V) x i k j • Gamma x k) +
      ∑ k : Fin 4, vectorJacobian V x k j • connectionFirstJet Gamma x i k := by
  have hP := vector_jacobian_smooth U hU V hV
  have hterm (k : Fin 4) :
      SmoothMatrixOn U (fun y => vectorJacobian V y k j • Gamma y k) := by
    intro a b
    exact (hP k j).mul (hG k a b)
  have hsum : SmoothMatrixOn U (fun y =>
      ∑ k : Fin 4, vectorJacobian V y k j • Gamma y k) := by
    intro a b
    change ContDiffOn ℝ ∞ (fun y => ∑ k : Fin 4, vectorJacobian V y k j*Gamma y k a b) U
    exact ContDiffOn.sum (fun k _ => (hP k j).mul (hG k a b))
  change tensorFieldJet (fun y => matrixTransport V (fun z => Gamma z j) y +
    ∑ k : Fin 4, vectorJacobian V y k j • Gamma y k) x i = _
  rw [tensorFieldJet_add _ _ x
    (smooth_matrix_differentiableAt U hU _
      (matrix_transport_smooth U hU V _ hV (hG j)) x hx)
    (smooth_matrix_differentiableAt U hU _ hsum x hx)]
  simp only [Pi.add_apply]
  rw [matrix_transport_jet U hU V _ hV (hG j) x hx i,
    tensor_jet_sum U hU (fun k y => vectorJacobian V y k j • Gamma y k) hterm x hx i]
  have hprod (k : Fin 4) := tensor_jet_scalar_product U hU
    (fun y => vectorJacobian V y k j) (fun y => Gamma y k)
    (hP k j) (hG k) x hx i
  simp_rw [hprod]
  simp only [Finset.sum_add_distrib,connectionFirstJet,connectionSecondJet,tensorFieldJet]
  abel

#print axioms base_connection_lie_jet

theorem base_curvature_lie_variation (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x∈U) (i j : Fin 4) :
    curvatureVariation Gamma (baseConnectionLie Gamma V) x i j =
      matrixTransport V (fun y => coordinateCurvature Gamma y i j) x +
      (∑ k : Fin 4, vectorJacobian V x k i • coordinateCurvature Gamma x k j) +
      ∑ k : Fin 4, vectorJacobian V x k j • coordinateCurvature Gamma x i k := by
  unfold curvatureVariation
  rw [base_connection_lie_jet U hU Gamma V hG hV x hx i j,
    base_connection_lie_jet U hU Gamma V hG hV x hx j i]
  have hdd (a b c : Fin 4) :
      connectionSecondJet Gamma x a b c=connectionSecondJet Gamma x b a c :=
    tensorFieldJet_commute U hU (fun y => Gamma y c) (hG c) x hx a b
  have hH := vector_jacobian_hessian_symmetry U hU V hV x hx
  unfold baseConnectionLie matrixTransport
  simp_rw [coordinate_curvature_derivative U hU Gamma hG x hx]
  simp only [coordinateCurvature,connectionCurvatureJet,curvatureDerivativeJet,
    Fin.sum_univ_four,Matrix.add_mul,Matrix.mul_add,
    Matrix.smul_mul,Matrix.mul_smul]
  simp only [hdd,hH,connectionFirstJet]
  module

#print axioms base_curvature_lie_variation

theorem curvature_connection_lie_variation (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x∈U) (i j : Fin 4) :
    curvatureVariation Gamma (coordinateConnectionLie Gamma V) x i j =
      matrixTransport V (fun y => coordinateCurvature Gamma y i j) x +
      (∑ k : Fin 4, vectorJacobian V x k i • coordinateCurvature Gamma x k j) +
      (∑ k : Fin 4, vectorJacobian V x k j • coordinateCurvature Gamma x i k) +
      coordinateCurvature Gamma x i j*vectorJacobian V x -
      vectorJacobian V x*coordinateCurvature Gamma x i j := by
  rw [connection_lie_split,curvature_variation_add U hU Gamma _ _
    (base_connection_lie_smooth U hU Gamma V hG hV)
    (gauge_direction_smooth U hU Gamma _ hG (vector_jacobian_smooth U hU V hV)) x hx i j,
    base_curvature_lie_variation U hU Gamma V hG hV x hx i j,
    curvature_gauge_variation U hU Gamma _ hG (vector_jacobian_smooth U hU V hV) x hx i j]
  abel

#print axioms curvature_connection_lie_variation

theorem ricci_connection_lie_variation (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x∈U) :
    ricciVariation Gamma (coordinateConnectionLie Gamma V) x =
      coordinateMetricLie (coordinateRicci Gamma) V x := by
  ext b j
  rw [coordinate_metric_lie_matrix_formula]
  simp only [ricciVariation,curvature_connection_lie_variation U hU Gamma V hG hV x hx]
  simp only [matrixTransport,Matrix.add_apply,Matrix.sub_apply,Matrix.mul_apply,
    Matrix.transpose_apply,Fin.sum_univ_four,Matrix.smul_apply,smul_eq_mul]
  simp_rw [ricci_derivative_trace U hU Gamma hG x hx]
  simp only [coordinateRicci,Fin.sum_univ_four]
  ring

#print axioms ricci_connection_lie_variation

theorem actual_levi_civita_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (hg : SmoothMatrixOn U g)
    (hi : ∀ x∈U, IsUnit (g x)) :
    SmoothConnectionOn U (leviCivitaField g (fun y => (g y)⁻¹)) := by
  intro i
  exact SmoothMatrixOn.mul U _ _ (smooth_matrix_inverse U g hg hi)
    (fun a b => lower_metric_jet_smooth U hU g hg i a b)

#print axioms actual_levi_civita_smooth

/-- Infinitesimal naturality for the real metric-induced Ricci, on an arbitrary curved chart. -/
theorem metric_lie_ricci_naturality
    (U : Set Coordinate4) (hU : IsOpen U) (g : TensorField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hs : ∀ x∈U, (g x)ᵀ=g x) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) (b j : Fin 4) :
    HasDerivAt (fun t => coordinateRicci
      (perturbedLeviCivita g (coordinateMetricLie g V) t) x b j)
      (coordinateMetricLie
        (coordinateRicci (leviCivitaField g (fun y => (g y)⁻¹))) V x b j) 0 := by
  have H := metric_lie_ricci_reduced_to_connection U hU g V hg hV hs hi x hx b j
  rw [ricci_connection_lie_variation U hU _ V
    (actual_levi_civita_smooth U hU g hg hi) hV x hx] at H
  exact H

#print axioms metric_lie_ricci_naturality

end
end ChatgptAudit.RicciLie
