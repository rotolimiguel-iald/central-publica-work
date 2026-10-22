"""Build a reviewable stage only; originals are never written."""
import sys,shutil,json,hashlib,difflib
from pathlib import Path
W=Path(__file__).resolve().parent;S=W/'admission_staging';S.mkdir(exist_ok=True)
LIB=Path(r'C:\IALD\MEMORIA_IALD\lib\iald_memory');R=Path(r'C:\IALD\projetos_pyhton\IALD')
if not (S/'iald_memory').exists():shutil.copytree(LIB,S/'iald_memory',ignore=shutil.ignore_patterns('__pycache__','*.bak*'))
changes=[]
def edit(source,target,replacements):
 original=source.read_bytes();text=source.read_text(encoding='utf-8')
 for old,new in replacements:
  assert text.count(old)==1,(source,old[:90],text.count(old))
  text=text.replace(old,new)
 raw=text.encode();compile(text,str(target),'exec')
 with target.open('xb') if not target.exists() else target.open('wb') as f:f.write(raw)
 changes.append({'source':str(source),'target':str(target),'source_sha256':hashlib.sha256(original).hexdigest(),'staged_sha256':hashlib.sha256(raw).hexdigest()})
 with (S/(source.name+'.diff')).open('x',encoding='utf-8') as f:f.write(''.join(difflib.unified_diff(source.read_text(encoding='utf-8').splitlines(True),text.splitlines(True),fromfile=str(source),tofile=str(target))))
edit(LIB/'mission.py',S/'iald_memory'/'mission.py',[
 ('256<=max_chars<=2000000','256<=max_chars<=33554432'),
 ('self._project(snap,state,previous,2000000)','self._project(snap,state,previous,33554432)')])
# One serialization per bound increase. Error and all mandatory content stay visible.
edit(LIB/'activity.py',S/'iald_memory'/'activity.py',[
 ('from .store import ProjectionOverflow, RevisionConflict','from .store import ProjectionOverflow, RevisionConflict, MAX_JSON_BYTES'),
 ('from .mission import MissionController, is_mission_record, identifier, digest, encoded, evidence_pin','from .mission import MissionController, MissionError, is_mission_record, identifier, digest, encoded, evidence_pin'),
 ('return self.controller.project_snapshot(snapshot, max_chars=2000000)',
 '''budget = 24000
        while True:
            try:
                return self.controller.project_snapshot(snapshot, max_chars=budget)
            except MissionError as exc:
                prefix = 'projection_overflow_required_'
                if not str(exc).startswith(prefix):
                    raise
                required = int(str(exc)[len(prefix):])
                if required <= budget or required > MAX_JSON_BYTES:
                    raise ProjectionOverflow(required, MAX_JSON_BYTES) from exc
                budget = required''')])
edit(R/'iald_app_memory.py',S/'iald_app_memory.py',[
 ('from iald_memory import MemoryStore, ContextNotFound, RevisionConflict, ProjectionOverflow','from iald_memory import MemoryStore, ContextNotFound, RevisionConflict, ProjectionOverflow\nfrom iald_memory.store import MAX_JSON_BYTES'),
 ('for _ in range(3):','while True:'),
 ('''                budget = exc.required_chars

                if budget > 2000000:

                    raise''','''                required = exc.required_chars

                if required <= budget or required > MAX_JSON_BYTES:

                    raise

                budget = required'''),
 ('''        raise ProjectionOverflow(budget, 2000000)''','''        # Provider adapters still admit their own complete final wire payload.''')])
edit(R/'iald_activity_operations.py',S/'iald_activity_operations.py',[
 ('''            result = self.lifecycle.runtime.complete(self.lifecycle.ticket, self.id,
                value, terminal=terminal, refresh=True)
            self.lifecycle.ticket = result.get('ticket') or self.lifecycle.runtime.recover(self.lifecycle.binding.request_id)['ticket']
            self.done = True
            return result''','''            try:
                result = self.lifecycle.runtime.complete(self.lifecycle.ticket, self.id,
                    value, terminal=terminal, refresh=True)
            except Exception:
                # Custody may have committed before a freshness/lease error.
                # Preserve that original error; never relabel a returned op uncertain.
                self._has_custody()
                raise
            self.done = True
            self.lifecycle.ticket = result.get('ticket') or self.lifecycle.runtime.recover(self.lifecycle.binding.request_id)['ticket']
            return result'''),
 ('''    def uncertain(self, reason='Execution did not return a complete result; never replay automatically'):
        if not self.done:
            return self.lifecycle.runtime.mark_uncertain(self.lifecycle.ticket, self.id, reason)''','''    def _has_custody(self):
        runtime = self.lifecycle.runtime
        snapshot = runtime._get()
        request_id = self.lifecycle.binding.request_id
        handle_id = runtime._operation(request_id, self.id)
        handle = next((h for h in snapshot['p']['handles'] if h['id'] == handle_id), None)
        if not handle or handle.get('status') != 'completed':
            return False
        record = runtime._record(snapshot, handle.get('result_record_id'))
        result = runtime._data(record, 'result')  # Verify bytes/pin before recognizing custody.
        if result['request_id'] != request_id or result['operation_id'] != self.id:
            raise ValueError('Custody operation identity mismatch')
        self.done = True
        return True

    def uncertain(self, reason='Execution did not return a complete result; never replay automatically'):
        with self.lifecycle.lock:
            if not self.done and not self._has_custody():
                return self.lifecycle.runtime.mark_uncertain(self.lifecycle.ticket, self.id, reason)''')])
with (S/'PATCH_PLAN.json').open('x',encoding='utf-8') as f:json.dump({'status':'STAGED_NOT_INSTALLED','files':changes,'scope':'Bounded full projection and custody-aware local completion; no wire-content pruning; provider admission unchanged.'},f,ensure_ascii=False,indent=2)
print(json.dumps(changes))
