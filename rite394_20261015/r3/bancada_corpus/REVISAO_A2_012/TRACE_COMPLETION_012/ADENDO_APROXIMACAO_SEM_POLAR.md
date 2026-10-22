# Adendo matemático — variante t e prova de traço sem polar

**[DERIVED — argumento matemático conferido, ainda não formalizado aqui] A variante t=r+s* é correta e permite uma prova por aproximação que dispensa construir a isometria parcial polar.** Este adendo complementa `REVISAO_MATEMATICA.md` e oferece uma alternativa à sua obrigação de implementação por polar. A1 já fornece a tracialidade quadrática, a monotonicidade e o lema de semicontinuidade necessário. Não se refaz normalidade nem se usa o leitor total como premissa.

Mantenha p,q≥0, n≥1 e r,s no mesmo von Neumann algebra M, com pr=rq, sp=qs, pⁿ=rs e qⁿ=sr. Todos os operadores abaixo são limitados e pertencem ao mesmo M. τ denota exclusivamente o peso positivo A1.

**A expansão sugerida.** Com t=r+s*, temos t*=r*+s e, pelas duas relações de entrelaçamento, pt=tq. Como rs e sr são auto-adjuntos,

\[
R:=t^*t=r^*r+ss^*+2q^n\ge 2q^n,
\qquad
T:=tt^*=rr^*+s^*s+2p^n\ge 2p^n.
\]

Portanto a correção de `s*s` para `ss*` no primeiro produto é essencial. Não se está descartando termos cruzados: eles são exatamente 2qⁿ e 2pⁿ. Tomando adjuntos de pt=tq, segue t* p=q t*, daí Rq=qR e Tp=pT.

As desigualdades dão ker(t)⊆ker(q) e ker(t*)⊆ker(p); por isso o polar de t é suficiente para as partes não nulas, com o mesmo argumento de inclusões do parecer principal. Em geral ainda há um bloco extra: p=q=e₁₁, r=I, s=p, n=1 dão t=I+p, com polar I e suportes maiores. A sugestão w=tqⁿ=pⁿt remove esse bloco: w* w=qⁿRqⁿ≥2q³ⁿ e ww*=pⁿTpⁿ≥2p³ⁿ. Além disso, w mata ker(q) e w* mata ker(p). Logo ker(w)=ker(q) e ker(w*)=ker(p), e seu polar teria suportes exatamente supp(q) e supp(p). A prova por aproximação a seguir usa t diretamente e não precisa construir w ou seu polar.

**Regularizadores e fatoração exata.** Para ε>0, ponha

\[
h_\varepsilon(z)=z(z+\varepsilon I)^{-1},\qquad
S_\varepsilon=\sqrt p\,h_\varepsilon(T),\qquad
K_\varepsilon=t\sqrt R\,(R+\varepsilon I)^{-1}\sqrt q.
\]

As inversas são apenas dos operadores estritamente positivos R+εI e T+εI, dentro da álgebra unital M. Não há inversão de r, t, R, T ou dos endpoints. O cálculo funcional de um único operador dá 0≤hε(R),hε(T)≤I. As comutações já provadas permitem mover q e √q através das funções de R e p e √p através das funções de T.

O entrelaçamento tR=Tt dá

\[
t(R+\varepsilon I)^{-1}=(T+\varepsilon I)^{-1}t.
\]

Consequentemente,

\[
\begin{aligned}
K_\varepsilon^*K_\varepsilon
 &=\sqrt q\,R^2(R+\varepsilon I)^{-2}\sqrt q
 =\sqrt q\,h_\varepsilon(R)^2\sqrt q\le q,\\
K_\varepsilon K_\varepsilon^*
 &=p\,tR(R+\varepsilon I)^{-2}t^*
 =p\,T^2(T+\varepsilon I)^{-2}
 =p\,h_\varepsilon(T)^2
 =S_\varepsilon^*S_\varepsilon.
\end{aligned}
\]

Para conferir a segunda linha sem supor um entrelaçamento de raízes, expanda KεKε*: √R comuta com q e com o resolvente, logo o miolo vira qR(R+εI)⁻²; use tq=pt e transporte somente o polinômio/resolvente através de t. As raízes de R se multiplicam antes desse transporte. Para a primeira desigualdade basta hε(R)²≤I e conjugação por √q.

Agora use somente A1:

\[
\tau(S_\varepsilon^*S_\varepsilon)
=\tau(K_\varepsilon K_\varepsilon^*)
=\tau(K_\varepsilon^*K_\varepsilon)
\le\tau(q).
\]

O termo central é exatamente uma aplicação de `scalarInverseLimitWeight_tracial`; a desigualdade usa `scalarInverseLimitWeight_mono`. Nenhum desses passos pressupõe τ(p)=τ(q), finitude de τ(q) ou ciclicidade de um traço total.

**Convergência em norma, sem projetor de suporte.** Ponha Eε=I−hε(T)=ε(T+εI)⁻¹. Então 0≤Eε≤I, TEε≤εI, e Eε comuta com p. Para todo δ>0 e x≥0,

\[
\sqrt x\le\sqrt\delta+\delta^{1/2-n}x^n.
\]

Se x≤δ, o primeiro termo basta; se x≥δ, o segundo é pelo menos √x porque n≥1. Aplicando cálculo funcional a p e multiplicando por Eε, com preservação de ordem pelas comutações, obtemos

\[
\begin{aligned}
0\le\sqrt p E_\varepsilon
&\le\sqrt\delta E_\varepsilon+\delta^{1/2-n}p^n E_\varepsilon\\
&\le\left(\sqrt\delta+\frac\varepsilon2\delta^{1/2-n}\right)I.
\end{aligned}
\]

Aqui se usou pⁿ≤T/2 e TEε≤εI. Como √p Eε é positivo, a ordem limita sua norma. Assim

\[
\|S_\varepsilon-\sqrt p\|
\le\sqrt\delta+\frac\varepsilon2\delta^{1/2-n}.
\]

Fixar primeiro δ pequeno e depois ε pequeno prova Sε→√p em norma. Alternativamente, δ=ε¹ᐟⁿ dá a estimativa explícita

\[
\boxed{\|S_\varepsilon-\sqrt p\|\le\tfrac32\varepsilon^{1/(2n)}}.
\]

Isso evita construir o limite forte de um polar regularizado, projeções espectrais mensuráveis ou a topologia de fechos de imagem. Ainda exige formalizar as identidades de resolventes e as desigualdades de cálculo funcional acima; não é um wrapper pronto.

**Aplicação exata do fornecedor pago.** Escolha εm=1/(m+1), para m∈ℕ, use a sequência `A m = S_(εm)`, o limite `S = √p` e a cota `C = τ(q)` em

`TGLV350.Regular.scalarInverseLimitWeight_square_le_of_strong`,

localizado em `TGLExt/V351InverseLimitTracialExtension.lean`, linha 46. Sua assinatura recebe convergência forte ponto a ponto e cotas uniformes de τ(A_m* A_m), e conclui τ(S* S)≤C; não exige convergência dos adjuntos nem que C seja finito. A convergência em norma demonstrada fornece a hipótese forte. Como (√p)*√p=p, resulta τ(p)≤τ(q). Aplique o mesmo argumento aos dados trocados (q,p,s,r), para os quais t'=t*, e obtenha τ(q)≤τ(p). Antissimetria em ENNReal fecha a igualdade, também no caso infinito.

Esta rota usa a semicontinuidade quadrática já paga de A1; não infere continuidade de τ para limites fortes ou em norma. Tais continuidades globais seriam uma hipótese indevida para um peso não limitado. Também não calcula τ(p)−τ(q).

**Situação do leitor congelado.** Foi lida a versão informada de `V354CyclicTraceCompletion.lean`, incluindo `positiveTrace_le_cyclicTraceCandidate`, `cyclicTraceCandidate_zero`, `cyclicTraceCandidate_positive_faithful` e a igualdade ainda condicionada por `compatible`. Zero e fidelidade positiva independem da compatibilidade: um auto-adjunto relacionado a zero é nilpotente e portanto zero; τ(p)≤F(p) impede que F anule um positivo não nulo. Essa cota inferior, mesmo junto de zero/fidelidade, não limita F(PF) superiormente nem prova aditividade positiva. A compatibilidade demonstrada no papel é que fornecerá F|M₊=τ. `asCore` apenas embala a pertença já contida em PositiveCoreInput; não cria projeção, peso ou testemunha analítica.

Os 16 nomes e o rc0 foram informados pela autoria [DECLARADO]; esta rodada permaneceu revisão matemática, sem nova compilação independente. As duas provas no papel tornam a rota matematicamente defensável; a formalização do argumento escolhido e a posterior revisão dos consumidores continuam [OPEN]. Não foi instanciado nem certificado ContinuousCoreData, ThreeLocksCoreData ou FullWitness nesta revisão. Não se declara A2 concluído.
