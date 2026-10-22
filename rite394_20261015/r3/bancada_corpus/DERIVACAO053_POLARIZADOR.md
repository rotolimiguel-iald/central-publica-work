# Derivação053 — polarizador por projeção real
[DERIVED — registrada antes do fonte; sem alegação de compilação]

Data: 07/09/2026. Autor: agente responsável por SymplecticPolarizer.
Escopo: Hilbert complexo H, visto também como espaço com produto interno real,
e submódulo real R completo. Nenhuma instância da torre é construída aqui.

## Definição e sinal
Se P é a projeção ortogonal real sobre R, definir o operador ambiente
D = P ∘ (-i) ∘ P. A composição é linear real e limitada. Para x,y em R:
Re〈x,Dy〉 = Re〈x,-iy〉 = Im〈x,y〉.
O sinal menos é necessário com produto interno conjugado no primeiro argumento.
O operador D não é denominado conjugação modular, gerador modular ou horizonte.

A imagem está em R e a norma é no máximo um: P é contração e a multiplicação
por -i é isometria. A versão ambiente satisfaz
Re〈x,Dy〉 = Im〈Px,Py〉 e D é antissimétrico para o produto interno real.
Por definitude e densidade interna do próprio R, um z em R é Dy exatamente
quando seus pareamentos reais com todos os x em R são Im〈x,y〉.
Em particular, para y em R, Dy=0 se e somente se todos esses pareamentos
imaginários são zero. Não se identifica esse núcleo com um centralizador
neste módulo genérico; a identificação pertence à instância da torre.

## Família de formas
Para epsilon real, definir
h_epsilon(x,y)=Re〈Dx,Dy〉+epsilon Re〈D(Dx),D(Dy)〉.
A forma é bilinear real e simétrica. Se epsilon>=0, sua diagonal é
||Dx||²+epsilon ||D²x||²>=0, e é zero exatamente quando Dx=0.
Logo não é anunciada positividade definida no Hilbert inteiro nem no R inteiro.
O segundo termo não pode remover o núcleo do primeiro.

## Covariância
Se W é uma equivalência isométrica linear complexa de H e W(R)=R, a unicidade
da projeção mostra P(Wx)=W(Px): W leva a decomposição ortogonal em R e R-perp
para outra decomposição com as mesmas propriedades.
A linearidade complexa também dá W(-ix)=-iW(x). Portanto D(Wx)=W(Dx), assim
como D²(Wx)=W(D²x), e h_epsilon(Wx,Wy)=h_epsilon(x,y).

A hipótese W(R)=R será paga pelo implementador GNS da automorfia do horizonte,
em outro módulo. Não se supõe que o unitário original h.U fixe o vetor Omega.
Não se usa uma comutação modular adicional nem um teorema de Bisognano-Wichmann.

## Contrato de implementação
Importações exclusivamente Mathlib. Namespace ChatgptAudit.Covariant053.
Operador público symplecticPolarizer R : H ->L[real] H; formas polarizerForm
e polarizerFormBilin. CompleteSpace R é uma hipótese explícita; a completude
de H não é exigida adicionalmente. Cada declaração será seguida no censo por
#print axioms, sem instâncias anônimas, sorry ou desativação de linter.
A área física, a seleção de regiões e H3 continuam OPEN.
