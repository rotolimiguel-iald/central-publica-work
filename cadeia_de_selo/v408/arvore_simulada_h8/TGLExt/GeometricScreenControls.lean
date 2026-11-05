-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_012 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.GeometricAreaHorizon
import TGLExt.ScreenEntropyObstruction
import TGLExt.HorizonBalanceControls

set_option autoImplicit false
set_option maxHeartbeats 4000000
set_option maxRecDepth 4096
namespace ChatgptAudit
open Matrix TGLExt Filter Topology
open scoped ContDiff
noncomputable section

def flatNullFrame : Tensor4 := !![1,-1/2,0,0;1,1/2,0,0;0,0,1,0;0,0,0,1]
def flatNullInverse : Tensor4 := !![1/2,1/2,0,0;-1,1,0,0;0,0,1,0;0,0,0,1]
def flatScreenVectors : ScreenVectors := screenColumns flatNullFrame
def stretchedScreen (t : ℝ) : ScreenVectors := (1+t) • flatScreenVectors

theorem flat_null_inverse : flatNullFrame*flatNullInverse=1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [flatNullFrame,flatNullInverse,Matrix.mul_apply,Fin.sum_univ_four,
      Matrix.cons_val_zero,Matrix.cons_val_one,Matrix.cons_val_two,Matrix.cons_val_three,
      Matrix.vecHead,Matrix.vecTail]

theorem flat_null_gram : flatNullFrameᵀ*eta4*flatNullFrame=nullScreenGram (-1) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [flatNullFrame,eta4,nullScreenGram,Matrix.mul_apply,Matrix.diagonal_apply,Fin.sum_univ_four,
      Matrix.cons_val_zero,Matrix.cons_val_one,Matrix.cons_val_two,Matrix.cons_val_three,
      Matrix.vecHead,Matrix.vecTail]

theorem flat_screen_metric : screenGram eta4 flatScreenVectors= -1 := by
  rw [flatScreenVectors,screen_gram_in_frame,flat_null_gram,null_gram_screen_block]

theorem flat_screen_area : screenArea (screenGram eta4 flatScreenVectors)=1 := by
  rw [flat_screen_metric]
  norm_num [screenArea,Matrix.det_neg]

theorem flat_induced_area (curve : ℝ → Coordinate4) (t : ℝ) :
    inducedArea (fun _ => eta4) curve (fun _ => flatScreenVectors) t=1 :=
  flat_screen_area

def flatScreenWitness : NullScreenAt eta4 0 horizonControlDirection flatScreenVectors where
  frame := flatNullFrame
  inverse := flatNullInverse
  metric := -1
  right_inverse := flat_null_inverse
  gram := flat_null_gram
  first_column := by
    intro a
    fin_cases a <;> rfl
  columns := rfl
  first_screen_negative := by norm_num
  determinant_positive := by norm_num [Matrix.det_neg]
  preserves_null_pairing := by simp

def flatGeometricScreen :
    GeometricScreenAlong (fun _ => eta4) (fun _ _ => 0)
      (fun _ => horizonControlDirection) (fun t => t • horizonControlDirection) where
  vectors := fun _ => flatScreenVectors
  continuous_zero := fun _ _ => continuousAt_const
  curve_tangent := by
    filter_upwards [] with t
    simpa using (hasDerivAt_id t).smul_const horizonControlDirection
  frames := by
    filter_upwards [] with t
    rw [flat_constant_gradient]
    exact ⟨flatScreenWitness⟩
  transport := by
    filter_upwards [] with t
    rw [flat_constant_gradient]
    intro a i
    simpa [connectionAlong] using hasDerivAt_const t (flatScreenVectors a i)

def flatGeometricHorizon (eta : ℝ) :
    GeometricHorizonPencil Set.univ (fun _ => eta4) (fun _ _ => 0) (fun _ => 0)
      eta 0 horizonControlDirection where
  neighborhood := Set.univ
  neighborhood_open := isOpen_univ
  neighborhood_subset := Set.Subset.refl _
  point_mem := Set.mem_univ _
  velocity := fun _ => horizonControlDirection
  velocity_smooth := fun _ => contDiffOn_const
  velocity_at_point := rfl
  velocity_null := by
    intro _ _
    simpa [controlConformalMetric,controlConformalFactor] using curved_control_direction_null
  geodesic := by
    intro y _
    simp [vectorAcceleration,flat_constant_gradient]
  equilibrium_gradient := flat_constant_gradient horizonControlDirection 0
  curve := fun t => t • horizonControlDirection
  curve_zero := zero_smul ℝ horizonControlDirection
  curve_tangent := by
    simpa using (hasDerivAt_id (0:ℝ)).smul_const horizonControlDirection
  rate := 1
  rate_nonzero := one_ne_zero
  screen := flatGeometricScreen
  area_positive_zero := by
    change 0<(screenGram eta4 flatScreenVectors).det
    rw [flat_screen_metric]
    norm_num [Matrix.det_neg]
  heat := fun _ => 0
  heat_continuous := continuousAt_const
  heat_zero := rfl
  heat_rate := by
    filter_upwards [] with t
    simp only [tensorQuad,Matrix.zero_mulVec,dotProduct_zero,mul_zero,zero_mul]
    exact hasDerivAt_const t (0:ℝ)
  clausius_to_second_order := by
    have ha : inducedArea (fun _ => eta4) (fun t => t • horizonControlDirection)
        flatGeometricScreen.vectors=(fun _ => 1) := by
      funext t
      exact flat_induced_area _ t
    rw [ha]
    simp only [horizonBalancePrimitive,sub_self,mul_zero,zero_div]
    exact tendsto_const_nhds

theorem flat_geometric_nonzero_inhabitant (eta : ℝ) :
    horizonControlDirection≠0 ∧
    Nonempty (GeometricHorizonPencil Set.univ (fun _ => eta4) (fun _ _ => 0)
      (fun _ => 0) eta 0 horizonControlDirection) := by
  exact ⟨(flat_nonzero_pencil_exists eta).1,⟨flatGeometricHorizon eta⟩⟩

theorem screen_area_signature_flip (h : ScreenMatrix) : screenArea (-h)=screenArea h := by
  simp [screenArea,Matrix.det_neg]

theorem screen_gram_rescale (g : Tensor4) (S : ScreenVectors) (r : ℝ) :
    screenGram g (r • S)=r^2 • screenGram g S := by
  unfold screenGram
  rw [Matrix.transpose_smul,Matrix.smul_mul,Matrix.smul_mul,Matrix.mul_smul,smul_smul]
  congr 1
  ring

theorem stretched_screen_area (t : ℝ) :
    screenArea (screenGram eta4 (stretchedScreen t))=(1+t)^2 := by
  rw [stretchedScreen,screen_gram_rescale,flat_screen_metric]
  have hd : (((1+t)^2) • (-1:ScreenMatrix)).det=(((1+t)^2)^2) := by
    simp [Matrix.det_neg]
  rw [screenArea,hd,Real.sqrt_sq_eq_abs,abs_of_nonneg (sq_nonneg (1+t))]

theorem stretched_screen_area_rate :
    HasDerivAt (fun t => screenArea (screenGram eta4 (stretchedScreen t))) 2 0 := by
  have he : (fun t => screenArea (screenGram eta4 (stretchedScreen t)))=
      (fun t : ℝ => (1+t)^2) := funext stretched_screen_area
  rw [he]
  have hp : (fun t : ℝ => (1+t)^2)=(fun t : ℝ => 1+t)^2 := rfl
  rw [hp]
  have hd := ((hasDerivAt_id (0:ℝ)).const_add 1).pow 2
  norm_num only [id_eq,pow_one,add_zero,mul_one] at hd
  exact hd

theorem stretched_cut_refuses_fixed_entropy (P : SiteProfile) (N : ℕ)
    (eta : ℝ) (heta : eta≠0) :
    ¬ (reducedDiagonalEntropy (towerCutDensity P N)=eta ∧
      ∀ᶠ t in 𝓝[<] (0:ℝ), reducedDiagonalEntropy (towerCutDensity P N)=
        eta*screenArea (screenGram eta4 (stretchedScreen t))) := by
  rintro ⟨h0,he⟩
  have hz := constant_entropy_forces_zero_area_rate
    (reducedDiagonalEntropy (towerCutDensity P N)) eta
    (fun t => screenArea (screenGram eta4 (stretchedScreen t))) 0 2 heta
    stretched_screen_area_rate (by simpa [stretched_screen_area] using h0) he
  norm_num at hz

#print axioms flat_null_inverse
#print axioms flat_null_gram
#print axioms flat_screen_metric
#print axioms flat_screen_area
#print axioms flat_induced_area
#print axioms flatScreenWitness
#print axioms flatGeometricScreen
#print axioms flatGeometricHorizon
#print axioms flat_geometric_nonzero_inhabitant
#print axioms screen_area_signature_flip
#print axioms screen_gram_rescale
#print axioms stretched_screen_area
#print axioms stretched_screen_area_rate
#print axioms stretched_cut_refuses_fixed_entropy
end
end ChatgptAudit
