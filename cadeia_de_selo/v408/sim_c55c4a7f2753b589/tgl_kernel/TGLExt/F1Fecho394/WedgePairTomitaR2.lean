import TGLExt.F1Fecho394.WedgeCyclicR3
import TGLExt.F1Fecho394.PairClosedTomitaR2
/-! The closed Tomita operator of the actual Weyl algebra/vacuum pair.
No cyclicity, separation or closability is an input: these are derived for
every standard K on the same canonical one-particle/Fock realization.
Identification of its polar factors with Gamma(J),Gamma(Delta) is separate. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Set Topology
namespace F1Fecho.WedgePairTomita
open TGLExt.ImportedSQ F1Rede.BosonicFock
open F1Fecho

def algebra (K : StandardSubspace H1) : StarSubalgebra ℂ (F →L[ℂ] F) :=
  (FieldWeyl.R K.toClosedSubmodule.toSubmodule).toStarSubalgebra

theorem orbit_dense (K : StandardSubspace H1) :
    Dense ((fun a : F →L[ℂ] F => a vacuum) '' (algebra K : Set (F →L[ℂ] F))) :=
  PairTomita.dense_orbit_of_dense_span (algebra K) vacuum (WedgeCyclic.vacuum_cyclic K)

theorem algebras_commute (K : StandardSubspace H1) :
    ∀ a ∈ algebra K, ∀ b ∈ algebra K.symplComp, Commute a b := by
  apply FieldWeyl.R_local
  intro f hf g hg
  exact ClosedSubmodule.mem_symplComp_iff.mp hg f hf

theorem graph_functional (K : StandardSubspace H1) (x y z : F)
    (hy : (x,y) ∈ closure (PairTomita.graph (algebra K) vacuum))
    (hz : (x,z) ∈ closure (PairTomita.graph (algebra K) vacuum)) : y=z :=
  PairTomita.closure_functional (algebra K) (algebra K.symplComp) vacuum
    (algebras_commute K) (orbit_dense K.symplComp) x y z hy hz

def domain (K : StandardSubspace H1) : Submodule ℂ F :=
  PairTomita.closedDomain (algebra K) vacuum

def S (K : StandardSubspace H1) : domain K →ₛₗ[starRingEnd ℂ] F :=
  PairTomita.closedTomita (graph_functional K)

theorem graph_eq (K : StandardSubspace H1) :
    Set.range (fun x : domain K => ((x : F),S K x)) =
      closure (ORDEM016.D6.pairTomitaGraph (algebra K) vacuum) :=
  PairTomita.closedTomita_graph_eq (graph_functional K)

theorem S_closed (K : StandardSubspace H1) :
    IsClosed (Set.range (fun x : domain K => ((x : F),S K x))) :=
  PairTomita.closedTomita_isClosed (graph_functional K)

theorem domain_dense (K : StandardSubspace H1) : Dense (domain K : Set F) :=
  PairTomita.closedDomain_dense (orbit_dense K)

theorem S_maps_domain (K : StandardSubspace H1) (x : domain K) : S K x ∈ domain K :=
  PairTomita.closedTomita_maps_domain (graph_functional K) x

theorem S_involutive (K : StandardSubspace H1) (x : domain K) :
    S K ⟨S K x,S_maps_domain K x⟩ = x :=
  PairTomita.closedTomita_involutive (graph_functional K) x

theorem algebra_vector_domain (K : StandardSubspace H1) (a : F →L[ℂ] F)
    (ha : a ∈ algebra K) : a vacuum ∈ domain K :=
  PairTomita.algebra_vector_mem_domain ha

theorem S_algebra_vector (K : StandardSubspace H1) (a : F →L[ℂ] F)
    (ha : a ∈ algebra K) :
    S K ⟨a vacuum,algebra_vector_domain K a ha⟩ = (star a) vacuum :=
  PairTomita.closedTomita_extends_adjoint (graph_functional K) ha

theorem S_Weyl_vector (K : StandardSubspace H1) (f : H1)
    (hf : f ∈ K.toClosedSubmodule) :
    S K ⟨FieldWeyl.W f vacuum,algebra_vector_domain K (FieldWeyl.W f)
      (FieldWeyl.W_mem_R _ f hf)⟩ = FieldWeyl.W (-f) vacuum := by
  have h := S_algebra_vector K (FieldWeyl.W f) (FieldWeyl.W_mem_R _ f hf)
  simpa only [FieldWeyl.W_star] using h

def canonicalS := S F1Rede.CanonicalWedge.spectralOutput.KWR

theorem canonicalS_closed : IsClosed (Set.range
    (fun x : domain F1Rede.CanonicalWedge.spectralOutput.KWR => ((x : F),canonicalS x))) :=
  S_closed F1Rede.CanonicalWedge.spectralOutput.KWR

end F1Fecho.WedgePairTomita
#print axioms F1Fecho.WedgePairTomita.graph_functional
#print axioms F1Fecho.WedgePairTomita.S
#print axioms F1Fecho.WedgePairTomita.graph_eq
#print axioms F1Fecho.WedgePairTomita.domain_dense
#print axioms F1Fecho.WedgePairTomita.S_involutive
#print axioms F1Fecho.WedgePairTomita.S_Weyl_vector
#print axioms F1Fecho.WedgePairTomita.canonicalS_closed
