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
import TGLExt.FiniteCurvatureAlgebra

set_option autoImplicit false
set_option maxHeartbeats 1600000
namespace ChatgptAudit.FiniteCoordinateCurvature
open Matrix Filter Topology Set TGLExt ChatgptAudit.FiniteCoordinates
  ChatgptAudit.FiniteLeviCivita ChatgptAudit.FiniteCurvatureAlgebra
  ChatgptAudit.GeneralMetric ChatgptAudit.MetricLie
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section
variable {U W : Set Coordinate4}

def coordinateConnection (C : SmoothCoordinateChange U W) (Gamma : ConnectionField4) :
    ConnectionField4 :=
  fun x => coordinateConnectionJet (changeJacobian C x) (Gamma (C.forward x))

theorem inverse_change_jacobian_jet (C : SmoothCoordinateChange U W)
    (x : Coordinate4) (hx : x ∈ U) (i : Fin 4) :
    tensorFieldJet (inverseChangeJacobian C) x i =
      -inverseChangeJacobian C x * tensorFieldJet (changeJacobian C) x i *
        inverseChangeJacobian C x := by
  have hdiff (A : TensorField4) (hA : SmoothMatrixOn U A) :=
    smooth_matrix_differentiableAt U C.source_open A hA x hx
  have he : EqOn (fun y => inverseChangeJacobian C y * changeJacobian C y)
      (fun _ => (1 : Tensor4)) U :=
    fun y hy => inverse_jacobian_mul_jacobian C y hy
  have hd := congrFun (tensorFieldJet_congr_on U C.source_open _ _ he x hx) i
  have hz : tensorFieldJet (fun _ : Coordinate4 => (1 : Tensor4)) x i = 0 := by
    ext a b
    simp [tensorFieldJet,coordinatePartial]
  rw [tensorFieldJet_mul _ _ x (hdiff _ (inverse_change_jacobian_smooth C))
    (hdiff _ (change_jacobian_smooth C)) i,hz] at hd
  have hh := congrArg (fun M : Tensor4 => M * inverseChangeJacobian C x) hd
  have hc (X : Tensor4) : X * changeJacobian C x * inverseChangeJacobian C x = X := by
    rw [Matrix.mul_assoc,jacobian_mul_inverse_jacobian C x hx,mul_one]
  have heq : tensorFieldJet (inverseChangeJacobian C) x i +
      inverseChangeJacobian C x * tensorFieldJet (changeJacobian C) x i *
        inverseChangeJacobian C x = 0 := by
    simpa only [Matrix.add_mul,hc,zero_mul] using hh
  calc
    _ = -(inverseChangeJacobian C x * tensorFieldJet (changeJacobian C) x i *
      inverseChangeJacobian C x) := eq_neg_of_add_eq_zero_left heq
    _ = _ := by simp only [neg_mul]

theorem coordinate_connection_smooth (C : SmoothCoordinateChange U W)
    (Gamma : ConnectionField4) (hGamma : SmoothConnectionOn W Gamma) :
    SmoothConnectionOn U (coordinateConnection C Gamma) := by
  intro i a b
  change ContDiffOn ℝ ∞
    (fun y => ∑ k : Fin 4, changeJacobian C y k i * Gamma (C.forward y) k a b) U
  exact ContDiffOn.sum (fun k _ =>
    (change_jacobian_smooth C k i).mul (matrix_composition_smooth C
      (fun y => Gamma y k) (hGamma k) a b))

theorem coordinate_connection_first_jet (C : SmoothCoordinateChange U W)
    (Gamma : ConnectionField4) (hGamma : SmoothConnectionOn W Gamma)
    (x : Coordinate4) (hx : x ∈ U) (i j : Fin 4) :
    connectionFirstJet (coordinateConnection C Gamma) x i j =
      coordinateConnectionDerivative (changeJacobian C x)
        (tensorFieldJet (changeJacobian C) x) (Gamma (C.forward x))
        (connectionFirstJet Gamma (C.forward x)) i j := by
  have hcomp (a : Fin 4) := matrix_composition_smooth C
    (fun y => Gamma y a) (hGamma a)
  have hterm (a : Fin 4) :
      SmoothMatrixOn U (fun y => changeJacobian C y a j • Gamma (C.forward y) a) := by
    intro b c
    exact (change_jacobian_smooth C a j).mul (hcomp a b c)
  change tensorFieldJet
    (fun y => ∑ a : Fin 4, changeJacobian C y a j • Gamma (C.forward y) a) x i = _
  rw [tensor_jet_sum U C.source_open _ hterm x hx i]
  have he (a : Fin 4) :
      tensorFieldJet (fun y => changeJacobian C y a j • Gamma (C.forward y) a) x i =
        tensorFieldJet (changeJacobian C) x i a j • Gamma (C.forward x) a +
          ∑ b : Fin 4, (changeJacobian C x a j * changeJacobian C x b i) •
            connectionFirstJet Gamma (C.forward x) b a := by
    rw [tensor_jet_scalar_product U C.source_open _ _
      (change_jacobian_smooth C a j) (hcomp a) x hx i,
      tensor_jet_composition C (fun y => Gamma y a) (hGamma a) x hx i]
    simp only [Finset.smul_sum,smul_smul]
    rfl
  simp_rw [he]
  rw [Finset.sum_add_distrib]
  rfl

theorem pullback_connection_smooth (C : SmoothCoordinateChange U W)
    (Gamma : ConnectionField4) (hGamma : SmoothConnectionOn W Gamma) :
    SmoothConnectionOn U (pullbackConnection C Gamma) := by
  intro i
  exact SmoothMatrixOn.mul U _ _ (inverse_change_jacobian_smooth C)
    (SmoothMatrixOn.add U _ _
      (SmoothMatrixOn.mul U _ _ (coordinate_connection_smooth C Gamma hGamma i)
        (change_jacobian_smooth C))
      (tensorFieldJet_smooth U C.source_open _ (change_jacobian_smooth C) i))

theorem pullback_connection_first_jet (C : SmoothCoordinateChange U W)
    (Gamma : ConnectionField4) (hGamma : SmoothConnectionOn W Gamma)
    (x : Coordinate4) (hx : x ∈ U) (i j : Fin 4) :
    connectionFirstJet (pullbackConnection C Gamma) x i j =
      gaugeConnectionDerivative (changeJacobian C x) (inverseChangeJacobian C x)
        (coordinateConnection C Gamma x) (tensorFieldJet (changeJacobian C) x)
        (connectionFirstJet (coordinateConnection C Gamma) x)
        (connectionFirstJet (fun y => tensorFieldJet (changeJacobian C) y) x) i j := by
  have hJ := change_jacobian_smooth C
  have hD := inverse_change_jacobian_smooth C
  have hA := coordinate_connection_smooth C Gamma hGamma j
  have hH := tensorFieldJet_smooth U C.source_open _ hJ j
  have hAJ := SmoothMatrixOn.mul U _ _ hA hJ
  have hdiff (A : TensorField4) (h : SmoothMatrixOn U A) :=
    smooth_matrix_differentiableAt U C.source_open A h x hx
  change tensorFieldJet (fun y =>
    inverseChangeJacobian C y *
      (coordinateConnection C Gamma y j * changeJacobian C y +
        tensorFieldJet (changeJacobian C) y j)) x i = _
  rw [tensorFieldJet_mul _ _ x (hdiff _ hD)
    (hdiff _ (SmoothMatrixOn.add U _ _ hAJ hH)) i]
  rw [tensorFieldJet_add _ _ x (hdiff _ hAJ) (hdiff _ hH)]
  simp only [Pi.add_apply]
  rw [tensorFieldJet_mul _ _ x (hdiff _ hA) (hdiff _ hJ) i,
    inverse_change_jacobian_jet C x hx i]
  rfl

theorem coordinate_curvature_finite_transformation (C : SmoothCoordinateChange U W)
    (Gamma : ConnectionField4) (hGamma : SmoothConnectionOn W Gamma)
    (x : Coordinate4) (hx : x ∈ U) (i j : Fin 4) :
    coordinateCurvature (pullbackConnection C Gamma) x i j =
      inverseChangeJacobian C x *
        pulledCurvatureJet (changeJacobian C x) (coordinateCurvature Gamma (C.forward x)) i j *
          changeJacobian C x := by
  have heA : connectionFirstJet (coordinateConnection C Gamma) x =
      coordinateConnectionDerivative (changeJacobian C x)
        (tensorFieldJet (changeJacobian C) x) (Gamma (C.forward x))
        (connectionFirstJet Gamma (C.forward x)) := by
    funext a b
    exact coordinate_connection_first_jet C Gamma hGamma x hx a b
  have heG : connectionFirstJet (pullbackConnection C Gamma) x =
      gaugeConnectionDerivative (changeJacobian C x) (inverseChangeJacobian C x)
        (coordinateConnection C Gamma x) (tensorFieldJet (changeJacobian C) x)
        (connectionFirstJet (coordinateConnection C Gamma) x)
        (connectionFirstJet (fun y => tensorFieldJet (changeJacobian C) y) x) := by
    funext a b
    exact pullback_connection_first_jet C Gamma hGamma x hx a b
  have hh (a b : Fin 4) :
      connectionFirstJet (fun y => tensorFieldJet (changeJacobian C) y) x a b =
        connectionFirstJet (fun y => tensorFieldJet (changeJacobian C) y) x b a :=
    tensorFieldJet_commute U C.source_open _ (change_jacobian_smooth C) x hx a b
  unfold coordinateCurvature
  rw [heG,heA]
  exact finite_curvature_jet_identity _ _ _ _ _ _
    (jacobian_mul_inverse_jacobian C x hx)
    (change_jacobian_hessian_symmetry C x hx) hh i j

#print axioms coordinateConnection
#print axioms inverse_change_jacobian_jet
#print axioms coordinate_connection_smooth
#print axioms coordinate_connection_first_jet
#print axioms pullback_connection_smooth
#print axioms pullback_connection_first_jet
#print axioms coordinate_curvature_finite_transformation
end
end ChatgptAudit.FiniteCoordinateCurvature
