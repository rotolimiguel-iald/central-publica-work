-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_024 (06/09/2026), transposta em 06/09/2026
-- Lote 024..026: a perturbacao de GIBBS realizada no mesmo Hilbert da torre (estado fiel,
--   normalizado, distinto da orbita modular; resposta quadratica; calor/fonte por normalizacao);
--   o LIMITE TERMICO: para perfil constante nao tracial a preparacao NAO tem limite em norma
--   (nao-Cauchy) e o acoplamento da torre e ilimitado; corte com escala escolhida; AFINIDADE:
--   criterio exato (Cauchy <=> afinidade-limite > 0), estado global no Hilbert original, fiel e
--   ciclico; perfil gradual (muda em infinitos sitios, ainda fiel). Estatuto [REAL / INPUT / OPEN]:
--   selecao fisica, area, H3 dinamico, dimensao/assinatura, globalizacao e a classificacao geral
--   dos estados normais (disjuncao) seguem INPUT/OPEN — a bancada NAO promoveu nao-Cauchy a teorema
--   geral de disjuncao nem importou Kakutani.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100%; manifestos 202/206/220;
--   3/3 auditores da bancada exit 0; recompilacao INDEPENDENTE 22/22, axiomas no trio; guarda de
--   colisao estatica no ROOT; enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.CoherentMatterControls
import TGLExt.ModularPower

set_option autoImplicit false
set_option maxHeartbeats 7000000
namespace ChatgptAudit.Thermal024
open Matrix Filter Topology Set TGLExt ChatgptAudit.Micro021
noncomputable section

def modularLocalState (P : SiteProfile) (N : ℕ) (t : ℝ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) : ℂ :=
  omegaState P (modularConjugation P t (towerPi P a))

def modularLocalWeights (P : SiteProfile) (N : ℕ) (t : ℝ) (i : chainIdx N) : ℝ :=
  (modularLocalState P N t (Matrix.diagonal (Pi.single i (1:ℂ)))).re

theorem modular_local_state_constant (P : SiteProfile) (N : ℕ) (t : ℝ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    modularLocalState P N t a=tState P N a := by
  rw [modularLocalState,modularConjugation_preserves_state,omegaState_pi]

theorem modular_local_weights_constant (P : SiteProfile) (N : ℕ) (t : ℝ) (i : chainIdx N) :
    modularLocalWeights P N t i=towerW P N i := by
  simp [modularLocalWeights,modular_local_state_constant,tState,Pi.single_apply]

theorem modular_local_weights_eq (P : SiteProfile) (N : ℕ) (t : ℝ) :
    modularLocalWeights P N t=towerW P N := funext (modular_local_weights_constant P N t)

def canonicalModularStateCurve (P : SiteProfile) (N : ℕ) : DiagonalStateCurve (towerW P N) where
  weights := modularLocalWeights P N
  tangent := fun _ _ => 0
  at_zero := modular_local_weights_constant P N 0
  trace_one := by intro t; simp only [modular_local_weights_constant,towerW_sum]
  derivative_zero := by
    intro i
    simpa only [modular_local_weights_constant] using hasDerivAt_const (0:ℝ) (towerW P N i)
  derivative_past := by
    filter_upwards [] with t
    intro i
    simpa only [modular_local_weights_constant] using hasDerivAt_const t (towerW P N i)
  tangent_continuous := fun _ => continuousAt_const

theorem canonical_modular_entropy_constant (P : SiteProfile) (N : ℕ) (t : ℝ) :
    finiteEntropy ((canonicalModularStateCurve P N).weights t)=towerEntropy P N := by
  simp only [canonicalModularStateCurve,modular_local_weights_eq,towerEntropy]

theorem canonical_modular_increment_zero (P : SiteProfile) (N : ℕ) (t : ℝ) :
    modularIncrement (towerW P N) ((canonicalModularStateCurve P N).weights t)=0 := by
  simp only [canonicalModularStateCurve,modular_local_weights_eq,modular_increment_self]

theorem canonical_modular_relative_entropy_zero (P : SiteProfile) (N : ℕ) (t : ℝ) :
    diagonalRelativeEntropy ((canonicalModularStateCurve P N).weights t) (towerW P N)=0 := by
  simp only [canonicalModularStateCurve,modular_local_weights_eq,relative_entropy_self]

theorem canonical_modular_generator_constant (P : SiteProfile) (N : ℕ) (t : ℝ) :
    modularLocalState P N t (diagonalModularGenerator (towerW P N))=(towerEntropy P N : ℂ) := by
  rw [modular_local_state_constant,←tower_entropy_modular_expectation]

#print axioms modular_local_state_constant
#print axioms modular_local_weights_constant
#print axioms modular_local_weights_eq
#print axioms canonicalModularStateCurve
#print axioms canonical_modular_entropy_constant
#print axioms canonical_modular_increment_zero
#print axioms canonical_modular_relative_entropy_zero
#print axioms canonical_modular_generator_constant
end
end ChatgptAudit.Thermal024
