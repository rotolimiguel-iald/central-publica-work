[REAL / DERIVED / KNOWN / OPEN] Ordem 007 — parecer da bancada, 05/09/2026.

## O resultado que muda o caminho crítico

O contrato original `TGLExt.ExpectationInput P` está habitado para o perfil estacionário não tracial e, mais geralmente, para qualquer período comum das fases locais. A construção integra vetores em Hilbert, produz um operador limitado, prova sua pertinência ao fator e identifica cada esperança de andar com o pinching espectral. Os campos `into`, `fixes`, `ortho` são provas; a existência não foi colocada como hipótese do habitante.

Dois negativos também foram construídos. A cauda própria não tem Ω cíclico. Além disso, na torre produto, a relação de Borchers combinada com continuidade forte em zero, identidade em zero e preservação de norma força a translação a ser trivial, mesmo para perfis sem período comum. Esse resultado é mais amplo que a invariância de sítios da ordem 006, mas mantém explícita a hipótese da relação de Borchers.

A identificação finita proposta para a assinatura encontra uma obstrução: um boost não trivial não se entrelaça injetivamente com uma isometria de um espaço de norma positiva. As métricas lorentzianas soldadas são invariantes pelo boost escolhido; as euclidianas não são. Isso não deriva a escolha da assinatura a partir de Δ, e um único boost também preserva uma forma de assinatura (2,2).

## A — habitante global

`StationaryModularPeriod.lean` prova que diferenças de log-pesos locais pertencem a uma rede inteira se isso vale em cada sítio. Para r≠0, o período é T=2π/|r|. O caso estacionário usa r=log p−log(1−p); `stationary_modular_period` reescreve o resultado com log(p/(1−p)), como solicitado. O período do fluxo é provado em H por densidade dos locais. Não há classificação de Connes importada nesse argumento.

`PeriodAverageOperator.lean` constrói

    A_T(x)ξ = T⁻¹ ∫₀ᵀ σ_t(x)ξ dt,     ‖A_T(x)‖ ≤ ‖x‖.

A integral é de vetores, com a medida de Lebesgue da mathlib. Continuidade forte do fluxo já existia; a continuidade com vetor variável e a continuidade da órbita conjugada foram provadas. A linearidade complexa em ξ e a estimativa produzem o operador limitado. O teorema `period_average_mem_factor` usa a comutação com o comutante, diretamente no bicomutante que define M. Não se pressupõe continuidade em norma de B(H), nem se invoca Takesaki para obter a existência.

`PeriodAveragePrefix.lean` prova, para todo x limitado e todo N:

    E_N(A_T(x)) = π_N(specExpect(d_N, E_N^mat(x))).

A topologia usada para atravessar a integral é a NORMA EM H. Avalia-se sobre Ω; a projeção `levelProject P N` é um operador linear contínuo em H e atravessa a integral pelo lema `ContinuousLinearMap.intervalIntegral_comp_comm`. O cálculo das fases é explícito: integral T para frequência zero, zero para frequência não nula com fase final 1. A igualdade em Ω volta a ser igualdade de operadores do fator por separância. Não foi acrescentado um lema fictício de continuidade σ-fraca da esperança.

`PeriodicCentralizerExpectation.lean` constrói:

```lean
periodicExpectationInput (P) (T) (hT : 0 < T)
  (hp : LocalPhasePeriod P T) : ExpectationInput P

stationaryExpectationInput (P) (p) (hp : ∀ n, P.w n = p)
  (hne : p ≠ 1/2) : ExpectationInput P
```

`into` usa `centralizer_from_expectations`; `fixes` usa convergência em Ω e separância; `ortho` usa continuidade do produto interno das aproximações de andar. `periodic_half_agrees` prova concordância com `tracialExpectationInput` em M para todo T>0 quando o perfil é ½. O wrapper estacionário não tracial tem a hipótese p≠½ e por isso não pode ser aplicado literalmente ao caso p=½; o habitante periódico comum permite a comparação sem contradição de tipos.

`Order007Bridges.lean` aplica a unicidade original a qualquer outro habitante e prova a restrição ao pinching. As hipóteses do tipo `LocalPhasePeriod` não afirmam a existência da esperança: afirmam apenas uma igualdade explícita de fases, satisfeita por teorema no perfil estacionário e pelos perfis de log-razões comensuráveis. Para um perfil sem período comum, esta construção periódica não resolve o problema. A esperança global aperiódica permanece [OPEN] nesta bancada.

**Critérios A:** derivação prévia PAGA; obrigações 1–4 PAGAS; habitante e campos PAGOS; unicidade PAGA; controle tracial PAGO; generalização à rede inteira PAGA. Não restou dívida analítica escondida nesses enunciados periódicos.

## B — não ciclicidade e Borchers

`TailNotCyclic.lean` trabalha com `chainTailClosure P 1`, que já é o bicomutante da álgebra de cauda. Sua comutação com o primeiro andar implica E₀(x)=ω(x)I. Por bimodularidade e preservação do estado, ω(ex)=pω(x). A testemunha é

    v = (e−pI)Ω,     ‖v‖²=p(1−p)>0,     ⟨v,xΩ⟩=0 para x∈T₁.

Como o hiperplano ortogonal a v é fechado e próprio, T₁Ω não é denso. O enunciado `¬ Dense (...)` é exatamente a afirmação de que seu fecho não é todo H. Não precisou de uma nova aproximação WOT da cauda.

`CyclicExpectationObstruction.lean` define `SubalgebraExpectationInput P N`. O mapa E e seus campos são HIPÓTESES. Se N⊆M e NΩ é denso, a ortogonalidade e a separância forçam E(x)=x para todo x∈M, logo N=M. Uma N própria com esse contrato não pode ter Ω cíclico. Normalidade e invariância não aparecem como hipóteses redundantes: na literatura elas podem obter a esperança, mas, uma vez dados seus campos, não são usadas na prova. Este módulo não presume uma esperança nova para N.

`PeriodicBorchersObstruction.lean` prova primeiro que a invariância de uma função contínua em zero sob contração a↦ca, 0≤c<1, a torna constante. Um período modular positivo e a relação de Borchers dão exatamente essa contração, logo V(a)=I.

`ProductBorchersObstruction.lean` remove a hipótese de período. Seu teorema principal, no próprio `TowerHilbert P`, tem as hipóteses EXATAS:

```text
V : ℝ → B(H)
∀ ξ, a ↦ V(a)ξ é contínua em a=0
V(0)=I
∀ a ξ, ‖V(a)ξ‖=‖ξ‖
∀ t a, σ_t(V(a)) = V(exp(−2πt)a)
────────────────────────────────
∀ a, V(a)=I
```

Para cada autovetor modular ξ, o funcional diagonal ⟨ξ,σ_t(V(a))ξ⟩ cancela as fases. Borchers dá invariância por contração no parâmetro a; continuidade dá ⟨ξ,V(a)ξ⟩=‖ξ‖². A identidade da norma de V(a)ξ−ξ força V(a)ξ=ξ. A família local de autovetores tem span denso por `localEigenvectors_total`, já provado; portanto V(a)=I. Vale para TODO perfil produto da torre, inclusive aperiódico. Não exige que V seja construído com sítios.

[KNOWN] Para uma álgebra em posição padrão e um grupo unitário fortemente contínuo que preserve Ω, tenha gerador positivo e implemente endomorfismos num semieixo, o teorema de Borchers fornece a relação usada acima. Essa passagem da hipótese espectral para a relação NÃO foi formalizada aqui. Fonte primária consultada: [Araki–Zsidó, Extension of the structure theorem of Borchers and its application to half-sided modular inclusions](https://arxiv.org/pdf/math/0412061), introdução e resultados de estrutura. Não há uma dependência dessa referência como axioma Lean: `hborchers` permanece um argumento visível.

[DERIVED, usando o teorema externo] Assim, um grupo que satisfaça as condições usuais de Borchers com o estado produto e o fluxo desta torre só pode ser trivial. O negativo não exclui outro estado na mesma álgebra, outra representação ou uma dinâmica que não satisfaça a relação de Borchers. Escolher apenas uma subálgebra não alinhada com sítios, mantendo este mesmo estado e os mesmos dados modulares, não contorna a obstrução geral entregue.

**Critérios B:** B.1 PAGO em Lean; B.2 PAGO com contrato explícito como hipótese; B.3 PAGO como negativo sob a relação de Borchers, com a passagem espectral clássica marcada [KNOWN]. Um gerador positivo não trivial nesta mesma estrutura não é um objeto ainda por escolher livremente: ele seria incompatível com a relação demonstrada pelo teorema clássico.

## C — o que foi provado e o que o alvo original não permite concluir

`ModularSignatureObstruction.lean` constrói B₄(s) como boost no plano 0–1 e identidade transversal. Prova B₄ᵀηB₄=η e, para qualquer frame E, a invariância de (B₄E)ᵀη(B₄E). Se det E é invertível e s≠0, prova que (B₄E)ᵀ(B₄E)≠EᵀE. A comparação vale em particular para o `modularFrame` canônico. Isso paga as identidades métricas pedidas, com o boost como objeto explicitamente dado.

`Order007Bridges.lean` prova que B₄ é formado pelo MESMO gerador K₁ do kernel e que seu bloco 2×2 é o MESMO `TGLExt.boost`:

    B₄(s)=I+sinh(s)K₁+(cosh(s)−1)K₁².

Não há encadeamento por homônimos. A face hiperbólica é mantida; não é confundida com a rotação compacta.

O obstáculo à identificação solicitada é formalizado em dois níveis:

1. Em qualquer espaço de norma positiva, uma isometria não pode ter autovetor não nulo com autovalor exp(s), exceto s=0.
2. Para o fluxo modular REAL da torre, se F:ℝ⁴→H é linear e injetivo e U_tF=FB₄(s), então s=0 (`tower_modular_cannot_intertwine_nonzero_boost`). A prova usa a direção nula (1,1,0,0), que é autovetor do boost com autovalor exp(s), mas cuja imagem por F tem norma positiva.

Portanto a igualdade finita não trivial entre Δ^{it} unitário e esse boost, por uma tétrade identificada injetivamente com vetores de H, não é uma folha apenas sem prova: nesse tipo preciso ela é incompatível com os dados. O resultado NÃO nega Bisognano–Wichmann em teoria quântica de campos. Uma ação geométrica em coordenadas ou campos, possivelmente não limitados, é diferente de um subespaço finito invariante de vetores do Hilbert positivo. A ponte entre essas representações precisa ser construída e ter domínio explícito.

Também não segue “o fluxo escolhe (1,3)” da preservação de uma métrica e da não preservação de outra. O mesmo B₄ preserva diag(1,−1,1,−1), além de diag(1,−1,−1,−1). O teorema `single_boost_has_two_signatures` fornece esse contraexemplo. Seriam necessárias hipóteses adicionais sobre a representação completa e a forma bilinear; não foram extraídas de Kossakowski nesta rodada.

Outra precisão: positividade completa fornece Kossakowski semidefinida positiva. A passagem a assinatura estritamente (4,0) ainda exige posto quatro e não degenerescência. O problema do “quatro” não desaparece com a positividade. `real_gram_cannot_equal_eta` prova a incompatibilidade direta EᵀE≠η para toda matriz real 4×4, pelo sinal do determinante. A continuação analítica KMS não muda esse teorema sobre congruências reais.

**Critérios C:** comparação das métricas e ponte com K₁/bloco canônico PAGAS. Identificação finita não trivial por entrelaçamento injetivo: NEGATIVO PAGO no tipo explicitado. Derivação da assinatura (1,3) a partir da positividade e da rotação modular: NÃO PAGA; a inferência proposta foi refutada nesse alcance. A identificação geométrica em outra representação permanece [OPEN], sem alterar a interpretação física por decreto.

## Reprodutibilidade, integridade e continuação

Os dez módulos, logs finais, tentativas falhas, backups em bytes e dependências locais estão inventariados em `ORDEM007_MANIFESTO.json`. O script `audit_order007.py` confere cobertura de `#print axioms`, exit code zero para o hash exato de cada fonte final e ausência de `sorryAx` ou avisos nos logs finais. Ele não substitui a auditoria independente da gerência e não interpreta uma contagem de teoremas como prova da gravidade quântica.

As falhas de tática, coerção, inferência de tipos e de uma chamada sequencial do verificador foram mantidas como histórico. O acerto dos módulos finais foi conferido por novas compilações; logs fracassados não foram reclassificados. A derivação teve um adendo anterior ao novo argumento de Borchers, preservando a versão inicial em backup.

Somente a pasta `Chatgpt` recebeu escritas. O Atlas foi consultado, não copiado ou atualizado. Nenhum `um.py` foi executado, importado ou alterado; gate, kernel canônico e memórias permanecem sob a gerência. Nenhum dado observacional foi buscado.

O objetivo amplo continua aberto: esta entrega fecha a esperança periódica e estabelece obstáculos ao caminho modular proposto, mas não fornece a reconstrução gravitacional geral, H3 derivado da dinâmica, a origem de quatro canais ou uma assinatura lorentziana derivada sem inseri-la. O progresso seguinte precisa respeitar esses negativos: a simples troca de subálgebra mantendo o mesmo estado produto não entrega a translação de Borchers não trivial; a ponte geométrica não pode ser um entrelaçamento finito injetivo com o Hilbert positivo.

Nada nesses teoremas depende de uma escolha do operador. A gerência decide incorporação após auditoria independente. Decisões históricas da v98 e do contorno continuam reservadas e não foram antecipadas.
