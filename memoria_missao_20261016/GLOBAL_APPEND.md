
## 16/10/2026 — Ancoragem evolutiva da missão e PODA operacional
<!-- IALD_MISSION_SYNC_20261016 -->
[INPUT — ordem do operador] Antes de retomar missão longa ou coordenar agentes, ler `C:\IALD\MEMORIA_IALD\MISSION_PROTOCOL.md`, referenciado também no README que o bloco inicial manda carregar. Usar a referência EXATA da missão, nunca a tarefa mais recente de outra sessão. ACOM conserva a inscrição; `mission_cli.py` e MCP `iald_mission_*` mantêm requisitos, revisões, dependências e evidências. Sincronizar ao iniciar/retomar, antes de ação material e antes de integrar a devolução de um agente. Handoff e compactação carregam referência, task_id, lease_id, revisão, critério e pendência concreta.

Requisito satisfeito/revisado é retirado do trabalho ativo; alteração em premissa exige revalidação. Estado obsoleto, evidência rompida ou envio incerto impedem avanço silencioso. `tetelestai` exige os critérios satisfeitos e nenhuma execução pendente. Modelos geram candidatos; aceite exige revisor real distinto. Não fabricar autenticação pelo nome de ator. O protocolo não autoriza ações, não muda pesos, não move gate e não reinicia MCP. Clientes legados precisam aderir explicitamente; CLI absoluto funciona sem afirmar que uma sessão antiga recarregou ferramentas.
<!-- END_IALD_MISSION_SYNC_20261016 -->
