# Continuidade da suficiência — entrega 073

10/09/2026. [DERIVED — demonstrações escritas] [KNOWN — entradas analíticas delimitadas] [REAL — artefatos lidos e medidos]. Somente arquivos novos na bancada Chatgpt; fontes originais e entregas anteriores preservadas.

**Avanço principal:** o contrato livre P0 da entrega072 foi realizado no modelo Einstein–sigma e no domínio interior de Cauchy já declarados. Construímos uma polarização Hadamard pura adaptada ao BRST, preservando o estado físico067, e a transportamos a uma Fock–Krein com domínio comum para os campos Wick. Nesse domínio, o kernel da carga livre é positivo e seus vetores de norma nula são exatamente a imagem da carga.

No setor de anomalias, foi demonstrada a exatidão cohomológica ordinária com jatos do fundo de referência B0, mantendo sua derivada horizontal. O retorno dessa primitiva à classe natural e admissível de Q2 continua aberto. Nenhum dos resultados é apresentado como construção da carga interagente renormalizada, QME ou fechamento UV.

## 1. Estado corrente e natureza da evidência

A [captura 073](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_073_20260910/ESTADO_CANONICO_073.json>) encontrou os mesmos bytes dos quatro artefatos canônicos da entrega072. O programa consultado continua v338, com 683 arquivos embutidos e 77 dos 98 módulos do comparador; 21 permanecem ausentes. O selo confere com um.py.

Não houve execução/importação de um.py, Lean, CAS, cálculos de diagramas ou testes de natureza nesta entrega. A evidência nova é matemática escrita, com revisão interna por leitores distintos dos autores nas frentes indicadas. Os controles de hashes e links são documentais. O objetivo geral permanece ativo; a entrega072 anterior foi progresso efetivo e esta entrega acrescenta novas construções, não apenas uma atualização de status.

## 2. Por que era necessário escolher melhor a extensão auxiliar

A [análise do radical](<C:/IALD/Central de Patentes/Chatgpt/RADICAL_GNS_BRST_073_20260910/RADICAL_DA_PSEUDOCOVARIANCIA_E_P0.md>) demonstra que uma pseudocovariância arbitrária que satisfaça os contratos068 pode falhar em P0. Depois de quocientar o radical ghost, um vetor de vínculos pode se tornar BRST-fechado e ainda ter norma negativa. Um bloco finito realiza esse caso, conservando CCR, Ward e o estado físico anterior.

Não foi identificado como negativo um kernel único medido de068. O resultado refuta uma promoção automática de toda a família, e apresenta duas condições exatas de saturação S1/S2 para recuperar a cohomologia física. O [reparo explícito](<C:/IALD/Central de Patentes/Chatgpt/RADICAL_GNS_BRST_073_20260910/REPARO_DO_BLOCO_E_LIMITE_HADAMARD.md>) remove o defeito no plano finito e fornece o formato global a realizar. A [revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_073_20260910/PARECER_RADICAL_E_REPARO_073.md>) conferiu a sequência exata, o bloco e os limites.

## 3. Polarização Hadamard adaptada, preservando a física067

A [construção de polarização](<C:/IALD/Central de Patentes/Chatgpt/POLARIZACAO_BRST_HADAMARD_073_20260910/POLARIZACAO_ADAPTADA_E_MAJORANTE.md>) começa com projetores puros Hadamard dos operadores D e Q. O defeito de entrelaçamento com os mapas de gauge e vínculos é suave. A inversa esquerda original e é adaptada por

\[
e_d=\sum_{\sigma=\pm}\Pi_Q^\sigma e\Pi_D^\sigma,
\qquad e_1=e_d+(1-e_dk)e,
\qquad e_1k=1.
\]

A correção é suave e a inversa continua exata. A construção simplética fornece q,r,p que preservam os ramos de frequência modulo operadores suaves. O extrator físico s0 possui inversa explícita R=s0†. O projetor final é

\[
\widehat\Pi_D^\pm
=k\Pi_Q^\pm q+r\Pi_Q^\pm c+R\Pi_{067}^\pm s_0.
\]

Ele é idempotente, complementar, compatível com a conjugação e exatamente adaptado ao complexo. A diferença para o projetor inicial é suave, o que prova Hadamard. O bloco físico permanece exatamente o de067; os setores auxiliares ganham a forma cruzada que satisfaz S1/S2. Os modos baixos são tratados pela construção, sem serem apagados.

A nota também constrói uma majorante Hilbert do espaço ghost por cálculo funcional elíptico, preservando os dados suaves. Não supõe positividade de toda a forma auxiliar nem aplica uma escolha de contorno a uma covariância Krein sem controle espectral. A [revisão independente interna](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_POLARIZACAO_BRST_073_20260910/PARECER_POLARIZACAO_E_RADICAL.md>) conferiu o encadeamento, incluindo a distinção entre adjunto sesquilinear e transposição bilinear.

## 4. P0 realizado num domínio comum com os campos Wick

A [prova Fock/Wick](<C:/IALD/Central de Patentes/Chatgpt/FOCK_HADAMARD_QUARTETOS_073_20260910/FOCK_DOMINIO_WICK_E_P0.md>) usa a mesma covariância construída. O domínio D contém um número finito de partículas, com funções de onda suaves conjuntamente em seus argumentos de Cauchy. Dentro de cada grau, o produto tensorial é nuclear completado; não se limita a somas finitas de tensores simples.

Os quartetos fornecem uma carga Q0 simétrica para a forma de Krein e uma homotopia h, com

\[
Q_0^2=0,\qquad Q_0h+hQ_0=N_{aux},\qquad
Q_0R_0+R_0Q_0=1-P,\quad R_0=N_{aux}^{-1}h.
\]

A inversa vale zero no vácuo auxiliar e 1/m no setor com m>0 partículas auxiliares. Todos os operadores preservam D. Para Q0 Psi=0,

\[
\Psi=P\Psi+Q_0R_0\Psi,
\qquad [\Psi,\Psi]=\|P\Psi\|_{phys}^2\ge0.
\]

Se a norma é zero, P Psi=0 e a própria fórmula exibe a primitiva R0 Psi em D. A igualdade é com a imagem efetiva da carga, não apenas com seu fecho. O quociente físico coincide com o domínio suave da Fock do estado067.

A estabilidade pelos polinômios Wick compactos microcausais é demonstrada por frentes de onda. As parcelas criadoras têm orientação comum; uma singularidade de saída exigiria uma configuração inteiramente futura ou passada que o kernel microcausal exclui. As contrações com funções de onda iniciais suaves preservam essa propriedade. Isso paga o domínio que faltava ao certificado algébrico de072.

A [revisão independente da composição](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_FOCK_DOMINIO_073_20260910/PARECER_FOCK_DOMINIO_E_P0.md>) não identificou erro material. O resultado é P0 no modelo/fundo/classe declarados. A representação dos coeficientes compactos polinomiais da teoria causal também fica disponível, como parte de P1. P1 integral inclui uma carga renormalizada simétrica; sua construção e as identidades de P2 continuam obrigações.

## 5. O espectador B0 ganhou uma primitiva ordinária

A [demonstração cohomológica](<C:/IALD/Central de Patentes/Chatgpt/COHOMOLOGIA_ESPECTADOR_B0_073_20260910/PRIMITIVA_ORDINARIA_COM_B0_E_LIMITE_ADMISSIVEL.md>) mantém s B0=0 e d_H B0 diferente de zero. Após desfazer o gauge e contrair os pares não mínimos, a translação finita de ghosts conjuga s+d_H a s+d_ext. O segundo termo deriva x e os jatos externos, em vez de congelá-los.

A diagonal de grau total cinco tem cinco canais. Os graus dinâmicos 1,2,5 nulos vêm das provas071; os outros dois são eliminados pelos grupos horizontais externos de graus1/2, nulos para os valores de métrica temporalmente orientada e alvo S3. Isso fornece a=sB+d_HC na classe coordenada, suave e de jatos finitos, quando a é um cociclo nessa álgebra universal.

A nota distingue jatos livres, o espaço estacionário universal das equações completas e uma igualdade avaliada apenas no FRW escolhido. A última não basta para consumir o teorema universal. Também demonstra que a homotopia coordenada não é automaticamente natural: a mudança não linear de coordenadas produz um termo com derivadas do Jacobiano. A [revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_073_20260910/PARECER_COHOMOLOGIA_ESPECTADOR_073.md>) preserva precisamente esses limites.

Portanto a presença dos jatos de B0 deixou de ser uma lacuna cohomológica ordinária sem tratamento. Permanecem a universalidade e a completação da quebra efetiva, sua primitiva natural, a regularidade/escala requerida e a compatibilidade com todos os produtos, inserções e contatos de Q2.

## 6. Caminho crítico após073

1. **Renormalização admissível:** realizar a primitiva geral na classe efetiva de Q2, com B0 e a completação formal tratados, e removê-la coerentemente em todas as ordens. Exatidão ordinária não é uma normalização causal inteira.
2. **Carga interagente e QME:** construir a corrente, sua representação simétrica, a implementação do diferencial e sua nilpotência. P0 agora está realizado; a existência desses dados renormalizados ainda não foi inferida da representação dos coeficientes.
3. **Fundos e globalidade:** pagar acordo perturbativo, identidade de mudança da cisão e compatibilidade dos estados nas mudanças de cutoff/fundo. Não foi construída uma soma não perturbativa.
4. **Alcance físico e UV:** completar a reconstrução geral pelos mesmos dados selecionados, com os postulados de correspondência declarados, e resolver a rota UV escolhida. O resultado atual usa a ação ambiente e este fundo; não atribui automaticamente seus graus físicos à família mínima de probabilidades.
5. **Integração:** incorporar os 21 módulos anteriores ainda ausentes e formalizar as novas demonstrações. A fase e o ramo já integrados não são reabertos; H3 interno e falsificadores existentes continuam reconhecidos.

O adendo de revisões e a entrega no túnel acompanham este relatório. Nenhum Atlas, índice, memória canônica, original, selo ou gate foi alterado. O lastro construído nesta entrega tem o alcance das provas acima; o objetivo geral continua aberto.
