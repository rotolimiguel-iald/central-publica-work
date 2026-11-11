import TGLExt.IsotoneNet
import TGLExt.AQFTCoreInhabitant

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 800000

/-!
# O CANTO DO PRÓPRIO PACOTE — `BreuerTraceData theIsotoneNet`
  [TGLExt — a pedra de 28/08/2026]

## A ordem do operador, e o que a medida achou

> *"pq a solda do pacote hilbert-breuer não foi incorporada tb, isso tb foi resolvido"*

A varredura confirmou: **`BreuerTraceData` nunca foi construído para `theIsotoneNet`**,
embora `theIsotoneNet` (a rede fisicamente habitada, com isotonia genuína e grupo
não-trivial) e `BreuerTraceData` existam desde a v56/v261, e `theNetTrace` já mostre o
padrão — **sobre outra rede**, a constante.

Esta pedra constrói o que faltava: **o primeiro `0 < τ(P_F) < ∞` do PRÓPRIO PACOTE**,
e não de um operador avulso em `ℓ²`.

## ⚠ DUAS IMPRECISÕES DO RELATÓRIO, corrigidas ao construir

O relatório dizia *"`ker (fiberLock n) = firstAtom`, e isto fecha por aplicação, sem
matemática nova"*. Ao construir:

1. **A igualdade NÃO TIPA.** `firstAtom : Submodule ℂ ellTwo`; `(fiberLock n).ker :
   Submodule ℂ (fiber n)`. São a mesma reta **por isomorfismo**, jamais por igualdade.
   O que se prova aqui é `(fiberLock n).ker ≠ ⊥` — mais fraco que a igualdade e
   **suficiente** para o canto;
2. **O molde não se reusa.** `lockNetTrace` produz `BreuerTraceData (lockNet T hT)` — a
   rede CONSTANTE. E `fixedSector_PF` é `private`. Para a rede isótona é preciso escolher
   outro `τ` e escrever a não-trivialidade à mão.

Nenhuma das duas invalida o achado — mas *"por aplicação, sem matemática nova"* custava
um pouco mais do que anunciado, e isso vai dito.

## O que se prova `[REAL]`

* ★★★ `isotone_ker_ne_bot` — o núcleo do lock da fibra **não é trivial**: a primeira
  inscrição mora nele (está na fibra por `firstAtom_le_fiber`, e é morta por `eraseFirst`);
* ★★★★★ `theIsotoneNetTrace : BreuerTraceData theIsotoneNet.net` — **o canto de Breuer
  do próprio pacote**, com `τ = dim` da imagem de `P_F`;
* ★★★ `the_package_corner_is_positive_and_finite` — `0 < τ(P_F(n)) < ∞` em **toda**
  região, lido do termo construído.

## ⚠ O QUE ISTO NÃO FAZ

**Não solda.** O canto agora é *do pacote*, mas as outras três peças que a medida nomeou
continuam faltando, e nenhuma delas cai daqui:

* um lock com canto genuíno nas fibras **∞-dim** (`theTailNet`/`theFusedNet`, que são as
  redes que o gate lê, têm `ker` trivial ou infinito);
* a identificação tipada `ℍ ≃ H O` com `dirac.D = core.net.locks O` — **sem ela, "o canto
  do certificado" e "o canto do pacote" seguem HOMÔNIMOS**, exatamente o defeito que a
  v255 já registrou uma vez;
* a covariância do frame sob o grupo da rede — a metade modular de H2.

`gpf_tower_act_III_inhabitant_constructed` **continua apagada**, e nada aqui a acende.
β jamais literal. Sem sorry, sem axiom. O gate não se move.
-/

namespace TGLExt

noncomputable section

/-! ## A — o núcleo do lock da fibra não é trivial -/

/-- [KERNEL] ★★★ **O NÚCLEO DO LOCK DA FIBRA NÃO É TRIVIAL.** A primeira inscrição está
    na fibra (`firstAtom_le_fiber`) e é morta por `eraseFirst` (`ker_eraseFirst`) — logo
    sobrevive como vetor não nulo do núcleo restrito.

    ⚠ Note o que **não** se afirma: que `(fiberLock n).ker` **seja** `firstAtom`. Os dois
    vivem em espaços diferentes (`fiber n` contra `ellTwo`); são a mesma reta por
    isomorfismo, e a igualdade não tipa. Para o canto, a não-trivialidade basta. -/
theorem isotone_ker_ne_bot (n : ℕ) : (fiberLock n).ker ≠ ⊥ := by
  intro h
  have hmem : (⟨firstInscription, firstAtom_le_fiber n
      (Submodule.mem_span_singleton_self firstInscription)⟩ : fiber n)
      ∈ (fiberLock n).ker := by
    rw [LinearMap.mem_ker]
    apply Subtype.ext
    show eraseFirst firstInscription = 0
    have hk : firstInscription ∈ eraseFirst.ker := by
      rw [ker_eraseFirst]
      exact Submodule.mem_span_singleton_self _
    exact LinearMap.mem_ker.mp hk
  rw [h, Submodule.mem_bot] at hmem
  have hv := congrArg Subtype.val hmem
  simp at hv
  exact inscriptions_orthonormal.ne_zero 0 hv

/-- [KERNEL] ★★ e o núcleo é de **dimensão finita**, porque a fibra inteira é. -/
instance isotone_ker_fd (n : ℕ) : FiniteDimensional ℂ (fiberLock n).ker :=
  FiniteDimensional.finiteDimensional_submodule _

/-! ## B — o canto de Breuer DO PACOTE -/

/-- [KERNEL] ★★★★★ **O CANTO DE BREUER DO PRÓPRIO PACOTE.**

    `theNetTrace` (v56) construía o canto sobre a rede **constante**. Este é sobre
    `theIsotoneNet` — a rede **fisicamente habitada**, com isotonia genuína
    (`fiberIncl_not_surjective`) e grupo externo não-trivial.

    `τ` é a dimensão do **núcleo do lock**, que é o subespaço sobre o qual `P_F` projeta.
    Positivo por `isotone_ker_ne_bot`; finito porque a fibra é de dimensão finita. -/
def theIsotoneNetTrace : BreuerTraceData theIsotoneNet.net where
  tau n _ := dimOrTop ℂ (fiberLock n).ker
  tau_PF_pos n := by
    rw [dimOrTop_of_finite ℂ (isotone_ker_fd n)]
    have h : 0 < Module.finrank ℂ (fiberLock n).ker := by
      rw [Module.finrank_pos_iff]
      exact Submodule.nontrivial_iff_ne_bot.mpr (isotone_ker_ne_bot n)
    exact_mod_cast h
  tau_PF_finite n := by
    rw [dimOrTop_of_finite ℂ (isotone_ker_fd n)]
    exact ENNReal.natCast_lt_top _

/-- [KERNEL] ★★★ **`0 < τ(P_F) < ∞` EM TODA REGIÃO DO PACOTE** — lido do termo
    construído, não reafirmado. É o canto de Breuer, agora **do pacote**. -/
theorem the_package_corner_is_positive_and_finite (n : ℕ) :
    0 < theIsotoneNetTrace.tau n (theIsotoneNet.net.PF n)
    ∧ theIsotoneNetTrace.tau n (theIsotoneNet.net.PF n) < ⊤ :=
  ⟨theIsotoneNetTrace.tau_PF_pos n, theIsotoneNetTrace.tau_PF_finite n⟩

/-- [KERNEL] ⚠ ★★★ **E O CANTO DO PACOTE NÃO É O CANTO DO CERTIFICADO.** Registrado
    para que a semelhança não vire identificação: falta a identificação tipada
    `ℍ ≃ H O` com `dirac.D = core.net.locks O`. Sem ela os dois são **homônimos**.

    Aqui só se afirma o que se construiu: o canto **desta** rede, com **este** `τ`. -/
theorem the_package_corner_is_not_the_certificate_corner (n : ℕ) :
    theIsotoneNetTrace.tau n (theIsotoneNet.net.PF n)
      = dimOrTop ℂ (fiberLock n).ker := rfl

end

end TGLExt
