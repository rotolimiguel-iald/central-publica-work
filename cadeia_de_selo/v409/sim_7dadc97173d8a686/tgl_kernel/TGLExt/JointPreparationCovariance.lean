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
import TGLExt.JointUnitaryPreparation
import TGLExt.CoherentScalarStress

set_option autoImplicit false
set_option maxHeartbeats 2800000
namespace ChatgptAudit.JointCovariance
open Matrix Set TGLExt ChatgptAudit.JointUnitary ChatgptAudit.Coherent023
noncomputable section

def frameMetric (E g : Tensor4) : Tensor4 := Eᵀ*g*E
def frameInverse (D gi : Tensor4) : Tensor4 := D*gi*Dᵀ
def frameCovectors {ι : Type} (E : Tensor4) (w : ι → Coordinate4) : ι → Coordinate4 :=
  fun j => Eᵀ *ᵥ w j

theorem frame_covectors_identity {ι : Type} (w : ι → Coordinate4) :
    frameCovectors 1 w=w := by
  funext j
  simp [frameCovectors]

theorem frame_covectors_composition {ι : Type} (E F : Tensor4) (w : ι → Coordinate4) :
    frameCovectors F (frameCovectors E w)=frameCovectors (E*F) w := by
  funext j
  simp only [frameCovectors, Matrix.mulVec_mulVec, Matrix.transpose_mul]

theorem frame_covectors_recovered {ι : Type} (E D : Tensor4) (hED : E*D=1)
    (w : ι → Coordinate4) : frameCovectors D (frameCovectors E w)=w := by
  rw [frame_covectors_composition, hED, frame_covectors_identity]

theorem transported_frequency {ι : Type} (E : Tensor4) (w : ι → Coordinate4)
    (d : Coordinate4) (j : ι) :
    covectorRead (frameCovectors E w j) d=covectorRead (w j) (E *ᵥ d) :=
  covector_read_change_basis E (w j) d

theorem transported_null_direction (E g : Tensor4) (d : Coordinate4) :
    tensorQuad (frameMetric E g) d=0 ↔ tensorQuad g (E *ᵥ d)=0 := by
  rw [frameMetric, tensorQuad_congruence]

theorem transported_inverse_is_inverse (E D g gi : Tensor4)
    (hED : E*D=1) (hDE : D*E=1) (hgi : gi*g=1) :
    frameInverse D gi * frameMetric E g=1 := by
  unfold frameInverse frameMetric
  have ht : Dᵀ*Eᵀ=1 := by rw [← Matrix.transpose_mul, hED, Matrix.transpose_one]
  calc
    (D*gi*Dᵀ)*(Eᵀ*g*E)=D*gi*(Dᵀ*Eᵀ)*g*E := by noncomm_ring
    _ = 1 := by rw [ht, mul_one, mul_assoc D gi g, hgi, mul_one, hDE]

theorem transported_inverse_quad (E D gi : Tensor4) (hED : E*D=1) (w : Coordinate4) :
    tensorQuad (frameInverse D gi) (Eᵀ *ᵥ w)=tensorQuad gi w := by
  have he : frameInverse D gi=(Dᵀ)ᵀ*gi*Dᵀ := by simp [frameInverse]
  rw [he, tensorQuad_congruence, Matrix.mulVec_mulVec, ← Matrix.transpose_mul,
    hED, Matrix.transpose_one, Matrix.one_mulVec]

theorem transported_covector_stress (E D g gi : Tensor4) (hED : E*D=1)
    (w : Coordinate4) (coupling : ℝ) :
    covectorStress (frameMetric E g) (frameInverse D gi) (Eᵀ *ᵥ w) coupling =
      Eᵀ * covectorStress g gi w coupling * E := by
  simp only [covectorStress, transported_inverse_quad E D gi hED w,
    outer_tensor_change_basis, frameMetric, Matrix.mul_smul, Matrix.smul_mul,
    Matrix.mul_sub, Matrix.sub_mul]

variable {ι : Type} [Fintype ι]

theorem transported_finite_source (E D g gi : Tensor4) (hED : E*D=1)
    (w : ι → Coordinate4) (weight coupling : ι → ℝ) :
    (∑ j, weight j • covectorStress (frameMetric E g) (frameInverse D gi)
      (frameCovectors E w j) (coupling j)) =
      Eᵀ * (∑ j, weight j • covectorStress g gi (w j) (coupling j)) * E := by
  simp only [frameCovectors, transported_covector_stress E D g gi hED,
    Matrix.mul_sum, Matrix.sum_mul, Matrix.mul_smul, Matrix.smul_mul]

theorem joint_curve_frame_covariance (C : UnitaryLabelData ι) (E : Tensor4)
    (w : ι → Coordinate4) (d : Coordinate4) :
    jointCovectorCurve C (frameCovectors E w) d=jointCovectorCurve C w (E *ᵥ d) := by
  unfold jointCovectorCurve
  congr 1
  funext j
  exact transported_frequency E w d j

theorem joint_weights_frame_covariance (C : UnitaryLabelData ι) (E : Tensor4)
    (w : ι → Coordinate4) (d : Coordinate4) (t : ℝ) :
    (jointCovectorCurve C (frameCovectors E w) d).weights t =
      (jointCovectorCurve C w (E *ᵥ d)).weights t := by
  rw [joint_curve_frame_covariance]

theorem joint_response_frame_covariance (C : UnitaryLabelData ι) (E : Tensor4)
    (w : ι → Coordinate4) (d : Coordinate4) :
    jointResponse C (fun j => covectorRead (frameCovectors E w j) d) =
      jointResponse C (fun j => covectorRead (w j) (E *ᵥ d)) := by
  congr 1
  funext j
  exact transported_frequency E w d j

theorem joint_flow_frame_covariance [DecidableEq ι] (C : UnitaryLabelData ι)
    (E : Tensor4) (w : ι → Coordinate4) (d : Coordinate4) (t : ℝ) :
    jointBlockFlow C (fun j => covectorRead (frameCovectors E w j) d) t =
      jointBlockFlow C (fun j => covectorRead (w j) (E *ᵥ d)) t := by
  congr 1
  funext j
  exact transported_frequency E w d j

theorem joint_amplitude_frame_covariance (C : UnitaryLabelData ι)
    (E : Tensor4) (w : ι → Coordinate4) (d : Coordinate4) (t : ℝ) :
    jointBlockAmplitude C (fun j => covectorRead (frameCovectors E w j) d) t =
      jointBlockAmplitude C (fun j => covectorRead (w j) (E *ᵥ d)) t := by
  congr 1
  funext j
  exact transported_frequency E w d j

#print axioms frameMetric
#print axioms frameInverse
#print axioms frameCovectors
#print axioms frame_covectors_identity
#print axioms frame_covectors_composition
#print axioms frame_covectors_recovered
#print axioms transported_frequency
#print axioms transported_null_direction
#print axioms transported_inverse_is_inverse
#print axioms transported_inverse_quad
#print axioms transported_covector_stress
#print axioms transported_finite_source
#print axioms joint_curve_frame_covariance
#print axioms joint_weights_frame_covariance
#print axioms joint_response_frame_covariance
#print axioms joint_flow_frame_covariance
#print axioms joint_amplitude_frame_covariance
end
end ChatgptAudit.JointCovariance
