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
import TGLExt.NonintegrablePotential
import TGLExt.SummableGravityControls

set_option autoImplicit false

namespace ChatgptAudit.Completion042
open Matrix Filter Topology Set TGLExt ChatgptAudit.Coherent023 ChatgptAudit.Response028
open scoped ContDiff
noncomputable section

/-- Realization of the already computed summable response on the chosen flat
background. The field w and the background remain inputs. -/
def HasSummableNullRealization (U : Set Coordinate4) (w : CovectorField4)
    (b : SummableAmplitude) : Prop :=
  ∃ T : TensorField4, SmoothMatrixOn U T ∧
    (∀ x ∈ U, (T x)ᵀ = T x) ∧
    (∀ x ∈ U, ∀ d, tensorQuad eta4 d = 0 →
      amplitudeResponse b (covectorRead (w x) d) = -Real.pi * tensorQuad (T x) d) ∧
    (∀ x ∈ U, ∀ j, tensorFieldDivergence flatMetric flatConnection T x j = 0)

/-- The conversion factor is fixed by the existing summable response. -/
theorem amplitude_response_null_value_iff (b : SummableAmplitude) (frequency value : ℝ) :
    amplitudeResponse b frequency = -Real.pi * value ↔
      value = amplitudeCoupling b * frequency^2 := by
  have he : amplitudeResponse b frequency =
      -Real.pi * (amplitudeCoupling b * frequency^2) := by
    unfold amplitudeResponse amplitudeCoupling
    field_simp [Real.pi_ne_zero]
  rw [he]
  constructor
  · intro h
    exact (mul_left_cancel₀ (neg_ne_zero.mpr Real.pi_ne_zero) h).symm
  · intro h
    rw [h]

theorem summable_coupling_positive (b : SummableAmplitude) (hb : 0 < amplitudeMass b) :
    0 < amplitudeCoupling b := by
  unfold amplitudeCoupling
  exact div_pos (mul_pos (Real.log_pos (by norm_num : (1 : ℝ) < 2)) hb) Real.pi_pos

theorem summable_null_realization_iff (U : Set Coordinate4) (w : CovectorField4)
    (b : SummableAmplitude) :
    HasSummableNullRealization U w b ↔
      HasConservedNullRealization U w (amplitudeCoupling b) := by
  constructor
  · rintro ⟨T,hT,hs,hn,hdiv⟩
    refine ⟨T,hT,hs,?_,hdiv⟩
    intro x hx d hd
    exact (amplitude_response_null_value_iff b (covectorRead (w x) d)
      (tensorQuad (T x) d)).1 (hn x hx d hd)
  · rintro ⟨T,hT,hs,hn,hdiv⟩
    refine ⟨T,hT,hs,?_,hdiv⟩
    intro x hx d hd
    exact (amplitude_response_null_value_iff b (covectorRead (w x) d)
      (tensorQuad (T x) d)).2 (hn x hx d hd)

theorem summable_null_realization_iff_potential (U : Set Coordinate4) (hU : IsOpen U)
    (w : CovectorField4) (b : SummableAmplitude)
    (hw : SmoothVectorOn U w) (hclosed : ClosedCovectorOn U w) :
    HasSummableNullRealization U w b ↔
      ∃ f : Coordinate4 → ℝ, ContDiffOn ℝ ∞ f U ∧
        ∀ x ∈ U, ∀ j, coordinatePartial f x j =
          -flatForce w (amplitudeCoupling b) x j :=
  (summable_null_realization_iff U w b).trans
    (conserved_null_realization_iff_potential U hU w (amplitudeCoupling b) hw hclosed)

/-- Every smooth symmetric conserved candidate is excluded, including all
variable traces, for this field on a neighborhood of mixedPoint. -/
theorem mixed_no_summable_null_realization (U : Set Coordinate4) (hU : IsOpen U)
    (hpoint : mixedPoint ∈ U) (b : SummableAmplitude) (hb : 0 < amplitudeMass b) :
    ¬ HasSummableNullRealization U mixedCovector b := by
  intro h
  exact mixed_no_conserved_null_response U hU hpoint (amplitudeCoupling b)
    (ne_of_gt (summable_coupling_positive b hb))
    ((summable_null_realization_iff U mixedCovector b).1 h)

/-- The limiting coefficient is identified by the established entropy theorem,
not by defining entropy in terms of a candidate tensor. -/
theorem summable_entropy_limit_iff_response (b : SummableAmplitude) (frequency value : ℝ) :
    Tendsto (fun t => amplitudeEntropyIncrement b (frequency*t) / t^2)
      (𝓝[<] 0) (𝓝 (-Real.pi * value)) ↔
        amplitudeResponse b frequency = -Real.pi * value := by
  constructor
  · intro h
    exact tendsto_nhds_unique (amplitude_entropy_quadratic_limit b frequency) h
  · intro h
    rw [← h]
    exact amplitude_entropy_quadratic_limit b frequency

/-- The obstruction stated directly for the actual summable entropy limits. -/
theorem mixed_no_summable_entropy_limit (U : Set Coordinate4) (hU : IsOpen U)
    (hpoint : mixedPoint ∈ U) (b : SummableAmplitude) (hb : 0 < amplitudeMass b) :
    ¬ ∃ T : TensorField4, SmoothMatrixOn U T ∧
      (∀ x ∈ U, (T x)ᵀ = T x) ∧
      (∀ x ∈ U, ∀ d, tensorQuad eta4 d = 0 →
        Tendsto (fun t => amplitudeEntropyIncrement b
          (covectorRead (mixedCovector x) d * t) / t^2)
          (𝓝[<] 0) (𝓝 (-Real.pi * tensorQuad (T x) d))) ∧
      (∀ x ∈ U, ∀ j, tensorFieldDivergence flatMetric flatConnection T x j = 0) := by
  rintro ⟨T,hT,hs,hlimit,hdiv⟩
  apply mixed_no_summable_null_realization U hU hpoint b hb
  refine ⟨T,hT,hs,?_,hdiv⟩
  intro x hx d hd
  exact (summable_entropy_limit_iff_response b (covectorRead (mixedCovector x) d)
    (tensorQuad (T x) d)).1 (hlimit x hx d hd)

/-- A nonzero summable profile already present in the library witnesses the
nonvacuous amplitude regime of the obstruction. -/
theorem mixed_geometric_no_summable_realization (U : Set Coordinate4)
    (hU : IsOpen U) (hpoint : mixedPoint ∈ U) :
    ¬ HasSummableNullRealization U mixedCovector geometricAmplitude := by
  apply mixed_no_summable_null_realization U hU hpoint geometricAmplitude
  rw [geometric_amplitude_mass]
  norm_num

theorem growing_summable_null_response (b : SummableAmplitude) (x d : Coordinate4)
    (hd : tensorQuad eta4 d = 0) :
    amplitudeResponse b (covectorRead (growingTimeCovector x) d) =
      -Real.pi * tensorQuad
        (traceCompletedStress growingTimeCovector (amplitudeCoupling b)
          (growingTraceCorrection (amplitudeCoupling b)) x) d :=
  (amplitude_response_null_value_iff b (covectorRead (growingTimeCovector x) d) _).2
    (growing_trace_completed_null_response (amplitudeCoupling b) x d hd)

/-- The growing field has an explicit conserved completion for every summable
amplitude; its uncompleted representative alone was not conserved. -/
theorem growing_summable_null_realization (b : SummableAmplitude) :
    HasSummableNullRealization univ growingTimeCovector b := by
  refine ⟨traceCompletedStress growingTimeCovector (amplitudeCoupling b)
    (growingTraceCorrection (amplitudeCoupling b)),
    trace_completed_smooth univ growingTimeCovector (amplitudeCoupling b)
      (growingTraceCorrection (amplitudeCoupling b)) growing_time_smooth
      (growing_trace_correction_smooth (amplitudeCoupling b)),?_,?_,
    growing_trace_completed_conserved (amplitudeCoupling b)⟩
  · intro x _
    exact trace_completed_symmetric growingTimeCovector (amplitudeCoupling b)
      (growingTraceCorrection (amplitudeCoupling b)) x
  · intro x _ d hd
    exact growing_summable_null_response b x d hd

/-- The zero response is realized by the zero tensor for every supplied field,
without any regularity assumption on that field. -/
theorem zero_amplitude_summable_null_realization (U : Set Coordinate4) (w : CovectorField4) :
    HasSummableNullRealization U w zeroAmplitude := by
  refine ⟨(fun _ => 0),?_,?_,?_,?_⟩
  · exact fun _ _ => contDiffOn_const
  · intro x _
    exact Matrix.transpose_zero
  · intro x _ d _
    rw [zero_amplitude_response]
    simp [tensorQuad]
  · intro x _ j
    simp [tensorFieldDivergence, tensorJetDivergence, covariantTensorJet,
      tensorFieldJet, coordinatePartial]

#print axioms HasSummableNullRealization
#print axioms amplitude_response_null_value_iff
#print axioms summable_coupling_positive
#print axioms summable_null_realization_iff
#print axioms summable_null_realization_iff_potential
#print axioms mixed_no_summable_null_realization
#print axioms summable_entropy_limit_iff_response
#print axioms mixed_no_summable_entropy_limit
#print axioms mixed_geometric_no_summable_realization
#print axioms growing_summable_null_response
#print axioms growing_summable_null_realization
#print axioms zero_amplitude_summable_null_realization

end
end ChatgptAudit.Completion042
