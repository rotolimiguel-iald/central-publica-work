"""DRAFT ONLY: eight append fragments and application proposals; never apply."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
OLD=WORK.parent/'mimo26_upgrade_20261020/memory_final/RFINAL3/PLAN.json'
ACTOR='codex-goodall-01a15aaa-d85e-7d01-bf9b-89747fc482d3'
MARKER='IALD_MIMO_MEDIA_CAPACITY_20261020_DRAFT_NEGATIVES_PRESERVED'


def digest(raw):return hashlib.sha256(raw).hexdigest()


def put(name,value):
    raw=value if isinstance(value,bytes) else json.dumps(value,ensure_ascii=False,indent=2).encode('utf-8')
    path=HERE/name
    if path.exists():raise RuntimeError('Draft already exists; no overwrite: '+name)
    with path.open('xb') as stream:stream.write(raw)
    if path.read_bytes()!=raw:raise RuntimeError('Draft bytes differ')
    return dict(path=str(path),sha256=digest(raw),bytes=len(raw))


def main():
    prior=json.loads(OLD.read_bytes());facts=json.loads((HERE/'FACTS_VERIFICATION_DRAFT.json').read_bytes())
    project=json.loads((HERE/'MISSION_PROJECT_DRAFT.json').read_bytes())['result']
    preflight=json.loads((HERE/'OWN_ACTOR_PREFLIGHT_DRAFT.json').read_bytes())
    sources=json.loads((HERE/'SOURCES.json').read_bytes())
    targets=[Path(row['path']) for row in prior['surfaces']]
    if len(targets)!=8 or len({str(path).casefold() for path in targets})!=8:
        raise RuntimeError('Exactly eight inherited operational surfaces required')
    if any('escritorio' in str(path).casefold() for path in targets):raise RuntimeError('Wrong house')
    paragraph=f'''## 20/10/2026 — Mídia MiMo: engenharia ampliada; negativos e pendências preservados
<!-- {MARKER} -->
[DRAFT/NÃO APLICADO — candidato preparado por {ACTOR}; aplicação somente pelo pai após revisão real, fontes atualizadas e preflight próprio.]

[REAL — fontes operacionais] A missão bcf544f7-1878-5d27-b532-f1e1aad466aa permanece na revisão8 consultada. FINAL_RUNTIME_PINS.json registra19 arquivos efetivos como retrato, NÃO como plano de instalação. BOOTSTRAP_LIVE_R7.json registra correção de bootstrap/mídia legada e UI sob o mesmo supervisor web. As instalações capability_R2 e availability_deploy_R1 têm recibos próprios: áudio-only passou a uma política sem alternativa fictícia FPS/resolução e houve separação de saúde de conexão de recusa por pedido. Isso não transforma pedido recusado em sucesso, nem autoriza repetição de execução incerta.

[REAL — verificação deste DRAFT] Na leitura de preparação,15/19 hashes do manifesto efetivo conferiram e quatro JS divergiram. A mudança posterior desses JS exige recibo/pinos atualizados; este texto NÃO afirma qual versão posterior está disponível. Ciência v394 conferida5/5 contra SCIENCE_BASELINE.json, sem executar um.py/Lean, sem alterar kernel/selo/gate. O manifesto de19 anterior é preservado como fonte histórica, sem atualização automática.

[REAL — engenharia, NÃO validação geral de percepção] Upload privado até37_499_904bytes, reservando margem para URI Base64 até50_000_000bytes; JSON final até64_000_000bytes. Retirados os tetos arbitrários de áudio30s/vídeo10s: duração real, bytes, contexto, FPS/resolução e cobertura integral do vídeo controlam admissão. Texto/TGL/histórico completos são preservados; áudio/vídeo têm estimativa separada com folga explícita; imagens legadas conservam bound anterior. Janela1048576, saída técnica dinâmica até131072 e piso16384; teto2048frames, sem cap silencioso. Capacidade de transporte/contexto NÃO demonstra percepção correta de todo áudio/vídeo.

[REAL — negativos custodiados] Pedido automático recusado pelo gate media_policy0,68<0,70 após resposta JEV HTTP200; custo estimado US$0.000837816, sem fingir sucesso ou custo zero. Áudio sintético120s: job terminou, mas resultado semântico PERCEPTION_FAILURE; tokens/ledger correspondem a US$0.12155292 estimados pelas tarifas configuradas, não fatura. A discrepância job completed/carteira cancelled com chamada liquidada fica preservada; causa/percepção não foram isoladas. Vídeo30s: falhou após309,913s; transporte/usage incompletos/incertos; débito ledger US$0.478237695 é cap reservado estimado, NÃO consumo medido do fornecedor nem fatura. Não reabrir nem repetir esses IDs.

[REAL/ESTIMADO — custos] TEST_COST_ROLLUP_R1.json recompõe US$0.6712981122 combinados, incluindo testes anteriores; componente vídeo é pessimista/estimado e não deve virar cobrança medida por redação. Cache só quando informado por usage. Nenhuma nova chamada foi feita para preparar esta memória. [INPUT/OPEN] Pergunta humana sobre US$0.50 extras continua pendente; não presume autorização para novo teste pago.

[INPUT/OPEN — disponibilidade no recorte deste rascunho] iOS4.1(35)/Android4.1(30) preparados; não declarar build executada, publicada, disponível nas lojas ou instalada fisicamente com base nesta preparação. Recibo posterior deverá atualizar essa matriz. Web/backend possuem recibos de instalação anteriores, mas o conjunto efetivo corrente precisa reconciliar os quatro JS divergentes. Alertas financeiros/infraestrutura continuam administrativos; contas, carteira, consentimentos MiMo2/Auto3 e cotas globais preservados.

[OPEN — fechamento operacional] Este pacote não aplica apêndices, não move mapa/quadro nem fecha missão; exige revisão real distinta e aplicação pelo pai com backup imediato de BYTES na mesma pasta, CAS de cada superfície e escrita atômica. O lease de aplicação pertence a codex-app-01a094df; preflight do preparador retornou lease_owner_mismatch e não foi contornado. Tetelestai/aceite final, percepção geral, reconciliação do vídeo incerto, autorização extra e disponibilidade posterior não são inferidos.

Fontes locais desta atualização: C:/IALD/Central de Patentes/work/mimo_media_capacity_20261020/FINAL_RUNTIME_PINS.json; BOOTSTRAP_LIVE_R7.json; host_followup/capability_R2/deployment.json; host_followup/availability_deploy_R1/deployment.json; live_stage/MANUAL_AUDIO_RESULT.json; live_stage/MANUAL_VIDEO_RESULT.json; live_stage/TEST_COST_ROLLUP_R1.json; SCIENCE_BASELINE.json; REVIEW_BUILD_PUSH_PHASE_R8.json. Pinos/tamanhos das fontes: memory_stage/SOURCES.json; divergências: FACTS_VERIFICATION_DRAFT.json. Referência própria: SESSION_REFERENCE.json nessa missão. Diário Claude fica em MEMORY_2.md; MEMORY.md conserva somente ponte ao diário. Atlas é fonte única: apenas este fragmento aditivo é proposto, sem copiar/bifurcar seu corpo.
<!-- END_{MARKER} -->
'''
    rows=[]
    for index,target in enumerate(targets,1):
        raw=target.read_bytes()
        if MARKER.encode() in raw:raise RuntimeError('Marker already in authoritative memory')
        newline='\r\n' if b'\r\n' in raw else '\n'
        suffix=('\n\n'+paragraph).replace('\n',newline).encode('utf-8')
        frag=put(f'APPEND_{index:02}.txt',suffix)
        rows.append(dict(path=str(target),before_sha256=digest(raw),before_bytes=len(raw),
            append=frag,expected_after_sha256=digest(raw+suffix),expected_after_bytes=len(raw)+len(suffix),
            operation='APPEND_ONLY_DRAFT_NOT_APPLIED',
            backup_plan=dict(path_template=str(target)+'.bak_{YYYYMMDD_HHMMSS_microseconds}',
                required_before_any_write=True,copy_mode='raw rb/wb byte-for-byte in SAME directory',
                verify_source_and_backup_sha256_equals_before=True,do_not_delete_backup=True),
            application_guard='Parent fresh CAS + real review; temporary file verify then atomic replace; restore backup on unexplained shrink'))
    index_path=targets[6].with_name('MEMORY.md')
    index_raw=index_path.read_bytes()
    index_policy=dict(path=str(index_path),sha256=digest(index_raw),bytes=len(index_raw),
        existing_bridge_to_MEMORY_2=b'MEMORY_2.md' in index_raw,operation='NO_CHANGE_REUSE_EXISTING_BRIDGE',
        new_diary_here=False,maximum_index_bytes=24576)
    if not index_policy['existing_bridge_to_MEMORY_2']:raise RuntimeError('Claude index bridge missing; parent clarification required')
    plan=dict(schema='iald.memory-append-plan/v1',status='DRAFT_DO_NOT_APPLY',
        reference=str(WORK/'SESSION_REFERENCE.json'),actor=dict(id=ACTOR,kind='agent'),
        mission_revision=project['receipt']['revision'],marker=MARKER,surfaces=rows,
        inherited_surface_list=dict(path=str(OLD),sha256=digest(OLD.read_bytes())),
        sources=sources,index_policy=index_policy,atlas_full_copy_created=False,backups_created=False,
        source_reconciliation_required=[r for r in facts['runtime'] if not r['matches']],
        own_actor_preflight=preflight['response'],lease_owner='codex-app-01a094df',
        apply_allowed=False,review_accepted=False,board_moved=False,map_moved=False,
        parent_requirements=['Reconcile effective JS pins and later availability receipts before apply',
            'Fresh own-actor owner preflight; do not impersonate owner or reuse stale revision',
            'Real reviewer different from preparer; keep all negative/uncertain cost results',
            'Immediate byte backups/CAS in original folders; additive atomic append only'])
    plan_pin=put('PLAN_DRAFT.json',plan)
    route=json.loads((WORK/'ROUTE_START.json').read_bytes())
    put('MAP_ROUTE_FINAL_RECEIPT_DRAFT.json',dict(status='DRAFT_NOT_RECORDED',route_id=route['rota_id'],
        reference=plan['reference'],source=plan_pin,verdict='ENGINEERING_DELIVERY_WITH_NEGATIVE_PERCEPTION_AND_OPEN_ITEMS',
        proposed_final=False,move_now=False,required_next_action='Parent source reconciliation + real review + fresh preflight',
        negative_results_preserved=True,science_gate_changed=False))
    put('BOARD_FINAL_RECEIPT_DRAFT.json',dict(status='DRAFT_NOT_SUBMITTED',unit='F9.MIMO_MEDIA_CAPACITY_20261020',
        owner='codex-app-01a094df',reference=plan['reference'],evidence_candidate=plan_pin,
        transition_now=False,final_status_requested_now=False,accepted_by=None,
        blockers=['15/19 current manifest matches; four JS require newer source',
            'Semantic audio failure/video uncertain remain explicit; no success by execution flag',
            'Extra USD0.50 pending; mobile execution/distribution needs subsequent receipts',
            'Owner preflight and independent review not replaced by this draft']))
    put('DELIVERY_DRAFT.json',dict(status='DRAFT_PREPARED_NOT_APPLIED',plan=plan_pin,
        surfaces=8,current_runtime_matches=facts['current_matches'],runtime_manifest_rows=19,
        science_matches=5,own_actor_preflight=preflight['response'],index_policy=index_policy,
        real_review_pending=True,source_refresh_pending=True,runtime_writes=False,
        authoritative_memory_writes=0,board_mutations=0,map_mutations=0,provider_calls=0,
        note='Application belongs to parent after review; this preparer contains no apply mode'))
    print(json.dumps(dict(status='DRAFT_PREPARED_NOT_APPLIED',surfaces=8,plan=plan_pin,
                         authoritative_memory_writes=0,apply_allowed=False),ensure_ascii=False))


if __name__=='__main__':main()
