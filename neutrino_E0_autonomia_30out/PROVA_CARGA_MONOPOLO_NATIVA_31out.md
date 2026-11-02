# Carga do monopolo e o ramo nativo de E₀

**Data:** 31/10/2026  
**Estatuto:** **[DERIVED condicional]** para a forma \(q=c\tau^\star/(4\pi)\); **[OPEN]** para uma escala que produza 1 eV.

## 1. Da lei de fluxo à carga

A lei de fluxo registrada fornece

\[
\mathcal F=\beta R_B,
\qquad
M=\frac{c^2}{4\pi G}\beta R_B,
\qquad
E=\frac{c^4}{4\pi G}\beta R_B .
\]

Comparando com a solução de monopolo \(E=c^4q/G\), identifica-se

\[
\boxed{q=\frac{\beta R_B}{4\pi}} .
\]

A escolha de \(R_B\) continua sendo o dado dimensional que falta; \(\beta\) sozinho não o seleciona.

## 2. A escala dissipativa e o cancelamento de β

Como entrada condicional, usa-se a forma causal-dissipativa registrada

\[
R_B=\frac{c}{\Gamma_B},
\]

e a identificação nativa \(\Gamma_B=\beta/\tau^\star\). A compatibilidade dessa taxa de fronteira com a lei canônica \(\Gamma_\omega=\tfrac12\beta\tau^\star\omega^2\) ainda deve ser demonstrada; não são objetos idênticos por homonímia. Sob essas duas entradas,

\[
R_B=\frac{c\tau^\star}{\beta}.
\]

Substituindo na carga,

\[
\boxed{q=\frac{\beta}{4\pi}\frac{c\tau^\star}{\beta}
=\frac{c\tau^\star}{4\pi}} .
\]

Logo,

\[
\boxed{E=\frac{c^4q}{G}
=\frac{c^5\tau^\star}{4\pi G}} .
\]

**β cancela exatamente.** A carga e a energia dependem apenas da escala temporal da dissipação, não mais da constante adimensional. Esta é uma redução independente de E₀, m₂ e Δm²₂₁.

## 3. O ramo nativo planckiano

Com \(\tau^\star=t_P\) e \(\ell_P=ct_P\),

\[
R_B=\frac{\ell_P}{\beta},
\qquad
\boxed{q=\frac{\ell_P}{4\pi}},
\qquad
\boxed{E=\frac{E_P}{4\pi}} .
\]

Usando as constantes dos artefatos, o cálculo em [calcular_carga_nativa.py](calcular_carga_nativa.py) fornece

\[
R_B=1{,}3433753094\times10^{-33}\ \mathrm m
\simeq83{,}1165\,\ell_P,
\]

\[
q=1{,}2861750138\times10^{-36}\ \mathrm m,
\qquad
E\simeq1{,}55667\times10^8\ \mathrm J
\simeq9{,}71597\times10^{26}\ \mathrm{eV}.
\]

A pequena diferença relativa entre a avaliação direta e \(E_P/(4\pi)\) vem das aproximações independentes de \(t_P\), \(\hbar\), \(c\) e \(G\) usadas nos arquivos.

**O ramo nativo produz escala planckiana, não 1 eV.**

## 4. Escala temporal exigida para 1 eV

A condição \(E=1\,\mathrm{eV}\) exige

\[
\boxed{
\tau^\star=\frac{4\pi G(1\,\mathrm{eV})}{c^5}
=5{,}5488494964\times10^{-71}\ \mathrm s
=1{,}0292330321\times10^{-27}\,t_P .
}
\]

Esse valor não decorre da taxa nativa nem dos perfis encontrados. Escolhê-lo por causa do alvo seria ajuste. Portanto, a rota nativa não fecha a escala do neutrino; apenas desloca a pergunta para a origem independente de \(\tau^\star\).

## Veredito

**Provado condicionalmente:** sob a lei de fluxo e a identificação nativa da taxa, a carga do monopolo tem forma \(q=c\tau^\star/(4\pi)\), com cancelamento exato de β; no ramo nativo, \(q=\ell_P/(4\pi)\) e \(E_{\rm fluxo}=E_P/(4\pi)\).

**Não provado:** a compatibilidade entre \(\Gamma_B=\beta/\tau^\star\) e a lei canônica de dephasing; a identificação \(E_{\rm fluxo}=E_0\) da fórmula do neutrino; e uma escala temporal que produza 1 eV. O valor necessário é aproximadamente \(5,55\times10^{-71}\) s, cerca de \(10^{-27}t_P\), e exige uma lei física independente. A estacionariedade, o Nome e a condensação não fornecem essa escala temporal por si sós.
