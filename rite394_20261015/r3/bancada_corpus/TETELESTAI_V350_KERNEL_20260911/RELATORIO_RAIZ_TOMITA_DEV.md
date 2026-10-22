# Resolvente e raiz positiva do mesmo S†S — desenvolvimento

2026-09-12T11:36:51-03:00. [REAL — cinco módulos/30 declarações compiladas localmente]
[OPEN — revisão independente e integração deste lote ainda pendentes]

Construído R=(I+A)^(-1), A=S†S, no mesmo H_I. Positividade e a
sobrejetividade anterior fornecem uma equivalência linear entre D(A)
e H_I. A inclusão da inversa em H_I satisfaz ||Rz||≤||z||;
R é injetivo, auto-adjunto e 0≤R≤I. A igualdade
resolventGraphOperator R=A foi provada como mapas parciais.

Aplicada a construção anterior por cálculo funcional limitado:
B tem gráfico (sqrt(R)v,sqrt(I−R)v), é positivo, auto-adjunto,
fechado, densamente definido e B²=A como mapas parciais, com
igualdade dos domínios sucessivos. Seu núcleo é trivial.
Em D(A), foi provada a igualdade ||Bx||²=||Sx||².

[OPEN] Não foi provado D(B)=D(S), nem a igualdade de energia em
todo esse domínio. Portanto não se declara B como fator de uma
decomposição polar já identificada de S. J, identificação modular/KMS
do peso, traço/escala dual, Three Locks/H1–H3 e setor interagente
permanecem abertos. Núcleo trivial não implica gap.

Este lote DEV não está no monólito: a cópia integrada anterior
continua em `77ddd4dd8d5a012e8a44b59e00f4eaf6b9958ce5c6ee1f74fae27b2085179632`. Nenhum gate mudou,
nenhuma execução integral do monólito ocorreu e as contagens DEV
não se somam ao Audit integrado. Tentativas rc1 preservadas em logs;
somente logs finais rc0 e hashes coincidentes sustentam a compilação.
O manifesto tomita_root_draft_status.json discrimina as fontes,
binários, axiomas e tentativas. O plano integral continua incompleto.
