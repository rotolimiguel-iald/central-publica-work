# Fator antiunitário polar do S original — DEV

2026-09-12T12:48:37-03:00. [REAL — três módulos/16 alvos compilados; revisão e integração pendentes]

O domínio D(B)=D(S) e a igualdade de normas já passaram pela revisão independente
de seis módulos/25 alvos. No mesmo ScalarGNSHilbert P, a raiz B é auto-adjunta,
densamente definida e tem núcleo zero. Um vetor ortogonal à imagem de B pertence
ao domínio do adjunto, com B†z=0; auto-adjunção e núcleo zero dão z=0. Logo Ran B
é denso. Isso não afirma que Ran B=H_I ou que haja inverso limitado/gap.

Sobre D(B), f(x)=Sx é conjugado-linear e tem norma igual à de Bx. Mathlib
LinearMap.extendOfNorm estende a regra U(Bx)=Sx a um mapa conjugado-linear contínuo
em todo H_I. A identidade das normas estende-se por densidade. Ran S contém
D(S), pela involutividade de S; portanto Ran f é denso. A imagem da isometria U
é fechada por completude e contém Ran f, logo U é sobrejetiva e antiunitária.

A aplicação concreta não recebe antiunitário, densidade das imagens ou igualdade
das normas como premissas novas: usa P e os resultados construídos. Conclui
Sx=U(Bx) para TODO x∈D(S), preservando o espaço, as inclusões e o operador S.
Todos os 16 alvos dependem somente de propext, Classical.choice e Quot.sound.
Tentativas rc1 ficam no manifesto, excluídas da evidência aceita.

[OPEN] Este pacote NÃO prova U²=I, a identificação de U como conjugação modular J,
o domínio máximo do peso, KMS, traço e escala dual, canto Three Locks nem
H1/H2/H3 físicos. Antiunitariedade e fatoração não são promovidas a essas condições.
O setor quântico interagente, o contrato completo consumido pelo gate e o runtime
integral também permanecem pendentes. As seis flags maiores não foram alteradas.

Mãe integrada `c2d6675fffdd6d96e2a8196d25b9170f69549dd75f7e411b633013c04c54dffe`; domínio DEV `7eb42a0f74036c38e00b964d95e7bc808f5abc8aa59bf172866654b30ab92c58`;
parecer do domínio `5674a2290dd57f8a670c4f11f9d8bc4904a36c151205bec40e36460b6620ae0c`. Cópia integrada ainda
`7ec13a8b82350390c7ef32d9319910398541b8966ecf5f28e928c492a626eb6a`. Nenhuma execução/importação do monólito.
