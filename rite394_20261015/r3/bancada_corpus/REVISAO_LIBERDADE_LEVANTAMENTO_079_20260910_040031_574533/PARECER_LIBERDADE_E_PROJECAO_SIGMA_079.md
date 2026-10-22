# Parecer independente: liberdade de levantamento e projeção sigma079

10/09/2026. [DERIVED — revisão matemática escrita delimitada] [REAL — medição documental]. Autor deste parecer: /root/selected_geometry_design. Revisão da nota de /root/prepare_integration_83, realizada separadamente de sua autoria. Este parecer pertence ao arco079 e não altera a entrega078.

**Conclusão: favorável no alcance enunciado, com duas precisões aditivas de domínio.** Não encontrei erro material nas espécies, nos sinais do sistema local, na projeção sigma ou no controle da corrente. As precisões são: interpretar o núcleo da projeção no complexo completo como ideal FECHADO por valência e conservar o anel de coeficientes herdado no alvo gravitacional. Nenhuma das duas autoriza reduzir a busca a uma classe menor sem demonstração.

Fonte revisada integralmente: [CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md](<C:/IALD/Central de Patentes/Chatgpt/LIBERDADE_DE_LEVANTAMENTO_079_20260910/CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md>), 15504 bytes, SHA-256 275d3fea7a26895ae705ef507457243a13bd4da671a63595d2673dd22aa4c53f. O manifesto da fonte foi lido e confrontado com os bytes atuais; os detalhes estão no recibo que acompanha este parecer.

## 1. Espécies e representação do núcleo

A relação de ghost nC−na−2nb=3 e a valência E=3+nu+2na+3nb fornecem exatamente uC³ em E4; u²C³ e u*C⁴ em E5; u³C³, u*uC⁴ e C*C⁵ em E6. Os antifields físicos são ímpares, os do ghost são pares. Jatos de um mesmo ghost são geradores ímpares distintos; portanto a presença de C⁵ com jatos não pode ser eliminada pelo número quatro de componentes sem derivadas.

A contagem cobre espécies, não contrações, ordens de jato ou dimensões de cohomologia. Coeficientes sem ghost adicional são uma hipótese essencial da nota; fontes externas de ghost positivo ou pares não mínimos mudariam a classificação.

Se a restrição de uma classe do núcleo a C3 é uma fronteira, uma primitiva em C3 admite prolongamento finito por valência. Subtrair seu diferencial elimina as componentes até E3 sem alterar a classe em C5. Portanto a procura por b4+b5 não perde os elementos desse núcleo. Esta é uma afirmação sobre a categoria de coeficientes local formal adotada, sem introduzir limite uniforme de ordem de jatos.

## 2. Diferencial e sinais do sistema (8–13)

A convenção efetiva é a do adendo KT077: s0u=R0C, s0u*=+H0u e s0C*=R0†u*. A ação071 confirma que não há potencial sigma. Com φ0 constante e a transformação cotangente correspondente, a mudança φ=Exp_φ0(tξ) dá s_tξ=t Lie_Cξ exatamente. A parte de gauge dos campos e do ghost termina em s1; os termos superiores das EOM nos antifields permanecem.

Refiz a comparação de valências. As equações (8) e (9) são s0b4=0 e s0b5+s1b4=0. Na valência seis, a correção fornece s0b6+s1b5+s2b4, e s2b4=0 porque b4 não contém antifields. O resíduo da classe077 já inclui os termos provenientes de seu líder e de suas componentes E4/E5; não cabe acrescentá-los outra vez ao sistema de β.

A expansão em parte sem antifields e parte linear neles reproduz (12) e (13). O fator 1/2 diante de D[u,u,R0C] vem de três variações de 1/6 D[u,u,u]. A variação do antifield em b5 produz +E2[u,u]R, sem inventar um fator adicional de Taylor. Com o antifield ímpar à esquerda,
s0(u*uE)=(H0u)uE−u*(R0C)E
e
s1(u*R)=(E2+Lie_Cu*)R−u*s1R.
Esses são precisamente os dois sinais negativos de (13). O termo s0(C*F)=R0†u*F tem sinal positivo.

Os pareamentos são pontuais entre jatos, não funcionais integrados. Derivadas dos antifields e das EOM devem acompanhar as contrações; integração por partes não pode ser usada silenciosamente para simplificar estas zeroformas.

O sistema é necessário e suficiente para fechamento em C6 de um representante da forma especificada. Esta suficiência é condicional à existência de operadores locais admissíveis P,Q,R,D,E,F que satisfaçam TODAS as identidades, não uma solução delas.

## 3. Projeção sigma e duas precisões de categoria

Na ação cinética071, φ=φ0 constante tem tensão e stress sigma nulos para toda métrica. A transformação de ξ permanece no ideal sigma; a de ξ* se anula na subvariedade ξ=ξ*=0. A contribuição sigma a h* e C* também desaparece nessa avaliação. O prolongamento aos jatos preserva essa propriedade. Isso verifica diretamente a estabilidade necessária para uma projeção BRST; não é deduzida apenas do fato de o fundo resolver as EOM.

**Precisão da completação.** No anel de polinômios finitos, usa-se o ideal diferencial gerado pelos jatos de ξ e ξ*. Na completação por valência, o mapa é definido coeficiente a coeficiente e é contínuo; seu núcleo é o FECHO desse ideal. Quando a ordem de jatos pode crescer com a valência, não se deve identificar automaticamente esse núcleo com o ideal algébrico formado por somas finitas de múltiplos de um número finito de geradores. A prova da nota funciona em cada truncamento e passa à projeção completa por compatibilidade, pagando exatamente esta leitura fechada.

**Precisão dos coeficientes.** O complexo Einstein de chegada deve conservar os coeficientes de referência e acoplamentos herdados, ou seus valores fixados consistentemente. A projeção não prova que uma primitiva com esses coeficientes pertença a um anel gravitacional mais restrito. A naturalidade simultânea pode ser conservada tratando os dados sigma remanescentes como parâmetros; exigir outra invariância ou eliminar parâmetros requer argumento próprio.

A projeção assim definida comuta com restrições e diferenciais de conexão. Logo (16) é uma condição necessária legítima para cancelamento no modelo completo. A recíproca não segue: um representante gravitacional que contenha h* recupera o stress sigma quando reinserido no modelo completo. A nota diz isso expressamente.

Este argumento usa o mapa sigma CONSTANTE do teste universal. Não é uma redução do habitante não constante φ=id do arco067 a matéria zero.

## 4. Avaliação TT e os antifields

O certificado078 fornece uma avaliação que anula s0 sobre todos os geradores e seus jatos: o campo satisfaz H0u=0, o ghost é combinação Grassmann de campos de Killing, e os antifields são avaliados em zero. Por isso ev(s0b6)=0 e ev(r6)=ev(A6).

Isso não faz ev(s1b5) desaparecer. Primeiro aplica-se s1; só então se avaliam os antifields. O termo h*R produz E_g,2[h,h]R, inclusive suas derivadas quando o pareamento usa jatos. Uma solução linear TT não resolve automaticamente a EOM quadrática. A fórmula (17) conserva exatamente esse termo.

Os termos sigma somem sob essa avaliação porque ξ=0 e E_sigma,2(h,0)=0 para qualquer h, juntamente com ξ*=0. Esta é uma propriedade do ideal sigma, não uma alegação geral de que uma EOM quadrática se anule sobre soluções lineares.

Consumo como antecedente o certificado078 pinado de ev(A6)≠0; esta revisão verifica seu uso no novo sistema e não declara uma nova execução ou uma segunda validação CAS daquele certificado.

## 5. Corrente natural e sinal da avaliação

Para a diferença exata de conexões torsion-free Θ, a identidade Θ^a_b∧dx^b=0 implica tr(Θ∧Rbar)=0 quando Rbar^a_b=K dx^a∧dx_b. Na transgressão ordinária, o termo 2 tr(Θ∧Rbar) se anula em todas as ordens, não só na primeira. Portanto seu coeficiente quadrático é tr(L∧Dbar L), sem contribuição adicional de Γ2.

A identidade tr(R∧R)=tr(W∧W), com W0=0, dá dJ2=tr(W1∧W1). Este é um cálculo de formas ordinárias; não torna J2 uma primitiva de s0.

Conferi o sinal de (21) com a normalização076: para J2=J^μ i_μ d⁴x, I_CJ2=J^μη_μ e s(J^μη_μ)=(∂_μJ^μ)η quando J é um vetor-densidade natural par. Na avaliação Killing, a referência é preservada e s1 faz J2 transformar pela derivada de Lie. Assim ev(s1 I_CJ2)=ev(I_C dJ2)=ev(A6), com sinal positivo e sem fator 4 ou 24. A variação do ghost faz parte da identidade; os campos de Killing escolhidos não precisam formar uma subálgebra de dimensão quatro para este passo.

## 6. Verificação independente do jato que impede o fechamento isolado

Refiz à mão o coeficiente específico de (22), na assinatura +---. Em coordenadas normais, com h22=(x1)² e h=∇h=0 no ponto, as partes relevantes são
L^1_2=x1 dx², L^2_1=−x1 dx² e L^2_2=−x1 dx¹.
Logo (Dbar L)^1_2=dx¹∧dx²; L(p)=0. O símbolo de s0L é +∂b∂μC^a, pois s0h=Lie_Cg0.

O jato livre ζ=∂0∂1C² produz (s0L)^2_1=ζ dx⁰. Seu produto com (Dbar L)^1_2, no traço, dá +ζ dx⁰∧dx¹∧dx². O outro componente com o mesmo ζ não encontra um fator Dbar L correspondente não nulo. O termo em que s0 varia o segundo fator contém L(p)=0. Avaliar a 3-forma em C0=θ0,C1=θ1,C2=θ2 produz +ζθ0θ1θ2.

Assim o coeficiente é +1. Curvatura de fundo multiplica jatos inferiores do ghost e não cancela este gerador livre de segunda ordem. O teste respeita as simetrias de uma conexão de Levi-Civita linearizada, pois L foi construído de h, e não escolhido independentemente.

Esse ghost não é Killing; isso é necessário para testar a identidade UNIVERSAL (9). O exemplo mostra que −I_CJ2 acerta a avaliação TT e falha ao fechamento se tomado isoladamente com b4=R=0. Ele não impede completar a corrente com outras correções.

## 7. Alcance final

[DERIVED] A nota fornece uma redução correta a um sistema local explícito, conserva as espécies de antifields relevantes, e exibe um controle que invalida o atalho de inferir ev(s1)=0 em toda a espécie h²C³.

[OPEN] Continua sem solução se −[A6] pertence à imagem de δ sobre o núcleo K. Não se demonstrou cancelamento, nem obstrução de todas as classes com o mesmo líder. A lista de espécies não fornece uma base tensorial finita sem controle adicional de jatos e coeficientes. Não se concluem H³/H⁴ completos, lim¹, Mittag–Leffler, QME, UV ou confirmação física.

A aprovação neste parecer é apenas da dedução escrita079 no alcance explicitado. Não transfere aprovações de077/078 nem atribui revisão independente a seus autores.

## 8. Custódia e execução

[REAL — documental] O recibo mede a nota, seu manifesto, o criador e as cinco referências declaradas, além da fonte076 usada para a identidade de avaliação. Os links locais da nota foram conferidos. As referências lidas permanecem com bytes idênticos entre as duas leituras desta revisão. A igualdade de pins antes/depois no manifesto anterior é conferida como registro histórico; não é apresentada como observação presencial desta revisão no momento de autoria.

O criador foi apenas medido como artefato, não executado nem revisado como programa. Nenhum um.py, CAS ou Lean foi executado/importado. Somente este parecer e seu recibo foram criados em pasta nova079 dentro de Chatgpt; nenhuma fonte existente foi alterada.
