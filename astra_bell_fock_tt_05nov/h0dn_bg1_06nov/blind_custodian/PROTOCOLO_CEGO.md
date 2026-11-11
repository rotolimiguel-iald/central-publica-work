# Custódia das injeções H0DN × BG1

Estado em 06/11/2026 — PREPARADO_AGUARDA_FREEZE. Os artefatos desta pasta são derivados prospectivos. A geração começa depois de o coordenador congelar o código do estimador, as matrizes, a seleção, os modelos de média, o suporte e os limites estatísticos.

O estimando primário é t = ĥ_local − b̂, com h = log10(H0), b = log10(H0_BG1) e ĥ obtido por GLS com perfil das colunas nuisance originais. O modelo de média da rede é A x + c_C δ_C. O modelo nulo põe h−b=0; a alternativa fixa põe h−b=log10 K, com β calculado em runtime a partir de α. A análise paralela admite δ_C livre no ajuste. A regra é relatar as duas especificações e todos os cenários congelados, sem escolher pelo maior sinal. A hipótese de desvio universal atua pela coluna de h de A.

## Estatística e significância

Sob a aproximação gaussiana conjunta da rede e de b̂, a estatística Z=t/√(v_h+v_b) tem distribuição normal padrão no nulo, depois de projetar os nuisance. O corte unilateral Z≥5 tem probabilidade Φ(−5). Para a alternativa de shift fixo e a mesma covariância, o log da razão de verossimilhanças é função afim de t. A escolha desse contraste é compatível com o teste de Neyman–Pearson nesse modelo. A independência entre rede e BG1 deve ser justificada pela composição dos dados admitidos.

A separação esperada s=log10K/√(v_h+v_b) determina poder 1−Φ(5−s). A separação s=5 corresponde a poder de 50%; poder de 95% exige s aproximadamente 6,645. O poder e o tamanho serão apresentados separadamente. A consistência com a amplitude TGL usa t−log10K e a propagação própria de BG1, conservando as covariâncias de b̂ com logK. Ela é uma segunda pergunta estatística, com critério explícito.

BG1 define se a injeção é gaussiana em H0 ou em log10H0. Se o arquivo entrega média e covariância de parâmetros que incluem H0, a passagem exata por log10 requer nova calibração. O desenho primário linearizado usa Jacobiano pinado, e o cenário de transformação exata mede o erro dessa aproximação, incluindo a possibilidade de parâmetros amostrados fora do domínio físico. Recusas serão contadas. Cada avaliação precisa indicar qual desses geradores foi usado.

## Suporte e covariância

A decomposição C=U₊Λ₊U₊ᵀ gera ruído U₊√Λ₊z, conservando as relações determinísticas do núcleo. Congelar a convenção numérica de posto com as unidades da matriz. Conferir PSD, simetria, finitude, tamanho, espectro e núcleo conhecido antes da geração. Verificar NᵀA e Nᵀc_C. As médias injetadas devem obedecer às mesmas equações de suporte, e todo ajuste deve impor Nᵀ(y−μ)=0. A pseudoinversa serve à distância no suporte. Divergência do suporte provoca recusa explícita.

A documentação de ORDEM_018 registra 72 ciclos estelares e uma família PSD interior que preserva o núcleo e as variâncias marginais. Ela trata de frações de erros MAS/HMS existentes. A análise deve preservar identificação de âncoras, HMS, MAS e calibradores compartilhados. Uma correlação de sensibilidade possui estatuto de hipótese instrumental. A demonstração de PSD autoriza simulação matemática daquela hipótese e deve acompanhar a interpretação.

## Geração e cegamento

1. Receber o manifesto de freeze, verificar todos os SHA-256 e criar um compromisso de custódia antes de gerar a primeira realização.
2. Gerar segredo/seed novo exclusivamente na custódia, conservá-lo em arquivo próprio e divulgar apenas seu SHA-256. Gerar rótulos aleatórios para os blocos e ocultar sua correspondência com hipóteses e cenários.
3. Gerar 100.000 ensaios ordinários por hipótese para a configuração congelada. Os dois estimadores perfilados podem analisar os mesmos ensaios, e a dependência desse pareamento ficará explícita. Ensaios serão gravados em blocos para conter a memória.
4. Os cenários de deslocamento Cefeida, se admitidos no freeze, são δ_C=0 e ±0,01, ±0,03, ±0,05, ±0,10 mag. Uma família de covariâncias só entra quando sua lista completa, sinais e regra de resumo estiverem pinados. Cenários de sensibilidade nunca se tornam medições de correlação.
5. Para a cauda nula, gerar 100.000 importance samples por caso admitido, deslocando em +5 a coordenada normal padronizada da estatística. O peso de cada realização é exp(−5z+25/2) na convenção em que z é a coordenada deslocada observada. Usar log-pesos para estabilidade, erro Monte Carlo e tamanho efetivo. O produto indicador×peso estima a probabilidade nula.
6. O coordenador recebe blocos com identificadores cegos e executa o estimador congelado. Antes do unblinding, pina os escores, os avisos de suporte, os ajustes e os intervalos. A custódia confere esses pinos e abre uma vez o mapa de rótulos, conservando os artefatos de ambas as etapas.

O cegamento é uma separação procedimental entre agentes e arquivos do mesmo workspace. O operador e processos com acesso ao workspace podem ler o material de custódia. A geração ocorrerá após o freeze, e o confronto de hashes documentará a ordem dos atos.

## Resultados exigidos

Por cenário, relatar poder de rejeitar offset0, cobertura dos intervalos da escala e de δ_C quando ajustado, viés, dispersão empírica e prevista, contagem de falhas e suporte, curva analítica quando aplicável e cauda nula com importance sampling. A cobertura de 95% usará intervalo Monte Carlo binomial; a taxa de rejeição a 5σ será comparada à cauda analítica no modelo gaussiano validado. Zero excedências em Monte Carlo ordinário fornece um limite binomial, cuja ordem é 3/N para confiança unilateral de 95%.

Nenhum ajuste de hiperparâmetros, tolerância, sinal, conjunto de cenários, direção de cauda, código ou seleção ocorrerá depois de acessar os escores para beneficiar uma hipótese. Reparos necessários serão registrados como nova versão com motivo e fonte, preservando toda a rodada anterior. O relatório trará separação esperada, poder, significância e dependência dos nuisance em termos próprios.
