# Topologia do alvo S³ e anomalias locais Einstein–sigma

Arco 070, 09/09/2026. [DERIVED — demonstrações escritas e redução condicional; não Lean]. Consulta de fontes primárias e leitura de artefatos anteriores. Nenhum original foi alterado, nenhum programa um.py foi executado/importado.

**Resultado.** A classe de volume do alvo S³ fornece uma corrente topológica de grau 3 e uma descida de grau total 3. Ela não fornece diretamente uma anomalia local de ghost 1 e forma 4. A possível composição de uma 2-forma fechada do alvo com uma descida gravitacional também é trivial na álgebra BRST local usual, por uma primitiva explícita. Para a classificação completa, esta nota reduz o setor covariante de grau total 5 ao contrato preciso H²_char,cov=0. Não transforma a resolução KT ordinária de 069 nessa cohomologia relativa.

## 1. Complexo, classe e simetrias

[INPUT] Quatro dimensões, métrica Lorentz não degenerada, conexão de Levi-Civita, mapa φ:M→S³ com métrica redonda h, ação Einstein–sigma com κ,c não nulos e constante cosmológica. A apresentação por vielbein acrescenta o gauge de Lorentz local como redundância equivalente da métrica; não acrescenta gauge interno ao sigma. Escrevemos

\[
s\phi^A=\xi^\mu\partial_\mu\phi^A,\qquad
s g=\mathcal L_\xi g,\qquad
s\xi^\mu=\xi^\nu\partial_\nu\xi^\mu,\qquad s^2=0.
\]

Os antifields completam o diferencial BV da ação. A álgebra admite ordem finita de jato, polinômios nos jatos diferenciados, ghosts e antifields, coeficientes suaves nos valores do alvo e os inversos métricos usuais. Não introduz inversos de dφ, de curvaturas ou de componentes privilegiadas da métrica. Quando se exige globalidade em S³, os coeficientes e os contratermos são objetos globais e compatíveis com mudanças de coordenadas do alvo.

A anomalia local procurada satisfaz
\[
s a^{1,4}+d a^{2,3}=0,\qquad
a^{1,4}\sim a^{1,4}+s b^{0,4}+d b^{1,3}.
\tag{1.1}
\]
O par sobrescrito é (ghost,forma). Os contratermos em (1.1) são locais e podem variar sob o gauge: exigir que b seja previamente gauge-invariante mudaria o problema de cohomologia. A naturalidade passiva em coordenadas e o respeito à simetria rígida do alvo não significam exigir s b=0.

A isometria SO(4) do alvo é **rígida**, sem ghost próprio. O(4), incluindo reflexão de orientação do alvo, é uma exigência adicional possível. Nenhum ghost de Weyl, conexão U(1), gauge da isometria do alvo ou campo de forma superior foi incluído. Inseri-los muda a classificação.

## 2. A corrente de volume e sua descida: cálculo direto

Em coordenadas ambientes z⁰,…,z³, Σ(zᴬ)²=1, tome a orientação e a forma normalizada
\[
\Omega_3=\frac{1}{2\pi^2\,3!}\,
 \epsilon_{ABCD}z^A\,dz^B\wedge dz^C\wedge dz^D,\qquad
\int_{S^3}\Omega_3=1.
\tag{2.1}
\]
A dimensão do alvo dá d_NΩ₃=0. Logo
\[
j_3=\phi^*\Omega_3,\qquad dj_3=\phi^*(d_N\Omega_3)=0
\tag{2.2}
\]
**off-shell**. Em uma hipersuperfície fechada Σ³, a integral é o grau do mapa quando Σ³ e a aplicação permitem essa interpretação; para φ=id em cada S³ do fundo I×S³, a integral é 1. Isso é carga topológica, sem uso de Einstein ou da equação sigma.

Defina o diferencial total \(\mathscr D=d+s\), com ds+sd=0, e substitua cada dφᴬ por \(\mathscr D\phi^A=d\phi^A+s\phi^A\). O pullback total
\[
\mathbf j_3=\frac1{3!}\Omega_{ABC}(\phi)
  \mathscr D\phi^A\mathscr D\phi^B\mathscr D\phi^C
\tag{2.3}
\]
satisfaz \(\mathscr D\mathbf j_3=0\), pois \(\mathscr D^2\phi=0\) e d_NΩ₃=0. A expansão por ghost tem somente
\[
j^{0,3},\quad j^{1,2},\quad j^{2,1},\quad j^{3,0}.
\tag{2.4}
\]
Em particular \(j^{1,2}=\frac12\Omega_{ABC}(\phi)(s\phi^A)d\phi^B d\phi^C\), com a convenção de ghosts à esquerda. As equações da descida são
\[
s j^{0,3}+d j^{1,2}=0,\quad
s j^{1,2}+d j^{2,1}=0,\quad
s j^{2,1}+d j^{3,0}=0,\quad s j^{3,0}=0.
\tag{2.5}
\]
Assim, o volume não contém componente (1,4): esse par tem grau total 5, enquanto (2.3) tem grau total 3. Também não define por si uma nova simetria Noether local; sua conservação é uma identidade topológica, não uma nova identidade de gauge.

Em um aberto contrátil do alvo Ω₃=d_NB₂, e j₃=dφ*B₂. Globalmente B₂ não pode existir, porque Stokes daria ∫S³Ω₃=0. Essa diferença real entre carta e alvo inteiro deve ser preservada. Ela não muda a contagem (2.4).

## 3. Coeficientes suaves: o que muda e o que não muda

[DERIVED] Toda 3-forma do alvo é fΩ₃ para f suave e é fechada. Sua classe global é
\[
[f\Omega_3]=\left(\int_{S^3} f\Omega_3\right)[\Omega_3].
\tag{3.1}
\]
Com a métrica redonda fixa, uma primitiva da parte de integral zero pode ser escolhida como
\[
B_2=\delta_h G_h
 \left(f\Omega_3-\left[\int f\Omega_3\right]\Omega_3\right),
\tag{3.2}
\]
onde G_h é o Green da Laplaciana de Hodge no complemento harmônico. A decomposição de Hodge e o fato de a forma ser fechada dão d_NB₂ igual ao argumento. Para uma 2-forma fechada Ω₂, H²_dR(S³)=0 e
\[
\alpha_1=\delta_hG_h\Omega_2,\qquad d_N\alpha_1=\Omega_2.
\tag{3.3}
\]
Esse operador age nos coeficientes prescritos sobre o alvo fixo, não resolve uma equação em M. O contratermo resultante continua dependendo de finitos jatos de φ em cada ponto de M. Não se está postulando uma regra universal local em jatos de métricas arbitrárias do alvo: essa seria uma classe mais estreita do que C∞(S³) com h fixo.

SO(4) age transitivamente: os escalares invariantes f são constantes. A forma Ω₃ é SO(4)-invariante. Uma reflexão do alvo troca seu sinal, de modo que não há 3-forma não nula invariante sob O(4) completo. Também não há 1-forma ou 2-forma SO(4)-invariante: no ponto, o estabilizador SO(3) não fixa vetor em Λ¹R³ ou Λ²R³.

Se uma anomalia global é SO(4)-invariante e já admite primitivas globais b,c na classe acima, então
\[
\bar b=\int_{SO(4)}R^*b\,dR,\qquad
\bar c=\int_{SO(4)}R^*c\,dR
\tag{3.4}
\]
satisfazem a mesma identidade s b+d c=a e preservam a simetria do alvo. s e d comutam com as isometrias da ação; a média compacta mantém ordem finita de jato e grau polinomial, alterando somente coeficientes suaves. Isso também vale para O(4) se a anomalia for O(4)-invariante. **A média não constrói uma primitiva que ainda não existe**; apenas preserva a simetria de uma solução global. Não se faz média sobre o grupo de Lorentz não compacto.

## 4. Mistura com descida gravitacional: primitiva explícita

[DERIVED] Na álgebra BRST usual por vielbein, use a conexão generalizada e os polinômios de Chern–Simons q₃ associados aos invariantes quadráticos de so(1,3). Sua normalização não importa para o argumento; fixe-a de modo que
\[
\mathscr D q_3=P_4(\mathbf R).
\tag{4.1}
\]
As curvaturas generalizadas \(\mathbf R\) são horizontais nas quatro 1-variáveis ímpares \(\tilde\xi^\mu=dx^\mu+\xi^\mu\). Os pullbacks totais de formas do alvo também são horizontais nessas variáveis.

Uma possível mistura de grau total 5 é \(\mathbf\Omega_2q_3\), com Ω₂ fechada no alvo. Pela equação (3.3), \(\mathbf\Omega_2=\mathscr D\boldsymbol\alpha_1\). Portanto
\[
\mathscr D(\boldsymbol\alpha_1q_3)
 =\mathbf\Omega_2q_3-\boldsymbol\alpha_1P_4(\mathbf R)
 =\mathbf\Omega_2q_3.
\tag{4.2}
\]
A última igualdade é algébrica: o produto omitido tem cinco fatores horizontais \(\tilde\xi\) em dimensão quatro e é zero. A componente (1,4) é, assim,
\[
[\mathbf\Omega_2q_3]^{1,4}
 =s[\boldsymbol\alpha_1q_3]^{0,4}
  +d[\boldsymbol\alpha_1q_3]^{1,3}.
\tag{4.3}
\]
A fórmula paga o representante misto inteiro, incluindo coeficientes suaves e a globalidade da primitiva do alvo.

O contratermo de forma 4 envolve φ*α₁∧CS₃. Ele pertence à álgebra local que admite conexões e contratermos gauge-variantes. **Não pertence automaticamente ao subcomplexo de formas estritamente Lorentz-invariantes que proíbe Chern–Simons.** Se essa restrição adicional for imposta, (4.3) deve ser classificado como uma primitiva na álgebra ampliada; não se pode anunciar sua existência na álgebra restrita. Essa é uma distinção entre cohomologia BRST usual e cohomologia invariante, não uma anomalia nova demonstrada.

A própria Ω₃ precisaria de um fator total de grau 2. Não há gerador de Lie de grau 2 para Lorentz; não há forma fechada não exata de grau 2 no alvo; e a gravidade métrica não possui polinômio invariante linear na curvatura, pois tr R=0. Formas extras, gauges abelianos ou restrições diferentes podem alterar essa análise e não fazem parte desta ação.

## 5. Um teorema de redução do grau total 5

Abaixo está uma demonstração **condicional precisa**, útil para fechar a lacuna restante sem assumir a conclusão inteira.

[INPUT — contratos algébricos] Considere a álgebra covariante A₂ em variáveis tensoriais, antifields covariantes, quatro ghosts de translação \(\hat\xi^a\) e ghosts de Lorentz \(\hat C\). Admita:

1. A resolução KT ordinária e a redução de \(s_0=\delta+\gamma_L\) valem na classe C∞(S³)[jatos] considerada, com primitivas covariantes na mesma classe.
2. Toda 2-forma tensorial nessa classe que é fechada módulo as equações Einstein–sigma é exata módulo essas equações, por uma 1-forma tensorial na mesma classe:
\[
H^2_{\mathrm{char,cov}}=0.
\tag{5.1}
\]
Quando se pretende globalidade no alvo, a primitiva de (5.1) também deve ser global.
3. O diferencial se decompõe \(s=s_0+s_1+s_2\), de graus 0,1,2 em \(\hat\xi\), com \(s_1=\hat\xi^a D_a\), e a redução de Lie usa módulos tensoriais localmente finitos.

**Teorema.** Sob esses contratos, \(H^5(s,A_2)=0\). A prova não precisa de C0 sobre polinômios característicos de grau 4.

**Prova.** Complexificar a álgebra real de Lorentz dá
\[
\mathfrak{so}(1,3)_\mathbb C
 \simeq\mathfrak{sl}_2(\mathbb C)\oplus\mathfrak{sl}_2(\mathbb C),
\quad
H^*_{\rm CE}\simeq\Lambda(\theta_3^+,\theta_3^-).
\tag{5.2}
\]
Logo os únicos graus CE são 0,3,6, e o grau 3 tem duas cópias. A vanishing complexa implica a real por extensão fiel de escalares.

Seja α um s-cociclo de ghost total 5 e ℓ o menor grau de \(\hat\xi\). O contrato 1 permite remover sua parte \(s_0\)-exata. A parte mínima restante é um tensor invariante sem antifield vezes um cociclo de Lie. Os únicos casos são:

| Nível ℓ | Grau CE exigido, 5−ℓ | Possibilidade |
|---:|---:|---|
| 0 | 5 | zero |
| 1 | 4 | zero |
| 2 | 3 | \(B_2^+\theta_3^++B_2^-\theta_3^-\) |
| 3 | 2 | zero |
| 4 | 1 | zero |

No caso ℓ=2, a equação no nível seguinte é \(s_1\alpha_2+s_0\alpha_3=0\). Projetando sobre as duas classes independentes CE³, obtemos \(D B_2^\pm\approx0\). Pelo contrato 2,
\(B_2^\pm\approx D A_1^\pm\).
A diferença fracamente nula tem a primitiva KT da mesma classe, pelo contrato 1. Subtrair o s de \((A_1^\pm+\text{termo de antifield})\theta_3^\pm\) elimina o nível 2. O produto com \(s\theta_3^\pm\) só introduz níveis superiores. Nos níveis 3 e 4 a cohomologia \(s_0\) é zero; eliminam-se ambos. Não existe nível 5, pois há só quatro \(\hat\xi\). Portanto α=sβ, com β da mesma classe. A indução tem no máximo cinco níveis, sem série infinita, sem ε=1 e sem recentramento de séries. □

O mesmo argumento em ghost total 2 mostra \(H^2(s,A_2)=0\) sob (5.1). Isso é útil para os produtos com as classes topológicas de vielbein de grau 3: não há fator de grau 2 que os complete até 5.

**O que esta prova paga.** Correntes Noether da isometria SO(4) e o volume topológico aparecem em grau horizontal 3; para contribuir aqui precisariam de CE², inexistente. A prova não exige classificá-los todos. A única passagem dinâmica residual no nível relevante é (5.1). A resolução δ ordinária, sozinha, não fornece (5.1).

## 6. Por que suavidade no alvo não invalida a etapa de Lie — e onde ainda importa

[DERIVED] Para ordem e grau polinomial fixados nos jatos diferenciados, há um número finito de tipos tensoriais de Lorentz. Os coeficientes f(y) são escalares para Lorentz local. Assim cada parcela tem a forma C∞(U)⊗V, com V módulo tensorial finito. As projeções e homotopias algébricas de Lie atuam em V, deixando f(y) intacta. A reunião por graus é localmente finita. Isso justifica a seleção de graus (5.2) também para coeficientes suaves em y; não se aplicou cegamente um teorema para módulos infinitos arbitrários.

Da mesma maneira, δ e γ_L anulam funções somente de y. Se a resolução \(s_0\) está construída em cartas do alvo com limites finitos de ordem/grau para o elemento em questão, uma partição de unidade finita em S³ cola suas primitivas \(s_0\), porque \(s_0\rho_i(y)=0\). A compacidade permite uma cobertura finita. Esta observação serve à etapa \(s_0\); ela **não** cola automaticamente primitivas de s completo ou de d:
\[
s\rho_i(y)=\xi^\mu\partial_\mu y^A\partial_A\rho_i,\qquad
d\rho_i(y)=d y^A\partial_A\rho_i.
\tag{6.1}
\]
Os termos extras de (6.1) são exatamente o motivo para não deduzir globalização relativa a partir de um certificado KT de carta.

O contrato (5.1) tem duas rotas concretas possíveis: estender o resultado característico covariante de BBH à classe suave atual, ou provar a comparação com parâmetros de redutibilidade e a ausência de parâmetros locais universais não triviais. Uma simetria Killing de um fundo especial não é um parâmetro universal que funcione para todos os jatos estacionários. Nenhuma dessas duas rotas foi presumida como concluída nesta nota.

## 7. Da álgebra covariante a H^(1,4): mapa de contratos

Na apresentação BRST de gravidade, a substituição \(\xi^\mu\mapsto\xi^\mu+dx^\mu\) relaciona cociclos de ghost total 5 às descidas (1.1). Na análise usual também se separam os pares contráteis e a topologia dos valores do vielbein.

O setor puramente de valores não introduz uma classe de grau 5 neste exemplo:
\[
H^2_{\rm dR}(S^3)=H^5_{\rm dR}(S^3)=0,\qquad
H^*_{\rm dR}(GL^+(4))\simeq H^*_{\rm dR}(SO(4))
 \simeq \Lambda(\zeta_3^+,\zeta_3^-).
\tag{7.1}
\]
O produto S³×GL⁺(4) só tem graus 0,3,6,9, portanto tampouco tem grau 5. Isso é uma afirmação de de Rham sobre esse setor, **não** uma identificação automática de toda a cohomologia BRST com esse produto. O alvo participa do diferencial covariante \(s_1\); não foi extraído artificialmente como fator independente de A₂.

Para concluir \(H^{1,4}(s_\sigma|d)=0\) para todas as anomalias admissíveis, ainda é necessário justificar na mesma álgebra: (i) (5.1); (ii) a comparação descida/cohomologia de s após eliminação de pares; (iii) preservação da classe dos contratermos e compatibilidade entre cartas/gauge de Lorentz. Com esses contratos, o teorema da seção 5 elimina o setor covariante; (7.1) e \(H^2(s,A_2)=0\) eliminam os candidatos de valores e suas misturas. Este é um caminho de prova finito e específico; não é uma declaração de que todos os contratos já foram pagos.

A classificação perturbativa local trata transformações infinitesimais e coeficientes reais/complexos. Não classifica por si grandes difeomorfismos, holonomias de linhas determinantes, fases discretas, condições de bordo ou uma medida global interagente.

## 8. Controle gravitacional e controle global que não devem ser confundidos

[DERIVED] O setor de anomalias quirais gravitacionais usuais em quatro dimensões exigiria um invariante cúbico da álgebra de Lorentz, ou seja, um polinômio característico de forma 6. A álgebra de invariantes de \(\mathfrak{sl}_2\oplus\mathfrak{sl}_2\) tem geradores quadráticos; não há cúbico. Na representação vetorial, a identidade também é direta: \(R^T=-gRg^{-1}\) e as entradas de R têm grau par, logo tr R³=−tr R³=0. Esse controle não substitui a classificação dos possíveis termos dependentes da matéria; estes são tratados pelas seções 4–7.

[KNOWN — limite concreto da inferência global] Lee–Ohmori–Tachikawa, §2.5, discutem o alvo SU(2)≃S³: não há 5-forma, mas há uma escolha discreta de termo de Wess–Zumino no contexto spin, associada a \(\widetilde\Omega^{\rm spin}_4(S^3)=\mathbb Z_2\). O exemplo é de QCD/sigma com dados adicionais. Não demonstra uma anomalia deste Einstein–sigma bosônico e não introduz automaticamente uma escolha spin no modelo. Mostra precisamente que a ausência de classes diferenciais reais não autoriza dizer que toda questão topológica global desapareceu. A presente nota não escolhe nem calcula uma fase discreta para a TGL.

## 9. Fontes primárias e contratos de uso

As afirmações matemáticas desenvolvidas acima têm seus argumentos escritos; não são atribuídas como um teorema pronto sobre este modelo aos artigos seguintes.

- **BBH 1995**, *Local BRST cohomology in Einstein–Yang–Mills theory*, [hep-th/9505173v2](https://arxiv.org/pdf/hep-th/9505173v2). Locadores: §2, p. 9 impressa, define matéria polinomial; §5, teorema 5.1; §6, teorema 6.1; §7.2, (7.16)–(7.30); §9, (9.6)–(9.7); §10.4; apêndice E. O formalismo distingue cohomologia relativa, correntes e topologia do vielbein. Importa-se a organização algébrica; a ampliação suave do alvo e os contratos relativos não são apagados.
- **BBH 2000**, *Local BRST cohomology in gauge theories*, [hep-th/0002245v3](https://arxiv.org/pdf/hep-th/0002245v3). Locadores: §5; teorema 6.2; §6.4.3, teorema 6.6; §6.4.4, teorema 6.7. A passagem à cohomologia relativa tem hipóteses adicionais de normalidade e de classe de funções. Em especial, a formulação por séries nos campos não autoriza avaliar ε=1 ou recentrar uma primitiva formal.
- **Henneaux–Wilch 1998**, *Local BRST cohomology of the gauged principal non-linear sigma model*, [hep-th/9802118v3](https://arxiv.org/pdf/hep-th/9802118v3). Locadores: §§5–6, 10, 12–14. É um modelo com grupo do alvo gauged e ghosts internos; não é diretamente o nosso BRST difeomórfico. Serve como controle de que a topologia do alvo e a restrição a uma carta são operações distintas.
- **Giachetta–Mangiarotti–Sardanashvily 2000**, *Cohomology of the variational bicomplex on the infinite order jet space*, [math/0006074v1](https://arxiv.org/pdf/math/0006074v1). Proposição 13 e teorema 18 identificam a cohomologia horizontal off-shell abaixo do grau máximo e preservam ordem finita de jato. Não fornecem, por nome, a versão covariante on-shell da equação (5.1).
- **Lee–Ohmori–Tachikawa 2020**, *Revisiting Wess–Zumino–Witten terms*, [2009.00033v2](https://arxiv.org/pdf/2009.00033v2), §2.5, (2.29) e apêndice B.1. O uso nesta nota limita-se ao controle de torsão da seção 8.

## 10. Entrega e limites

[DERIVED] Pagos aqui: a descida tipada do volume; a exclusão de sua contribuição direta a (1,4); a primitiva do candidato Ω₂q₃; a preservação da etapa de Lie para coeficientes suaves; a preservação por média da simetria rígida do alvo quando a primitiva global já existe; e a redução finita \(H^5(s,A_2)=0\) sob o contrato (5.1).

[OPEN — nesta nota] A existência das primitivas relativas covariantes de grau 2 e a aplicação integral das comparações à álgebra global escolhida. A nota KT069 é evidência para o primeiro contrato da seção 5 em carta; não foi recaracterizada como prova dos restantes. A prova de ausência de anomalia exige ou verificar esses contratos ou construir diretamente a primitiva da anomalia efetivamente produzida.

Nenhum CAS, Lean, gerador de artigos ou finalizador foi executado para esta entrega. Ela não prova QME, estado interagente físico, completude UV ou resolução da gravidade quântica. Os limites são da demonstração realizada, não uma refutação do modelo.
