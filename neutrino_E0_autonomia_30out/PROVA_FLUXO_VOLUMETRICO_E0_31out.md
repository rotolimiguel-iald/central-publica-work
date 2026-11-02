# Certificado volumétrico de E₀ — teorema do fluxo modular

**Data:** 31/10/2026  
**Estatuto:** **[DERIVED condicional]** para a redução a fluxo e para a carga singular; **[OPEN]** para a normalização de 1 eV.

## 1. Unidades corretas

Defina, com \(\theta_M>0\) constante,

\[
u(\mathbf x)=\log\frac{R_{\rm mod}(\mathbf x)}{\theta_M},
\qquad
\rho_{\rm eff}=-\frac{c^2}{4\pi G}\nabla^2u .
\]

Como \([c^2/G]=\mathrm{kg/m}\) e \([\nabla^2u]=\mathrm{m^{-2}}\), temos

\[
[\rho_{\rm eff}]=\mathrm{kg/m^3}.
\]

Logo, \(\rho_{\rm eff}\) é densidade de **massa**, não densidade de energia. A densidade de energia é \(c^2\rho_{\rm eff}\), e

\[
M(B)=\int_B\rho_{\rm eff}\,dV,\qquad E(B)=c^2M(B).
\]

A condição de Dirichlet \(R_{\rm mod}=\theta_M\) **somente na fronteira** fixa \(u|_{\partial B}=0\), mas não \(\partial_nu|_{\partial B}=0\); portanto, não fixa a energia. Se a igualdade valer em todo o domínio, então \(u\equiv0\) e a energia regular é zero.

## 2. Teorema do fluxo de fronteira

Para \(B\) regular, \(R_{\rm mod}>0\) e \(u\in C^2(\overline B)\), o teorema da divergência dá

\[
M(B)=-\frac{c^2}{4\pi G}\oint_{\partial B}\partial_nu\,dA .
\]

Defina o comprimento de fluxo modular

\[
\boxed{\mathcal F[B]:=-\oint_{\partial B}\partial_nu\,dA},
\qquad [\mathcal F]=\mathrm m .
\]

Então

\[
\boxed{M(B)=\frac{c^2}{4\pi G}\mathcal F[B]},
\qquad
\boxed{E(B)=\frac{c^4}{4\pi G}\mathcal F[B]} .
\]

Toda a estrutura interna desaparece da energia total: resta apenas o traço normal de \(u\) na fronteira.

Para uma bola \(B_R\), com \(u=u(r)\),

\[
\mathcal F[B_R]=-4\pi R^2u'(R),
\qquad
M=-\frac{c^2}{G}R^2u'(R),
\qquad
E=-\frac{c^4}{G}R^2u'(R).
\]

## 3. Fluxo exigido para 1 eV

Com \(E_0=1\,\mathrm{eV}=1{,}602176634\times10^{-19}\,\mathrm J\), a condição necessária e suficiente é

\[
\boxed{
\mathcal F[B]=\mathcal F_0
:=\frac{4\pi G E_0}{c^4}
=1{,}6635032296\times10^{-62}\ \mathrm m .
}
\]

A massa equivalente e a carga de monopolo são

\[
m_0=\frac{E_0}{c^2}=1{,}7826619216\times10^{-36}\ \mathrm{kg},
\qquad
q_0=\frac{GE_0}{c^4}=1{,}3237738092\times10^{-63}\ \mathrm m .
\]

Esses números foram recalculados em [calcular_fluxo_1eV.py](calcular_fluxo_1eV.py). Eles são critérios, não derivações.

## 4. A condição de fronteira não fixa o fluxo

Considere, para qualquer \(a\),

\[
u_a(r)=a\left(1-\frac{r^2}{R^2}\right).
\]

Todos os perfis obedecem \(u_a(R)=0\), isto é, a mesma condição de Dirichlet na fronteira. Contudo,

\[
u_a'(R)=-\frac{2a}{R},
\qquad
\mathcal F=8\pi aR,
\qquad
E_a=\frac{2c^4}{G}aR .
\]

A mesma condição \(R_{\rm mod}=\theta_M\) admite, portanto, energia arbitrária. Só se adicionalmente \(\partial_nu=0\) é que o fluxo regular se anula.

## 5. Condensação pontual: carga finita, magnitude livre

Para o monopolo radial

\[
u_q(r)=\frac qr,\qquad q>0,
\]

vale, distribucionalmente,

\[
\nabla^2u_q=-4\pi q\,\delta^3(\mathbf x).
\]

Logo,

\[
\rho_{\rm eff}=\frac{c^2q}{G}\delta^3(\mathbf x),
\qquad
M=\frac{c^2q}{G},
\qquad
E=\frac{c^4q}{G},
\qquad
\mathcal F=4\pi q .
\]

A integral é independente da região que contenha a singularidade. A condensação, portanto, pode produzir massa/energia de repouso finita, mas a carga \(q\) continua livre. Para obter 1 eV seria necessário provar independentemente \(q=q_0\); atribuir esse valor é repetir o alvo como entrada.

A regularização

\[
u_{q,a}(r)=\frac{q}{\sqrt{r^2+a^2}}
\]

mostra que \(\int_{\mathbb R^3}\rho_{q,a}\,dV=M\) permanece finita e constante para todo \(a>0\), enquanto a **densidade** converge distribucionalmente, \(\rho_{q,a}\rightharpoonup M\delta^3\), quando \(a\to0\). Contudo, a autoenergia de campo da carga exatamente pontual diverge no limite UV; uma conclusão física completa exige uma completação ou renormalização UV cujo **resultado finito** seja independente do regulador.

## 6. A lei de fluxo existente também não fornece o número

Se se adota a lei adicional já registrada \(\mathcal F=\beta R_B\), então

\[
E=\frac{c^4}{4\pi G}\beta R_B .
\]

Para obter 1 eV seria necessário

\[
R_B=\frac{\mathcal F_0}{\beta}
=1{,}3826462429\times10^{-60}\ \mathrm m .
\]

Esse raio não é fornecido pelos perfis físicos encontrados; escolhê-lo por causa do alvo seria ajuste. A lei de Gauss por si só não produz nem \(R_B\) nem a carga.

## Veredito

**Provado condicionalmente:** a energia volumétrica se reduz ao fluxo de \(\partial_n\log(R_{\rm mod}/\theta_M)\) na fronteira; uma condensação pontual pode ter carga integrada finita e independente da região.

**Não provado:** o valor 1 eV. A entrada independente ainda necessária é exatamente uma das seguintes:

- o fluxo \(\mathcal F[B]\) e sua região;
- a carga de monopolo \(q\); ou
- uma lei física independente que os determine, sem usar E₀, m₂ ou Δm²₂₁.

A estacionariedade e a condensação fixam o suporte da distribuição, não sua carga. A parte volumétrica da prova fica, portanto, fechada até a forma do fluxo, mas a normalização numérica continua aberta.
