# Controle racional da álgebra CE — três assinaturas

10/09/2026. [REAL — execução exata finita] [DERIVED — alcance matemático delimitado].

O script constrói as dez matrizes X_ab, 0≤a<b≤4, com X_ab[a,b]=ε_a e X_ab[b,a]=−ε_b. Os comutadores determinam os coeficientes f_ij^k. O diferencial exterior é dθ_k=−Σ_(i<j)f_ij^k θ_i∧θ_j, estendido como derivação ímpar.

Os modelos medidos têm métricas (+++++), (−++++) e (−+++−), correspondendo a so(5), so(1,4) e so(2,3). A isotropia é o subgrupo nos quatro primeiros índices. Todas as contas são racionais: nenhuma tolerância numérica decide posto, núcleo ou igualdade.

Para cada grau q=2,3,4, o programa constrói as seis matrizes de ação L_ab da isotropia. O operador auxiliar é C=Σ ε_a ε_b L_ab². Todo invariante pertence a ker C. O código calcula uma base COMPLETA desse núcleo e verifica que cada vetor é anulado por TODAS as seis ações; isso prova a inclusão inversa nos casos calculados. Portanto não depende de supor positividade de um Casimir não compacto.

| Medida em cada assinatura | Resultado |
|---|---:|
| dim(Λ²W)^G | 0 |
| dim(Λ³W)^G | 4 |
| dim(Λ⁴W)^G | 3 |
| posto de d3 no espaço invariante | 3 |
| dimensão do núcleo invariante de d3 | 1 |
| posto de d2 sem impor invariância | 35 |
| posto de d3 sem impor invariância | 84 |

A forma de Cartan é construída separadamente como tr(X_i[X_j,X_k]) nos índices ordenados. Verificam-se não nulidade, invariância, fechamento e igualdade de sua linha com o núcleo calculado. O JSON conserva bases explícitas para os espaços invariantes, coeficientes da cúbica e todos os controles.

Há 420 verificações aritméticas registradas, distribuídas pelos três modelos. Boa parte confere a representação matricial e os comutadores; esse número NÃO conta 420 teoremas BRST. A identificação com H³(C3), com a imagem desde C4 ou C5, exige as demonstrações e os domínios das notas077. O cálculo finito não contém os campos físicos, antifields, todos os jatos, limite inverso ou anomalia interagente.

## Execução e falhas visíveis

A primeira tentativa, com o Python empacotado, falhou por ausência de Sympy antes de criar artefatos de cálculo. Foi copiado Sympy1.14.0 e mpmath1.3.0 somente para a nova pasta de dependências da bancada, usando pip --target, --no-cache-dir e --no-compile. O ambiente restrito bloqueou inicialmente a rede; a operação escalada autorizada terminou. As instalações existentes não foram alteradas; avisos do pip sobre pacotes globais já existentes não foram tratados como ação de reparo.

Uma tentativa posterior sob o ambiente restrito encontrou apenas o namespace do pacote, cuja leitura completa estava bloqueada, e parou com AttributeError antes de qualquer cálculo matricial. Ela criou apenas a pasta de saída vazia. Não foi registrada como aprovação ou resultado matemático.

O sucessor run2 preserva o código aritmético e muda somente o nome da pasta de saída, com proveniência medida. Executado com Python3.14, -B e a biblioteca copiada, sob acesso escalado de leitura, terminou com 420/420 verificações. A pasta vazia e o código anterior foram preservados. A execução não importou ou executou um.py.

O recibo mede o script, o resultado e metadados das dependências. Isso registra o ambiente utilizado; não pretende ser uma prova formal Lean ou uma custódia hermética de todo o interpretador.
