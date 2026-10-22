# Mudança de base em H(s): domínio válido, completação e uma classe global perdida

10/09/2026, arco076. [DERIVED — demonstrações escritas de própria autoria] [KNOWN — mecanismo de tipos finitos e Cartan, com referência primária] [REAL — fontes medidas no manifesto]. Nenhum original, nota congelada ou um.py foi alterado; nenhum um.py, Lean ou CAS foi executado/importado.

**Resultado delimitado.** A mudança de base é demonstrável para a álgebra de somas tensoriais FINITAS, antes da completação diagonal, com tipos Lorentz localmente finitos. Isso vale inclusive quando os coeficientes inertes de B0 são quocientados por relações apenas de B0. Não demonstra a isomorfia μ da seção5 da nota de módulos076 na classe Rees completa: ainda é necessário identificar os representantes por K e controlar a completação. Há uma perda real de classe ao transportar a álgebra GLOBAL sem espectador ao domínio formal da diagonal: o ciclo de volume do alvo tem classe não nula no primeiro domínio orientado e é exato no segundo. Para a completação, uma sequência exata abaixo localiza os dados faltantes nos sistemas de cohomologia das truncagens e seus mapas, em vez de deixar “mudança de base” como expressão sem contrato.

A [nota de módulos076](<C:/IALD/Central de Patentes/Chatgpt/MODULOS_BRST_EBAR_076_20260910/MODULOS_H3_H4_E_SETOR_CALCULADO.md>) é entrada desta investigação. Seus resultados novos de superconexão, se produzidos posteriormente, não são presumidos aqui.

## 1. Quatro operações que precisam ser separadas

Escreva A para o complexo mínimo dos campos COMPLETOS, sem B0, e s para o BRST clássico. Após desfazer o gauge e retirar pares não mínimos, s é independente de B0 em coordenadas dos campos completos. Distinguimos:

1. acrescentar um anel C de coeficientes inertes: C⊗_R A, com somas finitas;
2. passar ao subcomplexo natural pela normalização dos jatos de B0 e invariância Lorentz;
3. permitir dependência C∞ CONJUNTA, sem hipótese de soma finita separável nos valores;
4. completar em torno da diagonal g=g0, φ=φ0, com a valência/escala da Q2.

O teorema da seção2 paga as duas primeiras operações num domínio declarado. As operações3/4 não são definições equivalentes das primeiras. A [nota073](<C:/IALD/Central de Patentes/Chatgpt/COHOMOLOGIA_ESPECTADOR_B0_073_20260910/PRIMITIVA_ORDINARIA_COM_B0_E_LIMITE_ADMISSIVEL.md>) já conserva C∞ conjunto e recusa substituir esse espaço por um tensor produto algébrico. A [normalização074](<C:/IALD/Central de Patentes/Chatgpt/NATURALIDADE_E_CURVATURA_B0_074_20260910/NORMALIZACAO_S_E_OBSTRUCAO_EULER.md>) transporta primitivas que JÁ existam na mesma completação; ela não produz por si essa comparação.

Também distinguimos dois sentidos de M_g^K:

- classes globais sem B0, representadas por ciclos de K, antes do transporte;
- classes representadas por K JÁ no H(s) com B0 e na completação final, portanto com todas as novas relações divididas.

Uma classe eliminada no transporte fornece núcleo no primeiro sentido. No segundo, ela já é zero em M_g^K; reapresentá-la como contraexemplo à injetividade de μ seria circular.

## 2. Teorema de mudança de base antes da completação

### 2.1 Domínio

Trabalhe no ponto de avaliação, em coordenadas normais de g0 e com frame de referência orientado e temporalmente orientado. Seja G=SO⁺(1,3), o grupo de mudanças LINEARES entre esses frames. Este G não é um gauge local de vielbein e não usa um ghost Lorentz convencional.

Seja C o espaço/anel dos jatos normais de B0, incluindo seus índices de formas horizontais quando necessário. C pode ser substituído por C/J, onde J é um ideal G-estável apenas dos coeficientes de B0. Para H(s), não se exige que J seja diferencial horizontal; essa hipótese adicional é necessária quando também se trabalha com d_H. As EOM universais prolongadas de B0 dão um exemplo compatível.

Seja A o complexo de jatos dinâmicos coordenados, de forma horizontal zero, com:

- polinômios finitos nos jatos diferenciados, ghosts e antifields;
- coeficientes C∞ nos valores escalares do alvo;
- dependência tensorial finita/racional nos valores métricos, seus inversos e volumes, regular na assinatura admitida;
- ausência de parâmetros externos dinâmicos ou de inversos de dφ0.

A dependência ativa nos valores métricos é restringida aqui para que cada expressão pertença a uma soma finita de tipos G. Não se declara uma função C∞ arbitrária desses valores localmente finita. Em C⊗A também exigimos soma finita de produtos separados nos coeficientes de B0 e nas variáveis ativas; esse domínio é menor que C∞ conjunto.

No ponto normal, os jatos ativos são componentes de derivadas parciais em coordenadas fixas. Sob uma mudança LINEAR de frame eles são tensores/densidades de tipo finito. O BRST possui a mesma fórmula coordenada universal e não depende de C. A álgebra natural deste domínio identifica-se com
\[
 A_{\rm nat,sep}=(C\otimes A)^G.
 \tag{1}
\]
A reconstrução de (1) em coordenadas arbitrárias é a normalização finita074: os jatos da exponencial de B0 removem mudanças não lineares, e G trata a liberdade residual. Invariância Lorentz sozinha, sem essa normalização, não provaria naturalidade.

### 2.2 Tensorizar e tomar invariantes

Como R é um corpo, tensorizar um complexo de espaços vetoriais por C é exato. Explicitamente, escolha em cada grau
\[
 A^g=B^g\oplus H_{\rm rep}^g\oplus L^g,\qquad
 Z^g=B^g\oplus H_{\rm rep}^g,
\]
com s:L^g→B^{g+1} um isomorfismo. A mesma decomposição tensorizada dá
\[
 H^g(C\otimes A,s)=C\otimes H^g(A,s).
 \tag{2}
\]
A escolha de complementos prova (2); não fornece uma homotopia regular em parâmetros C∞ conjuntos ou contínua em qualquer completação. Cada entrada na classe de somas finitas, contudo, continua um elemento de jatos finitos.

Para representações tensoriais localmente finitas do grupo semissimples conectado G, a projeção no tipo trivial preserva sequências exatas. Aplicando-a a ciclos e fronteiras,
\[
 H^g((C\otimes A)^G,s)
   \simeq (C\otimes H^g(A,s))^G.
 \tag{3}
\]
Quotientar C por um submódulo G-estável não altera esse argumento. Não aparece aqui um problema Tor sobre um anel de EOM: o tensor produto de (2) é sobre R, e s não age em C.

[KNOWN] O mecanismo de separação por tipos e exatidão está em [BBH1995, Apêndice C](https://arxiv.org/pdf/hep-th/9505173v2). A equação E.7 da mesma fonte exibe uma identidade de Cartan para a ação interna. A versão coordenada difeomórfica necessária abaixo é conferida diretamente; não se identifica por nome um ghost Lorentz com ∂c.

### 2.3 A ação linear dinâmica é nula na cohomologia

Para uma matriz a∈so(1,3), tome o campo vetorial coordenado X_a=a^\mu{}_\nu x^\nu∂_\mu, centrado no ponto x=0. Defina a contração ímpar ι_a substituindo o ghost e seus jatos pelos de X_a:
\[
 \iota_a(\partial_Ic^\mu)=\partial_I X_a^\mu,\qquad
 \iota_a(\text{campos ou antifields})=0.
 \tag{4}
\]
No ponto, somente os jatos de primeira ordem do ghost recebem a^\mu{}_\nu. O operador prolongado atua também antes da avaliação em x=0.

A ação mínima é sT=L_cT+termos KT sem c, para os geradores tensoriais pertinentes. A inserção (4) dá a ação L_{X_a} sobre campos e antifields; nos ghosts,
\[
 \iota_a(sc)=\iota_a(c^\nu\partial_\nu c)
 =X_a^\nu\partial_\nu c-c^\nu\partial_\nu X_a=[X_a,c].
\]
A parte KT não contribui à contração. Prolongar por derivadas e avaliar na origem fornece a ação linear nos jatos. Portanto, com a orientação da ação G assim fixada,
\[
 L_a=s\iota_a+\iota_as.
 \tag{5}
\]
Inverter a convenção de pullback de G inverte simultaneamente L_a e a inserção; sua nulidade em cohomologia é a mesma. Por (5), a álgebra de Lie age trivialmente em H(s,A). Como os tipos são localmente finitos e G é conectado, a ação do grupo também é trivial.

Substituindo em (3), obtemos o resultado positivo:
\[
 \boxed{
 H^g(s,A_{\rm nat,sep})
 \simeq C^G\otimes H^g(s,A).
 }
 \tag{6}
\]
Isso vale em particular para g=3 e g=4, sem escolher FRW e sem inverter dφ0. Vale com relações apenas de B0 nas condições acima.

A fórmula usa o H(s,A) INTEIRO. Para trocar esse fator por M_g^K é ainda necessário demonstrar que K representa todas as classes relevantes e especificar as relações. A nota de módulos não afirma essa geração. Além disso, (6) é uma afirmação sobre H(s); se representantes fora de K forem necessários, a ação Ebar_N sobre eles precisa ser calculada. Não se importam grupos E2 de coeficientes constantes apenas de (6).

## 3. Naturalidade adicional no alvo não é eliminada por (5)

G na seção2 é o grupo Lorentz residual do frame de referência. Uma exigência adicional de O(4) do alvo deve ser aplicada a ambos os fatores da equação (6) simultaneamente. As isometrias do alvo são simetrias RÍGIDAS do sigma, não um gauge O(4) inserido no BRST deste modelo; não se pode usar (5) para tornar sua ação cohomológica trivial.

O enunciado correto permanece do tipo
\[
 (C\otimes H)^{{O(4)}},
\]
e não C^{O(4)}⊗H^{O(4)} sem demonstração adicional. O controle finito é explícito: para V=R⁴ e C=R[S³], o elemento
\[
 \sum_A y_0^A\otimes e_A
\]
é O(4)-invariante e não nulo em C⊗V, enquanto V^{O(4)}=0. Logo tomar invariantes separadamente perde contrações entre coeficientes do fundo e representações ativas.

Esse é um controle representacional, não uma classe calculada de H³ Einstein–sigma. As correntes de Killing da nota de módulos, se classificadas como classes não triviais, devem conservar sua representação do alvo antes das contrações com B0. Uma base com rótulos AB externos não é automaticamente uma lista de escalares naturais invariantes. O exemplo acima identifica a obrigação, sem presumir a classificação dessas correntes.

## 4. Perda real de classe global no grau três

### 4.1 Não trivialidade global antes do espectador formal

Considere o domínio de campos completos com valores globais em S³, admitindo a orientação do alvo ou seu setor de paridade correspondente. Seja Ω a forma volume da esfera e
\[
 \tau_3=\frac1{3!}\Omega_{ABC}(\phi)\,
          s\phi^A\,s\phi^B\,s\phi^C.
 \tag{7}
\]
Por s²φ=0 e d_targetΩ=0, sτ₃=0. Como sφ=c^\mu∂_\muφ, esse representante pertence ao setor K da nota de módulos.

**Proposição:** τ₃ não é s-exato no complexo global suave dos campos completos que seja regular na família de soluções a seguir, mesmo permitindo antifields mínimos.

Use a extensão geométrica Einstein–sigma já calculada na [nota do habitante](<C:/IALD/Central de Patentes/Chatgpt/HABITANTE_CURVO_SIGMA_20260909_202000/HABITANTE_CURVO_SIGMA_E_AREA.md>):
\[
 M=I\times S^3,\quad
 g=dr^2-a(r)^2\gamma,\quad a=2\cos(r/2),\quad
 \Lambda=3/4,\quad\kappa c_\sigma=4.
 \tag{8}
\]
Escolha qualquer intervalo I no interior de (0,π). Identifique S³ com SU(2), com métrica bi-invariante. Para b∈SU(2),
\[
 \phi_b(r,x)=b\,x
 \tag{9}
\]
é solução sigma e mantém a mesma fonte métrica. Portanto (g,φ_b) é uma família de soluções do MESMO sistema ambiente. A extensão ao S³ inteiro é geométrica; não se afirma que um único registro de cinco probabilidades positivas a cubra.

Tome uma base T_a de su(2), [T_a,T_b]=f_{ab}{}^dT_d. Os campos K_a(x)=T_a x são invariantes à direita:
\[
 [K_a,K_b]=-f_{ab}{}^dK_d.
\]
Se η=b⁻¹db=η^aT_a é a forma de Maurer–Cartan esquerda no parâmetro b, ponha
\[
 c=\eta^aK_a,\quad c^r=0,\qquad
 d_b\eta^d=-\frac12 f_{ab}{}^d\eta^a\eta^b.
 \tag{10}
\]
Então d_bc=c^\mu∂_\mu c, pois o sinal do colchete dos K coincide com (10). Além disso,
\[
 d_b\phi_b=b\eta x=d\phi_b(c),\qquad
 d_bg=0=L_cg,
\]
já que os K são Killing da parte espacial. Todos os prolongamentos em jatos respeitam essas identidades.

Avalie os antifields e seus jatos em zero. Seus BRST são zero na família porque as EOM e todos os prolongamentos se anulam; os termos com antifields também desaparecem. Assim, num ponto espaço-temporal fixo p=(r_*,x_*), a substituição (8)–(10) define um mapa de complexos
\[
 \mathcal R_p:(A,s)\longrightarrow(\Omega^\bullet(SU(2)),d_b).
 \tag{11}
\]
A avaliação da expressão em jatos num ponto não destrói a identidade: a família fornece os jatos de campos efetivos, e (10) verifica s em todos os geradores antes de prolongar.

A imagem de τ₃ é a forma volume puxada pelo difeomorfismo b↦b x_*:
\[
 \mathcal R_p(\tau_3)=(R_{x_*})^*\Omega,\qquad
 \int_{SU(2)}\mathcal R_p(\tau_3)\ne0.
 \tag{12}
\]
Se τ₃=sβ₂ para β global suave, (11) daria uma 2-forma global suave com d_bR_pβ₂=R_pτ₃, contradizendo Stokes na variedade compacta sem borda SU(2). Isso prova a não trivialidade.

A família homogênea é um TESTE da identidade global alegada, não uma restrição da categoria geral a FRW. Nenhum inverso de dφ ou coordenada relacional foi introduzido. O argumento não se aplica a uma álgebra limitada a uma carta contrátil do alvo, nem transforma τ₃ em um escalar de paridade par sob todo O(4) se esse setor exclui a orientação. Esses limites são materiais.

### 4.2 A mesma classe é eliminada no domínio formal da diagonal

Acrescente agora φ0 inerte e use φ=Exp_{φ0}(tξ). A seção6 da nota de módulos constrói
\[
 F_u=\operatorname{Exp}_{\phi_0}(ut\xi),\qquad
 K_2=\int_0^1\frac12\Omega(F_u)
        (\partial_uF_u,sF_u,sF_u)\,du,
\qquad sK_2=\tau_3.
 \tag{13}
\]
O termo inicial em u=0 é zero porque sφ0=0. A integral é coeficiente a coeficiente em u e não usa uma trajetória no espaço-tempo. A fonte confere que cada coeficiente tem jatos finitos, naturalidade conjunta e a contagem Rees correspondente.

Com (12), (13) agora dá uma perda NÃO apenas possível de classe:
\[
 [\tau_3]_{\rm global}\ne0,\qquad
 [\tau_3]_{\rm diagonal\ formal}=0.
 \tag{14}
\]
Não há contradição: Log/Exp relativo não fornece um caminho global único para todos os pares (φ0,φ). A órbita inteira usada em (12) não pertence a uma única vizinhança formal da diagonal de um φ0 fixo.

Se M_3^K no domínio de μ significar o módulo global ANTERIOR, então 1⊗[τ₃] é não zero e (14) é núcleo da comparação ao domínio final. Se M_3^K já significa classes DEPOIS do quociente final, [τ₃] já é zero e (14) é somente uma relação que precisa estar incorporada à definição. Esta distinção impede usar o controle no sentido errado.

Não construí aqui um núcleo análogo em ghost4 nem uma falha efetiva de μ restrito à paridade par O(4). A proposição é a obstrução concreta em grau3 no domínio global orientado que a nota distingue.

## 5. O tensor produto algébrico também não é a completação

Mesmo em ghost zero e sem diferencial, C∞(b)[[z]] não coincide com C∞(b)⊗_R R[[z]]. A série
\[
 F(b,z)=e^{bz}=\sum_{n\ge0}\frac{b^n z^n}{n!}
 \tag{15}
\]
tem coeficiente finito em cada ordem. Se fosse uma soma finita Σ_{i=1}^m f_i(b)G_i(z), todos os coeficientes b^n/n! pertenceriam ao espaço finito gerado pelos f_i. Isso é impossível quando b varia num intervalo: os polinômios b^n são linearmente independentes.

O exemplo prova uma diferença entre classes de COCADEIAS; não prova uma classe nova de H³/H⁴. Ele basta para impedir identificar os dois espaços antes do cálculo cohomológico. Pode ser lido num setor de valores escalares ou num escalar de fundo variável; não exige inversos de gradientes. Se uma condição física restringir esses escalares, é essa classe restrita que deve ser descrita. Também não se afirma que (15) satisfaça uma cota particular de engenharia de um contratermo: tal cota é uma restrição adicional.

A notação ⊗ em μ precisa, portanto, declarar se significa soma finita ou um módulo completado por valência. Uma escolha arbitrária de complementos na prova de (2) não tem, por si, continuidade nessa completação nem regularidade paramétrica conjunta.

## 6. A completação do modelo e a sequência exata que localiza o resíduo

### 6.1 Truncagens legítimas

No sistema mínimo clássico, imponha as EOM universais apenas de B0 e tome a vizinhança formal da diagonal. Seja I o ideal gerado pelas flutuações e TODOS os ghosts/antifields normalizados, com seus jatos, contado por valência. No fundo diagonal on-shell:

- os BRST dos campos físicos têm ao menos um ghost;
- sc é quadrático em ghosts;
- a parte KT dos antifields começa com EOM ativas cuja parte constante é a EOM de B0, nula no quociente;
- os demais termos têm ao menos um gerador de I.

Logo sI⊂I, incluindo prolongamentos. Em variáveis Rees isso é a mesma afirmação de que o diferencial clássico respeita a filtração por valência mínima, podendo aumentar a valência. Ela utiliza o fundo on-shell. Em fundo arbitrário a parte KT pode possuir termo constante; não se pode construir essas mesmas truncagens ignorando-o.

Defina os complexos naturais truncados
\[
 C_N=A_{\rm nat}/F^{N+1},\qquad
 \widehat A_{\rm nat}=\varprojlim_N C_N.
 \tag{16}
\]
Cada coeficiente retido tem ordem de jatos finita, sem limite uniforme de ordem em N. Os mapas de COCADEIAS C_{N+1}→C_N são sobrejetivos. Na apresentação normal, relações de B0 têm valência zero e a projeção Lorentz é feita em cada tipo finito; ela não destrói essa sobrejetividade. Para uma apresentação com fontes θ,ω e tadpoles Laurent, é necessário usar a filtração multigraduada da Ward072; (16) não recategoriza esses termos como Rees sem fontes.

### 6.2 Prova elementar da sequência de limite

Considere a aplicação Δ sobre o produto dos complexos,
\[
 \Delta((x_N))=(x_N-r_Nx_{N+1}),\qquad
 0\longrightarrow\varprojlim C_N
 \longrightarrow\prod C_N
 \xrightarrow{\Delta}\prod C_N
 \longrightarrow0.
 \tag{17}
\]
A sobrejetividade de Δ nas cocadeias segue por escolha recursiva de x_{N+1}, usando a sobrejetividade de r_N. Produtos de espaços vetoriais são exatos; portanto H^g(∏C_N)=∏H^g(C_N). A sequência longa de (17) dá
\[
 \boxed{
 0\longrightarrow
 \operatorname{coker}\!\left[
   \Delta:\prod H^{g-1}(C_N)\to\prod H^{g-1}(C_N)\right]
 \longrightarrow H^g(\widehat A_{\rm nat})
 \longrightarrow
 \ker\!\left[
   \Delta:\prod H^g(C_N)\to\prod H^g(C_N)\right]
 \longrightarrow0.
 }
 \tag{18}
\]
O primeiro termo é a usual lim¹ H^{g−1}(C_N); o último é lim H^g(C_N). A prova foi dada, sem supor que a sobrejetividade nas cocadeias implique sobrejetividade na cohomologia.

Assim, para g=3 são necessários os sistemas H²(C_N), H³(C_N) e seus mapas; para g=4, H³(C_N), H⁴(C_N). Se as transições cohomológicas em grau g−1 forem sobrejetivas, a mesma recorrência elimina o cokernel. Essa condição é suficiente, não é uma propriedade que já tenhamos medido no Einstein–sigma.

Mesmo quando lim¹ desaparece, é necessário comparar o módulo de representantes proposto com lim H^g(C_N). A perda de classe global em (14) mostra que essa comparação pode ter núcleo ao partir do módulo global errado. Cotas de derivadas/regularidade de uma homotopia explícita seriam uma forma de pagar a comparação; a normalização074 paga somente seu retorno à naturalidade depois de ela existir.

## 7. Consequência prática para μ e os canais E2

A pergunta μ iso tem uma resposta positiva no domínio finito/separado, substituindo M_g^K pelo H(s,A) completo e usando apenas a invariância Lorentz da seção2. Relações de B0 on-shell não são, por si, um impedimento algébrico ali.

Para a μ da nota076 na categoria Q2, o resíduo preciso é:

1. escolher M_g^K antes/depois da completação e dividir relações como (14) no sentido correspondente;
2. identificar H³/H⁴ das truncagens da MESMA classe, provar geração por K ou acrescentar representantes que faltam, com as relações;
3. controlar os mapas entre truncagens e a comparação (18), em vez de trocar automaticamente lim H por H da álgebra global;
4. se houver invariância O(4), manter os módulos alvo e as contrações conjuntas antes de tomar invariantes;
5. conservar a classe real de coeficientes C∞/analítica, valência, fontes e ordem finita em cada coeficiente;
6. calcular Ebar_N sobre os representantes efetivamente necessários. E_N=0 em K não se estende a representantes adicionais por definição.

Esses itens são independentes do fato já pago075 de que a descida tolera um ideal diferencial apenas de B0. O cálculo de H(s) e dos canais com coeficientes deve usar justamente esse ideal/categoria, sem promover identidade relativa a identidade em todos os jatos de fundo.

[DERIVED] A seção2 é uma mudança de base real em um domínio explícito. A seção4 demonstra uma classe global não trivial e sua eliminação formal no domínio indicado. A seção6 dá a comparação exata necessária para a completação. [OPEN] Não se concluiu que μ seja isomorfismo em g=3/4 para a classe natural Rees causal completa, que os canais E2 se anulem, que a anomalia seja removida, que exista carga interagente ou que haja fechamento UV.

As fontes locais foram medidas antes e depois. O manifesto registra bytes e hashes, sem atribuir ao documento uma compilação ou aprovação externa.

