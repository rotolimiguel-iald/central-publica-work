import Mathlib

set_option autoImplicit false

/-!
# Probe -- API de projecao ortogonal (NAO importado pela biblioteca TGL)

RESOLVIDO: a projecao ortogonal como endomorfismo e' `Submodule.starProjection`.
  Submodule.starProjection            : (U : Submodule 𝕜 E) → [U.HasOrthogonalProjection] → E →L[𝕜] E
  Submodule.starProjection_apply_mem  : U.starProjection x ∈ U
  Submodule.starProjection_eq_self_iff: U.starProjection v = v ↔ v ∈ U
  Submodule.isIdempotentElem_starProjection : IsIdempotentElem U.starProjection

FALTA: o nome da AUTO-ADJUNCAO. Candidatos abaixo -- o que existir imprime a
assinatura; os demais acusam "Unknown constant" (que e' a informacao desejada).

Rodar:  lake env lean TGL/Probe.lean
-/

#check @Submodule.starProjection_isSelfAdjoint
#check @Submodule.starProjection_isSymmetric
#check @Submodule.inner_starProjection_left_eq_right
#check @Submodule.starProjection_inner_eq
#check @Submodule.isSelfAdjoint_starProjection
#check @Submodule.starProjection_adjoint
