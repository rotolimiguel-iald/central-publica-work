# Polarização Hadamard adaptada ao complexo BRST Einstein–sigma

10/09/2026, arco 073. [DERIVED — demonstração escrita] [KNOWN — cálculo pseudodiferencial e construção de parametrizes explicitados]. A construção é no fundo ambiente das entregas 067–068. Não é uma nova formalização Lean, cálculo CAS, execução de um.py ou afirmação da QME.

## 1. Resultado efetivo e escopo

No sistema Einstein–sigma de 068, em M=(0,pi)×S3, a=2cos(r/2), phi=id, c_m>0, kappa c_m=4 e Lambda=3/4, construímos uma escolha de polarização pura de Cauchy que:

1. é Hadamard e compatível com a conjugação real;
2. entrelaça exatamente os mapas de gauge e vínculos;
3. induz exatamente a polarização física 067;
4. tem no complexo de uma partícula somente a cohomologia física desejada, sem novas classes produzidas pelo radical da pseudocovariância;
5. fornece espaços de Krein regulares com majorantes pseudodiferenciais que preservam dados suaves.

Não se promove uma pseudocovariância arbitrária de 068 a essas propriedades. Escolhe-se uma nova extensão, por um split microlocalmente adaptado, e demonstra-se que sua diferença em relação a um par Hadamard inicial é suave. O estado físico não muda. A construção de operadores de Wick no domínio de Fock e a carga interagente são composições posteriores, não postulados escondidos neste teorema.

Fixe r0 estritamente no interior e uma faixa temporal compacta em torno de r0. Tudo é global em Sigma=S3, mas não há estimativa uniforme ao aproximar r=0 ou a=0. Não se exige Hamiltoniano global positivo para os ghosts.

Entradas locais:
- [Extensão 068](<C:/IALD/Central de Patentes/Chatgpt/EXTENSAO_BRST_COMPLETA_20260909_220941_811364/EXTENSAO_BRST_E_CORRECOES_SUAVES.md>), §§1–6: operadores reais D,Q, identidades de Green, extrator EK=1, split de Cauchy e redução física.
- [Estado 067](<C:/IALD/Central de Patentes/Chatgpt/HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912/ESTADO_FISICO_HADAMARD_E_CONTRATOS.md>), §§3–6: completude SVT, normalização simplética, modos exatos e Hadamard no sistema reduzido.
- [Jacobi 066](<C:/IALD/Central de Patentes/Chatgpt/QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md>): D=H+ell C* C, Q=CK, ell=1/(2 kappa)>0. Q não é substituído por K* K.

A literatura pertinente é [Gérard–Murro–Wrochna, §5.2, Proposições 5.2–5.4 e Observação 5.5](https://link.springer.com/article/10.1007/s00023-025-01539-1): o método fornece projetores Hadamard no fibrado hermitiano não degenerado, sem positividade em todo o fibrado. Usamos esse resultado analítico e verificamos abaixo a adaptação real, o entrelaçamento e o bloco físico; não importamos um resultado de vácuo Einstein para o acoplamento sigma.

[Wrochna–Zahn, §§2.5 e 3.2–3.3](https://arxiv.org/html/1407.8079v2) fixa o contrato de complexo e de covariâncias. Positividade no quociente clássico e uma representação de Fock/Krein com cohomologia da carga são passos diferentes. A presente construção acrescenta uma polarização projetora que comuta com o complexo.

## 2. Dados de Cauchy e ideal de operadores suaves

Sejam E e F os dados suaves complexificados de D e Q em Sigma, respectivamente, e Z os dados canônicos reduzidos S/V/TT. As formas reais simpléticas são Omega_E, Omega_F, Omega_Z, prolongadas de modo complexo bilinear. A forma hermitiana é H_E(u,v)=i Omega_E(jmath u,v), e analogamente nos outros espaços, com jmath a conjugação real e a orientação comum fixada para a covariância física. Uma troca conjunta do sinal de i não muda as identidades de adjuntos ou de projetores.

Dagger denota SEMPRE o adjunto sesquilinear relativo a H, incluindo os fatores cinéticos verdadeiros. Para mapas reais ele coincide com a extensão do adjunto simplético real empregado em 068. Para os projetores complexos, o adjunto sesquilinear fixa cada ramo; a transposição bilinear relativa a Omega troca os ramos. Não se misturam essas duas operações. As formas de Cauchy são matrizes locais invertíveis; logo os adjuntos de operadores espaciais diferenciais ou pseudodiferenciais de ordem finita continuam dessa classe.

Denote por J a classe de operadores com kernel C-infinito sobre Sigma×Sigma, inclusive entre os diferentes fibrados e espaços de dados. Em Sigma compacta, J é um ideal bilateral para operadores pseudodiferenciais de ordem finita. Uma alteração em J propaga para uma bisolução suave em qualquer faixa compacta interior. Escrevemos A~B quando A-B pertence a J.

Os mapas reais da fonte 068 são
\[
 k:E_Q\equiv F\longrightarrow E,\qquad c:E\longrightarrow F,\qquad
 e:E\longrightarrow F,
\]
com
\[
 ck=0,\qquad ek=1,\qquad k^\dagger=\ell c.
\tag{2.1}
\]
Eles são de ordem espacial finita. Em particular, e extrai os dois jets de E U_D e depois os interpreta como dados Q; não afirma Q(E U_D)=0.

A identidade EK=1 usa phi=id e Hubble distinto de zero. Por isso inclui todos os modos de gauge, mesmo os modos espaciais baixos. S3 compacta elimina diferenças entre suporte compacto e suporte arbitrário na superfície, mas a exatidão aqui decorre dos mapas (2.1), não da topologia por si.

## 3. Projetores iniciais puros e compatíveis com a realidade

Escolha projetores Hadamard iniciais Pi_D^± e Pi_Q^± de GMW:
\[
 \Pi^++\Pi^-=1,\qquad (\Pi^\pm)^2=\Pi^\pm,\qquad
 (\Pi^\pm)^\dagger=\Pi^\pm .
\tag{3.1}
\]
As pseudocovariâncias de dados correspondentes são
\[
 B_D^\pm(u,v)=\pm H_E(u,\Pi_D^\pm v),\qquad
 B_Q^\pm(z,w)=\pm H_F(z,\Pi_Q^\pm w).
\tag{3.2}
\]
Elas não precisam ser positivas nos setores não físicos. Não se usa uma média direta de projetores, pois isso pode destruir a idempotência.

### 3.1 Ajuste real na construção de Riccati

Aqui os operadores de onda são reais. Após transporte temporal que fixa a forma de fibra, escreva o operador normalizado como partial_t²+A(t), com A formalmente autoadjunto para uma forma real tau, independente de t. Na construção de GMW, o fator b tem símbolo principal positivo e satisfaz
\[
 i\partial_t b-b^2+A\in J.
\]
Se T designa transposição bilinear para tau, então A^T=A, e b^T satisfaz a mesma equação com o mesmo símbolo principal. A unicidade de Riccati modulo J dá b-b^T em J. Portanto substituir b por
\[
 b_s=\tfrac12(b+b^T)
\]
mantém a classe Hadamard e torna b_s^T=b_s exatamente.

A simetrização pode perturbar a invertibilidade em baixas frequências. Escolha um Laplaciano de referência real que preserve os subfibrados positivos e negativos de tau, e acrescente a b_s um operador real, tau-simétrico e suavizante de frequências limitadas. A positividade elíptica do símbolo principal e a desigualdade de Gårding permitem torná-lo estritamente acretivo para a norma Hilbert positiva auxiliar. O argumento é o mesmo controle de baixas frequências empregado na fatoração GMW: para frequências grandes o símbolo positivo já domina; um múltiplo de uma função espectral suave e compactamente suportada controla o complemento. Essa alteração não muda nenhum termo assintótico de alta frequência.

Com tau normalizada a uma involução auto-adjunta na norma auxiliar, a acretividade de b_s também implica a de b_s^star=tau b_s* tau. Logo b_s+b_s^star é invertível e elíptico. Defina
\[
 b^+=b_s,\qquad b^-=-b_s^\star.
\]
Como b_s^T=b_s, temos b^-=-\overline{b^+}. A fórmula de grafos (5.14) de GMW então produz projetores que, além de (3.1), obedecem
\[
 \jmath\Pi^+\jmath=\Pi^- ,
\tag{3.3}
\]
onde jmath é a conjugação real intrínseca dos dados. Se o segundo dado é i^{-1}partial_t u, jmath troca também seu sinal; não se usa conjugação ingênua de duas componentes nessa convenção.

Isso resolve os modos baixos por uma escolha de dados iniciais, seguida da evolução pelo operador original. Não modifica D ou Q, não retira seus modos e não exige que a evolução ghost tenha energia positiva.

### 3.2 Pureza do setor físico

Os modos 067 são f_p e sua conjugada, com Wronskiano não nulo e normalizado. Em cada harmônico real, eles formam uma base complexa das soluções reais complexificadas. A aplicação que conserva o coeficiente de f_p e anula o da conjugada é um projetor Pi_Z^+; Pi_Z^-=1-Pi_Z^+.

A normalização do Wronskiano dá auto-adjunção para H_Z e a conjugação troca os dois projetores. A positividade do coeficiente cinético reduzido dá H_Z positivo em Ran Pi_Z^+. A soma sobre os harmônicos é justamente a covariância 067; não se acrescenta população térmica. As fórmulas de Darboux e os fatores elípticos de ordem finita dessa fonte tornam Pi_Z pseudodiferencial em dados de Cauchy e preservam dados suaves. Assim o estado reduzido usado aqui é puro no sentido dessa decomposição de soluções.

## 4. O defeito de entrelaçamento é suave

A prova Ward suave da fonte 068, §4, aplica-se ao par inicial (3.2). A diferença dos defeitos de sinais opostos é zero pelas identidades de Green; suas frentes de onda têm orientações opostas. Logo o defeito é suave.

Em dados, para o sinal mais:
\[
 d(z,u)=B_D^+(kz,u)-\ell B_Q^+(z,cu)
       =\ell H_F(z,(c\Pi_D^+-\Pi_Q^+c)u).
\]
A forma de Cauchy H_F tem matriz local invertível. Portanto
\[
 c\Pi_D^\pm-\Pi_Q^\pm c\in J,\qquad
 \Pi_D^\pm k-k\Pi_Q^\pm\in J.
\tag{4.1}
\]
A segunda identidade é a adjunta da primeira e usa k^dagger=ell c. Não se deduz entrelaçamento exato de apenas uma concordância de símbolos principais; o resto em (4.1) é suave em todas as ordens.

## 5. Microlocalizar a inversa esquerda sem perder sua exatidão

Defina
\[
 e_d=\Pi_Q^+e\Pi_D^++\Pi_Q^-e\Pi_D^- .
\]
Temos e_d Pi_D^±=Pi_Q^± e_d exatamente. De (4.1) e ek=1,
\[
 e_dk\sim\Pi_Q^+ek\Pi_Q^++\Pi_Q^-ek\Pi_Q^-=1.
\]
Ajuste agora por uma correção explicitamente suave:
\[
 \boxed{e_1=e_d+(1-e_dk)e.}
\tag{5.1}
\]
Então e_1 k=1 exatamente e e_1-e_d pertence a J. Não há inversão de 1+um compacto, escolha de contorno Krein ou exclusão de um núcleo finito.

Como a conjugação troca simultaneamente os dois sinais e e é real, e_d e e_1 são reais. Eles têm ordem espacial finita e
\[
 e_1\Pi_D^\pm-\Pi_Q^\pm e_1\in J.
\tag{5.2}
\]

Aplique a construção de Darboux de 068 a e_1:
\[
 q=e_1-\tfrac12 e_1e_1^\dagger k^\dagger,\qquad
 r=\ell q^\dagger,\qquad
 p=1-kq-rc .
\tag{5.3}
\]
De e_1k=1 e k^dagger k=0, cálculo direto dá
\[
 qk=1,\quad qq^\dagger=0,\quad cr=1,\quad qr=0,\quad
 p^2=p=p^\dagger,\quad cp=qp=pk=pr=0 .
\tag{5.4}
\]
Por exemplo, qq^dagger tem os quatro termos
e_1e_1^dagger - (1/2)e_1e_1^dagger - (1/2)e_1e_1^dagger + 0.
Todo dado possui a decomposição única
\[
 u=pu+k(qu)+r(cu).
\tag{5.5}
\]
As imagens de k e r são isotrópicas; seu pareamento cruzado é ell Omega_F. A imagem de p é seu complemento simplético.

Aplicar adjuntos a (5.2) e usar (4.1) mostra
\[
 q\Pi_D^\pm\sim\Pi_Q^\pm q,\qquad
 \Pi_D^\pm r\sim r\Pi_Q^\pm,\qquad
 [p,\Pi_D^\pm]\in J.
\tag{5.6}
\]
Todos os produtos com J permanecem suaves porque os outros fatores têm ordem finita. Esse é o ponto que faltaria numa escolha arbitrária de split de Cauchy.

## 6. Extrator físico e sua inversa explícita

Seja s= rho_Z S U_D o extrator de dados reduzidos da fonte 068, §6. Defina s0=s p:E→Z. O campo U_D p u satisfaz C U_D p u=0 em todo o intervalo: C U_D p u é solução de Q cujos dois dados são zero. Portanto também H U_D p u=0.

A redução completa 067 fornece uma bijeção simplética pE→Z. Explicitamente:
\[
 s_0\text{ é sobrejetivo},\qquad
 \Omega_Z(s_0u,s_0v)=\Omega_E(pu,pv).
\tag{6.1}
\]
A sobrejetividade é a da reconstrução de soluções físicas modulo gauge, usando (5.5) para escolher o representante p. Não é acrescentada como uma nova hipótese de completude.

A inversa pode ser escrita sem escolher um inverso abstrato:
\[
 \boxed{R=s_0^\dagger.}
\tag{6.2}
\]
De (6.1), s0^dagger s0=p. Como s0 p=s0 e s0 é sobrejetivo, seguem
\[
 R s_0=p,\qquad s_0R=1,\qquad pR=R,\qquad R^\dagger=s_0 .
\tag{6.3}
\]
Os operadores S, os dois traces de Cauchy, p e as formas simpléticas são locais no tempo e pseudodiferenciais espaciais de ordem finita. Seus adjuntos também o são. Assim R e s0 são globais sobre S3 e preservam C-infinito, além das respectivas escalas de Sobolev com deslocamentos de ordem finitos.

## 7. Comparação do bloco físico: somente uma diferença suave é transportada

Ponha
\[
 A_Z^\pm=s_0\Pi_D^\pm R .
\tag{7.1}
\]
Esses operadores somam a identidade e são auto-adjuntos para H_Z, ainda que não se suponha sua idempotência exata. Suas formas B_Z,0^±=±H_Z(.,A_Z^±.) têm a CCR reduzida correta.

A propriedade Hadamard precisa de um argumento adicional, e não da palavra “projetor”. Por (5.6),
\[
 U_D p\Pi_D^\pm=U_D\Pi_D^\pm p+\text{operador com kernel suave}.
\tag{7.2}
\]
Assim o corte físico por p conserva os ramos de frequência modulo suaves. Os campos resultantes são soluções físicas exatas, e S os leva às equações reduzidas. A composição espacial com S conserva a orientação pelo argumento microlocal 067/068: em uma covariável característica não nula, a parte espacial é não nula; os operadores espaciais de ordem finita preservam a relação de meia onda pertinente. Não se afirma preservação desse tipo para um operador arbitrário propagado de Cauchy.

Portanto as formas (7.1), evoluídas pelo sistema reduzido, são bisoluções Hadamard com a mesma CCR que 067. Subtrair os pares de sinais opostos dá a mesma distribuição, mas as duas orientações são disjuntas. Logo a diferença é uma bisolução suave. Em dados:
\[
 \boxed{\Pi_Z^\pm-A_Z^\pm\in J.}
\tag{7.3}
\]
A passagem de covariância a projetor em (7.3) usa apenas a matriz simplética local invertível dos dados reduzidos. Não exige inverter uma covariância degenerada.

Consequentemente,
\[
 R\Pi_Z^\pm s_0-p\Pi_D^\pm p
 =R(\Pi_Z^\pm-A_Z^\pm)s_0\in J.
\tag{7.4}
\]
Apenas essa diferença suave é transportada. Não se substitui um bloco singular por congruência arbitrária e depois se presume Hadamard.

## 8. Projetor exato adaptado

Defina finalmente
\[
 \boxed{
 \widehat\Pi_D^\pm=
 k\Pi_Q^\pm q+r\Pi_Q^\pm c+R\Pi_Z^\pm s_0 .
 }
\tag{8.1}
\]
Na decomposição (5.5), são exatamente os três projetores por blocos. As identidades (5.4)/(6.3) provam
\[
 (\widehat\Pi_D^\pm)^2=\widehat\Pi_D^\pm,\quad
 \widehat\Pi_D^+\widehat\Pi_D^-=0,\quad
 \widehat\Pi_D^++\widehat\Pi_D^-=1 .
\tag{8.2}
\]
O adjunto troca os dois primeiros termos:
\[
 (k\Pi_Q^\pm q)^\dagger
 =q^\dagger\Pi_Q^\pm k^\dagger
 =r\Pi_Q^\pm c .
\]
O terceiro é auto-adjunto. Portanto (widehat Pi)^dagger=widehat Pi. Todos os mapas de split são reais e os três pares de polarização obedecem (3.3); logo a conjugação também troca os sinais de widehat Pi.

O entrelaçamento agora é exato:
\[
 \widehat\Pi_D^\pm k=k\Pi_Q^\pm,\quad
 c\widehat\Pi_D^\pm=\Pi_Q^\pm c,\quad
 q\widehat\Pi_D^\pm=\Pi_Q^\pm q,\quad
 s_0\widehat\Pi_D^\pm=\Pi_Z^\pm s_0 .
\tag{8.3}
\]
Não é apenas uma Ward sobre testes físicos.

### 8.1 Hadamard do projetor final

Escreva 1=p+kq+rc. Aplicar Pi_D à decomposição e usar (5.6) dá
\[
 \Pi_D^\pm\sim p\Pi_D^\pm p+k\Pi_Q^\pm q+r\Pi_Q^\pm c .
\]
Pela equação (7.4),
\[
 \boxed{\widehat\Pi_D^\pm-\Pi_D^\pm\in J.}
\tag{8.4}
\]
Logo o par final é Hadamard. A covariância física é exatamente a de 067 por (8.3) e pela isometria simplética de s0. A diferença entre o par final e o par construído em 068 também é suave: ambos têm a mesma CCR e orientações Hadamard. Não se exige identidade dos blocos não físicos anteriores.

O mesmo resultado pode ser visto diretamente na forma de dados:
\[
 \widehat B_D^+(u,v)=
 B_{067}^+(s_0u,s_0v)
 +\ell B_Q^+(qu,cv)+\ell B_Q^+(cu,qv).
\tag{8.5}
\]
A soma cruzada é hermitiana. A diferença de sinais reproduz exatamente a decomposição de Omega_E, não um propagador normalizado com a forma de fibra descartada.

## 9. Complexo de uma partícula e radical

Nas soluções completas de L, b=ell Cu; os dois espaços ghost são cópias de F. Após uma rescalagem constante do antighost, o complexo de Cauchy tem a forma
\[
 F_{-1}\ \xrightarrow{k}\ E_0\ \xrightarrow{c}\ F_{+1},
\tag{9.1}
\]
ou a graduação invertida se se usa a convenção de codiferencial de Wrochna–Zahn. Essa troca não muda as identidades de exatidão.

A soma diagonal do projetor final em E e dos projetores Pi_Q nos ghosts comuta exatamente com (9.1). Portanto seu subcomplexo de frequência escolhida é
\[
 F^+ \xrightarrow{k}
 RZ^+\oplus kF^+\oplus rF^+
 \xrightarrow{c}F^+ .
\tag{9.2}
\]
O mapa c envia rF+ isomorficamente a F+ e anula os outros blocos; k injeta F+ exatamente no bloco gauge. Sua cohomologia é Z+ em grau zero e zero nos graus restantes.

Na forma hermitiana de uma partícula, o par gauge/vínculo é cruzado e não degenerado, porque H_F é não degenerada em Ran Pi_Q^+. Os ghosts têm a mesma forma cruzada, com os sinais graduados do dicionário. A parte física é positiva. Assim não há radical adicional na imagem da polarização; o radical da pseudocovariância completa corresponde ao ramo complementar. Este é um subcomplexo direto, e quocientá-lo não cria as classes espúrias que podem surgir de uma pseudocovariância não projetora.

Este argumento é específico da escolha (8.1). Ele não prova que toda correção suave permitida de 068 preserve P0. Também não confunde cohomologia clássica de Cauchy com a cohomologia de Fock: esta última deve ser construída no domínio pelo certificado de quartetos.

## 10. Majorante Hilbert e regularidade do espaço ghost

Para Q, use o espaço de energia
\[
 {\cal E}_Q=H^{1/2}(\Sigma;W)\oplus H^{-1/2}(\Sigma;W)
\]
na convenção canônica valor/momento; as mudanças de densidade/forma de fibra de 068 são mantidas. Sua forma H_F é contínua e fortemente não degenerada: sua matriz é um pareamento de dualidade invertível, com fatores locais invertíveis.

As ordens matriciais dos projetores Hadamard são (0,-1;1,0), portanto Pi_Q é limitado nessa energia. Conjugar por potências de um Laplaciano positivo de referência identifica a energia com L2⊕L2; Pi torna-se Psi0. A forma tem operador representativo J0 autoadjunto, invertível e Psi0 elíptico.

### 10.1 Regularidade de Ran Pi

Pi é J0-auto-adjunto. Logo a decomposição em Ran Pi e Ker Pi é topológica e ortogonal para a forma indefinida. Isso implica que a forma restrita a Ran Pi é fortemente não degenerada: um funcional contínuo nessa imagem pode ser estendido por composição com Pi; aplicar o inverso da forma total e projetar fornece sua inversa restrita.

Uma projeção ortogonal Hilbert para o mesmo subespaço é explícita:
\[
 A=\Pi+\Pi^*-1,\qquad
 P=\Pi A^{-1}.
\tag{10.1}
\]
De A²=1-(Pi-Pi*)²>=1, segue invertibilidade. Como o símbolo principal de Pi na energia reescalada é o projetor ortogonal usual de meia onda, A é elíptico de ordem zero, e seu inverso é Psi0. A identidade A Pi*=Pi A mostra P*=P; a verificação na imagem e no kernel ortogonal dá P²=P e Ran P=Ran Pi.

Considere no Hilbert completo
\[
 G=P J_0 P+(1-P).
\tag{10.2}
\]
Ele é autoadjunto e invertível: no primeiro bloco representa a forma forte restrita; no segundo é a identidade. Seu símbolo principal é invertível, pois J0 e o símbolo de P comutam no limite principal, e J0 é não degenerado em cada ramo. Logo G é elíptico Psi0.

A separação espectral de G de zero agora é uma consequência da invertibilidade em um Hilbert positivo. Pode-se usar cálculo funcional elíptico:
\[
 J=\operatorname{sign}(G),\qquad |G|,\qquad |G|^{\pm1/2}\in\Psi^0 .
\tag{10.3}
\]
Para justificar a regularidade, escolha contornos que separem os espectros reais positivo/negativo de G e de seu símbolo principal. Nos contornos, z-G é elíptico e invertível; seu inverso preserva toda a escala Sobolev por regularidade elíptica. Integrar a resolvente dá as funções em (10.3). Esse é o cálculo funcional elíptico usual, não uma escolha de contorno do operador de pseudocovariância em um espaço de Krein sem controle de espectro.

Restrito a Ran P, J é uma simetria fundamental e
\[
 (u,v)_{\rm maj}=\langle u,|G|v\rangle
\]
é uma majorante Hilbert equivalente. Ela, J e suas potências preservam C-infinito. Nenhuma positividade foi imposta à forma ghost original.

### 10.2 Topologia adaptada ao split

Não se presume que k,c ou os extratores de ordem positiva sejam limitados no mesmo Sobolev padrão dos dados D. Use o isomorfismo
\[
 T:Z\oplus F\oplus F\longrightarrow E,\qquad
 T(z,f_1,f_2)=Rz+kf_1+rf_2,\qquad
 T^{-1}u=(s_0u,qu,cu).
\tag{10.4}
\]
Ele e sua inversa preservam C-infinito e têm perdas Sobolev finitas. Puxar a soma das majorantes dos três espaços fornece uma topologia Hilbert adaptada; no núcleo de dados suaves ela tem exatamente o split algébrico utilizado. Os diferenciais de (9.2) são então mapas de blocos explícitos. Não se afirma equivalência dessa norma a um único Sobolev D escolhido previamente.

Para a composição Fock, isso disponibiliza o espaço físico de uma partícula 067 e os pares auxiliares com forma cruzada regular, junto a operações que preservam dados suaves. A invariância de um domínio de partículas finitas suaves sob os operadores de Wick locais requer a prova por núcleos/microlocalidade correspondente. Não se conclui a existência de operadores para uma soma arbitrária de funcionais microcausais não polinomiais apenas por essa topologia.

## 11. Alcance da entrega

[DERIVED] Obtivemos projetores puros e reais, Hadamard e exatamente adaptados ao complexo, preservando o estado físico 067. O argumento trata a mudança de polarização, os modos baixos e o radical, e fornece majorantes compatíveis com dados suaves. Não usa Riesz de uma pseudocovariância Krein arbitrária ou uma promoção automática de 068.

[INPUT já explicitado] A aplicação consome as provas escritas de completude SVT, Green e extrator do fundo 067/068, e o teorema analítico de projetores Hadamard de GMW. Não estende esses contratos a outro fundo Einstein–matéria sem verificar seu próprio split e sua física.

[OPEN nesta nota] A representação de todos os coeficientes Wick/interagentes no domínio comum, a implementação da carga renormalizada e a QME são composições distintas. Nenhum resultado de ausência geral de anomalias, acordo perturbativo completo, estado não perturbativo, independência de cutoff/fundo, seleção física ou completude UV foi acrescentado.

Todos os artefatos novos desta entrega ficam na pasta Chatgpt. As fontes canônicas e congeladas permanecem somente leitura. Os pins serão medidos no manifesto; nenhuma hash de PDF consultado é inventada.
