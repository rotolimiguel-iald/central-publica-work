import TGLExt.F1Fecho394.CanonicalFockActualStarCoreTracialR1
import TGLExt.F1Fecho394.GeneralInverseFiniteApproximationR1
import TGLExt.F1Fecho394.CanonicalFockWeightInvarianceR4

/-! DECLARADO / UNCOMPILED CANDIDATE, R49, 2026-10-16.
Reuse the proved regular-average/Fatou extension on the SAME Fock core and
inverseSupremum. The generic extension is already present in
GeneralInverseFiniteApproximationR1, following V351InverseLimitTracialExtension.
Its vacuum-fixed premise is supplied by the actual Fock vacuum theorem.
The finite-star-core identity is supplied by the independently authored
CanonicalFockActualStarCoreTracialR1, rather than added to the final statement.

No representation, weight, Hilbert structure, regulator family, approximation,
or trace axiom is introduced. ENNReal values may be infinite. This is only the
bounded-core square law; total trace packaging, semifiniteness/PF and their
normalization remain separate. Require terminal EXIT0 for this file and the
star-core supplier, then independent review; source presence is not proof. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 8
noncomputable section
namespace F1Fecho.CanonicalFockActualTracialExtensionR1
open F1Fecho.CanonicalFockRegular (core fockFlow M)
open F1Fecho.CanonicalFockWeight (regularFockVacuum)
open F1Fecho.RegularInverseWeight (inverseSupremum)
open scoped ENNReal

-- Cache only native Fock dictionaries; the ambient regular representation
-- inside core fockFlow M and the original scalar-weight GNS are unchanged.
private abbrev fockNormedAddCommGroup : NormedAddCommGroup F1Rede.BosonicFock.F :=
  inferInstance
private abbrev fockInnerProductSpace : InnerProductSpace ℂ F1Rede.BosonicFock.F :=
  inferInstance
private abbrev fockCompleteSpace : CompleteSpace F1Rede.BosonicFock.F := inferInstance

/-- Concrete reduction using the existing sandwich bounds and strong Fatou.
This equivalence alone does not assert its finite-star-core premise. -/
theorem inverseSupremum_tracial_iff_finiteStarCore :
    (∀ a : core.toStarSubalgebra,
      inverseSupremum fockFlow regularFockVacuum (star a.val * a.val) =
        inverseSupremum fockFlow regularFockVacuum (a.val * star a.val)) ↔
    (∀ a : core.toStarSubalgebra,
      a ∈ F1Fecho.RegularFiniteStarCore.finiteDualStarCore fockFlow M →
      inverseSupremum fockFlow regularFockVacuum (star a.val * a.val) =
        inverseSupremum fockFlow regularFockVacuum (a.val * star a.val)) :=
  @F1Fecho.RegularInverseWeight.inverseSupremum_tracial_iff_core
    F1Rede.BosonicFock.F fockNormedAddCommGroup fockInnerProductSpace fockCompleteSpace
    fockFlow M regularFockVacuum
    F1Fecho.CanonicalFockWeightInvariance.fibre_boost_fixes_regularVacuum
#print axioms inverseSupremum_tracial_iff_finiteStarCore

/-- The existing inverse supremum satisfies the square law on EVERY bounded
core element. The finite-star-core equality is consumed, not hypothesized. -/
theorem inverseSupremum_tracial (a : core.toStarSubalgebra) :
    inverseSupremum fockFlow regularFockVacuum (star a.val * a.val) =
      inverseSupremum fockFlow regularFockVacuum (a.val * star a.val) :=
  inverseSupremum_tracial_iff_finiteStarCore.mpr
    F1Fecho.CanonicalFockActualStarCoreTracialR1.inverseSupremum_star_core a
#print axioms inverseSupremum_tracial

end F1Fecho.CanonicalFockActualTracialExtensionR1
