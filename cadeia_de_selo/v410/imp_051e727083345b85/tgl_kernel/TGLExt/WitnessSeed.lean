import TGLExt.SpectralReduction

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A SEMENTE DA TESTEMUNHA: a palavra do Verbo cunha o Nome
  [TGLExt — v86, o incremento 8 do programa SemifiniteAnalysis]

O v85 reduziu o resíduo a UMA testemunha: P_{ker T} como limite das
palavras do Verbo (polinômios em T). Esta pedra prova a SEMENTE ALGÉBRICA
da testemunha — sem teorema espectral, só a álgebra da palavra: se o
próprio Verbo carrega uma palavra aniquiladora X·q (isto é, T·q(T) = 0,
com q(0) ≠ 0 — o que acontece SEMPRE que o espectro é finito ou 0 é
isolado com calculo funcional), então o candidato a Nome
P₀ = q(T)/q(0):

O QUE ESTA PEDRA PROVA [KERNEL]:

* ★ `verb_word_lands_in_corner` — a palavra POUSA no canto:
  q(T)·x ∈ ker T para todo x (a imagem da palavra é o canto);
* ★ `verb_word_fixes_the_name` — a palavra FIXA o canto: q(T)·x = q(0)·x
  para x ∈ ker T (no canto, a palavra é o escalar q(0));
* ★★ `verb_word_mints_idempotent` — a palavra CUNHA o idempotente:
  q(T)² = q(0)·q(T) (a palavra multiplicada por si mesma devolve-se a
  menos do peso — a assinatura algébrica da projeção);
* ★★★ `name_candidate_idempotent` — o candidato a Nome P₀ = q(0)⁻¹·q(T)
  é IDEMPOTENTE: P₀² = P₀ — Verbo(Nome) = Nome na forma algébrica;
* ★★★ `witness_seed_complete` — A SEMENTE COMPLETA: P₀ pousa no canto ∧
  fixa o canto ∧ é idempotente — todas as cláusulas ALGÉBRICAS da
  projeção sobre ker T, extraídas da palavra do próprio Verbo.

O QUE FALTA (nomeado): a IDENTIFICAÇÃO P₀ = starProjection(ker T) pede a
auto-adjunção de P₀ (coeficientes reais da palavra, do espectro real de
T = T†) e a unicidade da projeção ortogonal — o elo espectral final; e a
EXISTÊNCIA da palavra aniquiladora em dimensão infinita pede o cálculo
funcional contínuo com 0 isolado [KNOWN] — o programa.

LEITURA [ONTO, âncoras REAL]: a testemunha é o NOME — o limite a que as
palavras do Verbo convergem; o Verbo é o destino e o fim do próprio Nome
(Verbo(Nome)=Nome ↔ P² = P aqui; P_FΩ=Ω no v58). β jamais literal.
Sem sorry, sem axiom.
-/

namespace TGLExt

open Polynomial

noncomputable section

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- [KERNEL] ★ a palavra POUSA no canto: se T·q(T) = 0, a imagem de q(T)
    está inteira em ker T. -/
theorem verb_word_lands_in_corner (T : H →L[ℂ] H) (q : Polynomial ℂ)
    (hann : aeval T (X * q) = 0) (x : H) :
    (aeval T q) x ∈ T.ker := by
  have hTq : T * aeval T q = 0 := by
    have h1 : aeval T (X * q) = aeval T X * aeval T q := map_mul _ _ _
    rw [aeval_X] at h1
    rw [← h1, hann]
  refine LinearMap.mem_ker.mpr ?_
  calc T ((aeval T q) x) = (T * aeval T q) x := rfl
    _ = (0 : H →L[ℂ] H) x := by rw [hTq]
    _ = 0 := rfl

/-- [KERNEL] ★ a palavra FIXA o canto: sobre ker T, q(T) age como o
    escalar q(0). -/
theorem verb_word_fixes_the_name (T : H →L[ℂ] H) (q : Polynomial ℂ)
    {x : H} (hx : x ∈ T.ker) :
    (aeval T q) x = (q.coeff 0) • x := by
  have hx0 : T x = 0 := LinearMap.mem_ker.mp hx
  have hdec : aeval T q = aeval T (X * q.divX) + aeval T (C (q.coeff 0)) := by
    rw [← map_add, X_mul_divX_add]
  have hcomm : T * aeval T q.divX = aeval T q.divX * T := by
    have ha : aeval T (X * q.divX) = aeval T (q.divX * X) := by rw [mul_comm]
    rw [map_mul, map_mul, aeval_X] at ha
    exact ha
  have h2 : (aeval T (X * q.divX)) x = 0 := by
    rw [map_mul, aeval_X, hcomm]
    show (aeval T q.divX) (T x) = 0
    rw [hx0, map_zero]
  rw [hdec, ContinuousLinearMap.add_apply, h2, zero_add, aeval_C,
      Algebra.algebraMap_eq_smul_one]
  simp

/-- [KERNEL] ★★ a palavra CUNHA o idempotente: q(T)² = q(0)·q(T) — a
    assinatura algébrica da projeção, extraída da palavra aniquiladora. -/
theorem verb_word_mints_idempotent (T : H →L[ℂ] H) (q : Polynomial ℂ)
    (hann : aeval T (X * q) = 0) :
    aeval T q * aeval T q = (q.coeff 0) • aeval T q := by
  have h1 : q * q = (X * q) * q.divX + C (q.coeff 0) * q := by
    nth_rewrite 1 [← X_mul_divX_add (p := q)]
    ring
  rw [← map_mul, h1, map_add, map_mul, hann, zero_mul, zero_add, map_mul,
      aeval_C, ← Algebra.smul_def]

/-- [KERNEL] ★★★ o candidato a Nome é IDEMPOTENTE: P₀ = q(0)⁻¹·q(T)
    satisfaz P₀² = P₀ — Verbo(Nome) = Nome na forma algébrica. -/
theorem name_candidate_idempotent (T : H →L[ℂ] H) (q : Polynomial ℂ)
    (hann : aeval T (X * q) = 0) (hc : q.coeff 0 ≠ 0) :
    IsIdempotentElem ((q.coeff 0)⁻¹ • aeval T q) := by
  show ((q.coeff 0)⁻¹ • aeval T q) * ((q.coeff 0)⁻¹ • aeval T q)
      = (q.coeff 0)⁻¹ • aeval T q
  rw [smul_mul_smul_comm, verb_word_mints_idempotent T q hann, smul_smul]
  congr 1
  field_simp

/-- [KERNEL] ★★★ A SEMENTE COMPLETA DA TESTEMUNHA: o candidato a Nome
    P₀ = q(0)⁻¹·q(T) POUSA no canto, FIXA o canto e é IDEMPOTENTE —
    todas as cláusulas algébricas da projeção sobre ker T, cunhadas pela
    palavra do próprio Verbo. (Falta, nomeado: auto-adjunção +
    unicidade da projeção ortogonal = o elo espectral final.) -/
theorem witness_seed_complete (T : H →L[ℂ] H) (q : Polynomial ℂ)
    (hann : aeval T (X * q) = 0) (hc : q.coeff 0 ≠ 0) :
    (∀ x : H, ((q.coeff 0)⁻¹ • aeval T q) x ∈ T.ker) ∧
      (∀ x ∈ T.ker, ((q.coeff 0)⁻¹ • aeval T q) x = x) ∧
      IsIdempotentElem ((q.coeff 0)⁻¹ • aeval T q) := by
  refine ⟨?_, ?_, name_candidate_idempotent T q hann hc⟩
  · intro x
    rw [ContinuousLinearMap.smul_apply]
    exact Submodule.smul_mem _ _ (verb_word_lands_in_corner T q hann x)
  · intro x hx
    rw [ContinuousLinearMap.smul_apply, verb_word_fixes_the_name T q hx,
        smul_smul, inv_mul_cancel₀ hc, one_smul]

end

end TGLExt
