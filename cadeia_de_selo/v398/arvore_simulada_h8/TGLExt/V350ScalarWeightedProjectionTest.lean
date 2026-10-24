import TGLExt.V350ScalarPairedProjectionBlocks
import TGLExt.V350ScalarPhaseVariational

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt
noncomputable section

private theorem weightedAdjoint {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (A B e : H →L[ℂ] H)
    (hA : star A=A) (he : star e=e) (hc : Commute e A) :
    star (e*(1-A)*B)=star B*e*(1-A) := by
  rw [star_mul,star_mul,star_sub,star_one,hA,he,mul_assoc]
  congr 1
  rw [sub_mul,one_mul,mul_sub,mul_one,hc.eq]

private theorem weightedFirstAction {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (A B e : H →L[ℂ] H) (v w : H)
    (hB : B*star B=A*(1-A)) (hv : B v=A w) :
    (e*(1-A)*B) v=(e*B*star B) w := by
  change e ((1-A) (B v))=e (B (star B w))
  rw [hv]
  have ha : (1-A)*A=B*star B := by
    rw [hB,sub_mul,one_mul,mul_sub,mul_one]
  exact congrArg e (congrArg (fun T : H →L[ℂ] H => T w) ha)

private theorem weightedSecondAction {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (A B e : H →L[ℂ] H) (v w : H)
    (hA : star A=A) (he : star e=e) (hc : Commute e A) (hw : B w=(1-A) v) :
    star (e*(1-A)*B) v=(star B*e*B) w := by
  rw [weightedAdjoint A B e hA he hc]
  change star B (e ((1-A) v))=star B (e (B w))
  rw [hw]

private theorem actualGNSPairedCommute (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (hT : T ∈ scalarGNSVonNeumann P)
    (a : scalarPairedRightAlgebra P) : Commute T a.val := by
  have hm := (scalarPairedRightAlgebra_centralizer P).symm.subset hT
  exact (hm a.val a.property).symm

/-- The weighted block pair is in the ORIGINAL S graph. The implementing
bounded K and both of its right actions are constructed, not assumed. -/
theorem scalarPairedProjection_weighted_graph (P : SiteProfile)
    (η : scalarClosedTomitaDomain P) (hη : scalarClosedTomita P η=(η:ScalarGNSHilbert P))
    (e : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (hem : e ∈ scalarGNSVonNeumann P) (hes : star e=e)
    (heA : Commute e (hilbertBlockA (scalarPairedMultiplicationGraph P η).starProjection)) :
    let B := hilbertBlockB (scalarPairedMultiplicationGraph P η).starProjection
    ∃ hy : (e*B*star B) (η:ScalarGNSHilbert P) ∈ scalarClosedTomitaDomain P,
      scalarClosedTomita P ⟨(e*B*star B) (η:ScalarGNSHilbert P),hy⟩ =
        (star B*e*B) (η:ScalarGNSHilbert P) := by
  let G := scalarPairedMultiplicationGraph P η
  let A := hilbertBlockA G.starProjection
  let B := hilbertBlockB G.starProjection
  have hA : star A=A := hilbertBlockA_adjoint G
  have hB : B ∈ scalarGNSVonNeumann P := scalarPairedProjection_B_mem P η
  have hY : e*B*star B ∈ scalarGNSVonNeumann P :=
    (scalarGNSVonNeumann P).mul_mem ((scalarGNSVonNeumann P).mul_mem hem hB)
      ((scalarGNSVonNeumann P).toStarSubalgebra.star_mem' hB)
  have hZ : star B*e*B ∈ scalarGNSVonNeumann P :=
    (scalarGNSVonNeumann P).mul_mem
      ((scalarGNSVonNeumann P).mul_mem ((scalarGNSVonNeumann P).toStarSubalgebra.star_mem' hB) hem) hB
  apply scalarClosedTomita_of_boundedPairAction P (e*(1-A)*B)
  · intro a
    have ht := weightedFirstAction A B e (scalarRightPairVector P a) (a.val η)
      (scalarPairedProjection_BBstar P η) (scalarPairedProjection_B_left P η hη a)
    exact ht.trans (congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => T η)
      (actualGNSPairedCommute P (e*B*star B) hY a).eq)
  · intro a
    have ht := weightedSecondAction A B e (scalarRightPairVector P a) (a.val η)
      hA hes heA (scalarPairedProjection_B_right P η a)
    exact ht.trans (congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => T η)
      (actualGNSPairedCommute P (star B*e*B) hZ a).eq)

private theorem equationOfGraphPair {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] (D : Submodule ℂ H) (S : D → H)
    (x η y w : H) (z : ℂ)
    (hp : ∃ hy : y ∈ D, S ⟨y,hy⟩=w)
    (he : ∀ u : D, 2 * inner ℂ x (S u) =
      z * inner ℂ η (S u) + star z * inner ℂ (u : H) η) :
    2 * inner ℂ x w = z * inner ℂ η w + star z * inner ℂ y η := by
  obtain ⟨hy,hw⟩ := hp
  have hh := he ⟨y,hy⟩
  rw [hw] at hh
  exact hh

/-- The existing phase variational equation is applied to the concrete weighted
pair after its original-domain membership has been proved. -/
theorem scalarPhaseVariational_weighted_block_equation (P : SiteProfile)
    (z : ℂ) (hz : 0 < z.re) (x : scalarTomitaAdjointDomain P)
    (hx : scalarTomitaAdjoint P x=(x:ScalarGNSHilbert P))
    (e : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (hem : e ∈ scalarGNSVonNeumann P) (hes : star e=e)
    (heA : Commute e (hilbertBlockA (scalarPairedMultiplicationGraph P
      (scalarPhaseVariational P z hz x)).starProjection)) :
    let η : ScalarGNSHilbert P := scalarPhaseVariational P z hz x
    let B := hilbertBlockB (scalarPairedMultiplicationGraph P η).starProjection
    2 * inner ℂ (x:ScalarGNSHilbert P) ((star B*e*B) η) =
      z * inner ℂ η ((star B*e*B) η) + (star z) * inner ℂ ((e*B*star B) η) η := by
  let η : ScalarGNSHilbert P := scalarPhaseVariational P z hz x
  let B := hilbertBlockB (scalarPairedMultiplicationGraph P η).starProjection
  refine equationOfGraphPair (scalarClosedTomitaDomain P) (fun u => scalarClosedTomita P u)
    (x : ScalarGNSHilbert P) η ((e*B*star B) η) ((star B*e*B) η) z ?_ ?_
  · have hf : ∃ hη : η ∈ scalarClosedTomitaDomain P,
        scalarClosedTomita P ⟨η,hη⟩ = η :=
      scalarPhaseVariational_fixed P z hz (x : ScalarGNSHilbert P)
    obtain ⟨hη,hval⟩ := hf
    exact scalarPairedProjection_weighted_graph P ⟨η,hη⟩ hval e hem hes heA
  · intro u
    exact scalarPhaseVariational_graph_equation P z hz x hx u

#print axioms scalarPairedProjection_weighted_graph
#print axioms scalarPhaseVariational_weighted_block_equation
end
end TGLV350.Regular
