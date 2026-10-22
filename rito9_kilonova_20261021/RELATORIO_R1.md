# Rito 9 — revisão e primeiro teste sintético

21/10/2026, codex-gerente-tgl. Unidade F1.RITO9_KN_20261021, reivindicação 1089.

## Resultado

**[REAL — cálculo local]** Executado `test_rito9.py` após gravar `PREREG_SYNTHETIC_R1.json`: 20 verificações passaram, incluindo controles contrários às interpretações fortes da proposta. Foram geradas 200.000 esperas sintéticas, semente 20261021. Isso verifica cálculos do modelo; não são 200.000 neutrinos observados nem uma significância experimental. `observed_sigma = null`.

**[DERIVED — condicional]** A escala de milissegundos de Kimi é reproduzida sob H-SEQ. A proposta merece desenvolvimento, mas ainda não define um teste observacional discriminante. O alcance atual é uma distribuição de transporte candidata, com hipóteses físicas explícitas. Não se atribui 5σ, nem zero sigma: a estatística observacional ainda não está definida.

Reaproveitados oito arquivos originais do caderno Kimi, custodiados por bytes e SHA256 em `sources/` e `CUSTODY_R1.json`. A rota consultada foi `d7.kilonova_fronteira_aguda` (1305/1307/1309/1311). O Nós Vivo não reconheceu a unidade recém-criada; essa falha foi visível, e a consulta à rota/fontes foi feita diretamente. Nenhum índice foi reconstruído. O script original do seletor usa beta literal; a execução nova extrai apenas ALPHA_FINE_CODATA_2018 da fonte um.py, sem importá-la, e calcula beta em runtime. Originais e um.py conferidos antes/depois, intactos. A presença do candidato Lean foi lida; sua recompilação não foi realizada nesta entrega e o build declarado pelo Kimi não é apresentado como build nosso.

## 1. O que a espera geométrica realmente entrega

Assumindo tentativas independentes, probabilidade de admissão p=beta e duração t0=l/c:

P(N=n)=beta(1-beta)^(n-1), n>=1.

E[T]=t0/beta; Var(T)=t0²(1-beta)/beta².

Se o observável desconta a travessia livre t0, E[T_adicional]=t0(1-beta)/beta. O documento M1 chama t0/beta de correção sobre free-streaming; isso precisa dessa subtração. Se t0 for uma espera adicional por definição, a convenção pode mudar, mas deve ser explicitada antes do teste.

| l exploratório [INPUT] | média total (ms) | média adicional (ms) | desvio-padrão (ms) |
|---|---:|---:|---:|
| 10 km | 2,772469 | 2,739113 | 2,755741 |
| 20 km | 5,544938 | 5,478226 | 5,511481 |
| 30 km | 8,317408 | 8,217338 | 8,267222 |

Beta runtime = 0,012031300400803142. theta_M = 6,297289216°.

Para 20 km, os quantis 5%, 50%, 95% da espera TOTAL individual são 0,333564, 3,869344 e 16,544779 ms. Eles não são intervalo de confiança da média. A dispersão não inviabiliza por si só uma medida com muitos eventos; exige uma verossimilhança de distribuição e contagem detectável. O primeiro sinal de m pacotes simultâneos independentes tem probabilidade por tentativa 1-(1-beta)^m, e não a mesma espera média de um pacote. Uma população com tempos diferentes de emissão exige ainda convolução com o perfil da fonte.

## 2. Passagens físicas ainda não demonstradas

1. **[CONJECTURE] H-SEQ não decorre da primeira lei.** deltaS=delta<K> não fixa taxa, tempo entre tentativas ou independência. Uma matriz unitária repetida mantém interferência; o modelo geométrico exige monitoramento/decoerência ou uma dinâmica de salto equivalente. Além disso, |R|²=beta é reflexão na convenção óptica: identificá-la com admissão do neutrino exige declarar qual saída é detectada. Se a admissão fosse a transmissão 1-beta, a média para 20 km seria 0,067525 ms. Não se escolhe o ramo pelo sinal desejado.
2. **[OPEN] l não está determinado pelas massas apenas.** Raio da neutrinosfera, espessura da camada, caminho livre e comprimento de uma tentativa são objetos distintos. Equação de estado, sabor, energia e estado do remanescente importam. A literatura de simulações mostra diferentes superfícies de desacoplamento e energias típicas MeV [Endrizzi et al., https://arxiv.org/abs/1908.04952v2]. Os 10–30 km foram mantidos como INPUT exploratório.
3. **[OPEN] Canal de referência GW.** Se ambos recebem a mesma contribuição média, ela cancela na média nu-GW. Isso não garante cancelamento realização a realização: dependeria da correlação entre transportes. A isenção GW precisa vir da dinâmica ou de fonte independente, não de uma escolha favorável de governança.
4. **[OPEN] Perfil de emissão e propagação.** O atraso de produção, transporte ordinário, massa do neutrino, resposta instrumental e distância têm de entrar. Para neutrinos relativísticos, o atraso cinemático inclui aproximadamente (D/2c)(m_nu c²/E)², distinto de uma espera local. Tempos locais precisam ser transportados ao relógio observado, incluindo fatores gravitacionais/cosmológicos pertinentes.
5. **[DERIVED] A média sozinha identifica l/beta.** Alterar ambos proporcionalmente preserva essa média. A distribuição discreta completa pode distinguir os parâmetros se a resolução for suficiente; não se afirmou degenerescência exata dela. Se o perfil intrínseco da fonte for irrestrito, ele também pode absorver a convolução de transporte: é necessária informação independente sobre a fonte.

## 3. Ângulo, seletor e fase

**[DERIVED/REAL numérico]** A condição polinomial do seletor foi conferida em casos numéricos. Não seleciona beta sem um observável físico especificado. Um projetor em qualquer direção phi fornece seletor theta=-phi módulo pi/2 na convenção matricial do arquivo. A=I comuta em todos os ângulos. A forma tan(2theta)=2b/(c-a) precisa das condições para dividir; a forma polinomial conserva os casos degenerados.

O próprio script Kimi reconhece que projetor em +theta_M dá 90°-theta_M no intervalo positivo pesquisado. Isso não invalida o lema, mas a passagem para abertura POSITIVA espacial precisa declarar orientação e ramo. Também falta a relação física entre ângulo de mistura de dois setores e semiabertura do jato (núcleo, asas, dependência temporal). H-KN sozinha, tal como escrita, fixa uma probabilidade; não fornece essa relação espacial. Ejecta massiva não alcança infinito nulo: a justificativa correspondente deve ser corrigida ao lado. Isso não é refutação da conjectura inteira.

**[DERIVED — contraexemplo]** theta constante não implica dS/dE=0. Para S(E)=exp(i E tau/hbar) R(theta), as probabilidades de mistura são constantes, mas Q=-i hbar S†dS/dE=tau I. A rota de Wigner é nula para a matriz inteira independente de energia; não foi eliminada para qualquer realização física. Fases que dependem da energia precisam de convenção de referência e podem carregar tempo.

**[DERIVED — unidades]** Na árvore F1/F2 preservada no documento FECHO, para 10–100 km, (l/c)beta é aproximadamente 0,4–4 microssegundos, não milissegundos; (l/c)theta_M é aproximadamente 3,7–37 microssegundos. A correção posterior para beta^-1 é outra hipótese de mecanismo e não apaga esse erro de unidades histórico.

## 4. Acesso instrumental

**[KNOWN — literatura, não dado reanalisado]** O canal de neutrinos térmicos do remanescente é MeV. A sensibilidade a neutrinos de alta energia do jato não se transfere automaticamente a ele. O trabalho de Kyutoku–Kashiyama apresenta, sob seus modelos e taxa, uma estimativa de cerca de 2500 fusões até 200 Mpc para detectar um único neutrino térmico, com exposição de ordem 80 Mt ano: https://arxiv.org/abs/1710.05922v3. É uma projeção publicada de 2018, não um limite universal nem um inventário atualizado de todos os instrumentos de 2026.

A busca conjunta de GW170817 não encontrou neutrinos coincidentes de alta energia nem um surto MeV: https://arxiv.org/abs/1710.05839v2. Não há nesse evento uma amostra de atrasos térmicos para executar o teste proposto. Esses resultados de literatura não foram somados à Fase 9 e não constituem teste novo da TGL.

## 5. Forma aprimorada que pode virar teste

Usar um kernel de transporte normalizado, não um deslocamento determinístico:

K_beta(t|l)=sum_{n>=1} beta(1-beta)^(n-1) delta(t-n l/c).

Para o atraso adicional, usar (n-1)l/c. Construir a intensidade de eventos detectados como a convolução do perfil fonte F_nu(t,E|Theta), K_beta, propagação e resposta instrumental, somada ao fundo. Para o ramo nulo, definir transporte padrão e as mesmas incertezas e seleção. Verificar se H-SEQ é contribuição adicional ou substituição de transporte já contabilizado: somá-la duas vezes seria erro.

O estudo de poder deve fixar fonte, distâncias, detector, exposição e nuisance parameters independentes do atraso. Simular ambas as hipóteses, calibrar a razão de verossimilhanças sob o nulo e informar taxa de falso positivo e poder. Não usar sqrt(delta chi²) automaticamente nem multiplicar testemunhas dependentes. A procura por canais/seleções também exige controle de multiplicidade apropriado. Um número grande de amostras Monte Carlo melhora a precisão computacional, não cria neutrinos detectados.

**Próxima ação física:** fornecer uma realização de transporte que fixe o ramo de admissão e o relógio GW; obter l e perfil de emissão de uma simulação BNS independente; então calcular contagens/resolução e poder. A comparação de aberturas de jato pode ser estudada separadamente depois de fixar o mapa angular e a distribuição nula. Não ajustar a GW170817 nem escolher l para atingir 5σ.

## Limites desta entrega

Relatório técnico local, ainda sem aceite de c1 ou revisão independente desta camada. Nenhum novo provedor acionado. Não executadas as instruções de infraestrutura embutidas no handoff, nem instalados candidatos. O um.py base e as oito fontes originais permaneceram byte a byte iguais nos pinos antes/depois. A ordem foi cumprida na parte hoje executável: exame e teste sintético. Teste observacional e poder de 5σ permanecem OPEN pelos motivos específicos acima.
