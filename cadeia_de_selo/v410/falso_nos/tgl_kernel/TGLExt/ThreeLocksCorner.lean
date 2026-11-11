import TGLExt.DimensionTrace
import TGL.FiniteThreeLocks

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O CANTO DOS THREE LOCKS PELA PONTE DA DIMENSÃO
  [TGLExt — v79, o Certificado II elevado a teorema de kernel]

O v77 fez o teorema abstrato de Breuer (v64) disparar sobre um operador
concreto genérico (H₀ − V sobre ℝⁿ). Esta pedra o dispara sobre O OPERADOR
DA TEORIA: `H3L = Dc*Dc + Db*Db + Dz*Dz` — os Three Locks da Ponte
Einstein–Cartan–Miguel, a face finita da hipótese H1
(TGL_INTERNAL_SUSY_RELATIVE_GAP), o mesmo operador que o Certificado II
instancia numericamente no runtime do um.py (gap 0,0481, zero isolado,
Nome = 1).

O QUE ESTA PEDRA PROVA [KERNEL]:

* `dimTraceDataOver` — a ponte da dimensão GENERALIZADA: τ = dim é camada
  tracial semifinita FIEL e MONÓTONA sobre o reticulado de subespaços de
  QUALQUER espaço de dimensão finita sobre QUALQUER corpo (v77 era ℝⁿ;
  agora ℂ entra — o corpo dos Three Locks);
* ★ `dimension_trace_over_top_finite` — τ(⊤) < ∞ em qualquer corpo
  (a semifinitude é a finitude, agora sem privilégio de ℝ);
* ★ `threeLocks_ker_ne_bot_of_witness` — a PORTA: um habitante não nulo
  das três fechaduras (Dc x = Db x = Dz x = 0, x ≠ 0) força ker H3L ≠ ⊥;
* ★★ `three_locks_corner_weight` — O CERTIFICADO II EM KERNEL: o pacote
  (ker H3L, gap = ⊤) instancia BreuerGapData na camada da dimensão sobre ℂ
  e o teorema ABSTRATO `breuer_kernel_weight` (v64) conclui
  0 < τ(ker H3L) < ∞ para o operador dos Three Locks;
* ★ `three_locks_corner_weight_eq_dim` — o peso abstrato É o observável
  do runtime: τ(ker H3L) = dim(canto) = Tr(P_F) (por definição — `rfl`);
* ★ `three_locks_name_is_one` — o NOME normalizado do canto é 1
  (τ_F(P_F) = 1, v58×v64×v79): ker ≠ ⊥ ⟹ dim > 0 ⟹ dim/dim = 1;
* ★ `corner_le_each_lock` / `three_locks_corner_dim_le` — o canto vive
  SOB cada fechadura e seu peso é limitado pela dimensão da inscrição
  (dim ker H3L ≤ n);
* ★★ `three_locks_corner_full_profile` — O PERFIL COMPLETO (v58×v64×v77×v79
  numa só implicação): de UMA testemunha explícita nas três fechaduras
  seguem peso POSITIVO ∧ FINITO ∧ Nome = 1 — as cláusulas de H1 na face
  finita, agora TEOREMA, não medida.

HONESTIDADE: dimensão finita — NÃO é prova de fator III₁; a EXISTÊNCIA da
testemunha (x ≠ 0 nas três fechaduras) é hipótese aqui e é exatamente o que
a rede concreta do Certificado II exibe numericamente no runtime — o kernel
prova tudo A JUSANTE dela. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal
open TGL.FiniteThreeLocks

noncomputable section

/- ═══════════ 1. A ponte da dimensão generalizada (qualquer corpo) ═══════════ -/

/-- [DATA — v77 generalizado] τ = dim no reticulado de subespaços de um
    espaço de dimensão finita sobre um corpo qualquer: FIEL e MONÓTONO.
    O ℝⁿ do v77 dá lugar ao corpo dos Three Locks (ℂ). -/
def dimTraceDataOver (K V : Type) [Field K] [AddCommGroup V] [Module K V]
    [FiniteDimensional K V] : SemifiniteTraceData (Submodule K V) where
  tau := fun S => (Module.finrank K S : ℝ≥0∞)
  mono := by
    intro p q hpq
    exact_mod_cast Submodule.finrank_mono hpq
  faithful := by
    intro p hp
    have h0 : Module.finrank K p = 0 := by exact_mod_cast hp
    exact (Submodule.finrank_eq_zero (R := K)).mp h0

variable (K V : Type) [Field K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]

/-- [KERNEL] ★ τ(⊤) < ∞ sobre QUALQUER corpo — a semifinitude é a
    finitude, sem privilégio de ℝ. -/
theorem dimension_trace_over_top_finite :
    (dimTraceDataOver K V).tau ⊤ < ⊤ := by
  simp only [dimTraceDataOver]
  exact ENNReal.natCast_lt_top _

/- ═══════════ 2. O canto dos Three Locks entra na camada ═══════════ -/

variable {n : ℕ}
variable (Dc Db Dz : EuclideanSpace ℂ (Fin n) →ₗ[ℂ] EuclideanSpace ℂ (Fin n))

/-- [DATA] a camada da dimensão sobre o espaço dos Three Locks. -/
def threeLocksDimTrace (n : ℕ) :
    SemifiniteTraceData (Submodule ℂ (EuclideanSpace ℂ (Fin n))) :=
  dimTraceDataOver ℂ (EuclideanSpace ℂ (Fin n))

/-- [KERNEL] ★ a PORTA: um habitante não nulo das três fechaduras força
    o canto a ser não-trivial — `ker H3L ≠ ⊥`. É exatamente esta hipótese
    que a rede concreta do Certificado II exibe no runtime. -/
theorem threeLocks_ker_ne_bot_of_witness
    (x : EuclideanSpace ℂ (Fin n)) (hx : x ≠ 0)
    (hc : Dc x = 0) (hb : Db x = 0) (hz : Dz x = 0) :
    LinearMap.ker (H3L Dc Db Dz) ≠ ⊥ := by
  intro h
  have hmem : x ∈ LinearMap.ker (H3L Dc Db Dz) :=
    (mem_ker_H3L_iff Dc Db Dz x).mpr ⟨hc, hb, hz⟩
  rw [h, Submodule.mem_bot] at hmem
  exact hx hmem

/-- [DATA] o pacote de gap dos THREE LOCKS: ker = ker H3L no reticulado
    da dimensão sobre ℂ, gap = ⊤ (finito em dimensão finita). -/
def threeLocksCornerPackage
    (hker : LinearMap.ker (H3L Dc Db Dz) ≠ ⊥) :
    BreuerGapData (Submodule ℂ (EuclideanSpace ℂ (Fin n)))
      (threeLocksDimTrace n) where
  ker := LinearMap.ker (H3L Dc Db Dz)
  gap := ⊤
  ker_le_gap := le_top
  gap_finite := dimension_trace_over_top_finite ℂ (EuclideanSpace ℂ (Fin n))
  ker_ne_bot := hker

/- ═══════════ 3. Os teoremas do canto ═══════════ -/

/-- [KERNEL] ★★ O CERTIFICADO II EM KERNEL: o teorema ABSTRATO de Breuer
    (v64) dispara sobre o operador DA TEORIA — para o canto dos Three
    Locks, 0 < τ(ker H3L) < ∞. A face finita de H1 deixa de ser só medida
    de runtime e vira teorema. -/
theorem three_locks_corner_weight
    (hker : LinearMap.ker (H3L Dc Db Dz) ≠ ⊥) :
    0 < (threeLocksDimTrace n).tau (LinearMap.ker (H3L Dc Db Dz)) ∧
      (threeLocksDimTrace n).tau (LinearMap.ker (H3L Dc Db Dz)) < ⊤ :=
  breuer_kernel_weight (threeLocksCornerPackage Dc Db Dz hker)

/-- [KERNEL] ★ o peso abstrato É o observável do runtime: τ(ker H3L)
    coincide por DEFINIÇÃO com a dimensão do canto — o Tr(P_F) que o
    Certificado II mede (tr(P_F) = 4 na rede concreta). -/
theorem three_locks_corner_weight_eq_dim :
    (threeLocksDimTrace n).tau (LinearMap.ker (H3L Dc Db Dz))
      = (cornerDim Dc Db Dz : ℝ≥0∞) := rfl

/-- [KERNEL] ★ o NOME do canto é 1 (τ_F(P_F) = 1): do canto não-trivial
    segue dim > 0 e o traço normalizado é exatamente 1 — a normalização
    do Nome (v58) agora deduzida da não-trivialidade, não assumida. -/
theorem three_locks_name_is_one
    (hker : LinearMap.ker (H3L Dc Db Dz) ≠ ⊥) :
    (cornerDim Dc Db Dz : ℝ) / (cornerDim Dc Db Dz : ℝ) = 1 := by
  have hpos : 0 < cornerDim Dc Db Dz := by
    rcases Nat.eq_zero_or_pos (cornerDim Dc Db Dz) with h0 | h
    · exact absurd ((Submodule.finrank_eq_zero (R := ℂ)).mp h0) hker
    · exact h
  exact normalizedCornerTrace_PF Dc Db Dz hpos

/-- [KERNEL] ★ o canto vive SOB cada fechadura: ker H3L ≤ ker Dc
    (e por simetria da interseção, sob as outras duas). -/
theorem corner_le_each_lock :
    LinearMap.ker (H3L Dc Db Dz) ≤ LinearMap.ker Dc := by
  rw [ker_H3L_eq_threeLocks]
  exact le_trans inf_le_left inf_le_left

/-- [KERNEL] ★ o peso do canto é limitado pela dimensão da inscrição:
    dim(ker H3L) ≤ n — o eco do "≤ posto" (v65) na face dos Three Locks. -/
theorem three_locks_corner_dim_le :
    cornerDim Dc Db Dz ≤ n := by
  have h := Submodule.finrank_le (LinearMap.ker (H3L Dc Db Dz))
  rwa [finrank_euclideanSpace_fin] at h

/-- [KERNEL] ★★ O PERFIL COMPLETO DO CANTO DOS THREE LOCKS
    (v58 × v64 × v77 × v79 numa só implicação): de UMA testemunha
    explícita nas três fechaduras seguem peso POSITIVO ∧ FINITO ∧
    Nome = 1 ∧ dim ≤ n — as cláusulas de H1 na face finita como TEOREMA.
    A rede concreta do Certificado II fornece a testemunha; o kernel
    prova tudo a jusante. -/
theorem three_locks_corner_full_profile
    (x : EuclideanSpace ℂ (Fin n)) (hx : x ≠ 0)
    (hc : Dc x = 0) (hb : Db x = 0) (hz : Dz x = 0) :
    ((0 < (threeLocksDimTrace n).tau (LinearMap.ker (H3L Dc Db Dz)) ∧
      (threeLocksDimTrace n).tau (LinearMap.ker (H3L Dc Db Dz)) < ⊤) ∧
      (cornerDim Dc Db Dz : ℝ) / (cornerDim Dc Db Dz : ℝ) = 1) ∧
      cornerDim Dc Db Dz ≤ n := by
  have hker := threeLocks_ker_ne_bot_of_witness Dc Db Dz x hx hc hb hz
  exact ⟨⟨three_locks_corner_weight Dc Db Dz hker,
          three_locks_name_is_one Dc Db Dz hker⟩,
         three_locks_corner_dim_le Dc Db Dz⟩

end

end TGLExt
