# Revisão independente — cortes da ação dual e avaliação integral ENNReal

Data: 11/09/2026. Bancada: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911`.

**Parecer delimitado [REAL]: nenhum defeito substantivo bloqueante encontrado nas quatro fontes estabilizadas, nos tipos e nas composições examinadas.** Os três módulos inicialmente autorizados foram recompilados independentemente. `DualWeightExhaustion` foi recompilado posteriormente, após o aviso de estabilidade e a ampliação expressa do escopo, em adendo separado. As quatro recompilações terminaram com exit 0.

A auditoria própria cobriu **44 declarações escritas e seis declarações geradas por `Family`, totalizando 50**, sem axiomas além de `propext`, `Classical.choice` e `Quot.sound`. Três conferências adicionais de identidade/tipagem também passaram.

O resultado é uma construção de **operadores de corte por integrais vetoriais**, com positividade e monotonicidade dos cortes positivos, e de **avaliações escalares estendidas em ENNReal**, incluindo sua exaustão por cortes. Não é construção do cone ampliado da base, de um peso dual canônico ou de um traço. O parecer não atribui esses resultados a flags de core, canto ou testemunha completa.

## 1. Evidência e achados priorizados

**P0/P1/P2 — nenhum defeito concreto encontrado no incremento delimitado.** Em particular, não encontrei integração Bochner indevida na norma de B(H), integrabilidade assumida implicitamente, troca do bicomutante, uso da aditividade de `ENNReal.ofReal` sem positividade, perda do fator constante, sinal incompatível na composição da ação, ou substituição de um supremo escalar infinito por um operador limitado.

Os seguintes limites são parte do enunciado e **não são classificados como bugs**:

- Os cortes positivos exigem `R ≥ 0` e `A ≥ 0`. A monotonicidade em raio exige também `R ≤ S`. A família integral genérica exige continuidade forte e uma cota global de norma explicitamente fornecida.
- A avaliação ENNReal é definida em todo operador `A`, mas as leis de aditividade e de identificação com a avaliação do corte têm hipóteses de positividade. Não foi provada uma aplicação linear sobre todos os operadores.
- O fator `(2π)⁻¹` é uma constante escolhida e positiva. O vínculo dessa escolha com uma convenção de Fourier/Plancherel não é um teorema Lean deste pacote.
- A exaustão vive em ENNReal para cada vetor. Não produz um elemento do cone ampliado, um supremo limitado em B(H), semifinitude ou um traço.

**Modalidades efetivamente realizadas:** inspeção semântica das fontes e dos tipos impressos; recompilação independente das quatro fontes; auditoria própria dos 50 nomes; três conferências próprias de tipos; inspeção estática e conferência de hashes da integração final do autor. As raízes integradas e os 48 controles Python não foram reexecutados por este revisor nesta etapa.

## 2. `StrongOperatorIntegral`: integração em vetores e mesmo bicomutante

[StrongOperatorIntegral.lean:15](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/StrongOperatorIntegral.lean:15>) fornece `op : ℝ → (H →L[ℂ] H)`, continuidade de `t ↦ op t v` para cada vetor e `‖op t‖ ≤ bound`, com `bound ≥ 0`. Não contém hipótese de continuidade em norma de operadores nem uma hipótese de integrabilidade Bochner com valores em B(H).

[StrongOperatorIntegral.lean:22](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/StrongOperatorIntegral.lean:22>) tem valor em **H**: `∫ t in a..b, F.op t v`. A continuidade vetorial dá `IntervalIntegrable` em cada intervalo compacto, utilizada explicitamente na aditividade e na passagem de aplicações lineares pela integral. Assim, a construção não depende da convenção de integral nula para um integrando não integrável. A linearidade complexa e a estimativa

`‖vectorIntegral F a b v‖ ≤ (F.bound * |b-a|) * ‖v‖`

permitem a construção efetiva de `H →L[ℂ] H` por `mkContinuous` em [StrongOperatorIntegral.lean:45](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/StrongOperatorIntegral.lean:45>). A estimativa de norma do operador é comprovada em [StrongOperatorIntegral.lean:54](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/StrongOperatorIntegral.lean:54>). A integral pode ser orientada para quaisquer `a,b`; a positividade só é afirmada quando `a ≤ b`.

[StrongOperatorIntegral.lean:59](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/StrongOperatorIntegral.lean:59>) move um **operador fixo limitado B** através da integral vetorial. Se B comuta com todos os integrandos, comuta com o operador resultante. [StrongOperatorIntegral.lean:70](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/StrongOperatorIntegral.lean:70>) aplica esse fato a cada elemento do comutante da mesma `VonNeumannAlgebra N` e usa `N'' = N`. A orientação da igualdade de comutação é ajustada por simetria, sem trocar N por um modelo isomorfo. Essa prova usa diretamente o bicomutante; não precisa construir somas de Riemann ou supor integral em norma de operadores.

As identidades de produtos internos em [StrongOperatorIntegral.lean:79](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/StrongOperatorIntegral.lean:79>), [StrongOperatorIntegral.lean:84](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/StrongOperatorIntegral.lean:84>) e [StrongOperatorIntegral.lean:91](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/StrongOperatorIntegral.lean:91>) respeitam a convenção complexa: linearidade na segunda entrada e conjugação na primeira. A prova de positividade em [StrongOperatorIntegral.lean:100](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/StrongOperatorIntegral.lean:100>) verifica simetria e não negatividade da forma quadrática. A monotonicidade em [StrongOperatorIntegral.lean:120](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/StrongOperatorIntegral.lean:120>) assume `c ≤ a ≤ b ≤ d` e positividade de todos os integrandos; conclui a ordem de Loewner entre os dois operadores integrados. Não confunde ordem de operadores com comparação de normas.

## 3. `DualWeightCuts`: a órbita dual efetivamente construída

[DualWeightCuts.lean:14](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightCuts.lean:14>) usa exatamente `dualAmbient s A`, com continuidade forte já fornecida para todos os vetores e cota `‖A‖` obtida da isometria do automorfismo unitário. O operador é aquele do espaço `RegularHilbert H = Lp H 2 (volume : Measure ℝ)`; para a torre, `H = TowerHilbert P`.

[DualWeightCuts.lean:26](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightCuts.lean:26>) define `T_R(A)` pelo intervalo orientado `(-R)..R`. [DualWeightCuts.lean:34](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightCuts.lean:34>) prova `‖T_R(A)‖ ≤ ‖A‖ |2R|` para todo R. A positividade exige `R ≥ 0` e `A ≥ 0`, em [DualWeightCuts.lean:46](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightCuts.lean:46>). A monotonicidade provada em [DualWeightCuts.lean:52](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightCuts.lean:52>) é **em relação ao raio**: `0 ≤ R ≤ S` implica `T_R(A) ≤ T_S(A)` para A positivo. Não a relato como um teorema separado de monotonicidade em A, que não foi escrito nesse módulo.

[DualWeightCuts.lean:59](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightCuts.lean:59>) vale para todo `A ∈ regularCoreAlgebra P`, não apenas para os geradores. O pertencimento dos integrandos é extraído de `(regularDualAction P s ⟨A,hA⟩).property`. A coerção dessa ação restrita coincide definicionalmente com `dualAmbient`; essa identidade foi ainda conferida em um exemplo próprio, com a integral inteira escrita usando `regularDualAction` no mesmo subtipo. O resultado permanece no mesmo bicomutante concreto.

[DualWeightCuts.lean:67](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightCuts.lean:67>) dá `T_R(fibre A) = (2R) • fibre A` porque a ação dual fixa essa amplificação. [DualWeightCuts.lean:77](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightCuts.lean:77>) especializa para a unidade. Essas igualdades conservam o comprimento do intervalo; não são médias divididas por `2R`. Elas também não dizem que todos os cortes de todo A pertencem à imagem da base: o pertencimento provado é à álgebra regular gerada.

## 4. `DualWeightForm`: constante, positividade, invariância e avaliação

**Normalização.** [DualWeightForm.lean:17](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightForm.lean:17>) é literalmente `(2 * Real.pi)⁻¹ : ℝ`; [DualWeightForm.lean:19](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightForm.lean:19>) prova positividade estrita. [DualWeightForm.lean:23](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightForm.lean:23>) multiplica o corte por essa constante fixa, não por um fator dependente de R. A passagem entre escalares reais e sua coerção complexa nas provas de positividade e pertencimento conserva o mesmo CLM. Uma conferência própria confirmou por `rfl` a fórmula com `(2π)⁻¹`.

O pacote prova positividade e pertencimento do corte normalizado em [DualWeightForm.lean:27](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightForm.lean:27>) e [DualWeightForm.lean:36](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightForm.lean:36>). A monotonicidade dos cortes normalizados segue matematicamente da positividade do escalar e da monotonicidade dos cortes crus; não há um teorema separado com esse nome na fonte, e não o conto como declaração adicional compilada.

**Domínio da avaliação.** [DualWeightForm.lean:43](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightForm.lean:43>) é

`ENNReal.ofReal (Re ⟨v, dualAmbient s A v⟩)`.

[DualWeightForm.lean:62](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightForm.lean:62>) define

`q_A(v) = ENNReal.ofReal ((2π)⁻¹) * ∫⁻ s, dualQuadraticIntegrand A v s`.

O alvo é ENNReal, com infinito permitido, e a medida é Lebesgue. A definição total para A arbitrário aplica o truncamento de `ofReal` à parte real; não é, por isso só, uma forma quadrática estendida com todas as leis usuais. A mensurabilidade é comprovada por continuidade da avaliação escalar, inclusive para A não positivo.

**Aditividade positiva.** [DualWeightForm.lean:74](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightForm.lean:74>) declara explicitamente `(hA : 0 ≤ A)` e `(hB : 0 ≤ B)`. [DualWeightForm.lean:53](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightForm.lean:53>) assegura não negatividade das duas avaliações antes de usar `ENNReal.ofReal_add`. A soma passa pela integral não negativa usando mensurabilidade. Nenhuma hipótese de finitude dos integrais é usada, nem subtração de infinitos. As leis de zero para A e para v também foram auditadas.

**Invariância dual e composição.** [DualWeightForm.lean:87](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightForm.lean:87>) vale até para A arbitrário, porque a transformação é uma translação da função já truncada: `dualAmbient s (dualAmbient r A)` corresponde a `dualAmbient (r+s) A`. O lema `dualAmbient_add` usa `StarAlgEquiv.trans` nessa ordem; a fonte não confunde a ordem de composição. `lintegral_add_left_eq_self` usa a invariância de Lebesgue por translação. Isso prova `q_(θ_r A)(v) = q_A(v)`; não é uma lei de escala tracial nem uma construção de um objeto operadorial fixo na base.

**Corte restrito.** [DualWeightForm.lean:98](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightForm.lean:98>) afirma, para `R ≥ 0` e `A ≥ 0`,

`ofReal (Re ⟨v, T_R(A)v⟩) = ∫⁻ s in Ioc (-R) R, dualQuadraticIntegrand A v s`.

O lado esquerdo avalia o operador vetorial anteriormente construído. A prova move o funcional pela integral, usa a orientação correta e aplica `ofReal_integral_eq_lintegral_ofReal` com integrabilidade real e não negatividade demonstradas. O conjunto formal é **(-R,R]**, compatível com a integral de intervalo de Lean; a notação informal de corte fechado não deve apagar essa precisão. Seus extremos não afetam a integral de Lebesgue.

[DualWeightForm.lean:112](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightForm.lean:112>) conserva o fator `ofReal dualHaarFactor` ao comparar o corte com o integral total. É uma desigualdade escalar em ENNReal, não uma comparação com um operador ilimitado já construído.

**Unidade infinita.** [DualWeightForm.lean:121](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightForm.lean:121>) exige `v ≠ 0`. A ação preserva 1, a avaliação constante é `‖v‖² > 0` e `volume univ = ∞`; os dois fatores positivos não nulos permitem concluir `q_1(v)=∞`. O caso v=0 é tratado pela lei `dualQuadraticIntegral_zero_vector`, com resultado zero. Não houve uso de cancelamento inválido em `0 * ∞`.

## 5. Adendo autorizado após estabilização — `DualWeightExhaustion`

O manifesto inicial dos três módulos permanece intacto e conserva a exclusão que vigorava ao criá-lo. O aviso posterior autorizou este adendo, cuja fonte, log do autor, manifesto e compilação estão em diretório separado. Não se recompilou o arquivo enquanto permanecia declarado editável pelo pai.

Os três enunciados adicionais foram inspecionados e recompilados:

1. [DualWeightExhaustion.lean:14](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightExhaustion.lean:14>) assume somente `f : ℝ → ENNReal` mensurável. Define `g_n = 1_{(-n,n]} f`, prova a mensurabilidade e monotonicidade dos indicadores e demonstra pontualmente `sup_n g_n = f`. Para cada s escolhe n com `|s| < n`, preservando o extremo esquerdo estrito; portanto não perde pontos na união. `lintegral_iSup` aplica convergência monótona à sequência, inclusive para valor infinito. Não usa convergência dominada nem limite em norma de operadores.
2. [DualWeightExhaustion.lean:55](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightExhaustion.lean:55>) exige A positivo e aplica a identidade anterior ao integrando já mensurável. `ENNReal.mul_iSup` transporta o fator fixo através do supremo, e a igualdade de avaliação dos cortes identifica cada termo. O supremo é sobre `n : ℕ`, com raio `(n : ℝ)`; n=0 dá intervalo vazio e não prejudica a exaustão. A conclusão é `q_A(v) = sup_n [(2π)⁻¹ * avaliação_ENN(T_n(A),v)]`.
3. [DualWeightExhaustion.lean:70](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualWeightExhaustion.lean:70>) combina a identidade com `q_1(v)=∞` para `v ≠ 0`. O resultado afasta a interpretação dos cortes como uma família de médias que preserva a unidade, sem pretender construir um supremo limitado de operadores.

Os termos normalizados no supremo estão escritos como `ofReal dualHaarFactor * ofReal (Re ⟨v,T_n(A)v⟩)`. São avaliações escalares com o fator constante; a fonte não muda o tipo do supremo para uma álgebra ou um cone ampliado. A exaustão usa uma sequência cofinal de raios para esta integral, não uma nova afirmação de normalidade para redes arbitrárias de operadores.

## 6. Recompilação independente: arquivos, hashes e base de confiança

Compilador: `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`. Executável, hash, `LEAN_PATH` e comandos completos constam dos manifestos e registros.

| Fonte efetivamente recompilada | Linhas medidas | Exit | SHA-256 da fonte |
| --- | ---: | ---: | --- |
| [StrongOperatorIntegral.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_weight_independent_20260911_223930_194521/sources/TGLV350/StrongOperatorIntegral.lean>) | 147 | 0 | `de838ce57caf44ccf168c55810301302d0e0f2db24f90cd14e8e64270948f6a4` |
| [DualWeightCuts.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_weight_independent_20260911_223930_194521/sources/TGLV350/DualWeightCuts.lean>) | 91 | 0 | `27d186a2918e0c1bde98531197bbaebaba45d66d7de9d6446510899cf07fd435` |
| [DualWeightForm.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_weight_independent_20260911_223930_194521/sources/TGLV350/DualWeightForm.lean>) | 141 | 0 | `2b896e38d989f5060619a69611edc639e44f227752ac561a28bc91c39e18bca9` |
| [DualWeightExhaustion.lean — adendo](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_weight_independent_20260911_223930_194521/exhaustion_addendum_20260911_224248_455303/sources/TGLV350/DualWeightExhaustion.lean>) | 81 | 0 | `88ba65a291939d452227430581e50967c7da0165401514e88cbcb1816196772c` |

Foram congeladas **314 dependências de projeto**, com cópias de fontes e binários e hashes conferidos. O `LEAN_PATH` começa pela árvore própria e exclui os builds vivos do projeto pai e do projeto canônico. `DualWeightCuts` usa o `StrongOperatorIntegral` recompilado aqui; `DualWeightForm` usa esses binários próprios; o adendo usa o `DualWeightForm` recompilado aqui. Não se reutilizou o parecer anterior como prova dos módulos novos.

Os pacotes de biblioteca instalados, incluindo Mathlib, foram usados em modo de leitura. **Limite da independência:** o compilador e a biblioteca Mathlib não foram reconstruídos nem tiveram a árvore integral de binários duplicada nesta etapa. O congelamento/hash por módulo aqui declarado cobre as dependências de projeto; não é uma auditoria integral da implementação de Lean/Mathlib.

O primeiro grupo auditou 41 declarações escritas, incluindo `Family`, e seis nomes gerados: construtor e projeções. O adendo auditou três teoremas. A lista efetiva de axiomas coincidiu com todos os nomes esperados; nenhum ficou fora do trio permitido. Os dois arquivos próprios de auditoria também compilaram com exit 0. No adendo, três exemplos adicionais verificaram a mesma ação restrita sob a integral, o fator constante e o codomínio vetorial da integral.

Evidência reproduzível:

- [Manifesto dos três módulos e das 314 dependências](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_weight_independent_20260911_223930_194521/manifest.json>).
- [Compilações independentes e auditoria dos primeiros 47 nomes](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_weight_independent_20260911_223930_194521/compilation.json>) e [tipos e axiomas impressos](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_weight_independent_20260911_223930_194521/logs/DualWeightFullAudit.stdout.txt>).
- [Manifesto separado do adendo](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_weight_independent_20260911_223930_194521/exhaustion_addendum_20260911_224248_455303/manifest.json>) e [compilação/auditoria do adendo e três conferências de tipos](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_weight_independent_20260911_223930_194521/exhaustion_addendum_20260911_224248_455303/compilation.json>).
- [Fonte própria da auditoria e das conferências do adendo](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_weight_independent_20260911_223930_194521/exhaustion_addendum_20260911_224248_455303/sources/ExhaustionFullAudit.lean>).

## 7. Integração final do autor: evidência inspecionada, não recompilação das raízes pelo revisor

**SHA-256 do monólito experimental lido e conferido:** `cb7b87f8f64a7bb0483767809d6712d1d381c6530c24d733de87473a5d2ba7b1`.

O hash coincide com `integration.json` e `gate_tests.json`. A análise estática do dicionário embutido encontrou 727 fontes, sem execução ou importação de `um.py`. Os quatro fontes integrados coincidem com os snapshots dev exceto pelas substituições previstas de caminhos de importação; seus bytes também coincidem com o conteúdo embutido:

| Módulo integrado | SHA-256 da fonte integrada |
| --- | --- |
| StrongOperatorIntegral | `7ee0e23dc3319a72734ce420f540251f59a27561fa61221d6ab5f98b2989dfa7` |
| DualWeightCuts | `cad8c916c67f1329afbac42658d13e8930e065e8f6a69152d4c9caf93cedd91b` |
| DualWeightForm | `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4` |
| DualWeightExhaustion | `b09270078d8522f00acddd75b90a36f92b332330521aaec3253087414555c697` |

**Conferido em arquivos/logs do autor:** 25/25 registros Lean com exit 0, todos com hash de fonte e `.olean` correspondentes; 48/48 controles Python marcados aprovados; 5922 declarações distintas no Audit, sem axiomas fora do trio. O conjunto de registros coincide com os módulos acrescentados e as duas raízes descritos na integração. Não declaro ter executado essas 25 compilações integradas ou os 48 controles: executei as quatro recompilações dev e as auditorias próprias acima.

O estrato anterior, 21 módulos/46 controles/5.897 alvos, foi preservado. A comparação mostrou 19 módulos anteriores com os mesmos hashes de fonte e binário; as seis compilações novas correspondem aos quatro módulos desta etapa e às duas raízes. Entre os fontes antigos embutidos, mudaram apenas `TGLExt.lean` e `TGL/Audit.lean`. O AST Python fora do dicionário embutido é idêntico ao backup do estrato 21, de hash `e89ca44ad7a7ecc4e37eac69d882934ad82cb014ea8ce5cf60af5702aac684c3`; `gate_extension.py` é byte a byte idêntico ao daquele estrato.

Os dois controles novos registrados são `extended_dual_integral_is_not_a_canonical_trace_certificate` e `infinite_unit_does_not_supply_a_finite_three_locks_corner`. Seus resultados foram lidos no relatório do autor; não foram reexecutados aqui. A extensão do gate continua com escopo modular e não recebeu os novos nomes como quitação de core, traço ou Three Locks.

Evidência congelada: [verificação independente dos hashes e comparação entre estratos](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_weight_independent_20260911_223930_194521/final_integrated_20260911_224417_017286/verification.json>), [compilações integradas do autor](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_weight_independent_20260911_223930_194521/final_integrated_20260911_224417_017286/integrated_compile.json>), [controles Python do autor](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_weight_independent_20260911_223930_194521/final_integrated_20260911_224417_017286/gate_tests.json>) e [nomes/axiomas extraídos do Audit](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_weight_independent_20260911_223930_194521/final_integrated_20260911_224417_017286/axioms.json>).

## 8. Limitações e preservação

A nota [DUAL_WEIGHT_CONSTRUCTION.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_weight_independent_20260911_223930_194521/research_note/DUAL_WEIGHT_CONSTRUCTION.md>) foi consultada como roteiro de construção e de convenções, não como prova Lean. Não certifiquei nesta revisão suas etapas de Fourier, identificação de pontos fixos com a imagem da base, teoria espectral de cones ampliados, densidade de domínio finito, peso dual canônico, semifinitude, Stone/afiliação ou passagem ao traço.

O pacote não formaliza todas as propriedades de uma forma quadrática estendida ou de um peso operadorial. Ter uma avaliação ENNReal aditiva em A positivo, invariância pela ação e uma expressão por supremos escalares não fornece, sozinho, essas estruturas. A divergência na unidade é compatível com a necessidade de permitir infinito; não prova, isoladamente, nem refuta semifinitude.

Não ficou pendente uma análise específica identificada dos quatro enunciados/módulos delimitados. A revisão não afirma exaustividade de todo o kernel, não repete a revisão semântica das 5.922 declarações e não executa o runtime monolítico. Não houve ampliação para construir o traço.

Todos os pareceres anteriores identificados no manifesto foram preservados por hash. Fontes do autor e originais permaneceram somente leitura; logs e snapshots anteriores foram mantidos. Somente scripts, snapshots, binários próprios, logs próprios e este relatório foram gravados sob `revisao`. Nenhuma memória global, raiz de implementação, integração ou monólito foi alterado pelo revisor. Não há aprovação de QG, quitação de core/canto ou autorização de transposição ao canônico neste parecer.
