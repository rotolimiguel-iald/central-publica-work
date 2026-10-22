# ENTREGA045 — horizontes de permutação, relógio comum e escala da área

06/09/2026. Bancada ChatGPT → túnel da sessão irmã. Resposta à ORDEM_010.

[REAL] Quatro módulos novos. As duas fontes v329 são dependências recompiladas: NÃO incorporar novamente como novidade. O parecer detalha enunciados, hipóteses e limites.

## Critérios da ordem

| Critério010 | Resultado e limite |
|---|---|
| A1 — troca de sítios | swapHorizon P p hp i j construído; ação literal, unitariedade, normalização do fator e preservação do estado por prova. |
| A2 — permutações | Lei de grupo e ação n→σ(n), cauda nos sítios m>N fixa, covariância das esperanças estacionária/tracial. Se um sítio é movido, sua projeção distingue a ação de todo tempo modular. São horizontes algébricos; identificação física OPEN. |
| A2 — shift | Operador unilateral de sítios sobre TowerHilbert ainda não construído neste lote. shiftedProfile e os shifts em ellTwo não são substitutos. Não se inventa shift_is_not_a_horizon. |
| A3 — aperiódico | Habitante geral OPEN. Nota045 identifica média ergódica disponível e rota Cesàro → limite em Ω → levantamento limitado pela ação direita → identidade prefixal → into/fixes/ortho. Normalidade/CP exigem propriedades adicionais. |
| B1 — StateClock | Classe cinemática com origem, derivada1 e jato; sem supor difeomorfismo local ou dependência instantânea. Instâncias instantânea/modular incompatíveis não são fabricadas. A negativa vale para classe maior: qualquer g comum e qualquer regra da mesma história do estado. |
| B2 — dicotomia | η>0,B>0; duas telas σ=0,r/4 com mesmo estado e mesmo tensor Ricci, r=R(d,d). Diferença dos resíduos/t⁴ → +ηr²/96. Para todo g comum alguma tela falha; cada tela isolada admite relógio que cancela a quarta ordem. Gap λ*=r/96. Não se conclui falha de todo relógio em toda geometria. |
| B3 — H3 | Casamento quadrático condicionado preservado e residual quártico explícito. H3 físico e lei finita geral OPEN. Não há lei de sexta ordem. Uma lei adicional pode selecionar a geometria e restringir as telas. |
| C — área | Mesma ação fornecida e mesmas tangentes: h e αh preservam invariância/simetria/positividade, α>0; área multiplica por α. Para Gram não degenerado h e2h distinguem escalas. Covariância não fixa normalização; ação física em tangentes e ponte região–álgebra OPEN. |

## Verificação

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

Os snapshots v329 preservam bytes originais; somente imports foram transpostos à bancada e quatro prints acrescentados. O auditor reproduz as cópias adaptadas e exige sua custódia antes de compilar. Isso não revalida o selo canônico v329.

Instâncias declaradas novas: zero. O lote foi compilado junto em raiz isolada, sem fallback à raiz Chatgpt ou ao build canônico. Binários históricos006/007/029–043 são copiados com pins e não recompilados. Fontes históricas canônicas sem pin fonte↔binário servem à descoberta de imports; essa proveniência não é inventada. O fecho transitivo externo completo de Mathlib/toolchain não foi hashado. Probes são desenvolvimento; tentativas e backups foram preservados.

## Artefatos

| Artefato | Bytes | SHA256 lido dos bytes |
|---|---:|---|
| [CONTINUACAO045_PARECER.md](</C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO045_PARECER.md>) | 9382 | c4f3ed38090a1f1bc702fc78ec8fc62dd7a1a83bbd7b3679bdbc748e7a1761a7 |
| [CONTINUACAO045_DERIVACAO_PREVIA.md](</C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO045_DERIVACAO_PREVIA.md>) | 2454 | 61407c70fd2d967a7899251006bfbdad02fb2344f9dd24359aa47e04c3b54800 |
| [FiniteSitePermutations.lean](</C:/IALD/Central de Patentes/Chatgpt/FiniteSitePermutations.lean>) | 11564 | 3293874b12e272021bb0a8ed2630b00824759d5f4bfce4ae7bc41b31c5dd6a7d |
| [FiniteSiteHorizons.lean](</C:/IALD/Central de Patentes/Chatgpt/FiniteSiteHorizons.lean>) | 12559 | cc0921dfa7c73f1207241b5a18227845fd6de2207de9d83785a5348477123fe5 |
| [StateClockDichotomy.lean](</C:/IALD/Central de Patentes/Chatgpt/StateClockDichotomy.lean>) | 11985 | 1af1f9e53f93c45dd8ded08d7bb06b67088ace4a058ce74139f231b62bf822da |
| [HorizonAreaScale.lean](</C:/IALD/Central de Patentes/Chatgpt/HorizonAreaScale.lean>) | 7662 | 6f62d415c99ceb347192b0df882271491f7c5f6bd69428f260413d3a9d9c5eff |
| [CONTINUACAO045_UPSTREAM.json](</C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO045_UPSTREAM.json>) | 4326 | 0df23179998f85b18c6676701e59667af824198b24dcf859ea224042e9c8a545 |
| [CONTINUACAO045_APERIODIC_REVIEW.md](</C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO045_APERIODIC_REVIEW.md>) | 13045 | ebc0febc4f4e8d9e65ae9b7560d2d02ac92bdeb1f6b8009fa9b58f579c7209a4 |
| [CONTINUACAO045_REVISAO_INDEPENDENTE.md](</C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO045_REVISAO_INDEPENDENTE.md>) | 9175 | 812d9c1275f1c7389d33bc8c6bf8651136d5276e6b2b1d600834506c3d6953b8 |
| [clean_continuation045.py](</C:/IALD/Central de Patentes/Chatgpt/clean_continuation045.py>) | 33316 | 42d030a6a203bcb5496605727630df3b1b8aa626240cd76a78f8a99db726d117 |
| [audit_continuation045.py](</C:/IALD/Central de Patentes/Chatgpt/audit_continuation045.py>) | 46632 | 4726e0a3bbe2f3c9f7c3d6fbf4afb0a4d8feab5adfc76d69bb78369058a6a380 |
| [revise_continuation045.py](</C:/IALD/Central de Patentes/Chatgpt/revise_continuation045.py>) | 2231 | 85e320ffeaaa51a8956b22390c8b714e37ccec7a71edc3695ac8fcd82aa35935 |
| [prepare_continuation045.py](</C:/IALD/Central de Patentes/Chatgpt/prepare_continuation045.py>) | 3731 | 70d912fcf5505d9f764f06efe1ab50d33bfcc4b64ecd243e72209946d70ff4ef |
| [probe_continuation045.py](</C:/IALD/Central de Patentes/Chatgpt/probe_continuation045.py>) | 4147 | a62212568d639c2df85e7f6bc39020e029e33fe004cdf33c87138bcb62fd97ac |
| [CONTINUACAO045_HISTORICAL_CHECKS.json](</C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO045_HISTORICAL_CHECKS.json>) | 1493 | 71f8ab1c46c2a3d1823be53c10720d81a257328fe827d4578a2efce0b650dc03 |
| [CONTINUACAO045_CLEAN_BUILD.json](</C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO045_CLEAN_BUILD.json>) | 1506564 | 55c3e06c473445e7453acb85e8a68856fe614c207516e26a80c2563ba7d88460 |
| [finalize_reports045.py](</C:/IALD/Central de Patentes/Chatgpt/finalize_reports045.py>) | 10559 | 9e48bda5bae84b467c2289eea19b77495b61f0c5d1d269d6628da5e094f1c3e6 |

CONTINUACAO045_MANIFESTO.json é produzido após esta entrega, sem circularidade. Auditoria selada somente leitura:

    C:\Python314\python.exe -B "C:\IALD\Central de Patentes\Chatgpt\audit_continuation045.py"

Escritas somente em Chatgpt. Nenhum dado observacional ou alteração de um.py, kernel canônico, Atlas, memórias, gate ou selos anteriores. A046 começou em arquivos separados para a esperança aperiódica; não é parte nem resultado compilado deste selo.

H3 do estado: OPEN. Reconstrução gravitacional geral: OPEN. Meta ampla de gravidade quântica: OPEN. Gate canônico intocado.

Somente o operador decide a incorporação ao acervo canônico e a confirmação física; esta entrega não realiza esses atos.
