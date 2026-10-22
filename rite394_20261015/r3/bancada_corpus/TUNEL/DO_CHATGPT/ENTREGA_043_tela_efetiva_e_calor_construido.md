# Entrega 043 — tela efetiva de Jacobi e calor construído

06/09/2026. Complemento à ORDEM009. [REAL / DERIVED / INPUT / OPEN].

Foi construído um habitante explícito de EquilibriumScreenData para a curva e as colunas de Jacobi036. O construtor geométrico recebe apenas os parâmetros a,c≥0 da métrica escolhida. Não recebe estado, matéria, entropia, calor, eta ou casamento de Clausius.

No aberto onde cos(√a u) e cos(√c u) não zeram, as razões q_a=F'/F e q_c=G'/G satisfazem Riccati. O campo V=(1/2+B,q_a X,q_c Y,1/2−B), B=[(q_a²−a)X²+(q_c²−c)Y²]/2, é suave, não nulo, nulo para a métrica e geodésico. Na curva central seu gradiente é diag(0,q_a,q_c,0), zero na origem. A tela usa literalmente [F(t)e1,G(t)e2], com área |F G|. O parceiro nulo do frame tem o sinal g(d,n)=−1.

A função opticalScreenHeat instancia constructedHeat com essa tela. Sua igualdade com opticalHeat041 foi provada como germe em t→0−, pela congruência das integrais no intervalo passado suficientemente pequeno. Não se afirma igualdade global entre extensões contínuas arbitrárias.

Sem casamento, o defeito de Clausius satisfaz
lim D(t)/t²=kappa[eta(a+c)−2pi m]/(4pi).
Para kappa≠0, o balanço quadrático equivale a eta(a+c)=2pi m. No controle a=c=0, a tela existe e A=1; m≠0 e kappa≠0 impedem esse balanço. Assim, a construção da tela não esconde a condição física.

Sob casamento e kappa,eta>0,a+c>0, a quarta ordem transportada é
lim D(t)/t⁴=kappa eta(a²+c²)/(24pi)>0.
Esse resíduo positivo impede igualdade finita exata no modelo, preservando o balanço infinitesimal.

A precisão angular do operador foi registrada como construção ilustrativa separada dos teoremas043: uma amplitude projetada pode produzir uma inscrição quadrática, e duas direções ortogonais iguais dão G=|r|² I_2 e sqrt(det G)=|r|². Na tela isotrópica a=c, a área é cos²(√a t). Isso não identifica a amplitude de Jacobi com a fase de L, nem deriva isotropia, métrica, escala física ou estabilização do estado. A ressalva034 sobre área dos raios GNS versus observabilidade no estado restrito permanece explícita. O gradiente zero na origem é uma condição instantânea; não é um teorema de retorno estável.

## Verificação

[REAL — compilação final e auditoria independente] Em CONTINUACAO043_CLEAN_20260906_215833_696140, os quatro módulos e Imports043All passaram: 60 teoremas, 15 definições, 75 impressões de axiomas e zero instâncias. Os cinco passos retornaram exit0/PASS, sem erros ou advertências, com cobertura exata e apenas propext, Classical.choice e Quot.sound. As quatro fontes de trabalho são idênticas às cópias compiladas; os snapshots de 2.029 entradas congeladas permaneceram idênticos em bytes. O auditor independente --build-only retornou BUILD_PASS/exit0, conferindo 2.048 arquivos de build e 180 registros históricos. O revisor também conferiu diretamente os cinco metadados, logs, hashes de fonte/binário, o censo real das linhas de axiomas e o importador literal. As tentativas anteriores e os backups foram preservados. O manifesto final será produzido depois do parecer e da entrega; sua auditoria somente leitura confere a custódia completa.

| Artefato | Bytes | SHA256 lido dos bytes |
|---|---:|---|
| [CONTINUACAO043_PARECER.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO043_PARECER.md>) | 9360 | 5a1d7f422e7419bd9ae553594172c51874444adfd49c58bf05ecd1c4fa4fbabd |
| [CONTINUACAO043_DERIVACAO_PREVIA.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO043_DERIVACAO_PREVIA.md>) | 5014 | 3e664034600d5af5cf58732c3bdf1d986d54d15ba428da3f9ca2d9471f717127 |
| [JacobiRiccatiProfile.lean](<C:/IALD/Central de Patentes/Chatgpt/JacobiRiccatiProfile.lean>) | 5406 | 5441c477b069389595679796e218e5e881383ab7316766ec2e6cfbf87af8ccd4 |
| [OpticalNullCongruence.lean](<C:/IALD/Central de Patentes/Chatgpt/OpticalNullCongruence.lean>) | 16018 | 9e3a0ea12d518fe8739903e43e25aecf1bc3e8355a6febce9ceebb7811b30b6f |
| [OpticalEquilibriumScreen.lean](<C:/IALD/Central de Patentes/Chatgpt/OpticalEquilibriumScreen.lean>) | 12752 | 2b1e893f16a3567fd24dbd6f2d561bb2c6ce65ff134aeb0a5a54b72ad3834403 |
| [OpticalConstructedHeat.lean](<C:/IALD/Central de Patentes/Chatgpt/OpticalConstructedHeat.lean>) | 10531 | bf052a256ae8a16b1e4499cd673439cebf74d81bf5d45a3badc0c2badb5ad63a |
| [clean_continuation043.py](<C:/IALD/Central de Patentes/Chatgpt/clean_continuation043.py>) | 32328 | 5f5252066c4652c39989a1d7feb05d149b9c1ce555a2a2dcd567ae377c2bf258 |
| [audit_continuation043.py](<C:/IALD/Central de Patentes/Chatgpt/audit_continuation043.py>) | 40039 | 47f690d847ab8b2d87aa84aae9fe75421ece72fa08b335b4f45afa6efc68f596 |
| [revise_continuation043.py](<C:/IALD/Central de Patentes/Chatgpt/revise_continuation043.py>) | 2112 | 859e9464db8d8702f78f791cdb6289d07f8fb1f9930f6ee9f46d0369424e3d7e |
| [CONTINUACAO043_CLEAN_BUILD.json](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO043_CLEAN_BUILD.json>) | 1347788 | ab9f9903ced9aaa32911a13a6aa52b0ba428805453587164118a99b9ceaea84f |

O manifesto é CONTINUACAO043_MANIFESTO.json, produzido pelo auditor depois desta entrega, evitando dependência circular entre hashes. Auditoria selada, somente leitura:
`C:\Python314\python.exe -B "C:\IALD\Central de Patentes\Chatgpt\audit_continuation043.py"`.

## Critérios da ordem e limites

- A — relógio relativo: esta entrega não seleciona um relógio canônico a partir do estado. Os resultados039/040/041 permanecem antecedentes; nenhum parâmetro foi ajustado para acertar a área.
- B — H3: foi removida a lacuna entre a tela explícita036 e o tipo geométrico usado pelo calor020. O casamento térmico é uma condição independente com equivalência e controle negativo provados. H3 a partir do estado permanece OPEN.
- C — região–álgebra: nenhuma ponte nova é reivindicada.
- INPUT: carta029, família de métricas com a,c≥0, normalização afim, fonte waveMatter e interpretação física dos parâmetros. Não há reconstrução da métrica nem seleção de escala a partir do estado nesta etapa.
- Domínio: certificação geométrica local no aberto sem zeros dos fatores de Jacobi. Ele pode ser desconexo; não se afirma que todo o aberto precede a primeira cáustica, nem que há horizonte causal global.
- Igualdades: curva, colunas e área são funções literais036. Identificação do constructedHeat é germinal no passado. O peso −kappa t não é identificado com um gerador físico de Killing/modular em todas as ordens.
- Guardas: escritas somente em Chatgpt; originais, um.py, kernel canônico, Atlas, memórias, gates e selos anteriores somente leitura. Nenhum dado observacional.
- Custódia: binários históricos conferidos por hash, sem recompilação histórica. Fontes canônicos sem pin de fonte servem à descoberta de imports; dependências externas diretas conferidas, sem hash de todo fechamento transitivo de Mathlib/toolchain.
- Estatutos: o cálculo angular e a consequência de não estacionariedade q_a'(0)=−a são identificados como álgebra analítica fora dos novos enunciados Lean. A ausência de uma solução estacionária zero para a>0 não é apresentada como prova de instabilidade.

H3 do estado: OPEN. Reconstrução gravitacional geral: OPEN. Meta ampla de gravidade quântica: OPEN. Gate canônico intocado.

Somente o operador decide a incorporação ao acervo canônico e a confirmação física; esta entrega não realiza esses atos.
