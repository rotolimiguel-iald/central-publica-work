# Revisão independente045 — fontes finais e infraestrutura

[REAL — revisão e auditoria independente do build, 06/09/2026] A revisão inicial ocorreu durante o build. Após seu encerramento, a execução somente leitura de audit_continuation045.py --build-only terminou com exit0 e BUILD_PASS, sealed=false. A conferência do selo final permanece pendente. Este resultado não é aprovação gerencial nem confirmação física.

## Independência e objeto

A revisão independente cobre A1/A2, de Newton, C, de Beauvoir, e a infraestrutura do root. O presente revisor é autor de StateClockDichotomy.lean: este registro NÃO constitui revisão independente da prova B. Não foram alterados esses fontes, scripts, canônicos, selos anteriores ou memórias. Somente este documento novo foi criado.

## A1/A2

[DERIVED — exame matemático dos enunciados e construções] Não identifiquei falha material. chainWordEquiv representa os N+1 sítios do nível N, incluindo os extremos 0 e N. A permutação de índices é contravariante e a matriz correspondente compõe covariantemente; a conjugação final envia o observável do sítio n ao do sítio sigma(n). O tensor completo transporta sua família de matrizes por sigma inversa, coerentemente.

A hipótese explícita de pesos constantes prova a invariância do produto de pesos, a comutação com a densidade e a pertença ao centralizador. A preservação do estado é por conjugação em M; não se afirma que o unitário interno fixa Omega. Os campos de TowerHorizon são construídos a partir desses resultados, não recebidos como hipótese circular.

Os observáveis de sítios m>N ficam fixos pela localidade. A não modularidade usa uma projeção diagonal local concreta: o fluxo modular fixa essa projeção e uma permutação que move o sítio a leva a uma projeção distinta. O argumento vale para todo tempo modular e explicita a condição de sítio movido. Para swapHorizon, N=max(i,j) contém ambos os sítios naturais e hij:i!=j é exigido apenas no controle não modular. Os casos i=j dos adaptadores de ação não produzem uma afirmação falsa de não trivialidade.

A covariância de E é incondicional quanto à escolha de horizonte porque o horizonte foi construído; a existência de E continua fornecida pelo habitante estacionário não tracial ou pelo tracial. O teorema com I:ExpectationInput é honestamente condicional a I. Nenhuma expectativa aperiódica geral ou ação em tela física foi obtida por esses módulos.

[REAL — referência conferida] FiniteSiteHorizons importa agora AffineClockAndRegion e usa ChatgptAudit.Clock040.region_site_noncommutation. A dependência sem pin ChainFaithful foi removida. Censo textual: A1 tem 23 teoremas, 7 definições e 30 prints; A2 tem 25 teoremas, 3 definições e 28 prints. As listas de declarações e prints correspondem exatamente. Este censo não substitui o resultado do compilador.

## C e infraestrutura

[DERIVED] Em C, a comparação h com 2h mantém a mesma família de operadores e o mesmo par de tangentes. det(G)>0 garante área positiva e distingue as escalas. A ligação 034 é apenas a homogeneidade de sqrt(det), com valor de referência 2/9; não presume uma ação de horizontes nessa tela. Uma normalização adicional pode remover essa liberdade.

[REAL — leitura dos scripts] O auditor contém replay determinístico das transposições upstream, caminhos esperados, igualdade origem/snapshot, igualdade dos bytes adaptados, inventário e metadados cruzados. Exige upstream_paths contidos em custody_keys; as guardas posteriores conferem o fechamento dos snapshots congelados e dos inputs de cada etapa. A precedência dos pins é ordenada como no runner, incluindo 006/007. Os rótulos históricos foram ajustados. As fontes de tentativas anteriores dentro de TGLExt são inventariadas explicitamente.

O diretório de módulos é único e isolado: LEAN_PATH começa no clean, seguido apenas das raízes externas declaradas. As classes de módulos recompilados e fronteira pinada continuam disjuntas, com resolução e hashes próprios. Não há fallback para a raiz Chatgpt ou para o kernel canônico. Permanecem verificações de cópias, ordem de imports, importador completo, logs, censo de axiomas, estabilidade dos inputs e bins. O selo distingue quatro módulos novos dos dois fontes upstream recompilados e compara também as contagens separadas.

[REAL/OPEN] A auditoria independente do build completo foi concluída, conforme o adendo abaixo. Depois de eventual selo pelo root, ainda resta a conferência final somente leitura. Os bins históricos são pinados, não recompilados; o fechamento transitivo externo não é integralmente inventariado. A cópia upstream é de fontes atuais e não equivale à revalidação do selo canônico v329. H3 e a reconstrução física geral permanecem abertas; nenhum gate é movido.

## Bytes observados nesta revisão

Hashes calculados diretamente dos arquivos, não tomados de relatos. Estes são os bytes lidos; qualquer mudança posterior exige nova conferência pertinente.

| Arquivo | Bytes | SHA256 |
|---|---:|---|
| `FiniteSitePermutations.lean` | 11564 | `3293874b12e272021bb0a8ed2630b00824759d5f4bfce4ae7bc41b31c5dd6a7d` |
| `FiniteSiteHorizons.lean` | 12559 | `cc0921dfa7c73f1207241b5a18227845fd6de2207de9d83785a5348477123fe5` |
| `clean_continuation045.py` | 33316 | `42d030a6a203bcb5496605727630df3b1b8aa626240cd76a78f8a99db726d117` |
| `audit_continuation045.py` | 46632 | `4726e0a3bbe2f3c9f7c3d6fbf4afb0a4d8feab5adfc76d69bb78369058a6a380` |
| `prepare_continuation045.py` | 3731 | `70d912fcf5505d9f764f06efe1ab50d33bfcc4b64ecd243e72209946d70ff4ef` |

## Adendo — validação independente do build completo

[REAL] Comando executado exclusivamente em leitura: `C:\Python314\python.exe -B audit_continuation045.py --build-only`. Resultado: exit0, BUILD_PASS, sealed=false. Não foi executado Lean nem criado manifesto por este revisor.

Diretório: `CONTINUACAO045_CLEAN_20260906_233647_202656`. O auditor verificou 2287 arquivos do build e 207 registros históricos. Contagens: 97 teoremas, 20 definições incluindo estruturas, 117 prints e zero instâncias. Os quatro módulos novos correspondem a 83/18/101; os dois upstream recompilados correspondem a 14/2/16, respectivamente. Os resultados antigos recompilados não são apresentados como novos teoremas.

[REAL — conferência adicional de bytes e metadados] Foram lidos os sete logs e metadados, independentemente da saída resumida do auditor. Todos tiveram exit0/PASS, zero erros ou avisos; as listas reais de axiomas coincidem com os metadados e usam apenas propext, Classical.choice e Quot.sound. Hashes e tamanhos dos artefatos produzidos, hashes de fonte/log/olean e cópias dos seis fontes correspondem aos registros. Os inputs antes/depois são não vazios, iguais e marcados estáveis; os outputs são novos.

| Módulo | Prints | Inputs por etapa | Resultado |
|---|---:|---:|---|
| `TGLExt.TheLiftFiresOnThePeriodicTower` | 6 | 1395 | PASS, exit0, sem avisos |
| `TGLExt.TheModularFlowIsAHorizon` | 10 | 1395 | PASS, exit0, sem avisos |
| `StateClockDichotomy` | 21 | 2123 | PASS, exit0, sem avisos |
| `HorizonAreaScale` | 22 | 2031 | PASS, exit0, sem avisos |
| `FiniteSitePermutations` | 30 | 1363 | PASS, exit0, sem avisos |
| `FiniteSiteHorizons` | 28 | 2204 | PASS, exit0, sem avisos |
| `Imports045All` | 0 | 2269 | PASS, exit0, sem avisos |

Os snapshots FROZEN_INPUTS e FROZEN_INPUTS_AFTER contêm 2262 registros e são iguais byte a byte. Imports045All contém exatamente os seis imports na ordem declarada. LEAN_PATH possui dez raízes: clean mais as nove raízes externas; a fronteira pinada ocupa o próprio clean e não há fallback para a raiz da bancada ou para o kernel canônico.

[DECLARADO — revisão de B recebida por comunicação do root] Newton revisou StateClockDichotomy independentemente e confirmou os quantificadores, o sinal e o coeficiente positivo eta*r^2/96. Este registro atribui essa revisão a Newton; não a apresenta como revisão independente feita pelo autor de B. As precisões de escopo foram registradas: r é a contração de Ricci R(d,d) na direção fixada, não a curvatura escalar; o relógio escolhido por tela cancela a quarta ordem do resíduo, sem estabelecer igualdade funcional exata dos incrementos finitos. A obstrução é a um relógio comum às duas telas e é compatível com o casamento quadrático já pago.

[OPEN] Nenhuma discrepância foi encontrada no build completo. O selo ainda será criado e conferido separadamente. H3 infinitesimal, a identificação física da geometria e a reconstrução geral permanecem abertas.

| Evidência adicional | Bytes | SHA256 |
|---|---:|---|
| `CONTINUACAO045_CLEAN_BUILD.json` | 1506564 | `55c3e06c473445e7453acb85e8a68856fe614c207516e26a80c2563ba7d88460` |
| `CONTINUACAO045_CLEAN_20260906_233647_202656\FROZEN_INPUTS.json` | 520299 | `6d35cf98407de06cb135ef2e3bbf3c336f88077146b64b77bacf81ac2b58efbd` |
| `CONTINUACAO045_CLEAN_20260906_233647_202656\FROZEN_INPUTS_AFTER.json` | 520299 | `6d35cf98407de06cb135ef2e3bbf3c336f88077146b64b77bacf81ac2b58efbd` |
