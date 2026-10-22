# Revisão independente da fonte quártica e do habitante corrigido

09/09/2026. [DERIVED — análise matemática escrita desta sessão]. Esta nota examina `FONTE_QUARTICA_E_HABITANTE_CORRIGIDO.md` da frente complementar. Não representa aprovação em nome do operador ou de terceiros. O recibo de oito controles simbólicos foi lido; seu script não foi executado nesta revisão.

## 1. Variação métrica e identidade de Noether

Para L₄=b₁Q²+b₂W², Q=g^{μν}W_{μν} e W_{μν}=〈u_μ,u_ν〉, uma variação da métrica inversa com φ fixado fornece

\[
\delta L_4=(2b_1QW_{\mu\nu}+2b_2W_{\mu\rho}W_\nu{}^\rho)\delta g^{\mu\nu}.
\]

Como δμ_g=−μ_g g_{μν}δg^{μν}/2 e T=2μ_g⁻¹δS_m/δg⁻¹, segue precisamente

\[
T^{(4)}_{\mu\nu}=4b_1QW_{\mu\nu}+4b_2W_{\mu\rho}W_\nu{}^\rho-g_{\mu\nu}L_4.
\tag{1}
\]

Seu traço é 4b₁Q²+4b₂W²−4L₄=0 em quatro dimensões. Os sinais são compatíveis com assinatura (+---), ação gravitacional −(R−2Λ)/(2κ) e equação G+Λg=κT. A nulidade desse traço é clássica, com coeficientes constantes; não afirma uma identidade de traço quântica.

Na variação tangente de φ, δu_μ=D_μξ e

\[
\delta S_m=\int\mu_g\langle J^\mu,D_\mu\xi\rangle
=-\int\mu_g\langle D_\mu J^\mu,\xi\rangle,
\]
\[
J^\mu=c u^\mu+4b_1Q u^\mu+4b_2W^{\mu\nu}u_\nu.
\tag{2}
\]

Para difeomorfismo gerado por v, δg^{μν}=−2∇^{(μ}v^{ν)} e δφ=v^νu_ν. A integração por partes em δS_m=0 dá

\[
\nabla^\mu T_{\mu\nu}=\langle D_\mu J^\mu,u_\nu\rangle.
\tag{3}
\]

Assim também o sinal da identidade de Noether está correto. Não se inverte o sinal de (3) ao confundir D·J com a derivada funcional, que é −D·J.

## 2. Restrição ao mapa identidade

Para g=dr²−a²γ e φ(r,z)=z, temos W_{ij}=γ_{ij}, W_{rr}=W_{ri}=0, Q=−3/a² e W²=3/a⁴. Definindo B=3b₁+b₂, a corrente se torna

\[
J^r=0,\qquad J^i=\left(-\frac c{a^2}+\frac{4B}{a^4}\right)\gamma^{ij}u_j.
\tag{4}
\]

A divergência espacial de γ^{ij}u_j é a tensão intrínseca do mapa identidade de S³ e vale zero. O fator da corrente depende apenas de r e J^r=0; portanto D_μJ^μ=0, inclusive quando o fator espacial se anula. Isso verifica a equação sigma corrigida; não demonstra hiperbolicidade das perturbações nesse possível ponto degenerado.

Na componente espacial de (1), os três termos somam

\[
\frac1{a^2}(-12b_1-4b_2+9b_1+3b_2)\gamma_{ij}
=-\frac B{a^2}\gamma_{ij}.
\]

O resultado completo é ρ₄=−3B/a⁴, p₄=−B/a⁴. De fato ρ₄−3p₄=0 e ρ̇₄+3H(ρ₄+p₄)=0. Para B>0 essa contribuição à densidade é negativa na convenção escolhida; isso não contradiz a álgebra de pesos positivos, que não fixa os coeficientes finitos b₁,b₂ da ação.

## 3. As duas equações de Einstein e os pontos H=0

Nas convenções mantidas, as componentes geométricas são

\[
G_{rr}=3(H^2+a^{-2}),\qquad
G_{ij}=-(2a\ddot a+\dot a^2+1)\gamma_{ij}.
\]

Somando ρ₂=3c/(2a²), p₂=−c/(2a²), e fixando κc=4, Λ=3/4, a componente rr dá

\[
\dot a^2=1-\frac{a^2}{4}-\frac{\kappa B}{a^2}.
\tag{5}
\]

A componente espacial **independente** é

\[
2a\ddot a+\dot a^2+1+\Lambda a^2
=\frac{\kappa c}{2}+\frac{\kappa B}{a^2}.
\tag{6}
\]

Juntamente com (5), ela é equivalente a

\[
\ddot a=-\frac a4+\frac{\kappa B}{a^3},\qquad
\dot H=-\frac1{a^2}+\frac{2\kappa B}{a^4}.
\tag{7}
\]

Inserir (5) e (7) em (6) faz os dois lados valerem 2+κB/a². Essa verificação não divide por H ou por ȧ e é válida nos pontos de retorno enquanto a>0. Ela remove a possível lacuna de deduzir uma solução completa somente da restrição de Friedmann.

## 4. Solução explícita e endpoint

Se d=√(1−κB)>0, ponha y=a²=2+2d cos(r−r₀), num intervalo em que y>0. Então

\[
\dot y^2=4(1-\kappa B)-(y-2)^2,
\qquad \ddot y=2-y.
\tag{8}
\]

A primeira identidade equivale a (5). Usando ambas, obtemos diretamente

\[
\dot H=\frac{\ddot y}{2y}-\frac{\dot y^2}{2y^2}
=-\frac1y+\frac{2\kappa B}{y^2},
\]

logo também (6) está satisfeita. φ=id satisfaz (2); a ansatz resolve, portanto, o sistema clássico da ação truncada explicitada.

Para B=0 e r₀=0, y=4cos²(r/2), recuperando o habitante anterior no domínio correspondente. No endpoint κB=1, y=2 constante satisfaz (5) e (6): a componente espacial dá 1+Λy=5/2 e κc/2+κB/y=5/2. Não basta verificar apenas rr nesse endpoint; a conta acima confere a segunda componente também.

A frase sobre mínimo positivo pressupõe 0<κB≤1: para 0<κB<1, y_min=2−2√(1−κB)>0; para κB=1 a solução é estática. κB>1 não fornece solução real dessa restrição, e B<0 exige restringir o intervalo para manter y>0. A nota original já impõe 1−κB>0 antes de apresentar a família e separa o endpoint.

Para B pequeno, y=4cos²(r/2)−κB cos r+O(B²), uniformemente em compactos interiores. O mínimo da solução exata truncada não comprova validade da aproximação efetiva ali. A escala de curvatura pode fazer termos omitidos competirem com os retidos; a análise de estabilidade/Hadamard do fundo B=0 não se transporta sem recalcular a Hessiana.

## 5. Resultado e limites da revisão

Não encontrei falha nos sinais de T⁽⁴⁾, na corrente sigma, na conservação, nas duas componentes de Einstein, na solução explícita ou no endpoint estático. O enunciado é corretamente delimitado como solução **clássica da ação truncada**, com coeficientes lorentzianos finitos escolhidos. Ele não demonstra uma expectativa quântica total, equivalência direta de sinais euclidianos, estabilidade do fundo corrigido, resolução UV ou bounce físico controlado.

A representação por dados probabilísticos livres citada na seção final da nota original depende do adendo de representação da frente 067. Não rederivei esse teorema nesta revisão; as contas acima verificam o sistema ambiente e seu habitante. A ação escolhida, os valores finitos b₁,b₂ e a ampliação ambiente permanecem entradas.

O manifesto mede as fontes efetivamente lidas, o script citado pelo recibo e esta nota. Distingue os oito controles **lidos** de uma execução própria, que não ocorreu. Nenhum arquivo existente foi editado.
