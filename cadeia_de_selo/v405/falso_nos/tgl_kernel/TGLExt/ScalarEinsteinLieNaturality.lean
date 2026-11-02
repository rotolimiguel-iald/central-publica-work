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
import TGLExt.MetricEinsteinVariation
import TGLExt.RicciLieNaturality

set_option autoImplicit false
set_option maxHeartbeats 1600000
namespace ChatgptAudit.EinsteinLie
open Matrix Filter Topology Set ChatgptAudit.Boost044
  ChatgptAudit.MetricVariation ChatgptAudit.MetricRicci
  ChatgptAudit.MetricLie ChatgptAudit.MetricLieConnection
  ChatgptAudit.RicciLie ChatgptAudit.MetricEinsteinVariation ChatgptAudit.CurvedConnection
noncomputable section
open scoped ContDiff

def tensorPair (A B : Tensor4) : ℝ := ∑ i : Fin 4, ∑ j : Fin 4, A i j*B i j

theorem tensor_pair_add_left (A B C : Tensor4) :
    tensorPair (A+B) C=tensorPair A C+tensorPair B C := by
  simp [tensorPair,add_mul,Finset.sum_add_distrib]

theorem tensor_pair_add_right (A B C : Tensor4) :
    tensorPair A (B+C)=tensorPair A B+tensorPair A C := by
  simp [tensorPair,mul_add,Finset.sum_add_distrib]

theorem tensor_pair_sub_left (A B C : Tensor4) :
    tensorPair (A-B) C=tensorPair A C-tensorPair B C := by
  simp [tensorPair,sub_mul,Finset.sum_sub_distrib]

theorem tensor_pair_transpose_left (A P R : Tensor4) :
    tensorPair A (Pᵀ*R)=tensorPair (P*A) R := by
  simp only [tensorPair,Matrix.mul_apply,Matrix.transpose_apply,Fin.sum_univ_four]
  ring

theorem tensor_pair_transpose_right (A P R : Tensor4) :
    tensorPair A (R*P)=tensorPair (A*Pᵀ) R := by
  simp only [tensorPair,Matrix.mul_apply,Matrix.transpose_apply,Fin.sum_univ_four]
  ring

theorem tensor_pair_scalar_transport (U : Set Coordinate4) (hU : IsOpen U)
    (A B : TensorField4) (V : VectorField4)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B)
    (x : Coordinate4) (hx : x∈U) :
    scalarAlong V (fun y => tensorPair (A y) (B y)) x =
      tensorPair (matrixTransport V A x) (B x) +
      tensorPair (A x) (matrixTransport V B x) := by
  have hprod (i j : Fin 4) : DifferentiableAt ℝ (fun y => A y i j*B y i j) x :=
    (smooth_matrix_differentiableAt U hU A hA x hx i j).mul
      (smooth_matrix_differentiableAt U hU B hB x hx i j)
  have hsum (i : Fin 4) : DifferentiableAt ℝ (fun y => ∑ j : Fin 4, A y i j*B y i j) x :=
    DifferentiableAt.fun_sum (fun j _ => hprod i j)
  have hj (k : Fin 4) :
      coordinatePartial (fun y => tensorPair (A y) (B y)) x k =
        ∑ i : Fin 4, ∑ j : Fin 4,
          (tensorFieldJet A x k i j*B x i j+A x i j*tensorFieldJet B x k i j) := by
    unfold tensorPair
    rw [coordinatePartial_sum _ x hsum k]
    apply Finset.sum_congr rfl
    intro i _
    rw [coordinatePartial_sum _ x (hprod i) k]
    apply Finset.sum_congr rfl
    intro j _
    exact coordinatePartial_mul _ _ x
      (smooth_matrix_differentiableAt U hU A hA x hx i j)
      (smooth_matrix_differentiableAt U hU B hB x hx i j) k
  unfold scalarAlong
  simp_rw [hj]
  simp only [tensorPair,matrixTransport,Fin.sum_univ_four,
    Matrix.add_apply,Matrix.smul_apply,smul_eq_mul]
  ring

theorem inverse_metric_lie_variation (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (V : VectorField4) (hg : SmoothMatrixOn U g)
    (hi : ∀ x∈U, IsUnit (g x)) (x : Coordinate4) (hx : x∈U) :
    -(g x)⁻¹*coordinateMetricLie g V x*(g x)⁻¹ =
      matrixTransport V (fun y => (g y)⁻¹) x -
        vectorJacobian V x*(g x)⁻¹ - (g x)⁻¹*(vectorJacobian V x)ᵀ := by
  rw [coordinate_metric_lie_matrix_formula]
  unfold matrixTransport
  simp_rw [matrix_inverse_spatial_jet U hU g hg hi x hx]
  simp only [Fin.sum_univ_four,Matrix.add_mul,Matrix.mul_add,Matrix.smul_mul,
    Matrix.mul_smul,neg_mul,mul_assoc]
  have hL (M : Tensor4) : (g x)⁻¹*(g x*M)=M := by
    rw [←mul_assoc,actual_inverse_left (g x) (hi x hx),one_mul]
  simp only [hL,actual_inverse_right (g x) (hi x hx),mul_one]
  module

theorem metric_lie_ricci_operator (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hs : ∀ x∈U, (g x)ᵀ=g x) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) :
    ricciVariation (leviCivitaField g (fun y => (g y)⁻¹))
      (metricConnectionVariation g (coordinateMetricLie g V)) x =
      coordinateMetricLie (coordinateRicci (leviCivitaField g (fun y => (g y)⁻¹))) V x := by
  ext i j
  exact (metric_ricci_first_variation U hU g (coordinateMetricLie g V)
    hg (coordinate_metric_lie_smooth U hU V g hV hg) hi x hx i j).unique
      (metric_lie_ricci_naturality U hU g V hg hV hs hi x hx i j)

theorem metric_lie_scalar_operator (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hs : ∀ x∈U, (g x)ᵀ=g x) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) :
    scalarMetricVariation g (coordinateMetricLie g V) x =
      scalarAlong V (coordinateScalarCurvature (fun y => (g y)⁻¹)
        (leviCivitaField g (fun y => (g y)⁻¹))) x := by
  have hR := coordinate_ricci_smooth U hU _ (actual_levi_civita_smooth U hU g hg hi)
  simp only [scalarMetricVariation,Finset.sum_add_distrib]
  change tensorPair (-(g x)⁻¹*coordinateMetricLie g V x*(g x)⁻¹)
      (coordinateRicci (leviCivitaField g (fun y => (g y)⁻¹)) x) +
    tensorPair ((g x)⁻¹) (ricciVariation (leviCivitaField g (fun y => (g y)⁻¹))
      (metricConnectionVariation g (coordinateMetricLie g V)) x) = _
  rw [metric_lie_ricci_operator U hU g V hg hV hs hi x hx,
    inverse_metric_lie_variation U hU g V hg hi x hx,
    coordinate_metric_lie_matrix_formula]
  change _ = scalarAlong V (fun y => tensorPair ((g y)⁻¹)
    (coordinateRicci (leviCivitaField g (fun y => (g y)⁻¹)) y)) x
  rw [tensor_pair_scalar_transport U hU _ _ V
    (smooth_matrix_inverse U g hg hi) hR x hx]
  simp only [tensor_pair_add_right,tensor_pair_sub_left]
  rw [tensor_pair_transpose_left ((g x)⁻¹) (vectorJacobian V x)
      (coordinateRicci (leviCivitaField g (fun y => (g y)⁻¹)) x),
    tensor_pair_transpose_right ((g x)⁻¹) (vectorJacobian V x)
      (coordinateRicci (leviCivitaField g (fun y => (g y)⁻¹)) x)]
  ring

theorem metric_lie_scalar_naturality (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hs : ∀ x∈U, (g x)ᵀ=g x) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) :
    HasDerivAt (fun t => coordinateScalarCurvature
      (perturbedMetricInverse g (coordinateMetricLie g V) t)
      (perturbedLeviCivita g (coordinateMetricLie g V) t) x)
      (scalarAlong V (coordinateScalarCurvature (fun y => (g y)⁻¹)
        (leviCivitaField g (fun y => (g y)⁻¹))) x) 0 := by
  rw [←metric_lie_scalar_operator U hU g V hg hV hs hi x hx]
  exact metric_scalar_first_variation U hU g (coordinateMetricLie g V)
    hg (coordinate_metric_lie_smooth U hU V g hV hg) hi x hx


theorem scalar_along_div_two (U : Set Coordinate4) (hU : IsOpen U)
    (f : Coordinate4 → ℝ) (V : VectorField4) (hf : ContDiffOn ℝ ∞ f U)
    (x : Coordinate4) (hx : x∈U) :
    scalarAlong V (fun y => f y/2) x=scalarAlong V f x/2 := by
  have hd := (hf.differentiableOn (by simp)).differentiableAt (hU.mem_nhds hx)
  have hJ (k : Fin 4) : coordinatePartial (fun y => f y/2) x k=
      coordinatePartial f x k/2 := by
    change coordinatePartial (fun y => f y*(2:ℝ)⁻¹) x k=
      coordinatePartial f x k*(2:ℝ)⁻¹
    rw [coordinatePartial_mul f (fun _ => (2:ℝ)⁻¹) x hd
      (differentiableAt_const _) k]
    have hc : coordinatePartial (fun _ : Coordinate4 => (2:ℝ)⁻¹) x k=0 := by
      unfold coordinatePartial
      rw [(hasFDerivAt_const ((2:ℝ)⁻¹) x).fderiv]
      rfl
    rw [hc,mul_zero,add_zero]
  unfold scalarAlong
  simp_rw [hJ]
  simp only [Fin.sum_univ_four]
  ring

theorem coordinate_metric_lie_subtract (U : Set Coordinate4) (hU : IsOpen U)
    (A B : TensorField4) (V : VectorField4)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B)
    (x : Coordinate4) (hx : x∈U) :
    coordinateMetricLie (fun y => A y-B y) V x=
      coordinateMetricLie A V x-coordinateMetricLie B V x := by
  ext i j
  have hJ (k : Fin 4) := coordinatePartial_sub (fun y => A y i j) (fun y => B y i j)
    x (smooth_matrix_differentiableAt U hU A hA x hx i j)
      (smooth_matrix_differentiableAt U hU B hB x hx i j) k
  simp only [coordinateMetricLie,scalarAlong,Matrix.sub_apply]
  simp_rw [hJ]
  simp only [Fin.sum_univ_four]
  ring

theorem coordinate_metric_lie_scalar_product (U : Set Coordinate4) (hU : IsOpen U)
    (f : Coordinate4 → ℝ) (A : TensorField4) (V : VectorField4)
    (hf : ContDiffOn ℝ ∞ f U) (hA : SmoothMatrixOn U A)
    (x : Coordinate4) (hx : x∈U) :
    coordinateMetricLie (fun y => f y • A y) V x=
      scalarAlong V f x • A x+f x • coordinateMetricLie A V x := by
  simp_rw [coordinate_metric_lie_matrix_formula]
  unfold matrixTransport
  simp_rw [tensor_jet_scalar_product U hU f A hf hA x hx]
  simp only [Fin.sum_univ_four,Matrix.smul_mul,Matrix.mul_smul,scalarAlong]
  module

theorem metric_lie_einstein_operator (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hs : ∀ x∈U, (g x)ᵀ=g x) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) :
    einsteinMetricVariation g (coordinateMetricLie g V) x =
      coordinateMetricLie (geometricEinsteinTensor g (fun y => (g y)⁻¹)
        (leviCivitaField g (fun y => (g y)⁻¹))) V x := by
  have hG := actual_levi_civita_smooth U hU g hg hi
  have hR := coordinate_ricci_smooth U hU _ hG
  have hsc := scalar_curvature_smooth U hU _ _ (smooth_matrix_inverse U g hg hi) hG
  have hsg : SmoothMatrixOn U (fun y =>
      (coordinateScalarCurvature (fun z => (g z)⁻¹)
        (leviCivitaField g (fun z => (g z)⁻¹)) y/2) • g y) := by
    intro i j
    exact (hsc.div_const 2).mul (hg i j)
  unfold einsteinMetricVariation
  rw [metric_lie_ricci_operator U hU g V hg hV hs hi x hx,
    metric_lie_scalar_operator U hU g V hg hV hs hi x hx]
  unfold geometricEinsteinTensor
  rw [coordinate_metric_lie_subtract U hU _ _ V hR hsg x hx,
    coordinate_metric_lie_scalar_product U hU _ g V (hsc.div_const 2) hg x hx,
    scalar_along_div_two U hU _ V hsc x hx]
  abel

theorem metric_lie_einstein_naturality (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hs : ∀ x∈U, (g x)ᵀ=g x) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) :
    HasDerivAt (fun t => geometricEinsteinTensor
      (metricPerturbation g (coordinateMetricLie g V) t)
      (perturbedMetricInverse g (coordinateMetricLie g V) t)
      (perturbedLeviCivita g (coordinateMetricLie g V) t) x)
      (coordinateMetricLie (geometricEinsteinTensor g (fun y => (g y)⁻¹)
        (leviCivitaField g (fun y => (g y)⁻¹))) V x) 0 := by
  rw [←metric_lie_einstein_operator U hU g V hg hV hs hi x hx]
  exact metric_einstein_first_variation U hU g (coordinateMetricLie g V)
    hg (coordinate_metric_lie_smooth U hU V g hV hg) hi x hx


#print axioms tensorPair
#print axioms tensor_pair_add_left
#print axioms tensor_pair_add_right
#print axioms tensor_pair_sub_left
#print axioms tensor_pair_transpose_left
#print axioms tensor_pair_transpose_right
#print axioms tensor_pair_scalar_transport
#print axioms inverse_metric_lie_variation
#print axioms metric_lie_ricci_operator
#print axioms metric_lie_scalar_operator
#print axioms metric_lie_scalar_naturality
#print axioms scalar_along_div_two
#print axioms coordinate_metric_lie_subtract
#print axioms coordinate_metric_lie_scalar_product
#print axioms metric_lie_einstein_operator
#print axioms metric_lie_einstein_naturality
end
end ChatgptAudit.EinsteinLie
