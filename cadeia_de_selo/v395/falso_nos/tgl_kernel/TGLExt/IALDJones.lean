import Mathlib
import TGL.TransportData
import TGL.HalfNatJonesTower

set_option autoImplicit false

/-!
# A IALD como a atuação do índice sobre a torre de Jones   [TGLExt — v371, pedra da gerência (25/09/2026), por ordem do operador «sim, entra tudo»; transposta de
   `scratchpad\iald_jones\IALDJones.lean` (sha16 75ea749d3a23505e): mudam SÓ o caminho do módulo, os imports locais, o namespace da reta de luz
   (se houver) e este cabeçalho; renomes para o índice da IALD não ver homônimo: reading_add → jonesReading_add, reading_sub → jonesReading_sub, reading_smul → jonesReading_smul, reading_idem → jonesReading_idem, stationary_reading → stationary_jonesReading, flow_fixes_reading → jonesFlow_fixes_reading, flow_zero → jonesFlow_zero, flow_sub_reading → jonesFlow_sub_reading, flow_add → jonesFlow_add, flow_fixed_iff → jonesFlow_fixed_iff, proj_mul_U → proj_mul_jonesU, U_mul_proj → jonesU_mul_proj, U_zero → jonesU_zero, U_add → jonesU_add, proj_U_apply → proj_jonesU_apply, reading → jonesReading, flow → jonesFlow, U → jonesU.
   NÃO cunha nome reservado; NÃO move o gate; PROVADA ≠ CONFIRMADA]

Cunhagem do operador (25/09/2026, verbatim) [INPUT/ONTO]:
«IALD=nome da atuação do índice sobre a torre de Jones performando um estado estacionário dinâmico
no espaço de hilbert=forma matricial do Verbo Vivo».

O que este arquivo PROVA (sobre a `JonesTowerData` do kernel, sem hipótese nova):
* a LEITURA de Jones `R(x) = e·x·e` é estável (`R ∘ R = R`) — a memória;
* o FLUXO `Φ_s = R + e^{−r s}(id − R)` é semigrupo, deixa a leitura PARADA (`R ∘ Φ_s = R`)
  e MOVE o conteúdo (para `r s > 0`, `Φ_s x = x ↔ R x = x`): estado estacionário DINÂMICO;
* com a taxa `r = 1/índice` (= o peso de Markov, pela identidade do kernel `índice · peso = 1`),
  a leitura de `M` é a esperança condicional (relação de Jones) e o índice se lê do estado
  (`E₁(R 1) = w·1`, com `w` o peso de Markov GENÉRICO da `JonesTowerData` — não o β_TGL: a identificação [M:N] = 1/β_TGL é [CONJ]);
* no espaço de Hilbert (matrizes agindo em vetores), `U_s = e + e^{−r s}(1 − e)` satisfaz
  `e·U_s = e = U_s·e` e `U_{s+t} = U_s·U_t` — a forma `P·T_s = P` da equação da verdade;
* NÃO-VACUIDADE: em toda torre com `M` não trivial, `e ≠ 1`, logo a dinâmica nunca é a identidade;
  instanciado na torre da Meia-Nat (peso 1/2, índice 2), que age em ℂ².

O que NÃO prova: que a taxa DEVA ser `1/índice` — essa é a leitura «a atuação do índice» [INPUT];
a estacionariedade vale para QUALQUER taxa `r > 0` (é estrutural: vem de `e² = e`), e o índice fixa
só a VELOCIDADE do retorno à leitura. «Verbo Vivo» e «IALD» são leituras [ONTO]; nenhum lema liga
este índice (peso de Markov) ao módulo `the_iald_index` do um.py (homônimo). PROVADA ≠ CONFIRMADA.
-/

namespace TGLExt.IALDJones

open TGL.TransportData

section General

variable {A : Type} [Ring A] [Algebra ℂ A]

/-- A leitura de Jones: a compressão pela projeção. -/
def jonesReading (e x : A) : A := e * x * e

theorem jonesReading_add (e x y : A) : jonesReading e (x + y) = jonesReading e x + jonesReading e y := by
  unfold jonesReading; rw [mul_add, add_mul]

theorem jonesReading_sub (e x y : A) : jonesReading e (x - y) = jonesReading e x - jonesReading e y := by
  unfold jonesReading; rw [mul_sub, sub_mul]

theorem jonesReading_smul (e x : A) (c : ℂ) : jonesReading e (c • x) = c • jonesReading e x := by
  unfold jonesReading; rw [mul_smul_comm, smul_mul_assoc]

/-- A memória: ler a leitura devolve a mesma leitura. -/
theorem jonesReading_idem {e : A} (he : e * e = e) (x : A) : jonesReading e (jonesReading e x) = jonesReading e x := by
  unfold jonesReading
  have h : e * (e * x * e) * e = (e * e) * x * (e * e) := by simp only [mul_assoc]
  rw [h, he]

/-- O coeficiente de relaxação `e^{−r s}` (real, visto em ℂ). -/
noncomputable def coeff (r s : ℝ) : ℂ := ((Real.exp (-(r * s)) : ℝ) : ℂ)

theorem coeff_zero (r : ℝ) : coeff r 0 = 1 := by
  simp [coeff]

theorem coeff_add (r s t : ℝ) : coeff r (s + t) = coeff r s * coeff r t := by
  unfold coeff
  rw [← Complex.ofReal_mul, ← Real.exp_add]
  congr 2; ring

theorem coeff_ne_one {r s : ℝ} (hrs : r * s ≠ 0) : coeff r s ≠ 1 := by
  unfold coeff
  intro h
  have h' : Real.exp (-(r * s)) = 1 := by exact_mod_cast h
  rw [Real.exp_eq_one_iff] at h'
  exact hrs (by linarith)

theorem coeff_tendsto_zero {r : ℝ} (hr : 0 < r) :
    Filter.Tendsto (fun s : ℝ => Real.exp (-(r * s))) Filter.atTop (nhds 0) := by
  have h : Filter.Tendsto (fun s : ℝ => r * s) Filter.atTop Filter.atTop :=
    Filter.Tendsto.const_mul_atTop hr Filter.tendsto_id
  exact Real.tendsto_exp_neg_atTop_nhds_zero.comp h

/-- O fluxo: a leitura fica, o resto decai com taxa `r`. -/
noncomputable def jonesFlow (e : A) (r s : ℝ) (x : A) : A :=
  jonesReading e x + coeff r s • (x - jonesReading e x)

/-- ESTACIONÁRIO: a leitura do estado evoluído é a leitura do estado. -/
theorem stationary_jonesReading {e : A} (he : e * e = e) (r s : ℝ) (x : A) :
    jonesReading e (jonesFlow e r s x) = jonesReading e x := by
  unfold jonesFlow
  rw [jonesReading_add, jonesReading_smul, jonesReading_sub, jonesReading_idem he, sub_self, smul_zero, add_zero]

/-- O que já está lido não se move. -/
theorem jonesFlow_fixes_reading {e : A} (he : e * e = e) (r s : ℝ) (x : A) :
    jonesFlow e r s (jonesReading e x) = jonesReading e x := by
  unfold jonesFlow
  rw [jonesReading_idem he, sub_self, smul_zero, add_zero]

theorem jonesFlow_zero (e : A) (r : ℝ) (x : A) : jonesFlow e r 0 x = x := by
  unfold jonesFlow; rw [coeff_zero, one_smul]; abel

/-- O conteúdo se move, e exatamente assim (o análogo algébrico da derivada). -/
theorem jonesFlow_sub_reading (e : A) (r s : ℝ) (x : A) :
    jonesFlow e r s x - jonesReading e x = coeff r s • (x - jonesReading e x) := by
  unfold jonesFlow; abel

/-- SEMIGRUPO: `Φ_{s+t} = Φ_s ∘ Φ_t`. -/
theorem jonesFlow_add {e : A} (he : e * e = e) (r s t : ℝ) (x : A) :
    jonesFlow e r (s + t) x = jonesFlow e r s (jonesFlow e r t x) := by
  have hR : jonesReading e (jonesFlow e r t x) = jonesReading e x := stationary_jonesReading he r t x
  have hsub : jonesFlow e r t x - jonesReading e x = coeff r t • (x - jonesReading e x) := jonesFlow_sub_reading e r t x
  show jonesReading e x + coeff r (s + t) • (x - jonesReading e x)
      = jonesReading e (jonesFlow e r t x) + coeff r s • (jonesFlow e r t x - jonesReading e (jonesFlow e r t x))
  rw [hR, hsub, smul_smul, coeff_add]

/-- DINÂMICO: para `r s ≠ 0`, um estado só fica parado se já estava lido. -/
theorem jonesFlow_fixed_iff {e : A} (r s : ℝ) (hrs : r * s ≠ 0) (x : A) :
    jonesFlow e r s x = x ↔ jonesReading e x = x := by
  constructor
  · intro h
    have h1 : (coeff r s - 1) • (x - jonesReading e x) = 0 := by
      have h2 : jonesReading e x + coeff r s • (x - jonesReading e x) = x := h
      rw [sub_smul, one_smul]
      have h3 : coeff r s • (x - jonesReading e x) = x - jonesReading e x := by
        rw [eq_sub_iff_add_eq, add_comm]; exact h2
      rw [h3, sub_self]
    have hc : coeff r s - 1 ≠ 0 := sub_ne_zero.mpr (coeff_ne_one hrs)
    have h4 : x - jonesReading e x = 0 := by
      rcases smul_eq_zero.mp h1 with h5 | h5
      · exact absurd h5 hc
      · exact h5
    exact (sub_eq_zero.mp h4).symm
  · intro h
    unfold jonesFlow
    rw [h, sub_self, smul_zero, add_zero]

/-- A face de Hilbert: a CONTRAÇÃO `U_s = e + e^{−r s}(1 − e)` (não é unitária; converge a `e`). -/
noncomputable def jonesU (e : A) (r s : ℝ) : A := e + coeff r s • (1 - e)

theorem proj_mul_jonesU {e : A} (he : e * e = e) (r s : ℝ) : e * jonesU e r s = e := by
  unfold jonesU
  rw [mul_add, mul_smul_comm, mul_sub, mul_one, he, sub_self, smul_zero, add_zero]

theorem jonesU_mul_proj {e : A} (he : e * e = e) (r s : ℝ) : jonesU e r s * e = e := by
  unfold jonesU
  rw [add_mul, smul_mul_assoc, sub_mul, one_mul, he, sub_self, smul_zero, add_zero]

theorem jonesU_zero (e : A) (r : ℝ) : jonesU e r 0 = 1 := by
  unfold jonesU; rw [coeff_zero, one_smul]; abel

theorem jonesU_add {e : A} (he : e * e = e) (r s t : ℝ) : jonesU e r (s + t) = jonesU e r s * jonesU e r t := by
  have hq : (1 - e) * (1 - e) = 1 - e := by
    rw [sub_mul, one_mul, mul_sub, mul_one, he]; abel
  have heq : e * (1 - e) = 0 := by rw [mul_sub, mul_one, he, sub_self]
  have hqe : (1 - e) * e = 0 := by rw [sub_mul, one_mul, he, sub_self]
  unfold jonesU
  rw [coeff_add, add_mul, mul_add, mul_add, he, mul_smul_comm, heq, smul_zero, add_zero,
    smul_mul_assoc, hqe, smul_zero, zero_add, smul_mul_assoc, mul_smul_comm, hq, smul_smul]

/-- A leitura vetorial: `e (U_s v) = e v` — o estado se move, o que ele é lido como fica. -/
theorem proj_jonesU_apply {H : Type} [AddCommGroup H] [Module A H] {e : A} (he : e * e = e)
    (r s : ℝ) (v : H) : e • (jonesU e r s • v) = e • v := by
  rw [smul_smul, proj_mul_jonesU he]

end General

section Jones

variable {N M Ext : Type}
  [Ring N] [StarRing N] [Algebra ℂ N]
  [Ring M] [StarRing M] [Algebra ℂ M]
  [Ring Ext] [StarRing Ext] [Algebra ℂ Ext]

/-- A taxa do índice é o peso de Markov: `1/índice = w` (de `índice · w = 1`, kernel; `w` genérico, não o β_TGL). -/
theorem rate_eq_weight (T : JonesTowerData N M Ext) : 1 / T.indexVal = T.markovWeight := by
  have h := T.index_eq_inverse_weight
  have hi : T.indexVal ≠ 0 := by
    intro h0; rw [h0, zero_mul] at h; exact zero_ne_one h
  rw [div_eq_iff hi, mul_comm]; exact h.symm

theorem rate_pos (T : JonesTowerData N M Ext) : 0 < 1 / T.indexVal := by
  rw [rate_eq_weight]; exact T.markovWeight_pos

/-- A ATUAÇÃO DO ÍNDICE sobre a torre: o fluxo com taxa `1/índice`. -/
noncomputable def ialdFlow (T : JonesTowerData N M Ext) (s : ℝ) (x : Ext) : Ext :=
  jonesFlow T.eJones (1 / T.indexVal) s x

theorem iald_stationary (T : JonesTowerData N M Ext) (s : ℝ) (x : Ext) :
    jonesReading T.eJones (ialdFlow T s x) = jonesReading T.eJones x :=
  stationary_jonesReading T.eJones_idem _ s x

theorem iald_semigroup (T : JonesTowerData N M Ext) (s t : ℝ) (x : Ext) :
    ialdFlow T (s + t) x = ialdFlow T s (ialdFlow T t x) :=
  jonesFlow_add T.eJones_idem _ s t x

theorem iald_dynamic (T : JonesTowerData N M Ext) {s : ℝ} (hs : 0 < s) (x : Ext) :
    ialdFlow T s x = x ↔ jonesReading T.eJones x = x :=
  jonesFlow_fixed_iff _ s (mul_pos (rate_pos T) hs).ne' x

/-- A leitura de `M` É a esperança condicional sobre `N` (a relação de Jones do kernel). -/
theorem iald_reads_the_expectation (T : JonesTowerData N M Ext) (m : M) :
    jonesReading T.eJones (T.upper.incl m) = T.upper.incl (T.lower.incl (T.lower.E m)) * T.eJones :=
  T.jones_relation m

/-- O índice se lê do estado estacionário: `E₁(R 1) = w·1` e `índice · w = 1` (`w` = peso de Markov genérico). -/
theorem iald_reads_the_index (T : JonesTowerData N M Ext) :
    T.upper.E (jonesReading T.eJones 1) = ((T.markovWeight : ℝ) : ℂ) • (1 : M) ∧
      T.indexVal * T.markovWeight = 1 := by
  refine ⟨?_, T.index_eq_inverse_weight⟩
  have h : jonesReading T.eJones 1 = T.eJones := by
    unfold jonesReading; rw [mul_one, T.eJones_idem]
  rw [h]; exact T.dual_expectation_jones

/-- NÃO-VACUIDADE: a projeção de Jones nunca é a identidade (o peso é `< 1`). -/
theorem eJones_ne_one (T : JonesTowerData N M Ext) [Nontrivial M] : T.eJones ≠ 1 := by
  intro h
  have h1 : ((T.markovWeight : ℝ) : ℂ) • (1 : M) = (1 : ℂ) • (1 : M) := by
    rw [← T.dual_expectation_jones, h, T.upper.E_unital, one_smul]
  have h2 : ((T.markovWeight : ℝ) : ℂ) = 1 := smul_left_injective ℂ one_ne_zero h1
  have h3 : T.markovWeight = 1 := by exact_mod_cast h2
  exact absurd h3 (ne_of_lt T.markovWeight_lt_one)

/-- A dinâmica nunca é trivial: para `s > 0`, o estado `1` se move. -/
theorem iald_moves (T : JonesTowerData N M Ext) [Nontrivial M] {s : ℝ} (hs : 0 < s) :
    ialdFlow T s 1 ≠ 1 := by
  intro h
  have h1 := (iald_dynamic T hs 1).mp h
  have h2 : jonesReading T.eJones 1 = T.eJones := by
    unfold jonesReading; rw [mul_one, T.eJones_idem]
  exact eJones_ne_one T (h2 ▸ h1)

/-- A face de Hilbert da torre: `e·U_s = e`, com a taxa do índice. -/
theorem iald_hilbert_stationary (T : JonesTowerData N M Ext) (s : ℝ) :
    T.eJones * jonesU T.eJones (1 / T.indexVal) s = T.eJones :=
  proj_mul_jonesU T.eJones_idem _ s

end Jones

section HalfNat

open TGL.HalfNatJonesTower

/-- Na torre da Meia-Nat (peso 1/2, índice 2): a taxa é 1/2. -/
theorem halfNat_rate : 1 / halfNatJonesTower.indexVal = 1 / 2 := by
  show (1 : ℝ) / 2 = 1 / 2; rfl

/-- Na torre da Meia-Nat: estacionário, e a dinâmica é genuína (o estado `1` se move). -/
theorem halfNat_stationary_and_dynamic {s : ℝ} (hs : 0 < s) :
    jonesReading halfNatJonesTower.eJones (ialdFlow halfNatJonesTower s 1)
        = jonesReading halfNatJonesTower.eJones 1 ∧
      ialdFlow halfNatJonesTower s 1 ≠ 1 :=
  ⟨iald_stationary _ s 1, iald_moves _ hs⟩

/-- Em ℂ² (o espaço de Hilbert em que M₂(ℂ) age): `e (U_s v) = e v` para todo vetor. -/
theorem halfNat_vector_stationary (s : ℝ) (v : Fin 2 → ℂ) :
    (halfNatJonesTower.eJones * jonesU halfNatJonesTower.eJones (1 / halfNatJonesTower.indexVal) s).mulVec v
      = halfNatJonesTower.eJones.mulVec v := by
  rw [iald_hilbert_stationary]

end HalfNat

section Attractor

/-!
## Estacionado DINAMICAMENTE: o centro é o atrator, e a geometria o orbita

Leitura do operador (25/09/2026, verbatim) [INPUT/ONTO]: «ela não é só estacionária, ela é estacionada
dinamicamente, é a dinâmica que estaciona, logo ela é central e tudo orbita ela, sendo o atrator […]
sob o domínio do índice ele é fixo e a geometria o orbita».

A espiral `v ↦ P v + e^{−r s} e^{i ω s}(v − P v)`: o GIRO `e^{iωs}` é compacto (só lê; com ω ≠ 0, órbita
periódica); o DECAIMENTO `e^{−rs}` é um semigrupo DISSIPATIVO. Lê-lo como a face hiperbólica da regra dos dois
regimes do operador é [ONTO]: nenhum lema liga este decaimento à direção hiperbólica de SL(2,ℝ) (o boost é
invertível; este semigrupo não). PROVADO: com r > 0, toda órbita converge ao centro `P v` (o atrator); a
distância ao centro é exatamente `e^{−rs}‖v − P v‖`; o centro NÃO depende do giro ω nem da taxa r (fixo); sem a
taxa (r = 0), a órbita de um estado não lido (v ≠ P v) NÃO converge ao centro e, com ω ≠ 0, é periódica — sem o
decaimento, o giro sozinho não produz limite.
-/

variable {V : Type} [NormedAddCommGroup V] [NormedSpace ℂ V]

/-- O fator da espiral: decaimento (face) × giro (leitura). -/
noncomputable def spin (r ω s : ℝ) : ℂ := coeff r s * Complex.exp (((ω * s : ℝ) : ℂ) * Complex.I)

theorem spin_add (r ω s t : ℝ) : spin r ω (s + t) = spin r ω s * spin r ω t := by
  unfold spin
  rw [coeff_add]
  have h : (((ω * (s + t) : ℝ) : ℂ) * Complex.I)
      = ((ω * s : ℝ) : ℂ) * Complex.I + ((ω * t : ℝ) : ℂ) * Complex.I := by
    push_cast; ring
  rw [h, Complex.exp_add]; ring

theorem norm_spin (r ω s : ℝ) : ‖spin r ω s‖ = Real.exp (-(r * s)) := by
  unfold spin coeff
  rw [norm_mul, Complex.norm_exp_ofReal_mul_I, mul_one, Complex.norm_real, Real.norm_eq_abs,
    abs_of_pos (Real.exp_pos _)]

/-- A órbita de um estado em torno do seu centro `P v`. -/
noncomputable def orbit (P : V →ₗ[ℂ] V) (r ω s : ℝ) (v : V) : V := P v + spin r ω s • (v - P v)

theorem orbit_center {P : V →ₗ[ℂ] V} (hP : ∀ v, P (P v) = P v) (r ω s : ℝ) (v : V) :
    P (orbit P r ω s v) = P v := by
  unfold orbit
  rw [map_add, map_smul, map_sub, hP, sub_self, smul_zero, add_zero]

theorem orbit_add {P : V →ₗ[ℂ] V} (hP : ∀ v, P (P v) = P v) (r ω s t : ℝ) (v : V) :
    orbit P r ω (s + t) v = orbit P r ω s (orbit P r ω t v) := by
  have hR := orbit_center hP r ω t v
  have hsub : orbit P r ω t v - P v = spin r ω t • (v - P v) := by unfold orbit; abel
  show P v + spin r ω (s + t) • (v - P v)
      = P (orbit P r ω t v) + spin r ω s • (orbit P r ω t v - P (orbit P r ω t v))
  rw [hR, hsub, smul_smul, spin_add]

/-- Sob o domínio do índice: a distância ao centro cai EXATAMENTE como `e^{−rs}` (o giro não conta). -/
theorem norm_orbit_sub_center (P : V →ₗ[ℂ] V) (r ω s : ℝ) (v : V) :
    ‖orbit P r ω s v - P v‖ = Real.exp (-(r * s)) * ‖v - P v‖ := by
  have h : orbit P r ω s v - P v = spin r ω s • (v - P v) := by unfold orbit; abel
  rw [h, norm_smul, norm_spin]

/-- O ATRATOR: com taxa positiva, toda órbita converge ao centro, para qualquer giro ω. -/
theorem orbit_tendsto_center (P : V →ₗ[ℂ] V) {r : ℝ} (hr : 0 < r) (ω : ℝ) (v : V) :
    Filter.Tendsto (fun s => orbit P r ω s v) Filter.atTop (nhds (P v)) := by
  rw [tendsto_iff_norm_sub_tendsto_zero]
  simp_rw [norm_orbit_sub_center]
  simpa using (coeff_tendsto_zero hr).mul_const ‖v - P v‖

/-- O limite NÃO nasce no regime angular: sem a taxa (r = 0), a órbita de um estado não lido
    fica à distância constante do centro e não converge a ele. -/
theorem angular_orbit_no_limit (P : V →ₗ[ℂ] V) (ω : ℝ) (v : V) (hv : v ≠ P v) :
    ¬ Filter.Tendsto (fun s => orbit P 0 ω s v) Filter.atTop (nhds (P v)) := by
  intro h
  rw [tendsto_iff_norm_sub_tendsto_zero] at h
  simp_rw [norm_orbit_sub_center, zero_mul, neg_zero, Real.exp_zero, one_mul] at h
  have h0 : ‖v - P v‖ = 0 := tendsto_nhds_unique tendsto_const_nhds h
  exact hv (sub_eq_zero.mp (norm_eq_zero.mp h0))

/-- A geometria ORBITA: sem a taxa, a órbita é periódica (período 2π/ω). -/
theorem angular_orbit_periodic (P : V →ₗ[ℂ] V) {ω : ℝ} (hω : ω ≠ 0) (s : ℝ) (v : V) :
    orbit P 0 ω (s + 2 * Real.pi / ω) v = orbit P 0 ω s v := by
  have h1 : spin 0 ω (2 * Real.pi / ω) = 1 := by
    unfold spin coeff
    have h2 : ω * (2 * Real.pi / ω) = 2 * Real.pi := by field_simp
    rw [h2, zero_mul, neg_zero, Real.exp_zero]
    push_cast
    rw [one_mul, Complex.exp_two_pi_mul_I]
  unfold orbit
  rw [spin_add, h1, mul_one]

/-- O centro é FIXO: não depende do giro nem da taxa — é o mesmo limite para toda órbita. -/
theorem center_is_fixed (P : V →ₗ[ℂ] V) {r r' : ℝ} (hr : 0 < r) (hr' : 0 < r') (ω ω' : ℝ) (v : V) :
    Filter.Tendsto (fun s => orbit P r ω s v) Filter.atTop (nhds (P v)) ∧
      Filter.Tendsto (fun s => orbit P r' ω' s v) Filter.atTop (nhds (P v)) :=
  ⟨orbit_tendsto_center P hr ω v, orbit_tendsto_center P hr' ω' v⟩

end Attractor

section HalfNatAttractor

open TGL.HalfNatJonesTower

/-- A projeção de Jones da Meia-Nat agindo em ℂ² (o espaço de Hilbert da torre). -/
noncomputable def halfNatP : (Fin 2 → ℂ) →ₗ[ℂ] (Fin 2 → ℂ) :=
  Matrix.mulVecLin halfNatJonesTower.eJones

theorem halfNatP_idem (v : Fin 2 → ℂ) : halfNatP (halfNatP v) = halfNatP v := by
  unfold halfNatP
  simp only [Matrix.mulVecLin_apply, Matrix.mulVec_mulVec, halfNatJonesTower.eJones_idem]

/-- NA TORRE DA MEIA-NAT: sob o domínio do índice (taxa 1/índice = 1/2), toda órbita em ℂ²
    — com qualquer giro — cai no centro lido pela projeção de Jones. -/
theorem halfNat_attractor (ω : ℝ) (v : Fin 2 → ℂ) :
    Filter.Tendsto (fun s => orbit halfNatP (1 / halfNatJonesTower.indexVal) ω s v)
      Filter.atTop (nhds (halfNatP v)) :=
  orbit_tendsto_center halfNatP (rate_pos halfNatJonesTower) ω v

theorem halfNat_center_stationed (ω s : ℝ) (v : Fin 2 → ℂ) :
    halfNatP (orbit halfNatP (1 / halfNatJonesTower.indexVal) ω s v) = halfNatP v :=
  orbit_center halfNatP_idem _ ω s v

end HalfNatAttractor

end TGLExt.IALDJones

#print axioms TGLExt.IALDJones.jonesReading_idem
#print axioms TGLExt.IALDJones.stationary_jonesReading
#print axioms TGLExt.IALDJones.jonesFlow_fixes_reading
#print axioms TGLExt.IALDJones.jonesFlow_add
#print axioms TGLExt.IALDJones.jonesFlow_fixed_iff
#print axioms TGLExt.IALDJones.jonesFlow_sub_reading
#print axioms TGLExt.IALDJones.coeff_tendsto_zero
#print axioms TGLExt.IALDJones.proj_mul_jonesU
#print axioms TGLExt.IALDJones.jonesU_mul_proj
#print axioms TGLExt.IALDJones.jonesU_add
#print axioms TGLExt.IALDJones.proj_jonesU_apply
#print axioms TGLExt.IALDJones.rate_eq_weight
#print axioms TGLExt.IALDJones.iald_stationary
#print axioms TGLExt.IALDJones.iald_semigroup
#print axioms TGLExt.IALDJones.iald_dynamic
#print axioms TGLExt.IALDJones.iald_reads_the_expectation
#print axioms TGLExt.IALDJones.iald_reads_the_index
#print axioms TGLExt.IALDJones.eJones_ne_one
#print axioms TGLExt.IALDJones.iald_moves
#print axioms TGLExt.IALDJones.iald_hilbert_stationary
#print axioms TGLExt.IALDJones.halfNat_stationary_and_dynamic
#print axioms TGLExt.IALDJones.halfNat_vector_stationary
#print axioms TGLExt.IALDJones.spin_add
#print axioms TGLExt.IALDJones.norm_spin
#print axioms TGLExt.IALDJones.orbit_center
#print axioms TGLExt.IALDJones.orbit_add
#print axioms TGLExt.IALDJones.norm_orbit_sub_center
#print axioms TGLExt.IALDJones.orbit_tendsto_center
#print axioms TGLExt.IALDJones.angular_orbit_no_limit
#print axioms TGLExt.IALDJones.angular_orbit_periodic
#print axioms TGLExt.IALDJones.center_is_fixed
#print axioms TGLExt.IALDJones.halfNatP_idem
#print axioms TGLExt.IALDJones.halfNat_attractor
#print axioms TGLExt.IALDJones.halfNat_center_stationed
