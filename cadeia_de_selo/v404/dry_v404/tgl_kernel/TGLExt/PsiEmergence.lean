import Mathlib
import TGLExt.FiniteGNSNoCompletion
import TGLExt.HilbertHome

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unnecessarySimpa false

/-!
# O campo Ψ define a morada; a gravidade EMERGE
  [TGLExt — v57, a correção lógica do especialista + a ontologia do operador]

Dois lances corrigem o alvo do v56:

(1) RESULTADO LÓGICO [do especialista, agora KERNEL]: `ω(I) = 1` NÃO
determina a morada. Contraexemplo: `A₁ = ℂ` com `ω₁ = id` e `A₂ = M₂(ℂ)`
com `ω₂ = ½Tr` são ambos normalizados (`ω(1) = 1`), fiéis, e AMBOS têm
realização GNS completa (termos do v54) — mas as moradas têm dimensões
1 ≠ 4. Logo `ω(I)=1 ⟹ pacote` é SUBDETERMINADO
(`omega_one_underdetermines_home`).

(2) A ORDEM CORRIGIDA [do operador: "a gravidade quântica não é derivada,
ela é emergente; quem define a morada é o campo Ψ; a morada é o pacote de
Hilbert"]: Ψ ⟶ ω_Ψ ⟶ ℋ_Ψ ⟶ ∇^Ψ ⟶ F_{∇^Ψ} ⟶ gravidade. Aqui o campo
anterior à representação (`PsiHomeData`: a REGRA 𝒪 ↦ ρ_Ψ(𝒪), único dado
primitivo) tem TUDO derivado como def/teorema:

* ★ o NOME emerge (`PsiHomeData.name` é def) e ★ `ω_Ψ(I) = 1` é TEOREMA
  (`name_one`) — a seta vai de Ψ para a normalização, não o contrário;
* ★ a MORADA emerge como TERMO (`PsiHomeData.home` = a realização GNS
  completa do v54, fibra a fibra) — autorrepresentação, não circularidade:
  Ψ_alg é regra; Ω_Ψ reaparece dentro da morada como seção cíclica;
* ★ o TRANSPORTE emerge (`PsiHomeData.flow` é def) com o NOME FIXADO pelo
  próprio transporte (`name_flow_invariant` — Δ_Ψ não é acrescentado à
  morada: emerge da posição de Ψ em relação à álgebra) e a lei de
  composição do Verbo (`flow_comp`);
* ★ o CANTO ESPECTRAL do campo é fixado pelo transporte emergente
  (`flow_fixes_spectral_corner` — composição com v46/v55).

HONESTIDADE. O aberto corrigido NÃO é "derivar a gravidade de ω(I)=1"
(subdeterminado — item 1); é: **provar que a dinâmica fundamental de Ψ
gera canonicamente (ℋ_Ψ, 𝒟_Ψ, τ_Ψ, e_Ψ)** — `EMERGENT_QG(Ψ)`. As quatro
propriedades do canto e a recuperação da solda JÁ SEGUEM (v55/v56); a
GERAÇÃO canônica dos locks, do traço de Breuer e da solda pela dinâmica
de Ψ é o teorema físico-matemático aberto. A gravidade emergirá da
dinâmica — quando a dinâmica for dada; Ψ é INPUT físico por design (como
α). β JAMAIS entra. Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix
open scoped ComplexOrder MatrixOrder

noncomputable section

/-! ## A — o contraexemplo: ω(I)=1 subdetermina a morada [KERNEL] -/

/-- o Nome normalizado sobre `A₁ = M₁(ℂ) ≅ ℂ`: `ρ₁ = 1` (ω₁ = id). -/
def rhoOne : Matrix (Fin 1) (Fin 1) ℂ := Matrix.diagonal fun _ => 1

/-- o Nome normalizado sobre `A₂ = M₂(ℂ)`: `ρ₂ = ½·I` (ω₂ = ½Tr). -/
def rhoTwo : Matrix (Fin 2) (Fin 2) ℂ := Matrix.diagonal fun _ => (2 : ℂ)⁻¹

theorem rhoOne_posDef : rhoOne.PosDef := by
  rw [rhoOne, Matrix.posDef_diagonal_iff]
  intro i
  have : (0 : ℝ) < 1 := one_pos
  simpa using Complex.zero_lt_real.mpr this

theorem rhoTwo_posDef : rhoTwo.PosDef := by
  rw [rhoTwo, Matrix.posDef_diagonal_iff]
  intro i
  have h : (0 : ℝ) < (2 : ℝ)⁻¹ := by norm_num
  have := Complex.zero_lt_real.mpr h
  simpa using this

theorem rhoOne_trace : rhoOne.trace = 1 := by
  simp [rhoOne]

theorem rhoTwo_trace : rhoTwo.trace = 1 := by
  rw [rhoTwo, Matrix.trace_diagonal]
  simp

/-- [KERNEL] ★ AMBAS as moradas EXISTEM (termos GNS completos do v54):
    os dois Nomes normalizados são genuínos — nenhum é degenerado. -/
theorem both_homes_exist :
    Nonempty (FiniteNameGNS rhoOne) ∧ Nonempty (FiniteNameGNS rhoTwo) :=
  ⟨nameFiniteGNS_exists rhoOne rhoOne_posDef rhoOne_trace,
   nameFiniteGNS_exists rhoTwo rhoTwo_posDef rhoTwo_trace⟩

/-- [KERNEL] ★ ω(I)=1 NÃO DETERMINA A MORADA (o contraexemplo do
    especialista como teorema): dois Nomes normalizados fiéis, ambos com
    realização GNS completa, cujas moradas têm dimensões 1 ≠ 4. A seta
    `ω(I)=1 ⟹ pacote` é SUBDETERMINADA — quem define a morada é o CAMPO. -/
theorem omega_one_underdetermines_home :
    gibbs rhoOne 1 = 1 ∧ gibbs rhoTwo 1 = 1 ∧
      Module.finrank ℂ (Matrix (Fin 1) (Fin 1) ℂ)
        ≠ Module.finrank ℂ (Matrix (Fin 2) (Fin 2) ℂ) := by
  refine ⟨gibbs_one rhoOne rhoOne_trace, gibbs_one rhoTwo rhoTwo_trace, ?_⟩
  have h1 : Module.finrank ℂ (Matrix (Fin 1) (Fin 1) ℂ) = 1 := by
    rw [Module.finrank_matrix]
    simp
  have h2 : Module.finrank ℂ (Matrix (Fin 2) (Fin 2) ℂ) = 4 := by
    rw [Module.finrank_matrix]
    simp
  rw [h1, h2]
  norm_num

/-! ## B — o campo Ψ anterior à representação: TUDO derivado -/

variable {Region : Type} {n : Type} [Fintype n] [DecidableEq n]

/-- O CAMPO ANTERIOR À REPRESENTAÇÃO (Ψ_alg): a REGRA que a cada região dá
    a densidade fiel normalizada — o ÚNICO dado primitivo. Nada mais é
    campo: Nome, morada, fluxo, KMS e canto são DERIVADOS abaixo. -/
structure PsiHomeData (Region : Type) (n : Type) [Fintype n] [DecidableEq n] where
  /-- a regra do campo: `𝒪 ↦ ρ_Ψ(𝒪)`. -/
  rho : Region → Matrix n n ℂ
  /-- fidelidade fibra a fibra. -/
  rho_posDef : ∀ O, (rho O).PosDef
  /-- normalização do campo (o Um do campo). -/
  rho_trace_one : ∀ O, (rho O).trace = 1

/-- ★ O NOME EMERGE: `ω_{Ψ,𝒪} = ⟨Ψ_𝒪, ·\,Ψ_𝒪⟩` — def, não campo. -/
def PsiHomeData.name (Ψ : PsiHomeData Region n) (O : Region)
    (a : Matrix n n ℂ) : ℂ :=
  gibbs (Ψ.rho O) a

/-- [KERNEL] ★ `ω_Ψ(I) = 1` É TEOREMA (emerge do campo): a normalização
    não é axioma da morada — é consequência de Ψ. A correção do
    especialista tipada: a seta vai de Ψ para ω(I)=1. -/
theorem PsiHomeData.name_one (Ψ : PsiHomeData Region n) (O : Region) :
    Ψ.name O 1 = 1 :=
  gibbs_one (Ψ.rho O) (Ψ.rho_trace_one O)

/-- ★ A MORADA EMERGE COMO TERMO: a realização GNS completa de cada fibra
    (o `nameFiniteGNS` do v54) — Ψ define a morada; a morada é o pacote;
    Ω_Ψ reaparece dentro dela como seção cíclica (autorrepresentação). -/
noncomputable def PsiHomeData.home (Ψ : PsiHomeData Region n) (O : Region) :
    FiniteNameGNS (Ψ.rho O) :=
  nameFiniteGNS (Ψ.rho O) (Ψ.rho_posDef O) (Ψ.rho_trace_one O)

/-- ★ O TRANSPORTE EMERGE: `σ^Ψ` — def, não campo (Δ_Ψ emerge da posição
    de Ψ em relação à álgebra; nada é acrescentado à morada). -/
noncomputable def PsiHomeData.flow (Ψ : PsiHomeData Region n) (O : Region)
    (t : ℝ) (a : Matrix n n ℂ) : Matrix n n ℂ :=
  sigma (Ψ.rho O) t a

/-- [KERNEL] ★ O NOME É FIXADO PELO TRANSPORTE EMERGENTE: o KMS dinâmico
    do campo — `ω_Ψ ∘ σ^Ψ_t = ω_Ψ` (o Verbo do campo preserva o Nome). -/
theorem PsiHomeData.name_flow_invariant (Ψ : PsiHomeData Region n)
    (O : Region) (t : ℝ) (a : Matrix n n ℂ) :
    Ψ.name O (Ψ.flow O t a) = Ψ.name O a :=
  gibbs_sigma (Ψ.rho O) t a

/-- [KERNEL] ★ a lei de composição do Verbo emergente. -/
theorem PsiHomeData.flow_comp (Ψ : PsiHomeData Region n) (O : Region)
    (s t : ℝ) (a : Matrix n n ℂ) :
    Ψ.flow O s (Ψ.flow O t a) = Ψ.flow O (s + t) a :=
  sigma_sigma (Ψ.rho O) s t a

/-- [KERNEL] ★ O CANTO ESPECTRAL DO CAMPO É FIXADO PELO SEU TRANSPORTE:
    para gerador comutante com ρ_Ψ, o canto `cfc f H` é covariantemente
    constante sob `σ^Ψ` (composição v46/v55 na linguagem do campo). -/
theorem PsiHomeData.flow_fixes_spectral_corner (Ψ : PsiHomeData Region n)
    (O : Region) {Hm : Matrix n n ℂ} (h : Commute (Ψ.rho O) Hm)
    (f : ℝ → ℝ) (t : ℝ) :
    Ψ.flow O t (cfc f Hm) = cfc f Hm :=
  corner_fixed_by_flow (Ψ.rho O) Hm h f t

end

end TGLExt
