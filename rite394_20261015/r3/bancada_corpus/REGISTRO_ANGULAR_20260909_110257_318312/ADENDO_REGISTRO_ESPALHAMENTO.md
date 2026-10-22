# Adendo — registro canônico de cada ramo de espalhamento

[REAL — 09/09/2026, compilação nova] ScatteringOutcomeRecord fecha a compatibilidade entre o registro e a matriz densidade canônica rhoOut(θ) = Smat(θ)|0⟩⟨0|Smat(θ)ᴴ. A igualdade com o produto externo de Smat(θ)e1 foi provada; rhoOut é positiva e tem traço 1, habitando QubitDensity.

## Correção ao lado e convenções de peso

O relatório anterior deve ser lido com esta precisão: fairRecord 0 e fairRecord 1 têm mesma fase angular, peso e ângulo. Separadamente, seus pesos e readouts coincidem com os ramos justos da plusDensity. A fase desses registros não foi extraída da plusDensity e a reconstrução declarada nunca foi uma inversão da densidade inteira dessa entrada. A matriz rhoOut de espalhamento é agora o referente explícito da extensão.

Há dois leitores com contratos diferentes:

- readRecord: weight é o peso geométrico de REFLEXÃO da forma, independentemente do rótulo.
- readScatteringRecord: weight é a probabilidade do RAMO escolhido — 1−p no ramo 0 (transmissão) e p no ramo 1 (reflexão).

O teorema weight_conventions_differ_at_pure_transmission impede tratá-los como intercambiáveis: selectionRecord 0 0 é distinto de scatteringRecord 0 0. A interpretação do campo acompanha o leitor e sua imagem admissível.

## Suficiência tipada e reconstrução

Na família principal θ = arcsin√p, 0 ≤ p ≤ 1:

1. scatteringRecord p outcome armazena o peso correto, a fase angular e o rótulo.
2. canonical_branch_weight_is_selected_probability liga esse peso ao branchWeight de rhoOut, para AMBOS os ramos.
3. scattering_record_reconstructs_branch recupera o ramo não normalizado; normalização exige peso não nulo; peso zero produz ramo zero.
4. readScatteringRecord tem seu próprio round-trip, e encodeScatteringOccurrence é injetivo no domínio de formas angulares admissíveis com rótulo.
5. Peso escolhido + rótulo recuperam p: p = 1−weight se outcome=0, p=weight se outcome=1. selected_weight_and_label_reconstruct_principal_form recupera a Smat da preparação principal sem precisar obter uma fase arbitrária descartada após o evento. O decoder por peso e o decoder por fase concordam nessa família.

O ângulo principal e o rótulo são informação suficiente para a forma e o ramo dessa preparação. Isso não demonstra um decoder universal de estados quânticos arbitrários nem uma inversa da redução não seletiva. Não há amostragem de ocorrência, comprovação instrumental de um registro físico ou alteração de gate.

## Verificação

ScatteringOutcomeRecord tem 23 teoremas e 8 outras declarações. A rodada conjunta válida recompilou 54 teoremas e 21 outras declarações (75 relatórios), em quatro execuções com retorno zero e sem mensagens extras. Todos os axiomas estão no trio. Fontes/binários diretos importados permaneceram iguais por hash; dependências transitivas não foram integralmente reconstruídas/auditadas. Rodada válida: BUILD_20260909_112251_810885. Rodadas falhas anteriores e backups binários foram preservados.

Revisão lógica: root e crítico independente leram convenções de peso, bordas p=0/1, imagem admissível e proveniência rhoOut; a validação independente da compilação deve registrar sua própria evidência.
