# Uma derivada de Weyl: o candidato J1β não se anula no teste k=2/z0

10/09/2026. Investigação083 NOVA, separada da entrega082. [DERIVED — demonstração escrita, aguardando revisão independente]. [REAL — dez controles algébricos racionais executados em script Python novo]. Nenhum original, fonte congelada ou um.py alterado, executado ou importado. Zero Lean.

**Resultado delimitado.** Fixando a normalização
\[
J_1=\frac{g_0^{ef}\operatorname{tr}
  ((\bar\nabla_eW_{[1]})\wedge(\bar\nabla_fW_{[1]}))}
 {\operatorname{vol}_{g_0}},
\qquad
\beta=\tfrac12\varepsilon_{abcd}C^aC^b m^{cd},
\]
o candidato natural \(b_5^{(1)}=\kappa^2J_1\beta\) é s0-fechado e satisfaz
\[
\boxed{
L_k(s_1b_5^{(1)})
=\kappa^2\left(
\frac{48k^5}{z_0}-\frac{1608k^3}{z_0^3}
+\frac{1920k}{z_0^5}
\right).
}
\tag{1}
\]
Em particular,
\[
\boxed{
k=2/z_0:\qquad
L_k(s_1b_5^{(1)})=-7488\,\kappa^2/z_0^6\ne0.
}
\tag{2}
\]
O teste que anulava TODO o setor sem derivadas082 não anula este candidato de primeira derivada. Isso fornece um perfil novo no detector; não demonstra uma igualdade universal que cancele −[A6].

## 1. Domínio, normalização e dimensão de engenharia

Mantemos a referência do [certificado078](<C:/IALD/Central de Patentes/Chatgpt/RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md>):
\[
g_0=a^2\eta,\quad a=\ell/z,\quad
\eta=\operatorname{diag}(1,-1,-1,-1),\quad
(\tau,x,y,z),\quad z>0,
\]
\[
R^a{}_{bcd}=\partial_c\Gamma^a{}_{bd}
-\partial_d\Gamma^a{}_{bc}
+\Gamma^a{}_{uc}\Gamma^u{}_{bd}
-\Gamma^a{}_{ud}\Gamma^u{}_{bc},
\qquad \operatorname{Ric}(g_0)=3K g_0,\quad K=\ell^{-2}>0.
\tag{3}
\]
z é espacial. A orientação é dτ∧dx∧dy∧dz. O setor é Einstein puro após a projeção com φ0 constante, com os escalares herdados mantidos no sentido do [adendo079](<C:/IALD/Central de Patentes/Chatgpt/LIBERDADE_DE_LEVANTAMENTO_079_20260910/ADENDO_IDEAL_FECHADO_E_COEFICIENTES_HERDADOS_079.md>). Não é uma substituição do fundo físico φ=id. Os coeficientes dos candidatos não dependem do k da solução de teste.

W=W[1][h] é a duas-forma de Weyl linearizada com valores em End(TM), de tipo tensorial (1,3). A derivada \(\bar\nabla_eW\) atua no índice alto, no índice interno baixo e nos DOIS índices covariantes da duas-forma. Não significa somente uma derivada exterior de conexão interna, nem a derivada ordinária dos coeficientes.

Com a mesma normalização de081,
\[
\operatorname{tr}(W\wedge W)=J\,\operatorname{vol}_{g_0},\qquad
g_0^{ef}\operatorname{tr}((\bar\nabla_eW)\wedge(\bar\nabla_fW))
=J_1\,\operatorname{vol}_{g_0}.
\tag{4}
\]
Use o dual de Hodge na última dupla do tensor de Weyl. Na assinatura e orientação de(3), \(\varepsilon^{0123}=-1/\sqrt{|\det g_0|}\), e
\[
J=\tfrac12 W_{abcd}(*W)^{abcd},\qquad
J_1=\tfrac12g_0^{ef}
 (\bar\nabla_eW_{abcd})(\bar\nabla_f(*W)^{abcd}).
\tag{5}
\]
O fator1/2 vem de escrever a duas-forma como Wcd dx^c∧dx^d/2 e tomar o traço dos índices internos antissimétricos. Por exemplo, nas formas de081 a contração \(W\cdot *W\) vale32EB, enquanto o coeficiente do traço exterior vale16EB. Se se escolher a contração sem o1/2 como definição de J1, todos os valores(1–2) dobram. Não há ambiguidade de normalização escondida no resultado.

A estrela, a métrica de contração e o volume de g0 são paralelos. A derivada não altera o fator de orientação.

A cúbica de ghosts é exatamente a \(\beta_o\) de081/082:
\[
m_{ab}=\bar\nabla_{[a}C_{b]},\quad
\beta=\tfrac12\varepsilon_{abcd}C^aC^b m^{cd}.
\tag{6}
\]
Não usamos a matriz M homônima das convenções082. Os colchetes incluem1/2.

J1 tem duas pernas h, \(\beta\) três ghosts. Logo \(b_5^{(1)}\) tem ghost3, valência5 e paridade ímpar. J1 e β são ambos pseudoescalares quanto à orientação, de modo que o produto é par sob essa inversão. Com [∇]=1, [C]=−1, [h]=0 e [κ]=−2,
\[
[J_1]=6,\quad[\beta]=-2,\quad[\kappa^2J_1\beta]=0.
\tag{7}
\]
O fatorκ² é herdado; não se introduz inverso de K ou de outro dado. Isso não verifica por si todas as restrições causais adicionais de scaling degree/contatos.

## 2. Fechamento linear e a identidade de onda com sinal derivado

O fechamento s0 é universal off-shell: \(W(g_0)=0\) e a naturalidade implicam \(W_{[1]}[\mathcal L_Cg_0]=0\) para todo ghost livre. A referência é inerte, logo
\[
s_0\bar\nabla W=s_0C=s_0m=0,\qquad
\boxed{s_0b_5^{(1)}=0.}
\tag{8}
\]
Nenhuma condição de Killing ou EOM foi usada nessa etapa.

Para calcular o detector, entramos na solução Einstein LINEAR de078. As EOM lineares implicam a Bianchi diferencial homogênea e a divergência nula de W:
\[
\bar\nabla^eW_{abed}=0,\qquad
\bar\nabla_eW_{abcd}+
\bar\nabla_cW_{abde}+
\bar\nabla_dW_{abec}=0.
\tag{9}
\]
Isso segue também diferenciando as identidades do Weyl do campo completo: numa família Einstein até primeira ordem, o Schouten é K g/2 até essa ordem, sua derivada covariante é zero e a Cotton linear é nula. Como W(g0)=0, não sobram termos de variação da conexão multiplicando um Weyl de fundo.

Aplique \(\bar\nabla^e\) à segunda identidade(9). Como as divergências de W são zero,
\[
\bar\Box W_{abcd}
=-g_0^{ef}[\bar\nabla_f,\bar\nabla_c]W_{abde}
-g_0^{ef}[\bar\nabla_f,\bar\nabla_d]W_{abec}.
\tag{10}
\]
Derivamos o sinal dos dois comutadores. Em um tensor de quatro índices baixos, cada índice recebe −R. Com
\[
\bar R^u{}_{afc}=K(\delta^u_f g_{0,ac}-\delta^u_c g_{0,af}),
\]
a primeira contração de(10) é
\[
\begin{aligned}
g_0^{ef}[\bar\nabla_f,\bar\nabla_c]W_{abde}
&=K\bigl(W_{cbda}+W_{acdb}-2W_{abcd}\bigr)\\
&=-3K W_{abcd}.
\end{aligned}
\tag{11}
\]
Na primeira linha, os traços de W foram zerados; as parcelas dos índices d,e dão \(+(1-3)K W=-2K W\). A Bianchi algébrica dá \(W_{cbda}+W_{acdb}=-W_{abcd}\). A segunda contração de(10) tem o mesmo valor −3KW, por trocar c,d e usar a antissimetria da dupla final.

Portanto
\[
\boxed{\bar\Box W_{abcd}=6K W_{abcd}.}
\tag{12}
\]
A convenção de \(\bar\Box=g_0^{ef}\bar\nabla_e\bar\nabla_f\) é a Lorentziana de(3). Não se importou o sinal de uma equação escrita noutra assinatura pelo nome de de Sitter ou AdS.

Levantar índices e aplicar estrela com g0 comutam com \(\bar\Box\). Usando Leibniz em(4), com a conexão em TODOS os slots,
\[
\bar\Box J=
2\,\frac{\operatorname{tr}((\bar\Box W)\wedge W)}
        {\operatorname{vol}_{g_0}}+2J_1
=12KJ+2J_1.
\]
Consequentemente
\[
\boxed{J_1=\tfrac12\bar\Box J-6KJ.}
\tag{13}
\]
(12–13) valem on-shell linear. Elas não substituem o fechamento off-shell de(8). O termo inferior −6KJ é parte essencial da resposta.

## 3. A família TT e por que □J não recebe uma derivada temporal esquecida

A solução de078 é \(h=a^2\gamma\), com
\[
\gamma_{11}=f(z)\cos(k\tau),\quad
\gamma_{22}=-f(z)\cos(k\tau),\quad
\gamma_{12}=f(z)\sin(k\tau),
\]
\[
f''-2f'/z+k^2f=0,\qquad
f(z_0)=0,\quad f'(z_0)=1,\quad z_0=\ell.
\tag{14}
\]
Ela satisfaz H0h=0 numa vizinhança inteira, com todos os prolongamentos. O código083 não reexecuta a prova078 das EOM.

A expressão J foi calculada081 ao longo de τ=x=y=0. Para usar \(\bar\Box J\), é necessário conhecer também a dependência fora dessa linha. O bloco transversal tem a forma
\[
Q(\tau)=
\begin{pmatrix}\cos(k\tau)&\sin(k\tau)\\
\sin(k\tau)&-\cos(k\tau)\end{pmatrix}
=R(k\tau/2)\,Q(0)\,R(k\tau/2)^T.
\tag{15}
\]
A transformação
\[
(\tau,(x,y),z)\mapsto
(\tau+\epsilon,R(k\epsilon/2)(x,y),z)
\]
é isometria orientada de g0 e preserva h por pullback: o R^T da transformação dos índices cancela o R acrescentado em Q. Equivalentemente,
\[
\mathcal L_Vg_0=\mathcal L_Vh=0,\qquad
V=\partial_\tau+\tfrac k2(-y\partial_x+x\partial_y).
\tag{16}
\]
Todo pseudoscalar natural construído de g0,h e seus jatos é invariante por essa simetria helicoidal. Como os dados já são independentes de x,y, (16) implica \(\partial_\tau J=0\) em toda a vizinhança, não apenas no ponto. Em particular \(\partial_\tau^2J=0\). O mesmo raciocínio se aplica a J1.

Assim, para uma função F(z) nessa família,
\[
\boxed{
\bar\Box F
=\frac1{a^4}\partial_z(-a^2F')
=\frac{z^2}{\ell^2}\left(-F''+\frac{2F'}z\right).
}
\tag{17}
\]
O termo 2F'/z vem da conexão/volume. Não foi usada uma derivada plana no lugar do laplaciano covariante.

## 4. Weyl antes dos dados pontuais e cálculo de J1

Na linha τ=x=y=0, ponha
\[
E(z)=\tfrac12(k^2f-f'/z),\qquad B(z)=\tfrac12kf'.
\]
Os componentes de Weyl de \(\eta+t\gamma\), como duas-formas com os índices internos abaixo por η, são
\[
\begin{aligned}
\widetilde W_{01}&=E e^{01}+B e^{23},&
\widetilde W_{02}&=-E e^{02}+B e^{13},\\
\widetilde W_{13}&=B e^{02}+E e^{13},&
\widetilde W_{23}&=B e^{01}-E e^{23}.
\end{aligned}
\tag{18}
\]
Os demais seguem das simetrias, ou são zero. Como em081, os componentes R0i0j=k²fQij/2 e R3i3j=−f''Qij/2, junto ao Schouten linear f'Qij/(2z) e aos componentes mistos de kf', fornecem(18). A EDO foi usada para a redução do Ricci. No campo conforme, \(W^a{}_{bcd}\) é invariante e \(W_{abcd}=a^2\widetilde W_{abcd}\).

O traço exterior dá
\[
J(z)=16(z/\ell)^4 EB
=\frac{4kz^4}{\ell^4}f'
 \left(k^2f-\frac{f'}z\right).
\tag{19}
\]
Agora use(13),(17), mantendo ℓ e k FIXOS ao diferenciar e reduzindo as derivadas de f pela EDO. Escrevendo p=f', obtém-se
\[
\boxed{
J_1(z)=\frac1{\ell^6}
\left[
80kz^3p^2
-100k^3z^4fp
-28k^3z^5p^2
+20k^5z^5f^2
+8k^5z^6fp
\right].
}
\tag{20}
\]
Essa expressão não é obtida derivando o valor pontual de J. Os dados f=0,p=1 e ℓ=z0 só entram DEPOIS das derivadas. Por isso
\[
\boxed{
J_1(z_0)=\frac{80k}{z_0^3}-\frac{28k^3}{z_0},\qquad
J_1'(z_0)=\frac{560k}{z_0^4}
-\frac{352k^3}{z_0^2}+8k^5.
}
\tag{21}
\]
Como controle relacionado, a mesma conta dá
\[
\boxed{(\bar\Box J)(z_0)=\frac{112k}{z_0^3}-\frac{56k^3}{z_0}.}
\tag{22}
\]
Não se extrai daqui uma primitiva CE horizontal; (22) é apenas o valor do laplaciano escalar, disponível para uma investigação separada desse candidato.

## 5. Controle independente de(13) pela derivada covariante explícita

O [script novo083](<C:/IALD/Central de Patentes/Chatgpt/CANDIDATO_DERIVADA_WEYL_083_20260910/compute_covariant_j1_new.py>) calcula J1 de DUAS maneiras. A primeira usa diretamente a conexão, sem usar a equação de onda(12) no corpo desse cálculo.

Escreva \(w=\log a\). A conexão é
\[
\bar\Gamma^u{}_{be}
=\delta^u_b w_e+\delta^u_e w_b-\eta_{be}w^u,
\qquad w_e=-\delta_{e3}/z.
\tag{23}
\]
Defina \(N_{e;abcd}=a^{-2}\bar\nabla_eW_{abcd}\). Então
\[
\boxed{
N_{e;abcd}=
\partial_e\widetilde W_{abcd}
+2w_e\widetilde W_{abcd}
-\bar\Gamma^u{}_{ae}\widetilde W_{ubcd}
-\bar\Gamma^u{}_{be}\widetilde W_{aucd}
-\bar\Gamma^u{}_{ce}\widetilde W_{abud}
-\bar\Gamma^u{}_{de}\widetilde W_{abcu}.
}
\tag{24}
\]
O termo \(2w_e\widetilde W\) vem do peso conforme a² dos quatro índices baixos. Ele não pode ser retirado porque o tensor misto seja conformemente invariante.

A derivada temporal em(24) também é conservada. Em τ=0, derive a conjugação(15): o gerador da rotação no bloco xy é
\[
A_{\rm rot}=\frac k2
\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\]
Ele atua em cada um dos quatro índices covariantes de \(\widetilde W\), no sentido da transformação ativa R de(15). As derivadas x,y são zero, mas suas derivadas COVARIANTES em(24) em geral não são zero: a conexão continua contribuindo para e=1,2.

Levante o primeiro índice de N com η e forme suas duas-formas matriciais. O fator de contração e volume é
\[
\boxed{
J_{1,\rm direto}=a^{-6}\sum_{e=0}^3
\eta^{ee}\,
\operatorname{coef}_{d\tau dxdy dz}
\operatorname{tr}\bigl((\eta^{-1}N_e)\wedge(\eta^{-1}N_e)\bigr).
}
\tag{25}
\]
As seis duplas exteriores independentes e os quatro índices internos são contraídos com os sinais exatos. O fator a^-6 é a^-2 da contração de e com f e a^-4 do volume, após o levantamento interno descrito. A conexão nos slots da forma já está em(24).

A segunda rota calcula \(J_{1,\rm onda}=\bar\Box J/2-6KJ\) pela derivada total
\[
D_z=\partial_z+p\,\partial_f+
\left(2p/z-k^2f\right)\partial_p
\tag{26}
\]
e por(17). O script encontra a identidade polinomial/Laurent EXATA
\[
J_{1,\rm direto}=J_{1,\rm onda},
\]
com ambos os lados iguais a(20), antes dos dados pontuais. Portanto não se está somente comparando duas avaliações numéricas.

O corpo aritmético é novo, escrito com Fraction e a biblioteca padrão. Não importou nem executou qualquer script081/082, não depende de SymPy ou instalação de pacotes e não materializa o kernel de um.py.

## 6. Variação BRST e o detector

É necessário conservar a correção s0 da covariância. Defina o pseudoscalar do campo completo
\[
\mathcal J_1(g)=
\frac{g^{ef}\operatorname{tr}
 ((\nabla^g_eW(g))\wedge(\nabla^g_fW(g)))}
 {\operatorname{vol}_g}.
\]
Como \(W(g_0)=\nabla^{g_0}W(g_0)=0\),
\[
\mathcal J_1(g_0+t h)=t^2J_1+t^3J_{1,3}+\cdots .
\]
A naturalidade orientada fornece \(s\mathcal J_1=tC^\mu\partial_\mu\mathcal J_1\). Comparar t³ dá a identidade OFF-SHELL
\[
\boxed{s_1J_1+s_0J_{1,3}=C^\mu\partial_\mu J_1.}
\tag{27}
\]
J1,3 é finito em jatos. Na avaliação078, os ghosts são combinações dos quatro Killing
\[
v_0=\partial_\tau,\quad v_1=\partial_x,\quad
v_2=\partial_y,\quad v_3=D/z_0.
\]
Logo R0C e todos os seus prolongamentos são zero, anulando s0J1,3. O termo não foi apagado antes dessa justificação.

Da [conta081](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md>),
\[
\operatorname{ev}\beta=-6\theta^{012}/z_0,\qquad
\operatorname{ev}(s_1\beta)=-18\theta^{0123}/z_0^2,
\qquad C^a(p_0)=\theta^a.
\tag{28}
\]
Os dados de ghosts são os mesmos em k e −k. A subálgebra dos Killing é fechada, com \(d_\theta\theta^i=\theta^i\theta^3/z_0\) para i=0,1,2, e \(d_\theta\theta^3=0\), pagando a segunda identidade(28) em todos os jatos.

J1 é par. No produto \((C\partial J_1)\beta\), as parcelas C0,1,2 se anulam por gerador repetido. A parcela θ3 atravessa três ghosts de θ012, dando o sinal negativo. Assim
\[
\operatorname{ev}(s_1(J_1\beta))=
\left(\frac6{z_0}J_1'-\frac{18}{z_0^2}J_1\right)\theta^{0123}.
\tag{29}
\]
Inserir(21) produz
\[
\frac6{z_0}(8k^5-352k^3/z_0^2+560k/z_0^4)
-\frac{18}{z_0^2}(80k/z_0^3-28k^3/z_0)
=\frac{48k^5}{z_0}-\frac{1608k^3}{z_0^3}
+\frac{1920k}{z_0^5}.
\tag{30}
\]
f−k=fk, e o resultado é ímpar em k. O [funcional079](<C:/IALD/Central de Patentes/Chatgpt/FUNCIONAL_IMPAR_TT_079_20260910/FUNCIONAL_IMPAR_E_ELIMINACAO_DA_CONTRIBUICAO_ANTIFIELD.md>) é a metade da diferença das duas avaliações; portanto conserva exatamente(30), sem um fator dois extra. Multiplicar peloκ² fixado dá(1).

Em k=2/z0, os três termos são \(1536-12864+3840=-7488\), todos sobre z0⁶. A resposta não é zero. A engenharia de(2) é consistente comκ² e com a dimensão escolhida dos ghosts.

## 7. O que o novo perfil decide e o que não decide

A [nota082 sem derivadas](<C:/IALD/Central de Patentes/Chatgpt/SETOR_QUADRATICO_SEM_DERIVADAS_082_20260910_050315_8076779/IMAGEM_DO_DETECTOR_NO_SETOR_FINITO.md>) demonstrou, naquele setor,
\[
L_k(s_1z_5)=A\,R(k),\qquad
R(k)=24k^3/z_0-96k/z_0^3,
\]
com A herdado e independente de k. Como R(2/z0)=0 e(2) não é zero, o novo perfil não pertence àquela linha de respostas.

Isso demonstra um limite efetivo do teste082: ele não pode ser promovido à anulação de todo o setor quadrático com jatos. O candidato083 é natural, s0-fechado e usa somente uma derivada de W em cada fator.

Por078/079, o detector anula s0 de qualquer expressão finita, incluindo primitivas com antifields, porque a família resolve as EOM lineares em toda a vizinhança e os ghosts são Killing. Consequentemente a avaliação(2) também certifica que \([s_1b_5^{(1)}]\ne0\) no alvo de E6. Não se trata apenas de uma expressão s0-exata escolhida com aparência não nula.

Ainda assim, NÃO foi demonstrado \(-[A_6]\in\delta(\mathcal K)\). Um detector linear não separa automaticamente todas as classes. Tampouco os DOIS perfis agora disponíveis bastam, sozinhos, para reproduzir \(+4k/z_0\) para todo k: em \(A R(k)+B R_1(k)\), comparar k⁵ força B=0, e depois comparar k³ força A=0. Aqui \(R_1\) é o perfil semκ² de(30); todos os coeficientes são herdados, sem depender de k.

Esta última observação é limitada à combinação desses perfis específicos. Não exclui outro candidato de primeira derivada, outros tipos de contração, jatos superiores ou uma combinação cuja igualdade de classes demande análise adicional.

[OPEN] A imagem completa do diferencial e a decisão de −[A6], o sistema universal de cancelamento, a classe causal admissível, outros fundos, anéis variáveis, QME e UV. Nenhuma conclusão geral de gravidade quântica é apresentada.

## 8. Custódia e natureza dos controles

O [recibo083](<C:/IALD/Central de Patentes/Chatgpt/CANDIDATO_DERIVADA_WEYL_083_20260910/CONTROLE_COVARIANTE_J1_083.json>) registra dez predicados algébricos exatos: simetrias de pares, Bianchi algébrica, traços do Weyl, normalização16EB, dois valores de referência de J, perfil081 usado como controle, igualdade da derivada covariante direta com(13), e paridade de J1 e de seu perfil. Alguns predicados percorrem componentes; a contagem declarada é dez predicados, não uma multiplicação artificial de verificações.

O recibo preserva separadamente as janelas antes/depois das três fontes do cálculo e do próprio script. O controle de preservação não é contado como um décimo primeiro teorema algébrico. A igualdade geral(12), a simetria helicoidal e as EOM na vizinhança são provas ESCRITAS com alcance explícito; o script não alega ter refeito Γ/Ricci de toda a solução078.

O manifesto desta nota mede novamente as fontes e os novos artefatos. Nenhum arquivo anterior foi editado. A confirmação limitada recebida de Turing sobre a simetria helicoidal não é apresentada como revisão integral083. A prova e o cálculo novos aguardam revisão independente específica.
