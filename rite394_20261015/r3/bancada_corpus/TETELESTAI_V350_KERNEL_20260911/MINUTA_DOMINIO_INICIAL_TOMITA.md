# Domínio GNS denso e gráfico inicial de Tomita

{date}. [REAL — Lean em cópia; revisão independente]

Na mesma álgebra regular N, com o peso escalar ν e o Hilbert H_I já
construídos, para A∈I, a regularização A_h=X_h* A pertence a I∩I* para h>0 e
Λ_ν(A_h) converge para Λ_ν(A) na norma de H_I. Isso prova densidade
de Λ_ν(I∩I*) em H_I, sem pressupor A*∈I nem continuidade geral da
adjunta na topologia forte.

A prova usa a fatoração da representação ambiente por dois operadores
fixos e uma fibra constante. Assim, limites fortes com uma cota uniforme
de norma atravessam essa representação para qualquer filtro de índices.
Não há interseção não enumerável de conjuntos conulos no argumento.

O gráfico inicial é exatamente G={(Λ_ν(A),Λ_ν(A*)): A∈I∩I*}.
A injetividade da inscrição prova sua univalência; star(star A)=A prova
invariância por troca das coordenadas. Seu domínio é denso em H_I.
Essa invariância é de uma relação involutiva, não simetria de operador
no sentido do produto interno.

[OPEN] Ainda é necessário provar que (0,y)∈fecho(G) implica y=0.
Densidade e univalência de G não foram promovidas a fechabilidade.
I continua sendo o ideal de finitude uniforme; não foi identificado
com o domínio escalar máximo. Não há Tomita fechado, decomposição polar,
identificação modular/KMS ou traço canônico novo neste pacote.

{target_count} alvos novos em quatro módulos; {build_count} registros Lean
incrementais; {controls} controles; {audit_count} declarações no Audit;
{embedded_count} arquivos embutidos. As fontes DEV passaram por revisão
e recompilação independente; a integração recebeu conferência separada.
[Parecer completo](<{review_path}>).

Base original: `{base_sha}`. Cópia: `{working_sha}`. O corpo Python fora
do dicionário Lean permanece igual ao estrato anterior. As seis flags
maiores continuam false, com controle explícito de que este gráfico
inicial não quita Tomita/KMS/traço. O gate legado permanece inalterado.

[OPEN] Além da fechabilidade: identificação do domínio escalar completo,
normalidade da representação, identificação modular/KMS, gerador afiliado,
perturbação e traço fiel normal semifinito com escala dual; interface
geral espectral/predual/peso operatorial; Three Locks/H1, H2/H3 na mesma
geometria física; estado quântico interagente, BRST/QME, anomalias/UV;
certificado completo consumido pelo gate e runtime integral isolado.
O inventário I/O histórico não libera o runtime da cópia atual.

Resultados DEV posteriores, se registrados na custódia, têm escopo e
estatuto próprios. Eles não integram as contagens ou o parecer acima.
