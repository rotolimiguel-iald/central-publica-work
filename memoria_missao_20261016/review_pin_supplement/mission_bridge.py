"""Mission tools for the existing MCP; exact references, no implicit latest task."""
from pathlib import Path
import json
import subprocess

PYTHON=Path(r'C:\Python314\python.exe')
CLI=Path(r'C:\IALD\MEMORIA_IALD\mission_cli.py')


def invoke(request: dict) -> dict:
    # All path/scope/content validation is shared with the installed local CLI.
    result=subprocess.run([str(PYTHON),'-B','-X','utf8',str(CLI)],
        input=json.dumps(request,ensure_ascii=False,allow_nan=False),
        text=True,encoding='utf-8',capture_output=True,timeout=45)
    try:payload=json.loads(result.stdout)
    except (ValueError,TypeError):raise RuntimeError('Mission CLI failed without a valid receipt') from None
    if result.returncode or payload.get('ok') is not True:
        raise ValueError('Mission synchronization refused: '+str(payload.get('error'))+': '+str(payload.get('message')))
    return payload['result']


def register_tools(server):
    @server.tool()
    def iald_mission_sync(reference: str, after_revision: int | None = None, wait_ms: int = 0, max_chars: int = 24000) -> dict:
        """Recupera a missão EXATA. Espera local até 30s, sem modelo; nunca adota a tarefa mais recente."""
        req={'operation':'project' if after_revision is None else 'poll','reference':reference,'max_chars':max_chars}
        if after_revision is not None:req.update(after_revision=after_revision,wait_ms=wait_ms)
        return invoke(req)

    @server.tool()
    def iald_mission_preflight(reference: str, task_id: str, actor_id: str, lease_id: str, expected_revision: int, projection_sha256: str) -> dict:
        """Antes de ação material: recusa revisão obsoleta, dependência alterada, pausa e posse vencida."""
        return invoke({'operation':'check','reference':reference,'task_id':task_id,
            'actor':{'id':actor_id,'kind':'agent'},'lease_id':lease_id,
            'expected_revision':expected_revision,'projection_sha256':projection_sha256})

    @server.tool()
    def iald_mission_transition(request: dict) -> dict:
        """Transição local CAS com evento estável e evidências. Não autentica operador nem autoriza publicação.

        configure/extend/claim/submit/accept/release/block/invalidate/hold/amend.
        Copie referência exata e revisão de sync. accept exige revisor distinto;
        o chamador local continua responsável por autenticação e revisão real.
        """
        if request.get('operation') not in {'configure','extend','claim','submit','accept','release','block','invalidate','hold','amend'}:
            raise ValueError('Unsupported mission transition')
        return invoke(request)

    @server.tool()
    def iald_mission_handoff(reference: str, task_id: str, actor_id: str, lease_id: str, expected_revision: int, projection_sha256: str) -> dict:
        """Pacote exato para agente delegado; retorno posterior exige nova sincronização antes de integrar."""
        req={'operation':'handoff','reference':reference,'task_id':task_id,'actor':{'id':actor_id,'kind':'agent'},
            'lease_id':lease_id,'expected_revision':expected_revision,'projection_sha256':projection_sha256}
        return invoke(req)
