import SchwartzMaxwellContinuousR3

/-! Real test tensors are a real subspace of the complex Schwartz test space.
Real/imaginary projections and decomposition are explicit; no wedge-support
or causal-locality conclusion follows from these algebraic identities. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open SchwartzMap

def tensorComponent (μ ν : Fin 4) : TensorValue →L[ℝ] ℂ :=
  (ContinuousLinearMap.proj ν : (Fin 4→ℂ) →L[ℝ] ℂ).comp
    (ContinuousLinearMap.proj μ)

def tensorRealPart : TensorValue →L[ℝ] TensorValue :=
  ContinuousLinearMap.pi (fun μ => ContinuousLinearMap.pi (fun ν =>
    (Complex.ofRealCLM.comp Complex.reCLM).comp (tensorComponent μ ν)))

def tensorImagPart : TensorValue →L[ℝ] TensorValue :=
  ContinuousLinearMap.pi (fun μ => ContinuousLinearMap.pi (fun ν =>
    (Complex.ofRealCLM.comp Complex.imCLM).comp (tensorComponent μ ν)))

def realPart (f : SchwartzTensor) : SchwartzTensor := SchwartzMap.postcompCLM tensorRealPart f

def imagPart (f : SchwartzTensor) : SchwartzTensor := SchwartzMap.postcompCLM tensorImagPart f

def IsRealTest (f : SchwartzTensor) : Prop := ∀ p μ ν,(f p μ ν).im=0

theorem realPart_apply (f : SchwartzTensor) (p : Spacetime) (μ ν : Fin 4) :
    realPart f p μ ν=((f p μ ν).re:ℂ) := rfl

theorem imagPart_apply (f : SchwartzTensor) (p : Spacetime) (μ ν : Fin 4) :
    imagPart f p μ ν=((f p μ ν).im:ℂ) := rfl

theorem realPart_real (f : SchwartzTensor) : IsRealTest (realPart f) := by
  intro p μ ν
  rw [realPart_apply]
  exact Complex.ofReal_im _

theorem imagPart_real (f : SchwartzTensor) : IsRealTest (imagPart f) := by
  intro p μ ν
  rw [imagPart_apply]
  exact Complex.ofReal_im _

theorem real_imag_decomposition (f : SchwartzTensor) : f=realPart f+Complex.I•imagPart f := by
  ext p μ ν
  change f p μ ν=realPart f p μ ν+Complex.I*imagPart f p μ ν
  rw [realPart_apply,imagPart_apply,mul_comm Complex.I]
  exact (Complex.re_add_im (f p μ ν)).symm

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.realPart_real
#print axioms F1Fecho.MaxwellGlobal.imagPart_real
#print axioms F1Fecho.MaxwellGlobal.real_imag_decomposition
