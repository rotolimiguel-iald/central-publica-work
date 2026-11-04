import TGLExt.SemifiniteLattice

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O RETICULADO FECHADO: a face de Hilbert da camada semifinita
  [TGLExt — v82, o incremento 4 do programa SemifiniteAnalysis]

O v80 provou a camada genuinamente semifinita no reticulado ALGÉBRICO
(todos os subespaços). Mas o reticulado de projeções de B(H) — o objeto
real da análise de Breuer — é o reticulado dos subespaços FECHADOS de um
Hilbert completo, com ortocomplemento. Esta pedra dá esse passo:

O QUE ESTA PEDRA PROVA [KERNEL]:

* ★ `atom_is_closed` — o átomo (a linha do Um, K·x) é FECHADO num espaço
  normado completo: o peso 1 vive no reticulado de projeções;
* ★★ `closed_lattice_semifinite` — o AXIOMA da semifinitude DENTRO do
  reticulado fechado: todo subespaço não-trivial contém um subespaço
  FECHADO de peso exatamente 1 (o Nome habita o reticulado de projeções);
* ★ `closed_double_orthocomplement` — Sᗮᗮ = S para S fechado (a involução
  do reticulado de projeções — a estrutura quântica genuína);
* ★ `orthocomplement_meet_bot` / ★ `closed_orthocomplement_isCompl` —
  S ⊓ Sᗮ = ⊥ e IsCompl S Sᗮ para S fechado: cada projeção divide o
  Hilbert em face e contra-face (a auto-conjugação da fronteira, 𝒞²=1,
  agora como estrutura de reticulado);
* ★★ `inscription_complement_infinite` — em H ∞-dim, o complemento de
  toda inscrição finita pesa ⊤: O INFINITO MORA NO COMPLEMENTO DA
  INSCRIÇÃO (τ(S) < ∞ fechado ⟹ τ(Sᗮ) = ⊤);
* ★ `atom_complement_infinite` — em particular o Nome: τ(K·x) = 1 e
  τ((K·x)ᗮ) = ⊤ — o Um pesa um, e o resto é o infinito conjugado;
* ★★ `closed_local_breuer_corner` — A FORMA DO CANTO DE BREUER NO
  RETICULADO DE PROJEÇÕES: kernel ≠ ⊥ sob gap de dimensão finita ⟹
  0 < τ(ker) < ∞ ∧ ker FECHADO ∧ τ(kerᗮ) = ⊤ — a inscrição é um projetor
  fechado FINITO dentro de um complemento INFINITO (exatamente o perfil
  da projeção finita numa álgebra infinita).

HONESTIDADE: o reticulado de projeções aqui é o de B(H) inteiro; o canto
de Breuer GENUÍNO pede a subálgebra de von Neumann (comutantes,
normalidade do τ, projeções DA álgebra) — o próximo tijolo; nada aqui é
III₁; nenhuma flag do fecho se move. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal

noncomputable section

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- [KERNEL] ★ o átomo é FECHADO: a linha do Um (peso 1, v80) vive no
    reticulado de projeções — não só no algébrico. -/
theorem atom_is_closed (x : H) : IsClosed ((ℂ ∙ x) : Set H) :=
  Submodule.closed_of_finiteDimensional _

/-- [KERNEL] ★★ o AXIOMA da semifinitude DENTRO do reticulado fechado:
    todo subespaço não-trivial contém um FECHADO de peso exatamente 1 —
    o Nome habita o reticulado de projeções. -/
theorem closed_lattice_semifinite (S : Submodule ℂ H) (hS : S ≠ ⊥) :
    ∃ T : Submodule ℂ H, T ≤ S ∧ IsClosed (T : Set H) ∧ T ≠ ⊥ ∧
      (semifiniteDimTrace ℂ H).tau T = 1 := by
  obtain ⟨x, hxS, hx0⟩ := (Submodule.ne_bot_iff S).mp hS
  refine ⟨ℂ ∙ x, (Submodule.span_singleton_le_iff_mem x S).mpr hxS,
          atom_is_closed x, ?_, semifinite_trace_atom ℂ x hx0⟩
  intro h
  exact hx0 (Submodule.span_singleton_eq_bot.mp h)

/-- [KERNEL] ★ a involução do reticulado de projeções: Sᗮᗮ = S para S
    fechado — a estrutura quântica genuína (dupla contra-face = face). -/
theorem closed_double_orthocomplement (S : Submodule ℂ H)
    (hS : IsClosed (S : Set H)) : Sᗮᗮ = S := by
  haveI : CompleteSpace S := hS.completeSpace_coe
  exact Submodule.orthogonal_orthogonal S

/-- [KERNEL] ★ face e contra-face não se tocam: S ⊓ Sᗮ = ⊥. -/
theorem orthocomplement_meet_bot (S : Submodule ℂ H) : S ⊓ Sᗮ = ⊥ :=
  (Submodule.orthogonal_disjoint S).eq_bot

/-- [KERNEL] ★ cada projeção fechada divide o Hilbert em face e
    contra-face: IsCompl S Sᗮ (a auto-conjugação da fronteira como
    estrutura de reticulado). -/
theorem closed_orthocomplement_isCompl (S : Submodule ℂ H)
    (hS : IsClosed (S : Set H)) : IsCompl S Sᗮ := by
  haveI : CompleteSpace S := hS.completeSpace_coe
  exact Submodule.isCompl_orthogonal S

/-- [KERNEL] ★★ O INFINITO MORA NO COMPLEMENTO DA INSCRIÇÃO: em H ∞-dim,
    o ortocomplemento de todo subespaço fechado de dimensão FINITA pesa ⊤. -/
theorem inscription_complement_infinite (hH : ¬FiniteDimensional ℂ H)
    (S : Submodule ℂ H) (hS : IsClosed (S : Set H))
    [FiniteDimensional ℂ S] :
    (semifiniteDimTrace ℂ H).tau Sᗮ = ⊤ := by
  have hcompl := closed_orthocomplement_isCompl S hS
  by_cases hfd : FiniteDimensional ℂ Sᗮ
  · exfalso
    haveI := hfd
    exact hH (Submodule.prodEquivOfIsCompl S Sᗮ hcompl).finiteDimensional
  · show dimOrTop ℂ (Sᗮ) = ⊤
    exact dimOrTop_of_infinite ℂ hfd

/-- [KERNEL] ★ o Nome e o seu conjugado: τ(K·x) = 1 e τ((K·x)ᗮ) = ⊤ em
    H ∞-dim — o Um pesa um; o resto é o infinito conjugado. -/
theorem atom_complement_infinite (hH : ¬FiniteDimensional ℂ H)
    (x : H) (hx : x ≠ 0) :
    (semifiniteDimTrace ℂ H).tau (ℂ ∙ x) = 1 ∧
      (semifiniteDimTrace ℂ H).tau (ℂ ∙ x)ᗮ = ⊤ :=
  ⟨semifinite_trace_atom ℂ x hx,
   inscription_complement_infinite hH (ℂ ∙ x) (atom_is_closed x)⟩

/-- [KERNEL] ★★ A FORMA DO CANTO DE BREUER NO RETICULADO DE PROJEÇÕES:
    kernel não-trivial sob gap de dimensão finita ⟹ peso POSITIVO ∧
    FINITO ∧ kernel FECHADO ∧ complemento de peso ⊤ — a inscrição é um
    projetor fechado FINITO dentro de um complemento INFINITO (o perfil
    exato da projeção finita numa álgebra infinita). -/
theorem closed_local_breuer_corner (hH : ¬FiniteDimensional ℂ H)
    (kr gp : Submodule ℂ H) (hker : kr ≠ ⊥) (hle : kr ≤ gp)
    (hgp : FiniteDimensional ℂ gp) :
    ((0 < (semifiniteDimTrace ℂ H).tau kr ∧
        (semifiniteDimTrace ℂ H).tau kr < ⊤) ∧ IsClosed (kr : Set H)) ∧
      (semifiniteDimTrace ℂ H).tau krᗮ = ⊤ := by
  have hw := infinite_dim_local_breuer_weight ℂ kr gp hker hle hgp
  haveI : FiniteDimensional ℂ kr := hw.2
  have hcl : IsClosed (kr : Set H) := Submodule.closed_of_finiteDimensional _
  exact ⟨⟨hw.1, hcl⟩, inscription_complement_infinite hH kr hcl⟩

end

end TGLExt
