# Fecho objetivo — matriz de dependência (25/10/2026)

## Resultado medido nesta rodada

A fonte original da Ordem 025 compila contra a `FalsidadeDaInercia.lean` da v401 (`9f6efcb2a0987e18`), com `lake build TGLExt.PonteDaEscalaDual` terminando em `Build completed successfully (9267 jobs)`. A compatibilidade formal está demonstrada nesta cópia; produção, espelho e gate não foram tocados. Isto não é fechamento físico nem confirmação.

## A diferença que a cadeia curta deve tornar impossível apagar

O trio de axiomas do Lean audita dependências lógicas. Não apaga campos de estruturas, escolhas geométricas, constantes físicas, literatura ou identificações com a natureza. Uma prova objetiva deve mostrar cada um desses fornecedores e impedir que o alvo seja reintroduzido como premissa.

| elo | fornecedor atual | estatuto observado | o que falta para fechamento objetivo |
|---|---|---|---|
| `ω(I)=1` | operador/posto | fundamento declarado | nenhum; não confundir posto com medição da natureza |
| Meia-Nat | autocorrelação da fronteira | teorema condicionado à autocorrelação | preservar explicitamente o antecedente |
| `α` | CODATA | constante física importada | não é derivada pela forma |
| `β=α√e` | composição da Meia-Nat com α | forma derivada; seta física em teste | demonstrar o observável sem trocar β por parâmetro livre |
| `DualScalingData.scaling` | campo da estrutura | lei de Takesaki [KNOWN] | identificar a ação dual com dinâmica física |
| `τ=pPlus` | Ordem 025 | instância construída e agora compatível com v401 | calibrar unidades e referente de um corpo/processos |
| `θ(s)=boost(-s)` | Ordem 025 | ação de Lorentz importada e composta | ligar ao fluxo modular físico/BW, inclusive `2π` |
| `m²=pPlus*pMinus` | álgebra da métrica escolhida | invariante demonstrado | derivar a métrica e selecionar a escala de massa |
| `μ²` | parâmetro do `lift` | livre; `lift_mass_not_selected` | uma lei dinâmica de seleção, não outro nome |
| `E=mc²` | casca + repouso + sinais | teorema sob premissas explícitas | derivar as premissas físicas sem importar o alvo |
| `η₄` | representação 4D importada | métrica lorentziana dada | derivar a assinatura `(1,3)` |
| `Fin 4` | representação 4D importada | dimensão escolhida | derivar `rank c=4`/H2 |
| `coreLift` | cone positivo do núcleo regular | mapa não necessariamente injetivo | identificação algébrica/observável, não só do traço |
| `Tᵘᵛ` | ainda não consumido pela ponte | ausente no resultado O25 | tensor simétrico, conservado, normalizado |
| fluxo nulo/`δQ` | `ConstructedHeatPrimitive` existe mas não foi ligado | fiação aberta | identificar o fluxo do tensor na tela |
| H3/Clausius | Jacobson/estruturas nomeadas | antecedente, não consequência | provar em toda direção nula ou limitar a tese |
| `G` | constante física | input | não derivar retoricamente de normalização |
| região↔álgebra | torre-produto/realizações | ponte física aberta | identificar regiões do espaço-tempo |
| III₁/UV/global | literatura e escopo das instâncias | não construído em geral | existência global, interação e regime UV |
| dados prospectivos | ainda não abertos nesta frente | ausentes | pré-registro, réplica independente e regra 5σ |

## Bloqueio estrutural que a próxima derivação deve respeitar

A lei `τ∘θ_s=e^{-s}τ` é homogênea de grau um. Ela fornece uma componente nula que escala; não seleciona, sozinha, uma massa de repouso não nula e invariante. A Ordem 025 já transforma isso em teorema ao permitir `μ²` arbitrários. Portanto:

1. não é possível obter seleção única de massa apenas repetindo a mesma lei de escala;
2. é necessário um segundo invariante dinâmico com origem independente, ou uma equação de estado/campo que fixe a casca;
3. se esse segundo invariante for posto à mão, a cadeia continua condicional;
4. o alvo correto é derivar a dinâmica que o produz, não declarar que `τ` já era massa.

## Próximo alvo formal

Construir, sem usar `E=mc²`, Einstein ou H3 como premissa, uma dinâmica candidata na qual o segundo invariante e o tensor de matéria surjam da mesma realização. Se a construção precisar assumir exatamente o tensor, a casca, a assinatura ou a lei de campo pretendida, ela será marcada como condicional e não contará como fecho objetivo.

`NOT_FALSIFIED` não é `CONFIRMED`; compatibilidade no kernel não é creditação; nenhum resultado a 5σ foi produzido.
