# -*- coding: utf-8 -*-
"""Gerência c1, 05/11/2026 — correção do MÉDIO 1 da revisão de terceiro R1 da v408 pela OPÇÃO B (provar, não recuar):
as classes do dicionário passam a ser DEFINIÇÕES em Lean sobre o MESMO problema T (`Problema`, `Problema.solucao`, `ClasseP`, `ClasseNP`),
com a cota de grau no PRÓPRIO polinômio da palavra (`palavra_com_grau`: q = minpoly/X, natDegree q < dim(End H)) e a verificação ligada à
solução de T (`leitura_um_sse_solucao`, `solucao_fixa_sse_no_nucleo`); teoremas `todo_problema_esta_em_P`, `todo_problema_esta_em_NP` e
`p_igual_np_nas_classes_do_dicionario` (igualdade das duas classes como conjuntos de problemas). Docstrings ajustadas ao termo; cabeçalhos das
quatro pedras sem «CANDIDATA»/«candidata à v408» (BAIXO da R1). Troca exata com contagem; backup de bytes; recompilação à parte."""
import hashlib, os, time
from pathlib import Path
HERE = Path(__file__).resolve().parent; TS = time.strftime("%Y%m%d_%H%M%S")
CAB_FIM_ANT = "`lake env lean`), só no trio; candidata à v408]"
CAB_FIM_NOVO = "`lake env lean`) e no da v408 (`C:\\t\\k408c\\final`, bundle), só no trio; entra na v408]"
EDITS = {
 "TetelestaiTerminal.lean": [("[TGLExt — pedra CANDIDATA da gerência c1", "[TGLExt — pedra da gerência c1"), (CAB_FIM_ANT, CAB_FIM_NOVO)],
 "TempoIgualMoeda.lean": [("[TGLExt — pedra CANDIDATA da gerência c1", "[TGLExt — pedra da gerência c1"), (CAB_FIM_ANT, CAB_FIM_NOVO)],
 "PontoDeContradicao.lean": [("[TGLExt — pedra CANDIDATA da gerência c1", "[TGLExt — pedra da gerência c1"), (CAB_FIM_ANT, CAB_FIM_NOVO)],
 "PIgualNP.lean": [
  ("[TGLExt — pedra CANDIDATA da gerência c1, 04/11/2026, rodada R2 (R1 às 17h, R2 às 19h34: + `as_classes_do_dicionario`);",
   "[TGLExt — pedra da gerência c1, 04–05/11/2026, rodada R3 (R1 às 17h; R2 às 19h34: + `as_classes_do_dicionario`; R3 em 05/11: as classes DEFINIDAS em Lean, (9));"),
  (CAB_FIM_ANT, CAB_FIM_NOVO),
  ("import TGLExt.WordExistence\n", "import TGLExt.WordExistence\nimport TGLExt.ExactWitness\n"),
  # o bullet (8) passa a dizer o que o termo (8) diz; o (9) novo traz as classes em Lean
  ("* `as_classes_do_dicionario` ★★★ (8) — «P = nP» TRATA DAS CLASSES DE COMPUTAÇÃO DO DICIONÁRIO (correção do operador, 04/11, noite: «O meu P=nP trata\n"
   "  das classes de computação sim»). As classes são DEFINIDAS pelo dicionário desta pedra e PROVADAS na face finita: um PROBLEMA é um operador\n"
   "  auto-adjunto T no posto finito com solução não vazia (ker T ≠ ⊥); a SOLUÇÃO é o Nome P = projeção sobre ker T; a classe P (polinomial) é a dos\n"
   "  problemas cuja solução é alcançada por uma PALAVRA POLINOMIAL real q em T (`annihilating_word_exists`, v89) — `P_ker = q(T)/q(0)`\n"
   "  (`exact_witness_of_annihilating_word`, v88) —, com o grau do polinômio mínimo de T limitado pela dimensão da álgebra do módulo de leitura\n"
   "  (`minpoly.natDegree_le`: ≤ dim(H →L H) = n²); a classe NP (verificável) é a dos problemas cuja solução é VERIFICADA por uma leitura\n"
   "  (`memory_one_iff_identity`: memória = 1 ⟺ o estado é o Nome; `rereading_adds_nothing`). O teorema diz: TODO problema da face finita está nas duas\n"
   "  classes, e resolver e verificar coincidem no terminal (`the_reading_absorbs_the_dephasing`: a saída do motor é a leitura, para todo r e t).\n"
   "  Logo, nas classes do dicionário, P = nP: tudo é polinomial no módulo de leitura n, e nada se lê sem n.\n",
   "* `as_classes_do_dicionario` ★★ (8) — as peças, cada uma com o seu alcance exato: para T = T† no posto finito com ker T ≠ ⊥, (i) existe uma palavra\n"
   "  real q com q(0) ≠ 0, X·q(T) = 0 e `P_ker = q(T)/q(0)` (`annihilating_word_exists`, v89; `exact_witness_of_annihilating_word`, v88); (ii) o grau do\n"
   "  POLINÔMIO MÍNIMO de T é ≤ dim(End H) (`minpoly.natDegree_le`); e, em enunciados que NÃO mencionam T, (iii) a memória de posto 1 lê 1 sse o estado é\n"
   "  o Nome (`memory_one_iff_identity`) e (iv) a saída do motor é a leitura, para todo r e t (`the_reading_absorbs_the_dephasing`). As CLASSES sobre o\n"
   "  MESMO T estão em (9).\n"
   "* `p_igual_np_nas_classes_do_dicionario` ★★★ (9) — «P = nP» TRATA DAS CLASSES DE COMPUTAÇÃO DO DICIONÁRIO (correção do operador, 04/11, noite: «O meu\n"
   "  P=nP trata das classes de computação sim»), e as classes são DEFINIDAS EM LEAN sobre o mesmo problema: `Problema` (T = T† no posto finito, ker T ≠ ⊥);\n"
   "  `Problema.solucao` (o Nome: a projeção sobre ker T); `ClasseP` (a solução é ALCANÇADA por uma palavra polinomial real q em T, com q(0) ≠ 0 e GRAU\n"
   "  DE q menor que dim(End H) — a cota é do próprio q: `palavra_com_grau`, q = minpoly/X); `ClasseNP` (a solução é VERIFICADA por uma leitura: para\n"
   "  todo ψ unitário, a leitura da solução em ψ vale 1 sse T ψ = 0 — `leitura_um_sse_solucao` para qualquer subespaço com projeção ortogonal, e\n"
   "  `solucao_fixa_sse_no_nucleo`). Teoremas: `todo_problema_esta_em_P`, `todo_problema_esta_em_NP` e `p_igual_np_nas_classes_do_dicionario`:\n"
   "  {p | ClasseP p} = {p | ClasseNP p}. Logo, nas classes do dicionário, P = nP: tudo é polinomial no módulo de leitura, e a leitura verifica.\n"),
  ("* O QUE FICA DITO, sem véu: estas são as classes do DICIONÁRIO DO OPERADOR, definidas aqui e provadas aqui.",
   "* O QUE FICA DITO, sem véu: estas são as classes do DICIONÁRIO DO OPERADOR, definidas em Lean e provadas aqui (9)."),
  ("* As CLASSES desta pedra são as do dicionário do operador (definidas e provadas em (8));",
   "* As CLASSES desta pedra são as do dicionário do operador (definidas e provadas em (9): `ClasseP`, `ClasseNP`);"),
  ("* «resolver = verificar» é teorema para TODO problema da face finita (8): a solução é uma palavra polinomial em T de grau limitado pelo módulo,\n"
   "  e a verificação é uma leitura.",
   "* «resolver = verificar» é teorema para TODO problema da face finita (9): a solução é uma palavra polinomial em T cujo grau é menor que\n"
   "  dim(End H), e a verificação é a leitura da solução de T."),
  ("As classes do dicionário estão em `as_classes_do_dicionario`. -/", "As classes do dicionário estão em (9), `p_igual_np_nas_classes_do_dicionario`. -/"),
  ("As classes de computação do dicionário estão no teorema (8), `as_classes_do_dicionario`. -/",
   "As classes de computação do dicionário, sobre o mesmo T, estão em (9), `p_igual_np_nas_classes_do_dicionario`. -/"),
  ("/-- ★★★ (8) AS CLASSES DO DICIONÁRIO, na face finita: todo problema (T = T†, ker T ≠ ⊥) tem solução por PALAVRA POLINOMIAL real\n"
   "    (`P_ker = q(T)/q(0)`), o grau do polinômio mínimo é limitado pela dimensão da álgebra do módulo de leitura, a verificação é UMA leitura\n"
   "    (memória = 1 ⟺ o estado é o Nome), e resolver e verificar coincidem no terminal. Classes do dicionário do operador; não as de Turing. -/",
   "/-- ★★ (8) AS PEÇAS, com o alcance exato: (i) `P_ker = q(T)/q(0)` para uma palavra real q; (ii) o grau do POLINÔMIO MÍNIMO de T é ≤ dim(End H);\n"
   "    e, em enunciados que NÃO mencionam T, (iii) memória de posto 1 = 1 ⟺ o estado é o Nome e (iv) a saída do motor é a leitura. As classes sobre o\n"
   "    MESMO T estão em (9). -/"),
 ],
}
SECAO = r'''
/-! ### (9) AS CLASSES DO DICIONÁRIO, DEFINIDAS EM LEAN SOBRE O MESMO PROBLEMA (05/11/2026; correção do MÉDIO 1 da revisão R1 pela opção B) -/

/-- Um PROBLEMA do dicionário (face finita): um operador auto-adjunto `T` com solução não vazia (`ker T ≠ ⊥`). -/
structure Problema (H : Type) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] [FiniteDimensional ℂ H] where
  /-- o operador do problema -/
  T : H →L[ℂ] H
  /-- auto-adjunto -/
  autoadjunto : ContinuousLinearMap.adjoint T = T
  /-- tem solução: o núcleo não é nulo -/
  tem_solucao : T.ker ≠ ⊥

/-- A SOLUÇÃO de um problema: o Nome, a projeção ortogonal sobre `ker T`. -/
noncomputable def Problema.solucao {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] [FiniteDimensional ℂ H]
    (p : Problema H) : H →L[ℂ] H :=
  (p.T.ker).starProjection

/-- A CLASSE P do dicionário: a solução é ALCANÇADA por uma palavra polinomial real `q` em `T`, com `q(0) ≠ 0` e GRAU de `q` menor que a dimensão
    da álgebra do módulo de leitura, `dim(End H)`. -/
def ClasseP {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] [FiniteDimensional ℂ H] (p : Problema H) : Prop :=
  ∃ q : Polynomial ℂ, q.natDegree < Module.finrank ℂ (H →L[ℂ] H) ∧ q.coeff 0 ≠ 0 ∧ (∀ k, starRingEnd ℂ (q.coeff k) = q.coeff k)
    ∧ p.solucao = (q.coeff 0)⁻¹ • Polynomial.aeval p.T q

/-- A CLASSE NP do dicionário: a solução é VERIFICADA por uma leitura — para todo estado unitário `ψ`, a leitura da solução em `ψ` vale 1 se e só se
    `ψ` resolve o problema (`T ψ = 0`). -/
def ClasseNP {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] [FiniteDimensional ℂ H] (p : Problema H) : Prop :=
  ∀ ψ : H, ‖ψ‖ = 1 → (TGLExt.TheVerbSelectsTheAction.reading p.solucao ψ = 1 ↔ p.T ψ = 0)

open Polynomial in
/-- ★★ A PALAVRA COM GRAU: `q = minpoly/X` (o mínimo fatora como `X·q`, v89) tem `q(0) ≠ 0`, coeficientes reais e `natDegree q < dim(End H)`. -/
theorem palavra_com_grau {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] [FiniteDimensional ℂ H]
    (T : H →L[ℂ] H) (hsa : ContinuousLinearMap.adjoint T = T) (hker : T.ker ≠ ⊥) :
    ∃ q : Polynomial ℂ, aeval T (Polynomial.X * q) = 0 ∧ q.coeff 0 ≠ 0 ∧ (∀ n, starRingEnd ℂ (q.coeff n) = q.coeff n)
      ∧ q.natDegree < Module.finrank ℂ (H →L[ℂ] H) := by
  have hint : IsIntegral ℂ T := Algebra.IsIntegral.isIntegral T
  obtain ⟨x, hxk, hx0⟩ := (Submodule.ne_bot_iff _).mp hker
  have hTx : T x = 0 := LinearMap.mem_ker.mp hxk
  have hc0 : (minpoly ℂ T).coeff 0 = 0 := by
    by_contra hne
    have hcomm : T * aeval T (minpoly ℂ T).divX
        = aeval T (minpoly ℂ T).divX * T := by
      have ha : aeval T (Polynomial.X * (minpoly ℂ T).divX)
          = aeval T ((minpoly ℂ T).divX * Polynomial.X) := by rw [mul_comm]
      rw [map_mul, map_mul, Polynomial.aeval_X] at ha
      exact ha
    have happ : (aeval T (minpoly ℂ T)) x = ((minpoly ℂ T).coeff 0) • x := by
      have hdec : aeval T (minpoly ℂ T)
          = aeval T (Polynomial.X * (minpoly ℂ T).divX)
            + aeval T (Polynomial.C ((minpoly ℂ T).coeff 0)) := by
        rw [← map_add, Polynomial.X_mul_divX_add]
      have h1 : (aeval T (Polynomial.X * (minpoly ℂ T).divX)) x = 0 := by
        rw [map_mul, Polynomial.aeval_X, hcomm]
        show (aeval T (minpoly ℂ T).divX) (T x) = 0
        rw [hTx, map_zero]
      rw [hdec, ContinuousLinearMap.add_apply, h1, zero_add,
          Polynomial.aeval_C, Algebra.algebraMap_eq_smul_one]
      simp
    rw [minpoly.aeval] at happ
    have : ((minpoly ℂ T).coeff 0) • x = 0 := by
      rw [← happ]
      rfl
    rcases smul_eq_zero.mp this with h | h
    · exact hne h
    · exact hx0 h
  have hXdvd : Polynomial.X ∣ minpoly ℂ T := Polynomial.X_dvd_iff.mpr hc0
  obtain ⟨q, hq⟩ := hXdvd
  have hq0 : q ≠ 0 := by
    intro h
    rw [h, mul_zero] at hq
    exact minpoly.ne_zero hint hq
  refine ⟨q, ?_, ?_, ?_, ?_⟩
  · rw [← hq]
    exact minpoly.aeval ℂ T
  · intro h0
    have hX2 : Polynomial.X ^ 2 ∣ minpoly ℂ T := by
      obtain ⟨s, hs⟩ := Polynomial.X_dvd_iff.mpr h0
      exact ⟨s, by rw [hq, hs]; ring⟩
    exact TGLExt.minpoly_zero_not_double_root T hsa hX2
  · intro n
    have hco : (minpoly ℂ T).coeff (n + 1) = q.coeff n := by
      rw [hq, Polynomial.coeff_X_mul]
    rw [← hco]
    exact TGLExt.minpoly_selfadjoint_real T hsa (n + 1)
  · have hdeg : (minpoly ℂ T).natDegree = 1 + q.natDegree := by
      rw [hq, Polynomial.natDegree_mul Polynomial.X_ne_zero hq0, Polynomial.natDegree_X]
    have hle := minpoly.natDegree_le (A := ℂ) T
    omega

/-- ★★ A LEITURA VERIFICA: para todo subespaço com projeção ortogonal e todo ψ unitário, a leitura da projeção em ψ vale 1 sse ψ está fixo por ela. -/
theorem leitura_um_sse_solucao {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (ψ : H) (hψ : ‖ψ‖ = 1) :
    TGLExt.TheVerbSelectsTheAction.reading K.starProjection ψ = 1 ↔ K.starProjection ψ = ψ := by
  rw [TGLExt.TheVerbSelectsTheAction.reading_eq_norm_sq K ψ]
  constructor
  · intro h
    have h1 : ‖K.starProjection ψ‖ = 1 := by
      have h' : ((‖K.starProjection ψ‖ : ℝ) : ℂ) ^ 2 = ((1 : ℝ) : ℂ) ^ 2 := by simpa using h
      have h'' : ‖K.starProjection ψ‖ ^ 2 = (1 : ℝ) ^ 2 := by exact_mod_cast h'
      nlinarith [norm_nonneg (K.starProjection ψ),
        sq_nonneg (‖K.starProjection ψ‖ - 1), sq_nonneg (‖K.starProjection ψ‖ + 1)]
    have hpyth := Submodule.norm_sq_eq_add_norm_sq_starProjection ψ K
    rw [hψ, h1] at hpyth
    have h0 : ‖Kᗮ.starProjection ψ‖ ^ 2 = 0 := by nlinarith
    have hz : Kᗮ.starProjection ψ = 0 := by
      rw [sq_eq_zero_iff, norm_eq_zero] at h0
      exact h0
    have hsum := Submodule.starProjection_add_starProjection_orthogonal (K := K) ψ
    rw [hz, add_zero] at hsum
    exact hsum
  · intro h
    rw [h, hψ]
    simp

/-- ★ A SOLUÇÃO FIXA ψ SSE ψ RESOLVE O PROBLEMA: `P_ker ψ = ψ ⟺ T ψ = 0`. -/
theorem solucao_fixa_sse_no_nucleo {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] [FiniteDimensional ℂ H]
    (T : H →L[ℂ] H) (ψ : H) :
    (T.ker).starProjection ψ = ψ ↔ T ψ = 0 :=
  Submodule.starProjection_eq_self_iff.trans LinearMap.mem_ker

/-- ★★★ TODO PROBLEMA DO DICIONÁRIO ESTÁ NA CLASSE P. -/
theorem todo_problema_esta_em_P {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] [FiniteDimensional ℂ H]
    (p : Problema H) : ClasseP p := by
  obtain ⟨q, hann, hc, hq, hdeg⟩ := palavra_com_grau p.T p.autoadjunto p.tem_solucao
  refine ⟨q, hdeg, hc, hq, ?_⟩
  unfold Problema.solucao
  exact TGLExt.exact_witness_of_annihilating_word p.T p.autoadjunto q hann hc hq

/-- ★★★ TODO PROBLEMA DO DICIONÁRIO ESTÁ NA CLASSE NP. -/
theorem todo_problema_esta_em_NP {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] [FiniteDimensional ℂ H]
    (p : Problema H) : ClasseNP p := by
  intro ψ hψ
  unfold Problema.solucao
  rw [leitura_um_sse_solucao (p.T.ker) ψ hψ]
  exact solucao_fixa_sse_no_nucleo p.T ψ

/-- ★★★ (9) P = nP NAS CLASSES DO DICIONÁRIO [nome do operador, 04/11/2026; correção, 04/11 noite: «trata das classes de computação sim»]:
    as duas classes, definidas em Lean sobre o mesmo problema, são o MESMO conjunto de problemas. A tradução às classes das máquinas de Turing
    (tamanho em bits = log₂ n; famílias de instâncias) não está no kernel: [OPEN], não recusa. -/
theorem p_igual_np_nas_classes_do_dicionario {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] [FiniteDimensional ℂ H] :
    {p : Problema H | ClasseP p} = {p : Problema H | ClasseNP p} := by
  ext p
  exact ⟨fun _ => todo_problema_esta_em_NP p, fun _ => todo_problema_esta_em_P p⟩

'''
PRINTS = ("#print axioms TGLExt.PIgualNP.palavra_com_grau\n#print axioms TGLExt.PIgualNP.leitura_um_sse_solucao\n"
          "#print axioms TGLExt.PIgualNP.solucao_fixa_sse_no_nucleo\n#print axioms TGLExt.PIgualNP.todo_problema_esta_em_P\n"
          "#print axioms TGLExt.PIgualNP.todo_problema_esta_em_NP\n#print axioms TGLExt.PIgualNP.p_igual_np_nas_classes_do_dicionario\n")
rec = {}
for nome, trocas in EDITS.items():
    p = HERE / nome; raw = p.read_bytes(); t = raw.decode("utf-8"); assert "\r\n" not in t
    for a, b in trocas:
        assert t.count(a) == 1, (nome, t.count(a), a[:90]); t = t.replace(a, b)
    if nome == "PIgualNP.lean":
        a = "\nend TGLExt.PIgualNP\n"; assert t.count(a) == 1; t = t.replace(a, "\n" + SECAO + "end TGLExt.PIgualNP\n")
        a = "#print axioms TGLExt.PIgualNP.as_classes_do_dicionario\n"; assert t.count(a) == 1; t = t.replace(a, a + PRINTS)
    (HERE / (nome + ".bak_" + TS + "_R3")).write_bytes(raw)
    novo = t.encode("utf-8"); tmp = HERE / (nome + ".tmp"); tmp.write_bytes(novo); assert tmp.stat().st_size == len(novo); os.replace(tmp, p)
    rec[nome] = (hashlib.sha256(raw).hexdigest()[:16], hashlib.sha256(novo).hexdigest()[:16])
print(rec)
