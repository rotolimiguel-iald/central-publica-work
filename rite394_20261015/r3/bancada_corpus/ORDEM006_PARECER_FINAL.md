[REAL / DERIVED / KNOWN / OPEN] Ordem 006 — parecer da bancada, 05/09/2026.

## Resultado formal e seu alcance

Foram compilados cinco módulos novos. O inventário automático distingue teoremas de definições e registra cada impressão de axiomas. A construção tracial habita o contrato original `TGLExt.ExpectationInput P`. A construção para perfis arbitrários tem domínio local; NÃO habita por si só o contrato global.

`CentralizerLocal`: o pinching espectral de cada andar entra no centralizador GLOBAL de ω; a esperança de andar preserva esse centralizador; caracterização por blocos e ortogonalidade finita.

`LocalCentralizerExpectation`: mapa local concreto com `into`, `fixes`, `ortho` contra TODO o centralizador global, e unicidade. `LocalCentralizerInput` é um tipo auxiliar explicitamente distinto do contrato original. Não confundir o domínio matricial com todo M.

`TracialCentralizerExpectation`: a partir de E_N(x) e E_N(x*) convergindo sobre Ω, `centralizer_from_expectations` prova que x pertence ao centralizador se todas as suas esperanças de andar pertencem. Não precisou pressupor normalidade σ-fraca de uma média. Densidades escalares para o perfil todo ½ dão M_ω=M e o habitante original `tracialExpectationInput`, E=id.

`SiteModularInvariance`: σ_t(A(I))=A(I) para qualquer conjunto de sítios e qualquer perfil; σ_t(T_N)=T_N nos bicomutantes das caudas; inexistência de compressão estrita dessas caudas.

`CentralizerContractBridge`: qualquer futuro habitante global RESTRINGE-SE ao pinching já construído. Se P.w(0)≠½, nenhum desses habitantes pode coincidir em todo M com uma esperança de andar. Imagem de shift igual à cauda implica invariância da imagem; a igualdade de imagem é hipótese declarada, não uma construção de shift.

## A — construção não tracial: derivação e parede exata

[DERIVED analítico; OPEN em Lean] Para perfil constante p∈(0,1), p≠½, d_i/d_j=(p/(1−p))^k. Assim T=2π/|log(p/(1−p))| é um período: todas as fases locais em T são 1. Igualdade em domínio denso e continuidade do unitário dão U_T=1 em H. Isto não calcula o invariante T completo de Connes e não usa classificação do fator.

A média deve ser construída por integração vetorial forte t↦σ_t(x)ξ, ou integral fraca de operadores. Integrar em norma de B(H) sem demonstrar essa continuidade seria lacuna. A média é limitada por ‖x‖, e comuta com M′ por integração, logo pertence a M=M″. Periodicidade dá invariância pelo fluxo. No andar, a integral de cada fase é 0 ou 1, exatamente `specExpect`.

Lista SUFICIENTE de obrigações ainda não construídas nesta bancada, com nomes propostos (não são teoremas existentes):

1. `stationary_modular_period`: a periodicidade local e sua extensão a `modularFlow P T = 1`, sob perfil constante não tracial.
2. `period_average_operator`: produzir um operador limitado A_T(x), provando, para todo ξ, A_T(x)ξ = T⁻¹∫₀ᵀσ_t(x)ξ dt; incluir T>0, integrabilidade, linearidade em ξ e estimativa ‖A_T(x)‖≤‖x‖.
3. `period_average_mem_factor`: integração preserva comutação com cada elemento de M′, logo A_T(x)∈M quando x∈M.
4. `period_average_prefix`: E_N(A_T(x)) = π_N(specExpect(d_N,E_N^mat(x))). Exige passar E_N pela integral, justificando sua continuidade para a topologia usada, e calcular as fases locais. Não basta citar a comutação de E_N com σ_t pontualmente.

Os campos do contrato seguem dessas obrigações, sem nova hipótese de Takesaki: `into` usa o item 4 e `centralizer_from_expectations`; para `fixes`, se x∈M_ω então E_N(x)∈M_ω, o pinching fixa essas matrizes e E_N(A_T(x))Ω=E_N(x)Ω para todo N, logo A_T(x)Ω=xΩ e separância implica igualdade. Para `ortho`, aproximar x, A_T(x) e b pelos E_N sobre Ω e usar a ortogonalidade finita. Como E_N(b) é centralizador e o item 4 identifica E_N(A_T(x)), o produto interno de cada andar é zero; continuidade do produto interno fornece o limite zero. Esses últimos encadeamentos da média ainda são DERIVAÇÃO, não declarações Lean entregues.

Consequentemente, a parede não pode mais ser descrita genericamente como “falta normalidade de ω”: a passagem de centralizadores via esperanças já está paga. Falta construir a média limitada e sua ponte exata com E_N. Não foi adicionado um campo que assuma a média pronta.

Para perfis gerais, aperiodicidade NÃO é automática. Por exemplo, pesos alternados 1/3 e 2/3 têm log-razões ±log 2 e período comum 2π/log 2. Para perfis sem período comum, a projeção ergódica no GNS é uma rota [KNOWN]; reconstruir dela um operador em M com norma controlada ainda é obrigação. Nem a existência dessa projeção nem o nome Takesaki foram usados como axioma novo no Lean entregue.

## B — inclusão meia-lateral: correção do enunciado e redirecionamento

[REAL] Invariância bilateral foi provada, incluindo o fecho de cauda. Logo não há compressão estrita por σ_t nessas subálgebras. Para θ(M), o resultado vale condicionado à imagem ser a cauda: nenhuma extensão normal de shift foi construída aqui. “Exige estacionariedade” era forte demais; estacionariedade é suficiente para o shift canônico preservador do estado, não uma necessidade universal para qualquer extensão normal.

[KNOWN] A condição meia-lateral usual é σ_t(N)⊆N num semieixo. Ela admite igualdade; portanto o critério B.2 da ordem, como escrito, não é correto. O obstáculo à inclusão própria útil para Wiesbrock é também a ciclicidade comum, e não redefinir ⊆ como ⊊. Referência primária: [Araki–Zsidó, Extension of the structure theorem of Borchers](https://arxiv.org/abs/math/0412061). Para inclusões modulares e condições sobre o vetor, ver [Correa da Silva–Lechner, Modular Structure and Inclusions of Twisted Araki-Woods Algebras](https://arxiv.org/abs/2212.02298).

[DERIVED, não formalizado aqui] A cauda que exclui o sítio 0 não tem Ω cíclico no GNS inteiro. Escreva e=E₀₀ no sítio 0, p=P.w(0), v=(e−pI)Ω. O produto dá ‖v‖²=p(1−p)>0. Para x na cauda, ω(e x)=pω(x), logo ⟨v,xΩ⟩=0. A fatoração estende-se da álgebra local à cauda por continuidade WOT do funcional vetorial. Portanto o fecho de T₁Ω é próprio. Este argumento não exige identificar abstratamente todo H com um produto tensorial infinito. A formalização da não ciclicidade não consta dos cinco módulos; o negativo formal entregue é o da compressão estrita.

Uma inclusão própria globalmente invariante, com estado fiel normal e esperança preservadora do estado, não pode ter Ω cíclico para N no GNS de M: a projeção sobre fecho(NΩ) seria I e a esperança seria identidade pela separância. Aqui isso é um argumento [KNOWN/DERIVED] com existência da esperança declarada; não é usado para fingir a construção não tracial do alvo A.

| Rota | O que existe no material lido | Custo e obrigação aberta |
|---|---|---|
| Estado não produto | Torre produto e cálculos locais explícitos | Construir novo estado fiel e GNS, seus operadores modulares e a inclusão; os lemas do perfil produto não migram automaticamente. |
| Subálgebra não alinhada com sítios | M, fluxo modular, comutantes e rede de sítios | Exibir N próprio, provar ciclicidade/separância comuns e compressão num semieixo. O negativo de sítios não exclui essa rota. |
| Borchers/Longo–Witten | Nenhum U(a) não trivial de energia positiva identificado nos módulos examinados | Construir grupo fortemente contínuo, gerador positivo com domínios, invariância do vácuo e U(a)MU(a)*⊆M. Só então obter a relação de dilatação. Não usar o próprio resultado procurado como hipótese. |
| `BisognanoWichmann` | Boosts 2×2, preservação da forma de Minkowski/cunha; identidade de Gibbs modular finita | Falta identificar esses boosts com automorfismos da rede e construir translações não triviais de energia positiva. |
| `ContinuousModularZero` | Gerador matricial e funções hiperbólicas com derivadas em κ | Não fornece por si operador de translação no GNS, domínio autoadjunto ou inclusão modular. O regime hiperbólico é respeitado; uma derivada escalar não paga esses objetos. |
| `WedgeNet` | Testemunha de rede com translações triviais U=1 | A covariância trivial não fornece o elemento parabólico não trivial. |

O inventário refere-se às cópias de fonte examinadas, listadas no manifesto; não é uma busca negativa universal em todos os arquivos da máquina. Não foi demonstrada impossibilidade de toda inclusão no fator.

## C — domínio físico da forma v98

[REAL — ordem de trabalho] As seis razões foram lidas na ordem 005, antes desta encomenda. A derivação prévia desta ordem registra esse conhecimento. Não há seleção cega retroativa. Nesta rodada nenhuma nova observação foi buscada.

[DERIVED condicional] Se M(r)=κr em um intervalo e a descrição esférica newtoniana for aplicável, ρ(r)=κ/(4πr²) nesse intervalo e v_c²=Gκ. A fórmula não pode ser estendida automaticamente ao centro (singularidade) nem além da borda escolhida. O regime dinâmico e a definição da borda precisam ser independentes; dispersão não é velocidade circular sem anisotropia, perfil de traçadores e equação de Jeans. Virialização ou o rótulo “aglomerado” não determinam a normalização κ. A igualdade abstrata de pesos ½ não fornece um procedimento observacional para identificar essa borda em um objeto astronômico.

Condições que poderiam ser examinadas sem ler uma massa catalogada: geometria/borda definidas previamente; validade e estabilidade temporal do regime dinâmico; forma de uma curva cinemática em intervalo previamente fixado; perfil dos traçadores e anisotropia quando se usa dispersão. Essas verificações são condições de aplicação do modelo dinâmico, NÃO uma derivação do coeficiente universal. A escolha v_c≈βc/√(2π) já verifica o consequente da fórmula no regime circular; tolerância e intervalo precisariam ser fixados antes. Usá-la para escolher a amostra e depois contar concordância de massa reutiliza a mesma informação.

| Âncora histórica | Admissibilidade independente com os dados autorizados | Razão já conhecida M_form/M_lit, mostrada depois da classificação |
|---|---|---:|
| Grande Atrator | INDETERMINADA | 0,508063 |
| Coma | INDETERMINADA | 1,203308 |
| Norma | INDETERMINADA | 0,962647 |
| Laniakea | INDETERMINADA | 0,385059 |
| Via Láctea | INDETERMINADA | 48,132327 |
| Grupo Local | INDETERMINADA | 144,396982 |

A fonte é `ORDEM005_MASSA_CONTROLES.json`; são números históricos já autorizados, não medições novas nem estimativas de precisão observacional. Falta o conjunto de observáveis independente necessário para certificar entrada/saída. Não foi inventado corte por escala para excluir apenas as duas razões grandes. Perfis de igual raio podem ter normalizações diferentes; raio sozinho não determina o gradiente.

[OPEN] As premissas atuais não produzem um critério independente executável para as seis âncoras. Isso impede usar (iii) agora como lei física validada com domínio certificado. Não prova impossibilidade de qualquer critério futuro nem elimina a validade lógica de um enunciado condicional. A escolha editorial/histórica entre (i)/(ii)/(iii), o texto da errata e o JOINT_CONTOUR permanecem com o operador. O veto GA não foi alterado.

## Limites da entrega

Não há habitante não tracial global, integral modular Lean, translação positiva não trivial, reconstrução gravitacional geral, seleção observacional nova ou confirmação física nesta entrega. Não houve execução de um.py. Kernel, gate, acervo e memórias canônicas não foram escritos. A bancada entrega matemática e suas paredes; a gerência decide incorporação após auditoria independente. Nenhuma escolha matemática pendente foi atribuída ao operador como se fosse aprovação de prova.
