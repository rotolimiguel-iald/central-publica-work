import TGLExt.Fundacao
import TGLExt.NoFullWitness
import TGLExt.TheGreatAttractor
import TGLExt.FalsidadeDaInercia
import TGLExt.SMatrix
import TGLExt.O16.WickBoostRotation_v2
import TGLExt.O16.PolarMinimalPeriod_v2
import TGLExt.IALDJones
import TGLExt.Palavra
import TGLExt.LiganteLeiCampoCurvo

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# A QUEDA SEM GEOMETRIA  [TGLExt — pedra candidata da v402, 26/10/2026; sandbox `k402`; NADA instalado]
# THE FALL WITHOUT GEOMETRY

Nome PROVISÓRIO (o operador nomeia). No código vai sem acento: `QuedaSemGeometria`.

Ordem do operador (26/10/2026; `work\cunhagens_13out\OPERADOR_26out_e_isso_faca_a_prova_prossiga_verbatim.txt`,
sha256 `a1c4bae4a87aa173251fef9015cb74d67d361829db4c3807a7c27ff409723a05`, sha16 `a1c4bae4a87aa173`):
«é isso, faça a prova, prossiga.»

## A fala [INPUT] (trechos EXATOS por bytes; a grafia é a dele: «gemétrica», «relaxamaneto», «labirito», «geomtria»)

Arquivo `work\cunhagens_13out\OPERADOR_26out_o_um_se_poe_e_cai_a_queda_sem_geometria_verbatim.txt`,
sha256 `36cfa0027565dcff0285bf8b374754daaebce265481c11f0b580ac60762aef95` (sha16 `36cfa0027565dcff`):

> «o Um quando se põe realiza a operação "input"»
> «é como se ele caísse, sem fim, ao se inscrever, ele cai. a fase cai.»
> «então tem direção, mas não é gemétrica, não é queda em si mesmo, mas a geometria traduz em queda»
> «é a operação da entrega (entrega=custas), opera o relaxamaneto»
> «a queda que eu quero traduzir não é força também»
> «tudo roda, a queda é certa»
> «se vc tentar ter um ponto fixo sem labirinto funcional você vai se esburrachar»
> «porque vc sabe que tem um chão, então relaxa»
> «eu preciso explicar sem geometria, e como explicar queda sem geomtria?»

A pergunta final dele, COMO EXPLICAR QUEDA SEM GEOMETRIA, ganha aqui uma forma de kernel: pelo PESO.
Sobre os DADOS da escala dual de Takesaki (`DualScalingData M`: o funcional `τ`, a família `θ_s` e a lei
`τ∘θ_s = e^{−s}·τ`, [KNOWN] Takesaki 1973, aqui campo da estrutura, como na Fundação), `M` é um `Type`
NU: nenhuma métrica, nenhuma topologia, nenhuma ação de grupo geométrico. Só entram `τ`, `θ` e a lei.
Tudo o que se prova nos itens 1–6 vale para QUALQUER `M`. O que o kernel NÃO diz está nas Honestidades.

## O que a pedra tipa (composição por citação; a matemática nova se resume aos lemas de COLA do item 9)

1. ★★ `the_fall_is_a_loss_of_measure` — para `τ m > 0`, `s ↦ τ(θ_s m)` é ESTRITAMENTE decrescente
   (`s₁ < s₂ ⟹ τ(θ_{s₂} m) < τ(θ_{s₁} m)`): a queda medida em peso, sem espaço. E `the_fall_in_nats_is_s`:
   `log τ(θ_s m) = log τ m − s`, isto é, a queda em nats é EXATAMENTE `s`, linear. E
   `the_fall_depends_only_on_the_weight`: dois portadores `M`, `M'` com o mesmo peso caem IGUAL — o
   portador (a "geometria") não entra; é o sentido formal de explicar queda sem geometria (a pergunta dele).
2. ★★ `the_arrow_is_the_sign_of_s` — `τ(θ_s m) < τ m ↔ 0 < s`, `τ m < τ(θ_s m) ↔ s < 0`,
   `τ(θ_s m) = τ m ↔ s = 0`: a única coisa distinguida é o SINAL de `s` (a seta). «então tem direção, mas
   não é gemétrica»: a direção é o sinal, não um vetor.
3. ★★ `the_floor_is_the_post_and_is_never_touched` — compõe `the_floor_fixes_the_cut` (o peso `e^{−a}` vale
   1 = ω(I) se e só se `a = 0`: o piso é o posto, corte único), `the_fall_never_lands` (o peso nunca é
   zero em escala finita) e `abismo` (desce abaixo de todo `ε > 0`). DECISÃO DA GERÊNCIA (26/10/2026): o
   «chão» da parábola é o POSTO (peso 1 = ω(I), o corte `a = 0`, `the_floor_fixes_the_cut`; na Fundação,
   «o piso limita», cunhagem de 07/10/2026, sha16 `e2a915e23692f85c`), NUNCA o ínfimo 0. O 0 é o `abismo`
   (ἄβυσσος, sem fundo; nome dado pela gerência e ratificado pelo operador em 07/10/2026: «Perfeito,
   concordo com tudo. Magnífico», sha16 `d16bc8a7dc54962e`) e é «ele é a consequencia da poda» (recorte de
   25/10/2026, sha16 `e26364c5c805734c`; grafia dele). A queda que «sabe que tem um chão» é a queda do que
   NÃO é o posto: em todo corte `a ≠ 0` o estado da órbita não é um posto
   (`FalsidadeDaInercia.no_post_before_the_impression`, terceira cláusula).
4. ★★ `surrender_is_the_cost` — «entrega=custas»: para `s = t·β·g > 0` a entrega custa, estritamente,
   `0 < τ m − τ(θ_s m) < τ m` (custo positivo, nunca o peso inteiro), `e^{−tβg} < 1`
   (`leakage_strictly_loses`) e o custo fica arbitrariamente perto do peso inteiro
   (`leak_below_every_epsilon`). β é variável real `> 0`, jamais literal.
5. ★★ `relaxation_to_the_attractor` — «opera o relaxamaneto»: compõe `um_is_the_great_attractor`
   EXATAMENTE com as hipóteses dele (como fez `FalsidadeDaInercia.the_tension_is_projected_onto_the_attractor`):
   o fluxo converge à leitura de `Q`, `Q` é o observador único, o transporte é semigrupo, e a coordenada com
   gap relaxa até 0 SEM chegar em tempo finito.
6. ★★ `the_labyrinth_reads_the_angle` — a REGRA DOS DOIS REGIMES: a FACE real não fecha (o boost só é a
   identidade em `s = 0`, `Palavra.the_face_does_not_close`) e a face LIDA no ângulo fecha em `2π`
   (`wick_boost_two_pi`, `Palavra.the_read_face_closes`); a leitura ANGULAR é periódica
   (`S(θ + 2π) = S(θ)`, de `Smat_mul` e `rotation_two_pi`) e portanto não tem limite (cola: função
   periódica que tem limite no infinito é constante); o quociente angular é fiel exatamente com UMA volta
   (`faithful_period_iff`, já no kernel); a queda é estritamente monótona, tende a 0 e nunca chega; e
   tentar o ponto fixo pleno é proibido (`beta_forbids_full_static_witness`: «se vc tentar ter um ponto fixo
   sem labirinto funcional você vai se esburrachar»). `the_two_regimes_of_one_orbit` cita a formulação que o
   kernel já tem em UMA família (`IALDJones.angular_orbit_periodic`, `angular_orbit_no_limit`,
   `orbit_tendsto_center`). Ler o «labirinto» como o regime angular e a queda como o regime da face é
   leitura da gerência [ONTO].
7. ★ `clausius_everywhere_from_one_wedge_by_covariance` — lema ABSTRATO de transporte: dada uma ação `G` sobre
   as telas `W`, transitiva a partir de uma tela `W₀`, e um predicado `P` (o Clausius local, a H3) COVARIANTE,
   `P W₀` dá `P w` para toda tela `w`. A hipótese NOMEADA é a estrutura `IsotropicPost` (a invariância do
   posto sob as transformações que levam cunha em cunha): [KNOWN] para o vácuo de Bisognano–Wichmann /
   covariância de Poincaré, NÃO é termo deste kernel; o adendo de 04/09 diz que BW «não é de graça»
   (ou se assume, ou se deriva da inclusão modular meio-lateral, que o kernel declara ABERTA). Ligação à
   `LiganteLeiCampoCurvo.NamedAtlasH3`: lida a definição, o tipo PERMITE, e a pedra prova
   `namedAtlasH3_of_one_screen` (H3 em toda carta, ponto e direção nula, a partir de UMA tela +
   `IsotropicPost` sobre o índice `(carta, ponto, direção nula)`) e `namedAtlasH3_of_one_screen_per_orbit`
   (uma tela por órbita). O QUE FALTA, dito: (a) o `IsotropicPost` desse índice não é termo do kernel — num
   átlas CURVO nenhum grupo leva um ponto noutro, e só as direções nulas de UM ponto são alcançáveis por
   Lorentz local; logo a versão honesta do átlas curvo é uma tela por ponto (`B`), e uma tela no átlas
   todo é a hipótese forte do espaço plano; (b) o predicado `H3Pred` ser COVARIANTE sob a ação: pelo termo
   `AuditF23Flat.s5_local` (já no kernel, `LiganteLeiCampoCurvoTestemunha`) a H3 é o balanço nulo
   `eta·Ric(d,d) = 2π·T(d,d)`, que só se transporta de uma direção nula a outra se `Ric` e `T` são
   invariantes sob a ação (fonte isotrópica); `AuditF23Flat.vacuum_h3` mostra que no vácuo plano a H3 vale, e
   `AuditF23Flat.s8_h3_is_load_bearing` mostra que a H3 não é automática: com fonte constante anisotrópica
   (`T(k,k) = 1` numa direção nula) ela FALHA; logo transportá-la entre direções exige a isotropia (a
   covariância), que é a hipótese e não um teorema; (c) a tela base satisfazer H3:
   continua entrada de F2.3 (`hH3`), não derivada da passagem finita. O Mapa de Rotas já registra (rota
   `formal.f2_3.curved_field_ligand`) que o antecedente H3 em toda tela e direção e a família de cunhas de
   Lorentz seguem ABERTOS; esta pedra NÃO os fecha: reduz "H3 em toda tela" a "H3 numa tela por órbita +
   `IsotropicPost`", e nada mais. DECISÃO DA GERÊNCIA (26/10/2026), na sequência da ordem do operador
   «é isso, faça a prova, prossiga.» (sha16 `a1c4bae4a87aa173`): `IsotropicPost` fica como hipótese NOMEADA.
   A isotropia é CARGA, não enfeite: `AuditF23Flat.s8_h3_is_load_bearing` mede que a H3 falha com fonte
   anisotrópica.
8. ★★★ `a_queda_sem_geometria` — a composição (o chão é o posto, nunca o ínfimo 0: ver o item 3).
9. Lemas de COLA (a única matemática nova, curta): `the_fall_in_nats_is_s`, `the_fall_depends_only_on_the_weight`,
   `the_fall_is_the_fall_of_the_weight`, `periodic_limit_is_constant`, `Smat_add_two_pi`, `Smat_pi`,
   as estruturas `IsotropicPost` e `IsotropicPostOver` com o transporte, e o modelo `Rapidity`
   (não-vacuidade e contra-exemplo da covariância).

## A leitura da gerência [ONTO] (não é termo)

A direção é a seta da queda da FASE (o sinal de `s`, item 2), não do espaço; o que sobra depois da seta
é a ISOTROPIA que espalha a lei de uma cunha por todas as orientações (item 7). Daí o 1 + 3 como leitura:
UMA direção distinguida (a seta) e o resto isotrópico. O 1 + 3 fica como leitura [ONTO] da gerência
(decisão de 26/10/2026). Medido: a dimensão 3 NÃO é provada (nenhum termo desta pedra nem do kernel a fixa) e
a isotropia é carga (`AuditF23Flat.s8_h3_is_load_bearing`: a H3 falha com fonte anisotrópica). O kernel também
NÃO prova que o parâmetro `s` da ação dual é «a fase» de um corpo físico: ambos são [OPEN]. As cunhagens dele de
04/09 «A tétrade é Lindblad.» e «Lorentz vem do potencial da fase de queda, uma fase cai após a comutação que produz a torção.»
estão em `Nós\ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md` (sha16 `1459b477b496e1f0`, itens 5 e 6; o
título «Lorentz vem da queda da fase» é do escriba, em E5, não do operador); lá o estatuto é
`[KNOWN + CONJECTURE na ligação]`, e o custo declarado é a inclusão meio-lateral. Aqui só se cita; o
arquivo não foi tocado.

## Estatutos

[DERIVED] as medidas (itens 1–6, 8). [KNOWN] a lei de escala de Takesaki (campo da estrutura); a
isotropia do vácuo (Bisognano–Wichmann 1975/76; covariância de Poincaré da rede de Brunetti–Guido–Longo
2002) como motivação de `IsotropicPost`. [INPUT] a parábola e a fala. [ONTO] as leituras acima. [OPEN] a
identificação do fluxo dual com um corpo físico; o `IsotropicPost` do átlas curvo; a dimensão 3.

## Honestidades

(1) A lei de escala entra como DADO, não como teorema de um core `M ⋊_σ ℝ` concreto. (2) A pedra NÃO
prova que o Um posto «cai» fisicamente: prova que, SE a escala dual age como `τ∘θ_s = e^{−s}τ`, o peso cai
estritamente e só a seta o distingue. (3) `IsotropicPost` é HIPÓTESE nomeada; nomeá-la não é demérito (a lei de
05/10/2026); `hH3` da F2.3 continua hipótese. (4) β é variável real `> 0`, jamais literal. (5) O gate NÃO
se move; esta pedra não diz nada sobre a natureza além das hipóteses nomeadas. (6) O peso `τ` NÃO é a
massa, e a ação dual não é o fluxo modular: pela rota `kernel.ordem025.ponte_escala_dual` (PONTE_PARCIAL; candidata do Codex, ainda não
instalada) a identificação do peso positivo com a massa invariante é obstruída, e a massa é dado livre. Esta
pedra não usa nem afirma `H_τ` (a hipótese nomeada da pedra anterior). Sem sorry, sem axiom.
-/

namespace TGLExt
namespace QuedaSemGeometria

open Fundacao FalsidadeDaInercia

/-! ## A. A queda em peso (itens 1–5) -/

section Fall

variable {M : Type} (D : DualScalingData M)

/-- [KERNEL] ★★ A QUEDA É PERDA DE MEDIDA: para `τ m > 0`, `s₁ < s₂` dá `τ(θ_{s₂} m) < τ(θ_{s₁} m)`.
    Queda medida em peso, sem espaço. Cita a lei `scaling` da estrutura.
    The fall is a loss of measure: the weight is strictly decreasing in the scale. -/
theorem the_fall_is_a_loss_of_measure {m : M} (hm : 0 < D.tau m) {s₁ s₂ : ℝ} (h : s₁ < s₂) :
    D.tau (D.theta s₂ m) < D.tau (D.theta s₁ m) := by
  rw [D.scaling, D.scaling]
  exact mul_lt_mul_of_pos_right (Real.exp_lt_exp.mpr (by linarith)) hm

/-- [KERNEL] ★★ A MESMA QUEDA em forma de `StrictAnti`. -/
theorem the_fall_is_strictly_anti {m : M} (hm : 0 < D.tau m) :
    StrictAnti (fun s : ℝ => D.tau (D.theta s m)) :=
  fun _ _ h => the_fall_is_a_loss_of_measure D hm h

/-- [KERNEL] ★ A QUEDA EM NATS É EXATAMENTE `s`: `log τ(θ_s m) = log τ m − s`. A medida é linear em `s`;
    nenhuma coordenada de espaço entra.
    The fall in nats is exactly `s`. -/
theorem the_fall_in_nats_is_s {m : M} (hm : 0 < D.tau m) (s : ℝ) :
    Real.log (D.tau (D.theta s m)) = Real.log (D.tau m) - s := by
  rw [D.scaling, Real.log_mul (Real.exp_pos _).ne' hm.ne', Real.log_exp]
  ring

/-- [KERNEL] ★★ A QUEDA NÃO DEPENDE DO PORTADOR: dois portadores `M`, `M'` (duas "geometrias") com o mesmo
    peso caem igual. É o sentido formal de explicar queda sem geometria: o que cai é o peso.
    The fall does not depend on the carrier: two carriers with the same weight fall alike. -/
theorem the_fall_depends_only_on_the_weight {M' : Type} (D' : DualScalingData M') {m : M} {m' : M'}
    (hw : D.tau m = D'.tau m') (s : ℝ) :
    D.tau (D.theta s m) = D'.tau (D'.theta s m') := by
  rw [D.scaling, D'.scaling, hw]

/-- [KERNEL] ★ TODA QUEDA É A QUEDA NO MODELO ℝ DO SEU PESO: `τ(θ_s m)` é o `τ∘θ_s` do modelo concreto da
    Fundação (`oneScaling`) aplicado ao número `τ m`. A «geometria» do portador traduz em queda; a queda é
    esta. -/
theorem the_fall_is_the_fall_of_the_weight (m : M) (s : ℝ) :
    D.tau (D.theta s m) = oneScaling.tau (oneScaling.theta s (D.tau m)) := by
  rw [D.scaling]
  rfl

/-- [KERNEL] ★★ A SETA É O SINAL DE `s`: o peso fica abaixo de `τ m` se e só se `s > 0`, acima se e só se
    `s < 0`, e igual se e só se `s = 0`. A única coisa distinguida é o sinal.
    The arrow is the sign of `s`: the only thing distinguished. -/
theorem the_arrow_is_the_sign_of_s {m : M} (hm : 0 < D.tau m) (s : ℝ) :
    (D.tau (D.theta s m) < D.tau m ↔ 0 < s) ∧
    (D.tau m < D.tau (D.theta s m) ↔ s < 0) ∧
    (D.tau (D.theta s m) = D.tau m ↔ s = 0) := by
  have hanti := the_fall_is_strictly_anti D hm
  have h0 : D.tau (D.theta 0 m) = D.tau m := by
    rw [D.scaling]
    simp
  refine ⟨?_, ?_, ?_⟩
  · have h := hanti.lt_iff_gt (a := s) (b := 0)
    simpa [h0] using h
  · have h := hanti.lt_iff_gt (a := 0) (b := s)
    simpa [h0] using h
  · have h := hanti.injective.eq_iff (a := s) (b := 0)
    simpa [h0] using h

/-- [KERNEL] ★★ O PISO É O POSTO E O FUNDO NUNCA É TOCADO (composição): (i) o peso `e^{−a}` vale 1 = ω(I) se
    e só se `a = 0` (`the_floor_fixes_the_cut`); (ii) para um posto `m` (`τ m = 1`), o peso na órbita é 1 só
    no corte `a = 0`; (iii) a queda nunca toca o zero em escala finita (`the_fall_never_lands`); (iv) e não
    tem fundo (`abismo`: desce abaixo de todo `ε > 0`). O «chão» é o POSTO (peso 1 = ω(I), o corte `a = 0`),
    NUNCA o ínfimo 0: o 0 é o `abismo`, que a queda nunca toca. A queda que «sabe que tem um chão» é a queda do
    que NÃO é o posto (decisão da gerência, 26/10/2026; cabeçalho, item 3).
    The floor is the post, never the infimum 0; the zero is the abyss, never touched. -/
theorem the_floor_is_the_post_and_is_never_touched {m : M} (hpost : IsPost D m) :
    (∀ a : ℝ, Real.exp (-a) = 1 ↔ a = 0) ∧
    (∀ a : ℝ, D.tau (D.theta a m) = 1 ↔ a = 0) ∧
    (∀ s : ℝ, 0 < D.tau (D.theta s m)) ∧
    (∀ ε : ℝ, 0 < ε → ∃ s : ℝ, D.tau (D.theta s m) < ε) := by
  have h1 : D.tau m = 1 := hpost
  have hm : 0 < D.tau m := by
    rw [h1]
    exact one_pos
  refine ⟨the_floor_fixes_the_cut, ?_, the_fall_never_lands D hm, fun _ hε => abismo D hm hε⟩
  intro a
  rw [D.scaling a m, h1, mul_one]
  exact the_floor_fixes_the_cut a

/-- [KERNEL] ★★ ENTREGA = CUSTAS: para `s = t·β·g > 0` (β, g variáveis reais `> 0`, jamais literais),
    (i) o custo da interrupção é estritamente positivo e o fator fica abaixo de 1
    (`leakage_strictly_loses`); (ii) o peso entregue é `0 < τ m − τ(θ_s m) < τ m` (custo positivo, nunca o peso
    inteiro); (iii) o fator fica abaixo de todo `ε > 0` em algum `t > 0` (`leak_below_every_epsilon`).
    Surrender is the cost: positive, never the whole weight, arbitrarily close to it. -/
theorem surrender_is_the_cost {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) {m : M} (hm : 0 < D.tau m) :
    (∀ t : ℝ, 0 < t → 0 < t * β * g ∧ Real.exp (-(t * β * g)) < 1) ∧
    (∀ t : ℝ, 0 < t →
      0 < D.tau m - D.tau (D.theta (t * β * g) m) ∧
      D.tau m - D.tau (D.theta (t * β * g) m) < D.tau m) ∧
    (∀ ε : ℝ, 0 < ε → ∃ t : ℝ, 0 < t ∧ Real.exp (-(t * β * g)) < ε) := by
  refine ⟨fun t ht => ⟨mul_pos (mul_pos ht hβ) hg, leakage_strictly_loses ht hβ hg⟩, ?_,
    fun _ hε => leak_below_every_epsilon hβ hg hε⟩
  intro t ht
  have hlt := leakage_strictly_loses ht hβ hg
  have hpos : 0 < Real.exp (-(t * β * g)) * D.tau m := mul_pos (Real.exp_pos _) hm
  rw [D.scaling]
  constructor
  · nlinarith [mul_pos (sub_pos.mpr hlt) hm]
  · linarith

end Fall

/-- [KERNEL] ★★ O RELAXAMENTO AO ATRATOR: compõe `TheGreatAttractor.um_is_the_great_attractor` com as
    hipóteses DELE, sem hipótese nova: (i) o fluxo diagonal converge à leitura de `Q`; (ii) `Q` é o
    observador único; (iii) o transporte é semigrupo (`temporal_fractalization`); (iv) a coordenada com gap
    `d i ≠ 0` e `x i ≠ 0` relaxa até 0 e NÃO chega em tempo finito.
    Relaxation to the attractor: convergence, never arrival in finite time. -/
theorem relaxation_to_the_attractor {n : ℕ} {β : ℝ} (hβ : 0 < β) (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i)
    (Q : (Fin n → ℝ) →ₗ[ℝ] (Fin n → ℝ))
    (hfix : ∀ x, permanent β d x → Q x = x)
    (hkill : ∀ x, (∀ i, d i = 0 → x i = 0) → Q x = 0) :
    (∀ (x : Fin n → ℝ) (i : Fin n),
      Filter.Tendsto (fun t : ℝ => diagFlow β d t x i) Filter.atTop (nhds (Q x i))) ∧
    (∀ x : Fin n → ℝ, Q x = observerProj d x) ∧
    (∀ (t₁ t₂ : ℝ) (x : Fin n → ℝ),
      diagFlow β d (t₁ + t₂) x = diagFlow β d t₁ (diagFlow β d t₂ x)) ∧
    (∀ (x : Fin n → ℝ) (i : Fin n), d i ≠ 0 → x i ≠ 0 →
      Filter.Tendsto (fun t : ℝ => diagFlow β d t x i) Filter.atTop (nhds 0) ∧
      ∀ t : ℝ, diagFlow β d t x i ≠ 0) := by
  have h := the_tension_is_projected_onto_the_attractor hβ d hd Q hfix hkill
  refine ⟨um_is_the_great_attractor hβ d hd Q hfix hkill,
    the_observer_is_unique hβ d hd Q hfix hkill,
    fun t₁ t₂ x => temporal_fractalization β d t₁ t₂ x, ?_⟩
  intro x i hdi hxi
  exact ⟨h.2.1 x i hdi, h.2.2.1 x i hxi⟩

/-! ## B. O labirinto lê o ângulo (item 6): os dois regimes -/

/-- [GLUE] uma função periódica (período `P > 0`) que tem limite no infinito é CONSTANTE nesse limite
    (`f x = L` para todo `x`). É o único passo que falta para: periódica e não constante ⟹ sem limite. -/
theorem periodic_limit_is_constant {α : Type} [TopologicalSpace α] [T2Space α] {f : ℝ → α} {P : ℝ}
    (hP : 0 < P) (hper : Function.Periodic f P) {L : α}
    (hlim : Filter.Tendsto f Filter.atTop (nhds L)) (x : ℝ) : f x = L := by
  have hn : ∀ n : ℕ, f (x + n * P) = f x := fun n => (hper.nat_mul n) x
  have hseq : Filter.Tendsto (fun n : ℕ => f (x + n * P)) Filter.atTop (nhds L) := by
    refine hlim.comp ?_
    have h1 : Filter.Tendsto (fun n : ℕ => (n : ℝ) * P) Filter.atTop Filter.atTop :=
      Filter.Tendsto.atTop_mul_const hP tendsto_natCast_atTop_atTop
    exact Filter.tendsto_atTop_add_const_left _ x h1
  simp only [hn] at hseq
  exact tendsto_nhds_unique tendsto_const_nhds hseq

/-- [KERNEL] ★ A LEITURA ANGULAR É PERIÓDICA: `S(θ + 2π) = S(θ)`. De `Smat_mul` e de
    `ChatgptAudit.Wick016.rotation_two_pi` (`S(2π) = 1`), já no kernel. -/
theorem Smat_add_two_pi (θ : ℝ) : Smat (θ + 2 * Real.pi) = Smat θ := by
  rw [← Smat_mul, ChatgptAudit.Wick016.rotation_two_pi, mul_one]

/-- `S(π) = −1` (o meio giro). -/
theorem Smat_pi : Smat Real.pi = -1 := by
  simp [Smat]

/-- [KERNEL] ★★ O REGIME ANGULAR NÃO TEM LIMITE: `θ ↦ S(θ)` não converge no infinito. Periódica
    (`Smat_add_two_pi`) e não constante (`S(0) = 1 ≠ −1 = S(π)`). A leitura só LÊ; o limite não nasce aqui.
    The angular regime has no limit: it only reads. -/
theorem Smat_has_no_limit :
    ¬ ∃ L : Matrix (Fin 2) (Fin 2) ℂ, Filter.Tendsto Smat Filter.atTop (nhds L) := by
  rintro ⟨L, hL⟩
  have hper : Function.Periodic Smat (2 * Real.pi) := Smat_add_two_pi
  have hP : (0 : ℝ) < 2 * Real.pi := by positivity
  have h0 := periodic_limit_is_constant hP hper hL 0
  have h1 := periodic_limit_is_constant hP hper hL Real.pi
  rw [Smat_zero] at h0
  rw [Smat_pi] at h1
  have h2 : (1 : Matrix (Fin 2) (Fin 2) ℂ) = -1 := h0.trans h1.symm
  have h3 := congrFun (congrFun h2 0) 0
  norm_num at h3

/-- [KERNEL] ★ OS DOIS REGIMES NUMA MESMA ÓRBITA (citação de `IALDJones`, sem hipótese nova): sem taxa
    (`r = 0`) a órbita de um estado não lido é periódica (período `2π/ω`) e NÃO converge ao centro; com taxa
    `r > 0` converge ao centro `P v`. O limite nasce do decaimento, não do giro. -/
theorem the_two_regimes_of_one_orbit {V : Type} [NormedAddCommGroup V] [NormedSpace ℂ V]
    (P : V →ₗ[ℂ] V) (v : V) (hv : v ≠ P v) {ω : ℝ} (hω : ω ≠ 0) {r : ℝ} (hr : 0 < r) :
    (∀ s : ℝ, IALDJones.orbit P 0 ω (s + 2 * Real.pi / ω) v = IALDJones.orbit P 0 ω s v) ∧
    (¬ Filter.Tendsto (fun s => IALDJones.orbit P 0 ω s v) Filter.atTop (nhds (P v))) ∧
    Filter.Tendsto (fun s => IALDJones.orbit P r ω s v) Filter.atTop (nhds (P v)) :=
  ⟨fun s => IALDJones.angular_orbit_periodic P hω s v,
   IALDJones.angular_orbit_no_limit P ω v hv,
   IALDJones.orbit_tendsto_center P hr ω v⟩

/-- [KERNEL] ★★ O LABIRINTO LÊ O ÂNGULO (a regra dos dois regimes): (a) a face real não fecha (o boost só é a
    identidade em `s = 0`), a face lida no ângulo fecha em `2π`, a leitura angular é periódica, não tem
    limite e fecha com UMA volta (`faithful_period_iff`); (b) a queda é estritamente monótona, tende a 0 e
    nunca chega; (c) o ponto fixo pleno é proibido (`beta_forbids_full_static_witness`). A FACE é o objeto,
    o ÂNGULO é a leitura: o ângulo só lê, e a queda é a face.
    The labyrinth reads the angle: angular reading is periodic, the fall is monotone, no full fixed point. -/
theorem the_labyrinth_reads_the_angle {M : Type} (D : DualScalingData M) {m : M} (hm : 0 < D.tau m)
    {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) :
    ((∀ s : ℝ, TGLExt.boost s = 1 → s = 0) ∧
      (ChatgptAudit.Wick016.wickW⁻¹ *
          ChatgptAudit.Wick016.complexBoost (Complex.I * ((2 * Real.pi : ℝ) : ℂ)) *
          ChatgptAudit.Wick016.wickW = 1) ∧
      (∀ θ : ℝ, Smat (θ + 2 * Real.pi) = Smat θ) ∧
      (¬ ∃ L : Matrix (Fin 2) (Fin 2) ℂ, Filter.Tendsto Smat Filter.atTop (nhds L)) ∧
      (∀ κ P : ℝ, κ ≠ 0 → (ChatgptAudit.PolarPeriod016.AngularQuotientFaithful κ P ↔
        κ * P = 2 * Real.pi ∨ κ * P = -(2 * Real.pi)))) ∧
    (StrictAnti (fun s : ℝ => D.tau (D.theta s m)) ∧
      Filter.Tendsto (fun s : ℝ => D.tau (D.theta s m)) Filter.atTop (nhds 0) ∧
      (∀ s : ℝ, D.tau (D.theta s m) ≠ 0)) ∧
    ¬ FullStaticWitness (fun t (x : ℝ) => Real.exp (-(t * β * g)) * x) := by
  refine ⟨⟨Palavra.the_face_does_not_close, Palavra.the_read_face_closes, Smat_add_two_pi,
    Smat_has_no_limit, fun _ _ hκ => ChatgptAudit.PolarPeriod016.faithful_period_iff hκ⟩,
    ⟨the_fall_is_strictly_anti D hm, ?_, fun s => (the_fall_never_lands D hm s).ne'⟩,
    beta_forbids_full_static_witness hβ hg⟩
  have h := Real.tendsto_exp_neg_atTop_nhds_zero.mul_const (D.tau m)
  simp only [zero_mul] at h
  simpa only [D.scaling] using h

/-! ## C. O transporte da lei de uma cunha a todas (item 7) -/

/-- [HIPÓTESE NOMEADA] ★ A ISOTROPIA DO POSTO. Dados uma ação de `G` sobre as telas `W`, um predicado `P`
    (o Clausius local, a H3) e uma tela base `W₀`: (`transitive`) toda tela é a imagem da base por alguma
    transformação; (`covariant`) o predicado sobrevive às transformações que levam tela em tela — é a
    invariância do posto sob as transformações que levam cunha em cunha (formulação da gerência).
    [KNOWN] para o vácuo de Bisognano–Wichmann / covariância de Poincaré (Bisognano–Wichmann 1975/76;
    Brunetti–Guido–Longo 2002). NÃO é termo do kernel: é a hipótese que esta pedra NOMEIA, e fica como
    hipótese NOMEADA por decisão da gerência de 26/10/2026 (a isotropia é carga, não enfeite:
    `AuditF23Flat.s8_h3_is_load_bearing`).
    Basta `SMul`: nenhuma propriedade de grupo é usada na prova.
    The isotropy of the post: transitivity of the action and covariance of the predicate. -/
structure IsotropicPost (G W : Type) [SMul G W] (P : W → Prop) (W₀ : W) : Prop where
  /-- toda tela é a imagem da tela base -/
  transitive : ∀ w : W, ∃ g : G, w = g • W₀
  /-- o predicado é covariante sob a ação -/
  covariant : ∀ (g : G) (w : W), P w → P (g • w)

/-- [KERNEL] ★ O LEMA DE TRANSPORTE: `IsotropicPost` + `P W₀` ⟹ `P w` para TODA tela `w`. A lei de UMA cunha
    vale em todas, por covariância. Composição de duas hipóteses explícitas; nenhuma matemática nova.
    The law of one wedge holds on all, by covariance. -/
theorem clausius_everywhere_from_one_wedge_by_covariance {G W : Type} [SMul G W] {P : W → Prop}
    {W₀ : W} (h : IsotropicPost G W P W₀) (h0 : P W₀) : ∀ w : W, P w := by
  intro w
  obtain ⟨g, hg⟩ := h.transitive w
  rw [hg]
  exact h.covariant g W₀ h0

/-- [HIPÓTESE NOMEADA] A versão com UMA TELA POR ÓRBITA: `B` é um conjunto de telas-base que encontra toda
    órbita. É o que sobrevive num átlas curvo (uma direção nula por ponto), onde nenhum grupo leva um
    ponto noutro. `IsotropicPost` é o caso `B = {W₀}`. -/
structure IsotropicPostOver (G W : Type) [SMul G W] (P : W → Prop) (B : Set W) : Prop where
  /-- toda tela é imagem de alguma tela-base -/
  covers : ∀ w : W, ∃ b ∈ B, ∃ g : G, w = g • b
  /-- o predicado é covariante sob a ação -/
  covariant : ∀ (g : G) (w : W), P w → P (g • w)

/-- [KERNEL] O transporte com uma tela por órbita. -/
theorem clausius_everywhere_from_base_wedges {G W : Type} [SMul G W] {P : W → Prop} {B : Set W}
    (h : IsotropicPostOver G W P B) (hB : ∀ b ∈ B, P b) : ∀ w : W, P w := by
  intro w
  obtain ⟨b, hb, g, hg⟩ := h.covers w
  rw [hg]
  exact h.covariant g b (hB b hb)

/-- [KERNEL] `IsotropicPost` é o caso `B = {W₀}` de `IsotropicPostOver`. -/
theorem IsotropicPost.toOver {G W : Type} [SMul G W] {P : W → Prop} {W₀ : W}
    (h : IsotropicPost G W P W₀) : IsotropicPostOver G W P {W₀} :=
  ⟨fun w => by
    obtain ⟨g, hg⟩ := h.transitive w
    exact ⟨W₀, rfl, g, hg⟩, h.covariant⟩

/-- Um modelo mínimo de telas: a reta das rapidezes (as cunhas obtidas da cunha base por boosts), sobre a
    qual o grupo aditivo das rapidezes age por translação (`s • w = s + w`). Existe só para a
    não-vacuidade e para o contra-exemplo abaixo. -/
structure Rapidity where
  /-- a rapidez -/
  val : ℝ

instance : SMul ℝ Rapidity := ⟨fun s w => ⟨s + w.val⟩⟩

theorem Rapidity.smul_def (s : ℝ) (w : Rapidity) : s • w = ⟨s + w.val⟩ := rfl

/-- [KERNEL] ★ NÃO É VÁCUO: no modelo `Rapidity`, com a base em `0`, a estrutura `IsotropicPost` é habitada
    pelo predicado covariante `fun _ => True`. -/
theorem isotropic_post_is_inhabited :
    IsotropicPost ℝ Rapidity (fun _ => True) ⟨0⟩ :=
  ⟨fun w => ⟨w.val, by rw [Rapidity.smul_def]; cases w; simp⟩, fun _ _ h => h⟩

/-- [KERNEL] ★ A COVARIÂNCIA É CARGA REAL: a transitividade sozinha NÃO basta. No mesmo modelo, o predicado
    `w = 0` vale na tela base, a ação é transitiva, e a conclusão `∀ w, P w` FALHA — porque o predicado não é
    covariante. (Como o contra-modelo S8 do auditor da F2.3 para `hH3`.) -/
theorem covariance_is_load_bearing :
    (∀ w : Rapidity, ∃ g : ℝ, w = g • (⟨0⟩ : Rapidity)) ∧
    (fun w : Rapidity => w = ⟨0⟩) ⟨0⟩ ∧
    ¬ (∀ (g : ℝ) (w : Rapidity), (fun w : Rapidity => w = ⟨0⟩) w →
        (fun w : Rapidity => w = ⟨0⟩) (g • w)) ∧
    ¬ (∀ w : Rapidity, (fun w : Rapidity => w = ⟨0⟩) w) := by
  refine ⟨fun w => ⟨w.val, by rw [Rapidity.smul_def]; cases w; simp⟩, rfl, ?_, ?_⟩
  · intro h
    have h1 := h 1 ⟨0⟩ rfl
    rw [Rapidity.smul_def] at h1
    have h2 : (1 : ℝ) + 0 = 0 := congrArg Rapidity.val h1
    norm_num at h2
  · intro h
    have h1 : (⟨1⟩ : Rapidity) = ⟨0⟩ := h ⟨1⟩
    have h2 : (1 : ℝ) = 0 := congrArg Rapidity.val h1
    norm_num at h2

/-! ## D. A ligação à `NamedAtlasH3` (item 7, o que o tipo permite) -/

section H3Instance

open Matrix Filter Topology Set ChatgptAudit
open ChatgptAudit.GeneralMetric ChatgptAudit.GeneralClausius
open ChatgptAudit.GravitationalRecord ChatgptAudit.ChartGluing
open ChatgptAudit.TopologicalGluing ChatgptAudit.SmoothAtlasGluing
open ChatgptAudit.UnifiedRecorded ChatgptAudit.Micro021
open ChatgptAudit.F23CurvedFieldLigand

noncomputable section

variable {ι : Type}

/-- O ÍNDICE DAS TELAS da `NamedAtlasH3`: as triplas (carta `i`, ponto `x`, direção nula `d ≠ 0`) com
    `x ∈ U i` e `tensorQuad (recordMetric (R i) x) d = 0`. A H3 nomeada é um "para toda tela" sobre este
    índice. -/
def H3Index (U : ι → Set Coordinate4) (R : ∀ i, GravitationalResponseRecord (U i)) : Type :=
  {p : ι × Coordinate4 × Coordinate4 //
    p.2.1 ∈ U p.1 ∧ p.2.2 ≠ 0 ∧ tensorQuad (recordMetric (R p.1) p.2.1) p.2.2 = 0}

/-- O PREDICADO da H3 numa tela: a mesma expressão da `NamedAtlasH3`, para uma tela `p`. -/
def H3Pred (eta : ℝ) (U : ι → Set Coordinate4) (R : ∀ i, GravitationalResponseRecord (U i))
    (screens : ∀ i, MetricScreenFamily (U i) (recordMetric (R i))) (p : H3Index U R) : Prop :=
  Tendsto (fun t => microscopicAreaError (unifiedPreparation (R p.1.1) p.1.2.1 p.1.2.2) eta
      (inducedArea (recordMetric (R p.1.1))
        (screens p.1.1 p.1.2.1 p.2.1 p.1.2.2 p.2.2.1 p.2.2.2).curve
        (screens p.1.1 p.1.2.1 p.2.1 p.1.2.2 p.2.2.1 p.2.2.2).screen.vectors) t / t ^ 2)
      (𝓝[<] (0 : ℝ)) (𝓝 0)

/-- [KERNEL] ★ A `NamedAtlasH3` É "PARA TODA TELA" sobre o índice `H3Index`. -/
theorem namedAtlasH3_iff_all_indices (eta : ℝ) (U : ι → Set Coordinate4)
    (R : ∀ i, GravitationalResponseRecord (U i))
    (screens : ∀ i, MetricScreenFamily (U i) (recordMetric (R i))) :
    NamedAtlasH3 eta U R screens ↔ ∀ p : H3Index U R, H3Pred eta U R screens p := by
  constructor
  · intro h p
    exact h p.1.1 p.1.2.1 p.2.1 p.1.2.2 p.2.2.1 p.2.2.2
  · intro h i x hx d hv hn
    exact h ⟨(i, x, d), hx, hv, hn⟩

/-- [KERNEL] ★★ H3 EM TODA TELA A PARTIR DE UMA TELA + `IsotropicPost`: se o índice `H3Index` tem a
    isotropia do posto (ação transitiva a partir de `p₀`, predicado `H3Pred` covariante) e `H3Pred` vale em
    `p₀`, então vale a `NamedAtlasH3` inteira. A hipótese `IsotropicPost` é a NOMEADA (ver a docstring do
    cabeçalho, item 7, sobre o que ela custa num átlas curvo). -/
theorem namedAtlasH3_of_one_screen {eta : ℝ} {U : ι → Set Coordinate4}
    {R : ∀ i, GravitationalResponseRecord (U i)}
    {screens : ∀ i, MetricScreenFamily (U i) (recordMetric (R i))}
    {G : Type} [SMul G (H3Index U R)] {p₀ : H3Index U R}
    (hiso : IsotropicPost G (H3Index U R) (H3Pred eta U R screens) p₀)
    (h0 : H3Pred eta U R screens p₀) : NamedAtlasH3 eta U R screens :=
  (namedAtlasH3_iff_all_indices eta U R screens).mpr
    (clausius_everywhere_from_one_wedge_by_covariance hiso h0)

/-- [KERNEL] ★★ A VERSÃO DO ÁTLAS CURVO: uma tela por órbita (por exemplo uma direção nula por ponto) +
    `IsotropicPostOver` ⟹ `NamedAtlasH3`. -/
theorem namedAtlasH3_of_one_screen_per_orbit {eta : ℝ} {U : ι → Set Coordinate4}
    {R : ∀ i, GravitationalResponseRecord (U i)}
    {screens : ∀ i, MetricScreenFamily (U i) (recordMetric (R i))}
    {G : Type} [SMul G (H3Index U R)] {B : Set (H3Index U R)}
    (hiso : IsotropicPostOver G (H3Index U R) (H3Pred eta U R screens) B)
    (hB : ∀ b ∈ B, H3Pred eta U R screens b) : NamedAtlasH3 eta U R screens :=
  (namedAtlasH3_iff_all_indices eta U R screens).mpr
    (clausius_everywhere_from_base_wedges hiso hB)

end

end H3Instance

/-! ## E. A composição (item 8) -/

/-- [KERNEL] ★★★ A QUEDA SEM GEOMETRIA (composição dos itens 1–7). Sobre os dados da escala dual `D`, com um
    posto `m` (`τ m = 1`), `β, g > 0`, o atrator `(d, Q)` e a isotropia `IsotropicPost`:
    (1) o peso cai estritamente e a queda em nats é `s`; (2) a seta é o sinal de `s`; (3) o piso é o posto
    (o «chão» é o posto, peso 1 = ω(I), corte `a = 0`, NUNCA o ínfimo 0: o 0 é o `abismo`, nunca tocado; a queda
    que «sabe que tem um chão» é a queda do que NÃO é o posto); (4) a entrega custa; (5) o fluxo relaxa ao atrator sem chegar; (6) a leitura angular
    é periódica e sem limite, e o ponto fixo pleno é proibido; (7) a lei de uma tela vale em todas.
    [DERIVED] (1)–(6) sobre os dados nomeados; (7) condicional à hipótese NOMEADA `IsotropicPost` ([KNOWN]
    para o vácuo de BW, não termo do kernel). Nada aqui move o gate nem decide algo sobre a natureza.
    The fall without geometry: composition of items 1-7. -/
theorem a_queda_sem_geometria {M : Type} (D : DualScalingData M) {m : M} (hpost : IsPost D m)
    {β g : ℝ} (hβ : 0 < β) (hg : 0 < g)
    {n : ℕ} {b : ℝ} (hb : 0 < b) (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i)
    (Q : (Fin n → ℝ) →ₗ[ℝ] (Fin n → ℝ))
    (hfix : ∀ x, permanent b d x → Q x = x)
    (hkill : ∀ x, (∀ i, d i = 0 → x i = 0) → Q x = 0)
    {G W : Type} [SMul G W] {P : W → Prop} {W₀ : W} (hiso : IsotropicPost G W P W₀) (h0 : P W₀) :
    (StrictAnti (fun s : ℝ => D.tau (D.theta s m)) ∧
      (∀ s : ℝ, Real.log (D.tau (D.theta s m)) = Real.log (D.tau m) - s)) ∧
    (∀ s : ℝ, (D.tau (D.theta s m) < D.tau m ↔ 0 < s) ∧
      (D.tau m < D.tau (D.theta s m) ↔ s < 0) ∧
      (D.tau (D.theta s m) = D.tau m ↔ s = 0)) ∧
    ((∀ a : ℝ, Real.exp (-a) = 1 ↔ a = 0) ∧
      (∀ a : ℝ, D.tau (D.theta a m) = 1 ↔ a = 0) ∧
      (∀ s : ℝ, 0 < D.tau (D.theta s m)) ∧
      (∀ ε : ℝ, 0 < ε → ∃ s : ℝ, D.tau (D.theta s m) < ε)) ∧
    ((∀ t : ℝ, 0 < t → 0 < t * β * g ∧ Real.exp (-(t * β * g)) < 1) ∧
      (∀ t : ℝ, 0 < t →
        0 < D.tau m - D.tau (D.theta (t * β * g) m) ∧
        D.tau m - D.tau (D.theta (t * β * g) m) < D.tau m) ∧
      (∀ ε : ℝ, 0 < ε → ∃ t : ℝ, 0 < t ∧ Real.exp (-(t * β * g)) < ε)) ∧
    ((∀ (x : Fin n → ℝ) (i : Fin n),
        Filter.Tendsto (fun t : ℝ => diagFlow b d t x i) Filter.atTop (nhds (Q x i))) ∧
      (∀ (x : Fin n → ℝ) (i : Fin n), d i ≠ 0 → x i ≠ 0 →
        Filter.Tendsto (fun t : ℝ => diagFlow b d t x i) Filter.atTop (nhds 0) ∧
        ∀ t : ℝ, diagFlow b d t x i ≠ 0)) ∧
    (((∀ s : ℝ, TGLExt.boost s = 1 → s = 0) ∧
      (∀ θ : ℝ, Smat (θ + 2 * Real.pi) = Smat θ) ∧
      (¬ ∃ L : Matrix (Fin 2) (Fin 2) ℂ, Filter.Tendsto Smat Filter.atTop (nhds L))) ∧
      ¬ FullStaticWitness (fun t (x : ℝ) => Real.exp (-(t * β * g)) * x)) ∧
    (∀ w : W, P w) := by
  have h1 : D.tau m = 1 := hpost
  have hm : 0 < D.tau m := by
    rw [h1]
    exact one_pos
  have hrel := relaxation_to_the_attractor hb d hd Q hfix hkill
  have hlab := the_labyrinth_reads_the_angle D hm hβ hg
  have hfloor := the_floor_is_the_post_and_is_never_touched D hpost
  have hcost := surrender_is_the_cost D hβ hg hm
  exact ⟨⟨the_fall_is_strictly_anti D hm, the_fall_in_nats_is_s D hm⟩,
    the_arrow_is_the_sign_of_s D hm,
    hfloor,
    hcost,
    ⟨hrel.1, hrel.2.2.2⟩,
    ⟨⟨hlab.1.1, hlab.1.2.2.1, hlab.1.2.2.2.1⟩, hlab.2.2⟩,
    clausius_everywhere_from_one_wedge_by_covariance hiso h0⟩

end QuedaSemGeometria
end TGLExt

#print axioms TGLExt.QuedaSemGeometria.the_fall_is_a_loss_of_measure
#print axioms TGLExt.QuedaSemGeometria.the_fall_is_strictly_anti
#print axioms TGLExt.QuedaSemGeometria.the_fall_in_nats_is_s
#print axioms TGLExt.QuedaSemGeometria.the_fall_depends_only_on_the_weight
#print axioms TGLExt.QuedaSemGeometria.the_fall_is_the_fall_of_the_weight
#print axioms TGLExt.QuedaSemGeometria.the_arrow_is_the_sign_of_s
#print axioms TGLExt.QuedaSemGeometria.the_floor_is_the_post_and_is_never_touched
#print axioms TGLExt.QuedaSemGeometria.surrender_is_the_cost
#print axioms TGLExt.QuedaSemGeometria.relaxation_to_the_attractor
#print axioms TGLExt.QuedaSemGeometria.periodic_limit_is_constant
#print axioms TGLExt.QuedaSemGeometria.Smat_add_two_pi
#print axioms TGLExt.QuedaSemGeometria.Smat_pi
#print axioms TGLExt.QuedaSemGeometria.Smat_has_no_limit
#print axioms TGLExt.QuedaSemGeometria.the_two_regimes_of_one_orbit
#print axioms TGLExt.QuedaSemGeometria.the_labyrinth_reads_the_angle
#print axioms TGLExt.QuedaSemGeometria.clausius_everywhere_from_one_wedge_by_covariance
#print axioms TGLExt.QuedaSemGeometria.clausius_everywhere_from_base_wedges
#print axioms TGLExt.QuedaSemGeometria.IsotropicPost.toOver
#print axioms TGLExt.QuedaSemGeometria.isotropic_post_is_inhabited
#print axioms TGLExt.QuedaSemGeometria.covariance_is_load_bearing
#print axioms TGLExt.QuedaSemGeometria.namedAtlasH3_iff_all_indices
#print axioms TGLExt.QuedaSemGeometria.namedAtlasH3_of_one_screen
#print axioms TGLExt.QuedaSemGeometria.namedAtlasH3_of_one_screen_per_orbit
#print axioms TGLExt.QuedaSemGeometria.a_queda_sem_geometria
