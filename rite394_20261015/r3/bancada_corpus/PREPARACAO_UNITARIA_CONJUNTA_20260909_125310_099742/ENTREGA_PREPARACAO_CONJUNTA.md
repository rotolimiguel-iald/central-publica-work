# Entrega — preparação unitária conjunta finita

[REAL] JointUnitaryPreparation.lean está congelado: 21 teoremas, 11 definições/estrutura e 32 declarações auditadas. Módulo e importador compilaram com saída 0, sem avisos; somente propext, Classical.choice e Quot.sound. A fronteira direta de dependências permaneceu inalterada.

Fonte: C:/IALD/Central de Patentes/Chatgpt/PREPARACAO_UNITARIA_CONJUNTA_20260909_125310_099742/JointUnitaryPreparation.lean
Bytes: 15923
SHA-256 medido: 8af3cebce6b400f2bf4f5dba3813d76eca9522d71f342e085f8f207aba20a5af
Recibo: C:/IALD/Central de Patentes/Chatgpt/PREPARACAO_UNITARIA_CONJUNTA_20260909_125310_099742/BUILD_20260909_125817_530685/BUILD_RESULT.json

A estrutura UnitaryLabelData ι contém pesos constantes positivos de soma 1 e os parâmetros normalizados canônicos de cada bloco. jointUnitaryCurve C frequency é uma DiagonalStateCurve REAL sobre ι×Fin2: pesos C.weight_j·pairWeights_j(t), normalização em todo tempo, não negatividade global, positividade estrita perto de zero e tangente inicial nula. Cada componente usa a curva unitária canônica.

jointCovectorCurve C w direction fixa frequency_j=covectorRead(w_j)direction. Para campos, usa-se w_j(x) no ponto x: esta é preparação direcional local, não amostragem do campo em x+t direction.

Os teoremas joint_entropy_increment e joint_modular_increment decompõem os incrementos da curva conjunta em Σλ_j vezes os incrementos canônicos. A entropia constante dos rótulos cancela exatamente. joint_modular_quadratic_limit e joint_entropy_quadratic_limit provam o mesmo coeficiente jointResponse C frequency = Σλ_j unitaryResponse_j. joint_relative_entropy_quadratic_zero prova o coeficiente quadrático zero de entropia relativa.

A unitariedade não ficou isolada dos pesos: jointBlockFlow é a matriz de fluxos canônicos por blocos; joint_block_flow_prepares_amplitude prova sua ação sobre jointInitialAmplitude; joint_block_amplitude_weights prova que os módulos quadrados das amplitudes produzidas são os pesos conjuntos. Matrix.blockDiagonal usa índices (ramo,rótulo), os pesos usam (rótulo,ramo); essa troca aparece no próprio enunciado. twoLabelData é um controle concreto normalizado; two_label_zero_tangent_positive_response prova tangente nula e resposta quadrática estritamente positiva na mesma preparação de dois rótulos.

[INPUT] Fidelidade aqui significa positividade da distribuição diagonal de referência. Não foi afirmada invertibilidade/fidelidade de uma densidade pura na álgebra matricial total, nem separância de Tomita. A entropia usada é finiteEntropy dos pesos diagonais; não a entropia de von Neumann da amplitude pura total.

[INPUT] Positividade dos pesos e unitariedade não fixam o sinal de unitaryResponse ou coherentCoupling. Setores de fonte assinada continuam compatíveis com probabilidades positivas; admissibilidade energética é uma restrição física própria, que precisa ser declarada. Os rótulos são finitos e os pesos λ são constantes durante a preparação. Não há acoplamento quântico entre blocos nesta construção.

[OPEN] A preparação conjunta está construída. Matching de calor com uma fonte total identificada, realização de área, conservação dessa fonte no alcance geral, geometria global, interações e UV não são demonstrados só por este módulo. A próxima composição pode usar jointResponse para relacionar o mesmo estado à soma finita de fontes; não precisa postular uma resposta total separada.

Preservação: tentativas anteriores permanecem. A primeira falhou por redução beta na igualdade inicial; a segunda teve apenas aviso redundante de simp. Correções precedidas de backup em bytes, escrita temporária verificada e substituição. A build final passou. Nenhum original, Atlas, um.py ou módulo entregue anteriormente foi alterado/importado/executado. As fontes/binários diretamente importados foram medidos antes/depois; as dependências transitivas não foram todas reconstruídas nem todas hasheadas.
