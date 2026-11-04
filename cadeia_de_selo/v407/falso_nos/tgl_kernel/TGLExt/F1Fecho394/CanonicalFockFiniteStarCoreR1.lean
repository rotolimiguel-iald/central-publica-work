import TGLExt.F1Fecho394.CanonicalFockFiniteWeightR4
import TGLExt.F1Fecho394.RegularFiniteStarCoreR2
/-! The finite star core of the concrete regular Fock algebra. The underlying
weight and algebra are unchanged. Strong-star approximation supplies a domain
statement; it does not supply a tracial identity or an exponential scaling law. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockFiniteStarCore
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular Filter
open F1Fecho.CanonicalFockRegular
open scoped Topology

abbrev finiteStarCore := F1Fecho.RegularFiniteStarCore.finiteDualStarCore fockFlow M
abbrev finiteSandwich := F1Fecho.RegularFiniteStarCore.regularSandwich fockFlow M

theorem finiteSandwich_mem (A : core.toStarSubalgebra) (h : ℝ) (hh : 0 < h) :
    finiteSandwich A h ∈ finiteStarCore :=
  F1Fecho.RegularFiniteStarCore.regularSandwich_mem_finiteDualStarCore fockFlow M A h hh

theorem finiteSandwich_norm_le (A : core.toStarSubalgebra) (h : ℝ) :
    ‖(finiteSandwich A h).val‖ ≤ ‖A.val‖ :=
  F1Fecho.RegularFiniteStarCore.regularSandwich_norm_le fockFlow M A h

theorem finiteStarCore_strongStar_approximation (A : core.toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → finiteSandwich A h ∈ finiteStarCore) ∧
    (∀ h : ℝ, ‖(finiteSandwich A h).val‖ ≤ ‖A.val‖) ∧
    (∀ v, Tendsto (fun h : ℝ => (finiteSandwich A h).val v) (𝓝[>] 0) (𝓝 (A.val v))) ∧
    (∀ v, Tendsto (fun h : ℝ => star (finiteSandwich A h).val v) (𝓝[>] 0)
      (𝓝 (star A.val v))) :=
  F1Fecho.RegularFiniteStarCore.finiteDualStarCore_strongStar_approximation fockFlow M A

end F1Fecho.CanonicalFockFiniteStarCore
#print axioms F1Fecho.CanonicalFockFiniteStarCore.finiteStarCore
#print axioms F1Fecho.CanonicalFockFiniteStarCore.finiteSandwich
#print axioms F1Fecho.CanonicalFockFiniteStarCore.finiteSandwich_mem
#print axioms F1Fecho.CanonicalFockFiniteStarCore.finiteSandwich_norm_le
#print axioms F1Fecho.CanonicalFockFiniteStarCore.finiteStarCore_strongStar_approximation
