# Existência da dinâmica extensiva na álgebra quase local canônica

Demonstração matemática escrita para `BondInteractionData` — 9 de setembro de 2026.

[DERIVED + KNOWN] O contrato canônico de interação entre vizinhos, com termos autoadjuntos uniformemente limitados, determina uma dinâmica em todo tempo no fecho C* quase local. O resultado permanece válido com o fundo modular do perfil, mesmo quando seus geradores de sítio não têm norma uniformemente limitada. A prova analítica abaixo é distinta de sua formalização: o limite infinito não é apresentado como teorema Lean compilado.

A conclusão inclui automorfismos da álgebra C* e existência de estados KMS nessa álgebra. Não inclui extensão normal universal ao fator original, escolha de um estado físico, limite ultravioleta ou fechamento da gravidade quântica. A seção 9 demonstra uma obstrução concreta à extensão normal.

## 1. Contrato e enunciado

Fixe um `SiteProfile P`, com 0 < P.w(j) < 1 em cada sítio. Escreva H = `TowerHilbert P` e AΛ = `chainLocalAlgebra P Λ` para conjuntos finitos Λ. Todos os operadores estão no mesmo B(H). Para ΛR = {0,…,R}, escreva AR = AΛR. Defina Aloc como a união crescente dos AR e A como seu fecho na norma de operador. Denote o fator original por M = A′′, identificado com o fator da torre canônica, sem trocar a representação.

> Aloc = união dos AR; A = fecho de Aloc na norma ‖·‖.

Um D : `BondInteractionData P` fornece Vj = D.term(j), J = D.bound ≥ 0, Vj* = Vj, Vj ∈ A{j,j+1} e ‖Vj‖ ≤ J. Não exige convergência de Σj‖Vj‖. Escolha também, em cada sítio, h_j = h_j* ∈ A{j}. Cada h_j é limitado porque o sítio é matricial, mas a sequência de suas normas pode ser ilimitada. A especialização canônica é h_j = siteOperator(P,j,diag(log P.w(j), log(1−P.w(j)))).

> H_N = Σ(j<N) Vj; H⁰_N = Σ(j≤N) h_j; K_N = H⁰_N + H_N.
>
> τᴺ_t(A) = exp(itK_N) A exp(−itK_N).

**Teorema.** Para cada A ∈ A, τ_t(A) = lim(N→∞) τᴺ_t(A) existe na norma, uniformemente em t em qualquer intervalo compacto. Os τ_t formam um grupo de automorfismos *, unital e isométrico, e t ↦ τ_t(A) é contínua na norma para cada A. A sequência de prefixos pode ser substituída por qualquer exaustão crescente por subconjuntos finitos, incluindo h_j quando j pertence ao volume e Vj quando o bond declarado {j,j+1} está contido no volume. Para cada temperatura inversa θ > 0 existe ao menos um estado θ-KMS para esse grupo. θ é aqui um parâmetro termodinâmico, sem identificação com β_TGL.

O caso h_j = 0 é a interação pura. O caso h_j = log ρ_j é a perturbação extensiva do fundo modular canônico. A propriedade “automorfismo normal de M” não é consequência desse contrato.

## 2. A álgebra de sítios é a canônica

[REAL — enunciados consultados] `ChainSiteOperators` define os sítios por `towerPi` de matrizes inseridas na torre e `chainLocalAlgebra` por adjunção *. `ChainPrefix.chain_prefix_eq_level` identifica AR com a imagem matricial do andar R. `TowerAction` prova preservação de 1, produto e estrela; `ExpectationPositive.towerPi_injective` prova injetividade. Logo a imagem é uma álgebra C* finita, fechada e isometricamente isomorfa a M_(2^(R+1))(C): um homomorfismo * injetivo entre álgebras C* preserva a norma. Não se usa a norma de Frobenius como norma de operador.

As inclusões entre andares são a ↦ a⊗1, e `towerPi_compat` as identifica no mesmo H. Para Λ finito, produtos de elementos matriciais de seus sítios geram a cópia tensorial de ⊗(j∈Λ)M₂(C), dentro de qualquer prefixo que contenha Λ. A inserção matricial seguida de `towerPi` é injetiva. Assim há uma única norma compatível; A é a álgebra UHF de spins de dimensão 2 em sua representação canônica. A fidelidade transporta a estrutura e a norma; não pressupõe normalidade da dinâmica futura.

`ChainLocality.chain_locality` garante comutação de suportes disjuntos, e a isotonia permite aumentar suportes. Aloc é uma *-álgebra unital. Seu fecho é uma C*-subálgebra de B(H), pela continuidade de produto e estrela. Como exp(itK_N) pertence ao andar N, cada τᴺ_t é um automorfismo de A e ‖τᴺ_t(A)‖ = ‖A‖.

## 3. Estimativa local e estabilização

Escreva ad_B(A) = [B,A]. Se A ∈ AR, somente os bonds j ≤ R podem dar um primeiro comutador não nulo. O resultado fica em A_(R+1). Repetir essa observação dá suporte em A_(R+k) após k comutadores. A desigualdade ‖[B,C]‖ ≤ 2‖B‖‖C‖ fornece, para todo N:

> ‖ad_(H_N)^k(A)‖ ≤ (2J)^k · (R+k)!/R! · ‖A‖. (1)

Prova por indução: no passo k+1 o observável intermediário tem suporte em 0,…,R+k; há no máximo R+k+1 bonds relevantes, cada um contribuindo no máximo 2J vezes sua norma. Multiplicar o majorante anterior por 2J(R+k+1) produz (1). Em cortes pequenos há menos bonds; portanto (1) é uniforme em N.

> N,M ≥ R+k ⇒ ad_(H_N)^k(A) = ad_(H_M)^k(A). (2)

Para (2), a ordem zero é A. Admitindo a igualdade na ordem k, ambos os cortes contêm todos os bonds j ≤ R+k necessários ao passo seguinte se N,M ≥ R+k+1. Os demais comutam com o observável intermediário. Isso prova estabilização, sem afirmar convergência de H_N.

[REAL — Lean] `BondLocalityEstimates` contém `iterated_bracket_mem_prefix`, `iterated_bracket_cutoff_independent` e `iterated_bracket_uniform_bound`, com recibo `PASS_COMPILED_SCOPE`. O quociente de fatoriais de (1) é a simplificação matemática do produto finito usado em `commutatorGrowth`.

## 4. Interação pura: convergência numa janela temporal

Para N fixo, L_N = i ad_(H_N) é linear limitado no espaço de Banach A. A série exp(tL_N) converge para todo t. Tanto exp(tL_N)(A) quanto exp(itH_N)Aexp(−itH_N) resolvem Y′ = L_NY, Y(0) = A. A unicidade da equação limitada segue, por exemplo, da iteração da equação integral com resto fatorial. Portanto:

> exp(itH_N) A exp(−itH_N) = Σ(k≥0) [(it)^k/k!] ad_(H_N)^k(A). (3)

A série é a evolução finita real, não uma evolução definida formalmente sem identificação. Fixe T > 0 com q = 2JT < 1. Se J = 0, todos os Vj são zero e a dinâmica de interação é a identidade, sem divisão por J. Para J > 0, (1) e (3) dão o majorante independente de N e de |t| ≤ T:

> |t|^k ‖ad_(H_N)^k(A)‖/k! ≤ ‖A‖ C(R+k,k) q^k.
>
> Σ(k≥0) C(R+k,k) q^k = (1−q)^(−R−1). (4)

A última identidade resulta de diferenciar R vezes a série geométrica dentro de |q| < 1, ou do binômio negativo. Sua convergência também segue do teste da razão. Se N,M ≥ R+L, as primeiras L+1 parcelas coincidem por (2), logo:

> sup(|t|≤T) ‖τᴺ_t(A)−τᴹ_t(A)‖ ≤ 2‖A‖ Σ(k>L) C(R+k,k)q^k → 0. (5)

A completude de A fornece o limite local uniforme. O raio 1/(2J) não depende de R, embora o majorante dependa. Não se usa a série de (3) uniformemente em N fora dessa janela.

## 5. Do limite local ao grupo em todo tempo

Para A geral, aproxime por B local. A isometria finita dá ‖τᴺ_t(A)−τᴹ_t(A)‖ ≤ 2‖A−B‖ + ‖τᴺ_t(B)−τᴹ_t(B)‖. Usar (5) prova Cauchy uniforme na mesma janela para cada A ∈ A. Os limites preservam linearidade, produto, estrela, unidade e norma. A continuidade temporal segue da convergência uniforme de trajetórias contínuas.

Precisaremos do seguinte lema de compactos. Se isometrias S_N(t) convergem para S(t) uniformemente em t num intervalo I para cada entrada fixa, a convergência é uniforme para entradas em qualquer compacto C ⊂ A. Escolha uma rede finita ε-densa em C. Nas entradas da rede a convergência é uniforme; para as restantes, os dois erros de aproximação somam no máximo 2ε. Isso prova o lema sem convergência em norma de operadores.

Fixe T arbitrário e escolha m inteiro positivo com T/m dentro da janela anterior. Ponha s = t/m. A identidade finita τᴺ_t = (τᴺ_s)^m e telescopagem dão:

> ‖(τᴺ_s)^m A − (τ_s)^m A‖ ≤ Σ(0≤r<m) ‖(τᴺ_s−τ_s)((τ_s)^r A)‖. (6)

Em (6), τ_s ainda é o limite na janela. Os mapas s ↦ (τ_s)^r A são contínuos por indução, usando a isometria para controlar a entrada móvel. Suas imagens em |s| ≤ T/m são compactas. O lema anterior faz (6) tender a zero uniformemente em |t| ≤ T. Assim τᴺ_t(A) converge em qualquer compacto. A independência de m vem de ser o limite da mesma sequência de evoluções finitas.

Passe ao limite em τᴺ_t(τᴺ_s(A)) = τᴺ_(t+s)(A). A entrada móvel é controlada pela soma de ‖τᴺ_s(A)−τ_s(A)‖ e ‖τᴺ_t(τ_s(A))−τ_t(τ_s(A))‖. Resultam τ_tτ_s = τ_(t+s), τ_0 = id e τ_tτ_(−t) = id. Portanto cada τ_t é sobrejetivo, um automorfismo, e não só um endomorfismo isométrico.

Também há independência da exaustão finita. Para A ∈ AR, basta o volume conter 0,…,R+k para estabilizar a ordem k. Em qualquer volume parcial a contagem de bonds relevantes só diminui, preservando (1). Comparar duas exaustões pelo mesmo L e pelo resto (5), depois aplicar (6), identifica seus limites.

## 6. Fundo modular sem norma global do gerador

As dinâmicas de sítio exp(ith_j) comutam entre sítios e definem em cada AR um grupo α⁰_t por conjugação com Σ(j≤R)h_j. As definições nos prefixos são compatíveis, pois os sítios adicionais comutam com AR. A isometria permite extensão única a A; continuidade em cada AR e densidade dão continuidade pontual na norma. Não foi necessário definir Σ(j≥0)h_j como operador limitado.

No perfil canônico, ρ_j = diag(P.w(j),1−P.w(j)) é estritamente positivo; logρ_j é matriz autoadjunta finita. Os pesos da torre são produtos dos pesos de sítio, e o logaritmo do produto é a soma dos logaritmos. Logo H⁰_N coincide com `finiteModularHamiltonian P N`. `finite_modular_action_eq_canonical` identifica α⁰_t com `modularConjugation P t` em cada andar. `SiteModularInvariance.chain_flow_into` preserva regiões; `canonical_conjugation_norm` preserva norma; `local_modular_orbit_norm_continuous` fornece continuidade local.

Defina V_j(t) = α⁰_t(Vj). Cada termo permanece autoadjunto, no mesmo bond e com norma ≤ J. Para cada j sua curva é contínua na norma, por estar numa álgebra finita dimensional. Não se exige continuidade da família inteira numa norma sup sobre todos os sítios.

> U_N(t) = exp(itK_N) exp(−itH⁰_N), B_N(t) = α⁰_t(H_N).
>
> U_N′(t) = U_N(t) iB_N(t). (7)

A ordem em (7) é pela direita. Diferenciar as exponenciais dá i exp(itK_N)(K_N−H⁰_N)exp(−itH⁰_N), igual a U_N iB_N. Defina γ_N(t)(A) = U_N(t)AU_N(t)* e δ_(N,t)(A) = i[B_N(t),A]. Então γ_N′(t) = γ_N(t)∘δ_(N,t), com γ_N(0) = id.

Para N fixo, iterar Volterra fornece a série cronológica no espaço de Banach dos operadores lineares de A. A parcela de ordem k aplicada a A é a integral de δ_(N,s_k)⋯δ_(N,s_1)(A) sobre 0 ≤ s_k ≤ ⋯ ≤ s_1 ≤ t. A ordem corresponde à derivada pela direita de (7). A convergência para N fixo segue da norma limitada de δ_(N,s) num compacto e do resto fatorial; para t < 0 usam-se integrais orientadas.

Para A ∈ AR, cada integrando de ordem k tem suporte em A_(R+k), norma ≤ (2J)^k(R+k)!‖A‖/R! e é independente do corte quando N ≥ R+k. A indução da seção 3 vale com tempos distintos porque usa somente suporte e norma. O volume do simplex é |t|^k/k!. Assim a série de γ_N tem precisamente o majorante (4) e a estimativa Cauchy (5) para q < 1, sem derivar h_j e sem usar sua norma na constante.

Se N ≥ R, τᴺ_t(A) = γ_N(t)(α⁰_t(A)). A entrada α⁰_t(A) permanece em AR, com norma ‖A‖, e sua trajetória compacta é tratada pelo lema da seção 5. Equivalentemente, o resto (5) já é uniforme em todas as entradas de AR com norma fixada. Isso prova convergência na janela. Os τᴺ_t são grupos, embora γ_N isoladamente não seja; aplicar a seção 5 conclui a existência em todo tempo e para qualquer exaustão.

Não se conclui convergência de U_N em B(H), nem existência de uma soma limitada dos Vj: convergem suas ações sobre observáveis quase locais. Para A ∈ AR, o gerador da dinâmica é i[Σ(j≤R)h_j + Σ(j≤R)Vj,A], soma finita obtida do termo linear em (7). Não se atribui domínio total ou norma finita ao gerador fechado global.

## 7. Conferência com Nachtergaele–Sims

[KNOWN] Nachtergaele e Sims, *On the dynamics of lattice systems with unbounded on-site terms in the Hamiltonian*, arXiv:1410.8174 (2014), seção 3 e teorema 4.1, tratam o limite com termos autoadjuntos de sítio e interação de norma F finita. A aplicação é corroborativa; as seções 3–6 já deram uma prova própria para este contrato. [Fonte primária](https://arxiv.org/abs/1410.8174), [PDF primário](https://arxiv.org/pdf/1410.8174).

Conferência calculada aqui: a rede é N, com distância |x−y|; cada sítio é C²; inclusões e normas são as da seção 2. Escolha F(r) = (1+r)^−2. Ela é positiva e decrescente, e S = sup_x Σ_y F(|x−y|) ≤ 1+2Σ(n≥1)(1+n)^−2 < ∞. Se r = |x−y|, todo z satisfaz |x−z| ≥ r/2 ou |z−y| ≥ r/2. Em cada metade o fator distante é ≤ 4F(r), e a soma do outro fator é ≤ S. Portanto:

> Σ(z≥0) F(|x−z|)F(|z−y|) ≤ 8S F(|x−y|). (8)

Defina Φ({j,j+1}) = Vj e Φ(X) = 0 para os demais conjuntos. No par x=y há até dois bonds, dando 2J. Se |x−y|=1 há um bond e F(1)=1/4, dando 4J. Se a distância é maior, a soma é zero. Logo a norma F da interação é ≤ 4J. Os h_j são matrizes autoadjuntas de domínio total em C², satisfazendo a hipótese individual de sítio, sem limite uniforme de suas normas.

O resultado citado é a existência do limite em norma sobre observáveis locais, uniforme em compactos temporais, independente da exaustão, com extensão a automorfismos da álgebra quase local. A continuidade pontual na norma desta especialização já foi demonstrada acima. Não se importam uma extensão normal ao fator original nem um estado KMS especificado.

## 8. Estados KMS: construção e passagem ao limite

Fixe θ > 0 e a convenção τ_t = Ad exp(itH), com Gibbs finito exp(−θH)/Tr exp(−θH). Defina φ_N em A pelo Gibbs de K_N no prefixo 0,…,N, tensorizado com o estado tracial nos sítios restantes. O produto é consistente nos andares e define um estado de A. τᴺ_t é a identidade fora do prefixo. Num andar maior a densidade é Gibbs de K_N tensorizado com identidade normalizada; a ciclicidade do traço prova a condição θ-KMS. A densidade estende a condição a A.

A é separável: bastam coeficientes racionais complexos nas matrizes dos andares. Seu espaço de estados é compacto metrizável na topologia fraca*. Extraia uma subsequência φ_N convergente para um estado φ. A convergência das dinâmicas é uniforme em compactos reais para cada observável. A passagem KMS pode ser verificada diretamente por regularização gaussiana, sem supor limite complexo das evoluções originais.

> f_a(t) = √(a/π) exp(−at²), a > 0.
>
> B_(N,a)(z) = ∫(t∈R) f_a(t−z) τᴺ_t(B) dt. (9)

As integrais de Bochner em (9) são inteiras em z: em compactos complexos, todas as derivadas são dominadas por polinômio vezes gaussiana integrável. Para z=x+iy, |f_a(t−z)|=exp(ay²)f_a(t−x). Divida a integral em um compacto real e sua cauda. Convergência das dinâmicas e isometria dão B_(N,a)(z) → B_a(z), uniformemente em compactos complexos; B_a usa τ_t em lugar de τᴺ_t. B_(N,a)(0) é inteiro analítico para τᴺ e sua translação complexa é B_(N,a)(z).

A identidade KMS finita dá φ_N(A B_(N,a)(iθ)) = φ_N(B_(N,a)(0) A), para todos A,B ∈ A. Passe ao limite pela convergência em norma dos elementos e fraca* dos estados:

> φ(A B_a(iθ)) = φ(B_a(0) A). (10)

Para cada a, G_a(z)=φ(A B_a(z)) é analítica na faixa 0<Im z<θ e contínua no fecho. Sua borda inferior é φ(Aτ_t(B_a(0))). Aplicar (10) ao observável τ_t(B) dá a borda superior φ(τ_t(B_a(0))A). Ambas têm módulo ≤ ‖A‖‖B_a(0)‖. No interior, (9) dá limite finito uniforme em Re z. O princípio das três linhas para funções limitadas na faixa fornece a mesma estimativa em toda a faixa.

Quando a→∞, B_a(0)→B em norma: gaussianas formam identidade aproximada e t↦τ_t(B) é contínua. A estimativa de faixa aplicada a G_a−G_b dá sup|G_a−G_b| ≤ ‖A‖‖B_a(0)−B_b(0)‖. Portanto G_a converge uniformemente no fecho da faixa para uma função G contínua, analítica no interior, com bordas G(t)=φ(Aτ_t(B)) e G(t+iθ)=φ(τ_t(B)A). Esta é a condição θ-KMS, agora para o limite. Nenhum limite de matrizes densidade globais ou de vetores no H original foi presumido.

**Precisão de sinal.** O kernel usa gerador modular finito +logρ e α_t(A)=ρ^(it)Aρ^(−it). Na convenção de faixa superior adotada aqui, ρ é Gibbs com parâmetro −1 para +logρ, ou com parâmetro +1 para o relógio invertido α_(−t). Isso é convenção temporal explícita. Os estados θ-KMS acima existem para a dinâmica escolhida; não foram identificados com a referência ωP, com um estado Araki normal no fator original nem com uma temperatura física determinada.

[DERIVED] Um estado KMS é invariante: com A=1, as duas bordas da função KMS coincidem. Repetir essa função por faixas de altura θ produz uma função inteira limitada (a colagem é analítica por Morera); Liouville a torna constante, dando φ(τ_t(B))=φ(B). Em sua própria GNS, a invariância define U_tπφ(A)Ωφ=πφ(τ_t(A))Ωφ; igualdade de normas e densidade estendem U_t a um grupo unitário fortemente contínuo. Sua conjugação preserva πφ(A)′′ e é normal. Essa álgebra de von Neumann pertence à representação do estado escolhido, sem identificação automática com M do perfil original.

## 9. Obstrução à extensão normal ao fator original

[DERIVED — contraexemplo] Tome perfil constante p∈(0,1), p≠1/2. Ponha Z=diag(1,−1), X=[[0,1],[1,0]], Z_j=siteOperator(P,j,Z), X_j=siteOperator(P,j,X) e m=2p−1≠0. Escolha Vj=X_j. Por isotonia ele pertence ao bond {j,j+1}, é autoadjunto e tem norma 1. É um `BondInteractionData` legítimo, embora seu suporte possa ser menor que o bond declarado.

> M_N = (1/N) Σ(j<N) Z_j, N≥1.
>
> ‖(M_N−m1)ΩP‖² = (1−m²)/N. (11)

(11) usa ωP(Z_j)=m, Z_j²=1 e ωP(Z_jZ_k)=m² para j≠k, pelo estado produto canônico. As âncoras são `omegaState_pi` e `site_operator_product_state`. Para B com suporte em 0,…,R, ‖[M_N,B]‖ ≤ 2(R+1)‖B‖/N. Assim (M_N−m1)BΩP = B(M_N−m1)ΩP + [M_N,B]ΩP tende a zero. Os BΩP são densos por `towerPi_orbit_dense`, e ‖M_N−m1‖ ≤ 1+|m|. Logo M_N → m1 fortemente em todo H.

Para Vj=X_j e h_j=0, no tempo t=π/2 temos exp(iπX/2)=iX e XZX=−Z. Consequentemente τ_(π/2)(Z_j)=−Z_j e τ_(π/2)(M_N)=−M_N. Se houvesse extensão normal desse automorfismo a M, a continuidade ultra-fraca preservaria M_N→m1, dando imagem convergente a m1. Mas −M_N→−m1 fortemente e ultra-fracamente. A unicidade do limite e m≠0 dão contradição. Foi usado que convergência forte de uma sequência limitada implica convergência ultra-fraca.

O controle também inclui o fundo modular: num perfil constante, h_j=logρ_j tem a mesma norma finita em todos os sítios. Escolha Vj=X_j−h_j, bond admissível com J=1+‖logρ‖. Então K_N=Σ(j<N)X_j+h_N. Para cada sítio fixo, o termo de fronteira h_N acaba fora do suporte; o limite é a mesma dinâmica de X. Incluir o fundo modular não elimina a obstrução.

O contraexemplo não diz que toda interação deixa de ser normal; impede deduzir normalidade de toda interação somente de `BondInteractionData`. Para um caso particular, preservação do fólio normal da referência, implementação no mesmo H ou outro critério suficiente são obrigações adicionais. A existência no fecho C* permanece demonstrada.

## 10. Estatutos e fronteiras

> [nota operacional do operador — omitida no retrato público]

## 11. Fontes e âncoras

Todos os caminhos locais foram consultados como texto. O manifesto registra hashes medidos. Nenhum `um.py` foi executado ou importado. As referências de implementação não conferem, por si, um selo Lean ao argumento infinito escrito.

- [Contrato e estimativas](<C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/BondLocalityEstimates.lean:12>); estabilização na linha 177 e majorante na linha 205.
- [Álgebra local](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/ChainSiteOperators.lean:77>).
- [Prefixo = andar](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/ChainPrefix.lean:80>).
- [Localidade](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/ChainLocality.lean:40>).
- [Fidelidade matricial](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/ExpectationPositive.lean:24>).
- [Órbita densa](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/TowerAction.lean:420>).
- [Estado da torre](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/TheFactorObject.lean:109>).
- [Produto entre sítios](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/SitePauliObservables.lean:140>).
- [Fundo modular preserva regiões](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/SiteModularInvariance.lean:37>).
- [Gerador finito +log dos pesos](<C:/IALD/Central de Patentes/Chatgpt/INTEGRADOR_SELETOR_LOCALIDADE_20260909_174443_581582/BUILD_SUCCESSOR_20260909_174751_385895/TGLExt/FiniteModularHamiltonian.lean:20>).
- [Isometria e continuidade local](<C:/IALD/Central de Patentes/Chatgpt/INTEGRADOR_SELETOR_LOCALIDADE_20260909_174443_581582/BUILD_SUCCESSOR_20260909_174751_385895/TGLExt/SummableInteractionModularOrbit.lean:43>); continuidade na linha 57.
- [Nachtergaele–Sims (2014), artigo primário](https://arxiv.org/abs/1410.8174), teorema 4.1 na página 11 e hipóteses da seção 3 nas páginas 7–8.

As constantes de (8), a conferência do contrato, a prova por séries e o controle de normalidade foram calculados nesta nota; não são transcrições do artigo externo.
