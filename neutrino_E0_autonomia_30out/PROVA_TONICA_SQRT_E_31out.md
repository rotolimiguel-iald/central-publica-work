# A tônica √e e o fechamento algébrico de E₀

**Data:** 31/10/2026  
**Estatuto:** **[DERIVED condicional]** para a álgebra da tônica; **[INPUT do operador]** para “o tom é a nat”; **[OPEN]** para a leitura física da tônica pelo Hamiltoniano oculto.

## 1. O passo pinado

O operador fixou que **o tom é a nat**. Portanto, o meio-tom é a Meia-Nat:

\[
r=e^{-1/2}.
\]

Não é o semitom temperado \(2^{-1/12}\), nem a oitava \(\ln2\). A pedra candidata `LeiDoMeioTom` prova ainda que a oitava não é um número inteiro de meios-tons: \(1/2<\ln2<1\).

## 2. A tônica da pêntada

A tônica natural candidata é o volume mínimo da fronteira, já presente na cadeia canônica:

\[
\operatorname{Vol}_\partial^{\min}=e^{S_\partial}=e^{1/2}=\sqrt e .
\]

Na unidade da nota fundamental \(U_E=1\,\mathrm{eV}\), escreve-se

\[
E_{\rm pent}=\operatorname{Vol}_\partial^{\min}\,U_E
=\sqrt e\,\mathrm{eV}.
\]

**A atribuição dessa leitura ao Hamiltoniano oculto é a ponte física ainda a demonstrar.** O volume é adimensional; convertê-lo em energia exige a regra de leitura e a unidade, não apenas a fórmula do volume.

## 3. Fechamento exato

Pela regra \(E_0=rE_{\rm pent}\),

\[
\begin{aligned}
E_0
&=e^{-1/2}\left(\sqrt e\,\mathrm{eV}\right)\\
&=e^{-1/2}e^{1/2}\,\mathrm{eV}\\
&=\boxed{1\,\mathrm{eV}} .
\end{aligned}
\]

Logo,

\[
\begin{aligned}
m_2
&=\beta\,\operatorname{sen}(\pi/4)\,E_0\\
&=\alpha\sqrt e\,\frac{\sqrt2}{2}\,e^{-1/2}\left(\sqrt e\,\mathrm{eV}\right)\\
&=\alpha\frac{\sqrt2}{2}\left(\sqrt e\,\mathrm{eV}\right)\\
&=\beta\,\operatorname{sen}(\pi/4)\,(1\,\mathrm{eV})\\
&=\boxed{8{,}5074140999\ \mathrm{meV}} .
\end{aligned}
\]

A Meia-Nat entra em β e sai em E₀; o fator √e cancela no produto final. A pedra `LeiDoMeioTom` registra os teoremas correspondentes:

- `E0_determined_by_the_tonic`: dada a tônica, E₀ fica determinado;
- `massa_le_alpha`: \(m_2=\alpha\,\mathrm{sen}(\pi/4)\,E_{\rm pent}\);
- `tonic_sqrt_e_gives_one`: a tônica \(\sqrt e\) dá E₀ = 1;
- `one_needs_tonic_sqrt_e`: E₀ = 1 exige a tônica \(\sqrt e\).

Arquivo: `C:\IALD\Central de Patentes\work\e0_cadeia_31out\LeiDoMeioTom.lean`.

## 4. O que está provado e o que falta

**Provado algebricamente:** a escolha da tônica \(\sqrt e\,\mathrm{eV}\), com o passo \(e^{-1/2}\), produz exatamente 1 eV e a previsão de m₂. Não há ajuste de parâmetro nessa identidade, e nenhum dado de neutrino é usado.

**Ainda aberto fisicamente:** demonstrar que a leitura do Hamiltoniano oculto, regularizado e com unidade, atribui à tônica o valor \(\sqrt e\,\mathrm{eV}\) por lei, não por conveniência. Em particular:

1. qual é a leitura \(\mathcal R\) que transforma \(\operatorname{Vol}_\partial^{\min}\) em tônica energética;
2. por que a unidade fundamental é 1 eV, sem usar o dado de oscilação;
3. como a região e o Hamiltoniano regularizado produzem essa tônica sem cutoff ou normalização arbitrária;
4. como essa tônica se relaciona com \(E_{\rm fluxo}\) do monopolo, sem identificar automaticamente os dois símbolos E₀.

**Veredito:** a álgebra da tônica está fechada. A tônica natural é \(\sqrt e\,\mathrm{eV}\), não \(2^{1/12}\,\mathrm{eV}\). O trabalho restante é a prova física da leitura da tônica pelo Hamiltoniano oculto, não mais a álgebra de E₀.

## 5. Auditoria da conversão modular–energia

A conversão física existente é condicional: \(K=2\pi B\) e \(\varepsilon=T_U k\), com \(\delta Q=T_U\delta S_{\rm nat}\). Ela fornece calor proporcional à entropia, não \(U_Ee^S\). A normalização do relógio continua sendo entrada, e o vácuo tem

\[
k_\Omega=b_\Omega=\varepsilon_\Omega=0 .
\]

Logo, **a tônica não pode ser a energia do estado fundamental lida pelo Hamiltoniano modular**. Se vier dessa rota, terá de ser um gap, uma excitação ou uma normalização independente. Além disso, para qualquer \(\lambda>0\), \(U_E\mapsto\lambda U_E\) preserva a álgebra e muda \(E_0\) e m₂ pelo mesmo fator. A unidade de 1 eV é metrologicamente legítima, mas sua escolha como escala física continua `[INPUT]`, não consequência do volume adimensional.

O enunciado rigoroso final é: `HALF_NAT_EXPONENTIATION_CLOSED__E_PENT_SCALE_NORMALIZED__E0_CLOSURE_ALGEBRAIC_NOT_NEW_PHYSICS__ABSOLUTE_EV_SCALE_OPEN`. A prova física exige derivar independentemente \(U_E\), \(T_U\), \(\tau^\star\) ou a carga, sem usar o dado de oscilação.
