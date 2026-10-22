# Operador fechado do gráfico original e seu subespaço real padrão

[REAL — Lean DEV; revisão independente deste pacote pendente]
Este pacote constrói S no mesmo H_I = ScalarGNSHilbert P. Seu domínio
D é {x | existe y, (x,y) pertence ao fecho do gráfico original G_I}.
A univalência desse fecho, provada no pacote gaussiano anterior,
permite escolher o valor de S; a escolha não é uma hipótese nova.

Em ScalarClosedTomita, o gráfico inicial contém zero, é aditivo e
é estável por (x,y) ↦ (c x, conjugado(c) y). Essas propriedades passam
ao fecho por continuidade. A simetria (x,y) ↦ (y,x) também passa ao
fecho. Assim D é um submódulo complexo e S:D→H_I é antilinear.
Prova-se igualdade entre seu gráfico e o fecho de G_I, domínio denso,
invariância de D sob S, S²x=x e SΛ(A)=Λ(A*) para A∈I∩I*.
Não se declara D=H_I, continuidade ou limitação de S.

As operações de adição e escala no núcleo estrelado usam instâncias
explícitas, herdadas do subobjeto; as identidades de estrela são
conferidas no operador subjacente. Não há alteração de redutibilidade
insegura nem axioma novo. Tentativas com erro de elaboração permanecem
nos logs, sem integrar a evidência aceita.

ScalarTomitaStandardSubspace aplica o teorema genérico existente
ClosedAntilinearStandardSubspace ao D e S efetivos, com as quatro
hipóteses demonstradas: gráfico fechado, domínio invariante, involução
e densidade. Obtém K=Fix(S), real fechado, K∩iK={0} e fecho(K+iK)=H_I.
O domínio é exatamente K+iK e S(h+ik)=h-ik. K aqui é o subespaço
real, não o gerador modular denotado K em outros módulos.

Os dois módulos somam 24 alvos; hashes, logs e axiomas aceitos são
registrados por record_tomita_closed_draft.py, que falha se não houver
compilação rc0 da fonte final ou se algum alvo depender de axioma fora
de propext, Classical.choice e Quot.sound. O pacote gaussiano anterior
foi revisto separadamente em REVIEW_GAUSSIAN_CLOSABILITY.md, sem P0–P2.

[OPEN] Não se identifica I com n_ν, nem se afirma que D seja o domínio
máximo do operador modular do peso ν. A ponte de domínio/core,
adjunto e decomposição polar, identificação do fluxo/KMS, traço
canônico e sua escala dual permanecem necessárias. Fix(S) não é
identificado com Fix(J); nenhum quociente de dimensões é promovido a
entropia, Meia-Nat, área, geometria de cunha ou Bisognano–Wichmann.
Three Locks/H1, H2/H3, setor quântico interagente, composição física,
gate ampliado e runtime integral não são quitados por este pacote.
Não há integração nova no monólito nesta entrega DEV.
