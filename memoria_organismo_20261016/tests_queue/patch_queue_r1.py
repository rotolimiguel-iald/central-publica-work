"""Apply exact anchored edits to copied queue sources; preserve original baseline."""
from pathlib import Path
W=Path(__file__).resolve().parents[1];Q=W/'staging/queue/iald_orchestrator'
def edit(name, pairs):
 p=Q/name;text=p.read_text(encoding='utf-8')
 for old,new in pairs:
  assert text.count(old)==1,(name,old[:100],text.count(old))
  text=text.replace(old,new)
 p.write_text(text,encoding='utf-8',newline='\n')

edit('operational_memory.py',[
 ("changes = {'flow': {'phase': phase, 'next_action': next_action,\n                       'handles': [{'id': handle_id, 'phase': phase}]}}", "handle_phase = {'result_ready':'returned', 'failed':'uncertain', 'interrupted':'uncertain'}.get(phase, phase)\n    changes = {'flow': {'phase': phase, 'next_action': next_action,\n                       'handles': [{'id': handle_id, 'phase': handle_phase, 'queue_phase':phase, 'no_repeat':True}]}}"),
 ("value = store(runtime).project(reference, SCOPE,\n        max_chars=max_chars or max(6500, len(objective) + len(encode(constraints or {})) + 4000))", "memory = store(runtime)\n    from .queue_activity import runtime_for\n    from iald_memory.mission import MissionController\n    _, mission, _ = MissionController(memory, reference, SCOPE).load_snapshot(state)\n    budget = max_chars or max(125000, len(objective) + len(encode(constraints or {})) + 10000)\n    value = (runtime_for(runtime, reference).project(max_chars=budget) if mission is not None\n             else memory.project(reference, SCOPE, max_chars=budget))"),
 ("body=json.loads(projection['text'].rsplit('\\n',1)[1])", "content=projection['text'].split('\\n<IALD_ACTIVITY_V1>\\n',1)[0]\n    body=json.loads(content.rsplit('\\n',1)[1])\n    if 'activity' in projection: body['activity']=copy.deepcopy(projection['activity'])")])

edit('runtime.py',[
 ('operational_memory as opmem, scientific_binding as binding','operational_memory as opmem, scientific_binding as binding, queue_activity as activity'),
 ('            opmem.init_db(db)\n', "            if 'activity_version' not in {r[1] for r in db.execute('PRAGMA table_info(tasks)')}:\n                db.execute('ALTER TABLE tasks ADD COLUMN activity_version INTEGER NOT NULL DEFAULT 0')\n            activity.init_db(db)\n            opmem.init_db(db)\n"),
 ('memory_context_id=None, scientific_binding_job_id=None):\n        constraints=', 'memory_context_id=None, scientific_binding_job_id=None, activity_parent_job_id=None):\n        constraints='),
 ('        reference = memory_context_id or opmem.context_id(request_id)\n', "        reference = memory_context_id or opmem.context_id(request_id)\n        if memory_context_id:\n            if not activity_parent_job_id:\n                raise ValueError('Explicit server coordination parent required; no scope inference')\n            activity.validate_parent(self, activity_parent_job_id, prompt, request_id, routing_prompt, reference)\n"),
 ("            return self.task(existing['id'])\n", "            if existing['activity_version'] == 1:\n                activity.admit(self,'task',existing['id'],activity_parent_job_id)\n            return self.task(existing['id'])\n"),
 ('memory_context_id,scientific_binding_job_id) VALUES(?,?,?,?,?,\'queued\',?,?,?,?)', 'memory_context_id,scientific_binding_job_id,activity_version) VALUES(?,?,?,?,?,\'queued\',?,?,?,?,1)'),
 ('        opmem.sync(self, reference)\n        if start_worker:', "        opmem.sync(self, reference)\n        activity.admit(self,'task',task_id,activity_parent_job_id)\n        if start_worker:"),
 ('        event = self.cancel_events.get(task_id)\n', "        # Hold is durable before cancellation can race a received return.\n        if task['activity_version'] == 1:\n            activity.cancel(self,'task',task_id,'Authorized queue cancellation; no remote retry.')\n        event = self.cancel_events.get(task_id)\n"),
 ('        attempt_id = None\n', '        attempt_id = None\n        activity_started = False\n        returned = False\n'),
 ("            self._memory_phase(task_id, 'prepared')", "            activity.load(self,'task',task_id)\n            activity.refresh(self,'task',task_id)\n            self._memory_phase(task_id, 'prepared')"),
 ('            result = providers.execute(decision["selected"], prompt, workspace, cancel=cancel, memory_packet=packet, execution_constraints=c,', "            activity.preflight(self,'task',task_id)\n            activity_started = True\n            # Rebuild the packet on the exact post-intent revision before effect.\n            projection=binding.project(self,task['memory_context_id'],routing_prompt or prompt,task['original_execution_constraints'],task['scientific_binding'])\n            packet=nos_packet.prepare_queue(prompt,c,providers.SYSTEM,decision['selected'],operational_projection=projection)\n            controls.enforce_packet(packet,c,providers.SYSTEM)\n            activity.verify_dispatch(self,task_id,packet)\n            result = providers.execute(decision[\"selected\"], prompt, workspace, cancel=cancel, memory_packet=packet, execution_constraints=c,"),
 ('            # The provider return is durable before any optional follow-up call.\n', "            # Full raw bytes are durable even if cancel/stale/accounting wins next.\n            activity.raw_return(self,'task',task_id,result)\n            returned = True\n            self._update(task_id,result=result)\n            parent, _, _ = activity.load(self,'task',task_id)\n            outcome=activity.complete(self,'task',task_id,result,terminal=parent['parent_id'] is None)\n            # The provider return is durable before any optional follow-up call.\n"),
 ('            if not cancel.is_set() and self.task(task_id)["status"] != "cancelled":\n', '            if not outcome["integrated"]:\n                if self.task(task_id)["status"] != "cancelled":\n                    self._update(task_id,status="review_required",error="Received result preserved; activity reconciliation required: "+outcome["error"])\n                return\n            if not cancel.is_set() and self.task(task_id)["status"] != "cancelled":\n'),
 ('        except Exception as exc:\n            if isinstance(exc, providers.ProviderLimitError):', '        except Exception as exc:\n            if activity_started and not returned:\n                try: activity.uncertain(self,"task",task_id,"Provider dispatch interrupted; no automatic resend.")\n                except Exception: pass  # durable intent itself remains unresolved\n            if isinstance(exc, providers.ProviderLimitError):'),
 ('            if attempt_id:\n                with self.db() as db:\n                    db.execute("UPDATE attempts SET finished_at=?,status=\'failed_or_interrupted\' WHERE id=?", (now(), attempt_id))', '            if attempt_id and not returned:\n                with self.db() as db:\n                    db.execute("UPDATE attempts SET finished_at=?,status=\'failed_or_interrupted\' WHERE id=?", (now(), attempt_id))'),
 ('                self._update(task_id, status="failed", error=message[:600])', '                self._update(task_id, status="review_required" if returned else "failed", error=message[:600])')])

edit('coordination.py',[
 ('operational_memory as opmem, scientific_binding as binding','operational_memory as opmem, scientific_binding as binding, queue_activity as activity'),
 ("            if 'execution_constraints' not in", "            if 'activity_version' not in {r[1] for r in db.execute('PRAGMA table_info(coordination_jobs)')}:\n                db.execute('ALTER TABLE coordination_jobs ADD COLUMN activity_version INTEGER NOT NULL DEFAULT 0')\n            if 'execution_constraints' not in"),
 ("            return self.get(existing['id'])\n", "            row=activity._row(self.runtime,'coord',existing['id'])\n            if row['activity_version']==1: activity.admit(self.runtime,'coord',existing['id'])\n            return self.get(existing['id'])\n"),
 ("stage,execution_constraints,memory_context_id) VALUES(?,?,?,?,?,?,?,?)", "stage,execution_constraints,memory_context_id,activity_version) VALUES(?,?,?,?,?,?,?,?,1)"),
 ('        return self.get(job_id)\n\n    def get', "        activity.admit(self.runtime,'coord',job_id)\n        return self.get(job_id)\n\n    def get"),
 ('    def act(self,job_id,action,payload=None):\n', '''    def act(self,job_id,action,payload=None):
        payload={} if payload is None else payload
        if not isinstance(payload,dict): raise ValueError('Payload must be an object')
        if any(k in payload for k in ('actor','scope','context_id','ticket','review_evidence','evidence_path')):
            raise ValueError('Server identity/evidence is not a model argument')
        # Work results are durable before hold/epoch checks or stage transitions.
        if action in ('accept_prompt','complete','complete_without_work'):
            activity.raw_return(self.runtime,'coord',job_id,{'action':action,'payload':payload},suffix='received-'+action)
        if action not in ('cancel','fail','sync_execution'):
            activity.refresh(self.runtime,'coord',job_id)
        if action=='cancel': activity.cancel(self.runtime,'coord',job_id,'Authorized coordination cancellation.')
        if action=='accept_prompt':
            result=activity.complete(self.runtime,'coord',job_id,{'prompt':payload.get('prompt')},terminal=False,suffix='draft')
            if not result['integrated']: raise ValueError('Draft return preserved; activity stale')
        if action=='complete':
            result=activity.complete(self.runtime,'coord',job_id,{'text':payload.get('text')},terminal=False,suffix='synthesis')
            if not result['integrated']: raise ValueError('Synthesis return preserved; activity stale')
        value=self._act(job_id,action,payload)
        if value['stage'] in ('draft_dispatching','synthesis_dispatching') and action in ('begin_draft','begin_synthesis'):
            value['activity_dispatch']=activity.preflight(self.runtime,'coord',job_id,'draft' if action=='begin_draft' else 'synthesis')
        if value['stage']=='completed' and action in ('complete','complete_without_work','begin_synthesis'):
            value['activity_completion']=activity.complete(self.runtime,'coord',job_id,{'text':value['final_text'],'source':value['synthesis_source']},terminal=True)
            if not value['activity_completion']['integrated']:
                value['activity_reconciliation_required']=True
        return value

    def _act(self,job_id,action,payload=None):
'''),
 ("scientific_binding_job_id=job_id if job['scientific_binding'] else None)\n                value=self._change", "scientific_binding_job_id=job_id if job['scientific_binding'] else None,activity_parent_job_id=job_id)\n                value=self._change"),
 ("if task['status'] in ('failed','cancelled','interrupted'):", "if task['status'] in ('failed','cancelled','interrupted','review_required'):")])
print('Exact anchored patches applied to staging only.')
