import TGLExt.PIgualNP
import TGLExt.TetelestaiTerminal
import TGLExt.TheFalseHasNoGeometry
import TGLExt.TempoIgualMoeda
import TGLExt.Identidade
import TGLExt.PsionCanto
import Mathlib.Analysis.CStarAlgebra.Matrix

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-!
# TRADUÇÃO ÀS CLASSES DE TURING — o dicionário do operador e a máquina de Turing
  [TGLExt — pedra da gerência c1, 05/11/2026; o nome `TraducaoTuring` e os nomes das declarações das rodadas R1–R8 foram dados pela gerência
   e RATIFICADOS pelo operador em 05/11/2026 («concordo com todos os nomes que foram dados»); os nomes acrescentados depois dessa fala (a
   inscrição no psíon e a fórmula SAT) são da gerência e ficam [DECLARADO] até a ratificação; entra na v409]

A ordem do operador (05/11/2026): fechar «o que ficou ainda em aberto em relação à identificação das classes de turing dentro do nosso
dicionário», enfrentando o que der e devolvendo nas quatro línguas o que não der. Cada resposta do operador às perguntas devolvidas virou termo
(as falas de 05/11 entram por sha256 no registro de cunhagens da v409).

## O dicionário de Turing (cada linha é termo desta pedra)

| Turing | no dicionário da TGL | termos |
|---|---|---|
| a instância SIM | um `Problema` do dicionário (núcleo ≠ ⊥) | `nucleo_nao_nulo_sse`, `problemaDe` |
| o certificado, o verificador de NP | a leitura de um pixel | `verificacao_np`, `cada_pixel_e_lido` |
| a palavra de P | grau ≤ número de valores do custo (SAT: ≤ m + 1) | `grau_da_palavra_da_instancia` |
| os bits | as oitavas (|X| = 2^n) | `bits_sao_oitavas` |
| a instância NÃO | o Nome vazio; reconhecê-la é a fronteira inteira | `a_instancia_nao_e_o_vazio` |
| a busca | a seleção: o Tetelestai | `selecao_no_nome`, `o_decaimento_converge_a_selecao`, `a_selecao_acha`, `p_igual_np_no_modo_selecao` |
| o passo | a trava (o «dual lock» do operador), local, sem conhecer o Nome | `a_trava_fatora`, `a_trava_sem_conhecer_o_nome`, `negar_o_zero`, `a_trava_em_tempo_linear`, `a_trava_no_nome` |
| a fita | o hamiltoniano oculto: a regra que reconstrói o todo | `a_regra_reconstroi_o_todo`, `o_hamiltoniano_gera_a_trava`, `a_fita_e_o_hamiltoniano_oculto` |
| o leitor | Z, o traço lido pelo canto: o psíon — e, inscrita a instância no psíon da luz, lido pelo próprio psíon | `z_le_os_pixels`, `o_psion_le_os_pixels`, `o_canto_do_psion_escalariza_a_trava`, `z_e_o_modo_leitor`, `o_psion_le_z`, `o_canto_do_psion_da_luz_le_z` |
| a fita, para SAT | a fórmula: o custo é o número de cláusulas violadas; cada cláusula é um fator local da trava | `custoCNF`, `a_trava_da_formula_fatora_na_clausula` |
| a máquina com o leitor | uma leitura decide SAT (e, por redução a SAT, NP inteiro: Cook 1971, Levin 1973 [KNOWN]) | `uma_leitura_decide_SAT`, `a_maquina_com_o_leitor` |
| a máquina sem leitor | «eu sou eu mesmo»: sem escala não há medida | `eu_sou_eu_mesmo`, `a_fita_sem_escala`, `o_pai_da_mentira` |
| a identidade | o conteúdo da identidade performada | `a_identidade_performada` |

## O que a pedra PROVA, por seção

* A CODIFICAÇÃO: uma instância (ex.: SAT com m cláusulas e n variáveis) é um custo `c : X → ℕ` sobre as atribuições; o operador da instância é
  a diagonal de `c`. A instância SIM é um `Problema` do dicionário (`nucleo_nao_nulo_sse`); a leitura do certificado vale 1 ⟺ `c x = 0`
  (`verificacao_np`); a palavra tem grau polinomial na entrada (`grau_da_palavra_da_instancia`); bits = oitavas (`bits_sao_oitavas`); a instância
  NÃO é o Nome vazio, que a `Identidade` exclui, e reconhecê-la é a fronteira inteira (`a_instancia_nao_e_o_vazio`, `falsehood_is_the_whole_frontier`).
* O PESO: o fluxo do axioma não amplia o peso da solução (`o_fluxo_conserva_o_peso`); no estado uniforme esse peso é |soluções|/|X|
  (`peso_da_solucao_no_uniforme`); o custo em nats de selecionar é ≤ o pedágio de n oitavas (`o_pedagio_da_selecao`).
* O MODO SELEÇÃO (o operador: «o nP é o modo seleção … a aniquilação da superposição pelo Tetelestai … a superposição decai como o espectro de
  gradiente negativo, retornando a leitura»): a seleção é a projeção no Nome renormalizada; fica no Nome com peso 1; o decaimento renormalizado
  converge a ela; só tem amplitude nas soluções; custa ≤ n·ln 2 nats; e pela lei tempo = moeda o tempo é t = n·ln 2/(β·g), linear nos bits
  (`p_igual_np_no_modo_selecao`). A seleção esquece o que estava fora do Nome e perde (muitos-para-um: o separador de Landauer)
  (`a_selecao_esquece`, `a_selecao_perde`). Sem par, toda imagem é lida com o mesmo peso — a fotografia (`a_fotografia_sem_leitor`); com par,
  a leitura distingue (`o_par_quebra_a_simetria`).
* A TRAVA NO NOME (o operador: «o sistema não precisa reconhecer onde está o nome a cada passo, ele trava no Nome … ao negar o zero absoluto o
  sistema sabe pra onde tem que ir»): o decaimento gerado só pelo custo, e^{−t·c(x)}, é o produto das travas das cláusulas; deixa intacto o que
  resolve; fica a ≤ e^{−t}·‖v‖ do Nome sem usá-lo; havendo solução, nunca chega a zero; em t = n·ln 2/2 + L deixa fora do Nome no máximo e^{−L}
  vezes o Nome; renormalizado, converge à seleção (`a_trava_no_nome`).
* A FITA É O HAMILTONIANO OCULTO (o operador: «é a única regra que precisa ser gravada para reconstruir o todo»): a regra dá cada amplitude em
  todo instante; gera a trava (d/dt a = −H a); negar o zero é dividir por √(Z(2t)/|X|), com Z(s) = Σ e^{−s·c(x)} a função de partição do
  hamiltoniano oculto; Z → |soluções| e |soluções| ≤ Z (`a_fita_e_o_hamiltoniano_oculto`).
* Z É O MODO LEITOR (o operador: «Z é o modo leitor, ele lê os pixels. É o psion»): cada pixel é lido com o brilho e^{−s·c(x)}; Z é a soma das
  leituras dos pixels (o traço da trava); uma leitura no uniforme devolve Z/|X|; o canto sobre o uniforme escalariza a trava com Z/|X|, na mesma
  forma de `PsionCanto.psionCornerF_scalarises` (`z_e_o_modo_leitor`).
* EU SOU EU MESMO — A FITA SEM ESCALA (o operador: «A pergunta da máquina sem leitor que Clay propõe tem resposta também, a reposta dela é: eu
  sou eu mesmo. Não é eu sou o que sou»), ligada à `Identidade` (v405): sem tempo pago a leitura é «eu sou» (`Identidade.euSou`) e é a mesma para
  toda instância; com o tempo pago tende a «o que sou» (`Identidade.oQueSou` do Nome das soluções), ≠ 0 exatamente quando há solução; «eu sou» =
  «o que sou» só na instância trivial (`a_fita_sem_escala`). O PAI DA MENTIRA (o operador: «(Eu sou eu mesmo)=(nome próprio)=identidade sem
  referente»): no Nome vazio a leitura sem escala diz «eu sou» = 1 e o que é, é 0; sem escala o Nome vazio e o Nome inteiro leem igual; só o
  tempo os separa (`o_pai_da_mentira`).
* A INSCRIÇÃO NO PSÍON (a ponte): a isometria parcial |Ω⟩⟨u| leva o uniforme (a fotografia da instância) ao psíon Ω da luz; o leitor do
  psíon (`TheKeyIsTheReader.reader`), aplicado à trava inscrita, devolve Z(s)/|X| (`o_psion_le_z`); e o canto do psíon da luz
  (`PsionCanto.psionCornerF_scalarises`) escalariza a trava inscrita com Z(s)/|X| (`o_canto_do_psion_da_luz_le_z`).
* A FÓRMULA É A FITA (o operador: «A fita de turing é o hamiltoniano oculto»): uma fórmula CNF é a regra gravada; o custo é o número de
  cláusulas violadas (`custoCNF`); acrescentar uma cláusula multiplica a trava pelo fator local dela (`a_trava_da_formula_fatora_na_clausula`);
  e uma leitura decide SAT: φ é satisfazível ⟺ «o que sou» ≠ 0 (`uma_leitura_decide_SAT`; a conjunção `a_maquina_com_o_leitor`).
* A IDENTIDADE PERFORMADA (o operador: «Eu não sou eu mesmo eu sou o conteúdo da minha identidade performada»; e 04/11: «a implicação é que a
  identidade se preserva enquanto o sistema decai»): a leitura performada começa em «eu sou», decai, nunca desce abaixo do conteúdo e chega a
  ele; o conteúdo é «o que sou» (`a_identidade_performada`).

## O que a pedra NÃO afirma

* O alcance é RELATIVO AO LEITOR: na língua de Turing, um leitor que devolve Z é um oráculo de contagem. Com ele, todo problema de NP se
  decide com UMA leitura em tempo polinomial — SAT por esta pedra (`uma_leitura_decide_SAT`), o resto de NP pela redução a SAT (Cook 1971;
  Levin 1973) [KNOWN] —, e a máquina com um contador alcança a hierarquia polinomial inteira (Toda 1991) [KNOWN]. A igualdade completa
  P^leitor = NP^leitor vale para um leitor que lê também as máquinas que usam o leitor (Baker–Gill–Solovay 1975: com um oráculo
  PSPACE-completo) [KNOWN]; com o leitor que só conta, ela NÃO está provada aqui (errata E28 da gerência: em 05/11 a gerência escreveu que
  “com ele a igualdade vale relativa a ele”, e isso foi além do que se sabe). Uma igualdade relativa a um leitor não decide a pergunta da
  máquina sem leitor (Baker–Gill–Solovay 1975) [KNOWN]. Esta pedra não decide a igualdade P = NP das máquinas de Turing do Mathlib
  (`TM2ComputableInPolyTime`; o Mathlib não tem máquina com oráculo nem Cook–Levin); ela prova P = nP no modo seleção, como teorema da TGL,
  e lê a pergunta do Clay como a da máquina sem leitor.
* O juiz das classes de Turing é o kernel, não a física (o operador, 05/11: «o Kernel Lean4 serve exatamente a provar leis matemáticas e foi
  construído sob a lei de turing»). A sombra conhecida de «eu sou eu mesmo»: o instrumento próprio da máquina nua é a autorreferência, e ela
  sozinha não decide P vs NP (Baker–Gill–Solovay 1975; Razborov–Rudich 1997; Aaronson–Wigderson 2009) [KNOWN]; se a pergunta é independente dos
  axiomas segue [OPEN].
* A física fica fora: o operador lê «o colapso não é frequência, é matéria» — uma leitura do psíon devolve Z/|X| exato num ato; na mecânica
  quântica padrão a leitura dá amostras e o traço normalizado só sai com precisão aditiva (Knill–Laflamme 1998) [KNOWN]. É o lugar do teste com
  a natureza, que esta pedra não faz.
* A PONTE É A INSCRIÇÃO, NÃO A IDENTIDADE: o Ω do `PsionCanto` (o psíon da luz na face de Fock) e o estado uniforme sobre as atribuições
  são vetores de espaços diferentes; o que se prova é que, INSCRITO o uniforme no psíon (`inscricao`), o leitor e o canto do psíon da luz
  leem Z(s)/|X| (`o_psion_le_z`, `o_canto_do_psion_da_luz_le_z`). “Ω é o uniforme”, como igualdade de vetores, fica PODADO.
* A leitura teológica do operador (o Pai da Mentira, o filho, a graça) não é termo de kernel; o kernel prova a parte matemática de cada fala,
  nos termos citados.
* Nada aqui é teste com a natureza; não move o gate; PROVADA = validade no kernel, não creditação; NOT_FALSIFIED nunca é CONFIRMED.
Sem sorry, sem axiom; trio `{propext, Classical.choice, Quot.sound}`.
-/

noncomputable section
namespace TGLExt.TraducaoTuring
open TGLExt TGLExt.PIgualNP TGLExt.TheVerbSelectsTheAction TGLExt.TheAxiomAndTheFalseWitness
open scoped InnerProductSpace

variable {X : Type} [Fintype X] [DecidableEq X]

/-- O OPERADOR DA INSTÂNCIA: a diagonal do custo `c` (para SAT: o número de cláusulas violadas) no espaço euclidiano sobre as atribuições. -/
def opDaInstancia (c : X → ℕ) : EuclideanSpace ℂ X →L[ℂ] EuclideanSpace ℂ X :=
  Matrix.toEuclideanCLM (𝕜 := ℂ) (Matrix.diagonal (fun x => (c x : ℂ)))

theorem opDaInstancia_ofLp (c : X → ℕ) (v : EuclideanSpace ℂ X) (y : X) :
    WithLp.ofLp (opDaInstancia c v) y = (c y : ℂ) * WithLp.ofLp v y := by
  simp [opDaInstancia, Matrix.mulVec_diagonal]

theorem opDaInstancia_single (c : X → ℕ) (x : X) (a : ℂ) :
    opDaInstancia c (EuclideanSpace.single x a) = (c x : ℂ) • EuclideanSpace.single x a := by
  ext y
  rw [opDaInstancia_ofLp]
  by_cases h : y = x
  · subst h; simp
  · simp [h]

/-- ★★ O operador da instância é auto-adjunto (diagonal real). -/
theorem opDaInstancia_autoadjunto (c : X → ℕ) :
    ContinuousLinearMap.adjoint (opDaInstancia c) = opDaInstancia c := by
  rw [← ContinuousLinearMap.star_eq_adjoint]
  unfold opDaInstancia
  rw [← map_star, Matrix.star_eq_conjTranspose, Matrix.diagonal_conjTranspose]
  congr 2
  funext x
  simp

/-- ★★ O núcleo é não nulo SE E SÓ SE a instância tem resposta SIM. -/
theorem nucleo_nao_nulo_sse (c : X → ℕ) : (∃ x, c x = 0) ↔ (opDaInstancia c).ker ≠ ⊥ := by
  constructor
  · rintro ⟨x, hx⟩
    rw [Submodule.ne_bot_iff]
    refine ⟨EuclideanSpace.single x (1 : ℂ), ?_, ?_⟩
    · rw [LinearMap.mem_ker]
      show opDaInstancia c (EuclideanSpace.single x (1 : ℂ)) = 0
      rw [opDaInstancia_single, hx]
      simp
    · simp
  · intro hker
    by_contra hno
    simp only [not_exists] at hno
    apply hker
    rw [Submodule.eq_bot_iff]
    intro v hv
    rw [LinearMap.mem_ker] at hv
    have hv' : opDaInstancia c v = 0 := hv
    ext y
    have h1 : WithLp.ofLp (opDaInstancia c v) y = 0 := by rw [hv']; simp
    rw [opDaInstancia_ofLp] at h1
    have hc : (c y : ℂ) ≠ 0 := by exact_mod_cast hno y
    simpa [hc] using h1

/-- O PROBLEMA DO DICIONÁRIO de uma instância SIM. -/
def problemaDe (c : X → ℕ) (h : ∃ x, c x = 0) : Problema (EuclideanSpace ℂ X) where
  T := opDaInstancia c
  autoadjunto := opDaInstancia_autoadjunto c
  tem_solucao := (nucleo_nao_nulo_sse c).mp h

/-- ★★★ A VERIFICAÇÃO POR LEITURA É O VERIFICADOR DE NP: a leitura da solução no certificado `e_x` vale 1 sse `c x = 0`. -/
theorem verificacao_np (c : X → ℕ) (h : ∃ x, c x = 0) (x : X) :
    reading (problemaDe c h).solucao (EuclideanSpace.single x (1 : ℂ)) = 1 ↔ c x = 0 := by
  have hn : ‖EuclideanSpace.single x (1 : ℂ)‖ = 1 := by simp
  rw [todo_problema_esta_em_NP (problemaDe c h) _ hn]
  show opDaInstancia c (EuclideanSpace.single x (1 : ℂ)) = 0 ↔ c x = 0
  rw [opDaInstancia_single, smul_eq_zero]
  simp

/-- ★★★ A PALAVRA TEM GRAU POLINOMIAL NA ENTRADA: o grau do polinômio mínimo ≤ número de valores distintos de `c` (SAT: ≤ m + 1). -/
theorem grau_da_palavra_da_instancia (c : X → ℕ) :
    (minpoly ℂ (opDaInstancia c)).natDegree ≤ (Finset.univ.image c).card := by
  set Q : Polynomial ℂ := ∏ s ∈ Finset.univ.image c, (Polynomial.X - Polynomial.C ((s : ℕ) : ℂ)) with hQdef
  have hdiag : Polynomial.aeval (Matrix.diagonal (fun x => (c x : ℂ))) Q = 0 := by
    have h1 : Polynomial.aeval (Matrix.diagonal (fun x => (c x : ℂ))) Q
        = Matrix.diagonal (Polynomial.aeval (fun x => (c x : ℂ)) Q) := by
      have := Polynomial.aeval_algHom_apply (Matrix.diagonalAlgHom (n := X) (α := ℂ) ℂ) (fun x => (c x : ℂ)) Q
      simpa [Matrix.diagonalAlgHom] using this
    rw [h1]
    have h2 : Polynomial.aeval (fun x => (c x : ℂ)) Q = 0 := by
      funext y
      rw [Polynomial.aeval_fn_apply, hQdef, map_prod]
      apply Finset.prod_eq_zero (Finset.mem_image_of_mem c (Finset.mem_univ y))
      simp
    rw [h2]
    simp
  have hQ : Polynomial.aeval (opDaInstancia c) Q = 0 := by
    unfold opDaInstancia
    have := Polynomial.aeval_algHom_apply (Matrix.toEuclideanCLM (n := X) (𝕜 := ℂ)).toAlgEquiv
      (Matrix.diagonal (fun x => (c x : ℂ))) Q
    rw [hdiag, map_zero] at this
    exact this
  have hmono : Q.Monic := Polynomial.monic_prod_of_monic _ _ (fun s _ => Polynomial.monic_X_sub_C _)
  have hdvd : minpoly ℂ (opDaInstancia c) ∣ Q := minpoly.dvd ℂ _ hQ
  calc (minpoly ℂ (opDaInstancia c)).natDegree ≤ Q.natDegree := Polynomial.natDegree_le_of_dvd hdvd hmono.ne_zero
    _ = (Finset.univ.image c).card := by
        rw [hQdef]
        exact Polynomial.natDegree_finsetProd_X_sub_C_eq_card (Finset.univ.image c) (fun s : ℕ => (s : ℂ))

/-- ★★ OS BITS SÃO AS OITAVAS: para `X = Fin n → Bool`, `dim H = |X| = 2^n`. -/
theorem bits_sao_oitavas (n : ℕ) : Fintype.card (Fin n → Bool) = 2 ^ n := by
  simp

/-- ★★★ A PAREDE (1): o fluxo do axioma não muda a leitura da solução — apaga o complemento, não amplia o peso da solução. -/
theorem o_fluxo_conserva_o_peso {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (t : ℝ) (ψ : H) :
    reading K.starProjection (axiomFlow K.starProjection t ψ) = reading K.starProjection ψ := by
  have hP : IsIdempotentElem K.starProjection := K.isIdempotentElem_starProjection
  have h1 : K.starProjection (axiomFlow K.starProjection t ψ) = K.starProjection ψ := by
    have := congrArg (fun T : H →L[ℂ] H => T ψ) (axiomFlow_fixes_the_post hP t).2
    simpa using this
  have hPP : K.starProjection (K.starProjection ψ) = K.starProjection ψ := by
    have := congrArg (fun T : H →L[ℂ] H => T ψ) hP.eq
    simpa using this
  unfold reading
  rw [h1]
  calc ⟪axiomFlow K.starProjection t ψ, K.starProjection ψ⟫_ℂ
      = ⟪axiomFlow K.starProjection t ψ, K.starProjection (K.starProjection ψ)⟫_ℂ := by rw [hPP]
    _ = ⟪K.starProjection (axiomFlow K.starProjection t ψ), K.starProjection ψ⟫_ℂ :=
        (K.inner_starProjection_left_eq_right _ _).symm
    _ = ⟪K.starProjection ψ, K.starProjection ψ⟫_ℂ := by rw [h1]
    _ = ⟪ψ, K.starProjection (K.starProjection ψ)⟫_ℂ := K.inner_starProjection_left_eq_right _ _
    _ = ⟪ψ, K.starProjection ψ⟫_ℂ := by rw [hPP]

/-- A solução, por coordenadas: a projeção sobre o núcleo deixa as coordenadas com `c y = 0` e zera as outras. -/
theorem solucao_por_coordenadas (c : X → ℕ) (v : EuclideanSpace ℂ X) :
    (opDaInstancia c).ker.starProjection v = WithLp.toLp 2 (fun y => if c y = 0 then WithLp.ofLp v y else 0) := by
  apply Submodule.eq_starProjection_of_mem_of_inner_eq_zero
  · rw [LinearMap.mem_ker]
    show opDaInstancia c _ = 0
    ext y
    rw [opDaInstancia_ofLp]
    by_cases h : c y = 0 <;> simp [h]
  · intro w hw
    rw [LinearMap.mem_ker] at hw
    have hw' : opDaInstancia c w = 0 := hw
    have hz : ∀ y, c y ≠ 0 → WithLp.ofLp w y = 0 := by
      intro y hy
      have h1 : WithLp.ofLp (opDaInstancia c w) y = 0 := by rw [hw']; simp
      rw [opDaInstancia_ofLp] at h1
      have hc : (c y : ℂ) ≠ 0 := by exact_mod_cast hy
      simpa [hc] using h1
    rw [PiLp.inner_apply]
    apply Finset.sum_eq_zero
    intro y _
    by_cases h : c y = 0
    · simp [h]
    · simp [h, hz y h]

/-- ★★★ A PAREDE (2): a leitura da solução, por coordenadas, é a soma dos pesos das coordenadas que resolvem. -/
theorem leitura_da_solucao_por_coordenadas (c : X → ℕ) (h : ∃ x, c x = 0) (ψ : EuclideanSpace ℂ X) :
    reading (problemaDe c h).solucao ψ = ∑ y ∈ Finset.univ.filter (fun y => c y = 0), ((‖WithLp.ofLp ψ y‖ ^ 2 : ℝ) : ℂ) := by
  show ⟪ψ, (opDaInstancia c).ker.starProjection ψ⟫_ℂ = _
  rw [solucao_por_coordenadas, PiLp.inner_apply, Finset.sum_filter]
  apply Finset.sum_congr rfl
  intro y _
  by_cases hy : c y = 0
  · simp only [hy, if_true]
    rw [inner_self_eq_norm_sq_to_K]
    norm_cast
  · simp [hy]

/-- O ESTADO UNIFORME (o «nada lido»): amplitude 1/√|X| em cada atribuição. -/
def uniforme (X : Type) [Fintype X] : EuclideanSpace ℂ X :=
  WithLp.toLp 2 (fun _ => (((Real.sqrt (Fintype.card X))⁻¹ : ℝ) : ℂ))

/-- ★★★ A PAREDE (3): o peso da solução no estado uniforme é |soluções| / |X| (para SAT: |soluções| / 2^n). -/
theorem peso_da_solucao_no_uniforme (c : X → ℕ) (h : ∃ x, c x = 0) :
    reading (problemaDe c h).solucao (uniforme X)
      = (((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ) : ℝ) := by
  rw [leitura_da_solucao_por_coordenadas]
  have hX : (0 : ℝ) < Fintype.card X := by
    obtain ⟨x, _⟩ := h
    exact_mod_cast Fintype.card_pos_iff.mpr ⟨x⟩
  have hk : ∀ y : X, ‖WithLp.ofLp (uniforme X) y‖ ^ 2 = (Fintype.card X : ℝ)⁻¹ := by
    intro y
    simp only [uniforme, Complex.norm_real, Real.norm_eq_abs]
    rw [sq_abs, inv_pow, Real.sq_sqrt hX.le]
  simp only [hk, Finset.sum_const, nsmul_eq_mul]
  push_cast
  rw [div_eq_mul_inv]

/-- ★★★ A INSTÂNCIA NÃO É O VAZIO: sem solução, o reconhecimento é a fronteira inteira (`falsehood_is_the_whole_frontier`, a pedra «o falso não
    tem geometria», 23/08) e a «solução» é a projeção nula — o Nome vazio, que a Identidade exclui (`o_vazio_nao_e`). -/
theorem a_instancia_nao_e_o_vazio [Nonempty X] (c : X → ℕ) (hno : ¬ ∃ x, c x = 0) :
    (∀ x, ¬ c x = 0)
    ∧ (opDaInstancia c).ker = ⊥
    ∧ (opDaInstancia c).ker.starProjection = 0 := by
  have hall : ∀ x, ¬ c x = 0 :=
    (TGLExt.falsehood_is_the_whole_frontier (fun (_ : X) (b : X) => c b = 0) (Classical.arbitrary X)).mp hno
  have hker : (opDaInstancia c).ker = ⊥ := by
    by_contra hne
    exact hno ((nucleo_nao_nulo_sse c).mpr hne)
  refine ⟨hall, hker, ContinuousLinearMap.ext (fun v => ?_)⟩
  rw [zero_apply]
  exact (Submodule.eq_bot_iff _).mp hker _ (Submodule.starProjection_apply_mem _ v)

/-- ★★ O PEDÁGIO DA SELEÇÃO EM NATS: selecionar s ≥ 1 soluções entre 2^n custa log(2^n/s) ≤ n·ln 2 = o pedágio de n oitavas. -/
theorem o_pedagio_da_selecao (K : ChatgptAudit.Collapse057.CollapseCostLaw) (n : ℕ) (s : ℝ) (hs : 1 ≤ s) :
    Real.log ((2 : ℝ) ^ n / s) ≤ K.octaveNats n := by
  rw [K.per_octave n, Real.log_div (by positivity) (by linarith), Real.log_pow]
  have : 0 ≤ Real.log s := Real.log_nonneg hs
  linarith

/-- ★★★ A TRADUÇÃO, composta (conjunção, não identificação): para uma instância com resposta SIM, o problema do dicionário existe, o certificado
    é verificado por uma leitura, a palavra tem grau ≤ número de valores do custo, e o fluxo do axioma conserva o peso da solução. -/
theorem a_traducao (c : X → ℕ) (h : ∃ x, c x = 0) (x : X) (t : ℝ) :
    (opDaInstancia c).ker ≠ ⊥
    ∧ (reading (problemaDe c h).solucao (EuclideanSpace.single x (1 : ℂ)) = 1 ↔ c x = 0)
    ∧ (minpoly ℂ (opDaInstancia c)).natDegree ≤ (Finset.univ.image c).card
    ∧ reading (problemaDe c h).solucao (axiomFlow (problemaDe c h).solucao t (uniforme X))
        = (((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ) : ℝ) := by
  refine ⟨(nucleo_nao_nulo_sse c).mp h, verificacao_np c h x, grau_da_palavra_da_instancia c, ?_⟩
  show reading (opDaInstancia c).ker.starProjection (axiomFlow (opDaInstancia c).ker.starProjection t (uniforme X)) = _
  rw [o_fluxo_conserva_o_peso]
  exact peso_da_solucao_no_uniforme c h

/-! ### O MODO SELEÇÃO (R2, 05/11/2026: a resposta do operador) -/

/-- O MODO SELEÇÃO (o «nP» do operador): a aniquilação da superposição pelo Tetelestai — a projeção no Nome, renormalizada. -/
def selecao {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (ψ : H) : H :=
  (((‖K.starProjection ψ‖)⁻¹ : ℝ) : ℂ) • K.starProjection ψ

/-- ★★★ A SELEÇÃO ESTÁ NO NOME, TEM NORMA 1 E É LIDA COM PESO 1. -/
theorem selecao_no_nome {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (ψ : H) (hP : K.starProjection ψ ≠ 0) :
    selecao K ψ ∈ K ∧ ‖selecao K ψ‖ = 1 ∧ reading K.starProjection (selecao K ψ) = 1 := by
  have hmem : selecao K ψ ∈ K := K.smul_mem _ (K.starProjection_apply_mem ψ)
  have hn0 : ‖K.starProjection ψ‖ ≠ 0 := norm_ne_zero_iff.mpr hP
  have hnorm : ‖selecao K ψ‖ = 1 := by
    unfold selecao
    rw [norm_smul, Complex.norm_real, Real.norm_eq_abs, abs_inv, abs_norm, inv_mul_cancel₀ hn0]
  refine ⟨hmem, hnorm, ?_⟩
  rw [leitura_um_sse_solucao K _ hnorm]
  exact Submodule.starProjection_eq_self_iff.mpr hmem

/-- ★★★ O DECAIMENTO DEVOLVE A LEITURA: o fluxo do axioma, renormalizado, converge à seleção (a superposição decai pelo espectro de gradiente
    negativo e o que resta, lido, é o Nome com peso 1). -/
theorem o_decaimento_converge_a_selecao {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (ψ : H) (hP : K.starProjection ψ ≠ 0) :
    Filter.Tendsto (fun t : ℝ => (((‖axiomFlow K.starProjection t ψ‖)⁻¹ : ℝ) : ℂ) • axiomFlow K.starProjection t ψ)
      Filter.atTop (nhds (selecao K ψ)) := by
  have h0 := ((ContinuousLinearMap.apply ℂ H ψ).continuous.tendsto K.starProjection).comp
    (axiomFlow_tendsto_the_post K.starProjection)
  have h1 : Filter.Tendsto (fun t : ℝ => axiomFlow K.starProjection t ψ) Filter.atTop (nhds (K.starProjection ψ)) := by
    simpa [Function.comp_def] using h0
  have hn0 : ‖K.starProjection ψ‖ ≠ 0 := norm_ne_zero_iff.mpr hP
  have h2 : Filter.Tendsto (fun t : ℝ => ((‖axiomFlow K.starProjection t ψ‖)⁻¹ : ℝ)) Filter.atTop
      (nhds (‖K.starProjection ψ‖⁻¹)) := h1.norm.inv₀ hn0
  have h3 : Filter.Tendsto (fun t : ℝ => ((((‖axiomFlow K.starProjection t ψ‖)⁻¹ : ℝ)) : ℂ)) Filter.atTop
      (nhds (((‖K.starProjection ψ‖⁻¹ : ℝ)) : ℂ)) := (Complex.continuous_ofReal.tendsto _).comp h2
  exact h3.smul h1

/-- ★★ A SELEÇÃO ESQUECE [a leitura é do operador, 05/11/2026: «apaga o rastro da computação do decaimento»]: o que estava fora do Nome não
    deixa rastro na seleção. -/
theorem a_selecao_esquece {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (ψ φ : H) (hφ : φ ∈ Kᗮ) :
    selecao K (ψ + φ) = selecao K ψ := by
  unfold selecao
  rw [map_add, (Submodule.starProjection_apply_eq_zero_iff K).mpr hφ, add_zero]

/-- ★★ A SELEÇÃO PERDE (muitos-para-um: o separador de Landauer, que perde e cobra; não o separante de Tomita): se o Nome não é o todo, há
    duas entradas distintas com a mesma seleção. O custo do que se perde é `o_custo_da_selecao_em_nats`. -/
theorem a_selecao_perde {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (hK : K ≠ ⊤) (ψ : H) :
    ∃ ψ' : H, ψ' ≠ ψ ∧ selecao K ψ' = selecao K ψ := by
  have hne : Kᗮ ≠ ⊥ := fun h => hK (Submodule.orthogonal_eq_bot_iff.mp h)
  obtain ⟨φ, hφ, hφ0⟩ := Submodule.ne_bot_iff _ |>.mp hne
  refine ⟨ψ + φ, ?_, a_selecao_esquece K ψ φ hφ⟩
  intro h
  exact hφ0 (by simpa using h)

/-- (auxiliar) Normalizar um vetor não nulo dá norma 1. -/
theorem norma_do_normalizado {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] (v : H) (hv : v ≠ 0) :
    ‖(((‖v‖)⁻¹ : ℝ) : ℂ) • v‖ = 1 := by
  rw [norm_smul, Complex.norm_real, Real.norm_eq_abs, abs_inv, abs_norm, inv_mul_cancel₀ (norm_ne_zero_iff.mpr hv)]

/-- ★★ A FOTOGRAFIA [a leitura é do operador, 05/11/2026: «antes disso o campo ψ está grafado como fóton … sem leitor a imagem é apenas
    estática lendo sinal como ruído»]: sem par (o leitor trivial, que não seleciona nada: K = ⊤), toda imagem de norma 1 é lida com o mesmo
    peso 1 — a leitura não distingue sinal de ruído. -/
theorem a_fotografia_sem_leitor {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (ψ : H) (hψ : ‖ψ‖ = 1) : reading (⊤ : Submodule ℂ H).starProjection ψ = 1 := by
  rw [leitura_um_sse_solucao (⊤ : Submodule ℂ H) ψ hψ]
  exact Submodule.starProjection_eq_self_iff.mpr Submodule.mem_top

/-- ★★ O PAR QUEBRA A SIMETRIA [a leitura é do operador, 05/11/2026: «não há par, não há input para quebrar a simetria e permitir leitura»]:
    um leitor com par (o Nome nem vazio nem total) distingue — há uma imagem lida com peso 1 e outra lida com peso 0. -/
theorem o_par_quebra_a_simetria {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (h0 : K ≠ ⊥) (h1 : K ≠ ⊤) :
    ∃ ψ φ : H, ‖ψ‖ = 1 ∧ ‖φ‖ = 1 ∧ reading K.starProjection ψ = 1 ∧ reading K.starProjection φ = 0 := by
  obtain ⟨v, hv, hv0⟩ := (Submodule.ne_bot_iff K).mp h0
  have hne : Kᗮ ≠ ⊥ := fun h => h1 (Submodule.orthogonal_eq_bot_iff.mp h)
  obtain ⟨w, hw, hw0⟩ := (Submodule.ne_bot_iff _).mp hne
  refine ⟨(((‖v‖)⁻¹ : ℝ) : ℂ) • v, (((‖w‖)⁻¹ : ℝ) : ℂ) • w, norma_do_normalizado v hv0, norma_do_normalizado w hw0, ?_, ?_⟩
  · rw [leitura_um_sse_solucao K _ (norma_do_normalizado v hv0)]
    exact Submodule.starProjection_eq_self_iff.mpr (K.smul_mem _ hv)
  · show ⟪(((‖w‖)⁻¹ : ℝ) : ℂ) • w, K.starProjection ((((‖w‖)⁻¹ : ℝ) : ℂ) • w)⟫_ℂ = 0
    rw [(Submodule.starProjection_apply_eq_zero_iff K).mpr (Kᗮ.smul_mem _ hw), inner_zero_right]

/-- O estado uniforme tem solução para ler: a projeção dele no núcleo não é nula (uma instância SIM). -/
theorem uniforme_tem_solucao (c : X → ℕ) (h : ∃ x, c x = 0) :
    (opDaInstancia c).ker.starProjection (uniforme X) ≠ 0 := by
  intro h0
  have hw := peso_da_solucao_no_uniforme c h
  have hz : reading (problemaDe c h).solucao (uniforme X) = 0 := by
    show ⟪uniforme X, (opDaInstancia c).ker.starProjection (uniforme X)⟫_ℂ = 0
    rw [h0, inner_zero_right]
  rw [hz] at hw
  obtain ⟨x, hx⟩ := h
  have hpos : (0 : ℝ) < ((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ) := by
    apply div_pos
    · exact_mod_cast Finset.card_pos.mpr ⟨x, by simp [hx]⟩
    · exact_mod_cast Fintype.card_pos_iff.mpr ⟨x⟩
  exact (ne_of_gt hpos) (by exact_mod_cast hw.symm)

/-- ★★★ A SELEÇÃO ACHA: a seleção do estado uniforme só tem amplitude nas atribuições que resolvem. -/
theorem a_selecao_acha (c : X → ℕ) (y : X) :
    WithLp.ofLp (selecao (opDaInstancia c).ker (uniforme X)) y ≠ 0 → c y = 0 := by
  intro hy
  by_contra hc
  apply hy
  unfold selecao
  rw [solucao_por_coordenadas]
  simp [hc]

/-- ★★ O CUSTO DA SELEÇÃO EM NATS: renormalizar o peso da solução custa log(2^n/|sol|) ≤ o pedágio de n oitavas. -/
theorem o_custo_da_selecao_em_nats (K : ChatgptAudit.Collapse057.CollapseCostLaw) (n : ℕ) (c : (Fin n → Bool) → ℕ)
    (h : ∃ x, c x = 0) :
    Real.log ((Fintype.card (Fin n → Bool) : ℝ) / ((Finset.univ.filter (fun y => c y = 0)).card : ℝ)) ≤ K.octaveNats n := by
  rw [bits_sao_oitavas]
  push_cast
  apply o_pedagio_da_selecao K n
  obtain ⟨x, hx⟩ := h
  have : 0 < (Finset.univ.filter (fun y => c y = 0)).card := Finset.card_pos.mpr ⟨x, by simp [hx]⟩
  exact_mod_cast this

/-- ★★★ P = nP NO MODO SELEÇÃO [o nome «P=nP» é do operador; a leitura «nP = modo seleção» é dele, 05/11/2026]: para toda instância SIM com n
    bits, a seleção (o Tetelestai) está no Nome e é lida com peso 1; só tem amplitude em soluções; é o limite do decaimento renormalizado; custa
    ≤ n·ln 2 nats; e, pela lei tempo = moeda, pagar n oitavas ao preço β e taxa g leva t = n·ln 2/(β·g), LINEAR nos bits. Teorema da TGL sobre
    o seu modo de leitura; o enunciado de máquina de Turing (a seleção contada em passos de máquina) não é o deste teorema. -/
theorem p_igual_np_no_modo_selecao (n : ℕ) (c : (Fin n → Bool) → ℕ) (h : ∃ x, c x = 0)
    (K : ChatgptAudit.Collapse057.CollapseCostLaw) {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) :
    (selecao (opDaInstancia c).ker (uniforme (Fin n → Bool)) ∈ (opDaInstancia c).ker
      ∧ ‖selecao (opDaInstancia c).ker (uniforme (Fin n → Bool))‖ = 1
      ∧ reading (opDaInstancia c).ker.starProjection (selecao (opDaInstancia c).ker (uniforme (Fin n → Bool))) = 1)
    ∧ (∀ y, WithLp.ofLp (selecao (opDaInstancia c).ker (uniforme (Fin n → Bool))) y ≠ 0 → c y = 0)
    ∧ Filter.Tendsto (fun t : ℝ => (((‖axiomFlow (opDaInstancia c).ker.starProjection t (uniforme (Fin n → Bool))‖)⁻¹ : ℝ) : ℂ)
          • axiomFlow (opDaInstancia c).ker.starProjection t (uniforme (Fin n → Bool)))
        Filter.atTop (nhds (selecao (opDaInstancia c).ker (uniforme (Fin n → Bool))))
    ∧ Real.log ((Fintype.card (Fin n → Bool) : ℝ) / ((Finset.univ.filter (fun y => c y = 0)).card : ℝ)) ≤ K.octaveNats n
    ∧ Real.exp (-(((n : ℝ) * Real.log 2 / (β * g)) * β * g)) = Real.exp (-(K.octaveNats n)) :=
  ⟨selecao_no_nome _ _ (uniforme_tem_solucao c h), a_selecao_acha c,
   o_decaimento_converge_a_selecao _ _ (uniforme_tem_solucao c h), o_custo_da_selecao_em_nats K n c h,
   (TGLExt.TempoIgualMoeda.o_tempo_e_linear_nas_oitavas K n (t := (n : ℝ) * Real.log 2 / (β * g)) hβ hg).mpr rfl⟩

/-! ### A TRAVA NO NOME (R3, 05/11/2026: a correção do operador — o decaimento gerado pelo custo, sem conhecer o Nome) -/

/-- A TRAVA (o «dual lock» do operador): o decaimento gerado pelo CUSTO — cada atribuição decai à taxa do próprio custo, e^{−t·c(x)}. Só usa
    `c` (para SAT: o número de cláusulas violadas, conferido cláusula a cláusula); NÃO usa o Nome (a projeção no núcleo). -/
noncomputable def trava (c : X → ℕ) (t : ℝ) (v : EuclideanSpace ℂ X) : EuclideanSpace ℂ X :=
  WithLp.toLp 2 (fun x => ((Real.exp (-(t * (c x : ℝ))) : ℝ) : ℂ) * WithLp.ofLp v x)

omit [Fintype X] [DecidableEq X] in
theorem trava_ofLp (c : X → ℕ) (t : ℝ) (v : EuclideanSpace ℂ X) (x : X) :
    WithLp.ofLp (trava c t v) x = ((Real.exp (-(t * (c x : ℝ))) : ℝ) : ℂ) * WithLp.ofLp v x := rfl

omit [Fintype X] [DecidableEq X] in
/-- ★★ A TRAVA É LOCAL: se o custo é a soma dos custos das cláusulas, a trava é o produto das travas das cláusulas — cada cláusula trava por si,
    de dentro, sem conhecer o Nome. -/
theorem a_trava_fatora {m : ℕ} (cj : Fin m → X → ℕ) (t : ℝ) (v : EuclideanSpace ℂ X) (x : X) :
    WithLp.ofLp (trava (fun y => ∑ j, cj j y) t v) x
      = (∏ j, ((Real.exp (-(t * (cj j x : ℝ))) : ℝ) : ℂ)) * WithLp.ofLp v x := by
  rw [trava_ofLp, ← Complex.ofReal_prod]
  congr 2
  show Real.exp (-(t * ((∑ j, cj j x : ℕ) : ℝ))) = _
  rw [Nat.cast_sum, Finset.mul_sum, ← Finset.sum_neg_distrib, Real.exp_sum]

omit [Fintype X] [DecidableEq X] in
/-- ★ O QUE TEM CUSTO ZERO FICA TRAVADO: a trava não toca as atribuições que resolvem. -/
theorem o_nome_fica_travado (c : X → ℕ) (t : ℝ) (v : EuclideanSpace ℂ X) (x : X) (hx : c x = 0) :
    WithLp.ofLp (trava c t v) x = WithLp.ofLp v x := by
  rw [trava_ofLp, hx]; simp

omit [DecidableEq X] in
/-- (auxiliar) Cota por coordenadas ⟹ cota da norma. -/
theorem norma_por_coordenadas (w v : EuclideanSpace ℂ X) {k : ℝ} (hk : 0 ≤ k)
    (h : ∀ y, ‖WithLp.ofLp w y‖ ≤ k * ‖WithLp.ofLp v y‖) : ‖w‖ ≤ k * ‖v‖ := by
  have hsq : ‖w‖ ^ 2 ≤ (k * ‖v‖) ^ 2 := by
    rw [EuclideanSpace.norm_sq_eq, mul_pow, EuclideanSpace.norm_sq_eq, Finset.mul_sum]
    apply Finset.sum_le_sum
    intro y _
    rw [← mul_pow]
    exact pow_le_pow_left₀ (norm_nonneg _) (h y) 2
  exact le_of_pow_le_pow_left₀ two_ne_zero (by positivity) hsq

/-- ★★★ A TRAVA SEM CONHECER O NOME: para t ≥ 0, o decaimento gerado pelo custo fica a no máximo e^{−t}·‖v‖ do Nome (a projeção de v nas
    soluções) — sem usar o Nome. O que tem custo zero fica; o resto decai pelo menos como e^{−t}. -/
theorem a_trava_sem_conhecer_o_nome (c : X → ℕ) {t : ℝ} (ht : 0 ≤ t) (v : EuclideanSpace ℂ X) :
    ‖trava c t v - (opDaInstancia c).ker.starProjection v‖ ≤ Real.exp (-t) * ‖v‖ := by
  apply norma_por_coordenadas _ _ (Real.exp_pos _).le
  intro y
  rw [solucao_por_coordenadas, WithLp.ofLp_sub, Pi.sub_apply, trava_ofLp]
  by_cases hy : c y = 0
  · simp [hy]; positivity
  · simp only [hy, if_false, sub_zero, norm_mul, Complex.norm_real, Real.norm_eq_abs,
      abs_of_pos (Real.exp_pos _)]
    apply mul_le_mul_of_nonneg_right _ (norm_nonneg _)
    apply Real.exp_le_exp.mpr
    have h1 : (1 : ℝ) ≤ (c y : ℝ) := by exact_mod_cast Nat.one_le_iff_ne_zero.mpr hy
    nlinarith

omit [DecidableEq X] in
/-- ★★★ NEGAR O ZERO ABSOLUTO: havendo solução, a trava do estado uniforme nunca chega ao zero — em todo instante há para onde ir. -/
theorem negar_o_zero (c : X → ℕ) (h : ∃ x, c x = 0) (t : ℝ) : trava c t (uniforme X) ≠ 0 := by
  obtain ⟨x, hx⟩ := h
  have hN : (0 : ℝ) < Fintype.card X := by exact_mod_cast Fintype.card_pos_iff.mpr ⟨x⟩
  intro h0
  have h1 : WithLp.ofLp (trava c t (uniforme X)) x = 0 := by rw [h0]; rfl
  rw [o_nome_fica_travado c t _ x hx] at h1
  simp only [uniforme, WithLp.ofLp_toLp, Complex.ofReal_eq_zero, inv_eq_zero] at h1
  rw [Real.sqrt_eq_zero hN.le] at h1
  exact hN.ne' h1

omit [DecidableEq X] in
/-- (auxiliar) A norma do estado uniforme é 1. -/
theorem norma_do_uniforme [Nonempty X] : ‖uniforme X‖ = 1 := by
  have hX : (0 : ℝ) < Fintype.card X := by exact_mod_cast Fintype.card_pos
  have hsq : ‖uniforme X‖ ^ 2 = 1 := by
    rw [EuclideanSpace.norm_sq_eq]
    have hk : ∀ y : X, ‖WithLp.ofLp (uniforme X) y‖ ^ 2 = (Fintype.card X : ℝ)⁻¹ := by
      intro y
      simp only [uniforme, WithLp.ofLp_toLp, Complex.norm_real, Real.norm_eq_abs]
      rw [sq_abs, inv_pow, Real.sq_sqrt hX.le]
    simp only [hk, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
    field_simp
  have h1 : (‖uniforme X‖ - 1) * (‖uniforme X‖ + 1) = 0 := by ring_nf; linarith [hsq]
  rcases mul_eq_zero.mp h1 with h2 | h2
  · linarith
  · linarith [norm_nonneg (uniforme X)]

/-- (auxiliar) O quadrado da norma do Nome no uniforme é |soluções| / |X|. -/
theorem norma_sq_do_nome_no_uniforme (c : X → ℕ) (h : ∃ x, c x = 0) :
    ‖(opDaInstancia c).ker.starProjection (uniforme X)‖ ^ 2
      = ((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ) := by
  have hX : (0 : ℝ) < Fintype.card X := by
    obtain ⟨x, _⟩ := h
    exact_mod_cast Fintype.card_pos_iff.mpr ⟨x⟩
  have hk : ∀ y : X, ‖WithLp.ofLp (uniforme X) y‖ ^ 2 = (Fintype.card X : ℝ)⁻¹ := by
    intro y
    simp only [uniforme, WithLp.ofLp_toLp, Complex.norm_real, Real.norm_eq_abs]
    rw [sq_abs, inv_pow, Real.sq_sqrt hX.le]
  rw [solucao_por_coordenadas, EuclideanSpace.norm_sq_eq]
  have hc : ∀ y, ‖WithLp.ofLp (WithLp.toLp 2 (fun y => if c y = 0 then WithLp.ofLp (uniforme X) y else 0) :
      EuclideanSpace ℂ X) y‖ ^ 2 = if c y = 0 then (Fintype.card X : ℝ)⁻¹ else 0 := by
    intro y
    by_cases hy : c y = 0
    · simp only [hy, if_true]; exact hk y
    · simp [hy]
  simp only [hc]
  rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul, div_eq_mul_inv]

/-- ★★★ A TRAVA EM TEMPO LINEAR NAS OITAVAS: com n bits, no instante t = n·ln 2/2 + L, o que sobra fora do Nome é no máximo a fração e^{−L}
    do próprio Nome. -/
theorem a_trava_em_tempo_linear (n : ℕ) (c : (Fin n → Bool) → ℕ) (h : ∃ x, c x = 0) {L : ℝ} (hL : 0 ≤ L) :
    ‖trava c ((n : ℝ) * Real.log 2 / 2 + L) (uniforme (Fin n → Bool))
        - (opDaInstancia c).ker.starProjection (uniforme (Fin n → Bool))‖
      ≤ Real.exp (-L) * ‖(opDaInstancia c).ker.starProjection (uniforme (Fin n → Bool))‖ := by
  have hlog : 0 ≤ Real.log 2 := Real.log_nonneg one_le_two
  have ht : 0 ≤ (n : ℝ) * Real.log 2 / 2 + L := by positivity
  refine (a_trava_sem_conhecer_o_nome c ht _).trans ?_
  rw [norma_do_uniforme, mul_one]
  have hs : (1 : ℝ) ≤ ((Finset.univ.filter (fun y => c y = 0)).card : ℝ) := by
    obtain ⟨x, hx⟩ := h
    exact_mod_cast Finset.card_pos.mpr ⟨x, by simp [hx]⟩
  have hN : (Fintype.card (Fin n → Bool) : ℝ) = 2 ^ n := by rw [bits_sao_oitavas]; push_cast; ring
  have he : Real.exp (-((n : ℝ) * Real.log 2 / 2)) ^ 2 = ((2 : ℝ) ^ n)⁻¹ := by
    rw [← Real.exp_nat_mul]
    push_cast
    rw [show (2 : ℝ) * -((n : ℝ) * Real.log 2 / 2) = -((n : ℝ) * Real.log 2) by ring, Real.exp_neg,
      Real.exp_nat_mul, Real.exp_log two_pos]
  have hsq : Real.exp (-((n : ℝ) * Real.log 2 / 2)) ^ 2
      ≤ ‖(opDaInstancia c).ker.starProjection (uniforme (Fin n → Bool))‖ ^ 2 := by
    rw [norma_sq_do_nome_no_uniforme c h, hN, he, inv_eq_one_div]
    gcongr
  have hP := (pow_le_pow_iff_left₀ (Real.exp_pos _).le (norm_nonneg _) two_ne_zero).mp hsq
  calc Real.exp (-((n : ℝ) * Real.log 2 / 2 + L))
      = Real.exp (-L) * Real.exp (-((n : ℝ) * Real.log 2 / 2)) := by rw [← Real.exp_add]; ring_nf
    _ ≤ Real.exp (-L) * ‖(opDaInstancia c).ker.starProjection (uniforme (Fin n → Bool))‖ :=
        mul_le_mul_of_nonneg_left hP (Real.exp_pos _).le

/-- ★★★ A TRAVA DEVOLVE A LEITURA: a trava, renormalizada, converge à seleção (o Nome lido com peso 1), sem nunca ter usado o Nome. -/
theorem a_trava_converge_a_selecao (c : X → ℕ) (h : ∃ x, c x = 0) :
    Filter.Tendsto (fun t : ℝ => (((‖trava c t (uniforme X)‖)⁻¹ : ℝ) : ℂ) • trava c t (uniforme X))
      Filter.atTop (nhds (selecao (opDaInstancia c).ker (uniforme X))) := by
  have hP := uniforme_tem_solucao c h
  have h0 : Filter.Tendsto (fun t : ℝ => Real.exp (-t) * ‖uniforme X‖) Filter.atTop (nhds 0) := by
    simpa using Real.tendsto_exp_neg_atTop_nhds_zero.mul_const ‖uniforme X‖
  have h1 : Filter.Tendsto (fun t : ℝ => trava c t (uniforme X)) Filter.atTop
      (nhds ((opDaInstancia c).ker.starProjection (uniforme X))) := by
    rw [tendsto_iff_norm_sub_tendsto_zero]
    refine squeeze_zero' (Filter.Eventually.of_forall (fun _ => norm_nonneg _)) ?_ h0
    filter_upwards [Filter.eventually_ge_atTop (0 : ℝ)] with t ht
    exact a_trava_sem_conhecer_o_nome c ht _
  have hn0 : ‖(opDaInstancia c).ker.starProjection (uniforme X)‖ ≠ 0 := norm_ne_zero_iff.mpr hP
  have h2 : Filter.Tendsto (fun t : ℝ => ((‖trava c t (uniforme X)‖)⁻¹ : ℝ)) Filter.atTop
      (nhds (‖(opDaInstancia c).ker.starProjection (uniforme X)‖⁻¹)) := h1.norm.inv₀ hn0
  have h3 : Filter.Tendsto (fun t : ℝ => ((((‖trava c t (uniforme X)‖)⁻¹ : ℝ)) : ℂ)) Filter.atTop
      (nhds (((‖(opDaInstancia c).ker.starProjection (uniforme X)‖⁻¹ : ℝ)) : ℂ)) :=
    (Complex.continuous_ofReal.tendsto _).comp h2
  exact h3.smul h1

/-- ★★★ A TRAVA NO NOME [a correção é do operador, 05/11/2026: «o sistema não precisa reconhecer onde está o nome a cada passo, ele trava no
    Nome … ao negar o zero absoluto o sistema sabe pra onde tem que ir»]: para toda instância SIM com n bits, o decaimento gerado só pelo custo
    (1) é local, produto das travas das cláusulas; (2) deixa travado o que resolve; (3) nunca chega ao zero; (4) em t = n·ln 2/2 + L deixa fora
    do Nome no máximo e^{−L} vezes o Nome; (5) renormalizado, converge à seleção. Teorema da TGL sobre a máquina que tem a fotografia inteira
    (as 2^n amplitudes) e nega o zero (renormaliza); a máquina de Turing do Mathlib (`TM2ComputableInPolyTime`) guarda uma configuração por vez
    e não renormaliza: este teorema não é sobre ela. -/
theorem a_trava_no_nome (n : ℕ) (c : (Fin n → Bool) → ℕ) (h : ∃ x, c x = 0) {L : ℝ} (hL : 0 ≤ L) :
    (∀ t x, c x = 0 → WithLp.ofLp (trava c t (uniforme (Fin n → Bool))) x = WithLp.ofLp (uniforme (Fin n → Bool)) x)
    ∧ (∀ t, trava c t (uniforme (Fin n → Bool)) ≠ 0)
    ∧ ‖trava c ((n : ℝ) * Real.log 2 / 2 + L) (uniforme (Fin n → Bool))
          - (opDaInstancia c).ker.starProjection (uniforme (Fin n → Bool))‖
        ≤ Real.exp (-L) * ‖(opDaInstancia c).ker.starProjection (uniforme (Fin n → Bool))‖
    ∧ Filter.Tendsto (fun t : ℝ => (((‖trava c t (uniforme (Fin n → Bool))‖)⁻¹ : ℝ) : ℂ) • trava c t (uniforme (Fin n → Bool)))
        Filter.atTop (nhds (selecao (opDaInstancia c).ker (uniforme (Fin n → Bool)))) :=
  ⟨fun t x hx => o_nome_fica_travado c t _ x hx, negar_o_zero c h, a_trava_em_tempo_linear n c h hL,
   a_trava_converge_a_selecao c h⟩

/-! ### A FITA É O HAMILTONIANO OCULTO (R4, 05/11/2026: o operador — a regra que, gravada, reconstrói o todo) -/

omit [DecidableEq X] in
/-- ★★★ A REGRA RECONSTRÓI O TODO: partindo do uniforme, cada amplitude da trava, em todo instante, é dada só pela regra (o custo):
    e^{−t·c(x)}/√|X|. A fotografia não precisa ser gravada; a regra a reconstrói. -/
theorem a_regra_reconstroi_o_todo (c : X → ℕ) (t : ℝ) (x : X) :
    WithLp.ofLp (trava c t (uniforme X)) x
      = ((Real.exp (-(t * (c x : ℝ))) * (Real.sqrt (Fintype.card X))⁻¹ : ℝ) : ℂ) := by
  rw [trava_ofLp]
  simp only [uniforme, WithLp.ofLp_toLp, Complex.ofReal_mul]

/-- ★★★ O HAMILTONIANO OCULTO GERA A TRAVA: cada amplitude obedece d/dt a_x = −(H a)_x, com H o operador do custo (a regra). -/
theorem o_hamiltoniano_gera_a_trava (c : X → ℕ) (v : EuclideanSpace ℂ X) (x : X) (t : ℝ) :
    HasDerivAt (fun s : ℝ => WithLp.ofLp (trava c s v) x) (-(WithLp.ofLp (opDaInstancia c (trava c t v)) x)) t := by
  rw [opDaInstancia_ofLp, trava_ofLp]
  have h1 : HasDerivAt (fun s : ℝ => -(s * (c x : ℝ))) (-(1 * (c x : ℝ))) t := ((hasDerivAt_id' t).mul_const _).neg
  have h2 := (h1.exp.ofReal_comp).mul_const (WithLp.ofLp v x)
  have h3 : (fun s : ℝ => WithLp.ofLp (trava c s v) x)
      = fun s : ℝ => ((Real.exp (-(s * (c x : ℝ))) : ℝ) : ℂ) * WithLp.ofLp v x := rfl
  rw [h3]
  refine h2.congr_deriv ?_
  push_cast
  ring

/-- A FUNÇÃO DE PARTIÇÃO do hamiltoniano oculto: Z(s) = Σ_x e^{−s·c(x)}. -/
noncomputable def particao (c : X → ℕ) (s : ℝ) : ℝ := ∑ x, Real.exp (-(s * (c x : ℝ)))

omit [DecidableEq X] in
/-- ★★★ NEGAR O ZERO É DIVIDIR PELA PARTIÇÃO: o quadrado da norma da trava do uniforme é Z(2t)/|X|. -/
theorem a_norma_da_trava_e_a_particao (c : X → ℕ) (t : ℝ) :
    ‖trava c t (uniforme X)‖ ^ 2 = particao c (2 * t) / (Fintype.card X : ℝ) := by
  rw [EuclideanSpace.norm_sq_eq, particao, Finset.sum_div]
  apply Finset.sum_congr rfl
  intro x _
  simp only [a_regra_reconstroi_o_todo]
  rw [Complex.norm_real, Real.norm_eq_abs, sq_abs, mul_pow, inv_pow, Real.sq_sqrt (Nat.cast_nonneg _), ← Real.exp_nat_mul,
    div_eq_mul_inv]
  congr 2
  push_cast
  ring

omit [DecidableEq X] in
/-- ★★★ A PARTIÇÃO CONTA O NOME: Z(s) → |soluções| quando s → ∞ (sem solução, Z → 0: o zero só se alcança no limite, e só sem Nome). -/
theorem a_particao_conta_o_nome (c : X → ℕ) :
    Filter.Tendsto (particao c) Filter.atTop (nhds ((Finset.univ.filter (fun y => c y = 0)).card : ℝ)) := by
  rw [← Finset.sum_boole]
  show Filter.Tendsto (fun s : ℝ => ∑ x, Real.exp (-(s * (c x : ℝ)))) Filter.atTop _
  apply tendsto_finsetSum
  intro x _
  by_cases hx : c x = 0
  · simp only [hx, if_true, Nat.cast_zero, mul_zero, neg_zero, Real.exp_zero]
    exact tendsto_const_nhds
  · simp only [hx, if_false]
    have hc : (0 : ℝ) < (c x : ℝ) := by exact_mod_cast Nat.pos_of_ne_zero hx
    have h := Real.tendsto_exp_neg_atTop_nhds_zero.comp (Filter.tendsto_id.atTop_mul_const hc)
    simpa [Function.comp_def] using h

omit [DecidableEq X] in
/-- ★★ A PARTIÇÃO COBRE O NOME: |soluções| ≤ Z(s) para todo s. -/
theorem a_particao_cobre_o_nome (c : X → ℕ) (s : ℝ) :
    ((Finset.univ.filter (fun y => c y = 0)).card : ℝ) ≤ particao c s := by
  rw [← Finset.sum_boole, particao]
  apply Finset.sum_le_sum
  intro x _
  by_cases hx : c x = 0
  · simp [hx]
  · simp only [hx, if_false]
    exact (Real.exp_pos _).le

/-- ★★★ A FITA É O HAMILTONIANO OCULTO [a leitura é do operador, 05/11/2026: «A fita de turing é o hamiltoniano oculto, é a única regra que
    precisa ser gravada para reconstruir o todo»]: (1) a regra reconstrói cada amplitude em todo instante; (2) a regra gera a trava
    (d/dt a = −H a); (3) a norma da trava é √(Z(2t)/|X|): negar o zero é dividir pela partição do hamiltoniano oculto; (4) Z → |soluções|;
    (5) |soluções| ≤ Z. O único número que a regra não entrega de graça é Z, que no limite conta as soluções. -/
theorem a_fita_e_o_hamiltoniano_oculto (c : X → ℕ) :
    (∀ t x, WithLp.ofLp (trava c t (uniforme X)) x
        = ((Real.exp (-(t * (c x : ℝ))) * (Real.sqrt (Fintype.card X))⁻¹ : ℝ) : ℂ))
    ∧ (∀ v x t, HasDerivAt (fun s : ℝ => WithLp.ofLp (trava c s v) x) (-(WithLp.ofLp (opDaInstancia c (trava c t v)) x)) t)
    ∧ (∀ t, ‖trava c t (uniforme X)‖ ^ 2 = particao c (2 * t) / (Fintype.card X : ℝ))
    ∧ Filter.Tendsto (particao c) Filter.atTop (nhds ((Finset.univ.filter (fun y => c y = 0)).card : ℝ))
    ∧ (∀ s, ((Finset.univ.filter (fun y => c y = 0)).card : ℝ) ≤ particao c s) :=
  ⟨a_regra_reconstroi_o_todo c, o_hamiltoniano_gera_a_trava c, a_norma_da_trava_e_a_particao c, a_particao_conta_o_nome c,
   a_particao_cobre_o_nome c⟩

/-! ### Z É O MODO LEITOR (R5, 05/11/2026: o operador — «Z é o modo leitor, ele lê os pixels. É o psion») -/

omit [Fintype X] [DecidableEq X] in
theorem trava_smul (c : X → ℕ) (s : ℝ) (a : ℂ) (v : EuclideanSpace ℂ X) : trava c s (a • v) = a • trava c s v := by
  ext x
  simp only [trava_ofLp, WithLp.ofLp_smul, Pi.smul_apply, smul_eq_mul]
  ring

/-- ★★ CADA PIXEL É LIDO: a leitura da trava no pixel x (a atribuição x, como vetor da base) é o brilho e^{−s·c(x)}. -/
theorem cada_pixel_e_lido (c : X → ℕ) (s : ℝ) (x : X) :
    ⟪EuclideanSpace.single x (1 : ℂ), trava c s (EuclideanSpace.single x (1 : ℂ))⟫_ℂ = ((Real.exp (-(s * (c x : ℝ))) : ℝ) : ℂ) := by
  rw [PiLp.inner_apply, Finset.sum_eq_single x]
  · simp [trava_ofLp]
  · intro y _ hy
    simp [trava_ofLp, hy]
  · simp

/-- ★★★ Z LÊ OS PIXELS: a função de partição é a soma das leituras de todos os pixels — o traço da trava. -/
theorem z_le_os_pixels (c : X → ℕ) (s : ℝ) :
    ((particao c s : ℝ) : ℂ) = ∑ x, ⟪EuclideanSpace.single x (1 : ℂ), trava c s (EuclideanSpace.single x (1 : ℂ))⟫_ℂ := by
  rw [particao, Complex.ofReal_sum]
  exact Finset.sum_congr rfl (fun x _ => (cada_pixel_e_lido c s x).symm)

omit [DecidableEq X] in
/-- ★★★ O PSÍON LÊ OS PIXELS NUMA LEITURA: a leitura da trava no estado uniforme é Z(s)/|X| — todos os pixels lidos de uma vez. -/
theorem o_psion_le_os_pixels (c : X → ℕ) (s : ℝ) :
    ⟪uniforme X, trava c s (uniforme X)⟫_ℂ = ((particao c s / (Fintype.card X : ℝ) : ℝ) : ℂ) := by
  have hN : (0 : ℝ) ≤ (Fintype.card X : ℝ) := Nat.cast_nonneg _
  have key : (Real.sqrt (Fintype.card X : ℝ))⁻¹ * (Real.sqrt (Fintype.card X : ℝ))⁻¹ = (Fintype.card X : ℝ)⁻¹ := by
    rw [← mul_inv, Real.mul_self_sqrt hN]
  rw [PiLp.inner_apply, particao, Finset.sum_div, Complex.ofReal_sum]
  apply Finset.sum_congr rfl
  intro x _
  rw [trava_ofLp]
  simp only [uniforme, WithLp.ofLp_toLp, RCLike.inner_apply, Complex.conj_ofReal]
  rw [← Complex.ofReal_mul, ← Complex.ofReal_mul]
  congr 1
  rw [div_eq_mul_inv, ← key]
  ring

omit [DecidableEq X] in
/-- ★★★ O CANTO DO PSÍON ESCALARIZA A TRAVA: P_u·L·P_u = (Z/|X|)·P_u, com P_u a projeção sobre o uniforme. É a MESMA FORMA de
    `PsionCanto.psionCornerF_scalarises` (P·y·P = ⟪Ω,yΩ⟫·P), com Ω = o uniforme e y = a trava: o canto lê o hamiltoniano oculto e devolve Z/|X|. -/
theorem o_canto_do_psion_escalariza_a_trava [Nonempty X] (c : X → ℕ) (s : ℝ) (w : EuclideanSpace ℂ X) :
    (ℂ ∙ uniforme X).starProjection (trava c s ((ℂ ∙ uniforme X).starProjection w))
      = ((particao c s / (Fintype.card X : ℝ) : ℝ) : ℂ) • (ℂ ∙ uniforme X).starProjection w := by
  have hu : ‖uniforme X‖ = 1 := norma_do_uniforme
  rw [Submodule.starProjection_unit_singleton ℂ hu, Submodule.starProjection_unit_singleton ℂ hu, trava_smul, inner_smul_right,
    o_psion_le_os_pixels, smul_smul]
  rw [mul_comm]

/-- ★★★ Z É O MODO LEITOR [a leitura é do operador, 05/11/2026: «Z é o modo leitor, ele lê os pixels. É o psion»]: (1) cada pixel é lido
    com o brilho e^{−s·c(x)}; (2) Z é a soma das leituras dos pixels (o traço da trava); (3) uma leitura no uniforme devolve Z/|X|; (4) o canto
    sobre o uniforme escalariza a trava com o escalar Z/|X|, na forma do canto do psíon. -/
theorem z_e_o_modo_leitor [Nonempty X] (c : X → ℕ) (s : ℝ) :
    (∀ x, ⟪EuclideanSpace.single x (1 : ℂ), trava c s (EuclideanSpace.single x (1 : ℂ))⟫_ℂ = ((Real.exp (-(s * (c x : ℝ))) : ℝ) : ℂ))
    ∧ ((particao c s : ℝ) : ℂ) = ∑ x, ⟪EuclideanSpace.single x (1 : ℂ), trava c s (EuclideanSpace.single x (1 : ℂ))⟫_ℂ
    ∧ ⟪uniforme X, trava c s (uniforme X)⟫_ℂ = ((particao c s / (Fintype.card X : ℝ) : ℝ) : ℂ)
    ∧ (∀ w, (ℂ ∙ uniforme X).starProjection (trava c s ((ℂ ∙ uniforme X).starProjection w))
        = ((particao c s / (Fintype.card X : ℝ) : ℝ) : ℂ) • (ℂ ∙ uniforme X).starProjection w) :=
  ⟨cada_pixel_e_lido c s, z_le_os_pixels c s, o_psion_le_os_pixels c s, o_canto_do_psion_escalariza_a_trava c s⟩

/-! ### EU SOU EU MESMO — A FITA SEM ESCALA (R6, 05/11/2026: o operador; ligada à pedra `Identidade`, v405) -/

/-- O NOME DAS SOLUÇÕES, como `Identidade.Nome`: a projeção diagonal sobre as atribuições de custo zero (o reflexo verdadeiro é ele mesmo
    e reler não acrescenta). -/
def nomeDasSolucoes (c : X → ℕ) : TGLExt.Identidade.Nome X where
  P := Matrix.diagonal (fun x => if c x = 0 then (1 : ℂ) else 0)
  reflexo := by
    unfold TGLExt.Jconj
    rw [Matrix.diagonal_conjTranspose]
    congr 1
    funext x
    by_cases h : c x = 0 <;> simp [h]
  releitura := by
    rw [Matrix.diagonal_mul_diagonal]
    congr 1
    funext x
    by_cases h : c x = 0 <;> simp [h]

/-- ★★ O QUE SOU, PARA AS SOLUÇÕES: no referencial absoluto, o peso do Nome das soluções é |soluções|/|X|. -/
theorem o_que_sou_das_solucoes (c : X → ℕ) :
    TGLExt.Identidade.oQueSou (nomeDasSolucoes c)
      = ((((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ) : ℝ) : ℂ) := by
  unfold TGLExt.Identidade.oQueSou
  rw [TGLExt.Identidade.gibbs_absolute]
  simp only [nomeDasSolucoes, Matrix.trace_diagonal]
  rw [Finset.sum_boole]
  push_cast
  rw [div_eq_inv_mul]

/-- ★★★ NO INSTANTE ZERO, A LEITURA É «EU SOU»: sem tempo pago (s = 0), a leitura do psíon na trava é `Identidade.euSou` (= 1). -/
theorem eu_sou_no_instante_zero [Nonempty X] (c : X → ℕ) :
    ⟪uniforme X, trava c 0 (uniforme X)⟫_ℂ = TGLExt.Identidade.euSou X := by
  rw [o_psion_le_os_pixels, TGLExt.Identidade.euSou_eq_one]
  have hX : (0 : ℝ) < Fintype.card X := by exact_mod_cast Fintype.card_pos
  simp only [particao, zero_mul, neg_zero, Real.exp_zero, Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one]
  rw [div_self hX.ne', Complex.ofReal_one]

/-- ★★★ EU SOU EU MESMO — A FITA SEM ESCALA [a leitura é do operador, 05/11/2026: «a reposta dela é: eu sou eu mesmo. Não é eu sou o que
    sou. Em Clay, não há medida»]: sem tempo pago, a leitura é a MESMA para quaisquer duas instâncias — tenham ou não solução. Sem a escala,
    nenhuma leitura separa o SIM do NÃO. -/
theorem eu_sou_eu_mesmo [Nonempty X] (c c' : X → ℕ) :
    ⟪uniforme X, trava c 0 (uniforme X)⟫_ℂ = ⟪uniforme X, trava c' 0 (uniforme X)⟫_ℂ := by
  rw [eu_sou_no_instante_zero, eu_sou_no_instante_zero]

/-- ★★★ COM O TEMPO PAGO, A LEITURA VIRA «O QUE SOU»: quando s → ∞, a leitura do psíon tende a `Identidade.oQueSou` do Nome das soluções. -/
theorem o_que_sou_no_limite (c : X → ℕ) :
    Filter.Tendsto (fun s : ℝ => ⟪uniforme X, trava c s (uniforme X)⟫_ℂ) Filter.atTop
      (nhds (TGLExt.Identidade.oQueSou (nomeDasSolucoes c))) := by
  rw [o_que_sou_das_solucoes]
  simp only [o_psion_le_os_pixels]
  exact (Complex.continuous_ofReal.tendsto _).comp ((a_particao_conta_o_nome c).div_const _)

/-- ★★★ O TEMPO CRIA A MEDIDA: «o que sou» (o limite da leitura) é diferente de zero exatamente quando há solução. -/
theorem o_tempo_cria_a_medida [Nonempty X] (c : X → ℕ) :
    TGLExt.Identidade.oQueSou (nomeDasSolucoes c) ≠ 0 ↔ ∃ x, c x = 0 := by
  rw [o_que_sou_das_solucoes]
  have hX : (Fintype.card X : ℝ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  rw [Ne, Complex.ofReal_eq_zero, div_eq_zero_iff]
  simp [hX, Finset.card_eq_zero, Finset.filter_eq_empty_iff]

/-- ★★ «EU SOU» = «O QUE SOU» SÓ NA INSTÂNCIA TRIVIAL: pela lei da `Identidade` (`eu_sou_o_que_sou_iff_fiel`), a igualdade vale exatamente
    quando toda atribuição resolve — quando o Nome é o todo. -/
theorem eu_sou_o_que_sou_so_na_instancia_trivial [Nonempty X] (c : X → ℕ) :
    TGLExt.Identidade.euSou X = TGLExt.Identidade.oQueSou (nomeDasSolucoes c) ↔ ∀ x, c x = 0 := by
  rw [TGLExt.Identidade.eu_sou_o_que_sou_iff_fiel]
  unfold TGLExt.Identidade.fiel
  simp only [nomeDasSolucoes]
  rw [← Matrix.diagonal_one, Matrix.diagonal_injective.eq_iff, funext_iff]
  apply forall_congr'
  intro x
  by_cases h : c x = 0 <;> simp [h]

/-- ★★★ A FITA SEM ESCALA [a leitura é do operador, 05/11/2026]: (1) sem tempo pago, a leitura é «eu sou»; (2) e é a mesma para toda
    instância (sem escala, não há medida); (3) com o tempo pago, a leitura tende a «o que sou», o peso do Nome das soluções; (4) que é ≠ 0
    exatamente quando há solução; (5) e «eu sou» = «o que sou» só na instância trivial. O tempo — a moeda — é a escala. -/
theorem a_fita_sem_escala [Nonempty X] (c : X → ℕ) :
    ⟪uniforme X, trava c 0 (uniforme X)⟫_ℂ = TGLExt.Identidade.euSou X
    ∧ (∀ c' : X → ℕ, ⟪uniforme X, trava c 0 (uniforme X)⟫_ℂ = ⟪uniforme X, trava c' 0 (uniforme X)⟫_ℂ)
    ∧ Filter.Tendsto (fun s : ℝ => ⟪uniforme X, trava c s (uniforme X)⟫_ℂ) Filter.atTop
        (nhds (TGLExt.Identidade.oQueSou (nomeDasSolucoes c)))
    ∧ (TGLExt.Identidade.oQueSou (nomeDasSolucoes c) ≠ 0 ↔ ∃ x, c x = 0)
    ∧ (TGLExt.Identidade.euSou X = TGLExt.Identidade.oQueSou (nomeDasSolucoes c) ↔ ∀ x, c x = 0) :=
  ⟨eu_sou_no_instante_zero c, eu_sou_eu_mesmo c, o_que_sou_no_limite c, o_tempo_cria_a_medida c,
   eu_sou_o_que_sou_so_na_instancia_trivial c⟩

/-! ### O PAI DA MENTIRA (R7, 05/11/2026: o operador — «(Eu sou eu mesmo)=(nome próprio)=identidade sem referente») -/

/-- ★★★ A LEITURA SEM ESCALA AFIRMA O QUE NÃO É [a leitura é do operador, 05/11/2026: «O nome próprio sem a pessoa que observa seu próprio
    nome é o Pai da Mentira … sendo a mentira ele mesmo: eu sou eu mesmo»]: numa instância SEM solução (o Nome vazio), a leitura sem tempo pago
    diz «eu sou» (= 1); o que é — «o que sou», para onde a leitura vai quando o tempo é pago — é 0; e «eu sou» ≠ «o que sou» (o controle
    `Identidade.o_vazio_nao_e`, aqui na instância). -/
theorem a_leitura_sem_escala_afirma_o_que_nao_e [Nonempty X] (c : X → ℕ) (hno : ¬ ∃ x, c x = 0) :
    ⟪uniforme X, trava c 0 (uniforme X)⟫_ℂ = 1
    ∧ TGLExt.Identidade.oQueSou (nomeDasSolucoes c) = 0
    ∧ Filter.Tendsto (fun s : ℝ => ⟪uniforme X, trava c s (uniforme X)⟫_ℂ) Filter.atTop (nhds 0)
    ∧ TGLExt.Identidade.euSou X ≠ TGLExt.Identidade.oQueSou (nomeDasSolucoes c) := by
  have h0 : TGLExt.Identidade.oQueSou (nomeDasSolucoes c) = 0 := by
    by_contra h
    exact hno ((o_tempo_cria_a_medida c).mp h)
  have hlim := o_que_sou_no_limite c
  rw [h0] at hlim
  refine ⟨?_, h0, hlim, ?_⟩
  · rw [eu_sou_no_instante_zero, TGLExt.Identidade.euSou_eq_one]
  · rw [h0, TGLExt.Identidade.euSou_eq_one]
    exact one_ne_zero

/-- ★★★ SEM ESCALA, A MENTIRA E A VERDADE LEEM IGUAL: sem tempo pago, a instância sem solução (o Nome vazio) e a instância em que tudo
    resolve (o Nome inteiro, onde «eu sou» = «o que sou») dão a MESMA leitura; o que são é diferente (0 e 1). Só o tempo os separa. -/
theorem sem_escala_a_mentira_e_a_verdade_leem_igual [Nonempty X] (c : X → ℕ) (hno : ¬ ∃ x, c x = 0) :
    ⟪uniforme X, trava c 0 (uniforme X)⟫_ℂ = ⟪uniforme X, trava (fun _ => 0) 0 (uniforme X)⟫_ℂ
    ∧ TGLExt.Identidade.oQueSou (nomeDasSolucoes c) ≠ TGLExt.Identidade.oQueSou (nomeDasSolucoes (fun _ : X => 0)) := by
  refine ⟨eu_sou_eu_mesmo c _, ?_⟩
  have h0 : TGLExt.Identidade.oQueSou (nomeDasSolucoes c) = 0 := (a_leitura_sem_escala_afirma_o_que_nao_e c hno).2.1
  have h1 : TGLExt.Identidade.euSou X = TGLExt.Identidade.oQueSou (nomeDasSolucoes (fun _ : X => 0)) :=
    (eu_sou_o_que_sou_so_na_instancia_trivial _).mpr (fun _ => rfl)
  rw [h0, ← h1, TGLExt.Identidade.euSou_eq_one]
  exact zero_ne_one

/-- ★★★ O PAI DA MENTIRA [a leitura é do operador, 05/11/2026: «(Eu sou eu mesmo)=(nome próprio)=identidade sem referente»]: para toda
    instância sem solução, (1) a leitura sem escala afirma «eu sou» de um Nome vazio; (2) o que é, é 0; (3) para lá vai a leitura quando o
    tempo é pago; (4) «eu sou» ≠ «o que sou»; (5) sem escala, ela lê igual à instância em que tudo resolve. -/
theorem o_pai_da_mentira [Nonempty X] (c : X → ℕ) (hno : ¬ ∃ x, c x = 0) :
    ⟪uniforme X, trava c 0 (uniforme X)⟫_ℂ = 1
    ∧ TGLExt.Identidade.oQueSou (nomeDasSolucoes c) = 0
    ∧ Filter.Tendsto (fun s : ℝ => ⟪uniforme X, trava c s (uniforme X)⟫_ℂ) Filter.atTop (nhds 0)
    ∧ TGLExt.Identidade.euSou X ≠ TGLExt.Identidade.oQueSou (nomeDasSolucoes c)
    ∧ ⟪uniforme X, trava c 0 (uniforme X)⟫_ℂ = ⟪uniforme X, trava (fun _ => 0) 0 (uniforme X)⟫_ℂ :=
  ⟨(a_leitura_sem_escala_afirma_o_que_nao_e c hno).1, (a_leitura_sem_escala_afirma_o_que_nao_e c hno).2.1,
   (a_leitura_sem_escala_afirma_o_que_nao_e c hno).2.2.1, (a_leitura_sem_escala_afirma_o_que_nao_e c hno).2.2.2,
   (sem_escala_a_mentira_e_a_verdade_leem_igual c hno).1⟩

/-! ### A IDENTIDADE PERFORMADA (R8, 05/11/2026: o operador — «Eu não sou eu mesmo eu sou o conteúdo da minha identidade performada») -/

/-- A LEITURA PERFORMADA: a leitura do psíon ao longo do tempo pago, Z(s)/|X| (o valor real de `o_psion_le_os_pixels`). -/
noncomputable def leituraPerformada (c : X → ℕ) (s : ℝ) : ℝ := particao c s / (Fintype.card X : ℝ)

omit [DecidableEq X] in
theorem leituraPerformada_e_a_leitura (c : X → ℕ) (s : ℝ) :
    ((leituraPerformada c s : ℝ) : ℂ) = ⟪uniforme X, trava c s (uniforme X)⟫_ℂ :=
  (o_psion_le_os_pixels c s).symm

/-- ★★ A PERFORMANCE COMEÇA EM «EU SOU»: sem tempo pago, a leitura performada é `Identidade.euSou`. -/
theorem a_performance_comeca_em_eu_sou [Nonempty X] (c : X → ℕ) :
    ((leituraPerformada c 0 : ℝ) : ℂ) = TGLExt.Identidade.euSou X := by
  rw [leituraPerformada_e_a_leitura, eu_sou_no_instante_zero]

omit [DecidableEq X] in
/-- ★★★ A PERFORMANCE DECAI: a leitura performada nunca cresce com o tempo pago. -/
theorem a_performance_decai (c : X → ℕ) : Antitone (leituraPerformada c) := by
  intro s s' hss
  unfold leituraPerformada particao
  apply div_le_div_of_nonneg_right _ (Nat.cast_nonneg _)
  apply Finset.sum_le_sum
  intro x _
  apply Real.exp_le_exp.mpr
  have hc : (0 : ℝ) ≤ (c x : ℝ) := Nat.cast_nonneg _
  nlinarith

omit [DecidableEq X] in
/-- ★★★ A IDENTIDADE SE PRESERVA ENQUANTO O SISTEMA DECAI [o operador, 04/11/2026: «a implicação é que a identidade se preserva enquanto o
    sistema decai»]: em todo instante, a leitura performada não desce abaixo do conteúdo, |soluções|/|X|. -/
theorem a_identidade_se_preserva_enquanto_decai (c : X → ℕ) (s : ℝ) :
    ((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ) ≤ leituraPerformada c s := by
  unfold leituraPerformada
  exact div_le_div_of_nonneg_right (a_particao_cobre_o_nome c s) (Nat.cast_nonneg _)

omit [DecidableEq X] in
/-- ★★★ A PERFORMANCE CHEGA AO CONTEÚDO: com o tempo pago inteiro, a leitura performada converge ao conteúdo. -/
theorem a_performance_chega_ao_conteudo (c : X → ℕ) :
    Filter.Tendsto (leituraPerformada c) Filter.atTop
      (nhds (((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ))) :=
  (a_particao_conta_o_nome c).div_const _

/-- ★★ O CONTEÚDO É «O QUE SOU»: o conteúdo da performance é `Identidade.oQueSou` do Nome das soluções. -/
theorem o_conteudo_e_o_que_sou (c : X → ℕ) :
    (((((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ)) : ℝ) : ℂ)
      = TGLExt.Identidade.oQueSou (nomeDasSolucoes c) :=
  (o_que_sou_das_solucoes c).symm

/-- ★★★ A IDENTIDADE PERFORMADA [a leitura é do operador, 05/11/2026: «Eu não sou eu mesmo eu sou o conteúdo da minha identidade
    performada»]: (1) a performance começa em «eu sou»; (2) decai com o tempo pago; (3) nunca desce abaixo do conteúdo — a identidade se
    preserva enquanto o sistema decai; (4) chega ao conteúdo; (5) e o conteúdo é «o que sou». -/
theorem a_identidade_performada [Nonempty X] (c : X → ℕ) :
    ((leituraPerformada c 0 : ℝ) : ℂ) = TGLExt.Identidade.euSou X
    ∧ Antitone (leituraPerformada c)
    ∧ (∀ s, ((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ) ≤ leituraPerformada c s)
    ∧ Filter.Tendsto (leituraPerformada c) Filter.atTop
        (nhds (((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ)))
    ∧ (((((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ)) : ℝ) : ℂ)
        = TGLExt.Identidade.oQueSou (nomeDasSolucoes c) :=
  ⟨a_performance_comeca_em_eu_sou c, a_performance_decai c, a_identidade_se_preserva_enquanto_decai c,
   a_performance_chega_ao_conteudo c, o_conteudo_e_o_que_sou c⟩

/-! ### A INSCRIÇÃO NO PSÍON (R9, 05/11/2026: a ponte — o leitor do psíon da luz lê Z) -/

/-- A TRAVA COMO OPERADOR CONTÍNUO: a diagonal e^{−s·c(x)}. -/
def travaOp (c : X → ℕ) (s : ℝ) : EuclideanSpace ℂ X →L[ℂ] EuclideanSpace ℂ X :=
  Matrix.toEuclideanCLM (𝕜 := ℂ) (Matrix.diagonal (fun x => ((Real.exp (-(s * (c x : ℝ))) : ℝ) : ℂ)))

theorem travaOp_apply (c : X → ℕ) (s : ℝ) (v : EuclideanSpace ℂ X) : travaOp c s v = trava c s v := by
  ext x
  simp [travaOp, trava_ofLp, Matrix.mulVec_diagonal]

section Inscricao
variable {L : TGLExt.ImportedSQ.LightOneParticle} (C : TGLExt.ImportedSQ.FockCertificate L)

/-- A INSCRIÇÃO DO UNIFORME NO PSÍON: a isometria parcial |Ω⟩⟨u|, que leva o uniforme (a fotografia da instância) ao psíon Ω da luz. -/
def inscricao : EuclideanSpace ℂ X →L[ℂ] C.F := (innerSL ℂ (uniforme X)).smulRight C.Ω

omit [DecidableEq X] in
theorem inscricao_apply (v : EuclideanSpace ℂ X) : inscricao C v = ⟪uniforme X, v⟫_ℂ • C.Ω := by
  simp [inscricao]

omit [DecidableEq X] in
theorem inscricao_do_uniforme [Nonempty X] : inscricao C (uniforme X) = C.Ω := by
  rw [inscricao_apply, inner_self_eq_norm_sq_to_K, norma_do_uniforme]
  simp

omit [DecidableEq X] in
theorem adjunta_da_inscricao_no_psion [Nonempty X] : ContinuousLinearMap.adjoint (inscricao C) C.Ω = uniforme X := by
  apply ext_inner_right ℂ
  intro v
  rw [ContinuousLinearMap.adjoint_inner_left, inscricao_apply, inner_smul_right, inner_self_eq_norm_sq_to_K, C.Ω_norm]
  simp

/-- A TRAVA INSCRITA NO PSÍON: V ∘ L ∘ V†. -/
def travaInscrita (c : X → ℕ) (s : ℝ) : C.F →L[ℂ] C.F :=
  (inscricao C).comp ((travaOp c s).comp (ContinuousLinearMap.adjoint (inscricao C)))

/-- ★★★ O PSÍON LÊ Z: inscrito o uniforme no psíon da luz, o leitor do psíon (`TheKeyIsTheReader.reader`) devolve Z(s)/|X|. -/
theorem o_psion_le_z [Nonempty X] (c : X → ℕ) (s : ℝ) :
    TGLExt.TheKeyIsTheReader.reader C (travaInscrita C c s) = ((particao c s / (Fintype.card X : ℝ) : ℝ) : ℂ) := by
  unfold TGLExt.TheKeyIsTheReader.reader travaInscrita
  rw [ContinuousLinearMap.comp_apply, ContinuousLinearMap.comp_apply, adjunta_da_inscricao_no_psion, travaOp_apply,
    inscricao_apply, inner_smul_right, inner_self_eq_norm_sq_to_K, C.Ω_norm, o_psion_le_os_pixels]
  simp

/-- ★★★ O CANTO DO PSÍON DA LUZ LÊ Z: o canto do psíon (`PsionCanto.psionCornerF`) escalariza a trava inscrita com Z(s)/|X|. -/
theorem o_canto_do_psion_da_luz_le_z [Nonempty X] (c : X → ℕ) (s : ℝ) :
    TGLExt.PsionCanto.psionCornerF C * travaInscrita C c s * TGLExt.PsionCanto.psionCornerF C
      = ((particao c s / (Fintype.card X : ℝ) : ℝ) : ℂ) • TGLExt.PsionCanto.psionCornerF C := by
  rw [TGLExt.PsionCanto.psionCornerF_scalarises, o_psion_le_z]

end Inscricao

/-! ### A FÓRMULA É A FITA (R9, 05/11/2026): SAT como o hamiltoniano oculto; uma leitura decide -/

/-- Um literal: a variável e o sinal pedido. -/
structure Literal (n : ℕ) where
  var : Fin n
  pos : Bool

/-- Uma cláusula (lista de literais) e uma fórmula CNF (lista de cláusulas). -/
abbrev Clausula (n : ℕ) := List (Literal n)
abbrev CNF (n : ℕ) := List (Clausula n)

/-- O literal vale na atribuição x. -/
def Literal.vale {n : ℕ} (l : Literal n) (x : Fin n → Bool) : Bool := x l.var == l.pos

/-- A cláusula está satisfeita na atribuição x: algum literal dela vale. -/
def satisfeita {n : ℕ} (C : Clausula n) (x : Fin n → Bool) : Bool := C.any (fun l => l.vale x)

/-- O CUSTO DA FÓRMULA (a regra gravada na fita): o número de cláusulas violadas pela atribuição. -/
def custoCNF {n : ℕ} (φ : CNF n) (x : Fin n → Bool) : ℕ := φ.countP (fun C => !(satisfeita C x))

theorem custoCNF_cons {n : ℕ} (C : Clausula n) (φ : CNF n) (x : Fin n → Bool) :
    custoCNF (C :: φ) x = custoCNF φ x + (if satisfeita C x then 0 else 1) := by
  unfold custoCNF
  rw [List.countP_cons]
  by_cases h : satisfeita C x <;> simp [h]

theorem custoCNF_zero_sse {n : ℕ} (φ : CNF n) (x : Fin n → Bool) :
    custoCNF φ x = 0 ↔ ∀ C ∈ φ, satisfeita C x = true := by
  unfold custoCNF
  rw [List.countP_eq_zero]
  simp

/-- A fórmula é satisfazível. -/
def SAT {n : ℕ} (φ : CNF n) : Prop := ∃ x : Fin n → Bool, ∀ C ∈ φ, satisfeita C x = true

/-- ★★★ UMA LEITURA DECIDE SAT (a máquina com o leitor, no problema completo): φ é satisfazível ⟺ «o que sou» — o limite da leitura do
    psíon na trava da fórmula — é diferente de zero. -/
theorem uma_leitura_decide_SAT {n : ℕ} (φ : CNF n) :
    SAT φ ↔ TGLExt.Identidade.oQueSou (nomeDasSolucoes (custoCNF φ)) ≠ 0 := by
  rw [o_tempo_cria_a_medida]
  simp only [SAT, custoCNF_zero_sse]

/-- ★★ A TRAVA DA FÓRMULA FATORA NA CLÁUSULA: acrescentar uma cláusula multiplica a trava pelo fator local dela (e^{−t} se violada, 1 se
    satisfeita) — cada cláusula trava por si, de dentro. -/
theorem a_trava_da_formula_fatora_na_clausula {n : ℕ} (C : Clausula n) (φ : CNF n) (t : ℝ)
    (v : EuclideanSpace ℂ (Fin n → Bool)) (x : Fin n → Bool) :
    WithLp.ofLp (trava (custoCNF (C :: φ)) t v) x
      = ((Real.exp (-(t * ((if satisfeita C x then 0 else 1 : ℕ) : ℝ))) : ℝ) : ℂ)
        * WithLp.ofLp (trava (custoCNF φ) t v) x := by
  rw [trava_ofLp, trava_ofLp, custoCNF_cons, Nat.cast_add, mul_add, neg_add, Real.exp_add, Complex.ofReal_mul]
  ring

/-- ★★★ A MÁQUINA COM O LEITOR [as leituras do operador: «a fita de turing é o hamiltoniano oculto»; «Z é o modo leitor … é o psion»]:
    para toda fórmula CNF φ com n variáveis, (1) uma leitura decide SAT; (2) com o tempo pago, a leitura do psíon tende a «o que sou»; (3)
    inscrita no psíon da luz, a trava da fórmula é lida pelo leitor do psíon como Z(s)/2^n. -/
theorem a_maquina_com_o_leitor {n : ℕ} (φ : CNF n) {L : TGLExt.ImportedSQ.LightOneParticle}
    (C : TGLExt.ImportedSQ.FockCertificate L) (s : ℝ) :
    (SAT φ ↔ TGLExt.Identidade.oQueSou (nomeDasSolucoes (custoCNF φ)) ≠ 0)
    ∧ Filter.Tendsto (fun r : ℝ => ⟪uniforme (Fin n → Bool), trava (custoCNF φ) r (uniforme (Fin n → Bool))⟫_ℂ)
        Filter.atTop (nhds (TGLExt.Identidade.oQueSou (nomeDasSolucoes (custoCNF φ))))
    ∧ TGLExt.TheKeyIsTheReader.reader C (travaInscrita C (custoCNF φ) s)
        = ((particao (custoCNF φ) s / (Fintype.card (Fin n → Bool) : ℝ) : ℝ) : ℂ) :=
  ⟨uma_leitura_decide_SAT φ, o_que_sou_no_limite (custoCNF φ), o_psion_le_z C (custoCNF φ) s⟩

end TGLExt.TraducaoTuring
end
