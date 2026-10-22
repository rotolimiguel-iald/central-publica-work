import Mathlib
import TGL.ContinuousCornerAbstract

set_option autoImplicit false

/-!
# Testemunha AQFT especifica RIGIDA   [KERNEL/CONDITIONAL]   witness_constructed = TRUE desde v135 (TGLExt/WedgeNet: theSpecificAQFTWitness; nesta v23 era false)

v23 -- RIGIDIFICACAO (interface = luz = (forma = conteudo)).

A versao v22 desta estrutura era uma lista de campos `: Prop` (forma SEM conteudo):
trivialmente habitavel (`Region := Unit`, tudo `True`), como o controle negativo
`TGL/ProbeTrivial.lean` PROVOU ao compilar. `Nonempty` daquele tipo era VACUO.
(O original frouxo esta preservado em `SpecificAQFTWitness.lean.bak_v22_loose`.)

Nesta versao a testemunha e' o CONTEUDO CARREGANDO A PROVA DE QUE E' A FORMA:

    W  ~  Sigma_{x : Conteudo} Realiza(x, Forma)

  [DATA]          massa `m`, espaco de Hilbert `H`, rede `net : regioes -> vN-algebras`,
                  vacuo `vac`, translacoes `U` -- o conteudo fisico-matematico concreto.
  [KERNEL-RIGID]  cada obrigacao e' uma PROPOSICAO CONCRETA sobre esses dados
                  (isotonia, localidade em separacao tipo-espaco de Minkowski,
                  covariancia por translacao, vacuo invariante/ciclico/separador,
                  nao-abelianidade da cunha). Preencher exige matematica real.
  [EXTERNAL-KNOWN / OPEN]  o residuo modular NAO-enunciavel na mathlib de hoje
                  (tipo III_1, Bisognano--Wichmann, core de Takesaki, afiliacao de
                  H_3L, projecao espectral do zero, traco canonico, covariancia de
                  Poincare de P_F) fica QUARENTENADO em `TGLWitnessModularObligations`,
                  nomeado campo a campo -- nunca `axiom`, nunca escondido.
                  Formaliza-lo E' parte do teorema aberto.

  -- No inhabitant of TGLSpecificAQFTWitness is constructed in v23.
  -- ERRATA v304 (ao lado): desde a v135, TGLExt.theSpecificAQFTWitness O HABITA
  -- (WedgeNet). O aberto que resta e a realizacao modular (TGLModularRealization).

O criterio de rigidez e' MEDIDO, nao declarado: `TGL/ProbeTrivial.lean` (o habitante
trivial da versao frouxa) DEVE deixar de compilar contra esta estrutura. Nenhum
`sorry`/`axiom` aqui.
-/

namespace TGL.SpecificAQFT

open TGL.ContinuousCorner

/-- Forma quadratica de Minkowski em `ℝ^{1,3}`, assinatura `(+,-,-,-)`. [DATA/geometria] -/
def minkowskiSq (v : Fin 4 → ℝ) : ℝ :=
  v 0 ^ 2 - v 1 ^ 2 - v 2 ^ 2 - v 3 ^ 2

/-- Separacao tipo-espaco entre regioes: todo par de pontos e' spacelike. -/
def SpacelikeSep (O₁ O₂ : Set (Fin 4 → ℝ)) : Prop :=
  ∀ x ∈ O₁, ∀ y ∈ O₂, minkowskiSq (x - y) < 0

/-- Cunha direita de Rindler: `|x⁰| < x¹`. -/
def rightWedge : Set (Fin 4 → ℝ) := {x | |x 0| < x 1}

/-- Cunha esquerda: `|x⁰| < -x¹` (reflexao da direita). -/
def leftWedge : Set (Fin 4 → ℝ) := {x | |x 0| < -(x 1)}

/-- Translacao de uma regiao por `a`. -/
def translate (a : Fin 4 → ℝ) (O : Set (Fin 4 → ℝ)) : Set (Fin 4 → ℝ) :=
  (fun x => x + a) '' O

/-- [KERNEL, incondicional] As duas cunhas sao tipo-espaco separadas -- geometria
    de Minkowski provada pelo kernel, nao assumida. -/
theorem wedges_spacelike : SpacelikeSep rightWedge leftWedge := by
  intro x hx y hy
  simp only [rightWedge, Set.mem_setOf_eq] at hx
  simp only [leftWedge, Set.mem_setOf_eq] at hy
  obtain ⟨hx1, hx2⟩ := abs_lt.mp hx
  obtain ⟨hy1, hy2⟩ := abs_lt.mp hy
  simp only [minkowskiSq, Pi.sub_apply]
  have hposdiff : 0 < (x 1 - y 1) - (x 0 - y 0) := by linarith
  have hpossum : 0 < (x 1 - y 1) + (x 0 - y 0) := by linarith
  nlinarith [sq_nonneg (x 2 - y 2), sq_nonneg (x 3 - y 3), mul_pos hposdiff hpossum]

/-- A testemunha AQFT especifica RIGIDA: o conteudo (rede de von Neumann sobre
    `ℝ^{1,3}`, vacuo, translacoes, massa) acompanhado das provas de que ele
    realiza a forma. NENHUMA instancia e' construida em v23. -/
structure TGLSpecificAQFTWitness where
  -- [DATA] o conteudo fisico-matematico concreto
  /-- massa do campo escalar livre (dado fisico do modelo v21-A) -/
  m : ℝ
  /-- espaco de Hilbert do setor de vacuo -/
  H : Type
  [instNormed : NormedAddCommGroup H]
  [instInner : InnerProductSpace ℂ H]
  [instComplete : CompleteSpace H]
  /-- a rede local: regioes de `ℝ^{1,3}` → algebras de von Neumann em `B(H)` -/
  net : Set (Fin 4 → ℝ) → VonNeumannAlgebra H
  /-- o vetor de vacuo -/
  vac : H
  /-- representacao das translacoes de `ℝ^{1,3}` -/
  U : (Fin 4 → ℝ) → (H →L[ℂ] H)
  -- [KERNEL-RIGID] forma = conteudo: proposicoes concretas sobre os dados
  m_pos : 0 < m
  vac_norm : ‖vac‖ = 1
  /-- isotonia (Haag--Kastler): regiao maior, algebra maior -/
  isotony : ∀ O₁ O₂ : Set (Fin 4 → ℝ), O₁ ⊆ O₂ →
    (net O₁ : Set (H →L[ℂ] H)) ⊆ (net O₂ : Set (H →L[ℂ] H))
  /-- localidade (Haag--Kastler): observaveis em regioes tipo-espaco comutam -/
  locality : ∀ O₁ O₂ : Set (Fin 4 → ℝ), SpacelikeSep O₁ O₂ →
    ∀ a ∈ net O₁, ∀ b ∈ net O₂, Commute a b
  /-- grupo de translacoes: identidade, aditividade, unitariedade -/
  U_zero : U 0 = 1
  U_add : ∀ v w : Fin 4 → ℝ, U (v + w) = U v * U w
  U_star : ∀ v : Fin 4 → ℝ, star (U v) = U (-v)
  /-- covariancia por translacao da rede -/
  covariance : ∀ (a : Fin 4 → ℝ) (O : Set (Fin 4 → ℝ)) (x : H →L[ℂ] H),
    x ∈ net O ↔ U a * x * U (-a) ∈ net (translate a O)
  /-- o vacuo e' invariante por translacao -/
  vac_invariant : ∀ a : Fin 4 → ℝ, U a vac = vac
  /-- a algebra da cunha e' nao-abeliana (exclui degenerados comutativos) -/
  wedge_nonabelian : ∃ a ∈ net rightWedge, ∃ b ∈ net rightWedge, a * b ≠ b * a
  /-- [EXTERNAL-KNOWN: Reeh--Schlieder, aqui ENUNCIADO concretamente]
      o vacuo e' ciclico para a algebra da cunha -/
  vac_cyclic_wedge :
    Dense ((Submodule.span ℂ
      ((fun T : H →L[ℂ] H => T vac) '' (net rightWedge : Set (H →L[ℂ] H))) :
        Submodule ℂ H) : Set H)
  /-- [EXTERNAL-KNOWN: Reeh--Schlieder] o vacuo e' separador para a cunha -/
  vac_separating_wedge : ∀ a ∈ net rightWedge, (a : H →L[ℂ] H) vac = 0 → a = 0

attribute [instance] TGLSpecificAQFTWitness.instNormed
attribute [instance] TGLSpecificAQFTWitness.instInner
attribute [instance] TGLSpecificAQFTWitness.instComplete

/-- [KERNEL, condicional a `W` -- e aqui `W` e' USADO de verdade] Localidade das
    cunhas: toda observavel da cunha direita comuta com toda da esquerda, pela
    localidade de `W` aplicada ao teorema geometrico `wedges_spacelike`. -/
theorem wedge_locality (W : TGLSpecificAQFTWitness) :
    ∀ a ∈ W.net rightWedge, ∀ b ∈ W.net leftWedge, Commute a b :=
  fun a ha b hb => W.locality rightWedge leftWedge wedges_spacelike a ha b hb

/- v24: a antiga `TGLWitnessModularObligations` (campos `: Prop`, forma sem
   conteudo) foi SUBSTITUIDA pelas camadas de DADOS de `TGL/ModularRealization.lean`
   (WedgeModularData / ContinuousCoreData / ThreeLocksCoreData). Os teoremas
   `continuousCorner_of_witness` / `threeLocksCorner_of_witness` vivem la',
   com os MESMOS nomes e conteudo agora composicional (`cornerOf R`). O que a
   mathlib nao enuncia vive no ledger externo do um.py, nunca em campo `: Prop`. -/

end TGL.SpecificAQFT
