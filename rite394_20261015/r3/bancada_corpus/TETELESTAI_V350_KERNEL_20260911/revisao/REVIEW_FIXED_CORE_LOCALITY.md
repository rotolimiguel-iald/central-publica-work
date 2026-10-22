# Revisão independente — localidade da álgebra fixa

## Parecer das cinco fontes — 2026-09-12T05:02:49-03:00

**[REAL] Exame matemático e recompilação independente das cinco fontes concluídos, sem achados P0, P1 ou P2.** O resultado é a comutação de todo B∈F com os recortes mensuráveis no mesmo L² regular, obtida de pareamentos L¹ e unicidade Fourier. Não pressupõe decomposição em fibras de B, ação constante de B na fibra ou F=base. Este estrato certifica as fontes dev abaixo e o auditor próprio; **integração deste lote ainda não inspecionada aqui**. Eventual inspeção integrada será um adendo separado, com preservação deste texto.

### Fontes e alvos

| Módulo dev em `kernel/TGLV350` | Linhas | #print axioms | SHA-256 lido e congelado |
|---|---|---|---|
| `FixedCoreShiftCommutation` | 68 | 4 | `43214f23885e4991aa2da46379ace805f378bf2481664f11ed9bb2994f1ca2e9` |
| `FourierUniqueness` | 35 | 1 | `8800835e0c4cf3ad84696f810b7bbb02f4cbd8634b21f170117d9f8e4f694b72` |
| `CharacterLocality` | 60 | 3 | `04f9e81621308a942cf280a5c7c1bc4f1e4ca0ba2953c3268d13d50b17d1985f` |
| `L2MeasurableCut` | 74 | 6 | `6a85eeb58ed8805dc7857c0e6e3d61bbc50b8314f0c7ba26318afa648387e1f3` |
| `FixedCoreLocality` | 42 | 2 | `acdb5068048d838130af29523e7f106bcb79cc4d56788e2f393f139154cf5c74` |

São **16 alvos impressos e 17 declarações nomeadas**: `measurableCutLp_ae` é o auxiliar adicional, não impresso pelo autor. O auditor próprio fez `#check` de todas as 17 declarações, com universos, e `#print axioms` dos 16 alvos exatos. O auxiliar foi lido e é usado transitivamente pelos alvos auditados. Não há alvos importados contados como novos.

### Pontos adversariais conferidos, com linhas

**`FixedCoreShiftCommutation.lean:12,25,44,55`.** A translação ordinária é `shift s`, f(x)↦f(x−s); a família modular regular é `regularUnitary P t = fibre(modularFlowCLM P t) * shift t`. A prova mantém esses dois grupos distintos. Translações comutam com cada gerador de fibra constante e com cada unitário regular, usando `shift_mul` e comutatividade da adição real. A pertença ao comutante passa por `regularCore_minimal` aplicado ao comutante-estrela das translações; as condições envolvendo os adjuntos são demonstradas com `shift_star` e −s. Não se presume que um operador arbitrário de N seja fibra constante. As simetrias na passagem entre a convenção de `mem_centralizer_iff` e `mem_commutant_iff` produzem as orientações declaradas. No último lema, B∈F fornece B∈N e sua invariância dual; a comutação com caracteres vem dessa invariância já demonstrada, não da comutação com translações.

**`FourierUniqueness.lean:16–31`.** O teorema exige f,g:ℝ→H integráveis e igualdade dos Fourier ordinários em todas as frequências; conclui igualdade quase em toda parte para `volume`. Ele não exige continuidade de f/g, L² de f/g ou integrabilidade de suas transformadas. `fourier_test_pairing` é aplicado a 𝓕⁻φ para φ de Schwartz; `fourier_fourierInv_eq` devolve φ, preservando a convenção da transformada. A igualdade das transformadas dá igualdade dos pareamentos com todas essas funções teste. Os testes reais suaves de suporte compacto são embutidos em ℂ pelo mapa contínuo `Complex.ofRealCLM` e convertidos em Schwartz; a unicidade de funções localmente integráveis dá a conclusão ae. A hipótese L¹ é usada nessa cadeia, impedindo a vacuidade que seria possível ao tratar integrais de funções não integráveis como informação suficiente.

**`CharacterLocality.lean:16,28,40`.** `characterPhase s x = exp(−i s x)` é a fase efetiva do mesmo multiplicador dual. A identidade Fourier usa **s=2πξ**, com sinal negativo; não muda a normalização ou troca frequência angular por frequência sem o fator. O produto interno é conjugado-linear no primeiro argumento e linear no segundo: por isso a fase multiplica g em `⟨f,D_(2πξ)g⟩`, como mostram `inner_smul_right` e `L2.inner_def`.

Os dois pareamentos pontuais `⟨(B.adjoint f)(x),g(x)⟩` e `⟨f(x),(Bg)(x)⟩` pertencem a L¹ por `L2.integrable_inner`, para B contínuo complexo-linear no mesmo L². A igualdade das transformadas segue de `adjoint_inner_left` e da hipótese **∀s, D_s B = B D_s**, na orientação efetivamente necessária. Não se exige B positivo, auto-adjunto ou unitário; o adjunto existe no Hilbert completo. A conclusão é uma igualdade ae para **cada par fixado f,g**. O conjunto excepcional pode depender do par; a prova seguinte nunca promove essa conclusão a uma igualdade pontual simultânea para todos os vetores. Não se introduz separabilidade da fibra H nem um teorema de operadores decomponíveis.

**`L2MeasurableCut.lean:12–17,19–47,51–65`.** `measurableCutLp` usa `MemLp.indicator` e `toLp` no quociente L² existente. O auxiliar ae vincula o representante ao indicador; adição e escalares usam as igualdades ae de Lp, não igualdade arbitrária de representantes. A norma do recorte é ≤‖f‖ pelo limite pontual de normas, e `mkContinuous 1` constrói o operador complexo-linear limitado. A fórmula do produto interno é o integral restrito do pareamento L¹, por `integral_indicator` e congruência ae.

O conjunto S é **mensurável e pode ter volume finito, infinito ou zero**; não há hipótese de medida finita, intervalo, compacidade ou interior. A medida do espaço, porém, continua sendo **Lebesgue em ℝ**: estes enunciados não estão quantificados sobre uma medida arbitrária μ ou conjuntos não mensuráveis. “Qualquer medida do recorte” deve ser entendido como ausência de restrição ao valor de `volume S`, não como troca da medida-base. O recorte espacial não é a projeção finita P_F de outras etapas, nem a projeção posterior sobre funções constantes em um intervalo.

**`FixedCoreLocality.lean:16–28,32–37`.** Para cada S mensurável, a extensionalidade do operador e do produto interno reduz a igualdade `M_S B = B M_S` à identidade de pareamentos integrados sobre S. A identidade ae da etapa Fourier é restringida com `ae_restrict_of_ae`; isso funciona para qualquer S mensurável, sem uniformizar os conjuntos excepcionais em f,g. A posição do adjunto em `⟨B* f,M_S g⟩` e a simetria final estão corretas. O último lema compõe essa prova com a comutação por caracteres de B∈F. Não acrescenta premissa residual de localidade, decomposição, identidade F=base ou constância da fibra.

Todos os enunciados atuam no mesmo `RegularHilbert H = Lp H 2 (volume : Measure ℝ)`, especializado a H=`TowerHilbert P` nos resultados sobre N/F. Não se extrai informação de uma leitura em um único vetor, de uma função não integrável ou de um `toReal` aplicado a ∞; as novas fontes não usam essa conversão. A passagem decisiva usa integrabilidade dos pareamentos escalares, não integração em norma de B(H).

### Evidência independente e proveniência

Foi copiado apenas o fecho transitivo dos imports de projeto necessários às cinco fontes: **341 módulos**, com fontes e `.olean` de árvores próprias previamente verificadas. Cada par foi conferido por SHA-256; **todas essas fontes de dependência coincidem byte a byte com as fontes vivas correspondentes** no congelamento. O fecho não inclui `DualSemifiniteIdeal`, `BoundedDualValues` ou `BoundedFiniteSquares`; portanto não herda a diferença de comentário documentada na etapa anterior. Os mapas completos de origem e destino estão no [manifest.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/fixed_core_locality_independent_20260912_045728_705345/manifest.json>).

O `LEAN_PATH` aponta para o build isolado e para os pacotes instalados somente para leitura, sem os builds de projeto do autor. TMP/TEMP e todas as saídas estão na árvore própria em `revisao/`. Não recompilei Mathlib nem as dependências de projeto. Compilador: `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`; SHA do executável lido **`9b216deb50d37c32c829d1efaaa5bafd5560417d382df35a815489e31a31593f`**.

| Processo executado pelo revisor | Resultado | Tempo | SHA-256 `.olean` próprio |
|---|---|---|---|
| `FixedCoreShiftCommutation.lean` | rc0 | 28.361 s | `a33b5cf3cd9b0878f94c6a78648f338d8cab9c7f9d9e966ac102611e7380109f` |
| `FourierUniqueness.lean` | rc0 | 15.988 s | `1930e611096669ed0faddad47c63452b1c464a56302ddbbd6dd4d0822d500ae7` |
| `CharacterLocality.lean` | rc0 | 30.582 s | `69f6710af2cef0e129f522da7db9381437c29141fe4ddda6197aa52d11ffa0dd` |
| `L2MeasurableCut.lean` | rc0 | 34.069 s | `6e54e1986fc0f954c51266da0c11badffa152da71035334702e49dd69763c87d` |
| `FixedCoreLocality.lean` | rc0 | 32.531 s | `80538a1df96c6fabc8d2a34178212612f90d67b909261c3e3c25e434e69985ee` |
| `FixedCoreLocalityFullAudit.lean` | rc0 | 30.281 s | `6da60bb2aa57a510307d8fabea7477a322037a6eadc87ad4a08b04eec312ec39` |

Os cinco binários próprios coincidem com os respectivos binários dev do autor: **True** (confronto individual no recibo desta revisão). Fonte do auditor SHA **`ed3dce7efbf1ad8f37e651eddad9b52bbac97f94adf61f65ad8ae22e0058ac77`**. Todos os 16 alvos têm somente `propext`, `Classical.choice`, `Quot.sound`; não há axioma customizado, `sorryAx` ou `trustCompiler` em suas dependências transitivas auditadas. Os tipos elaborados do auditor foram lidos. [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/fixed_core_locality_independent_20260912_045728_705345/compilation.json>) registra seis processos rc0, conjunto exato de alvos, hashes das fontes/dependências preservados e pareceres anteriores intocados.

Os logs dev do autor abaixo foram copiados e confrontados com os hashes de fonte e binário; são evidência adicional do autor, distinta dos seis processos próprios:

- `FixedCoreShiftCommutation_20260912_042957_543666.json`.
- `FourierUniqueness_20260912_044014_302605.json`.
- `CharacterLocality_20260912_044308_803246.json`.
- `L2MeasurableCut_20260912_044527_302983.json`.
- `FixedCoreLocality_20260912_045342_506289.json`.

### Limites e preservação

**[OPEN]** Constância da ação de B na fibra; identificação F=base original; construção/interface padrão do peso operatorial e correspondência geral espectral/predual; traço canônico, Three Locks/H1–H3, física, contrato ampliado e runtime integral. A localidade por recortes aqui provada não é uma prova dessas identificações posteriores, nem uma hipótese delas assumida retroativamente. A etapa posterior de projeção da componente constante num intervalo está fora deste exame.

A integração deste lote não foi inspecionada neste estrato; contagens de build/testes/Audit do pacote anterior não são atribuídas às novas fontes. Não executei monólito, recorder, verifier ou controles Python do autor. Nenhuma flag ou QG foi aprovada.

Custódia anterior lida: `bounded_values_custody.json`, timestamp `2026-09-12T04:35:14-03:00`, SHA `1d6cf104ca09019639a9595108d57ee2a873cc14be1d0d0872f175775d9c8d03`. O parecer custodiado `REVIEW_BOUNDED_DUAL_VALUES.md` permanece igual ao hash `ddb959f15ea1cf02832b67a10179ad53112a7fbe39d12677c9a31c5f2bf1eefa`. Todos os pareceres anteriores mantêm os hashes do manifest desta revisão. Não os modifiquei, nem alterei fontes do autor, originais, monólito, logs ou memórias. Este novo parecer foi criado por temporário verificado e substituição; qualquer adendo preservará seus bytes por backup imediato e append.

**Conclusão delimitada das fontes: nenhum P0–P2 encontrado; cinco módulos e auditor próprio concluídos, 16 alvos no trio, sem análise matemática pendente nas fontes recebidas.**


## Adendo FINAL — 2026-09-12T05:07:29-03:00 — integração e documentação

**[REAL] Revisão delimitada CONCLUÍDA, sem achados P0, P1 ou P2.** Este adendo encerra a pendência de integração do primeiro estrato. O escopo efetivo foi: cinco fontes finais, 16 alvos impressos, auxiliar ae conferido, seis processos independentes, integração por leitura de fontes/bytes/AST/logs, minuta e recorder. Nenhuma análise específica permanece pendente nesse escopo.

**Conclusão matemática:** no mesmo L² de Lebesgue, todo B∈F comuta com as translações ordinárias e com a multiplicação por indicadora de qualquer conjunto mensurável S, sem hipótese de `volume S<∞`. A passagem pelos pareamentos L¹ é válida e não assume avaliação pontual contínua, conjunto excepcional comum a todos os vetores, decomposição de B ou constância da ação na fibra. Não houve alteração das cinco fontes desde seus snapshots e recompilações.

### Separação das evidências

| Evidência | O que foi efetivamente feito |
|---|---|
| Cinco fontes dev e auditor próprio | **Executados pelo revisor:** 5 recompilações + 1 auditor rc0; 16 #print axioms exatos, 17 #check incluindo o auxiliar; somente o trio. Fontes, binários e 341 dependências pinadas conforme o primeiro estrato. |
| Build integrado | **Executado pelo autor; inspecionado pelo revisor:** 63 registros rc0 com fontes e `.olean` atuais verificados por hash. 56 registros conservam fonte/binário; 5 módulos novos + 2 raízes recompilados. |
| Controles Python | **Executados pelo autor; registros e novo controle lidos pelo revisor:** 63/63 aprovados. Nenhuma repetição pelo revisor. |
| Audit integrado | Stdout lido: 6192 declarações distintas, mapa igual ao evidence; exatamente 16 nomes acrescidos, com axiomas iguais aos do auditor próprio. |
| Runtime/registro de memórias | Não executados pelo revisor. Runtime integral continua pendente; recorder foi somente lido e analisado estaticamente. |

Os cinco `.olean` dev próprios coincidem byte a byte em SHA com os do autor, como registra o recibo do primeiro estrato. Os novos `.olean` integrados são artefatos distintos, pois os imports usam os nomes TGLExt/V350; sua proveniência é a dos processos do autor abaixo. O frescor de dependências do build integrado é relatado pelo procedimento do autor, além do confronto de hashes atuais e do estrato anterior aqui efetuado.

### Snapshot integrado efetivamente lido

SHA-256 de `um.py`: **`19b2909469d6aa070075d7a956abb0ad1683272828242c28521b4802f0a112ae`**, igual a `integration.json` e `gate_tests.json`. Extraídos por AST/literal_eval **765 arquivos embutidos**, sem importação ou execução do monólito. O original canônico e a cópia-base foram relidos para hash: ambos **`c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`**, iguais ao `base_sha256` registrado.

As cinco cópias integradas coincidem com os respectivos dev mediante **somente a reescrita dos caminhos de import**, e com os textos embutidos byte a byte:

| Módulo | SHA-256 de `kernel/TGLExt/V350*.lean` |
|---|---|
| FixedCoreShiftCommutation | `efb3533d950d396ae8932ff9980500d6c65ee000e03952e385b038bc70588098` |
| FourierUniqueness | `16eba1061905aa2eabf73e388c47a8a4f522acacf18e2eb5a8293687121cd850` |
| CharacterLocality | `7a5d2f1b70b3d61307045c4460034e3821976c8b30b02d5bcf165d157f33419a` |
| L2MeasurableCut | `0a52d5d408c5f877b6eb95309cbb793ca385d2e9cfd7778e716442d104babb6b` |
| FixedCoreLocality | `b5cb6a24e5cc2ca221741f9e8dbb4ccc2361b7a7729886d2ab80ed723b1984a8` |

Em relação ao estrato custodiado `e5c97d1f3307edbfe96d1c7ff3278441ff3f666c2f383fbd2aa31da3cf32fe31`, foram acrescentados exatamente esses cinco arquivos; nenhum embutido foi excluído. Apenas `TGLExt.lean` e `TGL/Audit.lean` mudaram entre as fontes antigas, pelos cinco imports, comentário de alcance e 16 alvos. O namespace `TGLV350.Fourier` de `fourier_integral_ae_injective` foi preservado corretamente; os outros alvos estão em `TGLV350.Regular`. `measurableCutLp_ae` não foi contado como alvo novo impresso.

Os sete registros novos do autor têm rc0 e fonte inalterada durante a compilação; hashes de saída lidos:

| Registro | Timestamp do log | SHA-256 `.olean` integrado |
|---|---|---|
| `TGLExt/V350FixedCoreShiftCommutation.lean` | `20260912_045808_191897` | `f8b09bdcfb93b8b0e9de01efa226dc647e8f6ea28f73c8612e9d4e1f77700565` |
| `TGLExt/V350FourierUniqueness.lean` | `20260912_045841_191172` | `044ebc3d331c0b2ae61f9532992cd1b346c121ba3b439b88ac2868f0a61e277d` |
| `TGLExt/V350CharacterLocality.lean` | `20260912_045859_186309` | `66c7933f225568641a3bbeccd406fea1e5b29be89b372962aca2f4572e48cc71` |
| `TGLExt/V350L2MeasurableCut.lean` | `20260912_045930_947200` | `41378ac6d8012e4732a6d6a36543e27e6b1c46c9b8f33d7fea07cf55c3cff5e3` |
| `TGLExt/V350FixedCoreLocality.lean` | `20260912_050005_483196` | `cca3aa8f352ae4b5882ee8e1249e9ac6c0d4eef7cb410b7652cd7a9023a80b0c` |
| `TGLExt.lean` | `20260912_050037_640770` | `298c85f18982643577a4d7e04153d5b80559a7f0d91ff2e23fff456dd1c6dc0a` |
| `TGL/Audit.lean` | `20260912_050107_862323` | `94282c0734e5937e05a7264ffb85ef0efe3b74695b336e91cd098e7bc0092773` |

A AST Python fora de `_EMBEDDED_KERNEL_FILES` e os bytes de `gate_extension.py` permanecem iguais ao estrato anterior. O único controle acrescido, `fixed_core_locality_does_not_discharge_base_trace_or_physics`, verifica os nomes pertinentes e as seis flags maiores falsas. Os registros mantêm `legacy_gate_changed=false`, `full_plan_complete=false` e `full_monolithic_runtime_run=false`; nenhuma inferência de runtime/QG é extraída dessas contagens.

Evidências congeladas: [verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/fixed_core_locality_independent_20260912_045728_705345/final_integrated_20260912_050417_884240/verification.json>), [supplemental_verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/fixed_core_locality_independent_20260912_045728_705345/final_integrated_20260912_050417_884240/supplemental_verification.json>). Fontes integradas, stdout/stderr, relatórios e diffs dos agregadores/novo controle estão na mesma pasta. Os mapas inteiros de hashes/axiomas foram preservados, sem reescrever registros do autor.

### Minuta e recorder

Leitura integral, confronto conceitual e sintaxe AST concluídos, sem achados documentais. Hashes finais lidos, iguais aos snapshots examinados:

- `MINUTA_LOCALIDADE_FIXA.md`: **`d146b68d87623abf2efdf249717122c390d4b4df103013fbcc4493d671a858ea`**.
- `record_fixed_locality_progress.py`: **`2d1ff4e142ffaecb23a55ad6a8e593bbe19156290a4be926332c42a19fa33cc5`**.

A minuta descreve corretamente unicidade Fourier em L¹, igualdade ae dos pareamentos, integração restrita e comutação P_S B=B P_S. A cota de norma do recorte decorre da construção `mkContinuous 1`; não exige medida finita de S. Os termos B*f(x) e Bg(x) devem ser lidos como `(B.adjoint f)(x)` e `(B g)(x)`, conforme os tipos formais, sem presumir B como campo pontual de operadores. As menções à futura ação constante/F=base estão explicitamente OPEN; o resultado atual é uma identidade de operadores no quociente L².

O recorder distingue corretamente `FourierUniqueness` pelo namespace Fourier, preserva o alcance das provas e mantém as flags maiores e os indicadores de base/interface de peso/traço abertos. Programa **18 superfícies de append** (16 na ROOT e Atlas/índice), backups imediatos de bytes e escrita temporária verificada; exige `--review-read` e confronta fonte/binário, axiomas e snapshot antes de registrar. Essa leitura não certifica uma execução futura: não executei recorder ou verificador de custódia, nem escrevi nessas superfícies.

O inventário I/O permanece histórico, SHA `34133956b6a47012805003adfae734e7439b27e1f611466829af624b1857d89c`, associado à fonte `c712532dc079b832d9eb1ecc26ea50f2d49aa2c387afa435cc777eb302e96e09` pelos campos históricos da custódia anterior. Não houve promoção desse inventário a liberação de runtime da cópia atual. [Registro documental](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/fixed_core_locality_independent_20260912_045728_705345/documentary_20260912_050344_519440/verification.json>).

### Encerramento e preservação

**[OPEN]** Constância da ação na fibra e sua pertença à álgebra original/F=base; correspondência geral espectral/predual; interface padrão de peso operatorial, estado/gerador/perturbação e traço canônico; Three Locks/H1–H3 e física; contrato ampliado e runtime integral. Esses limites não são defeitos dos enunciados de localidade conferidos. **`UnitIntervalProjection` e a projeção posterior da componente constante não foram lidos, recompilados ou incluídos nesta revisão.**

Backup imediato deste parecer antes do adendo: `REVIEW_FIXED_CORE_LOCALITY.md.bak_20260912_050729_569574`, **11733 bytes**, SHA `1cf8f94e916f5752d77966b08d0191ac48c246b7700958ce428b6a297546027b`. O novo arquivo conserva integralmente esse prefixo. Todos os pareceres custodiados anteriores mantêm seus hashes; originais, fontes do autor, integração, logs, monólito e memórias permaneceram intocados pelo revisor. Escrita exclusivamente em `revisao/`. **Parecer final encerrado: nenhuma falha P0–P2 ou verificação delimitada pendente; nenhuma aprovação de F=base, traço, gate, QG ou runtime.**
