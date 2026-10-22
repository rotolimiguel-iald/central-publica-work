# Transgressão BRST característica com referência métrica

10/09/2026. [DERIVED — demonstração escrita da raiz, aguardando revisão independente]. Apresentação métrica mínima, B0 inerte. Novos arquivos somente em Chatgpt; fontes congeladas preservadas; zero um.py, CAS ou Lean executados.

**Resultado:** as zeroformas de ghost4 associadas às formas características quadráticas de g possuem uma primitiva s natural na vizinhança formal g=g0+t h. É uma relação explícita na família de ciclos de densidade076. Não classifica H⁴(s), não remove Euler(g0) diagonal e não resolve a anomalia de grau total5.

## 1. Domínio e convenções

Use sg=L_cg, sc^μ=c^ρ∂ρc^μ, sg0=0. Os dx ficam à esquerda e anticomutam com c, ambos ímpares em grau total. D=s+d_H, D²=0; portanto s(dx^ρ f)=−dx^ρ sf.

No fibrado tangente, escreva
\[
\omega^\mu{}_\nu=\Gamma^\mu{}_{\nu\rho}(g)dx^\rho,\qquad
v^\mu{}_\nu=\nabla_\nu c^\mu
=\partial_\nu c^\mu+\Gamma^\mu{}_{\nu\rho}c^\rho.
\]
v é tensorial, não o ghost Lorentz cru. Defina
\[
\mathcal A=\omega+v,\qquad \mathcal F=D\mathcal A+\mathcal A^2.
\tag{1}
\]
É uma conexão de grau total1, sem novos campos físicos. Produtos matriciais usam coeficientes graduados. A convenção é
\[
R^\mu{}_{\nu\rho\sigma}
=\partial_\rho\Gamma^\mu{}_{\nu\sigma}
+\Gamma^\mu{}_{\lambda\rho}\Gamma^\lambda{}_{\nu\sigma}
-(\rho\leftrightarrow\sigma).
\]
A raiz métrica será somente uma série formal junto à identidade. Não se supõe raiz real para duas métricas Lorentzianas arbitrariamente afastadas. Cada coeficiente usa jatos finitos; nenhuma inversão de dφ ou de curvatura é admitida.

## 2. Curvatura total calculada

Temos
\[
\boxed{\mathcal F^\mu{}_\nu
=\tfrac12 R^\mu{}_{\nu\rho\sigma}
 (dx^\rho+c^\rho)(dx^\sigma+c^\sigma).}
\tag{2}
\]
O componente ghost0 é a definição de R. Para conferir os outros, podemos escolher coordenadas normais de g no ponto: os dois lados transformam tensorialmente sob mudanças FIXAS de coordenadas. A escolha é usada apenas para verificar a identidade em cada jato, sem impor sΓ=0. De fato, em Γ=0,
\[
s\Gamma^\mu{}_{\nu\rho}
=c^\sigma\partial_\sigma\Gamma^\mu{}_{\nu\rho}
+\partial_\nu\partial_\rho c^\mu.
\tag{3}
\]
A parte mista de F é
\[
s\omega+d_Hv+\omega v+v\omega
=dx^\rho(\partial_\rho v-s\Gamma_\rho+[\Gamma_\rho,v]).
\]
Em Γ=0, cancelam-se as segundas derivadas de c, deixando
\[
dx^\rho(\partial_\rho\Gamma^\mu{}_{\nu\sigma}
-\partial_\sigma\Gamma^\mu{}_{\nu\rho})c^\sigma
=dx^\rho R^\mu{}_{\nu\rho\sigma}c^\sigma.
\tag{4}
\]
Para ghost2, não se pode tratar a conexão em v como fixa:
\[
sv^\mu{}_\nu=-(v^2)^\mu{}_\nu
+c^\rho\partial_\rho\partial_\nu c^\mu
+(s\Gamma^\mu{}_{\nu\rho})c^\rho.
\]
O termo ∂ν∂ρc^μ de (3) anticommuta com c^ρ e cancela a segunda parcela. Assim
\[
sv+v^2=\partial_\sigma\Gamma^\mu{}_{\nu\rho}c^\sigma c^\rho
=\tfrac12R^\mu{}_{\nu\sigma\rho}c^\sigma c^\rho.
\tag{5}
\]
Isso prova (2), pois as duas parcelas mistas de seu lado direito somam (4).

## 3. Transporte que conserva a variação da métrica

O par (g,A) é compatível para D:
\[
Dg=\mathcal A^Tg+g\mathcal A.
\tag{6}
\]
Na parcela forma1, isso é Levi-Civita. Em ghost1, v^Tg+gv=L_cg; os termos Γc fornecem c^ρ∂ρg.

Ponha S=(g0⁻¹g)^{1/2} pela série binomial. S é g0-autoadjunta e g=S^Tg0S. Transporte
\[
\mathcal A_1=S\mathcal AS^{-1}-(DS)S^{-1},\qquad
\mathcal A_0=\bar\omega=\Gamma(g0)_\rho dx^\rho.
\tag{7}
\]
O termo sS NÃO pode ser omitido. (6) implica Dg0=A1^Tg0+g0A1. A0 satisfaz a mesma equação porque sg0=0. Consequentemente
\[
\Theta=\mathcal A_1-\mathcal A_0
\]
é tensorial, de grau total1, com valores em so(g0). Sua parcela ghost1 é
\[
k=S vS^{-1}-(sS)S^{-1}.
\tag{8}
\]
Ela é g0-antissimétrica, mas não introduz um ghost Lorentz independente. Como D²=0,
\[
\mathcal F_1=S\mathcal FS^{-1},\qquad
\mathcal F_0=d_H\bar\omega+\bar\omega^2=\bar R.
\tag{9}
\]
F0 não tem componente de ghost positivo.

Tudo cola no fibrado formal junto à diagonal de métricas. Uma mudança de frame escolhida por B0 é s-inerte; A0 e A1 recebem o mesmo termo afim e Θ transforma por conjugação. Naturalidade aqui transporta simultaneamente campos ativos e referência.

## 4. Transgressão no complexo total

Seja P um polinômio invariante quadrático em so(g0), por exemplo traço quadrático ou Euler, com normalização fixa. Para
\[
\mathcal A_u=\mathcal A_0+u\Theta,\qquad
\mathcal F_u=\mathcal F_0+uD_0\Theta+u^2\Theta^2,\qquad
D_0=D+[\mathcal A_0,\cdot],
\]
as conexões continuam métricas para g0. Invariância de P e Bianchi dão
\[
\partial_uP(\mathcal F_u,\mathcal F_u)
=2D P(\Theta,\mathcal F_u).
\]
Logo
\[
\boxed{\mathcal T_P=2\int_0^1P(\Theta,\mathcal F_u)du
=2P(\Theta,\mathcal F_0)+P(\Theta,D_0\Theta)
+\tfrac23P(\Theta,\Theta^2)}
\tag{10}
\]
satisfaz
\[
\boxed{D\mathcal T_P=P(\mathcal F_1,\mathcal F_1)
-P(\mathcal F_0,\mathcal F_0).}
\tag{11}
\]
A integral é polinomial em u; não resolve uma equação no espaço-tempo. No caso de Euler, P é paralelo nas conexões métricas utilizadas; sua métrica de índices não é congelada artificialmente durante a derivação.

[KNOWN — identidade de transgressão] [Chern–Simons, §3](https://math.mit.edu/juvitop/pastseminars/notes_2019_Fall/Chern-Simons.pdf) fornece o argumento por invariância/Bianchi. A conexão total graduada e sua aplicação à apresentação métrica foram verificadas aqui, não atribuídas à fonte como resultado específico da TGL.

## 5. Primitiva de ghost3 para a densidade característica

Escreva P_g(R,R)=ρ_P(g)dx⁰dx¹dx²dx³. Pelo transporte métrico e (2),
\[
P(\mathcal F_1,\mathcal F_1)
=\rho_P(g)\prod_{\mu=0}^3(dx^\mu+c^\mu).
\tag{12}
\]
É uma substituição algébrica entre geradores exteriores de grau total ímpar. Decomponha T_P=T_0³+T_1²+T_2¹+T_3⁰, com subscrito de forma e sobrescrito de ghost. A parcela de forma0 de (11) dá
\[
\boxed{sT_0^3=A_P,\qquad A_P=\rho_P(g)c^0c^1c^2c^3.}
\tag{13}
\]
A expressão explícita é
\[
\boxed{T_0^3=P(k,sk)+\tfrac23P(k,k^2)
=P(k,\mathcal F_{1,0}^{2})-\tfrac13P(k,k^2).}
\tag{14}
\]
F0 só tem forma2, logo não contribui a essa parcela. Euler e Pontryagin entram com suas normalizações respectivas.

(13) dá uma relação explícita na família A_L da nota076. Não diz que todas as densidades A_L sejam exatas. Não afirma sequer a não trivialidade de A_P em alguma álgebra anterior: isso demandaria outro teorema. Impede, porém, tratar esse representante como classe independente no domínio formal de chegada sem levar em conta (13).

## 6. A classe diagonal de fundo permanece

O componente de forma4/ghost0 de (11) continua sendo
\[
d_HT_3^0=P_g(R,R)-P_{g0}(\bar R,\bar R).
\tag{15}
\]
É a transgressão relativa ordinária074. Não há primitiva natural de Euler(g0) produzida aqui. A distinção é de grau: (13) trata ghost4/forma0, enquanto a obstrução diagonal tem ghost0/forma4.

O novo transporte conserva também suas componentes positivas de ghost. Omitir sS as alteraria. O termo de curvatura de fundo em (11) não é apagado; ele permite separar o ciclo total diagonal do ciclo de ghost4.

Esta nota tem grau total4, com transgressão de grau3. Não constrói uma primitiva de anomalia de grau total5. Seus resultados precisam ser usados com as relações e módulos corretos.

## 7. Completação por valência e limites

Com g=g0+t h e c=tC,
\[
s_t h=\mathcal L_Cg0+t\mathcal L_Ch,\qquad
s_tC=tC\cdot\partial C.
\]
Cada termo t^m h^m de S produz sob s_t uma soma cujos monômios continuam com peso t^E para E campos normalizados, contando C no lugar de h. Termos de curvatura de fundo contam E=0. Derivar um campo apenas muda seu jato; não muda a valência.

Assim cada monômio de S vS⁻¹ e de (sS)S⁻¹ tem peso t^E com E igual ao número de campos normalizados. k começa em uma perna ghost. O mesmo controle vale para s_tk: ele pode aumentar E, mas não introduz potências negativas ou contribuições infinitas a um coeficiente fixado.

A_P e T_0³ pertencem à completação por valência. Multiplicá-los por t^(2L−2) os coloca em R_L. Cada coeficiente possui ordem finita de jatos e operações finitas; não há ressoma a t numérico. A expressão usa somente a raiz formal e inversos métricos regulares junto a g0.

Esse controle algébrico não prova admissibilidade de toda uma família de normalizações causais: escala por aridade, independência funcional, inserções, realidade e contatos continuam a requerer demonstração. A naturalidade do representante não é suficiência de renormalização.

## 8. Custódia e estatuto

As fontes locais foram medidas antes/depois; o manifesto registra os pins. Esta prova aguarda revisão independente específica. Nenhuma revisão075 ou de outra nota076 é reaproveitada como sua aprovação.

[DERIVED — sujeito à revisão] Relação natural formal sT_0³=A_P para densidades características quadráticas, preservando B0 e a completação declarada.

[OPEN] Classificação completa de H³/H⁴, canais E2, primitiva admissível da anomalia, corrente/carga/QME, generalidade gravitacional e UV.
