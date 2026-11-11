import TGLExt.F1Fecho394.ConcreteWeylR1
import TGLExt.F1Fecho394.BosonicGammaJR5
import TGLExt.F1Fecho394.FieldWeylR3
/-! Antiunitary covariance of the concrete displacement, derived on the total
exponential family. This is algebraic covariance, not a modular identification. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.WeylAntiunitary
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.Antilinear F1Fecho.WeylCoefficients ChatgptAudit.Continuous050

variable (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1) (hj : Function.Involutive j)

theorem amplitude_anti (f g : H1) : amplitude (j f) (j g) = star (amplitude f g) := by
  simp only [amplitude, antiunitary_inner_conj, Complex.star_def, ← Complex.exp_conj,
    map_sub, map_neg, map_div₀, map_ofNat]

def conjugateDisplacement (f : H1) : F →L[ℂ] F where
  toFun x := gammaJ j hj (ConcreteWeyl.W f (gammaJ j hj x))
  map_add' x y := by simp only [map_add]
  map_smul' c x := by
    simp only [map_smulₛₗ, map_smul, starRingEnd_apply, star_star, RingHom.id_apply]
  cont := (gammaJ j hj).continuous.comp ((ConcreteWeyl.W f).continuous.comp (gammaJ j hj).continuous)

theorem conjugate_displacement (f : H1) :
    conjugateDisplacement j hj f = ConcreteWeyl.W (j f) := by
  apply F1Fecho.WeylConstruction.clm_ext_total exponential exponential_total
  intro g
  change gammaJ j hj (ConcreteWeyl.W f (gammaJ j hj (exponential g))) = _
  rw [gammaJ_exponential, ConcreteWeyl.W_exponential, map_smulₛₗ,
    gammaJ_exponential, ConcreteWeyl.W_exponential]
  simp only [map_add, starRingEnd_apply]
  rw [← amplitude_anti j f (j g), hj g]

theorem displacement_intertwining (f : H1) (v : F) :
    gammaJ j hj (ConcreteWeyl.W f v) = ConcreteWeyl.W (j f) (gammaJ j hj v) := by
  have h := congrArg (fun A : F →L[ℂ] F => A (gammaJ j hj v)) (conjugate_displacement j hj f)
  change gammaJ j hj (ConcreteWeyl.W f (gammaJ j hj (gammaJ j hj v))) = _ at h
  simpa only [gammaJ_involutive j hj v] using h

theorem field_intertwining (f : H1) (v : F) :
    gammaJ j hj (FieldWeyl.W f v) = FieldWeyl.W (-j f) (gammaJ j hj v) := by
  change gammaJ j hj (ConcreteWeyl.W (Complex.I • f) v) =
    ConcreteWeyl.W (Complex.I • (-j f)) (gammaJ j hj v)
  rw [displacement_intertwining]
  have h : j (Complex.I • f) = Complex.I • (-j f) := by
    rw [map_smulₛₗ]
    change (starRingEnd ℂ) Complex.I • j f = Complex.I • (-j f)
    exact (congrArg (fun z : ℂ => z • j f) Complex.conj_I).trans
      ((neg_smul Complex.I (j f)).trans (smul_neg Complex.I (j f)).symm)
  rw [h]

end F1Fecho.WeylAntiunitary
#print axioms F1Fecho.WeylAntiunitary.amplitude_anti
#print axioms F1Fecho.WeylAntiunitary.conjugate_displacement
#print axioms F1Fecho.WeylAntiunitary.displacement_intertwining

#print axioms F1Fecho.WeylAntiunitary.field_intertwining
