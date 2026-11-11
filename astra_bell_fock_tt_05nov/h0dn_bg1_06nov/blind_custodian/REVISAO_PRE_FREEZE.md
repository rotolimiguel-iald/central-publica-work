# Revisão do plano e do estimador antes das injeções

[DERIVED] A estatística unilateral proposta é apropriada à comparação de dois deslocamentos fixos com a mesma covariância gaussiana. O estimador de h por SVD do desenho branqueado perfila os nuisance originais. Acrescentar c_C ao desenho permite medir quanto a liberdade de viés diferencial Cefeida amplia a incerteza sobre h. O teste primário se refere ao nulo offset0. A atribuição à amplitude TGL exige também a consistência do resíduo com logK.

[REAL — inspeção do código] geometry calcula o suporte espectral de C, recusa espectro negativo significativo, recusa posto ambíguo, confere A e c_C no suporte e verifica a identidade da influência sobre todas as colunas ajustadas. O código usa SVD para evitar formar e inverter explicitamente a matriz normal mal condicionada. A definição de tolerância foi estabelecida antes de avaliar os centros. Falta confrontar o resultado com os ciclos de rede documentados e com os pinos efetivos dos artefatos.

[OPEN — reparo pré-freeze solicitado] evaluate precisa recusar NaN/Inf em entradas e parâmetros do estimador, verificar as dimensões exatas, os desvios padrão positivos e os resultados finitos. No texto inicialmente lido, um NaN faz a desigualdade da guarda de suporte resultar falsa e pode chegar à saída como NaN. Não houve execução nem injeção para esse achado.

[DERIVED] No gerador linear, as variâncias do teste nulo e da consistência TGL são distintas. A primeira usa grad(logH). A segunda usa grad(logH+logK), conservando o termo cruzado. Se K varia com os parâmetros BG, um centro logK fixado por outra fonte mais a derivada no BG representa uma linearização ancorada. O diagnóstico exato deve declarar sua regra de ancoragem.

[DERIVED] O nulo com δ_C arbitrário deixa a média da estatística baseline deslocada por w_hᵀc_C δ_C. Portanto a cauda normal padrão baseline está condicionada a δ_C=0. No segundo ajuste é preciso verificar w_hᵀc_C≈0. Um ensaio com δ_C=±0,05 quantifica esse mecanismo sem alterar a amplitude física TGL. Um termo adicional σ²c_Cc_Cᵀ pode ser usado como cenário declarado de covariância incluída no ajuste, ou como erro omitido para avaliar quebra de cobertura. Essa escolha deve constar no freeze.

[INPUT — protocolo de coordenação recebido] A configuração efetiva dos stress usa deslocamentos fixos ±0,05 mag e desvios adicionais 0,01/0,03/0,05/0,10 mag. A proposta preliminar mais ampla registrada em PROTOCOLO_CEGO.md fica restrita por essa especificação do coordenador. O plano pinado no freeze governará os ensaios. As duas especificações de nuisance analisarão as mesmas realizações, com pareamento explicitado.

[DERIVED] A cauda a 5σ será calculada analiticamente no modelo gaussiano linear e verificada por importance sampling. No vetor normal primitivo conjunto z, se g é a influência normalizada do teste, a mudança de medida z=q+5g com q∼N(0,I) dá peso exp(−5gᵀz+12,5). O peso usa a densidade primitiva inteira, e a geração mantém os modos ortogonais aleatórios. A validação por Monte Carlo ordinário mede poder e cobertura. Seus zeros na cauda rara serão apresentados como limites binomiais.

Nenhum bloco de injeção foi gerado nesta etapa. Esta revisão prepara a execução, e seu escopo será complementado após a leitura das matrizes e do freeze efetivo.
