# Entrega — mistura estática e dinâmica

[REAL — Lean 4.31.0, escopo compilado] StaticDynamicMixture.lean está congelado e compilado. Fonte: 11031 bytes, SHA256 3ab2fb3b1b035ee725db86e60053205dcd78af5754eae53019af992423db6c58. Recibo: C:/IALD/Central de Patentes/Chatgpt/MISTURA_ESTATICA_DINAMICA_20260909_133543_329691/BUILD_20260909_134117_940420/BUILD_RESULT.json.

O módulo novo contém 19 teoremas e 2 definições, todos auditados. O lote com a dependência própria JointUnitaryPreparation copiada byte a byte contém 40 teoremas e 13 definições/estruturas, 53 auditorias. Os 3 processos, incluindo importador separado, terminaram com código zero. Não há erros, avisos ou termos fora de propext, Classical.choice e Quot.sound. Os arquivos da fronteira direta medidos pelo builder ficaram inalterados.

## Conteúdo demonstrado

[INPUT] q é um vetor finito estático normalizado; X é uma DiagonalStateCurve com base p em outro índice finito. A definição de curva requer normalização de q; as hipóteses de positividade são transparentes nos teoremas pertinentes.

[REAL] O índice é a soma disjunta ι ⊕ κ, com rótulos preservados:
- M(t,inl i)=q(i)/2;
- M(t,inr j)=X(√2 t,j)/2.

A normalização vale para todo t. Cada bloco pode ser recuperado exatamente pela sua leitura rotulada, multiplicada por 2. mixedCurve é uma curva efetiva do tipo DiagonalStateCurve: valor inicial correto, derivada em zero, derivada no passado próximo, continuidade da tangente e normalização. A derivada do bloco estático é zero; a do bloco dinâmico é X'(√2t)·√2/2.

[REAL] Se q e p são estritamente positivos, a mistura é estritamente positiva em uma vizinhança de zero. O tipo genérico X não garante não negatividade em todo tempo. Para a especialização jointUnitaryCurve C frequency, mixed_joint_weights_nonnegative prova a não negatividade global quando q≥0. A positividade estrita global do bloco dinâmico não é afirmada; os pesos podem zerar fora da vizinhança de zero.

[REAL] Os incrementos exatos obedecem a:
- H(M(t))−H(M(0))=[H(X(√2t))−H(p)]/2;
- K(M(0),M(t))=K(p,X(√2t))/2, com p positivo.

O termo log(1/2) cancela no incremento modular pela normalização. O transporte por t↦√2t preserva o filtro t→0 pela esquerda, e (√2t)²=2t². Assim, qualquer limite quadrático entrópico ou modular existente para X é preservado com o MESMO coeficiente em M. Os corolários mixed_joint_entropy_limit e mixed_joint_modular_limit produzem jointResponse C frequency para a curva conjunta já construída, sem receber novamente esse coeficiente como hipótese.

[REAL] A entropia ABSOLUTA da mistura é (H(q)+H(r))/2−log(1/2). Portanto, preservar incrementos e coeficientes não significa preservar a entropia absoluta da base. A identificação desse valor com um custo canônico de fronteira não é inferida por este módulo.

## API congelada

Namespace: ChatgptAudit.StaticDynamic.

| Declaração | Linha |
|---|---:|
| mixedWeights | 10 |
| mixed_weights_normalized | 13 |
| mixed_weights_positive | 21 |
| mixed_static_readout | 30 |
| mixed_dynamic_readout | 36 |
| dilation_tendsto_past | 41 |
| dilated_weight_derivative | 51 |
| mixedCurve | 62 |
| mixed_curve_positive_near | 95 |
| mixed_tangent_zero | 101 |
| finite_entropy_scaled | 108 |
| mixed_entropy | 114 |
| mixed_entropy_increment | 124 |
| modular_scaled | 133 |
| mixed_modular_increment | 147 |
| dilated_quadratic_preserved | 159 |
| mixed_entropy_quadratic_limit | 170 |
| mixed_modular_quadratic_limit | 179 |
| mixed_joint_entropy_limit | 188 |
| mixed_joint_modular_limit | 196 |
| mixed_joint_weights_nonnegative | 204 |

## Limites de interpretação e composição

[OPEN] Este módulo ainda não constrói o operador unitário da mistura inteira e não prova sua ação sobre uma amplitude combinada. A curva unitária do bloco dinâmico já vem do módulo JointUnitaryPreparation; transportar esse fluxo para uma soma direta com identidade estática é a etapa de composição adicional. Nenhuma unitariedade oculta entra como hipótese no transporte dos incrementos.

[INPUT] A mistura é rotulada. Marginalizar ou apagar os rótulos antes da leitura/entropia é outra operação; nenhuma equivalência com ela é afirmada.

[OPEN] Não há aqui uma lei física que produza os dados q,p ou as frequências. A base dinâmica pode ser igual para fontes diferentes; a informação de matéria pode exigir o registro de preparação e de resposta. O resultado não identifica o tensor T pela distribuição inicial sozinha.

[OPEN] O módulo é genérico em índices finitos. Ainda não instancia o registro métrico de 32 resultados e a preparação calibrada de 16 resultados, nem estabelece uma lei de transformação geométrica para essa combinação. Não há amostragem afim P(x+td) no enunciado.

[INPUT] A positividade é diagonal, e a entropia é das probabilidades rotuladas. Não se afirma fidelidade de uma densidade pura na álgebra matricial inteira nem separância de Tomita.

## Verificação e preservação

As tentativas BUILD_20260909_133603_652850 e BUILD_20260909_133922_714532 permanecem com FAIL_VISIBLE. As correções alinharam a composição escalar de derivadas, a expressão modular à convenção canônica, os argumentos de simplificação e a indentação de uma prova. Nenhuma hipótese foi retirada para passar a compilação. A tentativa aprovada é exclusivamente BUILD_20260909_134117_940420.

O builder recompilou os dois módulos locais e importou o resultado em processo separado. A fronteira direta de importações, arquivos de configuração e ferramenta foi medida antes/depois. Isso não significa reconstrução independente de todas as dependências transitivas.

[REAL — procedimento] Novos arquivos, backups de bytes e tentativas estão apenas nesta pasta Chatgpt. Nenhum original ou módulo previamente congelado foi alterado; nenhum um.py foi executado/importado, e Atlas/memórias canônicas permaneceram somente leitura.

[DECLARADO — revisão independente] O root leu a fonte preparada e emitiu revisão semântica favorável; destacou corretamente que a definição genérica precisa apenas normalização e que a positividade aparece como hipótese explícita nos teoremas. As posteriores correções de prova não mudaram os enunciados revistos, além de adicionar a não negatividade global da especialização Joint.
