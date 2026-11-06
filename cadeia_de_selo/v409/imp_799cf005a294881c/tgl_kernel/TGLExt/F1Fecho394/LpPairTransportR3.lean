import TGLExt.F1Fecho394.CoefficientBoostR1
import TGLExt.F1Fecho394.CoefficientConjugationR2
import Mathlib.Analysis.InnerProductSpace.ProdL2

/-! Exact continuous transport between coefficient pairs and Hilbert pair valued L2.
No GNS representation or graph equality is assumed here. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory
namespace F1Fecho.LpPairTransport
open TGLV350.Regular F1Fecho.RegularCovariantCore
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
abbrev PairH (H:Type) := WithLp 2 (H×H)
abbrev PairLp (H:Type) [NormedAddCommGroup H] := Lp (PairH H) 2 (volume:Measure ℝ)

def leftMap : H→L[ℂ]PairH H :=
  (WithLp.prodContinuousLinearEquiv 2 ℂ H H).symm.toContinuousLinearMap.comp
    (ContinuousLinearMap.inl ℂ H H)
def rightMap : H→L[ℂ]PairH H :=
  (WithLp.prodContinuousLinearEquiv 2 ℂ H H).symm.toContinuousLinearMap.comp
    (ContinuousLinearMap.inr ℂ H H)
def fstMap : PairLp H→L[ℂ]RegularHilbert H := (WithLp.fstL 2 ℂ H H).compLpL 2 volume
def sndMap : PairLp H→L[ℂ]RegularHilbert H := (WithLp.sndL 2 ℂ H H).compLpL 2 volume

def pair (f g:RegularHilbert H) : PairLp H :=
  (leftMap (H:=H)).compLpL 2 volume f+(rightMap (H:=H)).compLpL 2 volume g

theorem pair_ae (f g:RegularHilbert H) :
    pair f g =ᵐ[volume] fun a=>WithLp.toLp 2 (f a,g a) := by
  filter_upwards [Lp.coeFn_add ((leftMap (H:=H)).compLpL 2 volume f)
      ((rightMap (H:=H)).compLpL 2 volume g),
    (leftMap (H:=H)).coeFn_compLpL f,(rightMap (H:=H)).coeFn_compLpL g] with a ha hb hc
  change pair f g a=_
  change (((leftMap (H:=H)).compLpL 2 volume f+(rightMap (H:=H)).compLpL 2 volume g) a)=_ at ha
  rw [show pair f g a= _ from ha]
  simp only [Pi.add_apply]
  rw [hb,hc]
  apply (WithLp.linearEquiv 2 ℂ (H×H)).injective
  change (f a,0)+(0,g a)=(f a,g a)
  simp

theorem fst_pair (f g:RegularHilbert H) : fstMap (pair f g)=f := by
  apply Lp.ext
  filter_upwards [(WithLp.fstL 2 ℂ H H).coeFn_compLpL (pair f g),pair_ae f g] with a ha hb
  change fstMap (pair f g) a=_
  change (WithLp.fstL 2 ℂ H H).compLpL 2 volume (pair f g) a=_ at ha
  rw [show fstMap (pair f g) a=_ from ha,hb]
  rfl

theorem snd_pair (f g:RegularHilbert H) : sndMap (pair f g)=g := by
  apply Lp.ext
  filter_upwards [(WithLp.sndL 2 ℂ H H).coeFn_compLpL (pair f g),pair_ae f g] with a ha hb
  change sndMap (pair f g) a=_
  change (WithLp.sndL 2 ℂ H H).compLpL 2 volume (pair f g) a=_ at ha
  rw [show sndMap (pair f g) a=_ from ha,hb]
  rfl

def encode (B:UnitaryFlow H) (f g:RegularHilbert H) : PairLp H :=
  pair f (CoefficientBoost.multiplier B 1 (CoefficientConjugation.reflection g))

def decode (B:UnitaryFlow H) : PairLp H→L[ℂ](RegularHilbert H×RegularHilbert H) :=
  fstMap.prod (CoefficientConjugation.reflection.toLinearIsometry.toContinuousLinearMap.comp
    ((CoefficientBoost.multiplier B (-1)).comp sndMap))

theorem decode_encode (B:UnitaryFlow H) (f g:RegularHilbert H) :
    decode B (encode B f g)=(f,g) := by
  apply Prod.ext
  · exact fst_pair _ _
  · change CoefficientConjugation.reflection
      (CoefficientBoost.multiplier B (-1) (sndMap (pair f _)))=g
    rw [snd_pair,CoefficientBoost.multiplier_inverse]
    exact CoefficientConjugation.reflectionMap_involutive g

theorem encode_ae (B:UnitaryFlow H) (f g:RegularHilbert H) :
    encode B f g =ᵐ[volume] fun a=>WithLp.toLp 2 (f a,B.U a (g (-a))) := by
  filter_upwards [pair_ae f (CoefficientBoost.multiplier B 1 (CoefficientConjugation.reflection g)),
    CoefficientBoost.multiplier_ae B 1 (CoefficientConjugation.reflection g),
    CoefficientConjugation.reflectionMap_ae g] with a ha hb hc
  change encode B f g a=_
  change pair f _ a=_ at ha
  rw [show encode B f g a=_ from ha,hb]
  change (CoefficientConjugation.reflection g) a=g (-a) at hc
  rw [hc,one_mul]

end F1Fecho.LpPairTransport
#print axioms F1Fecho.LpPairTransport.pair_ae
#print axioms F1Fecho.LpPairTransport.fst_pair
#print axioms F1Fecho.LpPairTransport.snd_pair
#print axioms F1Fecho.LpPairTransport.decode_encode
#print axioms F1Fecho.LpPairTransport.encode_ae
