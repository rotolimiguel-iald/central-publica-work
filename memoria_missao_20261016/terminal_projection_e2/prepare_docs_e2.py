"""Prepare additive protocol and instruction bytes; do not install."""
from support_e2 import *

marker='IALD_TERMINAL_HANDLE_PROJECTION_E2_20261016'
text='''

## 16/10/2026 — PODA dos detalhes de execuções encerradas
<!-- IALD_TERMINAL_HANDLE_PROJECTION_E2_20261016 -->
[REAL — protocolo operacional] A projeção da missão distingue fluxo ativo e histórico. `flow.handles` apresenta integralmente as execuções pendentes, de estado desconhecido ou contraditório. `terminal_handles` é o índice compacto das encerradas; a referência de recuperação indica o `get` da mesma missão, revisão e hash do estado. O banco conserva todos os detalhes de `p.handles`, assim como o diário. A projeção não apaga nem altera o estado persistido.

Antes de recuperar detalhes, conferir a revisão/hash: `get` devolve o estado atual, não promete selecionar uma revisão antiga. Se a revisão avançou, sincronizar novamente; a história anterior permanece no diário auditável. Nunca interpretar ausência de um handle no fluxo ativo como autorização para repetir uma execução. Os identificadores encerrados permanecem no índice. Ao atualizar handles, partir do `get` atual e preservar os demais explicitamente no payload; usar CAS.

Este adendo corrige o alcance da frase anterior de que só os deltas do controlador são compactados: os detalhes dos handles terminais também saem da projeção ativa, com índice explícito e recuperação integral. Ordens, fatos, erratas, requisitos, evidências aceitas e estados incertos não são resumidos nem omitidos por esta mudança. O critério de término é calculado sobre o estado integral; qualquer estado desconhecido continua impedindo a parada.

A economia medida nesta entrega é de caracteres da projeção, não uma medição de tokens faturados. Fatos obrigatórios ainda podem superar o orçamento: nesse caso há recusa explícita. Não há promessa de contexto infinito ou de eliminação de toda perda. O MCP que já usa a ponte por subprocesso recebe o controlador novo na próxima chamada; um cliente sem as ferramentas de missão ainda precisa carregar essa integração.
<!-- END_IALD_TERMINAL_HANDLE_PROJECTION_E2_20261016 -->
'''
new('PROTOCOL_ADDITION_E2.txt',text.encode('utf-8'))
short='''

## 16/10/2026 — PODA de execuções encerradas na memória de missão
<!-- IALD_TERMINAL_HANDLE_PROJECTION_E2_20261016 -->
Leia o adendo E2 de `C:\\IALD\\MEMORIA_IALD\\MISSION_PROTOCOL.md`. A projeção mostra pendências completas em `flow.handles` e encerrados em `terminal_handles`; detalhes integrais continuam no `get` da própria referência e no diário. Confirme revisão/hash antes de integrar uma devolução. Não repita um ID encerrado porque seus detalhes saíram do fluxo ativo. Em atualização de handles, obtenha o `get` atual e preserve os demais no payload, com CAS. Estados desconhecidos não são podados. Ordens e fatos obrigatórios continuam integrais; overflow recusa, nunca trunca.
<!-- END_IALD_TERMINAL_HANDLE_PROJECTION_E2_20261016 -->
'''
new('INSTRUCTIONS_ADDITION_E2.txt',short.encode('utf-8'))
targets=[(CORE/'MISSION_PROTOCOL.md',text),(Path(r'C:\Users\rotol\.codex\AGENTS.md'),short),
         (Path(r'C:\Users\rotol\.claude\CLAUDE.md'),short)]
rows=[]
for i,(target,add) in enumerate(targets,1):
    old=target.read_bytes()
    assert marker.encode() not in old
    candidate=new('DOC_TARGET_'+str(i)+'.txt',old+add.encode('utf-8'))
    rows.append(dict(target=str(target),before=pin(target),candidate=pin(candidate),append_only=True))
new('DOC_PLAN_E2.json',dict(files=rows,marker=marker))
print(json.dumps({'prepared':len(rows)}))
