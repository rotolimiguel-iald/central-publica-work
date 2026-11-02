import TGLExt.F1Fecho394.CanonicalWeylKMSFiniteR2
import TGLExt.F1Fecho394.KMSGraphClosureR3
import TGLExt.F1Fecho394.BicommutantStarGraphR1
/-! The actual bounded KMS condition on the von Neumann wedge algebra.
Finite Weyl sums supply analytic strips. Proved joint approximation of A Omega
and A* Omega, plus the strip maximum theorem, supplies the full closure.
The physical KMS flow is Gamma(B0(+2*pi*t)); the modular CFC convention has
negative sign. No Fock KMS or analytic-domain premise is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.CanonicalWedgeKMS
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.CanonicalWedge
open F1Fecho.WeylExponentialCore F1Fecho.WeylFiniteAlgebra
open F1Fecho.CanonicalWeylKMSFinite

def finitePairs : Set (F×F) :=
  {p | ∃ A∈finiteAlgebra,p=(A vacuum,(star A) vacuum)}

theorem finite_pair_graph (x y : F×F) (hx : x∈finitePairs) (hy : y∈finitePairs) :
    KMSGraphClosure.Pair boostFlow x y := by
  obtain ⟨A,hA,rfl⟩ := hx
  obtain ⟨B,hB,rfl⟩ := hy
  obtain ⟨G,hd,⟨C,hC⟩,hl,hu⟩ := finite_pair A B hA hB
  exact ⟨G,hd,⟨C,fun z hz => hC z hz.1 hz.2⟩,hl,hu⟩

theorem pair_mem_closure (A : F→L[ℂ]F) (hA : A∈FieldWeyl.R K) :
    (A vacuum,(star A) vacuum)∈closure finitePairs :=
  StarGraphDensity.star_pair_mem_set_closure_of_bicommutant finiteAlgebra A vacuum
    (R_bicommutant_finite A hA)

theorem canonical_bw_kms :
    KMSBody (FieldWeyl.R KWR.toClosedSubmodule.toSubmodule) vacuum
      (fun t => gamma (B0 (2*Real.pi*t))) 1 := by
  intro A hA B hB
  have hp := KMSGraphClosure.of_dense_pairs boostFlow finitePairs
    (fun x hx y hy => finite_pair_graph x y hx hy)
    (A vacuum,(star A) vacuum) (B vacuum,(star B) vacuum)
    (pair_mem_closure A hA) (pair_mem_closure B hB)
  obtain ⟨G,hd,⟨C,hC⟩,hl,hu⟩ := hp
  refine ⟨G,hd,⟨C,fun z h0 h1 => hC z ⟨h0,h1⟩⟩,hl,?_⟩
  intro t
  simpa only [Complex.ofReal_one,one_mul,boostFlow] using hu t

end F1Fecho.CanonicalWedgeKMS
#print axioms F1Fecho.CanonicalWedgeKMS.finite_pair_graph
#print axioms F1Fecho.CanonicalWedgeKMS.pair_mem_closure
#print axioms F1Fecho.CanonicalWedgeKMS.canonical_bw_kms
