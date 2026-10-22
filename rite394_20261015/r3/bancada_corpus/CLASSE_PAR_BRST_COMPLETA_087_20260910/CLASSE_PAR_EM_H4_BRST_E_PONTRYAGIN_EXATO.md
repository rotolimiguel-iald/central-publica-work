# Uma classe par não nula no BRST completo e a exatidão de Pontryagin

10/09/2026. Investigação087. Autor: raiz. [DERIVED — demonstração escrita proposta à revisão independente]. A entrada CE quadrática087 também está sob revisão própria. As duas revisões precisam ser consumidas antes da consolidação desta composição; a existência do texto não é uma compilação Lean.

**Resultado no contrato fixado:** a densidade natural completa I(g)vol_g, com I(g)=½W(g)², fornece um ciclo A_I de ghost quatro cuja classe gera uma cópia livre de Rher em H⁴(C_N,s) para todo N≥6 e em H⁴(Ĉ,s), onde Ĉ é a completação por valência já definida. Em contraste, a densidade completa de Pontryagin A_P é s-exata por uma primitiva explícita. A prova da não exatidão de A_I inclui primitivas com antifields e é detectada já em C₆; não usa intercâmbio de cohomologia e limite inverso.

Não se afirma que H⁴ seja apenas essa linha. Também não se infere anomalia quântica de ghost um, QME ou suficiência física geral.

## 1. Categoria e dados que serão efetivamente usados

Fixe a referência espaço-forma Lorentziana orientada de dimensão quatro, K>0 real fixado, κ real não nulo e sigma constante já projetado ao complexo métrico mínimo. Rher é uma álgebra real unital não nula, de ghost zero e inerte para os operadores fixados. Os coeficientes de cada valência usam finitos jatos, sem tensores espectadores ou dependência coordenada ativa. O complexo inclui os antifields métricos e de ghost; não é um subcomplexo obtido apagando-os.

Escreva A_E para a parcela de valência E, s=s₀+s₁+s₂+…, onde s_j aumenta E em j e ghost em um. Como a referência é on-shell, s não diminui valência. Defina C_N=Ĉ/F^(N+1) e Ĉ=∏_(E≥0)A_E com a completação ALGÉBRICA por valência. Cada coeficiente conserva ordem finita de jatos. As projeções são mapas de complexos.

Os resultados usados são:

- [Transgressão076](<C:/IALD/Central de Patentes/Chatgpt/TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md>) e seu [parecer específico](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_TRANSGRESSAO_BRST_076_20260910/PARECER_TRANSGRESSAO_TOTAL_E_GHOST4.md>): sg=Lie_cg, sc=c·∂c e uma primitiva natural formal T_P para A_P, preservando o termo sS do transporte métrico.
- [Levantamento077](<C:/IALD/Central de Patentes/Chatgpt/SOBREVIVENTE_PONTRYAGIN_077_20260910/PONTRYAGIN_CE3_E_LEVANTAMENTO_C5.md>) com [parecer posterior](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_077_20260910/PARECER_PONTRYAGIN_E_C5_077.md>): im[H³(C₅)→H³(C₃)]=Rher[α₃], com α₃ líder do ciclo T_P,≤5.
- [Transferência080](<C:/IALD/Central de Patentes/Chatgpt/TRANSFERENCIA_DELTA_PARA_E5_080_20260910/IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md>): se Kcal=ker[H³(C₅)→H³(C₃)], então δ(Kcal)=im(d₁:H³(A₅,s₀)→H⁴(A₆,s₀)), para a conexão δ de C₆→C₅.
- [Identificação082](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>): a diagonal m=E−ghost=2, depois de H(s₀), é o complexo C(g,N₂)^h, com diferencial induzido por s₁.
- [Cálculo quadrático087](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612/GERACAO_CURVA_RELATIVO_E_CE_QUADRATICO.md>): H⁴ desse CE é Rher[I₀ν]⊕Rher[J₀ν], com I₀=½W[1]² e J₀=J_W. Para a presente prova basta a INDEPENDÊNCIA dessas duas classes; a exaustão de H⁴ CE é informação adicional da fonte.

As fontes077/080/082 são consumidas com seus pareceres independentes pinados no manifesto. O estado da086 foi relido, não presumido pelo nome. A notação H³ cohomológica não designa o H3 interno da reconstrução do programa. J_W não é J=Luz; Mcal não é a matriz de ghosts.

## 2. Ciclo natural completo associado à densidade par

Para a métrica dinâmica formal g=g₀+t h, use sua própria curvatura de Weyl W(g), sua inversa métrica e seu volume orientado. Defina

       I(g)=½W_abcd(g) W^abcd(g),
       Ω_I(g)=I(g) vol_g,
       Ω_I=ρ_I(g) dx⁰dx¹dx²dx³,
       A_I=ρ_I(g)c⁰c¹c²c³,              c=tC.           (1)

A expressão A_I é escalar sob mudanças FIXAS de coordenadas orientadas: substitui os quatro geradores exteriores de uma forma natural pelos quatro ghosts vetoriais. O volume e os índices contraídos são os de g, não os de g₀ congelados durante a transformação ativa. A referência serve para expandir formalmente a expressão, não para substituir sua lei de transformação.

Como Ω_I é uma quatro-forma natural da métrica, sua variação ativa é Lie_cΩ_I. Em coordenadas, isso diz

       sρ_I=c^μ∂_μρ_I+(∂_μc^μ)ρ_I.                    (2)

É possível verificar o fechamento diretamente, incluindo os sinais. Ponha G=c⁰c¹c²c³. A regra de Leibniz ímpar e sc^μ=c^ν∂_νc^μ dão

                         sG=−G∂_μc^μ.                  (3)

No termo em que se deriva c^μ, só a parcela ν=μ pode sobreviver: para ν≠μ um dos três outros ghosts é repetido. Mover ∂_μc^μ através dos ghosts à direita dá o sinal (−1)^(3−μ), que, multiplicado pelo (−1)^μ de Leibniz, é sempre −1. Isso prova (3) sem assumir que as derivadas dos ghosts sejam números comutativos.

Por outro lado, (c·∂ρ_I)G=0 pela repetição de um quinto ghost de valor. O produto G tem paridade par, então o termo restante de (2) cancela ρ_IsG. Portanto

                              sA_I=0.                   (4)

Essa conta é off-shell e não usa antifields, as EOM de h ou uma integração por partes. As EOM entram somente depois, ao examinar todas as possíveis fronteiras no complexo mínimo completo. O fechamento de (4) não decide sozinho a não exatidão.

## 3. Primeiro coeficiente e admissibilidade algébrica

W(g₀)=0 e a variação linear W[1] é s₀-invariante. Logo

       W(g₀+t h)=tW[1]+O(t²),
       I(g₀+t h)=t²I₀+O(t³),
       vol_(g₀+t h)=vol₀(1+O(t)).

As quatro pernas de c=tC acrescentam quatro unidades de valência. Assim

                    A_I=t⁶I₀ν+O(t⁷),                  (5)
       ν=vol₀(C,C,C,C)/4! na convenção de avaliação
         antissimétrica, ou √|det g₀| C⁰C¹C²C³
         na convenção de coeficiente exterior ordenado.

A primeira escrita de ν usa a contração de componentes totalmente antissimétricas com os quatro ghosts e o fator1/4!; não significa avaliar uma forma alternada quatro vezes no MESMO vetor comutativo. Os ghosts anticomutam. A convenção ordenada da segunda escrita fixa a normalização sem ambiguidade.

Cada coeficiente de g⁻¹ e do volume é polinomial em h com coeficientes da referência. Pode-se escrever formalmente vol_g=vol₀ exp[½ tr log(1+t g₀⁻¹h)], com termo constante1. Não é necessária uma raiz real entre métricas afastadas. W(g) envolve jatos de g até ordem dois; por isso cada coeficiente de (1) é local e usa finitos jatos. Em uma valência fixada entram somente finitíssimas parcelas das séries formais.

Portanto A_I pertence à mesma completação por valência que a transgressão076. Não se ressoma t numericamente e não se introduzem inversos de t, gradientes sigma ou operadores diferenciais. Essa pertença é algébrica; não certifica as exigências de escala, contatos e normalização causal de produtos temporais.

## 4. Toda a imagem da conexão em C₆, incluindo antifields

A sequência curta

             0→(A₆,s₀)→C₆→C₅→0

tem conexão δ:H³(C₅)→H⁴(A₆,s₀). Escreva T=T_P,≤5. Pela transgressão e sua expansão078, δ[T]=[J₀ν]. O resíduo do truncamento pode diferir do coeficiente característico por −s₀T_[6], que não altera essa classe.

Todo y∈H³(C₅) tem imagem λ[α₃] em C₃, com λ∈Rher. Assim y−λ[T]∈Kcal. Aplicando a igualdade de imagens080, obtemos

          im δ = Rher[J₀ν] + im d₁|_(E=5)              (6)

como submódulos de H⁴(A₆,s₀). A inclusão da direita em imδ também vale: a primeira linha vem de T, e o segundo submódulo vem de δ(Kcal). Não se requer uma cisão global de H³(C₅) nem se afirma que Kcal seja zero.

A transferência080 tratou primitivas e correções no complexo COM antifields. Sua eliminação usa a exatidão linear e as EOM, não uma restrição inicial aos representantes sem antifields. Portanto (6) restringe qualquer fronteira admissível no complexo aqui fixado.

## 5. Não exatidão já no truncamento C₆

Suponha que λ(A_I mod C₆)=sB em C₆, com B de ghost três. Em C₅, o lado esquerdo é zero por (5), de modo que y=[B mod C₅] pertence a H³(C₅). A definição da conexão dá

                           δy=λ[I₀ν].                  (7)

O componente B_[6] só acrescenta uma fronteira s₀ ao representante de (7). Por (6), existem μ∈Rher e uma classe z de ghost três/E5 tais que

                       λ[I₀ν]−μ[J₀ν]=d₁z               (8)

em H⁴(A₆,s₀). Os dois alvos são ciclos do primeiro diferencial; tomar sua cohomologia pela identificação082 transforma (8) em

                    λ[I₀ν]=μ[J₀ν] em H⁴ CE.            (9)

A independência das duas classes no cálculo087 força λ=μ=0. Ela é sobre o anel real herdado inteiro, incluindo nilpotentes. Não se testou a igualdade apenas em valores numéricos dos coeficientes.

Concluímos a injeção

          Rher → H⁴(C₆,s),   λ ↦ λ[A_I mod C₆].         (10)

Este argumento não confunde H⁴ CE com H⁴(C₆). Usa exatamente a imagem da conexão entre os truncamentos para decidir quais classes CE podem virar fronteiras. O termo J₀ν está nessa imagem; o termo I₀ν não está.

## 6. Todos os truncamentos posteriores e o complexo formal

Por (4), A_I mod C_N é ciclo para todo N≥6. Se algum múltiplo λ dessa classe fosse fronteira em C_N, sua projeção em C₆ também seria fronteira, contrariando (10), salvo λ=0. Portanto

       Rher ↪ H⁴(C_N,s) para todo N≥6,
       λ ↦ λ[A_I mod C_N].                              (11)

As classes construídas são compatíveis com todos os mapas de truncamento, pois vêm da MESMA expressão A_I. Da mesma forma, uma fronteira λA_I=sB em Ĉ se projetaria em uma fronteira em C₆. Logo

                  Rher ↪ H⁴(Ĉ,s),   λ↦λ[A_I].            (12)

A prova de (12) é detecção por uma projeção de complexos. Não identifica H⁴(Ĉ) com lim H⁴(C_N), não troca limite e cohomologia, não calcula lim¹ e não usa Mittag-Leffler. Tampouco exige uma cota uniforme para a ordem de jatos de TODA primitiva: uma primitiva formal permitida teria um truncamento finito em C₆, e isso já é impossível.

Não foi demonstrada exaustividade de (11–12). Outros ciclos, outros primeiros graus de valência e outras classes podem existir. O resultado é uma linha livre não nula efetivamente construída na cohomologia do diferencial s completo do teste.

## 7. Por que o pseudoescalar de Pontryagin se comporta de outro modo

Defina A_P pela densidade tr(R(g)∧R(g))=tr(W(g)∧W(g)), com a normalização076. Sua expansão começa em t⁶J₀ν. A transgressão fornece

       S=(g₀⁻¹g)^(1/2),
       k=S(∇c)S⁻¹−(sS)S⁻¹,
       Ω=sk+k²,
       T_P=tr(kΩ)−⅓tr(k³),
       sT_P=A_P.                                        (13)

Todas essas expressões são formais naturais e finitas em cada coeficiente. O termo sS é parte do transporte; não pode ser omitido. Consequentemente A_P é fronteira em Ĉ e em cada C_N após truncar a própria primitiva.

Seu líder J₀ν, contudo, é não nulo em H⁴ CE quadrático. Isso é compatível: a primitiva T_P começa em valência TRÊS, e a relação sT_P=A_P mistura valências. O primeiro diferencial CE da diagonal m=2 não vê sozinho essa primitiva de valências inferiores. A igualdade(6) conserva essa contribuição precisamente pela conexão dos truncamentos.

Assim os dois alvos têm destinos distintos no BRST completo: [A_P]=0 por construção, enquanto Rher[A_I] é livre e não nulo. A classificação da diagonal CE não pode ser promovida em bloco à cohomologia total. Esta nota não depende de rotular a seta como um diferencial de determinada página; a interpretação por páginas deve manter sua convenção de índices explícita.

## 8. Consequência para o objetivo e limites

[DERIVED — sujeito às revisões indicadas] Obtivemos uma informação sobre H⁴(s COMPLETO) do teste, além de H(s₀) e do primeiro CE. A linha par tem representante natural completo e detector em C₆ que inclui todas as primitivas com antifields. A linha característica ímpar possui uma primitiva completa explícita.

[OPEN] O critério suficiente de anomalias em estudo não exige que H⁴(s) inteiro seja zero: ele envolve também a cohomologia horizontal com coeficientes nesse módulo. Logo (12) não refuta o critério e não demonstra anomalia física. Ainda é necessário calcular a ação horizontal pertinente e os outros grupos, na mesma classe de coeficientes, além da admissibilidade causal.

O teste fixa sigma constante; esta prova não transporta suas classes ao fundo sigma físico não constante, a categorias com espectadores, a séries de infinitos jatos em um coeficiente ou a operadores que variem com novos campos. Não é cálculo de um coeficiente de anomalia quântica, de QME, de positividade interagente, de UV ou da reconstrução geral pelos mesmos dados selecionados.

Os resultados anteriores de fase/ramo e H3 interno do programa continuam distintos desta cohomologia. Nenhum gate é alterado por (10–13). A TGL inteira não recebe um veredito de confirmação ou falsificação a partir desse teste local.

[REAL — custódia] Somente arquivos novos em Chatgpt. Os pins são lidos dos bytes antes/depois; não são contagem de provas. Zero execução matemática, CAS, Lean, teste de natureza ou execução/importação de um.py nesta nota. A revisão independente da entrada quadrática087 e desta composição será ligada em adendo posterior; os estatutos históricos permanecem intactos.
