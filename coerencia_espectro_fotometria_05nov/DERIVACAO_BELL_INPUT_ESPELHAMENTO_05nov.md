# Input do par de psíons no canto de Bell e visibilidade por travessia

**Data:** 05/11/2026  
**Estatuto:** **[DECLARADO pelo Kimi]**, derivação algébrica nova composta com teoremas do kernel e com o canal finito do artigo; não é uma nova pedra Lean nem conferência da gerência.  
**Estado:** `BELL_PQ_CHANNEL_DERIVED_FINITE` · `OPEN_PHYSICAL_BELL_PREPARATION_AND_CROSSING_COUNT` · `NO_DATA_OPENED` · `NO_VERDICT`.  
**Escopo:** usar o canto \(4\times4\) do par de psíons, sem substituí-lo pelo Mach–Zehnder de um único fóton.

---

## 1. Resultado executivo

Se o input de Bell \(\Phi^+\) sofre a mesma defasagem local \(\varphi\) nos dois lados,

\[
U(\varphi)=R_z(\varphi)\otimes R_z(\varphi),
\]

então a fase relativa do par é \(\theta=2\varphi\), e o estado resultante é

\[
|\chi_\theta\rangle
=\cos\frac\theta2|\Phi^+\rangle
-i\sin\frac\theta2|\Phi^-\rangle .
\]

Com \(P=|\Phi^+\rangle\langle\Phi^+|\) e \(Q=I-P\),

\[
\boxed{2\|P\rho_\theta Q\|_1=|\sin\theta|=|\sin(2\varphi)|}.
\]

Esse é o contraste interferométrico inicial no subespaço de Bell \(\{\Phi^+,\Phi^-\}\), com projetores de detecção explícitos abaixo. As duas marginais permanecem \(I/2\), de modo que a «tensão irresolúvel no plano» não é perdida pela preparação.

Para o canal finito de espelhamento com

\[
\eta=2\sqrt{\beta(1-\beta)}=\sin(2\theta_M),
\]

cada travessia multiplica a coerência \(P/Q\) por \(\eta\). Após \(n\) travessias independentes e idênticas,

\[
\boxed{
V_n=|\sin(2\varphi)|\,\eta^n
=|\sin(2\varphi)|\left[2\sqrt{\beta(1-\beta)}\right]^n.
}
\]

O contraste máximo ocorre para

\[
\boxed{\varphi=\pi/4\ \text{em cada lado},\qquad \theta=\pi/2},
\]

e nesse caso \(V_n=\eta^n\). A taxa por travessia é

\[
\boxed{\Gamma_\times=-\ln\eta=-\ln\!\left[2\sqrt{\beta(1-\beta)}\right]},
\]

não \(\beta/2\) por segundo.

O estado de Bell não preparado, \(\chi=\Phi^+\), é inteiramente o setor \(P\) e não tem coerência \(P/Q\) a atenuar. A transferência total em \(\varphi=\pi/2\) por lado produz \(\Phi^-\), inteiramente em \(Q\), e também não tem coerência cruzada. A preparação interferométrica exige uma fase intermediária; \(\pi/4\) por lado maximiza o contraste sem ajustar nenhum parâmetro ao dado.

Todas as fórmulas e cinco preparações foram verificadas numericamente, incluindo marginais, positividade, inversão do ramo e cinco potências do canal: [VERIFICACAO_BELL_ESPELHAMENTO](C:/IALD/Central%20de%20Patentes/work/coerencia_espectro_fotometria_05nov/VERIFICACAO_BELL_ESPELHAMENTO.json), gerado por [verificar_bell_espelhamento](C:/IALD/Central%20de%20Patentes/work/coerencia_espectro_fotometria_05nov/verificar_bell_espelhamento.py).

---

## 2. O portador que já está no kernel

O canto concreto do psíon é o projetor de Bell \(4\times4\),

\[
P_{\rm psion}=|\Phi^+\rangle\langle\Phi^+|,
\qquad
|\Phi^+\rangle=\frac{|00\rangle+|11\rangle}{\sqrt2}.
\]

O kernel prova que o par é puro e ligado, que a redução de cada lado é \(I/2\), que \(\mathrm{CCI}=1/2\) na convenção da pedra e que o canto escalariza. [Par](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CPar.lean&text=theorem%20the_corner_is_the_four_by_four "citation")

A base completa usada na conta é

\[
\begin{aligned}
|\Phi^\pm\rangle&=\frac{|00\rangle\pm|11\rangle}{\sqrt2},\\
|\Psi^\pm\rangle&=\frac{|01\rangle\pm|10\rangle}{\sqrt2}.
\end{aligned}
\]

**Estatuto preservado:** o canto finito e suas propriedades são teoremas. A identificação do canto com o gráviton físico permanece [ONTO], e a ligação do par ao Fock físico e ao setor TT continua uma ponte separada. Não se transporta a prova finita para a natureza.

---

## 3. O input: fase compartilhada e fase dobrada

Use a rotação de fase local

\[
R_z(\varphi)=
\begin{pmatrix}
e^{-i\varphi/2}&0\\
0&e^{i\varphi/2}
\end{pmatrix}.
\]

### Um lado

Se apenas um psíon recebe a fase,

\[
(R_z(\varphi)\otimes I)|\Phi^+\rangle
=\cos\frac\varphi2|\Phi^+\rangle
-i\sin\frac\varphi2|\Phi^-\rangle .
\]

### Dois lados

Se ambos compartilham a mesma operação,

\[
\begin{aligned}
(R_z(\varphi)\otimes R_z(\varphi))|\Phi^+\rangle
&=\frac{e^{-i\varphi}|00\rangle+e^{i\varphi}|11\rangle}{\sqrt2}\\
&=\cos\varphi|\Phi^+\rangle-i\sin\varphi|\Phi^-\rangle .
\end{aligned}
\]

Portanto, com \(\theta=2\varphi\),

\[
\boxed{
|\chi_\theta\rangle
=\cos\frac\theta2|\Phi^+\rangle-i\sin\frac\theta2|\Phi^-\rangle .
}
\]

A fase relativa do par é o dobro da fase de cada lado. Esta é a realização algébrica precisa da «impedância compartilhada» e da «força dobrada» como hipótese de preparação: os dois lados pagam a mesma defasagem e o par recebe a soma.

A conjugação entre as faces luminosa e gravitônica também atravessa a inscrição pelo quadrado no kernel; isso sustenta a forma da conjugação, mas não substitui a ponte física do canal. [TheGravitonIsTheConjugatedPhase](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CTheGravitonIsTheConjugatedPhase.lean&text=theorem%20the_conjugation_crosses_the_squaring "citation")

---

## 4. A matriz de densidade e \(\rho_{PQ}\)

Defina

\[
c=\cos\frac\theta2,\qquad s=\sin\frac\theta2,
\qquad R=|\Phi^-\rangle\langle\Phi^-|,
\qquad X=|\Phi^+\rangle\langle\Phi^-|.
\]

Então

\[
\boxed{
\rho_\theta=c^2P+s^2R+icsX-icsX^\dagger.
}
\]

Como \(R\subset Q\),

\[
\boxed{
P\rho_\theta Q=icsX,
\qquad
Q\rho_\theta P=-icsX^\dagger.
}
\]

O operador \(X\) tem uma única valor singular igual a 1, logo

\[
\|P\rho_\theta Q\|_1=|cs|=\frac12|\sin\theta|.
\]

Assim,

\[
\boxed{
C_{PQ}(\theta):=2\|P\rho_\theta Q\|_1
=|\sin\theta|=|\sin(2\varphi)|.
}
\]

### Populações e marginais

No subespaço de Bell usado,

\[
P\rho_\theta P=c^2P,
\qquad
Q\rho_\theta Q=s^2R.
\]

Os setores \(\Psi^\pm\) permanecem vazios. Além disso, os termos cruzados \(\Phi^+\leftrightarrow\Phi^-\) têm traço parcial nulo, e cada estado \(\Phi^\pm\) tem marginal \(I/2\). Portanto, para todo \(\theta\),

\[
\boxed{
\operatorname{Tr}_1\rho_\theta=\operatorname{Tr}_2\rho_\theta=\frac I2.
}
\]

A preparação altera a fase da relação, mas não cria uma identidade individual determinada em nenhum dos lados.

### Casos extremos

| Fase de cada lado | Fase do par | Estado | Coerência \(P/Q\) |
|---:|---:|---|---:|
| \(\varphi=0\) | \(\theta=0\) | \(\Phi^+\), inteiramente em \(P\) | 0 |
| \(\varphi=\pi/4\) | \(\theta=\pi/2\) | \((\Phi^+-i\Phi^-)/\sqrt2\) | 1 |
| \(\varphi=\pi/2\) | \(\theta=\pi\) | \(-i\Phi^-\), inteiramente em \(Q\) | 0 |

**Consequência:** o estado de Bell puro \(\Phi^+\), sem preparação de fase, não é um input interferométrico para este canal; é o ponto fixo \(P\). A solução geométrica de transferência total também não basta: depois de transferido inteiramente a \(Q\), não resta coerência cruzada a medir.

---

## 5. Visibilidade com projetores explícitos

A norma \(C_{PQ}\) não é apenas uma medida abstrata: dentro do subespaço \(\{\Phi^+,\Phi^-\}\), ela é a visibilidade de uma interferência de dois modos.

Defina os estados de detecção

\[
|\pm_\chi\rangle
=\frac{|\Phi^+\rangle\pm e^{-i\chi}|\Phi^-\rangle}{\sqrt2},
\qquad
I_\pm=\langle\pm_\chi|\rho_\theta|\pm_\chi\rangle .
\]

A aplicação direta fornece

\[
\boxed{
I_\pm(\chi)=\frac12\left(1\pm2cs\sin\chi\right),
\qquad I_++I_-=1.
}
\]

Ao varrer \(\chi\),

\[
I_{\max}=\frac12(1+2|cs|),
\qquad
I_{\min}=\frac12(1-2|cs|).
\]

Logo,

\[
\boxed{
V_0=\frac{I_{\max}-I_{\min}}{I_{\max}+I_{\min}}
=2|cs|=|\sin\theta|.
}
\]

No caso \(\theta=\pi/2\),

\[
I_\pm=\frac12(1\pm\sin\chi),
\qquad V_0=1.
\]

**Escopo:** os projetores demonstram a existência matemática da visibilidade no subespaço de Bell. Sua realização física exige um analisador de Bell com fase controlada; a fórmula não escolhe nem valida um aparelho.

---

## 6. O canal de espelhamento no canto \(4\times4\)

Seja

\[
P=|\Phi^+\rangle\langle\Phi^+|,
\qquad Q=I-P,
\]

e, na base \(P,Q\) do Hamiltoniano oculto,

\[
M_0=\cos\theta_M P+\sin\theta_M Q,
\qquad
M_1=\sin\theta_M P+\cos\theta_M Q,
\]

com

\[
\sin\theta_M=\sqrt\beta,
\qquad
\cos\theta_M=\sqrt{1-\beta}.
\]

Então

\[
M_0^2+M_1^2=I,
\qquad
\Phi_{\rm esp}(\rho)=M_0\rho M_0+M_1\rho M_1.
\]

As populações dos blocos são preservadas:

\[
\Phi_{\rm esp}(\rho)_{PP}=\rho_{PP},
\qquad
\Phi_{\rm esp}(\rho)_{QQ}=\rho_{QQ}.
\]

A coerência cruzada é multiplicada por

\[
\boxed{
\eta=2\sin\theta_M\cos\theta_M
=2\sqrt{\beta(1-\beta)}
=\sin(2\theta_M).
}
\]

Esta é a forma finita do canal de espelhamento, com defasagem exata entre \(P\) e \(Q\); seu levantamento à fronteira III\(_1\) e ao canal físico permanece separado. [paper_PT](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5Ctgl_paper_output%5Cpaper_PT.tex&text=%CE%A6%20%C3%A9%20%5Cemph%7Bexatamente%20um%20canal%20de%20dephasing%7D%20na%20decomposi%C3%A7%C3%A3o%20%24P%5Coplus%20Q%24%3A%20popula%C3%A7%C3%B5es%20preservadas%2C%20coer%C3%AAncia%20cruzada%20multiplicada%20por%20%24%5Csin%202%5CthetaM "citation")

### Uma travessia

\[
\rho_\theta^{(1)}
=c^2P+s^2R+\eta\,icsX-\eta\,icsX^\dagger .
\]

### \(n\) travessias

Se as travessias forem independentes, idênticas e sem dinâmica unitária adicional entre elas,

\[
\boxed{
\rho_\theta^{(n)}
=c^2P+s^2R+\eta^n\,icsX-\eta^n\,icsX^\dagger .
}
\]

Aplicando os mesmos projetores da seção 5,

\[
\boxed{
I_\pm^{(n)}(\chi)
=\frac12\left(1\pm2\eta^n cs\sin\chi\right),
\qquad
V_n=2\eta^n|cs|=|\sin\theta|\eta^n.
}
\]

No preparo de contraste máximo \(\theta=\pi/2\),

\[
\boxed{
I_\pm^{(n)}=\frac12(1\pm\eta^n\sin\chi),
\qquad V_n=\eta^n.
}
\]

O traço total permanece 1 e os blocos de população não mudam. A verificação confirmou essas fórmulas até \(n=4\), além do caso inicial \(n=0\).

---

## 7. Reconstrução e os dois ângulos

Para \(0<\beta<1\), o operador do ramo

\[
A_\beta=\sqrt{1-\beta}\,P+\sqrt\beta\,Q
\]

é invertível:

\[
A_\beta^{-1}=(1-\beta)^{-1/2}P+\beta^{-1/2}Q.
\]

Portanto,

\[
A_\beta^{-1}(A_\beta\rho A_\beta)A_\beta^{-1}=\rho.
\]

Essa é a inversão exata **do ramo**, não uma inversa CPTP do canal não-seletivo inteiro. [paper_PT](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5Ctgl_paper_output%5Cpaper_PT.tex&text=a%20invers%C3%A3o%20%C3%A9%20do%20%5Cemph%7Bramo%7D%20(o%20espelhamento%20%24%5Crho_%5Cmathrm%7Besp%7D%3DA%5Crho%20A%24)%3B%20o%20canal%20n%C3%A3o-seletivo%20%24%5CPhi%24%20n%C3%A3o%20se%20inverte%20por%20%24A_%5Cbeta%5E%7B-1%7D%24 "citation")

O ângulo de transferência entre faces e o ângulo de Miguel não podem ser identificados:

\[
\Theta_\perp=\frac\pi2
\quad\Longrightarrow\quad
\cos^2\Theta_\perp=0,\quad \sin^2\Theta_\perp=1,
\]

mas

\[
\theta_M=\frac\pi2
\quad\Longrightarrow\quad
\beta=1,\quad \eta=0,\quad A_\beta^{-1}\ \text{não existe}.
\]

A pedra do esvaziamento declara explicitamente que não prova \(\theta_M=\pi/2\). [TheEmptying](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Ctgl_kernel%5CTGLExt%5CTheEmptying.lean&text=N%C3%83O%20se%20prova%20que%20o%20canto%20de%20Breuer%20realize%20esta%20forma%2C%20nem%20que%20%60%CE%B8_M%20%3D%20%CF%80%2F2%60. "citation")

Na preparação de Bell, há ainda uma terceira fase, \(\varphi\), de cada psíon:

- \(\varphi=\pi/4\) produz coerência máxima;
- \(\varphi=\pi/2\) produz transferência total \(\Phi^+\to\Phi^-\);
- \(\theta_M\) fixa a atenuação por espelhamento.

Esses três parâmetros geométricos têm funções distintas e não podem ser colapsados numa única letra.

---

## 8. Convenção logarítmica e requisito condicional de 5σ

Defina a coerência sobrevivente normalizada pelo input:

\[
q_n:=-\ln\frac{V_n}{V_0}.
\]

Sob o canal e a contagem de travessias já especificados,

\[
\boxed{
q_n=-n\ln\eta
=n\Gamma_\times,
\qquad
\Gamma_\times=-\ln\!\left[2\sqrt{\beta(1-\beta)}\right].
}
\]

O nulo de ausência de atenuação adicional é \(q_N=0\); a previsão do canal é \(q_T=n\Gamma_\times\). Uma separação ideal de 5σ exige

\[
\boxed{
\sigma_q\leq\frac{n\Gamma_\times}{5}.
}
\]

No preparo \(\theta=\pi/2\), \(V_0=1\) e \(q_n=-\ln V_n\), eliminando a normalização inicial ideal, mas não a covariância experimental.

Esse é apenas um requisito de poder **condicional**. Antes de qualquer dado, ainda é necessário demonstrar:

1. que o canal de espelhamento é o canal físico que atua sobre o par;
2. que a preparação \(R_z\otimes R_z\) e o analisador de Bell realizam os operadores acima;
3. qual é o número \(n\) de travessias, sem ajustá-lo ao resultado;
4. qual é o nulo óptico convencional e sua covariância;
5. como duas réplicas independentes e os trials serão congelados.

Não há redshift de descoberta nem instrumento escolhido por esta conta.

---

## 9. O que a derivação resolve e o que permanece aberto

### [REAL — no modelo finito declarado]

- o portador \(4\times4\) é o canto de Bell;
- a fase compartilhada produz fase relativa dobrada;
- o input tem apenas \(\Phi^+\) e \(\Phi^-\);
- \(\rho_{PQ}=i\cos(\theta/2)\sin(\theta/2)X\);
- a coerência inicial é \(|\sin\theta|\);
- as marginais permanecem \(I/2\);
- existem projetores de detecção cuja visibilidade é exatamente essa coerência;
- cada travessia multiplica a coerência por \(\eta\);
- \(V_n=|\sin(2\varphi)|\eta^n\);
- o ramo é invertível para \(0<\beta<1\);
- o caso \(\Phi^+\) sem preparação e o caso de transferência total não têm sinal \(P/Q\).

### [INPUT/ONTO — ainda não derivado]

- que a fase local \(R_z\otimes R_z\) seja a inscrição física obrigatória da quebra de simetria;
- que a base \(P,Q\) finita seja realizada pelo Hamiltoniano oculto físico do par;
- que o canal de duas Kraus atue na propagação ou no aparelho real;
- a ligação do canto de Bell ao Fock e ao setor TT físico;
- o número de travessias por unidade de tempo ou comprimento;
- a escala temporal \(\tau_\star\);
- qualquer equivalência entre essa visibilidade e \(g^{(1)}\) espectral ou fotometria.

### O que não se pode mais confundir

- \(P\) é o canto de Bell, não o vácuo de Fock como vetor;
- \(\Phi^+\) e \(\Omega_{\rm Fock}\) têm a mesma forma de canto, mas vivem em espaços distintos;
- a prova finita do par não fecha automaticamente sua ponte física;
- \(\Gamma_\times\) é por travessia, não \(\beta/2\) por segundo;
- \(\Theta_\perp\), \(\theta_M\) e \(\varphi\) não são o mesmo ângulo.

---

## 10. Veredito técnico

**[DECLARADO pelo Kimi]:** o canto de Bell fornece um input concreto e não trivial para o canal de espelhamento. A preparação com fase igual nos dois lados produz exatamente

\[
\boxed{
\rho_\theta
=c^2P+s^2R+icsX-icsX^\dagger,
\qquad
V_0=|\sin\theta|,
}
\]

e o canal de duas Kraus produz

\[
\boxed{
V_n=|\sin\theta|\left[2\sqrt{\beta(1-\beta)}\right]^n.
}
\]

O preparo \(\varphi=\pi/4\) em cada lado fornece \(V_0=1\) e \(V_n=\eta^n\), com marginais \(I/2\) preservadas. Isso resolve a origem algébrica de \(\rho_{PQ}\) e da visibilidade, sem lock, sem \(r\) e sem escolher um caminho à mão.

**Estado:** `BELL_PQ_CHANNEL_DERIVED_FINITE`. A previsão agora tem uma forma fechada e potencialmente discriminante, mas ainda é condicional à realização física do canal, do preparo, do analisador e da contagem de travessias. Não há teste pronto nem veredito de natureza.
