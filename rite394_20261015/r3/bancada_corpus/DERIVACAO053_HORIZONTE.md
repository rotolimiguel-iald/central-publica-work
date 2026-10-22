# Continuação053 — implementador GNS de todo horizonte
[DERIVED — derivação anterior ao fonte; nenhuma compilação053 afirmada]

Fixar SiteProfile P, H=TowerHilbert P, M=theFactorObject P e
h:TowerHorizon P. A automorfia alfa=adT h preserva M e o estado omega.
Não supor h.U Omega=Omega. O implementador procurado W_h é construído
a partir de alfa e do vetor cíclico, não identificado com h.U.

Primeiro, para A,B em M, estrela, produto e omega_adT dão
<alfa(A)Omega,alfa(B)Omega>=<AOmega,BOmega>.
Logo também as normas e distâncias GNS são preservadas em todo M.

No pré-Hilbert definir
Wpre([N,a])=alfa(towerPi P a)Omega.
O valor está em H, possivelmente fora de um nível finito: alfa não foi
suposta preservar os prefixos. A compatibilidade towerPi_compat mostra
que essa definição respeita o quociente TowerPre. As operações num nível
comum dão linearidade complexa; a identidade GNS dá isometria.
Estender Wpre por UniformSpace.Completion.extension ao H completo.
Pagar continuidade, fórmula na inclusão, adição, multiplicação complexa
e preservação da norma por densidade. Não usar Completion.map com
codomínio pré-Hilbert indevidamente.

Para A global em M, aproximar AOmega por towerExpectation P N A Omega,
usando expectation_omega_limit. A continuidade de W_h dá o limite à
esquerda; a isometria GNS de alfa em todo M dá o limite à direita.
Assim W_h(AOmega)=alfa(A)Omega para todo A em M, não somente para locais.
Aplicar a mesma fórmula a h.inv para provar inversas bilaterais,
portanto W_h é uma isometria linear complexa bijetiva; W_h Omega=Omega
segue de alfa(1)=1. Nenhuma existência de esperança nova é postulada.

Definir uma única realStateSubspace P: fecho topológico do span real dos
AOmega com A autoadjunto em M. Seus geradores pertencem por inclusão
no span e no fecho. A imagem de um gerador por W_h é gerador porque alfa
preserva M e estrela. Linearidade real e continuidade passam a propriedade
ao span e ao fecho. O horizonte inverso dá sobrejetividade nesse mesmo
subespaço. O fechamento fornece completude para projeção ortogonal real.

[OPEN] Este resultado implementa todas as simetrias TowerHorizon no
espaço GNS. Não constrói localização física, não identifica W_h com h.U,
não identifica o polarizador real com J ou com logDelta e não resolve H3.
Será a ponte para formas no quociente de direções efetivas na053.

Custódia: somente os novos DERIVACAO053_HORIZONTE.md e
HorizonGNSImplementation.lean em Chatgpt. Originais e selos ate052
permanecem somente leitura. Revisões exigem backup imediato dos bytes,
temporário verificado e substituição; nenhuma compilação fora do runner
pinado que será disponibilizado pela raiz.

Emissao UTC: 2026-09-07T05:01:54.942932+00:00
