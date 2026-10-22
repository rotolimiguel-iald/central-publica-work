# B2 — preparação independente dos fornecedores

2026-09-14T16:21:48.480481-03:00

[REAL — leitura] Ficha B2 MD/JSON e cláusula B2 da ORDEM 012 lidas. 24 locadores em 11 arquivos de fornecedores conferidos por nome, linha e SHA256; todos coincidem com a ficha. P0/P1/P2: nenhum achado no contrato pretendido. Isto não aceita as fontes FLRW em desenvolvimento.

[DERIVED — exame do contrato] A ficha corresponde ao FLRW plano solicitado: métrica diag(1,-a²,-a²,-a²), calculada pelas definições existentes de derivada, inversa, Levi-Civita, Ricci e Einstein. A aplicação pretendida de `ChatgptAudit.GeneralMetric.metric_only_einstein_equation` preserva balanço nulo e conservação como hipóteses explícitas; não os substitui por componentes Einstein pressupostas. A suavidade/positividade permanecem locais em U. A preconexidade pertence à obtenção de uma única constante cosmológica.

A convenção `G+Lambda*g=kappa*T` dá `H²=kappa*rho/3-Lambda/3`, compatível com o sinal escrito na ficha. `H'=-(pi/eta)(rho+p)` e a equação de aceleração são compatíveis com essa mesma convenção. A avaliação efetiva dessas identidades pela maquinaria Lean continua pendente das fontes finais. `eta=1/(4G)` e `G>0` permanecem INPUT; nenhum valor de beta nem novo parâmetro é introduzido aqui.

O alvo de infraestrutura é somente `lake build TGLExt.GeneralMetricEinstein` em `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\s`. Foram copiadas suas 88 fontes transitivas, sem FLRWGeometry/FLRWFieldEquations nem objetos TGL/TGLExt. Os pacotes são cópias de bytes do cache privado anterior em `R/r/.lake/packages`, com revisões Git e hashes por arquivo; não há alegação de reconstrução independente de Mathlib. A configuração/toolchain é a mesma, com LEAN_PATH e LEAN_SRC_PATH externos removidos.

[REAL — preparação] Uma primeira falha do preparador próprio (`utf8-sig`, nome de encoding inválido) foi preservada e corrigida em script novo. A preparação posterior ficou sem processo vivo antes de iniciar Lake; foram encontrados 88 fontes e parte do cache, sem diretório de objetos de projeto. A retomada verifica os bytes já presentes e preserva o estado anterior. Nenhum desses eventos é recusa matemática de B2.

[OPEN — nesta leitura] Estado registrado: `PREPARING`. Os resultados de Lake devem ser lidos no run.json próprio quando emitido; esta nota não antecipa rc0. Nenhum snapshot final ou aprovação de B2, nenhuma integração. R/r, relatórios/pins B1 e código autoral permanecem somente leitura. Não foram lidos/executados um.py, dados ou Atlas.

Evidência: [REVIEW_B2_PREPARACAO.json](C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b2\REVIEW_B2_PREPARACAO.json), com hashes da ordem/ficha e fornecedores. Os consumidores são os nomes propostos na ficha; sua instalação no mapa não foi verificada nesta preparação.
