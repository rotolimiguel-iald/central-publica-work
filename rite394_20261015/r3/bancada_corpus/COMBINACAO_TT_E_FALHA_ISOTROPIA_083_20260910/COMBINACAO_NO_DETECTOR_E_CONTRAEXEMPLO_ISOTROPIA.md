# A combinação passa no detector TT e falha numa componente de isotropia

10/09/2026. Adendo083 NOVO, sem alterar083/J1 ou a entrega082. [DERIVED — demonstração escrita, aguardando revisão independente específica]. Zero novos cálculos CAS/algébricos executados ou Lean; somente escrita documental com pins lidos. Nenhum original ou um.py alterado, executado ou importado.

**Resultado.** No fundo K=1/z0² FIXADO, a cocadeia
\[
\boxed{
Q=-\frac{J\beta_o}{12K}-\frac{q_{\rm grad}}{28K}
}
\tag{1}
\]
reproduz \(+4k/z_0\) para TODO k no detector ímpar TT usado079–083. Entretanto,
\[
\boxed{d_{\rm CE}Q\ne-a,\qquad a=J\nu(p)}
\tag{2}
\]
no complexo completo: uma avaliação por outros quatro Killing locais, na MESMA solução TT, isola uma componente de \(p^2M^2\) do defeito. Ela dá
\[
\boxed{
\operatorname{ev}_{\rm iso}(d_{\rm CE}Q+a)
=\frac{2k}{3Kz_0}\theta^{0123};
\quad k=2/z_0:\quad
\frac43\theta^{0123}\ne0.
}
\tag{3}
\]
Isso exclui essa combinação específica como cancelamento universal, inclusive modulo fronteiras s0. Não decide a existência de outra combinação.

## 1. Domínio e fontes que entram

Use exatamente a [identificação CE082](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>): apresentação métrica mínima, g0 espaço-forma Lorentziana orientada de assinatura(+---), K>0 real fixado, φ0 constante e coeficientes escalares herdados conservados. A referência TT é
\[
g_0=(\ell/z)^2\eta,\quad
(\tau,x,y,z),\quad \eta=\operatorname{diag}(1,-1,-1,-1),
\quad z_0=\ell,\quad K=\ell^{-2}.
\tag{4}
\]
z é espacial. Os parâmetros herdados e a referência são os mesmos ao variar k. O [contrato do anel079](<C:/IALD/Central de Patentes/Chatgpt/LIBERDADE_DE_LEVANTAMENTO_079_20260910/ADENDO_IDEAL_FECHADO_E_COEFICIENTES_HERDADOS_079.md>) não é reduzido.

Aqui \(\nu(p)=\varepsilon_{abcd}p^ap^bp^cp^d/4!\), \(p=C\), e \(J=\operatorname{tr}(W_{[1]}\wedge W_{[1]})/\operatorname{vol}_{g_0}\). O alvo a é a classe de A6, com a normalização e o volume conferidos na [nota da raiz082](<C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_CE_E_CORRENTE_HORIZONTAL_082_20260910/CLASSE_CE_DO_RESIDUO_E_CORRENTE_GRADIENTE.md>).

O símbolo M nesta nota é a matriz da identificação CE,
\[
M=\operatorname{antisym}_{g_0}(\bar\nabla C),\qquad
M^a{}_b=\bar\nabla_bC^a\quad\text{em Killing}.
\tag{5}
\]
Não é o m covariante elevado da nota finita082: \(m_{ab}=\bar\nabla_{[a}C_{b]}\) satisfaz \(m_{ab}=-M_{ab}\) nessa identificação. Assim
\[
\beta_o=\tfrac12\varepsilon_{abcd}p^ap^b m^{cd}
=-\tfrac12\varepsilon_{abcd}p^ap^b M^{cd}.
\tag{6}
\]
Todos os ghosts têm paridade ímpar. Os índices de M² abaixo são levantados com g0, que é s-inerte.

A corrente horizontal é a já construída pela raiz:
\[
q_{\rm grad}=
\frac1{3!}\varepsilon_{abcd}
 (\bar\nabla^aJ)p^bp^cp^d,\qquad
d_{\rm CE}q_{\rm grad}=(\bar\Box J)\nu(p).
\tag{7}
\]
Seu [parecer independente082](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_OBSTRUCAO_CE_CORRENTE_082_20260910_053437_900535/PARECER_CLASSE_CE_E_CORRENTE_GRADIENTE_082.md>) foi lido. O uso de(7) conserva a correção s0q6 da realização no BRST original; não presume que uma identidade de cohomologia seja literalmente o s1 sem essa correção.

## 2. A combinação no detector anterior é exata para todos os k

A [exclusão finita082](<C:/IALD/Central de Patentes/Chatgpt/SETOR_QUADRATICO_SEM_DERIVADAS_082_20260910_050315_8076779/IMAGEM_DO_DETECTOR_NO_SETOR_FINITO.md>) calculou
\[
L_k(s_1(J\beta_o))
=R(k)=24k^3/z_0-96k/z_0^3.
\tag{8}
\]
A [nota083 de J1](<C:/IALD/Central de Patentes/Chatgpt/CANDIDATO_DERIVADA_WEYL_083_20260910/CANDIDATO_J1_BETA_E_DETECTOR_NAO_NULO.md>) derivou, com a conexão conforme e a simetria helicoidal conservadas,
\[
(\bar\Box J)(p_0)=112k/z_0^3-56k^3/z_0.
\tag{9}
\]
Por(7), esse é o perfil de qgrad no detector original: ali \(\nu(p_0)=\theta^{0123}\). Os dois perfis são ímpares em k, portanto a metade da diferença entre k e −k conserva seus coeficientes.

Inserir K=1/z0² em(1) dá
\[
\begin{aligned}
L_k(s_1Q)
&=-\frac1{12K}(24k^3/z_0-96k/z_0^3)
  -\frac1{28K}(112k/z_0^3-56k^3/z_0)\\
&=(-2k^3z_0+8k/z_0)+(-4k/z_0+2k^3z_0)\\
&=\boxed{+4k/z_0}.
\end{aligned}
\tag{10}
\]
É uma identidade de polinômios em k com coeficientes da referência. Não é interpolação em k=2/z0 nem escolha de coeficientes dependentes da perturbação.

O perfil do alvo é \(L_k(A_6)=-4k/z_0\), logo o detector ORIGINAL anula o defeito \(A_6+s_1Q\) para toda essa família. Precisamente por isso é necessário testar outras componentes.

## 3. Derivada da cúbica com os ghosts de isotropia conservados

As fórmulas CE082 são
\[
dp=-Mp,\qquad dM=-M^2+Kpp^\flat,\qquad
dJ=p^e\bar\nabla_eJ.
\tag{11}
\]
O último termo não tem ação de M porque J é pseudoscalar orientado e sua ação de isotropia é trivial.

Ao derivar(6), deve-se usar a paridade dos fatores. Uma forma compacta de organizar a conta é introduzir a ação covariante de M em TODOS os índices. A invariância do tensor volume deixa o resultado escalar inalterado. Nessa organização,
\[
Dp=dp+Mp=0,\qquad
DM=dM+[M,M]_{\rm gr}=dM+2M^2.
\]
O fator2 não pode ser retirado: M e M têm ambos grau ímpar. Substituir(11) dá \(DM=M^2+Kpp^\flat\). Portanto
\[
\boxed{
d\beta_o=
-\tfrac12\varepsilon_{abcd}p^ap^b(M^2)^{cd}
-12K\nu(p).
}
\tag{12}
\]
No termo de curvatura, \((pp^\flat)^{cd}=p^cp^d\) e \(\varepsilon pppp=4!\nu\), o que explica−12K. A fórmula também segue expandindo \(d(p^ap^b)=dp^a p^b-p^a dp^b\) em(6), sem a notação D.

Consequentemente,
\[
d(J\beta_o)
=(p\cdot\bar\nabla J)\beta_o
-\frac J2\varepsilon_{abcd}p^ap^b(M^2)^{cd}
-12KJ\nu(p).
\tag{13}
\]
Os tipos são, respectivamente, \(p^3M\), \(p^2M^2\) e \(p^4\). A corrente qgrad e o alvo só têm a última espécie em suas derivadas. A coincidência de(10) não elimina as duas primeiras espécies universalmente.

Por exemplo, a expressão inteira do defeito é
\[
\boxed{
dQ+a=
-\frac{(p\cdot\bar\nabla J)\beta_o}{12K}
+\frac{J}{24K}\varepsilon_{abcd}p^ap^b(M^2)^{cd}
+\left(2J-\frac{\bar\Box J}{28K}\right)\nu(p).
}
\tag{14}
\]
Não se resolve sua nulidade comparando apenas a parcela horizontal após uma avaliação particular que relaciona M e p.

## 4. Outra avaliação Killing que isola p²M²

No ponto \(p_0=(0,0,0,z_0)\), temos \(g_0(p_0)=\eta\). Para a convenção matricial da álgebra Lorentz, defina J_ab por
\[
J_{ab}[a,b]=\eta_{aa},\qquad
J_{ab}[b,a]=-\eta_{bb},
\]
com as outras entradas zero. Assim J02 e J03 são os boosts de suas respectivas duplas.

Escolha quatro Killing LOCAIS com os seguintes dados no ponto:
\[
\begin{array}{c|cc}
 &v(p_0)&\bar\nabla v(p_0)\\ \hline
v_0&e_0&0\\
v_1&e_1&0\\
v_2&0&J_{02}\\
v_3&0&J_{03}.
\end{array}
\tag{15}
\]
Esses dados são realizáveis: na espaço-forma, a conexão de transporte de Killing é plana e associa unicamente a cada valor e primeira derivada antissimétrica uma solução local. Os demais jatos são os prolongamentos desses MESMOS campos. A realização também vem das matrizes \(X(A,a)=\bigl(\begin{smallmatrix}A&a\\-Ka^\flat&0\end{smallmatrix}\bigr)\) na quádrica da identificação082. Não se escolhem jatos independentes incompatíveis com a equação de Killing. O resultado local de transporte está em [Khavkine, arXiv:1805.03751v2, §3, equações22–25](https://arxiv.org/pdf/1805.03751); não se importa dessa fonte a conta do defeito que segue.

Com \(C=\theta^0v_0+\theta^1v_1+\theta^2v_2+\theta^3v_3\), a avaliação dá
\[
p=\theta^0e_0+\theta^1e_1,\qquad
M=\theta^2J_{02}+\theta^3J_{03}.
\tag{16}
\]
Os quatro θ são independentes; só os VALORES p ocupam duas direções. Portanto
\[
p^3=p^4=0,\qquad \nu(p)=0.
\tag{17}
\]
A derivada dos dois ghosts de isotropia não é zero. Multiplicar as matrizes fornece
\[
[J_{02},J_{03}]=-J_{23},\qquad
M^2=-\theta^{23}J_{23}.
\tag{18}
\]
Como J23[2,3]=−1 e J23[3,2]=+1, segue
\[
(M^2)^2{}_3=\theta^{23},\quad
(M^2)^3{}_2=-\theta^{23},\quad
(M^2)^{23}=-\theta^{23},\quad
(M^2)^{32}=+\theta^{23}.
\]
Na contração orientada,
\[
\varepsilon_{abcd}p^ap^b(M^2)^{cd}
=-4\theta^{0123}.
\tag{19}
\]
O fator4 são as duas ordens de a,b e as duas de c,d. Por(12) e(17),
\[
\boxed{\operatorname{ev}_{\rm iso}(d\beta_o)=+2\theta^{0123}.}
\tag{20}
\]

Um controle direto dos sinais evita esconder o cálculo na notação covariante. Na avaliação(16), \(dp^2=\theta^{02}\), \(dp^3=\theta^{03}\), e os outros dp de valor são zero. As parcelas de \(d(pp)\) em β dão \(+4\theta^{0123}\). A parcela de dm tem \(dm^{23}=-\theta^{23}\), dando \(-2\theta^{0123}\). A soma é exatamente+2.

Esses quatro Killing NÃO foram afirmados como uma subálgebra de dimensão quatro fechada. Aplicamos o diferencial CE completo ANTES de restringir seus dados a(16). Embora β se anule nessa restrição, sua derivada não se anula: seria incorreto aplicar um suposto diferencial zero à expressão já restrita. O transporte assegura a existência dos campos; não transforma essa restrição num morfismo CE para um alvo com diferencial zero.

## 5. A solução TT fornece um coeficiente não nulo, sem usar seus jatos superiores

Mantenha o mesmo h_k on-shell do certificado078, com
\[
f''-2f'/z+k^2f=0,\quad f(z_0)=0,\quad f'(z_0)=1.
\]
O valor do pseudoscalar é
\[
J(p_0)=-4k/z_0.
\tag{21}
\]
Agora mudamos SOMENTE os quatro Killing usados no teste, conforme(15), mantendo o fundo e essa solução. Nenhum gradiente de J precisa ser calculado para o novo teste: o primeiro termo de(13) contém três p e se anula por(17).

As identidades horizontais dão
\[
\operatorname{ev}_{\rm iso}(dq_{\rm grad})=0,\qquad
\operatorname{ev}_{\rm iso}(a)=0,
\]
enquanto
\[
\operatorname{ev}_{\rm iso}(d(J\beta_o))
=2J(p_0)\theta^{0123}.
\]
Assim
\[
\operatorname{ev}_{\rm iso}(dQ+a)
=-\frac{J(p_0)}{6K}\theta^{0123}
=\frac{2k}{3Kz_0}\theta^{0123}.
\tag{22}
\]
Escolher o mesmo k=2/z0 que separava os setores nas notas082/083 produz
\[
\frac{2(2/z_0)}{3(1/z_0^2)z_0}=\frac43.
\]
Isso prova(3). É uma conta algébrica escrita; não foi acrescentado um CAS para reexecutar os perfis existentes.

## 6. Por que a falha não desaparece numa fronteira s0

Os Killing(15) são soluções locais exatas, então R0C e todos os seus prolongamentos são zero. A família TT satisfaz H0h=0 em toda uma vizinhança, e os antifields são postos em zero APÓS aplicar o diferencial. Com a convenção KT corrigida, essa avaliação anula s0 de toda expressão de jatos finitos, inclusive as que contêm antifields.

A identificação CE082 e a realização(7) possuem correções s0 explícitas. Essas correções se anulam no presente teste pelas condições anteriores. Consequentemente(22) implica
\[
\operatorname{ev}_{\rm iso}(s_1Q+A_6)
=\frac43\theta^{0123}\ne0
\quad\text{em }k=2/z_0.
\]
Não existe um termo de valência6 F, na mesma categoria, com
\[
s_1Q+A_6=s_0F,
\]
pois sua avaliação seria zero. Trocar Q por Q+s0χ também não resolve: s1s0χ=−s0s1χ tem avaliação zero. Logo a falha é da classe representada por ESSA combinação, não apenas da escolha de um representante dentro dela.

Não se conclui que nenhuma outra classe Q possa cancelar A6. Em especial, componentes adicionais de isotropia ou derivadas podem ser necessárias para reparar(14); sua existência e as condições de fechamento seguem abertas.

## 7. O alcance de 1/K e da coincidência no detector

O K de(1) é um número real fixo estritamente positivo da referência escolhida. Portanto 1/K é uma constante real, uma unidade na extensão por Rher, e o candidato está definido nesse domínio. Ele não depende de k, não contém uma divisão por um campo dinâmico e conserva os outros coeficientes herdados.

Isso NÃO promove(1) a uma cocadeia admissível num anel universal restrito em que K é variável e só se permitem expressões polinomiais regulares em K. A fórmula é singular em K=0 nesse anel, a menos que uma extensão/localização específica seja autorizada e tipada. O teste atual é deliberadamente o de K fixo de080–083; não se transpõe silenciosamente o resultado entre essas categorias.

A dimensão de engenharia é consistente no mesmo contrato: [Jβo]=[qgrad]=2 e [K]=2, logo Q tem engenharia zero. Isso tampouco prova as demais condições Q2 de escala, inserções, contatos ou covariância de um contratermo universal.

[DERIVED] A identidade de perfis(10) passa para todo k no detector TT original; o teste de isotropia(22) a refuta como cancelamento universal e modulo s0. A diferença entre detector e igualdade de classes foi materializada por um contraexemplo finito.

[OPEN] A existência de OUTRO Q com \(d_{\rm CE}Q=-a\), a imagem CE completa, prolongamentos posteriores, admissibilidade causal, outros fundos, QME e UV.

[REAL — documental] O manifesto mede sete fontes antes/depois e os novos arquivos. Nenhuma fonte existente foi modificada; nenhuma nova execução matemática ou Lean foi feita. Revisões082 são usadas como antecedentes, sem lhes atribuir aprovação antecipada deste adendo083.
