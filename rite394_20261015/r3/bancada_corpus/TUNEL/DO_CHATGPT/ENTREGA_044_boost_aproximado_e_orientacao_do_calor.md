# ENTREGA 044 — boost aproximado e orientação do calor
06/09/2026. Bancada ChatGPT → túnel da sessão irmã.

[REAL] Continuação da linha H3 de041/043: o peso −kappa t é realizado por um campo de boost e seu fluxo geométrico explícitos. O pullback da métrica, o defeito de Lie e sua ordem transversal são calculados. A corrente central coincide com o fluxo de calor da tela043, e a orientação do passado até a origem é certificada.

A ordem010 apareceu durante a verificação desta etapa e foi lida. Seus alvos de horizontes não modulares, classe de relógios e seleção do protocolo de área ficam discriminados abaixo; não são declarados resolvidos pela044.

## Resultados

1. **Fluxo efetivo.** Na carta029, chi=−kappa u partial_u+kappa v partial_v e Phi_s(u,v,X,Y)=(exp(−kappa s)u,exp(kappa s)v,X,Y). Grupo, inversa, derivada temporal, Jacobiano espacial e preservação plana demonstrados. Na central gamma(t)=t d, chi=−kappa t d; para kappa>0,t<0, a componente temporal é positiva.
2. **Aproximação geométrica.** Para g=2du dv−dX²−dY²+(aX²+cY²)du², o pullback literal difere de g por (exp(−2kappa s)−1)(aX²+cY²)du². A expressão de Lie, calculada pelas derivadas efetivas, é −2kappa(aX²+cY²)du² e coincide com a derivada do pullback. Ela e seu primeiro jato zeram na central; o segundo jato transversal registra −4kappa a e −4kappa c.
3. **Controle negativo delimitado.** Se kappa≠0 e (a≠0 ou c≠0), esse campo não é Killing em nenhum aberto contendo0. Isso não exclui outros campos, nem invalida sua aproximação local. Os casos planos e de taxa zero são controles exatos.
4. **Calor.** Para qualquer tensor T, T(chi(gamma(t)),d)=−kappa t T(d,d), e a área literal043 liga essa contração a screenHeatFlux. Para waveMatter, Q_boost=opticalHeat041 globalmente e coincide com opticalScreenHeat043 como germe no passado. Fora da central só a contração especial com waveMatter é igual; os campos vetoriais não são identificados.
5. **Orientação.** Q_segment=integral de t até0=−Q_boost e DeltaA_segment=A(0)−A(t). O fluxo e Q_segment são não negativos para kappa,m≥0,t≤0. Os sinais do calor e da área se invertem juntos; o matching quadrático continua eta(a+c)=2pi m, para kappa≠0.

[INPUT / OPEN] A família de métricas, a carta e kappa são entradas. A cinemática vale para quaisquer a,c reais; a ligação à tela043 conserva a,c≥0 e sua regularidade local. kappa/(2pi) é a normalização herdada, sem derivação de temperatura Unruh/KMS. Não há identificação com o fluxo modular, seleção da métrica pelo estado ou construção de horizonte causal global.

## Precisão solicitada pelo operador

[ONTO / CONJECTURE] L como cauda/poço e a geometria como inscrição da leitura angular são a hipótese a investigar. Não se identifica L_phi do Atlas com log H de030–033 sem ponte própria.

[DERIVED — álgebra fora dos novos lemas044] Uma amplitude projetada r em duas direções ortogonais igualmente escaladas dá Gram G=|r|² I_2 e densidade de área relativa sqrt(det G)=|r|². Com amplitudes distintas, a densidade é |r_1 r_2|. A tela isotrópica043 realiza A(t)=cos²(sqrt(a)t) numa métrica já fornecida; não demonstra origem dessa amplitude na fase de L. Protocolo, escala e identificação física continuam OPEN.

[DERIVED / OPEN] No fluxo044, a central aproxima a origem quando s→+infinito e kappa>0, mas a direção conjugada v cresce exponencialmente. Esse fluxo não é estável perante perturbações gerais da origem no espaço coordenado. Isso não decide a estabilização física proposta: parâmetro de boost, tempo afim, dinâmica material e fluxo modular não foram identificados. Retorno periódico, positividade da área e atração não são equivalentes.

## Verificação

[REAL] Compilação final limpa em CONTINUACAO044_CLEAN_20260906_224045_647263: 76 teoremas, 14 definições, 90 prints, zero instâncias. Quatro módulos e Imports044All: 5/5 PASS, exit0, sem erros/avisos, cobertura exata e somente propext, Classical.choice, Quot.sound.

[REAL] Auditoria independente --build-only: BUILD_PASS/exit0, 2.066 arquivos de build e 207 registros históricos. Fontes4/4 idênticas às cópias compiladas; 2.047 inputs congelados idênticos antes/depois. Metadados, logs, binários, hashes, importador e linhas de axiomas também conferidos diretamente. Tentativas e backups anteriores preservados. O manifesto final é produzido após esta entrega.

## Artefatos

| Artefato | Bytes | SHA256 lido dos bytes |
|---|---:|---|
| [CONTINUACAO044_PARECER.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO044_PARECER.md>) | 11723 | 3da8c063949633bbd2741a940ec8dcb2ac50b7b58200ef9075662132fa14180e |
| [CONTINUACAO044_DERIVACAO_PREVIA.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO044_DERIVACAO_PREVIA.md>) | 5181 | f371bb66aae4dfbf2e50dedd72c415450c73ef8f8ab645e9c8f9b6fc65c4dd5b |
| [ApproximateBoostFlow.lean](<C:/IALD/Central de Patentes/Chatgpt/ApproximateBoostFlow.lean>) | 13752 | 7ebef02628695e63527764baa04283ab7b3325f59b5dbf5e0848da0158b1fdba |
| [BoostMetricPullback.lean](<C:/IALD/Central de Patentes/Chatgpt/BoostMetricPullback.lean>) | 5498 | 66a64e6a57aaa010258423e4698ff8e898914d1f1110a3c41ffd0109f7496b55 |
| [BoostMetricJets.lean](<C:/IALD/Central de Patentes/Chatgpt/BoostMetricJets.lean>) | 7673 | 97644f0b3ae15658c786f421afcec46b0bb31ea0cfa0a60d3fe438b88604a440 |
| [BoostHeatConstruction.lean](<C:/IALD/Central de Patentes/Chatgpt/BoostHeatConstruction.lean>) | 9266 | 234220c4ca22132fb06bf0f467d6485b4da3e40b352bb6d724e77117b476bad1 |
| [clean_continuation044.py](<C:/IALD/Central de Patentes/Chatgpt/clean_continuation044.py>) | 32336 | 8f5bfb006e145323c99a5ac6b126cc568fdc25651c1dd79d448965becbab5216 |
| [audit_continuation044.py](<C:/IALD/Central de Patentes/Chatgpt/audit_continuation044.py>) | 40311 | 6f52af094ed87d4811be967af09176f8acf7e1b79a76d07f28c5c6a566ec0fb9 |
| [revise_continuation044.py](<C:/IALD/Central de Patentes/Chatgpt/revise_continuation044.py>) | 2100 | 6f84c229b1b293fe4fd48be61994541b797ce88c089c5cdb6d6843fb866d8069 |
| [CONTINUACAO044_CLEAN_BUILD.json](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO044_CLEAN_BUILD.json>) | 1359345 | 2e0ed7e6535e1963b5f1c2fdd8e840d78a007589dc1fabc9ab33fa94a4c4d6ea |

O manifesto é CONTINUACAO044_MANIFESTO.json, produzido pelo auditor após esta entrega, sem dependência circular. Auditoria selada somente leitura:
`C:\Python314\python.exe -B "C:\IALD\Central de Patentes\Chatgpt\audit_continuation044.py"`.

## Critérios e continuidade da ordem010

- **A — horizontes.** Não construídos pela044. As fontes TheLiftFiresOnThePeriodicTower e TheModularFlowIsAHorizon foram localizadas e lidas, sem revalidar a custódia v329. A triagem aponta a rota da matriz local unitária V, comutante com a densidade, seguida de U=towerPi(V). Restam a permutação concreta, invariância dos pesos, ação literal nos sítios e controle de não modularidade. A esperança aperiódica continua OPEN.
- **B — relógio e H3.** A044 justifica o campo geométrico e a corrente, preservando o balanço infinitesimal condicional. Não define StateClock nem resolve a dicotomia proposta. Sob eta>0 e B>0, a040 impede um relógio único de casar simultaneamente duas geometrias do mesmo estado; isso não implica que todo relógio falhe em cada geometria isolada. Uma classe instantânea bilateral enfrenta a paridade da curva; Fisher/entrópico usam orientação/referência e a órbita modular estacionária não percorre essa curva.
- **C — área.** [DERIVED — fora do Lean044] Se h é invariante, alpha h também o é para alpha>0; em dimensão2, a densidade de área multiplica por alpha. Invariância isolada não fixa a escala. Não foi selecionado um protocolo físico nem construída uma ponte região–álgebra.
- **Guardas.** Escritas somente em Chatgpt. Originais, um.py, kernel canônico, Atlas, memórias, gates e selos anteriores somente leitura. Nenhum dado observacional e nenhuma alteração de gate.
- **Limites da custódia.** Binários históricos conferidos por hash, sem recompilação histórica. Fontes canônicos sem pin histórico de fonte servem à descoberta de imports; o fechamento transitivo inteiro de Mathlib/toolchain não é hashado.
- **Referências primárias.** Jacobson, https://arxiv.org/pdf/gr-qc/9504004, para boost aproximado e entradas térmicas; Kolodrubetz et al., https://arxiv.org/abs/1602.01062, para métrica de estados. As referências não demonstram a ponte física proposta pelo operador.

H3 do estado: OPEN. Reconstrução gravitacional geral: OPEN. Meta ampla de gravidade quântica: OPEN. Gate canônico intocado.

Somente o operador decide a incorporação ao acervo canônico e a confirmação física; esta entrega não realiza esses atos.
