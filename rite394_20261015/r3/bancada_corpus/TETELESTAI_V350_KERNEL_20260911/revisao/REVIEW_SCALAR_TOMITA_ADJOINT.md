# Revisão independente DEV — adjunto antilinear de Tomita

2026-09-12T10:50:30-03:00. **[REAL — dois módulos/23 alvos conferidos e recompilados; nenhum achado P0, P1 ou P2.]** Escopo: `AntilinearAdjointGraph` (11) e `ScalarTomitaAdjoint` (12), nas fontes finais congeladas. A composição S†S e módulos posteriores não foram lidos, compilados ou aprovados nesta revisão. Nenhuma integração nova foi examinada.

## Significado, hipóteses e composição das provas

[AntilinearAdjointGraph.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/AntilinearAdjointGraph.lean:13>) define a relação por **∀x∈D, ⟨Sx,y⟩=⟨z,x⟩** e o domínio por existência de tal z. Isso testa todo D, não somente o gráfico inicial ou algum subdomínio escolhido. A convenção complexa é linear na segunda entrada. Por isso o representante de cy é **conj(c)z**, exatamente o testemunho de `smul_mem'` (linha 25), e o mapa resultante é `LinearPMap (starRingEnd ℂ) H H`, antilinear. Não é um CLM em todo H nem um adjunto complexo-linear inadvertido.

[Escolha, unicidade e mapa](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/AntilinearAdjointGraph.lean:32>): `Classical.choose` escolhe um representante cuja existência consta da propriedade do subtipo; `choose_spec` fornece o pareamento. Essa escolha e a relação existem antes de hD, mas a unicidade e as leis do mapa usam explicitamente **hD : Dense D** (linhas 40–73). O `include hD` do lema de unicidade é efetivo no tipo impresso. A igualdade de produtos internos no conjunto denso implica igualdade dos representantes. Não se pressupõem continuidade, limitação ou fechabilidade de S na construção genérica, e não há afirmação de unicidade sem densidade.

[Maximalidade e fechamento](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/AntilinearAdjointGraph.lean:80>): qualquer par que satisfaz o pareamento fornece pertinência ao domínio e o valor escolhido igual ao representante proposto. `graph_eq` prova igualdade entre o gráfico efetivo do mapa parcial e toda a relação. Esta é interseção, sobre x∈D, de igualdades fechadas em H×H; Sx fica fixo em cada igualdade, dispensando continuidade de S. O que é fechado é **o gráfico**, não necessariamente D. Os tipos genéricos usam `H : Type` com `NormedAddCommGroup` e `InnerProductSpace ℂ`; não exigem `CompleteSpace H` e não reivindicam aqui generalização a `Type u` arbitrário.

[Aplicação ao mesmo objeto](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarTomitaAdjoint.lean:13>) especializa literalmente `scalarClosedTomitaDomain P` e `scalarClosedTomita P`, no `ScalarGNSHilbert P` anterior. A densidade do domínio de S é fornecida pelo teorema já construído. `domain_iff` explicita o quantificador sobre **todo D(S)**; `maximal` e `isClosed` herdam a relação exata. Os tipos auditados das conclusões de existência do mapa, fechamento, densidade e involução têm somente P como parâmetro estrutural: nenhuma premissa adicional de separação, densidade do adjunto, KMS ou inversibilidade foi acrescida a P. Não há instâncias locais novas nesses dois arquivos.

[Transporte do pareamento gaussiano](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarTomitaAdjoint.lean:45>) usa T=`scalarGaussianGNSMap P`: H_I→L²(ℝ,L²(ℝ,TowerHilbert P)), e o **adjunto limitado Mathlib T***. Para B∈ρ(N)' e x∈D(S), o par (Tx,TSx) pertence ao fecho do gráfico auxiliar pela prova anterior `scalarGaussian_maps_graph_closure`. A cadeia efetiva é

`⟨Sx,T*BΩg⟩ = ⟨TSx,BΩg⟩ = ⟨B*Ωg,Tx⟩ = ⟨T*B*Ωg,x⟩`.

As orientações de `adjoint_inner_right` e `adjoint_inner_left` foram confrontadas com a Mathlib. Assim T*BΩg pertence ao domínio máximo e tem representante T*B*Ωg (linha 64), sem inverter T. Ωg, T, a álgebra auxiliar e o gráfico transportado são os mesmos já revisados; não há substituição de peso, medida, fator Haar ou Hilbert por homônimo.

[Densidade de D(S†)](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarTomitaAdjoint.lean:75>) prova primeiro D(S†)⊥=0. Se v está no ortogonal, a pertinência acima dá `⟨T*BΩg,v⟩=0`, logo `⟨BΩg,Tv⟩=0` para todo B∈ρ(N)'. A órbita é densa pela separação de Ωg **para a imagem ρ(N)**; então Tv=0 e a injetividade gaussiana dá v=0. A equivalência Mathlib entre ortogonal trivial e fecho total usa a completude herdada de H_I. Não se pressupõe que T tenha inversa limitada, que sua imagem seja fechada/sobrejetiva, ou que Ωg seja separante para todo B(H). Não se usa interseção a.e. não enumerável. O grafo de imports de 401 módulos de projeto é acíclico, e nenhuma das 399 dependências antigas importa estes dois novos módulos: não há circularidade introduzida na densidade ou na separação.

[Troca e involução](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarTomitaAdjoint.lean:93>) substitui x por Sx, legitimamente em D(S) por `scalarClosedTomita_maps_domain`, e usa S²x=x. Conjugar o pareamento fornece a relação trocada `(z,y)`. A maximalidade do domínio coloca S†y de volta em D(S†); a unicidade do representante prova `(S†)²y=y` (linhas 108–119). É involução no domínio invariante, não alegação de operador limitado definido em todo H_I. Nenhum J substituto é introduzido.

## Evidência própria e pins

| Fonte DEV | Alvos | SHA256 fonte lido | SHA256 .olean próprio = autor |
|---|---:|---|---|
| AntilinearAdjointGraph | 11 | `6a3cbe3ded292e347a885be00be565c6b030d6971a7ac035096966028a552e98` | `6a28461d1006fe9f9c206bbb87909e43e81fbfc332e13e41abffe32f9dc9002e` |
| ScalarTomitaAdjoint | 12 | `1ad4e1d9e475e8ee94b65a87f05033b26c06d46e1cd30a62eb63e07f685df139` | `24d29ed253a9c3e7c54db77326c3d70df915cfb7b2126848bb7c38184f7b25da` |

| Processo próprio | rc | Segundos |
|---|---:|---:|
| TGLV350/AntilinearAdjointGraph.lean | 0 | 15.452 |
| TGLV350/ScalarTomitaAdjoint.lean | 0 | 66.884 |
| ScalarTomitaAdjointAudit.lean | 0 | 31.348 |

**Três processos próprios rc0**, sem warnings ou stderr; 23 `#check` com universos e 23 `#print axioms`, cobertura exata dos alvos das fontes, sem pressupostos acrescentados pelo auditor. Todos usam apenas `propext`, `Classical.choice`, `Quot.sound`. Ambos os .olean coincidem byte a byte com os finais do autor. A leitura integral das fontes não encontrou `axiom`, `sorry`, `admit`, `unsafe`, atributo de redutibilidade ou mudança de transparência. As opções são somente `autoImplicit false`, desativação do linter de variáveis não usadas e `maxHeartbeats 1000000`.

Árvore: [manifest.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/scalar_tomita_adjoint_independent_20260912_104520_672232/manifest.json>); 399 dependências de projeto próprias congeladas, herdadas do lote anterior, com fontes/binários e origem pinados; oito pacotes externos somente leitura. **Nenhum build autoral de projeto no LEAN_PATH**. Não recompilei esses pacotes/dependências nem renovei a certificação global deles; mantêm-se os limites da proveniência anterior e a errata histórica de comentário de `DualSemifiniteIdeal`. Compilador `9b216deb50d37c32c829d1efaaa5bafd5560417d382df35a815489e31a31593f`: Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release).

Resultados: [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/scalar_tomita_adjoint_independent_20260912_104520_672232/compilation.json>), [verification_dev.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/scalar_tomita_adjoint_independent_20260912_104520_672232/verification_dev.json>), [23 tipos e axiomas completos](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/scalar_tomita_adjoint_independent_20260912_104520_672232/logs/ScalarTomitaAdjointAudit.stdout.txt>). Auditor fonte `81090ae356900969b636fc4ee7c5cb50afb4e2f39b2cd809c0731259e722ac79`, binário `627cbf35bb87e005e357894c566d29eea1031a7aebf3ac2525a3586f7cd9a83a`, stdout `137158ccc3a6ad17e4fedafde590871ecacfd2f41f33103a39a673ac17ef147c`. Referências Mathlib relevantes foram preservadas e pinadas no relatório de verificação.

| Log autoral final aceito | SHA256 do JSON |
|---|---|
| AntilinearAdjointGraph_20260912_103611_347285.json | `5943e44fcd0d7ca222b1a34df9b19d67b33c7f53fe8e26c01fa205fcc8733a18` |
| ScalarTomitaAdjoint_20260912_104146_918776.json | `9d1ddfa794a8d57ff34db3882147146c8f5cf9606025763ceba994fd15fdf1fb` |

Os cinco logs JSON e seus streams foram lidos/preservados em [author_history.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/scalar_tomita_adjoint_independent_20260912_104520_672232/author_history.json>). Há três tentativas rc1: uma em `AntilinearAdjointGraph` (hD omitido do escopo do lema, metas excedentes/tipagem), duas em `ScalarTomitaAdjoint` (timeout de elaboração e simplificação da conjugação). Seus `sorryAx` são resíduos desses erros registrados, **não evidência aceita** e não achados pendentes das fontes finais. Só os dois logs finais rc0/fonte inalterada e as três execuções próprias finais sustentam esta conclusão; os 23 axiomas próprios coincidem com os finais autorais.

## Preservação e limites

Custódia antecessora lida e pinada: `closed_tomita_custody.json` SHA `3a2d5b8753b884965d000beb5a43a5eae59ebb3b81ccc2f037851b86f787a63c`; seu relatório de verificação, SHA `90dab0d890a0b074d2e9fe8f3f3bfc38a7df53d85035c26e11c03c59984b1dee`, declara rc0/30 pares de backup e prefixo. Conferi seu pin e os hashes dos três pareceres vinculados; **não reexecutei o verifier nem uma auditoria integral dos 30 backups**. Original relido `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`; cópia permanece `4309a3cc34b3e8360872e1c49ff78334c422359df1eb4cfa45890084abee15f8`. Os números 118 registros/75 controles/6456 Audit pertencem à custódia integrada anterior; os 23 DEV novos não foram somados a eles.

Foram preservados os hashes de todos os pareceres anteriores, inclusive `REVIEW_CLOSED_SCALAR_TOMITA.md`. Nenhuma fonte autoral, original, monólito, memória ou log foi alterado. Nenhum monólito, recorder, integrador ou teste autoral foi executado/importado. Todas as saídas estão em `revisao/`.

**Conclusão delimitada:** existe o adjunto antilinear máximo por pareamento de S no mesmo H_I; seu gráfico é fechado, seu domínio é denso, invariante e nele o adjunto é involutivo. Não são concluídos S†S, sua auto-adjunticidade/identificação modular, decomposição polar, KMS, igualdade I=n_ν, traço, Three Locks/H1–H3, promoção de gate ou runtime. **Nenhuma análise DEV necessária resta nestes dois módulos/23 alvos.**


## ADENDO DEV — composição S†S e auto-adjunticidade

<!-- DEV_TOMITA_SQUARE_REVIEW -->

2026-09-12T11:16:46-03:00. **[REAL — revisão DEV encerrada, sete módulos/53 alvos; nenhum achado P0, P1 ou P2.]** Este adendo incorpora os três auxiliares/12 alvos e os dois módulos concretos/18 alvos ao estrato anterior de dois módulos/23. As exclusões de S†S no texto anterior descrevem aquele escopo histórico; a composição e suas propriedades passam a ser conferidas aqui. O texto anterior permanece integralmente como prefixo de 11029 bytes, SHA `4250693ad95a4cd05b9662acf1589397dc1715678a7e38f2c8bbe9c27da57bf1`, com [backup imediato exato](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_SCALAR_TOMITA_ADJOINT.md.bak_20260912_111646_309867>).

**Resultado delimitado:** no mesmo `ScalarGNSHilbert P = H_I`, A é o `LinearPMap` complexo-linear **S†S**, com domínio exato **{x∈D(S) : Sx∈D(S†)}**. As provas fornecem sua simetria, positividade, sobrejetividade de I+A, domínio denso, auto-adjunticidade pelo adjunto máximo Mathlib, gráfico fechado e núcleo trivial. As hipóteses dos critérios genéricos são efetivamente demonstradas para esse A; não foram acrescentadas como premissas a P.

[AntilinearComposition.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/AntilinearComposition.lean:12>): a preimagem exige a pertinência efetiva a D e a imagem por S em E. A inclusão no domínio original preserva o vetor por `rfl` (linhas 32–39); a restrição da imagem usa o testemunho de pertinência. A composição na linha 45 cancela duas conjugações escalares, produzindo um mapa parcial complexo-linear no domínio inteiro dessa preimagem. Não se omite o domínio da segunda aplicação nem se prolonga S ao ambiente.

[ClosedAntilinearResolvent.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ClosedAntilinearResolvent.lean:18>): o gráfico é um submódulo **real** de `WithLp 2 (H×H)`, com a norma/produto interno de Hilbert do produto. O fechamento é transportado pela preimagem contínua de `ofLp` (linha 34). A única instância local nova é a canônica `InnerProductSpace.complexToReal` (linha 13); `CompleteSpace G` na linha 51 vem do fechamento do gráfico. Não há estrutura complexa fictícia no gráfico antilinear, nem completude postulada de um domínio não fechado.

[ClosedAntilinearResolvent.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ClosedAntilinearResolvent.lean:46>): a projeção ortogonal real de (z,0) produz **x∈D** e `Re⟨z−x,u⟩=Re⟨Sx,Su⟩` para todo u∈D. O auxiliar exige H completo e gráfico fechado; não exige D denso nem S limitado. No teste em iu (linha 68), S(iu)=−iSu. Se a=⟨z−x,u⟩ e b=⟨Sx,Su⟩, a identidade real testada dá −Im(a)=Im(b). A conjugação de b, junto da parte real, fornece exatamente **⟨Su,Sx⟩=⟨z−x,u⟩**, com a orientação necessária ao adjunto antilinear. Esse é um teste legítimo porque D é submódulo complexo.

[PositiveSurjectiveResolvent.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/PositiveSurjectiveResolvent.lean:17>): `hp` pede apenas **0≤Re⟨x,Tx⟩**; `hr` pede **∀z∈H, ∃x∈D(T), x+Tx=z**, sobrejetividade inteira. A densidade é deduzida: para v∈D(T)⊥, escrever v=x+Tx dá 0=‖x‖²+Re⟨x,Tx⟩, portanto x=0 e v=0. A completude permite passar do ortogonal trivial ao fecho total. A realidade completa do pareamento não é uma hipótese escondida desse lema de densidade; no critério de auto-adjunticidade a simetria é hipótese adicional explícita.

[PositiveSurjectiveResolvent.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/PositiveSurjectiveResolvent.lean:43>): a prova obtém primeiro a densidade e só então usa `LinearPMap.adjoint_isFormalAdjoint`, evitando a alternativa degenerada da definição Mathlib do adjunto quando não há densidade. Para a∈D(T*), resolve x+Tx=a+T*a. Testa contra cada b∈H, também escrito u+Tu; o pareamento do adjunto e a simetria dão ⟨a,b⟩=⟨x,b⟩. Assim a=x e Tx=T*a, isto é, **todo o gráfico de T*** está no de T, incluindo o domínio. A inclusão oposta vem de `hs.le_adjoint hd`. `isSelfAdjoint_def` conclui T*=T como mapas parciais. Não se confunde simetria num domínio prescrito com auto-adjunticidade, e não se pressupõe T fechado para obter esse resultado.

[ScalarTomitaSquare.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarTomitaSquare.lean:14>) especializa D, E e S literalmente nos objetos do primeiro estrato. `domain_iff` (linha 40) e `apply` (linha 45) são igualdades definicionais que explicitam o domínio e a aplicação S†(Sx). O pareamento da linha 50 vale para x∈D(A) e **todo y∈D(S)**: **⟨Ax,y⟩=⟨Sy,Sx⟩**. A simetria usa a conjugação correta dos produtos internos; a identidade quadrática é **Re⟨x,Ax⟩=‖Sx‖²** (linha 75), e o lema `positive` expressa sua não negatividade. Essa identidade, acompanhada da simetria provada, justifica a positividade do operador; não é apenas uma inferência a partir do nome do lema.

[ScalarTomitaSelfAdjoint.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarTomitaSelfAdjoint.lean:15>) fecha a passagem genérico→P: usa o fechamento **anterior de S** para obter x∈D(S) e o pareamento complexo da projeção. `scalarTomitaAdjoint_maximal P hx` fornece Sx∈D(S†) e S†Sx=z−x. O testemunho w da linha 22 está, portanto, no domínio exato de A. Isso prova I+A sobrejetivo sem pressupor densidade, fechamento ou auto-adjunticidade de A. Nas linhas 28–40, os critérios genéricos recebem a positividade, a sobrejetividade e a simetria já provadas para o **mesmo** A. O fechamento de A vem de `IsSelfAdjoint.isClosed` da Mathlib. Os tipos concretos impressos usam P, sem premissas residuais de resolução variacional ou auto-adjunticidade.

[ScalarTomitaSelfAdjoint.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarTomitaSelfAdjoint.lean:42>): Sx=0 implica x=0 pela involução anterior de S no domínio invariante. Se Ax=0, a identidade quadrática dá ‖Sx‖²=0, logo x=0 (linha 52). A conclusão é núcleo trivial. **Não fornece gap espectral, cota inferior uniforme positiva ou inversa limitada de A.** Também não afirma D(A)=H_I ou limitação de A/S.

Os tipos genéricos foram impressos com universos explícitos: H está em `Type` nesta implementação, não em um universo arbitrário reivindicado por extensão verbal. A aplicação concreta usa as estruturas de Hilbert herdadas do mesmo H_I. O grafo congelado de 406 módulos é acíclico, e nenhuma dependência anterior aos sete novos os importa. A prova gaussiana do primeiro estrato conserva sua proveniência: densidade do adjunto por T* e injetividade de T, sem inverter T, sem alterar Haar/medida e sem substituir I por n_ν.

### Recompilação própria e reconciliação de pins

| Fonte acrescentada | Alvos | SHA256 fonte | SHA256 .olean próprio = autor |
|---|---:|---|---|
| AntilinearComposition | 6 | `68f3ef51e3ea0c8334a9b3d2ca20aeecc16286807d1ac6067795cfc1c3d7eae6` | `75522b727ac319a06ac1b8371e6ea48909faf5520c7f74c486e1d98b872e1cca` |
| ClosedAntilinearResolvent | 4 | `78024edd14e15109b9c4587e512c70a8ae09dc5e796c8e793ce58e113972526e` | `1f25a2e15c722a30c98ea4e7713e78f16f9faa1d061e36fb1d71acd05c141b08` |
| PositiveSurjectiveResolvent | 2 | `e8fee08097f79b97e8d824d352c755983ae8b774a12fc37811c44a93b1883c89` | `b9ed179a325244578ba468a2a2ac2541b7a155d7bbf98bdc83dd9702db4e8ee0` |
| ScalarTomitaSquare | 12 | `a5fe02b5e2486cef5a3999bcfecffea33fd5bdb1a47a700880cfb2c50220dd31` | `670b55c8a75e933aa184ccee905e843b23c4161a3f90f57874f2bdd03aa1459b` |
| ScalarTomitaSelfAdjoint | 6 | `a36ada20b2a52ad6c3696abfa777fd8c708fb2b1d015d7e8632f447005a1b6f0` | `c25e688491d4afa663b020498e7a921c445e3293d51b0398f182c7a8d33eaea0` |

| Processo próprio acrescentado | rc | Segundos |
|---|---:|---:|
| TGLV350/AntilinearComposition.lean | 0 | 15.657 |
| TGLV350/ClosedAntilinearResolvent.lean | 0 | 18.29 |
| TGLV350/PositiveSurjectiveResolvent.lean | 0 | 16.147 |
| ResolventAuxAudit.lean | 0 | 15.283 |
| TGLV350/ScalarTomitaSquare.lean | 0 | 45.671 |
| TGLV350/ScalarTomitaSelfAdjoint.lean | 0 | 40.253 |
| TomitaSquareFullAudit.lean | 0 | 29.799 |

São **sete novos processos próprios rc0** neste adendo: três auxiliares e auditor/12, dois concretos e auditor cumulativo/53. Somados aos três processos do primeiro estrato, há **dez processos rc0: sete compilações de módulos e três auditores**. Os dois primeiros módulos não foram recompilados redundantemente na última árvore; seus binários próprios foram reutilizados, seus hashes foram relidos e todos os 53 tipos/axiomas foram auditados novamente em conjunto. **Os sete .olean próprios coincidem byte a byte com os sete finais autorais.**

O auditor final contém 53 `#check` com universos e 53 `#print axioms`, sem hipóteses acrescentadas. A cobertura coincide exatamente com o manifesto e as fontes; cada alvo depende somente de **propext, Classical.choice e Quot.sound**. Os 35 tipos dos auditores anteriores coincidem com os do auditor cumulativo, normalizando apenas espaços da impressão. Nenhum `axiom`, `sorry`, `admit`, `unsafe` ou alteração de redutibilidade/transparência foi encontrado no código das sete fontes. O auxiliar de instância real não é um alvo adicional contado; foi lido e fica incluído nas dependências transitivas dos teoremas auditados.

Evidências próprias: [compilação dos três auxiliares e auditor/12](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/resolvent_aux_independent_20260912_105957_572044/compilation.json>); [compilação dos dois concretos e auditor/53](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_square_independent_20260912_110352_968866/compilation.json>); [53 tipos e axiomas completos](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_square_independent_20260912_110352_968866/logs/TomitaSquareFullAudit.stdout.txt>); [verificação final e comparação de tipos/pins](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_square_independent_20260912_110352_968866/verification_dev.json>). Auditor final: fonte `82c55a7466de1fc69a13a3143b807db89e676e25433d3711b7e366e5dbbc5e67`, binário `300eb330a755dcffe4a0819dbe93b3057b170c32debbbd0422c9db20c66e4d8b`, stdout `2ef8123c994197e57ae904b02c6a81e340538b9622ee44d536162bcc166de27d`. O manifesto [da árvore final](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_square_independent_20260912_110352_968866/manifest.json>) pina 404 dependências próprias de projeto, inclusive os cinco módulos já recompilados nas duas árvores precedentes. O auxiliar usou apenas uma dependência de projeto própria, `AntilinearAdjointGraph`; o restante veio dos oito pacotes externos somente leitura. **Nenhum build autoral de projeto integra o LEAN_PATH.**

O compilador é o mesmo já pinado no primeiro estrato, SHA `9b216deb50d37c32c829d1efaaa5bafd5560417d382df35a815489e31a31593f`. Pacotes e dependências anteriores não foram recompilados nem receberam nova certificação global; mantêm-se os limites de proveniência anteriores, inclusive a errata histórica exclusivamente de comentário de `DualSemifiniteIdeal`. Os fontes/binários congelados foram reconferidos. As referências locais primárias da Mathlib sobre `LinearPMap`, adjunto máximo, projeção, produto L² e restrição ℂ→ℝ estão copiadas e pinadas em `mathlib_references` da árvore final. A única falha de preparação própria ocorreu **antes de executar Lean**, por o inventário de declarações ler a palavra `structure` dentro de comentário; foi corrigido somente o parser do revisor. A tentativa e a correção permanecem preservadas em `revisao/resolvent_aux_independent_20260912_105904_319758/preparation_failure.json` e nos scripts/backups próprios. Não é falha da fonte final nem processo Lean rc1 omitido.

| Log autoral final acrescentado | SHA256 do JSON |
|---|---|
| AntilinearComposition_20260912_104911_690291.json | `a959cf4ae33fe5fae1557464c1d6ae6b8cc74fc1ad245553057e896fb6342335` |
| ClosedAntilinearResolvent_20260912_105618_331202.json | `b677342dead94505d397578719c107b33a218c356dcd9de0e6c9772ba22c4b2b` |
| PositiveSurjectiveResolvent_20260912_105619_781262.json | `72d971fd6265942142091a7f6e810414d0c6f8f899e1a60eec409bd8550baf9b` |
| ScalarTomitaSquare_20260912_105822_725293.json | `ef04d6783278aa10f5ec776d7fd61150f4d7d8f7b3b0c417107592afa0cd1920` |
| ScalarTomitaSelfAdjoint_20260912_105946_717528.json | `f4f50fe0cecb73d12a1dc90d9760baa867f131ec5e5a8319113e5ca042708746` |

Os três `author_history.json` das árvores próprias preservam **18 tentativas: 7 rc0 finais e 11 rc1 históricos**. Seus JSONs e streams foram relidos por hash. Os erros anteriores são de elaboração, instâncias/simplificação e limites de heartbeats; eventuais `sorryAx` nesses outputs fracassados não são aceitos como prova. A conclusão usa exclusivamente as fontes finais, seus sete logs rc0 coincidentes e a recompilação própria. Nenhum erro histórico foi apagado nem tratado como achado pendente sem correspondência na versão final.

### Documentação, preservação e alcance final

Lidos integralmente e conciliados: `tomita_square_draft_status.json`, SHA **`e46bfab305e6acd956ce268bd55f3944bcb81ddd2c9cad16b761af65735e016c`**, e `RELATORIO_ADJUNTO_QUADRADO_DEV.md`, SHA **`ca29180ef7b6025361cc07337a8794a8f777dab92ee493d9a1e97a400769e2bf`**. O hash do relatório coincide com o pin do manifesto. O texto distingue domínio exato, mesmo H_I, passagem pelo gráfico real, auto-adjunticidade deduzida e núcleo trivial sem gap. **Nenhum P2 documental encontrado.**

Original relido `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`; cópia relida `4309a3cc34b3e8360872e1c49ff78334c422359df1eb4cfa45890084abee15f8`, ambos coerentes com a custódia antecedente. **Esta é revisão DEV, sem exame de nova integração.** Os 118 registros/75 controles/6456 Audit mencionados no estrato anterior pertencem à custódia precedente; não se somam os sete/53 a essas contagens. Não executei novos testes autorais, raízes, monólito, integrador, recorder ou verifier. Todas as escritas ficaram em `revisao/`; os demais pareceres, fontes autorais, originais, logs e memórias foram preservados.

**[OPEN — fora deste resultado]** Raiz positiva e decomposição polar deste S†S no mesmo H_I, identificação modular do peso, ponte de domínio/núcleo envolvendo n_ν, KMS, traço e escala dual, Three Locks/H1–H3, física, certificado consumido pelo gate e runtime. Nada no pacote fornece gap ou altera essas flags. **Não resta análise DEV necessária dentro dos sete módulos/53 alvos; o escopo delimitado está encerrado.**


## ADENDO — conferência da integração dos sete módulos/53 alvos

<!-- INTEGRATED_TOMITA_SQUARE_REVIEW -->

2026-09-12T11:36:38-03:00. **[REAL — inspeção integrada encerrada; nenhum achado P0, P1 ou P2 novo.]** Foram conferidos exclusivamente os mesmos sete módulos/53 alvos do parecer DEV, as duas raízes, seus registros, a transposição, a AST, os controles e os dois scripts prospectivos de registro/custódia. **Nenhum processo Lean ou teste autoral foi executado neste adendo.** A matemática e as dez execuções próprias DEV já documentadas permanecem a evidência independente de recompilação; a integração abaixo é sustentada pela inspeção própria dos bytes e pela releitura dos resultados executados pelo autor.

O prefixo anterior foi preservado integralmente: 26219 bytes, SHA `635dfa3adc294ab7af8939e0318d0d971b28848d1608495e0a8dfc50a3c1549c`, com [backup imediato de bytes](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_SCALAR_TOMITA_ADJOINT.md.bak_20260912_113638_196801>). Nenhum parecer custodiado anterior foi alterado.

**Snapshot conferido:** cópia **`77ddd4dd8d5a012e8a44b59e00f4eaf6b9958ce5c6ee1f74fae27b2085179632`**, antecessor **`4309a3cc34b3e8360872e1c49ff78334c422359df1eb4cfa45890084abee15f8`**, original **`c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`**. O original e a cópia-base local concordam com o pin antecedente. A cópia antecessora foi localizada pelo hash em backup real e comparada por AST, sem executar/importar nenhum dos monólitos.

### Transposição, mesmos objetos e integração

Nas sete fontes, a substituição literal de bytes `^import TGLV350.` por `import TGLExt.V350` reproduz **exatamente** o arquivo integrado. As fontes DEV coincidem com os pins aprovados. Cada valor embutido corresponde aos bytes da fonte integrada. Não houve mudança de enunciado, hipótese, namespace de declaração, corpo de prova, instância, definição de domínio ou representação: os nomes permanecem `TGLV350.Regular.*`, e S, S†, A e H_I continuam os objetos do parecer DEV. A leitura não reclassifica a auto-adjunticidade como identificação polar ou modular do peso.

O dicionário passa a **827 arquivos**, com exatamente sete entradas adicionadas e nenhuma removida. Entre as entradas preexistentes, somente `TGLExt.lean` e `TGL/Audit.lean` mudaram. Cada raiz importa os sete módulos uma vez; o Audit acrescenta exatamente **53** `#print axioms`, preservando todos os alvos antigos e suas multiplicidades. Os diffs estão em [TGLExt](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_square_independent_20260912_110352_968866/integrated_20260912_113250_461146/TGLExt.lean.diff.txt>) e [Audit](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_square_independent_20260912_110352_968866/integrated_20260912_113250_461146/TGL_Audit.lean.diff.txt>). Não há inclusão de módulo posterior neste conjunto.

**AST Python fora de `_EMBEDDED_KERNEL_FILES` idêntica ao antecessor**, com hash da AST normalizada `c240ac1eb2d27fb2d2d388fac24dc0387d8f352ceae2e72a7ab6a50fec3dd617`. `gate_extension.py` coincide byte a byte com o artefato pinado na custódia antecedente. As alterações estáticas dos helpers são delimitadas: sete nomes na lista do integrador, sete módulos na lista de compilação, atualização da contagem cumulativa de seu lote anterior de 99 para 152 (=99+53) e duas entradas no dicionário de controles. Isso não significa 152 alvos novos nesta revisão.

### Resultados autorais relidos e pins medidos

**125 registros rc0 = 116 herdados + sete módulos novos + duas raízes novas.** Os 116 mantêm os mesmos hashes de fonte e binário da captura custodiada; não são 125 recompilações novas. Para todos os 125, conferi fonte, .olean, JSON individual coincidente com o registro e os streams preservados. Nos nove novos, os logs declaram também `lean_returncode=0` e `source_unchanged_during_compile=true`; não há warnings nesses outputs. O mecanismo de cache segue o estrato anterior: hashes de fonte/binário e frescor dos imports locais, sem rebuild dos pacotes.

| Fonte integrada recompilada pelo autor | SHA256 fonte | SHA256 .olean relido |
|---|---|---|
| TGLExt/V350AntilinearAdjointGraph.lean | `6a3cbe3ded292e347a885be00be565c6b030d6971a7ac035096966028a552e98` | `fc40b032c56f26893a1c1bdf6f6d65e157fd391799d22643b768cea6ea6cee33` |
| TGLExt/V350ScalarTomitaAdjoint.lean | `be788eff71d166991b356d5d780825238e272c1c824bfe9857b4492cbfd04968` | `cf74990e5e1079ebc286906f3e67e61e1cc1d62e47aa7d34d817adbd79a1b6c8` |
| TGLExt/V350AntilinearComposition.lean | `521e97302de691528b2b85e0a6e9eec0920533ebd370b55f64e3703172ba65b7` | `778f06a35ccd7e5f83482494b6c735a6b67de1431e29a8cb8c0ae09e5e9dd3a4` |
| TGLExt/V350ScalarTomitaSquare.lean | `ca781e13f5857fcb348fd2cc1e68a2fb3397ae352b168e9ba9a6425517634a2a` | `fd379a3c7681b59b6fee509951165c2efdb901616b16d51a8f03338aeaaee9a3` |
| TGLExt/V350ClosedAntilinearResolvent.lean | `f1af44b5212378f0c5b8a4535258c4fc6f07ea8445a9278f7b3b5005a8a9a633` | `1771c37d1f348ea20a5f5318d93ace54598292624f54797d2887e66b0d437abf` |
| TGLExt/V350PositiveSurjectiveResolvent.lean | `cda1cc7ef883c273d58bbf83524b31837509f8dc9a6a2df28bd77fae7ee0821b` | `c275ac98335d5b213095d2b3513ca38898e2cfb72328a6a9524e87722b531d86` |
| TGLExt/V350ScalarTomitaSelfAdjoint.lean | `2dbdfdaa1f1383036a2e0954347058d32de7c8343942a3ca15f5c81e30266af0` | `615a10ea865a567fc15117ffd1234667941868442fc4717a9a12acd87218d947` |
| TGLExt.lean | `8061c5776d98a3c5caaf7e56af6cd1a2f9bf422d18379b5608549e2ec83116aa` | `0b51c1c69919787a94507ef9a0b83af71d3a012f4311af24ec7e7bc3629e2597` |
| TGL/Audit.lean | `abcc0f4b2769497b152f5c6f8e4a8fb5468b79b64ddea37b34ac05e5e73cd3f0` | `a0563607faf338d53ece922469d5234c7448c561eb43955366bb95f9006ce4a8` |

| Log final autoral | SHA256 JSON |
|---|---|
| V350AntilinearAdjointGraph_20260912_112020_694574.json | `be748d1291a63be7354b14cab88c2d9e14aa5c61e6af7ce7ca58b2236ab71cb2` |
| V350ScalarTomitaAdjoint_20260912_112033_811467.json | `aa8d646476ed97818db4c8a81afac84c2fd37bd5815111e92ae43e6c3684d27f` |
| V350AntilinearComposition_20260912_112135_861682.json | `aa34c9ea1d174038a967a7afb109477e5f257e5c54c4c8b9f48da85bacc29b5d` |
| V350ScalarTomitaSquare_20260912_112148_375726.json | `9e147e2e4015d02ebe71d59787faf3cc0802503792527a09d180fd55de1ceb39` |
| V350ClosedAntilinearResolvent_20260912_112231_616345.json | `66d4c664de6cd00190f656934a95b81401448a0ac462e023f15a3ff63926ca52` |
| V350PositiveSurjectiveResolvent_20260912_112246_479741.json | `af652e379a192fdc45c15e6e227f4fa21efa72eac382204bf4698c4195dcf137` |
| V350ScalarTomitaSelfAdjoint_20260912_112302_099936.json | `30039f7ec48d0b20e26c2094db20bf1c79a237528545719c432c35cb7d87c0e2` |
| TGLExt_20260912_112340_413502.json | `e4c9434e79367d76f5af4afcc34ff28915d56a787a76166a979ba47e9dca6953` |
| Audit_20260912_112411_517888.json | `7abb9b65572b36365a48ace2b7225eceaee25001741955208e5a246719484a2b` |

O stdout final de `TGL/Audit.lean`, SHA **`cf6fd894533b06a506b79b4f54a0344ca05a676307aa109f78a3cf55e243ff72`**, foi analisado diretamente: **6509 declarações distintas**, sem axiomas fora de `propext`, `Classical.choice`, `Quot.sound`. O seu mapa coincide com `kernel_incremental_evidence.json`; o incremento em relação ao Audit anterior é exatamente o conjunto dos **53 alvos**, cujos axiomas coincidem também com o auditor DEV próprio. Os axiomas antigos permanecem iguais. Isto confere as declarações e axiomas integrados, apoiado na transposição literal dos tipos já impressos; **não houve novo `#check` ou nova compilação própria de raízes/integrados**.

**77/77 controles constam aprovados nos registros autorais**, com os 75 anteriores preservados. As duas entradas novas testam presença dos respectivos teoremas, as seis flags falsas e ausência de alteração do gate/plano: `maximal_antilinear_adjoint_does_not_discharge_KMS_trace_or_physical_frontier` e `positive_selfadjoint_Tomita_square_does_not_discharge_KMS_trace_or_physical_frontier`. Removidas somente essas duas entradas do dicionário da versão atual, a AST inteira de `test_gate_extension.py` coincide com a anterior. O corpo do laço e as condições antigas não mudaram. Uma primeira comparação própria exigiu indevidamente o mesmo nó inteiro do laço e interrompeu a inspeção; o diff mostrou apenas essas duas entradas, o comparador foi corrigido e a captura concluída. A interrupção está preservada, sem ser tratada como defeito autoral nem como teste Lean fracassado.

**As seis flags maiores são False** (`qgf_continuous_modular_realization_constructed`, `qgf_unconditional_continuous_corner_proved`, `qgf_full_TGL_witness_constructed`, `gpf_H1_internal_susy_relative_gap_discharged`, `gpf_H2_smooth_modular_four_frame_discharged`, `gpf_H3_local_horizon_equilibrium_discharged`). `frontier.legacy_gate_changed=false`, `frontier.full_plan_complete=false`, `full_monolithic_runtime_run=false`; o valor textual do gate legado também coincide com o antecedente. Nenhum certificado novo é consumido pelo gate.

**Limite de proveniência herdado:** `audit_stdout_sha256` e `audit_capture_sha256_full` no objeto global `kernel_incremental_evidence.json` continuam iguais ao estrato anterior (`8bc3e69e0bad91bfe9e07bb1c516d8bca5a54fb790edadbe2fa5c6f818402fe1`); não são o hash do stdout incremental atual. Para esta rodada, a cadeia usada foi o **log específico final de Audit → stream relido → 6509 axiomas**, e não aqueles campos históricos. Os metadados globais herdados não foram promovidos a evidência de rebuild completo da base. Também não foi refeito o inventário I/O histórico, a auditoria de todos os pacotes ou qualquer runtime.

### Scripts e minuta de custódia — inspeção integral, sem execução

Li as **211** linhas de [record_tomita_square_progress.py](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/record_tomita_square_progress.py>) e as **78** linhas de [verify_tomita_square_custody.py](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/verify_tomita_square_custody.py>), inclusive toda a minuta interpolada e o adendo de memória. A sintaxe AST é válida. As contagens são coerentes: grupos `adjoint=23`, `composition=18`, `resolvent=6`, `selfadjoint=6`, total **53**, sem alvo 55 ou módulo futuro contado. O texto mantém domínio exato, mesmo H_I, densidade/sobrejetividade/auto-adjunticidade deduzidas, núcleo trivial sem gap, ausência de I=n_ν e estatuto aberto de polar/KMS/traço.

O recorder exige `--review-read` e o marcador deste adendo (linhas 62–71), verifica original/cópia/custódia anterior, AST, registros, transposição, axiomas e flags antes de escrever o relatório. **32 superfícies distintas existentes** são calculadas nas linhas 178–180: as 30 da custódia anterior mais `RELATORIO_TOMITA_FECHADO_INTEGRADO.md` e `ROTA_APOS_TOMITA_FECHADO.md`. Não incluem pareceres em `revisao/`. A lista e seus hashes de leitura estão na verificação própria; esses hashes são um retrato da inspeção, não uma exigência de imutabilidade das memórias compartilhadas até a execução futura.

O mecanismo das linhas 26–53 lê o estado imediato, cria backup com `xb`, compara seus bytes, grava temporário, verifica bytes/tamanho, reconfere o estado esperado e só então substitui. O append conserva o prefixo e cresce; a custódia registra o hash do backup efetivamente tocado e eventuais mudanças intervenientes desde o antecessor. O verifier (linhas 29–39) confere os hashes das superfícies, o prefixo estrito, o backup imediato e a classificação das mudanças intervenientes; depois confere binários/registros, controles, alvos e flags. Sua própria saída também usa backup e substituição por temporário (linhas 63–77). **Trata-se de 32 backups/prefixos previstos e mecanismo inspecionado, não de custódia executada/verificada por mim.** Na leitura, os novos relatório integrado, custody e verification ainda não existiam.

A referência a `ROTA_POLAR_MESMO_GNS.md` aparece como **rota posterior, sem prova nova**. Não examinei sua matemática nem qualquer fonte posterior; nenhuma entra na conclusão. O pin do inventário I/O no recorder é apenas transporte documental de artefato histórico e não liberação de runtime. Não houve achado documental P2 neste escopo.

| Artefato lido e congelado na revisão | SHA256 |
|---|---|
| integration.json | `a4f9bfb9d91fc56644b4488ff7b7cc0e7ac68a6098f0bfdf7f5973686d4c4b01` |
| integrated_compile.json | `67c79de47c16a2e167e70d5400d96fcd33b22e65c16fca4c49a790515e153ea4` |
| gate_tests.json | `ab6b03a28f34c7e4f55de759a2f5ba68d97f5344c2bad74a24d5ca3e799057ef` |
| kernel_incremental_evidence.json | `3281510b4791c61f26505b1652f278adf138081c102b2218028f004b70202199` |
| gate_extension.py | `c819810b5540747f0a0b7b07b36bb9d7f5e9dd868192ad7410ea15829c566a9e` |
| record_tomita_square_progress.py | `92b507c84367964c85d2e3a988f249655481942b3965c4b93812636c7f52e8eb` |
| verify_tomita_square_custody.py | `f3c9d5d07d5ef1a276b9e83234b9bb9fc6c16363b214e257b732bb7bcfdba9fc` |

Captura e verificações: [verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_square_independent_20260912_110352_968866/integrated_20260912_113250_461146/verification.json>); [axiomas extraídos do Audit final](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_square_independent_20260912_110352_968866/integrated_20260912_113250_461146/axioms.json>). A captura guarda os scripts lidos, fontes integradas, JSONs e streams, com hashes. Os pins do compilador, dependências próprias e limitações binárias do DEV permanecem nos estratos anteriores; esta inspeção não os recompilou.

**Conclusão integrada delimitada:** transposição e evidências conferidas para os sete/53, sem P0–P2 e sem análise necessária pendente neste adendo. Permanecem os limites DEV: núcleo trivial não é gap; nenhuma identificação polar/modular do peso, KMS, traço, Three Locks/H1–H3, física ou runtime completo. Não houve execução/importação de monólito, scripts autorais, recorder ou verifier; fontes e memórias ficaram intactas e todas as saídas próprias estão em `revisao/`.
