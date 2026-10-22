# Parecer independente: candidatos Weyl CCm e dual079

10/09/2026. [DERIVED — revisão matemática escrita delimitada] [REAL — custódia documental]. Autor: /root/selected_geometry_design. A nota revisada foi construída por /root/finish_gibbs_realization; esta revisão é independente de sua autoria.

**Parecer favorável, sem erro material identificado no alcance anunciado.** Li integralmente a [nota dos dois candidatos](<C:/IALD/Central de Patentes/Chatgpt/CANDIDATOS_WEYL_E_OBSTRUCAO_079_20260910_041607_7604358/WEYL_CC_M_E_FALHA_DO_COMPLETAMENTO.md>) e seu manifesto; conferi as remissões pertinentes ao sistema079, à correção KT077, ao dicionário Cartan e ao habitante linear078. A fonte tem 16685 bytes e SHA-256 4436140a9b0f3164c2fca0237f1bd4389ad1cbf5a61d4fbfd82ff0ef52b6aeb5.

A exclusão obtida aplica-se aos membros NÃO NULOS da família restrita ao fundo/teste declarado. Não exclui b4=0 com outras correções Q/R, outros ciclos b4 nem coeficientes que sejam zero neste teste e não em outras referências.

## 1. Espécies, fechamento inicial e sinal de A

P=W_abcd C^a C^b m^cd tem ghost3 e valência quatro, com m_ab=∇_[a C_b] incluindo o fator 1/2. Em um ghost Killing, A^a_b=∇bC^a satisfaz A_ab=−m_ab. O Weyl linear é s0-invariante porque W0=0; portanto P e seu dual satisfazem s0P=0 antes de restringir o ghost a Killing.

Refiz a conversão do traço:
tr(AU)=−m^a_b W^b_acd C^cC^d/2
=+m^ab W_abcd C^cC^d/2.
A antissimetria da primeira dupla fornece o segundo sinal; a troca das duplas de W produz P/2. Logo P=+2tr(AU), apesar de A ser −m com índice elevado. A convenção KT efetivamente usada é a corrigida +H0u; a ocorrência histórica de −H0u na fonte077 é acompanhada pelo adendo que a corrige e não é reaplicada nesta nota.

## 2. s1A, s1U e o traço graduado

s1p=C·∇C=−Ap, pela troca de dois fatores ímpares. Para a convenção de curvatura da casa, a integrabilidade Killing em curvatura constante dá
∇b∇eC^a=K(δ^a_b C_e−δ^a_d g_eb C^d).
Na derivada de C^e∇eC^a, o produto dos primeiros jatos é −A²; o termo de segundas derivadas é +Kpp♭. Isso confirma s1A=−A²+Ω0 com o sinal de (10).

A equivariância de W[1] sob as isometrias da referência fornece a derivada de Lie do tensor, incluindo seus quatro índices. Nos dois índices internos End(TM), restam −AU+UA. Nos dois índices de 2-forma, as parcelas ∇C cancelam as variações dos dois C de U, usando s(C^cC^d)=(sC^c)C^d−C^c(sC^d). O termo de transporte não é descartado: V=(C·∇W)CC/2. Assim (11) é s1U=UA−AU+V.

Como A é ímpar e U par, s tr(AU)=tr((sA)U−A(sU)). A ciclicidade é graduada: tr(AUA)=−tr(A²U). Substituir as duas transformações resulta exatamente
s1P=2tr(Ω0U+A²U−AV).
O sinal positivo de A²U é essencial e foi conferido, sem tratar A como uma matriz par.

O dual na segunda dupla preserva a troca das duplas para Weyl em quatro dimensões: o operador de Weyl em duas-formas comuta com Hodge, e a obstrução seria a Ricci sem traço ausente nesse tensor. Os Killing locais preservam o Hodge da referência; as mesmas fórmulas se aplicam ao dual. Isso não exige uma identidade diferencial adicional para eliminar V.

## 3. Realização dos quatro jatos de Killing

Os dados (valor, derivada antissimétrica) escolhidos na tabela (14) são realizáveis por campos de Killing genuínos, não apenas por primeiros jatos independentes sem continuação. No modelo de quádrica, para um ponto X e um vetor tangente v, escolha uma transformação ambiente antissimétrica B com BX=v; na decomposição RX⊕T_XM, sua parcela tangente pode ser qualquer A antissimétrica. Explicitamente, sobre um vetor tangente Y, B Y=A Y−<v,Y>X/<X,X>. A projeção tangente dessa expressão é A Y, logo a derivada covariante no ponto é a desejada. Essa construção também produz o prolongamento dos jatos em uma vizinhança.

Assim existem os dois Killing com valores e0,e1 e derivada covariante zero e os dois com valor zero e derivadas J02,J12. A matéria constante é preservada. Em p, C usa somente θ0 e θ1; por isso C³=0, V=0 e Ω0U=0. Não se usou uma Bianchi adicional para anular o transporte.

A matriz J02 envia e2↦e0 e e0↦e2; J12 envia e2↦−e1 e e1↦e2. O comutador é J01, com tr(J01²)=2 e tr(J01J23)=0. Os produtos Grassmann dão A²=θ2θ3 J01 e U=W01^End θ0θ1, sem fator dois adicional. Mover os dois últimos geradores através dos dois primeiros conserva o sinal. Isso confirma a fórmula de avaliação (18).

## 4. Solução TT, ponto normalizado e dual

A EDO e a solução TT078 valem em uma vizinhança e anulam H0(h,0), juntamente com todos os jatos das EOM. Isso é o que permite usar a avaliação para testar s0-exatidão mesmo com antifields de ordem arbitrária finita.

A escolha z0=ell dá a(p)=1 no mesmo fundo com K=1/ell². A base coordenada é ortonormal no ponto, embora não seja necessariamente uma coordenada normal para a conexão. Os jatos de Killing usados são COVARIANTES, portanto a conexão coordenada não nula não invalida a tabela. A escala entre o Weyl com índices baixos e o cálculo conforme é justamente um nesse ponto.

As componentes078 são W0101=−1/(2z0) e W2301=W0123=k/2. Levantar o primeiro índice dá W01^End=−aW J01+bW J23; daí 2tr(J01 W01^End)=−4aW=−2/z0.

Com epsilon0123=+1 e assinatura +---, elevar os índices 2 e 3 introduz dois sinais negativos: epsilon^23_01=+1. O fator 1/2 do dual é cancelado pelos pares 23/32. Consequentemente (W*)0101=W0123=bW, e a segunda avaliação é +4bW=+2k. Não se dualizou silenciosamente a primeira dupla nem se importou uma convenção euclidiana de *².

Essas verificações foram feitas por álgebra escrita. Não houve CAS, Lean ou reexecução do certificado078.

## 5. Obstrução ao completamento e comparação dos dois sinais de k

A avaliação anula todo s0F porque usa soluções lineares e ghosts Killing em uma vizinhança, com todos os antifields zero. Não é necessário que os quatro Killing fechem uma subálgebra: a chegada tem diferencial zero para s0. A nota também não define s1 por aplicar um diferencial à expressão já avaliada.

Como s0P=0, s1P é s0-fechado. As avaliações não nulas mostram que ele não é exato. Portanto Q[u,R0C] e todos os jatos de H0u emparelhados com R não podem cancelar s1P em (5). A permissão de antifields, derivadas finitas altas ou coeficientes coordenados regulares na primitiva não muda esse certificado.

Para lambda P+mu P*, os coeficientes herdados ficam fixos quando se varia somente a solução h_k. Avaliar em k e −k dá −2lambda/z0±2mu k. A anulação universal nas duas soluções força os DOIS valores escalares lambda e mu a zero no teste. Isso exclui qualquer combinação cujo par de coeficientes restritos seja não nulo. Não força coeficientes universais a serem zero em referências onde não foram avaliados.

Adicionar uma fronteira s0B não altera a classe detectada, pois s1s0B=−s0s1B. Adicionar outro ciclo independente pode alterá-la e não foi excluído. A formulação final sobre reparar a corrente quadrática deve conservar o qualificativo “membros não nulos desta família”: o certificado não elimina a escolha b4=0 acompanhada de outros Q/R, nem enumera todos os candidatos P.

## 6. Fronteira e custódia

[DERIVED] O resultado exclui a família calculada já na equação de valência cinco. Não é um novo teste de A6: nesta avaliação só dois valores de C são independentes, de modo que C⁴ e A6 se anulam. O valor detectado tem tipo W[1]C²m² e pertence a H⁴(s0) em valência cinco. Essa distinção impede trocar ghost4 por valência seis ou reutilizar o detector como se ele medisse o resíduo078.

[OPEN] Permanecem outros ciclos lineares, correções mistas e a questão −[A6]∈δ(K). Não foram decididos o levantamento de toda a linha CE, Mittag–Leffler, lim¹, anomalia efetiva, QME ou UV. A aprovação é apenas da família e de seu certificado escrito.

[REAL — documental] O recibo mede a nota, o manifesto, o script de medição e as cinco fontes, confronta os pins históricos e verifica os cinco links locais. A conferência do script de medição é somente de custódia, sem execução ou revisão nova de sua implementação. As fontes permanecem com os mesmos bytes entre as duas leituras desta revisão. Somente este parecer e seu recibo foram escritos em pasta nova079; nenhum original, documento078 ou um.py foi alterado/executado.
