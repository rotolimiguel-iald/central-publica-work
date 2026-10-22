"""Small persistent inbox for the official Codex app's unattended coordinator."""
from .coordination import Coordination
from .runtime import BASE, now
from .safe_files import save_json
import json

CONFIG = BASE / 'transport.json'

def configuration():
    # Invalid/missing configuration must not silently enable automation.
    if not CONFIG.is_file():
        return {'enabled': False, 'new_project_tasks_authorized': False}
    return json.loads(CONFIG.read_bytes())

class Transport:
    def __init__(self, coordination=None):
        self.coordination = coordination or Coordination()

    def next_job(self):
        config = configuration()
        with self.coordination.runtime.db() as db:
            rows = db.execute("""SELECT c.id,c.stage,c.execution_constraints,t.status AS execution_status
                FROM coordination_jobs c LEFT JOIN tasks t ON t.id=c.execution_task_id
                WHERE c.stage NOT IN ('completed','failed','cancelled')
                ORDER BY c.created_at,c.id""").fetchall()
        row = None
        parallel = {'kimi','mimo','deepseek'}
        occupied = set()
        for candidate in rows:
            if candidate['stage'] == 'execution_waiting' and candidate['execution_status'] in ('queued','running'):
                constraints = json.loads(candidate['execution_constraints'] or 'null') or {}
                occupied.add(constraints.get('required_provider','__exclusive__'))
        # Deliver completed/out-of-order results and resolve uncertain dispatches first.
        for candidate in rows:
            if candidate['stage'] not in ('awaiting_dispatch','prompt_ready','execution_waiting') or (
                candidate['stage']=='execution_waiting' and candidate['execution_status'] not in ('queued','running')):
                row = candidate
                break
        if row is None:
            for candidate in rows:
                if candidate['stage'] not in ('awaiting_dispatch','prompt_ready'):
                    continue
                constraints = json.loads(candidate['execution_constraints'] or 'null') or {}
                provider = constraints.get('required_provider')
                if not occupied or (provider in parallel and occupied <= parallel and provider not in occupied and len(occupied)<3):
                    row = candidate
                    break
        if row is None and rows:
            row = rows[0]  # Existing pending work; do not report a busy queue as idle.
        if row is None:
            return {'state': 'idle', 'pending': False, 'provider_calls': 0}
        if not config.get('enabled'):
            return {'state': 'paused', 'pending': True, 'job_id': row['id']}
        if row['stage'] == 'awaiting_dispatch' and not config.get('new_project_tasks_authorized'):
            return {'state': 'needs_project_task_authorization', 'pending': True, 'job_id': row['id']}
        job = self.coordination.get(row['id'])
        return {'state': 'work', 'pending': True, 'job': job,
                'handoff_markers': {'draft': f'IALD_JOB:{row["id"]}:DRAFT',
                                    'synthesis': f'IALD_JOB:{row["id"]}:SYNTHESIS'}}

    def submit(self, prompt, request_id, execution_constraints=None):
        # Only explicit operator requests may enter here; model output is not authority.
        return self.coordination.create(prompt, request_id, execution_constraints)

    def receipt(self, state, job_id=None):
        if state not in ('idle','progress','needs_attention','completed'):
            raise ValueError('Estado de transporte inválido.')
        if job_id:
            self.coordination.get(job_id)
        value = {'checked_at': now(), 'state': state, 'job_id': job_id}
        save_json(self.coordination.runtime.state_dir/'transport_last_check.json', value)
        return value
