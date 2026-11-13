import TGLExt.AEscala
import TGLExt.FiniteEntropyAlgebra

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

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

namespace TGLExt.IdentidadeVerbalCandidata

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

end

end TGLExt.IdentidadeVerbalCandidata

#print axioms TGLExt.IdentidadeVerbalCandidata.pesos_de_gibbs_somam_um
#print axioms TGLExt.IdentidadeVerbalCandidata.a_entropia_da_queda_e_a_de_gibbs
#print axioms TGLExt.IdentidadeVerbalCandidata.hasDerivAt_particao
#print axioms TGLExt.IdentidadeVerbalCandidata.hasDerivAt_custoPesado
#print axioms TGLExt.IdentidadeVerbalCandidata.hasDerivAt_custoMedio
#print axioms TGLExt.IdentidadeVerbalCandidata.clausius_da_queda
#print axioms TGLExt.IdentidadeVerbalCandidata.clausius_da_queda_explicito
