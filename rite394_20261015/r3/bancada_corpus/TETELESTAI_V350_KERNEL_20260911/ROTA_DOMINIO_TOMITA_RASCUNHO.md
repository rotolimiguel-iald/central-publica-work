# Densidade do domínio de Tomita na norma do peso — desenvolvimento posterior

[REAL — Lean DEV local; ainda sem integração e revisão independente]
Os três módulos DualOrbitStrongLimits, ScalarGNSStarApproximation e
ScalarGNSStarDensity têm nove alvos compilados. O status será pinado em
tomita_domain_draft_status.json após a custódia da representação GNS.
Eles não pertencem ao escopo de REVIEW_GNS_REPRESENTATION.md.

A ação ambiente admite a fatoração L_A = W_+ · fibre(A) · W_-, onde
W_± são os campos s↦characterMultiplier(±s). A identidade foi provada
por igualdades quase em toda parte para cada A e vetor fixados. Isso
transporta redes fortemente convergentes com cota uniforme, por meio
do lema já provado para fibre, sem interseção não enumerável de conjuntos
conulos e sem impor continuidade em norma operatorial.

Para A∈I, basta regularizar à esquerda: A_h=X_h* A. A_h∈I pelo fechamento
à esquerda; A_h*=A*X_h∈I porque X_h∈I para h>0. Logo A_h∈I∩I*.
Os adjuntos das contrações X_h convergem fortemente para a identidade.
A fatoração da ação e o entrelaçamento dão Λ_ν(A_h)→Λ_ν(A) em norma
no L² exterior e no Hilbert H_I. Como Λ_ν(I) é denso em H_I, segue
DenseRange da inscrição de I∩I* em H_I.

Esse resultado corrige a rota anterior: para obter esta densidade não foi
necessário provar convergência à direita A X_h na norma ν nem usar a
regularização bilateral X_h* A X_h. A estimativa antiga não é apresentada
como refutada; ela simplesmente não é necessária à prova agora compilada.

ScalarGNSStarEmbedding é uma função para o Hilbert, obtida restringindo a
aplicação linear já construída sobre I. Não foi empacotada aqui como novo
LinearMap. O tipo de densidade usa a norma do Hilbert, não a topologia
forte de N. Não identifica I com o domínio escalar máximo.

[OPEN] Construir S_0Λ_ν(A)=Λ_ν(A*) com domínio denso e provar que o fecho
do seu gráfico é univalente. Densidade não implica fechabilidade. A prova
TomitaClosability da torre base usa a identidade de emparelhamento com
rTowerPi e densidade de vetores na torre; ela não pode ser transplantada
para este peso sem construir a correspondente identidade sobre H_I.
Permanecem polar, identificação modular/KMS, gerador afiliado e traço,
interface geral espectral/predual/peso operatorial, Three Locks/H1, H2/H3,
setor quântico interagente, BRST/QME/anomalias/UV, contrato completo
consumido pelo gate e runtime integral isolado. Nenhuma flag maior muda.

Tentativas falhadas foram preservadas: inferência do espaço na ação,
composição de funções não explicitada e timeout ao empacotar a restrição
como mapa linear sobre o subtipo. Só os logs finais rc0 são evidência.


## Adendo — 2026-09-12T07:32:41.228455-03:00

[REAL — DEV, fora da revisão/integrado] ScalarTomitaGraph acrescenta cinco
alvos aos nove anteriores: inscrição restrita injetiva, gráfico inicial,
univalência desse gráfico, invariância pela troca das coordenadas e domínio
denso. Total agora: quatro módulos / 14 alvos. O gráfico é exatamente
{(Λ_ν(A),Λ_ν(A*)): A∈I∩I*}. Univalência usa a injetividade da inscrição;
a troca usa star(star A)=A. A prova de densidade usa o resultado em norma
GNS recém-compilado, não a densidade forte em N.

O adendo não afirma univalência do FECHO do gráfico. Essa é precisamente
a obrigação seguinte. Ainda não há operador Tomita fechado deste peso,
decomposição polar, KMS ou traço canônico. Não foi empacotado um novo mapa
semilinear parcial neste arquivo; o objeto provado é o gráfico inicial.
