"""Versioned mission control on the existing ACOM ledger, not a second database.

The projection is an evolving materialized index. Historical records are never
deleted. Local OS authorization remains the trust boundary; receipts are not
proof of human authority, scientific truth, or execution in model weights.
"""
from __future__ import annotations
import copy
import hashlib
import json
import re
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from . import guard
from .store import RevisionConflict, IdempotencyConflict

PROTOCOL = 'iald-mission/v1'
KEY = 'iald_mission_state_v1'
TERMINAL = {'satisfied', 'superseded'}
STATES = {'open','working','review_pending','satisfied','needs_revalidation','blocked','superseded'}
ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,159}\Z', re.ASCII)


class MissionError(ValueError):
    pass


def encoded(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(x):
    return hashlib.sha256(encoded(x).encode('utf-8')).hexdigest()


def require(condition, reason):
    if not condition:
        raise MissionError(reason)


def identifier(x):
    require(isinstance(x,str) and ID.fullmatch(x), 'invalid_identifier')
    return x


def now():
    return time.time()


def evidence_pin(value):
    require(isinstance(value,dict) and set(value)=={'path','sha256'}, 'evidence_requires_path_and_sha256')
    require(isinstance(value['sha256'],str) and re.fullmatch('[0-9a-f]{64}',value['sha256']), 'invalid_evidence_hash')
    final,raw=guard.read_checked(value['path'],max_bytes=64*1024*1024,where='mission.evidence')
    require(len(raw)<=64*1024*1024,'evidence_too_large')
    require(hashlib.sha256(raw).hexdigest()==value['sha256'],'evidence_hash_mismatch')
    return {'path':str(final),'sha256':value['sha256']}


def pins(values):
    require(isinstance(values,list) and 0<len(values)<=100,'evidence_required')
    return [evidence_pin(v) for v in values]


def is_mission_record(r):
    # Models may attach arbitrary metadata to candidates, never execute that metadata.
    return r.get('kind')=='fact' and r.get('statute')=='REAL' and KEY in r.get('meta',{})


def manifest_check(requirements):
    require(isinstance(requirements,list) and 0<len(requirements)<=500,'requirements_required')
    result={}
    for r in requirements:
        require(isinstance(r,dict) and set(r)=={'id','criterion','depends_on'},'requirement_schema')
        i=identifier(r['id'])
        require(i not in result,'duplicate_requirement')
        require(isinstance(r['criterion'],str) and 0<len(r['criterion'])<=6000,'criterion_required')
        require(isinstance(r['depends_on'],list) and all(isinstance(d,str) for d in r['depends_on']),'dependency_schema')
        require(len(set(r['depends_on']))==len(r['depends_on']),'duplicate_dependency')
        result[i]=copy.deepcopy(r)
    visited=set()
    def visit(i,stack):
        require(i in result,'missing_dependency')
        require(i not in stack,'dependency_cycle')
        if i in visited:return
        for d in result[i]['depends_on']:visit(d,stack|{i})
        visited.add(i)
    for i in result:visit(i,set())
    return result


class MissionController:
    def __init__(self,store,context_id,scope):
        guard.assert_scope_allowed(scope)
        self.store,self.context_id,self.scope=store,context_id,scope

    def load(self):
        snap=self.store.get(self.context_id,self.scope)
        records=[r for r in snap['q']['records'] if is_mission_record(r)]
        previous=None
        state=None
        for record in records:
            require(record.get('supersedes')==previous,'mission_lineage_broken')
            delta=record['meta'][KEY]
            require(delta['protocol']==PROTOCOL,'mission_protocol_mismatch')
            if 'configure' in delta:
                require(state is None,'duplicate_mission_configuration')
                state=copy.deepcopy(delta['configure'])
            else:
                require(state is not None,'mission_delta_without_anchor')
                for k,v in delta.get('fields',{}).items():
                    require(k in {'hold','hold_reason'},'invalid_mission_field')
                    state[k]=copy.deepcopy(v)
                for i,t in delta.get('tasks',{}).items():
                    state['tasks'][i]=copy.deepcopy(t)
            previous=record['id']
        return snap,state,previous

    def _project(self,snap,state,previous,max_chars):
        require(state is not None,'mission_not_initialized')
        tasks=state['tasks']
        for t in tasks.values():
            if t['status']=='satisfied':
                pins(t['evidence']);pins(t['review_evidence'])
        active=[]
        settled=[]
        for i,t in tasks.items():
            row={'id':i,**copy.deepcopy(t)}
            row['ready']=t['status'] in {'open','needs_revalidation'} and all(tasks[d]['status']=='satisfied' for d in t['depends_on'])
            (settled if t['status'] in TERMINAL else active).append(row)
        terminal_handle_states={'completed','returned','failed','cancelled','closed','accepted','consumed','done','terminated'}
        unresolved_handles=[]
        for h in snap['p']['handles']:
            values=[h[k] for k in ('phase','status') if k in h]
            if not values or any(not isinstance(v,str) or v not in terminal_handle_states for v in values):
                unresolved_handles.append(h)
        done=all(t['status']=='satisfied' for t in tasks.values()) and not unresolved_handles
        # An erratum may correct one clause, not replace the entire prior order.
        # Only controller deltas are compacted; all other source records stay visible.
        current_records=[r for r in snap['q']['records'] if not is_mission_record(r)]
        body={'protocol':PROTOCOL,'context_id':self.context_id,'scope':self.scope,
            'objective':snap['objective'],'objective_sha256':snap['objective_sha256'],
            'constraints':snap['constraints'],'revision':snap['revision'],
            'state_sha256':snap['receipt']['state_sha256'],'mission_record_id':previous,
            'hold':state['hold'],'hold_reason':state['hold_reason'],
            'active':active,'settled':settled,'tetelestai':done,
            'current_records':current_records,'flow':snap['p'],
            'unresolved_handles':unresolved_handles,
            'next_ready':[] if state['hold'] or done else [r['id'] for r in active if r['ready']],
            'history':{'operation':'get','context_id':self.context_id,'records':len(snap['q']['records'])},
            'scope_note':'Operational satisfaction only. Original and history preserved. No scientific gate changes.'}
        require(type(max_chars) is int and 256<=max_chars<=2000000,'invalid_projection_budget')
        text=encoded(body)
        require(len(text)<=max_chars,f'projection_overflow_required_{len(text)}')
        guard.assert_clean_text(text,'mission.project')
        return {'projection':body,'projection_sha256':digest(body),'actual_chars':len(text),
                'receipt':snap['receipt']}

    def project(self,max_chars=24000):
        return self._project(*self.load(),max_chars)

    def poll(self,after_revision,wait_ms=0,max_chars=24000):
        require(type(after_revision) is int and after_revision>=0,'invalid_revision')
        require(type(wait_ms) is int and 0<=wait_ms<=30000,'invalid_wait')
        end=time.monotonic()+wait_ms/1000
        while True:
            value=self.project(max_chars)
            require(after_revision<=value['receipt']['revision'],'revision_from_future')
            if value['receipt']['revision']>after_revision:
                return {'changed':True,**value}
            if time.monotonic()>=end:
                return {'changed':False,'receipt':value['receipt'],'projection_sha256':value['projection_sha256']}
            time.sleep(min(.25,max(0,end-time.monotonic())))

    def _current(self,request,snap,state,previous):
        require(type(request.get('expected_revision')) is int,'expected_revision_required')
        require(request['expected_revision']==snap['revision'],'stale_revision_refresh_required')
        p=self._project(snap,state,previous,2000000)
        require(request.get('projection_sha256')==p['projection_sha256'],'stale_projection_refresh_required')

    def _task(self,state,request):
        i=identifier(request.get('task_id'))
        require(i in state['tasks'],'unknown_requirement')
        return i,state['tasks'][i]

    def _lease(self,t,actor,request):
        lease=t.get('lease')
        require(lease and lease['id']==request.get('lease_id'),'lease_mismatch')
        require(lease['owner']==actor['id'],'lease_owner_mismatch')
        require(lease['expires_at']>now(),'lease_expired_explicit_recovery_required')
        require(lease['task_epoch']==t['epoch'],'lease_epoch_mismatch')

    def _dependencies(self,state,t):
        pending=list(t['depends_on']);seen=set()
        while pending:
            d=pending.pop()
            if d in seen:continue
            seen.add(d)
            dep=state['tasks'][d]
            require(dep['status']=='satisfied','dependencies_not_satisfied')
            pins(dep['evidence'])
            pins(dep['review_evidence'])
            pending.extend(dep['depends_on'])

    def check(self,request):
        snap,state,previous=self.load()
        return self._check(request,snap,state,previous)

    def _check(self,request,snap,state,previous):
        self._current(request,snap,state,previous)
        require(not state['hold'],'mission_on_hold')
        i,t=self._task(state,request)
        require(t['status']=='working','task_not_working_or_already_satisfied')
        self._lease(t,request['actor'],request)
        self._dependencies(state,t)
        return {'ready':True,'task_id':i,'criterion':t['criterion'],'receipt':snap['receipt'],
                'lease_id':t['lease']['id'],'projection_sha256':request['projection_sha256']}

    def handoff(self,request):
        snap,state,previous=self.load()
        checked=self._check(request,snap,state,previous)
        return {'reference':request['reference'],'preflight':checked,
            **self._project(snap,state,previous,request.get('max_chars',24000)),
            'instruction':'Read this exact mission before work and after resumption. Before material actions run sync then preflight. Submit pinned candidate; never mark yourself accepted. If stale, recover and reconcile; never repeat an uncertain provider call.'}

    def action(self,request):
        require(isinstance(request,dict),'request_object_required')
        guard.assert_clean_text(encoded(request),'mission.action')
        op=request.get('operation')
        require(op in {'configure','extend','claim','submit','accept','release','block','invalidate','hold','amend'},'unknown_mission_operation')
        actor=request.get('actor')
        require(isinstance(actor,dict) and set(actor)=={'id','kind'} and actor['kind']=='agent','trusted_local_agent_required')
        identifier(actor['id'])
        event=identifier(request.get('event_id'))
        request_hash=digest(request)
        snap,state,previous=self.load()
        old_state=copy.deepcopy(state)
        # Retry the same event returns its existing receipt; changed payload is refused.
        for r in snap['q']['records']:
            if is_mission_record(r) and r.get('meta',{}).get('mission_event_id')==event:
                require(r['meta']['request_sha256']==request_hash,'idempotency_conflict')
                return {'replayed':True,'record_id':r['id'],'receipt':snap['receipt']}
        require(type(request.get('expected_revision')) is int and request['expected_revision']==snap['revision'],'stale_revision_refresh_required')
        if op=='configure':
            require(state is None,'mission_already_initialized')
            manifest=manifest_check(request['requirements'])
            sources=pins(request['sources'])
            state={'protocol':PROTOCOL,'hold':False,'hold_reason':'','tasks':{}}
            for i,r in manifest.items():
                state['tasks'][i]={**r,'status':'open','epoch':0,'lease':None,
                    'evidence':[],'review_evidence':[],'submitted_by':None,'reviewed_by':None,
                    'attempts':0,'note':''}
        else:
            # An explicit invalidation must remain possible when pinned bytes changed.
            if op in {'invalidate','hold'}:
                require(request.get('state_sha256')==snap['receipt']['state_sha256'],'state_receipt_required_for_invalidation')
            else:self._current(request,snap,state,previous)
            sources=[]
            if op=='extend':
                require(isinstance(request.get('reason'),str) and request['reason'],'reason_required')
                additions=manifest_check(request['requirements']) if not state['tasks'] else {r['id']:r for r in request['requirements']}
                require(len(additions)==len(request['requirements']) and not set(additions)&set(state['tasks']),'duplicate_requirement')
                combined=[{k:t[k] for k in ['id','criterion','depends_on']} for t in state['tasks'].values()]+request['requirements']
                manifest=manifest_check(combined);sources=pins(request['sources'])
                for i in additions:
                    state['tasks'][i]={**manifest[i],'status':'open','epoch':0,'lease':None,
                        'evidence':[],'review_evidence':[],'submitted_by':None,'reviewed_by':None,'attempts':0,'note':request['reason']}
            elif op=='hold':
                require(type(request.get('hold')) is bool,'hold_must_be_boolean')
                require(isinstance(request.get('reason'),str) and request['reason'],'reason_required')
                sources=pins(request['sources'])
                state['hold'],state['hold_reason']=request['hold'],request['reason']
            else:
                i,t=self._task(state,request)
                if op=='claim':
                    require(not state['hold'],'mission_on_hold')
                    require(t['status'] in {'open','needs_revalidation'},'already_claimed_or_satisfied')
                    self._dependencies(state,t)
                    seconds=request.get('lease_seconds',3600)
                    require(type(seconds) is int and 60<=seconds<=43200,'invalid_lease_duration')
                    t['status']='working';t['epoch']+=1;t['attempts']+=1
                    t['lease']={'id':str(uuid.uuid4()),'owner':actor['id'],'task_epoch':t['epoch'],
                                'expires_at':now()+seconds}
                elif op=='submit':
                    require(t['status']=='working','task_not_working')
                    self._lease(t,actor,request)
                    self._dependencies(state,t)
                    sources=pins(request['evidence'])
                    t.update(status='review_pending',evidence=sources,submitted_by=actor['id'],lease=None,
                             review_evidence=[],reviewed_by=None,note=request.get('note',''))
                elif op=='accept':
                    require(not state['hold'],'mission_on_hold')
                    require(t['status']=='review_pending','no_candidate_to_accept')
                    require(t['submitted_by']!=actor['id'],'independent_reviewer_required')
                    self._dependencies(state,t)
                    pins(t['evidence']);sources=pins(request['review_evidence'])
                    t.update(status='satisfied',review_evidence=sources,reviewed_by=actor['id'],note=request.get('note',''))
                elif op in {'release','block'}:
                    require(t['status']=='working','task_not_working')
                    # Expired work is not silently retried; the owner supplies a recovery reason and receipt.
                    require(t.get('lease',{}).get('owner')==actor['id'],'lease_owner_mismatch')
                    require(isinstance(request.get('reason'),str) and request['reason'],'reason_required')
                    sources=pins(request['sources'])
                    t.update(status='blocked' if op=='block' else 'open',lease=None,note=request['reason'])
                    t['epoch']+=1
                elif op in {'invalidate','amend'}:
                    require(isinstance(request.get('reason'),str) and request['reason'],'reason_required')
                    sources=pins(request['sources'])
                    if op=='amend':
                        require(isinstance(request.get('criterion'),str) and 0<len(request['criterion'])<=6000,'criterion_required')
                        t['criterion']=request['criterion']
                    affected={i}
                    while True:
                        more={j for j,q in state['tasks'].items() if set(q['depends_on'])&affected}
                        if more<=affected:break
                        affected|=more
                    for j in affected:
                        q=state['tasks'][j]
                        q.update(status='needs_revalidation',lease=None,note=request['reason'])
                        q['epoch']+=1
        # Every mutation is one ACOM event: no second mutable store or dual-write window.
        record_id='mission_'+event
        delta={'protocol':PROTOCOL}
        if old_state is None:
            delta['configure']=state
        else:
            delta['fields']={k:state[k] for k in ['hold','hold_reason'] if state[k]!=old_state[k]}
            delta['tasks']={k:v for k,v in state['tasks'].items() if v!=old_state['tasks'].get(k)}
        meta={KEY:delta,'mission_event_id':event,'request_sha256':request_hash}
        record={'id':record_id,'kind':'fact','statute':'REAL',
                'text':f'Operational mission transition: {op}. Scientific truth and human permissions are not inferred.',
                'sources':[{'kind':'artifact','ref':s['path'],'sha256':s['sha256']} for s in sources]
                   or [{'kind':'artifact','ref':'acom:'+self.context_id+':'+str(snap['revision']),
                        'sha256':snap['receipt']['state_sha256']}],
                'meta':meta}
        if previous:record['supersedes']=previous
        try:
            result=self.store.transition(self.context_id,self.scope,snap['revision'],event,actor,
                {'records':[record],'flow':{'phase':'mission_held' if state['hold'] else 'mission_sync',
                 'next_action':'Use current mission projection and preflight before each material action.'}})
        except (RevisionConflict,IdempotencyConflict):
            # Same-event racing callers can generate distinct lease UUIDs before CAS.
            # Only the committed request hash decides replay; no external work is retried.
            latest=self.store.get(self.context_id,self.scope)
            for r in latest['q']['records']:
                if is_mission_record(r) and r.get('meta',{}).get('mission_event_id')==event:
                    require(r['meta']['request_sha256']==request_hash,'idempotency_conflict')
                    return {'replayed':True,'record_id':r['id'],'receipt':latest['receipt']}
            raise
        return {'replayed':False,'receipt':result,'record_id':record_id,
                'task':state['tasks'].get(request.get('task_id')),
                'next':'project: recompute satisfaction, pinned evidence and unresolved handles'}
