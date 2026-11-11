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
import TGLExt.GeneralMetricEinstein
import TGLExt.CoherentScalarStress

set_option autoImplicit false
set_option maxHeartbeats 3500000
namespace ChatgptAudit.SignedCoverage
open Matrix Set TGLExt ChatgptAudit.GeneralMetric ChatgptAudit.Coherent023
open scoped ContDiff
noncomputable section

def traceReverse (g gi A : Tensor4) : Tensor4 :=
  A - (Matrix.trace (gi * A) / 2) • g

def plusCovector (A : Tensor4) (i : Fin 4) : Coordinate4 :=
  fun j => (A i j + if i = j then 1 else 0) / 2

def minusCovector (A : Tensor4) (i : Fin 4) : Coordinate4 :=
  fun j => (A i j - if i = j then 1 else 0) / 2

theorem polarization_pair_entry (A : Tensor4) (i j k : Fin 4) :
    (Matrix.vecMulVec (plusCovector A i) (plusCovector A i) -
      Matrix.vecMulVec (minusCovector A i) (minusCovector A i)) j k =
    (A i j * (if i=k then 1 else 0) + (if i=j then 1 else 0) * A i k) / 2 := by
  simp only [Matrix.sub_apply, Matrix.vecMulVec, Matrix.of_apply, plusCovector, minusCovector]
  ring

theorem signed_polarization (A : Tensor4) (hs : Aᵀ=A) :
    (∑ i : Fin 4, (Matrix.vecMulVec (plusCovector A i) (plusCovector A i) -
      Matrix.vecMulVec (minusCovector A i) (minusCovector A i))) = A := by
  ext j k
  simp only [Matrix.sum_apply, polarization_pair_entry, add_div, Finset.sum_add_distrib]
  simp only [mul_ite, ite_mul, mul_one, mul_zero, one_mul, zero_mul]
  rw [← Finset.sum_div, ← Finset.sum_div]
  simp only [Finset.sum_ite_eq', Finset.mem_univ, if_true]
  have h := congrArg (fun M : Tensor4 => M j k) hs
  simp only [Matrix.transpose_apply] at h
  rw [h]
  ring

theorem trace_reverse_symmetric (g gi A : Tensor4) (hg : gᵀ=g) (hA : Aᵀ=A) :
    (traceReverse g gi A)ᵀ=traceReverse g gi A := by
  simp only [traceReverse, Matrix.transpose_sub, Matrix.transpose_smul, hg, hA]

theorem trace_reverse_add (g gi A B : Tensor4) :
    traceReverse g gi (A+B)=traceReverse g gi A+traceReverse g gi B := by
  simp only [traceReverse, Matrix.mul_add, Matrix.trace_add, add_div, add_smul]
  abel

theorem trace_reverse_sub (g gi A B : Tensor4) :
    traceReverse g gi (A-B)=traceReverse g gi A-traceReverse g gi B := by
  simp only [traceReverse, Matrix.mul_sub, Matrix.trace_sub, sub_div, sub_smul]
  abel

theorem trace_reverse_sum {ι : Type} [Fintype ι] (g gi : Tensor4) (A : ι → Tensor4) :
    traceReverse g gi (∑ i, A i)=∑ i, traceReverse g gi (A i) := by
  simp only [traceReverse, Matrix.mul_sum, Matrix.trace_sum, Finset.sum_div,
    Finset.sum_smul, Finset.sum_sub_distrib]

theorem trace_reverse_trace (g gi A : Tensor4) (hi : gi*g=1) :
    Matrix.trace (gi*traceReverse g gi A) = -Matrix.trace (gi*A) := by
  simp only [traceReverse, Matrix.mul_sub, Matrix.mul_smul, Matrix.trace_sub,
    Matrix.trace_smul, hi]
  norm_num
  ring

theorem trace_reverse_involutive (g gi A : Tensor4) (hi : gi*g=1) :
    traceReverse g gi (traceReverse g gi A)=A := by
  rw [traceReverse, trace_reverse_trace g gi A hi]
  simp only [traceReverse, neg_div, neg_smul]
  abel

theorem trace_outer_is_quad (gi : Tensor4) (w : Coordinate4) :
    Matrix.trace (gi*Matrix.vecMulVec w w)=tensorQuad gi w := by
  rw [Matrix.mul_vecMulVec, Matrix.trace_vecMulVec, dotProduct_comm]
  rfl

theorem trace_reverse_outer (g gi : Tensor4) (w : Coordinate4) :
    traceReverse g gi (Matrix.vecMulVec w w)=covectorStress g gi w 1 := by
  simp only [traceReverse, trace_outer_is_quad, covectorStress, one_smul]

theorem signed_pair_stress (g gi A : Tensor4) (i : Fin 4) :
    covectorStress g gi (plusCovector A i) 1 +
      covectorStress g gi (minusCovector A i) (-1) =
    traceReverse g gi (Matrix.vecMulVec (plusCovector A i) (plusCovector A i) -
      Matrix.vecMulVec (minusCovector A i) (minusCovector A i)) := by
  rw [trace_reverse_sub, trace_reverse_outer, trace_reverse_outer]
  simp only [covectorStress, one_smul, neg_one_smul, sub_eq_add_neg]

def signedStress (g gi A : Tensor4) : Tensor4 :=
  ∑ i : Fin 4, (covectorStress g gi (plusCovector A i) 1 +
    covectorStress g gi (minusCovector A i) (-1))

theorem signed_stress_is_trace_reverse (g gi A : Tensor4) (hA : Aᵀ=A) :
    signedStress g gi A=traceReverse g gi A := by
  unfold signedStress
  simp only [signed_pair_stress]
  rw [← trace_reverse_sum, signed_polarization A hA]

theorem every_symmetric_source_has_eight_covectors (g gi T : Tensor4)
    (hi : gi*g=1) (hg : gᵀ=g) (hT : Tᵀ=T) :
    signedStress g gi (traceReverse g gi T)=T := by
  rw [signed_stress_is_trace_reverse g gi _ (trace_reverse_symmetric g gi T hg hT),
    trace_reverse_involutive g gi T hi]

theorem plus_covector_smooth (U : Set Coordinate4) (A : TensorField4)
    (hA : SmoothMatrixOn U A) (i : Fin 4) :
    SmoothVectorOn U (fun x => plusCovector (A x) i) := by
  intro j
  exact ((hA i j).add contDiffOn_const).div_const 2

theorem minus_covector_smooth (U : Set Coordinate4) (A : TensorField4)
    (hA : SmoothMatrixOn U A) (i : Fin 4) :
    SmoothVectorOn U (fun x => minusCovector (A x) i) := by
  intro j
  exact ((hA i j).sub contDiffOn_const).div_const 2

theorem trace_reverse_field_smooth (U : Set Coordinate4) (g gi A : TensorField4)
    (hg : SmoothMatrixOn U g) (hgi : SmoothMatrixOn U gi) (hA : SmoothMatrixOn U A) :
    SmoothMatrixOn U (fun x => traceReverse (g x) (gi x) (A x)) := by
  have hprod := SmoothMatrixOn.mul U gi A hgi hA
  have hsum : ContDiffOn ℝ ∞ (fun x => ∑ i : Fin 4, (gi x*A x) i i) U := by
    apply ContDiffOn.sum
    intro i _
    exact hprod i i
  have ht : ContDiffOn ℝ ∞ (fun x => Matrix.trace (gi x*A x)/2) U := by
    simpa only [Matrix.trace, Matrix.diag] using hsum.div_const 2
  intro i j
  exact (hA i j).sub (ht.mul (hg i j))

theorem smooth_metric_source_has_smooth_eight_covectors
    (U : Set Coordinate4) (g T : TensorField4)
    (hg : SmoothMatrixOn U g) (hT : SmoothMatrixOn U T)
    (hLor : ∀ x∈U, LorentzByCongruence (g x)) :
    (∀ i, SmoothVectorOn U
      (fun x => plusCovector (traceReverse (g x) (metricInverse g x) (T x)) i)) ∧
    (∀ i, SmoothVectorOn U
      (fun x => minusCovector (traceReverse (g x) (metricInverse g x) (T x)) i)) := by
  have hf := trace_reverse_field_smooth U g (metricInverse g) T hg
    (constructed_metric_inverse_smooth U g hg hLor) hT
  exact ⟨fun i => plus_covector_smooth U _ hf i, fun i => minus_covector_smooth U _ hf i⟩

theorem every_smooth_lorentz_source_is_represented
    (U : Set Coordinate4) (g T : TensorField4)
    (hLor : ∀ x∈U, LorentzByCongruence (g x))
    (hT : ∀ x∈U, (T x)ᵀ=T x) :
    ∀ x∈U, signedStress (g x) (metricInverse g x)
      (traceReverse (g x) (metricInverse g x) (T x))=T x := by
  intro x hx
  exact every_symmetric_source_has_eight_covectors (g x) (metricInverse g x) (T x)
    (constructed_metric_inverse_left g x (hLor x hx))
    (lorentz_metric_symmetric (g x) (hLor x hx)) (hT x hx)

#print axioms traceReverse
#print axioms plusCovector
#print axioms minusCovector
#print axioms polarization_pair_entry
#print axioms signed_polarization
#print axioms trace_reverse_symmetric
#print axioms trace_reverse_add
#print axioms trace_reverse_sub
#print axioms trace_reverse_sum
#print axioms trace_reverse_trace
#print axioms trace_reverse_involutive
#print axioms trace_outer_is_quad
#print axioms trace_reverse_outer
#print axioms signed_pair_stress
#print axioms signedStress
#print axioms signed_stress_is_trace_reverse
#print axioms every_symmetric_source_has_eight_covectors
#print axioms plus_covector_smooth
#print axioms minus_covector_smooth
#print axioms trace_reverse_field_smooth
#print axioms smooth_metric_source_has_smooth_eight_covectors
#print axioms every_smooth_lorentz_source_is_represented
end
end ChatgptAudit.SignedCoverage
