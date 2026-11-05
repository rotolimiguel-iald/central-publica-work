import Mathlib.Data.Complex.Basic
set_option autoImplicit false
open scoped ComplexConjugate
namespace F1Fecho.ComplexNormalization
 theorem half_conj : conj (1/2:ℂ)=(1/2:ℂ) := by
  simpa only [Complex.ofReal_div,Complex.ofReal_one,Complex.ofReal_ofNat] using
    Complex.conj_ofReal (1/2)
end F1Fecho.ComplexNormalization
#print axioms F1Fecho.ComplexNormalization.half_conj
