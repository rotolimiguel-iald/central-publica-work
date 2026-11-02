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
import TGLExt.UnitaryEntropyResponse
import TGLExt.DirectionalUnitaryFamily
import Mathlib.Data.Matrix.Block

set_option autoImplicit false
set_option maxHeartbeats 1500000
namespace ChatgptAudit.JointUnitary
open Matrix Filter Topology Set ChatgptAudit.Micro021 ChatgptAudit.Unitary022
  ChatgptAudit.Coherent023
noncomputable section
variable {ι : Type} [Fintype ι]

structure UnitaryLabelData (ι : Type) [Fintype ι] where
  weight : ι → ℝ
  weight_pos : ∀ j, 0 < weight j
  weight_sum : ∑ j, weight j = 1
  axisA : ι → ℝ
  axisB : ι → ℝ
  initialU : ι → ℝ
  initialV : ι → ℝ
  axis_normalized : ∀ j, (axisA j)^2 + (axisB j)^2 = 1
  initial_normalized : ∀ j, (initialU j)^2 + (initialV j)^2 = 1
  positive_u : ∀ j, 0 < initialU j
  positive_v : ∀ j, 0 < initialV j

def labelledWeights (weight : ι → ℝ) (p : ι → Fin 2 → ℝ) :
    ι × Fin 2 → ℝ := fun k => weight k.1 * p k.1 k.2

def jointBase (C : UnitaryLabelData ι) : ι × Fin 2 → ℝ :=
  labelledWeights C.weight (fun j => baseWeights (C.initialU j) (C.initialV j))

def jointWeights (C : UnitaryLabelData ι) (frequency : ι → ℝ) (t : ℝ) :
    ι × Fin 2 → ℝ :=
  labelledWeights C.weight (fun j => pairWeights (C.axisA j) (C.axisB j)
    (frequency j) (C.initialU j) (C.initialV j) t)

theorem joint_weights_normalized (C : UnitaryLabelData ι)
    (frequency : ι → ℝ) (t : ℝ) : ∑ k, jointWeights C frequency t k = 1 := by
  unfold jointWeights labelledWeights
  rw [Fintype.sum_prod_type]
  simp only [← Finset.mul_sum, pair_weights_normalized _ _ _ _ _ _ (C.initial_normalized _),
    mul_one]
  exact C.weight_sum

theorem joint_weights_nonnegative (C : UnitaryLabelData ι)
    (frequency : ι → ℝ) (t : ℝ) : ∀ k, 0 ≤ jointWeights C frequency t k := by
  intro k
  exact mul_nonneg (C.weight_pos k.1).le
    (pair_weights_nonnegative _ _ _ _ _ _ (C.axis_normalized k.1) k.2)

theorem joint_base_positive (C : UnitaryLabelData ι) : ∀ k, 0 < jointBase C k := by
  intro k
  exact mul_pos (C.weight_pos k.1)
    (base_weights_positive _ _ (C.positive_u k.1) (C.positive_v k.1) k.2)

def jointUnitaryCurve (C : UnitaryLabelData ι) (frequency : ι → ℝ) :
    DiagonalStateCurve (jointBase C) where
  weights := jointWeights C frequency
  tangent := fun t k => C.weight k.1 * pairTangent (C.axisA k.1) (C.axisB k.1)
    (frequency k.1) (C.initialU k.1) (C.initialV k.1) t k.2
  at_zero := by
    intro k
    dsimp only [jointWeights, jointBase, labelledWeights]
    rw [pair_weights_at_zero]
  trace_one := joint_weights_normalized C frequency
  derivative_zero := fun k => (pair_weights_derivative _ _ _ _ _ 0 k.2).const_mul (C.weight k.1)
  derivative_past := by
    filter_upwards [] with t
    intro k
    exact (pair_weights_derivative _ _ _ _ _ t k.2).const_mul (C.weight k.1)
  tangent_continuous := by
    intro k
    exact continuousAt_const.mul
      ((unitaryStateCurve (C.axisA k.1) (C.axisB k.1) (frequency k.1)
        (C.initialU k.1) (C.initialV k.1) (C.initial_normalized k.1)).tangent_continuous k.2)

theorem joint_curve_tangent_zero (C : UnitaryLabelData ι) (frequency : ι → ℝ) :
    (jointUnitaryCurve C frequency).tangent 0 = 0 := by
  funext k
  simp only [jointUnitaryCurve, pair_tangent_at_zero, Pi.zero_apply, mul_zero]

theorem joint_weights_positive_near (C : UnitaryLabelData ι) (frequency : ι → ℝ) :
    ∀ᶠ t in 𝓝 (0 : ℝ), ∀ k, 0 < jointWeights C frequency t k :=
  state_curve_positive_near (jointUnitaryCurve C frequency) (joint_base_positive C)

theorem entropy_atom_scaled (weight q : ℝ) :
    entropyAtom (weight*q) = weight * entropyAtom q - weight*q*Real.log weight := by
  by_cases hw : weight = 0
  · simp [hw, entropyAtom]
  by_cases hq : q = 0
  · simp [hq, entropyAtom]
  unfold entropyAtom
  rw [Real.log_mul hw hq]
  ring

theorem entropy_labelled_decomposition (weight : ι → ℝ) (p : ι → Fin 2 → ℝ)
    (hn : ∀ j, ∑ b, p j b = 1) :
    finiteEntropy (labelledWeights weight p) =
      finiteEntropy weight + ∑ j, weight j * finiteEntropy (p j) := by
  unfold finiteEntropy
  rw [Fintype.sum_prod_type, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro j _
  simp only [labelledWeights, Fin.sum_univ_two, entropy_atom_scaled]
  have hp : p j 1 = 1 - p j 0 := by
    have h := hn j
    simp only [Fin.sum_univ_two] at h
    linarith
  rw [hp]
  unfold entropyAtom
  ring

theorem modular_labelled_decomposition (weight : ι → ℝ)
    (hw : ∀ j, 0 < weight j) (p r : ι → Fin 2 → ℝ)
    (hp : ∀ j b, 0 < p j b) (hnp : ∀ j, ∑ b, p j b = 1)
    (hnr : ∀ j, ∑ b, r j b = 1) :
    modularIncrement (labelledWeights weight p) (labelledWeights weight r) =
      ∑ j, weight j * modularIncrement (p j) (r j) := by
  unfold modularIncrement
  rw [Fintype.sum_prod_type]
  apply Finset.sum_congr rfl
  intro j _
  simp only [labelledWeights, Fin.sum_univ_two]
  rw [Real.log_mul (ne_of_gt (hw j)) (ne_of_gt (hp j 0)),
    Real.log_mul (ne_of_gt (hw j)) (ne_of_gt (hp j 1))]
  have hp1 : p j 1 = 1 - p j 0 := by
    have h := hnp j
    simp only [Fin.sum_univ_two] at h
    linarith
  have hr1 : r j 1 = 1 - r j 0 := by
    have h := hnr j
    simp only [Fin.sum_univ_two] at h
    linarith
  rw [hp1, hr1]
  ring

theorem joint_entropy_decomposition (C : UnitaryLabelData ι)
    (frequency : ι → ℝ) (t : ℝ) :
    finiteEntropy (jointWeights C frequency t) = finiteEntropy C.weight +
      ∑ j, C.weight j * finiteEntropy
        (pairWeights (C.axisA j) (C.axisB j) (frequency j) (C.initialU j) (C.initialV j) t) := by
  apply entropy_labelled_decomposition
  intro j
  exact pair_weights_normalized _ _ _ _ _ _ (C.initial_normalized j)

theorem joint_base_entropy_decomposition (C : UnitaryLabelData ι) :
    finiteEntropy (jointBase C) = finiteEntropy C.weight +
      ∑ j, C.weight j * finiteEntropy (baseWeights (C.initialU j) (C.initialV j)) := by
  apply entropy_labelled_decomposition
  intro j
  simpa only [baseWeights, Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one]
    using C.initial_normalized j

theorem joint_entropy_increment (C : UnitaryLabelData ι)
    (frequency : ι → ℝ) (t : ℝ) :
    finiteEntropy (jointWeights C frequency t) - finiteEntropy (jointBase C) =
      ∑ j, C.weight j * (finiteEntropy
        (pairWeights (C.axisA j) (C.axisB j) (frequency j) (C.initialU j) (C.initialV j) t) -
          finiteEntropy (baseWeights (C.initialU j) (C.initialV j))) := by
  rw [joint_entropy_decomposition, joint_base_entropy_decomposition]
  simp only [mul_sub, Finset.sum_sub_distrib]
  ring

theorem joint_modular_increment (C : UnitaryLabelData ι)
    (frequency : ι → ℝ) (t : ℝ) :
    modularIncrement (jointBase C) (jointWeights C frequency t) =
      ∑ j, C.weight j * modularIncrement (baseWeights (C.initialU j) (C.initialV j))
        (pairWeights (C.axisA j) (C.axisB j) (frequency j) (C.initialU j) (C.initialV j) t) := by
  apply modular_labelled_decomposition _ C.weight_pos
  · intro j
    exact base_weights_positive _ _ (C.positive_u j) (C.positive_v j)
  · intro j
    simpa only [baseWeights, Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one]
      using C.initial_normalized j
  · intro j
    exact pair_weights_normalized _ _ _ _ _ _ (C.initial_normalized j)

def jointResponse (C : UnitaryLabelData ι) (frequency : ι → ℝ) : ℝ :=
  ∑ j, C.weight j * unitaryResponse (C.axisA j) (C.axisB j)
    (frequency j) (C.initialU j) (C.initialV j)

theorem joint_modular_quadratic_limit (C : UnitaryLabelData ι) (frequency : ι → ℝ) :
    Tendsto (fun t => modularIncrement (jointBase C) (jointWeights C frequency t) / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (jointResponse C frequency)) := by
  have hl := tendsto_finsetSum Finset.univ (fun j _ =>
    (unitary_modular_quadratic_limit (C.axisA j) (C.axisB j) (frequency j)
      (C.initialU j) (C.initialV j) (C.positive_u j) (C.positive_v j)).const_mul (C.weight j))
  have he : (fun t => modularIncrement (jointBase C) (jointWeights C frequency t) / t^2) =
      (fun t => ∑ j, C.weight j *
        (modularIncrement (baseWeights (C.initialU j) (C.initialV j))
          (pairWeights (C.axisA j) (C.axisB j) (frequency j) (C.initialU j) (C.initialV j) t) / t^2)) := by
    funext t
    rw [joint_modular_increment, Finset.sum_div]
    apply Finset.sum_congr rfl
    intro j _
    ring
  rw [he]
  exact hl

theorem joint_entropy_quadratic_limit (C : UnitaryLabelData ι) (frequency : ι → ℝ) :
    Tendsto (fun t => (finiteEntropy (jointWeights C frequency t) - finiteEntropy (jointBase C)) / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (jointResponse C frequency)) := by
  have hl := tendsto_finsetSum Finset.univ (fun j _ =>
    (unitary_entropy_quadratic_limit (C.axisA j) (C.axisB j) (frequency j)
      (C.initialU j) (C.initialV j) (C.initial_normalized j)
      (C.positive_u j) (C.positive_v j)).const_mul (C.weight j))
  have he : (fun t => (finiteEntropy (jointWeights C frequency t) - finiteEntropy (jointBase C)) / t^2) =
      (fun t => ∑ j, C.weight j *
        ((finiteEntropy (pairWeights (C.axisA j) (C.axisB j) (frequency j)
          (C.initialU j) (C.initialV j) t) -
          finiteEntropy (baseWeights (C.initialU j) (C.initialV j))) / t^2)) := by
    funext t
    rw [joint_entropy_increment, Finset.sum_div]
    apply Finset.sum_congr rfl
    intro j _
    ring
  rw [he]
  exact hl

theorem joint_relative_entropy_quadratic_zero (C : UnitaryLabelData ι) (frequency : ι → ℝ) :
    Tendsto (fun t => diagonalRelativeEntropy (jointWeights C frequency t) (jointBase C) / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 0) := by
  apply (relative_entropy_quadratic_zero_iff (jointUnitaryCurve C frequency)
    (joint_base_positive C)).mpr
  exact joint_curve_tangent_zero C frequency

def jointCovectorCurve (C : UnitaryLabelData ι) (w : ι → Coordinate4) (direction : Coordinate4) :
    DiagonalStateCurve (jointBase C) :=
  jointUnitaryCurve C (fun j => covectorRead (w j) direction)

theorem joint_covector_response (C : UnitaryLabelData ι)
    (w : ι → Coordinate4) (direction : Coordinate4) :
    jointResponse C (fun j => covectorRead (w j) direction) =
      ∑ j, C.weight j * unitaryResponse (C.axisA j) (C.axisB j)
        1 (C.initialU j) (C.initialV j) * (covectorRead (w j) direction)^2 := by
  unfold jointResponse
  apply Finset.sum_congr rfl
  intro j _
  unfold unitaryResponse
  ring

/-- Matrix.blockDiagonal uses (branch,label); probabilities explicitly use (label,branch). -/
def jointBlockFlow [DecidableEq ι] (C : UnitaryLabelData ι) (frequency : ι → ℝ) (t : ℝ) :
    Matrix (Fin 2 × ι) (Fin 2 × ι) ℂ :=
  Matrix.blockDiagonal (fun j => pairFlow (C.axisA j) (C.axisB j) (frequency j) t)

theorem joint_block_flow_unitary [DecidableEq ι] (C : UnitaryLabelData ι)
    (frequency : ι → ℝ) (t : ℝ) :
    (jointBlockFlow C frequency t)ᴴ * jointBlockFlow C frequency t = 1 ∧
      jointBlockFlow C frequency t * (jointBlockFlow C frequency t)ᴴ = 1 := by
  unfold jointBlockFlow
  constructor
  · rw [Matrix.blockDiagonal_conjTranspose, ← Matrix.blockDiagonal_mul]
    simp only [pair_flow_adjoint_mul _ _ _ _ (C.axis_normalized _)]
    exact Matrix.blockDiagonal_one
  · rw [Matrix.blockDiagonal_conjTranspose, ← Matrix.blockDiagonal_mul]
    simp only [pair_flow_mul_adjoint _ _ _ _ (C.axis_normalized _)]
    exact Matrix.blockDiagonal_one

def jointInitialAmplitude (C : UnitaryLabelData ι) (k : Fin 2 × ι) : ℂ :=
  (Real.sqrt (C.weight k.2) : ℂ) * initialPair (C.initialU k.2) (C.initialV k.2) k.1

def jointBlockAmplitude (C : UnitaryLabelData ι) (frequency : ι → ℝ) (t : ℝ)
    (k : Fin 2 × ι) : ℂ :=
  (Real.sqrt (C.weight k.2) : ℂ) * evolvedPair (C.axisA k.2) (C.axisB k.2)
    (frequency k.2) (C.initialU k.2) (C.initialV k.2) t k.1

theorem joint_block_amplitude_weights (C : UnitaryLabelData ι)
    (frequency : ι → ℝ) (t : ℝ) (k : Fin 2 × ι) :
    jointBlockAmplitude C frequency t k * star (jointBlockAmplitude C frequency t k) =
      (jointWeights C frequency t (k.2,k.1) : ℂ) := by
  have hs : (Real.sqrt (C.weight k.2) : ℂ)^2 = (C.weight k.2 : ℂ) := by
    exact_mod_cast Real.sq_sqrt (C.weight_pos k.2).le
  calc
    jointBlockAmplitude C frequency t k * star (jointBlockAmplitude C frequency t k) =
        (Real.sqrt (C.weight k.2) : ℂ)^2 *
          (evolvedPair (C.axisA k.2) (C.axisB k.2) (frequency k.2)
            (C.initialU k.2) (C.initialV k.2) t k.1 *
            star (evolvedPair (C.axisA k.2) (C.axisB k.2) (frequency k.2)
              (C.initialU k.2) (C.initialV k.2) t k.1)) := by
      simp only [jointBlockAmplitude, star_mul, Complex.star_def, Complex.conj_ofReal]
      ring
    _ = (C.weight k.2 : ℂ) *
        (pairWeights (C.axisA k.2) (C.axisB k.2) (frequency k.2)
          (C.initialU k.2) (C.initialV k.2) t k.1 : ℂ) := by
      rw [hs, pair_amplitude_weights _ _ _ _ _ _ (C.axis_normalized k.2)]
    _ = (jointWeights C frequency t (k.2,k.1) : ℂ) := by
      simp only [jointWeights, labelledWeights, Complex.ofReal_mul]

theorem joint_block_flow_prepares_amplitude [DecidableEq ι]
    (C : UnitaryLabelData ι) (frequency : ι → ℝ) (t : ℝ) :
    jointBlockFlow C frequency t *ᵥ jointInitialAmplitude C = jointBlockAmplitude C frequency t := by
  ext ⟨b,j⟩
  simp only [jointBlockFlow, jointInitialAmplitude, jointBlockAmplitude,
    Matrix.mulVec, dotProduct, Fintype.sum_prod_type, Matrix.blockDiagonal_apply,
    ite_mul, zero_mul]
  simp only [Finset.sum_ite_eq, Finset.mem_univ, if_true]
  simp only [evolvedPair, Matrix.mulVec, dotProduct, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro a _
  ring

/-- A concrete two-label preparation with faithful diagonal base. -/
def twoLabelData : UnitaryLabelData (Fin 2) where
  weight := fun _ => 1/2
  weight_pos := by intro j; norm_num
  weight_sum := by norm_num [Fin.sum_univ_two]
  axisA := fun _ => 0
  axisB := fun _ => 1
  initialU := fun _ => 3/5
  initialV := fun _ => 4/5
  axis_normalized := by intro j; norm_num
  initial_normalized := by intro j; norm_num
  positive_u := by intro j; norm_num
  positive_v := by intro j; norm_num

theorem two_label_positive_response : 0 < jointResponse twoLabelData (fun _ => 1) := by
  unfold jointResponse
  rw [Fin.sum_univ_two]
  dsimp only [twoLabelData]
  nlinarith only [positive_control_response_strict]

theorem two_label_zero_tangent_positive_response :
    (jointUnitaryCurve twoLabelData (fun _ => 1)).tangent 0 = 0 ∧
      0 < jointResponse twoLabelData (fun _ => 1) :=
  ⟨joint_curve_tangent_zero _ _, two_label_positive_response⟩

#print axioms UnitaryLabelData
#print axioms labelledWeights
#print axioms jointBase
#print axioms jointWeights
#print axioms joint_weights_normalized
#print axioms joint_weights_nonnegative
#print axioms joint_base_positive
#print axioms jointUnitaryCurve
#print axioms joint_curve_tangent_zero
#print axioms joint_weights_positive_near
#print axioms entropy_atom_scaled
#print axioms entropy_labelled_decomposition
#print axioms modular_labelled_decomposition
#print axioms joint_entropy_decomposition
#print axioms joint_base_entropy_decomposition
#print axioms joint_entropy_increment
#print axioms joint_modular_increment
#print axioms jointResponse
#print axioms joint_modular_quadratic_limit
#print axioms joint_entropy_quadratic_limit
#print axioms joint_relative_entropy_quadratic_zero
#print axioms jointCovectorCurve
#print axioms joint_covector_response
#print axioms jointBlockFlow
#print axioms joint_block_flow_unitary
#print axioms jointInitialAmplitude
#print axioms jointBlockAmplitude
#print axioms joint_block_amplitude_weights
#print axioms joint_block_flow_prepares_amplitude
#print axioms twoLabelData
#print axioms two_label_positive_response
#print axioms two_label_zero_tangent_positive_response

end
end ChatgptAudit.JointUnitary
