# Troca do resolvente e preparação da involução polar — DEV

2026-09-12T13:01:39-03:00. [REAL — dois módulos/quatro alvos compilados; sem revisão independente ou integração]

R=(I+S†S)⁻¹, no H_I já construído. O resolvente envia todo H_I para D(S).
Para x∈D(S), escreva u=Rx, w=x−u=S†Su e v=Sw. A involutividade de S
e de seu adjunto máximo põe v no domínio de S†S e dá S†Sv=Su.
Então v+S†Sv=Sx e a identidade inversa do resolvente dá R(Sx)=S(x−Rx).
Logo SRx=Sx−RSx, com todas as inclusões de domínios explícitas.

Os lemas existentes ResolventGraphTransport preservam o gráfico de B pela
ação de R. Com S=UB, obtém-se URz=(I−R)Uz inicialmente em Ran B.
A densidade de Ran B e a continuidade dos dois lados estendem a identidade
a todo H_I. Esse é o segundo resultado do pacote. Não foi assumido U²=I.

As quatro declarações usam apenas propext, Classical.choice e Quot.sound.
Uma tentativa de ScalarTomitaPolarResolvent terminou com timeout na reescrita;
foi substituída por congrArg explícito. O log rc1 foi preservado e excluído,
e o novo pin passou com rc0. Nenhum dos quatro alvos integra os nove/41.

[OPEN — rota proposta, ainda NÃO compilada] Para Q=√(I−R) e P₀=√R, provar
U P₀=Q U e U Q=P₀ U por conjugação antiunitária de operadores positivos e
unicidade da raiz limitada (Mathlib CFC.sqrt_unique). O candidato conjugado
U T U⁻¹ é linear complexo, embora U seja antilinear; sua positividade deve
ser demonstrada, sem supor previamente U=U⁻¹. O teorema já existente
ChatgptAudit.Continuous050.antiunitary_inner_conj pode ser reutilizado.

Se essas trocas forem provadas, S(P₀v)=UQv e S²=I dão U²P₀v=P₀v.
A densidade da imagem de P₀ permitirá U²=I. Essa é uma estratégia matemática
a verificar, não uma prova Lean já disponível. KMS, peso, traço e condições
físicas continuam posteriores. Não foi construído novo certificado de gate.

Mãe integrada histórica `c2d6675fffdd6d96e2a8196d25b9170f69549dd75f7e411b633013c04c54dffe`;
pacote polar DEV `29cf7851071ce34cbe1c0bbdd88fd3cc8787041ebf1961754c3f0c355a815392`.
Toda escrita restrita à cópia. Original não importado/executado/modificado.
