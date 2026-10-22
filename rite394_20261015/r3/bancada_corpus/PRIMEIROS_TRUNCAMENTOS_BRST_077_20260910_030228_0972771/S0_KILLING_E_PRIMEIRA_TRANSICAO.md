# Primeiros truncamentos BRST: Killing, ghost três e falha de sobrejetividade

10/09/2026, arco077, separado da entrega076. [DERIVED — cálculo escrito] [KNOWN — cohomologia CE finita importada no alcance especificado] [REAL — fontes medidas]. Nenhuma fonte congelada, original ou um.py alterado; zero execução/importação de um.py, Lean ou CAS.

**Resultado calculado.** Na referência permitida de curvatura constante não nula com φ0 constante, o primeiro truncamento natural de ghost3 tem dimensão4. O mapa H³(C₄)→H³(C₃) tem imagem de dimensão1 e não é sobrejetivo. O primeiro grupo de ghost4, H⁴(C₄), é zero nessa categoria de referência. Quatro representantes de C₃ são naturais e universais; sua restrição ao teste mostra também que não se pode presumir a sobrejetividade da transição UNIVERSAL com coeficientes regulares. Isso não demonstra lim¹ não nulo nem sobrevivência no BRST completo.

A [comparação076 por truncagens](<C:/IALD/Central de Patentes/Chatgpt/MUDANCA_BASE_BRST_076_20260910_024632_6031800/MUDANCA_BASE_E_COMPLETACAO_H3_H4.md>) dá a razão de examinar essas transições. Aqui C_N significa valência E≤N, incluindo todas as ordens de jatos que ocorram FINITAMENTE num elemento; não significa corte na ordem de derivadas.

## 1. Parte linear do BRST mínimo no fundo on-shell

Mantenha a ação Einstein–sigma com alvo S³ e somente gauge difeomórfico. Desfaça o gauge e retire pares não mínimos antes de usar este complexo. B0=(g0,φ0) é inerte, on-shell, e os argumentos dinâmicos permanecem off-shell. As [convenções BV069](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md>) fixam sg=L_cg, sφ=L_cφ e sc=c·∂c.

Se u=(h,ξ), com h uma perturbação métrica covariante e ξ∈φ0*TS³, defina
\[
 R_0 c=\left(2\bar\nabla_{(\mu}c_{\nu)},
              c^\mu\partial_\mu\phi_0^a\right).
 \tag{1}
\]
Seja H0 a Hessiana da ação física no fundo, SEM fixação de gauge. A identidade de Noether, linearizada em uma solução, fornece
\[
 H_0R_0=0,\qquad R_0^\dagger H_0=0.
 \tag{2}
\]
H0 é formalmente autoadjunta, com os pareamentos densitizados da ação. Não se supõe que esse operador não fixado por gauge seja inversível ou normalmente hiperbólico.

Uma convenção canônica consistente para o quadrático mínimo
\[
 S_{2,\min}=\tfrac12\langle u,H_0u\rangle
              +\langle u^*,R_0c\rangle
\]
é
\[
 s_0u=R_0c,\quad s_0c=0,\quad
 s_0u^*=-H_0u,\quad s_0c^*=R_0^\dagger u^*.
 \tag{3}
\]
A derivada ímpar à esquerda de u*Rc em c atravessa u*; isso dá o sinal positivo na última fórmula. Trocar convenção canônica e os sinais dos antifields produz um complexo isomorfo. O conteúdo usado abaixo é (1), a nulidade de s0c e as identidades (2).

Escrevendo u*=(π^{μν},p_a) como densidades,
\[
 (R_0^\dagger u^*)_\nu
 =-2\bar\nabla_\mu\pi^\mu{}_\nu
      +p_a\partial_\nu\phi_0^a.
 \tag{4}
\]
Os graus dos geradores u,c,u*,c* são respectivamente 0,1,−1,−2. As fórmulas (1)–(4) são prolongadas a todos os jatos. A nilpotência de (3) segue de (2). No setor linear de geradores, este é o complexo dual de jatos associado a R0,H0,R0†; não se identifica sua cohomologia com uma contagem de campos físicos ou com o quociente Hadamard.

Na normalização Rees g=g0+t h, φ=Exp_{φ0}(tξ), c=tC,
\[
 s_t h=2\bar\nabla_{(\mu}C_{\nu)}+t\,\mathcal L_C h,\quad
 s_t\xi=C\cdot d\phi_0+O(t),\quad
 s_t C=t\,C\cdot\partial C.
 \tag{5}
\]
Os termos omitidos no segundo membro de s_tξ possuem valência maior que1. A parte s0 preserva valência; as demais partes a aumentam. Os termos KT constantes são zero porque B0 é on-shell. Essa é a condição que torna C_N um complexo. Os tadpoles da extensão por θ,ω usam outra filtração e não são incluídos silenciosamente neste C_N mínimo sem fontes.

## 2. O quociente linear dos jatos ghosts

Fixe os jatos de uma referência admissível no ponto p. Seja V_c o espaço real de combinações lineares FINITAS dos jatos de c. No grau de ghost1 dos geradores lineares,
\[
 W(B0,p)=V_c/
   \operatorname{span}\{\partial_I(R_0c)\}.
 \tag{6}
\]
As relações em (6) vêm de s0 dos jatos de h e ξ. A Hessiana e os antifields não acrescentam fronteiras lineares de ghost1: seus graus impedem isso.

O dual formal de (6) é o espaço de jatos de soluções
\[
 \mathcal L_vg_0=0,\qquad v\cdot d\phi_0=0,
 \tag{7}
\]
incluindo TODOS os prolongamentos. É a álgebra de Killing que preserva a matéria dessa referência, não uma reducibilidade universal dependente de jatos que valha para todo fundo.

A distinção produz um salto concreto de posto. Na região em que
\[
 d\phi_0^1,\ d\phi_0^2,\ d\phi_0^3,\ dQ_0
\]
são independentes, (7) implica v(p)=0, porque Q0 é um escalar natural preservado por (7). Diferenciar v·dφ0=0 dá, com v(p)=0,
\[
 (\bar\nabla_\mu v^\nu)\partial_\nu\phi_0^a=0.
\]
A imagem da matriz ∇v está contida no núcleo unidimensional de dφ0, enquanto ∇v é g0-antissimétrica por Killing. Uma matriz antissimétrica tem posto par; posto≤1 implica ∇v=0. A equação de Killing é de tipo finito: seus prolongamentos determinam os jatos seguintes por v,∇v e curvatura. Logo todos os jatos de v são zero e W=0 nessa fibra.

A [prova070 pelos quatro covetores](<C:/IALD/Central de Patentes/Chatgpt/NORMALIDADE_RELATIVA_070_20260909_233414/NORMALIDADE_FORMAL_E_RESIDUO_SUAVE.md>), com sua [precisão de Hessiano](<C:/IALD/Central de Patentes/Chatgpt/NORMALIDADE_RELATIVA_070_20260909_233414/PRECISAO_HESSIANO_SIGMA.md>), constrói jatos estacionários nessa região: dφ0^i=dx^i e um Hessiano misto B^1_01≠0 dá dQ0 proporcional a dx0. Sua prolongabilidade é a entrada KT já declarada ali. Não divido por esse determinante para produzir coeficientes universais.

Essa região não esgota as referências. O teste seguinte tem W de dimensão10. Portanto a ausência de reducibilidade UNIVERSAL de070 não autoriza declarar que cada referência tenha estabilizador trivial nem que (6) seja um módulo de posto constante.

## 3. Referência de curvatura constante: dez geradores restantes

Tome φ0 constante e um espaço forma Lorentziano com
\[
 \operatorname{Ric}(g_0)=\Lambda g_0,\qquad
 K=\Lambda/3\ne0.
 \tag{8}
\]
O tensor sigma é zero; (8) satisfaz as EOM do mesmo sistema com Λ>0. O teste é local, podendo ser feito em uma vizinhança globalmente hiperbólica adequada. A denominação de Sitter/anti-de Sitter depende da convenção; a álgebra de isometrias é uma das formas reais so(1,4), so(2,3), ambas com complexificação so(5,C). Não se escolhe FRW nem se acrescenta um tempo relacional.

As relações ∇_(a c_b)=0 deixam p_a=c_a e m_ab=∇_[a c_b] no primeiro jato. A identidade de integrabilidade de Killing determina ∇∇c por Rbar·c e, recursivamente, todos os derivados superiores por p,m; o fundo tem ∇Rbar=0. Portanto dim W≤4+6.

A existência das dez soluções é explícita pela realização local do espaço forma como uma quádrica não degenerada em dimensão5. Cada matriz a do grupo ortogonal ambiente fornece o campo X↦aX tangente à quádrica. No ponto, decompor o espaço ambiente como R X⊕T_pM mostra que a↦(v(p),∇_[a v_b](p)) permite valor tangente arbitrário e parte antissimétrica arbitrária. São dez dados independentes. Assim não há relações adicionais:
\[
 \boxed{W\simeq\mathfrak k^*,\quad \dim W=10,\quad
 W_\mathbb C\simeq V_\mathbb C\oplus
                  \Lambda^2V_\mathbb C.}
 \tag{9}
\]
Aqui 𝔨 é a álgebra de Killing de (8) e V é o vetor Lorentz de dimensão4.

O termo não linear sc=c·∂c induz sobre esse quociente o diferencial CE de 𝔨, com possível sinal global conforme se identifica o colchete dos campos fundamentais. Isso segue porque o colchete de dois Killing continua Killing e o ghost é precisamente a combinação ímpar desses campos. Um sinal global do diferencial não altera núcleos, imagens ou dimensões usados abaixo.

Este CE é o PRIMEIRO diferencial induzido sobre os ghosts residuais do complexo linear. Ele não é identificado com o BRST completo dos campos/antifields.

## 4. Contagem natural, não apenas coordenada

Considere zeroformas naturais com a orientação espaço-temporal admitida, na categoria restrita a (8) e φ0 constante. No ponto normal, todos os coeficientes de fundo são invariantes pelo grupo de isotropia G=SO⁺(1,3). Fixados Λ e o valor de φ0, eles são escalares reais para essa contagem. Não se permite um frame adicional ou vetor escolhido no espaço-tempo.

A semissimplicidade dos tipos tensoriais finitos permite tomar invariantes após quocientar pelas relações de (6). Assim os espaços de ghosts puros relevantes são (Λ^qW)^G. Complexificar não muda suas dimensões reais.

Escreva H=Λ²V. Na notação das duas cópias de sl2,
\[
 V_\mathbb C=(\tfrac12,\tfrac12),\quad
 H_\mathbb C=(1,0)\oplus(0,1).
\]
As decomposições necessárias são
\[
 \Lambda^2H=(1,0)\oplus(0,1)\oplus(1,1),\qquad
 \Lambda^3H=2(0,0)\oplus2(1,1).
 \tag{10}
\]
Além disso Λ³V≃V*, Λ⁴V é trivial e Λ⁴H≃Λ²H como módulos. Expandir Λ^q(V⊕H) dá:

| q | Parcelas que contêm escalares | dim(Λ^qW)^G |
|---|---|---:|
| 2 | nenhuma | 0 |
| 3 | Λ²V⊗H: dois; Λ³H: dois | 4 |
| 4 | Λ⁴V: um; Λ²V⊗Λ²H: dois | 3 |

A contagem é finita e foi feita por decomposição tensorial, sem CAS. Representantes de grau3 podem ser escolhidos como as duas cúbicas invariantes de m e os dois emparelhamentos
\[
 m_{ab}p^ap^b,\qquad
 \epsilon_{abcd}m^{ab}p^cp^d.
 \tag{11}
\]
As cúbicas são as combinações reais par/ímpar dos volumes das duas partes autoduais complexificadas de Λ²V. Equivalentemente podem ser escritas pelas contrações invariantes com η e ε em três fatores m. São formas reais e independentes. Multiplicar os dois termos de (11) por Λ, constante não nula, iguala seu peso de engenharia ao das cúbicas: ∇c tem peso0, enquanto c tem peso−1. Todos são pares sob O(4) do alvo, pois não usam a matéria ou a orientação do alvo.

## 5. Cálculo dos primeiros grupos e da primeira transição

Use C_N=A_nat/F^{N+1}, em que cada campo, ghost ou antifield normalizado conta como uma perna. Para ghost g>0, a valência mínima é g, realizada somente por g ghosts c, pois nenhum gerador tem ghost maior que1.

### 5.1 Ghost três em C₃

C₃³ contém apenas cúbicas nos jatos ghosts. São automaticamente fechadas: s0c=0 e sc é quadrático, cuja ação em uma cúbica tem valência4, descartada em C₃.

Uma fronteira de ghost3 pode vir de:

- ghost2/valência2: duas cópias de c, cujo BRST quadrático induz d_CE:Λ²W→Λ³W;
- ghost2/valência3: um campo físico e dois ghosts, cujo s0 gera o ideal linear R0c multiplicado por dois ghosts.

Antifields não cabem nesses graus: um antifield físico de ghost−1 precisaria de três ghosts para produzir ghost2, tendo já valência4. Após retirar o ideal R0c e tomar invariantes,
\[
 H^3(C_3)\simeq
 \frac{(\Lambda^3W)^G}{d_{\rm CE}(\Lambda^2W)^G}.
\]
Como o denominador é zero pela tabela,
\[
 \boxed{\dim H^3(C_3)=4.}
 \tag{12}
\]

### 5.2 Quais dessas classes se levantam a C₄?

Uma correção de ghost3/valência4 tem a forma de um campo físico multiplicado por três ghosts. Sua variação por s0 gera precisamente o ideal R0c no grau4. Logo uma cúbica α de (12) admite levantamento a C₄ se e somente se
\[
 d_{\rm CE}\alpha=0
       \quad\text{em }\Lambda^4W.
 \tag{13}
\]
A suficiência merece ser dita: se (13) vale, a variação original sα de valência4 pertence ao ideal linear gerado pelos jatos de R0c. Cada termo finito desse ideal tem preimagem pelos jatos de u. Isso fornece a correção u·c³. A projeção no tipo trivial de G torna a escolha natural sem alterar a equação. A ordem de jatos é finita nesse coeficiente.

[KNOWN] Para a álgebra real 𝔨 em (9), H³_CE(𝔨,R) tem dimensão1: sua complexificação é so(5,C), cujos geradores primitivos têm graus3 e7. A importação é apenas de cohomologia de uma álgebra de Lie FINITA. Consulte [BBH1995, seção7.1 e Apêndice B](https://arxiv.org/pdf/hep-th/9505173v2), incluindo m(K)=2K para so(2r+1). Não se importa dali uma classificação do BRST Einstein–sigma completado.

A ação da isotropia na cohomologia CE é trivial por Cartan. Tomar invariantes é exato nos módulos finitos. Como (Λ²W)^G=0, segue
\[
 \dim\ker[d_{\rm CE}:(\Lambda^3W)^G
                  \to(\Lambda^4W)^G]=1.
\]
Portanto
\[
 \boxed{\dim\operatorname{im}
      [H^3(C_4)\longrightarrow H^3(C_3)]=1<4.}
 \tag{14}
\]
A Hessiana e os antifields podem alterar outros componentes de H³(C₄), mas não essa imagem: não aparecem em ghost3/valência≤3, e a condição do levantamento é exatamente (13).

### 5.3 Primeiro ghost quatro

C₄⁴ contém somente quatro ghosts. As fronteiras relevantes são s de três ghosts e s0 de u·c³. Assim
\[
 H^4(C_4)\simeq
 \frac{(\Lambda^4W)^G}
      {d_{\rm CE}(\Lambda^3W)^G}.
\]
Pela tabela, o numerador tem dimensão3; o mapa no denominador tem posto4−1=3. Logo
\[
 \boxed{H^4(C_4)=0}
 \tag{15}
\]
nessa categoria de referência. Não se conclui H⁴ do sistema universal ou da completação. C₄ é um corte por valência; uma classe que só começa em valência maior não foi examinada.

Como controle da importância de impor naturalidade, se se permitissem coeficientes coordenados arbitrários nos ghosts, (12) teria dimensão120−35=85 e o análogo de (15) dimensão210−84=126. Esses números NÃO são os grupos naturais usados em (12)–(15); os resultados principais mantêm G.

## 6. Consequência para a transição universal

A obstrução (14) não precisa permanecer apenas uma dimensão de fibra. Escolha, para qualquer B0, os quatro polinômios naturais universais de (11) e as duas cúbicas, usando
\[
 p=c,\qquad m_{ab}=\bar\nabla_{[a}c_{b]},
\]
contrações por g0/volume e o fator Λ nos termos com dois p. São expressões regulares de ghost3 e valência3, com ordem de jatos finita e sem inversos de gradientes. Como sB0=0 e sc é quadrático, todas são ciclos em C₃ UNIVERSAL.

A restrição à categoria (8) com φ0 constante é mapa de complexos e seus valores formam a base de (12). Se os quatro ciclos admitissem levantamentos universais a C₄, regulares nessa categoria, suas restrições levantariam as quatro classes de (12). Isso contradiz (14). Mais precisamente, o subespaço de combinações lineares desses quatro controles que admite um levantamento universal tem dimensão no máximo1.

Assim:
\[
 \boxed{\text{não há sobrejetividade universal automática de }
 H^3(C_4)\to H^3(C_3)
 \text{ na classe regular que contém esse teste}.}
 \tag{16}
\]
A prova usa o teste para refutar um levantamento universal alegado; não identifica a cohomologia universal com a cohomologia da referência. Ela também não presume que todo ciclo da fibra seja restrição de um ciclo universal: neste caso os quatro representantes foram escritos antes da restrição.

Uma categoria que excluísse as referências simétricas por inversos de dφ0 ou escolhesse um frame/tempo extra poderia não receber (16). Essa seria uma categoria diferente. Não a introduzimos.

## 7. O que este cálculo decide e o que não decide

[DERIVED] s0 é o complexo linear de jatos de R0,H0,R0†. O quociente ghost positivo é controlado pelos Killing que preservam a matéria de B0, e seu posto muda entre os jatos do controle genérico e a referência simétrica. A ausência de reducibilidade universal não apaga esse salto de estabilizadores.

[DERIVED] O primeiro corte natural foi calculado: quatro classes de ghost3 em C₃; somente uma dimensão na imagem desde C₄; ghost4 em C₄ é zero no teste. Há, portanto, uma obstrução concreta a supor transições cohomológicas sobrejetivas para todas as truncagens.

Isso NÃO implica que lim¹H³(C_N) ou lim¹H²(C_N) seja não nulo. Uma transição inicial não sobrejetiva é compatível com estabilização posterior das imagens; o critério suficiente de sobrejetividade de todas as transições da nota076 simplesmente não pode ser consumido sem análise. Igualmente, o único sobrevivente do teste CE não foi levantado até todas as ordens nem identificado com uma classe da teoria interagente.

Os próximos dados matemáticos efetivos são as imagens estabilizadas H²(C_M)→H²(C_N) e H³(C_M)→H³(C_N), M≥N, ou uma homotopia completa com controle da filtração. As equações de movimento lineares e os antifields começarão a participar de forma material nos graus/valências seguintes. Nenhuma conclusão de anomalia não nula, remoção de anomalia, QME, positividade interagente ou UV é extraída deste primeiro cálculo.

As fontes medidas e os arquivos próprios são registrados no manifesto. A análise é escrita e ainda depende de revisão independente; nenhuma revisão anterior é reaproveitada como aprovação deste resultado novo.

