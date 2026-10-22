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
import TGLExt.ConservativeNullResponse
import TGLExt.CoherentMatterControls

set_option autoImplicit false
set_option maxHeartbeats 12000000
set_option maxRecDepth 4096

namespace ChatgptAudit.Completion042
open Matrix Filter Topology Set TGLExt ChatgptAudit ChatgptAudit.Coherent023
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

/-- A smooth potential whose induced null response has no conserved completion
near the specified point in the fixed flat geometry. -/
def mixedPotential (x : Coordinate4) : ℝ := (x 0)^2*x 1

def mixedCovector (x : Coordinate4) : Coordinate4 := ![2*x 0*x 1,(x 0)^2,0,0]

def mixedPoint : Coordinate4 := ![1,1,0,0]

theorem mixed_potential_smooth : ContDiffOn ℝ ∞ mixedPotential univ := by
  unfold mixedPotential
  fun_prop

theorem mixed_covector_smooth : SmoothVectorOn univ mixedCovector := by
  intro j
  fin_cases j <;> dsimp [mixedCovector] <;> fun_prop

theorem mixed_potential_covector : potentialCovector mixedPotential=mixedCovector := by
  funext x i
  have hf := ((hasFDerivAt_apply (𝕜 := ℝ) 0 x).pow 2).mul
    (hasFDerivAt_apply (𝕜 := ℝ) 1 x)
  change HasFDerivAt (fun y : Coordinate4 => (y 0)^2*y 1) _ x at hf
  change fderiv ℝ (fun y : Coordinate4 => (y 0)^2*y 1) x (Pi.single i 1)=_
  rw [hf.fderiv]
  fin_cases i <;>
    simp [mixedCovector,ContinuousLinearMap.proj_apply,mul_comm,mul_assoc]

theorem mixed_covector_closed : ClosedCovectorOn univ mixedCovector := by
  rw [← mixed_potential_covector]
  exact potential_covector_closed univ isOpen_univ mixedPotential mixed_potential_smooth

theorem mixed_covector_partial (x : Coordinate4) (i j : Fin 4) :
    coordinatePartial (fun y => mixedCovector y j) x i=
      if j=0 then
        2*x 1*(if i=0 then 1 else 0)+2*x 0*(if i=1 then 1 else 0)
      else if j=1 then 2*x 0*(if i=0 then 1 else 0)
      else 0 := by
  fin_cases j
  · have hf := ((hasFDerivAt_apply (𝕜 := ℝ) 0 x).const_mul 2).mul
      (hasFDerivAt_apply (𝕜 := ℝ) 1 x)
    change HasFDerivAt (fun y : Coordinate4 => 2*y 0*y 1) _ x at hf
    change fderiv ℝ (fun y : Coordinate4 => 2*y 0*y 1) x (Pi.single i 1)=_
    rw [hf.fderiv]
    fin_cases i <;>
      simp [ContinuousLinearMap.proj_apply,mul_comm]
  · have hf := (hasFDerivAt_apply (𝕜 := ℝ) 0 x).pow 2
    change fderiv ℝ (fun y : Coordinate4 => (y 0)^2) x (Pi.single i 1)=_
    rw [hf.fderiv]
    fin_cases i <;>
      simp [ContinuousLinearMap.proj_apply]
  · change fderiv ℝ (fun _ : Coordinate4 => (0:ℝ)) x (Pi.single i 1)=_
    norm_num
  · change fderiv ℝ (fun _ : Coordinate4 => (0:ℝ)) x (Pi.single i 1)=_
    norm_num

theorem mixed_covector_divergence (x : Coordinate4) :
    covectorDivergence flatMetric flatConnection mixedCovector x=2*x 1 := by
  unfold covectorDivergence
  simp only [Fin.sum_univ_four]
  norm_num [flatMetric,eta4,flat_covector_derivative,mixed_covector_partial,
    Matrix.diagonal_apply,Matrix.cons_val_two,Matrix.cons_val_three,Fin.isValue]
  have h20 : (2 : Fin 4)≠0 := by decide
  have h21 : (2 : Fin 4)≠1 := by decide
  have h30 : (3 : Fin 4)≠0 := by decide
  have h31 : (3 : Fin 4)≠1 := by decide
  simp only [h20,h21,h30,h31,if_false,add_zero]

theorem mixed_force_formula (c : ℝ) (x : Coordinate4) :
    flatForce mixedCovector c x=![4*c*x 0*(x 1)^2,2*c*(x 0)^2*x 1,0,0] := by
  ext j
  simp only [flatForce,mixed_covector_divergence]
  fin_cases j <;> dsimp [mixedCovector] <;> ring

theorem mixed_force_partial_one_zero (c : ℝ) (x : Coordinate4) :
    coordinatePartial (fun y => flatForce mixedCovector c y 0) x 1=8*c*x 0*x 1 := by
  have he : (fun y => flatForce mixedCovector c y 0)=
      (fun y : Coordinate4 => 4*c*y 0*(y 1)^2) := by
    funext y
    rw [mixed_force_formula]
    rfl
  rw [he]
  have hf := ((hasFDerivAt_apply (𝕜 := ℝ) 0 x).const_mul (4*c)).mul
    ((hasFDerivAt_apply (𝕜 := ℝ) 1 x).pow 2)
  change HasFDerivAt (fun y : Coordinate4 => 4*c*y 0*(y 1)^2) _ x at hf
  unfold coordinatePartial
  rw [hf.fderiv]
  norm_num [ContinuousLinearMap.proj_apply,Pi.single_apply]
  ring

theorem mixed_force_partial_zero_one (c : ℝ) (x : Coordinate4) :
    coordinatePartial (fun y => flatForce mixedCovector c y 1) x 0=4*c*x 0*x 1 := by
  have he : (fun y => flatForce mixedCovector c y 1)=
      (fun y : Coordinate4 => 2*c*(y 0)^2*y 1) := by
    funext y
    rw [mixed_force_formula]
    rfl
  rw [he]
  have hf := (((hasFDerivAt_apply (𝕜 := ℝ) 0 x).pow 2).const_mul (2*c)).mul
    (hasFDerivAt_apply (𝕜 := ℝ) 1 x)
  change HasFDerivAt (fun y : Coordinate4 => 2*c*(y 0)^2*y 1) _ x at hf
  unfold coordinatePartial
  rw [hf.fderiv]
  norm_num [ContinuousLinearMap.proj_apply,Pi.single_apply]
  ring

/-- This is the (1,0) antisymmetric partial difference. The (0,1)
component has the opposite sign and the same nonvanishing obstruction. -/
theorem mixed_force_curl (c : ℝ) (x : Coordinate4) :
    coordinatePartial (fun y => flatForce mixedCovector c y 0) x 1-
      coordinatePartial (fun y => flatForce mixedCovector c y 1) x 0=
        4*c*x 0*x 1 := by
  rw [mixed_force_partial_one_zero,mixed_force_partial_zero_one]
  ring

theorem mixed_force_not_closed (U : Set Coordinate4) (hpoint : mixedPoint∈U)
    (c : ℝ) (hc : c≠0) : ¬ClosedCovectorOn U (flatForce mixedCovector c) := by
  intro hclosed
  have hh := hclosed mixedPoint hpoint 1 0
  rw [mixed_force_partial_one_zero,mixed_force_partial_zero_one] at hh
  norm_num [mixedPoint] at hh
  exact hc (by linarith)

/-- No smooth symmetric conserved tensor realizes this response on every null
direction in any open neighborhood of mixedPoint. The conclusion allows all
variable trace completions; the background metric remains fixed. -/
theorem mixed_no_conserved_null_response (U : Set Coordinate4) (hU : IsOpen U)
    (hpoint : mixedPoint∈U) (c : ℝ) (hc : c≠0) :
    ¬∃ T : TensorField4,
      SmoothMatrixOn U T ∧
      (∀ x∈U, (T x)ᵀ=T x) ∧
      (∀ x∈U, ∀ d, tensorQuad eta4 d=0 →
        tensorQuad (T x) d=c*(covectorRead (mixedCovector x) d)^2) ∧
      (∀ x∈U, ∀ j, tensorFieldDivergence flatMetric flatConnection T x j=0) := by
  rintro ⟨T,hT,hs,hn,hdiv⟩
  have hw : SmoothVectorOn U mixedCovector := by
    intro j
    exact (mixed_covector_smooth j).mono (subset_univ U)
  have hclosed : ClosedCovectorOn U mixedCovector :=
    fun x _ => mixed_covector_closed x (mem_univ x)
  exact mixed_force_not_closed U hpoint c hc
    (conserved_null_response_closed_force U hU mixedCovector c T hw hclosed hT hs hn hdiv)

/-- A variable trace repairs the older growing-potential control without changing
its null response. This does not assert any entropy-area equality. -/
def growingTraceCorrection (c : ℝ) (x : Coordinate4) : ℝ := -c*growingPotential x

theorem growing_trace_correction_smooth (c : ℝ) :
    ContDiffOn ℝ ∞ (growingTraceCorrection c) univ := by
  unfold growingTraceCorrection growingPotential
  fun_prop

theorem growing_flat_divergence (x : Coordinate4) :
    covectorDivergence flatMetric flatConnection growingTimeCovector x=1 := by
  unfold covectorDivergence
  simp only [Fin.sum_univ_four]
  norm_num [flatMetric,eta4,flat_covector_derivative,growing_time_partial,
    timeCovector,Matrix.diagonal_apply,Matrix.cons_val_two,Matrix.cons_val_three,Fin.isValue]

theorem growing_flat_force (c : ℝ) (x : Coordinate4) (j : Fin 4) :
    flatForce growingTimeCovector c x j=c*x 0*timeCovector j := by
  rw [flatForce,growing_flat_divergence]
  change c*(1*(x 0*timeCovector j))=_
  ring

theorem growing_trace_gradient (c : ℝ) (x : Coordinate4) (j : Fin 4) :
    coordinatePartial (growingTraceCorrection c) x j=
      -flatForce growingTimeCovector c x j := by
  change coordinatePartial (fun y : Coordinate4 => (-c)*growingPotential y) x j=_
  rw [coordinatePartial_mul _ _ x (differentiableAt_const (-c))
    (by unfold growingPotential; fun_prop) j]
  have hz : coordinatePartial (fun _ : Coordinate4 => -c) x j=0 := by
    simp [coordinatePartial]
  rw [hz,zero_mul,zero_add]
  have hp := congrFun (congrFun growing_potential_covector x) j
  change coordinatePartial growingPotential x j=growingTimeCovector x j at hp
  rw [hp,flatForce,growing_flat_divergence]
  ring

theorem growing_trace_completed_conserved (c : ℝ) :
    ∀ x∈(univ : Set Coordinate4), ∀ j,
      tensorFieldDivergence flatMetric flatConnection
        (traceCompletedStress growingTimeCovector c (growingTraceCorrection c)) x j=0 := by
  apply (completed_conserved_iff_gradient univ isOpen_univ growingTimeCovector c
    (growingTraceCorrection c) growing_time_smooth growing_time_closed
    (growing_trace_correction_smooth c)).2
  intro x _ j
  exact growing_trace_gradient c x j

theorem growing_trace_completed_null_response (c : ℝ) (x d : Coordinate4)
    (hd : tensorQuad eta4 d=0) :
    tensorQuad (traceCompletedStress growingTimeCovector c (growingTraceCorrection c) x) d=
      c*(covectorRead (growingTimeCovector x) d)^2 :=
  trace_completed_null growingTimeCovector c (growingTraceCorrection c) x d hd

/-- The uncompleted tensor fails conservation for nonzero coupling, while the
previous theorem constructs a completion with exactly the same null response. -/
theorem growing_uncompleted_not_conserved (c : ℝ) (hc : c≠0) :
    tensorFieldDivergence flatMetric flatConnection
      (flatCovectorStress growingTimeCovector c) timeCovector 0≠0 := by
  rw [flat_stress_divergence univ isOpen_univ growingTimeCovector c
    growing_time_smooth growing_time_closed timeCovector (mem_univ _) 0,
    growing_flat_divergence]
  simpa [growingTimeCovector,timeCovector] using hc

#print axioms mixedPotential
#print axioms mixedCovector
#print axioms mixedPoint
#print axioms mixed_potential_smooth
#print axioms mixed_covector_smooth
#print axioms mixed_potential_covector
#print axioms mixed_covector_closed
#print axioms mixed_covector_partial
#print axioms mixed_covector_divergence
#print axioms mixed_force_formula
#print axioms mixed_force_partial_one_zero
#print axioms mixed_force_partial_zero_one
#print axioms mixed_force_curl
#print axioms mixed_force_not_closed
#print axioms mixed_no_conserved_null_response
#print axioms growingTraceCorrection
#print axioms growing_trace_correction_smooth
#print axioms growing_flat_divergence
#print axioms growing_flat_force
#print axioms growing_trace_gradient
#print axioms growing_trace_completed_conserved
#print axioms growing_trace_completed_null_response
#print axioms growing_uncompleted_not_conserved
end
end ChatgptAudit.Completion042
