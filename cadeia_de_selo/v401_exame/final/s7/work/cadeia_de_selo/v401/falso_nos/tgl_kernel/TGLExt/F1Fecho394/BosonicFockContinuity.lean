import TGLExt.F1Fecho394.BosonicFock
import TGLExt.F1Fecho394.BosonicSectorContinuity
import TGLExt.F1Fecho394.SectorStrongContinuity
import TGLExt.LightOneParticleByTerm
/-! The constructed second quantization preserves strong continuity, for an
arbitrary topological parameter space. The real-time and spacetime fields of
the existing FockCertificate are thereby provided without postulating sector
continuity. This is not a construction of the remaining fields of that record. -/
set_option autoImplicit false
noncomputable section

namespace F1Rede.BosonicFock
open TGLExt.ImportedSQ F1Rede.BosonicSectors

theorem gamma_strong {A : Type*} [TopologicalSpace A]
    (u : A → H1 ≃ₗᵢ[ℂ] H1)
    (hu : ∀ x : H1, Continuous (fun a => u a x)) (f : F) :
    Continuous (fun a => gamma (u a) f) := by
  exact F1Rede.SectorStrongContinuity.diagonal_strongly_continuous
    (E := Sectors) (fun a => gammaSector (u a))
    (fun n x => F1Rede.BosonicSectorContinuity.gammaSector_strong u hu n x) f

theorem gamma_strong_real (u : ℝ → H1 ≃ₗᵢ[ℂ] H1)
    (hu : ∀ x : H1, Continuous (fun t => u t x)) (f : F) :
    Continuous (fun t => gamma (u t) f) := gamma_strong u hu f

theorem gamma_strong_spacetime (u : (Fin 4 → ℝ) → H1 ≃ₗᵢ[ℂ] H1)
    (hu : ∀ x : H1, Continuous (fun a => u a x)) (f : F) :
    Continuous (fun a => gamma (u a) f) := gamma_strong u hu f

theorem translations_strong (f : F) :
    Continuous (fun a : Fin 4 → ℝ => gamma (U1 a) f) :=
  gamma_strong U1 TGLExt.LightByTerm.light_translations_strongly_continuous f

theorem boosts_strong (f : F) :
    Continuous (fun s : ℝ => gamma (B0 s) f) :=
  gamma_strong B0 B0_continuous f

end F1Rede.BosonicFock

#print axioms F1Rede.BosonicFock.gamma_strong
#print axioms F1Rede.BosonicFock.gamma_strong_real
#print axioms F1Rede.BosonicFock.gamma_strong_spacetime
#print axioms F1Rede.BosonicFock.translations_strong
#print axioms F1Rede.BosonicFock.boosts_strong
