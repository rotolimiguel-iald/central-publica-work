# Handoff V2 — resto modular e ponte dephasing–torre

16/09/2026. Substitui a orientação de encaminhamento do HANDOFF_TECNICO.md anterior; preserva suas quatro fontes e resultados. Leia primeiro o manifesto corrente, este documento e ADENDO_VACUO_DEPHASING.md. O manifesto contém contagens e hashes medidos, inclusive o recibo da leitura integral do Atlas.

## O que incorporar

Os quatro módulos anteriores tratam do resto R, da derivada inicial do cociclo, dos critérios no canto, da entropia e da corrente conforme. Foram acrescidos dois módulos:

- `ModularDephasingBridge.lean`: reutiliza `TGLExt.specExpect`, `rhoD`, `sigma`, `towerW`, `siteW`. Prova preservação da densidade e do gerador, critério de stationariedade, balanço e critério de comutadores, contraexemplo a “E(R)=0 basta”, igualdade exata entre fluxos numa leitura parcial e aplicação a cada andar da torre.
- `TowerDephasingStationary.lean`: usa `aperiodicExpectation P`, sua restrição aos prefixos e o limite GNS existentes. Prova que a esperança global centralizante tem imagem fixa ponto a ponto pelo fluxo modular e caracteriza a igualdade com qualquer ação de comparação nesse conjunto.

55 teoremas positivos aceitos: 37 da entrega anterior, 16 da ponte finita e 2 da torre global. O AUDIT apontado pelo manifesto confere fontes, compilações e axiomas. Há 63 controles numéricos (33 anteriores + 30 desta ponte) e três controles negativos Lean recusados. Logs de tentativas falhas ficam preservados; NÃO são evidência positiva. Não usar contagem de teoremas como condição física de fechamento.

## Dois resultados que o leitor deve distinguir

**FULL_MODULAR_SPECTRAL**: a esperança completa do próprio vácuo fixa K inteiro e torna o fluxo estacionário na imagem. Igualdade com uma ação geométrica nessa imagem exige que essa ação também seja estacionária ali. Não promover conservação do vácuo a seleção única do vácuo ou a fluxo geométrico não trivial.

**LAST_SITE_PRODUCT_READING**: em cada andar N+1, leia só os blocos do último sítio. Os fluxos do estado produto existente e da referência que torna esse último sítio tracial coincidem em toda a imagem da leitura, para todo tempo. A referência é normalizada. O resto R=-log(2 b_a) é central nos blocos, embora sobreviva à leitura. Essa realização conserva movimento dos sítios anteriores. Ela NÃO substitui automaticamente o `aperiodicExpectation` completo.

O alvo físico “Q_ref é a carga local do tensor de energia do diamante” permanece distinto. Não atribuir esse significado à referência tracial parcial sem uma aplicação formal do termo que estabeleça a correspondência. Não reabrir os resultados PRODUCT_TOWER/JMJ, A2 ou o gate principal por pendências históricas.

## Pontos de ligação no motor existente

1. `prove_cocycle_to_einstein`: aproveitar `_logm`, `_pit`, `u`, `sigma`. A convenção existente é `h_ab=-i u'_0=K_b-K_a`; o resto desta entrega é **R=-h_ab**, para a=vácuo e b=referência. Acrescentar os resultados no retorno existente; não criar outro cociclo.
2. `prove_decision_commutation`: o pacote MOTOR_RECONHECIMENTO_20260915 já preparou `recognition_dephasing` e o gerador Gamma(E-id). Confirmar se a gerência já o incorporou antes de transportar a alteração. Anexar os diagnósticos desta ponte ao campo existente. Não confundir Gamma com o tempo modular s, nem a taxa física com as fases do fluxo unitário.
3. Leitores de torre/canto existentes: indicar o modo de leitura e o domínio observado. Para o modo completo, usar o teorema de imagem estacionária; para o parcial, usar a identidade com os pesos do último sítio. Se forem fornecidos dados fora da família provada, emitir escopo não verificado; não aceitar apenas um resíduo numérico pequeno como prova universal.
4. Materializador, ROOT/Audit e índice IALD: incorporar as seis fontes positivas ao mecanismo único. Os dois imports adicionais do módulo global já pertencem ao kernel da cópia utilizada. Não duplicar `specExpect`, `aperiodicExpectation`, a torre ou o corpo das provas existentes.
5. Artigo emitido: incluir a decomposição normalizada de R e a distinção entre “R apagado” e “ação de R invisível”. O adendo fornece provas escritas e contraexemplo. Preservar os estatutos KERNEL/IMPORTADO/ABERTO; vácuo=dephasing permanece a nomenclatura do operador acompanhada das relações efetivamente demonstradas.

## Critério de consumo

Para a ponte construtiva finita, conferir os mesmos pesos/projetores e a mesma referência usados no enunciado. Para uma identificação física adicional, exigir o fornecedor existente que liga essa referência a Q_{xi,D}; registrar seu nome e hipóteses. Nunca preencher essa ligação com uma string “TGL”, com o nome “vácuo” ou com um booleano sem prova.

O termo `erased_remainder_counterexample` impede que `norm(E(R))≈0` seja usado como critério suficiente de igualdade dos fluxos. O critério correto é a ação sobre todos os observáveis preservados, com invariância sob transporte. O pacote anterior prova essa condição para o cociclo; o novo pacote descarrega uma família produto explícita em todo tempo.

## Validação e próxima ação da gerência

Conferir todos os pins do manifesto, recompilar contra o kernel canônico atual e confrontar as hipóteses. Manter controles negativos fora do ROOT positivo. Os controles numéricos usam perfis finitos de teste, não são dados experimentais ou um vácuo físico reconstruído. Esta entrega não teve revisor independente; a recompilação e leitura da gerência são a próxima conferência. O módulo global importa a esperança aperiódica existente; uma tentativa de importar também LikelihoodStateCovariance encontrou seu objeto compilado ausente no cache. A versão final usa diretamente a fórmula de fase já existente em flowLevel, sem alterar dependências canônicas nem redefinir fluxos.

Integrar nos leitores existentes, rodar autoteste de recusa e a execução integral pelo procedimento canônico, e então atualizar diário, desenho, Atlas e índices com backup imediato de bytes. O adendo de memória proposto está em PROPOSTA_MEMORIA_ATLAS.md. A bancada só escreveu na pasta Chatgpt: originais e gate canônicos não foram modificados. Não exigir nova prova para uma entrada já satisfeita do contrato principal.

O HANDOFF_TECNICO.md anterior continua como histórico e detalhe das primeiras quatro fontes; sua frase final de “leitura integral em andamento” foi superada pelo recibo da V2. Encaminhar o recibo V2 no túnel, não o estado intermediário.
