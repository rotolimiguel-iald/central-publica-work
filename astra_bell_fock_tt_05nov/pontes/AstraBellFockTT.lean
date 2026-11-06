import TGLExt.ParNaFaceDeFock
import TGLExt.F1Fecho394.CreationAndSegalR2
import TGLExt.F1Fecho394.ExponentialVectorsR3
import TGLExt.LinearizedSpin2

set_option autoImplicit false
set_option maxHeartbeats 2000000
noncomputable section
open scoped InnerProductSpace
open Matrix

namespace TGL.Candidate.AstraBellFockTT
open TGLExt TGLExt.ImportedSQ TGLExt.ParNaFaceDeFock
open F1Rede.BosonicFock F1Rede.BosonicSectors F1Rede.SectorDirectSum
open F1Fecho.Exponential

/-- A normalized double occupation when the input mode has norm one. -/
def occupiedTwice (f : H1) : F := sectorEmbedding (E := Sectors) 2 (pureTensor 2 f)

theorem occupiedTwice_inner (f g : H1) :
    inner ℂ (occupiedTwice f) (occupiedTwice g) = (inner ℂ f g)^2 := by
  unfold occupiedTwice
  rw [LinearIsometry.inner_map_map, pureTensor_inner]

theorem pair_is_diagonal_code (f g : H1) :
    parFock f g = (((Real.sqrt 2)⁻¹ : ℝ) : ℂ) • (occupiedTwice f + occupiedTwice g) := by
  unfold parFock occupiedTwice
  rw [← map_add, ← map_smul]
  apply congrArg ((sectorEmbedding (E := Sectors) 2) : Sectors 2 → F)
  exact Subtype.ext (parSetor_eq f g)

theorem gamma_occupiedTwice (u : H1 ≃ₗᵢ[ℂ] H1) (f : H1) :
    gamma u (occupiedTwice f) = occupiedTwice (u f) := by
  unfold gamma occupiedTwice
  rw [F1Rede.SectorDirectSum.diagonal_single, gammaSector_pure]

theorem pair_mode_phase_doubles (u : H1 ≃ₗᵢ[ℂ] H1) (f : H1) (z : ℂ) (hf : u f = z • f) :
    gamma u (occupiedTwice f) = z^2 • occupiedTwice f := by
  rw [gamma_occupiedTwice, hf]
  simp only [occupiedTwice, pureTensor_smul, map_smul]

/-- The two measured quadratures of a complex coherence, expressed as a real TT tensor. -/
def quadratureTensor (x y : ℝ) := x • ePlus + y • eCross

theorem tt_rotates_quadratures (t x y : ℝ) :
    (rotZ t)ᵀ * quadratureTensor x y * rotZ t =
    quadratureTensor (x * Real.cos (2*t) + y * Real.sin (2*t))
      (-x * Real.sin (2*t) + y * Real.cos (2*t)) := by
  unfold quadratureTensor
  rw [Matrix.mul_add, Matrix.add_mul]
  simp only [Matrix.mul_smul, Matrix.smul_mul, helicity_two_rotation, helicity_two_rotation_cross,
    smul_sub, smul_add, smul_smul, add_smul, neg_mul, neg_smul]
  abel

open F1Fecho.Creation F1Fecho.Annihilation

/-- The real scale is sqrt(2), written through the normalization of the existing sector. -/
def createdTwice (f : H1) : F := (weight 2 : ℂ)⁻¹ • occupiedTwice f

theorem twice_against_exponential (h f : H1) :
    inner ℂ (exponential h) (createdTwice f) = (inner ℂ h f)^2 := by
  unfold createdTwice
  rw [inner_smul_right]
  change _ * inner ℂ (exponential h) (lp.single 2 2 (pureTensor 2 f)) = _
  rw [lp.inner_single_right]
  change _ * inner ℂ ((weight 2 : ℂ) • pureTensor 2 h) (pureTensor 2 f) = _
  rw [_root_.inner_smul_left (pureTensor 2 h) (pureTensor 2 f) (weight 2 : ℂ),
    Complex.conj_ofReal, pureTensor_inner, ← mul_assoc]
  rw [inv_mul_cancel₀, one_mul]
  exact_mod_cast ne_of_gt (weight_pos 2)

theorem creator_pairing (f : H1) (x : (annihilation f).domain) :
    inner ℂ (createdTwice f) (x : F) = inner ℂ (oneParticle f) (annihilation f x) := by
  classical
  let c := preimage x
  have hx : synthesize c = (x : F) := preimage_spec x
  change inner ℂ (createdTwice f) (x : F) = inner ℂ (oneParticle f) (weighted f c)
  rw [← hx]
  simp only [synthesize, weighted, Finsupp.linearCombination_apply, Finsupp.sum, inner_sum,
    inner_smul_right]
  apply Finset.sum_congr rfl
  intro h _
  have h2 := congrArg (starRingEnd ℂ) (twice_against_exponential h f)
  have h1 := congrArg (starRingEnd ℂ) (exponential_inner_oneParticle h f)
  simp only [inner_conj_symm, map_pow] at h1 h2
  rw [h2, h1, pow_two]

theorem closed_creator_on_one_particle (f : H1) :
    ∃ h : oneParticle f ∈ (annihilation f).adjoint.domain,
      (annihilation f).adjoint ⟨oneParticle f,h⟩ = createdTwice f := by
  let h := LinearPMap.mem_adjoint_domain_of_exists (T := annihilation f)
    (oneParticle f) ⟨createdTwice f, creator_pairing f⟩
  have hd : Dense ((annihilation f).domain : Set F) := domain_dense
  exact ⟨h,LinearPMap.adjoint_apply_eq (T := annihilation f) hd ⟨oneParticle f,h⟩ (creator_pairing f)⟩

end TGL.Candidate.AstraBellFockTT

#print axioms TGL.Candidate.AstraBellFockTT.occupiedTwice_inner
#print axioms TGL.Candidate.AstraBellFockTT.pair_is_diagonal_code
#print axioms TGL.Candidate.AstraBellFockTT.gamma_occupiedTwice
#print axioms TGL.Candidate.AstraBellFockTT.pair_mode_phase_doubles
#print axioms TGL.Candidate.AstraBellFockTT.tt_rotates_quadratures
#print axioms TGL.Candidate.AstraBellFockTT.twice_against_exponential
#print axioms TGL.Candidate.AstraBellFockTT.creator_pairing
#print axioms TGL.Candidate.AstraBellFockTT.closed_creator_on_one_particle
