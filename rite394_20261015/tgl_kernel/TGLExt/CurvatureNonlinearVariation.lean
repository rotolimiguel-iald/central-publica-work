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
import TGLExt.VectorCurvatureCommutator
import TGLExt.MetricCurvatureSymmetries

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.CurvedConnection
open Matrix Filter Topology Set
open scoped ContDiff
noncomputable section

def affineConnection (Gamma C : ConnectionField4) (t : ℝ) : ConnectionField4 :=
  fun x i => Gamma x i + t • C x i

def curvatureVariation (Gamma C : ConnectionField4) (x : Coordinate4)
    (i j : Fin 4) : Tensor4 :=
  connectionFirstJet C x i j - connectionFirstJet C x j i +
    Gamma x i * C x j + C x i * Gamma x j -
    Gamma x j * C x i - C x j * Gamma x i

def curvatureQuadratic (C : ConnectionField4) (x : Coordinate4)
    (i j : Fin 4) : Tensor4 := C x i * C x j - C x j * C x i

def ricciVariation (Gamma C : ConnectionField4) (x : Coordinate4) : Tensor4 :=
  fun b j => ∑ a, curvatureVariation Gamma C x a j a b

def ricciQuadratic (C : ConnectionField4) (x : Coordinate4) : Tensor4 :=
  fun b j => ∑ a, curvatureQuadratic C x a j a b

def connectionGaugeDirection (Gamma : ConnectionField4) (B : TensorField4) :
    ConnectionField4 := fun x i => mixedCovariantDerivative Gamma B x i

theorem affine_connection_smooth (U : Set Coordinate4) (Gamma C : ConnectionField4)
    (hG : SmoothConnectionOn U Gamma) (hC : SmoothConnectionOn U C) (t : ℝ) :
    SmoothConnectionOn U (affineConnection Gamma C t) := by
  intro i a b
  exact (hG i a b).add ((hC i a b).const_smul t)

theorem affine_connection_first_jet (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma C : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (hC : SmoothConnectionOn U C) (x : Coordinate4) (hx : x∈U)
    (t : ℝ) (i j : Fin 4) :
    connectionFirstJet (affineConnection Gamma C t) x i j =
      connectionFirstJet Gamma x i j + t • connectionFirstJet C x i j := by
  have hGi := smooth_matrix_differentiableAt U hU _ (hG j) x hx
  have hCi := smooth_matrix_differentiableAt U hU _ (hC j) x hx
  change tensorFieldJet (fun y => Gamma y j + t • C y j) x i = _
  have hScaled : ∀ a b, DifferentiableAt ℝ (fun y => (t • C y j) a b) x := by
    intro a b
    exact (hCi a b).const_mul t
  rw [tensorFieldJet_add (fun y => Gamma y j) (fun y => t • C y j) x hGi hScaled,
    tensorFieldJet_const_smul t (fun y => C y j) x hCi]
  rfl

theorem curvature_exact_expansion (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma C : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (hC : SmoothConnectionOn U C) (x : Coordinate4) (hx : x∈U)
    (t : ℝ) (i j : Fin 4) :
    coordinateCurvature (affineConnection Gamma C t) x i j =
      coordinateCurvature Gamma x i j +
        t • curvatureVariation Gamma C x i j + t^2 • curvatureQuadratic C x i j := by
  unfold coordinateCurvature connectionCurvatureJet
  rw [affine_connection_first_jet U hU Gamma C hG hC x hx t i j,
    affine_connection_first_jet U hU Gamma C hG hC x hx t j i]
  simp only [affineConnection,curvatureVariation,curvatureQuadratic,
    Matrix.add_mul,Matrix.mul_add,Matrix.smul_mul,Matrix.mul_smul]
  module

theorem curvature_exact_remainder (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma C : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (hC : SmoothConnectionOn U C) (x : Coordinate4) (hx : x∈U)
    (t : ℝ) (i j : Fin 4) :
    coordinateCurvature (affineConnection Gamma C t) x i j -
      coordinateCurvature Gamma x i j - t • curvatureVariation Gamma C x i j =
        t^2 • curvatureQuadratic C x i j := by
  rw [curvature_exact_expansion U hU Gamma C hG hC x hx t i j]
  abel

theorem curvature_parameter_derivative (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma C : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (hC : SmoothConnectionOn U C) (x : Coordinate4) (hx : x∈U)
    (t : ℝ) (i j a b : Fin 4) :
    HasDerivAt (fun s => coordinateCurvature (affineConnection Gamma C s) x i j a b)
      (curvatureVariation Gamma C x i j a b +
        2*t*curvatureQuadratic C x i j a b) t := by
  have he : (fun s => coordinateCurvature (affineConnection Gamma C s) x i j a b) =
      (fun s => coordinateCurvature Gamma x i j a b +
        s*curvatureVariation Gamma C x i j a b + s^2*curvatureQuadratic C x i j a b) := by
    funext s
    rw [curvature_exact_expansion U hU Gamma C hG hC x hx s i j]
    rfl
  rw [he]
  convert ((hasDerivAt_const t (coordinateCurvature Gamma x i j a b)).add
    ((hasDerivAt_id t).mul_const (curvatureVariation Gamma C x i j a b))).add
      (((hasDerivAt_id t).pow 2).mul_const (curvatureQuadratic C x i j a b)) using 1 <;> first | rfl | norm_num [id_eq]

theorem curvature_first_variation (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma C : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (hC : SmoothConnectionOn U C) (x : Coordinate4) (hx : x∈U)
    (i j a b : Fin 4) :
    HasDerivAt (fun s => coordinateCurvature (affineConnection Gamma C s) x i j a b)
      (curvatureVariation Gamma C x i j a b) 0 := by
  simpa using curvature_parameter_derivative U hU Gamma C hG hC x hx 0 i j a b

theorem ricci_exact_expansion (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma C : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (hC : SmoothConnectionOn U C) (x : Coordinate4) (hx : x∈U) (t : ℝ) :
    coordinateRicci (affineConnection Gamma C t) x =
      coordinateRicci Gamma x + t • ricciVariation Gamma C x + t^2 • ricciQuadratic C x := by
  ext b j
  simp only [coordinateRicci,curvature_exact_expansion U hU Gamma C hG hC x hx,
    Matrix.add_apply,Matrix.smul_apply,smul_eq_mul,Finset.sum_add_distrib,
    Finset.mul_sum,ricciVariation,ricciQuadratic]

theorem ricci_first_variation (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma C : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (hC : SmoothConnectionOn U C) (x : Coordinate4) (hx : x∈U) (b j : Fin 4) :
    HasDerivAt (fun t => coordinateRicci (affineConnection Gamma C t) x b j)
      (ricciVariation Gamma C x b j) 0 := by
  simpa only [coordinateRicci,ricciVariation] using
    HasDerivAt.fun_sum (u := Finset.univ)
      (fun a _ => curvature_first_variation U hU Gamma C hG hC x hx a j a b)

theorem gauge_direction_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (B : TensorField4)
    (hG : SmoothConnectionOn U Gamma) (hB : SmoothMatrixOn U B) :
    SmoothConnectionOn U (connectionGaugeDirection Gamma B) := by
  intro i
  exact SmoothMatrixOn.sub U _ _
    (SmoothMatrixOn.add U _ _ (tensorFieldJet_smooth U hU B hB i)
      (SmoothMatrixOn.mul U _ _ (hG i) hB))
    (SmoothMatrixOn.mul U _ _ hB (hG i))

theorem gauge_direction_first_jet (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (B : TensorField4)
    (hG : SmoothConnectionOn U Gamma) (hB : SmoothMatrixOn U B)
    (x : Coordinate4) (hx : x∈U) (i j : Fin 4) :
    connectionFirstJet (connectionGaugeDirection Gamma B) x i j =
      tensorFieldJet (fun y => tensorFieldJet B y j) x i +
        connectionFirstJet Gamma x i j * B x + Gamma x j * tensorFieldJet B x i -
        tensorFieldJet B x i * Gamma x j - B x * connectionFirstJet Gamma x i j := by
  have hdiff (A : TensorField4) (hA : SmoothMatrixOn U A) :=
    smooth_matrix_differentiableAt U hU A hA x hx
  change tensorFieldJet (fun y => tensorFieldJet B y j + Gamma y j * B y - B y * Gamma y j) x i = _
  rw [tensorFieldJet_sub _ _ x
      (hdiff _ (SmoothMatrixOn.add U _ _ (tensorFieldJet_smooth U hU B hB j)
        (SmoothMatrixOn.mul U _ _ (hG j) hB)))
      (hdiff _ (SmoothMatrixOn.mul U _ _ hB (hG j))),
    tensorFieldJet_add _ _ x (hdiff _ (tensorFieldJet_smooth U hU B hB j))
      (hdiff _ (SmoothMatrixOn.mul U _ _ (hG j) hB))]
  simp only [Pi.sub_apply,Pi.add_apply]
  rw [tensorFieldJet_mul _ _ x (hdiff _ (hG j)) (hdiff _ hB) i,
    tensorFieldJet_mul _ _ x (hdiff _ hB) (hdiff _ (hG j)) i]
  simp only [connectionFirstJet]
  abel

theorem curvature_gauge_variation (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (B : TensorField4)
    (hG : SmoothConnectionOn U Gamma) (hB : SmoothMatrixOn U B)
    (x : Coordinate4) (hx : x∈U) (i j : Fin 4) :
    curvatureVariation Gamma (connectionGaugeDirection Gamma B) x i j =
      coordinateCurvature Gamma x i j * B x - B x * coordinateCurvature Gamma x i j := by
  unfold curvatureVariation
  rw [gauge_direction_first_jet U hU Gamma B hG hB x hx i j,
    gauge_direction_first_jet U hU Gamma B hG hB x hx j i,
    tensorFieldJet_commute U hU B hB x hx i j]
  simp only [connectionGaugeDirection,mixedCovariantDerivative,coordinateCurvature,connectionCurvatureJet]
  noncomm_ring

theorem curvature_gauge_derivative (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (B : TensorField4)
    (hG : SmoothConnectionOn U Gamma) (hB : SmoothMatrixOn U B)
    (x : Coordinate4) (hx : x∈U) (i j a b : Fin 4) :
    HasDerivAt
      (fun t => coordinateCurvature (affineConnection Gamma (connectionGaugeDirection Gamma B) t) x i j a b)
      ((coordinateCurvature Gamma x i j * B x - B x * coordinateCurvature Gamma x i j) a b) 0 := by
  rw [← curvature_gauge_variation U hU Gamma B hG hB x hx i j]
  exact curvature_first_variation U hU Gamma _ hG (gauge_direction_smooth U hU Gamma B hG hB) x hx i j a b

theorem curvature_gauge_trace_zero (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (B : TensorField4)
    (hG : SmoothConnectionOn U Gamma) (hB : SmoothMatrixOn U B)
    (x : Coordinate4) (hx : x∈U) (i j : Fin 4) :
    Matrix.trace (curvatureVariation Gamma (connectionGaugeDirection Gamma B) x i j) = 0 := by
  rw [curvature_gauge_variation U hU Gamma B hG hB x hx i j,Matrix.trace_sub,
    Matrix.trace_mul_comm]
  ring

theorem flat_curvature_gauge_variation_zero (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (B : TensorField4)
    (hG : SmoothConnectionOn U Gamma) (hB : SmoothMatrixOn U B)
    (x : Coordinate4) (hx : x∈U) (i j : Fin 4)
    (hflat : coordinateCurvature Gamma x i j = 0) :
    curvatureVariation Gamma (connectionGaugeDirection Gamma B) x i j = 0 := by
  rw [curvature_gauge_variation U hU Gamma B hG hB x hx i j,hflat,zero_mul,mul_zero,sub_self]


/-- Constant matrix connections can have nonzero curvature through their commutator. -/
theorem constant_connection_curvature (G : ConnectionMatrix4) (x : Coordinate4) (i j : Fin 4) :
    coordinateCurvature (fun _ => G) x i j = G i * G j - G j * G i := by
  have hz (a b : Fin 4) : connectionFirstJet (fun _ => G) x a b = 0 := by
    ext k l
    simp [connectionFirstJet,tensorFieldJet,coordinatePartial]
  simp only [coordinateCurvature,connectionCurvatureJet,hz,sub_self,zero_add]

/-- The quadratic term is nonzero for an explicit connection direction. -/
theorem nonzero_quadratic_control :
    curvatureQuadratic
      (fun _ i => if i=0 then Matrix.single 0 1 (1:ℝ) else Matrix.single 1 0 (1:ℝ))
      0 0 1 0 0 = 1 := by
  norm_num [curvatureQuadratic,Matrix.mul_apply,Fin.sum_univ_four,Matrix.single_apply]

/-- Even a constant curved background need not have zero infinitesimal gauge variation. -/
theorem nonzero_curved_gauge_control :
    ∃ (Gamma : ConnectionField4) (B : TensorField4),
      SmoothConnectionOn univ Gamma ∧ SmoothMatrixOn univ B ∧
        curvatureVariation Gamma (connectionGaugeDirection Gamma B) 0 0 1 0 1 = -1 := by
  let Gamma : ConnectionField4 :=
    fun _ i => if i=0 then Matrix.single 0 0 (1:ℝ) else Matrix.single 0 1 (1:ℝ)
  let B : TensorField4 := fun _ => Matrix.single 0 0 (1:ℝ)
  have hG : SmoothConnectionOn univ Gamma := fun _ _ _ => contDiffOn_const
  have hB : SmoothMatrixOn univ B := fun _ _ => contDiffOn_const
  refine ⟨Gamma,B,hG,hB,?_⟩
  rw [curvature_gauge_variation univ isOpen_univ Gamma B hG hB 0 (mem_univ 0) 0 1,
    constant_connection_curvature]
  norm_num [Gamma,B,Matrix.sub_apply,Matrix.mul_apply,Fin.sum_univ_four,Matrix.single_apply]


/-- The first variation is the covariant exterior derivative of the connection direction. -/
theorem curvature_variation_covariant_exterior (Gamma C : ConnectionField4)
    (x : Coordinate4) (i j : Fin 4) :
    curvatureVariation Gamma C x i j =
      mixedCovariantDerivative Gamma (fun y => C y j) x i -
        mixedCovariantDerivative Gamma (fun y => C y i) x j := by
  simp only [curvatureVariation,mixedCovariantDerivative,connectionFirstJet]
  abel

/-- Ricci contracts a base and a vector index; it is not the matrix trace used above. -/
theorem ricci_gauge_variation (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (B : TensorField4)
    (hG : SmoothConnectionOn U Gamma) (hB : SmoothMatrixOn U B)
    (x : Coordinate4) (hx : x∈U) (b j : Fin 4) :
    ricciVariation Gamma (connectionGaugeDirection Gamma B) x b j =
      ∑ a, (coordinateCurvature Gamma x a j * B x -
        B x * coordinateCurvature Gamma x a j) a b := by
  unfold ricciVariation
  simp only [curvature_gauge_variation U hU Gamma B hG hB x hx]

#print axioms affineConnection
#print axioms curvatureVariation
#print axioms curvatureQuadratic
#print axioms ricciVariation
#print axioms ricciQuadratic
#print axioms connectionGaugeDirection
#print axioms affine_connection_smooth
#print axioms affine_connection_first_jet
#print axioms curvature_exact_expansion
#print axioms curvature_exact_remainder
#print axioms curvature_parameter_derivative
#print axioms curvature_first_variation
#print axioms ricci_exact_expansion
#print axioms ricci_first_variation
#print axioms gauge_direction_smooth
#print axioms gauge_direction_first_jet
#print axioms curvature_gauge_variation
#print axioms curvature_gauge_derivative
#print axioms curvature_gauge_trace_zero
#print axioms flat_curvature_gauge_variation_zero
#print axioms constant_connection_curvature
#print axioms nonzero_quadratic_control
#print axioms nonzero_curved_gauge_control
#print axioms curvature_variation_covariant_exterior
#print axioms ricci_gauge_variation
end
end ChatgptAudit.CurvedConnection
