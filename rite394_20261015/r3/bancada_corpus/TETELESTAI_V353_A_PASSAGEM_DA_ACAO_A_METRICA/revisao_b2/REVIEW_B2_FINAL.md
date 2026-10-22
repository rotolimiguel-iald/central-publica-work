# B2 — revisão independente final

2026-09-14T16:47:06.188601-03:00 · **B2_DEV_REVIEW**

[REAL] **Aceito no escopo B2. P0: nenhum; P1: nenhum; P2: nenhum.** Fontes integrais, ficha e cláusula B2 da ORDEM 012 lidas. Reprodução própria por Lake, seguida de auditor próprio com `#check`, universos e `#print axioms`: **32 declarações = 26 teoremas + 6 definições**, todas limitadas a `propext`, `Classical.choice`, `Quot.sound`. Nenhum aviso novo. Não há aceite de integração, B3–B6, nova calibração física ou alteração de gate.

## Reprodução e proveniência

Raiz própria curta: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\s`. Primeiro `lake build TGLExt.GeneralMetricEinstein`; depois `lake build TGLExt.FLRWGeometry TGLExt.FLRWFieldEquations TGLExt.AuditFLRW TGLExt.ReviewFLRW`. Os dois comandos finais terminaram rc0. Mesma Lean 4.31.0, com binários/toolchain pinados nos runs. `92` objetos TGL/TGLExt produzidos nesta raiz, incluindo o auditor próprio; nenhum objeto de projeto autoral ou de B1 foi copiado. As 88 fontes transitivas iniciais e as três fontes B2 foram copiadas em bytes e conferidas; o auditor próprio é a quarta fonte do delta.

Mathlib e oito pacotes auxiliares vieram do cache privado de B1 em `R/r/.lake/packages`, copiados com leitura/verificação dos hashes de cada arquivo e revisão Git igual ao manifesto. Este cache é **herdado**, não recompilação independente de Mathlib/toolchain. LEAN_PATH/LEAN_SRC_PATH externos removidos; as traces mostram somente bibliotecas da raiz privada e pacotes privados. Os objetos dos dois módulos novos e AuditFLRW são byte a byte iguais aos autorais. B1/R/r, seus relatórios, compilation/run e manifesto permanecem intocados e os pins protegidos foram relidos.

Falhas próprias preservadas: erro de encoding do preparador (`utf8-sig`, corrigido para `utf-8-sig` em arquivo novo); preparação interrompida antes de Lake, retomada verificando as cópias; recusa Git por propriedade de diretório do cache criado sob conta sandbox. Esta última foi resolvida por nove `safe.directory` exatos apenas no ambiente do processo, sem configuração global. Nenhuma dessas falhas é refutação matemática. Por isso `all_accepted_builds_exit_zero=true` e `all_attempts_exit_zero=false`.

## Hipóteses e consumidor real

`flrwMetric` é diag(1,-a²,-a²,-a²), na assinatura (+---). `flrw_metric_inverse` identifica a inversa diagonal com `metricInverse`; `flrw_connection` calcula a Levi-Civita dessa mesma métrica. `flrw_ricci` transporta a igualdade local da conexão aos jets em U aberto antes de avaliar a curvatura. As hipóteses hG/hJ do auxiliar algébrico são descarregadas. Nenhuma componente Ricci/Einstein foi pressuposta como campo.

`flrw_einstein_tensor` fornece a matriz inteira, incluindo componentes fora da diagonal nulas; as leituras 00/espaciais e a identidade de Ricci nulo usam esse mesmo objeto. `flrw_stress_divergence` calcula os quatro componentes de divergência do fluido; a continuidade é condicional à componente temporal nula. Há diferenciabilidade local de rho e pressão e suavidade local de a, não hipóteses globais fora de U.

As leituras `flrw_friedmann_first`, `flrw_acceleration` e `flrw_friedmann_second` têm hE tensorial explícita. Isso não é circularidade na entrega: `flrw_friedmann_from_general_metric` **obtém** hE de `metric_only_einstein_equation`, fornecendo Lorentz/suavidade/regularidade/simetria concretas e preservando **H_null e H_conservation como hipóteses nomeadas**. Abertura e preconexidade de U são explícitas; Lambda é uma única constante existencial em U. Não se afirma conservação, balanço nulo ou realização física incondicionais.

O sinal segue `G+Lambda*g=coupling*T`: `H²=coupling*rho/3-Lambda/3`, `a''/a=-coupling*(rho+3p)/6-Lambda/3` e `H'=-coupling*(rho+p)/2`. Não há divisão por H, portanto H=0 não é excluído. Nenhuma identificação automática com uma Lambda física de outra convenção. Eta é real arbitrário no teorema algébrico, com a divisão total de Lean; a leitura de Newton usa G>0 e eta=1/(4G) como INPUT. `flrw_newton_coefficient` consome `einstein_coefficient_from_clausius`, sem derivar essa calibração nem fixar beta.

Ficha: 24 locadores em 11 arquivos conferidos por hash/linha. A proposta coincide com a maquinaria solicitada; Ansätze antigos não foram renomeados como FLRW. As quatro entradas `ext_flrw_*` são consumidores propostos, não instalação revisada. Não houve leitura/execução de um.py, dados ou Atlas nesta rodada; a afirmação autoral de preservação de 941 fontes/um foi somente relida em AUDITORIA_B2.

## Evidência autora e controles negativos

Run final autoral `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\attempts\20260914_162109_507348\run.json` rc0 e snapshots iguais aos três pins próprios. AUDITORIA_B2, seu auditor de 32 alvos e streams das duas sondas foram relidos e pinados; nenhum desses scripts foi executado por esta revisão. A rodada válida rejeita por **Type mismatch** a troca 3→4 em G00 e a troca do sinal de Lambda, com imports funcionais. A rodada anterior FAILED_SYNTAX, com erro lexical em `a(y0)`, é preservada e **excluída** como controle matemático. Não foram ampliados controles.

## Pins do candidato congelado

| Arquivo | SHA256 fonte | SHA256 objeto próprio = autor |
|---|---|---|
| FLRWGeometry | `47aea5aebebd8611edab566724ce562508908dc86b96db7194dff2592bac9e92` | `c492c87f27c2f751ef9b5a6b58ad874489ecf506cc2447ad0bb1bf6b4512f09f` |
| FLRWFieldEquations | `5db1052c8fad79e2858715de70b7f2aef9691825d26e1c5f208a951c6299f6c8` | `5730c9d4cc58e486f06c5d3faa55cbab4e5026795af1f1b50e2d1a4fae280fe2` |
| AuditFLRW | `db1f1b0f494bca195511cbb7316e8d504760b3508301674bfbee81113e990730` | `fdcc722800d1ad2d3bb9ad301c4c1325dc698bcf142318d635cc29a5121bd71e` |

## Avisos herdados

59 mensagens de aviso em fornecedores reconstruídos, nenhuma nos módulos B2 ou auditores. São lints herdados (argumentos de simp/binders não usados e deprecações), preservados integralmente em `compilation.json → inherited_warnings` com módulo e mensagem; não foram silenciados nem corrigidos nesta revisão.

## Alvos conferidos

- `ChatgptAudit.FLRW.flrwMetric`
- `ChatgptAudit.FLRW.flrwInverse`
- `ChatgptAudit.FLRW.flrwHubble`
- `ChatgptAudit.FLRW.flrw_metric_lorentz`
- `ChatgptAudit.FLRW.flrw_inverse_left`
- `ChatgptAudit.FLRW.flrw_inverse_right`
- `ChatgptAudit.FLRW.flrw_metric_inverse`
- `ChatgptAudit.FLRW.coordinatePartial_time_function`
- `ChatgptAudit.FLRW.flrw_metric_smooth`
- `ChatgptAudit.FLRW.flrw_inverse_smooth`
- `ChatgptAudit.FLRW.flrw_metric_jet`
- `ChatgptAudit.FLRW.flrwConnectionForm`
- `ChatgptAudit.FLRW.flrwConnection`
- `ChatgptAudit.FLRW.flrw_connection`
- `ChatgptAudit.FLRW.flrw_connection_form_jet`
- `ChatgptAudit.FLRW.flrw_connection_form_ricci`
- `ChatgptAudit.FLRW.flrw_ricci`
- `ChatgptAudit.FLRW.flrw_einstein_tensor`
- `ChatgptAudit.FLRW.flrw_einstein_00`
- `ChatgptAudit.FLRW.flrw_einstein_spatial`
- `ChatgptAudit.FLRW.flrw_null_ricci`
- `ChatgptAudit.FLRW.flrwStress`
- `ChatgptAudit.FLRW.flrw_stress_symmetric`
- `ChatgptAudit.FLRW.flrw_stress_differentiable`
- `ChatgptAudit.FLRW.flrw_stress_jet`
- `ChatgptAudit.FLRW.flrw_stress_divergence`
- `ChatgptAudit.FLRW.flrw_continuity`
- `ChatgptAudit.FLRW.flrw_friedmann_first`
- `ChatgptAudit.FLRW.flrw_acceleration`
- `ChatgptAudit.FLRW.flrw_friedmann_second`
- `ChatgptAudit.FLRW.flrw_friedmann_from_general_metric`
- `ChatgptAudit.FLRW.flrw_newton_coefficient`

Os enunciados completos impressos pelo auditor, axiomas por alvo, fontes/objetos, traces, runs, pacotes e histórico estão em [compilation.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b2\compilation.json>) SHA256 `7b7bb4682c3e7cfda77b1eb26bdf92860c820300f4bf5ddc51368fd8de2f9a5d`. Evidência desta revisão: [REVIEW_B2_FINAL.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b2\REVIEW_B2_FINAL.json>) SHA256 `5a7cdc4999b103315fd1266bc1b5e3be503ed842b3841612b578fd093320deac`. Fontes e relatórios B1 preservados; nenhuma pendência de revisão B2 dentro deste escopo.
