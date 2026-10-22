# Weyl elétrico: o peso que corrige a leitura magnética não corrige o tensor inteiro

16/09/2026. [DERIVED — demonstração escrita, inicialmente submetida a revisão independente; não Lean]. Usa o mesmo estado linear 067, fundo e modos da [nota anterior](TESTE_GEOMETRICO_WEYL_ESTADO_067.md). Não muda a ação para obter uma simetria.

## Hipótese ampliada

Considere a ação infinitesimal, sobre todo o Weyl linear C(1,3),

\[
D_\xi\mathcal C=\mathcal L_\xi\mathcal C+w\psi_g(\xi)\mathcal C,
\quad \mathcal L_\xi g=2\psi_g(\xi)g,
\quad w\in\mathbb R\text{ constante}.
\]

É um único peso escalar para o tensor, sem misturas com outros campos ou termos diferenciais extras. Como antes, a hipótese modular é sobre os unitários de Weyl dos campos suavizados, usando o transporte dual dos testes. A regularidade da representação quase livre fornece a Ward de dois pontos. Não se presume um domínio comum de Hamiltonianos ilimitados.

A continuação analítica e SO(4) usadas na nota anterior também se aplicam a esse operador diferencial: ψg é analítica e a atribuição ξ↦Dξ é linear. Nos centros antipodais e raios L≠π/2, a soma exige invariância por

\[
D_{\partial_\eta}=\partial_\eta-w\tanh\eta,
\]

pois a=2 sech η e ψg(∂η)=a'/a=−tanh η. Assim, qualquer projeção espacial fixa de componentes do mesmo tensor, com variância V(η), deveria satisfazer

\[
V'(\eta)=2w\tanh\eta\,V(\eta). \tag{1}
\]

O modo magnético da nota anterior tem V_B=A cosh²η. Para η>0, (1) **obriga w=1**. Isso ainda é uma condição necessária; o cálculo seguinte a testa na componente elétrica do mesmo campo.

## Weyl elétrico calculado antes de usar as equações de movimento

Adote uma convenção de Riemann na qual o cilindro ḡ=dη²−γ tem Ric_ij=2γ_ij e R=−6. Uma convenção oposta multiplica todas as componentes de Weyl por −1, sem alterar as variâncias. Para a perturbação ḡ_ij=−γ_ij−t_ij, com t espacial TT, a variação de Ricci da esfera é

\[
\delta\mathrm{Ric}^{(3)}_{ij}=\tfrac12(-\Delta_\gamma+6)t_{ij}.
\]

Esta identidade segue da fórmula de variação de Ricci e dos comutadores de derivadas em curvatura seccional +1, com divergência e traço de t nulos. No cilindro, os termos temporais dão

\[
\delta R_{0i0j}=\tfrac12t''_{ij},\quad
\delta\mathrm{Ric}_{ij}=\tfrac12[t''+(-\Delta_\gamma+6)t]_{ij},
\quad\delta\mathrm{Ric}_{00}=0,\quad\delta R=0.
\]

Substitua na decomposição em quatro dimensões

\[
C_{0i0j}=R_{0i0j}-\tfrac12(g_{00}\mathrm{Ric}_{ij}+g_{ij}\mathrm{Ric}_{00})
+\tfrac R6g_{00}g_{ij}.
\]

A variação do último termo é +t_ij, porque R̄=−6 e δg_ij=−t_ij. Portanto

\[
\boxed{E_{ij}:=\mathcal C^\eta{}_{i\eta j}
=\tfrac14(t''+\Delta_\gamma t-2t)_{ij}.} \tag{2}
\]

A invariância conforme de C(1,3) torna (2) a componente coordenada do Weyl físico, sem acrescentar fatores de a. Não é a componente medida num referencial ortonormal móvel. A contração com um harmônico espacial TT normalizado isola o modo: partes escalares/vetoriais são traços ou gradientes simetrizados e se anulam por integração por partes. Como antes, essa leitura global só é usada depois da continuação da Ward local.

## A dispersão existente fornece a obstrução

Fixe n≥2 e escreva

\[
\lambda=(n+1)^2-3,\quad p^2=\lambda+9,\quad
c_n=\frac{\sqrt\kappa}{\sqrt{2p(p^2+1)}}.
\]

O modo TT existente é t_n=c_n(p coshη−i sinhη)e^(−ipη). Diferenciando,

\[
t_n''=-c_n(p^2+1)(p\cosh\eta+i\sinh\eta)e^{-ip\eta}.
\]

Aplicar (2), com Δγ t_n=−λt_n, dá exatamente

\[
\boxed{e_n(\eta)=\frac{c_n}{2}
[-p(\lambda+6)\cosh\eta-4i\sinh\eta]e^{-ip\eta}.} \tag{3}
\]

O número 4 resulta da dispersão p²=λ+9 e do operador geométrico (2), no fundo e acoplamentos já fixados da 067. Não foi identificado com β, com um coeficiente modular universal ou com uma taxa.

Para w=1, (1) equivaleria a estacionariedade da leitura reescalada a e_n. Mas sua variância é

\[
\boxed{V_{aE}(\eta)=\hbar c_n^2
[p^2(\lambda+6)^2+16\tanh^2\eta],} \tag{4}
\]

\[
\frac{dV_{aE}}{d\eta}=32\hbar c_n^2\tanh\eta\operatorname{sech}^2\eta>0
\qquad(\eta>0). \tag{5}
\]

Consequentemente **não existe peso escalar constante w que torne a ação acima o fluxo modular** no estado 067 e nos diamantes especificados. A componente magnética impõe w=1; a elétrica recusa w=1. É uma demonstração por condições necessárias de invariância, sem pretender diagonalizar δD.

Uma forma equivalente, que elimina qualquer reescala temporal escalar comum às duas leituras, é

\[
\frac{V_E}{V_B}=
\frac{p^2(\lambda+6)^2+16\tanh^2\eta}{4(p^2+1)^2},
\quad
\frac{d}{d\eta}\frac{V_E}{V_B}=
\frac{8\tanh\eta\operatorname{sech}^2\eta}{(p^2+1)^2}>0. \tag{6}
\]

Multiplicar ambos os modos pelo mesmo fator temporal não nulo não altera essa razão. Não se estende o argumento a reescalas diferentes por componente ou a misturas de campos sem conferir sua lei de transformação.

## O alcance que permanece aberto

- O caso L=π/2 não é decidido pela soma antipodal utilizada.
- A carga física renormalizada Kξ ainda precisa ter sua ação determinada. O no-go exclui a família explícita Lie+wψ, não toda ação que se possa construir com a mesma teoria.
- Não foi calculado R1 nem encontrado um observável do centralizador que detecte R. A nota anterior distingue essas perguntas.
- Não se transporta o resultado da teoria linear para uma QFT interagente UV completa sem construção adicional.

**Correção ao lado da entrega anterior:** permanece verdadeiro que a b_n é estacionário. Isso era somente um controle contra a exclusão indiscriminada de pesos. O teste elétrico demonstra agora que o mesmo peso não restaura a invariância do Weyl inteiro. Não há contradição entre os dois resultados.

As identidades novas são derivadas aqui da geometria e dos [modos TT existentes](../MODOS_TENSORIAIS_EXATOS_20260909/ACAO_TT_E_MODOS_EXATOS.md). A continuação analítica e o contrato regional estão na [prova regional](ESTADO_EINSTEIN_SIGMA_E_MODULAR_LOCAL.md). Controles e parecer desta etapa são registrados separadamente; controles numéricos não substituem o cálculo de curvatura.


## Parecer e controles recebidos

A derivação do Weyl elétrico e a exclusão do peso escalar receberam conferência independente favorável de Goodall. O revisor explicitou a variação do fator métrico no termo Rg/6, confirmou o sinal na convenção da fonte e a necessidade de projetar TT somente depois da continuação e soma antipodal. O relato integral de escopo está em REVISAO_INDEPENDENTE_PESO_CONFORME.md. Isso é revisão escrita, não Lean.

O script verify_electric_weyl.py e ELECTRIC_WEYL_CHECKS.json registram controles de nove pares modo/tempo, incluindo três linearizações da curvatura exata de Bianchi IX para o harmônico homogêneo n=2. Nos outros modos, verificam derivadas temporais, normalização e razão de variâncias; não fingem testar uma geometria não linear que não foi implementada.
