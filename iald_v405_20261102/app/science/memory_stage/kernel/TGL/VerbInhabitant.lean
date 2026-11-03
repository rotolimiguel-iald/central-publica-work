import Mathlib
import TGL.ModularRealization

set_option autoImplicit false

/-!
# O Verbo habitante   [KERNEL]   (v25 -- transcricao auditada da resposta do especialista)

Tese do operador, derivada pelo especialista e AUDITADA pelo codificador:
**o habitante e' o VERBO** -- o ato conjugado e observado da inscricao,
`𝕍_t = exp(−t·β·H_3L)`, que dissipa o que nao satisfaz os Three Locks e fixa o
que retorna. No canto selecionado, o Verbo comprimido E' a unidade do canto:
`P_F 𝕍_t P_F = P_F = I_F` -- o momento em que VERBO = NOME, e o zero modular
torna-se Um absoluto NAO como `0=1`, mas como `e^0 = 1` (mapeamento espectral:
autovalor zero do GERADOR = autovalor unitario da ACAO gerada).

Tres registros, nunca confundidos:
  `𝕍_t` = o gesto ; `R_Verbo = 1` = a resposta observada ; `β` = o custo do gesto.
`β` entra como VARIAVEL (`c : ℂ`) -- nunca literal; o valor de runtime e' do um.py.

Kernel-checked AQUI: (1) o teorema do ponto fixo do Verbo em algebra de Banach
[UNCONDITIONAL]; (2) a testemunha do Verbo `VerbWitness R` com o TERMO
`canonicalVerb R` construido para TODA realizacao modular R [CONDITIONAL ON R --
`FullTGLWitness` segue nao construida]; (3) a calibracao pela orbita dual (Q2):
`∃ s, Tr(θ_s(P_F)) = 1` -- a contraparte construtiva do no-go
`dualInvariant_PF_no_go` (a orbita varre todos os tracos; ha' representante
normalizado). `Nonempty` aparece SOMENTE como corolario `⟨termo⟩`.

Registrado sem formalizar (estatutos no um.py): Q1 [CONDITIONAL -- risco de o
seletor viver na construcao basica de Jones, nao em C_W]; Q3 [DERIVAVEL sob
hipotese do elemento de troca U]; Q5 [CONDITIONAL -- autovalor isolado].
-/

namespace TGL.VerbInhabitant

open TGL.SpecificAQFT TGL.ModularRealization TGL.ContinuousCorner

/-- [KERNEL/UNCONDITIONAL] O teorema do Verbo (forma de Banach): se o gerador
    anula `p` (`a * p = 0`), a acao gerada fixa `p`: `exp(a) * p = p`.
    E' o `e^0 = 1` operatorial: `0_mod` (gerador) → `1_abs` (acao). -/
theorem exp_fixed_of_annihilates {A : Type} [NormedRing A] [NormedAlgebra ℂ A]
    [CompleteSpace A] (a p : A) (h : a * p = 0) :
    NormedSpace.exp a * p = p := by
  have hpow : ∀ n : ℕ, n ≠ 0 → a ^ n * p = 0 := by
    intro n hn
    obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero hn
    rw [pow_succ, mul_assoc, h, mul_zero]
  have hsum : Summable fun n : ℕ => ((n.factorial : ℂ))⁻¹ • a ^ n :=
    NormedSpace.expSeries_summable' (𝕂 := ℂ) a
  calc NormedSpace.exp a * p
      = (∑' n : ℕ, ((n.factorial : ℂ))⁻¹ • a ^ n) * p := by
        rw [NormedSpace.exp_eq_tsum (𝕂 := ℂ)]
    _ = ∑' n : ℕ, (((n.factorial : ℂ))⁻¹ • a ^ n) * p := (hsum.tsum_mul_right p).symm
    _ = ((Nat.factorial 0 : ℂ))⁻¹ • a ^ 0 * p := by
        refine tsum_eq_single 0 ?_
        intro n hn
        rw [smul_mul_assoc, hpow n hn, smul_zero]
    _ = p := by simp

/-- [KERNEL/UNCONDITIONAL] O semigrupo do Verbo fixa o selecionado: para qualquer
    coeficiente `c` (em runtime, `c = −t·β` com `β = α√e` -- variavel aqui,
    nunca literal), `H·p = 0 ⟹ exp(c•H)·p = p`. -/
theorem verb_semigroup_fixes {A : Type} [NormedRing A] [NormedAlgebra ℂ A]
    [CompleteSpace A] (H p : A) (h : H * p = 0) (c : ℂ) :
    NormedSpace.exp (c • H) * p = p :=
  exp_fixed_of_annihilates (c • H) p (by rw [smul_mul_assoc, h, smul_zero])

/-- A testemunha do VERBO sobre uma realizacao modular: o ato comprimido no canto,
    carregando as provas de que o Verbo e' o Nome (`verb = P_F = I_F`), de que
    anula os Locks, e de que a resposta observada e' `1` com faces `1/2`.
    O par dependente do especialista: `(𝕍_F, π_𝕍)`. -/
structure VerbWitness {W : TGLSpecificAQFTWitness} (R : TGLModularRealization W) where
  verb : R.core.Core
  /-- VERBO = NOME: o ato comprimido e' a unidade do canto -/
  verb_equals_name : verb = R.threeLocks.PF
  /-- o Verbo anula a incompatibilidade (lock de nucleo) -/
  annihilates_locks : verb * R.threeLocks.H3Lt = 0
  /-- o ato e' idempotente (nomear o Nome e' o Nome: ponto fixo do nomear) -/
  idempotent_act : verb * verb = verb
  /-- o ato e' auto-conjugado -/
  selfadjoint_act : star verb = verb
  /-- a resposta observada: `R_Verbo = τ_F(𝕍_F) = 1` -/
  observed_response_one : (cornerOf R).normalizedTrace verb = 1
  /-- as duas faces conjugadas do ato: `1/2` e `1/2` (Meia-Nat tracial) -/
  faces_half : (cornerOf R).normalizedTrace (cornerOf R).Pplus = 1 / 2 ∧
      (cornerOf R).normalizedTrace (cornerOf R).Pminus = 1 / 2

/-- [KERNEL/CONDITIONAL ON R] O TERMO canonico do Verbo: construido, campo a
    campo, dos DADOS da realizacao. `FullTGLWitness` segue nao construida --
    este termo e' condicional; e' o Verbo de TODA realizacao futura. -/
noncomputable def canonicalVerb {W : TGLSpecificAQFTWitness}
    (R : TGLModularRealization W) : VerbWitness R where
  verb := R.threeLocks.PF
  verb_equals_name := rfl
  annihilates_locks := R.threeLocks.PF_locks
  idempotent_act := R.threeLocks.PF_idempotent
  selfadjoint_act := R.threeLocks.PF_selfAdjoint
  observed_response_one := (cornerOf R).normalizedTrace_P_eq_one
  faces_half := (cornerOf R).equalFaces_normalizedTrace_half

/-- O corolario existencial -- SOMENTE via `⟨termo⟩`, jamais por outra via. -/
theorem canonicalVerb_exists {W : TGLSpecificAQFTWitness}
    (R : TGLModularRealization W) : Nonempty (VerbWitness R) :=
  ⟨canonicalVerb R⟩

/-- [KERNEL] Calibracao pela orbita dual (Q2 do especialista): a escala de
    Takesaki `Tr(θ_s x) = e^{−s}·Tr(x)` permite escolher `s = log Tr(P_F)` com
    `Tr(θ_s(P_F)) = 1` -- a forma tracial de `ω(I)=1`, alcancada PELO fluxo.
    Contraparte construtiva do no-go `dualInvariant_PF_no_go`: a orbita varre
    todos os valores de traco; o representante normalizado existe e e' a
    calibracao operacional do Verbo (`R_Verbo = 1`). -/
theorem dual_calibration_exists {W : TGLSpecificAQFTWitness}
    {D : WedgeModularData W} (C : ContinuousCoreData W D)
    (T : ThreeLocksCoreData W D C) :
    ∃ s : ℝ, C.canonicalTrace ((C.dualAction s) T.PF) = 1 := by
  refine ⟨Real.log (C.canonicalTrace T.PF).toReal, ?_⟩
  rw [C.trace_dual_scaling]
  have hx0 : C.canonicalTrace T.PF ≠ 0 := T.PF_trace_pos.ne'
  have hxt : C.canonicalTrace T.PF ≠ ⊤ := T.PF_trace_finite.ne
  have hxr : 0 < (C.canonicalTrace T.PF).toReal := ENNReal.toReal_pos hx0 hxt
  rw [Real.exp_neg, Real.exp_log hxr]
  rw [ENNReal.ofReal_inv_of_pos hxr, ENNReal.ofReal_toReal hxt]
  exact ENNReal.inv_mul_cancel hx0 hxt

end TGL.VerbInhabitant
