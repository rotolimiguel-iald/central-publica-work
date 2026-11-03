import TGLExt.F1Fecho394.BosonicSectors
import TGLExt.F1Fecho394.SectorInfiniteDimension
/-! Concrete bosonic Hilbert space, vacuum and second-quantized unitary functor
on the canonical v392 H1. The n-particle sectors are closed spans of diagonal
tensor powers. This file supplies the kinematic objects and proves their laws;
it does not assert the remaining Weyl, modular, spectral or Maxwell fields of
TGLExt.ImportedSQ.FockCertificate. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
open scoped InnerProductSpace

namespace F1Rede.BosonicFock
open TGLExt.ImportedSQ F1Rede.BosonicSectors F1Rede.SectorDirectSum

abbrev Sectors (n : ℕ) : Type := Sector n
abbrev F := SumSpace Sectors
def vacuum : F := sectorEmbedding (E := Sectors) 0 vacuumSector
def gamma (u : H1 ≃ₗᵢ[ℂ] H1) : F ≃ₗᵢ[ℂ] F :=
  diagonal (E := Sectors) (gammaSector u)
def oneParticle : H1 →ₗᵢ[ℂ] F :=
  (sectorEmbedding (E := Sectors) 1).comp oneParticleEmbedding

theorem vacuum_norm : ‖vacuum‖ = 1 := by
  change ‖sectorEmbedding (E := Sectors) 0 vacuumSector‖ = 1
  rw [(sectorEmbedding (E := Sectors) 0).norm_map, vacuumSector_norm]

theorem gamma_refl : gamma (.refl ℂ H1) = .refl ℂ F := by
  change diagonal (E := Sectors) (fun n => gammaSector (.refl ℂ H1) n) = _
  simp only [gammaSector_refl]
  exact diagonal_refl (E := Sectors)

theorem gamma_trans (u v : H1 ≃ₗᵢ[ℂ] H1) :
    gamma (u.trans v) = (gamma u).trans (gamma v) := by
  change diagonal (E := Sectors) (fun n => gammaSector (u.trans v) n) = _
  simp only [gammaSector_trans]
  exact diagonal_trans (E := Sectors) (gammaSector u) (gammaSector v)

theorem gamma_vacuum (u : H1 ≃ₗᵢ[ℂ] H1) : gamma u vacuum = vacuum := by
  exact F1Rede.SectorDirectSum.vacuum_fixed (E := Sectors) (gammaSector u)
    vacuumSector (gammaSector_vacuum u)

theorem gamma_oneParticle (u : H1 ≃ₗᵢ[ℂ] H1) (x : H1) :
    gamma u (oneParticle x) = oneParticle (u x) := by
  change diagonal (gammaSector u) (sectorEmbedding 1 (oneParticleEmbedding x)) = _
  rw [diagonal_single, gammaSector_oneParticle]
  rfl

theorem oneParticle_isometric (x : H1) : ‖oneParticle x‖ = ‖x‖ :=
  oneParticle.norm_map x

theorem vacuum_orthogonal_oneParticle (x : H1) : ⟪vacuum, oneParticle x⟫_ℂ = 0 := by
  exact different_sectors_orthogonal (E := Sectors) 0 1 (by decide)
    vacuumSector (oneParticleEmbedding x)

theorem infinite_dimensional : ¬ FiniteDimensional ℂ F := by
  haveI := AuditF13v31.H1_nontrivial
  obtain ⟨x, hx⟩ := exists_ne (0 : H1)
  let e : H1 := (‖x‖⁻¹ : ℂ) • x
  have he : ‖e‖ = 1 := norm_smul_inv_norm hx
  apply F1Rede.SectorDirectSum.infinite_dimensional (fun n => pureTensor n e)
  intro n
  rw [pureTensor_norm, he, one_pow]

end F1Rede.BosonicFock

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    match ci with
    | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
    | _ => pure ()
