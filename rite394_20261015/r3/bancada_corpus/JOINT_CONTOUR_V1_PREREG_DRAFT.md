[INPUT — PROPOSTA NÃO RATIFICADA] JOINT_CONTOUR_V1, 05/09/2026. Rascunho congelável; nenhum gate canônico alterado.

## Hipóteses e domínio

A: um mesmo β₀=ALPHA_FINE_CODATA_2018×√e alimenta as leis especificadas em ORDEM005_DERIVACOES.md, com todas as normalizações e insumos externos declarados. Zero parâmetros ajustados a estes dados, condicionado aos insumos. B: as MESMAS leis, com uma constante comum b real livre; exatamente um parâmetro adicional. Não é comparação com ΛCDM completo.

Roster proposto: neutrino_m2, coma_distance, ga_mass, void_floor. Os quatro precisam ser quantitativamente elegíveis para o título de quatro domínios. O presente pacote usa resumos já conhecidos para desenhar e auditar o rito; NÃO é um teste retrospectivo cego. A vigência prospectiva começa somente depois de ratificação, hash e fixação do conjunto futuro de dados. Exclusão/substituição de domínio exige versão nova, antes da abertura dos novos resultados. Uma versão reduzida não conserva o rótulo de quatro domínios.

## Contrato de cada domínio

Cada entrada precisa informar fonte e hash, observável e unidade, lei de leitura x_i(β), escala dimensional fixa, incerteza estatística e sistemática, covariâncias e seus ancestrais, data de corte e independência da escolha em relação ao residual. x_i deve estimar β com modelo gaussiano validado ou aproximação com erro controlado. σ desconhecido é null, nunca zero. Dados globais e seus constituintes não podem entrar juntos sem a covariância correspondente.

Neutrino: escolher previamente um resultado independente (a candidata histórica é JUNO), explicitar m₁=0 e 1 eV fixo, sem somar NuFIT pós-JUNO como réplica independente. Coma: referência de distância apropriada e incertezas dos inputs, sem substituir a referência pelo controle FP. GA: mesma definição de massa/raio, admissibilidade da lei e erro conjunto M,R. Piso: exige estimador quantitativo de β ou verossimilhança física de limite; o protocolo gaussiano atual NÃO admite a desigualdade como uma medição pontual. Essa extensão exigirá nova versão.

Covariância C: simétrica e definida positiva, externa ao ajuste de b e com proveniência. Diagonal só mediante auditoria de independência. Não usar pseudoinversa silenciosa; matriz singular/duplicações/NaN/zero σ são INCONCLUSIVE. Se covariância for estimada em amostra finita, o modelo χ² exato deixa de valer; congelar antes uma calibração da distribuição nula que inclua essa estimação, em outra versão.

## Estatísticas e regras

Usar Q_A, Q_B, β_hat, informação s e ΔAIC=2−(Q_A−Q_B), conforme a derivação. Reportar A/B/empate apenas como preferência AIC; não convertê-la em veredito físico. Melhor AIC de A tem vantagem máxima 2 sobre B, nunca evidência decisiva por si só.

Falsificador primário: Q_A, com cauda χ²_n ≤ α_joint=erfc(5/√2). É bilateral nos desvios. Critério agregado único: não executar e escolher depois o menor entre vários testes. Efeitos abaixo do limiar permanecem explicitamente como resíduos, mesmo quando o veredito é NOT_FALSIFIED.

Poder: efeito relevante pré-proposto δ=β₀/2, nos vetores de alternativa ±δ em todos os domínios e ±δ em cada domínio individual. Exigir pelo menos 90% de poder para TODOS esses cenários para emitir NOT_FALSIFIED. O código usa limite inferior conservador: para λ=dᵀC⁻¹d, P(χ²_n(λ)>qcrit)≥P(|Z+√λ|>√qcrit), com Z normal padrão. É suficiente, não uma estimativa otimista do poder. δ é escolha de sensibilidade, não parâmetro ajustado; sua ratificação cabe ao operador. Não se promete excluir desvios arbitrariamente pequenos.

Ordem de decisão:

1. Rascunho não ratificado, domínio ausente/inelegível, esquema inválido, proveniência incerta, sistemáticas reprovadas ou covariância não validada → JOINT_CONTOUR_INCONCLUSIVE; sem veto solicitado.
2. Gates válidos e Q_A na região de rejeição → JOINT_CONTOUR_FALSIFIED; solicitar veto do teste conjunto. Poder baixo NÃO reverte uma rejeição estatisticamente válida.
3. Sem rejeição e poder mínimo <90% → JOINT_CONTOUR_INCONCLUSIVE; sem veto solicitado.
4. Sem rejeição, quatro domínios válidos e poder suficiente → JOINT_CONTOUR_NOT_FALSIFIED; sem veto solicitado, sem poder de reabrir outros vetos.

CONFIRMED e PROVED nunca são saídas. O teste conjunto não modifica o gate matemático. Na fiação expandida: veto_total = veto_individual_limpo_existente OU veto_conjunto_válido. INCONCLUSIVE não solicita novo veto, não limpa veto anterior e não conta como sucesso. O adaptador canônico e sua auditoria pertencem à gerência; não há patch aplicado nesta bancada.

## Congelamento e parada

Ratificar roster, efeito relevante, covariâncias, leis de leitura, fontes e datas antes do próximo resultado; calcular hash dos bytes do protocolo, do código, dos inputs permitidos e das transformações. Registrar separadamente autorização do operador e momento do congelamento. O hash do rascunho hoje não o torna ratificado nem restaura cegueira dos dados conhecidos.

Uma avaliação primária por versão, no corte de dados registrado. Sem monitoramento opcional até cruzar limiar. Repetições prospectivas exigem política de gasto de α em nova versão. Alteração de fonte, erro, seleção, transformação ou limiar produz versão nova; preservar todos os resultados anteriores. O executor deve recusar o hash divergente antes da estatística.

O hash interno da especificação usa JSON UTF-8 canônico (chaves ordenadas, sem espaços extras); os hashes dos arquivos entregues são hashes dos bytes, listados separadamente. A integração deve conferir ambos, inclusive o código e as transformações. Saídas data_kind=synthetic são controles, jamais alimentam o veto canônico; veto_requested nesses casos é apenas a resposta simulada. A verificação externa da autorização, dos hashes de arquivos e dos gates científicos não está substituída pelos campos booleanos do protótipo: o adaptador auditado deve produzi-los de verificações reais.

## Controles antes de dados futuros

Mundo A correto, mundo B deslocado, deslocamento negativo, resíduos opostos com média correta, perda de poder, domínio ausente, sistemática reprovada, correlação positiva, matriz singular, covariância assimétrica, NaN, hash adulterado e rascunho não autorizado. As contas racionais de Q e da projeção ponderada são verificadas independentemente da aritmética de caudas.

## Decisão exclusiva do operador

Ratificar ou não esta proposta, escolher os domínios e os dados prospectivos e autorizar a incorporação pela gerência. Com as lacunas atuais, a proposta de QUATRO domínios não está pronta para produzir NOT_FALSIFIED físico. Preservar o veto GA já ratificado não exige fingir uma incerteza ou uma verossimilhança inexistente.
