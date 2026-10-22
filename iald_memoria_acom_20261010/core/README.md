# Núcleo de memória IALD — inscrição, estado e fluxo

[REAL — implementação em staging] Biblioteca Python exclusivamente stdlib. A instalação é responsabilidade da gerência; esta pasta não modifica a produção. Destino acordado: `C:\IALD\MEMORIA_IALD\lib\iald_memory`; estado único: `C:\IALD\MEMORIA_IALD\state`.

A biblioteca preserva a inscrição UTF-8 original byte a byte, inclusive CRLF, em um envelope zlib/SHA-256. A relação reutilizada de `acom_codec.py` é sua separação explícita entre representação REFLECT/MANIFEST e compressão sem perdas de bytes por DEFLATE. Não importa o aplicativo, NumPy, código selado ou o programa `um.py`. Não afirma compressão de bytes pela raiz quadrada, acesso ao KV-cache, instalação nos pesos ou armazenamento do tensor interno de um provedor.

O estado `q` reúne registros tipados. O fluxo `p` reúne fase, próxima ação e identificadores de trabalho. São estado operacional próprio da IALD, gravado na mesma transação; a relação com a linguagem da teoria tem estatuto de adaptação de engenharia. Autoridade e autenticação permanecem no aplicativo chamador. Receber `actor.kind='operator'` significa que o chamador autenticou essa origem; o núcleo sozinho não a autentica.

## API pública

```python
from iald_memory import MemoryStore

store = MemoryStore(root)
scope = {'house': 'IALD', 'principal': 'operator'}
actor = {'id': 'coordinator', 'kind': 'agent'}

snapshot = store.ensure_context(
    context_id,
    objective='Texto original, sem resumo',  # str ou bytes UTF-8
    scope=scope,
    actor={'id': 'operator', 'kind': 'operator'},
    constraints={'max_calls': 1},
    parent_id=None,
)
snapshot = store.get(context_id, scope)
projection = store.project(context_id, scope, max_chars=12000, current_input='pedido atual')
receipt = store.transition(
    context_id, scope, expected_revision=snapshot['revision'], event_id='evento-estavel',
    actor=actor,
    changes={
        'candidates': [{
            'id': 'resultado-estavel', 'text': 'Saída integral recebida',
            'statute': 'DECLARADO',
            'source': {'kind': 'executor', 'ref': 'job:identidade-real'},
        }],
        'flow': {'phase': 'result_ready', 'next_action': 'verificar fontes',
                 'handles': [{'id': 'job', 'job_id': 'identidade-real', 'status': 'result_ready'}]},
    },
)
receipt = store.receipt(context_id, scope)
verification = store.verify(context_id, scope)
```

`scope` exige exatamente `house` e `principal`. Toda entrada verifica isolamento, inclusive filhos e replay. Contextos filhos herdam as restrições integralmente e só podem apontar a pai do mesmo escopo. Identificadores: ASCII `[A-Za-z0-9][A-Za-z0-9_.:-]{0,159}`. Atores: `operator`, `agent`, `model`, `measurement`, `system`.

`ensure_context` retorna snapshot. Repetir a mesma âncora é idempotente; mudar objetivo, bytes, ator original, pai ou restrições na mesma identidade causa `AnchorConflict`. Objetivo e restrições não aparecem entre os campos mutáveis. Erratas são novos registros com `supersedes`; o texto original permanece. Uma saída de modelo ou executor só pode entrar como `candidate/DECLARADO`; um ator `model` não estabelece âncora nem altera fluxo.

Forma completa de um registro:

```json
{"id":"registro","kind":"candidate","text":"conteúdo integral","statute":"DECLARADO","sources":[{"kind":"model","ref":"job:123"}],"meta":{}}
```

Campos permitidos: `id`, `kind`, `text`, `statute`, `sources`, opcionais `supersedes` e `meta`. Tipos: `fact`, `decision`, `candidate`, `contradiction`, `pending`, `erratum`. Estatutos: `INPUT`, `DECLARADO`, `REAL`, `DERIVED`, `POSTULATE`, `CONJECTURE`, `ONTO`, `KNOWN`, `OPEN`, `LEGAL`. Fonte exige `kind` e `ref`, admite `sha256` hexadecimal e outros metadados JSON. Tipos de fonte: `artifact`, `operator`, `model`, `executor`, `measurement`, `document`, `tool`. A fonte é referência fornecida, não uma prova automaticamente validada pelo núcleo.

`changes` aceita `records`, o atalho `candidates`, e `flow`. No fluxo, `phase` e `next_action` substituem o valor corrente com história preservada; `handles` faz merge por `id`, preservando identificadores remotos não modificados. O núcleo não envia nem reenvia trabalhos. Não há campo que conceda autorização ou mova gate.

Snapshot: `context_id`, `scope`, `objective`, `objective_bytes_b64`, `objective_sha256`, `anchor_sha256`, `constraints`, `parent_id`, `anchor_actor`, `revision`, `q.records`, `p.phase`, `p.next_action`, `p.handles`, `state_sha256`, `receipt`.

Recibo: `context_id`, `scope`, `revision`, `event_id`, `event_hash`, `objective_sha256`, `anchor_sha256`, `state_sha256`, `replayed`. Revisão inicial zero. A transição exige CAS. Replay de mesmo `event_id`, ator e conteúdo normalizado devolve o recibo original, mesmo se a revisão esperada ficou antiga. Reuso de evento com outro conteúdo é recusado. Conflito de revisão autoriza somente recuperar o estado e tentar novamente a escrita local idempotente; nunca repetir uma chamada remota incerta.

Projeção: `text`, `receipt`, `included_record_ids`, `omitted_record_ids`, `overflow`, `required_chars`, `actual_chars`, `projection_sha256`, `current_input_sha256`. A seleção é determinística e preserva objetivo, restrições e fluxo completos. Original e cadeia de erratas formam bloco inseparável. Se o obrigatório não cabe, lança `ProjectionOverflow` com `required_chars/max_chars`. A omissão do restante é declarada; `get` recupera o conteúdo inteiro. Ler/projetar nunca poda o ledger, altera q/p ou reforça memória implicitamente.

`verify` reexecuta a mesma verificação integral usada nas leituras, em processo novo se desejado. Retorna `ok`, `event_count`, `objective_bytes`, `receipt` e `validation_scope='local_integrity_and_replay_only'`.

Exceções exportadas: `MemoryError` (base ValueError), `InvalidInput`, `ContextNotFound`, `ScopeViolation`, `AnchorConflict`, `RevisionConflict`, `IdempotencyConflict`, `IntegrityError`, `ProjectionOverflow`, `InvariantViolation`.

## Persistência e limites

SQLite em modo DELETE, transações `BEGIN IMMEDIATE`, sincronização FULL, CAS e índices únicos. Objetivo e eventos têm guardas contra UPDATE/DELETE. Toda leitura confere a âncora, a descompressão e os hashes, a sequência contínua de revisões e a reconstrução determinística de q/p. Antes de cada mutação, os bytes do banco completo são copiados na mesma pasta para `.bak_DATA_HORA_UUID` sob o lock de escrita, com tamanho e SHA-256 conferidos. Backups não são apagados. Falha antes de commit ou morte do processo reverte o estado inteiro pela recuperação transacional do SQLite.

Hashes e guardas detectam alterações inconsistentes e não constituem autenticação contra alguém que reescreva deliberadamente banco inteiro, hashes e programa. O recibo externo guardado pelo chamador é a âncora independente para comparar continuidade. Esta versão não implementa assinatura criptográfica, administração de ACL, rotação de backups ou garantia de integridade diante de hardware que não honre fsync.

Limites explícitos: objetivo/texto até 16 MiB UTF-8; payload ou estado JSON até 32 MiB; backup completo antes de escrita; replay integral e snapshots completos por evento. Isso privilegia rastreabilidade, com custo crescente de disco e leitura. Escala de longa duração exige medir esses custos antes de ampliar, preservando os mesmos invariantes. Ultrapassar limite produz recusa visível, nunca resumo substituindo a fonte. Não há migração automática de banco desconhecido.

## Fontes reutilizadas e estatutos

O inventário detalhado com hashes lidos do disco está em `SOURCE_INVENTORY.json`. O Atlas §VIII separa registro e inscrição, preserva o índice anterior e exige correção ao lado. A fonte Lean `TheExplosion.lean` demonstra propriedades de elemento idempotente sob hipóteses explícitas; isso não prova automaticamente a implementação SQLite. O código é verificado pelos testes de engenharia desta pasta.

`holographic_memory.py` é a implementação anterior de redução textual: mantém persistência apenas em dicionário de processo e pode descartar turnos/frases. É reutilizável como referência histórica de projeção, não como guarda da inscrição. `iald_orchestrator/matrix.py` já constrói um estado matricial finito para a seleção de provedores; não é tensor interno desses provedores. `ACOMPsibitV4` histórico usa quantização e constante literal antiga: não foi importado nem promovido a fonte vigente.

## Validação local

`C:\Python314\python.exe -X utf8 -m unittest discover -s tests -v`

17 testes passaram nesta entrega, incluindo cinco escritores em processos concorrentes, perda de processo depois do INSERT e antes do commit, adulteração de âncora/cadeia, CAS, replay, isolamento, restrições dos filhos, proibição de promoção de modelo, preservação de CRLF e projeção de erratas sem perda do original. Nenhum teste chama modelo ou usa conta de produção. A aprovação independente cabe à gerência.

## Correção ao lado — 10/10/2026, auditoria P1 de projeção

A versão inicialmente entregue podia omitir uma decisão posterior e mostrar só o objetivo original quando o orçamento era pequeno. A auditoria independente reproduziu isso com `Deliver route A` seguido de uma decisão `route B`. Esse comportamento estava errado: a omissão visível de um ID não bastava para preservar o comando vigente.

Leitura e contrato atuais: todos os registros `fact`, `decision`, `contradiction`, `pending` e `erratum` são obrigatórios na projeção, assim como candidatos com `meta.required=true`. Qualquer cadeia de `supersedes` conectada a um registro obrigatório também é obrigatória por inteiro. O objetivo original continua preservado e identificado como ORIGINAL; a decisão e a correção posteriores seguem ao lado em `records`. Isso não promove candidato a fato nem permite a modelo conceder autorização.

O campo `required_chars` passa a medir âncora + restrições + fluxo + estado obrigatório completo. Se esse conjunto não cabe, `project` lança `ProjectionOverflow`; não devolve uma projeção utilizável que tenha perdido steering, contradição, pendência ou fato consolidado. Somente candidatos opcionais podem aparecer em `omitted_record_ids`. O resultado ganhou `required_record_ids` para auditoria. `meta` deve ser objeto JSON e `meta.required`, se presente, booleano.

A validação atual compreende **20 testes aprovados**, incluindo casos negativos de mudança de rota, todos os tipos de estado consolidado, candidato explicitamente obrigatório e correção com ancestral candidato. O registro histórico dos 17 testes acima permanece como retrato da primeira entrega; esta correção foi feita somente na cópia de staging e aguarda reavaliação independente. Integrações devem tipar decisões/instruções posteriores como estado obrigatório; não devem escondê-las como candidatos opcionais.
