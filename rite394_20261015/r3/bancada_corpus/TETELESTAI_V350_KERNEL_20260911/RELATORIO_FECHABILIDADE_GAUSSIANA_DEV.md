# Fechabilidade do gráfico GNS original por transporte gaussiano

[REAL — Lean DEV, compilação autoral; revisão independente pendente]
O resultado deste pacote é

\[
(0,y)\in\overline{G_I}\implies y=0,
\qquad (x,y),(x,z)\in\overline{G_I}\implies y=z.
\]

Aqui G_I é exatamente `scalarTomitaGraph P`, já construído em H_I×H_I,
com H_I o fecho das órbitas do ideal `finiteDualLeftIdeal P`. Seu domínio
inicial usa `finiteDualStarCore P = I ∩ I*`. Não se troca esse gráfico
por um gráfico de estado nem se presume I=n_ν.

O pacote contém nove módulos e 49 declarações, todas com compilação rc0
e axiomas contidos em `propext`, `Classical.choice`, `Quot.sound`.
Os hashes e logs finais são calculados por `record_gaussian_closability_draft.py`
e registrados em `gaussian_closability_draft_status.json`. Os logs rc1
permanecem como tentativas falhas e não são aceitos como prova.

1. `L2PositiveMultiplier` constrói M_g para g contínua, real e 0≤g≤1.
   É contração complexo-linear no L² de Lebesgue. Se g>0 em toda parte,
   é injetiva como mapa de classes L², sem exigir inversa limitada.
   Comuta com campos fortemente contínuos uniformemente limitados.
2. `L2GaussianProfile` escolhe g(s)=exp(-s²), prova 0<g≤1 e a
   integrabilidade quadrática dos vetores g(s)v. O coeficiente 2 na
   integral de g² é calculado por exp(a)exp(a)=exp(2a).
3. `ScalarGaussianVacuum` constrói Ω_g(s)=g(s)√cη, com o mesmo fator
   Haar c=(2π)⁻¹ e η=`regularVacuum P`. Se ρ(A)Ω_g=0, cancelam-se
   g(s)>0 e √c>0 a.e.; logo θ_s(A)η=0 a.e., ν(A*A)=0 e A=0 pela
   fidelidade do peso escalar já demonstrada. Isso prova separação
   para a imagem concreta de N; não atribui separação a η em N.
4. `FibreVonNeumann` prova que a amplificação de uma álgebra de von
   Neumann coincide com seu bicomutante. Um operador no bicomutante
   comuta com shifts e caracteres externos, logo é fibra constante;
   testes contra todas as fibras de N' recolocam a fibra extraída em N.
5. `DualOrbitVonNeumann` constrói o campo unitário W e identifica
   ρ(A)=W fibre(A) W*. Transporta o bicomutante por essa equivalência.
   Assim a imagem inteira ρ(N) é efetivamente de von Neumann, sem
   invocar um teorema geral não formalizado sobre imagens normais.
6. `SeparatingCyclicCommutant` prova, para uma álgebra de von Neumann
   concreta, que um vetor separante tem órbita densa sob o comutante.
   A projeção sobre o fecho dessa órbita pertence ao bicomutante;
   a separação força seu complemento a ser zero. Não requer que a
   órbita sob a álgebra original seja densa no ambiente inteiro.
7. `VectorTomitaClosability` prolonga a identidade de pareamento com
   o comutante ao fecho do gráfico vetorial. A densidade do item 6
   elimina fibras verticais e prova univalência desse fecho.
8. `ScalarGaussianGNSMap` define T=M_g|H_I, contração injetiva para o
   mesmo L² ambiente, entrelaçando π_I e ρ. Prova exatamente
   TΛ(A)=ρ(A)Ω_g. Não afirma T(H_I)⊆H_I ou sobrejetividade.
9. `ScalarGaussianClosureTransport` leva G_I ao gráfico vetorial
   auxiliar por T×T, e a continuidade leva seus fechos. Um ponto
   (0,y) produz (0,Ty); o item 7 dá Ty=0 e a injetividade dá y=0.
   O mesmo transporte prova a univalência sobre cada x original.

[OPEN] Este resultado fecha o problema de fechabilidade do gráfico
especificado, na camada DEV. Ainda não identifica seu domínio com o
domínio GNS escalar máximo nem estabelece a ponte de núcleo necessária
para qualquer teorema externo. O operador fechado como mapa antilinear,
seu adjunto/decomposição modular, KMS, traço canônico e escala dual,
Three Locks/H1, H2/H3, setor interagente e certificado consumido pelo
gate permanecem fora deste pacote. `ScalarClosedTomita.lean` é uma
etapa posterior, excluída desta revisão. Não há integração no monólito,
mudança de gate ou runtime integral nesta entrega.

O perfil gaussiano é ferramenta auxiliar de prova. Não substitui o
peso original, não fixa uma escala física e não introduz postulado TGL.
