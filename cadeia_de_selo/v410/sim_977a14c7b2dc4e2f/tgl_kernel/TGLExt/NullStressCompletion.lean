-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_042 (06/09/2026), transposta em 06/09/2026
-- Lote 042..043 (complementos a ORDEM_009; ORDEM_008 cumprida: zero instancias anonimas, lote compilado
--   junto em diretorio limpo). 042: COMPLETAMENTO CONSERVADO DA RESPOSTA NULA — criterio completo, na
--   familia e fundo plano fixados, para a resposta nula admitir fonte conservada: toda fonte suave simetrica
--   com T(d,d) = c[w(d)]^2 nos nulos e S + f g com S = c(w x w - g^{-1}(w,w) g/2); conservacao <=> df = -c(div w) w;
--   criterio = existencia de potencial suave; controle phi = t^2/2 admite; CONTRAEXEMPLO phi = t^2 x exclui toda
--   fonte conservada (inclusive traco variavel) num aberto. 043: TELA EFETIVA DE JACOBI e calor construido —
--   habitante explicito de EquilibriumScreenData so com (a,c) da metrica (perfis de Riccati; campo nulo,
--   geodesico, gradiente diag(0,q_a,q_c,0)); opticalScreenHeat = constructedHeat, igual a opticalHeat041 como
--   germe em t -> 0-; sem casamento: lim D/t^2 = kappa[eta(a+c) - 2 pi m]/(4 pi); com casamento: lim D/t^4 =
--   kappa eta (a^2+c^2)/(24 pi) > 0 — a igualdade finita exata FALHA, o balanco infinitesimal fica.
--   Estatuto [REAL / DERIVED / INPUT / OPEN]: familia especificada; L, area fisica, retorno estabilizador,
--   materia/geometria/normalizacao e reconstrucao geral OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 10/10 + 10/10; 2/2 auditores exit 0;
--   recompilacao INDEPENDENTE 8/8, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.ScalarStressConservation

set_option autoImplicit false

namespace ChatgptAudit.Completion042
open Matrix Filter Topology Set TGLExt ChatgptAudit.Coherent023
open scoped ContDiff
noncomputable section

/-- The fixed Minkowski metric, with signature +---. -/
def flatMetric : TensorField4 := fun _ => eta4

/-- The connection in the same inertial coordinates. -/
def flatConnection : ConnectionField4 := fun _ _ => 0

/-- The previously constructed scalar stress, on the fixed flat background. -/
def flatCovectorStress (w : CovectorField4) (coupling : ℝ) : TensorField4 :=
  covectorStressField flatMetric flatMetric w coupling

/-- A variable metric multiple is invisible to every null quadratic reading. -/
def traceCompletedStress (w : CovectorField4) (coupling : ℝ)
    (f : Coordinate4 → ℝ) : TensorField4 :=
  fun x => flatCovectorStress w coupling x + f x • eta4

/-- The coefficient is extracted from the actual candidate tensor. -/
def traceCompletion (w : CovectorField4) (coupling : ℝ)
    (T : TensorField4) (x : Coordinate4) : ℝ :=
  (T x - flatCovectorStress w coupling x) 0 0

theorem flat_metric_smooth (U : Set Coordinate4) : SmoothMatrixOn U flatMetric :=
  fun _ _ => contDiffOn_const

theorem flat_metric_inverse (x : Coordinate4) : flatMetric x * flatMetric x = 1 :=
  eta4_mul_self

theorem flat_metric_compatible (x : Coordinate4) :
    ∀ i, covariantTensorJet (flatMetric x) (tensorFieldJet flatMetric x)
      (flatConnection x) i = 0 := by
  intro i
  ext j k
  simp [flatMetric, flatConnection, covariantTensorJet, tensorFieldJet, coordinatePartial]

theorem flat_covector_derivative (w : CovectorField4) (x : Coordinate4)
    (i j : Fin 4) :
    covectorDerivative flatConnection w x i j =
      coordinatePartial (fun y => w y j) x i := by
  simp [covectorDerivative, flatConnection, vectorPartial]

theorem flat_stress_smooth (U : Set Coordinate4) (w : CovectorField4) (coupling : ℝ)
    (hw : SmoothVectorOn U w) : SmoothMatrixOn U (flatCovectorStress w coupling) :=
  covector_stress_field_smooth U flatMetric flatMetric w coupling
    (flat_metric_smooth U) (flat_metric_smooth U) hw

theorem flat_stress_symmetric (w : CovectorField4) (coupling : ℝ) (x : Coordinate4) :
    (flatCovectorStress w coupling x)ᵀ = flatCovectorStress w coupling x :=
  covector_stress_symmetric (flatMetric x) (flatMetric x) (w x) coupling eta4_symm

theorem flat_stress_null (w : CovectorField4) (coupling : ℝ) (x d : Coordinate4)
    (hd : tensorQuad eta4 d = 0) :
    tensorQuad (flatCovectorStress w coupling x) d =
      coupling * (covectorRead (w x) d)^2 :=
  covector_stress_null (flatMetric x) (flatMetric x) (w x) d coupling hd

theorem trace_completed_smooth (U : Set Coordinate4) (w : CovectorField4)
    (coupling : ℝ) (f : Coordinate4 → ℝ) (hw : SmoothVectorOn U w)
    (hf : ContDiffOn ℝ ∞ f U) :
    SmoothMatrixOn U (traceCompletedStress w coupling f) := by
  intro i j
  change ContDiffOn ℝ ∞
    (fun x => flatCovectorStress w coupling x i j + f x * eta4 i j) U
  exact (flat_stress_smooth U w coupling hw i j).add (hf.mul contDiffOn_const)

theorem trace_completed_symmetric (w : CovectorField4) (coupling : ℝ)
    (f : Coordinate4 → ℝ) (x : Coordinate4) :
    (traceCompletedStress w coupling f x)ᵀ = traceCompletedStress w coupling f x := by
  simp only [traceCompletedStress, Matrix.transpose_add, Matrix.transpose_smul,
    flat_stress_symmetric, eta4_symm]

theorem trace_completed_null (w : CovectorField4) (coupling : ℝ)
    (f : Coordinate4 → ℝ) (x d : Coordinate4) (hd : tensorQuad eta4 d = 0) :
    tensorQuad (traceCompletedStress w coupling f x) d =
      coupling * (covectorRead (w x) d)^2 := by
  have he : traceCompletedStress w coupling f x =
      flatCovectorStress w coupling x - (-f x) • eta4 := by
    simp [traceCompletedStress]
  rw [he, tensorQuad_sub_smul, flat_stress_null w coupling x d hd,
    hd, mul_zero, sub_zero]

/-- Algebraic classification; conservation is not assumed for either tensor. -/
theorem null_stress_classification (w : CovectorField4) (coupling : ℝ)
    (T : TensorField4) (x : Coordinate4) (hs : (T x)ᵀ = T x)
    (hn : ∀ d, tensorQuad eta4 d = 0 →
      tensorQuad (T x) d = coupling * (covectorRead (w x) d)^2) :
    T x = traceCompletedStress w coupling (traceCompletion w coupling T) x := by
  have hsDiff : (T x - flatCovectorStress w coupling x)ᵀ =
      T x - flatCovectorStress w coupling x := by
    rw [Matrix.transpose_sub, hs, flat_stress_symmetric]
  have hnDiff : ∀ d, tensorQuad eta4 d = 0 →
      tensorQuad (T x - flatCovectorStress w coupling x) d = 0 := by
    intro d hd
    have hq := tensorQuad_sub_smul (T x) (flatCovectorStress w coupling x) 1 d
    simp only [one_smul, one_mul] at hq
    rw [hq, hn d hd, flat_stress_null w coupling x d hd, sub_self]
  have he := minkowski_tensor_null_rigidity
    (T x - flatCovectorStress w coupling x) hsDiff hnDiff
  change T x - flatCovectorStress w coupling x =
    traceCompletion w coupling T x • eta4 at he
  change T x = flatCovectorStress w coupling x + traceCompletion w coupling T x • eta4
  rw [← he]
  abel

theorem trace_completion_smooth (U : Set Coordinate4) (w : CovectorField4)
    (coupling : ℝ) (T : TensorField4) (hw : SmoothVectorOn U w)
    (hT : SmoothMatrixOn U T) :
    ContDiffOn ℝ ∞ (traceCompletion w coupling T) U := by
  change ContDiffOn ℝ ∞
    (fun x => T x 0 0 - flatCovectorStress w coupling x 0 0) U
  exact (hT 0 0).sub (flat_stress_smooth U w coupling hw 0 0)

/-- Closedness of w, without imposing the wave equation. -/
theorem flat_stress_divergence (U : Set Coordinate4) (hU : IsOpen U)
    (w : CovectorField4) (coupling : ℝ) (hw : SmoothVectorOn U w)
    (hclosed : ClosedCovectorOn U w) (x : Coordinate4) (hx : x ∈ U) (j : Fin 4) :
    tensorFieldDivergence flatMetric flatConnection (flatCovectorStress w coupling) x j =
      coupling * (covectorDivergence flatMetric flatConnection w x * w x j) := by
  have hg : ∀ i k, DifferentiableAt ℝ (fun y => flatMetric y i k) x :=
    fun _ _ => differentiableAt_const _
  have hd : ∀ i, tensorFieldJet flatMetric x i =
      -flatConnection x i * flatMetric x - flatMetric x * (flatConnection x i)ᵀ := by
    intro i
    ext k l
    simp [flatMetric, flatConnection, tensorFieldJet, coordinatePartial]
  have hW : ∀ i k, covectorDerivative flatConnection w x i k =
      covectorDerivative flatConnection w x k i := by
    intro i k
    rw [flat_covector_derivative, flat_covector_derivative]
    exact hclosed x hx i k
  exact covector_stress_divergence_closed flatMetric flatMetric flatConnection w coupling x
    hg hg (smooth_vector_differentiableAt U hU w hw x hx)
    (flat_metric_inverse x) eta4_symm (flat_metric_compatible x) hd hW j

/-- The free trace contributes its actual gradient to conservation. -/
theorem trace_completed_divergence (U : Set Coordinate4) (hU : IsOpen U)
    (w : CovectorField4) (coupling : ℝ) (f : Coordinate4 → ℝ)
    (hw : SmoothVectorOn U w) (hclosed : ClosedCovectorOn U w)
    (hf : ContDiffOn ℝ ∞ f U) (x : Coordinate4) (hx : x ∈ U) (j : Fin 4) :
    tensorFieldDivergence flatMetric flatConnection (traceCompletedStress w coupling f) x j =
      coupling * (covectorDivergence flatMetric flatConnection w x * w x j) +
        coordinatePartial f x j := by
  have hfAt : DifferentiableAt ℝ f x :=
    (hf.differentiableOn (by simp)).differentiableAt (hU.mem_nhds hx)
  have hg : ∀ i k, DifferentiableAt ℝ (fun y => flatMetric y i k) x :=
    fun _ _ => differentiableAt_const _
  have hS : ∀ i k, DifferentiableAt ℝ
      (fun y => flatCovectorStress w coupling y i k) x :=
    smooth_matrix_differentiableAt U hU (flatCovectorStress w coupling)
      (flat_stress_smooth U w coupling hw) x hx
  have hnegTrace : ∀ i k, DifferentiableAt ℝ
      (fun y => ((-f y) • flatMetric y) i k) x := by
    intro i k
    exact hfAt.neg.mul (hg i k)
  have he : traceCompletedStress w coupling f =
      (fun y => flatCovectorStress w coupling y - (-f y) • flatMetric y) := by
    funext y
    simp [traceCompletedStress, flatMetric]
  rw [he, tensorFieldDivergence_sub flatMetric flatConnection
    (flatCovectorStress w coupling) (fun y => (-f y) • flatMetric y) x hS hnegTrace j,
    flat_stress_divergence U hU w coupling hw hclosed x hx j,
    pure_trace_field_divergence flatMetric flatMetric flatConnection (fun y => -f y)
      x hfAt.neg hg (flat_metric_inverse x) (flat_metric_compatible x) j]
  have hneg : coordinatePartial (fun y => -f y) x j = -coordinatePartial f x j := by
    simp [coordinatePartial]
  rw [hneg, sub_neg_eq_add]

#print axioms flatMetric
#print axioms flatConnection
#print axioms flatCovectorStress
#print axioms traceCompletedStress
#print axioms traceCompletion
#print axioms flat_metric_smooth
#print axioms flat_metric_inverse
#print axioms flat_metric_compatible
#print axioms flat_covector_derivative
#print axioms flat_stress_smooth
#print axioms flat_stress_symmetric
#print axioms flat_stress_null
#print axioms trace_completed_smooth
#print axioms trace_completed_symmetric
#print axioms trace_completed_null
#print axioms null_stress_classification
#print axioms trace_completion_smooth
#print axioms flat_stress_divergence
#print axioms trace_completed_divergence

end
end ChatgptAudit.Completion042
