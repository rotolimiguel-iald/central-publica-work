# Teste geométrico quântico do estado 067 por sua curvatura de Weyl

16/09/2026. [DERIVED — demonstração escrita, não Lean]. Esta nota testa uma ação geométrica **especificada**, utilizando a mesma ação Einstein–sigma e o mesmo estado linear 067. Não modifica a teoria para forçar uma igualdade modular e não classifica o centralizador que ainda não foi calculado.

## 1. A hipótese submetida ao teste

Seja \(\mathcal C^a{}_{bcd}=\delta C^a{}_{bcd}\) a perturbação linear do tensor de Weyl com um índice alto. O fundo FLRW da 067 tem Weyl zero. Consequentemente \(\mathcal C\) é invariante de gauge linear: \(\delta_v\mathcal C=\mathcal L_v\bar C=0\). É um campo local obtido por um operador diferencial de segunda ordem sobre h, e pode ser lido por testes físicos locais da construção anterior.

**[INPUT do teste, não conclusão sobre toda definição de Kξ]** A ação geométrica candidata é o pullback tensorial ordinário de \(\mathcal C^a{}_{bcd}\) pelo fluxo conforme do diamante, sem um peso conforme adicional, sem mistura de campos e sem transformação dos acoplamentos. Infinitesimalmente é \(\mathcal L_\xi\mathcal C\), com o sinal global do parâmetro indiferente para o teste de invariância. A escolha é a ação natural do tensor de Weyl (1,3), que é invariante sob reescala conforme da métrica; não supõe que a ação Einstein–sigma inteira tenha simetria conforme.

**Hipótese em operadores limitados.** Para cada teste tensorial real compacto q no diamante, use o unitário de Weyl \(W_{\mathcal C}(s q)=\exp[i s\mathcal C(q)]\), que pertence à álgebra regional porque \(\mathcal C\) é um campo linear local físico. A identificação proposta exige \(\sigma_t^\omega(W_{\mathcal C}(s q))=W_{\mathcal C}(s T_tq)\), onde Tt é o transporte dual do pullback tensorial, incluindo a transformação da densidade de teste. Na representação quase livre regular, as expectativas de produtos desses unitários são diferenciáveis nos parâmetros reais de teste; suas derivadas mistas recuperam a covariância de dois pontos e a identidade de Ward abaixo. Não é preciso presumir um domínio comum para os geradores não limitados.

Se essa transformação fosse o fluxo modular do estado regional, a invariância do estado pelo próprio fluxo modular exigiria, no diamante,

\[
\mathfrak W_\xi W_{\mathcal C}:=
(\mathcal L_\xi^{(x)}+\mathcal L_\xi^{(y)})W_{\mathcal C}(x,y)=0.
\tag{1}
\]

A nota prova que (1) é impossível para a classe de diamantes abaixo. Isso exclui esta identificação geométrica pura. **Não prova** que toda carga renormalizada \(\int\xi T\) aja dessa forma, nem que R aja não trivialmente no centralizador em particular.

## 2. Um modo físico fornece uma correlação exata

Usamos a convenção e a reconstrução TT da [fonte existente](../MODOS_TENSORIAIS_EXATOS_20260909/ACAO_TT_E_MODOS_EXATOS.md). O fundo é
\(g=a^2(d\eta^2-\gamma)\), \(a=2\operatorname{sech}\eta\), η>0, e

\[
t_n(\eta)=\frac{2\sqrt\kappa}{a(\eta)}f_{p_n}(\eta),\qquad
f_p(\eta)=\frac{(p-i\tanh\eta)e^{-ip\eta}}{\sqrt{2p(p^2+1)}},
\quad p_n^2=(n+1)^2+6,\quad n\ge2.
\]

Aqui t_n é a função de modo da perturbação métrica TT; n é o grau harmônico e não o raio do diamante. Diferenciando **a função reconstruída**, não apenas f,

\[
t_n(\eta)=\sqrt\kappa\,
\frac{(p_n\cosh\eta-i\sinh\eta)e^{-ip_n\eta}}
{\sqrt{2p_n(p_n^2+1)}},
\]
\[
\boxed{t_n'(\eta)=-i\sqrt{\frac{\kappa(p_n^2+1)}{2p_n}}
\cosh\eta\,e^{-ip_n\eta}.}
\tag{2}
\]

**Por que isto mede Weyl e não uma coordenada de gauge?** Pela invariância conforme de C(1,3), podemos calcular no cilindro \(\bar g=d\eta^2-(\gamma+t)\). Para uma perturbação TT, Codazzi e \(\delta\mathrm{Ric}_{0i}=0\) dão

\[
\mathcal C^\eta{}_{ikl}=	frac12(D_k t'_{il}-D_l t'_{ik}).
\]

O sinal acompanha a convenção de Riemann da fonte; invertê-lo não altera as correlações seguintes. Introduza a leitura auxiliar
\(B_{ij}=	frac12\epsilon_j{}^{kl}\mathcal C^\eta{}_{ikl}\), com epsilon da **esfera unitária**, independente de η. Sua parte TT é \(B^{TT}=\tfrac12\operatorname{curl}_\gamma t'\). Não se trata do campo magnético medido com normal unitária do espaço-tempo físico: manter C(1,3), epsilon_γ e o tempo conforme é essencial para não esconder fatores de a.

Para um harmônico real normalizado TT Y_n, tome
\(S_n=2\operatorname{curl}Y_n/\|\operatorname{curl}Y_n\|^2\).
O curl de um TT é TT e
\(\operatorname{curl}^2Y_n=(-\Delta_\gamma+3)Y_n=(n+1)^2Y_n\), portanto o denominador não zera. A identidade é cinemática na esfera; não importamos as equações de um fluido perfeito para o sigma. Curl é formalmente autoadjunto nos tensores TT reais da esfera sem bordo: integração por partes e a antissimetria de epsilon dão \(\langle U,\operatorname{curl}V\rangle=\langle\operatorname{curl}U,V\rangle\). Portanto \(\langle S_n,\tfrac12\operatorname{curl}Y_m\rangle=\delta_{nm}\) numa base ortonormal que respeita as degenerescências. Os setores S/V são ortogonais a esta leitura TT: sua contribuição tem traços e gradientes simetrizados, cuja contração integrada com um TT se anula por traço zero e divergência zero. A base pode ser escolhida ortonormal dentro de cada degenerescência, e curl preserva os subespaços de autovalor. Assim

\[
b_n(\eta):=\int_{S^3}S_n^{ij}B_{ij}(\eta,z)dV_\gamma
\quad\text{tem função de modo }t_n'(\eta).
\]

É uma leitura espacial **global** de um campo local; só será utilizada depois da continuação da identidade (1), não como se tivesse suporte no diamante. Sua correlação é suave nos dois tempos, pois seleciona um único modo:

\[
\boxed{W_n(\eta,\eta')=A_n\cosh\eta\cosh\eta'
e^{-ip_n(\eta-\eta')},\qquad
A_n=\frac{\hbar\kappa(p_n^2+1)}{2p_n}>0.}
\tag{3}
\]

Em particular,

\[
V_n(\eta)=A_n\cosh^2\eta,\qquad
\frac{d}{d\eta}\log V_n=2\tanh\eta\ne0.
\tag{4}
\]

A escolha dos modos da 067 fixa (3). Não há estatística observacional ou novo parâmetro ajustado neste número.

## 3. Da identidade local ao teste global, sem presumir localidade de TT

A [prova regional anterior](ESTADO_EINSTEIN_SIGMA_E_MODULAR_LOCAL.md), §4, estabelece o tubo holomorfo para o campo de uma partícula H. O operador diferencial local que leva H a \(\mathcal C\) tem coeficientes analíticos, pois \(\delta C(\mathcal L_vg)=0\); preserva a estimativa e a orientação analítica. Sua covariância tem frente de onda analítica contida em um cone de sinal oposto na primeira variável e de sinal positivo na segunda. Esse cone no produto não encontra seu negativo, salvo o zero que não pertence à frente de onda.

A derivação tensorial \(\mathfrak W_\xi\), com coeficientes analíticos, não amplia essa frente de onda. Pelo princípio de continuação única usado anteriormente (SVW, Proposição 5.3, aplicado ao fibrado no espaço conectado M×M), se (1) se anula em D×D, anula-se em todo M×M. Este é o passo que autoriza posteriormente a leitura em harmônicos na esfera inteira. Não extrapolamos um teste numérico global para um resultado local.

## 4. Dois centros antipodais obrigariam uma estacionariedade falsa

Escreva z∈S³⊂R⁴, escolha um centro espacial unitário n₀ e ponha h(z)=n₀·z. O vetor conforme do diamante de raio angular L e tempo central η₀ é

\[
\xi_{n_0}=\frac{\cos(\eta-\eta_0)h-\cos L}{\sin L}\partial_\eta
 +\frac{\sin(\eta-\eta_0)}{\sin L}\nabla_\gamma h.
\]

Tome 0<L<min(η₀,π), com L≠π/2 e o intervalo de trabalho contendo as pontas temporais. A expressão é um campo analítico global no interior; não é necessário que seu fluxo preserve M para todo parâmetro para testar a identidade infinitesimal.

O estado 067 é SO(4)-invariante: suas covariâncias somam cada degenerescência harmônica com a mesma função temporal, e a reconstrução respeita as rotações simultâneas do fundo sigma. Para o campo de Weyl, a rotação do alvo não acrescenta ação. Logo a identidade global (1) para n₀ implicaria a mesma identidade para −n₀ por uma rotação SO(4). Mas

\[
\boxed{\xi_{n_0}+\xi_{-n_0}=-2\cot L\,\partial_\eta.}
\tag{5}
\]

A derivada de Lie é linear no vetor. Como cot L≠0, somar as duas identidades imporia
\((\partial_\eta+\partial_{\eta'})W_{\mathcal C}=0\)
nas componentes coordenadas, porque o vetor constante ∂η não tem derivadas de componentes. A projeção TT global fixa usada em (3) comuta com essa derivada. Resultaria

\[
0=(\partial_\eta+\partial_{\eta'})W_n
=(\tanh\eta+\tanh\eta')W_n,
\]

contradizendo (3)–(4). Portanto a identidade (1) **não** vale em D×D. O argumento não cobre o raio excepcional L=π/2, no qual a combinação (5) se anula; não existe aqui uma conclusão por divisão por zero.

**Conclusão [DERIVED, específica]:** o fluxo modular da rede física linear, no estado 067 e nesses diamantes, não pode agir sobre C(1,3) somente pelo pullback tensorial conforme sem peso adicional. O fluxo modular existe pelo resultado anterior, mas essa apresentação geométrica pura não preserva a sua referência.

## 5. A hipótese de peso não pode ficar escondida

Há um controle que impede interpretar a conclusão como proibição de toda transformação modificada. Reescale apenas a leitura de modo por a: \(\widetilde b_n=a b_n\). Então

\[
\langle\widetilde b_n(\eta)\widetilde b_n(\eta')\rangle
=4A_n e^{-ip_n(\eta-\eta')},
\]

que é estacionária. Isso mostra que a objeção (4) depende da ação escolhida: um peso conforme adicional ou mistura de campos muda o teste. **A reescala não demonstra covariância sob ξ, KMS, igualdade modular, nem compatibilidade com todas as equações.** Também não é o pullback ordinário do mesmo tensor C(1,3). A carga Kξ deve determinar sua ação a partir do tensor de energia renormalizado; ela não pode ser escolhida depois só para anular este diagnóstico.

## 6. Relação com o resto e o centralizador

Se um candidato Kξ estiver definido na mesma implementação e realmente gerar a ação especificada no §1, a violação de (1) impede sua igualdade com Kω até constante: uma constante não muda a ação nem restaura a invariância do estado. A conclusão segura é a desigualdade dos fluxos em algum unitário de Weyl local. Se houver um domínio comum invariante no qual ambos os geradores implementem derivações, então a diferença dessas derivações também não pode se anular em todo esse domínio gerador; essa afirmação adicional depende do domínio, não presumido aqui. Não afirmamos que esse observável esteja no centralizador.

O número \(2\tanh\eta\) é o coeficiente logarítmico da **variação de uma correlação** para translação conforme global. Não é \(R_1\), uma taxa de Lindblad ou um coeficiente universal de gravidade. O parâmetro deste teste é o transporte infinitesimal, não uma expansão de acoplamento da teoria interagente.

Para saber a ação de R na imagem da esperança centralizante, ainda se precisa conhecer essa imagem física. A existência de ΔD não informa sozinha se seu centralizador é não escalar. A distinção é tratada no [critério espectral separado](CENTRALIZADOR_FOCK_E_ESPECTRO.md).

## Referências e verificações

- Fontes 067/TT e prova regional citadas acima, sem executar ou modificar originais.
- [Brechet–Hobson–Lasenby, equação (117)](https://arxiv.org/pdf/0909.5384): identidade geométrica curl-curl de TT. Não importamos sua dinâmica de fluido perfeito.
- [Harmônicos de S³](https://arxiv.org/html/1709.08020v1): setores, autovalores e ortogonalidade.
- [Strohmaier–Verch–Wollenberg](https://arxiv.org/pdf/math-ph/0202003): continuação única analítica e extensão para fibrados, aplicadas com as estimativas já demonstradas.

Os controles computacionais de (2)–(5) estão em `WEYL_WARD_CHECKS.json`. Não substituem os argumentos de suporte, gauge e analiticidade. O parecer independente desta nota, quando disponível, fica em arquivo próprio; não é antecipado por esta redação.


## Revisão independente incorporada

O parecer favorável, com alcance e leituras, está em REVISAO_INDEPENDENTE_WEYL.md. As precisões sobre unitários limitados, domínio de derivações e autoadjunticidade de curl foram incorporadas antes desta entrega. Não foi compilação Lean.
