import TGLExt.F1Fecho394.CanonicalTensorMultiplierR3
import TGLExt.F1Fecho394.ScalarL2ImaginaryR5
/-! Scalar identity for the actual second-quantized resolvent; no false
second-quantized square-sum normalization is used. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
open MeasureTheory
namespace F1Fecho.TensorCoordinates
open ChatgptAudit.Continuous049

def realProduct (w:ℝ→ℝ) : (n:ℕ)→(data n).Index→ℝ
  | 0 => w
  | n+1 => fun p=>w p.2*realProduct w n p.1

lemma realProduct_pos (w:ℝ→ℝ) (hw:∀x,0<w x) (n:ℕ) (p:(data n).Index) :
    0<realProduct w n p := by
  induction n with
  | zero => exact hw p
  | succ n ih => exact mul_pos (hw p.2) (ih p.1)

lemma productWeight_ofReal (w:ℝ→ℝ) (n:ℕ) (p:(data n).Index) :
    productWeight (fun x=>(w x:ℂ)) n p=(realProduct w n p:ℂ) := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [productWeight,realProduct,ih,Complex.ofReal_mul]

lemma product_ratio (c:ℝ) (n:ℕ) (p:(data n).Index) :
    realProduct (spectralWeightB c) n p=Real.exp (-c*rapiditySum n p)*
      realProduct (spectralWeightA c) n p := by
  induction n with
  | zero => exact spectral_weight_ratio c p
  | succ n ih =>
    change spectralWeightB c p.2*realProduct (spectralWeightB c) n p.1=_
    rw [spectral_weight_ratio,ih]
    change _=Real.exp (-c*(p.2+rapiditySum n p.1))*
      (spectralWeightA c p.2*realProduct (spectralWeightA c) n p.1)
    rw [mul_add,Real.exp_add]
    ring

def sumEnergy (c:ℝ) (n:ℕ) (p:(data n).Index) : ℝ := -2*c*rapiditySum n p
lemma sumEnergy_measurable (c:ℝ) (n:ℕ) : Measurable (sumEnergy c n) :=
  (rapiditySum_measurable n).const_mul _

def tensorR (c:ℝ) (n:ℕ) : Space n→L[ℂ]Space n :=
  ScalarL2Spectral.R (data n).measure (sumEnergy c n) (sumEnergy_measurable c n)

lemma tensorR_ae (c:ℝ) (n:ℕ) (x:Space n) :
    tensorR c n x=ᵐ[(data n).measure] fun p=>(Real.sigmoid (-sumEnergy c n p):ℂ)•x p :=
  ScalarL2.op_ae _ _ _

lemma scalar_resolvent_identity (c:ℝ) (n:ℕ) (p:(data n).Index) :
    (productWeight (weightA c) n p*productWeight (weightA c) n p+
      productWeight (weightB c) n p*productWeight (weightB c) n p)*
      (Real.sigmoid (-sumEnergy c n p):ℂ)=
      productWeight (weightA c) n p*productWeight (weightA c) n p := by
  have hA : productWeight (weightA c) n p=(realProduct (spectralWeightA c) n p:ℂ) :=
    productWeight_ofReal (spectralWeightA c) n p
  have hB : productWeight (weightB c) n p=(realProduct (spectralWeightB c) n p:ℂ) :=
    productWeight_ofReal (spectralWeightB c) n p
  rw [hA,hB]
  norm_cast
  rw [product_ratio]
  unfold sumEnergy Real.sigmoid
  have he : Real.exp (-(c*rapiditySum n p))^2=Real.exp (-(c*rapiditySum n p*2)) := by
    rw [pow_two,←Real.exp_add]
    congr 1
    ring
  field_simp
  rw [he]

lemma scalar_coefficient_nonzero (c:ℝ) (n:ℕ) (p:(data n).Index) :
    productWeight (weightA c) n p*productWeight (weightA c) n p+
      productWeight (weightB c) n p*productWeight (weightB c) n p≠0 := by
  have hA : productWeight (weightA c) n p=(realProduct (spectralWeightA c) n p:ℂ) :=
    productWeight_ofReal (spectralWeightA c) n p
  have hB : productWeight (weightB c) n p=(realProduct (spectralWeightB c) n p:ℂ) :=
    productWeight_ofReal (spectralWeightB c) n p
  rw [hA,hB]
  norm_cast
  have ha:=realProduct_pos (spectralWeightA c) (spectral_weightA_pos c) n p
  have hb:=realProduct_pos (spectralWeightB c) (spectral_weightB_pos c) n p
  positivity

end F1Fecho.TensorCoordinates
#print axioms F1Fecho.TensorCoordinates.product_ratio
#print axioms F1Fecho.TensorCoordinates.scalar_resolvent_identity
#print axioms F1Fecho.TensorCoordinates.scalar_coefficient_nonzero
