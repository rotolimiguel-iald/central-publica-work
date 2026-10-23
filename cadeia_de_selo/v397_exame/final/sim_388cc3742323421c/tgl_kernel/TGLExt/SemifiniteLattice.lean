import TGLExt.ThreeLocksCorner

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O RETICULADO GENUINAMENTE SEMIFINITO: a morada ∞-dim da camada da dimensão
  [TGLExt — v80, o incremento 3 do programa SemifiniteAnalysis]

O v77 habitou a camada abstrata (v64) em dimensão finita; o v79 a disparou
sobre o operador da teoria. MAS em dimensão finita a semifinitude é a
finitude (τ(⊤)<∞) — o gap = ⊤ sempre serve, e a correção da Resposta 8
(gap LOCAL, não global) parece opcional. Esta pedra remove a hipótese de
finitude do espaço ambiente e mostra que, em dimensão INFINITA:

* o traço da dimensão continua camada tracial FIEL e MONÓTONA — mas agora
  GENUINAMENTE semifinita: τ(⊤) = ⊤ e todo subespaço não-trivial domina
  um subespaço de peso finito (= 1, o átomo);
* **o gap GLOBAL é IMPOSSÍVEL POR TEOREMA** — a correção da parede (v64,
  Resposta 8: "o certo é o GAP LOCAL") deixa de ser escolha e vira
  NECESSIDADE do reticulado;
* o Breuer LOCAL dispara: kernel não-trivial sob um gap de dimensão
  finita ⟹ 0 < τ(ker) < ∞ — num espaço onde o todo pesa ⊤;
* a morada existe: ℕ →₀ K é genuinamente ∞-dim e o pacote local é
  HABITADO nela, com τ(ker) = 1 = ω(I) e τ(⊤) = ⊤.

O QUE ESTA PEDRA PROVA [KERNEL]:

* `semifiniteDimTrace` — [DATA] τ = dim-ou-⊤ sobre Submodule K V, SEM
  hipótese de finitude em V: fiel + monótona (a 1ª instância da camada
  v64 que NÃO é um caso finito disfarçado);
* ★ `semifinite_trace_bot` / ★ `semifinite_trace_atom` — τ(⊥) = 0 e
  τ(K·x) = 1 para x ≠ 0: O ÁTOMO PESA 1 — ω(I) = 1 no reticulado;
* ★★ `semifinite_trace_is_semifinite` — O AXIOMA DA SEMIFINITUDE, agora
  genuíno: todo S ≠ ⊥ contém T ≠ ⊥ com τ(T) = 1 < ∞ (o Nome habita todo
  canto não-trivial);
* ★ `semifinite_trace_top_infinite` — em ∞-dim, τ(⊤) = ⊤ (o todo pesa
  infinito — o território II_∞ no nível do reticulado);
* ★★ `global_gap_impossible_infinite_dim` — **a REFUTAÇÃO do global como
  teorema**: em ∞-dim NÃO existe gap = ⊤ com peso finito; o certificado
  local do v64 é a ÚNICA porta (eco em reticulado do
  global_tau_compactness_refuted);
* ★★ `infinite_dim_local_breuer_weight` — o Breuer abstrato (v64) dispara
  em ∞-dim: ker ≠ ⊥ sob gap de dim finita ⟹ 0 < τ(ker) < ∞, e o kernel
  é finito-dimensional (a inscrição é finita DENTRO do infinito);
* ★ `not_finiteDimensional_finsupp` — ℕ →₀ K é genuinamente ∞-dim
  (a morada concreta existe);
* ★★ `first_infinite_dim_inhabitant` — o pacote local de Breuer é
  HABITADO em ℕ →₀ K: τ(ker) = 1 = ω(I) num espaço com τ(⊤) = ⊤.

HONESTIDADE: reticulado de TODOS os subespaços (face algébrica) — o
reticulado de projeções ORTOGONAIS de um Hilbert ∞-dim (subespaços
FECHADOS, comutantes, normalidade do τ) é o próximo tijolo; nada aqui é
III₁; nenhuma flag do fecho se move. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal

noncomputable section

variable (K : Type) [Field K] {V : Type} [AddCommGroup V] [Module K V]

/-- [DEF] dimensão-ou-⊤: o peso de um subespaço é sua dimensão se finita,
    e ⊤ caso contrário. -/
noncomputable def dimOrTop (S : Submodule K V) : ℝ≥0∞ :=
  open Classical in
  if FiniteDimensional K S then (Module.finrank K S : ℝ≥0∞) else ⊤

theorem dimOrTop_of_finite {S : Submodule K V} (h : FiniteDimensional K S) :
    dimOrTop K S = (Module.finrank K S : ℝ≥0∞) := by
  unfold dimOrTop
  exact if_pos h

theorem dimOrTop_of_infinite {S : Submodule K V} (h : ¬FiniteDimensional K S) :
    dimOrTop K S = ⊤ := by
  unfold dimOrTop
  exact if_neg h

/-- [KERNEL] o peso é finito EXATAMENTE nos subespaços de dimensão finita. -/
theorem dimOrTop_lt_top_iff {S : Submodule K V} :
    dimOrTop K S < ⊤ ↔ FiniteDimensional K S := by
  constructor
  · intro h
    by_contra hS
    rw [dimOrTop_of_infinite K hS] at h
    exact lt_irrefl ⊤ h
  · intro h
    rw [dimOrTop_of_finite K h]
    exact ENNReal.natCast_lt_top _

variable (V) in
/-- [DATA — a 1ª instância GENUINAMENTE SEMIFINITA da camada v64] τ = dim-ou-⊤
    no reticulado de TODOS os subespaços de V, SEM hipótese de finitude no
    ambiente: FIEL e MONÓTONA. -/
def semifiniteDimTrace : SemifiniteTraceData (Submodule K V) where
  tau := fun S => dimOrTop K S
  mono := by
    intro p q hpq
    by_cases hq : FiniteDimensional K q
    · haveI := hq
      haveI hp : FiniteDimensional K p :=
        (Submodule.comapSubtypeEquivOfLe hpq).finiteDimensional
      rw [dimOrTop_of_finite K hp, dimOrTop_of_finite K hq]
      have hle : Module.finrank K p ≤ Module.finrank K q := by
        calc Module.finrank K p
            = Module.finrank K (p.comap q.subtype) :=
              (Submodule.comapSubtypeEquivOfLe hpq).finrank_eq.symm
          _ ≤ Module.finrank K q := Submodule.finrank_le _
      exact_mod_cast hle
    · rw [dimOrTop_of_infinite K hq]
      exact le_top
  faithful := by
    intro p hp
    by_cases hpf : FiniteDimensional K p
    · haveI := hpf
      rw [dimOrTop_of_finite K hpf] at hp
      have h0 : Module.finrank K p = 0 := by exact_mod_cast hp
      exact (Submodule.finrank_eq_zero (R := K)).mp h0
    · rw [dimOrTop_of_infinite K hpf] at hp
      exact absurd hp ENNReal.top_ne_zero

/-- [KERNEL] ★ τ(⊥) = 0 — o vazio não pesa (agora sem finitude ambiente). -/
theorem semifinite_trace_bot :
    (semifiniteDimTrace K V).tau ⊥ = 0 := by
  have : FiniteDimensional K (⊥ : Submodule K V) := inferInstance
  show dimOrTop K (⊥ : Submodule K V) = 0
  rw [dimOrTop_of_finite K this]
  simp

/-- [KERNEL] ★ O ÁTOMO PESA 1: τ(K·x) = 1 para x ≠ 0 — ω(I) = 1 no
    reticulado; a linha do Um pesa exatamente a identidade. -/
theorem semifinite_trace_atom (x : V) (hx : x ≠ 0) :
    (semifiniteDimTrace K V).tau (K ∙ x) = 1 := by
  have hfd : FiniteDimensional K (K ∙ x) := inferInstance
  show dimOrTop K (K ∙ x) = 1
  rw [dimOrTop_of_finite K hfd, finrank_span_singleton hx]
  simp

/-- [KERNEL] ★★ O AXIOMA DA SEMIFINITUDE, genuíno: todo subespaço
    não-trivial CONTÉM um subespaço de peso 1 — o Nome habita todo canto
    não-trivial, mesmo quando o todo pesa ⊤. -/
theorem semifinite_trace_is_semifinite (S : Submodule K V) (hS : S ≠ ⊥) :
    ∃ T : Submodule K V, T ≤ S ∧ T ≠ ⊥ ∧ (semifiniteDimTrace K V).tau T = 1 := by
  obtain ⟨x, hxS, hx0⟩ := (Submodule.ne_bot_iff S).mp hS
  refine ⟨K ∙ x, ?_, ?_, semifinite_trace_atom K x hx0⟩
  · exact (Submodule.span_singleton_le_iff_mem x S).mpr hxS
  · intro h
    exact hx0 (Submodule.span_singleton_eq_bot.mp h)

/-- [KERNEL] ★ em dimensão INFINITA o todo pesa ⊤ — a semifinitude deixa
    de ser finitude: o território II_∞ no nível do reticulado. -/
theorem semifinite_trace_top_infinite (hV : ¬FiniteDimensional K V) :
    (semifiniteDimTrace K V).tau ⊤ = ⊤ := by
  have htop : ¬FiniteDimensional K (⊤ : Submodule K V) := by
    intro h
    haveI := h
    exact hV (Submodule.topEquiv.finiteDimensional)
  show dimOrTop K (⊤ : Submodule K V) = ⊤
  exact dimOrTop_of_infinite K htop

/-- [KERNEL] ★★ A REFUTAÇÃO DO GLOBAL COMO TEOREMA: em ∞-dim NÃO existe
    certificado com gap = ⊤ (peso finito no todo é impossível) — o gap
    LOCAL do v64 (Resposta 8) é a ÚNICA porta; a correção da parede era
    necessidade, não escolha. -/
theorem global_gap_impossible_infinite_dim (hV : ¬FiniteDimensional K V) :
    ¬((semifiniteDimTrace K V).tau ⊤ < ⊤) := by
  rw [semifinite_trace_top_infinite K hV]
  exact lt_irrefl ⊤

/-- [DATA] o pacote de gap LOCAL em dimensão qualquer: kernel não-trivial
    sob um gap de dimensão FINITA. -/
def infiniteDimLocalGapPackage (kr gp : Submodule K V)
    (hker : kr ≠ ⊥) (hle : kr ≤ gp) (hgp : FiniteDimensional K gp) :
    BreuerGapData (Submodule K V) (semifiniteDimTrace K V) where
  ker := kr
  gap := gp
  ker_le_gap := hle
  gap_finite := by
    show dimOrTop K gp < ⊤
    exact (dimOrTop_lt_top_iff K).mpr hgp
  ker_ne_bot := hker

/-- [KERNEL] ★★ O BREUER LOCAL DISPARA EM ∞-DIM: kernel não-trivial sob
    gap finito ⟹ 0 < τ(ker) < ∞ E o kernel é finito-dimensional — a
    inscrição é FINITA dentro do infinito (o certificado do v64 na sua
    morada genuína). -/
theorem infinite_dim_local_breuer_weight (kr gp : Submodule K V)
    (hker : kr ≠ ⊥) (hle : kr ≤ gp) (hgp : FiniteDimensional K gp) :
    (0 < (semifiniteDimTrace K V).tau kr ∧
      (semifiniteDimTrace K V).tau kr < ⊤) ∧ FiniteDimensional K kr := by
  have hw := breuer_kernel_weight (infiniteDimLocalGapPackage K kr gp hker hle hgp)
  haveI := hgp
  exact ⟨hw, (Submodule.comapSubtypeEquivOfLe hle).finiteDimensional⟩

/-- [KERNEL] ★ a morada concreta existe: ℕ →₀ K é GENUINAMENTE ∞-dim
    (a base canônica é infinita). -/
theorem not_finiteDimensional_finsupp : ¬FiniteDimensional K (ℕ →₀ K) := by
  intro h
  haveI := h
  haveI : Fintype ℕ :=
    FiniteDimensional.fintypeBasisIndex (Finsupp.basisSingleOne (R := K) (ι := ℕ))
  exact not_finite ℕ

/-- [KERNEL] ★★ O PRIMEIRO HABITANTE ∞-DIM: em ℕ →₀ K o pacote local de
    Breuer é HABITADO — τ(ker) = 1 = ω(I) num espaço onde τ(⊤) = ⊤.
    O Nome pesa 1 dentro do infinito. -/
theorem first_infinite_dim_inhabitant :
    ∃ G : BreuerGapData (Submodule K (ℕ →₀ K)) (semifiniteDimTrace K (ℕ →₀ K)),
      (semifiniteDimTrace K (ℕ →₀ K)).tau G.ker = 1 ∧
        (semifiniteDimTrace K (ℕ →₀ K)).tau ⊤ = ⊤ := by
  have hx : (Finsupp.single 0 (1 : K) : ℕ →₀ K) ≠ 0 := by
    simp [Finsupp.single_eq_zero]
  have hne : (K ∙ (Finsupp.single 0 (1 : K) : ℕ →₀ K)) ≠ ⊥ := by
    intro h
    exact hx (Submodule.span_singleton_eq_bot.mp h)
  refine ⟨infiniteDimLocalGapPackage K _ _ hne le_rfl inferInstance,
          semifinite_trace_atom K _ hx,
          semifinite_trace_top_infinite K (not_finiteDimensional_finsupp K)⟩

end

end TGLExt
