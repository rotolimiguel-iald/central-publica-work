[REAL — B6 pago como proposta documental tipada e auditoria de dez declarações existentes. Zero teoremas novos; hipóteses importadas e aberturas preservadas. Integração pela gerência.]

# ENTREGA 012 / B6 — importações, entradas e limites da passagem

2026-09-14T17:29:29.848254-03:00

**B6 acrescenta documentação de escopo e referências; não acrescenta matemática.** O auditor consulta oito teoremas e duas estruturas já construídos. A proposta JSON tem quatro referências externas com imported_into_witness=false e onze linhas de estatuto. Não foi instalada no um.py.

## Critérios da ordem

| Critério B6 | Resultado |
|---|---|
| Ficha anterior ao artefato e reaproveitamento | PAGO; dez fornecedores existentes, MD/JSON anexos; seis modalidades de busca com recortes e falhas de acesso preservados. |
| Quatro referências, exact_role e importação false | PAGO; proposta JSON com validação de esquema e campos. Leitura parcial da literatura discriminada abaixo. |
| H3 importado | PAGO como estatuto, **não como construção de H3**. the_trio_is_a_pair exige imported:H2→H3. |
| Escala de área INPUT | PAGO; newtonPlanck_equivalence e halfNat_over_two_faces_eq_quarter conferidos. Nenhum G determinado pelo kernel. |
| H_nx e w_i constante nomeados | PAGO; SectorFluid registra ambos; H_nx não foi deduzido microscopicamente. |
| Lema3 global OPEN | PAGO como delimitação; nenhuma prova local→global adicionada. |
| TGL-S versus TGL-L OPEN | PAGO como delimitação; não foi construído ou escolhido fechamento perturbativo. |
| Correções B4 preservadas | PAGO; raio no fluxo, termo Φ', suporte de densidade para igualdade, E≠0 para unicidade e constante explícita. |
| Lake próprio e axiomas | PAGO; auditor autoral e reprodução independente rc0, dez nomes existentes no trio ou sem axiomas. |
| Integração / gate / dados | NÃO EXECUTADOS, fora do escopo: proposta aditiva para gerência; campos não alterados. |

## Tabela final de estatutos

| Item | Estatuto | Fornecedor | Condição |
|---|---|---|---|
| H3: equilíbrio local | IMPORTED | `TGLExt.the_trio_is_a_pair` | A implicação imported:H2->H3 precisa ser fornecida; o teorema é modus ponens, não demonstra H3. |
| Escala de área / G | INPUT | `TGL.AreaScale.newtonPlanck_equivalence` | G>0 medido/calibrado, eta=1/(4G). Nenhum valor de G derivado. |
| Não-troca e w_i constante | INPUT | `ChatgptAudit.FLRW.SectorFluid` | H_nx é campo HasDerivAt; w_i tem somente índice de setor. |
| Entropia diferencial modificada | INPUT | `ChatgptAudit.FLRW.HubbleHorizonInput` | differential_entropy é explícita. S=A/(4G Phi(t)) exige o termo de Phi-prime e não é equivalente em geral. |
| Fator total e fator setorial | REAL | `ChatgptAudit.FLRW.the_two_routes_differ` | Teorema condicional; densidade positiva, entalpia não negativa, H_nx onde aplicável. Nenhuma rota ratificada por esta entrega. |
| Unicidade Phi_flux | REAL | `ChatgptAudit.FLRW.the_entropy_factor_that_reproduces_the_sector_closure` | Entalpia total diferente de zero. No fluxo zero não há fator único. |
| Constante de integração | INPUT | `ChatgptAudit.FLRW.tgl_friedmann_zero_cosmological` | O caso sem constante exige H_zero_cosmological; o resultado geral mantém Lambda/C. |
| Lema3 global | OPEN | `ORDEM_012 §0 e B6(d)` | Nenhuma identificação local-global provada nesta ordem. |
| TGL-S versus TGL-L | OPEN | `ORDEM_012 B6(e); RhoPlusPClosure` | Fechamento perturbativo não construído e não escolhido pela bancada. |
| Valor físico de beta | INPUT | `TGLExt.TGLCoupling` | O kernel usa beta variável em(0,1); a forma alpha=beta/exp(1/2) não deriva CODATA. Runtime não foi executado. |
| Ângulo na métrica | REAL | `ChatgptAudit.FLRW.the_angle_reaches_the_metric` | Somente reescrita sin²(thetaMiguel beta)=beta; não acrescenta variável ou observável ao motor. |

Na linha da constante, INPUT qualifica **a escolha do caso sem constante**: a existência de Λ/C já é conclusão dos teoremas gerais, e eliminá-la exige uma condição adicional. Nas linhas REAL, o estatuto é da implicação formal com as hipóteses indicadas, não da ocorrência física de seus antecedentes.

## Referências e papel exato

**Jacobson local horizon thermodynamics (1995)** — [T. Jacobson, Phys. Rev. Lett. 75 (1995) 1260, doi:10.1103/PhysRevLett.75.1260](https://arxiv.org/html/gr-qc/9504004). Motiva a implicação termodinâmica local sob equilíbrio, lei de área, temperatura e balanço para horizontes de Rindler. Não fornece por si a hipótese H3 da realização escolhida nem a correção Phi_TGL. Leitura: Texto primário HTML, hipóteses locais e argumento termodinâmico lidos. `imported_into_witness: false`.

**Cai-Kim apparent-horizon Friedmann route (2005)** — [R.-G. Cai & S. P. Kim, JHEP 02 (2005) 050, doi:10.1088/1126-6708/2005/02/050](https://arxiv.org/html/hep-th/0501055). Prescrições de horizonte aparente, calor A(rho+p)H*r_A dt e T=1/(2pi*r_A), com r_A=1/H no caso plano. A lei de entropia modificada é entrada TGL separada; o raio não pode ser omitido. Leitura: Seção2 primária lida, eqs.2.3,2.12–2.17 e discussão da temperatura dinâmica; convenção qdot=-dE/dt do artigo. `imported_into_witness: false`.

**Padmanabhan thermodynamical aspects of gravity (2010)** — [T. Padmanabhan, Rep. Prog. Phys. 73 (2010) 046901, doi:10.1088/0034-4885/73/4/046901](https://arxiv.org/html/0911.5004v2). Referência de enquadramento da relação entre dinâmica gravitacional e termodinâmica de horizontes. Não é uma premissa adicional que fixe Phi, G ou escolha entre rotas. Leitura: Resumo e trechos introdutórios primários; não se alega leitura integral das85 páginas. `imported_into_witness: false`.

**Gibbons-Hawking cosmological horizon thermodynamics (1977)** — [G. W. Gibbons & S. W. Hawking, Phys. Rev. D 15 (1977) 2738, doi:10.1103/PhysRevD.15.2738](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.15.2738). Origem da temperatura/termodinâmica do horizonte cosmológico no regime considerado. Sua extensão a um horizonte FLRW dinâmico em B4 é a prescrição explícita de Cai-Kim, não um teorema geral deduzido desta citação. Leitura: Metadados e resumo oficiais lidos; PDF oficial respondeu401. Leitura integral não realizada. `imported_into_witness: false`.

O campo KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED qualifica essas referências bibliográficas, não rebaixa os teoremas condicionais efetivamente provados em B2–B5. A extensão modificada da entropia é entrada da TGL; nenhuma citação acima a prova. Temperatura FLRW dinâmica é uma prescrição explicitada em B4, não consequência irrestrita da referência de 1977. O PDF oficial dessa referência retornou 401; a proposta não mascara a leitura parcial.

## Reprodução e alcance

Na bancada `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA`, `run_b6_lake.py` invoca `lake build TGLExt.AuditPassageScope` na raiz kernel. Run `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\attempts\20260914_170651_058055\run.json`, rc0, 8689 jobs, fontes idênticas antes/depois. `audit_b6.py` executou o auditor por `lake env lean`, conferiu os dez nomes, o esquema documental, as quatro importações false e a preservação das 941 fontes-base e do um.py copiado.

Revisão independente: run `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b6\independent_20260914_172114_917733\run.json` e compilation JSON pinados. Usa sua própria raiz s, sem cópia de objetos do projeto autoral, com auditor próprio de tipos/axiomas. Mathlib e oito pacotes são caches herdados/pinados, não reconstruídos. Foram 19 fornecedores recompilados e dois auditores: 21 objetos novos, 141 no total privado. **Há diferença binária em três fornecedores — MixedLadder, SecondCone e AreaScale — embora fontes, .ilean e C gerado coincidam.** A causa de serialização não foi estabelecida; o aceite usa rc0/tipos/axiomas, sem alegação de igualdade binária integral. AuditPassageScope e outros 16 objetos coincidem com o autoral. A primeira finalização recusou a alegação mais forte e foi preservada. Nove avisos herdados permanecem; nenhum nos auditores B6. O parecer integral e binary_reproducibility_limit.json delimitam o alcance; não se confunde auditoria documental com integração no runtime.

Não foram inventados novos testes negativos para uma bibliografia. As paredes matemáticas pertinentes já foram auditadas em B4 e seus tipos foram relidos aqui; o modo importado também contém a parede existente the_pair_still_needs_its_hypotheses. Não há nova prova de existência do horizonte, traço ou testemunha global. Falhas de acesso nas buscas foram repetidas em leitura autorizada e registradas; o 401 bibliográfico permanece como limitação. Logs de avisos herdados de fornecedores não foram apagados; nenhum aviso novo é atribuído ao auditor B6.

## Axiomas dos dez nomes EXISTENTES

| Alvo | Axiomas |
|---|---|
| `TGL.AreaScale.newtonPlanck_equivalence` | propext, Classical.choice, Quot.sound |
| `TGL.AreaScale.halfNat_over_two_faces_eq_quarter` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.SectorFluid` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.HubbleHorizonInput` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.variable_entropy_derivative` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.the_two_routes_equal_iff` | propext, Classical.choice, Quot.sound |
| `ChatgptAudit.FLRW.zero_flux_has_no_unique_factor` | propext, Classical.choice, Quot.sound |
| `TGLExt.the_trio_is_a_pair` | nenhum |
| `TGLExt.the_pair_still_needs_its_hypotheses` | nenhum |
| `TGLExt.discharge_by_import` | nenhum |

## Arquivos e hashes lidos

| Arquivo | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\AuditPassageScope.lean` | `cbf0ff8d70b98d56aa229dea2392c98f5c8b387580bf4a0cc0aa97941c97b4d2` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\REAPROVEITAMENTO_B6.md` | `f657122a890f798429e5d633f5155c5936265607708428c49e7ab789106d3d55` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\REAPROVEITAMENTO_B6.json` | `b252cc0dbf00d0d79d0f042961e14bf77e85f60ee141f641129b4f1b7022e697` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\PROPOSTA_EXTERNAL_KNOWN_THEOREMS_B6.json` | `42eb7f61c444f84fe22434e1a4dd9f99970db9017a0203d15c9802f4bd4d28f6` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\VALIDACAO_DOCUMENTAL_B6.json` | `e6313bb164aa226084bc017d8ac6dd70f8159d0f103143dbde44d08a99bad2e5` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\AUDITORIA_B6.json` | `93158a14a6bf82ab4104a866c41469cd003f979fbed2194c82137629c4abe227` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\ALVOS_B6.json` | `235109fc6c1d7fe8e0f08856a1368e7c2e3e2daf1b9068899f72a05fbafa8c02` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b6\REVIEW_B6_FINAL.md` | `86361d053273bd18cfc2ac41394be9437dcf0d24185ab9b36720a7d87cc1ce48` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b6\REVIEW_B6_FINAL.json` | `6caa0786bd0544967d2f84aaf40d5498c0e0e86a98925e83d34b0fbcee0b99ff` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\revisao_b6\compilation.json` | `f19d2e229a7f0fb3a045da7b3bdea8a1e266ea0285cefc632f3cee6548ae336a` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\run_b6_lake.py` | `d9ed8ecd55105de0423ef61b26c79ba2bcc172691eb97baaba1f99ba9911036c` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\audit_b6.py` | `15f59569f88a8ce1d5a103c20b6de9b152d275a9d7c200abbf024f3b775be577` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\prepare_b6_ficha.py` | `96a05419b673fd54f334eae4a311fc135fdd744085aeafdc515a3f405b20fb33` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\prepare_b6_scope.py` | `c1cb82f8e84d9af6d4e09086e0b32af00f1314e2892f9bc3dc5d5e8ad3dae12d` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\deliver_b6.py` | `1225248e0d07205ade88054e2e8d4b1bfb9552e8e86f4a8c405065f4e36a4e65` |

MANIFESTO_B6 e RECIBO_B6 vinculam este documento à proposta, fontes, objetos e duas auditorias. As entregas B1–B6 encerram os seis deltas desta ordem na bancada, com as correções de B4. A gerência ainda incorpora e audita a integração. A1(b) da ORDEM 011 retoma após esta entrega; seu traço concreto permanece pendente.

## Parecer independente integral

# B6 — revisão independente documental final

2026-09-14T17:28:31.824555-03:00 · **B6_SCOPE_REVIEW**

[REAL] **Aceito no escopo B6, sem P0, P1 ou P2.** Ficha MD/JSON, proposta, validação, auditor e tipos dos fornecedores conferidos. A reprodução Lake própria terminou rc0 e auditou **dez declarações EXISTENTES: oito teoremas e duas estruturas; zero teoremas novos**. A proposta permanece documental, **não instalada no witness ou no runtime**.

## Tipos e alcance

`the_trio_is_a_pair` recebe `master : H1 ∧ H2 ∧ H3 → P` e `imported : H2 → H3`; `discharge_by_import` aplica uma implicação já fornecida. Nenhum deles constrói a premissa física H3. `the_pair_still_needs_its_hypotheses` preserva justamente a insuficiência da implicação desacompanhada das hipóteses. Os três não dependem de axiomas; os outros sete usam somente **propext, Classical.choice, Quot.sound**, com universos normalizados no parser próprio. “all_trio” foi interpretado como subconjunto permitido, não como presença obrigatória dos três.

`AreaScale` fornece identidades de normalização, sem medir/derivar G. A identidade total de divisão, inclusive sua elaboração em G=0, não constitui calibração física; a interpretação usa G>0. As estruturas `SectorFluid` e `HubbleHorizonInput` mantêm H_nx e a lei diferencial de entropia como campos de entrada. A derivada do quociente contém Phi′. A igualdade das rotas usa suporte de **densidade positiva**, incluindo vácuo quando aplicável, e a unicidade do fator de fluxo exige entalpia total não nula.

## Onze estatutos conferidos

| # | Item | Estatuto | Condição mantida |
|---|---|---|---|
| 1 | H3: equilíbrio local | IMPORTED | A implicação imported:H2->H3 precisa ser fornecida; o teorema é modus ponens, não demonstra H3. |
| 2 | Escala de área / G | INPUT | G>0 medido/calibrado, eta=1/(4G). Nenhum valor de G derivado. |
| 3 | Não-troca e w_i constante | INPUT | H_nx é campo HasDerivAt; w_i tem somente índice de setor. |
| 4 | Entropia diferencial modificada | INPUT | differential_entropy é explícita. S=A/(4G Phi(t)) exige o termo de Phi-prime e não é equivalente em geral. |
| 5 | Fator total e fator setorial | REAL | Teorema condicional; densidade positiva, entalpia não negativa, H_nx onde aplicável. Nenhuma rota ratificada por esta entrega. |
| 6 | Unicidade Phi_flux | REAL | Entalpia total diferente de zero. No fluxo zero não há fator único. |
| 7 | Constante de integração | INPUT | O caso sem constante exige H_zero_cosmological; o resultado geral mantém Lambda/C. |
| 8 | Lema3 global | OPEN | Nenhuma identificação local-global provada nesta ordem. |
| 9 | TGL-S versus TGL-L | OPEN | Fechamento perturbativo não construído e não escolhido pela bancada. |
| 10 | Valor físico de beta | INPUT | O kernel usa beta variável em(0,1); a forma alpha=beta/exp(1/2) não deriva CODATA. Runtime não foi executado. |
| 11 | Ângulo na métrica | REAL | Somente reescrita sin²(thetaMiguel beta)=beta; não acrescenta variável ou observável ao motor. |

No item “constante de integração”, INPUT refere-se à **escolha do caso zero**; não apaga a existência de Λ/C no resultado geral. Os itens REAL são teoremas condicionais já reproduzidos em B3–B5, não ratificação experimental. As quatro correções explícitas de B4 e a recusa de seu contrato literal continuam preservadas.

## Referências e integração

As quatro entradas têm `KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED`, papel delimitado e **imported_into_witness:false**. Schema e onze linhas foram checados independentemente contra os arquivos atuais, sem usar o booleano da validação como substituto da leitura.

- [Jacobson 1995](https://arxiv.org/html/gr-qc/9504004): HTML primário lido nas hipóteses e derivação local; o argumento exige equilíbrio, proporcionalidade área/entropia, temperatura e balanço. A citação não fornece H3 da realização nem Phi_TGL.
- [Cai–Kim 2005](https://arxiv.org/html/hep-th/0501055): herança explícita da leitura primária própria de B4, seção 2; calor −dE, fator **H r_A**, e prescrição de temperatura no horizonte aparente. Não se restaura o fluxo literal sem raio.
- [Padmanabhan 2010](https://arxiv.org/html/0911.5004v2): resumo e início da introdução relidos; referência de enquadramento, sem alegar leitura integral ou fornecedor de Phi/G.
- [Gibbons–Hawking 1977](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.15.2738): metadados e resumo APS relidos; horizonte de eventos cosmológico no regime considerado. O PDF não foi lido nesta revisão. A limitação autoral histórica HTTP401 permanece explícita; não se atribui ao artigo uma prova geral de FLRW dinâmico.

A cláusula B6 da ORDEM 012 (linhas 149–153) é atendida como **proposta** para gerência. `changes_gate`, `implements_runtime` e `chooses_route` são false. Não se revisou/instalou toda a lista antiga EXTERNAL_KNOWN_THEOREMS, nem se alterou D1, A1, campos de gate, código canônico ou memórias.

## Reprodução e proveniência

Raiz curta `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\s`. Comando próprio: `lake build TGLExt.AuditPassageScope TGLExt.ReviewPassageScope`, Lean 4.31.0. Auditor autoral copiado byte a byte, mais auditor independente de `#check` com universos e `#print axioms`. Os **19 fornecedores existentes faltantes** foram reconstruídos de fontes copiadas, sem objetos autorais. Com os dois auditores, **21 novos objetos privados**, somados aos **120 próprios anteriores preservados**, dão **141**. **17 dos 20** objetos com equivalente autoral coincidem byte a byte, inclusive AuditPassageScope. **MixedLadder, SecondCone e AreaScale têm .olean diferente**; fontes copiadas são idênticas, e .ilean/C gerado desses três coincidem. A causa interna da diferença de serialização não foi estabelecida. A aceitação documental usa recompilação própria rc0 e os dez tipos/axiomas conferidos, **sem alegar reprodução binária integral dos fornecedores**. Pins de ambos os lados e traces estão em `binary_reproducibility_limit.json`. A primeira finalização recusou a afirmação mais forte de igualdade de todos os binários antes de escrever qualquer parecer/compilation; script e registro foram preservados. Esta segunda finalização lê os mesmos logs, sem novo build.

Nenhum aviso nos dois auditores B6. Foram preservados **9 avisos de fornecedores existentes** (TGL.AreaScale, TGLExt.GeneralNull, TGLExt.MixedLadder, TGLExt.SecondCone), ligados às traces no JSON. O total de jobs mostrado por Lake inclui reuso; não é contagem de novas provas. Fontes e objetos/traces previamente pinados B1–B5 e relatórios/compilations protegidos foram revalidados sem alteração.

Mathlib e oito pacotes auxiliares vêm do cache privado cuja cópia/pins foram registrados em B1/B2 e herdados até B5. Nesta rodada se reconferiram os manifestos e configuração/toolchain; **não se reconstruiu nem se rehashou integralmente o cache**. LEAN_PATH do build usa o projeto privado e pacotes; nenhum objeto TGL/TGLExt autoral foi copiado. Não se executou monólito ou auditor autoral.

Auditoria autoral e seus streams rc0 foram relidos e coincidem com os dez resultados próprios. Não foram criados novos negativos: B6 não acrescenta asserção matemática. A preservação ampla das 941 fontes continua [DECLARADO] no auditor autoral, sem nova varredura. O hash da cópia ROOT/um.py foi lido e coincide com a ficha. A cronologia local coloca a ficha antes do auditor; não é selo externo de tempo.

## Pins e saída

- Auditor fonte: `cbf0ff8d70b98d56aa229dea2392c98f5c8b387580bf4a0cc0aa97941c97b4d2`.
- Auditor .olean próprio = autor: `07093e1982b228dc36b234c73372cc15cb951473139a995c9a8c1a09708e7931`.
- Proposta documental: `42eb7f61c444f84fe22434e1a4dd9f99970db9017a0203d15c9802f4bd4d28f6`.
- [Revisão JSON](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b6/REVIEW_B6_FINAL.json>) — `6caa0786bd0544967d2f84aaf40d5498c0e0e86a98925e83d34b0fbcee0b99ff`.
- [Compilação própria](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b6/compilation.json>) — `f19d2e229a7f0fb3a045da7b3bdea8a1e266ea0285cefc632f3cee6548ae336a`.
- [Run rc0](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b6/independent_20260914_172114_917733/run.json>) — `82adfa73056b983dfc494efc78f8564b2420545c21b29509b508c6bc86fcc68f`.
- [Snapshot](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b6/independent_20260914_172114_917733/snapshot.json>), [tabela/ficha](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b6/independent_20260914_172114_917733/documentary_inspection.json>) e [referências](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/revisao_b6/independent_20260914_172114_917733/reference_inspection.json>).

**B6 concluído no escopo solicitado.** Não resta build, negativo ou pesquisa deste delta. Esta revisão não é entrega pelo túnel, instalação da proposta ou nova custódia. Nenhum alvo posterior foi iniciado.


## Ficha integral anterior ao artefato

[OPEN — ficha anterior aos artefatos B6]

# B6 — estatutos e importações explícitas

REUSAR e documentar: nenhum teorema novo; somente auditor de fornecedores existentes e propostas documentais tipadas.

## Tipo do produto
```text
B6 adds no mathematical assertion or axiom. Deliver typed JSON proposal:
 external_known_theorems: four entries with name,status,citation,exact_role,verified_url,
 source_read_scope,imported_into_witness=false;
 scope: H3 IMPORTED (conditional modus ponens), G/eta INPUT, H_nx INPUT,
 modified differential entropy INPUT, global Lemma3 OPEN, TGL-S/TGL-L OPEN;
 corrections: radius in Cai-Kim flux, variable-Phi derivative, density support for equality,
 nonzero total enthalpy for unique Phi_flux, explicit cosmological/integration constant;
 changes_gate=false, implements_runtime=false, chooses_route=false.
Audit existing fullnames by Lake: TheImportedEquilibrium logical providers, AreaScale calibration,
SectorFluid H_nx structure, HubbleHorizonInput, B4 derivative/support conditions.
No new theorem is needed for a bibliography or status table; importing a theorem as an implication
does not construct its horizon/equilibrium premise. The four literature sources do not prove Phi_TGL.
```

## Consumidores
```json
[
  {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\um.py",
    "line": 134757,
    "text": "EXTERNAL_KNOWN_THEOREMS = [",
    "sha256": "c1c761809efcde52ea8c6c4f7f0e7598c1d8e636e6858f1780dd622ef62a1d40"
  },
  {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\um.py",
    "line": 180955,
    "text": "def prove_d1_camb_protocol(ONE):",
    "sha256": "c1c761809efcde52ea8c6c4f7f0e7598c1d8e636e6858f1780dd622ef62a1d40"
  }
]
```

## Fornecedores

### the_trio_is_a_pair
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheImportedEquilibrium.lean:140 · SHA256 `6ce0e9c29fd9267078783b2f28dcd82d935ba784ebbcc6f2270de5f1f9e2eda0`
```lean
theorem the_trio_is_a_pair {H1 H2 H3 P : Prop}
    (master : H1 ∧ H2 ∧ H3 → P) (imported : H2 → H3) :
    H1 ∧ H2 → P
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### the_pair_still_needs_its_hypotheses
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheImportedEquilibrium.lean:149 · SHA256 `6ce0e9c29fd9267078783b2f28dcd82d935ba784ebbcc6f2270de5f1f9e2eda0`
```lean
theorem the_pair_still_needs_its_hypotheses :
    ∃ H1 H2 P : Prop, (H1 ∧ H2 → P) ∧ ¬ P
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### discharge_by_import
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\TheImportedEquilibrium.lean:129 · SHA256 `6ce0e9c29fd9267078783b2f28dcd82d935ba784ebbcc6f2270de5f1f9e2eda0`
```lean
theorem discharge_by_import {H C : Prop} (h : H) (imported : H → C) : C
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### newtonPlanck_equivalence
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGL\AreaScale.lean:24 · SHA256 `7058ae26f99f44f2d81d0c51e39bf435359a94c410405e52da4c4a44834ce075`
```lean
theorem newtonPlanck_equivalence (kappa G : ℝ) (hk : 0 < kappa) (hG : 0 < G) :
    2 * Real.pi / (1 / (2 * kappa)) = 8 * Real.pi * G ↔ kappa = 2 * G
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### halfNat_over_two_faces_eq_quarter
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGL\AreaScale.lean:41 · SHA256 `7058ae26f99f44f2d81d0c51e39bf435359a94c410405e52da4c4a44834ce075`
```lean
theorem halfNat_over_two_faces_eq_quarter (G : ℝ) :
    (1 / 2) / (2 * G) = 1 / (4 * G)
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### SectorFluid
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorFluidClosure.lean:20 · SHA256 `2cf4ae9ae038c5e4a5bcf9099db27cda667020f7f8693498c9ebc1684fba2dc3`
```lean
structure SectorFluid (ι : Type*) [Fintype ι] (I : Set ℝ) (H : ℝ → ℝ)
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### HubbleHorizonInput
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\ThermodynamicFriedmann.lean:38 · SHA256 `aa6b1c852034c4ca8b71872446ada2ec1d121dca213471eb6fa17eda147bc3a3`
```lean
structure HubbleHorizonInput (H : ℝ → ℝ) (t G Phi enthalpy : ℝ)
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### variable_entropy_derivative
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\ThermodynamicFriedmann.lean:81 · SHA256 `aa6b1c852034c4ca8b71872446ada2ec1d121dca213471eb6fa17eda147bc3a3`
```lean
theorem variable_entropy_derivative (A Phi : ℝ → ℝ) (t G : ℝ)
    (ha : DifferentiableAt ℝ A t) (hp : DifferentiableAt ℝ Phi t)
    (hg : G ≠ 0) (hz : Phi t ≠ 0) :
    HasDerivAt (fun u => A u/(4*G*Phi u))
      (deriv A t/(4*G*Phi t)-A t*deriv Phi t/(4*G*(Phi t)^2)) t
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### the_two_routes_equal_iff
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorRouteComparison.lean:106 · SHA256 `b6295c52d8a3f7718eabded61f3b95a81f4e0de6fe39bf0455687f926715d2a4`
```lean
theorem the_two_routes_equal_iff (F : SectorFluid ι I H) (c : TGLCoupling)
    (t : ℝ) (ht : t∈I) (hr : 0 < F.totalRho t) (he : 0 ≤ F.enthalpy t) :
    F.correctedTotalRho c t+F.correctedTotalPressure c t =
      entropyFactor c (F.wEff t)*F.enthalpy t ↔
      ∃ commonW : ℝ, ∀ i, 0 < F.rho i t → F.w i = commonW
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

### zero_flux_has_no_unique_factor
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt\SectorRouteComparison.lean:165 · SHA256 `b6295c52d8a3f7718eabded61f3b95a81f4e0de6fe39bf0455687f926715d2a4`
```lean
theorem zero_flux_has_no_unique_factor (F : SectorFluid ι I H) (c : TGLCoupling)
    (t : ℝ) (he : F.enthalpy t = 0) :
    ¬ ∃! factor : ℝ, factor*F.enthalpy t =
      F.correctedTotalRho c t+F.correctedTotalPressure c t
```
REUSAR sem novo teorema; auditar os fornecedores de estatuto

## Buscas
```json
[
  {
    "timestamp": "2026-09-14T16:59:48.950118-03:00",
    "searches": [
      {
        "label": "01_kernel",
        "command": [
          "rg",
          "-n",
          "the_trio_is_a_pair|invariance_does_not_fix_area|EXTERNAL_KNOWN_THEOREMS|TGL.S|TGL.L|gpf_H3_local_horizon_equilibrium_discharged|globalLemma3",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\kernel",
          "-g",
          "*.lean",
          "-g",
          "!**/.lake/**"
        ],
        "returncode": 0,
        "stdout_bytes": 11740,
        "stderr_bytes": 0
      },
      {
        "label": "02_notes",
        "command": [
          "rg",
          "-n",
          "the_trio_is_a_pair|invariance_does_not_fix_area|EXTERNAL_KNOWN_THEOREMS|TGL.S|TGL.L|gpf_H3_local_horizon_equilibrium_discharged|globalLemma3",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911",
          "-g",
          "*.md",
          "-g",
          "!*.bak*",
          "-g",
          "!**/r/**",
          "-g",
          "!**/revisao/**"
        ],
        "returncode": 0,
        "stdout_bytes": 17145,
        "stderr_bytes": 0
      },
      {
        "label": "03_deliveries",
        "command": [
          "rg",
          "-n",
          "the_trio_is_a_pair|invariance_does_not_fix_area|EXTERNAL_KNOWN_THEOREMS|TGL.S|TGL.L|gpf_H3_local_horizon_equilibrium_discharged|globalLemma3",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT",
          "-g",
          "*.md"
        ],
        "returncode": 0,
        "stdout_bytes": 172,
        "stderr_bytes": 0
      },
      {
        "label": "03_workbenches",
        "command": [
          "rg",
          "-l",
          "the_trio_is_a_pair|invariance_does_not_fix_area|EXTERNAL_KNOWN_THEOREMS|TGL.S|TGL.L|gpf_H3_local_horizon_equilibrium_discharged|globalLemma3",
          "C:\\IALD\\Central de Patentes\\Chatgpt",
          "-g",
          "*.lean",
          "-g",
          "!**/.lake/**",
          "-g",
          "!**/attempts/**",
          "-g",
          "!**/revisao/**",
          "-g",
          "!**/DEPENDENCIAS_CE*/**",
          "-g",
          "!*.bak*"
        ],
        "returncode": 0,
        "stdout_bytes": 223003,
        "stderr_bytes": 0
      },
      {
        "label": "04_tree",
        "command": [
          "rg",
          "-n",
          "the_trio_is_a_pair|invariance_does_not_fix_area|EXTERNAL_KNOWN_THEOREMS|TGL.S|TGL.L|gpf_H3_local_horizon_equilibrium_discharged|globalLemma3|Einstein|Clausius",
          "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\\inputs\\A_PROVA_DA_QG_TGL_arvore.md"
        ],
        "returncode": 0,
        "stdout_bytes": 5855,
        "stderr_bytes": 0
      },
      {
        "label": "05_toe",
        "command": [
          "rg",
          "-n",
          "the_trio_is_a_pair|invariance_does_not_fix_area|EXTERNAL_KNOWN_THEOREMS|TGL.S|TGL.L|gpf_H3_local_horizon_equilibrium_discharged|globalLemma3",
          "C:\\IALD\\Artigo\\BANCADA_TOE\\kernel_bancada",
          "-g",
          "*.lean",
          "-g",
          "!**/.lake/**"
        ],
        "returncode": 2,
        "stdout_bytes": 0,
        "stderr_bytes": 144
      },
      {
        "label": "06_acervo",
        "command": [
          "C:\\Python314\\python.exe",
          "-X",
          "utf8",
          "-B",
          "C:\\IALD\\INDICE_DO_ACERVO\\buscar.py",
          "the_trio_is_a_pair|invariance_does_not_fix_area|TGL-S",
          "--max",
          "25",
          "--ctx",
          "140"
        ],
        "returncode": 2,
        "stdout_bytes": 0,
        "stderr_bytes": 112
      }
    ]
  },
  {
    "timestamp": "2026-09-14T17:00:44.475206-03:00",
    "searches": [
      {
        "label": "05_toe",
        "command": [
          "rg",
          "-n",
          "the_trio_is_a_pair|invariance_does_not_fix_area|EXTERNAL_KNOWN_THEOREMS|TGL.S|TGL.L|gpf_H3_local_horizon_equilibrium_discharged|globalLemma3",
          "C:\\IALD\\Artigo\\BANCADA_TOE\\kernel_bancada",
          "-g",
          "*.lean",
          "-g",
          "!**/.lake/**"
        ],
        "returncode": 0,
        "stdout_bytes": 373,
        "stderr_bytes": 0
      },
      {
        "label": "06_acervo",
        "command": [
          "C:\\Python314\\python.exe",
          "-X",
          "utf8",
          "-B",
          "C:\\IALD\\INDICE_DO_ACERVO\\buscar.py",
          "the_trio_is_a_pair|invariance_does_not_fix_area|TGL-S",
          "--max",
          "25",
          "--ctx",
          "140"
        ],
        "returncode": 0,
        "stdout_bytes": 11574,
        "stderr_bytes": 0
      }
    ]
  }
]
```

- Buscas por nomes/tipos e recortes, não varredura exaustiva de todo conteúdo.
- Gibbons–Hawking: metadados e resumo oficiais lidos; PDF oficial retornou 401. Não alegar leitura integral.
- Cai–Kim: seção2 lida em HTML primário, incluindo raio, fluxo, temperatura e conservação. Jacobson: texto primário lido sobre horizontes locais/hipóteses. Padmanabhan: resumo e trechos introdutórios primários lidos, papel contextual.
- Não alterar EXTERNAL_KNOWN_THEOREMS canônico: gerar proposta para gerência.
- Não derivar H3, G ou lei Phi por mera citação. B6 não encerra A1(b), que retoma após as entregas B1–B6.

2026-09-14T17:04:54.683217-03:00
