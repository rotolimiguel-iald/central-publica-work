# Símbolo da divergência em todas as ordens finitas do Weyl quadrático

10/09/2026. Investigação086 NOVA. Autor: selected_geometry_design. [DERIVED — demonstração escrita, pendente de revisão independente específica]. [KNOWN — fatos planos localizados nas primárias abaixo]. Zero CAS, Lean ou execução/importação de um.py. As fontes anteriores permanecem intactas.

**Resultado proposto à revisão.** Na referência espaço-forma orientada em quatro dimensões, com K>0 real fixado, sem tensores espectadores e com coeficientes escalares herdados inertes, não existe vetor natural V, quadrático em classes de jatos de Weyl/EOM e de ordem finita, tal que

                         div_0 V = J_W.                    (A)

O detector é o termo de maior ordem de derivadas, e não a integral global de Pontryagin. A passagem ao graduado é demonstrada por estriteza das relações Einstein; não se presume liberdade da torre curva080.

Mais precisamente, o símbolo de divergência é injetivo em cada grau do espaço de vetores naturais quadráticos do módulo plano maior. A injeção do graduado curvo nesse espaço basta. A prova é na categoria ALGÉBRICA de elementos finitos; séries de ordens infinitas, coeficientes tensoriais externos ou operadores ainda dependentes de K variável não entram.

## 1. Categoria e o primeiro controle: a integral ordinária não separa

Mantenha Mcal=ker γ/E, com U o espaço das expressões lineares em jatos de h, E a imagem dos jatos de Hh e γ induzido por h↦R0C. São os objetos080–085. N=Rher⊗Sym²Mcal. O anel Rher é uma álgebra real unital inerte depois de fixar o operador; nilpotentes são permitidos.

Uma corrente aqui é V∈(N⊗V0)^h. Isso exige invariância gauge no módulo efetivo, além de covariância simultânea do fundo e do campo. Não se identifica essa classe com todas as expressões tensoriais locais em h e g0.

Há uma obstrução concreta ao detector integral mais imediato. Para um h global e g(ε)=g0+εh, tome a conexão de Levi-Civita na apresentação GL sobre o mesmo fibrado tangente,

A(ε)=Γ(g(ε))−barΓ=εL+ε²L2+… .

A diferença é uma End(TM)-valued uma-forma global. A transgressão ordinária fornece

tr(R(g(ε))∧R(g(ε)))−tr(R0∧R0)
 = d[2tr(A∧R0)+tr(A∧Dbar A)+(2/3)tr(A³)].               (1)

Nesta apresentação ambas as conexões são sem torção no mesmo coframe e0, logo A^a_b∧e0^b=0. Como R0^b_a=K e0^b∧e0_a, tr(A∧R0)=0. Além disso tr(R∧R)=tr(W∧W) para conexões métricas em dimensão quatro e W(g0)=0. O coeficiente ε² de(1) é, portanto,

                   tr(W[1]∧W[1])=d tr(L∧Dbar L).           (2)

Não se usaram EOM. Numa variedade fechada onde o h seja global e as hipóteses façam sentido, a integral do lado esquerdo é zero. O mesmo vale sob condições que eliminem o termo de bordo, por exemplo quando as perturbações de conexão relevantes têm suporte compacto. Não se está afirmando a existência de uma compactificação específica da referência ou de uma solução linear global não trivial nessa compactificação.

A primitiva de(2) é natural sob transformações simultâneas de h/g0, mas não é uma corrente gauge-invariante do módulo N. No símbolo plano, δ_vL=d(∂v); a variação de tr(L∧dL) contém tr(d(∂v)∧dL), uma derivada exterior em geral não nula. Invariância apenas modulo d não é a invariância das classes lineares Mcal exigida em(A).

Se a conexão for antes transportada ao fibrado ortonormal de g0 por uma raiz S, a diferença não permanece sem torção no MESMO coframe e0. Nessa apresentação, o coeficiente de transgressão tem em geral 2tr(a2∧R0)+tr(a1∧Dbar a1). Não se apaga o primeiro termo só por usar o nome Levi-Civita. Essa diferença de apresentações não afeta o detector simbólico abaixo.

## 2. Filtração por ordem: K não recebe grau de derivada

Trabalhe primeiro sobre R, num ponto da referência. Ponha F_jU igual ao espaço de combinações dos jatos de h de ordem ≤j. K e todos os parâmetros já fixados têm grau ZERO para essa filtração. Ela mede ordem efetiva em h; não é a contagem de engenharia, na qual curvatura tem peso dois.

Os geradores p_I de antifield métrico têm grau |I|+2 e q_I têm grau |I|+3. Assim H e D têm mapas principais homogêneos de grau zero nas respectivas cadeias, pois H tem ordem dois e D tem ordem um. Em coordenadas normais, seus símbolos são o Hessiano Einstein plano e a divergência plana. Comutadores de derivadas e conexões entram estritamente abaixo da ordem principal.

É essencial provar que o quociente curvo pelas EOM tem o graduado principal esperado. Apenas apontar para os símbolos de H não bastaria.

### 2.1. Estriteza da imagem de H

Seja e=P[Hh] uma combinação finita de EOM e prolongamentos, cujo resultado tem ordem ≤j em h. Se P tem ordem r e r+2>j, seu símbolo superior satisfaz

                       σ_r(P) σ_2(H)=0.

A [fatoração explícita079](<C:/IALD/Central de Patentes/Chatgpt/SUBSETOR_ANTIFIELD_PURO_079_20260910_041018_659161/ANTIFIELD_PURO_FATORACAO_BIANCHI_E_DELTA.md>), §§3–4, não precisa da identidade inteira PH=0 para este passo de símbolo: seu lema polinomial dá um símbolo de B de ordem r−1 com

                         σ_r(BD)=σ_r(P).

O fator dois da passagem do gradiente simetrizado à divergência está incluído em B. Quantize B por derivadas simetrizadas, com coeficientes à esquerda. Então

              (P−BD)H=PH,    ord(P−BD)<r,                  (3)

porque DH=0 como identidade diferencial completa. Os termos inferiores de conexão/curvatura são conservados. Repita até obter P' de ordem ≤j−2. Se j<2, o resultado só pode ser zero: no resto de ordem zero, o núcleo do símbolo Einstein em coeficientes constantes é zero.

Portanto

 E∩F_jU = {P[Hh] : ord P≤j−2},                            (4)

com o lado direito zero para j<2. Este é um enunciado sobre a imagem em U; não diz que H tenha inverso ou que toda solução de Weyl admita um potencial global.

A prova pontual segue a mesma indução de081. Não diferencia extensões arbitrárias dos coeficientes: eles ficam à esquerda, e DH=0 fornece a identidade necessária em todos os estágios. Tudo é finito, real e h-equivariante.

### 2.2. Identificação do quociente graduado e injeção suficiente

Por(4), as relações iniciais de E são precisamente os prolongamentos do símbolo plano Hflat. Assim

               gr(U/E) ≅ Uflat/Eflat.                      (5)

Dê a Mcal⊂U/E a filtração INDUZIDA. A inclusão é estrita por essa definição e fornece

                gr Mcal ↪ gr(U/E).                        (6)

Para um representante gauge-fechado de grau mínimo, a parte de maior ordem continua aniquilada pelo símbolo plano do operador Killing. Somar uma EOM não muda esse fechamento, pois HR0=0. Logo a imagem de(6) está no módulo plano gauge-invariante

                  Mflat=ker γflat/Eflat.                   (7)

Não foi afirmada sobrejetividade de gr Mcal→Mflat. Somente a injeção é usada adiante.

Derivar uma classe por bar∇ acrescenta no máximo uma ordem, preserva o ideal E e o fechamento gauge. No graduado de(5), a operação é a derivada total plana, incluindo todos os índices dos jatos. Consequentemente a injeção(6–7) ENTRELAÇA as derivadas principais. Essa compatibilidade é necessária: uma mera injeção de representações de h, sem a derivada, não resolveria(A).

A filtração de Sym²Mcal é a filtração tensorial pela SOMA das ordens dos dois fatores. Sobre um corpo, gr Sym²Mcal=Sym²(gr Mcal), por cisões de espaços filtrados, ou pela exatidão de tensorizar e simetrizar. Ela injeta em Sym²Mflat. As peças em qualquer ordem são h-finitas; tomar invariantes e extrair o termo principal conservam a injeção. Não há limite inverso.

## 3. O módulo plano maior: geração e controle das relações

Complexifique apenas para decompor as representações de Lorentz; a conclusão retorna aos reais. Escreva (a,b) para os pesos inteiros 2j de sl2(C)⊕sl2(C), e V0,C=(1,1). O Weyl plano divide-se nas duas quiralidades ψ_ABCD e tildeψ_A'B'C'D'.

A geração plana por curvatura é a compatibilidade do operador Killing plano pelo Riemann linear (Saint-Venant). Ela é a versão plana dos argumentos de Calabi já usados080; a [primária de Khavkine](https://arxiv.org/pdf/1805.03751), §3, descreve esse caso de curvatura constante. Também se verifica diretamente no grau j: o produto de representações GL S^jV*⊗S²V* contém os diagramas (j+2),(j+1,1),(j,2); o mapa de gauge ocupa os dois primeiros, e o último é gerado pelas j−2 derivadas do Riemann linear. Para j=0,1 não sobra curvatura. As EOM Einstein planas equivalem a Ricci linear nulo em dimensão quatro e eliminam suas derivadas. Fica Weyl com Bianchi/divergência e seus prolongamentos.

Em spinors, essas relações dizem

              ∂^{AA'}ψ_ABCD=0,    e a conjugada.            (8)

A [primária de Anco–Pohjanpelto](https://arxiv.org/pdf/math-ph/0202019), equações(2.1)–(2.4), apresenta precisamente os jatos simetrizados como coordenadas do sistema plano de spin s. Usamos apenas esse fato linear para s=2, não a classificação global de suas correntes com tensores de Killing externos.

Para explicitar a redução: a decomposição de ∂_EE'ψ_ABCD separa a parte totalmente simétrica nos cinco índices sem prima e sua contração epsilon. A contração é a equação(8). Ao prolongar, as derivadas planas comutam; qualquer antissimetria dos índices primados de duas derivadas reduz a uma contração epsilon e a □ψ, que é zero como consequência de(8). Por indução, os únicos geradores de ordem r em Weyl são os spinors totalmente simétricos separadamente nos r+4 índices sem prima e nos r primados, e a quiralidade inversa:

              W_r^+=(r+4,r),   W_r^-=(r,r+4).              (9)

Eles têm ordem r+2 em h. O argumento dá um LIMITE SUPERIOR por esses dois módulos irredutíveis; não infere a liberdade da torre curva.

Para confirmar que nenhum desses módulos planos desaparece no quociente Einstein métrico, use ondas planas complexas. Tome p_AA'=λ_A tildeλ_A', e escolha tildeξ com [tildeλ tildeξ]≠0. O potencial

 h_AA'BB' = λ_A λ_B tildeξ_A' tildeξ_B'
              exp(i p·x)/[tildeλ tildeξ]²                  (10)

é sem traço e transversal, satisfaz Hflat h=0 e produz uma curvatura ψ proporcional a λ_Aλ_Bλ_Cλ_D exp(i p·x), com proporcionalidade não nula; a outra quiralidade é zero. A fórmula segue das duas derivadas de h: as contrações primadas dão [tildeλ tildeξ]², enquanto a curvatura oposta contém λ^Aλ_A=0. Um fator global não nulo pode normalizar ψ. Trocar os índices primados dá a outra quiralidade.

No ponto, o r-ésimo jato é proporcional a λ^(r+4) tildeλ^r. Variando os dois spinors, esses tensores puros geram a representação(9). Assim cada cópia é não nula e o limite superior é atingido no módulo plano. Ordens diferentes são graus distintos; não há relação plana não homogênea. Esta realização métrica verifica a passagem do sistema abstrato de spin2 ao quociente Einstein usado, sem escolher uma solução curva com jatos arbitrários.

A complexificação é lícita: uma identidade polinomial real que valha no quociente também vale após extensão a C. As ondas complexas são testemunhas algébricas do símbolo, não estados físicos ou uma continuação global da referência.

## 4. Todas as possibilidades para um vetor quadrático principal

O produto (a,b)⊗(c,d) contém (1,1) exatamente quando cada fator sl2 contém peso1: as diferenças dos pesos são no máximo um e as somas são ímpares. A multiplicidade, quando aparece, é um.

Aplicando a(9), o canal W_r^+⊗W_s^+ exige |r−s|≤1 e r+s ímpar; portanto |r−s|=1. O mesmo vale para --. Nos canais cruzados seriam exigidas simultaneamente

                   |r−s+4|≤1 e |r−s−4|≤1,

o que é impossível. Logo vetores só aparecem com uma quantidade ímpar 2r+1 de derivadas adicionais em Weyl, em

                   W_r^+⊗W_{r+1}^+,
                   W_r^-⊗W_{r+1}^- .                      (11)

Existe uma cópia por quiralidade. Por serem fatores de ordens distintas, cada cópia aparece uma vez na potência SIMÉTRICA total, sem duplicar a ordem dos dois fatores.

Não há vetor quadrático de ordem total menor que cinco em h: os dois Weyl já têm ordem dois cada, e o primeiro vetor exige uma derivada adicional. Este limite inferior é indispensável na comparação com J_W.

## 5. A divergência é não nula em cada cópia; não se trata só de contar tipos

Em W_r^+, a contração completa de dois spinors define o escalar S_r^+. A paridade da contração sob troca dos dois fatores é (−1)^((r+4)+r)=+1, portanto esse escalar pertence à potência simétrica. Defina S_r^- analogamente. A derivada plana grad S_r^± pertence à cópia vetorial correspondente de(11).

Mostramos que esse vetor e sua divergência não são zero como polinômios on-shell. Tome duas ondas da mesma quiralidade, com

 p=λ tildeλ,  q=μ tildeμ,
 <λμ>≠0,    [tildeλ tildeμ]≠0.                            (12)

Elas podem ser escolhidas separadamente por(10), logo sua soma é uma solução métrica plana. Polarizando S_r^+ nessa soma, o termo cruzado é um múltiplo NÃO NULO de

 <λμ>^(r+4)[tildeλ tildeμ]^r exp(i(p+q)·x).                (13)

Os sinais i das derivadas só multiplicam esse valor por uma constante não nula. O próprio produto tensorial spinorial garante que não há outro termo de mesma polarização que o cancele; os dois termos trocados coincidem porque a contração é simétrica.

Aplicar □ multiplica(13) por −(p+q)². Como p²=q²=0 e p·q é um múltiplo não nulo de <λμ>[tildeλ tildeμ], o resultado não é zero. Assim

                  div grad S_r^± ≠ 0                     (14)

em Sym²Mflat. Isso demonstra também que grad S_r^± gera a única cópia de(11).

As duas imagens são linearmente independentes: para separar a imagem +, use somente ondas +, fazendo todos os geradores − iguais a zero; a realização(10) permite isso. O teste oposto separa a imagem −. Não se usa uma avaliação real numérica para separar um anel herdado.

Consequentemente, em C e depois em R, a aplicação principal

 div_flat : (Sym²Mflat⊗V0)^h_degree_d
                    → (Sym²Mflat)^h_degree_(d+1)

é INJETIVA para todo grau d. Nos graus sem vetor, a afirmação é vazia. Nos graus d=2r+5 há as duas cópias de(11), ambas detectadas por(12–14). Esta é uma afirmação de injetividade de uma expressão de divergência, não apenas de sua classe modulo curls ou modulo integrais.

## 6. Transporte do detector e exclusão de todas as ordens finitas

Seja V um vetor curvo natural quadrático não nulo de ordem finita, sobre R. Escolha seu maior grau efetivo d na filtração INDUZIDA. Seu termo principal não é zero e, pelas injeções(5–7) e da potência simétrica, é um vetor natural no módulo plano maior. A derivada principal entrelaça essas injeções. Pela injetividade do §5,

                  gr_(d+1)(div_0V) ≠ 0.                  (15)

Logo div_0V tem grau EXATAMENTE d+1. Como d≥5, sua ordem total é pelo menos seis. O alvo J_W tem grau quatro: cada fator W[1] começa em duas derivadas de h, e sua parte principal é o Pontryagin Weyl plano. Esse termo não é zero no quociente plano: em duas ondas + de(12), a contração S_0^+ detecta a parte quiral correspondente de J_W, com coeficiente não nulo. Portanto gr_4J_W≠0.

Assim div_0V não pode ser J_W. V=0 tampouco serve. Isso prova(A) sobre R, sem determinar toda a torre curva e sem levantar dados de Weyl arbitrários a soluções curvas.

Sobre Rher, cada grau envolvido é uma extensão escalar de mapas reais. Tensorizar a injetividade principal por Rher preserva-a, porque R é um corpo. A mesma prova de maior grau funciona para um elemento finito com coeficientes herdados, inclusive nilpotentes. O alvo 1⊗J_W permanece não nulo numa álgebra real unital não nula.

A conclusão também mostra que não há vetor natural quadrático finito não nulo de divergência zero nesta categoria. Não contradiz correntes de energia, zilch ou superenergia com índices livres adicionais ou contrações com campos de Killing externos: esses objetos não pertencem ao espaço de vetores sem espectadores usado em(11).

A finitude é necessária: a prova escolhe um maior grau. Não autoriza uma conclusão sobre uma série com ordens ilimitadas, uma expressão não local ou uma localização em dados dinâmicos. A filtração ignora o peso de engenharia de K porque K está fixado; termos multiplicados por K podem mudar graus inferiores, mas não apagar o termo principal não nulo de um elemento.

## 7. Consequência condicional à revisão e limites da obstrução

A [nulidade de invariantes085](<C:/IALD/Central de Patentes/Chatgpt/INVARIANTES_QUADRATICOS_KILLING_085_20260910_060005_9363957/N_INVARIANTES_KILLING_ZERO_POR_KT_LINEAR.md>) remove N^g. A [forma normal084](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md>) reduz a exatidão de J_Wν no CE natural à equação(A). Com a prova simbólica acima, o alvo não é exato NESSE complexo e nessa categoria fixada.

Pela [transferência080](<C:/IALD/Central de Patentes/Chatgpt/TRANSFERENCIA_DELTA_PARA_E5_080_20260910/IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md>), isso obstrui o próximo levantamento do ramo e do líder ali fixados. Não foi afirmado um resultado sobre todo ramo possível, cohomologia global da teoria, admissibilidade Q2 de primitivas ampliadas ou coeficientes de uma anomalia quântica efetivamente calculada. O alvo considerado é o resíduo específico de ghost quatro; não se converte por nome numa anomalia física de ghost um.

A apresentação ordinária por conexão(2) continua exata e não contradiz o resultado: o detector distingue a classe natural GAUGE-INVARIANTE de Weyl/EOM da classe coordenada ou apenas simultaneamente covariante em h. Nenhuma solução física foi excluída pelo fato de esse ramo cohomológico falhar.

[OPEN — fora do alcance] Outras categorias com espectadores ou dependência espacial ativa, séries infinitas de jatos, o fundo físico sigma não constante, K variável, QME, UV e reconstrução geral. Não se conclui falsificação ou confirmação da TGL inteira. A presente demonstração escrita aguarda revisão integral independente antes de ser usada como resultado consolidado086.

## 8. Proveniência

As entradas locais principais são a fórmula explícita do núcleo principal e DH=0 em079/081, a geração por curvatura e a identificação das ações080/082, e as reduções084/085. As fontes foram medidas antes/depois, sem modificações. As primárias foram consultadas diretamente; nenhum hash de PDF local inexistente foi criado.

A classificação de uma derivada feita por Singer086 é compatível com r=0 de(11), mas não é usada como prova de todas as ordens. As mensagens curtas recebidas sobre a contagem e a transgressão não são apresentadas como revisão integral deste texto. A novidade que precisa dessa revisão é a sequência estriteza → injeção graduada com derivada → injetividade plana em todas as ordens → comparação de graus.

[REAL — documental] O manifesto registra os arquivos efetivamente medidos e as URLs primárias. O helper desta emissão apenas lê, mede e publica texto novo por temporário verificado. Zero execução matemática, CAS ou Lean; nenhum original, Atlas, memória canônica, selo ou gate foi alterado.
