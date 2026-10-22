[REAL / INPUT / OPEN] ENTREGA 020 ESPONTÂNEA — área quadrática, integral de calor e reconstrução condicional de Einstein.

06/09/2026. Continuação de 019. Auditoria independente da gerência pendente. Nenhuma alteração de gate.

## Critérios

| Critério | Estado | Evidência |
|---|---|---|
| Derivação anterior ao código | PAGO | CONTINUACAO020_DERIVACAO_PREVIA.md. |
| Área da tela em segunda ordem | PAGO | screen_area_quadratic_limit: (A(t)−1)/t² → −Ric(v,v)/2. |
| Extensão contínua do germe | PAGO | pastContinuousExtension, com truncamento a um intervalo [a,0]. |
| Integral efetiva do fluxo estipulado | PAGO | constructedHeat é uma integral intervalar; constructed_heat_rate prova sua derivada local. |
| Coeficiente de calor | PAGO | constructed_heat_quadratic_limit: Q(t)/t² → −rate T(v,v)/2. |
| Independência da extensão | PAGO | heat_extension_difference_quadratic_zero. |
| Coeficiente do resíduo | PAGO | screen_clausius_coefficient: rate/2 × (η Ric(v,v)/(2π) − T(v,v)). |
| Equivalência exata de Clausius | PAGO sob INPUT | constructed_clausius_at_iff; exige rate≠0 e η≠0. Clausius não foi deduzido da geometria. |
| Construção de GeometricHorizonPencil | PAGO sob INPUT | horizonPencilFromScreen constrói os campos e a integral; recebe a condição de Clausius. |
| Reconstrução geral em aberto conexo | PAGO CONDICIONAL | einstein_from_constructed_clausius: G+Λg=(2π/η)T, com todas as hipóteses expostas. |
| Controle de vácuo plano | PAGO | flat_vacuum_clausius, com objetos efetivamente construídos. |
| Controle negativo conservado | PAGO | conserved_matter_does_not_force_constructed_clausius: T=diag(1,0,0,0) é simétrico e conservado, mas o resíduo dividido por t² tende a −1/2. |
| Justificação física de Clausius/H3 | NÃO PAGO | Condição explícita, equivalente à relação nula de Einstein nos dados considerados. |
| Horizonte imerso, área espacial integrada e ponte microscópica | NÃO PAGO | A integral construída é temporal, e o nome do tipo não fornece uma hipersuperfície nula. |

7 módulos; 48 teoremas declarados; 6 definições com axiomas impressos separadamente. Contagens lidas dos fontes.
As compilações finais fixadas têm exit 0, fonte estável e nenhum erro, aviso ou sorryAx. Os axiomas impressos pertencem ao trio propext, Classical.choice, Quot.sound. As contagens incluem lemas auxiliares, aplicações e controles.

## Enunciado principal

Dados U⊆R⁴ aberto e conexo, A,B suaves com AB=BA=I em U, T diferenciável, simétrico e covariantemente conservado, rate≠0 e η≠0, constrói-se para cada p∈U e v≠0 nulo uma congruência geodésica de equilíbrio, sua tela e a integral Q do fluxo estipulado −rate·t·T(V,V)·A(t).
Se, para todos esses p e v, o resíduo Q(t)−rate·η/(2π)·(A(t)−1) dividido por t² tende a zero pela esquerda, existe uma constante Λ tal que G+Λg=(2π/η)T em U.
O antecedente termodinâmico é ConstructedClausiusAt. O teorema constructed_clausius_at_iff mostra que ele equivale a Ric(v,v)=(2π/η)T(v,v). Ele não pode ser considerado demonstrado apenas porque Q foi integrado.

## Controle que delimita o resultado

Na solda identidade, Ric=0. Com T=diag(1,0,0,0), direção v=(1,1,0,0), rate=1 e η=2π, o tensor é simétrico e conservado, e T(v,v)=1. A área tem coeficiente quadrático zero; o calor e o resíduo têm coeficiente −1/2. Logo a condição de Clausius falha. Com T=0, o controle positivo satisfaz a condição.

## Reprodução

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation020.py'
```

O comando só lê e confere bytes, logs e axiomas registrados. A gerência deve recompilar em uma cópia para a auditoria independente. Ordem dos novos módulos:
- PastContinuousExtension.lean
- EquilibriumAreaExpansion.lean
- ConstructedHeatPrimitive.lean
- ScreenClausiusCoefficient.lean
- ConstructedHorizonPencil.lean
- ConstructedEinsteinReconstruction.lean
- ConstructedClausiusControls.lean

ConstructedClausiusControls importa a árvore inteira 020 e as dependências locais anteriores. O manifesto registra a ordem local completa. O wrapper documenta Lean 4.31.0/mathlib; não se declara um pacote portátil integral.

## Axiomas impressos

```text
ChatgptAudit.Flow020.past_clamp_continuous: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.past_clamp_mem: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.past_clamp_fixes: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.pastContinuousExtension: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.past_integral_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.past_integral_continuous: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.past_integral_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.past_integral_initial_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.past_integral_matches_flux: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.screen_area_continuous_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.screen_curve_eventually_neighborhood: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.screen_matter_continuous_at: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.screen_matter_continuous_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.screen_matter_continuous_past: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.area_quadratic_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.screen_area_quadratic_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.screen_heat_flux_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.screen_heat_flux_continuous_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.screen_heat_flux_continuous_past: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.screenHeatExtension: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.constructedHeat: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.constructed_heat_continuous: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.constructed_heat_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.constructed_heat_rate: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.screen_heat_flux_linear_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.screen_heat_quadratic_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.constructed_heat_quadratic_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.heat_extension_difference_quadratic_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.residual_quadratic_coefficient: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.clausius_coefficient_zero_iff: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.past_zero_limit_iff: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.screen_clausius_coefficient: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.screen_clausius_iff_null_balance: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.constructed_clausius_iff_null_balance: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.horizonPencilFromScreen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.null_balance_produces_pencil: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.ConstructedClausiusAt: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.constructed_clausius_at_iff: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.einstein_from_constructed_clausius: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.flat_solder_inverse: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.flat_solder_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.flat_control_null: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.flat_connection_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.flat_ricci_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.flatConstructedScreen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.control_matter_differentiable: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.control_matter_symmetric: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.control_matter_conserved: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.control_matter_null_value: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.flat_constructed_residual_coefficient: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.flat_nonzero_matter_residual: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.flat_nonzero_matter_not_clausius: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.flat_vacuum_clausius: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow020.conserved_matter_does_not_force_constructed_clausius: [propext, Classical.choice, Quot.sound]
```

## Artefatos e hashes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO020_MANIFESTO.json` — SHA256 `ce73afc38c941d9956dfb04c5cf2065186c4a4256a95320f9704f0e42c97272a`.
Inventário: 591 caminhos absolutos, com tamanho e hash dos bytes.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation020.py` | `fbb7f23f5879f6054daaa78b2daeb0952aff8510ce17a69580a50e582840a4ea` |
| `C:\IALD\Central de Patentes\Chatgpt\ConstructedClausiusControls.20260906_033658.log` | `bacd969867d6eb200f60cca4e490ef4124e32e7aab976220478490d4247dba37` |
| `C:\IALD\Central de Patentes\Chatgpt\ConstructedClausiusControls.lean` | `5f3d290d33090aa3699d8e2a744c70f88e4f995de1d87e270c02062a0cda4e0e` |
| `C:\IALD\Central de Patentes\Chatgpt\ConstructedEinsteinReconstruction.20260906_033143.log` | `3b92fcec3ca737b35b7165f75213c24ebeb96e66c4988860b331a96ee93f5eff` |
| `C:\IALD\Central de Patentes\Chatgpt\ConstructedEinsteinReconstruction.lean` | `6078d3e8a39400156a4b7cdfb2172ef61895fc896c557a931b9e2778c15617be` |
| `C:\IALD\Central de Patentes\Chatgpt\ConstructedHeatPrimitive.20260906_032211.log` | `ab47e0245bc9d05640577d270c9f79b57d211784cffc243af16fb841cdaa87b3` |
| `C:\IALD\Central de Patentes\Chatgpt\ConstructedHeatPrimitive.lean` | `02aaf7d2bd42e74e03be4590316b53b226ca947c8f3515cd5bd9ae3df6e5a891` |
| `C:\IALD\Central de Patentes\Chatgpt\ConstructedHorizonPencil.20260906_033048.log` | `9e65aa4f0afc2832c0da6aa058603b37156ac660df7668ed34472497172bfc0b` |
| `C:\IALD\Central de Patentes\Chatgpt\ConstructedHorizonPencil.lean` | `fe72bdca5282d3f31783dcf63cd4fcbc14a9cb6ab6bfb451575134cc42ad6190` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO020_DERIVACAO_PREVIA.md` | `bfc7915e00a987574361a43a898aa289b9d20e41a310b1b5f58d248b349a115e` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO020_PARECER.md` | `5a9ca55d1873c28e7f585930a5556edd8e64156015d3c198d1835079d3276e29` |
| `C:\IALD\Central de Patentes\Chatgpt\EquilibriumAreaExpansion.20260906_031936.log` | `e857d776a6598762ca1389a22de1b6614bac01aacf3019b714c8b25a84a9c972` |
| `C:\IALD\Central de Patentes\Chatgpt\EquilibriumAreaExpansion.lean` | `a948480f487da4f8ef5f57ef021d8fc13620d5d0dd51b932ffeb4867f0007809` |
| `C:\IALD\Central de Patentes\Chatgpt\PastContinuousExtension.20260906_031908.log` | `f923e33646f31649c159d53724a636618df98abd374c0f2870e94612647a934a` |
| `C:\IALD\Central de Patentes\Chatgpt\PastContinuousExtension.lean` | `8cf1ca55d4d44e216c63ede7a0a535375c537d62cd4ea0e0e77e664b2bbff191` |
| `C:\IALD\Central de Patentes\Chatgpt\ScreenClausiusCoefficient.20260906_032825.log` | `4522b07d7dc2cc6d2dd9bf1463ea0c6231c82fe0b7cbf0ee4fa4c61c959d6d4e` |
| `C:\IALD\Central de Patentes\Chatgpt\ScreenClausiusCoefficient.lean` | `2845ae502d5f0c083ec70dbf135a144b136a1c4d68969a83a8320b8af1958486` |

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\PastContinuousExtension.20260906_031552.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\EquilibriumAreaExpansion.20260906_031738.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\ScreenClausiusCoefficient.20260906_032737.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\ConstructedHorizonPencil.20260906_032931.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\ConstructedClausiusControls.20260906_033313.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\ConstructedClausiusControls.20260906_033423.rejected_warning.log`: exit code 0; cópia exata do log rejeitado.

Todas as versões compiladas são recuperáveis pelo fonte final ou pelos backups de bytes. Somente as compilações finais limpas sustentam esta entrega; falhas intermediárias e avisos foram preservados.

## Limites

O avanço remove a primitiva e o lápis geométrico inteiro da lista de objetos recebidos como hipótese. Não remove Clausius: a nova equivalência e o controle negativo expõem precisamente esse limite.
O fluxo de energia-momento é uma expressão matemática estipulada a partir de T. Sua identificação com calor físico ou energia modular, temperatura e coeficiente de entropia por área não foi demonstrada.
A área é a área normalizada da tela transportada ao longo da curva. A integral é temporal. Não se construiu uma hipersuperfície nula imersa nem uma integral espacial de área sobre horizonte.
Dimensão, assinatura e solda são INPUT. Região–álgebra, entropia–área microscópica, identificação do tensor T, Clausius/H3, origem modular da solda e globalização seguem OPEN.
A constante Λ é obtida no aberto conexo considerado, por conservação e Bianchi já formalizados. Isso não equivale a construir uma variedade global ou demonstrar gravidade quântica.

Nenhum um.py executado, importado ou editado. Todas as escritas em Chatgpt; kernel canônico, Atlas, memórias, selos e gate intocados pela bancada. A custódia 019 foi reconferida em modo de leitura.
O objetivo amplo permanece ativo e não alcançado. Incorporação pela gerência após auditoria; confirmação física reservada ao observador.

Parecer: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO020_PARECER.md.

Ordens de entrada encontradas no inventário:
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_001_esperanca_condicional_e_escala.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_002_veredito_da_auditoria_e_incorporacao.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_003_localizacao_na_cadeia_e_ponte_volume.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_004_D1_fiacao_e_D7_segundo_objeto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_005_reabertura_v98_e_teste_conjunto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md
