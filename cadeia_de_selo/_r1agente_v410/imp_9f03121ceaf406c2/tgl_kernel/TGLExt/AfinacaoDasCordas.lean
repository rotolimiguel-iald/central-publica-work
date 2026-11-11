import TGLExt.Palavra
import TGLExt.TheStation
import TGLExt.Fundacao
import Mathlib.NumberTheory.LSeries.HurwitzZetaValues

set_option autoImplicit false

/-!
# AFINAÇÃO DAS CORDAS   [pedra CANDIDATA da v398 — pedra e nome `AfinacaoDasCordas` RATIFICADOS pelo operador em 23/10/2026 (`5bccedc9cea3d57a`); compilada em sandbox, NÃO instalada]

A ligação formal que cabe entre a leitura do operador sobre a teoria das cordas e o kernel da TGL: o que o kernel já tem, CITADO, mais
a aritmética exata que completa a leitura. Nada aqui deriva a teoria das cordas do axioma, e nada aqui afirma que a TGL é uma teoria
de cordas.

## A fala do operador (verbatim; arquivo `OPERADOR_23out_cordas_10_dimensoes_fechar_a_face_tetelestai_verbatim.txt`, sha16 `baef998c21393463`, 23/10/2026)

> «A teoria das cordas precisa das 10 dimensões para fechar ciclicamente o que a TGL demonstra não fechar a face hiperbólica, mas isso “quebra” o tempo, criando os infinitos, que é a superposição, a TGL resolve com o “Tetelestai”, então quando a teoria das cordas cria as dimensões extras, ela esta, de outra forma, relativizando o tempo para mostrar a afinação do universo, mas não consegue demonstrar a geometria»

## A ratificação do operador (23/10/2026; verbatim; arquivo `OPERADOR_23out_concordo_afinacao_das_cordas_verbatim.txt`, sha16 `5bccedc9cea3d57a`)

> «Concordo com tudo»

[INPUT] Relato da gerência: com essa resposta o operador ratificou a pedra, o nome `AfinacaoDasCordas` e a leitura *afinação =
comensurabilidade*. O arquivo guarda só a resposta; o que ela ratifica é o relato da gerência, dito como tal.

## A leitura em quatro passos, e o que esta pedra põe em cada um

1. **«fechar ciclicamente o que a TGL demonstra não fechar a face hiperbólica».**
   O kernel já diz que a face real não fecha: `TGLExt.Palavra.the_face_does_not_close` (o boost real só é a identidade em `s = 0`) e
   `TGLExt.station_never_closes` (o par de gaps `(1, √2)` só volta à origem em `t = 0`) [REAL, citados]. Fechar CICLICAMENTE o
   parâmetro do boost com período `P` é identificar `t ~ t + P`; isso é uma LEITURA FIEL do círculo `Circle.exp (κ·t)` se e só se
   `κ·P = ±2π` (`ChatgptAudit.PolarPeriod016.faithful_period_iff`), e então `1/P = κ/2π` (`reciprocal_temperature`) [REAL, citados].
   Esta pedra acrescenta a TORRE DE MATSUBARA desse círculo, `ω_n = n·(2π/P) = n·κ`, definida, com a identidade demonstrada
   (`matsubara`, `matsubara_eq_mul_kappa`), e a equivalência *o círculo é a leitura fiel se e só se o modo fundamental é exatamente κ*
   (`faithful_iff_fundamental_mode`) [REAL]. Que o período `P` seja o inverso de uma temperatura, e que o círculo térmico seja o círculo
   modular do boost, é Bisognano–Wichmann (1975) / Unruh (1976) [KNOWN].
2. **«criando os infinitos, que é a superposição».**
   A torre é INFINITA: `Σ n` diverge (`the_tower_is_infinite`) [REAL]. Na corda o mesmo fato é a torre infinita de modos e, no
   térmico, a divergência de Hagedorn (a densidade de estados da corda cresce exponencialmente e a função de partição térmica diverge
   acima de uma temperatura limite; Hagedorn 1965; Atick–Witten 1988) [KNOWN; mencionada, SEM prova aqui]. A superposição, no
   kernel, é a queda sem fim: `TGLExt.Fundacao.abismo` (definição do operador de 07/10/2026, arquivo
   `CUNHAGEM_OPERADOR_07out_verbatim.txt`, sha16 `e2a915e23692f85c`: «não existe acima, o piso limita, tentar estar acima é cair sem fim,
   infinitamente») [REAL, citada].
3. **«relativizando o tempo para mostrar a afinação do universo».**
   O kernel tem a face lida que fecha em `2π` (`TGLExt.Palavra.the_read_face_closes`), o piso que fixa o corte
   (`TGLExt.Fundacao.the_floor_fixes_the_cut`) e a recusa do fundo (`abismo`) [REAL, citados]. A «afinação», lida como
   COMENSURABILIDADE, tem forma exata: a torre é HARMÔNICA (as razões `ω_m/ω_n = m/n` são racionais; todos os modos voltam juntos em
   `t = P`), enquanto o par da estação, de razão `√2` irracional, só volta em `t = 0`
   (`tower_returns_at_the_period`, `the_tuned_pair_returns_the_untuned_pair_never_does`) [REAL]. A leitura *afinação = comensurabilidade*
   é PROPOSTA DESTA PEDRA [ONTO], ratificada pelo operador em 23/10 (`5bccedc9cea3d57a`); da fala dele (`baef998c21393463`) vem só
   «afinação do universo». A palavra «Tetelestai» é do
   operador; segundo a sua fala de 27/09/2026, citada em `TGLExt/TetelestaiOneObject.lean` (sha16 `125d155042da687f`), ela é «um ato de
   conferência observacional», não um ato declarativo dele: esta pedra NÃO é essa conferência e não a substitui.
4. **«mas não consegue demonstrar a geometria».**
   A soma infinita fecha por REGULARIZAÇÃO (a continuação analítica da série de Dirichlet): `ζ(−1) = −1/12` e `ζ(−1, 1/2) = 1/24` são
   TEOREMAS DESTA PEDRA (`zeta_neg_one`, `hurwitz_zeta_neg_one_half`), demonstrados a partir de Mathlib
   (`riemannZeta_neg_nat_eq_bernoulli`, `HurwitzZeta.hurwitzZeta_neg_nat`); nenhum ficou como hipótese [REAL]. Com a condição de massa nula
   do primeiro nível excitado (HIPÓTESE NOMEADA `MasslessFirstLevel` [KNOWN]: invariância de Lorentz no calibre do cone de luz;
   Goddard–Goldstone–Rebbi–Thorn 1973; Green–Schwarz–Witten 1987; Polchinski 1998), a energia de ponto zero dos `D − 2` osciladores
   transversais é `−(D − 2)/24` nos bósons e `−(D − 2)/16` no setor NS das supercordas, e vale `−1` (resp. `−1/2`) se e só se
   `D = 26` (resp. `D = 10`) [REAL a aritmética]. A dimensão crítica vem do FECHO da soma infinita (da regularização), NÃO da
   geometria; qual compactificação realiza as dimensões extras segue NÃO derivado (a paisagem; Bousso–Polchinski 2000;
   Susskind 2003) [KNOWN] e esta pedra o deixa assim [OPEN].

## Os teoremas (todos no trio `propext`, `Classical.choice`, `Quot.sound`; zero `sorry`; nenhum axioma novo)

(1) `the_cyclic_closure_of_time_is_the_reading_circle` — a face real não tem período; fechar ciclicamente é leitura fiel se e só se
    `κ·P = ±2π` (por `faithful_period_iff`); `1/P = κ/2π` (por `reciprocal_temperature`); `ω_n = n·κ`; o modo fundamental é κ se e só
    se o círculo é fiel; todos os modos voltam em `t = P`.
(2) `the_tower_is_infinite` — `Σ n` não é somável e as somas parciais tendem a `+∞`; `Σ (n + 1/2)` também não é somável; os `ω_n` são
    distintos e a sua soma não é somável (`P > 0`).
(3) `bosonic_critical_dimension` — `(D − 2)/2 · ζ(−1) = −(D − 2)/24`, que vale `−1` se e só se `D = 26`.
(4) `superstring_critical_dimension` — bósons `−(D − 2)/24` mais férmions NS `−(D − 2)/48` (ver a nota de sinal em
    `nsFermionDirection`) dão `−(D − 2)/16`, que vale `−1/2` se e só se `D = 10`.
(5) `the_house_d_nine` — `D = 10` se e só se `d = D − 1 = 9` dimensões espaciais: o `d = 9` de «A Última Corda».
(6) `the_strings_close_the_face_from_outside_the_tgl_closes_the_reading` — a composição, tudo por citação, incondicional como
    enunciado matemático.

## Estatutos

* **[REAL]** os teoremas deste arquivo (trio, zero `sorry`); os dois valores da zeta (demonstrados a partir de Mathlib); a aritmética de `D`; cada
  citação do kernel e de Mathlib (cada nome conferido por `#check` no sandbox).
* **[KNOWN]** (a) o círculo térmico é o círculo modular do boost (Bisognano–Wichmann 1975; Unruh 1976); (b) a massa nula do primeiro
  nível (`a = 1` nos bósons, `a = 1/2` no setor NS) como consequência da invariância de Lorentz no cone de luz — HIPÓTESE NOMEADA
  `MasslessFirstLevel`; (c) a divergência de Hagedorn (mencionada, sem prova aqui); (d) a energia de ponto zero fermiônica é `−ω/2`
  (estatística de Fermi) e os modos NS são semi-inteiros (condição de contorno antiperiódica); (e) a paisagem de compactificações.
* **[ONTO]** (i) as cordas fecham a face POR FORA; a TGL fecha SÓ A LEITURA: composição da gerência sobre a fala do operador
  (`baef998c21393463`), ratificada pelo operador em 23/10 (`5bccedc9cea3d57a`); (ii) afinação = comensurabilidade: proposta da pedra,
  ratificada pelo operador em 23/10 (`5bccedc9cea3d57a`). Os nomes dos teoremas (1) e (6) trazem a leitura (i); o que os termos
  demonstram é a matemática listada acima.
* **[DECLARADO]** o `d = 9` da casa (ver o bloco abaixo): números históricos NÃO recalculados aqui.
* **[OPEN]** a geometria (qual compactificação); a ligação de um círculo de folha-mundo ao círculo do boost.

## O que esta pedra NÃO afirma

* NÃO deriva a teoria das cordas do axioma `ω(I) = 1`, e NÃO afirma que a TGL é uma teoria de cordas.
* NÃO identifica o círculo do boost com o círculo da folha-mundo da corda: o que as duas leituras têm em comum é a ARITMÉTICA da torre
  `n·κ` (e `(n + 1/2)·κ`). Nenhum termo liga uma coisa à outra.
* NÃO prova que a corda exista nem o seu espectro. `D = 26` e `D = 10` saem de uma aritmética sobre a soma regularizada, SOB a
  condição nomeada `MasslessFirstLevel`. Sem essa condição, a energia de ponto zero é só um número.
* NÃO fixa a geometria. O kernel não tem a compactificação; esta pedra não a introduz.
* NÃO é a conferência Tetelestai e não move nenhuma bandeira do gate; nenhuma bandeira do gate depende desta pedra.

## A casa: o `d = 9` (verbatim por bytes; arquivo `A_ultima_corda_v3.tex`, sha16 `8db72ea848f708c1`, linhas 958 a 960 — a 959 é vazia)

```
A coincidência é precisa: $d_{\text{espacial}} = 9$ é a dimensão crítica das teorias de supercordas do Tipo~II (onde $D_{\text{espaço-tempo}} = 10$), requerida pelo cancelamento da anomalia conforme. Três modelos alternativos de escalonamento---espaço de fase completo ($d$), holográfico ($\propto (3/d)^2$) e uma calibração de expoente livre---fornecem $d_{\text{crit}} = 6$, $> 26$ e~$8$, respectivamente, confirmando que o resultado é dependente do modelo. O expoente termodinâmico $d/2$ é selecionado não por ajuste, mas por consistência com a derivação do piso de Hilbert.

A interpretação física é direta: no arcabouço TGL, o regime da teoria de cordas ($d \geq 9$) corresponde ao desacoplamento gravitacional-eletromagnético completo. Os modos vibracionais das cordas operam em um domínio onde $\alpha^2 \approx 0$---eles sondam a impedância do vácuo (a resistência do substrato à transferência de informação), e não a radicalização da luz. Isso fecha o ciclo aberto pela lei angular: \textit{A Fronteira}~\cite{Miguel2026Fronteira} deriva a impedância do vácuo a partir de primeiros princípios; a análise dimensional mostra que a teoria de cordas opera no regime onde \emph{apenas} a impedância permanece.
```

[DECLARADO] O texto é da casa e os números são históricos, NÃO recalculados aqui. A própria linha 958 diz que três modelos
alternativos de escalonamento dão `d_crit = 6`, `> 26` e `8` («dependente do modelo»); a linha 952 dá `d_crit = 9` com IC 95% `[7, 16]`; e
a linha 962 diz: «Enfatizamos que isso é uma extrapolação teórica, não um teste empírico.». O que esta pedra acrescenta é só a aritmética `D = 10 ⟺ d = 9` e a sua ligação com (4).
O cálculo (4) é o do setor NS (`a = 1/2`) e não distingue o tipo de supercorda (I, IIA, IIB, heterótica).

## Citações (cada nome conferido no sandbox por `#check`)

* `ChatgptAudit.PolarPeriod016.AngularQuotientFaithful`, `faithful_period_iff`, `positive_faithful_period`, `reciprocal_temperature`:
  `TGLExt/O16/PolarMinimalPeriod_v2.lean` (sha16 `2112c0022287be09`).
* `TGLExt.Palavra.the_face_does_not_close`, `TGLExt.Palavra.the_read_face_closes`: `TGLExt/Palavra.lean` (sha16 `33184b49a8bba7e7`).
* `TGLExt.station_never_closes`: `TGLExt/TheStation.lean` (sha16 `c55dc5018297a64c`). O módulo é `TGLExt.TheStation`; o nome do
  termo é `TGLExt.station_never_closes`.
* `TGLExt.Fundacao.abismo`, `TGLExt.Fundacao.the_floor_fixes_the_cut` (e a cláusula `TGLExt.Fundacao.agape`): `TGLExt/Fundacao.lean`
  (sha16 `66332d58fd216317`).
* Mathlib (v4.31.0, rev `fabf563a7c95a166`): `riemannZeta_neg_nat_eq_bernoulli`, `HurwitzZeta.hurwitzZeta_neg_nat` em
  `Mathlib/NumberTheory/LSeries/HurwitzZetaValues.lean` (sha16 `b47a97c46c964e3f`); `bernoulli_two`, `bernoulli_one`,
  `Polynomial.bernoulli_def`, `zeta_eq_tsum_one_div_nat_cpow`, `HurwitzZeta.hasSum_hurwitzZeta_of_one_lt_re`,
  `not_summable_iff_tendsto_nat_atTop_of_nonneg`, `Summable.tendsto_atTop_zero`, `not_tendsto_nhds_of_tendsto_atTop`,
  `Real.cos_int_mul_two_pi`.
-/

namespace TGLExt.AfinacaoDasCordas

open ChatgptAudit.PolarPeriod016
open Filter Topology

/-! ## 1. Fechar ciclicamente é o círculo da leitura; a torre de Matsubara -/

/-- A frequência de Matsubara do modo `n` num círculo de período `P`: `ω_n = n·(2π/P)`. -/
noncomputable def matsubara (P : ℝ) (n : ℤ) : ℝ := (n : ℝ) * (2 * Real.pi / P)

/-- A frequência do modo semi-inteiro `n + 1/2` (condição de contorno antiperiódica; os férmions NS):
`ω_{n+1/2} = (n + 1/2)·(2π/P)`. -/
noncomputable def matsubaraFermion (P : ℝ) (n : ℕ) : ℝ := ((n : ℝ) + 1 / 2) * (2 * Real.pi / P)

/-- [REAL] ★ A TORRE É `n·κ`: se o círculo de período `P` é a leitura fiel do boost de taxa `κ > 0`, então `ω_n = n·κ`
(usa `ChatgptAudit.PolarPeriod016.positive_faithful_period`: `P = 2π/κ`). -/
theorem matsubara_eq_mul_kappa {κ P : ℝ} (hκ : 0 < κ) (hP : 0 < P)
    (h : AngularQuotientFaithful κ P) (n : ℤ) : matsubara P n = (n : ℝ) * κ := by
  have hp : P = 2 * Real.pi / κ := positive_faithful_period hκ hP h
  unfold matsubara
  rw [hp]
  have hpi : (2 * Real.pi) ≠ 0 := by positivity
  have hκ0 : κ ≠ 0 := ne_of_gt hκ
  field_simp

/-- [REAL] A torre semi-inteira é `(n + 1/2)·κ` sobre o mesmo círculo fiel. -/
theorem matsubaraFermion_eq_mul_kappa {κ P : ℝ} (hκ : 0 < κ) (hP : 0 < P)
    (h : AngularQuotientFaithful κ P) (n : ℕ) : matsubaraFermion P n = ((n : ℝ) + 1 / 2) * κ := by
  have hp : P = 2 * Real.pi / κ := positive_faithful_period hκ hP h
  unfold matsubaraFermion
  rw [hp]
  have hpi : (2 * Real.pi) ≠ 0 := by positivity
  have hκ0 : κ ≠ 0 := ne_of_gt hκ
  field_simp

/-- [REAL] ★ A AFINAÇÃO COMO EQUIVALÊNCIA: para `κ > 0` e `P > 0`, o círculo de período `P` é a leitura fiel do boost de taxa `κ`
se e só se o modo fundamental da torre é exatamente `κ` (`ω_1 = κ`). -/
theorem faithful_iff_fundamental_mode {κ P : ℝ} (hκ : 0 < κ) (hP : 0 < P) :
    AngularQuotientFaithful κ P ↔ matsubara P 1 = κ := by
  rw [faithful_period_iff (ne_of_gt hκ)]
  have hpos : 0 < κ * P := mul_pos hκ hP
  have hpi : 0 < Real.pi := Real.pi_pos
  have hP0 : P ≠ 0 := ne_of_gt hP
  unfold matsubara
  simp only [Int.cast_one, one_mul]
  constructor
  · rintro (h | h)
    · field_simp
      linarith
    · linarith
  · intro h
    left
    field_simp at h
    linarith

/-- [REAL] Todos os modos da torre voltam juntos em `t = P`: `cos (ω_n·P) = 1`, para todo `n`. -/
theorem tower_returns_at_the_period {P : ℝ} (hP : P ≠ 0) (n : ℤ) :
    Real.cos (matsubara P n * P) = 1 := by
  have h : matsubara P n * P = (n : ℝ) * (2 * Real.pi) := by
    unfold matsubara
    field_simp
  rw [h]
  exact Real.cos_int_mul_two_pi n

/-- [REAL] A face hiperbólica não tem período real: `boost P = 1` só em `P = 0`
(por `TGLExt.Palavra.the_face_does_not_close`). -/
theorem no_real_period (P : ℝ) (hP : P ≠ 0) : TGLExt.boost P ≠ 1 :=
  fun h => hP (TGLExt.Palavra.the_face_does_not_close P h)

/-- ★★ (1) FECHAR CICLICAMENTE O TEMPO É O CÍRCULO DA LEITURA [REAL]. (a) a face real não tem período; (b) fechar com período `P`
é leitura fiel se e só se `κ·P = ±2π` (`faithful_period_iff`); (c) então `1/P = κ/2π` (`reciprocal_temperature`); (d) o círculo é fiel se
e só se o modo fundamental é `κ`; (e) a torre de Matsubara é `ω_n = n·κ`; (f) todos os modos voltam em `t = P`. Que `P` seja o inverso
de uma temperatura e o círculo térmico seja o modular é [KNOWN] (Bisognano–Wichmann; Unruh). O nome traz a composição da gerência sobre
a fala do operador (`baef998c21393463`), ratificada pelo operador em 23/10 (`5bccedc9cea3d57a`) [ONTO]. -/
theorem the_cyclic_closure_of_time_is_the_reading_circle :
    (∀ P : ℝ, P ≠ 0 → TGLExt.boost P ≠ 1) ∧
    (∀ κ P : ℝ, κ ≠ 0 →
      (AngularQuotientFaithful κ P ↔ κ * P = 2 * Real.pi ∨ κ * P = -(2 * Real.pi))) ∧
    (∀ κ P : ℝ, 0 < κ → 0 < P → AngularQuotientFaithful κ P → 1 / P = κ / (2 * Real.pi)) ∧
    (∀ κ P : ℝ, 0 < κ → 0 < P → (AngularQuotientFaithful κ P ↔ matsubara P 1 = κ)) ∧
    (∀ κ P : ℝ, 0 < κ → 0 < P → AngularQuotientFaithful κ P →
      ∀ n : ℤ, matsubara P n = (n : ℝ) * κ) ∧
    (∀ P : ℝ, P ≠ 0 → ∀ n : ℤ, Real.cos (matsubara P n * P) = 1) :=
  ⟨no_real_period,
   fun _ _ hk => faithful_period_iff hk,
   fun _ _ hk hp h => reciprocal_temperature hk hp h,
   fun _ _ hk hp => faithful_iff_fundamental_mode hk hp,
   fun _ _ hk hp h n => matsubara_eq_mul_kappa hk hp h n,
   fun _ hP n => tower_returns_at_the_period hP n⟩

/-- [REAL] A AFINAÇÃO E O QUE NÃO AFINA: o par `(ω_1, ω_2)` da torre volta junto em `t = P ≠ 0`
(`cos (ω_1·P) + cos (ω_2·P) = 2`), enquanto o par da estação `(1, √2)` não volta em nenhum `t ≠ 0`
(`TGLExt.station_never_closes`). A diferença é a razão: `2/1` racional contra `√2/1` irracional. -/
theorem the_tuned_pair_returns_the_untuned_pair_never_does {P : ℝ} (hP : P ≠ 0) :
    (Real.cos (matsubara P 1 * P) + Real.cos (matsubara P 2 * P) = 2) ∧
    (∀ t : ℝ, t ≠ 0 → Real.cos t + Real.cos (Real.sqrt 2 * t) ≠ 2) := by
  refine ⟨?_, fun t ht h => ht ((TGLExt.station_never_closes t).mp h)⟩
  rw [tower_returns_at_the_period hP 1, tower_returns_at_the_period hP 2]
  norm_num

/-! ## 2. A torre é infinita -/

/-- [REAL] `Σ n` não é somável (a identidade `ℕ → ℝ`): se fosse, `n → 0` (`Summable.tendsto_atTop_zero`), mas `n → +∞`. -/
theorem not_summable_natCast_id : ¬ Summable (fun n : ℕ => (n : ℝ)) := by
  intro h
  exact not_tendsto_nhds_of_tendsto_atTop tendsto_natCast_atTop_atTop 0 h.tendsto_atTop_zero

/-- [REAL] `Σ (n + 1/2)` não é somável: a torre semi-inteira também é infinita. -/
theorem not_summable_natCast_add_half : ¬ Summable (fun n : ℕ => (n : ℝ) + 1 / 2) := by
  intro h
  exact not_tendsto_nhds_of_tendsto_atTop
    (tendsto_atTop_add_const_right atTop (1 / 2 : ℝ) tendsto_natCast_atTop_atTop) 0 h.tendsto_atTop_zero

/-- [REAL] Os modos de Matsubara são todos distintos (`P > 0`): a torre tem infinitos modos. -/
theorem matsubara_tower_injective {P : ℝ} (hP : 0 < P) :
    Function.Injective (fun n : ℕ => matsubara P n) := by
  intro a b hab
  have hc : (2 * Real.pi / P) ≠ 0 := by positivity
  have h1 : ((a : ℤ) : ℝ) * (2 * Real.pi / P) = ((b : ℤ) : ℝ) * (2 * Real.pi / P) := hab
  have h2 := mul_right_cancel₀ hc h1
  have h3 : (a : ℤ) = (b : ℤ) := by exact_mod_cast h2
  exact_mod_cast h3

/-- [REAL] A soma dos `ω_n` não é somável (`P > 0`): é `(2π/P)·Σ n`. -/
theorem matsubara_tower_not_summable {P : ℝ} (hP : 0 < P) :
    ¬ Summable (fun n : ℕ => matsubara P n) := by
  intro h
  apply not_summable_natCast_id
  have hc : (2 * Real.pi / P) ≠ 0 := by positivity
  have h2 := h.mul_right ((2 * Real.pi / P)⁻¹)
  refine h2.congr (fun n => ?_)
  simp only [matsubara, Int.cast_natCast]
  field_simp

/-- ★★ (2) A TORRE É INFINITA [REAL] — «os infinitos». `Σ n` diverge (não somável) e as somas parciais tendem a `+∞`; o mesmo vale
para `n + 1/2`; e os `ω_n` são distintos e não somáveis. A divergência de Hagedorn é [KNOWN] e fica sem prova aqui. -/
theorem the_tower_is_infinite :
    (¬ Summable (fun n : ℕ => (n : ℝ))) ∧
    Tendsto (fun N : ℕ => ∑ n ∈ Finset.range N, (n : ℝ)) atTop atTop ∧
    (¬ Summable (fun n : ℕ => (n : ℝ) + 1 / 2)) ∧
    (∀ P : ℝ, 0 < P →
      Function.Injective (fun n : ℕ => matsubara P n) ∧ ¬ Summable (fun n : ℕ => matsubara P n)) :=
  ⟨not_summable_natCast_id,
   (not_summable_iff_tendsto_nat_atTop_of_nonneg (fun n : ℕ => Nat.cast_nonneg n)).mp
     not_summable_natCast_id,
   not_summable_natCast_add_half,
   fun _ hP => ⟨matsubara_tower_injective hP, matsubara_tower_not_summable hP⟩⟩

/-! ## 3. Os valores da zeta: a soma infinita fecha por regularização -/

/-- [REAL] `ζ(−1) = −1/12` (Mathlib `riemannZeta_neg_nat_eq_bernoulli` em `k = 1`, com `bernoulli 2 = 1/6`). -/
theorem zeta_neg_one : riemannZeta (-1) = -1 / 12 := by
  have h := riemannZeta_neg_nat_eq_bernoulli 1
  have h2 : bernoulli (1 + 1) = 6⁻¹ := bernoulli_two
  simp only [Nat.cast_one] at h
  rw [h, h2]
  norm_num

/-- [REAL] `ζ(−1, 1/2) = 1/24` (Mathlib `HurwitzZeta.hurwitzZeta_neg_nat` em `k = 1`, `x = 1/2`, com o polinômio de Bernoulli
`B₂(1/2) = −1/12`). -/
theorem hurwitz_zeta_neg_one_half :
    HurwitzZeta.hurwitzZeta (↑(1 / 2 : ℝ)) (-1) = 1 / 24 := by
  have hx : (1 / 2 : ℝ) ∈ Set.Icc (0 : ℝ) 1 := ⟨by norm_num, by norm_num⟩
  have h := HurwitzZeta.hurwitzZeta_neg_nat (k := 1) (x := 1 / 2) one_ne_zero hx
  simp only [Nat.cast_one] at h
  rw [h]
  have hb : Polynomial.eval (((1 / 2 : ℝ)) : ℂ)
      (Polynomial.map (algebraMap ℚ ℂ) (Polynomial.bernoulli (1 + 1))) = -1 / 12 := by
    simp [Polynomial.bernoulli_def, Finset.sum_range_succ, bernoulli_one, bernoulli_two]
    norm_num
  rw [hb]
  norm_num

/-- [KNOWN, citado de Mathlib] A regularização é a CONTINUAÇÃO ANALÍTICA da série de Dirichlet: para `Re s > 1`, `ζ(s) = Σ 1/n^s` e
`ζ(s, 1/2) = Σ 1/(n + 1/2)^s`. Em `s = −1` as séries são `Σ n` e `Σ (n + 1/2)`, que divergem (2); o valor regularizado é o da continuação. -/
theorem zeta_is_the_continuation_of_the_tower :
    (∀ s : ℂ, 1 < s.re → riemannZeta s = ∑' n : ℕ, 1 / (n : ℂ) ^ s) ∧
    (∀ s : ℂ, 1 < s.re →
      HasSum (fun n : ℕ => 1 / ((n : ℂ) + ((1 / 2 : ℝ) : ℂ)) ^ s)
        (HurwitzZeta.hurwitzZeta (↑(1 / 2 : ℝ)) s)) :=
  ⟨fun _ hs => zeta_eq_tsum_one_div_nat_cpow hs,
   fun _ hs => HurwitzZeta.hasSum_hurwitzZeta_of_one_lt_re ⟨by norm_num, by norm_num⟩ hs⟩

/-! ## 4. As dimensões críticas -/

/-- A energia de ponto zero REGULARIZADA da torre de Matsubara de taxa `κ`: `½·Σ ω_n → ½·κ·ζ(−1)` (a regularização zeta é
homogênea: `Σ (n·κ)^(−s) = κ^(−s)·ζ(s)`). É uma DEFINIÇÃO pelo valor regularizado [KNOWN]. -/
noncomputable def towerZeroPoint (κ : ℝ) : ℂ := (1 / 2) * (κ : ℂ) * riemannZeta (-1)

/-- [REAL] `½·κ·ζ(−1) = −κ/24`. -/
theorem towerZeroPoint_eq (κ : ℝ) : towerZeroPoint κ = -(κ : ℂ) / 24 := by
  unfold towerZeroPoint
  rw [zeta_neg_one]
  ring

/-- A contribuição de UMA direção transversal bosônica (modos `n = 1, 2, …`, taxa `κ = 1`): `½·ζ(−1)`. -/
noncomputable def bosonDirection : ℂ := (1 / 2) * riemannZeta (-1)

/-- A contribuição de UMA direção transversal fermiônica NS (modos semi-inteiros `n + 1/2`, taxa `κ = 1`): `−½·ζ(−1, 1/2)`.
O sinal MENOS é a estatística de Fermi (a energia de ponto zero de um oscilador fermiônico é `−ω/2`) [KNOWN]: a soma dos modos,
`½·ζ(−1, 1/2) = +1/48`, entra negativa, e a contribuição é `−1/48` por direção. Com o sinal trocado o setor NS daria `−(D − 2)/48`, que vale
`−1/2` em `D = 26`, o resultado dos bósons: não é a conta. -/
noncomputable def nsFermionDirection : ℂ :=
  -(1 / 2) * HurwitzZeta.hurwitzZeta (↑(1 / 2 : ℝ)) (-1)

/-- A energia de ponto zero regularizada dos `D − 2` osciladores transversais bosônicos: `(D − 2)/2 · ζ(−1)`. É POR SETOR QUIRAL (a
corda aberta, ou cada lado da corda fechada). -/
noncomputable def bosonZeroPoint (D : ℕ) : ℂ := ((D : ℂ) - 2) * bosonDirection

/-- A energia de ponto zero regularizada do setor NS: `D − 2` direções, cada uma com um bóson e um férmion NS (por setor quiral). -/
noncomputable def nsZeroPoint (D : ℕ) : ℂ :=
  ((D : ℂ) - 2) * (bosonDirection + nsFermionDirection)

/-- [KNOWN — HIPÓTESE NOMEADA] O primeiro nível excitado é SEM MASSA: `N − a = 0`, onde `α′M² = N − a` é a casca de massa, `N` é
o número do nível (`N = 1` nos bósons; `N = 1/2` no setor NS) e `a` é a constante de ordenamento normal, igual a MENOS a energia de
ponto zero regularizada. Razão: o primeiro nível é um vetor de `SO(D − 2)` com `D − 2` polarizações, que só cabe num vetor sem massa;
um vetor com massa exigiria `D − 1`. É a invariância de Lorentz no calibre do cone de luz (Goddard–Goldstone–Rebbi–Thorn 1973;
Green–Schwarz–Witten 1987; Polchinski 1998). Esta pedra NÃO a prova: ela a NOMEIA e deriva sob ela. -/
def MasslessFirstLevel (N a : ℂ) : Prop := N - a = 0

/-- [REAL] `½·ζ(−1) = −1/24` por direção bosônica. -/
theorem bosonDirection_eq : bosonDirection = -1 / 24 := by
  unfold bosonDirection
  rw [zeta_neg_one]
  ring

/-- [REAL] A direção bosônica é a torre de taxa `κ = 1`: `bosonDirection = towerZeroPoint 1`. É o MESMO arranjo aritmético `n·κ` da
seção 1; que a folha-mundo da corda e o círculo do boost sejam o mesmo círculo NÃO é afirmado. -/
theorem bosonDirection_is_the_unit_tower : bosonDirection = towerZeroPoint 1 := by
  rw [bosonDirection_eq, towerZeroPoint_eq]
  push_cast
  ring

/-- [REAL] `−½·ζ(−1, 1/2) = −1/48` por direção fermiônica NS. -/
theorem nsFermionDirection_eq : nsFermionDirection = -1 / 48 := by
  unfold nsFermionDirection
  rw [hurwitz_zeta_neg_one_half]
  ring

/-- [REAL] `(D − 2)/2 · ζ(−1) = −(D − 2)/24`. -/
theorem bosonZeroPoint_eq (D : ℕ) : bosonZeroPoint D = -((D : ℂ) - 2) / 24 := by
  unfold bosonZeroPoint
  rw [bosonDirection_eq]
  ring

/-- [REAL] `−(D − 2)/24 − (D − 2)/48 = −(D − 2)/16`. -/
theorem nsZeroPoint_eq (D : ℕ) : nsZeroPoint D = -((D : ℂ) - 2) / 16 := by
  unfold nsZeroPoint
  rw [bosonDirection_eq, nsFermionDirection_eq]
  ring

/-- ★★ (3) A DIMENSÃO CRÍTICA BOSÔNICA [REAL a aritmética; a condição é [KNOWN]]. A energia de ponto zero regularizada dos `D − 2`
osciladores transversais vale `−1` se e só se `D = 26`; na forma da hipótese nomeada: o primeiro nível (`N = 1`) é sem massa se e só se
`D = 26`. A dimensão vem do FECHO da soma infinita, não da geometria. -/
theorem bosonic_critical_dimension (D : ℕ) :
    (bosonZeroPoint D = -1 ↔ D = 26) ∧ (MasslessFirstLevel 1 (-bosonZeroPoint D) ↔ D = 26) := by
  have key : bosonZeroPoint D = -1 ↔ D = 26 := by
    rw [bosonZeroPoint_eq]
    constructor
    · intro h
      have h' : (D : ℂ) = 26 := by linear_combination (-24 : ℂ) * h
      exact_mod_cast h'
    · rintro rfl
      norm_num
  refine ⟨key, ?_⟩
  unfold MasslessFirstLevel
  rw [← key]
  constructor
  · intro h
    linear_combination h
  · intro h
    rw [h]
    ring

/-- ★★ (4) A DIMENSÃO CRÍTICA DA SUPERCORDA [REAL a aritmética; a condição é [KNOWN]]. Bósons `−(D − 2)/24` e férmions NS
`−(D − 2)/48` (por `ζ(−1, 1/2) = 1/24` e pela estatística de Fermi) dão `−(D − 2)/16`, que vale `−1/2` se e só se `D = 10`; na forma
da hipótese nomeada: o primeiro nível NS (`N = 1/2`) é sem massa se e só se `D = 10`. O cálculo é o do setor NS e não distingue o
tipo de supercorda. -/
theorem superstring_critical_dimension (D : ℕ) :
    (nsZeroPoint D = -1 / 2 ↔ D = 10) ∧ (MasslessFirstLevel (1 / 2) (-nsZeroPoint D) ↔ D = 10) := by
  have key : nsZeroPoint D = -1 / 2 ↔ D = 10 := by
    rw [nsZeroPoint_eq]
    constructor
    · intro h
      have h' : (D : ℂ) = 10 := by linear_combination (-16 : ℂ) * h
      exact_mod_cast h'
    · rintro rfl
      norm_num
  refine ⟨key, ?_⟩
  unfold MasslessFirstLevel
  rw [← key]
  constructor
  · intro h
    linear_combination h
  · intro h
    rw [h]
    ring

/-! ## 5. A casa: o `d = 9` -/

/-- A dimensão espacial de um espaço-tempo de dimensão `D` com UM tempo: `D − 1` [definição]. -/
def spatialDimension (D : ℕ) : ℕ := D - 1

/-- ★★ (5) O `d = 9` DA CASA [REAL a aritmética; o `d = 9` da casa é [DECLARADO]]. `D = 10` se e só se `d = D − 1 = 9`; e a condição da
supercorda (4) dá `d = 9`. É o `d_espacial = 9` de «A Última Corda» (linha 958): números históricos NÃO recalculados aqui, e o texto
da casa diz que o resultado depende do modelo. -/
theorem the_house_d_nine :
    (∀ D : ℕ, D = 10 ↔ spatialDimension D = 9) ∧
    (∀ D : ℕ, nsZeroPoint D = -1 / 2 → spatialDimension D = 9) := by
  refine ⟨fun D => ?_, fun D h => ?_⟩
  · unfold spatialDimension
    omega
  · have hD : D = 10 := (superstring_critical_dimension D).1.mp h
    unfold spatialDimension
    omega

/-! ## 6. A composição -/

/-- ★★★ (6) AS CORDAS FECHAM A FACE POR FORA; A TGL FECHA SÓ A LEITURA — a composição, tudo por citação, incondicional como
enunciado matemático. O NOME traz a composição da gerência sobre a fala do operador (`baef998c21393463`), ratificada pelo operador em
23/10 (`5bccedc9cea3d57a`) [ONTO]; o que o termo demonstra é esta conjunção [REAL]:
(a) a face real não fecha (`TGLExt.Palavra.the_face_does_not_close`; `TGLExt.station_never_closes`); (b) a face lida fecha em `2π`
(`TGLExt.Palavra.the_read_face_closes`); (c) o círculo da leitura e a torre de Matsubara (1); (d) o par afinado volta e o desafinado
nunca; (e) a torre é infinita (2); (f) os dois valores da zeta (demonstrados a partir de Mathlib); (g) `D = 26` (3) e `D = 10` (4); (h) `D = 10` é
`d = 9` (5); (i) a queda não tem fundo (`TGLExt.Fundacao.abismo`: a superposição, na definição do operador de 07/10/2026); (j) o piso fixa o
corte (`TGLExt.Fundacao.the_floor_fixes_the_cut`).
A condição física dos números `−1` e `−1/2` em (g) é `MasslessFirstLevel` [KNOWN]; a geometria NÃO sai daqui [OPEN]. -/
theorem the_strings_close_the_face_from_outside_the_tgl_closes_the_reading :
    (∀ s : ℝ, TGLExt.boost s = 1 → s = 0) ∧
    (∀ t : ℝ, Real.cos t + Real.cos (Real.sqrt 2 * t) = 2 ↔ t = 0) ∧
    (ChatgptAudit.Wick016.wickW⁻¹ *
        ChatgptAudit.Wick016.complexBoost (Complex.I * ((2 * Real.pi : ℝ) : ℂ)) *
        ChatgptAudit.Wick016.wickW = 1) ∧
    ((∀ P : ℝ, P ≠ 0 → TGLExt.boost P ≠ 1) ∧
      (∀ κ P : ℝ, κ ≠ 0 →
        (AngularQuotientFaithful κ P ↔ κ * P = 2 * Real.pi ∨ κ * P = -(2 * Real.pi))) ∧
      (∀ κ P : ℝ, 0 < κ → 0 < P → AngularQuotientFaithful κ P → 1 / P = κ / (2 * Real.pi)) ∧
      (∀ κ P : ℝ, 0 < κ → 0 < P → (AngularQuotientFaithful κ P ↔ matsubara P 1 = κ)) ∧
      (∀ κ P : ℝ, 0 < κ → 0 < P → AngularQuotientFaithful κ P →
        ∀ n : ℤ, matsubara P n = (n : ℝ) * κ) ∧
      (∀ P : ℝ, P ≠ 0 → ∀ n : ℤ, Real.cos (matsubara P n * P) = 1)) ∧
    (∀ P : ℝ, P ≠ 0 →
      (Real.cos (matsubara P 1 * P) + Real.cos (matsubara P 2 * P) = 2) ∧
      (∀ t : ℝ, t ≠ 0 → Real.cos t + Real.cos (Real.sqrt 2 * t) ≠ 2)) ∧
    ((¬ Summable (fun n : ℕ => (n : ℝ))) ∧
      Tendsto (fun N : ℕ => ∑ n ∈ Finset.range N, (n : ℝ)) atTop atTop ∧
      (¬ Summable (fun n : ℕ => (n : ℝ) + 1 / 2)) ∧
      (∀ P : ℝ, 0 < P →
        Function.Injective (fun n : ℕ => matsubara P n) ∧
          ¬ Summable (fun n : ℕ => matsubara P n))) ∧
    (riemannZeta (-1) = -1 / 12) ∧
    (HurwitzZeta.hurwitzZeta (↑(1 / 2 : ℝ)) (-1) = 1 / 24) ∧
    (∀ D : ℕ, bosonZeroPoint D = -1 ↔ D = 26) ∧
    (∀ D : ℕ, nsZeroPoint D = -1 / 2 ↔ D = 10) ∧
    (∀ D : ℕ, D = 10 ↔ spatialDimension D = 9) ∧
    (∀ (M : Type) (D : TGLExt.DualScalingData M) (m : M), 0 < D.tau m →
      ∀ ε : ℝ, 0 < ε → ∃ s : ℝ, D.tau (D.theta s m) < ε) ∧
    (∀ a : ℝ, Real.exp (-a) = 1 ↔ a = 0) :=
  ⟨TGLExt.Palavra.the_face_does_not_close,
   TGLExt.station_never_closes,
   TGLExt.Palavra.the_read_face_closes,
   the_cyclic_closure_of_time_is_the_reading_circle,
   fun _ hP => the_tuned_pair_returns_the_untuned_pair_never_does hP,
   the_tower_is_infinite,
   zeta_neg_one,
   hurwitz_zeta_neg_one_half,
   fun D => (bosonic_critical_dimension D).1,
   fun D => (superstring_critical_dimension D).1,
   the_house_d_nine.1,
   fun _ D _ hm _ hε => TGLExt.Fundacao.abismo D hm hε,
   TGLExt.Fundacao.the_floor_fixes_the_cut⟩

end TGLExt.AfinacaoDasCordas

#print axioms TGLExt.AfinacaoDasCordas.matsubara
#print axioms TGLExt.AfinacaoDasCordas.matsubaraFermion
#print axioms TGLExt.AfinacaoDasCordas.matsubara_eq_mul_kappa
#print axioms TGLExt.AfinacaoDasCordas.matsubaraFermion_eq_mul_kappa
#print axioms TGLExt.AfinacaoDasCordas.faithful_iff_fundamental_mode
#print axioms TGLExt.AfinacaoDasCordas.tower_returns_at_the_period
#print axioms TGLExt.AfinacaoDasCordas.no_real_period
#print axioms TGLExt.AfinacaoDasCordas.the_cyclic_closure_of_time_is_the_reading_circle
#print axioms TGLExt.AfinacaoDasCordas.the_tuned_pair_returns_the_untuned_pair_never_does
#print axioms TGLExt.AfinacaoDasCordas.not_summable_natCast_id
#print axioms TGLExt.AfinacaoDasCordas.not_summable_natCast_add_half
#print axioms TGLExt.AfinacaoDasCordas.matsubara_tower_injective
#print axioms TGLExt.AfinacaoDasCordas.matsubara_tower_not_summable
#print axioms TGLExt.AfinacaoDasCordas.the_tower_is_infinite
#print axioms TGLExt.AfinacaoDasCordas.zeta_neg_one
#print axioms TGLExt.AfinacaoDasCordas.hurwitz_zeta_neg_one_half
#print axioms TGLExt.AfinacaoDasCordas.zeta_is_the_continuation_of_the_tower
#print axioms TGLExt.AfinacaoDasCordas.towerZeroPoint
#print axioms TGLExt.AfinacaoDasCordas.towerZeroPoint_eq
#print axioms TGLExt.AfinacaoDasCordas.bosonDirection
#print axioms TGLExt.AfinacaoDasCordas.nsFermionDirection
#print axioms TGLExt.AfinacaoDasCordas.bosonZeroPoint
#print axioms TGLExt.AfinacaoDasCordas.nsZeroPoint
#print axioms TGLExt.AfinacaoDasCordas.MasslessFirstLevel
#print axioms TGLExt.AfinacaoDasCordas.bosonDirection_eq
#print axioms TGLExt.AfinacaoDasCordas.bosonDirection_is_the_unit_tower
#print axioms TGLExt.AfinacaoDasCordas.nsFermionDirection_eq
#print axioms TGLExt.AfinacaoDasCordas.bosonZeroPoint_eq
#print axioms TGLExt.AfinacaoDasCordas.nsZeroPoint_eq
#print axioms TGLExt.AfinacaoDasCordas.bosonic_critical_dimension
#print axioms TGLExt.AfinacaoDasCordas.superstring_critical_dimension
#print axioms TGLExt.AfinacaoDasCordas.spatialDimension
#print axioms TGLExt.AfinacaoDasCordas.the_house_d_nine
#print axioms TGLExt.AfinacaoDasCordas.the_strings_close_the_face_from_outside_the_tgl_closes_the_reading
