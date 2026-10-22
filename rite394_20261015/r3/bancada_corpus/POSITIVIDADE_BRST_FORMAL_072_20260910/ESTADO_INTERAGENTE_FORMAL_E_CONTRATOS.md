# Do estado linear positivo ao espaço físico interagente formal

10/09/2026, arco 072. [DERIVED — demonstração escrita e aplicação condicional]. Esta nota não altera o estatuto das fontes 067–071: não houve execução de um.py, Lean ou CAS, nem modificação de arquivos anteriores.

**Resultado:** sob uma representação auxiliar livre compatível com os campos Hadamard e uma implementação renormalizada da simetria por carga BRST, cada vetor físico livre admite um levantamento interagente formal. O quociente pela carga possui produto interno formal positivo; um levantamento normalizado do vetor do estado 067 define um estado positivo na álgebra física interagente admitida. A recorrência é explícita. Esta nota fornece também um certificado algébrico suficiente para a positividade/completude livre, por quartetos, e demonstra quando a nilpotência da carga decorre da identidade implementada. A compatibilidade entre esse certificado de Fock e os campos Hadamard locais permanece uma obrigação identificada, não deduzida da palavra “pseudocovariância”.

## 1. Modelo, entradas e objeto a construir

O modelo é a ação **ambiente** Einstein–sigma adotada nas fontes: campos independentes g e φ, alvo S³ redondo, ação física

\[
S[g,\phi]=-{1\over2\kappa}\int (R-2\Lambda)\,d\mu_g
 +{c\over2}\int g^{\mu\nu}h_{AB}(\phi)\partial_\mu\phi^A\partial_\nu\phi^B\,d\mu_g,
\]

com as convenções de curvatura das notas anteriores. Fixamos c>0, κc=4, Λ=3/4 e o fundo on-shell

\[
M=(0,\pi)\times S^3,\qquad
\bar g=dr^2-a(r)^2\gamma,\quad a=2\cos(r/2),\qquad \bar\phi=\mathrm{id}_{S^3}.
\]

O parâmetro formal z abaixo não é o tempo r. Trabalhamos em faixas temporais relativamente compactas do interior. A extensão a S³ inteira é geométrica; não é uma carta global dos cinco pesos positivos.

Entradas locais lidas:

- `HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912/ESTADO_FISICO_HADAMARD_E_CONTRATOS.md`: estado quase livre físico 067, redução completa S/V/TT e modos de grau ℓ≥2.
- `EXTENSAO_BRST_COMPLETA_20260909_220941_811364/EXTENSAO_BRST_E_CORRECOES_SUAVES.md`: pseudocovariâncias completas, Ward exatas, extrator EK=1 e split simplético de Cauchy.
- `CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md`: ação graduada, involução, antifields externos e diferencial livre.
- `CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md`: produtos temporais, campos de Bogoliubov e álgebra auxiliar local, com a quebra de Ward localizada.

O estado 067 possui espaço de uma partícula físico obtido da forma de Gram de seus modos. Sua Fock bosônica, ou equivalentemente a representação GNS desse estado quase livre, fornece o vetor Ω_phys com norma um. Os coeficientes cinéticos positivos e os modos baixos já foram tratados naquela fonte. Esta nota não os reconta ou recompila.

Há três objetos diferentes: a cohomologia de densidades locais H¹,⁴(s|d), a álgebra de observáveis de número fantasma zero e a cohomologia da **carga nos vetores de uma representação**. A última é o objeto principal aqui.

## 2. Contratos exatos e fontes primárias

[KNOWN] O resultado de estabilidade pertinente é [Dütsch–Fredenhagen, hep-th/9807078v2, Teorema 4, §§4.2–4.3](https://arxiv.org/pdf/hep-th/9807078v2), com normalização e estados nos Corolários 5–6. As hipóteses são uma carga simétrica e nilpotente num domínio auxiliar comum e, no nível livre, positividade de ker Q₀ com vetores nulos exatamente im Q₀. Não basta positividade numa subálgebra. A formulação resumida está em [hep-th/9807215v1, Teorema 1](https://arxiv.org/pdf/hep-th/9807215v1). A verificação específica de QED dessas fontes não é importada para Einstein–sigma.

[KNOWN] A ligação BV–carga em teorias locais é estabelecida, com hipóteses de QME e anomalia removida, por [Rejzner, 1301.7037v3, Teorema 4.2, equações (65)–(66)](https://arxiv.org/pdf/1301.7037v3). O enunciado é on-shell e inclui a correção quântica do diferencial. Ele não constrói uma representação positiva. A organização gravitacional por faixas de Cauchy compactas e a discussão condicional de estados aparecem em [Brunetti–Fredenhagen–Rejzner, §§3.4, 5 e Apêndice B](https://arxiv.org/html/1306.1058v4). Para evitar qualquer ambiguidade de notação na enumeração do §5, usamos as duas condições precisas de DF(4.8): no **kernel** livre, norma não negativa; nesse kernel, norma zero implica **imagem** da carga.

Fixe uma faixa J×S³, com fecho no interior de M, e uma função de corte χ=1 numa vizinhança dessa faixa. As hipóteses operacionais são:

**P₀ — representação livre.** Existe um domínio complexo graduado D, com forma hermitiana não degenerada [·,·] (antilinear na primeira entrada), representação da álgebra livre de campos e Wick, e operador ímpar Q₀:D→D. Todos preservam o domínio; Q₀ é simétrico nessa forma, Q₀²=0, e

\[
[\psi,\psi]\ge0\quad(\psi\in\ker Q_0),\qquad
\ker Q_0\cap\{\psi:[\psi,\psi]=0\}=\operatorname{im}Q_0.\tag{2.1}
\]

O quociente em ghost zero coincide isometricamente com a representação física 067 e possui um representante Ω₀ do vetor Ω_phys. A compatibilidade Hadamard inclui a realização dos campos compostos utilizados em 069. A forma não é positiva em todo D; exigir simultaneamente isso e uma carga simétrica nilpotente não nula seria contraditório.

**P₁ — operadores interagentes.** Os campos renormalizados localizados e a carga são séries de endomorfismos no mesmo D[[z]], com adjuntos para [·,·]. A carga tem ghost um,

\[
\mathsf Q(z)=Q_0+\sum_{n\ge1}z^nQ_n,\qquad Q_n^{\times}=Q_n.\tag{2.2}
\]

Não basta que cada coeficiente exista como distribuição numérica: seus produtos e ações nos vetores usados devem estar definidos no domínio comum. A realização de 069 é a entrada algébrica; P₁ explicita o seu consumo representacional.

**P₂ — identidade implementada.** O diferencial renormalizado d_z é nilpotente, preserva a álgebra local admitida e a sua involução graduada, e

\[
d_z A(z)={i\over\hbar_*}[\mathsf Q(z),A(z)]_{\rm gr},\qquad \mathsf Q(z)^2=0.\tag{2.3}
\]

Aqui ħ_*>0 é a unidade quântica fixada para a representação; não é uma avaliação de uma série infinita em ħ. A orientação de (2.3) pode ser convertida à convenção com [A,Q] por Q→−Q. Ela é compatível com o dicionário 069: d(A*)=(−1)^|A|(dA)*. A seção 4 mostra como deduzir a segunda identidade de (2.3), em vez de pressupô-la isoladamente, sob um contrato preciso de comutante.

As entradas QME e corrente de P₂ são condicionais aos passos de renormalização em curso. A prova de um H¹,⁴ nulo em uma álgebra maior não é marcada aqui como verificação de P₂ no espaço Q2.

## 3. Certificado livre: quartetos e a propriedade dos vetores nulos

Esta seção é uma construção algébrica efetiva; **não** é por si uma construção Hadamard de campos locais.

O split de Cauchy 068 fornece dados físicos pE e dois setores bosônicos de gauge/vínculo kF e rF; os complexos em ghost ±1 são exatos. As identidades qk=1, cr=1, qr=0, cp=qp=0 e EK=1 incluem os modos baixos, sem retirar arbitrariamente um núcleo. Esse é o conteúdo real que permite testar uma realização por quartetos.

Para cada índice de uma base de um espaço auxiliar G, introduza dois criadores bosônicos b†,c† e dois fermiônicos a†,d†. A letra c nesta seção é um oscilador, não o acoplamento sigma. As relações não nulas, e seus adjuntos, são

\[
[b_m,c_n^\dagger]=[c_m,b_n^\dagger]=\delta_{mn},\qquad
\{a_m,d_n^\dagger\}=\{d_m,a_n^\dagger\}=\delta_{mn}.\tag{3.1}
\]

Todos os aniquiladores matam Ω_aux, de norma um; a forma nos polinômios é definida por (3.1). As matrizes de uma partícula são cruzadas e não degeneradas. A realização pode ser obtida diagonalizando essas matrizes em assinaturas ± e tomando as Fock bosônica/fermiônica correspondentes. O produto interno é indefinido.

Atribua ghost(a†)=−1, ghost(d†)=1 e ghost(b†)=ghost(c†)=0. A involução conserva esses graus; ela não é a convenção em que o adjunto troca ghost e antighost. Defina, no domínio de partículas finitas,

\[
Q_{\rm qt}=\sum_m(b_m^\dagger d_m+d_m^\dagger b_m),\qquad
h_{\rm qt}=\sum_m(a_m^\dagger c_m+c_m^\dagger a_m).\tag{3.2}
\]

Os dois operadores são simétricos. Como [b,b†]=0 e {d,d†}=0, os termos do quadrado de Q cancelam: Q_qt²=0. Seus brackets graduados nos criadores são

\[
Q:a^\dagger\mapsto b^\dagger,\quad c^\dagger\mapsto d^\dagger,
\quad b^\dagger,d^\dagger\mapsto0;
\]
\[
h:b^\dagger\mapsto a^\dagger,\quad d^\dagger\mapsto c^\dagger,
\quad a^\dagger,c^\dagger\mapsto0.
\]

Consequentemente {Q_qt,h_qt} age como a identidade em cada criador e mata o vácuo. Pela regra de derivação, no monômio de grau auxiliar m age por m:

\[
\{Q_{\rm qt},h_{\rm qt}\}=N_{\rm aux}.\tag{3.3}
\]

Tensore esse domínio com a Fock física 067 e ponha Q₀=1⊗Q_qt. Seja P a projeção sobre F_phys⊗Ω_aux. A inversa de N_aux é definida apenas nos setores m>0; no setor m=0 usamos zero. Não aparece um inverso de frequência ou de um modo físico nulo. Para Q₀ψ=0,

\[
\psi=P\psi+Q_0\chi,\qquad
\chi=N_{\rm aux}^{-1}h_{\rm qt}\psi.\tag{3.4}
\]

P é ortogonal, Q₀P=0. Simetria e nilpotência dão [Q₀χ,Q₀χ]=0 e [Pψ,Q₀χ]=0; portanto

\[
[\psi,\psi]=\|P\psi\|_{\rm phys}^2.\tag{3.5}
\]

Isso prova (2.1) nesse domínio: se a norma é zero, Pψ=0 e (3.4) fornece uma primitiva. A imagem física tem ghost zero; não sobrevivem cohomologias extras de ghosts. A fórmula continua válida em um domínio maior de partículas finitas com funções de onda suaves, desde que os quatro operadores e P preservem esse domínio. As somas de (3.2) então representam as operações matriciais nos argumentos de cada função de onda, não uma soma de normas de vácuo.

**O que esta prova paga e o que não paga.** Paga um critério verificável para P₀ e um modelo algébrico de Fock cujo quociente é exatamente F_phys. Transportar os campos completos para esse domínio requer um mapa que preserve CCR/CAR, diferencial, involução e a condição Hadamard necessária aos campos compostos. O split simplético de Cauchy, sozinho, não garante que a polarização de quartetos tenha a orientação microlocal correta depois da evolução. A fonte 068 já adverte contra essa inferência. As pseudocovariâncias Hadamard daquela fonte e o certificado (3.4) não são declarados automaticamente a mesma representação.

Uma forma concreta de quitar esse resíduo é exibir uma polarização de uma partícula BRST compatível, com os blocos físicos 067, cuja diferença em relação às pseudocovariâncias 068 seja suave, e provar que seu Fock possui (3.4) no domínio de Wick/interações. Uma realização diferente que prove diretamente (2.1) nesse domínio também basta. Esta nota não presume tal diferença suave.

## 4. Faixa de Cauchy, corrente e nilpotência da carga

Uma corrente BRST renormalizada conservada na faixa J×S³ pode ser suavizada no tempo. Tome f∈C∞_c(J), integral um, e a 1-forma η=f(r)dr. Para a corrente como 3-forma J_BRST, escreva

\[
\mathsf Q_\chi=\int_M\eta\wedge J_{{\rm BRST},\chi}.\tag{4.1}
\]

O suporte é compacto porque S³ é compacta. Se dJ_BRST=0 na faixa, escolhas de f ali com a mesma integral diferem por derivada de uma função compacta; integração por partes mostra independência nessa faixa. Isso não é conservação através da região em que dχ≠0, nem passagem a um limite temporal assintótico. Corrente, contatos e identidade de implementação precisam ser os renormalizados.

**Lema da comutante.** Suponha que os campos A(z) da faixa implementem d_z por (2.3), que d_z²=0 ali, e que seus termos de ordem zero gerem no domínio a álgebra completa de Cauchy de uma representação Fock cuja comutante seja somente C·1. Então Q(z)²=0.

Prova. A Jacobi graduada fornece

\[
[\mathsf Q,[\mathsf Q,A]_{\rm gr}]_{\rm gr}=[\mathsf Q^2,A].
\]

Logo Q² comuta com todos esses campos. Se B(z) comuta com a família deformada, B₀ comuta com toda a família livre e é escalar; subtraia B₀·1 e repita na primeira ordem restante. Assim B(z) é uma série escalar. No Fock algébrico completo, a afirmação livre tem uma prova curta: BΩ é morto por todos os aniquiladores, portanto é múltiplo do vácuo; comutar com os criadores fixa B em todo o domínio polinomial. Finalmente Q² tem ghost dois, enquanto uma série escalar tem ghost zero. Como a graduação é direta, Q²=0. Não é necessário supor de antemão um vácuo interagente aniquilado por Q.

Este lema não pode ser aplicado usando somente uma pequena região O cuja comutante inclua campos causalmente separados. A faixa contendo a Cauchy inteira é o dado que evita esse salto. Também exige compatibilidade da graduação e ausência de uma extensão central de ghost dois na representação escolhida. Se esses contratos não estiverem demonstrados, mantém-se Q²=0 como hipótese explícita em P₂.

## 5. Recorrência dos vetores e positividade formal

Trabalhe primeiro sobre C[[z]], z*=z, estendendo [·,·] por convolução dos coeficientes. “Positivo formal” significa uma série zero ou de primeira potência não nula **par**, com coeficiente positivo. Equivalentemente, a série é c(z)*c(z). Isso é mais preciso que exigir uma constante positiva; também inclui vetores cujo primeiro componente físico aparece em uma ordem superior.

### 5.1 Levantar qualquer vetor livre fechado

Escolha uma inversa direita linear R₀:im Q₀→D de Q₀, preservando o grau pertinente. O certificado de quartetos fornece uma escolha por (3.4); em geral essa escolha algébrica é parte da realização de P₀. Para ψ₀∈ker Q₀, procure

\[
\Psi(z)=\sum_{n\ge0}z^n\psi_n,\qquad
Q_0\psi_n=-\sum_{j=1}^nQ_j\psi_{n-j}.\tag{5.1}
\]

Suponha ψ₀,…,ψ_N escolhidos e ponha

\[
\Psi^{(N)}=\sum_{j=0}^Nz^j\psi_j,\qquad
\mathsf Q\Psi^{(N)}=z^{N+1}r_{N+1}+O(z^{N+2}).
\]

Nilpotência dá Q₀r_{N+1}=0. Simetria dá a identidade exata

\[
[\mathsf Q\Psi^{(N)},\mathsf Q\Psi^{(N)}]
=[\Psi^{(N)},\mathsf Q^2\Psi^{(N)}]=0.
\]

Seu coeficiente de ordem 2N+2 é [r_{N+1},r_{N+1}]=0. Por (2.1), r_{N+1}∈im Q₀. Assim a próxima etapa está definida:

\[
\boxed{\psi_{N+1}=-R_0r_{N+1}
=-R_0\sum_{j=1}^{N+1}Q_j\psi_{N+1-j}.}\tag{5.2}
\]

Ela cancela exatamente a ordem N+1, sem modificar as anteriores. O limite é puramente z-ádico: cada coeficiente se estabiliza. Não se exige convergência numérica, e não se precisa introduzir uma hipótese independente H¹(Q₀)=0 nos vetores; a obstrução produzida pela recorrência já é nula e portanto exata por P₀.

### 5.2 Positividade e radical do quociente deformado

Para Ψ fechado, se [ψ₀,ψ₀]>0, a norma formal tem constante positiva. Se [ψ₀,ψ₀]=0, escolha χ₀=R₀ψ₀ e subtraia Qχ₀. O novo representante é divisível por z e continua fechado. A norma não muda, pois uma parcela exata é ortogonal a todo vetor fechado.

Repita o procedimento. Ou a primeira componente não exata aparece na ordem m, e

\[
[\Psi,\Psi]=z^{2m}\bigl(\nu+O(z)\bigr),\qquad \nu>0,
\tag{5.3}
\]

ou todas as componentes são removidas e Ψ=QΧ para uma série Χ. Portanto

\[
\mathcal H_z=\ker\mathsf Q/\operatorname{im}\mathsf Q
\]

tem forma positiva formal e radical zero. A construção não faz um quociente por uma imagem fechada em alguma norma topológica desconhecida: é a imagem algébrica z-ádica produzida coeficiente a coeficiente.

### 5.3 Módulo físico e não unicidade

Escolha representantes livres i:H₀→ker Q₀ e aplique (5.2) linearmente para obter I(z). Cada classe de H_z pode ser reduzida, ordem a ordem, por uma parcela I(z)h_n e uma parcela exata. Isso constrói uma identificação não canônica

\[
H_0[[z]]\longrightarrow\mathcal H_z.
\tag{5.4}
\]

Ela é injetiva: se o primeiro coeficiente h_m≠0 de uma série estivesse na imagem zero, o representante teria norma com primeiro termo z^{2m}||h_m||²>0, contradizendo a nulidade de um exato. É sobrejetiva pela eliminação descrita. Não se afirma que (5.4) preserve a forma livre sem correções, nem que haja uma escolha natural única de I. A homotopia R₀ e as escolhas de normalização são dados.

## 6. Estado e representação dos observáveis interagentes

Seja F_z a álgebra auxiliar on-shell representada no domínio de P₁. A álgebra física pertinente é

\[
\mathcal A_z=H^0(d_z,F_z).
\]

Uma classe fechada [A] age por [Ψ]↦[AΨ]. As identidades de P₂ provam que AΨ é fechado e que mudar A por d_zB, ou Ψ por QΧ, altera o resultado por um vetor exato. O mesmo cálculo mostra que qualquer representante BV fornecido por uma **comparação on-shell compatível** age dessa maneira. Não se identifica um antifield externo com um novo operador propagante.

Levante Ω₀ por (5.2). Sua norma é N(z)=1+O(z), real. A raiz inversa formal existe, determinada por N^{-1/2}=1−(N−1)/2+3(N−1)²/8−… . Ponha

\[
\Omega(z)=N(z)^{-1/2}I(z)\Omega_{\rm phys},\qquad
\boxed{\omega_z([A])=[\Omega(z),A(z)\Omega(z)].}\tag{6.1}
\]

Essa fórmula é independente de representantes, normalizada e hermitiana. Para A fechado,

\[
\omega_z([A]^*[A])=[A\Omega,A\Omega]\ge0
\tag{6.2}
\]

pela seção 5. A ordem zero é o estado 067, para observáveis que possuam um levantamento fechado com esse termo inicial. O novo estado não é em geral quase livre: sua série contém correções do vetor e dos campos.

O levantamento de **vetores** não prova que todo observável livre admita um levantamento **local** no espaço Q2. Se um A(z) fechado já foi construído e sua ação livre é não nula no quociente, a ação deformada permanece não nula: uma ação identicamente exata contradiz o termo livre, usando os levantamentos de todos os vetores livres. Isso protege observáveis admitidos; não inventa novos observáveis locais.

## 7. O parâmetro formal, ħ e a localização do estado

Na expansão 069, g=bar g+z h e φ=Exp_barφ(z ξ); um termo de n pernas e L laços da ação inicial de duas derivadas possui peso z^{n+2L−2}. Em cada peso fixo que contribui à carga ou aos campos polinomiais considerados, n≥0 e L são limitados; os termos constantes de vácuo não entram numa carga de ghost um. Assim, depois da organização dos campos relativos, cada coeficiente de z possui somente uma quantidade finita de potências de ħ e pode ser realizado para ħ_*>0 fixado. A prova sobre C[[z]] é suficiente para essa organização, desde que P₁ seja verificado.

Isso não é somar os laços a z=1. Para uma EFT com novos acoplamentos independentes ou para uma organização bivariada irrestrita em ħ e z, deve-se fixar uma filtração positiva localmente finita e uma noção de positividade do anel antes de repetir a prova. A prova univariada não é importada por chamar qualquer série de “formal”.

O estado (6.1) é construído para o cutoff e a faixa fixados. Se dois cutoffs dão isomorfismos * de álgebras físicas implementados por U e interligam suas cargas, podemos transportar o vetor por U e o estado por composição com o isomorfismo; positividade é preservada. Porém a existência de isomorfismos algébricos, sem essa escolha compatível, não torna iguais os estados obtidos separadamente.

Portanto não se deduz aqui um estado global independente de cutoff, um limite adiabático de Wightman, um vácuo preferido, um estado KMS, uma matriz S assintótica ou independência quântica de fundo. A compactação espacial facilita (4.1); ela não resolve por nome essas questões, nem autoriza levar a construção até a=0 ou H=0.

## 8. Balanço e próximo contrato mensurável

- [DERIVED] A identidade de quartetos (3.3) fornece certificado explícito para positividade e completude livre e um operador R₀, em sua realização algébrica.
- [DERIVED] A implementação numa faixa de Cauchy completa, com comutante escalar e graduação preservada, reduz a nilpotência da carga à nilpotência da derivação renormalizada.
- [DERIVED/KNOWN] Sob P₀–P₂, as fórmulas (5.2) e (6.1) produzem um quociente físico e um estado positivo interagente **formal**, conservando o estado 067 no termo inicial.
- [OPEN — representação] Exibir no sistema Einstein–sigma a compatibilidade Hadamard/Wick/domínio comum do certificado de quartetos, ou provar diretamente (2.1) na representação auxiliar usada para 069. A homologia de Cauchy 068 e a positividade física 067 são entradas fortes; não são essa verificação por si.
- [OPEN — renormalização] Construir as identidades de corrente/QME e a comparação on-shell no espaço Q2 efetivamente admitido, com os contatos e a involução corretos. As frentes cohomológicas 071/072 são pertinentes, mas esta nota não as antecipa como concluídas.
- [OPEN — globalidade] Compatibilidade dos estados nas mudanças de cutoff/fundo e controle das extremidades. Não tratados: anomalias globais, convergência ou completude UV.

O resultado condicional é operacional: fornecidos os coeficientes Qₙ e a realização livre compatível, cada ψₙ é calculado pela soma finita (5.2), e o estado segue por normalização. O enunciado não depende de identificar a fonte sigma com um estado de Gibbs, nem de atribuir à família probabilística P todos os graus de liberdade da extensão ambiente.
