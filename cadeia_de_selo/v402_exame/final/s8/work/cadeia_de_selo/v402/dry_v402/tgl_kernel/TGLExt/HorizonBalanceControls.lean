-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_010 (05-06/09/2026), transposta em 06/09/2026
-- Lote 007..023: habitante GLOBAL periodico da esperanca do centralizador; cauda nao ciclica;
--   obstrucoes de Borchers e da assinatura; e a camada GEOMETRICA GERAL em carta: tensores,
--   conexao de Levi-Civita, curvatura, Bianchi, Einstein geometrico + conservacao, Raychaudhuri,
--   Clausius local <=> balanco nulo de Ricci, telas/congruencias nulas construidas, area e calor,
--   entropia relativa, dinamica unitaria, covetor de materia. Estatuto [REAL / INPUT / OPEN]:
--   Clausius, a metrica lorentziana, H3 dinamico, assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100% nas 17 entregas; 17/17
--   auditores da bancada exit 0; recompilacao INDEPENDENTE 116/116 exit 0, todos os axiomas no
--   trio [propext, Classical.choice, Quot.sound]; zero sorry/warning; enunciados lidos.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports; nada mais.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.HorizonEinsteinReconstruction
import TGLExt.CurvatureControls
import TGLExt.TheImportedEquilibrium

set_option autoImplicit false
set_option maxHeartbeats 3600000
set_option maxRecDepth 4096
namespace ChatgptAudit
open Matrix TGLExt Filter Topology
open scoped ContDiff
noncomputable section

def horizonControlDirection : Coordinate4 := ![1,1,0,0]
def horizonControlArea (t : ℝ) : ℝ := Real.exp (-(t^2)/2)

theorem balanced_flux_control (t : ℝ) :
    horizonFluxResidual 1 (2*Real.pi) (fun s => -s) horizonControlArea (fun _ => 1) t=0 := by
  unfold horizonFluxResidual
  field_simp [Real.pi_ne_zero]
  ring

theorem balanced_local_control :
    LocalClausiusPast 1 (2*Real.pi) (fun s => -s) horizonControlArea (fun _ => 1) := by
  unfold LocalClausiusPast
  simp only [balanced_flux_control,zero_div]
  exact tendsto_const_nhds

theorem curved_control_direction_null :
    tensorQuad (controlConformalMetric (0:Coordinate4)) horizonControlDirection=0 := by
  norm_num [controlConformalMetric,controlConformalFactor,horizonControlDirection,tensorQuad,
    eta4,Matrix.mulVec,dotProduct,Fin.sum_univ_four,Fin.isValue,Matrix.cons_val_zero,
    Matrix.cons_val_one,Matrix.cons_val_two,Matrix.cons_val_three,Matrix.vecHead,Matrix.vecTail]

theorem curved_control_no_vacuum_pencil (eta : ℝ) (heta : eta≠0) :
    ¬ Nonempty (LocalHorizonPencil Set.univ controlConformalMetric
      (leviCivitaField controlConformalMetric controlConformalInverse) (fun _ => 0)
      eta (0:Coordinate4) horizonControlDirection) := by
  rintro ⟨P⟩
  have he : leviCivitaField controlConformalMetric controlConformalInverse=controlConformalConnection := by
    funext x
    exact control_conformal_levi_civita x
  have hG : SmoothConnectionOn Set.univ
      (leviCivitaField controlConformalMetric controlConformalInverse) := by
    rw [he]
    intro i a b
    exact contDiffOn_const
  have hg : ∀ x∈(Set.univ : Set Coordinate4), (controlConformalMetric x)ᵀ=controlConformalMetric x := by
    intro x _
    simp [controlConformalMetric,eta4,Matrix.transpose_smul]
  have ht := levi_civita_field_torsion_free Set.univ isOpen_univ
    controlConformalMetric controlConformalInverse hg
  have hT : ∀ a b : Fin 4, DifferentiableOn ℝ (fun _ : Coordinate4 => (0:Tensor4) a b) Set.univ :=
    fun _ _ => differentiableOn_const _
  have hr := pencil_ricci_balance Set.univ isOpen_univ controlConformalMetric
    (leviCivitaField controlConformalMetric controlConformalInverse) (fun _ => 0) eta heta hG hT
    (0:Coordinate4) horizonControlDirection (ht 0 (Set.mem_univ _)) P
  rw [control_conformal_ricci] at hr
  norm_num [horizonControlDirection,tensorQuad,Matrix.mulVec,dotProduct,Fin.sum_univ_four,
    Fin.isValue,Matrix.diagonal_apply,Matrix.cons_val_zero,Matrix.cons_val_one,Matrix.cons_val_two,
    Matrix.cons_val_three,Matrix.vecHead,Matrix.vecTail] at hr

theorem kms_with_incompatible_geometric_data (l : ℝ) (hl : 0<l) (N : ℕ) (eta : ℝ) (heta : eta≠0) :
    ((towerEquilibriumInput l hl N).flow 1=1) ∧
    (∀ a b : Matrix (chainIdx N) (chainIdx N) ℂ,
      (towerEquilibriumInput l hl N).state (a*b)=
        (towerEquilibriumInput l hl N).state (b*(towerEquilibriumInput l hl N).flow a)) ∧
    ¬ Nonempty (LocalHorizonPencil Set.univ controlConformalMetric
      (leviCivitaField controlConformalMetric controlConformalInverse) (fun _ => 0)
      eta (0:Coordinate4) horizonControlDirection) := by
  have he := qgImport_H3_localHorizonEquilibrium_bridged l hl N
  exact ⟨he.1,he.2,curved_control_no_vacuum_pencil eta heta⟩


theorem flat_constant_gradient (v y : Coordinate4) :
    covariantVectorGradient (fun _ _ => 0) (fun _ => v) y=0 := by
  ext a i
  simp [covariantVectorGradient,covariantVectorDerivative,vectorPartial,coordinatePartial]

theorem flat_constant_expansion (v y : Coordinate4) :
    vectorExpansion (fun _ _ => 0) (fun _ => v) y=0 := by
  rw [vectorExpansion,flat_constant_gradient]
  simp

def flatHorizonPencil (eta : ℝ) (v : Coordinate4) (hv : tensorQuad eta4 v=0) :
    LocalHorizonPencil Set.univ (fun _ => eta4) (fun _ _ => 0) (fun _ => 0) eta 0 v where
  neighborhood := Set.univ
  neighborhood_open := isOpen_univ
  neighborhood_subset := Set.Subset.refl _
  point_mem := Set.mem_univ _
  velocity := fun _ => v
  velocity_smooth := fun _ => contDiffOn_const
  velocity_at_point := rfl
  velocity_null := fun _ _ => hv
  geodesic := by
    intro y _
    simp [vectorAcceleration,flat_constant_gradient]
  equilibrium_gradient := flat_constant_gradient v 0
  curve := fun t => t • v
  curve_zero := zero_smul ℝ v
  curve_tangent := by
    simpa using (hasDerivAt_id (0:ℝ)).smul_const v
  rate := 1
  rate_nonzero := one_ne_zero
  area := fun _ => 1
  area_continuous := continuousAt_const
  area_nonzero := one_ne_zero
  heat := fun _ => 0
  heat_continuous := continuousAt_const
  heat_zero := rfl
  area_rate := by
    filter_upwards [] with t
    simp only [flat_constant_expansion,zero_mul]
    exact hasDerivAt_const t (1:ℝ)
  heat_rate := by
    filter_upwards [] with t
    simp only [tensorQuad,Matrix.zero_mulVec,dotProduct_zero,mul_zero,zero_mul]
    exact hasDerivAt_const t (0:ℝ)
  clausius_to_second_order := by
    simp only [horizonBalancePrimitive,sub_self,mul_zero,zero_div]
    exact tendsto_const_nhds

theorem flat_nonzero_pencil_exists (eta : ℝ) :
    horizonControlDirection≠0 ∧
    Nonempty (LocalHorizonPencil Set.univ (fun _ => eta4) (fun _ _ => 0)
      (fun _ => 0) eta 0 horizonControlDirection) := by
  have hv : tensorQuad eta4 horizonControlDirection=0 := by
    simpa [controlConformalMetric,controlConformalFactor] using curved_control_direction_null
  refine ⟨?_,⟨flatHorizonPencil eta horizonControlDirection hv⟩⟩
  intro hz
  have h0 := congrArg (fun v : Coordinate4 => v 0) hz
  norm_num [horizonControlDirection] at h0

#print axioms flat_constant_gradient
#print axioms flat_constant_expansion
#print axioms flatHorizonPencil
#print axioms flat_nonzero_pencil_exists

#print axioms balanced_flux_control
#print axioms balanced_local_control
#print axioms curved_control_direction_null
#print axioms curved_control_no_vacuum_pencil
#print axioms kms_with_incompatible_geometric_data
end
end ChatgptAudit
