# Peso escalar dual — desenvolvimento ainda não integrado nem revisado

[REAL — compilação local, não revisão independente]

Quatro módulos e 23 alvos foram compilados em desenvolvimento. A cópia
integrada permanece na custódia fixed_base_custody.json: esta nota não
amplia seu escopo nem altera flags.

FixedBaseEquivalence empacota a mesma amplificação M→F como equivalência
de álgebras com involução e isomorfismo de ordem; a inversa é e*Be.
BoundedBaseDualValues transporta os valores positivos limitados para M,
prova sua unicidade e a aproximação forte por entradas com quadrados finitos.

ScalarDualWeightFaithfulness usa η=eΩ. η é separante para F porque Ω é
separante para M. Se q_A(η)=0, o resolvente minimizador satisfaz Rη=η;
R∈F implica R=I. A identidade de energia, com finitude explícita, dá
q_A(v)=0 para todo v, e a fidelidade da forma conclui A=0.

ScalarDualWeight define ν(A)=q_A(η) no cone positivo de N e prova zero,
aditividade, homogeneidade por escalares não negativos, monotonia,
fidelidade e normalidade para supremos dirigidos internos. O ideal
complexo esquerdo já construído é fortemente denso e seus quadrados têm
ν finito. Para um valor limitado fibre(D), ν coincide com a avaliação
do estado vetorial original em D. O enunciado exato de densidade e a
conexão com a interface padrão de peso precisam de revisão independente.

[OPEN] Este peso não é um traço. Ainda faltam a identificação de seu
grupo modular/condição KMS, o gerador afiliado e a perturbação que produz
o traço canônico e sua escala. A correspondência geral espectral/predual,
o contrato de peso operatorial, Three Locks/H1–H3 físicos, interações,
contrato ampliado do gate e runtime integral permanecem abertos.
Não se reivindica fidelidade apenas de um funcional normalizado ou de
um estado alternativo: a prova usa a forma dual e a torre desta construção.

Os hashes e logs exatos estão em scalar_weight_draft_status.json. Todas
as tentativas de compilação, inclusive falhas, permanecem em logs/.
Próximo passo: revisão independente dos quatro módulos, integração e
custódia, antes de prosseguir para a condição modular do peso escalar.
