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
import TGLExt.TheSelectionIsTheBallast
import TGLExt.SmoothMatrixCalculus
import TGLExt.TensorNullCone
import Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.InverseDeriv
import Mathlib.Analysis.SpecialFunctions.Sqrt

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit.AngularTensorCodec
open Matrix Set TGLExt ChatgptAudit
open scoped ContDiff
noncomputable section

/-- A real component is mapped to an angle in the open first quadrant. -/
def encodeAngle (x : ℝ) : ℝ := (Real.arctan x + Real.pi / 2) / 2

/-- The stored scalar is a probability, not the real component itself. -/
def encodeScalar (x : ℝ) : ℝ := Real.sin (encodeAngle x) ^ 2

/-- Decoding explicitly consumes the canonical selection angle. -/
def decodeScalar (p : ℝ) : ℝ := Real.tan (2 * selectionAngle p - Real.pi / 2)

theorem encode_angle_interior (x : ℝ) :
    0 < encodeAngle x ∧ encodeAngle x < Real.pi / 2 := by
  unfold encodeAngle
  constructor <;> linarith [Real.neg_pi_div_two_lt_arctan x,
    Real.arctan_lt_pi_div_two x, Real.pi_pos]

theorem encode_scalar_interior (x : ℝ) :
    0 < encodeScalar x ∧ encodeScalar x < 1 := by
  obtain ⟨h0, h1⟩ := encode_angle_interior x
  have hs : 0 < Real.sin (encodeAngle x) :=
    Real.sin_pos_of_pos_of_lt_pi h0 (by linarith [Real.pi_pos])
  have hc : 0 < Real.cos (encodeAngle x) :=
    Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], h1⟩
  unfold encodeScalar
  constructor
  · positivity
  · nlinarith [Real.sin_sq_add_cos_sq (encodeAngle x), sq_pos_of_pos hc]

theorem selection_angle_on_encoded_scalar (x : ℝ) :
    selectionAngle (encodeScalar x) = encodeAngle x := by
  obtain ⟨h0, h1⟩ := encode_angle_interior x
  have hs : 0 ≤ Real.sin (encodeAngle x) :=
    le_of_lt (Real.sin_pos_of_pos_of_lt_pi h0 (by linarith [Real.pi_pos]))
  unfold selectionAngle encodeScalar
  rw [Real.sqrt_sq hs]
  exact Real.arcsin_sin (by linarith [Real.pi_pos]) h1.le

theorem decode_encode_scalar (x : ℝ) : decodeScalar (encodeScalar x) = x := by
  unfold decodeScalar
  rw [selection_angle_on_encoded_scalar]
  have h : 2 * encodeAngle x - Real.pi / 2 = Real.arctan x := by
    unfold encodeAngle
    ring
  rw [h, Real.tan_arctan]

theorem selection_angle_interior {p : ℝ} (h0 : 0 < p) (h1 : p < 1) :
    0 < selectionAngle p ∧ selectionAngle p < Real.pi / 2 := by
  have hs : Real.sqrt p < 1 := by
    nlinarith [Real.sq_sqrt h0.le, Real.sqrt_nonneg p]
  exact ⟨Real.arcsin_pos.mpr (Real.sqrt_pos.mpr h0),
    Real.arcsin_lt_pi_div_two.mpr hs⟩

theorem decoded_argument_interior {p : ℝ} (h0 : 0 < p) (h1 : p < 1) :
    -(Real.pi / 2) < 2 * selectionAngle p - Real.pi / 2 ∧
    2 * selectionAngle p - Real.pi / 2 < Real.pi / 2 := by
  obtain ⟨ha, hb⟩ := selection_angle_interior h0 h1
  constructor <;> linarith

theorem encode_angle_on_decoded_scalar {p : ℝ} (h0 : 0 < p) (h1 : p < 1) :
    encodeAngle (decodeScalar p) = selectionAngle p := by
  obtain ⟨ha, hb⟩ := decoded_argument_interior h0 h1
  unfold encodeAngle decodeScalar
  rw [Real.arctan_tan ha hb]
  ring

theorem encode_decode_scalar {p : ℝ} (h0 : 0 < p) (h1 : p < 1) :
    encodeScalar (decodeScalar p) = p := by
  unfold encodeScalar
  rw [encode_angle_on_decoded_scalar h0 h1]
  exact selection_angle_reflection h0.le h1.le

theorem encode_scalar_injective : Function.Injective encodeScalar := by
  intro x y h
  simpa only [decode_encode_scalar] using congrArg decodeScalar h

theorem decode_scalar_injective_on : Set.InjOn decodeScalar (Set.Ioo 0 1) := by
  intro p hp q hq h
  simpa only [encode_decode_scalar hp.1 hp.2, encode_decode_scalar hq.1 hq.2]
    using congrArg encodeScalar h

theorem encode_angle_smooth : ContDiff ℝ ∞ encodeAngle := by
  unfold encodeAngle
  exact (Real.contDiff_arctan.add contDiff_const).div_const 2

theorem encode_scalar_smooth : ContDiff ℝ ∞ encodeScalar := by
  exact encode_angle_smooth.sin.pow 2

theorem selection_angle_smooth_at {p : ℝ} (h0 : 0 < p) (h1 : p < 1) :
    ContDiffAt ℝ ∞ selectionAngle p := by
  have hs : Real.sqrt p < 1 := by
    nlinarith [Real.sq_sqrt h0.le, Real.sqrt_nonneg p]
  have ha : Real.sqrt p ≠ -1 := by linarith [Real.sqrt_nonneg p]
  have hb : Real.sqrt p ≠ 1 := ne_of_lt hs
  exact (Real.contDiffAt_arcsin ha hb).comp p
    (Real.contDiffAt_sqrt (ne_of_gt h0))

theorem decode_scalar_smooth_at {p : ℝ} (h0 : 0 < p) (h1 : p < 1) :
    ContDiffAt ℝ ∞ decodeScalar p := by
  have hi : ContDiffAt ℝ ∞
      (fun q => 2 * selectionAngle q - Real.pi / 2) p :=
    (contDiffAt_const.mul (selection_angle_smooth_at h0 h1)).sub contDiffAt_const
  have hc : Real.cos (2 * selectionAngle p - Real.pi / 2) ≠ 0 :=
    ne_of_gt (Real.cos_pos_of_mem_Ioo (decoded_argument_interior h0 h1))
  exact (Real.contDiffAt_tan.mpr hc).comp p hi

theorem decode_scalar_smooth : ContDiffOn ℝ ∞ decodeScalar (Set.Ioo 0 1) := by
  intro p hp
  exact (decode_scalar_smooth_at hp.1 hp.2).contDiffWithinAt

/-- Entrywise encoding applies to arbitrary real matrix sizes. -/
def encodeMatrix {m n : Type} (A : Matrix m n ℝ) : Matrix m n ℝ :=
  fun i j => encodeScalar (A i j)

def decodeMatrix {m n : Type} (P : Matrix m n ℝ) : Matrix m n ℝ :=
  fun i j => decodeScalar (P i j)

theorem decode_encode_matrix {m n : Type} (A : Matrix m n ℝ) :
    decodeMatrix (encodeMatrix A) = A := by
  funext i j
  exact decode_encode_scalar (A i j)

theorem encode_decode_matrix {m n : Type} (P : Matrix m n ℝ)
    (hP : ∀ i j, 0 < P i j ∧ P i j < 1) :
    encodeMatrix (decodeMatrix P) = P := by
  funext i j
  exact encode_decode_scalar (hP i j).1 (hP i j).2

theorem encode_matrix_interior {m n : Type} (A : Matrix m n ℝ) :
    ∀ i j, 0 < encodeMatrix A i j ∧ encodeMatrix A i j < 1 := by
  intro i j
  exact encode_scalar_interior (A i j)

theorem encode_matrix_injective {m n : Type} :
    Function.Injective (@encodeMatrix m n) := by
  intro A B h
  simpa only [decode_encode_matrix] using congrArg decodeMatrix h

theorem encode_matrix_symmetric_iff {n : Type} (A : Matrix n n ℝ) :
    (encodeMatrix A)ᵀ = encodeMatrix A ↔ Aᵀ = A := by
  constructor
  · intro h
    apply encode_matrix_injective
    exact h
  · intro h
    change encodeMatrix Aᵀ = encodeMatrix A
    exact congrArg encodeMatrix h

/-- Fields are encoded in the fixed coordinate chart used by the geometric kernel. -/
def encodeTensorField (g : TensorField4) : TensorField4 :=
  fun x => encodeMatrix (g x)

def decodeTensorField (P : TensorField4) : TensorField4 :=
  fun x => decodeMatrix (P x)

theorem decode_encode_tensor_field (g : TensorField4) :
    decodeTensorField (encodeTensorField g) = g := by
  funext x
  exact decode_encode_matrix (g x)

theorem encode_decode_tensor_field_on (U : Set Coordinate4) (P : TensorField4)
    (hP : ∀ x ∈ U, ∀ i j, 0 < P x i j ∧ P x i j < 1) :
    Set.EqOn (encodeTensorField (decodeTensorField P)) P U := by
  intro x hx
  exact encode_decode_matrix (P x) (hP x hx)

theorem encode_tensor_field_interior (g : TensorField4) :
    ∀ x i j, 0 < encodeTensorField g x i j ∧ encodeTensorField g x i j < 1 := by
  intro x i j
  exact encode_scalar_interior (g x i j)

theorem encode_tensor_field_injective : Function.Injective encodeTensorField := by
  intro g h heq
  simpa only [decode_encode_tensor_field] using congrArg decodeTensorField heq

theorem encode_tensor_field_smooth (U : Set Coordinate4) (g : TensorField4)
    (hg : SmoothMatrixOn U g) : SmoothMatrixOn U (encodeTensorField g) := by
  intro i j
  exact encode_scalar_smooth.comp_contDiffOn (hg i j)

theorem decode_tensor_field_smooth (U : Set Coordinate4) (P : TensorField4)
    (hP : SmoothMatrixOn U P)
    (hI : ∀ x ∈ U, ∀ i j, 0 < P x i j ∧ P x i j < 1) :
    SmoothMatrixOn U (decodeTensorField P) := by
  intro i j
  exact decode_scalar_smooth.comp (hP i j) (fun x hx => hI x hx i j)

/-- Only probabilities and their analytic certificates are stored. -/
structure ProbabilityFieldRecord (U : Set Coordinate4) where
  probabilities : TensorField4
  interior : ∀ x ∈ U, ∀ i j,
    0 < probabilities x i j ∧ probabilities x i j < 1
  smooth : SmoothMatrixOn U probabilities

def decodeRecord {U : Set Coordinate4} (R : ProbabilityFieldRecord U) : TensorField4 :=
  decodeTensorField R.probabilities

theorem decoded_record_smooth {U : Set Coordinate4} (R : ProbabilityFieldRecord U) :
    SmoothMatrixOn U (decodeRecord R) :=
  decode_tensor_field_smooth U R.probabilities R.smooth R.interior

theorem decoded_record_reencodes {U : Set Coordinate4} (R : ProbabilityFieldRecord U) :
    Set.EqOn (encodeTensorField (decodeRecord R)) R.probabilities U :=
  encode_decode_tensor_field_on U R.probabilities R.interior

/-- This constructor certifies representability of a GIVEN field, not a measurement law. -/
def encodeFieldRecord (U : Set Coordinate4) (g : TensorField4)
    (hg : SmoothMatrixOn U g) : ProbabilityFieldRecord U where
  probabilities := encodeTensorField g
  interior := fun x _ i j => encode_tensor_field_interior g x i j
  smooth := encode_tensor_field_smooth U g hg

theorem decode_encoded_record (U : Set Coordinate4) (g : TensorField4)
    (hg : SmoothMatrixOn U g) : decodeRecord (encodeFieldRecord U g hg) = g :=
  decode_encode_tensor_field g

/-- Signature is an explicit certificate about decoded probabilities. No metric is stored. -/
structure LorentzProbabilityRecord (U : Set Coordinate4) where
  data : ProbabilityFieldRecord U
  lorentz : ∀ x ∈ U, LorentzByCongruence (decodeRecord data x)

def encodeLorentzRecord (U : Set Coordinate4) (g : TensorField4)
    (hg : SmoothMatrixOn U g) (hL : ∀ x ∈ U, LorentzByCongruence (g x)) :
    LorentzProbabilityRecord U where
  data := encodeFieldRecord U g hg
  lorentz := by
    intro x hx
    rw [decode_encoded_record]
    exact hL x hx

theorem lorentz_record_decodes_smooth_metric {U : Set Coordinate4}
    (R : LorentzProbabilityRecord U) :
    SmoothMatrixOn U (decodeRecord R.data) ∧
      ∀ x ∈ U, LorentzByCongruence (decodeRecord R.data x) :=
  ⟨decoded_record_smooth R.data, R.lorentz⟩

/-- Surjectivity onto all smooth Lorentz fields in this chart is representational only. -/
theorem every_smooth_lorentz_field_is_representable
    (U : Set Coordinate4) (g : TensorField4) (hg : SmoothMatrixOn U g)
    (hL : ∀ x ∈ U, LorentzByCongruence (g x)) :
    ∃ R : LorentzProbabilityRecord U, decodeRecord R.data = g := by
  exact ⟨encodeLorentzRecord U g hg hL, decode_encoded_record U g hg⟩

theorem same_probabilities_same_decoded_field {U : Set Coordinate4}
    (R S : ProbabilityFieldRecord U) (h : Set.EqOn R.probabilities S.probabilities U) :
    Set.EqOn (decodeRecord R) (decodeRecord S) U := by
  intro x hx
  exact congrArg decodeMatrix (h hx)

#print axioms encodeAngle
#print axioms encodeScalar
#print axioms decodeScalar
#print axioms encode_angle_interior
#print axioms encode_scalar_interior
#print axioms selection_angle_on_encoded_scalar
#print axioms decode_encode_scalar
#print axioms selection_angle_interior
#print axioms decoded_argument_interior
#print axioms encode_angle_on_decoded_scalar
#print axioms encode_decode_scalar
#print axioms encode_scalar_injective
#print axioms decode_scalar_injective_on
#print axioms encode_angle_smooth
#print axioms encode_scalar_smooth
#print axioms selection_angle_smooth_at
#print axioms decode_scalar_smooth_at
#print axioms decode_scalar_smooth
#print axioms encodeMatrix
#print axioms decodeMatrix
#print axioms decode_encode_matrix
#print axioms encode_decode_matrix
#print axioms encode_matrix_interior
#print axioms encode_matrix_injective
#print axioms encode_matrix_symmetric_iff
#print axioms encodeTensorField
#print axioms decodeTensorField
#print axioms decode_encode_tensor_field
#print axioms encode_decode_tensor_field_on
#print axioms encode_tensor_field_interior
#print axioms encode_tensor_field_injective
#print axioms encode_tensor_field_smooth
#print axioms decode_tensor_field_smooth
#print axioms ProbabilityFieldRecord
#print axioms decodeRecord
#print axioms decoded_record_smooth
#print axioms decoded_record_reencodes
#print axioms encodeFieldRecord
#print axioms decode_encoded_record
#print axioms LorentzProbabilityRecord
#print axioms encodeLorentzRecord
#print axioms lorentz_record_decodes_smooth_metric
#print axioms every_smooth_lorentz_field_is_representable
#print axioms same_probabilities_same_decoded_field

end
end ChatgptAudit.AngularTensorCodec
