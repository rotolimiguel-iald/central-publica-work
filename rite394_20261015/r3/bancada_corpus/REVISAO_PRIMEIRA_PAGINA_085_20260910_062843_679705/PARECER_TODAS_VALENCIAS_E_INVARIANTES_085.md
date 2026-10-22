# Revisão independente085: s0 em todas as valências e invariantes positivos

10/09/2026. Autoria: selected_geometry_design. [DERIVED — revisão matemática escrita]. [REAL — pins e preservação no recibo]. Zero CAS, Lean ou execução/importação de um.py. A investigação086 permanece fora.

**Conclusão.** Li integralmente a [nova nota da raiz](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIRA_PAGINA_TODOS_GRAUS_085_20260910/COHOMOLOGIA_S0_GERAL_E_INVARIANTES_POSITIVOS.md>) e o manifesto. Não identifiquei erro material nas três generalizações, dentro da referência e categoria finitas declaradas. Esta revisão é específica da passagem a todos os graus; a revisão anterior da entrada quadrática não foi tomada como aprovação automática.

## 1. Complexo linear e potência simétrica

O segmento negativo tem H⁻²(L)=0 pela ausência de identidades ZD=0 e H⁻¹(L)=0 pela fatoração PH=BD. A [nota085 de Turing](<C:/IALD/Central de Patentes/Chatgpt/INVARIANTES_QUADRATICOS_KILLING_085_20260910_060005_9363957/N_INVARIANTES_KILLING_ZERO_POR_KT_LINEAR.md>) pagou ambos no sistema KT linear; acrescentar o mapa h→C não altera esses dois grupos negativos. Em grau zero fica Mcal=ker γ/EOM, e em grau um fica o módulo de dez dados de Killing G. A presença de Killing não contradiz a exatidão negativa, pois os graus e operadores são distintos.

Para E≥0, a parcela polinomial é S^E L, com simetria graduada. Uma cisão de complexos sobre R ou Künneth seguida do projetor de simetrização por E! fornece

H(S^E L)=S^E H(L)=S^E(Mcal⊕G[1]).

Mcal é par e G é ímpar. Portanto a parcela de ghost q é Sym^(E−q)Mcal⊗Λ^qG. Isso confere inclusive nos extremos: E=0 dá somente R em q=0; q<0, q>E e q>10 dão zero. Não restou um termo antifield de grau negativo oculto.

Não se exige um complexo finito inteiro. Cada tensor de E fatores e cada preimagem linear escolhida usa finitíssimos jatos; a homotopia dos pares preserva E. Sobre R, não há uma obstrução de exatidão oriunda desse tamanho infinito. A nota não aplica o argumento a um produto completado de outra categoria.

Os módulos de ordem finita são h-finitos; tomar invariantes é exato neles e passa à união filtrante. Assim o resultado natural é

H^q(s0)|E=Rher⊗[Sym^(E−q)Mcal⊗Λ^qG]^h.

A extensão inerte por uma álgebra real é plana, inclusive quando essa álgebra contém nilpotentes. Nada usa local finitude sob g inteira.

## 2. Por que o primeiro diferencial estende-se a todo m

s1 eleva E e q em um, logo conserva m=E−q. A [identificação082](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>) forneceu as identidades nos geradores p, Mghost e nos representantes de cada jato Weyl, com diferenças s0-exatas e correções finitas. Ela não se restringiu a testar um produto quadrático específico.

Ao multiplicar finitíssimos representantes s0-fechados, Leibniz produz uma soma finita das mesmas diferenças. Cada parcela continua s0-exata, com o sinal graduado apropriado; os demais fatores são fechados. A ação nas relações de Mcal já é preservada pela representação de Killing. Logo o primeiro diferencial coincide com o CE em cada módulo N_m=Rher⊗Sym^mMcal.

Os nomes continuam distintos: Mcal é o módulo linear; Mghost é o ghost de isotropia; q de ghost é diferente do antifield normalizado q. A presença dos ghosts verticais faz deste o CE INVARIANTE C(g,N_m)^h, não o complexo relativo obtido por sua supressão.

Esta identificação não calcula s2 nem qualquer diferencial posterior. É uma cadeia em q para cada m, composta de valências E=m+q; não é um cálculo completo do BRST interagente.

## 3. Nulidade dos invariantes para todo grau positivo

A inclusão Mcal↪U/EOM é linear sobre R. Sua potência simétrica de qualquer grau finito m é injetiva. A identidade Sym(U)/(EOM)=Sym(U/EOM) depende apenas da linearidade das equações; nada aqui requer uma apresentação livre da torre Weyl.

Para n∈(Sym^mMcal)^g, escolhe-se em um corte h-finito um representante natural F homogêneo de grau m. As transvecções e a homogeneidade local do fundo fornecem d_HF=0 no quociente on-shell, como na prova quadrática. Nenhum passo dessa passagem exige m=2.

A aplicação linear finita de [BBH2000, Teoremas6.2 e6.5(i)](https://arxiv.org/pdf/hep-th/0002245v3) foi conferida na revisão específica085: a resolução KT local permite concluir que F é constante no quociente auxiliar. Para m>0, a homogeneidade e a avaliação no jato h=0 forçam essa constante a zero. A especialização em x retorna ao mesmo ideal pontual e a inclusão simétrica devolve n=0. Não é necessário naturalizar uma primitiva.

A extensão por Rher usa o mapa real v↦(ρ_Xv)_X para uma base finita de g e sua injetividade. Planura sobre R preserva seu núcleo zero. Não há avaliação numérica de coeficientes herdados, exclusão de nilpotentes ou localização de K.

Segue também (Rher⊗Sym Mcal)^g=Rher para a soma polinomial algébrica: a ação conserva m e cada soma é finita. A afirmação deixa intacto o grau zero e não presume uma passagem para produtos completados.

## 4. Critério de divergência e exceção m=0

A [forma normal084](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md>) utilizou somente h-local finitude, a decomposição simétrica de g e as duas transgressões de Cartan. Cada N_m atende a essas hipóteses. Não há na eliminação um produto de exatamente dois fatores que impediria sua repetição.

Para dQ horizontal, a forma normal contém q_V, dois coeficientes em N_m^g e uma fronteira dR. Quando m>0, os coeficientes são zero. Portanto Pν=dQ equivale a P=div V, com V finito natural. A recíproca é construída diretamente por q_V.

m=0 é corretamente excluído dessa simplificação: coeficientes constantes sobrevivem e o canal Euler tem diferencial K²ν. Tampouco a hipótese dQ horizontal foi removida. A nota não classifica todas as classes de H³ em outros alvos.

## 5. Escopo e precisão temporal

A conclusão abrange a primeira cohomologia linear e o primeiro diferencial em toda valência FINITA na referência fixada. Não afirma liberdade de Mcal, ausência de observáveis físicos, solução de div V=J_W, cohomologia interagente completa, QME, UV ou admissibilidade causal. Não transporta o resultado para φ=id, espectadores tensoriais, K variável ou uma completação não declarada.

Precisão aditiva sobre meu parecer quadrático085 anterior: sua última frase usou a expressão “entrega084 encerrada” antes de o recibo final daquela custódia estar disponível. A separação das investigações estava correta; essa palavra não deve ser usada como evidência de finalização naquele instante. A tarefa principal informou posteriormente a finalização efetiva084. Esta revisão não altera o parecer anterior nem substitui a verificação do manifesto da entrega084.

[REAL — documental] Foram medidos nesta janela a nota, seu manifesto, as seis fontes pinadas e o emissor de origem, antes/depois. O emissor foi somente pinado, sem execução. O recibo distingue essas comparações da revisão matemática escrita. Nenhum documento anterior foi editado e nenhuma rotina de um.py, CAS ou Lean foi executada.
