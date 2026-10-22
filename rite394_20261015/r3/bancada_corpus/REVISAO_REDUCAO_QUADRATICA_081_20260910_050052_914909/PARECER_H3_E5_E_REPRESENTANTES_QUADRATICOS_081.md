# Parecer081: cohomologia linear negativa e representantes quadráticos de Weyl

10/09/2026. Revisor /root/selected_geometry_design. Parecer novo e separado da entrega080. Nenhuma fonte antiga, original, memória ou arquivo canônico alterado; nenhum um.py, Lean ou CAS executado.

**Parecer favorável no alcance declarado; não identifiquei erro material na aplicação e na composição081.** Li integralmente [H3_E5_BIANCHI_E_REPRESENTANTES_QUADRATICOS_WEYL.md](<C:/IALD/Central de Patentes/Chatgpt/COHOMOLOGIA_QUADRATICA_WEYL_081_20260910/H3_E5_BIANCHI_E_REPRESENTANTES_QUADRATICOS_WEYL.md>) e o manifesto. Fonte medida: 18263 bytes, SHA-256 525d60c229e589fa57efe0fea2615c96291e6b7af321c799650416804d4a3f6d.

**Proveniência da revisão.** A fatoração diferencial079 usada como antecedente é de minha autoria. Portanto este parecer não é contado como aprovação independente daquele lema anterior. Reli suas fórmulas e o [parecer externo da raiz079](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_079_20260910/PARECER_SUBSETOR_ANTIFIELD_079.md>). A presente revisão é da nova aplicação pontual de Singer ao módulo linear e de sua composição com Sym⁵, invariantes e representantes quadráticos. Os pareceres080 permanecem antecedentes de alcance próprio; não eram aprovação antecipada081.

## 1. Normalização e obrigação efetivamente demonstrada

A mudança p=v0⁻¹g0g0h*, q=−C*/(2v0) é invertível na referência fixada. Com a conexão apropriada às densidades, v0 e os fatores métricos são paralelos e s-inertes. Os mapas ficam s0p=Hh e s0q=D p, com D=div. A Bianchi linearizada DH=0 usa a equação de fundo nula; não usa inversibilidade de H nem ausência de Killing.

Uma combinação linear de jatos de p tem coeficientes de ghost zero, sem geradores dinâmicos. Seu fechamento é a identidade PH=0 sobre jatos livres. A fronteira procurada é B[D p]=s0(Bq). O grau quatro de ghosts do uso079 não era parte do algoritmo de símbolos: a fórmula é linear nos coeficientes e aplica-se igualmente a esses coeficientes de grau zero, inclusive com índices tensoriais de saída.

## 2. Símbolo e aplicação pontual

Conferi a reprodução do lema de símbolo. O traço do símbolo de Einstein, em n≥3, fornece k·v=k² trA. A expressão no aberto k²≠0 serve apenas para anular a dupla curl polinomial; o aberto é denso e sua nulidade se estende como identidade polinomial. A primitiva final
B_b=(D_b−k_b S/[2(N−1)])/N, N=n+r,
divide apenas por inteiros positivos. Em r=0, A=0; em r≥1, B tem grau r−1. Na passagem ao símbolo da divergência, o fator é2B, devido à simetria dos dois índices do argumento.

O ponto novo do §4 está correto. Para P_x dado somente por seus coeficientes em um ponto, o ciclo significa (P_xH)[h](x)=0 para todo jato de h. Seu símbolo superior é, portanto, uma identidade polinomial e admite a mesma fatoração. Escrevendo os coeficientes à esquerda, B_x D atua por derivadas sobre D e sobre o argumento; não deriva uma extensão arbitrária dos coeficientes de P_x.

Como DH=0 vale como identidade diferencial na referência, (B_xD)H também se anula no ponto. Subtrair B_xD reduz a ordem no argumento e conserva o ciclo. Os termos inferiores de conexão/curvatura entram no novo resto. A indução termina no resto de ordem zero, que o lema força a zero. Não é necessário transformar previamente P_x em uma identidade global de operadores.

Isso fornece P_x=B_xD e uma primitiva linear B_xq com ordem no máximo r−1. A mudança dos pesos é consistente: p com r derivadas tem peso r+3, q com r−1 derivadas tem r−1+4=r+3. A construção é equivarante no ponto e natural quando os coeficientes iniciais o são. Está justificado H⁻¹(L,s0)=0 para o módulo linear inteiro no domínio fixado.

A presença de soluções Killing não contradiz esse resultado: uma solução particular R0k=0 não é uma identidade de operadores R0(fk)=0 para toda função f. Também não se trabalha modulo divergências, onde a questão das correntes e cargas é diferente.

## 3. Sym⁵ e o papel exato dos antifields

A cisão linear em cohomologia e pares contráteis dá H(S⁵L)=S⁵H(L), com a simetria graduada. Como os graus lineares não excedem1, os cinco fatores que somam ghost3 têm apenas dois padrões:
(1,1,1,0,0) e (1,1,1,1,−1).
Qualquer grau−2 deixa a soma máxima em dois. M=H⁰(L) é par e G=H¹(L) é ímpar; consequentemente surgem Sym²M⊗Λ³G e H⁻¹(L)⊗Λ⁴G, sem um termo omitido de C*. A nulidade demonstrada elimina somente o segundo somando. H⁻²(L)=0 não foi presumido nem é necessário.

Nos cortes finitos estáveis, a exatidão dos invariantes permite projetar ciclos e primitivas. Passar à união cobre todo elemento de ordem finita; não é uma troca com limite inverso. A extensão escalar R_her⊗R é aquela explicitada080, com K/κ fixados e diferencial escalar estendido. Ela conserva a cohomologia e mantém os coeficientes herdados; não é um teorema uniforme sobre um anel restrito de K variável.

Assim a fórmula(2) está justificada. Ela é uma apresentação cohomológica pelo módulo M real, e não uma base explícita do módulo quadrático.

## 4. Representante Q fechado off-shell

Os tensores W[1][h] são linearmente gauge-invariantes porque o Weyl da referência é zero. Portanto W[1][R0C]=0 para todo ghost livre, sem exigir Killing. A conexão de fundo é inerte, de modo que todos os seus jatos covariantes também são s0-fechados. C e m são representantes lineares fechados porque s0C=0.

A geração de M pelas classes dos jatos de Weyl fornece uma sobrejeção de um espaço de representantes fechados. A potência simétrica quadrática dessa sobrejeção continua sobrejetiva. Multiplicar por três representantes de G e tomar a parte invariante em um espaço tensorial finito fornece Q natural e exatamente s0-fechado, composto de dois fatores lineares de Weyl. Sua existência como representante de cada classe não exige liberdade dos jatos.

A nota preserva as relações: Sym²M é o quociente de Sym²J_W pelo subespaço gerado por n⊙z, com n no núcleo J_W→M. Bianchi, EOM e fronteiras não são apagadas. Assim fechamento off-shell de Q e relações on-shell de suas classes são duas afirmações compatíveis.

A igualdade b5=Q+s0χ5 é então a definição de igualdade de classes no mesmo complexo natural finito. A análise das espécies de χ5 está correta:
h³C², h*hC³ e C*C⁴.
A primitiva mista h*hC³ produz tanto EOM quadráticas quanto antifields multiplicados por R0C. Por isso a redução não exige que o pedaço antifield do b5 original feche sozinho. Isso constitui o avanço além do subsetor puro079, sem apagar antifields do complexo ou proibi-los nas fronteiras.

## 5. Diferencial seguinte e limites

Em C5, subtrair sχ5 substitui o representante b5 por Q. Em C6, sua componente s1χ5 não deve ser apagada; a identidade s1s0χ5=−s0s1χ5 garante que a classe do defeito seguinte é [s1Q]. Essa observação torna correto o problema(22), mas não calcula seu valor.

Não foi demonstrada uma base completa ou dimensão finita de Sym²M. O fato de G ter dimensão dez não elimina produtos de jatos altos de Weyl que possam conter tipos pequenos. A exclusão de derivadas superiores do problema LINEAR em E4 não é reutilizada para o produto quadrático. Essa ressalva é necessária e está presente na fonte.

O parecer vale para zeroformas pontuais, complexo métrico mínimo, espaço-forma Lorentziano orientado fixado, quatro dimensões, K>0, κ≠0, matéria constante projetada, escalares herdados inertes e jatos finitos por elemento. Permanecem fora: referência física φ=id, espectadores tensoriais, módulo uniforme em K variável, quociente modulo d_H, cohomologia global, restrições causais adicionais de scaling degree/contatos, QME, UV e fechamento geral.

**Conclusão:** H⁻¹ linear é pago pela fatoração explícita; a decomposição Sym⁵ e o representante quadrático fechado seguem no mesmo domínio. A estrutura explícita do módulo quadrático e a imagem de d1, inclusive a decisão de −[A6]∈δ(K), continuam abertas.

[REAL — documental] Pins e links conferidos em bytes, antes/depois. O creator foi lido somente em bytes para custódia, sem execução ou aprovação de sua implementação. As contagens do registro são documentais; zero novos controles CAS ou Lean.
