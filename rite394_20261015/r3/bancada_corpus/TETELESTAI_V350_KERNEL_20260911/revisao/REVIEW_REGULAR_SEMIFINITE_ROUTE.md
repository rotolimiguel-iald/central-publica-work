# Revisão independente — rota regular para semifinitude

## Estrato 1 — RegularApproximation

2026-09-12T03:27:08-03:00. **Revisão deste módulo concluída; parecer conjunto ainda pendente das próximas fontes finais e das evidências de integração da etapa.** Nenhum achado P0, P1 ou P2 identificado nos 11 alvos de `RegularApproximation.lean`. Os módulos FourierL1L2 e do ideal do peso, ainda não liberados pelo autor, não foram lidos, congelados ou certificados aqui.

[REAL — recompilação independente] Fonte e auditor próprio passaram rc0. Os 11 tipos foram impressos com universos; todos os axiomas transitivos são exatamente `propext`, `Classical.choice`, `Quot.sound`. A aproximação forte da identidade não foi tomada como prova de semifinitude.

## Provas e tipos conferidos

- **Mesma realização**, [RegularApproximation.lean:16](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularApproximation.lean:16>)–32. `regularBundledUnitary P t` apenas empacota `regularUnitary P t`, sem trocar P ou o operador. A definição anterior relida é `fibre (modularFlowCLM P t) * shift t`, agindo em `Lp (TowerHilbert P) 2 volume`, sobre ℝ com Lebesgue. O certificado unitário fornece preservação da norma vetorial. `regularIntegralFamily` usa a continuidade forte dessa mesma família e obtém a cota uniforme de norma operacional 1; não recebe continuidade em norma de operadores como premissa.
- **Integral de vetores e pertinência**, [RegularApproximation.lean:36](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularApproximation.lean:36>)–49. M_h=`regularAverage P h` é h⁻¹ vezes a integral forte construída em `StrongOperatorIntegral`. Sua aplicação é literalmente h⁻¹·∫₀ʰΛ_t v. A dependência integra vetores de Hilbert e depois constrói um CLM; a prova de pertinência à mesma N usa o bicomutante e a comutação transportada sob a integral. Não há integral de Bochner com valores em B(H) pressuposta. A multiplicação real é coerente com a inclusão ℝ→ℂ na subálgebra.
- **Contração para todo h real**, [RegularApproximation.lean:51](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularApproximation.lean:51>)–64. h=0 é um ramo explícito: a definição vale zero, logo satisfaz a cota. Para h≠0, a estimativa da integral usa |h| e conclui |h⁻¹|·|h|=1. Isso cobre h negativo e positivo com a orientação de `intervalIntegral`. Não se usou positividade dos unitários; o resultado certificado é uma contração, sem afirmar que M_h seja positivo, unitário ou uma projeção.
- **FTC e topologia correta**, [RegularApproximation.lean:68](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularApproximation.lean:68>)–76. Para cada v fixo, f_v(t)=Λ_t v é contínua. A FTC dá derivada f_v(0)=v para h↦∫₀ʰf_v(t)dt. O intervalo inicial 0..0 não torna a prova vazia: o teorema Mathlib exige adicionalmente mensurabilidade forte junto ao filtro e continuidade em zero, ambas fornecidas por f_v. O lema de quocientes diferenciais fornece h⁻¹·(F(0+h)−F(0))→v. O filtro elaborado é **𝓝[≠]0**, vizinhança perfurada bilateral real; o limite usa a norma do vetor em H. O enunciado não contém convergência em norma operacional nem continuidade da extensão M_0=0 até I.
- **Orientação da composição**, [RegularApproximation.lean:78](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularApproximation.lean:78>)–83. Para todo operador limitado A, `(A * M_h) v` tende a A v pela continuidade de A sobre H. O produto é A∘M_h e a afirmação é forte, vetor a vetor. Não foi acrescentada uma hipótese de pertinência de A a N, nem afirmada aqui uma propriedade do ideal do peso.
- **Transporte dual e sinal**, [RegularApproximation.lean:87](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularApproximation.lean:87>)–112. A conjugação θ_s pela multiplicação de caracteres passa pela integral por continuidade e linearidade de D_s, com D_s* aplicado ao vetor de entrada. Especializando a família regular, `dualAmbient_regular` fornece `characterPhase s t • Λ_t`. A definição congelada de `characterPhase` é exp(−i s t). Portanto θ_s(M_h)v=h⁻¹·∫₀ʰexp(−i s t)Λ_t v, com o mesmo grupo, orientação de integral e escalar h⁻¹. A prova vale também em h=0, com ambos os lados nulos. Trata-se da expressão modulada exata, sem uma identidade de Plancherel ou estimativa L² dual demonstrada neste módulo.

Conferi as declarações Mathlib efetivamente usadas: `intervalIntegral.integral_hasDerivAt_right` (linhas 727–730 da referência congelada) e `hasDerivAt_iff_tendsto_slope_zero`/seu alias (linhas 82–87). As referências foram copiadas apenas para `revisao/`, com hashes lidos; os pacotes originais permaneceram em leitura.

## Evidência própria e herança

Fonte final: `cf847f376210447912ca2d08644c06e66375a6f89e82cffe844a241f92c89414` (126 linhas). Log do autor conferido por fonte rc0/inalterada: [RegularApproximation_20260912_032118_790451.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/logs/RegularApproximation_20260912_032118_790451.json>). O log e seus stdout/stderr foram preservados no snapshot.

| Processo executado pelo revisor | rc | Tempo | Alvos de axiomas |
|---|---:|---:|---:|
| RegularApproximation.lean | 0 | 33.366 s | 11 |
| RegularApproximationFullAudit.lean | 0 | 27.364 s | 11 |

Hash do `.olean` próprio do módulo: `4077e3b96cccf34f9721c647ba03c97d9edce9f7d3e1216aa0f5a11a7a779a60`, coincidente com o dev final do autor. Hash do `.olean` do auditor: `eca29782b976ede0067669a6cad708883cd8b52db2cb9515d32476fd1e27cc02`. A repetição dos 11 alvos no auditor não conta como 22 teoremas distintos.

Congelados **349 pares de fonte/binário de dependências do projeto**, herdados do snapshot anterior e conferidos por hash, incluindo as duas fontes da etapa do peso. Não recompilados neste estrato. `LEAN_PATH` próprio começa no build deste snapshot e usa somente os pacotes preexistentes em leitura; não usa o build do projeto do autor como alternativa. Os pacotes não foram reconstruídos. Compilador `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`, SHA `9b216deb50d37c32c829d1efaaa5bafd5560417d382df35a815489e31a31593f`. Os diretórios temporários, fontes e saídas novas ficam em `revisao/`.

Evidências: [manifest.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/regular_approximation_independent_20260912_032358_906563/manifest.json>); [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/regular_approximation_independent_20260912_032358_906563/compilation.json>); [tipos e axiomas completos](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/regular_approximation_independent_20260912_032358_906563/logs/RegularApproximationFullAudit.stdout.txt>); [FTC congelada](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/regular_approximation_independent_20260912_032358_906563/references/Mathlib/MeasureTheory/Integral/IntervalIntegral/FundThmCalculus.lean>); [quocientes diferenciais congelados](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/regular_approximation_independent_20260912_032358_906563/references/Mathlib/Analysis/Calculus/Deriv/Slope.lean>).

A custódia anterior `fixed_weight_custody.json`, datada 2026-09-12T03:13:27-03:00, foi lida e congelada; o hash do parecer anterior confere `8de2c32f60b4b3d03a5c86965ddba24dd33a9326d9f63d61167fe7670f8ee64c`. Os dados anteriores 52/60/6123 e a cópia `a6073b7ed0a8226c794dd822c3803635c2b456807de72010d5253af7f12b1d74` são **estrato histórico do peso fixo**, não contagens da integração deste módulo. Não se executou novamente o verificador de custódia; o registro do autor sobre os 15 backups foi preservado para proveniência.

## Limites e continuação autorizada

[OPEN] Nenhuma finitude do peso de M_h*M_h, estimativa Fourier L¹/L², ideal denso de entradas de peso finito ou semifinitude é concluída por estes 11 enunciados. A cota ‖M_h‖≤1 e M_h→I fortemente não substituem essas obrigações. Também não se concluem F=base original, correspondência espectral/predual geral, traço, Three Locks ou alteração de flags/gate.

Este estrato encerra o exame de `RegularApproximation` sem análise matemática pendente nesse arquivo. O parecer conjunto aguarda o aviso de fontes finais dos próximos módulos; integração/minuta/controles dessa nova etapa ainda não foram certificados. Adendos a este documento exigem backup imediato byte a byte e escrita atômica. Os pareceres custodiados anteriores permanecem intocados; fontes do autor, originais, monólito, memórias e logs não foram alterados pelo revisor. Não executei/importei monólito, recorder ou testes do autor.


## Estrato 2 — FourierL1L2

2026-09-12T03:38:35-03:00. **Revisão deste segundo módulo concluída; parecer conjunto ainda pendente de RegularFiniteWeight final e da integração.** Este adendo atualiza o estatuto de espera de FourierL1L2 registrado no estrato 1, cujo texto e evidências permanecem preservados. Nenhum achado P0, P1 ou P2 identificado nos oito alvos finais. `RegularFiniteWeight`, ainda em autoria, não foi lido ou certificado.

[REAL — processos próprios] `FourierL1L2.lean` e `FourierL1L2FullAudit.lean` recompilados rc0. O auditor imprime os tipos com universos e os axiomas de todos os **oito** alvos, no namespace exato `TGLV350.Fourier`. Todos dependem exatamente de `propext`, `Classical.choice`, `Quot.sound`. Com o estrato 1, são 19 alvos de fontes novas examinados em quatro processos próprios rc0; a integração conjunta não está certificada por essa contagem.

### Conteúdo e encadeamento

1. **Hipóteses e Fourier concretos.** O espaço H é um Hilbert complexo completo arbitrário; as funções têm domínio ℝ, e todas as medidas elaboradas são `volume` de Lebesgue. `fourier_integrable_continuous` ([FourierL1L2.lean:13](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/FourierL1L2.lean:13>)) deriva continuidade da integral Fourier de uma função L¹. `fourier_test_pairing` ([FourierL1L2.lean:18](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/FourierL1L2.lean:18>)) prova a identidade bilinear ∫(𝓕g)·f=∫g·(𝓕f), para g de Schwartz, via o lema vetorial de Fubini com as duas hipóteses de integrabilidade. A dualidade de distribuições usada aqui é bilinear, sem conjugação de g; não é uma alegação de auto-adjunção hermitiana da transformada. O `flip` do emparelhamento real em ℝ é compatível com sua simetria.

2. **Distribuições → igualdade quase sempre, sem círculo.** Em [FourierL1L2.lean:26](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/FourierL1L2.lean:26>), f∈L¹∩L² e F=`hf2.toLp f` são relacionados por `hf2.coeFn_toLp`, explicitamente quase sempre. A igualdade anterior de Mathlib entre a transformada distribucional de F e a transformada L² é avaliada em cada teste de Schwartz; seu tipo e sua prova foram lidos. Essa dependência é construída pela extensão isométrica a partir de Schwartz e por densidade, sem pressupor o novo resultado para integrais Fourier de funções arbitrárias em L¹∩L². O lado da integral usual é localmente integrável porque é contínuo; o lado do representante da transformada L² é localmente integrável porque pertence a L². Só então se aplica `ae_eq_of_integral_contDiff_smul_eq`. As linhas 46–49 convertem cada teste real suave de suporte compacto em teste complexo de Schwartz via `Complex.ofRealCLM`, cobrindo os testes exigidos pelo lema de unicidade. A conclusão é igualdade **quase sempre**; não se promove um representante de L² a igualdade pontual em todo lugar.

3. **Pertinência a L² derivada antes da versão positiva.** [FourierL1L2.lean:51](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/FourierL1L2.lean:51>) transporta `MemLp` pela igualdade quase sempre com a transformada L². A transformada integral não é assumida L² na hipótese. [FourierL1L2.lean:56](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/FourierL1L2.lean:56>) usa a definição do produto interno de L² e a integrabilidade do produto interno para obter ∫‖F(x)‖²=‖F‖²; a parte real passa sob a integral com sua hipótese apropriada. [FourierL1L2.lean:62](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/FourierL1L2.lean:62>) transfere essa igualdade ao representante original f usando `MemLp`. São integrais de funções realmente integráveis neste contexto, não igualdades obtidas pelo valor convencional de uma integral não integrável.

4. **Plancherel real e ENNReal.** [FourierL1L2.lean:71](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/FourierL1L2.lean:71>) combina igualdade quase sempre, identidade da norma L² e isometria `Lp.norm_fourier_eq`. Em [FourierL1L2.lean:82](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/FourierL1L2.lean:82>), primeiro se obtém `hF : MemLp (𝓕 f) 2`; depois `memLp_two_iff_integrable_sq_norm` fornece integrabilidade dos quadrados tanto de f como de 𝓕f. Sua não negatividade é dada ponto a ponto por `sq_nonneg`. `ofReal_integral_eq_lintegral_ofReal` é usado com essas hipóteses, e a igualdade real precedente termina a prova. Não aparece `ENNReal.toReal`; em particular, não se identifica infinito a zero para justificar Plancherel. Os dois lados da identidade ENNReal são finitos sob as hipóteses L¹/L² dadas, embora o enunciado use o tipo estendido.

5. **Convenção que a próxima aplicação deve transportar.** A instância Fourier de Mathlib examinada usa `fourierChar (-⟨t,ξ⟩)`, com `fourierChar(x)=exp(2π i x)`: neste domínio, a fase é exp(−2π i tξ), com Lebesgue e isometria L² sem fator adicional. O estrato anterior da regular usa `characterPhase s t=exp(−i s t)`. Este módulo prova Plancherel na convenção Mathlib; não declara ainda a mudança de variável entre ξ e s, nem a identidade normalizada com `(2π)⁻¹` para o peso. Essa conexão e sua finitude serão examinadas na fonte seguinte quando final. Não é um defeito destes oito teoremas, que não afirmam tal conexão.

### Evidência, hashes e limite

Fonte final (104 linhas), SHA-256 **`49c8e43b55cbd48b3a2c9f1bdfa01a31af9566e7a3cccbb4eed119fc1c750f13`**. Log do autor lido e congelado: [FourierL1L2_20260912_033331_168906.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/logs/FourierL1L2_20260912_033331_168906.json>), rc0 com fonte inalterada durante sua compilação e hash correspondente.

| Processo próprio | rc | Tempo | Alvos |
|---|---:|---:|---:|
| FourierL1L2.lean | 0 | 16.245 s | 8 |
| FourierL1L2FullAudit.lean | 0 | 14.84 s | 8 |

`.olean` próprio do módulo: `ae4d1296abfe671e92d88586345f0337152ad0dfed7fdeae40a40ab81938991b`, igual ao binário dev final do autor. `.olean` do auditor: `8bc5953358177f528bb1a8f4b2e7c0a1a07e9aa33132a78245c11dcb5dba0bb9`. Snapshot próprio com **350 pares de fonte/binário de dependências do projeto**, herdados e conferidos por hash, acrescentando a aproximação regular recompilada no estrato 1. Não houve recompilação dos módulos anteriores ou dos pacotes. O build e `LEAN_PATH` são próprios, com pacotes somente leitura; fontes e saídas novas estão exclusivamente em `revisao/`.

Evidências: [manifesto e fontes congeladas](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/fourier_l1l2_independent_20260912_033536_591616/manifest.json>); [resultados dos dois processos próprios](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/fourier_l1l2_independent_20260912_033536_591616/compilation.json>); [oito tipos e axiomas](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/fourier_l1l2_independent_20260912_033536_591616/logs/FourierL1L2FullAudit.stdout.txt>). Referências primárias da Mathlib foram congeladas e tiveram hashes lidos: `Analysis/Fourier/LpSpace.lean` (extensão isométrica, norma e compatibilidade distribucional), `Analysis/Distribution/AEEqOfIntegralContDiff.lean` (unicidade), `Analysis/Fourier/FourierTransform.lean`, `Analysis/Complex/Circle.lean` e `Analysis/Distribution/TemperedDistribution.lean`. Seus hashes constam no recibo deste estrato.

[OPEN] Aplicação à expressão modulada da regular, mudança de normalização, finitude do peso e construção do ideal adequado denso na álgebra. Este resultado analítico isolado não certifica semifinitude, F=base, traço ou alteração de gate. O parecer conjunto aguarda as próximas fontes finais e a integração; nenhum teste do autor, recorder, monólito ou pacote foi executado/reconstruído nesta revisão. Os pareceres custodiados anteriores permanecem byte a byte iguais.


## Estrato 3 — RegularFiniteWeight

2026-09-12T03:45:29-03:00. **Revisão dos dez alvos finais concluída, sem achados P0, P1 ou P2.** Módulo e auditor próprio passaram rc0, todos os tipos conferidos e axiomas exatamente no trio. Este adendo encerra, para a família regular especificada, a mudança de normalização e a identidade finita que estavam pendentes no estrato 2. O parecer conjunto continua aguardando `DualSemifiniteIdeal` final e as evidências integradas; esse arquivo em autoria não foi lido ou certificado.

### Conteúdo matemático conferido

**Corte Ioc e integrabilidade**, [RegularFiniteWeight.lean:17](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularFiniteWeight.lean:17>)–47. A função recortada é exatamente 1_(0,h](t)Λ_t v, na mesma realização e com o mesmo P. A continuidade forte fornece mensurabilidade forte; a norma coincide com o indicador da constante ‖v‖. A medida de Ioc é finita, provando `MemLp` para todo p:ENNReal, inclusive os casos L¹ e L² usados adiante. A integrabilidade L¹ é obtida expressamente. Para h>0, a integral do quadrado da norma é h‖v‖². O `toReal` da linha 47 só avalia a medida **finita** `ENNReal.ofReal h`; não é uma conversão do valor ∞ de uma forma. Ioc evita discrepância de extremos com `intervalIntegral.integral_of_le`. As fórmulas Fourier seguintes exigem h>0: o fato de o corte Ioc ser vazio quando h≤0 não foi ocultado nem usado para provar uma média orientada de sinal contrário.

**Fase, variável e fator 2π**, [RegularFiniteWeight.lean:49](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularFiniteWeight.lean:49>)–67. A igualdade provada é θ_s(X_h)v=h⁻¹(𝓕f_h,v)(s/(2π)), X_h=`regularAverage P h`. A expansão Mathlib usa exp(−2πitξ); a substituição ξ=s/(2π) dá precisamente exp(−ist), com coerções reais/complexas conferidas. Indicador e integral sobre Ioc são tratados explicitamente. Assim a ponte entre as duas convenções é agora um teorema para esta órbita recortada, preservando os mesmos operadores e vetores.

**Plancherel com integrabilidade prévia**, [RegularFiniteWeight.lean:69](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularFiniteWeight.lean:69>)–94. L¹∩L² do corte permite aplicar o módulo Fourier já recompilado. O quadrado da norma da transformada é integrável; `Integrable.comp_div` usa 2π≠0 e o fator constante |h⁻¹|² preserva integrabilidade. `Measure.integral_comp_div` fornece o jacobiano |2π|, que é 2π. Plancherel e ∫‖f_h,v‖²=h‖v‖² dão, na direção correta,

    ∫ ds ‖θ_s(X_h)v‖² = (2π) h⁻¹ ‖v‖².

Portanto não foi trocado o jacobiano por seu inverso, nem aceita uma integral não integrável pelo valor convencional da integral de Bochner. A cota e a igualdade usam norma vetorial no Hilbert regular; não assumem integrabilidade em norma de B(H).

**Quadrado correto e energia positiva**, [RegularFiniteWeight.lean:95](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularFiniteWeight.lean:95>)–119. O integrando de X*X é identificado a `ofReal ‖θ_s(X)v‖²` usando θ multiplicativa e compatível com adjuntos, depois ⟨v,B*Bv⟩=⟨Bv,Bv⟩. Não há troca entre X*X e XX*. A conversão da integral real para ENNReal recebe explicitamente a integrabilidade recém-provada e `sq_nonneg`. O fator fixado `(2π)⁻¹` de `dualHaarFactor` cancela o 2π calculado acima, resultando no enunciado exato:

    ∀ P, ∀ h>0, ∀ v,
      q_(X_h* X_h)(v) = ENNReal.ofReal (h⁻¹ * ‖v‖²).

**Uniformidade e significado da finitude**, [RegularFiniteWeight.lean:108](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularFiniteWeight.lean:108>)–125. A constante C=1/h é finita, não negativa e independente de v para cada h>0 fixo. A igualdade fornece uma forma limitada em todo H, mais que uma afirmação de finitude em um vetor ou pertença a `quadDomain`. O último lema deriva a desigualdade estrita com ⊤. A expressão à direita é a forma quadrática limitada do operador h⁻¹I; ela **não** é h⁻¹·q_I, cujo setor infinito continua preservado pelas etapas anteriores. A constante 1/h não é uniforme quando h→0. Nenhuma cota uniforme dos pesos nessa aproximação foi afirmada.

Pela pertinência de X_h a N já provada no estrato 1, X_h*X_h é uma entrada positiva da mesma álgebra. O módulo atual certifica sua avaliação q e a cota uniforme nos vetores; a definição do ideal de entradas de peso finito e sua densidade ainda serão objeto do próximo módulo. Esta distinção delimita o avanço sem reduzir o resultado a mera finitude vetorial.

### Processos e proveniência

Fonte final (138 linhas), SHA-256 **`924dc63843fc622089d36d8dc44269150b71fd932d7af31dc213778a38e2faa5`**. Log do autor lido e congelado: [RegularFiniteWeight_20260912_034024_228200.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/logs/RegularFiniteWeight_20260912_034024_228200.json>), rc0/fonte inalterada, com hash correspondente.

| Processo próprio | rc | Tempo | Alvos |
|---|---:|---:|---:|
| RegularFiniteWeight.lean | 0 | 31.625 s | 10 |
| RegularFiniteWeightFullAudit.lean | 0 | 26.533 s | 10 |

`.olean` próprio do módulo: `fb658885733086bb19dd961af678e9efb1cdfa9f8b76baec76a2ecb3a6b098ba`, igual ao dev final do autor. `.olean` do auditor: `ca1dd8ebe6040bfbb145c5f8551c5aab2d9ae4fa0e732280f25e46892b50569f`. Os dez alvos foram auditados nominalmente por `#check` com universos e `#print axioms`, sem omissões. No conjunto dos três estratos, **29 alvos distintos de fontes novas e seis processos próprios rc0**; não são contagens de integração ou de testes Python.

Snapshot: **351 pares fonte/binário de dependências do projeto** herdados e conferidos por hash; agora inclui FourierL1L2 recompilado pelo revisor. Mesma ferramenta fixada e `LEAN_PATH` próprio, pacotes em leitura, sem rebuild da biblioteca ou dos módulos anteriores. Evidências: [manifesto](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/regular_finite_weight_independent_20260912_034212_433603/manifest.json>); [compilação e auditor](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/regular_finite_weight_independent_20260912_034212_433603/compilation.json>); [dez tipos e axiomas](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/regular_finite_weight_independent_20260912_034212_433603/logs/RegularFiniteWeightFullAudit.stdout.txt>). As referências Mathlib de Fourier, mudança de variável Haar em ℝ e indicador Lp foram lidas e congeladas, com hashes no recibo deste estrato.

[OPEN] Construção e densidade do ideal semifinito, integração/minuta da etapa, F=base original, correspondência geral espectral/predual, traço, Three Locks e efeitos sobre gate. Não foi conferida nem reivindicada aqui a conclusão de `DualSemifiniteIdeal`. Pareceres anteriores custodiados e os bytes dos dois estratos precedentes foram preservados; nenhum recorder, monólito, memória ou teste do autor foi executado/alterado pelo revisor.


## Leitura documental preliminar — minuta do ideal

2026-09-12T03:48:22-03:00. [REAL — inspeção estática, sem execução.] Lidas integralmente `MINUTA_IDEAL_SEMIFINITO.md`, `record_semifinite_ideal_progress.py` e `verify_semifinite_ideal_custody.py`; cópias e hashes preservados em [documentary_preview_20260912_034741_173063](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/regular_finite_weight_independent_20260912_034212_433603/documentary_preview_20260912_034741_173063>).

A minuta (SHA **`c58da6a3729c372bb32f202f5656e2e48814051aaef24a54bf975b7de620d458`**) descreve corretamente os três módulos já examinados: continuidade/FTC vetoriais, igualdade ae da Fourier L¹∩L², corte Ioc e coeficiente uniforme nos vetores 1/h para h>0. As linhas 33–37 descrevem o quarto módulo ainda em compilação; **essa parte continua declarada pelo autor e não foi validada contra a fonte nesta leitura**. O mesmo limite vale para os campos de construção/densidade do ideal projetados no recorder.

O alcance documental está delimitado: linhas 56–62 mantêm abertas a realização dos valores finitos como operadores limitados de F, o peso operatorial padrão, F=base, a correspondência espectral/predual e o traço. O recorder fixa `finite_values_as_bounded_operators_in_F=false`, `operator_valued_weight_semifinite=false`, `canonical_trace_constructed=false` e `full_goal_complete=false`. Não encontrei sobreafirmação concreta nessa distinção; seu registro como resultado concluído depende da revisão final do módulo faltante e da integração.

Pelo AST, são 16 superfícies previstas. A implementação de append preserva o prefixo de bytes, cria backup imediato de bytes e escreve por temporário verificado antes de substituir. O verifier compara hashes e prefixos dos backups após o registro. Isso é exame do mecanismo, **não execução ou certificação dos 16 backups desta etapa**. Recorder SHA `ffc1ed7bace930cfa7511770e9cc41fc5c338202eb7e33640ebdd6866304a7ca`; verifier SHA `262a0611e604b3067a4353d9a41172e05fb7482cb8487e834e493340b0a6208a`.

A checagem histórica do inventário é coerente: compara tanto seu hash ao `runtime_io_inventory_sha256` da custódia anterior quanto o hash de sua fonte ao `runtime_io_inventory_source_sha256`. O inventário pertence a `c712532dc079b832d9eb1ecc26ea50f2d49aa2c387afa435cc777eb302e96e09`, enquanto a cópia da custódia imediatamente anterior é `a6073b7ed0a8226c794dd822c3803635c2b456807de72010d5253af7f12b1d74`. Os dois hashes não foram confundidos. Permanece `NOT_RUNTIME_CLEARANCE`; nenhuma liberação de execução da cópia atual foi inferida.

Esta leitura não acrescenta alvos Lean, testes ou registros integrados. O parecer conjunto continua pendente. Nenhum recorder, verifier, gerador de registro ou monólito foi executado pelo revisor.


## Estrato 4 — DualSemifiniteIdeal e auditoria conjunta das fontes

2026-09-12T03:52:49-03:00. **Os quatro módulos foram examinados e recompilados; a conclusão conjunta ainda aguarda a integração.** Nenhum achado P0 ou P1 nas provas finais. Há uma ressalva documental P2 localizada no comentário indicado abaixo. `DualSemifiniteIdeal` e auditor cumulativo passaram rc0; todos os **40 alvos das quatro fontes** foram conferidos nominalmente, com tipos e axiomas exatamente no trio.

### Achado documental P2

[DualSemifiniteIdeal.lean:15](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualSemifiniteIdeal.lean:15>)–16, fonte congelada SHA `6af7365befd3125fa1b8a9a03f26bcd96d723659d035d2b52e73a8ced09b70b3`: a descrição “finiteness of the output form as a bounded operator” pode sugerir que a realização por operador já integra o contrato. O tipo seguinte só afirma **∃C:NNReal, ∀v, q_(A*A)(v)≤C·ofReal(‖v‖²)**; não constrói o operador limitado de F. Recomenda-se “as a uniformly bounded quadratic form”. É precisão de estatuto no comentário, sem falha do enunciado ou de sua prova. A minuta/recorder já mantêm expressamente aberta a realização dos valores finitos por operadores de F. Ressalva comunicada ao autor; eventual correção deve ser registrada ao lado, preservando este snapshot.

### Provas e composição conferidas

**Uma constante para todos os vetores**, [DualSemifiniteIdeal.lean:17](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualSemifiniteIdeal.lean:17>)–19. `HasFiniteDualSquare` quantifica C antes de v, com C:NNReal finito. É uma condição sobre a família inteira q_(A*A); não uma escolha de cota dependente de cada vetor, nem apenas domínio finito denso. O predicado é definido inicialmente para operadores limitados arbitrários do Hilbert regular. A pertinência a N é acrescentada efetivamente no submódulo adiante.

**Multiplicação à esquerda por operador arbitrário**, [DualSemifiniteIdeal.lean:21](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualSemifiniteIdeal.lean:21>)–60. A desigualdade q_((BA)*(BA))(v)≤ofReal(‖B‖²)q_(A*A)(v) passa pelo integrando de normas quadradas: θ_s(BA)v=θ_s(B)θ_s(A)v, e ‖θ_s(B)‖≤‖B‖ vem de `dualIntegralFamily B`, cuja cota é demonstrada pela isometria da conjugação dual. O quadrado preserva a desigualdade de normas não negativas; `lintegral_mono` e a extração do fator constante usam integrando mensurável. O fator Haar está em ambos os lados. A prova não exige B∈F, B positivo ou B de peso finito, e continua correta quando uma avaliação é ∞ ou B=0. Para uma entrada finita, a nova constante é ‖B‖₊²C, ainda finita e independente de v.

**Soma e escala complexa**, [DualSemifiniteIdeal.lean:62](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualSemifiniteIdeal.lean:62>)–93. A diferença entre 2(A*A+B*B) e (A+B)*(A+B) é exatamente (A−B)*(A−B), positiva na ordem de operadores. A passagem pela forma q usa monotonicidade, homogeneidade por 2≥0 e aditividade aplicada expressamente aos dois quadrados positivos. A constante escolhida é 2(C_A+C_B); não se presume positividade de A ou de B. Para c∈ℂ, cA=(cI)A reduz o caso à multiplicação à esquerda, cobrindo zero, negativos e fases complexas. Com o caso zero, isso fornece os campos reais do submódulo complexo.

**Ideal dentro da mesma N**, [DualSemifiniteIdeal.lean:96](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualSemifiniteIdeal.lean:96>)–105. `finiteDualLeftIdeal P` é um `Submodule ℂ (regularCoreAlgebra P).toStarSubalgebra`; seu portador exige `HasFiniteDualSquare A.val`. A pertinência ao core é estrutural pelo subtipo, não um nome. A estabilidade B*A é um teorema adicional para todos A,B no mesmo N. O pacote apresenta um submódulo com fechamento por multiplicação à esquerda; não afirma ser ideal bilateral, fechado em norma ou uma instância nova de outra estrutura de ideal.

**Aproximação forte efetiva**, [DualSemifiniteIdeal.lean:107](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualSemifiniteIdeal.lean:107>)–129. O cálculo do estrato 3 constrói o certificado de X_h com C=1/h para h>0. Para cada A∈N, a mesma família A X_h tem certificado finito para h>0, pertence a N para todo h e satisfaz A X_h v→A v para **todo v**, ao longo de `𝓝[>]0`. A restrição do filtro perfurado é feita com a inclusão h>0⇒h≠0, na direção correta de `mono_left`. A vizinhança direita de zero em ℝ não é vazia; não há uma hipótese de filtro vazio ou um limite fornecido como premissa. O enunciado entrega explicitamente o pertencimento dos aproximantes e a convergência vetor a vetor, mesmo sem escrever uma igualdade de fecho em um tipo com topologia SOT empacotada. Não se assume convergência em norma de operadores.

A família aproximante tem cota de norma operacional herdada de ‖X_h‖≤1, mas a cota de suas formas pode crescer como ‖A‖²/h. Assim não se deduz finitude do peso de I pela passagem ao limite; o setor q_I(v)=∞ para v≠0 não foi suprimido. A conclusão é um ideal de quadrados com formas uniformemente limitadas nos vetores, fortemente aproximante em N.

### Evidência e atualização documental

Fonte final de 143 linhas: SHA **`6af7365befd3125fa1b8a9a03f26bcd96d723659d035d2b52e73a8ced09b70b3`**. Log do autor conferido e congelado: [DualSemifiniteIdeal_20260912_034726_500111.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/logs/DualSemifiniteIdeal_20260912_034726_500111.json>), rc0 e fonte inalterada.

| Processo próprio deste estrato | rc | Tempo | Alvos de axiomas |
|---|---:|---:|---:|
| DualSemifiniteIdeal.lean | 0 | 35.063 s | 11 |
| RegularSemifiniteRouteFullAudit.lean | 0 | 32.682 s | 40 |

`.olean` próprio do módulo: `6a242f29df8816cf7e741cb043f6c24f88fb9e844fc60f90d3bce25a4c1f26df`. `.olean` do auditor: `a2d3e7ce10bb0dba21d53f22bf2364df27d84830b9ca377b09fb5f4759e6b92b`. O primeiro coincide com o binário dev final do autor. O auditor inclui os 11 alvos deste módulo e os 29 anteriores, incluindo o namespace `TGLV350.Fourier` correto dos oito alvos analíticos. No total, foram oito processos próprios rc0: quatro fontes e quatro auditores. Não se recompilaram novamente as três fontes anteriores para o auditor final.

Snapshot com **352 pares fonte/binário de dependências do projeto**, herdados e conferidos por hash; inclui os três módulos precedentes recompilados nesta revisão. Ferramenta fixada, `LEAN_PATH` próprio e pacotes somente leitura. Evidências: [manifesto](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_semifinite_ideal_independent_20260912_034956_288489/manifest.json>); [compilação e auditor cumulativo](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_semifinite_ideal_independent_20260912_034956_288489/compilation.json>); [40 tipos e axiomas completos](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_semifinite_ideal_independent_20260912_034956_288489/logs/RegularSemifiniteRouteFullAudit.stdout.txt>).

As afirmações sobre o quarto módulo nas linhas 33–37 da minuta anteriormente congelada agora conferem com seus tipos e provas, com a ressalva P2 restrita ao comentário Lean. A descrição do ideal/densidade é adequada no alcance de formas uniformemente finitas. Semifinitude operatorial padrão, realização dos valores limitados em F, identificação F=base, correspondência geral espectral/predual, traço, Three Locks e runtime permanecem abertos. Integração, contagens finais e igualdade de AST/hashes deste lote ainda serão conferidas após o aviso do autor; não se encerra aqui o parecer conjunto.


## Conclusão FINAL conjunta — fontes, integração e minuta

2026-09-12T03:56:14-03:00. **Escopo de revisão concluído para os quatro módulos, 40 alvos, integração e documentação indicada.** Este adendo encerra as pendências de revisão/integração dos estratos anteriores, que permanecem registrados como histórico.

**Achados:** nenhum P0/P1 nem falha de prova identificada. Permanece **um P2 documental**, comunicado no estrato 4: `DualSemifiniteIdeal.lean:15–16` descreve a cota da forma “as a bounded operator”, embora o contrato ainda não construa o valor como operador de F. A mesma redação está na cópia integrada `TGLExt/V350DualSemifiniteIdeal.lean:15–16`. Recomenda-se dizer “uniformly bounded quadratic form”. O achado não invalida os tipos/provas recompilados e não implica ausência de uma cota uniforme: essa cota está efetivamente provada. A realização por operador deve conservar o estatuto aberto já adotado na minuta/recorder.

[REAL — processos próprios] **Quatro módulos + quatro auditores = oito processos rc0.** Auditor final cumulativo com `#check` e `#print axioms` dos **40 alvos**, todos exatamente no trio `propext`, `Classical.choice`, `Quot.sound`. Resultados detalhados: [RegularApproximation](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/regular_approximation_independent_20260912_032358_906563/compilation.json>); [FourierL1L2](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/fourier_l1l2_independent_20260912_033536_591616/compilation.json>); [RegularFiniteWeight](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/regular_finite_weight_independent_20260912_034212_433603/compilation.json>); [DualSemifiniteIdeal](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_semifinite_ideal_independent_20260912_034956_288489/compilation.json>). Não se recompilaram as dependências já congeladas nem a Mathlib. A herança consiste nos pares fonte/binário pinados e nos pacotes/compilador em leitura descritos nos manifestos; essa revisão não é um rebuild independente de toda a biblioteca.

O conteúdo conjunto verificado é: médias contrações X_h∈N na mesma representação regular, X_h→I fortemente; ponte entre Fourier integral e Fourier L² para L¹∩L²; mudança ξ=s/(2π) e igualdade q_(X_h*X_h)(v)=ofReal(h⁻¹‖v‖²) para h>0; submódulo de N com estabilidade por multiplicação à esquerda, definido por uma constante finita comum a todos os vetores; aproximação forte de cada A∈N por A X_h pertencente a esse domínio para h>0. O produto, os adjuntos, a positividade dos quadrados e os filtros são os especificados nas fontes. O resultado analítico fornece formas uniformemente limitadas nos vetores, sem declarar uma constante uniforme em h→0.

### Snapshot integrado efetivamente conferido

Cópia final SHA-256 **`d031ba6775ae6dc1317c60186288f8928c42d65907146c5d99624bf05382404e`**, lida de `um.py` como bytes e confrontada com `integration.json` e `gate_tests.json`. Original canônico e cópia-base relidos: `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`, ambos iguais ao `base_sha256` da integração. O monólito não foi executado/importado.

[REAL — inspeção dos processos do autor] **56 registros** em `integrated_compile.json`, todos rc0 e com SHA-256 atual da fonte e do `.olean` correspondente. São **50 registros anteriores conservados + quatro módulos novos + TGLExt/Audit recompilados pelo autor**. Os seis registros novos indicam fonte inalterada durante a compilação. **758 arquivos** foram extraídos por AST/literal_eval do dicionário Lean. Os quatro fontes dev coincidem com os integrados após somente a reescrita dos imports, e os textos integrados coincidem byte a byte com os embutidos:

| Módulo | SHA-256 dev recompilado pelo revisor | SHA-256 TGLExt/V350 integrado |
|---|---|---|
| RegularApproximation | `cf847f376210447912ca2d08644c06e66375a6f89e82cffe844a241f92c89414` | `d8e7830989e0ba3d71f0e8495f54414cedc12a9eac16b1bc0501f15342b8bb44` |
| FourierL1L2 | `49c8e43b55cbd48b3a2c9f1bdfa01a31af9566e7a3cccbb4eed119fc1c750f13` | `49c8e43b55cbd48b3a2c9f1bdfa01a31af9566e7a3cccbb4eed119fc1c750f13` |
| RegularFiniteWeight | `924dc63843fc622089d36d8dc44269150b71fd932d7af31dc213778a38e2faa5` | `39e417e41adf90a2d575b6a93f8a35ccd2d816a445097745fd3c540ab240baf6` |
| DualSemifiniteIdeal | `6af7365befd3125fa1b8a9a03f26bcd96d723659d035d2b52e73a8ced09b70b3` | `1e5adb9ef248136bab5c0a6f9ae2cce90ded5d19d39c729ed6a954da9f953251` |

Os diffs dos agregadores contêm somente os quatro imports e os 40 alvos novos de auditoria pertinentes. `FourierL1L2` conserva seu namespace `TGLV350.Fourier`; os outros usam `TGLV350.Regular`. Não houve exclusão de arquivo embutido; além dos quatro acréscimos, somente as duas raízes antigas mudaram.

O stdout integrado do Audit contém **6163 declarações distintas**, sem axiomas fora do trio; seu mapa é igual ao de `kernel_incremental_evidence.json`. Os 40 novos nomes e seus axiomas coincidem com o auditor próprio. O relatório `gate_tests.json` registra **61/61 controles aprovados**. Essas 56 compilações/61 verificações são evidência de **execução pelo autor**, conferida por fontes, logs e hashes; não são processos que executei novamente.

Contra a custódia do peso fixo, snapshot `a6073b7ed0a8226c794dd822c3803635c2b456807de72010d5253af7f12b1d74`, a AST Python fora de `_EMBEDDED_KERNEL_FILES` é idêntica e `gate_extension.py` é byte a byte idêntico. O novo controle confere a presença dos alvos e as seis flags abertas falsas. Os registros mantêm `legacy_gate_changed=false`, `full_plan_complete=false` e `full_monolithic_runtime_run=false`. Isso não constitui teste integral de runtime ou nova prova física.

Evidências congeladas e resultados da inspeção: [verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_semifinite_ideal_independent_20260912_034956_288489/final_integrated_20260912_035324_363904/verification.json>); [supplemental_verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_semifinite_ideal_independent_20260912_034956_288489/final_integrated_20260912_035324_363904/supplemental_verification.json>); [final_scope_verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_semifinite_ideal_independent_20260912_034956_288489/final_integrated_20260912_035324_363904/final_scope_verification.json>). O frescor de dependências dos processos integrados é relatado pelo procedimento do autor; minha inspeção acrescenta o confronto dos hashes atuais, a comparação ao estrato anterior e a recompilação própria dos quatro fontes dev.

### Minuta final e limite restante

A versão final de `MINUTA_IDEAL_SEMIFINITO.md` permaneceu igual à examinada: **3485 bytes**, SHA **`c58da6a3729c372bb32f202f5656e2e48814051aaef24a54bf975b7de620d458`**. Recorder SHA `ffc1ed7bace930cfa7511770e9cc41fc5c338202eb7e33640ebdd6866304a7ca`; verifier SHA `262a0611e604b3067a4353d9a41172e05fb7482cb8487e834e493340b0a6208a`. As descrições do quarto módulo, antes condicionadas ao exame da fonte final, agora foram confrontadas com seus tipos e provas. Não foi identificada sobreafirmação adicional nessa minuta.

O registro previsto de 16 superfícies e seus backups foi examinado estaticamente; não executei recorder, verifier ou gerador. A custódia desta nova etapa será ato posterior do autor. O inventário de I/O continua com hash `34133956b6a47012805003adfae734e7439b27e1f611466829af624b1857d89c`, vinculado à fonte histórica `c712532dc079b832d9eb1ecc26ea50f2d49aa2c387afa435cc777eb302e96e09` pelos campos históricos corretos da custódia anterior. Permanece `NOT_RUNTIME_CLEARANCE`, sem reutilização como auditoria de execução da cópia atual.

**[OPEN]** Realização dos valores finitos como operadores limitados de F no contrato adotado; semifinitude operatorial padrão; F=base original; correspondência espectral/predual geral; estado modular, gerador, perturbação e traço canônico; Three Locks/H1–H3 e compatibilidade física; contrato ampliado do gate; runtime integral isolado. Esses limites não são falhas das provas aqui reivindicadas. A existência de um ideal de formas uniformemente finitas e fortemente aproximante é o avanço certificado; não se promove isso a traço ou a quitação de flag maior.

Nenhuma análise específica de prova/tipo/integração/documentação ficou pendente no escopo recebido. O P2 documental permanece uma recomendação localizada ao autor. Todos os pareceres custodiados anteriores e os prefixos de bytes dos estratos deste parecer foram preservados; originais, implementação, logs e memórias não foram alterados pelo revisor. Não houve aprovação de QG, runtime, publicação ou transposição canônica.


## Adendo FINAL — 2026-09-12T04:06:39-03:00 — errata documental e encerramento do P2

**[REAL — comparação literal e inspeção de evidências] P2 RESOLVIDO.** A correção em `kernel/TGLV350/DualSemifiniteIdeal.lean:15–17` distingue corretamente a cota uniforme da forma quadrática da obrigação de realizá-la por um operador limitado pertencente à álgebra fixa. O comentário agora diz:

> A single bound for all vectors: the output is a uniformly bounded quadratic form, not just finite on a chosen vector domain. Realization by a bounded operator in the fixed algebra is a separate obligation.

Todos os bytes anteriores e posteriores a esse único comentário são idênticos aos da fonte congelada recompilada independentemente. Não houve mudança de definição, hipótese, tipo, prova, import ou alvo de auditoria. O diagnóstico P2 e os resultados do estrato anterior permanecem integralmente no prefixo deste parecer; este adendo encerra a pendência documental, sem apagar a constatação histórica. Não há P0–P2 pendente no escopo delimitado.

### Proveniência da errata

- Fonte dev anterior, efetivamente recompilada pelo revisor: `6af7365befd3125fa1b8a9a03f26bcd96d723659d035d2b52e73a8ced09b70b3`.
- Fonte dev corrigida, congelada e relida: **`f1c93aa724c9eb82df3d1ec74d040cdab6a78f0b57f51b224f60656669128da3`**.
- Fonte integrada `TGLExt/V350DualSemifiniteIdeal.lean`: **`63c88763eaa1c837ed0a28057d044a7627e57f993f4fcc4c7bddf44dcea07cbe`**; coincide com dev mediante somente a reescrita dos imports, e com o texto embutido byte a byte.
- `.olean` dev atual: `6c4981c0c7f74504c87ee1c91f79995e7138e355d8b4f8cc225e4efd4b797165`, confrontado com `logs/DualSemifiniteIdeal_20260912_035730_251164.json`: rc0, fonte inalterada durante a compilação e 11 alvos com axiomas somente no trio.

**Distinção de execução:** as quatro recompilações próprias e os quatro auditores próprios anteriores, com os 40 alvos do pacote, continuam sendo a evidência independente dos corpos Lean. Para esta alteração exclusiva de comentário, fiz comparação literal, inspeção dos logs do autor, leitura dos binários para hashes e análise estática da integração; **não recompilei independentemente a nova fonte com comentário corrigido e não executei novos testes**. O registro antigo de fonte inalterada refere-se àquela compilação anterior, não ao hash posterior à errata.

### Snapshot final após a correção

SHA-256 atual de `um.py`, lido de seus bytes e igual aos campos de `integration.json` e `gate_tests.json`: **`8140d4b75c8a0da8b4517635fd41db17cb8a8289b1671bb04fe5a5ddb480867b`**. O snapshot anterior `d031ba6775ae6dc1317c60186288f8928c42d65907146c5d99624bf05382404e` fica preservado como estrato histórico.

[REAL — inspeção de execuções do autor] `integrated_compile.json` contém **56 registros rc0**, todos confrontados com os hashes atuais de fonte e `.olean`: **53 registros conservados**, com os mesmos hashes e timestamps anteriores, e os três registros recompilados abaixo. Os três registram fonte inalterada durante a compilação.

| Registro recompilado pelo autor | Timestamp do log | SHA-256 `.olean` lido |
|---|---|---|
| `TGLExt/V350DualSemifiniteIdeal.lean` | `20260912_035826_685273` | `a17f870959c960c5ad2e1e2315734af186af4d593c0ff8b1b9437fa71aae2f19` |
| `TGLExt.lean` | `20260912_035857_703359` | `79cf096d4f4799fbd6df3fcfd3880bed4448ab493cef70cf70561847b531477b` |
| `TGL/Audit.lean` | `20260912_035925_107007` | `d90423cf8c6f568f6c7e1cb2bce7b0ee60ca3fece42bfcdde2c87600409242a8` |

Permanecem **758 arquivos embutidos**: nenhum acréscimo ou remoção; a única alteração textual em relação ao snapshot anterior está no comentário de `V350DualSemifiniteIdeal.lean`. As fontes dos agregadores permanecem iguais. Os outros três módulos dev permanecem byte a byte iguais aos respectivos snapshots revisados. A AST Python externa ao dicionário embutido, `gate_extension.py` e o script de testes permanecem iguais ao estrato anterior.

O stdout atual de Audit contém **6163 declarações distintas**, com o mesmo mapa de axiomas anterior, igual ao de `kernel_incremental_evidence.json`, sem axiomas fora de `propext`, `Classical.choice`, `Quot.sound`. Os 40 alvos da auditoria própria continuam com os mesmos axiomas. O `gate_tests.json` atual registra **61/61 controles aprovados** e referencia o SHA atual acima. Essas compilações e esses controles foram executados pelo autor; o revisor conferiu seus registros. O frescor de dependências do rebuild é evidência relatada pelo procedimento do autor, além do confronto independente dos hashes aqui registrado.

As seis flags abertas permanecem falsas, assim como `legacy_gate_changed`, `full_plan_complete` e `full_monolithic_runtime_run`. Não executei nem importei o monólito.

### Documentação, limite e custódia do parecer

A minuta segue idêntica à examinada: `MINUTA_IDEAL_SEMIFINITO.md`, SHA **`c58da6a3729c372bb32f202f5656e2e48814051aaef24a54bf975b7de620d458`**. Recorder e verifier também permanecem idênticos aos snapshots já examinados; nenhum foi executado pelo revisor. Mantém-se o estatuto histórico do inventário de I/O, sem clearance de runtime da cópia atual.

O resultado matemático revisado continua sendo a aproximação forte da identidade, a ligação Fourier/Plancherel com o fator 2π, a avaliação uniforme dos quadrados das médias para h>0 e o ideal à esquerda fortemente aproximante de formas uniformemente finitas. **[OPEN, neste pacote]** Realização dos valores finitos como operadores limitados em F, semifinitude operatorial padrão, identificação F=base, correspondência geral espectral/predual, traço, Three Locks/H1–H3, física e runtime integral. A correção documental não resolve essas obrigações. `BoundedDualValues` não foi lido, recompilado ou incluído no parecer, e está ausente da integração inspecionada.

Evidência final: [verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_semifinite_ideal_independent_20260912_034956_288489/erratum_final_20260912_040455_412019/verification.json>), com fontes, registros e logs congelados na mesma pasta. A comparação literal inicial permanece em `dual_semifinite_ideal_independent_20260912_034956_288489/comment_erratum_20260912_035824_337251`.

Backup imediato deste parecer antes do adendo: `REVIEW_REGULAR_SEMIFINITE_ROUTE.md.bak_20260912_040639_916330`, **44466 bytes**, SHA `7aa52e64828d8cbd003661cbddcee6dbc709c6d4e5e8d4ae2823f0efdaefcc00`; o novo arquivo preserva exatamente esse prefixo. Os pareceres custodiados anteriores foram conferidos e permanecem intocados. Escrita exclusivamente em `revisao/`; nenhuma alteração pelo revisor em fontes do autor, originais, logs, integração ou memórias. **Revisão delimitada encerrada; P2 documental resolvido e nenhuma análise deste escopo pendente.**
