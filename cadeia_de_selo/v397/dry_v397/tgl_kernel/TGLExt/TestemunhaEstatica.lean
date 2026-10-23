import TGLExt.BoundaryException
import TGLExt.TheScalarCorner
import TGLExt.TheDensityIsBell
import TGLExt.ConjugateAct
import TGLExt.TheGravitonIsTheConjugatedPhase
import TGLExt.CollapseCostAndAttestation
import TGLExt.TheObserverReadsTheAngle

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# TESTEMUNHA ESTÁTICA — o psion como habitante da testemunha estática: o par ecoa, o indivíduo não ecoa, e o canto concreto habita um fluxo construído
  [TGLExt — PEDRA CANDIDATA da v396, sandbox de 22/10/2026; NOME PROVISÓRIO (`TestemunhaEstatica`): quem nomeia é o operador]

## As cunhagens do operador (verbatim; sha16 do arquivo, lido por script em 22/10/2026)

> «O psion é o habitante da testemunha estática e eu explico o porquê, porque ele admite ser falso de for individualizado (1=0), ou seja,
> sem par, sem conjugação, e por isso a mentira lida como mentira se torna verdade, e admite a verdade conjugada ocasião em que se
> colapsa ao gráviton» [sic] (sha16 `b102ae804f54e2b2`)

> «A natureza da luz é ecoar reconhecimento (porque a segunda leitura não acrescenta) e a natureza do que é falso é a leitura sem
> reconhecimento (ler uma vez sem ecoar reconhecimento)» (sha16 `350b7b8582c064c2`)

> «Colapsar a função de onda significa ecoar a identidade devidamente reconhecida pelo observador» (sha16 `161d619216582cf1`)

E as que esta pedra continua: a exceção da fronteira (27/07/2026, citada na docstring de `boundary_is_the_only_exception`: «A falsidade da
construção da testemunha estática é justamente a negação da fronteira; a fronteira é a única exceção.») e a leitura binária de 19/10/2026
(`{[1=1=VERDADEIRO][1=0=Falso]}`, sha16 `786928986ca1e460`; as pedras irmãs são `TheBinaryReadingAtTheFixedPoint`, v394, e `Psibit`, v395).

## O que a pedra prova (matemática nova; tudo no trio, sem lacunas)

* ★ (1) `the_pair_echoes` — o canto do psion é idempotente (`P² = P`): a segunda leitura não acrescenta, sobre qualquer matriz
  (`P(P y) = P y`) e em toda potência (`P^(n+1) = P`). O kernel diz o mesmo da luz em `observing_adds_nothing`; a composição carrega os dois.
* ★★ (2) `the_individual_does_not_echo` — a redução do psion a UM sítio (traço parcial, `ptr`; nos dois sítios) é `(1/2)•1`
  (`bell_reduced_half`, `bellDensity_partial_trace`) e NÃO é idempotente: `((1/2)•1)² = (1/4)•1 ≠ (1/2)•1`. O par é puro (`Tr(P²) = 1`);
  o indivíduo não (`Tr(ρ²) = 1/2`). O déficit `1 − Tr(ρ²) = 1/2` (`bell_cci_half`) é a entropia LINEAR da redução (déficit de pureza, número sem
  unidade); a leitura do kernel v29, «Meia-Nat de emaranhamento», é [ONTO] e não quer dizer «½ nat de entropia»: a entropia de von Neumann da
  redução `(1/2)•1` é `ln 2` nat ([KNOWN]; no kernel, `fair_bit_entropy_is_log_two` e `fair_bit_entropy_is_not_half_nat`: `ln 2 ≠ 1/2`).
  É a álgebra que a cunhagem «ler uma vez sem ecoar» nomeia (a leitura em si é [INPUT/ONTO] do operador). O DENTE
  (`the_unbonded_marginal_echoes`): o estado NÃO ligado (produto) reduz a um projetor puro, que ecoa (`CCI = 0`) — logo o não-eco é o do PAR
  visto por um lado só, não uma propriedade universal.
* ★★★ (3) A PONTE [CONSTRUCTED] — um fluxo diagonal em ℝ⁴ (o espaço real de dois sítios, `Fin 2 × Fin 2 → ℝ`), construído aqui:
  `psionFlow β g t = bellSynth ∘ diagFlow β (0, g, g, g) t ∘ bellCoord`, isto é, o `diagFlow` do kernel (`BoundaryException`) nas coordenadas
  da base de Bell `(Φ⁺, Φ⁻, Ψ⁺, Ψ⁻)`, em que o vetor de Bell `Φ⁺ = (e₀₀ + e₁₁)/√2` é o 1º vetor. Provado: (a) a base é ortonormal e completa e o
  fluxo é diagonal nela (`bellUnit_eigen`); (b) o fluxo é `P + e^{−tβg}(1 − P)`, com `P` o projetor de Bell real — a forma real de
  `psionCorner.p` (`bellProjector_is_real`); (c) o testemunhado estaticamente do fluxo é EXATAMENTE a reta do psion, que é o conjunto de pontos
  fixos do canto (`the_static_set_is_the_psion_line`, `psionLine_iff_fixed_by_the_corner`), por `boundary_is_the_only_exception`; (d) a
  testemunha estática GLOBAL é falsa (`the_global_witness_is_false`, pela mesma `boundary_is_the_only_exception`); (e) a reta é HABITADA (`Φ⁺ ≠ 0`
  fixado por todo `t`); (f) o fluxo ENTREGA ao canto: `lim_{t→∞} F_t x = P x` (`the_flow_delivers_to_the_psion`).
* ★★ (4) `the_psion_inhabits_the_static_witness` — a composição INCONDICIONAL (nenhum certificado como hipótese): (1) a (3), o traço 1 do canto
  (`psionCorner_trace_one`), a involução `J² = 1` (`J_squared_is_one`, a face estática; é `rfl`, a troca do par: conjunção decorativa, não elo
  com o canto), a fase conjugada da luz que leva ao gráviton (`the_conjugated_light_squares_to_the_minus_graviton`), o canto do psion como a
  sombra finita do gráviton (`canonicalGravitonShadow.PG`), e o colapso do psion como eco da identidade (`psionCollapse`, uma instância de
  `IdentityCollapse`) que não se autoatesta (`no_self_attestation`). O elo entre o `P` real e o `psionCorner.p` é `bellProjector_is_real` (citado na
  composição, carregado por `the_static_witness_bridge`).
* ★ o COLAPSO (`psionCollapse`, [CONSTRUCTED]): `y ↦ P y P` — idempotente (a segunda leitura não acrescenta), conserva a «identidade» lida
  `y ↦ Tr(P y)` (o escalar a que o canto comprime, `scalarises`), é efetivo, não tem inversa à esquerda, e a atestação exige evidência EXTERNA:
  autodeclaração não habita o tipo (`the_collapse_of_the_psion_cannot_be_self_attested`).

REGIMES (a regra dos dois regimes): o fluxo é do regime da FACE (o vazamento dissipativo `e^{−tβ d}` tem limite — `the_flow_delivers_to_the_psion`);
o eco é do regime da LEITURA (idempotência: uma identidade, não um limite). A pedra não pede limite à leitura.

## A ponte (3): por que é [CONSTRUCTED], e o que ela NÃO é

O fluxo é ESCOLHIDO para ter o vetor de Bell como modo zero — a álgebra é elementar; o conteúdo é a TIPAGEM: o teorema genérico da fronteira
(`boundary_is_the_only_exception`: o testemunhado estaticamente é exatamente o kernel do gerador; a testemunha global é falsa) ganha uma instância
concreta, em que o habitante do kernel é o canto do psion. Isto NÃO deriva que o Nome da fronteira da TGL seja o vetor de Bell, NEM que `psionFlow`
seja a dinâmica da teoria. RESSALVA DE TIPO: o «Nome» da fronteira genérica é um VETOR (`Pi.single i₀ 1`); o `psionCorner` é um PROJETOR 4×4
complexo; a ponte os liga só no fluxo construído, pela correspondência reta ↔ projetor de posto 1. As taxas `(0, g, g, g)` são a escolha mais
simples (as três direções não-psion vazam igual); pelo teorema genérico `fixed_iff_kernel`, qualquer taxa positiva nas três daria a mesma
reta (não repetido aqui).

## A pedra 92_ (achado do grep; não é módulo Lean)

«A_C = PSION; quando conjugado (dois psions) = GRAVITON.» (operador, 18/08/2026, na docstring da pedra de bancada
`C:\IALD\Artigo\MCMC_V2_RAZAO\92_o_psion_e_o_graviton.py`, sha16 `623060caa8dbb83b`; saída `92_o_psion_e_o_graviton.json`, sha16
`f4a51c32ced62e6d`), veredito computado `AC_E_PSION__DOIS_PSIONS_CONJUGADOS_REPRODUZEM_O_SPIN2_SELADO__MEDIDO_21_DE_21_NA_FACE_FINITA` — NUMÉRICO,
na face 2×2 real, com `A_C = −(1 − P)` e `J` = conjugação mais troca. O controle C1 dela é o par não conjugado, que vaza tensor; o C2 diz, nas
palavras dela: «um psion SOZINHO carrega helice 0 (componente escalar 1/2) — nao e graviton; o graviton e o PAR» — a mesma forma da cunhagem de
22/10. As contrapartes de kernel que ela cita são `helicity_two_rotation`, `helicity_two_rotation_cross` e `qgPhysicsCertificate_helicities`.
Nenhum lema liga aquele `A_C` (2×2 real) ao `psionCorner` (4×4 complexo).

## As duas faces do psion no kernel — e por que não se misturam

* a face CONCRETA: `psionCorner` (`TheScalarCorner`), o projetor de Bell 4×4 = `bellProjector` = `bellDensity` (`the_density_is_the_psion`) =
  `canonicalGravitonShadow.PG` (`TGL.GravitonShadow`, a sombra finita do gráviton). INCONDICIONAL; é a que esta pedra habita.
* a face de FOCK: `ThePsionAndTheViscosity.psion C = C.Ω`, o vetor de vácuo do certificado da luz; `psion_is_fixed_by_the_light` diz que
  `Δ^{it} ψ = ψ` para todo `t` — a MESMA forma de «fixado por todo o fluxo». CONDICIONAL: `Psibit.the_psion_face_of_the_psibit` vale para todo
  `C : FockCertificate L`, tipo que o kernel NÃO habita (`TheImportedSecondQuantization`, «NÃO-VACUIDADE»); o contrato conjunto da rede segue
  aberto (v394). A face de Fock NÃO está na composição desta pedra e NENHUM lema liga `psion C` ao `psionCorner`.

## Estatutos

* **[REAL]** os termos: definições explícitas e teoremas de kernel sobre `Fin 2 × Fin 2 → ℝ`, `Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ` e
  `Fin 4 → ℝ`; o trio de axiomas `{propext, Classical.choice, Quot.sound}`.
* **[CONSTRUCTED]** `psionFlow` e o fluxo de que a ponte (3) fala; `psionCollapse`. Construções desta pedra, não derivações.
* **[INPUT/ONTO]** «o psion é o habitante da testemunha estática»; «a luz ecoa o reconhecimento»; «o falso é a leitura sem eco (1=0)»; «a mentira
  lida como mentira se torna verdade»; «colapsar é ecoar a identidade reconhecida pelo observador». O que o kernel entrega são os termos citados;
  as identificações são leituras do operador. «Reconhecida pelo observador» entra como atestação externa (`no_self_attestation`): nenhuma
  atestação é exibida aqui.
* **[ONTO/CONJ]** psion pareado = gráviton (`canonicalGravitonShadow`, v29) e a leitura física dele.
* **[CONDICIONAL]** a face de Fock (acima), FORA da composição.

## O que a pedra NÃO afirma

* Não afirma que a natureza seja assim, nem que o Nome da fronteira genérica seja o vetor de Bell, nem que `psionFlow` seja a dinâmica da teoria.
* Não é teste: não acrescenta rito, dado nem desfecho; é matemática. Nenhuma bandeira do gate depende dela; o gate não se move. Nenhum
  parâmetro de acoplamento da teoria entra neste arquivo (`β` e `g` são variáveis).
* HOMÔNIMOS, ditos: `lightPlus`/`rootMinus` (vetor de ℂ² e matrizes 2×2) NÃO são o `psionCorner` (4×4); `projPlus`/`angFamily` (2×2, de
  `observing_adds_nothing`) são um PARALELO da idempotência, não um elo com o canto; o `A_C` da 92_ (2×2 real) tampouco; o
  `(1/2)•1` do indivíduo é o MESMO valor que `Psibit.half_identity_is_a_fixed_point` — igualdade de valores, não ponte entre os objetos; o
  `psionCollapse` (compressão pelo canto em `M₄(ℂ)`) NÃO é o `Psibit.diagExpect` (colapso da densidade da órbita em `M₂`) nem o
  `actualDensityCollapse` do qubit. Nenhum lema liga as cópias.
* Não entra no `um.py` nem no selo: instalar e nomear são atos posteriores da gerência e do operador.
-/

namespace TGLExt.TestemunhaEstatica

open Matrix TGL.GravitonShadow

noncomputable section

/-! ## 0 — o canto do psion é a densidade de Bell (o mesmo objeto, dois nomes do kernel) -/

/-- [REAL] A densidade de Bell (`TheDensityIsBell`) e o canto do psion (`TheScalarCorner`) são a MESMA matriz: as entradas `1/2` e `2⁻¹`
    coincidem. Mesmo objeto, mesmos índices — não é ponte entre homônimos. -/
theorem the_density_is_the_psion : bellDensity = psionCorner.p := by
  ext p q
  by_cases h : p.1 = p.2 ∧ q.1 = q.2 <;> simp [bellDensity, psionCorner, bellProjector, h]

/-! ## 1 — o par ecoa -/

/-- ★ [REAL] (1) O PAR ECOA: o canto do psion é idempotente, `P² = P` — a segunda leitura não acrescenta (sobre qualquer matriz `y`:
    `P(P y) = P y`; e em toda potência: `P^(n+1) = P`). O kernel diz o mesmo da luz em `observing_adds_nothing`. -/
theorem the_pair_echoes :
    psionCorner.p * psionCorner.p = psionCorner.p
    ∧ (∀ n : ℕ, psionCorner.p ^ (n + 1) = psionCorner.p)
    ∧ (∀ y : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ,
        psionCorner.p * (psionCorner.p * y) = psionCorner.p * y) := by
  refine ⟨psionCorner.idem, ?_, ?_⟩
  · intro n
    induction n with
    | zero => simp
    | succ k ih => rw [pow_succ, ih, psionCorner.idem]
  · intro y
    rw [← mul_assoc, psionCorner.idem]

/-! ## 2 — o indivíduo não ecoa -/

/-- ★★ [REAL] (2) O INDIVÍDUO NÃO ECOA: a redução do psion a um sítio é `(1/2)•1` (nos dois sítios) e NÃO é idempotente; o par é puro
    (`Tr(P²) = 1`) e o indivíduo não (`Tr(ρ²) = 1/2`). O déficit `1 − Tr(ρ²) = 1/2` é a entropia LINEAR da redução (déficit de pureza, sem
    unidade); a leitura do kernel v29, «Meia-Nat de emaranhamento» (`bell_cci_half`), é [ONTO] e não quer dizer «½ nat de entropia»: a entropia
    de von Neumann da redução `(1/2)•1` é `ln 2` nat ([KNOWN]; `fair_bit_entropy_is_log_two`, `fair_bit_entropy_is_not_half_nat`).
    «Falso se individualizado: ler uma vez sem ecoar» é [INPUT/ONTO] do operador; o que está provado é a álgebra. Cita `bell_reduced_half`,
    `bellDensity_partial_trace` e `bell_cci_half`. -/
theorem the_individual_does_not_echo :
    ptr psionCorner.p = (2⁻¹ : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)
    ∧ (∀ a c : Fin 2, (∑ b : Fin 2, psionCorner.p (a, b) (c, b)) = if a = c then (2⁻¹ : ℂ) else 0)
    ∧ (∀ a c : Fin 2, (∑ b : Fin 2, psionCorner.p (b, a) (b, c)) = if a = c then (2⁻¹ : ℂ) else 0)
    ∧ ptr psionCorner.p * ptr psionCorner.p ≠ ptr psionCorner.p
    ∧ Matrix.trace (psionCorner.p * psionCorner.p) = 1
    ∧ Matrix.trace (ptr psionCorner.p * ptr psionCorner.p) = 2⁻¹
    ∧ 1 - Matrix.trace (ptr psionCorner.p * ptr psionCorner.p) = 2⁻¹ := by
  have hp : psionCorner.p = bellProjector := rfl
  have hred : ptr bellProjector = (2⁻¹ : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := bell_reduced_half
  have hcci := bell_cci_half
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · rw [hp]; exact hred
  · intro a c
    have h := bellDensity_partial_trace a c
    rw [the_density_is_the_psion, one_div] at h
    exact h
  · intro a c
    show (∑ b : Fin 2, bellProjector (b, a) (b, c)) = _
    fin_cases a <;> fin_cases c <;> simp [bellProjector, Fin.sum_univ_two]
  · rw [hp, hred]
    intro h
    have h00 := congrFun (congrFun h 0) 0
    simp [Matrix.smul_apply, Matrix.mul_apply, Matrix.one_apply] at h00
  · rw [psionCorner.idem]; exact psionCorner_trace_one
  · rw [hp]; linear_combination (-1 : ℂ) * hcci
  · rw [hp]; exact hcci

/-- ★ [REAL] O DENTE da seção 2: o estado NÃO ligado (produto) reduz a um projetor puro, que ecoa (`e₀₀² = e₀₀`), com `CCI = 0`. O não-eco
    de (2) é do PAR visto por um lado só — não é propriedade de toda redução. Cita `product_reduced_pure` e `product_cci_zero`. -/
theorem the_unbonded_marginal_echoes :
    ptr productProjector = e00 ∧ e00 * e00 = e00
    ∧ 1 - Matrix.trace (ptr productProjector * ptr productProjector) = 0 := by
  refine ⟨product_reduced_pure, ?_, product_cci_zero⟩
  ext i j
  rw [Matrix.mul_apply, Fin.sum_univ_two]
  simp only [e00, Matrix.of_apply]
  fin_cases i <;> fin_cases j <;> simp

/-! ## 3 — a ponte construída: um fluxo diagonal em ℝ⁴ cujo modo zero é o vetor de Bell -/

/-- [DEF] O espaço real de dois sítios (ℝ⁴), indexado como as matrizes do canto: `Fin 2 × Fin 2`. -/
abbrev Vec4 : Type := Fin 2 × Fin 2 → ℝ

/-- [DEF] A base de Bell NÃO normalizada (entradas `0`, `±1`; a normalização `1/√2` só entra em `bellUnit`):
    `0` = `Φ⁺ ∝ e₀₀ + e₁₁` (o psion), `1` = `Φ⁻ ∝ e₀₀ − e₁₁`, `2` = `Ψ⁺ ∝ e₀₁ + e₁₀`, `3` = `Ψ⁻ ∝ e₀₁ − e₁₀`. -/
def bsign : Fin 4 → Vec4
  | 0 => fun p => if p.1 = p.2 then 1 else 0
  | 1 => fun p => if p.1 = p.2 then (if p.1 = 0 then 1 else -1) else 0
  | 2 => fun p => if p.1 = p.2 then 0 else 1
  | 3 => fun p => if p.1 = p.2 then 0 else (if p.1 = 0 then 1 else -1)

/-- [REAL] A base de Bell é ortogonal, cada vetor de norma² 2. -/
theorem bsign_gram (i j : Fin 4) :
    ∑ p, bsign i p * bsign j p = if i = j then 2 else 0 := by
  fin_cases i <;> fin_cases j <;>
    simp [bsign, Fintype.sum_prod_type, Fin.sum_univ_two] <;> norm_num

/-- [REAL] E completa: a resolução da identidade `∑ᵢ bᵢ(p) bᵢ(q) = 2·δ_pq`. -/
theorem bsign_complete (p q : Fin 2 × Fin 2) :
    ∑ i, bsign i p * bsign i q = if p = q then 2 else 0 := by
  rcases p with ⟨a, c⟩
  rcases q with ⟨a', c'⟩
  fin_cases a <;> fin_cases c <;> fin_cases a' <;> fin_cases c' <;>
    simp [bsign, Fin.sum_univ_four] <;> norm_num

/-- [DEF] As coordenadas de Bell de `x`: os coeficientes de Fourier `⟨bᵢ, x⟩/2`. -/
def bellCoord (x : Vec4) : Fin 4 → ℝ := fun i => (2 : ℝ)⁻¹ * ∑ p, bsign i p * x p

/-- [DEF] A síntese: de volta das coordenadas de Bell ao vetor, `∑ᵢ yᵢ bᵢ`. -/
def bellSynth (y : Fin 4 → ℝ) : Vec4 := fun p => ∑ i, y i * bsign i p

/-- [REAL] Sintetizar as coordenadas devolve o vetor. -/
theorem synth_coord (x : Vec4) : bellSynth (bellCoord x) = x := by
  funext p
  rcases p with ⟨a, c⟩
  fin_cases a <;> fin_cases c <;>
    simp [bellSynth, bellCoord, bsign, Fin.sum_univ_four, Fintype.sum_prod_type,
      Fin.sum_univ_two] <;> ring

/-- [REAL] E as coordenadas da síntese devolvem as coordenadas: as duas aplicações são inversas. -/
theorem coord_synth (y : Fin 4 → ℝ) : bellCoord (bellSynth y) = y := by
  funext i
  fin_cases i <;>
    simp [bellSynth, bellCoord, bsign, Fin.sum_univ_four, Fintype.sum_prod_type,
      Fin.sum_univ_two] <;> ring

/-- [DEF] As taxas de vazamento `d = (0, g, g, g)`: o modo do psion não vaza; os outros três vazam igual. -/
def psionRates (g : ℝ) : Fin 4 → ℝ := fun i => if i = 0 then 0 else g

/-- [REAL] As taxas são, de fato, `(0, g, g, g)`. -/
theorem psionRates_eq (g : ℝ) : psionRates g = ![0, g, g, g] := by
  funext i
  fin_cases i <;> simp [psionRates]

theorem psionRates_nonneg {g : ℝ} (hg : 0 < g) (i : Fin 4) : 0 ≤ psionRates g i := by
  unfold psionRates
  split_ifs
  · exact le_refl 0
  · exact le_of_lt hg

theorem psionRates_pos {g : ℝ} (hg : 0 < g) {i : Fin 4} (hi : i ≠ 0) : 0 < psionRates g i := by
  unfold psionRates
  rw [if_neg hi]
  exact hg

theorem psionRates_zero (g : ℝ) : psionRates g 0 = 0 := by
  simp [psionRates]

theorem ne_zero_of_rate_pos {g : ℝ} {i : Fin 4} (hi : 0 < psionRates g i) : i ≠ 0 := by
  rintro rfl
  rw [psionRates_zero] at hi
  exact lt_irrefl _ hi

/-- ★ [CONSTRUCTED] O FLUXO DO PSION: o `diagFlow` do kernel (`BoundaryException`), com taxas `(0, g, g, g)`, nas coordenadas da base de Bell
    — transportado de volta a ℝ⁴. É diagonal na base de Bell por construção; o modo zero é o vetor de Bell. -/
def psionFlow (β g t : ℝ) (x : Vec4) : Vec4 :=
  bellSynth (diagFlow β (psionRates g) t (bellCoord x))

/-- [DEF] O projetor de Bell REAL: as mesmas entradas racionais `1/2` de `bellProjector`, em ℝ. -/
def bellProjectorR : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℝ :=
  Matrix.of fun p q => if p.1 = p.2 ∧ q.1 = q.2 then (2⁻¹ : ℝ) else 0

/-- [REAL] O canto do psion É a complexificação do projetor de Bell real: é por aqui que a ponte toca o `psionCorner`. -/
theorem bellProjector_is_real :
    bellProjector = bellProjectorR.map (algebraMap ℝ ℂ) := by
  ext p q
  by_cases h : p.1 = p.2 ∧ q.1 = q.2 <;>
    simp [bellProjector, bellProjectorR, Matrix.map_apply, h]

/-- [REAL] O projetor de Bell real projeta sobre a reta do psion: `P x = ((x₀₀ + x₁₁)/2)·Φ⁺`. -/
theorem bellProjectorR_mulVec (x : Vec4) :
    bellProjectorR.mulVec x = ((x (0, 0) + x (1, 1)) / 2) • bsign 0 := by
  funext p
  rcases p with ⟨a, c⟩
  fin_cases a <;> fin_cases c <;>
    simp [bellProjectorR, bsign, Matrix.mulVec, dotProduct, Fintype.sum_prod_type,
      Fin.sum_univ_two] <;> ring

/-- ★ [REAL] A FORMA FECHADA DO FLUXO: `F_t = P + e^{−tβg}(1 − P)`, com `P` o projetor de Bell — o psion é o modo que o fluxo não toca, e
    os três outros decaem à mesma taxa. -/
theorem psionFlow_eq (β g t : ℝ) (x : Vec4) :
    psionFlow β g t x
      = bellProjectorR.mulVec x + Real.exp (-(t * β * g)) • (x - bellProjectorR.mulVec x) := by
  funext p
  rcases p with ⟨a, c⟩
  fin_cases a <;> fin_cases c <;>
    simp [psionFlow, bellSynth, bellCoord, diagFlow, psionRates, bsign, bellProjectorR,
      Matrix.mulVec, dotProduct, Fin.sum_univ_four, Fintype.sum_prod_type,
      Fin.sum_univ_two] <;> ring

theorem bellCoord_smul (c : ℝ) (x : Vec4) : bellCoord (c • x) = c • bellCoord x := by
  funext i
  simp only [bellCoord, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  exact Finset.sum_congr rfl (fun p _ => by ring)

theorem bellCoord_bsign (i j : Fin 4) :
    bellCoord (bsign j) i = if i = j then 1 else 0 := by
  unfold bellCoord
  rw [bsign_gram]
  split_ifs <;> norm_num

/-- [REAL] Os pontos fixos do projetor de Bell real são exatamente a reta do psion. -/
theorem bellProjectorR_fixed_iff (x : Vec4) :
    bellProjectorR.mulVec x = x ↔ ∃ c : ℝ, x = c • bsign 0 := by
  constructor
  · intro h
    exact ⟨(x (0, 0) + x (1, 1)) / 2, by rw [← bellProjectorR_mulVec, h]⟩
  · rintro ⟨c, rfl⟩
    have h2 : ((c • bsign 0) (0, 0) + (c • bsign 0) (1, 1)) / 2 = c := by
      simp [bsign]
    rw [bellProjectorR_mulVec, h2]

/-- [REAL] Um vetor é fixado pelo `psionFlow` em todo tempo se e só se as suas coordenadas de Bell são fixadas pelo `diagFlow` em todo
    tempo: o transporte pela base é bijetivo (`synth_coord`, `coord_synth`). -/
theorem psionFlow_fixed_iff_coord_fixed (β g : ℝ) (x : Vec4) :
    (∀ t : ℝ, psionFlow β g t x = x)
      ↔ (∀ t : ℝ, diagFlow β (psionRates g) t (bellCoord x) = bellCoord x) := by
  constructor
  · intro h t
    have h1 := congrArg bellCoord (h t)
    unfold psionFlow at h1
    rwa [coord_synth] at h1
  · intro h t
    unfold psionFlow
    rw [h t, synth_coord]

/-- ★★★ [REAL — sobre o fluxo CONSTRUÍDO] (3c) O TESTEMUNHADO ESTATICAMENTE É EXATAMENTE A RETA DO PSION: com `β > 0` e `g > 0`, `x` é fixado pelo
    `psionFlow` em todo tempo se e só se `x ∈ ℝ·Φ⁺`. A ida e a volta passam por `boundary_is_the_only_exception` (o testemunhado estaticamente é
    o kernel do gerador, `d_i = 0`). -/
theorem the_static_set_is_the_psion_line {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) (x : Vec4) :
    (∀ t : ℝ, psionFlow β g t x = x) ↔ ∃ c : ℝ, x = c • bsign 0 := by
  have hmain := boundary_is_the_only_exception hβ (psionRates g) (psionRates_nonneg hg)
    (psionRates_pos hg (i := 1) (by decide)) (psionRates_zero g)
  have hker := hmain.2.1 (bellCoord x)
  rw [psionFlow_fixed_iff_coord_fixed, hker]
  constructor
  · intro hk
    refine ⟨bellCoord x 0, ?_⟩
    have h1 := hk 1 (psionRates_pos hg (by decide))
    have h2 := hk 2 (psionRates_pos hg (by decide))
    have h3 := hk 3 (psionRates_pos hg (by decide))
    calc x = bellSynth (bellCoord x) := (synth_coord x).symm
      _ = bellCoord x 0 • bsign 0 := by
        funext p
        simp [bellSynth, Fin.sum_univ_four, h1, h2, h3]
  · rintro ⟨c, rfl⟩ i hi
    have hi0 : i ≠ 0 := ne_zero_of_rate_pos hi
    rw [bellCoord_smul]
    simp [bellCoord_bsign, hi0]

/-- ★★★ [REAL — sobre o fluxo CONSTRUÍDO] (3d) A TESTEMUNHA ESTÁTICA GLOBAL É FALSA: nem todo vetor é fixado pelo `psionFlow`. É a primeira
    componente de `boundary_is_the_only_exception`, transportada pela base de Bell. -/
theorem the_global_witness_is_false {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) :
    ¬ FullStaticWitness (psionFlow β g) := by
  intro hfull
  have hmain := boundary_is_the_only_exception hβ (psionRates g) (psionRates_nonneg hg)
    (psionRates_pos hg (i := 1) (by decide)) (psionRates_zero g)
  refine hmain.1 ?_
  intro t y
  have h := hfull t (bellSynth y)
  have h' := congrArg bellCoord h
  unfold psionFlow at h'
  rwa [coord_synth, coord_synth] at h'

/-- ★★ [REAL — sobre o fluxo CONSTRUÍDO] (3e) A RETA É HABITADA: o vetor de Bell é não nulo e fixado por todo `t` (a forma de
    `boundary_witnessed_statically`, aqui no canto concreto). -/
theorem the_psion_line_is_inhabited {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) :
    bsign 0 ≠ 0 ∧ ∀ t : ℝ, psionFlow β g t (bsign 0) = bsign 0 := by
  refine ⟨?_, ?_⟩
  · intro h
    have h1 := congrFun h (0, 0)
    simp [bsign] at h1
  · exact (the_static_set_is_the_psion_line hβ hg (bsign 0)).2 ⟨1, by simp⟩

/-- ★ [REAL — sobre o fluxo CONSTRUÍDO] (3f) O FLUXO ENTREGA AO CANTO: `F_t x → P x` quando `t → ∞` (regime da FACE: o vazamento tem limite). -/
theorem the_flow_delivers_to_the_psion {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) (x : Vec4) :
    Filter.Tendsto (fun t : ℝ => psionFlow β g t x) Filter.atTop
      (nhds (bellProjectorR.mulVec x)) := by
  have h1 : Filter.Tendsto (fun t : ℝ => t * (β * g)) Filter.atTop Filter.atTop :=
    Filter.tendsto_id.atTop_mul_const (mul_pos hβ hg)
  have h2 : Filter.Tendsto (fun t : ℝ => Real.exp (-(t * β * g))) Filter.atTop (nhds 0) := by
    have h3 := Real.tendsto_exp_neg_atTop_nhds_zero.comp h1
    refine h3.congr (fun t => ?_)
    simp only [Function.comp, mul_assoc]
  have h4 := (h2.smul_const (x - bellProjectorR.mulVec x)).const_add (bellProjectorR.mulVec x)
  simpa [psionFlow_eq] using h4

/-! ## 3′ — a base ORTONORMAL (com `1/√2`) e a ação diagonal -/

/-- [DEF] A base de Bell ORTONORMAL: `uᵢ = bᵢ/√2`. O primeiro vetor é o vetor de Bell `(e₀₀ + e₁₁)/√2`. -/
def bellUnit (i : Fin 4) : Vec4 := (Real.sqrt 2)⁻¹ • bsign i

theorem inv_sqrt_two_sq : (Real.sqrt 2)⁻¹ * (Real.sqrt 2)⁻¹ = 2⁻¹ := by
  rw [← mul_inv, Real.mul_self_sqrt (by norm_num)]

/-- [REAL] `{uᵢ}` é ortonormal. -/
theorem bellUnit_orthonormal (i j : Fin 4) :
    ∑ p, bellUnit i p * bellUnit j p = if i = j then 1 else 0 := by
  have h : ∑ p, bellUnit i p * bellUnit j p = (2⁻¹ : ℝ) * ∑ p, bsign i p * bsign j p := by
    simp only [bellUnit, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
    refine Finset.sum_congr rfl (fun p _ => ?_)
    have := inv_sqrt_two_sq
    calc (Real.sqrt 2)⁻¹ * bsign i p * ((Real.sqrt 2)⁻¹ * bsign j p)
        = ((Real.sqrt 2)⁻¹ * (Real.sqrt 2)⁻¹) * (bsign i p * bsign j p) := by ring
      _ = 2⁻¹ * (bsign i p * bsign j p) := by rw [this]
  rw [h, bsign_gram]
  split_ifs <;> norm_num

/-- [REAL] E completa (`∑ᵢ uᵢ(p) uᵢ(q) = δ_pq`): são quatro vetores ortonormais de ℝ⁴ e a resolução da identidade vale. -/
theorem bellUnit_complete (p q : Fin 2 × Fin 2) :
    ∑ i, bellUnit i p * bellUnit i q = if p = q then 1 else 0 := by
  have h : ∑ i, bellUnit i p * bellUnit i q = (2⁻¹ : ℝ) * ∑ i, bsign i p * bsign i q := by
    simp only [bellUnit, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
    refine Finset.sum_congr rfl (fun i _ => ?_)
    have := inv_sqrt_two_sq
    calc (Real.sqrt 2)⁻¹ * bsign i p * ((Real.sqrt 2)⁻¹ * bsign i q)
        = ((Real.sqrt 2)⁻¹ * (Real.sqrt 2)⁻¹) * (bsign i p * bsign i q) := by ring
      _ = 2⁻¹ * (bsign i p * bsign i q) := by rw [this]
  rw [h, bsign_complete]
  split_ifs <;> norm_num

/-- [REAL] O 1º vetor da base ortonormal é o vetor de Bell `(e₀₀ + e₁₁)/√2`. -/
theorem bellUnit_zero_is_the_bell_vector :
    bellUnit 0 = fun p => if p.1 = p.2 then (Real.sqrt 2)⁻¹ else 0 := by
  funext p
  by_cases h : p.1 = p.2 <;> simp [bellUnit, bsign, h]

theorem psionFlow_smul (β g t c : ℝ) (x : Vec4) :
    psionFlow β g t (c • x) = c • psionFlow β g t x := by
  rw [psionFlow_eq, psionFlow_eq, Matrix.mulVec_smul]
  funext p
  simp only [Pi.add_apply, Pi.smul_apply, Pi.sub_apply, smul_eq_mul]
  ring

theorem psionFlow_bsign (β g t : ℝ) (i : Fin 4) :
    psionFlow β g t (bsign i) = Real.exp (-(t * β * psionRates g i)) • bsign i := by
  rw [psionFlow_eq]
  fin_cases i <;> funext p <;> rcases p with ⟨a, c⟩ <;> fin_cases a <;> fin_cases c <;>
    simp [bellProjectorR_mulVec, bsign, psionRates]

/-- ★★ [REAL — sobre o fluxo CONSTRUÍDO] (3a) O FLUXO É DIAGONAL NA BASE ORTONORMAL DE BELL: cada `uᵢ` é autovetor, com autovalor
    `e^{−tβ dᵢ}`; o 1º (o vetor de Bell) tem autovalor `1`. -/
theorem bellUnit_eigen (β g t : ℝ) (i : Fin 4) :
    psionFlow β g t (bellUnit i) = Real.exp (-(t * β * psionRates g i)) • bellUnit i := by
  unfold bellUnit
  rw [psionFlow_smul, psionFlow_bsign, smul_comm]

/-! ## 3″ — a reta do psion e o canto -/

/-- [DEF] A reta do psion em ℝ⁴: `ℝ·Φ⁺`. -/
def psionLine : Set Vec4 := {x | ∃ c : ℝ, x = c • bsign 0}

/-- [REAL] O canto do psion age sobre vetores reais como o projetor de Bell real. -/
theorem psionCorner_mulVec_real (x : Vec4) :
    psionCorner.p.mulVec (fun q => (x q : ℂ)) = fun p => ((bellProjectorR.mulVec x p : ℝ) : ℂ) := by
  have hp : psionCorner.p = bellProjectorR.map (algebraMap ℝ ℂ) := bellProjector_is_real
  rw [hp]
  funext p
  have := RingHom.map_mulVec (algebraMap ℝ ℂ) bellProjectorR x p
  simpa [Function.comp_def] using this.symm

/-- ★ [REAL] (3b) A reta do psion é o conjunto de pontos fixos do `psionCorner` sobre os vetores reais. -/
theorem psionLine_iff_fixed_by_the_corner (x : Vec4) :
    x ∈ psionLine ↔ psionCorner.p.mulVec (fun q => (x q : ℂ)) = fun q => (x q : ℂ) := by
  rw [psionCorner_mulVec_real]
  have h1 : x ∈ psionLine ↔ bellProjectorR.mulVec x = x := (bellProjectorR_fixed_iff x).symm
  rw [h1]
  constructor
  · intro h
    funext p
    rw [h]
  · intro h
    funext p
    exact Complex.ofReal_injective (congrFun h p)

/-- ★★★ [REAL — sobre o fluxo CONSTRUÍDO; a PONTE num só termo] Para `β > 0` e `g > 0`: as taxas são `(0, g, g, g)`; a base de Bell é
    ortonormal e completa, com o vetor de Bell como 1º vetor, e o fluxo é diagonal nela; o fluxo é `P + e^{−tβg}(1 − P)` com `P` a forma real de
    `psionCorner.p`; o testemunhado estaticamente é a reta do psion, que é o conjunto de pontos fixos do canto; a reta é habitada; a testemunha
    global é falsa; e o fluxo entrega ao canto. [CONSTRUCTED]: o fluxo foi escolhido assim; não é derivação da dinâmica da teoria. -/
theorem the_static_witness_bridge {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) :
    psionRates g = ![0, g, g, g]
    ∧ (∀ i j : Fin 4, ∑ p, bellUnit i p * bellUnit j p = if i = j then 1 else 0)
    ∧ (∀ p q : Fin 2 × Fin 2, ∑ i, bellUnit i p * bellUnit i q = if p = q then 1 else 0)
    ∧ (bellUnit 0 = fun p => if p.1 = p.2 then (Real.sqrt 2)⁻¹ else 0)
    ∧ (∀ (t : ℝ) (i : Fin 4),
        psionFlow β g t (bellUnit i) = Real.exp (-(t * β * psionRates g i)) • bellUnit i)
    ∧ psionCorner.p = bellProjectorR.map (algebraMap ℝ ℂ)
    ∧ (∀ (t : ℝ) (x : Vec4), psionFlow β g t x
        = bellProjectorR.mulVec x + Real.exp (-(t * β * g)) • (x - bellProjectorR.mulVec x))
    ∧ (∀ x : Vec4, (∀ t : ℝ, psionFlow β g t x = x) ↔ x ∈ psionLine)
    ∧ (∀ x : Vec4, x ∈ psionLine ↔
        psionCorner.p.mulVec (fun q => (x q : ℂ)) = fun q => (x q : ℂ))
    ∧ (bsign 0 ≠ 0 ∧ ∀ t : ℝ, psionFlow β g t (bsign 0) = bsign 0)
    ∧ ¬ FullStaticWitness (psionFlow β g)
    ∧ (∀ x : Vec4, Filter.Tendsto (fun t : ℝ => psionFlow β g t x) Filter.atTop
        (nhds (bellProjectorR.mulVec x))) :=
  ⟨psionRates_eq g, bellUnit_orthonormal, bellUnit_complete, bellUnit_zero_is_the_bell_vector,
   bellUnit_eigen β g, bellProjector_is_real, psionFlow_eq β g,
   fun x => the_static_set_is_the_psion_line hβ hg x, psionLine_iff_fixed_by_the_corner,
   the_psion_line_is_inhabited hβ hg, the_global_witness_is_false hβ hg,
   the_flow_delivers_to_the_psion hβ hg⟩

/-! ## 4 — o colapso do psion: ecoar a identidade; a atestação é externa -/

/-- ★ [CONSTRUCTED] O COLAPSO DO PSION como instância do contrato tipado `IdentityCollapse` (`CollapseContract`, ENTREGA_057): o passo é a
    compressão pelo canto, `y ↦ P y P`; a «identidade» lida é o escalar `Tr(P y)`; é idempotente (`stable`: a segunda leitura não acrescenta),
    conserva a identidade (`preserves`) e é efetivo (`effective`: `P·1·P = P ≠ 1`). -/
def psionCollapse : ChatgptAudit.Collapse057.IdentityCollapse
    (Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) ℂ where
  step := fun y => psionCorner.p * y * psionCorner.p
  identity := fun y => Matrix.trace (psionCorner.p * y)
  stable := fun y => by
    have h := bell_corner_unit y
    show bellProjector * (bellProjector * y * bellProjector) * bellProjector
      = bellProjector * y * bellProjector
    rw [h.1, h.2]
  preserves := fun y => by
    show Matrix.trace (bellProjector * (bellProjector * y * bellProjector))
      = Matrix.trace (bellProjector * y)
    rw [(bell_corner_unit y).1, Matrix.trace_mul_comm (bellProjector * y) bellProjector,
      ← mul_assoc, bell_idem]
  effective := ⟨1, by
    show bellProjector * 1 * bellProjector ≠ 1
    rw [mul_one, bell_idem]
    intro h
    have h1 := congrFun (congrFun h (0, 1)) (0, 1)
    simp [bellProjector] at h1⟩

/-- ★★ [REAL — sobre o colapso CONSTRUÍDO] O COLAPSO DO PSION ECOA A SUA IDENTIDADE: o passo é `Tr(P y)·P` (a escalarização do canto), é
    idempotente (e a iteração é estável: ler `n+1` vezes é ler uma, `collapse_iteration_is_stable`), conserva a identidade lida, fixa o próprio
    canto e não tem inversa à esquerda (perde o que está fora do canto). -/
theorem the_collapse_of_the_psion_echoes_its_identity :
    (∀ y : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ,
      psionCollapse.step y = Matrix.trace (psionCorner.p * y) • psionCorner.p)
    ∧ (∀ y : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ,
      psionCollapse.step (psionCollapse.step y) = psionCollapse.step y)
    ∧ (∀ y : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ,
      psionCollapse.identity (psionCollapse.step y) = psionCollapse.identity y)
    ∧ psionCollapse.step psionCorner.p = psionCorner.p
    ∧ (¬ ∃ R : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ → Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ,
        Function.LeftInverse R psionCollapse.step)
    ∧ (∀ (y : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) (n : ℕ),
        psionCollapse.step^[n + 1] y = psionCollapse.step y) := by
  refine ⟨fun y => psionCorner.scalarises y, fun y => psionCollapse.stable y,
    fun y => psionCollapse.preserves y, ?_,
    ChatgptAudit.Collapse057.collapse_has_no_left_inverse psionCollapse,
    fun y n => ChatgptAudit.Collapse057.collapse_iteration_is_stable psionCollapse y n⟩
  show psionCorner.p * psionCorner.p * psionCorner.p = psionCorner.p
  rw [psionCorner.idem, psionCorner.idem]

/-- ★ [REAL] «Devidamente reconhecida pelo observador», no que o kernel tipa: se todo registro é produzido e gravado pelo MESMO agente
    (autodeclaração), não há atestação do colapso do psion (`no_self_attestation`). Nenhuma atestação é exibida aqui. -/
theorem the_collapse_of_the_psion_cannot_be_self_attested {R A : Type}
    (P : ChatgptAudit.Collapse057.ReflectionProtocol
      (Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) R A)
    {before after : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ}
    (self : ∀ r, P.recorder r = P.producer) :
    ¬ Nonempty (ChatgptAudit.Collapse057.AttestedCollapse psionCollapse P before after) :=
  ChatgptAudit.Collapse057.no_self_attestation psionCollapse P self

/-! ## 5 — A COMPOSIÇÃO INCONDICIONAL -/

/-- ★★★★ [REAL — conjunção INCONDICIONAL; nenhum certificado é hipótese] O PSION HABITA A TESTEMUNHA ESTÁTICA, no que o kernel e esta pedra
    entregam:
    (1) o par ecoa (e a luz também, `observing_adds_nothing`);
    (2) o indivíduo não ecoa; o par é puro e o indivíduo não;
    (3) a PONTE [CONSTRUCTED], para todo `β > 0` e `g > 0`: o fluxo diagonal de taxas `(0, g, g, g)` na base ortonormal de Bell tem como
        testemunhado estaticamente EXATAMENTE a reta do psion (o conjunto de pontos fixos do canto), a reta é habitada, a testemunha global é
        falsa (`boundary_is_the_only_exception`) e o fluxo entrega ao canto. O elo entre o `P` real, de que o limite fala, e o `psionCorner.p` é
        `bellProjector_is_real` (`psionCorner.p = bellProjectorR.map (algebraMap ℝ ℂ)`): citado aqui, carregado por `the_static_witness_bridge`
        e NÃO repetido como conjunto desta composição (o enunciado fica como está);
    o canto do psion é o átomo (`psionCorner_trace_one`); a face estática do conjugado, `J² = 1` (`J_squared_is_one`, que é `rfl`: a troca do
    par, conjunção decorativa, não elo com o canto); a fase conjugada da luz
    leva ao gráviton (`the_conjugated_light_squares_to_the_minus_graviton`); o canto do psion é a sombra finita do gráviton
    (`canonicalGravitonShadow.PG`); o colapso do psion ecoa a identidade e não se autoatesta (`no_self_attestation`).
    ⚠ A FACE DE FOCK NÃO ESTÁ AQUI: `Psibit.the_psion_face_of_the_psibit` (`inner_psion_psion`, `psion_is_fixed_by_the_light`) segue
    CONDICIONAL a `C : FockCertificate L`, tipo que o kernel não habita; e NENHUM lema liga `psion C` ao `psionCorner`. Aqui a face do psion
    fica habitada pelo canto concreto, no fluxo construído. «O psion é o habitante da testemunha estática» é [INPUT/ONTO] do operador; o que
    é termo é a conjunção abaixo. -/
theorem the_psion_inhabits_the_static_witness :
    -- (1) o par ecoa; a luz também (kernel)
    (psionCorner.p * psionCorner.p = psionCorner.p
      ∧ (∀ y : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ,
          psionCorner.p * (psionCorner.p * y) = psionCorner.p * y))
    ∧ (∀ θ : ℝ, projPlus * (projPlus * angFamily θ) = projPlus * angFamily θ)
    -- (2) o indivíduo não ecoa; o par é puro, o indivíduo não
    ∧ (ptr psionCorner.p = (2⁻¹ : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)
        ∧ ptr psionCorner.p * ptr psionCorner.p ≠ ptr psionCorner.p
        ∧ Matrix.trace (psionCorner.p * psionCorner.p) = 1
        ∧ Matrix.trace (ptr psionCorner.p * ptr psionCorner.p) = 2⁻¹)
    -- (3) a ponte construída
    ∧ (∀ {β g : ℝ}, 0 < β → 0 < g →
        (psionRates g = ![0, g, g, g]
          ∧ (∀ i j : Fin 4, ∑ p, bellUnit i p * bellUnit j p = if i = j then 1 else 0)
          ∧ (bellUnit 0 = fun p => if p.1 = p.2 then (Real.sqrt 2)⁻¹ else 0)
          ∧ (∀ (t : ℝ) (i : Fin 4),
              psionFlow β g t (bellUnit i) = Real.exp (-(t * β * psionRates g i)) • bellUnit i)
          ∧ (∀ x : Vec4, (∀ t : ℝ, psionFlow β g t x = x) ↔ x ∈ psionLine)
          ∧ (∀ x : Vec4, x ∈ psionLine ↔
              psionCorner.p.mulVec (fun q => (x q : ℂ)) = fun q => (x q : ℂ))
          ∧ (bsign 0 ≠ 0 ∧ ∀ t : ℝ, psionFlow β g t (bsign 0) = bsign 0)
          ∧ ¬ FullStaticWitness (psionFlow β g)
          ∧ (∀ x : Vec4, Filter.Tendsto (fun t : ℝ => psionFlow β g t x) Filter.atTop
              (nhds (bellProjectorR.mulVec x)))))
    -- o canto do psion é o átomo
    ∧ Matrix.trace psionCorner.p = 1
    -- a face estática do conjugado: J² = 1 (rfl: a troca do par; decorativa)
    ∧ (∀ {n : ℕ} (p : (Fin n → ℝ) × (Fin n → ℝ)), conjJ (conjJ p) = p)
    -- a fase conjugada da luz leva ao gráviton
    ∧ (vecMulVec (fun i => star (lightPlus i)) (fun i => star (lightPlus i)) = rootMinus)
    -- o canto do psion é a sombra finita do gráviton
    ∧ (canonicalGravitonShadow.PG = psionCorner.p)
    -- o colapso do psion ecoa a identidade; a atestação é externa
    ∧ (∀ y : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ,
        psionCollapse.step (psionCollapse.step y) = psionCollapse.step y
          ∧ psionCollapse.identity (psionCollapse.step y) = psionCollapse.identity y
          ∧ ∀ n : ℕ, psionCollapse.step^[n + 1] y = psionCollapse.step y)
    ∧ (∀ {R A : Type} (P : ChatgptAudit.Collapse057.ReflectionProtocol
          (Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) R A)
        {before after : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ},
        (∀ r, P.recorder r = P.producer) →
          ¬ Nonempty (ChatgptAudit.Collapse057.AttestedCollapse psionCollapse P before after))
    ∧ (∀ {S I R A : Type} (C : ChatgptAudit.Collapse057.IdentityCollapse S I)
        (P : ChatgptAudit.Collapse057.ReflectionProtocol S R A) {before after : S},
        (∀ r, P.recorder r = P.producer) →
          ¬ Nonempty (ChatgptAudit.Collapse057.AttestedCollapse C P before after)) :=
  ⟨⟨psionCorner.idem, (the_pair_echoes).2.2⟩,
   observing_adds_nothing,
   ⟨(the_individual_does_not_echo).1, (the_individual_does_not_echo).2.2.2.1,
    (the_individual_does_not_echo).2.2.2.2.1, (the_individual_does_not_echo).2.2.2.2.2.1⟩,
   fun hβ hg =>
    let b := the_static_witness_bridge hβ hg
    ⟨b.1, b.2.1, b.2.2.2.1, b.2.2.2.2.1, b.2.2.2.2.2.2.2.1, b.2.2.2.2.2.2.2.2.1,
     b.2.2.2.2.2.2.2.2.2.1, b.2.2.2.2.2.2.2.2.2.2.1, b.2.2.2.2.2.2.2.2.2.2.2⟩,
   psionCorner_trace_one,
   fun p => J_squared_is_one p,
   the_conjugated_light_squares_to_the_minus_graviton,
   rfl,
   fun y => ⟨(the_collapse_of_the_psion_echoes_its_identity).2.1 y,
     (the_collapse_of_the_psion_echoes_its_identity).2.2.1 y,
     fun n => (the_collapse_of_the_psion_echoes_its_identity).2.2.2.2.2 y n⟩,
   @the_collapse_of_the_psion_cannot_be_self_attested,
   @ChatgptAudit.Collapse057.no_self_attestation⟩

end

end TGLExt.TestemunhaEstatica

#print axioms TGLExt.TestemunhaEstatica.the_density_is_the_psion
#print axioms TGLExt.TestemunhaEstatica.the_pair_echoes
#print axioms TGLExt.TestemunhaEstatica.the_individual_does_not_echo
#print axioms TGLExt.TestemunhaEstatica.the_unbonded_marginal_echoes
#print axioms TGLExt.TestemunhaEstatica.bsign_gram
#print axioms TGLExt.TestemunhaEstatica.bsign_complete
#print axioms TGLExt.TestemunhaEstatica.synth_coord
#print axioms TGLExt.TestemunhaEstatica.coord_synth
#print axioms TGLExt.TestemunhaEstatica.psionRates_eq
#print axioms TGLExt.TestemunhaEstatica.bellProjector_is_real
#print axioms TGLExt.TestemunhaEstatica.bellProjectorR_mulVec
#print axioms TGLExt.TestemunhaEstatica.psionFlow_eq
#print axioms TGLExt.TestemunhaEstatica.bellProjectorR_fixed_iff
#print axioms TGLExt.TestemunhaEstatica.psionFlow_fixed_iff_coord_fixed
#print axioms TGLExt.TestemunhaEstatica.the_static_set_is_the_psion_line
#print axioms TGLExt.TestemunhaEstatica.the_global_witness_is_false
#print axioms TGLExt.TestemunhaEstatica.the_psion_line_is_inhabited
#print axioms TGLExt.TestemunhaEstatica.the_flow_delivers_to_the_psion
#print axioms TGLExt.TestemunhaEstatica.bellUnit_orthonormal
#print axioms TGLExt.TestemunhaEstatica.bellUnit_complete
#print axioms TGLExt.TestemunhaEstatica.bellUnit_zero_is_the_bell_vector
#print axioms TGLExt.TestemunhaEstatica.bellUnit_eigen
#print axioms TGLExt.TestemunhaEstatica.psionLine_iff_fixed_by_the_corner
#print axioms TGLExt.TestemunhaEstatica.the_static_witness_bridge
#print axioms TGLExt.TestemunhaEstatica.psionCollapse
#print axioms TGLExt.TestemunhaEstatica.the_collapse_of_the_psion_echoes_its_identity
#print axioms TGLExt.TestemunhaEstatica.the_collapse_of_the_psion_cannot_be_self_attested
#print axioms TGLExt.TestemunhaEstatica.the_psion_inhabits_the_static_witness
