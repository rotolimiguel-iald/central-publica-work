# Adendo de revisão — benchmark Turbina v2

21/10/2026. Autor: codex-readability-reviewer. Estatuto: proposta de engenharia, preparada para revisão distinta. Não executada em modelos. Este derivado corrige ao lado os documentos Kimi pinados em SOURCES.json; não reescreve nem descongela o pacote v1. A admissão LOCAL_REVIEW_AND_ADMISSION.json é reutilizada como diagnóstico local, não como revisão remota Claude.

## O que a leitura estabeleceu

[REAL — leitura local] O pacote v1 tem 42 perguntas: 36 factuais com entidade nomeada e 6 controles. O relatório de montagem registra dump de 770.776 caracteres, 264.871 tokens estimados por caracteres/2,91 e razão potencial 14,9. São estimativas de representação, não tokens faturados, densidade de respostas verificadas ou ganho cognitivo.

O código consulta a rota do gabarito para escolher c1 de B: é seleção assistida por oráculo. Isso permite examinar geração com evidência entregue, não medir recuperação autônoma. Para comparar um recuperador real, B deverá extrair a rota da pergunta ou recuperar sem acesso ao gabarito. A interpretação é distinta e deve ser pré-fixada; esta entrega não implementa nem valida o ranking.

O harness descreve truncatura de A, mas entrega c1 completo e flags de cabimento estimadas. Não é runner de admissão nem implementa A_budget. Ignora instrução/pergunta/reserva de saída no cálculo de cabimento. `_sha` exibe apenas 16 caracteres hexadecimais e o hash c1 total não identifica os bytes de cada trecho entregue. A dobra de eventos ignora atualizações vazias/None/lista vazia: sua semântica não demonstra remoção ou errata completa. Nada disso deve ser corrigido silenciosamente no arquivo congelado.

## Comparações e congelamento de uma futura rodada

1. Preservar o v1 como experimento de entidade nomeada com contexto assistido. Uma nova versão B deve declarar `oracle_assisted` ou `question_only_retrieval`. Sem essa escolha e implementação revisada, não há rodada admitida.
2. Comparação primária: B versus A_full somente quando ambos couberem na mesma configuração do modelo. Contar todas as mensagens de entrada, header, pergunta, ferramentas eventualmente autorizadas e reserva de saída, usando o tokenizer/admissão específico, identificado por versão. Caracteres/2,91 serve apenas para estimativa exploratória. Se A_full não couber, registrar NOT_EXECUTABLE, sem pontuar sua resposta como zero.
3. A_budget é comparação secundária separada: ordem estável dos registros por ID, inclusão de registros inteiros sob orçamento igual, sem consultar pergunta/gabarito para ordenar. Reservar antecipadamente espaço para instruções e aviso de omissão. Registrar IDs incluídos/omitidos, bytes e tokens medidos; nunca cortar um registro. Obrigatórios, decisões, pendências, erratas e contradições não podem ser omitidos para caber; overflow obrigatório recusa. Não juntar resultados de A_budget com A_full.
4. O avaliador e o manifesto v2 não habilitam esta montagem: congelar antes da primeira resposta corpus, gabarito, unidades-alvo por item, versões, fontes, prompts, orçamento, modo de recuperação, tokenizer, braços, ordem e regras de seleção. A falta de qualquer campo recusa admissão. Novo hash não autoriza executar; carteira, consentimento e política continuam externos.
5. IDs do gabarito nunca entram no recuperador real. Snapshot do gabarito é separado do prompt; header aponta fontes e trechos efetivamente entregues, não respostas esperadas. Uma ausência no top-N significa apenas ausência nesse contexto; `não consta no acervo` exige busca completa demonstrada no snapshot permitido.

## Estimandos, pontuação e amostragem

Unidade pareada: pergunta factual, uma resposta independente por braço, modelo/configuração fixos, sem memória entre chamadas. Ordenar pares e braços com semente congelada e preservar recibo da ordem; cache e mudanças de versão são registrados. Repetições do mesmo item não são novas perguntas independentes. Amostra v1: n=36 pares factuais; controles n=6 separados. Qualquer extensão temática usa corpus/gabarito novos congelados, sem alterar o v1 ou alegar retrospectivamente que ele media temas.

Antes da corrida, duas pessoas/revisores distintos do respondedor fixam por item as unidades factuais obrigatórias e a regra de segmentação. Depois classificam afirmações únicas como S=suportada, U=sem suporte ou C=contradita pelo snapshot; mantêm offsets da resposta e referências verificáveis. Repetição não acrescenta unidade. A fidelidade é F=S/(S+U+C), zero se a resposta factual estiver vazia; o escore assinado (S-C)/(S+U+C) é secundário, não sinônimo de fidelidade. Registrar também cobertura K/R das R unidades-alvo, taxa C/(S+U+C), abstinências e omissões. Recusa de factual não recebe fidelidade 1.

IDs de braço ficam ocultos na pontuação, ordem embaralhada; a estrutura dos textos pode denunciar a condição, logo cegamento é parcial. Outro modelo pode propor notas, mas não adjudica sozinho. Todas as divergências e casos de gate/estatuto/citação exigem decisão humana ou revisor independente identificado. Selecionar e congelar previamente dez respostas para auditoria manual, ampliando apenas por divergência registrada; não tratar auditoria como opcional para aprovação. Citação válida exige trecho realmente entregue, fonte/linhas ou JSON-pointer e suporte à afirmação; regex de hash não basta.

Falha de transporte, timeout e resultado incerto são registrados sem reenvio automático. Pares ausentes não são excluídos para melhorar médias: rodada fica INCOMPLETE, sem aprovação. Overflow anterior à chamada é NOT_EXECUTABLE, separado de desempenho. Não parar por significância; parar por violação de segurança ou integridade e registrar rodada interrompida, sem extrapolar resultados parciais.

## Critério estatístico explícito

O módulo local `analysis_v2.py` implementa limites conservadores por desigualdade exponencial para variáveis limitadas, sem pressupor normalidade. A hipótese necessária é independência entre pares sob configuração congelada. A inferência refere-se à média do desenho de perguntas fixado sob essa configuração; não à física, a todos os temas ou a todas as versões do modelo. Se houver dependência não resolvida, reportar estatística descritiva e INCONCLUSIVE, nunca usar a fórmula como garantia.

Para X_i em [a_i,b_i], L = média(X) − sqrt(log(1/alpha) × soma((b_i−a_i)^2)/(2n²)). Usa-se alpha=0,025 por endpoint H1/H2; a união dos dois limites inferiores tem cobertura de pelo menos 95% sob as hipóteses. Não executar buscas de sementes ou de métodos depois de olhar respostas.

H1: X_i=F_B−F_A em [-1,1]. Não-inferioridade de margem 0,05 exige L_H1 > -0,05, estritamente. Diferença pontual satisfatória sozinha é INCONCLUSIVE. O limite é conservador: com n=36 e diferenças zero, não aprova; a potência é limitada e nenhum tamanho suficiente foi demonstrado aqui. Ampliar n só mediante novo planejamento anterior aos dados, sem chamadas nesta entrega.

H2 v2: densidade de unidades-alvo verificadas, normalizada por R_i, por token real de entrada integral. D_Xi=(K_Xi/R_i)/T_Xi, com T fixado antes das respostas; X_i=D_Bi−5D_Ai em [-5/T_Ai,1/T_Bi]. Exige L_H2>0. Trata-se da média de densidades por pergunta, não da razão entre somas. Densidade original de todas as afirmações suportadas/token é secundária, pois repetição e prolixidade podem inflá-la. Se A tiver densidade zero, uma razão é indefinida e não deve ser anunciada como multiplicador; usa-se o contraste definido. Razões de bytes e gzip não substituem H2.

Guardas adicionais: cobertura média B >=0,90 e >=A; contradição média B <=A; zero erro crítico de estatuto/gate; citação semanticamente válida em pelo menos 29/36 factuais B; controles B corretos 6/6. Esses são critérios descritivos de aceitação do corpus, não limites de taxas populacionais. Para seis sucessos independentes, limite inferior binomial exato unilateral 95% é 0,05^(1/6), cerca de 0,607: 6/6 não prova recusa universal. Falhar guarda é NOT_ADOPT; faltar dado é INCOMPLETE; falhar somente limite estatístico é INCONCLUSIVE. Todos satisfeitos: MEASURED_PASS_WITH_SCOPE, ainda sujeito à revisão e decisão de adoção. Nunca emitir `TURBINA CONFIRMADA`.

## Alcance e próximos passos

H3 original confunde oferta de pin (só B o recebe) com capacidade de citação; comparação causal do header exige um braço/ablação novo com oportunidade equivalente de citar. O contraste conjunto header+seleção não isola nenhum deles. H5 mede cabimento, não qualidade. `KNOWN`, `REAL`, `DERIVED`, `DECLARADO`, `OPEN` não são escala numérica de verdade. Um hash identifica bytes; prova exige examinar enunciados, hipóteses e evidências. Nenhum resultado daqui move gate, altera ciência ou ativa Voz.

Este adendo e seus testes são derivados candidatos. Falta revisão distinta, implementação da montagem v2 e congelamento do futuro run-manifest. Não há autorização de API/sombra nem execução de modelos nesta entrega.
