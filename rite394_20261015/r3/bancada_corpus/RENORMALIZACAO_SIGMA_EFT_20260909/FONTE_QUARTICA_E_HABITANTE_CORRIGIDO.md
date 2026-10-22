# Fonte quartica e solução clássica da ação efetiva truncada

[DERIVED — demonstração escrita] Os operadores sigma de quatro derivadas calculados na nota de um laço produzem uma fonte geométrica explícita. Este adendo deriva a fonte e um habitante curvo da ação clássica truncada que a inclui. Os coeficientes finitos são entradas; o resultado não é a equação semiclassica completa, que também recebe termos não locais, contribuições métricas e dependência do estado.

## 1. Ação lorentziana e coeficientes distintos dos euclidianos

Use assinatura +--- e as convenções Einstein–sigma das entregas 066/067:

\[
S=-\frac1{2\kappa}\int\mu_g(R-2\Lambda)
+\int\mu_g\left(\frac c2 Q+b_1 Q^2+b_2 W_{\mu\nu}W^{\mu\nu}\right),
\quad \phi:M\to S^3.
\]

Q=g^{µν}W_{µν} e W_{µν}=〈∂µφ,∂νφ〉. Os números reais b₁,b₂ são os coeficientes **lorentzianos** renormalizados da ação escolhida. A nota anterior fixou um sinal euclidiano para o cálculo de divergências; não se igualam esses coeficientes sem realizar a conversão e escolher condições finitas de renormalização. Aqui c>0, κc=4 e Λ=3/4, nas unidades geométricas do habitante anterior.

Defina L₄=b₁Q²+b₂W². Variação em g^{µν}, com T_{µν}=2µ_g⁻¹δS_m/δg^{µν}, dá

\[
\boxed{T^{(4)}_{\mu\nu}
=4b_1QW_{\mu\nu}+4b_2W_{\mu\rho}W_\nu{}^\rho-g_{\mu\nu}L_4.}
\tag{1.1}
\]

Foram usadas δQ=W_{µν}δg^{µν}, δW²=2W_{µρ}W_ν{}^ρδg^{µν} e δµ_g=−µ_g g_{µν}δg^{µν}/2. Em quatro dimensões o traço de (1.1) é zero. Isso é uma identidade clássica desses termos homogêneos de quatro derivadas; não é uma afirmação de ausência de anomalia de traço quântica.

A variação sigma tangente tem corrente

\[
J^\mu=c u^\mu+4b_1Q u^\mu+4b_2W^{\mu\nu}u_\nu,
\qquad u_\mu=\partial_\mu\phi,
\]

e equação intrínseca DµJµ=0. A identidade de Noether sob difeomorfismos dá

\[
\nabla^\mu T_{\mu\nu}=\langle D_\mu J^\mu,u_\nu\rangle,
\]

com o tensor total sigma, incluindo o termo c. Logo a conservação não é imposta separadamente: segue da equação sigma corrigida. As constantes b₁,b₂ são mantidas fixas nesse cálculo; fazê-las depender de uma coordenada exigiria variar também essa entrada.

## 2. No mapa identidade de S³ a fonte tem forma de radiação

Considere g=dr²−a(r)²γ_{S³} e φ(r,z)=z. Então W_{rr}=W_{ri}=0, W_{ij}=γ_{ij}, Q=−3/a² e W²=3/a⁴. O mapa continua satisfazendo a equação sigma intrínseca, inclusive com os termos quarticos: sua corrente temporal é zero e a parte espacial é uma função de r multiplicando a corrente do mapa identidade harmônico.

Ponha B=3b₁+b₂. Substituir em (1.1) dá

\[
\boxed{\rho_4=T^{(4)}_{rr}=-\frac{3B}{a^4},\qquad
T^{(4)}_{ij}=-\frac{B}{a^2}\gamma_{ij},\qquad
p_4=-\frac{B}{a^4}=\frac{\rho_4}{3}.}
\tag{2.1}
\]

Por isso ρ̇₄+3H(ρ₄+p₄)=ρ̇₄+4Hρ₄=0. A fonte possui a dependência a⁻⁴; seu sinal depende dos coeficientes adotados e não é fixado pela positividade dos pesos do registro.

O termo de duas derivadas tem ρ₂=3c/(2a²), p₂=−c/(2a²). Somando as fontes, a equação rr de Einstein na convenção usada é

\[
3(H^2+a^{-2})+\Lambda
=\kappa\left(\frac{3c}{2a^2}-\frac{3B}{a^4}\right).
\]

Com os acoplamentos acima,

\[
\boxed{\dot a^2=1-\frac{a^2}{4}-\frac{\kappa B}{a^2},\qquad
\dot H=-a^{-2}+2\kappa B a^{-4}.}
\tag{2.2}
\]

A segunda equação segue da primeira onde H≠0 e também da equação espacial independente. Não se usa divisão por H para estender a conclusão a um ponto em que ele se anule.

## 3. Solução exata da ação truncada

Defina y=a². A primeira equação de (2.2) equivale a

\[
\dot y^2=4y-y^2-4\kappa B
=4(1-\kappa B)-(y-2)^2.
\]

Se 1−κB>0, tome d=√(1−κB). Uma família explícita é

\[
\boxed{a_B(r)^2=2+2d\cos(r-r_0),}
\tag{3.1}
\]

restrita a qualquer intervalo em que o lado direito seja positivo. Diferenciação fornece ÿ=−(y−2) e verifica também a segunda equação de (2.2), sem depender apenas da restrição rr. Juntamente com a equação sigma e as componentes isotrópicas da fonte, isso verifica o sistema clássico completo dessa ansatz para a ação truncada adotada.

B=0 e r₀=0 recuperam a²=4cos²(r/2). Para B=1/κ há também a solução constante a²=2, verificada diretamente; ela não pertence ao domínio H≠0 usado para a fixação de calibre e para o estado quântico de 067. Não se aplica esse estado a ela por continuidade nominal.

Para κB pequeno,

\[
a_B^2=4\cos^2(r/2)-\kappa B\cos r+O(B^2)
\quad(r_0=0).
\]

Essa expansão é uniforme em compactos interiores do domínio anterior. Perto de a=0, o termo relativo κB/a² pode deixar de ser pequeno. Se B>0, a solução exata truncada admite um mínimo positivo; esse fato algébrico **não** demonstra uma resolução física da singularidade ou uma conclusão UV. Precisamente nessa região, termos omitidos da ação efetiva e correções não locais podem ser igualmente importantes.

Se b₁,b₂ forem de ordem ℏ, a deformação calculada fornece a parte da resposta clássica associada a esses termos locais na primeira ordem formal. O valor renormalizado do tensor quântico total depende também da covariância escolhida e das demais contribuições. Essa resposta não pode ser chamada de solução semiclassica completa sem calculá-las.

## 4. Ligação com o registro e alcance do resultado

Na classe probabilística livre, W, Q e T⁽⁴⁾ são funções diferenciais dos mesmos campos reconstruídos (g[P],φ[P]). Portanto o termo local novo não precisa receber um tensor de fonte independente: (1.1) o fornece explicitamente a partir dos dados e dos coeficientes da ação. A representação livre local já permite representar cada habitante (3.1) no seu domínio, com relógio e residual admissíveis. Uma realização global exige a construção correspondente; não é presumida a partir desse fato local.

Os valores finitos b₁,b₂, a escolha física da ação e a correspondência entre dados e modelo continuam [INPUT/POSTULATE]. A nova fonte e (3.1) são [DERIVED] dentro desse contrato. A detecção de um coeficiente divergente não seleciona os valores finitos.

O estado de Hadamard de 067 foi construído para B=0. A Hessiana e as frequências mudam quando B muda; a expressão antiga dos modos não é reutilizada como prova de um estado no novo fundo. A análise de calibre, estabilidade e quantização desse habitante corrigido é uma obrigação própria quando esse alcance for requerido.

O recibo simbólico associado verifica contrações, conservação e as equações da ansatz. A prova permanece escrita, sem nova compilação Lean. Nenhum original foi alterado e nenhum `um.py` foi executado.
