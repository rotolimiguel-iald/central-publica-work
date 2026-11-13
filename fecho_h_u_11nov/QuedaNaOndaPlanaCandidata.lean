import TGLExt.AEscala
import TGLExt.FiniteEntropyAlgebra
import TGLExt.DiagonalStateCurve
import TGLExt.MicroscopicClausiusBridge
import TGLExt.QuadraticGibbsCurve
import TGLExt.GibbsMatterBridge
import TGLExt.PlaneWaveReconstructionControls

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 4000000

/-!
# (CANDIDATA, 11/11/2026) A queda numa onda plana: construção de um EXEMPLO
  [sandbox; fora do kernel canônico; nomes PROVISÓRIOS da gerência — o nome é do operador]

ESTE ARQUIVO É SUPERCONJUNTO de `QuedaComoCurvaDeEstadosCandidata.lean`: as PARTES 1 e 2 abaixo são
cópia fiel dele (mesmas definições e provas; namespace novo `TGLExt.QuedaOndaPlanaCandidata`; um
import a mais, `TGLExt.PlaneWaveReconstructionControls`), e a PARTE 3 (K4a, K4b, K4c) é o que se
acrescenta. Instalar um só dos dois.

O QUE A PARTE 3 É, SEM ENFEITE:

* é a CONSTRUÇÃO DE UM EXEMPLO, não um teste. O perfil da onda plana, `(a, c)`, é ESCOLHIDO para que
  o balanço `eta · (a + c) = 2π · gibbsCoupling (pesoDeGibbs custo s₀)` valha. O resultado é, portanto,
  EXISTÊNCIA POR ESCOLHA: a CONDIÇÃO do lado direito de K4a é satisfatível com Ricci e fonte não
  nulos (não-vacuidade). (R2, revisão de terceiro, achado 2: as hipóteses de regularidade, torção
  e nulidade já se cumprem para todo `(a, c)`, inclusive o plano; o que K4c mostra é a condição.)
  NÃO é derivação da geometria a partir da queda: a geometria é dada pelo kernel (`waveSolder`) e
  o perfil é escolhido;
* o cisalhamento da onda (`a − c`) fica LIVRE, e isso se vê no próprio K4a: a condição só envolve
  `a + c`. (R2, achado 3: `matched_curvature_distinguishes` e
  `state_alone_not_curvature_coordinate` dizem o mesmo para a família de AMPLITUDE da bancada, não
  para a queda; o análogo de amplitude deste exemplo já existe no kernel: `geometric_wave_curved`,
  `geometric_wave_matter_nonzero`.)
* `eta` não tem restrição de sinal no existencial (R2, achado 4). Para `eta < 0` sai `a = c < 0`,
  com Ricci negativo na direção nula e fonte não negativa: é só formal. A leitura de energia
  positiva seria a de `eta > 0` e NÃO é provada aqui;
* na direção nula paralela à onda (frequência zero) os dois lados do balanço somem e o limite vale
  com ou sem a condição: o conteúdo não trivial só existe para frequência não nula (R2, achado 5);
* o relógio quadrático `s = s₀(1 + t²)` e o acoplamento `gibbsCoupling` (variância modular sobre π)
  são os definidos pelo kernel, não derivados da queda (ver o cabeçalho da PARTE 2, K3d);
* não é `NamedAtlasH3` (outro tipo: registro de probabilidades), não é a lei de área em geral, não é a
  seta H3 do fecho. K4a é um SE E SÓ SE sobre a tela da origem; K4c-i vale em todo ponto e em toda
  direção nula, mas dentro da família da onda plana (`waveSolder a c`) e com o balanço como hipótese.

β_TGL não aparece. O gate não se move. Sem sorry, sem axiom.
-/

/-!
# (CANDIDATA, 11/11/2026) A queda como curva de estados diagonais
  [sandbox; fora do kernel canônico; nomes PROVISÓRIOS da gerência — o nome é do operador]

ESTE ARQUIVO TEM TRÊS PARTES (a terceira é a da onda plana, descrita no cabeçalho acima).

PARTE 1 — cópia fiel de `ClausiusDaQuedaCandidata.lean` (mesmas definições e provas, namespace novo
`TGLExt.QuedaOndaPlanaCandidata` para não colidir com o original). O cabeçalho original segue abaixo,
sem alteração. Diferenças reais em relação ao original: cinco imports a mais e `maxHeartbeats`
maior. Este arquivo é superconjunto do original: instalar um só.

PARTE 2 — o que se acrescenta (K1, K2, K3):

* K1 `aQuedaComoCurvaDeEstados` — habita `DiagonalStateCurve (pesoDeGibbs c s₀)` do kernel
  (`ChatgptAudit.Micro021`), com `weights t = pesoDeGibbs c (s₀ + t)` e a tangente dada pela derivada
  do peso (`tangenteDaQueda`); todos os campos provados;
* K2 `o_erro_de_area_da_queda` — o erro de área do kernel (`microscopicAreaError`) dessa curva é
  `(S(s₀+t) − S(s₀)) − η·(A t − A 0)`, com `S = entropiaDaQueda`;
* K3 — a comparação com a família de Gibbs do kernel (`quadraticGibbsCurve`, usada por
  `gibbs_area_matching_iff_ricci` e `einstein_from_gibbs_area_matching`): ver os teoremas da seção
  final e o que eles dizem e NÃO dizem.

HONESTIDADE (a régua; R2, revisão de terceiro, achados 2, 3 e 5): K1 a K3c são identidades de
famílias de pesos finitos e cálculo de somas. K3d e K3e INSTANCIAM teoremas geométricos do kernel
(Ricci, área induzida, balanço de horizonte, limites pela esquerda), e o dado geométrico (a tela `P`,
a métrica, a conexão, a regularidade, a direção nula) entra como HIPÓTESE: não há aqui testemunha de
que esses dados existam juntos. A curva `s = s₀(1+(ωt)²)` é o relógio quadrático IMPOSTO pela
construção do kernel, não derivado da queda (a curva linear falha, K3e). O acoplamento
`gibbsCoupling` é DEFINIDO no kernel como a variância modular sobre π: por isso o lado direito de
K3d casa com a resposta de entropia por construção; em termos da variância do custo ele não foi
calculado aqui. Nos casos degenerados (`s₀ = 0`, custo constante, `ω = 0`) o lado da queda some e
K3d reduz-se a uma condição só sobre a área e a curvatura. Nada disto é a lei de área, nem Clausius
de horizonte, nem a seta H3 do fecho: K3d é um SE E SÓ SE. β_TGL não aparece. O gate não se move;
sem sorry, sem axiom.
-/

/-!
# (CANDIDATA, 11/11/2026; R2 depois da revisão de terceiro) A identidade termodinâmica dos pesos da queda
  [sandbox; fora do kernel canônico; nomes PROVISÓRIOS da gerência — o nome é do operador]

O QUE É, SEM ENFEITE (correção da revisão de terceiro, achados 1 e 2, ALTO e MÉDIO):

* isto é a identidade canônica `d(log Z + s·E) = s·dE` da família de pesos `e^{−s·c(x)}/Z(s)`
  `[KNOWN]`. Ela vale para QUALQUER custo `c : X → ℕ` e a prova é cálculo de somas finitas;
* ela NÃO usa a identidade verbal (`IdentidadeVerbalCandidata`), nem `trava`, nem
  `opDaInstancia`. O que a liga à queda é um teorema do kernel, fora deste arquivo:
  `TraducaoTuring.a_norma_da_trava_e_a_particao` (`‖trava c t (uniforme X)‖² = Z(2t)/|X|`),
  de modo que o `s` daqui é o `2t` da trava;
* a "temperatura" `1/s` é a variável conjugada de `E` por definição: não há temperatura
  independente (em `s = 0` ela nem está definida). Por isso a igualdade é quase definicional;
* a SETA do fecho (`hH3`: da covariância do posto a Clausius em todo ponto e direção, na
  forma de ÁREA do F2.3, `NamedAtlasH3`) segue NÃO derivada. A primeira versão deste
  cabeçalho dizia que a seta era teorema no espaço do Tetelestai: dizia mais do que o tipo
  prova, e a gerência retira a frase.

O QUE PROVA:

* `pesoDeGibbs c s` — os pesos `e^{−s·c(x)}/Z(s)`; `pesos_de_gibbs_somam_um`;
* `custoMedio c s` — `E(s) = (Σ c·e^{−s c}) / Z(s)`; `entropiaDaQueda c s := log Z(s) + s·E(s)`;
* ★★ `a_entropia_da_queda_e_a_de_gibbs` — `entropiaDaQueda` É a entropia `−Σ p log p` dos pesos,
  na definição que o kernel usa no erro de área (`ChatgptAudit.finiteEntropy`);
* `hasDerivAt_particao`, `hasDerivAt_custoPesado`, `hasDerivAt_custoMedio` — as derivadas;
* ★★★ `clausius_da_queda` — `dS = s · dE`, a forma canônica (de Gibbs) da igualdade de Clausius;
  `clausius_da_queda_explicito` — a mesma, com a derivada do custo médio escrita.

HONESTIDADE (a régua): NÃO é a prova global, não é Clausius de horizonte e não é a lei de
área. O dicionário entropia ↔ área da tela não está aqui; o kernel registra um negativo da
bancada (06/09/2026, `OpticalHeatClausius`): a área não é escalar só da álgebra e do estado.
O gate não se move; β não aparece; sem sorry, sem axiom.
-/

namespace TGLExt.QuedaOndaPlanaCandidata

open TGLExt.TraducaoTuring

noncomputable section

variable {X : Type} [Fintype X] [DecidableEq X]

/-- a soma dos custos pesados pela queda: `Σ c(x)·e^{−s·c(x)}`. -/
def custoPesado (c : X → ℕ) (s : ℝ) : ℝ := ∑ x, (c x : ℝ) * Real.exp (-(s * (c x : ℝ)))

/-- a soma dos quadrados dos custos pesados pela queda: `Σ c(x)²·e^{−s·c(x)}`. -/
def custoQuadPesado (c : X → ℕ) (s : ℝ) : ℝ := ∑ x, (c x : ℝ) ^ 2 * Real.exp (-(s * (c x : ℝ)))

/-- o custo médio: `E(s) = (Σ c·e^{−s c}) / Z(s)`. -/
def custoMedio (c : X → ℕ) (s : ℝ) : ℝ := custoPesado c s / particao c s

/-- `S(s) = log Z(s) + s·E(s)`; é a entropia dos pesos por `a_entropia_da_queda_e_a_de_gibbs`. -/
def entropiaDaQueda (c : X → ℕ) (s : ℝ) : ℝ := Real.log (particao c s) + s * custoMedio c s

/-- os pesos de Gibbs: `e^{−s·c(x)}/Z(s)`. -/
def pesoDeGibbs (c : X → ℕ) (s : ℝ) (x : X) : ℝ := Real.exp (-(s * (c x : ℝ))) / particao c s

/-- a partição é positiva. -/
theorem particao_pos [Nonempty X] (c : X → ℕ) (s : ℝ) : 0 < particao c s := by
  unfold particao
  exact Finset.sum_pos (fun x _ => Real.exp_pos _) Finset.univ_nonempty

/-- [candidata] os pesos de Gibbs somam 1. -/
theorem pesos_de_gibbs_somam_um [Nonempty X] (c : X → ℕ) (s : ℝ) :
    ∑ x, pesoDeGibbs c s x = 1 := by
  unfold pesoDeGibbs
  rw [← Finset.sum_div]
  exact div_self (particao_pos c s).ne'

/-- [candidata] ★★ A ENTROPIA DA QUEDA É A DE GIBBS: `log Z + s·E` é `−Σ p log p` dos pesos, na
    definição de entropia que o kernel usa no erro de área. -/
theorem a_entropia_da_queda_e_a_de_gibbs [Nonempty X] (c : X → ℕ) (s : ℝ) :
    ChatgptAudit.finiteEntropy (pesoDeGibbs c s) = entropiaDaQueda c s := by
  have hZ : 0 < particao c s := particao_pos c s
  have hlog : ∀ x, Real.log (pesoDeGibbs c s x)
      = -(s * (c x : ℝ)) - Real.log (particao c s) := by
    intro x
    unfold pesoDeGibbs
    rw [Real.log_div (Real.exp_pos _).ne' hZ.ne', Real.log_exp]
  have key : ∀ x, -(pesoDeGibbs c s x * (-(s * (c x : ℝ)) - Real.log (particao c s)))
      = (s / particao c s) * ((c x : ℝ) * Real.exp (-(s * (c x : ℝ))))
        + (Real.log (particao c s) / particao c s) * Real.exp (-(s * (c x : ℝ))) := by
    intro x
    unfold pesoDeGibbs
    ring
  have hsum : (∑ x, Real.exp (-(s * (c x : ℝ)))) = particao c s := rfl
  unfold ChatgptAudit.finiteEntropy ChatgptAudit.entropyAtom
  simp only [hlog, key]
  rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum, hsum]
  unfold entropiaDaQueda custoMedio custoPesado
  field_simp
  ring

/-- (auxiliar) a derivada de um peso da queda. -/
theorem hasDerivAt_peso (k s : ℝ) :
    HasDerivAt (fun y : ℝ => Real.exp (-(y * k))) (-(k * Real.exp (-(s * k)))) s := by
  have h00 : HasDerivAt (fun y : ℝ => y * k) k s := by
    simpa using (hasDerivAt_id s).mul_const k
  have h0 : HasDerivAt (fun y : ℝ => -(y * k)) (-k) s := h00.neg
  have h2 := h0.exp
  exact h2.congr_deriv (by ring)

/-- [candidata] a derivada da partição é menos o custo pesado. -/
theorem hasDerivAt_particao (c : X → ℕ) (s : ℝ) :
    HasDerivAt (particao c) (-(custoPesado c s)) s := by
  have h : ∀ x ∈ (Finset.univ : Finset X), HasDerivAt (fun y : ℝ => Real.exp (-(y * (c x : ℝ))))
      (-((c x : ℝ) * Real.exp (-(s * (c x : ℝ))))) s := fun x _ => hasDerivAt_peso (c x : ℝ) s
  have hs := HasDerivAt.fun_sum h
  have hv : (∑ x, -((c x : ℝ) * Real.exp (-(s * (c x : ℝ))))) = -(custoPesado c s) := by
    unfold custoPesado
    rw [Finset.sum_neg_distrib]
  rw [hv] at hs
  exact hs

/-- [candidata] a derivada do custo pesado é menos o custo quadrático pesado. -/
theorem hasDerivAt_custoPesado (c : X → ℕ) (s : ℝ) :
    HasDerivAt (custoPesado c) (-(custoQuadPesado c s)) s := by
  have h : ∀ x ∈ (Finset.univ : Finset X),
      HasDerivAt (fun y : ℝ => (c x : ℝ) * Real.exp (-(y * (c x : ℝ))))
        (-((c x : ℝ) ^ 2 * Real.exp (-(s * (c x : ℝ))))) s := by
    intro x _
    have h2 := (hasDerivAt_peso (c x : ℝ) s).const_mul (c x : ℝ)
    exact h2.congr_deriv (by ring)
  have hs := HasDerivAt.fun_sum h
  have hv : (∑ x, -((c x : ℝ) ^ 2 * Real.exp (-(s * (c x : ℝ))))) = -(custoQuadPesado c s) := by
    unfold custoQuadPesado
    rw [Finset.sum_neg_distrib]
  rw [hv] at hs
  exact hs

/-- [candidata] a derivada do custo médio (regra do quociente). -/
theorem hasDerivAt_custoMedio [Nonempty X] (c : X → ℕ) (s : ℝ) :
    HasDerivAt (custoMedio c)
      ((-(custoQuadPesado c s) * particao c s - custoPesado c s * (-(custoPesado c s)))
        / (particao c s) ^ 2) s :=
  (hasDerivAt_custoPesado c s).div (hasDerivAt_particao c s) (particao_pos c s).ne'

/-- [candidata] ★★★ A FORMA CANÔNICA: `dS = s · dE`. Identidade termodinâmica da família de
    pesos `e^{−s c}/Z` `[KNOWN]`; vale para todo custo `c`; não usa a identidade verbal. -/
theorem clausius_da_queda [Nonempty X] (c : X → ℕ) (s E' : ℝ)
    (hE : HasDerivAt (custoMedio c) E' s) :
    HasDerivAt (entropiaDaQueda c) (s * E') s := by
  have hlog : HasDerivAt (fun s : ℝ => Real.log (particao c s))
      (-(custoPesado c s) / particao c s) s :=
    (hasDerivAt_particao c s).log (particao_pos c s).ne'
  have hmul := (hasDerivAt_id s).mul hE
  have h := hlog.add hmul
  have h2 : HasDerivAt (entropiaDaQueda c)
      (-(custoPesado c s) / particao c s + (1 * custoMedio c s + id s * E')) s := h
  refine h2.congr_deriv ?_
  simp only [custoMedio, id]
  ring

/-- [candidata] ★★ a mesma, com a derivada do custo médio escrita. -/
theorem clausius_da_queda_explicito [Nonempty X] (c : X → ℕ) (s : ℝ) :
    HasDerivAt (entropiaDaQueda c)
      (s * ((-(custoQuadPesado c s) * particao c s - custoPesado c s * (-(custoPesado c s)))
        / (particao c s) ^ 2)) s :=
  clausius_da_queda c s _ (hasDerivAt_custoMedio c s)

/-! ## PARTE 2 — K1: a queda como curva de estados diagonais -/

/-- a tangente da queda: `d/ds [e^{−s c(x)}/Z(s)] = peso · (E(s) − c(x))`. -/
def tangenteDaQueda (c : X → ℕ) (s : ℝ) (x : X) : ℝ :=
  pesoDeGibbs c s x * (custoMedio c s - (c x : ℝ))

/-- [candidata] o peso de Gibbs é positivo. -/
theorem pesoDeGibbs_pos [Nonempty X] (c : X → ℕ) (s : ℝ) (x : X) : 0 < pesoDeGibbs c s x :=
  div_pos (Real.exp_pos _) (particao_pos c s)

/-- [candidata] a derivada do peso de Gibbs em `s`: `peso · (E(s) − c(x))` (regra do quociente). -/
theorem hasDerivAt_pesoDeGibbs [Nonempty X] (c : X → ℕ) (s : ℝ) (x : X) :
    HasDerivAt (fun y : ℝ => pesoDeGibbs c y x) (tangenteDaQueda c s x) s := by
  have hZ : particao c s ≠ 0 := (particao_pos c s).ne'
  have h := (hasDerivAt_peso (c x : ℝ) s).div (hasDerivAt_particao c s) hZ
  refine h.congr_deriv ?_
  unfold tangenteDaQueda pesoDeGibbs custoMedio
  field_simp
  ring

/-- [candidata] o peso de Gibbs é contínuo em `s`. -/
theorem pesoDeGibbs_continuo [Nonempty X] (c : X → ℕ) (x : X) :
    Continuous (fun s : ℝ => pesoDeGibbs c s x) :=
  continuous_iff_continuousAt.mpr (fun s => (hasDerivAt_pesoDeGibbs c s x).continuousAt)

/-- [candidata] o custo médio é contínuo em `s`. -/
theorem custoMedio_continuo [Nonempty X] (c : X → ℕ) : Continuous (custoMedio c) :=
  continuous_iff_continuousAt.mpr (fun s => (hasDerivAt_custoMedio c s).continuousAt)

/-- [candidata] a tangente da queda é contínua em `s`. -/
theorem tangenteDaQueda_continua [Nonempty X] (c : X → ℕ) (x : X) :
    Continuous (fun s : ℝ => tangenteDaQueda c s x) :=
  (pesoDeGibbs_continuo c x).mul ((custoMedio_continuo c).sub continuous_const)

/-- (auxiliar) a derivada do peso ao longo da translação `t ↦ s₀ + t`. -/
theorem hasDerivAt_peso_transladado [Nonempty X] (c : X → ℕ) (s₀ t : ℝ) (x : X) :
    HasDerivAt (fun u : ℝ => pesoDeGibbs c (s₀ + u) x) (tangenteDaQueda c (s₀ + t) x) t :=
  (hasDerivAt_pesoDeGibbs c (s₀ + t) x).comp_const_add s₀ t

/-- [candidata] ★ K1. A QUEDA É UMA CURVA DE ESTADOS DIAGONAIS: habita a `DiagonalStateCurve` do
    kernel com base `pesoDeGibbs c s₀`, `weights t = pesoDeGibbs c (s₀ + t)` e tangente
    `tangenteDaQueda c (s₀ + t)`. A curva é LINEAR no parâmetro `s`; ela não é a curva quadrática
    `quadraticGibbsCurve` do kernel (ver a seção K3). -/
def aQuedaComoCurvaDeEstados [Nonempty X] (c : X → ℕ) (s₀ : ℝ) :
    ChatgptAudit.Micro021.DiagonalStateCurve (pesoDeGibbs c s₀) where
  weights := fun t => pesoDeGibbs c (s₀ + t)
  tangent := fun t => tangenteDaQueda c (s₀ + t)
  at_zero := fun x => by simp
  trace_one := fun t => pesos_de_gibbs_somam_um c (s₀ + t)
  derivative_zero := fun x => hasDerivAt_peso_transladado c s₀ 0 x
  derivative_past := by
    filter_upwards [] with t
    exact fun x => hasDerivAt_peso_transladado c s₀ t x
  tangent_continuous := fun x =>
    ((tangenteDaQueda_continua c x).comp (continuous_const.add continuous_id)).continuousAt

/-! ## PARTE 2 — K2: o erro de área da queda em termos da entropia da queda -/

/-- [candidata] ★ K2. O erro de área do kernel (`microscopicAreaError`) da curva da queda é
    `(S(s₀+t) − S(s₀)) − η·(A t − A 0)`, com `S = entropiaDaQueda`. Usa
    `a_entropia_da_queda_e_a_de_gibbs` nos dois termos. A área `A` e o `η` ficam livres. -/
theorem o_erro_de_area_da_queda [Nonempty X] (c : X → ℕ) (s₀ η : ℝ) (A : ℝ → ℝ) (t : ℝ) :
    ChatgptAudit.Micro021.microscopicAreaError (aQuedaComoCurvaDeEstados c s₀) η A t
      = (entropiaDaQueda c (s₀ + t) - entropiaDaQueda c s₀) - η * (A t - A 0) := by
  have h1 : ChatgptAudit.finiteEntropy ((aQuedaComoCurvaDeEstados c s₀).weights t)
      = entropiaDaQueda c (s₀ + t) := a_entropia_da_queda_e_a_de_gibbs c (s₀ + t)
  have h0 : ChatgptAudit.finiteEntropy (pesoDeGibbs c s₀) = entropiaDaQueda c s₀ :=
    a_entropia_da_queda_e_a_de_gibbs c s₀
  unfold ChatgptAudit.Micro021.microscopicAreaError
  rw [h1, h0]

/-- [candidata] a tangente da curva da queda em `0` é nula se, e só se, o custo é constante igual
    ao custo médio em `s₀`. Para custo não constante a tangente NÃO é nula (a variância do custo
    sob a queda é positiva). -/
theorem a_tangente_da_queda_em_zero_e_nula_sse [Nonempty X] (c : X → ℕ) (s₀ : ℝ) :
    (aQuedaComoCurvaDeEstados c s₀).tangent 0 = 0 ↔ ∀ x, (c x : ℝ) = custoMedio c s₀ := by
  constructor
  · intro h x
    have hx := congrFun h x
    change tangenteDaQueda c (s₀ + 0) x = 0 at hx
    rw [add_zero] at hx
    unfold tangenteDaQueda at hx
    rcases mul_eq_zero.mp hx with h1 | h1
    · exact absurd h1 (pesoDeGibbs_pos c s₀ x).ne'
    · linarith
  · intro h
    funext x
    change tangenteDaQueda c (s₀ + 0) x = 0
    rw [add_zero]
    unfold tangenteDaQueda
    rw [h x]
    ring

/-! ## PARTE 2 — K3: a família de Gibbs do kernel é a queda, reparametrizada

O kernel (`ChatgptAudit.Thermal024`) usa a inclinação modular `gibbsWeights p s = p^{1+s}/Z`
(`gibbsAtom p s i = p i · e^{−s·modularScore p i}`, `modularScore p i = −log (p i)`) e a CURVA
`quadraticGibbsCurve p hp hs ω`, com `s = (ω t)²`. Aqui se mede a relação com a queda. -/

/-- [candidata] ★ K3a. Para a base `p = pesoDeGibbs c s₀`, a inclinação modular do kernel É a queda
    em outro parâmetro: `gibbsWeights p s = pesoDeGibbs c (s₀·(1+s))`. (Para `s₀ = 0` a base é
    uniforme, o escore modular é constante e a inclinação é trivial: `p` permanece `p`.) -/
theorem os_pesos_de_gibbs_do_kernel_sao_a_queda [Nonempty X] (c : X → ℕ) (s₀ s : ℝ) (x : X) :
    ChatgptAudit.Thermal024.gibbsWeights (pesoDeGibbs c s₀) s x
      = pesoDeGibbs c (s₀ * (1 + s)) x := by
  have hZ : 0 < particao c s₀ := particao_pos c s₀
  have hp : ∀ y : X, pesoDeGibbs c s₀ y
      = Real.exp (-(s₀ * (c y : ℝ)) - Real.log (particao c s₀)) := by
    intro y
    unfold pesoDeGibbs
    rw [Real.exp_sub, Real.exp_log hZ]
  have hatom : ∀ y : X, ChatgptAudit.Thermal024.gibbsAtom (pesoDeGibbs c s₀) s y
      = Real.exp (-((1 + s) * Real.log (particao c s₀)))
        * Real.exp (-((s₀ * (1 + s)) * (c y : ℝ))) := by
    intro y
    unfold ChatgptAudit.Thermal024.gibbsAtom ChatgptAudit.Thermal024.modularScore
    rw [hp y, Real.log_exp, ← Real.exp_add, ← Real.exp_add]
    congr 1
    ring
  have hpart : ChatgptAudit.Thermal024.gibbsPartition (pesoDeGibbs c s₀) s
      = Real.exp (-((1 + s) * Real.log (particao c s₀))) * particao c (s₀ * (1 + s)) := by
    have hZs : particao c (s₀ * (1 + s))
        = ∑ y, Real.exp (-((s₀ * (1 + s)) * (c y : ℝ))) := rfl
    unfold ChatgptAudit.Thermal024.gibbsPartition
    rw [hZs, Finset.mul_sum]
    exact Finset.sum_congr rfl (fun y _ => hatom y)
  unfold ChatgptAudit.Thermal024.gibbsWeights
  rw [hatom x, hpart]
  unfold pesoDeGibbs
  rw [mul_div_mul_left _ _ (Real.exp_pos _).ne']

/-- [candidata] ★ K3b. A curva quadrática do kernel sobre a base da queda é a queda no parâmetro
    `s₀·(1 + (ω t)²)`. -/
theorem a_curva_quadratica_do_kernel_e_a_queda_reparametrizada [Nonempty X] (c : X → ℕ)
    (s₀ ω t : ℝ) (x : X) :
    ChatgptAudit.Thermal024.quadraticGibbsWeights (pesoDeGibbs c s₀) ω t x
      = pesoDeGibbs c (s₀ * (1 + (ω * t) ^ 2)) x :=
  os_pesos_de_gibbs_do_kernel_sao_a_queda c s₀ ((ω * t) ^ 2) x

/-- [candidata] ★ K3c. O erro de área da curva quadrática do kernel, sobre a base da queda, escrito
    com a entropia da queda: `(S(s₀(1+(ωt)²)) − S(s₀)) − η·(A t − A 0)`. -/
theorem o_erro_de_area_da_curva_quadratica_da_queda [Nonempty X] (c : X → ℕ) (s₀ : ℝ)
    (hp : ∀ x, 0 < pesoDeGibbs c s₀ x) (ω η : ℝ) (A : ℝ → ℝ) (t : ℝ) :
    ChatgptAudit.Micro021.microscopicAreaError
        (ChatgptAudit.Thermal024.quadraticGibbsCurve (pesoDeGibbs c s₀) hp
          (pesos_de_gibbs_somam_um c s₀) ω) η A t
      = (entropiaDaQueda c (s₀ * (1 + (ω * t) ^ 2)) - entropiaDaQueda c s₀) - η * (A t - A 0) := by
  have hw : (ChatgptAudit.Thermal024.quadraticGibbsCurve (pesoDeGibbs c s₀) hp
        (pesos_de_gibbs_somam_um c s₀) ω).weights t
      = pesoDeGibbs c (s₀ * (1 + (ω * t) ^ 2)) :=
    funext (fun x => a_curva_quadratica_do_kernel_e_a_queda_reparametrizada c s₀ ω t x)
  have h1 : ChatgptAudit.finiteEntropy ((ChatgptAudit.Thermal024.quadraticGibbsCurve
        (pesoDeGibbs c s₀) hp (pesos_de_gibbs_somam_um c s₀) ω).weights t)
      = entropiaDaQueda c (s₀ * (1 + (ω * t) ^ 2)) := by
    rw [hw]
    exact a_entropia_da_queda_e_a_de_gibbs c _
  have h0 : ChatgptAudit.finiteEntropy (pesoDeGibbs c s₀) = entropiaDaQueda c s₀ :=
    a_entropia_da_queda_e_a_de_gibbs c s₀
  unfold ChatgptAudit.Micro021.microscopicAreaError
  rw [h1, h0]

section K3geometria

open Filter Topology ChatgptAudit ChatgptAudit.Micro021 ChatgptAudit.Coherent023 ChatgptAudit.Flow019
  ChatgptAudit.Flow020 ChatgptAudit.Thermal024

/-- [candidata] ★★ K3d. O COROLÁRIO. `gibbs_area_matching_iff_ricci` do kernel, instanciado na base
    `p = pesoDeGibbs c s₀` (positiva e normalizada), com o erro de área escrito pela entropia da
    queda: o erro de área sobre `t²` da queda reparametrizada `s = s₀(1+(ωt)²)`, com
    `ω = covectorRead (w x) d`, tende a zero PELA ESQUERDA (`𝓝[<] 0`) se, e só se,
    `η·Ric(d,d) = 2π·T(d,d)`, onde `T` é o tensor de tensão do covetor com acoplamento
    `gibbsCoupling (pesoDeGibbs c s₀)`.
    NÃO é a lei de área, é um SE E SÓ SE: a área `inducedArea` e o dado geométrico `P` são
    ARGUMENTOS (hipóteses); o relógio quadrático é o imposto pelo kernel, não derivado da queda; e
    o acoplamento é a variância modular sobre π por definição do kernel, de modo que o lado direito
    casa com a resposta de entropia por construção. O que se acrescenta aqui é só a leitura do lado
    da entropia como a entropia da queda. β_TGL não aparece. -/
theorem o_balanco_de_area_da_queda_e_ricci [Nonempty X]
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x d : Coordinate4}
    (P : EquilibriumScreenData U g Gamma x d) (gInv : TensorField4) (w : CovectorField4)
    (c : X → ℕ) (s₀ eta : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (ht : ∀ i j k, Gamma x i k j = Gamma x j k i) (hn : tensorQuad (g x) d = 0) :
    Tendsto (fun t => ((entropiaDaQueda c (s₀ * (1 + (covectorRead (w x) d * t) ^ 2))
        - entropiaDaQueda c s₀)
        - eta * (inducedArea g P.curve P.screen.vectors t
          - inducedArea g P.curve P.screen.vectors 0)) / t ^ 2)
      (𝓝[<] 0) (𝓝 0) ↔
      eta * tensorQuad (coordinateRicci Gamma x) d
        = 2 * Real.pi * tensorQuad (covectorStressField g gInv w
            (gibbsCoupling (pesoDeGibbs c s₀)) x) d := by
  have h := gibbs_area_matching_iff_ricci P gInv w (pesoDeGibbs c s₀)
    (pesoDeGibbs_pos c s₀) (pesos_de_gibbs_somam_um c s₀) eta hU hg hG ht hn
  have hf : (fun t => microscopicAreaError (quadraticGibbsCurve (pesoDeGibbs c s₀)
        (pesoDeGibbs_pos c s₀) (pesos_de_gibbs_somam_um c s₀) (covectorRead (w x) d)) eta
        (inducedArea g P.curve P.screen.vectors) t / t ^ 2)
      = (fun t => ((entropiaDaQueda c (s₀ * (1 + (covectorRead (w x) d * t) ^ 2))
        - entropiaDaQueda c s₀)
        - eta * (inducedArea g P.curve P.screen.vectors t
          - inducedArea g P.curve P.screen.vectors 0)) / t ^ 2) := by
    funext t
    rw [o_erro_de_area_da_curva_quadratica_da_queda c s₀ (pesoDeGibbs_pos c s₀)]
  rw [hf] at h
  exact h

/-- [candidata] K3e. O QUE A CURVA LINEAR DE K1 NÃO DÁ. Para a curva da queda `s = s₀ + t` (K1), o
    balanço de Clausius em ordem `t²` do kernel (`microscopic_clausius_iff_zero_tangent`, com as
    hipóteses de calor e de área do kernel) equivale a `tangent 0 = 0`, isto é, a o custo ser
    CONSTANTE igual ao custo médio. Para custo não constante a curva linear tem tangente não nula em
    `0` (os PESOS variam em primeira ordem em `t`; a entropia, em `s₀ = 0`, não) e o balanço
    quadrático não fecha por esta via:
    a família de Gibbs do kernel só é alcançada pela REPARAMETRIZAÇÃO quadrática (K3a a K3d). -/
theorem o_balanco_quadratico_da_queda_linear_sse_custo_constante [Nonempty X] (c : X → ℕ)
    (s₀ rate eta : ℝ) (hrate : rate ≠ 0) (area heat : ℝ → ℝ)
    (hheat : Tendsto (fun t => microscopicHeatError (aQuedaComoCurvaDeEstados c s₀) rate heat t
      / t ^ 2) (𝓝[<] 0) (𝓝 0))
    (harea : Tendsto (fun t => microscopicAreaError (aQuedaComoCurvaDeEstados c s₀) eta area t
      / t ^ 2) (𝓝[<] 0) (𝓝 0)) :
    Tendsto (fun t => horizonBalancePrimitive rate eta area heat t / t ^ 2) (𝓝[<] 0) (𝓝 0) ↔
      ∀ x, (c x : ℝ) = custoMedio c s₀ :=
  (microscopic_clausius_iff_zero_tangent (aQuedaComoCurvaDeEstados c s₀)
    (pesoDeGibbs_pos c s₀) rate eta hrate area heat hheat harea).trans
    (a_tangente_da_queda_em_zero_e_nula_sse c s₀)

end K3geometria

/-! ## PARTE 3 — K4: a queda numa onda plana (construção de um EXEMPLO) -/

section K4ondaPlana

open Filter Topology Matrix Set TGLExt ChatgptAudit ChatgptAudit.Coherent023 ChatgptAudit.Response028
  ChatgptAudit.Flow019 ChatgptAudit.Flow020 ChatgptAudit.Micro021 ChatgptAudit.Profile026
  ChatgptAudit.Thermal024 ChatgptAudit.Thermal025 ChatgptAudit.Wave029

/-- [candidata] ★★ K4a. O balanço de área da queda na tela da origem da onda plana
    `waveOriginScreen a c` (direção nula `waveTestDirection`, frequência `1`): o erro de área da
    queda reparametrizada `s = s₀(1 + t²)`, sobre `t²`, tende a zero pela esquerda se, e só se,
    `eta · (a + c) = 2π · gibbsCoupling (pesoDeGibbs custo s₀)`.
    É `o_balanco_de_area_da_queda_e_ricci` instanciado na onda plana do kernel, com
    `wave_ricci_quad` e `wave_matter_quad` (mesmo caminho de `wave_origin_area_iff`, trocando o teorema
    de amplitude pelo de Gibbs). O cisalhamento `a − c` não entra: fica livre. -/
theorem o_balanco_de_area_da_queda_na_onda_plana [Nonempty X] (a c : ℝ) (custo : X → ℕ)
    (s₀ eta : ℝ) :
    Tendsto (fun t => ((entropiaDaQueda custo (s₀ * (1 + t ^ 2)) - entropiaDaQueda custo s₀)
        - eta * (inducedArea (frameMetricField (waveSolder a c)) (waveOriginScreen a c).curve
            (waveOriginScreen a c).screen.vectors t
          - inducedArea (frameMetricField (waveSolder a c)) (waveOriginScreen a c).curve
            (waveOriginScreen a c).screen.vectors 0)) / t ^ 2) (𝓝[<] 0) (𝓝 0) ↔
      eta * (a + c) = 2 * Real.pi * gibbsCoupling (pesoDeGibbs custo s₀) := by
  have hG : SmoothConnectionOn univ (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) := by
    rw [wave_levi_civita]
    exact wave_connection_smooth a c
  have ht : ∀ i j k, frameLeviCivita (waveSolder a c) (waveInverseSolder a c) 0 i k j =
      frameLeviCivita (waveSolder a c) (waveInverseSolder a c) 0 j k i := by
    rw [wave_levi_civita]
    exact wave_connection_torsion_free a c 0
  have h := o_balanco_de_area_da_queda_e_ricci (waveOriginScreen a c)
    (inverseFrameMetricField (waveInverseSolder a c)) waveCovectorField custo s₀ eta isOpen_univ
    (frame_metric_smooth univ _ (wave_solder_smooth a c)) hG ht (wave_test_null a c)
  change (Tendsto (fun t => ((entropiaDaQueda custo
        (s₀ * (1 + (covectorRead waveCovector waveTestDirection * t) ^ 2))
        - entropiaDaQueda custo s₀)
        - eta * (inducedArea (frameMetricField (waveSolder a c)) (waveOriginScreen a c).curve
            (waveOriginScreen a c).screen.vectors t
          - inducedArea (frameMetricField (waveSolder a c)) (waveOriginScreen a c).curve
            (waveOriginScreen a c).screen.vectors 0)) / t ^ 2) (𝓝[<] 0) (𝓝 0) ↔
      eta * tensorQuad (coordinateRicci
          (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) 0) waveTestDirection
        = 2 * Real.pi * tensorQuad (waveMatter a c (gibbsCoupling (pesoDeGibbs custo s₀)) 0)
          waveTestDirection) at h
  simpa only [wave_ricci_quad, wave_matter_quad, wave_test_frequency, one_pow, mul_one,
    one_mul] using h

/-- (auxiliar) os pesos de Gibbs não são todos iguais quando `s₀ ≠ 0` e o custo não é constante. -/
theorem os_pesos_da_queda_nao_sao_todos_iguais [Nonempty X] (custo : X → ℕ) (s₀ : ℝ)
    (hs : s₀ ≠ 0) (hc : ∃ x y, custo x ≠ custo y) :
    ∃ i j, pesoDeGibbs custo s₀ i ≠ pesoDeGibbs custo s₀ j := by
  obtain ⟨x, y, hxy⟩ := hc
  refine ⟨x, y, ?_⟩
  intro h
  unfold pesoDeGibbs at h
  have hZ : particao custo s₀ ≠ 0 := (particao_pos custo s₀).ne'
  have h1 : Real.exp (-(s₀ * (custo x : ℝ))) = Real.exp (-(s₀ * (custo y : ℝ))) :=
    (div_left_inj' hZ).mp h
  have h2 : -(s₀ * (custo x : ℝ)) = -(s₀ * (custo y : ℝ)) := Real.exp_injective h1
  have h3 : (custo x : ℝ) = (custo y : ℝ) := by
    have h4 : s₀ * (custo x : ℝ) = s₀ * (custo y : ℝ) := neg_inj.mp h2
    exact mul_left_cancel₀ hs h4
  exact hxy (Nat.cast_injective h3)

/-- [candidata] ★ K4b. O acoplamento da queda é positivo: se `s₀ ≠ 0` e o custo não é constante,
    `0 < gibbsCoupling (pesoDeGibbs custo s₀)`. Usa `modular_variance_positive` (a hipótese dele é
    que os pesos não sejam todos iguais, provada em `os_pesos_da_queda_nao_sao_todos_iguais`). -/
theorem o_acoplamento_da_queda_e_positivo [Nonempty X] (custo : X → ℕ) (s₀ : ℝ)
    (hs : s₀ ≠ 0) (hc : ∃ x y, custo x ≠ custo y) :
    0 < gibbsCoupling (pesoDeGibbs custo s₀) :=
  div_pos (modular_variance_positive (pesoDeGibbs custo s₀) (pesoDeGibbs_pos custo s₀)
    (pesos_de_gibbs_somam_um custo s₀) (os_pesos_da_queda_nao_sao_todos_iguais custo s₀ hs hc))
    Real.pi_pos

/-- [candidata] K4c-i. Dado o balanço `eta · (a + c) = 2π · gibbsCoupling`, o erro de área da queda
    tende a zero pela esquerda em TODO ponto `x` e em TODA direção nula `d` (qualquer tela `P` do
    kernel na onda plana), com a frequência `covectorRead waveCovector d`. Os dois lados do
    `gibbs_area_matching_iff_ricci` são proporcionais a `(covectorRead waveCovector d)²`
    (`wave_ricci_quad`, `wave_matter_quad`). -/
theorem o_balanco_da_queda_em_todo_ponto_e_direcao_nula [Nonempty X] (a c : ℝ) (custo : X → ℕ)
    (s₀ eta : ℝ) (hbal : eta * (a + c) = 2 * Real.pi * gibbsCoupling (pesoDeGibbs custo s₀))
    (x d : Coordinate4)
    (P : EquilibriumScreenData univ (frameMetricField (waveSolder a c))
      (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x d)
    (hn : tensorQuad (frameMetricField (waveSolder a c) x) d = 0) :
    Tendsto (fun t => ((entropiaDaQueda custo
        (s₀ * (1 + (covectorRead waveCovector d * t) ^ 2)) - entropiaDaQueda custo s₀)
        - eta * (inducedArea (frameMetricField (waveSolder a c)) P.curve P.screen.vectors t
          - inducedArea (frameMetricField (waveSolder a c)) P.curve P.screen.vectors 0)) / t ^ 2)
      (𝓝[<] 0) (𝓝 0) := by
  have hG : SmoothConnectionOn univ (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) := by
    rw [wave_levi_civita]
    exact wave_connection_smooth a c
  have ht : ∀ i j k, frameLeviCivita (waveSolder a c) (waveInverseSolder a c) x i k j =
      frameLeviCivita (waveSolder a c) (waveInverseSolder a c) x j k i := by
    rw [wave_levi_civita]
    exact wave_connection_torsion_free a c x
  have h := (o_balanco_de_area_da_queda_e_ricci P
    (inverseFrameMetricField (waveInverseSolder a c)) waveCovectorField custo s₀ eta isOpen_univ
    (frame_metric_smooth univ _ (wave_solder_smooth a c)) hG ht hn).2
  refine h ?_
  change eta * tensorQuad (coordinateRicci
      (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x) d
    = 2 * Real.pi * tensorQuad (waveMatter a c (gibbsCoupling (pesoDeGibbs custo s₀)) x) d
  rw [wave_ricci_quad, wave_matter_quad]
  linear_combination (covectorRead waveCovector d) ^ 2 * hbal

/-- [candidata] ★★ K4c. EXISTE UMA ONDA PLANA QUE CASA COM A QUEDA. Para `eta ≠ 0`, `s₀ ≠ 0` e custo
    não constante existem `a c` com `a + c ≠ 0` e `a ≠ 0` tais que:
    (1) `eta · (a + c) = 2π · gibbsCoupling (pesoDeGibbs custo s₀)` (o balanço de K4a);
    (2) a curvatura da onda é não nula em todo ponto (`coordinateCurvature … x 1 0 ≠ 0`: é a
        componente (1,0,1,0) do Riemann, igual a `a`; o Ricci não nulo vem de `a + c ≠ 0`);
    (3) a fonte `waveMatter` com o acoplamento da queda é não nula em todo ponto;
    (4) o erro de área da queda tende a zero pela esquerda na tela da origem (K4a);
    (5) em todo ponto `x` e direção nula `d ≠ 0` existe tela do kernel (`localEquilibriumScreen`) e,
        para qualquer tela `P`, o mesmo limite vale (K4c-i).
    NÃO é derivação: o perfil `(a, c)` é ESCOLHIDO (`a = c = π·acoplamento/eta`, cisalhamento zero)
    para que o balanço valha; é existência por escolha: a condição do lado direito de K4a é
    satisfatível com curvatura e fonte não nulas. `eta` não tem restrição de sinal; para `eta < 0`
    o perfil é negativo e o exemplo é só formal. -/
theorem existe_onda_plana_que_casa_com_a_queda [Nonempty X] (custo : X → ℕ) (s₀ eta : ℝ)
    (heta : eta ≠ 0) (hs : s₀ ≠ 0) (hc : ∃ x y, custo x ≠ custo y) :
    ∃ a c : ℝ, a + c ≠ 0 ∧ a ≠ 0 ∧
      eta * (a + c) = 2 * Real.pi * gibbsCoupling (pesoDeGibbs custo s₀) ∧
      (∀ x : Coordinate4,
        coordinateCurvature (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x 1 0 ≠ 0) ∧
      (∀ x : Coordinate4, waveMatter a c (gibbsCoupling (pesoDeGibbs custo s₀)) x ≠ 0) ∧
      Tendsto (fun t => ((entropiaDaQueda custo (s₀ * (1 + t ^ 2)) - entropiaDaQueda custo s₀)
        - eta * (inducedArea (frameMetricField (waveSolder a c)) (waveOriginScreen a c).curve
            (waveOriginScreen a c).screen.vectors t
          - inducedArea (frameMetricField (waveSolder a c)) (waveOriginScreen a c).curve
            (waveOriginScreen a c).screen.vectors 0)) / t ^ 2) (𝓝[<] 0) (𝓝 0) ∧
      (∀ x d : Coordinate4, d ≠ 0 → tensorQuad (frameMetricField (waveSolder a c) x) d = 0 →
        Nonempty (EquilibriumScreenData univ (frameMetricField (waveSolder a c))
          (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x d) ∧
        ∀ P : EquilibriumScreenData univ (frameMetricField (waveSolder a c))
          (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x d,
          Tendsto (fun t => ((entropiaDaQueda custo
            (s₀ * (1 + (covectorRead waveCovector d * t) ^ 2)) - entropiaDaQueda custo s₀)
            - eta * (inducedArea (frameMetricField (waveSolder a c)) P.curve P.screen.vectors t
              - inducedArea (frameMetricField (waveSolder a c)) P.curve P.screen.vectors 0))
            / t ^ 2) (𝓝[<] 0) (𝓝 0)) := by
  have hk : 0 < gibbsCoupling (pesoDeGibbs custo s₀) :=
    o_acoplamento_da_queda_e_positivo custo s₀ hs hc
  set k := gibbsCoupling (pesoDeGibbs custo s₀) with hkdef
  have ha : Real.pi * k / eta ≠ 0 :=
    div_ne_zero (mul_ne_zero Real.pi_ne_zero hk.ne') heta
  have hbal : eta * (Real.pi * k / eta + Real.pi * k / eta) = 2 * Real.pi * k := by
    field_simp
    ring
  have hsum : Real.pi * k / eta + Real.pi * k / eta ≠ 0 := by
    intro h0
    rw [h0, mul_zero] at hbal
    exact (mul_ne_zero (mul_ne_zero two_ne_zero Real.pi_ne_zero) hk.ne') hbal.symm
  refine ⟨Real.pi * k / eta, Real.pi * k / eta, hsum, ha, hbal, ?_, ?_, ?_, ?_⟩
  · intro x
    exact wave_curvature_nonzero _ _ ha x
  · intro x
    exact wave_matter_nonzero _ _ _ hk.ne' x
  · exact (o_balanco_de_area_da_queda_na_onda_plana _ _ custo s₀ eta).mpr hbal
  · intro x d hd hn
    refine ⟨⟨localEquilibriumScreen univ isOpen_univ _ _
      (fun y _ => wave_solder_inverse _ _ y) (fun y _ => wave_inverse_solder _ _ y)
      (wave_solder_smooth _ _) (wave_inverse_solder_smooth _ _) x d (mem_univ _) hd hn⟩, ?_⟩
    intro P
    exact o_balanco_da_queda_em_todo_ponto_e_direcao_nula _ _ custo s₀ eta hbal x d P hn

end K4ondaPlana

end

end TGLExt.QuedaOndaPlanaCandidata

#print axioms TGLExt.QuedaOndaPlanaCandidata.pesos_de_gibbs_somam_um
#print axioms TGLExt.QuedaOndaPlanaCandidata.a_entropia_da_queda_e_a_de_gibbs
#print axioms TGLExt.QuedaOndaPlanaCandidata.hasDerivAt_particao
#print axioms TGLExt.QuedaOndaPlanaCandidata.hasDerivAt_custoPesado
#print axioms TGLExt.QuedaOndaPlanaCandidata.hasDerivAt_custoMedio
#print axioms TGLExt.QuedaOndaPlanaCandidata.clausius_da_queda
#print axioms TGLExt.QuedaOndaPlanaCandidata.clausius_da_queda_explicito
#print axioms TGLExt.QuedaOndaPlanaCandidata.hasDerivAt_pesoDeGibbs
#print axioms TGLExt.QuedaOndaPlanaCandidata.aQuedaComoCurvaDeEstados
#print axioms TGLExt.QuedaOndaPlanaCandidata.o_erro_de_area_da_queda
#print axioms TGLExt.QuedaOndaPlanaCandidata.a_tangente_da_queda_em_zero_e_nula_sse
#print axioms TGLExt.QuedaOndaPlanaCandidata.os_pesos_de_gibbs_do_kernel_sao_a_queda
#print axioms TGLExt.QuedaOndaPlanaCandidata.a_curva_quadratica_do_kernel_e_a_queda_reparametrizada
#print axioms TGLExt.QuedaOndaPlanaCandidata.o_erro_de_area_da_curva_quadratica_da_queda
#print axioms TGLExt.QuedaOndaPlanaCandidata.o_balanco_de_area_da_queda_e_ricci
#print axioms TGLExt.QuedaOndaPlanaCandidata.o_balanco_quadratico_da_queda_linear_sse_custo_constante
#print axioms TGLExt.QuedaOndaPlanaCandidata.o_balanco_de_area_da_queda_na_onda_plana
#print axioms TGLExt.QuedaOndaPlanaCandidata.os_pesos_da_queda_nao_sao_todos_iguais
#print axioms TGLExt.QuedaOndaPlanaCandidata.o_acoplamento_da_queda_e_positivo
#print axioms TGLExt.QuedaOndaPlanaCandidata.o_balanco_da_queda_em_todo_ponto_e_direcao_nula
#print axioms TGLExt.QuedaOndaPlanaCandidata.existe_onda_plana_que_casa_com_a_queda
