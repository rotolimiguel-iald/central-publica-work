# Construções por termo — primeira entrega aplicada da F1.CITACOES_20261025

[REAL — sandbox verificado; integração na versão selada pendente]

O avanço desta etapa é aplicar as construções já existentes à declaração final e à escala dual do mesmo núcleo de Fock. A v401 consultada permanece intacta. O programa de eliminar as dependências bibliográficas ainda não está concluído: esta entrega paga alvos concretos e registra separadamente o que continua aberto.

## O que foi efetivamente construído

1. **Declaração aplicada.** `applied_qg_solution_end_to_end` recebe a rede Maxwell compacta, `physicalFockCertificate` e `physicalMaxwellCertificate N` já construídos no túnel. Os três certificados deixam de ser parâmetros livres desta assinatura. O resultado conserva N, G>0, admissibilidade e a condição terminal de equilíbrio. `appliedFullWitness` fornece o representante do tipo existente; o nome não prova canonicidade, unicidade ou classificação III₁.
2. **Escala dual no núcleo da rede.** `FiniteTraceProjection` seleciona projeções autoadjuntas de traço finito positivo do próprio core Fock. O corte PF habita esse tipo, tem τ(PF)=1 e é transportado pela ação dual. `physicalDualScaling` satisfaz τ(θ_s A)=exp(−s)τ(A); `actual_core_agape` aplica as seis cláusulas da Fundação a esse corte concreto. O uso da versão v351 na fundação é reaproveitamento de uma dependência incorporada, não retorno do programa inteiro à v351.
3. **Ponte longitudinal aplicada.** O lift da ORDEM 025 passa a consumir esse traço concreto. A covariância de p+ e a invariância de p+p− são termos. O mesmo corte admite μ²=1 e μ²=4: a lei de escala não seleciona a massa. Em unidades c=1, a fórmula dá respectivamente (E,p)=(1,0) e (5/2,−3/2) [DERIVED algébrico], ambas com p+=1; esses números não são massas medidas.
4. **Obstrução interna.** `actual_dual_not_inner` prova que θ_s, com s≠0, não pode ser conjugação por um invertível do mesmo core. A conjugação preservaria o traço do corte; a escala dual o altera. Isso exclui essa identificação direta, não uma ação externa ou uma ponte covariante com o fluxo modular de BW. A realização longitudinal construída não identifica automaticamente peso com energia física.
5. **Unicidade da raiz usada.** `RootUniquenessR5` mostra que o grafo completo determina a resolvente, e que raízes da classe construída por resolventes — ou por pares positivos normalizados A²+B²=1 — são únicas quando seus quadrados completos coincidem. A igualdade inclui os domínios. Aplica-se a T_c e à raiz do S†S no GNS efetivo. Há habitante para todo parâmetro c e um controle finito com imagem não nula. Não se invoca Kato irrestrito nesses consumidores.

## Reaproveitamento e verificação

Os fornecedores de Fock/Maxwell não foram refeitos: 564 objetos de seu cache e os recibos anteriores foram conferidos. A representação global de helicidade, a covariância de Lorentz, BW/KMS/Tomita e o traço/PF já estavam construídos no sandbox posterior. Ler somente o livro antigo da v391/v374 teria recriado pendências já atendidas.

Duas fontes novas finais compilaram em Lean 4.31.0: 13 teoremas da raiz e 16 declarações da aplicação (11 teoremas, 4 definições e 1 abreviação), total 29. Todos os relatórios finais usam somente propext, Classical.choice e Quot.sound, sem sorry. Tempos: raiz 80,4029 s; intervalo início/fim da compilação aplicada 61,6480 s. O campo seconds=62,5669 do recibo aplicado inclui verificações posteriores; essa diferença LOW foi apontada pela revisão e fica corrigida aqui. Fontes, logs, LEAN_PATH literal, início/fim, códigos de saída e hashes estão nos recibos. Tentativas que falharam foram preservadas e não contam como prova.

O censo lexical inclui 1.427 fontes Lean presentes, inclusive ignorados/ocultos, excluindo .lake/.git: 1.299 linhas candidatas em 503 arquivos. O inventário semântico priorizado cobre 15 temas e 29 fontes. O censo não certifica que toda referência seja lacuna; importação de teorema Lean já compilado é reaproveitamento de prova, não dispensa de prova. As fontes científicas e a implementação precisam ser avaliadas pelo enunciado, não só pelo rótulo histórico [KNOWN].

## Limites que ficam no enunciado

- O H3 aplicado é a resposta geométrica linearizada em direção nula fixa. O fator 8πG entra no construtor dessa resposta; β não entra na implicação Clausius examinada. Não foi exibida nesta entrega uma janela com θ terminal zero e δA≠0. A testemunha Maxwell de energia modular não nula não substitui essa janela.
- A conclusão original `qg_solution_end_to_end` ainda contém, por conjunção, o canto da torre v354. O novo corte pertence ao core Fock. Não foi afirmada igualdade entre os dois, nem entre PF e o projetor de vácuo em espaços diferentes.
- O traço ENNReal total é a extensão cíclica já construída, com acordo comprovado no cone positivo. Não se reivindica funcional complexo linear sobre toda a álgebra nem classificação III₁ automática.
- A unicidade de Kato entre todas as raízes positivas auto-adjuntas ilimitadas continua aberta por termo. Falta construir a representação normalizada para uma raiz arbitrária, sem tomá-la como hipótese.
- Nenhum dado observado, ajuste a dados, novo sigma, confirmação física ou mudança de gate foi produzido.

## Programa de avanço, com critérios concretos

| Alvo seguinte | Construção exigida | O que passa a permitir |
|---|---|---|
| Raiz positiva geral | De uma raiz positiva auto-adjunta arbitrária, obter A,B positivos limitados, A injetivo, A²+B²=1 e igualdade do grafo, com domínio exato | Aplicar a unicidade já provada e remover a citação geral de Kato nesse tipo |
| Janela Clausius não trivial | Estado regular do mesmo Maxwell, intervalo c<d, θ(d)=0 e δA≠0, sem redefinir o estado para igualar a conclusão | Testar que o consumidor aplicado não se reduz ao vácuo/janela degenerada |
| Fonte e métrica acopladas | Derivar a fonte da ação completa com seus termos não minimais, construir/identificar a métrica que a satisfaz e transportar H3 para todo ponto/direção | Consumir a implicação Einstein no atlas suave já demonstrada |
| Classificação e canonicidade | Critério formal de III₁ e prova para a álgebra da rede concreta; critério de equivalência/unicidade do representante | Separar um habitante efetivo do representante físico canônico |
| Correspondência vácuo/core | Mapa tipado entre o projetor no Fock e o corte no core, com propriedades de domínio, localização e transformação | Religar os objetos sem igualdade mal tipada nem homônimo |
| Calibração e massa | Estado/preparação e observável independentes que fixem a normalização p+/τ, o relógio N e o invariante μ² | Levar a representação matemática a uma previsão física sem ajuste ao dado |

A ordem útil é consumir os termos concretos agora e trabalhar os resíduos pelo seu tipo. Recompilar um caso mais restrito não permite apagar a hipótese do teorema geral. A nova obstrução de ação interna orienta a ponte: procurar o entrelaçamento correto entre representações, e não igualar dois grupos porque compartilham um fator exponencial.

Esta é uma entrega parcial do programa amplo. Os próximos alvos permanecem no estado da missão; nenhuma instalação, ratificação da gerência ou encerramento de toda a pesquisa é presumido.

## Revisão desta entrega

A aplicação recebeu PASS_WITH_SCOPE de /root/applied_review, com sonda independente de cinco teoremas: EXIT 0, 59,6129 s, somente o trio. A raiz, construída por /root/unbounded_root, foi lida integralmente e revisada por /root, com conferência de fontes, tipos, pinos e relatório do compilador; essa segunda revisão não repetiu a compilação. A aprovação técnica tem esse alcance, não é AUDITADA/FECHADA da gerência. A R1 do relatório permanece preservada; esta R2 esclarece a duração e incorpora as revisões.
