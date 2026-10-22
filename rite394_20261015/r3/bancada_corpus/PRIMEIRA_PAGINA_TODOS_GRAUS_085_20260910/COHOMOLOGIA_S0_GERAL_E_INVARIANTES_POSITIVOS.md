# Primeira cohomologia de valência e invariantes em todos os graus polinomiais

10/09/2026. [DERIVED — nova demonstração escrita da raiz, pendente de revisão independente]. Esta é uma consequência adicional das provas anteriores, especialmente da exatidão completa do complexo linear paga085. Zero nova execução matemática, CAS ou Lean. Investigação086 excluída.

**Resultados no domínio fixado.** Denote por E a valência total e por q o número de ghost. Para os polinômios naturais finitos no setor métrico mínimo da referência de curvatura constante K>0, com escalares herdados inertes Rher,

H^q(s0)|_E = Rher ⊗ [Sym^(E−q) M ⊗ Λ^q G]^h,
se 0≤q≤min(E,10),                                      (1)

e o grupo é zero fora dessa faixa. M é o módulo linear Weyl/EOM, G é o módulo dos dez jatos de Killing, h=so(1,3). As potências simétricas de expoente negativo não aparecem.

Para m=E−q fixo, o primeiro diferencial induzido por s1 é o CE natural sobre N_m=Rher⊗Sym^m M. Além disso,

(N_m)^g=0 para todo inteiro m>0.                         (2)

Se P∈(N_m)^h, m>0, é um escalar homogêneo e ν a forma horizontal de volume em ghosts, então

Pν é exato no CE natural ⇔ P=div V
para um vetor natural V∈(N_m⊗V0)^h de ordem finita.       (3)

Esses são resultados sobre a primeira cohomologia de s0 e seu primeiro diferencial, não o cálculo da cohomologia total do BRST interagente. Não se estabelece uma solução de(3) para J_W ou para todo P.

## 1. Categoria e complexo linear inteiro

Mantemos a referência orientada Lorentziana de quatro dimensões, K real positivo fixado, κ real não nulo fixado, φ0 constante projetada, coeficientes herdados inertes e finitíssimos jatos por expressão. O escalar K não é uma variável ainda presente no operador. Não se acrescentam espectadores tensoriais ou coeficientes espaciais arbitrários à classe natural.

O complexo L das expressões LINEARES tem somente quatro graus de ghost:

L^−2 = jatos de C*,
L^−1 = jatos de h*,
L^0  = jatos de h,
L^1  = jatos de C.

Todos os seus geradores têm valência um, independentemente do número de derivadas. Com as normalizações invertíveis de077/081, o diferencial é o da cadeia q → p → h → C, com δq=Dp, δp=Hh e s0h=R0C. As identidades DH=0 e HR0=0 asseguram que é um complexo. Aqui q e p nesta cadeia são nomes auxiliares de antifields, diferentes do número de ghost q em(1) e do ghost vetorial p usado no CE.

A [prova085](<C:/IALD/Central de Patentes/Chatgpt/INVARIANTES_QUADRATICOS_KILLING_085_20260910_060005_9363957/N_INVARIANTES_KILLING_ZERO_POR_KT_LINEAR.md>), §2, paga dois fatos: PH=0 implica P=BD por fatoração finita de Bianchi; ZD=0 implica Z=0. Portanto H^−1(L)=0 e H^−2(L)=0. O diferencial h→C não muda esses dois núcleos e imagens: a aciclicidade KT usada para pagá-los é exatamente a parte negativa da mesma cadeia.

Por definição H^0(L)=M=ker(U→U_C)/EOM. A redução dos jatos de Killing da referência identifica H^1(L)=G=V0⊕Λ²V0, de dimensão dez, com valor de C e parte antissimétrica de ∇C. Os jatos superiores são fixados pelas relações de Killing e curvatura, não tratados como variáveis livres. Esta entrada é a já usada na [identificação082](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>).

Assim H(L)=M em grau zero mais G em grau um, sem outros graus. M conserva TODAS as relações das EOM, traços, Bianchi e prolongamentos. Nada exige que sua torre de Weyl seja livre.

## 2. Potência simétrica graduada: prova de(1)

Trabalhe primeiro sobre R. A parte de valência E da álgebra polinomial de jatos é a potência simétrica GRADUADA S^E L. O diferencial s0 é linear nos geradores e estende-se por Leibniz, preservando E. Sobre um corpo de característica zero, o complexo linear cinde em sua cohomologia e pares contráteis.

Essa cisão pode ser usada elemento a elemento, ou via cortes estáveis finitos e fatorações finitas como081/085. Um polinômio contém somente finitíssimos geradores; cada preimagem linear escolhida é uma combinação finita. Na álgebra dos pares contráteis, a contração dividida pelo número inteiro positivo de fatores de pares elimina precisamente os monômios que contêm esses fatores. Não introduz valência diferente nem uma série de derivadas.

Equivalentemente, a fórmula de Künneth sobre R identifica a cohomologia de L^⊗E com H(L)^⊗E; a projeção graduada de simetrização divide por E! e é exata. Segue

H(S^E L)=S^E(H(L)) = S^E(M⊕G[1]).

Como M é par de ghost zero e G é ímpar de ghost um, a parcela de ghost q é Sym^(E−q)M⊗Λ^qG. Ela é zero para q<0, q>E ou q>10. Também cobre E=0: só q=0 dá R.

Para a classe natural toma-se a parte h-invariante. Os cortes de ordem dos jatos são finitos sob h, e a imagem no quociente continua localmente finita. As potências simétricas e exteriores preservam isso. A completa redutibilidade finita de h torna exata a operação de tomar invariantes, e a união filtrante conserva essa exatidão. Logo H((S^E L)^h)=H(S^E L)^h. Não se exige finitude sob a álgebra g inteira, cujas transvecções elevam a ordem.

Por fim Rher é uma extensão escalar real inerte. A planura sobre R e a mesma finitude dos elementos dão(1), inclusive com nilpotentes em Rher. Este passo não afirma que invariantes comutem com produtos completados de outra categoria.

## 3. O primeiro diferencial em cada m é o mesmo CE

O diferencial induzido por s1 aumenta E e q de um, conservando m=E−q. A [prova082](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>) estabeleceu identidades nos GERADORES:

d p = −Mghost p,
d Mghost = −Mghost²+Kpp♭,
d [∇^rW] = p^a[∇_a∇^rW]+r_h(Mghost)[∇^rW].

O símbolo r_h inclui todos os índices tensoriais e de derivadas. As correções omitidas nessas expressões são s0-exatas, com primitivas finitas explicitadas naquela prova. Mghost é a parte antissimétrica de ∇C; não é o módulo M.

Essas identidades não usam que o produto tenha exatamente dois fatores de Weyl. Tanto s1 quanto o CE são derivações graduadas. Para um produto finito de m representantes s0-fechados, a diferença das duas ações é uma soma finita de termos s0-exatos multiplicados por representantes fechados; portanto continua s0-exata, com primitiva finita. As relações de M são preservadas pela naturalidade/isometria já paga082.

Isso demonstra, para todo m≥0, que a cadeia em q dada por(1), com o primeiro diferencial, é

C^•(g,N_m)^h,  N_m=Rher⊗Sym^mM.

É o CE invariante, com os ghosts verticais Mghost presentes, não o CE relativo obtido simplesmente apagando-os. Esta identificação vale no primeiro diferencial; termos s2,s3,... e suas relações continuam necessários na teoria interagente.

## 4. Invariantes de qualquer grau positivo: prova de(2)

A prova085 não precisa do número dois em sua passagem pelo grau zero horizontal. Para deixar isso explícito, seja m>0. A inclusão M↪U/EOM, sobre R, implica a inclusão Sym^mM↪Sym^m(U/EOM), pois uma inclusão de espaços vetoriais cinde. Como as EOM são lineares, Sym(U)/(EOM)=Sym(U/EOM). Não há radicalização de um ideal nem hipótese de liberdade da torre Weyl.

Um elemento n∈(Sym^mM)^g é h-invariante e possui representante homogêneo natural F de grau m, por uma cisão h-equivariante num corte finito. A ação das transvecções no ponto é a classe de ∇F. A invariância completa, o transporte por isometrias da espaço-forma e a naturalidade do representante fornecem d_HF=0 no quociente local on-shell de h.

[KNOWN — mesma importação delimitada085] A resolução KT estritamente linear, local e acíclica paga085 permite usar [BBH2000, Teoremas6.2 e6.5(i)](https://arxiv.org/pdf/hep-th/0002245v3): a cohomologia característica ordinária de grau zero, numa carta contrátil permitindo coeficientes suaves explícitos em x, consiste em constantes. A prova linear termina com ordem finita; não é a iteração por série formal do caso apenas linearizável.

Logo [F]=c no quociente on-shell auxiliar. Especializar em qualquer ponto devolve uma igualdade no ideal polinomial das MESMAS EOM, pois δ não age em x. O ideal é homogêneo e F tem grau m>0. Avaliar em h=0 força c=0. A inclusão simétrica dá n=0 no módulo original, sem exigir uma primitiva natural do elemento auxiliar.

Após fixar o operador, a ação em Rher é trivial. Para uma base de dez elementos de g, o mapa v↦(ρ_XAv)_A é injetivo no espaço real Sym^mM. Tensorizar por Rher preserva a injetividade e prova(2). Alternativamente, separar os finitíssimos coeficientes herdados por uma base REAL não é avaliá-los por homomorfismos numéricos; os nilpotentes são preservados.

Em particular, para a álgebra polinomial ALGÉBRICA de elementos finitos,

(Rher⊗Sym M)^g = Rher.

A ação preserva o grau, e uma soma finita invariante tem cada parcela homogênea invariante; as parcelas positivas são zero. A unidade de grau zero permanece. Não se afirma uma identidade para um produto completado sem declarar sua categoria.

## 5. Alvos horizontais de grau quatro: prova de(3)

A [forma normal084](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md>) usou somente local finitude sob h, a decomposição simétrica g=h⊕V0, os dois cociclos de Cartan de h e as identidades dp/dMghost. Cada N_m satisfaz as mesmas condições. Nenhum passo da eliminação vertical requer m=2.

Portanto, se Q∈C^3(g,N_m)^h e dQ é horizontal, a mesma prova finita dá

Q=q_V+ftr CStr+fE CSE+dR,
ftr,fE∈(N_m)^g.

Para m>0, ambos os coeficientes são zero por(2). Assim Q=q_V+dR. Aplicar d fornece dQ=(divV)ν. Reciprocamente, P=divV constrói a primitiva horizontal q_V. Essa equivalência é exatamente(3).

O caso m=0 é diferente: o canal Euler com coeficiente constante existe e dCSE=K²ν. Não foi excluído por(2), cujo enunciado exige m>0. A forma normal não se converte numa afirmação de que todo H³ do CE é horizontal: a hipótese dQ horizontal continua necessária.

## 6. Utilidade e fronteira

O caso m=2 recupera a investigação085: para J_W, a pendência é construir ou excluir uma corrente natural quadrática V com divV=J_W. A exclusão084 de c gradJ_W permanece, mas não esgota outras contrações ou derivadas superiores.

(1) descreve a primeira cohomologia em TODAS as valências finitas; não calcula H(s0+s1+...). (2) elimina invariantes positivos nesse módulo linearizado; não elimina invariantes de outra teoria nem afirma ausência de observáveis físicos. (3) reduz a exatidão de alvos horizontais homogêneos; não prova que sejam divergências ou que não sejam.

Permanecem por pagar a admissibilidade causal dos contratermos, os diferenciais e levantamentos posteriores, as demais anomalias, QME, a rota UV e o vínculo à reconstrução geral dos mesmos dados. Não se transporta a prova ao fundo físico φ=id ou a K variável. Nenhuma série infinita de jatos por elemento, completação inversa ou hipótese Mittag–Leffler foi usada.

[REAL — documental] O manifesto mede seis fontes antes/depois e esta nota nova. Os hashes são integridade de arquivo, não contagem de teoremas. Nenhum original, Atlas, índice, selo ou um.py foi alterado ou executado. A generalização da raiz aguarda revisão independente própria; a revisão da entrada quadrática085 não é apresentada como aprovação antecipada deste texto.
