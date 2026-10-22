# Ward clássico-linear para campos suaves gerais — entrega R3
Data: 09/09/2026. [REAL — compilação isolada verificada; revisão independente pendente.]

## Resultado principal
Para h_{μν}: R^4→R e ξ_μ: R^4→R suaves componente a componente,
o módulo demonstra, para quaisquer μ,ν,x:

R1(h + Dξ + (Dξ)^T)_{μν}(x) = R1(h)_{μν}(x).

R1 é exatamente TGLExt.linRicci, já definido em ContinuumTT.lean. Não foi substituído
por um símbolo de Fourier, por uma onda plana ou por uma soma finita de modos.
A hipótese adotada é ContDiff R ∞, aprovada pelo orquestrador para esta etapa.
Não se exige TT, cone nulo, equação de movimento, perfil de onda ou comutação como INPUT.
A identidade vale inclusive sem impor simetria a h; para a interpretação métrica
usa-se sua subclasse simétrica, e a própria transformação de gauge é simétrica.

Consequências formais: o escalar linearizado e o tensor de Einstein linearizado permanecem
iguais após a transformação; a condição de vácuo R1=0 é preservada em ambas as direções.

## Dedução, reutilização e novidade
DEDUCAO_PREVIA.md foi gravado antes do primeiro módulo Lean e permanece intacto.
A investigação encontrou o cálculo de coordinatePartial já presente em SmoothMatrixCalculus.
A linha 18 prova pd = coordinatePartial por redução definicional.
As linhas 21–51 transportam suavidade, linearidade e a comutação proveniente de Schwarz,
já derivada da regularidade no cálculo canônico com a Mathlib.
Esses transportes são infraestrutura reutilizada, não uma reivindicação de redescoberta de Schwarz.

A parte nova é a aplicação ao operador geral:
- linha 86: linRicci_as_sum, com o traço diferenciado por regras válidas de soma finita;
- linha 100: permutação de derivadas terceiras a partir da suavidade;
- linha 113: linRicci_pure_gauge_zero, cancelamento dos termos de terceira ordem;
- linha 137: linRicci_add_smooth, linearidade com diferenciabilidade garantida;
- linha 151: general_smooth_gauge_invariance, teorema principal;
- linhas 166,172,179: invariância do escalar, de Einstein e preservação do vácuo.

## Evidência formal
Fonte: GeneralLinearizedGauge.lean
Namespace: ChatgptAudit.GeneralLinearized
Imports: TGLExt.ContinuumTT e TGLExt.SmoothMatrixCalculus.
Build: BUILD_20260909_120659_151046/BUILD_RESULT.json
Estado: PASS_COMPILED_SCOPE.
Contagem medida: 20 teoremas + 7 definições/abreviações = 27 termos auditados.
Módulo e importador conjunto: exit 0; zero warnings; axiomas somente propext,
Classical.choice e Quot.sound. SHA-256 da fonte: 41f58f1a574b0c9ba726038ab1ae8f02597c8d14b3941b15b1c37964b1ec9721.
A fonte corrente confere byte a byte com o hash do resultado final.
Os três builds anteriores com falhas visíveis e todos os backups em bytes foram preservados.

A compilação usa binários canônicos previamente construídos, com fontes/binários dos imports
diretos, ferramenta e pinos medidos antes/depois. Não recompila nem verifica por hash todos os
imports transitivos. Nenhum um.py foi executado/importado. Nenhum original ou Atlas foi alterado.

## O que muda e o que permanece aberto
[REAL] Ward clássico-linear do operador Ricci no campo suave geral está demonstrado nesta bancada.
A antiga restrição a ondas planas deixa de ser necessária para ESTA identidade.
Não se promove a antiga flag relevante_anomalies_absent ao setor quântico: seu alvo canônico
continua sendo qgPhysicsCertificate_anomaly, que trata do símbolo clássico-linear.

[OPEN / fora deste lote] anomalias quânticas com interações; decomposição/espectro físico e
ausência de ghosts para perturbações gerais; ação Fierz–Pauli completa; problema UV.
Bianchi geral não foi acrescentado neste lote. A invariância de Einstein aqui é sob gauge,
e não uma nova prova de conservação de sua divergência.
O fundo é plano com a etaDiag canônica: não há reivindicação de gauge em fundo curvo arbitrário,
quantização, comportamento não linear completo, confirmação física ou fechamento geral da QG.
Não houve otimização da regularidade de ∞ para ordens finitas mínimas.

## Handoff para incorporação
Fonte congelada e revisável. Pode ser embutida como TGLExt/GeneralLinearizedGauge.lean,
com import TGLExt.GeneralLinearizedGauge no agregador; não há import local a transpor.
Os 20 nomes de teoremas e os 7 nomes auxiliares constam de MANIFESTO_ENTREGA.json.
Uma busca dos 27 nomes curtos nas declarações da cópia integrada de sete módulos não encontrou
colisão. Isso não substitui a comparação estática e compilação do futuro integrador.
A entrega não altera flags, gate, manifesto canônico ou a versão original do programa.
