"""Local OS-authenticated CLI/MCP surface: opaque ledger IDs, no arbitrary pins."""
from . import queue_activity

def invoke(runtime, request):
    allowed={'operation','entity_kind','entity_id','max_chars'}
    if not isinstance(request,dict) or set(request)-allowed:
        raise ValueError('Unknown or privileged activity argument')
    kind=request.get('entity_kind')
    if kind not in ('task','coord'): raise ValueError('Invalid entity kind')
    op=request.get('operation')
    if op=='activity_get':
        return queue_activity.recover(runtime,kind,request['entity_id'])
    if op=='activity_project':
        return queue_activity.describe(runtime,kind,request['entity_id'],request.get('max_chars',125000))
    if op=='activity_reconcile':
        return queue_activity.reconcile(runtime,kind,request['entity_id'])
    raise ValueError('Activity operation not exposed; review/actor/evidence remain privileged')

def register_tools(server,runtime):
    @server.tool()
    def iald_activity_get(entity_kind:str,entity_id:str)->dict:
        """Estado da atividade do ledger local exato; sem reenvio ou aceite."""
        return invoke(runtime,dict(operation='activity_get',entity_kind=entity_kind,entity_id=entity_id))
    @server.tool()
    def iald_activity_project(entity_kind:str,entity_id:str,max_chars:int=125000)->dict:
        """ACOM e missão da mesma revisão; overflow visível, sem identidade escolhida pelo modelo."""
        return invoke(runtime,dict(operation='activity_project',entity_kind=entity_kind,entity_id=entity_id,max_chars=max_chars))
    @server.tool()
    def iald_activity_reconcile(entity_kind:str,entity_id:str)->dict:
        """Concilia apenas retorno já durável. Nunca reenvia provedor nem aceita requisito."""
        return invoke(runtime,dict(operation='activity_reconcile',entity_kind=entity_kind,entity_id=entity_id))
