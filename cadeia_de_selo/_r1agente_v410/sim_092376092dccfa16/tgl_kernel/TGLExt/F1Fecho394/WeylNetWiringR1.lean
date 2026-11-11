import TGLExt.V350DualFixedCore
import TGLExt.TheOathOnTheTower
import TGLExt.TheConjugationMapsCommutants
/-!
Generator-to-net wiring using existing commutants. The generator family W and
its star/locality/covariance laws remain explicit inputs. This file does not
construct the concrete Fock Weyl operators, a cyclic/separating vacuum, Tomita
data, a physical stress tensor or H3. It does not assert an inhabitant for that
physical realization. A noncommuting generator pair gives a nonabelian algebra.
The von Neumann algebra uses mathlib's double-commutant definition.
-/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.WeylNet
open TGLExt TGLV350.Regular

variable {F : Type} [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

theorem starCommutant_coe_of_star_closed (S : Set (F →L[ℂ] F))
    (hs : ∀ x ∈ S, star x ∈ S) :
    (starCommutantAlgebra S : Set (F →L[ℂ] F)) = commutantSet S := by
  ext x
  change x ∈ StarSubalgebra.centralizer ℂ S ↔ _
  rw [StarSubalgebra.mem_centralizer_iff]
  constructor
  · intro h s hmem
    exact (h s hmem).1
  · intro h s hmem
    exact ⟨h s hmem, h (star s) (hs s hmem)⟩

def generatedAlgebra (S : Set (F →L[ℂ] F)) : VonNeumannAlgebra F :=
  (starCommutantAlgebra S).commutant

theorem generatedAlgebra_coe (S : Set (F →L[ℂ] F))
    (hs : ∀ x ∈ S, star x ∈ S) :
    (generatedAlgebra S : Set (F →L[ℂ] F)) = commutantSet (commutantSet S) := by
  rw [generatedAlgebra, VonNeumannAlgebra.coe_commutant,
    starCommutant_coe_of_star_closed S hs]
  rfl

theorem generators_mem (S : Set (F →L[ℂ] F))
    (hs : ∀ x ∈ S, star x ∈ S) :
    S ⊆ (generatedAlgebra S : Set (F →L[ℂ] F)) := by
  rw [generatedAlgebra_coe S hs]
  exact subset_bicommutant S

theorem generatedAlgebra_mono (S T : Set (F →L[ℂ] F))
    (hs : ∀ x ∈ S, star x ∈ S) (ht : ∀ x ∈ T, star x ∈ T) (h : S ⊆ T) :
    (generatedAlgebra S : Set (F →L[ℂ] F)) ⊆ generatedAlgebra T := by
  rw [generatedAlgebra_coe S hs, generatedAlgebra_coe T ht]
  exact bicommutant_mono h

theorem generatedAlgebra_local (S T : Set (F →L[ℂ] F))
    (hs : ∀ x ∈ S, star x ∈ S) (ht : ∀ x ∈ T, star x ∈ T)
    (h : ∀ x ∈ S, ∀ y ∈ T, Commute x y) :
    ∀ x ∈ generatedAlgebra S, ∀ y ∈ generatedAlgebra T, Commute x y := by
  have hST : S ⊆ commutantSet T := by
    intro x hx y hy
    exact (h x hx y hy).eq.symm
  have hb := bicommutant_mono hST
  rw [commutant_triple] at hb
  intro x hx y hy
  rw [← SetLike.mem_coe, generatedAlgebra_coe S hs] at hx
  rw [← SetLike.mem_coe, generatedAlgebra_coe T ht] at hy
  exact hy x (hb hx)

theorem doubleCommutant_transport
    (e : (F →L[ℂ] F) ≃⋆ₐ[ℂ] (F →L[ℂ] F)) (S : Set (F →L[ℂ] F)) :
    e '' commutantSet (commutantSet S) =
      commutantSet (commutantSet (e '' S)) := by
  rw [conj_commutant_of_biinverse e e.symm (fun x y => map_mul e x y)
    e.symm_apply_apply e.apply_symm_apply,
    conj_commutant_of_biinverse e e.symm (fun x y => map_mul e x y)
    e.symm_apply_apply e.apply_symm_apply]

theorem generatedAlgebra_cov (S T : Set (F →L[ℂ] F))
    (hs : ∀ x ∈ S, star x ∈ S) (ht : ∀ x ∈ T, star x ∈ T)
    (e : (F →L[ℂ] F) ≃⋆ₐ[ℂ] (F →L[ℂ] F)) (he : e '' S = T)
    (x : F →L[ℂ] F) : x ∈ generatedAlgebra S ↔ e x ∈ generatedAlgebra T := by
  have htransport : e '' (generatedAlgebra S : Set (F →L[ℂ] F)) =
      (generatedAlgebra T : Set (F →L[ℂ] F)) := by
    rw [generatedAlgebra_coe S hs, generatedAlgebra_coe T ht,
      doubleCommutant_transport, he]
  constructor
  · intro hx
    rw [← SetLike.mem_coe, ← htransport]
    exact ⟨x,hx,rfl⟩
  · intro hx
    rw [← SetLike.mem_coe, ← htransport] at hx
    obtain ⟨y,hy,hxy⟩ := hx
    have : y = x := e.injective hxy
    simpa [this] using hy

theorem generatedAlgebra_nonabelian (S : Set (F →L[ℂ] F))
    (hs : ∀ x ∈ S, star x ∈ S)
    (h : ∃ a ∈ S, ∃ b ∈ S, a * b ≠ b * a) :
    ∃ a ∈ generatedAlgebra S, ∃ b ∈ generatedAlgebra S, a * b ≠ b * a := by
  obtain ⟨a,ha,b,hb,hab⟩ := h
  exact ⟨a,generators_mem S hs ha,b,generators_mem S hs hb,hab⟩

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

def generators (W : H → (F →L[ℂ] F)) (K : Submodule ℝ H) : Set (F →L[ℂ] F) :=
  W '' (K : Set H)

theorem generators_star_closed (W : H → (F →L[ℂ] F))
    (hstar : ∀ f, star (W f) = W (-f)) (K : Submodule ℝ H) :
    ∀ x ∈ generators W K, star x ∈ generators W K := by
  rintro x ⟨f,hf,rfl⟩
  exact ⟨-f,K.neg_mem hf,(hstar f).symm⟩

def R (W : H → (F →L[ℂ] F)) (K : Submodule ℝ H) : VonNeumannAlgebra F :=
  generatedAlgebra (generators W K)

theorem R_mono (W : H → (F →L[ℂ] F)) (hstar : ∀ f, star (W f) = W (-f))
    (K K' : Submodule ℝ H) (h : K ≤ K') :
    (R W K : Set (F →L[ℂ] F)) ⊆ R W K' :=
  generatedAlgebra_mono _ _ (generators_star_closed W hstar K)
    (generators_star_closed W hstar K') (Set.image_mono h)

theorem R_local (W : H → (F →L[ℂ] F)) (hstar : ∀ f, star (W f) = W (-f))
    (hlocal : ∀ f g, (inner ℂ f g).im = 0 → Commute (W f) (W g))
    (K K' : Submodule ℝ H)
    (h : ∀ f ∈ K, ∀ g ∈ K', (inner ℂ f g).im = 0) :
    ∀ x ∈ R W K, ∀ y ∈ R W K', Commute x y := by
  apply generatedAlgebra_local _ _ (generators_star_closed W hstar K)
    (generators_star_closed W hstar K')
  rintro x ⟨f,hf,rfl⟩ y ⟨g,hg,rfl⟩
  exact hlocal f g (h f hf g hg)

theorem R_cov (W : H → (F →L[ℂ] F)) (hstar : ∀ f, star (W f) = W (-f))
    (u : H ≃ₗᵢ[ℂ] H) (e : (F →L[ℂ] F) ≃⋆ₐ[ℂ] (F →L[ℂ] F))
    (hcov : ∀ f, e (W f) = W (u f))
    (K K' : Submodule ℝ H) (hK : ∀ f, f ∈ K ↔ u f ∈ K')
    (x : F →L[ℂ] F) : x ∈ R W K ↔ e x ∈ R W K' := by
  apply generatedAlgebra_cov _ _ (generators_star_closed W hstar K)
    (generators_star_closed W hstar K') e _ x
  apply Set.Subset.antisymm
  · rintro z ⟨y,⟨f,hf,rfl⟩,rfl⟩
    exact ⟨u f,(hK f).mp hf,(hcov f).symm⟩
  · rintro z ⟨g,hg,rfl⟩
    refine ⟨W (u.symm g),⟨u.symm g,?_,rfl⟩,?_⟩
    · exact (hK (u.symm g)).mpr (by simpa using hg)
    · simpa using hcov (u.symm g)

end F1Fecho.WeylNet

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.WeylNet).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
