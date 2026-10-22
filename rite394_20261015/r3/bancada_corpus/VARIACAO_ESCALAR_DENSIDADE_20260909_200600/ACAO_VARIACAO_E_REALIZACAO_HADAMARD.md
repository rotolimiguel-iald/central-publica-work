# A mesma fonte: ação escalar, variação métrica e realização Hadamard

09/09/2026. Nota própria, aditiva, produzida em Chatgpt. Estatutos e domínios abaixo fazem parte dos enunciados. Nenhum `um.py` foi executado ou importado; nenhum original foi editado.

## 1. Escopo e escolha da ação

[INPUT/POSTULATE] Escolhemos uma variedade lorentziana suave de dimensão quatro, assinatura (+---), com métrica não degenerada g, conexão de Levi-Civita, um conjunto finito J de campos escalares reais φ_j e constantes k_j>0. O acoplamento que a resposta Gibbs mista já fornece é

\[
c_j=\frac{k_j}{\pi\cosh^2 k_j}>0.
\]

A lei de resposta e o tensor reconstruído não selecionam, por si, uma ação única. Aqui a ação de matéria é uma hipótese adicional explícita, escolhida pela sua densidade cinética:

\[
\mu_g=\sqrt{|\det g|},\qquad
\mathcal L_m(g,d\phi)=\frac{\mu_g}{2}\sum_jc_jg^{ab}\partial_a\phi_j\partial_b\phi_j,
\qquad S_m=\int_M\mathcal L_m\,d^4x.
\]

Não definimos a ação a partir de um tensor de energia dado. A conta abaixo começa na inversa e no determinante da métrica. Fixados η>0 e κ=2π/η, a ação gravitacional mínima compatível com a convenção usada nesta nota é

\[
S_{\rm EH}=-\frac1{2\kappa}\int_M\mu_g(R-2\Lambda)\,d^4x.
\]

Usamos variações de suporte compacto no interior; alternativamente seriam necessários condições e termos de fronteira apropriados. A validade das integrais globais é hipótese: para extrair equações locais basta um domínio relativamente compacto contendo o suporte da variação. A ação de Einstein não é deduzida da TGL nesta nota.

## 2. Derivada local, calculada antes da interpretação física

[DERIVED; o subconjunto efetivamente compilado será identificado pelo recibo da folha `ScalarMatterDensityVariation.lean`] Para quaisquer matrizes reais g invertível e h, ponha g_t=g+th. A substituição da linha i pela linha h_i dá

\[
\left.\frac{d}{dt}\det g_t\right|_0
=\sum_i\det(g\text{ com linha }i\text{ substituída por }h_i)
=\det g\;\mathrm{tr}(hg^{-1}).
\]

A primeira igualdade é a derivada de uma aplicação multilinear contínua nas linhas. Para a segunda, escreva h=(hg^{-1})g e use multilinearidade: na substituição da linha i, todas as componentes de linhas distintas de i produzem duas linhas iguais e determinante zero. Essa prova não depende da assinatura e não presume a fórmula de Jacobi.

Como det g≠0, o sinal do determinante fica constante perto de t=0. Logo

\[
\delta\mu_g=\frac{\mu_g}{2}\mathrm{tr}(hg^{-1}),\qquad
\delta g^{-1}=-g^{-1}hg^{-1}.
\]

Fixe os covetores w_j enquanto varia a métrica, e escreva Q_j=w_j^Tg^{-1}w_j. As regras de produto e soma finita dão

\[
\delta\mathcal L_m
=\frac{\mu_g}{4}\mathrm{tr}(hg^{-1})\sum_jc_jQ_j
-\frac{\mu_g}{2}\sum_jc_j w_j^Tg^{-1}hg^{-1}w_j.
\]

Defina apenas agora o tensor obtido pela variação:

\[
T=\sum_j c_j\left(w_jw_j^T-\frac12Q_jg\right).
\]

Esta expressão coincide, ponto a ponto, com `finiteCovectorStressField g gInv w (fun _ => 1) c` quando gInv=g⁻¹. A identidade de traço \(\mathrm{tr}(Aww^T)=w^TAw\) fornece

\[
\boxed{\delta\mathcal L_m
=-\frac{\mu_g}{2}\mathrm{tr}\bigl((g^{-1}hg^{-1})T\bigr)
=-\frac{\mu_g}{2}\mathrm{tr}\bigl(hg^{-1}Tg^{-1}\bigr).}
\]

Para g simétrica, T e g⁻¹Tg⁻¹ também são simétricos. Portanto, se h é a variação de g_cov,

\[
\delta\mathcal L_m=-\frac{\mu_g}{2}T^{ab}h_{ab};
\quad \delta g^{ab}=-g^{ac}h_{cd}g^{db};
\quad \delta S_m=\frac12\int\mu_gT_{ab}\,\delta g^{ab}.
\]

A derivada é uma derivada real de t↦𝓛_m(g+th,w,c), e não uma igualdade que assume antecipadamente a variação desejada. A fórmula com traço é válida já para matrizes invertíveis arbitrárias; a interpretação como métrica lorentziana usa simetria e assinatura fixa.

## 3. Euler–Lagrange e a condição topológica dos potenciais

[DERIVED — prova escrita] Agora imponha w_j=dφ_j, com campos suaves globalmente definidos, e varie φ_j→φ_j+εψ_j com ψ_j suave de suporte compacto. A métrica fica fixa nesta variação. Por simetria de g⁻¹,

\[
\delta_\phi S_m
=\sum_jc_j\int\mu_g g^{ab}(\partial_a\phi_j)(\partial_b\psi_j)
=-\sum_jc_j\int\mu_g\psi_j\Box_g\phi_j.
\]

A segunda igualdade é integração por partes: \(\Box_g\phi=\mu_g^{-1}\partial_a(\mu_g g^{ab}\partial_b\phi)\). A contribuição de fronteira é zero pelo suporte compacto. O lema fundamental do cálculo das variações, aplicado separadamente a cada j e em cada carta, dá

\[
\delta_\phi S_m=0\ \text{para toda variação}\quad\Longleftrightarrow\quad
c_j\Box_g\phi_j=0\ \text{para todo }j.
\]

Como c_j>0, as equações são precisamente □_gφ_j=0. Para a conexão de Levi-Civita vale ainda a identidade fora das soluções

\[
\nabla^aT_{ab}=\sum_jc_j(\Box_g\phi_j)\partial_b\phi_j.
\]

Ela decorre da regra de Leibniz, ∇g=0 e da comutação das segundas derivadas de escalares. Nas soluções a fonte é conservada, pagando exatamente a condição `CovectorWaveOn` já usada na reconstrução; dφ é fechado pela simetria das segundas derivadas. A conservação isolada da soma não permite concluir individualmente todas as equações de onda, pois os termos podem cancelar. A ação e a liberdade de variar cada campo são o que fornecem cada equação.

[INPUT — alcance global] Um covetor fechado é gradiente local em vizinhanças contráteis. Para representar **todo** covetor reconstruído por um escalar real global, é necessário que sua classe em H¹_dR(M) seja zero; equivalentemente, seus períodos em laços devem desaparecer. Um domínio simplesmente conexo é uma condição suficiente usual. Não inferimos exatidão global apenas de `ClosedCovectorOn`. Potenciais locais podem diferir por constantes nos recobrimentos, mantendo T bem definido; isso ainda não constrói um campo escalar real global para a realização quântica abaixo. Campos compactos ou setores topológicos seriam extensões distintas.

[DERIVED] Com a variação de Einstein–Hilbert na convenção acima, δ(S_EH+S_m)=0 na métrica dá

\[
G_{ab}+\Lambda g_{ab}=\kappa T_{ab}.
\]

Isso mostra compatibilidade variacional da equação reconstruída com a ação adotada. Não transforma a correspondência área–resposta, que permanece hipótese da reconstrução, em consequência desta ação. A integral de Einstein–Hilbert e o lema fundamental não são declarados Lean por esta nota.

## 4. Uma realização quântica concreta da mesma fonte

[INPUT] Fixe agora um espaço-tempo globalmente hiperbólico (M,g) e campos reais globais suaves φ_j que resolvam □_gφ_j=0. Ponha σ_j=√c_j φ_j. Considere a álgebra CCR de J campos escalares livres, sem massa e minimamente acoplados, e um estado de referência centrado Hadamard ω₀. Fixe uma única prescrição local de renormalização do tensor de energia para comparar os estados.

[DERIVED] A translação por solução clássica define um automorfismo da álgebra de campos:

\[
\alpha_\sigma(\widehat\sigma_j(f))
=\widehat\sigma_j(f)+\left(\int_M\sigma_jf\,d\mu_g\right)\mathbf1.
\]

A equação de campo é preservada porque σ_j é solução e os testes têm suporte compacto. Os comutadores são preservados porque a parcela adicionada é central, e a involução é preservada porque σ_j é real. A inversa é α_{−σ}. Consequentemente ω_σ=ω₀∘α_σ é normalizado e positivo:

\[
\omega_\sigma(A^*A)=\omega_0(\alpha_\sigma(A)^*\alpha_\sigma(A))\ge0.
\]

Não se pressupõe que essa translação seja implementável por um operador unitário global na representação escolhida; essa propriedade depende do espaço de uma partícula e da solução. O argumento algébrico continua válido sem tal implementador.

Como ω₀ é centrado, a função de dois pontos de cada campo satisfaz

\[
W_{\sigma,j}(x,y)-W_{0,j}(x,y)=\sigma_j(x)\sigma_j(y).
\]

A diferença é suave. Portanto o comportamento singular Hadamard permanece o mesmo. Ao aplicar a **mesma** operação de separação de pontos e tomar a coincidência x=y, a subtração Hadamard e todos os termos geométricos independentes do estado se cancelam. Para o tensor minimal sem massa, isso dá exatamente

\[
\boxed{\langle\widehat T_{ab}\rangle_{\omega_\sigma}^{\rm ren}
-\langle\widehat T_{ab}\rangle_{\omega_0}^{\rm ren}
=\sum_j\left(\nabla_a\sigma_j\nabla_b\sigma_j-
\frac12g_{ab}|d\sigma_j|_g^2\right)
=T_{ab}[\phi,c].}
\]

[DERIVED/KNOWN] O cancelamento mostra que a fonte construída tem uma realização quântica exata como **diferença de valores esperados renormalizados**, no regime livre em fundo fixo. O formalismo local de renormalização e de conservação usado aqui é o de [Hollands e Wald, *Conservation of the stress tensor in perturbative interacting quantum field theory in curved spacetimes*](https://arxiv.org/abs/gr-qc/0404074). A nota usa o caso minimal livre; não transfere automaticamente os resultados para a métrica quantizada. A identidade da translação e da diferença suave foi deduzida acima.

Essa realização não identifica a álgebra CCR com o fator Gibbs da torre, nem identifica estados por terem o mesmo tensor ou coeficiente de resposta. Construir tal identificação seria outro teorema. A igualdade vale para o incremento relativo: o valor de referência ⟨T̂⟩_ω₀ pode ser diferente de zero e não é, em geral, proporcional a g. Portanto não pode ser omitido ou absorvido em Λ indiscriminadamente. O fato de o incremento clássico ter energia nula positiva não prova uma condição de energia positiva para todos os valores esperados quânticos absolutos.

## 5. O avanço e o que ele ainda não conclui

O elo acrescentado é específico: a mesma fonte finita que a resposta mista reconstrói é obtida por variação de uma ação cinética explícita; quando os covetores são gradientes de soluções globais, a fonte também é um incremento exato do tensor de energia de um estado Hadamard deslocado.

[OPEN] O setor gravitacional quantizado interagente, o controle de BRST/BV quântico no modelo acoplado, uma identificação entre seus observáveis e os da torre e uma construção UV permanecem tarefas adicionais. A quantização perturbativa de gravitação pode ser organizada no formalismo local/BV de [Brunetti, Fredenhagen e Rejzner](https://arxiv.org/html/1306.1058v4), cujo artigo trata diretamente de gravidade pura; a extensão a esta matéria não é adquirida simplesmente por citá-lo. Renormalização perturbativa como EFT não é uma prova de completude UV.

[OPEN] A equação semiclássica exigiria levar em conta a referência e as ambiguidades locais de renormalização, além do incremento acima. Nada nesta nota confirma empiricamente a teoria nem move seu gate.
