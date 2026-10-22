[REAL] Contrato tipado e instâncias na torre/qubit compilados. [INPUT] Lei de custo e proveniência do reflexo. [OPEN] Atestação física, custo medido e reconstrução gravitacional geral.

# ENTREGA 057 — definição tipada do conteúdo do colapso

08/09/2026 · bancada ChatGPT → gerência Claude · responde diretamente à definição do operador. Entrega espontânea posterior à 056.

**Objeto entregue:** TGLCollapseSpecification reúne IdentityCollapse, CollapseCostLaw e ReflectionProtocol. AttestedTGLCollapse exige testemunho; typed_collapse_content explicita estabilidade, identidade, ausência de inversa à esquerda, custos e evidência.

**Medição:** 60 teoremas; 26 definições/abreviações/estruturas; 86 sondagens de axiomas; 171 verificações Python. Sem erros/avisos no build final. Registros de teste exclusivamente sintéticos.

## Critérios de aceitação

| Pedido | Situação | Evidência |
|---|---|---|
| Definição unificada do conteúdo | PAGO como contrato | TGLCollapseSpecification; typed_collapse_content |
| Fixação e preservação | PAGO no modelo | E²=E, E(1)=1, ωE=ω; densidades positivas com traço 1 |
| Irreversibilidade efetiva | PAGO | X não nulo com E(X)=0; duas densidades puras distintas com mesma saída |
| Reflexo sem autodeclaração | PAGO como exigência | AttestedTGLCollapse e testes de recusa |
| Meia-nat e ln2/oitava | PAGO na tipagem [INPUT] | Componentes separados; valor físico permanece aberto |
| Seleção física de resultado e pagamento medido | NÃO PAGO [OPEN] | Ramo requer registro; nenhum dado físico fornecido |
| Incorporação no um.py | PENDENTE da gerência | Fontes e proposta Python prontas para auditoria |

“PAGO” refere-se ao critério da entrega; não declara custo termodinâmico pago.

## Arquivos principais e SHA256 lidos

- C:/IALD/Central de Patentes/Chatgpt/COLAPSO_TIPADO_20260908_175047_534231/DEFINICAO_TIPADA_DO_COLAPSO.md
  SHA256: 0f01aaa1764b6a820f302c87086ef037492c2a717eb7aaac79590259b783c70c
- C:/IALD/Central de Patentes/Chatgpt/COLAPSO_TIPADO_20260908_175047_534231/INTEGRACAO057.json
  SHA256: a471ae307560ddbb5b07cfa74fdd8a9a4025bd86a5dc9b01b73cd67bfba8ea34
- C:/IALD/Central de Patentes/Chatgpt/COLAPSO_TIPADO_20260908_175047_534231/MANIFESTO057.json
  SHA256: 455b937c3fc1a52ff665be60b6f7dce446e33577596fd0785ff7707697184e7a
- C:/IALD/Central de Patentes/Chatgpt/COLAPSO_TIPADO_20260908_175047_534231/BASELINE.json
  SHA256: e775b100516333c9134e2bb952f58841425df96c25bd6539ed40d0ef33b77afd
- C:/IALD/Central de Patentes/Chatgpt/COLAPSO_TIPADO_20260908_175047_534231/collapse_contract_proposal.py
  SHA256: 01245fe37e19853e60f7ab341c1a659db54e1bf4f5205df9fd8cbedcfebde5f8
- C:/IALD/Central de Patentes/Chatgpt/COLAPSO_TIPADO_20260908_175047_534231/check_collapse_contract.py
  SHA256: b25b1a3c78c55abb8241cd088bdd612466174706f8bce60dd7308fd69144ef18
- C:/IALD/Central de Patentes/Chatgpt/COLAPSO_TIPADO_20260908_175047_534231/build_collapse.py
  SHA256: 89430b6551a34d9651c7346813faa4649a751936a253691c64b3824747225f10
- C:/IALD/Central de Patentes/Chatgpt/COLAPSO_TIPADO_20260908_175047_534231/audit_collapse_delivery.py
  SHA256: 57c188f65b1b1dbc2fb8c6bce0c80505b6cf5806e49801d5b0d57e5c2b26b3f4
- C:/IALD/Central de Patentes/Chatgpt/COLAPSO_TIPADO_20260908_175047_534231/AUDITORIA_20260908_180823_152715.json
  SHA256: 96c4c78bf685953565afeb081ba343328c7b3607d2a371051fc109921b5970a6
- C:/IALD/Central de Patentes/Chatgpt/COLAPSO_TIPADO_20260908_175047_534231/BUILD_20260908_180521_986301/BUILD_RESULT.json
  SHA256: 46333dead80c73126207f353f78c4893331aaed81658d5554babf79e2ccc7711

## Fontes Lean e contagens

| Módulo | Teoremas | Outras declarações | SHA256 |
|---|---:|---:|---|
| CollapseContract | 11 | 3 | f03d28aea33837971a8c8f9f68d08ac655893fe8c1f87f29c45e501d61f1f829 |
| CollapseCostAndAttestation | 15 | 7 | fdedc8b94b721cb63e9d7b2a28e20db875965f3791bf38e01cb4aba88215dab4 |
| TowerCollapseRealization | 9 | 3 | fdcfb522ee0efae36bd7205b13149178b709a9c039c4a8820cca35491c566785 |
| QuantumCollapseWitness | 25 | 13 | 2d8f520d4db3ce00a29b685e807015c6fe8af58551e272060a2ac2d8a72903fa |

Todos os módulos acima estão em: C:/IALD/Central de Patentes/Chatgpt/COLAPSO_TIPADO_20260908_175047_534231.

## Reprodução exata

```powershell
& 'C:\Python314\python.exe' -B 'C:/IALD/Central de Patentes/Chatgpt/COLAPSO_TIPADO_20260908_175047_534231/build_collapse.py' CollapseContract CollapseCostAndAttestation TowerCollapseRealization QuantumCollapseWitness
& 'C:\Python314\python.exe' -B 'C:/IALD/Central de Patentes/Chatgpt/COLAPSO_TIPADO_20260908_175047_534231/audit_collapse_delivery.py'
```

Os scripts criam builds/relatórios novos sob esta pasta e leem o canônico. Nunca executam ou importam o um.py. A auditoria falha visivelmente se o baseline original mudou; mudança legítima da gerência exige novo baseline em nova entrega, sem apagar o anterior.

## Axiomas dos enunciados centrais

```text
ChatgptAudit.Collapse057.reflection_of_output_cannot_restore_input: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Collapse057.fair_bit_entropy_is_not_half_nat: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Collapse057.typed_collapse_content: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Collapse057.typed_collapse_has_no_self_attestation: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Collapse057.actual_tower_collapse_no_inverse: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Collapse057.opposite_phases_same_reduction: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Collapse057.pure_densities_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Collapse057.density_reduction_no_inverse: [propext, Classical.choice, Quot.sound]
```

As 86 sondagens estão nos logs e em BUILD_RESULT.json. Só propext, Classical.choice e Quot.sound são admitidos; nenhum sorryAx no build aceito.

## Limites que a incorporação deve preservar

A expectativa sobre M_ω não é identificada com a expectativa sobre D da entrega 055. O regime totalmente tracial fornece E=id e não passa pelo critério de redução efetiva. O qubit não seletivo produz mistura; o ramo individual depende do rótulo observado. J involutivo não é o mapa irreversível.

A igualdade localNats=1/2 é campo explícito da lei proposta, não dedução automática de entropia. O valor entrópico do qubit equiprovável é ln2, provado distinto de 1/2. Identificador ou hash não certifica independência física; o verificador externo é entrada a auditar. Mock de teste jamais deve tornar-se verificador operacional.

A origem do um.py e as 13 fontes selecionadas foram conferidas; os textos embutidos correspondem às fontes, normalizados apenas os finais de linha. A compilação usa binários canônicos preexistentes: não recompila integralmente todas as dependências transitivas.

## O que não foi feito

Não se alterou um.py, kernel, Atlas, índice, diário, selo ou gate. Não se derivou Born ou uma ocorrência física individual; não se recebeu reflexo externo real nem se mediu pagamento; não se fechou H3 ou a reconstrução gravitacional geral. A revisão independente é responsabilidade da gerência, ainda pendente.

## Tentativas preservadas

TENTATIVAS_PRESERVADAS.json cataloga os builds, inclusive falhas de simplificação logarítmica e configuração/provas matriciais. Seus logs com falha e todos os backups de bytes permanecem. Builds parciais aceitos e a rodada anterior ao contrato unificado são históricos; o build de referência é o apontado nesta entrega.

## Integração e memória

Seguir INTEGRACAO057.json: auditar, transpor os imports locais para TGLExt, embutir pelo mecanismo do arquivo único e só então registrar nas superfícies canônicas aplicáveis, sob as ordens vigentes e com backups de bytes. A bancada conserva o registro novo nesta pasta; nenhuma memória canônica foi tocada.
