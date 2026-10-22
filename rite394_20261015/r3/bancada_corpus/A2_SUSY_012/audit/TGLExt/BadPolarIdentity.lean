import TGLExt.V354BoundedPolar
set_option autoImplicit false
namespace TGLV354.Probes
noncomputable section
-- Deliberate false mutation: a polar factor need not be an isometry on all H.
example : star (boundedPolar (0 : ℂ →L[ℂ] ℂ))*boundedPolar 0=1 :=
  boundedPolar_star_mul (0 : ℂ →L[ℂ] ℂ)
end
end TGLV354.Probes
