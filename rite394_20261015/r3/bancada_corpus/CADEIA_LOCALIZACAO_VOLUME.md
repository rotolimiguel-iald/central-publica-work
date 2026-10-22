# Cadeia de sítios, deslocamento e volume — demonstração anterior ao Lean

[DERIVED] Construções e obstruções para a ordem 003. Os estatutos de formalização serão discriminados na entrega. Os alvos não autorizam introduzir normalidade de um shift incompatível com o estado, nem um comprimento físico oculto.

## Convenções e rede

O andar `M_N` da bancada contém N+1 sítios. Portanto a relação correta é A({0,…,N})=M_N; A([0,N))=M_(N−1) para N≥1 e A(∅)=C1. A igualdade solicitada literalmente na ordem tem deslocamento de um índice e falha em N=0, pois M_0=M₂(C), não C.

Para um conjunto finito I⊂N, A(I) é a imagem no GNS do tensor de M₂ nos sítios de I e identidade nos demais. Inclua tudo em um andar K≥max I. A independência de K segue da inclusão a↦a⊗1. Então A(I)⊂A(J) se I⊂J, por inserir identidades. Se I∩J=∅, os fatores atuam em pernas distintas e comutam. A representação fiel, provada pela definitude GNS, preserva essas relações e discrimina sítios: dois geradores não comutativos de um sítio não podem ambos pertencer à álgebra de um conjunto que não contém esse sítio.

Para I finito e x em um andar que contém I, E_I(x) é o traço parcial ponderado pelas densidades dos sítios fora de I. Ele se estende a M pela mesma projeção GNS já demonstrada: H_I=A(I)Ω, p_I projeção, E_I(x)Ω=p_I xΩ. As ações esquerda/direita de A(I) reduzem H_I; a prova de compressão e positividade da entrega 001 se repete. E_I é normal, unital, completamente positivo, preserva ω e é bimodular. E_I E_J=E_(I∩J); para prefixos isto vira o mínimo dos andares. A ação modular produto preserva cada A(I), logo comuta com E_I. **Estender esses fatos em Lean exige construir as inclusões de sítios e identificar a fatia, não apenas repetir os campos do contrato.**

Para a cauda T_N=A({N,N+1,…})'', tome x∈∩T_N. Todo operador de suporte finito comuta com x. A esperança sobre um prefixo é então um elemento central do andar, portanto E_N(x)=ω(x)1. Como E_N(x)Ω→xΩ e Ω é separante, x=ω(x)1. Essa prova pode ser formalizada na interface da comutação com todos os andares; a igualdade entre uma apresentação por suporte da cauda e seu bicomutante ainda requer a construção da rede.

## Shift: o perfil precisa viajar com os sítios

No tensor algébrico/quase local, o deslocamento s(a₀⊗…⊗a_n)=1⊗a₀⊗…⊗a_n é unital, injetivo e tem imagem própria, independente dos pesos. Transporta A(I) em A(I+1).

No completamento de von Neumann, a distinção é essencial. Defina P⁺(k)=P(k+1). Há uma identificação normal da álgebra M(P⁺) com a cauda T_1(P), dada pela inserção da identidade no primeiro sítio. Isso usa a fatoração GNS H(P)≅H(P₀)⊗H(P⁺). **Não é automaticamente um endomorfismo normal de M(P) em si.** Para P constante, P⁺=P, e a identificação produz o endomorfismo normal próprio pretendido. Perfis não constantes podem permitir outra identificação, mas ela precisa ser provada; escolher uma isomorfia abstrata de fatores não garante que desloque os geradores prescritos.

Na forma correta, σ_t^P∘s_P=s_P∘σ_t^(P⁺). Num tensor elementar, ambos conjugam o fator a_k por diag(P(k+1),1−P(k+1))^(it). Para perfil constante isso é comutação exata. Para comparar σ^P com o mesmo perfil antes do shift, no andar finito a diferença é uma conjugação diagonal pelo produto das razões das densidades dos sítios adjacentes. No limite, não se presume que esse produto infinito convirja ou seja um unitário de M.

### Obstrução à extensão normal para perfis arbitrários

Escolha P(2k)=1/3 e P(2k+1)=2/3. Seja e_k a projeção |0⟩⟨0| no sítio k, e B_n=(1/n)Σ_(k<n)e_(2k). No estado produto,

    ω(B_n)=1/3,
    ||(B_n−(1/3)1)Ω||² = (2/9)/n →0.

As médias são uniformemente limitadas. Para todo operador local a, o comutador [B_n,a] tem norma O(1/n), pois só finitíssimos somandos encontram seu suporte. Logo B_n→(1/3)1 fortemente em H, pela densidade de aΩ. O mesmo argumento nos sítios ímpares dá s(B_n)→(2/3)1 fortemente.

Se existisse um endomorfismo **normal** unital ρ de M(P) que enviasse cada e_k em e_(k+1), a continuidade ultra-fraca em conjuntos limitados implicaria ρ(B_n)→(1/3)1 ultra-fracamente. Mas ρ(B_n)=s(B_n) tem limite (2/3)1. Contradição. Portanto o pedido universal não é válido na categoria normal. Isso não prova a inexistência de endomorfismos não normais, nem de shifts sob perfis adequados; identifica exatamente a hipótese necessária para a construção padrão.

Para P constante, ρ^n(M)=T_n forma uma cadeia decrescente de imagens próprias, com interseção C1. A inclusão é modularmente invariante para **todo** t, não apenas para um semieixo. Ω não é cíclico para a cauda em H: T_1Ω vive em Ω₀⊗H_tail, subespaço próprio. Assim nem mesmo esse shift estacionário é automaticamente uma inclusão modular meio-lateral standard no sentido de Borchers/Wiesbrock. Faltam standardness, translações contínuas com gerador positivo e a relação de dilatação; o semigrupo discreto não as fornece.

## Volume: objeto positivo, não uma falsa projeção

O candidato natural é q_I=Σ_(i∈I)e_i. Trata-se de um operador positivo local. Para conjuntos disjuntos, q_(I∪J)=q_I+q_J, e

    ω(q_I)=Σ_(i∈I)P(i).

q_I não é em geral projeção: e_i e_j≠0 para sítios distintos; no produto fiel, ω(e_i e_j)=P(i)P(j)>0. Mais fundamentalmente, nenhuma família de projeções de M pode satisfazer ω(q_I)=C|I| para todos os intervalos finitos com C>0, pois ω é normalizado e 0≤ω(q)≤1 para qualquer projeção, enquanto C|I| não é limitado.

Se P(i)=p em todos os sítios, a calibração exata é ω(q_I)=p·Vol(I), Vol(I)=|I|. Para perfil variável, a proporcionalidade com uma única constante para todos os singletons exige P constante, e isso também é suficiente. Uma alternativa q̃_I=Σ e_i/P(i) dá ω(q̃_I)=|I| para qualquer perfil fiel; a unidade é então escolhida pela normalização dos objetos. Não é emergência de uma escala universal independente do estado.

Outra representação possível usa projeções ortogonais em l²(N) e o traço usual: Tr(q_I)=|I|. É legítima, mas esse traço é de B(l²), não o traço dual do core da torre. Também não se identifica com o estado normalizado ω. A ponte disponível na cadeia é uma contagem calibrada de sítios, não `τ_core(q_O)=C Vol_g(O)`.

Para a versão contínua faltam: localização em variedade, regra de limite e espaçamento físico, ligação com densidade de volume/área, identificação do peso/traço e sua unidade. A obstrução de escala conforme da entrega 001 permanece.
