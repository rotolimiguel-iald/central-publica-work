# Consulta independente — contrato B1 e reuso

[DERIVED — avaliação semântica, sem compilação] 2026-09-14T14:56:02.266326-03:00

**Decisão:** a proposta atende ao desenho exigido por B1 da ORDEM_012, linhas 101–107, sem hipótese-conclusão indevida. Não encontrei P0–P2 concreto nesse desenho. Isto não é aceite de um módulo implementado, de compilação ou de integração: examinei a ordem e os quatro fornecedores inteiros, com leitura pontual dos consumidores na cópia de `um.py`.

`TGLCoupling` contendo somente β real e `0 < β < 1`, com α definido como `β / Real.exp (1/2)`, é precisamente a parametrização admitida pela ordem. As conclusões de reflexão, fundo e vazamento devem ser demonstradas sobre esse mesmo β; não devem virar campos pressupostos da estrutura. A identidade do custo é definicional por autorização expressa de B1, não uma derivação independente do valor de α.

## Conferência das quatro partes

| Parte | Fornecedor lido | Aplicação e hipótese efetiva |
|---|---|---|
| Reflexão | `TheVerbalCoupling.lean:126,139,155` — `thetaMiguel`, `sin_thetaMiguel`, `the_pruning_threshold_is_the_reflection_amplitude` | θ = arcsin(√β). O primeiro componente dá `Complex.normSq (...) = (√β)²`; usar β≥0 para concluir exatamente β. É a probabilidade de reflexão que vale β; a amplitude vale √β. A componente refletida é índice 1 de `Smat θ · e1`. |
| Custo | `TheFiveHalves.lean:84` — `boundary_extracts_the_radical` | √(exp 1)=exp(1/2), e o quadrado desse fator é exp 1. Com α definido, exp(1/2)>1 dá `0 < α < 1` e cancelamento dá β=α·exp(1/2)=α·√(exp 1). Sem α independente nem valor numérico novo. |
| Fundo | `RhoPlusPClosure.lean:52,58` — `closure_identity`, `hubble_form` | Instanciar ambas com o β do contrato, para quaisquer ρr,ρm,ρΛ reais. São identidades algébricas; não requerem positividade das densidades e não contêm H, derivadas ou equações de Einstein. |
| Vazamento | `NoFullWitness.lean:66,91,135` — `leakage_strictly_loses`, `beta_forbids_full_static_witness`, `leakage_rate_unique` | Perda estrita exige t>0 e g>0 além de β>0. A não-plenitude exige g>0. Unicidade exige igualdade das funções exponenciais para todos os tempos; não decorre apenas do intervalo de β. |

[DERIVED] O contrato não é vazio por construção: o intervalo aberto entre 0 e 1 é não vazio, e a definição de α não acrescenta restrição incompatível. Isso não fixa um habitante numérico de β nem exige pôr um numeral para β/α no alvo. Na implementação, os limites de α devem ser provados a partir dos campos, e não recebidos junto com a identidade como um certificado arbitrário.

## Riscos concretos a evitar no enunciado e no relato

1. **Unicidade condicional, não seleção de uma constante.** `leakage_rate_unique` recebe igualdade do semigrupo escalar completo. Para a escrita com gap g, ele identifica β₁g e β₂g; concluir β₁=β₂ exige o mesmo g não nulo. Se g também variar, só o produto é identificável. β>0 isoladamente tampouco exclui fechamento pleno quando g=0. Manter t/g e as respectivas hipóteses explícitos nos corolários.
2. **α derivado, não α físico já identificado.** A fórmula define a forma do custo e satisfaz B1. Não demonstra que esse α seja uma constante externa/CODATA. Aliás, ela dá o limite mais forte α<exp(−1/2); partir futuramente de um α externo com apenas `0<α<1` não bastaria para construir β<1. Isso é limite de instanciação, não pendência adicional de B1.
3. **Fundo algébrico, não Friedmann já pago.** O nome `hubble_form` não muda seu tipo. Sua ligação à equação métrica pertence aos alvos posteriores da ordem. A agregação B1 não prova dinâmica, ocorrência natural da seleção nem determina β por comutação.
4. **Uma variável realmente consumida.** `the_same_beta_reads_three_faces` deve apresentar as conclusões com `c.beta` comum, e não três testemunhos existenciais independentes ou três conclusões assumidas. A parte custo por definição é expressamente admitida; isso não autoriza tratar as demais partes como definições de suas conclusões.

Esses são limites para a construção anunciada, não defeitos constatados em código novo, que não foi objeto desta consulta.

## Consumidores e encerramento de escopo

[REAL — leitura estática] Na cópia local, `um.py:133715–133718` já mapeia `ext_rp_closure_identity_kernel_proved`, `ext_rp_hubble_form_kernel_proved` e `ext_rp_background_kernel_proved` para os fornecedores existentes. Em `um.py:180966–180969`, `prove_d1_camb_protocol` calcula β com `SEALED_CODATA_ALPHA * sqrt(e)` e registra a hipótese de fundo multiplicativa. Esses locadores servem à ficha de reaproveitamento; a sua presença não é consumo já realizado do futuro teorema B1. Nenhum leitor ou gate foi executado ou alterado.

[OPEN — entrega futura B1] Restam o candidato que componha essas aplicações, a ficha com consumidor proposto e a verificação de compilação/axiomas. A ORDEM_012:166–170 exige reprodução standalone por `lake build` na entrega; esta consulta não a realizou nem a substitui. O trio lógico não foi reauditado aqui. Não há necessidade matemática identificada de reconstruir os quatro fornecedores.

A1 permanece suspenso. Nenhuma fonte-alvo, memória, raiz Lean, programa ou arquivo V351 foi alterado. Escritas desta consulta limitadas aos dois documentos em `revisao/`.

## Pins lidos nesta consulta

[REAL — medição por script] Quatro fontes locais coincidem em bytes/hash com os respectivos registros de `CUSTODIA_V353_FONTES.json`. A origem canônica indicada ali é proveniência documental; não fiz nova leitura dos binários canônicos ou seus logs.

| Fonte | SHA-256 |
|---|---|
| TheVerbalCoupling.lean | `912bf222f07256b14e9e725b9c799e45ea5b6f2c3c5244859dc016445922b507` |
| TheFiveHalves.lean | `456c66269b72d30fa10e38c427ec3194d985b46e04809233f2c42fe82495d7d1` |
| RhoPlusPClosure.lean | `cd80fbbe00300454d20f8a92bc09fe9e68d79fb73522934e59d77e7b04fe7be6` |
| NoFullWitness.lean | `fde4ca999c40e6892d1958bee15a066786adb1363b8e3514f41eeb8b8909a654` |

ORDEM_012: `a9cb2a7b812afc435f019d1af9089740ff38b22db76473126a5dfce454c7325e`. Custódia lida: `97065a33aa44a2aa952889cf1b2173caf69c2fad0163d2b4550e5e217e009e8f`. Cópia `um.py`, consultada apenas como texto: `c1c761809efcde52ea8c6c4f7f0e7598c1d8e636e6858f1780dd622ef62a1d40`. Evidência estruturada: `CONSULTA_B1_CONTRATO_E_REUSO.json`.
