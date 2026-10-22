# Continuação045 — horizontes de permutação, relógio comum e escala da área

06/09/2026. Resposta à ORDEM_010, preservando o objetivo amplo de reconstrução gravitacional e as restrições de somente leitura do acervo.

## Resultado verificado

[REAL — compilação final] CONTINUACAO045_CLEAN_20260906_233647_202656: 7/7 etapas PASS, seis módulos e Imports045All, exit0 e zero erros/avisos. Quatro módulos novos: 83 teoremas, 18 definições/estruturas e 101 prints. Fontes v329 recompiladas, sem novidade contada: 14 teoremas, 2 definições, 16 prints. Total compilado: 97 teoremas, 20 definições/estruturas, 117 prints, 0 instâncias. Axiomas restritos a propext, Classical.choice, Quot.sound.

[REAL — custódia] 2262 registros congelados idênticos antes/depois; 2287 arquivos no inventário do build. Auditor --build-only: BUILD_PASS, 207 registros históricos. Conferidos replay v329, cópias, logs, binários, imports e guardas. A revisão independente está em CONTINUACAO045_REVISAO_INDEPENDENTE.md. O manifesto é emitido após a entrega.

| Módulo | Papel | Teoremas | Definições/estruturas | Prints |
|---|---|---:|---:|---:|
| TGLExt.TheLiftFiresOnThePeriodicTower | recompilado v329 | 6 | 0 | 6 |
| TGLExt.TheModularFlowIsAHorizon | recompilado v329 | 8 | 2 | 10 |
| StateClockDichotomy | novo045 | 18 | 3 | 21 |
| HorizonAreaScale | novo045 | 17 | 5 | 22 |
| FiniteSitePermutations | novo045 | 23 | 7 | 30 |
| FiniteSiteHorizons | novo045 | 25 | 3 | 28 |

## Horizontes construídos

A representação finita usa o andar N, com N+1 sítios binários. A permutação de palavras fornece uma matriz unitária, representada por towerPi na torre. Sua conjugação leva o observável do sítio n ao do sítio σ(n), fixando sítios m>N. Para perfil estacionário, a mesma construção comuta com a densidade e preserva o estado, fornecendo TowerHorizon sem assumir o horizonte como hipótese. O implementador interno atua por multiplicação à esquerda; a ação de permutação reclamada é sua conjugação sobre a álgebra. O contrato TowerHorizon não exige que esse implementador fixe Ω.

A não modularidade é medida num observável: o fluxo modular fixa cada projeção local e00, enquanto uma permutação que move n a envia a outra projeção. Não se pretende concluir que cada horizonte da torre é uma transformação do espaço-tempo. Falta essa identificação física.

## Relógio: quantificadores e consequência

[REAL — compilação final] StateClockDichotomy prova a incompatibilidade para qualquer função comum g:ℝ→ℝ. Na família anterior, escreva B=amplitudeMass b>0, η>0 e r=quarticMatchedRicci b η>0. Duas telas têm σ=0 e σ=r/4, logo os mesmos b, η e tensor de Ricci, cuja contração R(d,d)=r. Ao subtrair seus resíduos, a contribuição entrópica, avaliada no mesmo g, cancela exatamente. O limite da diferença dos resíduos divididos por t⁴ é ηr²/96>0.

Portanto não há um único g que anule os dois limites. O resultado não pede continuidade ou expansão cúbica de g. Como corolário, nenhuma regra que recebe somente a mesma história parametrizada do estado pode fornecer um relógio que satisfaça os dois testes. A hipótese de invariância por unitários restringiria essa classe e não eliminaria a obstrução.

A classe StateClock formalizada é cinemática: origem em0, derivada1 e jato cúbico. Ela não atribui dependência instantânea do estado a todo relógio. A curva de estado bilateral é par, e nenhum funcional instantâneo dela pode ter derivada1 na origem. A órbita modular estacionária também não parametriza a curva de amplitude não constante. Por isso as instâncias simultâneas pedidas na ordem, com essas propriedades incompatíveis, não são fabricadas. Fisher e entropia exigem a distinção de ramo/referência já estabelecida na040.

Cada tela isoladamente admite um relógio cúbico que anula o resíduo de quarta ordem, escolhido a partir de sua geometria; isso não estabelece igualdade finita exata. Isso controla o alcance da negativa. Para relógios com jato admissível, o coeficiente residual é
quarticMatchingCoefficient(b,η,σ) − 2λ log(2) B;
a diferença entre os dois λ necessários é r/96. O casamento quadrático condicionado permanece, pelo lema040 aplicado à classe. Não se prova aqui H3 físico a partir do estado.

[OPEN] Uma lei adicional que selecione a geometria, inclusive sua parte de maré, poderia restringir as telas admissíveis. O resultado refuta a exigência de um relógio somente do estado casar todas as geometrias admitidas nesta família; não refuta qualquer futura reconstrução com uma lei de seleção explicitada. O H3 finito geral não foi demonstrado.

## Área: a covariância não fixa a unidade

[REAL — compilação final] HorizonAreaScale considera uma família de operadores lineares ρ explicitamente fornecida, uma forma bilinear real h e o mesmo par de tangentes v,w. Se h é simétrica, estritamente positiva e ρ-invariante, αh também o é para α>0. O Gram do mesmo par é multiplicado por α, e sua densidade de área por α:
sqrt(det Gram(αh;v,w)) = α sqrt(det Gram(h;v,w)).

Com det Gram(h;v,w)>0, h e2h dão áreas positivas distintas mantendo ρ,v,w fixos. Logo invariância e positividade não selecionam um valor único de área. A conclusão pressupõe a existência dessa forma e desse plano não degenerado; não é uma impossibilidade de construir formas invariantes.

O vínculo com034 é exatamente a homogeneidade da função sqrt(det) aplicada à matriz angular cuja área de referência é2/9. Não se afirma que uma ação física dos TowerHorizon sobre essa tela foi construída. Protocolo de tangentes, ação física e normalização continuam dados a identificar.

[ONTO / CONJECTURE] A dobra como ponte entre fase e amplitude continua sendo uma proposta a formalizar. Mesmo que uma compressão angular produza um Gram, sua covariância não elimina automaticamente a escala. A045 não identifica o seletor IALD, J, log H e uma métrica física apenas por compartilhar vocabulário.

## Esperança aperiódica e shift

[DERIVED / OPEN] A revisão específica CONTINUACAO045_APERIODIC_REVIEW.md localiza a média ergódica discreta no mathlib e, de modo mais direto para a torre, uma rota pelas médias periodAverage(T), que já existem para qualquer T>0 sem periodicidade. Os novos passos necessários são: limite Cesàro das fases e de flowLevel; limite vetorial em Ω com cota de contração; levantamento a operador limitado pela ação direita densa; passagem ao limite da identidade prefixal; então os campos into, fixes e ortho de ExpectationInput. Normalidade e positividade completa exigem propriedades adicionais e não estão automaticamente contidas nesse registro mínimo.

A média de U(1) isoladamente não seleciona os fixos de todo U(t); a revisão dá o contraexemplo U(t)=exp(2πit). A próxima etapa deve trabalhar diretamente com os intervalos de média crescentes ou justificar a discretização escolhida.

[OPEN — objeto não construído neste lote] A busca dirigida em declarações Lean do kernel encontrou shiftedProfile e os entrelaçamentos nos geradores em ChainSiteFlow. Esses objetos não são um operador shift unilateral sobre TowerHilbert. Os evenShift/oddShift de TracelessAlgebra atuam em ellTwo e não serão tratados como esse operador da torre. Não foi produzido um teorema shift_is_not_a_horizon para um objeto que este lote ainda não construiu.

## Proveniência e verificação

As duas fontes v329 foram copiadas com snapshot byte a byte. Somente os imports dos módulos transpostos para a bancada foram ajustados, e quatro impressões de axiomas faltantes foram acrescentadas ao módulo modular. O replay do auditor reproduz exatamente as cópias adaptadas. Sua recompilação é reutilização de resultados; não são novos teoremas045. O selo canônico v329 não é revalidado apenas por essa cópia.

Os manifestos006/007 foram acrescentados às dependências históricas selecionadas. Seus auditores somente leitura passaram nesta sessão:006 conferiu408 hashes,32 teoremas e2 definições;007 conferiu459 hashes,58 teoremas e4 definições impressas. O registro está em CONTINUACAO045_HISTORICAL_CHECKS.json. Isso não recompila os módulos históricos.

O diretório final tem uma única raiz isolada de módulos, compartilhada pelas dependências copiadas com pin e pelos binários novos. Isso evita o sombreamento de TGLExt entre diretórios Lean. Não há fallback para a raiz Chatgpt nem para o build canônico. A fronteira histórica e os imports externos diretos são hashados; o fechamento transitivo completo de Mathlib/toolchain não é reconstituído.

Escritas exclusivamente em Chatgpt. Fontes originais, um.py, kernel canônico, Atlas, memórias e selos anteriores não são alterados. Nenhum dado observacional ou alteração de gate.

H3 do estado: OPEN. Reconstrução gravitacional geral: OPEN. Meta ampla de gravidade quântica: OPEN. Gate canônico intocado.

[REAL — interface solicitada] swapHorizon P p hp i j usa N=max(i,j); swap_horizon_left/right provam as trocas. expectation_commutes_with_site_swap compõe o horizonte com qualquer ExpectationInput; os lemas estacionário/tracial fornecem as esperanças concretas. swap_horizon_nonmodular cobre i≠j e todo tempo modular.
