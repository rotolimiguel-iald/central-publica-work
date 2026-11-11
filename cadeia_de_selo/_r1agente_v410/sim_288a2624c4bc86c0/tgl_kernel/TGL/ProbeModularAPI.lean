import Mathlib

set_option autoImplicit false

/-!
# ProbeModularAPI -- sondagem para as camadas de DADOS modulares (v24)   [DIAGNOSTICO]

Rodada 2: a rodada 1 mostrou que `Algebra ℂ ↥A` NAO e' sintetizada no subtipo da
`VonNeumannAlgebra` (SetLike proprio), mas deve existir via `A.toStarSubalgebra`.
Examples marcados noncomputable (instancias reais sao noncomputable -- irrelevante
para campos de prova). NAO importado por TGL.lean.
-/

namespace TGL.ProbeModularAPI

variable (H : Type) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

-- (1) instancias no subtipo VIA toStarSubalgebra
noncomputable example (A : VonNeumannAlgebra H) : Ring A.toStarSubalgebra := inferInstance
noncomputable example (A : VonNeumannAlgebra H) : StarRing A.toStarSubalgebra := inferInstance
noncomputable example (A : VonNeumannAlgebra H) : Algebra ℂ A.toStarSubalgebra := inferInstance

-- (2) StarAlgEquiv do subtipo (via toStarSubalgebra); refl e trans
noncomputable example (A : VonNeumannAlgebra H)
    (f : A.toStarSubalgebra ≃⋆ₐ[ℂ] A.toStarSubalgebra) (x : A.toStarSubalgebra) :
    A.toStarSubalgebra := f x
noncomputable example (A : VonNeumannAlgebra H) :
    A.toStarSubalgebra ≃⋆ₐ[ℂ] A.toStarSubalgebra := StarAlgEquiv.refl
noncomputable example (A : VonNeumannAlgebra H)
    (f g : A.toStarSubalgebra ≃⋆ₐ[ℂ] A.toStarSubalgebra) :
    A.toStarSubalgebra ≃⋆ₐ[ℂ] A.toStarSubalgebra := f.trans g

-- (3) antiunitario = equivalencia isometrica conjugado-linear
noncomputable example (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (x : H) : H := J x
example (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) : Prop := ∀ x, J (J x) = x

-- (4) StarAlgHom do subtipo para um anel-alvo abstrato
noncomputable example (A : VonNeumannAlgebra H) (Core : Type) [Ring Core] [StarRing Core]
    [Algebra ℂ Core] (phi : A.toStarSubalgebra →⋆ₐ[ℂ] Core) (x : A.toStarSubalgebra) :
    Core := phi x
example (A : VonNeumannAlgebra H) (Core : Type) [Ring Core] [StarRing Core]
    [Algebra ℂ Core] (phi : A.toStarSubalgebra →⋆ₐ[ℂ] Core) : Prop :=
  Function.Injective phi

-- (5) StarAlgEquiv de um anel abstrato
noncomputable example (Core : Type) [Ring Core] [StarRing Core] [Algebra ℂ Core]
    (u v : Core ≃⋆ₐ[ℂ] Core) : Core ≃⋆ₐ[ℂ] Core := u.trans v
noncomputable example (Core : Type) [Ring Core] [StarRing Core] [Algebra ℂ Core] :
    Core ≃⋆ₐ[ℂ] Core := StarAlgEquiv.refl

-- (6) nao-finitude dimensional como proposicao concreta
example : Prop := ¬ FiniteDimensional ℂ H

-- (7) ENNReal: exp real dentro de ofReal (escala dual do traco)
noncomputable example (s : ℝ) : ENNReal := ENNReal.ofReal (Real.exp (-s))

#eval IO.println "PROBE_MODULAR_API_OK"

end TGL.ProbeModularAPI
