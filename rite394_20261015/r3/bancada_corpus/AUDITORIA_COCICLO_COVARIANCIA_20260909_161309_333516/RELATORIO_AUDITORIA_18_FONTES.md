# Auditoria estática da continuação — cociclo e covariância

[REAL] PASS_STATIC_EVIDENCE_AUDIT. As 18 fontes congeladas coincidem byte a byte com as cópias dos seus recibos PASS: 203 teoremas + 42 outras declarações = 245 termos, incluindo 7 instâncias locais nomeadas. Foram verificados 2.847 itens, sem falhas finais, e medidos 532 arquivos.

| Módulo | Teoremas | Outras | Instâncias locais |
|---|---:|---:|---:|
| `SummableInteractionModularOrbit` | 24 | 3 | 0 |
| `UnitaryDuhamel` | 12 | 5 | 2 |
| `BoundedPerturbationCocycle` | 13 | 2 | 0 |
| `SpectatorCancellation` | 5 | 2 | 2 |
| `PauliInteractionCocycle` | 28 | 4 | 0 |
| `PauliCocycleGenerator` | 7 | 0 | 0 |
| `FiniteModularHamiltonian` | 20 | 7 | 2 |
| `FiniteLevelExponentials` | 5 | 1 | 1 |
| `CocycleNormLimit` | 15 | 2 | 0 |
| `DerivativeFromLinearCutoffError` | 4 | 0 | 0 |
| `CanonicalCocycleDerivative` | 4 | 1 | 0 |
| `PauliPerturbedDynamics` | 16 | 2 | 0 |
| `FiniteCoordinateMap` | 22 | 5 | 0 |
| `FiniteLeviCivita` | 8 | 2 | 0 |
| `FiniteCurvatureAlgebra` | 5 | 5 | 0 |
| `FiniteCoordinateCurvature` | 6 | 1 | 0 |
| `FiniteRicciContraction` | 4 | 0 | 0 |
| `FiniteEinsteinNaturality` | 5 | 0 | 0 |

[REAL] Os 17 recibos distintos que compilam as 18 fontes registram 35 saídas Lean, todas zero. Os logs auditam exatamente cada declaração explícita, com axiomas limitados a propext, Classical.choice e Quot.sound, admitindo subconjuntos desse trio. Não foram encontrados avisos, erros, sorry/admit/native_decide/axiom/unsafe nas fontes auditadas.

[REAL] O fecho recursivo inclui 19 recibos e 21 módulos locais: as fontes, os binários, as cópias de cache e os registros de fronteira direta foram rechecados; cada import local tem origem compilada identificada. Os seis módulos de coordenadas utilizam ainda a biblioteca45 transposta, cujo recibo PASS_TRANSPOSED_SCOPE, saídas e artefatos registrados foram conferidos. Nenhuma dependência herdada entra na contagem dos 245 termos novos.

[REAL] Zero colisões de nomes completos entre as fontes novas, com o cache local herdado e com as declarações explícitas da biblioteca45 registrada. Esta varredura não abrange todos os nomes gerados pelo Lean ou todo o namespace transitivo de Mathlib.

[DERIVED] O setor quântico constrói o cociclo concreto por cortes finitos, limite em norma com estimativa proporcional a |t|, e deriva seu gerador iV e a equação diferencial à direita. O Hamiltoniano modular de cada andar foi ligado ao fluxo canônico; a comutação do espectador foi derivada, não postulada. A não trivialidade para singleBond significa que o cociclo não é identicamente 1, sem afirmar que todo instante não nulo produz operador distinto de 1.

[DERIVED] PauliPerturbedDynamics foi revisto integralmente: β_t(A)=u_t α_t(A)u_t*, lei de grupo, inversa, preservação do fator e isometria são consequências da construção concreta. A continuidade temporal é condicionada à continuidade da órbita canônica de A; o módulo prova a aplicação a V.

[OPEN — fora desta entrega] Esta continuação não constrói um estado perturbado KMS/normal com esta dinâmica, não identifica o limite ℓ¹ com uma remoção geral de corte UV relativístico e não prova cancelamento geral de anomalias quânticas. As hipóteses do setor de geometria permanecem nos enunciados; a compilação não transforma dados geométricos fornecidos em sua seleção física.

[REAL — divisão de revisão] O auditor é autor de FiniteModularHamiltonian, FiniteLevelExponentials e das duas folhas derivativas; a revisão semântica independente dessas fontes foi realizada pela raiz. A raiz também revisou integralmente as seis fontes geométricas. Aqui foi feita a auditoria estática independente da composição e a revisão semântica de gerador/dinâmica das outras sessões.

[REAL — diagnósticos preservados] A primeira rodada registrou explicitamente bloqueios de leitura do sandbox e a diferença de esquema dos recibos geométricos (boundary/cached). A segunda, após leitura autorizada e tratamento do esquema, conservou apenas seis falsos negativos do auditor por esperar um nome de status diferente: o status real da biblioteca45 é PASS_TRANSPOSED_SCOPE. O script v3 corrige essa interpretação sem alterar os recibos; todos os diagnósticos anteriores permanecem ao lado. Não houve falha matemática ou divergência de bytes nas fontes.

[REAL] Nenhuma compilação nova foi executada nesta auditoria; nenhum um.py foi lido, importado ou executado; nenhum original ou documento existente foi alterado. O recibo final é AUDITORIA_ESTATICA_18_FONTES_FINAL.json; a lista para consolidação é FONTES_E_RECIBOS_18_FINAL.json.

SHA-256 do recibo final medido: `9b05a3017a2edf7764bc25be5d99e9a40cfd7993b7e6b2fd4e7e089ccd85785c`.
