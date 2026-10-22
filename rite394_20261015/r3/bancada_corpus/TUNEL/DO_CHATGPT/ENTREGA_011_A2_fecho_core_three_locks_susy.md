[REAL — A2 construído e revisto no representante mínimo do core regular. PROPOSTA — integração nos leitores do um.py; nenhuma rodada canônica feita pela bancada.]

# A2: o termo legado existe; A1, Three Locks e SUSY estão no mesmo core

Esta entrega responde à ORDEM011 A2 e ao §5.1 do ADENDO001 da ORDEM012. Resolve as duas pendências do marco `ENTREGA_011_A2_suporte_split_e_parede`: a extensão cíclica total compatível com A1 e o consumidor SUSY na realização concreta. O marco anterior permanece como histórico; seu estado OPEN não é o estado desta entrega.

O resultado final é um termo de **`TGL.ModularRealization.FullTGLWitness`**, o tipo dependente antigo, sem alterar seus campos. Seu alcance é a realização regular com o operador mínimo limitado **H_min=1−P_F**. Não se acrescentou a existência do próprio alvo como hipótese.

## O que foi ligado

| Critério | Resultado e fornecedor efetivo |
|---|---|
| Mesmo core e mesmo traço A1 | `regularCoreAlgebra mixProfile`; `cyclicTraceCandidate_positive` prova igualdade com `scalarInverseLimitWeight` em TODO positivo |
| Suporte positivo finito | `regularFiniteSupport`, já revisto no lote33; τ(P_F)=1, não nulo e finito |
| Faces e inscrição | `regularNormalizedFaces`, já revisto: faces ortogonais, soma P_F, traços iguais, leituras ½ e ½ |
| Operador, domínio e afiliação | H_min=1−P_F; grafo limitado de domínio total, fechado, auto-adjunto e afiliado por invariância sob o comutante; fornecedores do lote33 |
| Núcleo e gap | projeção de ker(H_min)=P_F; ‖H_min x‖=‖x‖ no complemento do núcleo; gap RELATIVO, não global |
| Contrato antigo do core | `regularLegacyCore : ContinuousCoreData theSpecificAQFTWitness towerWedgeData` |
| Contrato antigo Three Locks | `regularLegacyThreeLocks`, aplicando o construtor existente `threeLocksFromSupport` |
| Identificação dos campos montados | `regularLegacyThreeLocks_concrete`: PF e H3Lt são literalmente o suporte e H_min anteriores, por rfl |
| Realização modular dependente | `regularModularRealization : TGLModularRealization theSpecificAQFTWitness`; reutiliza `witnessV3_infinite` e `towerWedgeData` |
| Termo completo legado | `regularFullWitness : FullTGLWitness`, o par dependente concreto |
| SUSY relativo no mesmo N | `regularSusyData P`, no reticulado de todas as projeções de `regularCoreAlgebra P`, com o traço A1 |
| Consumidor Breuer | `regularSusy_gives_breuer` aplica `susy_relative_gives_breuer`; as identificações e o gap concreto acompanham o pacote |

Os cinco nomes da montagem estão em `TGLV354.TraceCompletion`. Os nomes SUSY estão em `TGLV354`. O manifesto fornece caminhos e hashes lidos; não se depende de homônimos para encontrar os objetos.

## Como a parede do traço foi resolvida

A extensão por zero fora do cone continua refutada por `positiveTraceReader_not_cyclic`. A construção nova usa uma relação algébrica de deslocamento com expoente positivo: a~b quando existem n>0 e r,s no MESMO core com ar=rb, sa=bs, aⁿ=rs e bⁿ=sr. Produtos xy e yx estão nessa relação. A leitura total é o supremo das leituras A1 dos positivos relacionados ao elemento.

A obrigação decisiva era provar que dois positivos relacionados têm o mesmo traço A1. Ela foi provada, não transferida para uma premissa final. O polar de r é construído dentro do mesmo von Neumann algebra, usando a extensão da isometria |r|x↦rx. As relações de potência controlam os núcleos; densidade controla o entrelaçamento sem cancelar um operador possivelmente não invertível. Obtém-se p=uqu* e (u*u)q=q. Para a=u√q, a*a=q e aa*=p; a tracialidade quadrática já paga em A1 dá τ(p)=τ(q).

Assim, o supremo não aumenta a leitura positiva. `cyclicTraceCandidate_positive` é a igualdade com A1, inclusive para traço infinito. A leitura total é cíclica, preserva star e zero e tem a escala dual exigida pelo contrato legado. Não é apresentada como uma função complexo-linear ou aditiva no anel inteiro: essas propriedades globais não são exigidas por esse contrato e não foram provadas. As leis de traço positivo vêm de A1 pela igualdade no cone.

Essa passagem usa um único polar compartilhado com SUSY. Os lemas antigos de potências, os fornecedores A1, `CoreSupport`, a cunha e o Hilbert infinito foram reaproveitados. Não há uma segunda construção desses objetos sob novos nomes.

## O alcance exato do SUSY construído

O reticulado contém todas as projeções do mesmo N, representadas por subespaços fechados invariantes sob o comutante. A ordem é inclusão, o supremo binário é o fecho da soma. O polar de (1−q)p prova a comparação do join; tracialidade, aditividade positiva e monotonicidade A1 dão τ(p∨q)≤τ(p)+τ(q). Não se exige que p e q comutem, nem se usa o modelo numérico `modelSusy` como substituto.

A instanciação é D=H_min=1−P_F, D₀=1, ker=gapD=diff=P_F e gapD₀=⊥. As identificações são demonstradas com as projeções de núcleo de D e D₀, a diferença 1−D e o gap relativo. O contrato reticular recebe a inclusão concreta já satisfeita; esta etapa não prova um teorema geral novo de perturbação microscópica. Não se criou uma API de janelas de Borel nem uma instância `CompleteLattice` para além do necessário ao consumidor.

## Auditoria e independência

A montagem e a compatibilidade têm 40 nomes autorais. SUSY tem 29, dos quais 11 são o polar compartilhado. A união é **58 declarações explícitas em 11 módulos**. Carver, agente revisor distinto dos autores, recompilou todos em cópia própria e descobriu ainda duas exportações geradas; os **60 nomes** foram impressos com tipos, corpos e axiomas. Todos dependem apenas do trio permitido, ou subconjunto. Parecer: **P0=0, P1=0, P2=0**, limitado ao alcance deste documento.

O revisor compilou 18 âncoras próprias e recusou seis adulterações semânticas. Entre elas: leitura do suporte trocada para 2, gap SUSY zerado e `modelSusy` passado ao tipo concreto. Os controles autorais também estão preservados: quatro da montagem e três SUSY. A falha `rfl` contra H3Lt=1 é rotulada como recusa daquela identificação definicional, não como prova autônoma de toda desigualdade possível.

Os 33 nomes do marco anterior e A1 foram reutilizados com seus recibos aceitos; não se recontaram como provas novas nem se repetiram seus testes sem mudança. Mathlib e dependências entram como caches declarados. A recompilação final de integração da gerência continua sendo o árbitro canônico.

## Ligação concreta ao um.py, sem outra camada de funções

A fonte v354 foi lida por AST, sem execução ou importação. A cópia dos leitores, a proposta e o diff estão no manifesto. Os quatro nomes Python existentes podem apontar diretamente aos termos abaixo, conservando os nomes das bandeiras:

| Bandeira existente | Referente direto proposto |
|---|---|
| `qgf_unconditional_continuous_corner_proved` | `TGLV354.TraceCompletion.regularLegacyThreeLocks` |
| `qgf_continuous_modular_realization_constructed` | `TGLV354.TraceCompletion.regularModularRealization` |
| `qgf_full_TGL_witness_constructed` | `TGLV354.TraceCompletion.regularFullWitness` |
| `gpf_H1_internal_susy_relative_gap_discharged` | `TGLV354.regularSusyData`, no alcance do representante mínimo |

`PROPOSTA_MAPA_CONSUMIDORES.json` lista também os fornecedores exigidos por cada entrada de `_V350_MODULAR_CONTRACTS`. A proposta reutiliza `verify_v350_modular_provenance`, `finalize_v350_modular_frontier` e `v350_frontier_flag_has_proof`. Nenhum nome novo de função Python e nenhum alias Lean foi criado. O auditor recebe cinco verificações explícitas de tipo, em `AuditReaderContracts012.lean`; elas devem entrar no Audit canônico junto aos prints, não como módulo de teoremas. Esse auditor compilou; `True.intro` recusou o tipo `FullTGLWitness`.

Dois leitores históricos rejeitam o resultado válido porque ainda exigem false. Na v354 consultada:

1. **Linha 160146**, atermacão/Bell: substituir apenas `and not kf.get("qgf_full_TGL_witness_constructed")` pela chamada ao leitor de prova existente. Manter `red_bell_is_the_corner is None` e a distinção entre o projetor Bell finito e P_F. Uma prova independente de FullTGLWitness não identifica esses dois projetores.
2. **Linha 160198**, extensão contínua: substituir `bool(not kf.get("qgf_continuous_modular_realization_constructed"))` pela chamada ao leitor de prova existente. Atualizar a frase envelhecida sobre a extensão ainda aberta: o módulo finito isolado não a fornece; A1/A2 agora a fornece no escopo tipado.

Ao ampliar o dicionário de contratos, `evaluate_v350_kernel_frontier` precisa continuar medindo o escopo modular antigo pelos seus três contratos, separadamente dos novos. Fazer `modular=all(proofs.values())` depois da ampliação apagaria indevidamente o avanço modular anterior se faltasse um item A2. A proposta já corrige esse consumidor, separando realização mínima contínua e SUSY, e mantendo H2/H3 e as identificações físicas como pendências distintas.

Os campos de relatório nas linhas 143382, 144058/144063 e 179912/179916/179944 já leem as bandeiras e não precisam de novos wrappers. A frase em 158178 e os comentários históricos em 179902–179918 precisam de errata ao lado, pois ainda descrevem os termos como ausentes. **`FullStaticWitness` não é `FullTGLWitness`**: manter a distinção e a obstrução estática sob contraste.

A bancada testou a cópia dos leitores com o relatório de axiomas da revisão real, além de adulterações e fixtures históricas explicitamente rotuladas para regressão. Isso é teste do leitor isolado, não execução integral do `um.py`. O manifesto da entrega aponta o resultado e o parecer independente específico sobre esta proposta. Nenhum True deve ser instalado literalmente como resultado matemático.

## Sequência de incorporação para a gerência

1. Conferir o manifesto desta entrega e os recibos do lote33 anterior. Materializar os fontes matemáticos únicos; `V354BoundedPolar` entra uma só vez. Não embutir arquivos DEV, Good/Bad ou scripts de empacotamento como teoremas.
2. Recompilar os alvos novos na raiz própria, usando o fecho de dependências registrado. Acrescentar ao auditor canônico os nomes públicos auditados e as cinco verificações de tipo. Não imprimir nomes privados como se fossem públicos.
3. Aplicar os mapas e os ajustes dos leitores existentes, preservando a verificação de fontes/dependências, rc, auditoria e axiomas. A proposta é uma cópia para revisão; não é um patch cego do arquivo canônico inteiro.
4. Executar a rodada integral e o autoteste de prova adulterada. Comparar as bandeiras antes/depois e reportar as quatro somente conforme a evidência efetiva. A proposta não altera `evaluate_quantum_gravity_closure` nem usa dados cosmológicos para suprir campos formais.
5. Atualizar selo, diário, desenho, Atlas e índice da casa canônica na incorporação, com backup imediato em bytes. A bancada atualizou somente a memória própria; este handoff fornece o conteúdo para as demais superfícies, sem cruzar a custódia.

## Limites que devem acompanhar a integração

- `FullTGLWitness` é o tipo legado efetivamente habitado. A cunha reutilizada mantém `U := fun _ => 1`; não há aqui nova identificação Bisognano–Wichmann com representação geométrica não trivial.
- H3Lt é H_min=1−P_F. A glosa antiga “transformada limitada” não prova a igualdade H3Lt=H/√(1+H²) para um Hamiltoniano microscópico independente.
- A bandeira H1 proposta quita o contrato SUSY reticular nesse representante matemático. Não significa que um Hamiltoniano físico da TGL foi derivado.
- H2, H3, interação, BRST/QME, anomalias, limite UV e identificação de horizonte físico não são promovidos por estes termos. Também não se altera o valor de G ou se deriva CODATA.
- Nenhuma pontuação sigma, confirmação experimental ou veredito de natureza foi calculado nesta etapa.

## Estado conjunto do ADENDO001

A2 está concluído na bancada no alcance acima. B1′ já foi entregue em `ENTREGA_012_B1_PRIME_quarta_face`, com a EOM como hipótese e ξ separado de β. Os saneamentos a–h foram respondidos em `ENTREGA_012_ADENDO001_saneamentos`; a causa integral do par binário histórico AreaScale e motivos históricos de orçamento não recuperados permanecem assim declarados, sem impedir a recompilação arbitral da gerência.

A escolha conceitual do operador pelo **fator sobre o fluido total** continua registrada. Sua leitura teológica distingue Ψ de Λ e não foi convertida em afirmação de energia negativa. A V3 do D1 é da gerência e não recebeu edição desta bancada.

**Gate canônico: não alterado aqui.** Foram construídos e revistos os termos que permitem a ligação das quatro bandeiras no escopo declarado. A confirmação da incorporação virá da rodada da gerência, não do nome deste recibo.


## Adendo de integração — leitor V2 e P2-READERS-01

[REAL — correção em cópia; revisão independente específica anexa] O candidato ativo é **`PROPOSTA_LEITORES_EXISTENTES_V2.py`**, com `PROPOSTA_MAPA_CONSUMIDORES_V2.json` e diff V2. As referências ao mapa sem sufixo no corpo acima descrevem a primeira proposta, que permanece preservada como histórico. Mapas, termos Lean, cinco verificações de tipo e os dois ajustes false-only são iguais em V1 e V2.

Carver encontrou uma falha herdada no leitor canônico: `audit_returncode == 0` também aceita `False`, pois `bool` é subclasse de `int` em Python. A V2 exige `type(audit_returncode) is int` antes da igualdade. Essa é a única alteração de lógica entre V1 e V2. Código de saída 0 inteiro continua válido; bool, string, float e None são recusados. Os códigos dos builds Lean desta entrega já eram inteiros.

`TESTES_LEITORES_COPIADOS_V2.json` registra 66 verificações autorais aprovadas, incluindo as cinco adulterações de tipo adicionais. Isso não é uma rodada canônica. O parecer independente do leitor distingue a aprovação da matemática, já encerrada, da correção desse limite de metadados. A V1 não deve ser integrada no lugar da V2.


## Recibo de transmissão e referências diretas

Transmissão: 2026-09-15T14:54:15.530582-03:00. Inventário conferido novamente: 81 artefatos selecionados, mais as fontes e objetos da ordem de montagem. A2 totaliza 19 módulos matemáticos únicos: oito do lote33 preservado e onze desta conclusão. A revisão dos leitores V2 quita P2-READERS-01 no delta; os pareceres V1 permanecem como histórico.

- [Manifesto da entrega](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_011_A2_fecho_core_three_locks_susy_manifesto.json>) — SHA256 `0c06ac31252330d6d673b7800fbfa43fad1fbbe22011f89712a2d85c84a8654a`.
- [Ordem dos fontes, nomes auditados e tipos](<C:/IALD/Central de Patentes/Chatgpt/A2_TRACE_COMPLETION_012/INTEGRACAO_A2_INVENTARIO.json>) — SHA256 `451b4527b6863efc84d8c0d0e43b29e27fe92fd72141584e9f0d8a9104b80d44`.
- [Revisão matemática independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/TRACE_COMPLETION_012/COMPATIBILIDADE_7/RECIBO_COMPATIBILIDADE_MONTAGEM_SUSY.md>) — SHA256 `8dbc6867fa885c7c50b8b7faa4b1300b80072d4dd9c6bf7c0d168a4bd7153055`.
- [Revisão independente dos leitores V2](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/TRACE_COMPLETION_012/LEITORES_PROPOSTOS/V2/RECIBO_LEITORES_V2.md>) — SHA256 `71ecc1213fd9d8bc1913d9808b1f03c5bf7d859de8a91c39039ad0621ed29926`.
- [Leitores existentes: cópia V2](<C:/IALD/Central de Patentes/Chatgpt/A2_TRACE_COMPLETION_012/PROPOSTA_LEITORES_EXISTENTES_V2.py>) — SHA256 `70db8370e0ca8ebb95d352de837bd870cf26745643608d6aa91851b67d5bbcfb`.
- [Mapa das bandeiras e das duas substituições](<C:/IALD/Central de Patentes/Chatgpt/A2_TRACE_COMPLETION_012/PROPOSTA_MAPA_CONSUMIDORES_V2.json>) — SHA256 `0763849f53694bcce28fb610368c7c8abbc5456762b5ebfe0c4e843dbd7043eb`.
- [Verificações de tipo para o auditor canônico](<C:/IALD/Central de Patentes/Chatgpt/A2_TRACE_COMPLETION_012/src/TGLExt/AuditReaderContracts012.lean>) — SHA256 `eb7581b2da89b4256d22943e0085547de7b478c2e89dfaae3fa6861f8394a357`.
- [Termos completos do contrato antigo](<C:/IALD/Central de Patentes/Chatgpt/A2_TRACE_COMPLETION_012/src/TGLExt/V354RegularLegacyWitness.lean>) — SHA256 `b0c9687acbe2990062c5d1e9035a0e28721c812326b12e11016b11507244c5a7`.
- [Instanciação SUSY concreta](<C:/IALD/Central de Patentes/Chatgpt/A2_SUSY_012/src/TGLExt/V354RegularSusy.lean>) — SHA256 `8cdb715ac6b6daa2151a36f4b67d120bb2297eedefee32b8600e57b691c12d4f`.

As três entregas anteriores de A2 parcial, B1′ e saneamentos a–h estão vinculadas no manifesto; seus conteúdos e recibos não foram sobrescritos.
