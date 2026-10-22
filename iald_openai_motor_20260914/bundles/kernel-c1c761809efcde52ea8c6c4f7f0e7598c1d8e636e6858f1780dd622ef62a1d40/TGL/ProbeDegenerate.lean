import TGL.SpecificAQFTWitness

set_option autoImplicit false

/-!
# ProbeDegenerate -- segundo controle negativo (v23.1/v24)   [DIAGNOSTICO]

Tenta habitar a testemunha-BASE rigida com um modelo FISICAMENTE VAZIO:
`H = ℂ²` (finito), rede CONSTANTE, `U ≡ 1`. As paredes esperadas sao as
fisicas: localidade (a rede constante nao-abeliana teria de comutar em pares
tipo-espaco), cunha nao-abeliana (o exibidor trivial e' refutavel) e
ciclicidade/separacao do vacuo. NAO importado por TGL.lean; fora do lake build.

VEREDITO = returncode. Se este arquivo COMPILAR, a testemunha-base ainda admite
modelo degenerado (negativo honesto a reportar). Se FALHAR, registra-se apenas
que ESTE probe degenerado foi rejeitado -- nunca universalidade.
-/

namespace TGL.ProbeDegenerate

open TGL.SpecificAQFT

/-- Tentativa degenerada: rede constante `A`, translacoes triviais. -/
noncomputable example (A : VonNeumannAlgebra (EuclideanSpace ℂ (Fin 2)))
    (v : EuclideanSpace ℂ (Fin 2)) (hv : ‖v‖ = 1) :
    TGLSpecificAQFTWitness where
  m := 1
  H := EuclideanSpace ℂ (Fin 2)
  net := fun _ => A
  vac := v
  U := fun _ => 1
  m_pos := one_pos
  vac_norm := hv
  isotony := fun _ _ _ => subset_rfl
  -- PAREDE 1: localidade da rede constante exigiria comutatividade global
  locality := fun _ _ _ a _ b _ => Commute.all a b
  U_zero := rfl
  U_add := fun _ _ => (one_mul (1 : _)).symm
  U_star := fun _ => star_one _
  covariance := fun a O x => by simp
  vac_invariant := fun _ => rfl
  -- PAREDE 2: o exibidor trivial (1,1) e' refutavel: 1*1 = 1*1
  wedge_nonabelian := ⟨1, one_mem _, 1, one_mem _, by simp⟩
  -- PAREDE 3: ciclicidade do vacuo nao sai por simp num modelo vazio
  vac_cyclic_wedge := by simp
  -- PAREDE 4: separacao do vacuo nao sai por simp num modelo vazio
  vac_separating_wedge := fun a _ h => by simpa using h

#eval IO.println "PROBE_DEGENERATE_COMPILES__BASE_WITNESS_ADMITS_DEGENERATE_MODEL"

end TGL.ProbeDegenerate
