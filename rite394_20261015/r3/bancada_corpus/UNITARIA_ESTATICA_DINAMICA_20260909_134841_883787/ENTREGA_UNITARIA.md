# Entrega — operador unitário da mistura

[REAL — escopo compilado] StaticDynamicUnitary.lean está congelado, com 7651 bytes e SHA256 f576746af188d260315be5d207e09bafb214e8a2d96d122a637cd5cf59e207ae. Recibo: C:/IALD/Central de Patentes/Chatgpt/UNITARIA_ESTATICA_DINAMICA_20260909_134841_883787/BUILD_20260909_135524_274453/BUILD_RESULT.json.

O novo módulo contém 9 teoremas e 4 definições, com 13 auditorias. A build recompilou também as duas dependências próprias copiadas byte a byte: no total 49 teoremas, 17 definições/estruturas e 66 auditorias. Os 4 processos, incluindo importador separado, terminaram com código zero, sem erros nem avisos e usando apenas propext, Classical.choice e Quot.sound. Fronteira direta medida antes/depois: inalterada. Isso não é reconstrução independente de todas as dependências transitivas.

[REAL] A família efetiva é U(t)=I ⊕ jointBlockFlow(C,f,√2t), em espaço complexo de amplitudes ι ⊕ (Fin 2 × κ). Foram demonstrados U†U=UU†=I e U(0)=I. Não se afirma neste suplemento uma nova prova da lei de grupo temporal.

[REAL] As amplitudes inicial e evoluída são construídas explicitamente: bloco estático √(1/2)√q; bloco dinâmico √(1/2) vezes a amplitude Joint correspondente. A identidade U(t)Ψ₀=Ψ(t) foi demonstrada, e a amplitude em zero é a inicial.

[REAL] mixedLabelEquiv leva ι ⊕ (Fin 2 × κ) a ι ⊕ (κ × Fin 2), mantendo o rótulo estático e trocando apenas os dois índices do bloco dinâmico. Não troca o ramo de reflexão/transmissão.

[REAL] Com q≥0 e soma q=1, o quadrado do módulo de cada amplitude evoluída é exatamente o peso de mixedCurve após essa reindexação. A soma dos pesos/normas quadráticas é 1. mixed_flow_diagonal_readout aplica a identidade diretamente ao vetor U(t)Ψ₀, ligando operador, amplitude e distribuição em um único teorema. q≥0/soma1 não são necessários à unitariedade do operador, e entram explicitamente na leitura/normalização.

## API

Namespace ChatgptAudit.StaticDynamicUnitary.

| Declaração | Linha |
|---|---:|
| mixedLabelEquiv | 11 |
| mixedBlockFlow | 14 |
| mixed_block_flow_unitary | 19 |
| mixed_block_flow_zero | 33 |
| mixedInitialAmplitude | 42 |
| mixedBlockAmplitude | 48 |
| mixed_block_flow_prepares_amplitude | 55 |
| mixed_block_amplitude_zero | 69 |
| sqrt_half_amplitude_weight | 76 |
| mixed_block_amplitude_weights | 87 |
| mixed_block_amplitude_normalized | 110 |
| mixed_initial_amplitude_normalized | 122 |
| mixed_flow_diagonal_readout | 129 |

## Alcance

[INPUT] Os resultados entrópicos da dependência StaticDynamicMixture referem-se à entropia das probabilidades da leitura diagonal rotulada. O vetor global puro não possui essa entropia como entropia de von Neumann de seu projetor. q estritamente positivo não torna esse projetor fiel/invertível na álgebra matricial inteira; não há conclusão de separância de Tomita.

[INPUT] A mistura preserva incrementos e coeficientes quadráticos. Sua entropia absoluta inclui o termo dos rótulos e não é afirmada igual à original; nenhum custo canônico absoluto é declarado preservado.

[OPEN] Ainda não há neste módulo a instanciação do codec geométrico de 32 resultados com a fonte calibrada de 16 resultados, nem uma origem física/lei de transformação para os registros. A distribuição inicial não identifica a fonte T sozinha; dados de preparação e resposta podem ser necessários.

[REAL — processo] Foram preservadas as duas tentativas anteriores FAIL_VISIBLE: a primeira requereu uma identidade explícita para o bloco em zero e coerções ℝ→ℂ tipadas no readout; a segunda passou todos os termos, mas ainda continha um aviso de hipótese Fintype desnecessária. A tentativa final removeu essa hipótese, sem desativar o verificador. Backups de bytes e logs permanecem na pasta.

[DECLARADO — revisão independente recebida] O root leu a fonte integral e considerou a construção favorável, conferindo a troca de índices, a ação do operador, as hipóteses q≥0/soma1 e os limites de entropia/fidelidade acima. Essa revisão foi de leitura.

[REAL — preservação] Somente esta pasta nova Chatgpt recebeu alterações. Dependências congeladas foram copiadas byte a byte e conferidas contra seus recibos PASS. Nenhum um.py foi executado/importado; originais, Atlas e lote integrado permaneceram intactos.
