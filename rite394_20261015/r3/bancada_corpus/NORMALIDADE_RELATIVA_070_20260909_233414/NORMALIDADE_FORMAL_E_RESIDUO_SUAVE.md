# Normalidade formal, reducibilidade e o resíduo relativo suave do Einstein–sigma

09/09/2026, arco 070. [DERIVED — demonstração escrita; nenhuma compilação Lean ou execução de um.py]. Nota de autoria desta tarefa, com correção ao lado da análise 069 e sem alteração de suas fontes.

**Resultado.** A constante cosmológica não é, por si, um obstáculo de normalidade. Construímos uma filtragem que transporta resultados relativos de Λ=0 para qualquer Λ fixo por um procedimento finito, sem especializar uma série em Λ. Demonstramos também que o Einstein–sigma com alvo tridimensional não possui parâmetros locais universais de reducibilidade: os três diferenciais sigma e o diferencial de sua energia cinética os anulam. Na completação formal dos valores dos campos, o quadrático Pauli–Fierz mais três escalares paga a hipótese de normalidade. Na classe original C∞(U), a passagem de primitivas formais a primitivas suaves permanece um contrato específico: a eliminação do representante quadrático puro em antifields, seguida da covariantização no grau dois. Não se declara H¹,⁴(s|d)=0 na classe suave inteira.

## 1. Modelo e duas álgebras que precisam permanecer distintas

[INPUT] Mantemos a ação ambiente já adotada nas notas 067–069:

\[
 S_\Lambda[g,y]=-{1\over2\kappa}\int(R-2\Lambda)\,dV_g
       +{c\over2}\int Q\,dV_g,
 \qquad Q=g^{ab}h_{AB}(y)u_a^Au_b^B,\quad u_a^A=\partial_a y^A.
\tag{1}
\]

A assinatura é (+---), c,κ são não nulos, h é a métrica positiva do S³ numa carta suave U e o único gauge é difeomorfismo. Não há gauge de Weyl nem gauge das isometrias rígidas do alvo. Os valores c=k/(π cosh²k), κc=4 e Λ=3/4 são permitidos, mas não necessários aos argumentos abaixo.

Escrevemos B=Ddu, τ=tr_g B e

\[
 E_{ab}=G_{ab}+\Lambda g_{ab}
       -\kappa c\bigl(h_{AB}u_a^Au_b^B-\tfrac12g_{ab}Q\bigr).
\tag{2}
\]

**A álgebra suave A_nat(U).** É a mesma da nota KT069: expressões naturais de ordem finita, polinomiais nos jatos diferenciados e antifields, com coeficientes C∞(U) nos valores y. A métrica entra por contrações, g⁻¹ e volume; denominadores em gradientes ou curvatura não são permitidos. A igualdade fraca é anulação em todos os jatos estacionários formais, incluindo os prolongamentos das EOM.

**A completação formal Â_(η,y₀).** Escolhemos g=η+q e y=y₀+z. Os coeficientes são séries formais em q,z não diferenciados; derivados e antifields continuam polinomiais com grau K limitado. Essa é uma álgebra formal de flutuações, não o anel C∞(U). A série de Taylor de f∈C∞(U) existe formalmente, mas o mapa de Taylor num ponto não é injetivo. Logo provar uma identidade depois dessa aplicação não prova a identidade suave original.

Nenhum resultado abaixo identifica essas duas álgebras. Tampouco identifica a ação ambiente com a ação composta exclusivamente nas probabilidades P: a degenerescência variacional dessa composição continua sendo uma questão separada.

## 2. O que a fonte primária efetivamente fornece

[KNOWN] BBH1994 declara Einstein, com ou sem constante cosmológica, normal (§10, p.31). O Teorema 10.1 controla o número de derivados, admitindo séries nos campos não diferenciados; o ganho inteiramente polinomial exige δ_int,0=0, que o próprio texto exclui para Einstein. O Teorema 11.2 elimina representantes quadráticos puros em antifields para teorias lineares e estende o argumento às normais. Esses enunciados não são uma afirmação de convergência suave das séries. [BBH1994, §§10–11](https://arxiv.org/pdf/hep-th/9405109v2).

[KNOWN] BBH2000 define normalidade pela aciclicidade positiva de δ_(0),0. O Teorema 6.6 transporta o Teorema 6.5 para polinômios nos derivados e séries nos campos não diferenciados. Na prova do Teorema 6.7, eliminar o coeficiente do ghost-antifield ainda deixa um termo quadrático puro; sua trivialidade usa precisamente 6.5(ii)/6.6. Portanto a classificação por reducibilidades não decorre apenas da KT ordinária. [BBH2000, §§6.4.2–6.4.4](https://arxiv.org/pdf/hep-th/0002245v3).

[KNOWN] BBH1995, Apêndice E, distingue primitivas quase locais de primitivas locais. O Lema E.2 remove a dependência formal problemática do vielbein projetando para grau zero nos pares U,V, pois essa contagem comuta com s. O próprio argumento é feito para o subcomplexo A₂; não converte automaticamente uma série formal numa variável material física em função suave dessa variável. [BBH1995, Apêndice E, especialmente E.2–E.3](https://arxiv.org/pdf/hep-th/9505173v2).

## 3. Errata ao lado da nota 069

Na [nota KT069, seção 8](../REGULARIDADE_KT_JATOS_20260909_224852/CERTIFICADO_POLINOMIAL_EINSTEIN_SIGMA.md), a advertência sobre expandir uma ação com Λ≠0 em torno de η era correta: η com y constante não resolve essa ação, e um termo linear não pode ser simplesmente omitido. Entretanto, seria excessivo transformar essa advertência numa obstrução de normalidade causada por Λ. A fonte primária acima afirma o contrário, e a seção seguinte fornece um transporte independente que trata Λ exatamente.

**Correção precisa:** o obstáculo residual desta análise é preservar a classe suave dos coeficientes do alvo na construção relativa, não a presença isolada de Λ. A prova KT069 de igualdade fraca e resolução ordinária permanece intacta.

## 4. Filtragem exata e transporte finito em Λ

[DERIVED] Trabalhemos primeiro em coordenadas de jatos parciais, com antifields densitizados canônicos. Dar peso zero aos campos não diferenciados é compatível com coeficientes suaves em seus valores. Defina

\[
 K=N_\partial+2N_{\Phi^*}+3N_{C^*},
 \qquad \Phi=(g_{ab},y^A).
\tag{3}
\]

Cada derivada parcial acrescenta um ao peso. O termo de Einstein sem Λ e a energia sigma têm duas derivadas totais em cada monômio. Em particular, g⁻¹(∂g)², h(y)(∂y)² e Γ(h)(∂y)² possuem peso dois; uma derivada de um coeficiente C∞(y) introduz ∂y e também aumenta o peso em um. Os geradores de Noether no diferencial de C* contêm uma derivada de g* ou um fator ∂y multiplicando y*. Assim

\[
 [K,\delta_0]=0,\qquad [K,d_H]=d_H.
\tag{4}
\]

O termo cosmológico altera somente a equação métrica por uma expressão de peso zero. Seus prolongamentos preservam a diferença de peso −2. Logo, sem expansão em Λ,

\[
 \delta_\Lambda=\delta_0+\Lambda\delta_{-2},
 \qquad [K,\delta_{-2}]=-2\delta_{-2}.
\tag{5}
\]

Aqui δ₀ é o diferencial **completo e não linear** de (1) em Λ=0, não apenas o diferencial livre. A identidade de Noether ∇E+κc⟨τ,u⟩=0 garante a nilpotência para todo Λ. Pode-se também verificar δ_-2²=0 e {δ₀,δ_-2}=0: a modificação de δg* é independente de antifields e sua contribuição à identidade de Noether é a divergência covariante de um múltiplo constante da métrica.

### Lema de transporte relativo

Considere uma classe de coeficientes preservada por δ₀,δ_-2,d_H, com K inteiro não negativo e com elementos de K limitado. Suponha, para o número de antifield k em questão, que toda solução homogênea

\[
 \delta_0a_N+d_Hb_{N-1}=0
\]

admita

\[
 a_N=\delta_0c_N+d_He_{N-1}
\tag{6}
\]

na **mesma classe**, com os pesos indicados. Então H⁴_k(δ_Λ|d_H)=0 nessa classe para qualquer Λ fixo.

**Prova.** Num ciclo a de grau máximo N, a parte de grau máximo satisfaz a primeira igualdade porque a correção cosmológica reduz K. Subtraia δ_Λc_N+d_He_(N−1). A parte a_N desaparece e a única contribuição adicional é −Λδ_-2c_N, de peso N−2. A operação preserva a condição de ciclo módulo d_H. Repita no novo peso máximo. Não pode aparecer grau acima de N e cada etapa elimina o grau máximo corrente. Como K≥0, são necessárias no máximo N+1 eliminações, mesmo quando há simultaneamente as duas paridades de K. A soma das primitivas é finita. Isso prova (6) com δ_Λ. ∎

Se a existência de primitivas para δ₀ é inicialmente dada sem homogeneidade, a decomposição em K fornece os componentes de (6), pois δ₀ preserva K e d_H o aumenta em um. A hipótese essencial é que uma primitiva de K limitado exista na classe original.

O lema vale tanto na classe suave, **se essa hipótese de base for paga**, quanto na completação formal. Ele não avalia em ε=1 uma expansão formal, não recenteriza um fundo fora das equações e não soma uma série infinita em Λ. Também não estabelece por si a hipótese relativa em Λ=0.

## 5. Normalidade diretamente demonstrada na completação formal

[DERIVED] Em Λ=0, (η,y₀ constante) resolve as EOM. Escolha coordenadas normais do alvo em y₀. O termo quadrático é a soma direta de Pauli–Fierz não degenerado e três escalares reais sem massa, com matriz cinética c h(y₀). O sinal global não muda o complexo KT enquanto κ,c e h forem invertíveis. O gauge livre é δq_ab=2∂_(a v_b), δz=0; o gauge completo é difeomorfismo e permanece irreducível.

A KT livre tem apenas as identidades lineares de Bianchi no bloco métrico. Sua resolução positiva resulta também da parte linear do split de jatos construído em KT069: as equações e as identidades independentes formam pares contráteis; o bloco scalar é o operador de onda sobre os jatos simétricos. Portanto δ_free,0=δ_free é acíclica em número positivo de antifield.

Com (3), todos os termos do δ₀ completo têm K=0. A expansão formal da ação em q,z começa no grau quadrático e a parte de interação tem grau de campos estritamente superior ao livre. Essas são as condições da normalidade na completação formal. O fato de h ser suave basta para sua série formal; não se usa convergência analítica. O Teorema 6.6 então fornece a eliminação de M₂, bem como o desaparecimento dos grupos com k≥3, com limite finito de K. O lema da seção 4 transporta o resultado para Λ fixo nessa mesma completação.

Para transformar a eliminação de M₂ em H⁴₂=0, é necessário excluir também a reducibilidade universal. Esse passo é provado a seguir diretamente no sigma, inclusive antes da completação.

## 6. Ausência de reducibilidade universal: prova pelos quatro covetores

[DERIVED] Um parâmetro universal de reducibilidade v=v(jets) satisfaz

\[
 \mathcal L_vg\approx0,\qquad v^a u_a^A\approx0.
\tag{7}
\]

São identidades em todos os jatos estacionários, e não uma escolha de Killing num fundo simétrico. Como Q é um escalar natural de g,y e seus primeiros derivados, a naturalidade e o prolongamento de (7) implicam

\[
 v^a\partial_a Q=\mathcal L_vQ\approx0.
\tag{8}
\]

Essa afirmação continua válida quando v depende de jatos: fixa-se seu valor como parâmetro na ação infinitesimal prolongada, e a identidade natural δ_vQ=ℒ_vQ contém as derivadas do mesmo v. Os termos δ_vg e D(δ_vy) desaparecem no ideal diferencial das EOM.

Fixe um valor arbitrário y₀ da carta. Num referencial ortonormal do alvo e num referencial Lorentziano no ponto, escolha o seguinte jato da matéria:

\[
 u_0^A=0,\quad u_i^A=\delta_i^A\ (i,A=1,2,3),
 \qquad B^1_{01}=B^1_{10}=b\ne0,
\tag{9}
\]

com os demais componentes de B iguais a zero. A simetria de B está satisfeita e tr_g B=0, logo a equação sigma de segunda ordem vale. A equação métrica fixa Ric_ab=Λg_ab+κcW_ab; qualquer tal Ricci simétrico é realizável por um jato métrico de segunda ordem. O split regular KT069 garante que esses dados podem ser prolongados a jatos estacionários de todas as ordens. Não é necessária uma solução global com essa forma.

Pela compatibilidade das conexões,

\[
 \partial_\mu Q=2h_{AB}g^{\nu\rho}B^A_{\mu\nu}u^B_\rho.
\]

Em (9), temos dQ=−2b dx⁰ e dy^i=dx^i. Portanto

\[
 dy^1\wedge dy^2\wedge dy^3\wedge dQ\ne0.
\tag{10}
\]

O determinante D desses quatro covetores é polinomial nos jatos diferenciados, com coeficientes suaves em y. Para cada y ele não é o polinômio zero no espaço de coordenadas estacionárias livres, como mostra (9) em bases adaptadas. Sua região não nula é densa nessa fibra finita de jatos. As equações (7)–(8) são um sistema linear homogêneo de quatro linhas em v. Multiplicar pela adjugata dá Dv≈0. Na região D≠0, v≈0; por continuidade, vale em toda a fibra. Como y era arbitrário, a conclusão vale em A_nat(U).

**Não se divide por D na construção de um coeficiente ou primitiva.** A região D≠0 é usada apenas para uma prova de anulação por densidade. A conclusão inclui os jatos degenerados onde os quatro covetores não são base. Na apresentação formal, o mesmo determinante é um elemento não nulo da álgebra formal de jatos sobre um corpo; o argumento de não divisor de zero dá a conclusão correspondente.

Consequentemente não há parâmetro local universal de reducibilidade não trivial para esta ação. Os Killing particulares do habitante homogêneo não são contraexemplos: (7) exige uma identidade sobre o espaço estacionário completo, e exige preservar também a matéria. As isometrias rígidas do alvo não acrescentam ghosts à álgebra adotada.

## 7. O passo relativo que KT ordinária não substitui

[DERIVED] Após integrações por partes, um representante de antifield dois pode ser escrito como

\[
 a_2=C^*_a f^a+M_2,
\tag{11}
\]

onde M₂ é quadrático nos antifields dos campos e seus derivados, sem C*. Da equação δa₂+d_Hb₁=0, a derivada de Euler em relação aos antifields dos campos dá a identidade de reducibilidade. A seção 6 implica f≈0. A KT069 fornece então f=δg₁ com coeficientes da mesma classe. Subtraindo o cobordo adequado com C*g₁, elimina-se o primeiro termo de (11).

**O restante não desaparece por esse argumento.** É necessário o lema

\[
 N_{C^*}M_2=0,\quad\delta M_2+d_Hb_1=0
 \ \Longrightarrow\ M_2=\delta c_3+d_He_2
\tag{M2}
\]

com c₃,e₂ na classe desejada. A seção 5 paga (M2) na completação formal, com K finito, e a seção 4 transporta-o em Λ quando se aplica o resultado para H⁴₂ completo em Λ=0. Juntas com a ausência de reducibilidade, elas dão

\[
 H^4_2(\delta_\Lambda\mid d_H,\widehat A)=0.
\tag{12}
\]

Esse resultado não é uma prova de (M2) em A_nat(U). O aumento de número de campos usado na demonstração formal pode continuar indefinidamente nos valores não diferenciados, todos com K=0. Ter um limite de K controla os derivados, mas não termina essa expansão.

## 8. Covariância, alvo suave e o contrato mínimo para o grau dois

A contagem de graus comunicada no arco 070 reduz o canal dinâmico relevante a H²_char,cov. Para esse uso não é necessário reabrir a independência das classes características de grau quatro. O resultado (12), a comparação KT–característica e a covariantização precisam, entretanto, ser usados na mesma classe de coeficientes.

A KT069 já é covariante e preserva C∞(U). Isso paga o levantamento ordinário das igualdades fracas. O Lema E.2 de BBH pode retirar séries formais do vielbein na apresentação adequada; ele não retira séries formais em y. Em particular, o valor y integra o setor tensorial físico A₂, enquanto os pares U,V eliminados pertencem ao setor contratível de coordenadas/gauge. Projetar U,V para grau zero deixa qualquer série em y exatamente como estava.

Também não se pode congelar C∞(y) como coeficientes constantes do diferencial horizontal: para uma função f,

\[
 d_Hf(y)=\partial_Af(y)\,dy^A.
\tag{13}
\]

Uma homotopia que ignorasse (13) calcularia outro complexo. A função suave exp(−1/|y−y₀|²), prolongada por zero em y₀, mostra por que uma identidade formal nesse ponto não controla o resto da carta. Isso é uma falha da inferência proposta, não a exibição de uma classe de anomalia.

No grau dois não há polinômio característico linear de curvatura Lorentz: tr R=0 por antissimetria. Para o setor de pullbacks de formas do alvo, numa carta estrelada U, a homotopia radial usual é efetiva e suave. Se F_t(y)=y₀+t(y−y₀), E=(y−y₀)^A∂_A, então, em grau p>0,

\[
 H\omega=\int_0^1{dt\over t}F_t^*(\iota_E\omega),
 \qquad dH\omega+Hd\omega=\omega.
\tag{14}
\]

O fator t^p do pullback torna o integrando regular em t=0. Pullback por y transforma (14) numa primitiva horizontal local, suave e com número finito de fatores dy. Assim o setor puramente topológico local do alvo não introduz um grau dois nessa carta. Isso não elimina, por si, classes características dinâmicas que usam EOM e antifields. A colagem no S³ global é outro enunciado, tratado separadamente no arco 070.

**Contrato residual suficiente, na classe pedida:** demonstrar (M2) com primitivas naturais de K finito e coeficientes C∞(U), ou fornecer diretamente uma homotopia covariante suave de H²_char,cov. A seção 4 mostra que basta fazê-lo em Λ=0. Uma construção em jatos não covariantes precisará ainda provar que sua primitiva volta à classe natural; excluir apenas tr R não substitui esse transporte.

## 9. Balanço verificável para integração

| Afirmação | Estatuto nesta nota |
|---|---|
| Λ isoladamente impede normalidade de Einstein | Corrigida: a fonte primária admite Λ |
| Filtragem K e δ_Λ=δ₀+Λδ_-2 | [DERIVED], exata na ação escolhida |
| Transporte de primitivas relativas com K controlado | [DERIVED], indução descendente finita; hipótese de base explícita |
| Ausência de reducibilidade universal Einstein–sigma tridimensional | [DERIVED], prova pelos quatro covetores; sem denominador em dy |
| Normalidade em Λ=0 na completação formal | [DERIVED] a partir do quadrático e KT livre, usando o critério [KNOWN] |
| H⁴₂(δ_Λ|d_H) na completação formal | [DERIVED + KNOWN], pela normalidade, ausência de reducibilidade e transporte |
| KT ordinária e certificado fraco na classe suave natural | Entrada demonstrada em KT069; não promovida a cohomologia relativa |
| (M2) e H²_char,cov para toda A_nat(U) | [OPEN] no alcance desta nota, com o contrato exato acima |
| Toda H¹,⁴(s|d) suave / ausência de todas as anomalias | Não concluída aqui |
| EFT UV completa ou medida funcional não perturbativa | Fora do resultado |

O resultado formal é pertinente à álgebra perturbativa formal. Para declarar o desaparecimento de obstruções na classe suave natural completa, a primitiva relativa suave ainda deve ser produzida ou importada de um teorema cujo enunciado cubra precisamente essa classe. Não há novo cálculo de um.py, teste de natureza, gate ou certificação Lean nesta nota.
