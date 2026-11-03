import TGLExt.TowerAction
import Mathlib.Analysis.VonNeumannAlgebra.Basic

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A PEDRA 86 — TheFactorObject: M_TGL = (π(torre))'' — O FATOR COMO OBJETO
  [TGLExt — v131, Bloco A do PLANO_ULTIMA_FLAG, pedra 4 de 5]

O resíduo nomeado do v130 era UM: "falta SÓ o limite fraco-* — o
completamento topológico". Esta pedra o realiza LITERALMENTE:

* `towerImage` — o conjunto π(torre) ⊆ B(H_φ); ★ `towerImage_star_closed`
  — fechado sob estrela (π é estrelada, pedra 85);
* ★★★ `theFactorObject : VonNeumannAlgebra (TowerHilbert P)` — **M_TGL :=
  (π(torre))'' cunhado como TERMO da estrutura `VonNeumannAlgebra` da
  mathlib** (o duplo comutante; o colapso do triplo comutante é álgebra
  pura) — o objeto de von Neumann da torre EXISTE em kernel;
* ★★ `towerPi_mem_factor` — π(torre) ⊆ M_TGL: a torre vive DENTRO do
  seu fecho;
* ★★★ `factor_omega_cyclic` — Ω é CÍCLICO para M_TGL: a órbita do objeto
  sobre o vetor do Nome é densa em H_φ;
* ★★★ `omegaState_pi` — A IDENTIDADE GNS: ω(π(x)) = φ(x) — o estado
  coerente da torre inteira VIVE no objeto (ω = ⟨Ω, · Ω⟩).

HONESTIDADE (a régua): M_TGL é objeto de von Neumann LEGÍTIMO (duplo
comutante de um conjunto estrelado). "Fator" e "III₁" seguem sendo
ASSINATURA (pedra 87), não teorema de tipo — o gate NÃO se move por esta
pedra. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix UniformSpace

noncomputable section

variable {P : SiteProfile}

/-! ## A — o conjunto π(torre) e sua estrela -/

/-- π(torre): a imagem da torre inteira em B(H_φ). -/
def towerImage (P : SiteProfile) :
    Set (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  {T | ∃ (N : ℕ) (x : Matrix (chainIdx N) (chainIdx N) ℂ), T = towerPi P x}

theorem towerPi_mem_towerImage {N : ℕ}
    (x : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P x ∈ towerImage P := ⟨N, x, rfl⟩

/-- [KERNEL] ★ π(torre) é fechado sob ESTRELA: star (π x) = π (x†). -/
theorem towerImage_star_closed {T : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hT : T ∈ towerImage P) : star T ∈ towerImage P := by
  obtain ⟨N, x, rfl⟩ := hT
  refine ⟨N, xᴴ, ?_⟩
  rw [towerPi_star, ContinuousLinearMap.star_eq_adjoint]

/-! ## B — O OBJETO: M_TGL = (π(torre))'' como VonNeumannAlgebra -/

/-- ★★★ M_TGL: o duplo comutante de π(torre), cunhado como TERMO da
    estrutura `VonNeumannAlgebra` da mathlib — O FATOR COMO OBJETO
    (o resíduo nomeado do v130, realizado; o colapso do triplo comutante
    é álgebra pura de centralizadores). -/
def theFactorObject (P : SiteProfile) : VonNeumannAlgebra (TowerHilbert P) where
  toStarSubalgebra := StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ (towerImage P) :
      StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) :
        Set (TowerHilbert P →L[ℂ] TowerHilbert P))
  centralizer_centralizer' := by simp

/-- [KERNEL] ★★ A TORRE VIVE NO SEU FECHO: π(torre) ⊆ M_TGL. -/
theorem towerPi_mem_factor {N : ℕ}
    (x : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P x ∈ theFactorObject P := by
  show towerPi P x ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ (towerImage P) :
      StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) :
        Set (TowerHilbert P →L[ℂ] TowerHilbert P))
  rw [StarSubalgebra.mem_centralizer_iff]
  intro g hg
  rw [SetLike.mem_coe, StarSubalgebra.mem_centralizer_iff] at hg
  have h1 := hg (towerPi P x) (towerPi_mem_towerImage x)
  refine ⟨h1.1.symm, ?_⟩
  have h2 := congrArg star h1.2
  rw [star_mul, star_mul, star_star] at h2
  exact h2

/-! ## C — Ω é cíclico para o OBJETO e o estado GNS vive nele -/

/-- [KERNEL] ★★★ Ω É CÍCLICO PARA M_TGL: a órbita do objeto sobre o
    vetor do Nome é DENSA em H_φ. -/
theorem factor_omega_cyclic :
    Dense ((fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T (hOmega P)) ''
      (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P))) := by
  apply Dense.mono ?_ (towerPi_orbit_dense (P := P))
  rintro z ⟨p, rfl⟩
  exact ⟨towerPi P p.2, towerPi_mem_factor p.2, rfl⟩

/-- o estado vetorial de Ω sobre B(H_φ). -/
def omegaState (P : SiteProfile)
    (T : TowerHilbert P →L[ℂ] TowerHilbert P) : ℂ :=
  inner ℂ (hOmega P) (T (hOmega P))

/-- [KERNEL] ★★★ A IDENTIDADE GNS: ω(π(x)) = φ(x) — o estado coerente da
    torre inteira VIVE no objeto completado. -/
theorem omegaState_pi {N : ℕ} (x : Matrix (chainIdx N) (chainIdx N) ℂ) :
    omegaState P (towerPi P x) = tState P N x := by
  unfold omegaState
  rw [towerPi_omega]
  unfold hOmega
  rw [Completion.inner_coe]
  rw [show towerOmega P = tof P 0 1 from rfl]
  rw [show (inner ℂ (tof P 0 1) (tof P N x) : ℂ)
      = innerPre P (tof P 0 1) (tof P N x) from rfl]
  rw [innerPre_tof_at (Nat.zero_le N) (le_refl N), tPush_one, tPush_self]
  unfold tInner
  rw [conjTranspose_one, one_mul]

/-- [KERNEL] ★★★ A SÍNTESE DA PEDRA 86: o objeto existe (VonNeumannAlgebra),
    a torre vive nele, Ω é cíclico para ele, e o estado coerente é o estado
    vetorial de Ω — "o fator como objeto", o resíduo do v130 realizado. -/
theorem the_factor_as_object :
    (∀ (N : ℕ) (x : Matrix (chainIdx N) (chainIdx N) ℂ),
      towerPi P x ∈ theFactorObject P)
    ∧ Dense ((fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T (hOmega P)) ''
        (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)))
    ∧ (∀ (N : ℕ) (x : Matrix (chainIdx N) (chainIdx N) ℂ),
        omegaState P (towerPi P x) = tState P N x) :=
  ⟨fun _ x => towerPi_mem_factor x, factor_omega_cyclic,
   fun _ x => omegaState_pi x⟩

end

end TGLExt
