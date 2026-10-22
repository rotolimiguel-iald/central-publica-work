# Entrega — estado normalizado do registro angular

[REAL — compilado em escopo isolado] Fonte ProbabilityRecordState.lean congelada. O novo módulo contém 19 teoremas e 6 definições/abreviação. A cópia byte a byte do codec e este módulo somam 51 teoremas, 18 definições/estruturas/abreviação e 69 declarações auditadas. Ambos os módulos e ImportsRealization compilaram com saída 0, sem avisos; as auditorias usam apenas o trio padrão ou nenhum axioma.

Fonte: C:/IALD/Central de Patentes/Chatgpt/ESTADO_REGISTRO_PROB_20260909_121641_954475/ProbabilityRecordState.lean
Bytes medidos: 7645
SHA-256 medido: d86dc99caadcdbb9f4fbed0dba0a4641a2b67c9f7824394020da2d2cdffd9836
Recibo: C:/IALD/Central de Patentes/Chatgpt/ESTADO_REGISTRO_PROB_20260909_121641_954475/BUILD_20260909_121932_066301/BUILD_RESULT.json

## API estável para composição

Namespace: ChatgptAudit.ProbabilityRecordState.

StateIndex = (Fin 4 × Fin 4) × Fin 2.

recordState R x ((i,j),1) = R.probabilities x i j / 16.
recordState R x ((i,j),0) = (1 − R.probabilities x i j) / 16.

A convenção preserva reflexão no ramo 1 e transmissão no ramo 0. O índice da componente é parte do resultado rotulado. Cada par tem massa 1/16; os 16 pares totalizam 1.

- record_state_normalized R: para todo x, a soma dos 32 pesos é 1; não depende de x∈U.
- record_state_positive R: para x∈U, todos os pesos são estritamente positivos.
- record_state_smooth R: para cada índice, o peso é ContDiffOn ℝ ∞ em U.
- record_state_recovers_probability R x i j: p_ij = 16 Q((i,j),1), com igualdade exata.
- record_state_injective: igualdade global de recordState implica igualdade de registros, incluindo os certificados por irrelevância de provas.
- record_state_eqOn_iff: igualdade dos estados em U equivale à igualdade dos campos de probabilidades em U.
- decode_record_from_state: recuperar as probabilidades e aplicar decodeTensorField devolve decodeRecord R, sem campo geométrico adicional.

labelled_state_of_state_probabilities caracteriza a imagem pelo certificado de massa 1/16 em cada par. Uma distribuição normalizada arbitrária não é automaticamente um registro dessa imagem.

## Derivada e fator de Fisher

labelledTangent w aplica w_ij/16 ao ramo 1 e −w_ij/16 ao ramo 0. labelled_state_derivative prova que esta é a derivada efetiva de labelledState para qualquer curva p(t) cuja derivada componente a componente seja w; não identifica um parâmetro de curva com fluxo modular.

labelled_state_fisher_average prova, para 0<p_ij<1:

Fisher(Q, dQ) = (1/16) Σ_(i,j) w_ij² / [p_ij (1−p_ij)].

O resultado é a média das contribuições Bernoulli, não sua soma sem fator. O módulo não supõe que w seja uma derivada sem certificado: a identidade algébrica de Fisher recebe w, e o teorema de derivada explicita a hipótese necessária para sua interpretação como tangente real. Na composição com probabilityFieldCurve, as tangentes são produzidas do próprio campo de pesos.

## Estatuto e limites

[DERIVED] A ponte entrega uma distribuição diagonal finita normalizada e fiel em U a partir do mesmo registro que decodifica o tensor. A informação das 16 probabilidades permanece recuperável.

[INPUT] A escolha uniforme do rótulo da componente é parte do codec proposto. Não foi derivada de dinâmica, cociclo, frequência empírica ou processo de observação. Um resultado único entre 32 não fornece automaticamente o vetor inteiro de probabilidades reais.

[OPEN] Fora de U, a soma ainda é 1 por identidade algébrica, mas não se afirma positividade. O sentido de distribuição positiva é certificado em U.

[OPEN] A construção é em carta fixa. A transformação entre cartas precisa especificar como o registro rotulado muda quando mudam as componentes de g. Os pesos codificados de componentes métricas não são automaticamente escalares sob simples composição de coordenadas. A covariância da composição com Fisher exige uma lei de transformação ou um referencial físico explicitado.

[OPEN] Não se identifica Fisher positivo com assinatura lorentziana. A assinatura segue certificado do tensor decodificado no codec. Matching geométrico/microscópico, conservação, globalização e origem física permanecem contratos separados. O módulo não move o gate nem declara QG resolvida.

## Preservação e auditoria

O codec é uma cópia em bytes da fonte congelada. A dependência foi compilada apenas dentro desta pasta nova. A primeira build preservada falhou na prova auxiliar de imagem por causa da separação automatizada de Fin 2; os demais resultados centrais já passaram nela. A correção foi precedida de backup byte a byte, seguida de escrita temporária verificada e substituição. A build final passou, inclusive os novos lemas de derivada e Fisher.

O recibo mede antes/depois as fontes e binários diretamente importados do acervo canônico; essa fronteira não mudou. Não recompila todas as dependências transitivas nem calcula hashes de todas elas. Nenhum original, Atlas, módulo de entrega anterior ou um.py foi alterado ou executado.

[INPUT] Revisão independente deste módulo solicitada; não marcada como concluída neste recibo.
