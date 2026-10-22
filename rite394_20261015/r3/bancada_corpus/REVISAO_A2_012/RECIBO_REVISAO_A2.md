# Recibo de revisão adversarial independente — A2, lote congelado V354

**[REAL — medido nesta revisão] VERIFICADO_NO_ESCOPO_DO_REPRESENTANTE_MINIMO_CCW_E_PAREDE__DELTA_P2_PENDENTE.** P0=0; P1=0; P2=1.

**Carver — agent_id `01a0a5b5-e12d-70c1-a68a-c6f13373e3c0`**, convocado pelo agente principal no escopo autorizado; não autor de A2. A identidade foi fornecida pelo agente principal [INPUT] e consta também do JSON. Nenhum outro usuário é apresentado como auditor/aprovador.

Os oito V354 e CoreSupport foram verificados no alcance do suporte construído, representante mínimo, leitura no cone, ContinuousCornerWitness e parede de não ciclicidade. **Não é aceite integral de A2 da ORDEM 011 nem do adendo.** ThreeLocksCoreData e FullWitness não foram construídos; o adapter de traço total legado permanece [OPEN]. Uma pendência P2 de remoção de dois corolários sem consumidor antecede a incorporação enxuta.

Escrita exclusiva da revisão A2 em `C:\IALD\Central de Patentes\Chatgpt\REVISAO_A2_012`. Fontes autorais congelados preservados; nenhum fonte A1 recompilado, nenhum objeto emprestado sobrescrito. O recibo B1′ foi fechado antes de A2; recebeu depois apenas a correção cadastral solicitada de identidade, com backup e novo selo.

## Resultado por obrigação

| Obrigação delimitada | Resultado e evidência |
|---|---|
| Mesmo core e traço A1 | `regularCoreAlgebra P`, em `RegularHilbert (TowerHilbert P)`, e `scalarInverseLimitWeight P` são mantidos em toda a cadeia. A1 entra por cache aceito e fornecedores explícitos. |
| Projeção não nula, traço um | `regularFiniteSupport_projection`, `_trace` e `_ne_zero`; nenhuma hipótese de suporte ou de finitude do projetor no resultado final. |
| Faces iguais e ortogonais | `a=vq`, q=a*a, r=aa*, qr=0. A igualdade de traços consome `scalarInverseLimitWeight_tracial P a`. A revisão também confirmou rq=0. |
| Calibração | Ação dual efetiva com s=log(tau(q+r).toReal), após provar traço positivo e finito. Transporta ambas as faces; não redefine o peso A1. |
| Projeção espectral | `regularMinimalLock_spectral_zero`: projker(1−PF)=PF como igualdade de operadores, obtida de ker=range(PF). |
| Gap | `regularMinimalLock_relative_gap`: norma preservada no complemento ortogonal do kernel. Controle próprio refuta a leitura global em todo H. |
| Domínio e afiliação | Grafo do operador limitado 1−PF com domínio top, auto-adjunto e fechado; invariância sob todo B limitado do comutante. Não identifica um operador microscópico distinto. |
| Leitura positiva / CCW | `positiveTraceReader_positive` vale para TODO positivo; `regularContinuousCorner` é termo no mesmo N, com leituras normalizadas 1, 1/2, 1/2. |
| Canto de Breuer delimitado | `regularMinimalLock_breuer_kernel`: p=projker(Hmin), tau_A1(p)=1, 0<tau_A1(p)<top, sem testemunha hipotética na assinatura. |
| Parede do reader | `positiveTraceReader_not_cyclic` refuta a ciclicidade global da extensão por zero. Não prova impossibilidade de qualquer outra extensão total. |

## Leitura adversarial dos enunciados e das escolhas

`regularTrace_finite_positive_below` exige um positivo não zero e usa semifinitude/fidelidade do contrato. Na cadeia concreta, o contrato é `scalarInverseLimitTraceData`. `positive_operator_has_threshold_projection` produz epsilon=norm(X)/2 e q=projker((X−epsilon I)^−); a positividade não nula dá q!=0 e epsilon q<=X. Finitude vem da ordem e homogeneidade do mesmo traço A1.

O auxiliar `scalarTrace_finite_subprojection_exists` recebe e projetor não zero, **sem exigir traço finito de e**. O consumidor principal fornece o canto matricial e e v construídos em `regularCore_matrix_corner`, obtendo q finito sob e. Não há hipótese de projeção finita oculta no resultado principal. `SiteProfile` contém w:N→R e 0<w(n)<1; a representação regular é L²(R,TowerHilbert P). `Fin 2` no sítio matricial não é hipótese de dimensão finita desse Hilbert.

`scalarTrace_finite_equal_split` usa efetivamente a tracialidade quadrática de A1 para a=vq. A revisão exibiu um contraexemplo em R×R: projeções ortogonais que somam a unidade, com peso cíclico e leituras 1 e 2. Assim, ortogonalidade ou soma sozinhas não pagam igualdade de faces; o fornecedor tracial e a equivalência via vq importam.

`regularNormalizedFaces` aplica Classical.choose/choose_spec ao existencial previamente provado por `scalarTrace_normalized_split_exists`. Não há testemunha introduzida sem prova. O `classical` do reader decide positividade em um if dependente. Todos os nomes públicos foram auditados, inclusive essas definições e os lemas não impressos individualmente no fonte.

CoreSupport é cópia byte-idêntica do fornecedor aceito. Seus lemas algébricos de aniquilação, auto-adjunção e maximalidade são os consumidores usados para Hmin. Auditar os construtores condicionais `threeLocksFromSupport` e `realizationFromSupport` não os instancia. A ocorrência de `¬FiniteDimensional` no segundo construtor legado não é uma premissa escondida dos V354.

## Alcance exato de ContinuousCornerWitness e da parede

A interface lida em [ContinuousCornerAbstract.lean](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/inputs/accepted_sources/TGL/ContinuousCornerAbstract.lean>) pede uma função total Core→ENNReal e leis apenas nas projeções e no split; não pede ciclicidade global, fidelidade global ou normalidade. O reader satisfaz esse contrato com a convenção zero fora do cone e coincide com A1 em todos os positivos. Portanto o termo CCW é válido, mas seu campo chamado `trace` não passa a ser um traço global genuíno por ocupar esse campo.

A parede constrói X=e+v* e Y=e: XY=e é positivo não zero, enquanto YX=e+v* não é positivo. O primeiro valor do reader é tau_A1(e)!=0 por fidelidade; o segundo é zero pela convenção. Logo este reader não pode preencher `ContinuousCoreData.trace_tracial`. A parede não resolve nem fecha a questão de outro adapter possível.

A prova de Breuer delimitada utiliza diretamente A1 na projeção do kernel do representante mínimo. Ela não depende de interpretar o reader fora do cone, nem de supor ContinuousCornerWitness como hipótese, nem promove o resultado a ThreeLocksCoreData/FullWitness.

W/D já têm fornecedores: `TGLExt.theSpecificAQFTWitness` em WedgeNet e `TGLExt.V350Continuous.towerWedgeData : WedgeModularData theSpecificAQFTWitness` em V350WedgeModularData, para mixProfile. Os fontes foram lidos e preservados em inputs/WD, com hashes em SEMANTICA_A2.json. Não se registra ausência genérica de W/D como pendência. O totalizador de traço Core→ENNReal com as leis legadas continua aberto; o reader construído é explicitamente excluído desse papel por sua própria parede.

## P2-01 — dois casos da unidade removíveis

1. [scalarTrace_finite_positive_seed](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/src/TGLExt/V354FiniteTraceSupport.lean:35>): apenas declaração e impressão de axiomas, sem consumidor matemático no lote.

2. [scalarTrace_finite_projection_exists](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/src/TGLExt/V354SpectralThreshold.lean:136>): mesma situação. A cadeia usa diretamente os lemas gerais sobre o canto e11 construído.

Conferência em fonte: [UNUSED_COROLLARIES.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/UNUSED_COROLLARIES.json>); conferência em termos impressos: [CONSUMER_PROOF_AUDIT.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/CONSUMER_PROOF_AUDIT.json>). Os demais termos impressos têm zero menções a ambos. O escopo é o lote congelado; não é alegação de inexistência de toda referência futura ou externa.

**Delta mínimo recomendado ao autor:** remover as duas declarações e seus dois `#print axioms`; atualizar Audit geral e contagens. Manter os dois módulos e seus fornecedores gerais. Não criar flags nem `have` sem uso para simular consumo. Nenhum desses fontes foi alterado nesta revisão. A pendência não invalida os teoremas compilados, mas impede chamar o lote atual de incorporação mínima sem sobras.

## Compilação, axiomas e controles

Lean medido: `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`. 9/9 fontes próprios compilados, além dos auditores e controles da revisão. 45/45 nomes públicos do lote/fornecedor e 25 nomes dos controles próprios com axiomas efetivamente lidos e contidos em propext/Classical.choice/Quot.sound. Evidência integral: [AUDITORIA_A2_INDEPENDENTE.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/AUDITORIA_A2_INDEPENDENTE.json>); log geral: [stdout.txt](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/build_logs/AuditAllPublic/stdout.txt>); log próprio: [stdout.txt](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/control_attempts/20260915_160413_973301/audit/stdout.txt>).

| Controle negativo próprio | Parede/contraparte positiva compilada | Resultado |
|---|---|---|
| TraceZero | `IndependentA2.trace_not_zero`; tau(PF)=1 exclui zero | rc=1, incompatibilidade semântica de tipo |
| TraceTwo | `IndependentA2.trace_not_two`; tau(PF)=1 exclui dois | rc=1, incompatibilidade semântica de tipo |
| SupportZero | `IndependentA2.support_nonzero`; PF!=0 usa a lei tau(0)=0 | rc=1, incompatibilidade semântica de tipo |
| SpectralZero | `IndependentA2.spectral_not_zero`; projker(Hmin)=PF!=0 | rc=1, incompatibilidade semântica de tipo |
| HalfAsOne | `IndependentA2.plus_not_one`; leitura normalizada da face é 1/2, não 1 | rc=1, incompatibilidade semântica de tipo |
| EqualFromOrthogonality | `IndependentA2.orthogonality_does_not_force_equal_trace`; contraexemplo em R×R: faces ortogonais somando a unidade, peso cíclico com leituras 1 e 2; igualdade exige informação adicional, aqui o transporte por vq e a tracialidade A1 | rc=1, incompatibilidade semântica de tipo |
| PositiveZero | `IndependentA2.zero_positive_has_no_positive_finite_minorant`; zero não tem minorante positivo de traço estritamente positivo; a hipótese não zero não pode desaparecer | rc=1, incompatibilidade semântica de tipo |
| GlobalGap | `IndependentA2.gap_not_global`; PF!=0 fornece vetor não zero no kernel; o gap é relativo ao complemento, não global | rc=1, incompatibilidade semântica de tipo |
| GlobalCyclicity | `IndependentA2.reader_not_global_cyclic`; a igualdade no cone positivo não autoriza ciclicidade do reader em todo o anel | rc=1, incompatibilidade semântica de tipo |

Cada recusa usa um fonte sintaticamente válido, em ambiente já compilado. O erro isolado rejeita o termo oferecido; o suporte semântico vem das paredes/contramodelos comprovados. Casos corretos compilam no módulo IndependentA2Controls. Nome ausente ou axioma fora do trio reprova o finalizador; não há literal autoral usado como aprovação.

Cache declarado: 683 módulos TGL/TGLExt aceitos, com 1366 arquivos de objetos/companheiros emprestados por hardlinks somente de leitura; Mathlib e pacotes de terceiros também são cache. Não houve reconstrução de A1, Mathlib ou toolchain. Objetos novos foram gravados apenas em caminhos inicialmente inexistentes. Integridade antes/depois de todos os objetos emprestados e fontes congelados: [INTEGRIDADE_A2.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/INTEGRIDADE_A2.json>).

O limiar espectral usa maxHeartbeats 600000 local, com motivo declarado no fonte (elaboração CFC/projeção). Nenhum comando novo axiom/sorry/native_decide/trustCompiler foi encontrado nos oito V354, CoreSupport ou controles próprios. Os axiomas Lean aceitos permanecem o trio; comentários históricos não são declarações axiomáticas.

## Tentativas preservadas e limitações de evidência

A primeira tentativa independente de compilação esbarrou na resolução de namespaces do Lean: dependências aceitas estavam em um segundo diretório de busca. Foram feitos hardlinks imutáveis também junto aos novos outputs, sem sobrescrever objetos, e os nove fontes foram então recompilados com sucesso. Os logs da falha inicial estão em failed_setup e não contam como prova.

O primeiro controle próprio de vetor no kernel usou uma extensionalidade excessiva e falhou; foi corrigido para ContinuousLinearMap.ext. Em seguida, os controles positivos e seu auditor compilaram. Uma execução das sondas foi interrompida por validação de caminho antes da criação de três fontes; todos os caminhos foram medidos dentro da raiz, os diretórios foram preparados sequencialmente e as nove sondas foram reexecutadas. Logs, snapshots e backups das tentativas anteriores foram preservados. Nenhum deles substitui o rc0 e os logs finais selecionados no JSON.

A revisão é de código e prova sobre os caches aceitos, sem execução de um.py, experimentos ou mudança de gate. O aceite do escopo matemático delimitado não elimina a pendência P2 nem autoriza afirmar encerramento do adendo, ThreeLocksCoreData, FullWitness, natureza realizando o modelo ou um traço global do reader.

## Arquivos congelados — origem, bytes, SHA256 e cobertura

| Fonte autoral / cópia compilada | Bytes | SHA256 | Nomes públicos auditados |
|---|---:|---|---:|
| [TGL.CoreSupport](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGL/CoreSupport.lean>) / [cópia](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/src/TGL/CoreSupport.lean>) | 6731 | `041fb863b07c3e0a167d5d0c8a522890d2da61586f41c27be2b06c46fac588e0` | 10 |
| [TGLExt.V354FiniteTraceSupport](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354FiniteTraceSupport.lean>) / [cópia](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/src/TGLExt/V354FiniteTraceSupport.lean>) | 2326 | `3745bc296cafaeea0c2725e1993d611b92c0a14be4fc392e88c06e1710ff890b` | 3 |
| [TGLExt.V354SpectralThreshold](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354SpectralThreshold.lean>) / [cópia](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/src/TGLExt/V354SpectralThreshold.lean>) | 6705 | `3eac1f59b2eee2a5226cca0b8feaec963e2ca9fd74208c9f331c0c4e0de47f3a` | 3 |
| [TGLExt.V354RegularMatrixCorner](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354RegularMatrixCorner.lean>) / [cópia](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/src/TGLExt/V354RegularMatrixCorner.lean>) | 2641 | `1f469df09c8ce12c58d7c8388dbedadb3fc9336a9c97757113693e7322e596f9` | 1 |
| [TGLExt.V354FiniteEqualSplit](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354FiniteEqualSplit.lean>) / [cópia](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/src/TGLExt/V354FiniteEqualSplit.lean>) | 3193 | `72876fa3cf13dbd947ab02f1f4bd378c8d0dc7b2ed9beb39d98d7bed8079552e` | 2 |
| [TGLExt.V354NormalizedSplit](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354NormalizedSplit.lean>) / [cópia](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/src/TGLExt/V354NormalizedSplit.lean>) | 2452 | `5e90a1c08de4dc4593e65d9b8dde4a4bd5a1e074b68f8be357d17d25bbebe91a` | 2 |
| [TGLExt.V354RegularSupport](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354RegularSupport.lean>) / [cópia](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/src/TGLExt/V354RegularSupport.lean>) | 6756 | `c80d99c73be4a676bcdc8cc21d476c249911d08f93fd914fda0d788019b1063e` | 18 |
| [TGLExt.V354PositiveTraceReader](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354PositiveTraceReader.lean>) / [cópia](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/src/TGLExt/V354PositiveTraceReader.lean>) | 4075 | `8133d88dcaf9ac3d58d739ecaf997312d7951be2c11fe1d08f21c8f90badf3ea` | 5 |
| [TGLExt.V354TraceReaderWall](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/A2_012/src/TGLExt/V354TraceReaderWall.lean>) / [cópia](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/src/TGLExt/V354TraceReaderWall.lean>) | 2630 | `7882c9df649971790dfa9545e802df5b2b4e31c8bc16d536cecfd4d64203efcc` | 1 |

## Entrega e reprodução

[AUDITORIA_A2_INDEPENDENTE.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/AUDITORIA_A2_INDEPENDENTE.json>) contém os nomes completos, axiomas, gates calculados, identidade do revisor e controles. [BUILD.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/BUILD.json>) contém cada comando efetivo, fonte, objeto, stdout/stderr e retorno. INPUTS.json contém os 683 fornecedores consultados e todos os caminhos/bytes/SHA de origem, cópia e hardlinks. MANIFESTO_A2.json inventaria artefatos próprios; SELO_A2.json sela o manifesto, o recibo e a auditoria sem hash autocircular.

Os scripts recusam sobrescrever objetos de build ou emprestados. Uma reprodução limpa precisa de outra raiz vazia autorizada, preservando a separação entre fontes novos e caches aceitos. Não se executou o roteiro autoral para emitir este parecer.
