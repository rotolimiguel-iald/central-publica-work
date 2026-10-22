# Habitante curvo categórico: matéria sigma, Einstein e área local

09/09/2026. Demonstração e análise próprias. **[DERIVED — prova escrita; este habitante completo não foi formalizado em Lean.]** Uma checagem simbólica independente calculou a conexão e Ricci diretamente na carta diagonal e verificou 14 grupos de identidades exatas; seu recibo é `VERIFICACAO_SIMBOLICA.json`. Essa checagem não é uma prova Lean. Nenhum original foi alterado e nenhum `um.py` foi executado ou importado.

**Resultado:** o candidato fornece uma solução local não plana do sistema Einstein–sigma, com métrica e fonte construídas da mesma família categórica P e com correspondência de área de equilíbrio para o protocolo Gibbs quadrático associado. Os sinais e fatores propostos conferem. Trata-se de um exemplo explícito de compatibilidade interna. A matéria com restrição sigma não é o setor de escalares livres independentes, e não herda sua realização Hadamard livre.

## 1. Os dados de probabilidade e o que é escolhido

[INPUT] Seja

\[
U=\{x\in\mathbb R^4:x_0,x_1,x_2,x_3>0,\quad x_0+x_1+x_2+x_3<1\}.
\]

Tome P_i=x_i para i=0,1,2,3 e P_4=1−Σ_{i<4}x_i. A soma é 1 em todo R⁴; os cinco pesos são positivos em U. O diferencial das quatro primeiras componentes é a identidade, de modo que o diferencial conjunto tem posto quatro. Selecione o rótulo 0: o relógio é dP₀=dx₀≠0.

A regra assinada escolhida é exatamente a definição `reflectedMetric` de `SelectedFisherLorentzMetric.lean`:

\[
F=\sum_{i=0}^4\frac{dP_i\otimes dP_i}{P_i},\qquad
g=\frac{2\,dP_0\otimes dP_0}{F^{-1}(dP_0,dP_0)}-F.
\]

Essa regra de leitura, o rótulo selecionado e a família P são entradas do modelo. Nenhum campo g ou T independente é fornecido à construção. Isso não significa que a normalização de P, sozinha, obrigue a natureza a escolher essa assinatura ou essa regra.

Escreva q=P₀, Q_a=P_a/(1−q), z_a=√Q_a, a=1,...,4. Então Σz_a²=1 e todos os z_a são positivos. A expansão direta do Fisher dá

\[
F=\frac{dq^2}{q(1-q)}+4(1-q)h_{S^3},\qquad
F^{-1}(dq,dq)=q(1-q).
\]

Logo, para r=2arcsin√q,

\[
q=\sin^2(r/2),\quad 0<r<\pi,\qquad
\boxed{g=dr^2-a(r)^2h_{S^3},\quad a(r)=2\cos(r/2)>0.}
\]

O domínio é difeomorfo a (0,π)×S³_+, onde S³_+ é o octante estritamente positivo da esfera. A reflexão é em relação ao covetor dP₀ normalizado pelo Fisher; atribuir sinais individualmente aos cinco termos dP_i²/P_i seria outra regra e não daria esta métrica.

## 2. Matéria construída dos mesmos pesos e restrição sigma

[INPUT] Escolhemos quatro campos reais e um parâmetro constante k>0 comum aos quatro canais:

\[
\phi_a=z_a=\sqrt{\frac{P_a}{1-P_0}},\qquad
w_a=d\phi_a,\qquad c=\frac{k}{\pi\cosh^2 k}>0.
\]

Os quatro acoplamentos iguais são parte deste exemplo. Não se está afirmando que acoplamentos arbitrários preservariam a mesma isotropia. A identidade da esfera implica

\[
\sum_a\phi_a^2=1,\qquad \sum_a\phi_a d\phi_a=0,\qquad
\sum_a d\phi_a\otimes d\phi_a=h_{S^3}.
\]

Adotamos a ação sigma com multiplicador escalar λ:

\[
S_m=\int\mu_g\left[\frac c2\sum_a g^{\mu\nu}\partial_\mu\phi_a\partial_\nu\phi_a
+\frac\lambda2\left(\sum_a\phi_a^2-1\right)\right]d^4x.
\]

A ação é [INPUT/POSTULATE], não uma consequência da igualdade ΣP_i=1. Variações de suporte compacto tratam g, φ e λ como variáveis independentes no sistema ambiente. A equação de λ é Σφ²=1; a equação de φ é

\[
-c\Box_g\phi_a+\lambda\phi_a=0.
\]

Pondo Q=Σ|dφ_a|²_g, a aplicação de □ à restrição dá Σφ_a□φ_a=−Q. Portanto λ=−cQ e a forma tangente à esfera é

\[
\Box_g\phi_a+Q\phi_a=0.
\]

Como os campos não dependem de r e as coordenadas da esfera unitária satisfazem Δ_{S³}z_a=−3z_a,

\[
Q=-\frac3{a^2},\qquad
\Box_g\phi_a=-a^{-2}\Delta_{S^3}\phi_a=\frac3{a^2}\phi_a,
\qquad \lambda=\frac{3c}{a^2}.
\]

A identidade Δ_{S³}z=−3z também decorre diretamente da segunda forma fundamental da esfera unitária: a Hessiana intrínseca de cada coordenada restrita é −z_a h, cujo traço em dimensão três é −3z_a. A checagem simbólica calculou □ individualmente em coordenadas esféricas e recuperou essas mesmas expressões.

**As ondas individuais não são zero.** Como φ_a>0 no domínio e a>0, □φ_a≠0 em cada canal. O novo mecanismo de conservação é o da soma com restrição, e não uma aplicação do teorema que exige `CovectorWaveOn` para cada canal.

## 3. Tensor da ação e conservação agregada

Na superfície da restrição, a contribuição métrica do termo λ(Σφ²−1)/2 se anula. A variação cinética, calculada na folha `ScalarMatterDensityVariation.lean`, dá exatamente

\[
T_{\mu\nu}=c\sum_a\left(\partial_\mu\phi_a\partial_\nu\phi_a
-\frac12g_{\mu\nu}|d\phi_a|_g^2\right).
\]

É a própria soma `finiteCovectorStressField`, com pesos 1 e acoplamentos c. Não se define uma ação retroativamente a partir de um T prescrito. Em coordenadas r e espaciais A,B,

\[
\boxed{T_{rr}=\frac{3c}{2a^2},\qquad T_{rA}=0,\qquad T_{AB}=-\frac c2h_{AB}.}
\]

A identidade fora das soluções para covetores exatos fornece

\[
\nabla^\mu T_{\mu\nu}=c\sum_a(\Box_g\phi_a)\partial_\nu\phi_a
=\frac{3c}{a^2}\sum_a\phi_a\partial_\nu\phi_a=0.
\]

Assim o requisito de conservação total do registro gravitacional é pago. A matéria tem ρ=3c/(2a²) e pressão p=−c/(2a²)=−ρ/3 no referencial comóvel; a equação ρ′+3(a′/a)(ρ+p)=0 é um controle adicional do sinal. Essa igualdade não transforma cada campo em uma solução livre.

## 4. Curvatura e equação de Einstein: conta explícita

Use a convenção

\[
R^\rho{}_{\sigma\mu\nu}=\partial_\mu\Gamma^\rho{}_{\nu\sigma}
-\partial_\nu\Gamma^\rho{}_{\mu\sigma}
+\Gamma^\rho{}_{\mu\lambda}\Gamma^\lambda{}_{\nu\sigma}
-\Gamma^\rho{}_{\nu\lambda}\Gamma^\lambda{}_{\mu\sigma},\qquad
R_{\sigma\nu}=R^\rho{}_{\sigma\rho\nu}.
\]

Esta é a ordem de índices lida em `connectionCurvatureJet` e `coordinateRicci` do kernel. Para a métrica acima, os símbolos mistos são

\[
\Gamma^r{}_{AB}=aa'h_{AB},\qquad
\Gamma^A{}_{rB}=\frac{a'}a\delta^A_B,\qquad
\Gamma^A{}_{BC}=\Gamma(h)^A{}_{BC}.
\]

Usando Ric(h)=2h, obtém-se R_rr=−3a″/a, R_rA=0 e R_AB=(2+aa″+2a′²)h_AB. Aqui

\[
a'=-\sin(r/2),\quad a''=-a/4,\quad a'^2=1-a^2/4.
\]

Consequentemente,

\[
R_{rr}=\frac34,\qquad R_{AB}=\left(4-\frac{3a^2}4\right)h_{AB},\qquad
R=3-\frac{12}{a^2},
\]

\[
\boxed{G_{rr}=\frac6{a^2}-\frac34,\qquad
G_{AB}=\left(-2+\frac{3a^2}4\right)h_{AB}.}
\]

Estas expressões também foram calculadas diretamente a partir da métrica diagonal

\[
\operatorname{diag}\left(1,-a^2,-a^2\sin^2\chi,
-a^2\sin^2\chi\sin^2\theta\right)
\]

na carta 0<χ,θ,ψ<π/2, sem inserir as fórmulas de Ricci como premissas na checagem simbólica.

Escolha as constantes do exemplo

\[
\boxed{\Lambda=\frac34,\qquad\kappa=\frac4c,\qquad
\eta=\frac{2\pi}{\kappa}=\frac{\pi c}{2}>0.}
\]

Então as componentes temporais e espaciais dão, respectivamente, 6/a² e −2h nos dois lados, logo

\[
\boxed{G[g[P]]+\Lambda g[P]=\kappa T[P].}
\]

O campo é não plano: R^A{}_{rAr}=−a″/a=1/4, sem soma. As constantes acima são escolhidas e identificadas dentro do exemplo; não são uma determinação experimental de G_N ou da constante cosmológica. A escala e as unidades físicas da métrica Fisher exigem calibração adicional. A ação de Einstein–Hilbert compatível com as convenções adotadas é −(2κ)⁻¹∫μ_g(R−2Λ); somada à ação sigma, ela tem este habitante como solução das equações ambientes.

## 5. Área real de tela e resposta Gibbs

Fixe um ponto p∈U e uma direção nula não zero ℓ. Escreva H=h_{S³}(ℓ_sp,ℓ_sp). A nulidade dá ℓ_r²=a²H. Como h é positiva e ℓ≠0, H>0. Calculando os dois tensores,

\[
\boxed{T(\ell,\ell)=cH>0,\qquad\operatorname{Ric}(\ell,\ell)=4H.}
\]

As telas não são definidas por uma área ajustada ao tensor. Escolha a congruência nula geodésica de equilíbrio que passa por (p,ℓ), com gradiente covariante zero em p, e transporte sua tela com Gram inicial −I₂. A área é a área induzida real `screenArea(screenGram(g(γ(t)),S(t)))`; o Gram inicial garante A(0)=1. Os teoremas existentes `localEquilibriumScreen` e `screen_area_quadratic_limit` dão, com a mesma convenção de Ricci,

\[
\boxed{\lim_{t\to0^-}\frac{A(t)-1}{t^2}
=-\frac12\operatorname{Ric}(\ell,\ell)=-2H.}
\]

O pacote de existência de tela usa um referencial lorentziano suave e sua inversa. Aqui esse requisito tem uma realização explícita em cartas: usando u=(z₁,z₂,z₃), z₄=√(1−|u|²)>0,

\[
h=I+\frac{uu^T}{z_4^2},\quad
E_h=I+\frac{uu^T}{z_4(1+z_4)},\quad
E_h^{-1}=I-\frac{uu^T}{1+z_4},\quad E_h^TE_h=h.
\]

O referencial E=diag(1,aE_h) é suave, invertível e satisfaz Eᵀdiag(1,−I₃)E=g em coordenadas (r,u). A mudança suave invertível para a carta original de probabilidades preserva esses requisitos. Assim a existência de tela de equilíbrio local não é uma hipótese de área escolhida ad hoc neste exemplo. A formalização de toda essa especialização ao habitante permanece trabalho posterior.

Para a matéria, em cada ponto e direção, use quatro sondas Gibbs mistas quadráticas, com parâmetro k comum e velocidades

\[
v_a=d\phi_a|_p(\ell),\qquad s_a(t)=v_a^2t^2.
\]

As identidades existentes de `MixedGibbsGravitationalBridge.lean` fornecem

\[
\lim_{t\to0^-}\frac{\Delta S_{\rm Gibbs}(t)}{t^2}
=-\frac{k}{\cosh^2k}\sum_a v_a^2
=-\pi c H=-\pi T(\ell,\ell).
\]

Portanto, com η=πc/2,

\[
\boxed{\lim_{t\to0^-}\frac{\Delta S_{\rm Gibbs}(t)-\eta[A(t)-1]}{t^2}=0.}
\]

O matching é para todas as direções nulas em cada ponto, com os mesmos campos e a mesma constante η. Reescalar ℓ reescala ambos os coeficientes quadraticamente; não introduz uma normalização oculta da direção. Como controle mais forte, a conta algébrica fora do cone dá

\[
-\pi c\sum_a[d\phi_a(\ell)]^2+\frac\eta2\operatorname{Ric}(\ell,\ell)
=\frac{3\pi c}{16}g(\ell,\ell).
\]

Assim o cancelamento é precisamente nulo, não uma igualdade para direções temporais ou espaciais arbitrárias. Verificar Einstein diretamente e depois verificar seu matching de área é uma prova de existência de um exemplo compatível. Não é uma derivação universal que imponha essa solução a preparações arbitrárias.

## 6. Mesma entrada P não significa mesma curva probabilística

O campo categórico P gera g[P] e φ[P]; seus diferenciais geram os parâmetros das sondas. Mas existem dois objetos probabilísticos:

1. Os cinco pesos P_i que definem Fisher e o relógio selecionado.
2. As probabilidades das quatro sondas Gibbs, construídas de dφ[P] e do relógio s_a=v_a²t².

O matching demonstrado utiliza a soma de entropias das sondas, equivalente à entropia do produto independente. Não é a entropia dos cinco pesos ao longo de P(x+tℓ) ou P(γ(t)). Esta última geralmente tem termo linear e já possui uma obstrução registrada no exemplo categórico original. Construir explicitamente um protocolo a partir de P resolve a compatibilidade matemática desse novo protocolo; não identifica automaticamente sua preparação física com a seleção categórica.

Se for exigida uma realização dos quatro qubits em uma torre canônica fixa, é preciso especificar quatro sítios com o perfil de base adequado, ou construir um perfil que os contenha. Um `SiteProfile` arbitrário não garante quatro sítios não traciais com o mesmo k. A realização matricial finita é imediata; seu encaixe em uma torre deve respeitar esse contrato.

## 7. Regra da cadeia para a ação dependente apenas de P

Neste exemplo g, φ e λ são todos funções de P, sendo g uma função também de dP. Considere a ação composta

\[
S_{\rm pullback}[P]=S[g[P],\phi[P],\lambda[P]],\qquad
\lambda[P]=\frac{3c}{4(1-P_0)}.
\]

Não se podem importar as equações de Euler–Lagrange independentes como se fossem equivalentes à equação de P. A primeira variação tem a forma

\[
\delta S_{\rm pullback}
=\langle E_g,Dg[P]\delta P\rangle
+\langle E_\phi,D\phi[P]\delta P\rangle
+\langle E_\lambda,D\lambda[P]\delta P\rangle,
\]

com as integrações e termos de fronteira usuais. Dg[P] contém derivadas da variação. Tomamos variações suaves de suporte compacto, normalizadas e suficientemente pequenas para permanecer no aberto positivo.

**A direção suficiente está paga:** calculamos neste habitante E_g=E_φ=E_λ=0 como campos. Logo todos os termos da cadeia se anulam e δS_pullback=0. Não é necessário ignorar ou postular a nulidade de Dg[P]. O recíproco pode falhar porque as variações induzidas por P não são todas as variações independentes de (g,φ,λ). Uma ação composta crítica não implica, em geral, cada equação ambiente separadamente.

## 8. Domínio, sinais globais e o setor quântico restante

O resultado foi construído em todo o aberto categórico U, equivalente ao octante positivo, e suas telas são locais. Não foi demonstrada completude geodésica. Tampouco o produto de um intervalo temporal com um octante espacial aberto deve ser tratado automaticamente como globalmente hiperbólico: a borda espacial retirada pode interromper curvas causais. Para trabalho local que exija hiperbologia global, podem-se escolher vizinhanças causais suficientemente pequenas dentro do domínio e demonstrar o contrato correspondente.

As fórmulas de Einstein–sigma se estendem geometricamente a (0,π)×S³ usando φ=z com sinais. Contudo, o único registro P_a=(1−q)z_a² perde os sinais e identifica pontos por reflexões independentes. Nas hipersuperfícies z_a=0 também falha a hipótese P_a>0 do contrato Fisher atual. Portanto a extensão da **geometria e dos campos assinados** ao S³ inteiro não é uma extensão já demonstrada da reconstrução a partir do mesmo registro positivo. Seriam necessárias cartas adicionais, dados de transição e informações de sinal; não os presumimos recuperados dos P_a.

Por fim, a realização quântica de uma fonte como diferença de valores esperados de estados Hadamard deslocados, na nota anterior, usava soluções de □φ_a=0 do campo livre minimal. Aqui □φ_a=3φ_a/a². O automorfismo de translação daquele CCR livre não preserva a equação de campo para este deslocamento. **Este habitante não herda essa realização quântica livre.** A ação sigma é outro setor, com restrição e interações, cuja quantização, observáveis e renormalização precisam ser tratados diretamente.

O que está demonstrado aqui é o habitante curvo compatível de P → métrica selecionada → campos sigma → fonte Gibbs → conservação agregada → Einstein → área local, pelas regras e escolhas explicitadas. Não há nesta nota uma prova de gravitação quantizada interagente, de controle de anomalias ou de completude UV; nenhum gate foi movido.
