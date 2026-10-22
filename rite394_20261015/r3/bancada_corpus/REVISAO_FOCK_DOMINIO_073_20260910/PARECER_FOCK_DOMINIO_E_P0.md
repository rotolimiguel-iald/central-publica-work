# Parecer independente sobre a composição Fock, Wick e P0

10/09/2026, arco 073. [DERIVED — revisão matemática interna por agente distinto do autor desta composição] [REAL — fontes lidas e pins medidos]. A fonte examinada é FOCK_DOMINIO_WICK_E_P0.md, da tarefa principal. Li-a integralmente, incluindo os contratos herdados da polarização. Não se atribui a este parecer uma revisão independente da polarização que eu próprio construí: para essa entrada, a revisão independente é a de outro agente, PARECER_POLARIZACAO_E_RADICAL.md, também lida integralmente.

**Resultado:** não identifiquei erro material na composição no fundo, domínio e classe polinomial compacta indicados. Ela realiza o contrato livre P0 depois de consumir os projetores e a majorante adaptados. A representação dos coeficientes de P1 é parcial no sentido declarado; P2, QME e a carga interagente renormalizada continuam abertos.

## 1. A identificação utiliza a covariância construída

A forma bosônica em (2) conserva exatamente o bloco A_067 e contém somente o pareamento cruzado ell G entre gauge e vínculos. O quociente pelo radical pode ser identificado com a imagem dos projetores puros. Como o radical é um subcomplexo direto, a construção não introduz as classes adicionais do contraexemplo da nota de radical.

Conferi a normalização com a seção 2 dessa nota: antes da rescalagem, as setas são a→ka e u→ell cu. Substituir r por r/ell deixa a segunda seta com coeficiente um e torna o pareamento gauge–vínculo igual ao pareamento ghost G. Isso não altera a forma original: é uma mudança explícita de coordenadas.

Escrevendo G(v,w)=(v,eta_K w)_K, com eta_K autoadjunta e eta_K²=1, compor simultaneamente os criadores c† e d† com eta_K transforma os dois pareamentos cruzados em (v,w)_K. O diferencial ainda leva c†(eta_K v) a d†(eta_K v). A mudança, portanto, conserva as setas e a função de dois pontos transportada. A forma auxiliar indefinida não é transformada em uma probabilidade física negativa.

As fases constantes dos ghosts são herdadas explicitamente do dicionário e da nota de radical. O adjunto é o de Krein nos campos; a involução cbar*=-cbar e o fator de paridade ao inverter [Q,A]_gr permanecem mantidos. Não é aplicada uma construção GNS positiva à álgebra auxiliar inteira.

## 2. Carga e homotopia

As relações cruzadas (5) fornecem as quatro setas de (7) e a identidade Q0 h+h Q0=N_aux. Nos produtos graduados, os termos de slots distintos se cancelam; os de um slot contam a partícula auxiliar. Os operadores são somas de mapas em cada slot, e não somas de criadores de pares de norma divergente sobre o vácuo.

Q0 e h são simétricos para a forma cruzada. A inversa de N_aux vale 1/m apenas em m>0 e zero no vácuo auxiliar; ela não exige uma inversa de frequência. A identidade Q0 R0+R0 Q0=1-P conserva o domínio suave.

Para um vetor fechado, Psi=P Psi+Q0 R0 Psi. Simetria e nilpotência anulam os termos exatos e cruzados da norma, dando [Psi,Psi]=||P Psi||². Se essa norma é zero, a parte física positiva é zero e a fórmula fornece uma primitiva no próprio domínio. A imagem não foi substituída pelo seu fecho desconhecido. Isso paga tanto positividade do kernel como exatidão dos vetores fechados nulos de P0.

## 3. O domínio completado em cada grau é necessário

A definição (6) usa funções de onda suaves conjuntamente em todos os argumentos de Cauchy, pelo produto tensorial nuclear completado em cada grau. Apenas a soma dos números de partículas é algébrica. Assim, a construção inclui as funções de onda emaranhadas que um Wick smeared pode criar; não fica restrita a somas finitas de tensores simples.

A majorante e os projetores preservam C-infinito e os mapas de split têm ordem espacial finita. As operações nos slots são contínuas nesse espaço nuclear. O domínio é denso na Fock e é preservado por Q0, h, R0 e P. Não se presume que k,c sejam limitados em um Sobolev D original não adaptado.

## 4. Estabilidade Wick: a condição de frente de onda usada é suficiente

No termo puramente criador de um Wick local testado por f suave compacto, todas as covariáveis de espaço-tempo dos kernels de meia onda têm a mesma orientação. Uma singularidade nos dados de Cauchy de saída, depois da integração, exigiria soma nula dessas covariáveis na variável integrada. Isso é impossível para covetores causais não nulos com orientação comum. As parcelas suavizantes e as derivadas dos campos não criam uma orientação contrária.

Quando há aniquiladores, a função de onda inicial é suave conjuntamente. A contração com suas variáveis de Cauchy fornece uma solução suave no espaço-tempo e nas variáveis remanescentes. O argumento das parcelas criadoras então se aplica, com multiplicação por esses coeficientes suaves.

Para um kernel polinomial compacto microcausal geral t_m, o critério é mais preciso que a soma no mesmo ponto: a condição microcausal exclui a tupla de covariáveis todas futuras ou todas passadas, **incluindo zeros nas entradas restantes**. Após as contrações suaves com as variáveis aniquiladas, uma singularidade de saída exigiria justamente uma tupla desse tipo no kernel t_m. Portanto também esses polinômios preservam o domínio (6).

A prova usa a propriedade pseudodiferencial da majorante e dos mapas de amplitude dentro do ramo Hadamard. Mera continuidade de um operador arbitrário em C-infinito não substituiria esse controle; a propriedade mais forte foi disponibilizada pela polarização. O suporte compacto de t_m/f e a compacidade espacial garantem a propriedade de suporte necessária aos pushforwards.

A conclusão é invariância do domínio e a identidade sesquilinear que representa a involução nele. Não é uma afirmação de limitação na Fock inteira, igualdade dos domínios máximos dos adjuntos fechados ou convergência de uma série não polinomial de operadores.

## 5. Alcance dos coeficientes interagentes

A seção 6 consome os coeficientes polinomiais microcausais compactos já construídos por Q2. As operações de produto, inversa da matriz S e Bogoliubov são finitas por coeficiente da filtração declarada; por isso podem ser representadas no domínio comum. Uma mudança suave de covariância tem isomorfia Wick finita em cada grau polinomial.

Esse argumento paga a existência representacional dos coeficientes indicados. Não prova que uma corrente candidata seja conservada, que implemente a identidade renormalizada ou que a carga interagente seja nilpotente. A fonte conserva precisamente essa diferença entre a parte representacional de P1 e P2. A recorrência 072 pode consumir o R0 agora realizado, mas ainda precisa dos coeficientes Q_n e das identidades de P2.

Também não foram afirmados positividade não perturbativa, estado global independente de cutoff, soma a z=1, completude UV ou quantização de todas as probabilidades P. O resultado livre usa a ação ambiente, o estado físico 067 e o fundo interior S3 da construção.

## 6. Limites desta revisão e custódia

Li a fonte Fock integral e o trecho de convenções/radical relevante. Conferi as identidades algébricas e o argumento de frentes de onda descritos acima. Não reexecutei a redução SVT067, o Jacobi066, a renormalização Q2 ou testes de natureza. O parecer da polarização é uma entrada independente separada, não uma aprovação minha da minha própria demonstração.

Nenhum Lean, CAS, um.py ou construtor anterior foi executado. Somente esta nota e seu recibo são novos nesta pasta. Os pins e a preservação byte a byte das fontes lidas constam do registro acompanhante.
