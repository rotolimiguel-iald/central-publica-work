# Disco de Euler — corte quântico e uma possível origem da escala

**Data:** 31/10/2026  
**Estatuto:** **[DERIVED condicional]** para a dinâmica e a álgebra do corte; **[OPEN]** para a existência do corte na trajetória, a identidade do disco e a ressonância residual.

## 1. O invariante e a parada

Seja \(K=\Omega^2E>0\), o invariante do disco. **Como hipótese adicional**, aplica-se a lei canônica TGL à precessão:

\[
\Gamma_\Omega E=\tfrac12\beta\tau^\star\Omega^2E
=\tfrac12\beta\tau^\star K ,
\]

que é constante. Nesse modelo, a energia decresce linearmente e o disco para em tempo finito. Antes da parada,

\[
\Omega^2=\frac KE
\]

cresce sem cota. A inscrição do zero absoluto aparece como frequência divergente, não como frequência finita residual.

No modelo físico de Moffatt, a dissipação não é constante: \(\Phi\propto\theta^{-2}\propto E^{-2}\), dando \(E\propto(t_f-t)^{1/3}\) e \(\Omega\propto(t_f-t)^{-1/6}\). O modelo linear acima é, portanto, uma dinâmica TGL condicional, não uma substituição da dinâmica experimental do disco de Euler.

## 2. O corte quântico e a escala condicional

Se o corte quântico \(\hbar\Omega=E\) ocorre durante a trajetória, então

\[
\hbar^2\frac KE=E^2
\quad\Longrightarrow\quad
\boxed{E_\star^3=\hbar^2K}.
\]

**Existência:** a fórmula só descreve um corte físico se \(0<E_\star<E_0\) e o modelo continuar válido até esse instante. A equivalência algébrica não demonstra que esse instante exista, nem que o modo de precessão permaneça como ressonância posterior.

A nota, caso a tônica seja o corte, seria

\[
U=e^{-1/2}E_\star
\quad\Longrightarrow\quad
\boxed{K=\frac{(e^{1/2}U)^3}{\hbar^2}} .
\]

A pedra `DiscoDeEuler.lean` registra `the_residual_resonance_iff` e `the_scale_is_the_invariant`, mas não fornece o operador residual nem prova a existência do corte.

## 3. O invariante exigido para 1 eV

Com \(U=1\,\mathrm{eV}\), a entrada necessária é

\[
\boxed{K=1{,}657374232266\times10^{12}\ \mathrm{J/s^2}} .
\]

A frequência instantânea no corte seria

\[
\Omega_\star=2{,}504848558735\times10^{15}\ \mathrm{s^{-1}},
\qquad
f_\star=3{,}986590298192\times10^{14}\ \mathrm{Hz}.
\]

Essas frequências são valores instantâneos, **não um autovalor residual demonstrado**.

No modelo físico de Moffatt, com energia total \(E=\tfrac32Mga\sin\theta\) e \(\Omega^2\sin\theta=4g/a\), o invariante é

\[
K=E\Omega^2=6Mg^2 .
\]

Para o invariante acima, a massa equivalente seria

\[
M=\frac{K}{6g^2}
=2{,}8722879808\times10^9\ \mathrm{kg},
\]

com \(g=9{,}80665\ \mathrm{m/s^2}\). Esse número não deriva o disco nem sua região; apenas mostra qual invariante a unidade exige. O cálculo do invariante está em [calcular_disco_euler.py](calcular_disco_euler.py), e a massa usa a correção \(6Mg^2\).

## 4. O que está provado e o que falta

**Provado condicionalmente:**

- sob a lei TGL, a perda é constante, a energia é linear e a parada ocorre em tempo finito;
- a frequência cresce sem cota antes da parada;
- se o corte ocorre, sua energia obedece \(E_\star^3=\hbar^2K\);
- o meio-tom fornece o valor da nota depois do corte.

**Ainda aberto:**

1. **Existência do corte:** é necessário \(0<E_\star<E_0\) e validade do modelo até ele.
2. **Disco da TGL:** massa, gravidade, região e origem de \(K\), sem usar a nota.
3. **Operador pós-parada:** Hamiltoniano residual com região, contorno e autovalor permanente; a parada por si só não seleciona suporte nem excitação.
4. **Persistência:** pode haver ringdown em vez de modo estacionário; a frequência instantânea não basta.
5. **Identificação com E₀:** a igualdade \(E_{\rm corte}=E_0\) precisa ser tipada, sem confundir os dois zeros nem os dois objetos de energia.

**Veredito:** a proposta é uma **candidata algébrica de mecanismo de escala**, não uma ressonância residual já estabelecida nem uma derivação física de 1 eV. O invariante parametriza a escala condicional, mas sua origem independente, a existência do corte e o modo pós-parada continuam abertos.
