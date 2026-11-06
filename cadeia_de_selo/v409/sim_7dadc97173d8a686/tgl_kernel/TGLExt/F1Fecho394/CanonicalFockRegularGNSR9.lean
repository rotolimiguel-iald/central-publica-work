import TGLExt.F1Fecho394.CanonicalFockRegularRightGNSR11
import TGLExt.F1Fecho394.RegularConjugationContinuityR1
import TGLExt.F1Fecho394.CanonicalFockWeightSandwichR5
import TGLExt.F1Fecho394.RegularRightContinuityR2
import TGLExt.F1Fecho394.ClosedSubmoduleStarLawsR1
/-! Actual commuting right action and regular-conjugation candidate on the
same weight GNS space. No equality with its CFC modular group is assumed. -/
set_option autoImplicit false
set_option maxErrors 2
set_option maxHeartbeats 800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockRegularGNS
open TGLExt.ImportedSQ F1Rede.BosonicFock
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightSandwich
open F1Fecho.CanonicalFockRegularRightGNS
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (GNSHilbert →L[ℂ] GNSHilbert) := F1Fecho.ClosedSubmoduleRestriction.endomorphismStar GNSSubspace
/-- Associativity on the full scalar-weight ideal, followed by density,
proves commutation with EVERY represented left algebra element. -/
theorem regularRightGNS_commutes_left (t : ℝ)
    (B : (core).toStarSubalgebra) :
    Commute (regularRightGNS t) (scalarGNSRepresentation B) := by
  apply ContinuousLinearMap.ext
  intro z
  change regularRightGNS t (scalarGNSRepresentation B z) =
    scalarGNSRepresentation B (regularRightGNS t z)
  refine (scalarWeightGNSEmbedding_denseRange).induction ?_
    (isClosed_eq ((regularRightGNS t).continuous.comp (scalarGNSRepresentation B).continuous)
      ((scalarGNSRepresentation B).continuous.comp (regularRightGNS t).continuous)) z
  rintro _ ⟨a,rfl⟩
  have hp : scalarRegularRightProduct t (scalarWeightLeftProduct B a) =
      scalarWeightLeftProduct B (scalarRegularRightProduct t a) := by
    apply Subtype.ext
    exact mul_assoc B a.val (regularRightCoreElement t)
  calc
    _ = regularRightGNS t (scalarWeightGNSEmbedding (scalarWeightLeftProduct B a)) :=
      congrArg (regularRightGNS t) (scalarWeightGNSAction_intertwines B a)
    _ = scalarWeightGNSEmbedding (scalarRegularRightProduct t (scalarWeightLeftProduct B a)) :=
      regularRightGNS_intertwines t (scalarWeightLeftProduct B a)
    _ = scalarWeightGNSEmbedding (scalarWeightLeftProduct B (scalarRegularRightProduct t a)) :=
      congrArg (scalarWeightGNSEmbedding) hp
    _ = scalarGNSRepresentation B (scalarWeightGNSEmbedding (scalarRegularRightProduct t a)) :=
      (scalarWeightGNSAction_intertwines B (scalarRegularRightProduct t a)).symm
    _ = _ := congrArg (scalarGNSRepresentation B) (regularRightGNS_intertwines t a).symm


theorem regularRightGNS_strongly_continuous (z : GNSHilbert) :
    Continuous (fun t : ℝ => regularRightGNS t z) := by
  apply continuous_induced_rng.mpr
  exact F1Fecho.RegularRightContinuity.rightAmbient_strongly_continuous (H := F) z.val

def regularConjugationGNS (t : ℝ) : GNSHilbert →L[ℂ] GNSHilbert :=
  scalarGNSRepresentation (regularRightCoreElement t) * regularRightGNS (-t)

theorem regularConjugationGNS_intertwines (t : ℝ) (A : scalarWeightLeftIdeal) :
    regularConjugationGNS t (scalarWeightGNSEmbedding A) =
      scalarWeightGNSEmbedding (scalarWeightLeftProduct (regularRightCoreElement t)
        (scalarRegularRightProduct (-t) A)) := by
  change scalarGNSRepresentation (regularRightCoreElement t)
    (regularRightGNS (-t) (scalarWeightGNSEmbedding A)) = _
  exact (congrArg (scalarGNSRepresentation (regularRightCoreElement t))
    (regularRightGNS_intertwines (-t) A)).trans
      (scalarWeightGNSAction_intertwines (regularRightCoreElement t) (scalarRegularRightProduct (-t) A))

theorem regularConjugationGNS_zero : regularConjugationGNS 0=1 := by
  have he : regularRightCoreElement 0 = 1 := Subtype.ext (F1Fecho.RegularCovariantCore.regular_zero fockFlow)
  change scalarGNSRepresentation (regularRightCoreElement 0) * regularRightGNS (-0)=1
  have hr : regularRightGNS (-(0:ℝ))=1 :=
    (congrArg regularRightGNS (neg_zero:-(0:ℝ)=0)).trans regularRightGNS_zero
  exact (congrArg₂ (fun a b : GNSHilbert →L[ℂ] GNSHilbert => a*b)
    ((congrArg scalarGNSRepresentation he).trans (map_one scalarGNSRepresentation))
    hr).trans (one_mul 1)


theorem regularRightCoreElement_mul (s t : ℝ) :
    regularRightCoreElement s * regularRightCoreElement t = regularRightCoreElement (s+t) :=
  Subtype.ext (F1Fecho.RegularCovariantCore.regular_mul fockFlow s t)

private theorem group_product_mul {A:Type*} [Monoid A] (L R:ℝ→A)
    (hL:∀s t,L s*L t=L (s+t)) (hR:∀s t,R s*R t=R (s+t))
    (hc:∀s t,Commute (R s) (L t)) (s t:ℝ) :
    (L s*R (-s))*(L t*R (-t))=L (s+t)*R (-(s+t)) := by
  calc
    _=L s*(R (-s)*L t)*R (-t) := by simp only [mul_assoc]
    _=(L s*L t)*(R (-s)*R (-t)) := by rw [(hc (-s) t).eq]; simp only [mul_assoc]
    _=_ := by rw [hL,hR,←neg_add]

theorem regularConjugationGNS_mul (s t : ℝ) :
    regularConjugationGNS s * regularConjugationGNS t = regularConjugationGNS (s+t) :=
  group_product_mul (fun a=>scalarGNSRepresentation (regularRightCoreElement a)) regularRightGNS
    (fun a b=>(map_mul scalarGNSRepresentation (regularRightCoreElement a) (regularRightCoreElement b)).symm.trans
      (congrArg scalarGNSRepresentation (regularRightCoreElement_mul a b)))
    regularRightGNS_mul (fun a b=>regularRightGNS_commutes_left a (regularRightCoreElement b)) s t

private theorem group_product_star {A:Type*} [Monoid A]
    (st:A→A) (hstm:∀x y,st (x*y)=st y*st x)
    (L R:ℝ→A) (hL:∀t,st (L t)=L (-t)) (hR:∀t,st (R t)=R (-t))
    (hc:∀s t,Commute (R s) (L t)) (t:ℝ) :
    st (L t*R (-t))=L (-t)*R (-(-t)) := by
  rw [hstm,hR,hL]
  exact (hc (-(-t)) (-t)).eq

theorem regularConjugationGNS_star (t : ℝ) :
    star (regularConjugationGNS t) = regularConjugationGNS (-t) :=
  group_product_star star (F1Fecho.ClosedSubmoduleRestriction.endomorphismStar_mul GNSSubspace)
    (fun a=>scalarGNSRepresentation (regularRightCoreElement a)) regularRightGNS
    (fun a=>(map_star scalarGNSRepresentation (regularRightCoreElement a)).symm.trans
      (congrArg scalarGNSRepresentation (regularRightCoreElement_star a)))
    regularRightGNS_star (fun a b=>regularRightGNS_commutes_left a (regularRightCoreElement b)) t

private theorem group_unitary {A:Type*} [Monoid A] [Star A]
    (U:ℝ→A) (h0:U 0=1) (hm:∀s t,U s*U t=U (s+t))
    (hs:∀t,star (U t)=U (-t)) (t:ℝ) : star (U t)*U t=1 ∧ U t*star (U t)=1 := by
  rw [hs,hm,hm,neg_add_cancel,add_neg_cancel,h0]
  exact ⟨rfl,rfl⟩

theorem regularConjugationGNS_unitary (t : ℝ) :
    star (regularConjugationGNS t) * regularConjugationGNS t=1 ∧
    regularConjugationGNS t * star (regularConjugationGNS t)=1 :=
  group_unitary regularConjugationGNS regularConjugationGNS_zero regularConjugationGNS_mul
    regularConjugationGNS_star t

theorem regularConjugationGNS_ambient (t : ℝ) (z : GNSHilbert) :
    (regularConjugationGNS t z).val =
      TGLV350.Regular.fibre (TGLV350.Regular.fibre
        (F1Fecho.RegularCovariantCore.boostCLM fockFlow t)) z.val := by
  change (TGLV350.Regular.dualOrbitRepresentation (regularUnitary t) *
    F1Fecho.RegularRightAction.ambient (H:=F) (-t)) z.val = _
  exact congrArg (fun T => T z.val)
    (F1Fecho.RegularConjugationAmbient.regular_conjugation_is_base_fibre fockFlow t)

theorem regularConjugationGNS_strongly_continuous (z : GNSHilbert) :
    Continuous (fun t : ℝ => regularConjugationGNS t z) := by
  apply continuous_induced_rng.mpr
  exact (F1Fecho.RegularConjugationAmbient.base_fibre_strongly_continuous fockFlow z.val).congr
    (fun t => (regularConjugationGNS_ambient t z).symm)

end F1Fecho.CanonicalFockRegularGNS
#print axioms F1Fecho.CanonicalFockRegularGNS.regularRightGNS_commutes_left
#print axioms F1Fecho.CanonicalFockRegularGNS.regularRightGNS_strongly_continuous
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_intertwines
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_zero

#print axioms F1Fecho.CanonicalFockRegularGNS.regularRightCoreElement_mul
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_mul
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_star
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_unitary

#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_ambient
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_strongly_continuous
