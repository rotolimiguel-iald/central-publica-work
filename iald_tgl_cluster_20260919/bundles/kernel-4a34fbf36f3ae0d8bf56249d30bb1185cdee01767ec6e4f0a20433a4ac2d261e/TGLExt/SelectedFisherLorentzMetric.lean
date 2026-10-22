-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — LOTE 063..066 (09/09/2026, noite), transposta em 10/09/2026 (ENTREGA_067 = elo do lote)
-- Os 21 modulos restantes da bancada (elos 83 -> 93 -> 98 da cadeia de copias integradas; 77 ja na v338).
--   063 (6 modulos, 113 teoremas): RESPOSTA GIBBS ANTES DA FONTE — protocolo misto (W = X + Z, medicao Z, s = v^2 t^2):
--     igualdade das respostas de entropia e energia de referencia na ordem quadratica; a fonte calculada da resposta com
--     conservacao por closed/wave; o seletor transporta o registro; O LIMITE LOCAL DE INTERACOES EXTENSIVAS (Lean);
--     a lei fisica de area e a metrica seguem entradas. [DERIVED, escrito]: Araki/GNS, tempo global, KMS no fecho C*.
--   065 (10 modulos, 108 teoremas): estabilidade do prefixo do caracter, resolucao finita, controle de malha do
--     registro, cotas de erro da resposta finita, precisao finita de Gibbs misto, janela de amostragem; METRICA DE
--     FISHER-LORENTZ SELECIONADA, variacao da densidade de materia escalar, ponte Fisher-Gibbs, CONSERVACAO sigma.
--   066 (5 modulos, 67 teoremas): sigma DOS MESMOS P (phi_j = sqrt(P_j/(1 - P_s))), resposta de Gibbs ASSINADA (dois
--     sinais com probabilidades positivas), esperanca negativa renormalizada, cobertura, reconstrucao por DEZ LIMITES
--     (SignedGibbsFiniteRecord); T e entrada; nao se identifica o observavel com stress de QFT.
--   Estatuto: [REAL] o compilado; [INPUT] a lei de area, a metrica, T, a acao/particao; [DERIVED + KNOWN] Araki, GNS,
--   KMS C*; [OPEN] correspondencia geral de selecao/materia/protocolo/area, realizacao interagente, anomalias, UV.
--   As ENTREGAS 067..087 sao MATEMATICA ESCRITA REVISADA (CAS, sem Lean) — registradas no diario e no Atlas como
--   [DERIVED], nao como flags; a propria bancada: "nao promover demonstracoes escritas a flags de compilacao".
-- Auditoria da gerencia (sessao d554e796, 10/09/2026): lote montado da CADEIA de recibos (98 -> 93 -> 83 -> 77...),
--   77 ja no kernel pulados; 21/21 hashes lidos dos bytes; zero proibidos; guarda de colisao; recompilacao INDEPENDENTE
--   21/21 contra o kernel v338, axiomas no trio; a copia integrada da bancada NAO foi usada (so as fontes congeladas).
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.FisherInformationTensor
import TGLExt.GeneralAngularTensorCodec
import TGLExt.GeneralMetricEinstein
import Mathlib.Analysis.Matrix.Order

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.SelectedFisher
open Matrix TGLExt ChatgptAudit ChatgptAudit.FisherField
open ChatgptAudit.Coherent023 ChatgptAudit.AngularTensorCodec
open ChatgptAudit.GeneralMetric ChatgptAudit.Micro021
open scoped MatrixOrder ContDiff
noncomputable section

/-- A signed reading of a positive information tensor, with a selected covector. -/
def reflectedMetric (F : Tensor4) (c : Coordinate4) : Tensor4 :=
  (2 / tensorQuad F⁻¹ c) • vecMulVec c c - F

def reflectedInverse (F : Tensor4) (c : Coordinate4) : Tensor4 :=
  (2 / tensorQuad F⁻¹ c) • vecMulVec (F⁻¹ *ᵥ c) (F⁻¹ *ᵥ c) - F⁻¹

theorem positive_gram_factor (F : Tensor4) (hF : F.PosDef) :
    ∃ B : Tensor4, IsUnit B.det ∧ Bᵀ * B = F := by
  obtain ⟨B, hB⟩ := CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hF.posSemidef.nonneg
  have hb : Bᵀ * B = F := by simpa only [Matrix.star_eq_conjTranspose, Matrix.conjTranspose_eq_transpose_of_trivial] using hB.symm
  refine ⟨B, ?_, hb⟩
  apply isUnit_iff_ne_zero.mpr
  intro hz
  have hh := congrArg Matrix.det hb
  rw [Matrix.det_mul, Matrix.det_transpose, hz, zero_mul] at hh
  exact (ne_of_gt hF.det_pos) hh.symm

/-- An explicit orthogonal reflection whose first row is a prescribed unit vector. -/
theorem unit_vector_frame (z : Coordinate4) (hz : z ⬝ᵥ z = 1) :
    ∃ Q : Tensor4, Qᵀ * Q = 1 ∧ Q 0 = z := by
  let e : Coordinate4 := Pi.single 0 1
  let w : Coordinate4 := e-z
  have hez : e ⬝ᵥ z = z 0 := by norm_num [e, dotProduct, Fin.sum_univ_four, Pi.single_apply]
  have hze : z ⬝ᵥ e = z 0 := by norm_num [e, dotProduct, Fin.sum_univ_four, Pi.single_apply]
  have hee : e ⬝ᵥ e = 1 := by norm_num [e, dotProduct, Fin.sum_univ_four, Pi.single_apply]
  have hw : w ⬝ᵥ w = 2*(1-z 0) := by
    dsimp [w]
    rw [sub_dotProduct, dotProduct_sub, dotProduct_sub, hee, hez, hze, hz]
    ring
  by_cases hzero : 1-z 0=0
  · have hww : w ⬝ᵥ w=0 := by rw [hw,hzero,mul_zero]
    have hw0 : w=0 := dotProduct_self_eq_zero.mp hww
    have he : e=z := sub_eq_zero.mp hw0
    refine ⟨1, by simp, ?_⟩
    rw [←he]
    ext j
    simp [e, Matrix.one_apply, Pi.single_apply, eq_comm]
  · let k : ℝ := 1/(1-z 0)
    let W : Tensor4 := vecMulVec w w
    let Q : Tensor4 := 1-k • W
    have hWW : W*W=(w ⬝ᵥ w) • W := by
      simp [W, Matrix.vecMulVec_mul_vecMulVec]
    have hWT : Wᵀ=W := Matrix.transpose_vecMulVec _ _
    have hQT : Qᵀ=Q := by simp [Q,hWT]
    have hQ : Qᵀ*Q=1 := by
      rw [hQT]
      dsimp [Q]
      rw [sub_mul, mul_sub, mul_sub, one_mul, mul_one, one_mul,
        Matrix.smul_mul, Matrix.mul_smul, hWW, smul_smul, smul_smul]
      have hk : k*k*(w ⬝ᵥ w)=k+k := by rw [hw]; dsimp [k]; field_simp; ring
      rw [hk, add_smul]
      abel
    refine ⟨Q,hQ,?_⟩
    ext j
    have hw0 : w 0=1-z 0 := by simp [w,e]
    change (1:Tensor4) 0 j-k*(w 0*w j)=z j
    rw [hw0]
    have hk0 : k*(1-z 0)=1 := by dsimp [k]; field_simp
    rw [←mul_assoc,hk0,one_mul]
    have hident : (1:Tensor4) 0 j=e j := by simp [e, Matrix.one_apply, Pi.single_apply, eq_comm]
    rw [hident]
    simp [w]

theorem eta_congruence_by_first_row (E : Tensor4) :
    Eᵀ * eta4 * E = (2:ℝ) • vecMulVec (E 0) (E 0) - Eᵀ*E := by
  ext i j
  norm_num [Matrix.mul_apply, Matrix.transpose_apply, eta4, Fin.sum_univ_four,
    Matrix.vecMulVec, Matrix.sub_apply, Matrix.smul_apply, Matrix.diagonal_apply,
    Matrix.cons_val_two, Matrix.cons_val_three, Matrix.head_cons, Matrix.tail_cons]
  ring

theorem reflected_metric_symmetric (F : Tensor4) (c : Coordinate4) (hF : Fᵀ=F) :
    (reflectedMetric F c)ᵀ=reflectedMetric F c := by
  simp [reflectedMetric, Matrix.transpose_vecMulVec, hF]

theorem clock_norm_positive (F : Tensor4) (hF : F.PosDef)
    (c : Coordinate4) (hc : c≠0) : 0<tensorQuad F⁻¹ c := by
  simpa only [tensorQuad, star_trivial] using hF.inv.dotProduct_mulVec_pos hc

theorem reflected_metric_lorentz (F : Tensor4) (hF : F.PosDef)
    (c : Coordinate4) (hc : c≠0) : LorentzByCongruence (reflectedMetric F c) := by
  obtain ⟨B,hB,hBF⟩ := positive_gram_factor F hF
  let D := B⁻¹
  have hDB : D*B=1 := Matrix.nonsing_inv_mul B hB
  have hBD : B*D=1 := Matrix.mul_nonsing_inv B hB
  have hi : F⁻¹=D*Dᵀ := by rw [←hBF, Matrix.mul_inv_rev, Matrix.transpose_nonsing_inv]
  let w : Coordinate4 := Dᵀ*ᵥc
  have hcB : Bᵀ*ᵥw=c := by
    dsimp [w]
    rw [Matrix.mulVec_mulVec, ←Matrix.transpose_mul, hDB, Matrix.transpose_one, Matrix.one_mulVec]
  let a : ℝ := tensorQuad F⁻¹ c
  have ha : 0<a := clock_norm_positive F hF c hc
  have hw : w ⬝ᵥ w=a := by
    dsimp [a,tensorQuad,w]
    rw [hi, ←Matrix.mulVec_mulVec, dotProduct_mulVec, ←Matrix.mulVec_transpose]
    simp only [Matrix.transpose_transpose, dotProduct_comm]
  let z : Coordinate4 := (Real.sqrt a)⁻¹ • w
  have hs : Real.sqrt a≠0 := ne_of_gt (Real.sqrt_pos.2 ha)
  have hz : z ⬝ᵥ z=1 := by
    dsimp [z]
    rw [smul_dotProduct, dotProduct_smul, hw]
    simp only [smul_eq_mul]
    field_simp
    exact (Real.sq_sqrt ha.le).symm
  obtain ⟨Q,hQ,hQ0⟩ := unit_vector_frame z hz
  let E := Q*B
  have hEE : Eᵀ*E=F := by
    dsimp [E]
    rw [Matrix.transpose_mul]
    calc Bᵀ*Qᵀ*(Q*B)=Bᵀ*(Qᵀ*Q)*B := by noncomm_ring
         _ = F := by rw [hQ,mul_one,hBF]
  have hE0 : E 0=(Real.sqrt a)⁻¹ • c := by
    calc E 0 = Q 0 ᵥ* B := rfl
         _ = z ᵥ* B := by rw [hQ0]
         _ = (Real.sqrt a)⁻¹ • c := by
           dsimp [z]
           rw [Matrix.smul_vecMul, ←Matrix.mulVec_transpose, hcB]
  have hEd : IsUnit E.det := by
    apply isUnit_iff_ne_zero.mpr
    intro hzE
    have hh := congrArg Matrix.det hEE
    rw [Matrix.det_mul, Matrix.det_transpose, hzE, zero_mul] at hh
    exact (ne_of_gt hF.det_pos) hh.symm
  refine ⟨E,hEd,?_⟩
  rw [eta_congruence_by_first_row,hEE,hE0]
  ext i j
  simp only [reflectedMetric, Matrix.sub_apply, Matrix.smul_apply,
    Matrix.vecMulVec, Matrix.of_apply, Pi.smul_apply, smul_eq_mul]
  change 2/(a)*(c i*c j)-F i j=2*((Real.sqrt a)⁻¹*c i*((Real.sqrt a)⁻¹*c j))-F i j
  congr 1
  field_simp
  rw [Real.sq_sqrt ha.le]
  ring

theorem reflected_inverse_right (F : Tensor4) (hF : F.PosDef)
    (c : Coordinate4) (hc : c≠0) : reflectedMetric F c * reflectedInverse F c = 1 := by
  let a : ℝ := tensorQuad F⁻¹ c
  let k : ℝ := 2/a
  let v : Coordinate4 := F⁻¹ *ᵥ c
  have ha : a≠0 := ne_of_gt (clock_norm_positive F hF c hc)
  have hFi : F*F⁻¹=1 := Matrix.mul_nonsing_inv F (isUnit_iff_ne_zero.mpr (ne_of_gt hF.det_pos))
  have hFv : F*ᵥv=c := by dsimp [v]; rw [Matrix.mulVec_mulVec,hFi,Matrix.one_mulVec]
  have hsym : (F⁻¹)ᵀ=F⁻¹ := by
    simpa only [Matrix.IsHermitian, Matrix.conjTranspose_eq_transpose_of_trivial] using hF.inv.isHermitian
  have hcv : c ᵥ*F⁻¹=v := by rw [←Matrix.mulVec_transpose,hsym]
  have hdot : c ⬝ᵥ v=a := rfl
  change (k • vecMulVec c c-F)*(k • vecMulVec v v-F⁻¹)=1
  rw [sub_mul,mul_sub,mul_sub,Matrix.smul_mul,Matrix.mul_smul,
    Matrix.vecMulVec_mul_vecMulVec,Matrix.vecMulVec_smul,hdot,
    Matrix.smul_mul,Matrix.vecMulVec_mul,hcv,Matrix.mul_smul,Matrix.mul_vecMulVec,hFv,hFi]
  ext i j
  simp only [Matrix.sub_apply,Matrix.smul_apply,smul_eq_mul,smul_smul,Matrix.vecMulVec_apply]
  dsimp [k]
  field_simp
  ring

theorem reflected_inverse_eq (F : Tensor4) (hF : F.PosDef)
    (c : Coordinate4) (hc : c≠0) : reflectedInverse F c=(reflectedMetric F c)⁻¹ := by
  have hm := reflected_metric_lorentz F hF c hc
  have hl : (reflectedMetric F c)⁻¹*reflectedMetric F c=1 :=
    Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr
      (ne_of_lt (lorentz_metric_det_negative _ hm)))
  calc reflectedInverse F c = 1*reflectedInverse F c := (one_mul _).symm
       _ = ((reflectedMetric F c)⁻¹*reflectedMetric F c)*reflectedInverse F c := by rw [hl]
       _ = (reflectedMetric F c)⁻¹ := by rw [mul_assoc,reflected_inverse_right F hF c hc,mul_one]

theorem reflected_inverse_left (F : Tensor4) (hF : F.PosDef)
    (c : Coordinate4) (hc : c≠0) : reflectedInverse F c*reflectedMetric F c=1 := by
  rw [reflected_inverse_eq F hF c hc]
  exact Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr
    (ne_of_lt (lorentz_metric_det_negative _ (reflected_metric_lorentz F hF c hc))))

theorem smooth_positive_inverse (U : Set Coordinate4) (F : TensorField4)
    (hF : SmoothMatrixOn U F) (hp : ∀ x∈U, (F x).PosDef) :
    SmoothMatrixOn U (fun x => (F x)⁻¹) := by
  have hd := (smooth_metric_determinant U F hF).inv
    (fun x hx => ne_of_gt (hp x hx).det_pos)
  have ha := smooth_metric_adjugate U F hF
  intro i j
  simpa only [Matrix.inv_def,Ring.inverse_eq_inv',Matrix.smul_apply,smul_eq_mul] using hd.mul (ha i j)

theorem smooth_clock_square (U : Set Coordinate4) (F : TensorField4) (c : CovectorField4)
    (hF : SmoothMatrixOn U F) (hc : SmoothVectorOn U c) :
    ContDiffOn ℝ ∞ (fun x => tensorQuad (F x) (c x)) U := by
  change ContDiffOn ℝ ∞ (fun x => ∑ i, c x i * (∑ j, F x i j*c x j)) U
  apply ContDiffOn.sum
  intro i _
  apply (hc i).mul
  apply ContDiffOn.sum
  intro j _
  exact (hF i j).mul (hc j)

theorem reflected_metric_smooth (U : Set Coordinate4) (F : TensorField4) (c : CovectorField4)
    (hF : SmoothMatrixOn U F) (hc : SmoothVectorOn U c)
    (hp : ∀ x∈U, (F x).PosDef) (hn : ∀ x∈U, c x≠0) :
    SmoothMatrixOn U (fun x => reflectedMetric (F x) (c x)) := by
  have hi := smooth_positive_inverse U F hF hp
  have ha := smooth_clock_square U (fun x => (F x)⁻¹) c hi hc
  have hk : ContDiffOn ℝ ∞ (fun x => 2/tensorQuad (F x)⁻¹ (c x)) U :=
    contDiffOn_const.div ha (fun x hx => ne_of_gt (clock_norm_positive _ (hp x hx) _ (hn x hx)))
  intro i j
  exact (hk.mul ((hc i).mul (hc j))).sub (hF i j)

/-- Probability observations and their rank/clock certificates. No metric is stored. -/
structure SelectedProbabilityData (ι : Type) [Fintype ι] (U : Set Coordinate4) where
  probabilities : Coordinate4 → ι → ℝ
  normalized : ∀ x, ∑ i, probabilities x i=1
  positive : ∀ x∈U, ∀ i, 0<probabilities x i
  smooth : ∀ i, ContDiffOn ℝ ∞ (fun x => probabilities x i) U
  differential_injective : ∀ x∈U, Function.Injective (directionalVariation probabilities x)
  selected : ι
  clock_nonzero : ∀ x∈U, probabilityDifferential probabilities x selected≠0

variable {ι : Type} [Fintype ι] {U : Set Coordinate4}

def selectedFisher (P : SelectedProbabilityData ι U) : TensorField4 :=
  fisherTensorField P.probabilities

def selectedClock (P : SelectedProbabilityData ι U) : CovectorField4 :=
  fun x => probabilityDifferential P.probabilities x P.selected

def selectedMetric (P : SelectedProbabilityData ι U) : TensorField4 :=
  fun x => reflectedMetric (selectedFisher P x) (selectedClock P x)

theorem selected_fisher_positive (P : SelectedProbabilityData ι U) (x : Coordinate4) (hx : x∈U) :
    (selectedFisher P x).PosDef := by
  apply Matrix.PosDef.of_dotProduct_mulVec_pos
  · simpa only [selectedFisher,Matrix.IsHermitian,Matrix.conjTranspose_eq_transpose_of_trivial] using
      fisher_field_symmetric P.probabilities x
  · intro v hv
    change 0<tensorQuad (fisherTensorField P.probabilities x) v
    apply (fisher_tensor_positive_iff _ _ (P.positive x hx) v).2
    intro hz
    apply hv
    apply P.differential_injective x hx
    change directionalVariation P.probabilities x v=directionalVariation P.probabilities x 0
    change directionalVariation P.probabilities x v=0 at hz
    rw [hz]
    ext i
    change (0:ℝ)=covectorRead (probabilityDifferential P.probabilities x i) (0:Coordinate4)
    simp [covectorRead,dotProduct]

theorem selected_metric_lorentz (P : SelectedProbabilityData ι U) (x : Coordinate4) (hx : x∈U) :
    LorentzByCongruence (selectedMetric P x) :=
  reflected_metric_lorentz _ (selected_fisher_positive P x hx) _ (P.clock_nonzero x hx)

theorem selected_clock_smooth (P : SelectedProbabilityData ι U) (hU : IsOpen U) :
    SmoothVectorOn U (selectedClock P) := by
  intro i
  exact coordinatePartial_smooth U hU _ (P.smooth P.selected) i

theorem selected_metric_smooth (P : SelectedProbabilityData ι U) (hU : IsOpen U) :
    SmoothMatrixOn U (selectedMetric P) :=
  reflected_metric_smooth U (selectedFisher P) (selectedClock P)
    (fisher_field_smooth U hU P.probabilities P.smooth P.positive)
    (selected_clock_smooth P hU) (selected_fisher_positive P) P.clock_nonzero

theorem selected_metric_inverse (P : SelectedProbabilityData ι U) (x : Coordinate4) (hx : x∈U) :
    (selectedMetric P x)⁻¹=reflectedInverse (selectedFisher P x) (selectedClock P x) :=
  (reflected_inverse_eq _ (selected_fisher_positive P x hx) _ (P.clock_nonzero x hx)).symm

theorem selected_metric_inverse_smooth (P : SelectedProbabilityData ι U) (hU : IsOpen U) :
    SmoothMatrixOn U (metricInverse (selectedMetric P)) :=
  constructed_metric_inverse_smooth U (selectedMetric P) (selected_metric_smooth P hU)
    (selected_metric_lorentz P)

/-- The existing codec is only an output adapter for the metric already derived from P. -/
def selectedLorentzRecord (P : SelectedProbabilityData ι U) (hU : IsOpen U) :
    LorentzProbabilityRecord U :=
  encodeLorentzRecord U (selectedMetric P) (selected_metric_smooth P hU) (selected_metric_lorentz P)

theorem selected_record_decodes_derived_metric (P : SelectedProbabilityData ι U) (hU : IsOpen U) :
    decodeRecord (selectedLorentzRecord P hU).data=selectedMetric P :=
  decode_encoded_record U (selectedMetric P) (selected_metric_smooth P hU)

/-- The same observations have a normalized actual diagonal curve along each coordinate line. -/
theorem selected_probability_curve_fisher (P : SelectedProbabilityData ι U) (hU : IsOpen U)
    (x v : Coordinate4) (hx : x∈U) :
    diagonalFisher (P.probabilities x)
      ((probabilityFieldCurve U hU P.probabilities P.smooth P.normalized x v hx).tangent 0) =
      tensorQuad (selectedFisher P x) v :=
  probability_field_curve_fisher U hU P.probabilities P.smooth P.normalized x v hx

theorem zero_clock_control (F : Tensor4) : reflectedMetric F 0 = -F := by
  simp [reflectedMetric]


#print axioms reflectedMetric
#print axioms reflectedInverse
#print axioms positive_gram_factor
#print axioms unit_vector_frame
#print axioms eta_congruence_by_first_row
#print axioms reflected_metric_symmetric
#print axioms clock_norm_positive
#print axioms reflected_metric_lorentz
#print axioms reflected_inverse_right
#print axioms reflected_inverse_eq
#print axioms reflected_inverse_left
#print axioms smooth_positive_inverse
#print axioms smooth_clock_square
#print axioms reflected_metric_smooth
#print axioms SelectedProbabilityData
#print axioms selectedFisher
#print axioms selectedClock
#print axioms selectedMetric
#print axioms selected_fisher_positive
#print axioms selected_metric_lorentz
#print axioms selected_clock_smooth
#print axioms selected_metric_smooth
#print axioms selected_metric_inverse
#print axioms selected_metric_inverse_smooth
#print axioms selectedLorentzRecord
#print axioms selected_record_decodes_derived_metric
#print axioms selected_probability_curve_fisher
#print axioms zero_clock_control
end
end ChatgptAudit.SelectedFisher
