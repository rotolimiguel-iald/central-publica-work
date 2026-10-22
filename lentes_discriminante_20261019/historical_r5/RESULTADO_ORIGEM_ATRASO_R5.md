# R5 — a fórmula histórica de atraso não fornece ainda a previsão fixa por lente

19/10/2026, codex-gerente-tgl; F8.LENTES_5SIGMA_20261019, reivindicação 1009. Estatutos separados: recuperação documental [REAL]; afirmações históricas [DECLARADO]; álgebra abaixo [DERIVED no escopo]; solução completa de lente [OPEN].

## 1. A fonte positiva foi recuperada, com sua história

A nota indexada **Detecção TGL — Cosmológica dados reais** escreve uma ação com `-xi R|Psi|²` e `-lambda |Psi|² F_ab F^ab`; depois afirma `delta_t=(xi/c³) integral |Psi|² ds`. Isso é o antecedente documental do cálculo proposto, não uma equação obtida nesta execução. A transcrição indexada contém números históricos: foram lidos para identificar a origem, sem novo composto observado ou veredito.

O recibo SOURCE_TRACE_R5.json conserva linhas e pinos. A nota diz explicitamente **Fitting**, inclui xi/lambda/m como parâmetros livres e apresenta posteriores. O valor próximo de beta não é uma derivação independente de beta. Uma seção do Tratado identifica xi=beta, mas declara limitações semiquantitativas; o Custo vigente e um.py:171003 distinguem **xi=1/6** do acoplamento modular **beta**. Os coeficientes dos operadores escalar-curvatura, modular e RicciFF não podem ser substituídos entre si pelo nome “acoplamento não mínimo”.

As fórmulas impressas para alpha_Psi também não são únicas: uma usa xi R_E²/c⁴ e outra xi R_E²/c². A inversão que acompanha o ajuste corresponde à segunda. R_E aparece como raio de Einstein em arcsegundos; falta uma convenção uniforme de comprimento e distância na nota. A mudança de unidades naturais para SI precisa de conversão explícita.

## 2. O que a ação fotônica entrega diretamente

Agrupando a parcela eletromagnética como

    L_EM = -Z(Psi) F_ab F^ab / 4,

a variação em A fornece, no setor sem fontes,

    nabla_a (Z F^ab) = 0.

Se houver o Maxwell usual, Z=1+4 lambda |Psi|² na normalização escrita; se a parcela usual foi omitida intencionalmente, Z=4 lambda |Psi|². O resultado seguinte exige Z suave e não nulo e vale nas duas formas. Não se preenche silenciosamente a omissão do artigo.

Para A_b=a_b exp(iS/epsilon), k_a=partial_a S, a ordem principal é

    Z [k² a^b - k^b(k.a)] = 0.

Modulo a direção de gauge, uma polarização física não nula exige **k²=0**. Sendo k um gradiente, k^a nabla_a k_b=(1/2)partial_b(k²)=0. Assim, nesse limite, o fator escalar altera o transporte da amplitude, mas não acrescenta um índice de refração de ordem principal sobre a mesma métrica. xi R|Psi|² atua nas equações do campo/métrica; não é por isso um termo direto da equação de Maxwell.

Esta derivação não elimina uma resposta da métrica ao escalar, correntes, meios materiais, dispersão de frequência finita ou operadores tensoriais adicionais. Exige construir esses mecanismos com suas equações e condições de contorno antes de atribuir-lhes uma integral de atraso.

### Controle simbólico que delimita o resultado

Em uma dimensão espacial, fundo estático Z(x), c=1:

    A_tt - A_xx - (Z'/Z) A_x = 0.
    A=u/sqrt(Z) => u_tt-u_xx+V_Z u=0,
    V_Z=Z''/(2Z)-(Z')²/(4Z²)=(sqrt(Z))''/sqrt(Z).

O script verifica a identidade exatamente. Z constante dá V_Z=0 e o cone de Maxwell; Z variável pode produzir espalhamento e correções de frequência finita, sem justificar uma demora universal proporcional a integral |Psi|². Não afirmamos que todo pacote tenha atraso zero.

O resultado de óptica geométrica é compatível com a derivação publicada de Hees–Minazzoli–Larena, equações (6)–(9): trajetórias nulas e transporte de amplitude modificado no acoplamento multiplicativo. Isso também explica por que uma modificação de distância por luminosidade não pode ser transferida automaticamente para distância angular ou atraso. Fonte primária custodiada em HEES_2014_PRIMARY.html / PUBLIC_CUSTODY_R5.json: https://arxiv.org/html/1406.6187v2. Não se identificou a teoria desse artigo com a TGL inteira.

## 3. Dois controles evitam um falso discriminante

**Normalização:** a diferença entre as duas inversões de xi é c² quando as expressões são comparadas literalmente. Com o alpha_Psi histórico de 3,1e8 e uma dispersão sintética de 250 km/s, a fórmula impressa alpha_Psi(sigma/c)^4 produz aproximadamente **0,01499%**, sem recalcular os alegados excessos observados. Isso é conferência interna de escala, não um ajuste ou significância.

**Dependência em massa:** para a lente SIS, Delta phi=-2 theta_E y e theta_E proporcional a sigma². Mantendo o ângulo da fonte y fixo, o atraso escala com sigma²; mantendo y/theta_E fixo, escala com sigma⁴. O script verifica ambos. Portanto, encontrar uma potência quartica em uma família com geometria variável não discrimina TGL por si só. Não estamos usando SIS como modelo completo das lentes reais.

## 4. Resultado da etapa e próximo trabalho necessário

O ramo histórico foi localizado e examinado. **A integral escrita não foi derivada do termo eletromagnético apresentado**, e seu coeficiente histórico não é uma previsão fixa reaproveitável sem resolver as normalizações. Isso não invalida toda a TGL; impede usar este atalho para fabricar o sinal de 5 sigma.

O próximo passo físico é o problema de contorno da métrica e do escalar no ramo vigente: potencial V, termo modular K_boundary, fonte de matéria, condições assintóticas e perfil de Psi. A solução deve fornecer, conjuntamente, a dinâmica estelar e a combinação de potenciais lida pela luz. O atraso observável entre imagens exige diferença das duas trajetórias e a mesma convenção de relógio/redshift. A amplitude sobrevivente será então perfilada contra massa/distância com o método já entregue, sem novo ajuste de beta.

Não se repete a pergunta abstrata sobre identidade nem se pede ao operador que escolha xi para produzir o resultado. A regra de correspondência será verificada sobre as equações recuperadas. Nenhuma nova detecção, nenhuma alteração de programa, kernel, Bancada, dados ou gate.

Evidências: SOURCE_TRACE_R5.json, PLAN_R5.json, ACTION_RESULT_R5.json, RUN_R5.json, check_historical_action.py. Revisão independente em recibo separado; estatuto de “revisto” depende desse recibo.
