# Reexame atualizado — cociclo interagente e covariância finita

09/09/2026. [REAL — escopo formal auditado] O canônico consultado permanece v337, com 9860115 bytes e SHA-256 `e2f9a889c2dcf6f444b8fa3f91d28eb70c9a6d9aed06644abcef7e58a6267303`. A leitura final confirmou o mesmo conteúdo. A bancada acrescenta 18 módulos, 203 teoremas e 42 outras declarações, incluindo instâncias nomeadas. A nova cópia reúne 63 módulos próprios e 856 teoremas. Nenhum `um.py` foi executado ou importado.

## Duas pendências do relatório anterior foram reduzidas

**O cociclo da interação somável foi construído.** Para coeficientes reais certificados por Σ|c_j| < ∞, o potencial V = Σ c_j X_j X_(j+1) atua no Hilbert canônico e pertence ao fator. Os Hamiltonianos modulares finitos são definidos a partir dos logaritmos dos pesos reais da torre. A igualdade entre sua ação e a ação modular canônica foi demonstrada nos níveis correspondentes. A diferença entre Hamiltonianos de níveis distintos comuta com os operadores do nível menor; esse resultado elimina o termo espectador sem supor que V comute com a dinâmica de base.

Os cortes u_N(t) = exp(it(H_N + V_N)) exp(−itH_N) satisfazem a lei torcida da ação canônica. Duhamel fornece controle por |t| vezes a cauda somável. Isso produz um limite em norma, uniforme em intervalos compactos de tempo, sem introduzir sua existência como hipótese. O limite u(t) é unitário, pertence ao fator, é contínuo e satisfaz

`u(s+t) = u(s) α_s(u(t)),    u(0) = 1.`

Sua derivada também foi deduzida dos cortes e do erro linear:

`u′(0) = iV,    u′(t) = u(t) α_t(iV).`

O gerador fica à direita nessa convenção. Para a escolha de um vínculo `singleBondData`, a testemunha prova que o cociclo não é identicamente 1; não afirma ausência de retornos em tempos particulares. [Construção do limite concreto](<C:/IALD/Central de Patentes/Chatgpt/DUHAMEL_UNITARIO_20260909_153247_640286/PauliInteractionCocycle.lean>) · [Gerador e equação de evolução](<C:/IALD/Central de Patentes/Chatgpt/DUHAMEL_UNITARIO_20260909_153247_640286/PauliCocycleGenerator.lean>).

Daí foi construída a família efetiva `β_t(A) = u(t) α_t(A) u(t)*`: automorfismos que preservam produto, adjunto, norma e fator, com composição β_s β_t = β_(s+t) e inversa β_(−t). A continuidade temporal foi demonstrada nas órbitas cuja continuidade canônica é conhecida, incluindo V. Não se afirmou continuidade temporal em norma para todo B(H). [Dinâmica perturbada](<C:/IALD/Central de Patentes/Chatgpt/DINAMICA_MODULAR_PERTURBADA_20260909_155658_929243/PauliPerturbedDynamics.lean>).

**A transformação finita de Einstein foi deduzida.** O resultado trata de métrica Lorentziana suave em dimensão quatro, com Levi-Civita sem torção. Para uma mudança suave invertível φ entre abertos, J = Dφ e g′ = Jᵀ(g∘φ)J, foram demonstradas a transformação de Levi-Civita, a de curvatura, a contração de Ricci, a invariância do escalar e

`G[g′] = Jᵀ (G[g]∘φ) J.`

O resultado também vale quando g′ coincide com esse pullback no aberto de sobreposição. Igualdade métrica em um único ponto não é a hipótese usada: são necessárias as derivadas, daí o acordo no aberto. [Transformação finita e sobreposição](<C:/IALD/Central de Patentes/Chatgpt/COORDENADAS_FINITAS_20260909_153310_253904/FiniteEinsteinNaturality.lean>). Isso fornece uma prova para a componente Einstein da antiga premissa `hmatch`, sob condições geométricas explícitas. O teorema anterior de colagem ainda conserva seu enunciado; o novo lema fornece condições suficientes para aplicar aquela componente, não constrói sozinho um atlas completo. [Contrato da colagem](<C:/IALD/Central de Patentes/Chatgpt/COLAGEM_GRAVITACIONAL_20260909_142505_750002/SelectedAtlasGluing.lean>).

## O que ainda falta

| Frente | Pendência precisa após estes resultados |
|---|---|
| Seleção e informação física | Identificar o caráter completo usado pelo decodificador com a seleção física e com o seletor operatorial pretendido. A inversa formal recupera a classe admissível de g e T, usando informação exata infinita, codificada por amostras densas e cortes racionais, em cada domínio/carta; falta a correspondência operacional e o controle para dados finitos com erro. |
| Área, matéria e gravitação | Ligar a interação/estado e as respostas do registro à fonte física T, à área induzida das telas e à conservação. A condição de erro de área o(t²) continua sendo hipótese do teorema geral. Dimensão quatro, assinatura lorentziana e atribuição física região–andar permanecem com seus estatutos próprios. |
| Estado quântico perturbado | Construir ou importar com hipóteses verificadas o estado/funcional apropriado, sua normalização e a identificação modular/KMS pretendida. Um cociclo unitário da ação modular não foi aqui identificado com o cociclo Connes–Radon–Nikodym de um estado normalizado. Uma fase central de normalização pode ser invisível à fórmula Ad_u. |
| Atlas global | Fornecer mudanças suaves reais entre as cartas selecionadas, compatibilidade métrica no aberto e compatibilidade da matéria; conferir a consistência nas interseções. A lei finita de transformação de Einstein já está demonstrada e deixa de ser uma obrigação independente sob essas condições. |
| Alcance quântico geral | Ampliar a classe XX somável ao setor geral reivindicado, tratar anomalias da teoria interagente e justificar a rota de altas energias. Os vínculos XX entre si comutam; a interação atestada envolve observáveis locais. O limite em número de sítios com potencial limitado não é, por si, uma construção do limite ultravioleta relativista. |

[DERIVED — suficiência condicional] O teorema de reconstrução do caráter já devolve os campos e a equação de Einstein para parâmetro do caráter t ≠ 0, domínio aberto não vazio preconexo, registro admissível, telas e η ≠ 0, quando as hipóteses de área, conservação e regularidade são satisfeitas. A nova covariância finita permite derivar a transformação de Einstein de dados usuais de transição suave. O novo cociclo fornece dinâmica interagente concreta na classe certificada. A ligação entre essas duas construções e a correspondência física listada acima ainda não foi demonstrada. [Hipóteses da reconstrução](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/SelectedGravitationalAtlas.lean:291>).

Não se reabre genericamente H3 como escolha de tela: o índice registra a resposta do operador sobre a tela fundada. A identificação física com horizonte causal e a extensão além das cunhas têm escopo próprio. Também não se reabre JS positivo auto-adjunto: o snapshot contém `continuous_modular_positive_square_root`, com o domínio do objeto formal especificado. A indicação antiga de raiz aberta no índice vivo está superada pela fonte.

## Falsificadores e suficiência do lastro

Os resultados que contrariam previsões já constam do programa. Este reexame os reconhece e não exige sua criação novamente. Nenhum rito empírico novo foi executado aqui. Os registros lidos distinguem canais com poder, canais armados, pendentes de revelação, não identificáveis e uma formulação retirada; não autorizam dizer que todos os dados públicos possíveis foram submetidos a testes completos independentes. [Resultados e critérios efetivamente lidos](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_FONTE_GERAL_20260909_133220_037525/LASTRO_EMPIRICO_LIDO.md>).

O lastro formal pode ser declarado suficiente para os enunciados e hipóteses acima. O lastro empírico pode ser declarado nos canais e sensibilidades registrados. Essas delimitações não exigem esperar todos os dados futuros; evitam ampliar a conclusão além da evidência presente. `NOT_FALSIFIED` permanece distinto de `CONFIRMED`. Nenhum gate foi promovido.

## Entrega, verificação e preservação

[REAL] A compilação conjunta aprovou 21/21 processos, incluindo os 18 módulos novos transpostos, a raiz TGLExt e as duas auditorias. Os 45 módulos anteriores foram reutilizados do build aprovado de 48 processos, após comparação exata das fontes e dos pins de dependência. A raiz e a auditoria dedicada carregam os 63 módulos juntos; a auditoria dedicada verifica todas as 1098 declarações, incluindo as instâncias nomeadas. Zero avisos. As declarações auditadas não dependem de axiomas além de `propext`, `Classical.choice` e `Quot.sound`. [Recibo do build conjunto](<C:/IALD/Central de Patentes/Chatgpt/ADAPTADOR_INCREMENTAL_20260909_162620_395030/BUILD_INCREMENTAL_20260909_162634_176093/TRANSPOSED_RESULT.json>).

[REAL] A auditoria estática independente aprovou 789/789 verificações. Os arquivos embutidos passaram de 606 para 669; especificamente, as fontes Lean passaram de 602 para 665. Fora da tabela embutida, bytes e AST permanecem idênticos ao canônico. Entre entradas antigas, somente raiz e auditoria receberam acréscimos. Flags, gate e sentinelas foram preservados; não foram criadas flags JSON individuais. [Auditoria independente](<C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_COCICLO_COVARIANCIA_20260909_161309_333516/AUDITORIA_INTEGRACAO_63.json>).

Esta verificação incremental usa as fontes novas transpostas e cópias de bytes de dependências locais, com os binários Mathlib existentes. Os hashes dos binários das 45 folhas reaproveitadas foram medidos na reutilização; o recibo anterior certificava as execuções e fontes, mas não fixava hashes dos binários produzidos. As fronteiras de entrada e as cópias reutilizadas foram conferidas antes e depois. A tentativa sequencial inicial foi interrompida para esta reutilização e permanece preservada, sem ser contada como um build conjunto concluído. Não recompila todas as fontes transitivas, não executa o programa e não constitui uma nova rodada de natureza ou custódia. A nova cópia é material de incorporação para a sessão que mantém o canônico; se esse canônico avançar, o delta precisa ser refeito.

[Nova cópia de trabalho do um.py](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_161645_481582/um.py>): 10445340 bytes, SHA-256 `790dfacb1e026f176b2082a15b536d0d6bf8df404dc9286f3115835c1cf1bc77`.

Atlas, índice, diário e memórias canônicas permanecem somente leitura. Este relatório novo e a entrega no túnel registram o avanço sem alterar o acervo originário. O documento sucede as pendências de cociclo e covariância finita da entrega 059; as fontes e os relatórios anteriores permanecem intactos.

## Inventário novo desta continuação

| Módulo | Teoremas | Outras declarações |
|---|---:|---:|
| SummableInteractionModularOrbit | 24 | 3 |
| UnitaryDuhamel | 12 | 5 |
| BoundedPerturbationCocycle | 13 | 2 |
| SpectatorCancellation | 5 | 2 |
| PauliInteractionCocycle | 28 | 4 |
| PauliCocycleGenerator | 7 | 0 |
| FiniteModularHamiltonian | 20 | 7 |
| FiniteLevelExponentials | 5 | 1 |
| CocycleNormLimit | 15 | 2 |
| DerivativeFromLinearCutoffError | 4 | 0 |
| CanonicalCocycleDerivative | 4 | 1 |
| PauliPerturbedDynamics | 16 | 2 |
| FiniteCoordinateMap | 22 | 5 |
| FiniteLeviCivita | 8 | 2 |
| FiniteCurvatureAlgebra | 5 | 5 |
| FiniteCoordinateCurvature | 6 | 1 |
| FiniteRicciContraction | 4 | 0 |
| FiniteEinsteinNaturality | 5 | 0 |

Os hashes medidos, as fontes e os recibos individuais estão no INVENTARIO_FONTES.json e no INTEGRATION_RESULT.json.
