# Invariância do peso, certificado e domínio estável por adjunção

{date}. [REAL — Lean, cópia isolada da v350, revisão independente]

A mesma ν(A)=q_A(eΩ) é invariante pela conjugação A↦Λ_t* A Λ_t.
Isso foi demonstrado pela comutação das translações ordinárias com N,
pela bimodularidade de q e pela invariância de Ω sob o fluxo da torre.
A orientação da fórmula está escrita; invariância para todos os tempos
reais não identifica a orientação KMS. KMS ainda não foi demonstrada.

O RegularScalarWeightCertificate reúne 13 campos sobre objetos definidos
pelo mesmo SiteProfile: base, amplificação, peso, normalidade, ideal de
quadrados finitos, aproximação e invariância. O construtor descarrega as
propriedades; não as recebe como hipóteses residuais nem como booleanos.
O campo de normalidade quantifica índices em universo arbitrário. Esse
certificado ainda não está ligado à decisão Python da fronteira.

Também foi construída a subálgebra complexa sem unidade I∩I*, onde I é o
ideal esquerdo de quadrados finitos já definido. Para todo A∈N,
A_h=X_h* A X_h pertence a I∩I* para h>0, ||A_h||≤||A||, A_h→A e A_h*→A*
fortemente. Seus dois quadrados, A_h* A_h e A_h A_h*, têm peso ν finito.
A prova usa que contrações tendendo fortemente à identidade também têm
adjuntos tendendo fortemente à identidade. Não presume continuidade da
adjunção em toda topologia forte, não afirma convergência em norma e não
presume que A_h≤A ou que os aproximantes sejam positivos para A arbitrário.

Esse domínio prepara a inscrição GNS e a análise de Tomita. Não constitui,
por si só, espaço GNS completo, identificação modular, traço ou dado físico.
ScalarGNSOrbit, em desenvolvimento posterior, não faz parte deste pacote.

{target_count} alvos novos no trio propext/Classical.choice/Quot.sound;
{build_count} registros Lean válidos, {controls} controles e {audit_count}
declarações no Audit. {embedded_count} arquivos embutidos. Build incremental;
não houve recompilação integral de Mathlib ou execução do monólito.
[Revisão independente](<{review_path}>).

Original preservado: `{base_sha}`. Cópia integrada: `{working_sha}`.
O AST Python fora do dicionário Lean permanece igual ao estrato anterior.
As seis flags maiores e o gate legado não foram alterados por esta etapa.

[OPEN] Inscrição GNS completa, KMS, gerador afiliado e perturbação para
obter o traço canônico fiel, normal, semifinito e com escala dual. Continuam
no objetivo a interface geral de peso operatorial/predual, Three Locks/H1,
H2/H3 na mesma geometria física, setor quântico interagente/BRST/QME/anomalias,
UV, composição do certificado completo consumido pelo gate e runtime integral
isolado. Inventário I/O histórico, sem liberação do runtime atual.
