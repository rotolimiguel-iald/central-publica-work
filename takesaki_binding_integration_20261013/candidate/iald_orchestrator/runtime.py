"""Persistent local queue, bounded execution and append-only attempt accounting."""
from __future__ import annotations

from datetime import datetime, timezone
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import sqlite3
import threading
import uuid

from . import VERSION, providers, jev, canonical_memory, request_controls as controls, nos_packet, jev_body_shadow, operational_memory as opmem, scientific_binding as binding
from .policy import route, validate_prompt, classify
from .process_lock import process_lock

BASE = Path(__file__).resolve().parents[1]


def now():
    return datetime.now(timezone.utc).isoformat()


class Runtime:
    def __init__(self, state_dir=None, *, recover=True, memory_root=None):
        self.state_dir = Path(state_dir or BASE / "state")
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.memory_root = Path(memory_root or (opmem.COMMON_STATE if state_dir is None else self.state_dir / "operational_memory"))
        self.db_path = self.state_dir / "tasks.sqlite3"
        self.worker_lock = threading.Lock()
        self.cancel_events = {}
        self.processes = {}
        recovered=[]
        with self.db() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS tasks (
                  id TEXT PRIMARY KEY, request_id TEXT UNIQUE NOT NULL, prompt TEXT NOT NULL,
                  created_at TEXT NOT NULL, updated_at TEXT NOT NULL, status TEXT NOT NULL,
                  decision TEXT, result TEXT, error TEXT);
                CREATE TABLE IF NOT EXISTS attempts (
                  id INTEGER PRIMARY KEY, task_id TEXT NOT NULL, provider TEXT NOT NULL,
                  started_at TEXT NOT NULL, finished_at TEXT, status TEXT NOT NULL, usage TEXT);
                CREATE TABLE IF NOT EXISTS provider_blocks (
                  provider TEXT PRIMARY KEY, reported_at TEXT NOT NULL, reason TEXT NOT NULL);
            """)
            if 'routing_prompt' not in {r[1] for r in db.execute('PRAGMA table_info(tasks)')}:
                db.execute('ALTER TABLE tasks ADD COLUMN routing_prompt TEXT')
            if 'execution_constraints' not in {r[1] for r in db.execute('PRAGMA table_info(tasks)')}:
                db.execute('ALTER TABLE tasks ADD COLUMN execution_constraints TEXT')
            if "memory_context_id" not in {r[1] for r in db.execute("PRAGMA table_info(tasks)")}:
                db.execute("ALTER TABLE tasks ADD COLUMN memory_context_id TEXT")
            if "memory_version" not in {r[1] for r in db.execute("PRAGMA table_info(tasks)")}:
                db.execute("ALTER TABLE tasks ADD COLUMN memory_version INTEGER NOT NULL DEFAULT 0")
            opmem.init_db(db)
            controls.init(db)
            binding.init_db(db)
            if recover:
                with process_lock(self.db_path, blocking=False) as idle:
                    if idle:
                        for row in db.execute("SELECT * FROM tasks WHERE status IN ('running','queued')").fetchall():
                            revision=row['memory_version']+1
                            if row['memory_context_id']:recovered.append((row['id'],row['memory_context_id']))
                            if row['memory_context_id']:
                                opmem.stage(db,row['memory_context_id'],row['routing_prompt'] or row['prompt'],json.loads(row['execution_constraints'] or 'null'),
                                    'task:'+row['id']+':'+str(revision),phase='interrupted',handle_id=row['id'],next_action='Recuperar evidência; NÃO repetir execução interrompida ou incerta.')
                            db.execute("UPDATE tasks SET status='interrupted',error='Servidor reiniciado; revise antes de reenviar.',updated_at=?,memory_version=? WHERE id=?",(now(),revision,row['id']))

        for task_id,reference in recovered:
            self._flush_memory(task_id,reference)

    @contextmanager
    def db(self):
        db = sqlite3.connect(self.db_path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def source_status(self):
        manifest = json.loads((BASE / "provenance.json").read_text(encoding="utf-8"))
        statuses = []
        for source in manifest["sources"]:
            path = Path(source["path"])
            try:
                matches = hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"]
            except OSError:
                matches = False
            statuses.append({"path": str(path), "matches": matches, "role": source["role"]})
        return {"ok": all(s["matches"] for s in statuses), "sources": statuses,
                "scope": manifest["scope"]}

    def counts(self):
        with self.db() as db:
            return {r["provider"]: r["n"] for r in db.execute(
                "SELECT provider,count(*) AS n FROM attempts WHERE started_at>=? GROUP BY provider",
                (datetime.now(timezone.utc).date().isoformat(),))}

    def status(self):
        with self.db() as db:
            tasks = [dict(r) for r in db.execute(
                "SELECT id,created_at,updated_at,status,error FROM tasks ORDER BY created_at DESC LIMIT 30")]
        return {"version": VERSION, "canonical_memory": canonical_memory.status(), "providers": self.connections(), "jev": jev.availability(), "jev_body": jev_body_shadow.status(),
                "coordinator": json.loads((BASE / "coordinator.json").read_text(encoding="utf-8")),
                "sources": self.source_status(), "attempts_today": self.counts(), "tasks": tasks,
                "scope": "Resposta e artefato textual; sem execução arbitrária de comandos ou edição dos originais.",
                "quality_status": "NOT_BENCHMARKED", "physical_verdict_allowed": False}

    def connections(self):
        rows = [dict(row) for row in providers.discover()]
        with self.db() as db:
            blocks = {r["provider"]: dict(r) for r in db.execute("SELECT * FROM provider_blocks")}
        for row in rows:
            if row["id"] in blocks:
                row.update(status=("paused_by_rite" if row["status"] == "paused_by_rite" else "provider_limit_reported"), quota_status="REQUIRES_USER_RECHECK",
                           limit_report=blocks[row["id"]])
        return rows

    def block_provider(self, provider, reason):
        with self.db() as db:
            db.execute("INSERT OR REPLACE INTO provider_blocks VALUES(?,?,?)", (provider, now(), reason))

    def request_recheck(self, provider):
        # Explicit admin action allows a future submitted task to try again;
        # it does not assert that the provider reset its quota.
        if provider not in {p["id"] for p in providers.discover()}:
            raise ValueError("Conexão desconhecida.")
        with self.db() as db:
            db.execute("DELETE FROM provider_blocks WHERE provider=?", (provider,))
        return {"status": "retry_allowed_on_next_task", "provider": provider,
                "quota_status": "NOT_RECHECKED_WITH_PROVIDER"}

    def preview(self, prompt, execution_constraints=None, *, memory_context_id=None, scientific_binding_job_id=None):
        if not self.source_status()["ok"]:
            raise ValueError("Âncora do Supercondutor mudou ou não pôde ser lida; conferir antes de selecionar.")
        # Preview is always local and never consumes external API credit.
        c=controls.normalize(execution_constraints)
        supplement=None
        anchor_constraints=c
        if scientific_binding_job_id:
            with self.db() as db:
                job=db.execute('SELECT * FROM coordination_jobs WHERE id=?',(scientific_binding_job_id,)).fetchone()
                expected,supplement=binding.effective(db,job)
            if not supplement or expected!=c or prompt!=job['prompt'] or memory_context_id!=job['memory_context_id']:raise ValueError('Preview binding differs')
            binding.ready(self,supplement)
            anchor_constraints=None
        projection=(opmem.projection(self,memory_context_id,prompt,anchor_constraints) if memory_context_id else opmem.preview_projection(prompt,c))
        projection=binding.project(self,memory_context_id,prompt,anchor_constraints,supplement) if supplement else projection
        packet = nos_packet.prepare_queue(prompt,c,providers.SYSTEM,operational_projection=projection)
        controls.enforce_packet(packet,c,providers.SYSTEM)
        quote=controls.quote(c)
        with self.db() as db: controls.check(db,c,quote)
        classification = classify(prompt)
        classification['estimated_input_tokens'] = classify(providers.SYSTEM + packet['prompt'])['estimated_input_tokens']
        classification['estimate_status'] = 'INCLUDES_SHARED_MEMORY_AND_WRAPPER_EXCLUDES_CLIENT_INTERNALS'
        decision = route(prompt, controls.restrict(self.connections(),c), self.counts(), classification=classification,max_prompt_chars=controls.prompt_limit(c))
        if decision['selected'] in ('mimo','kimi','deepseek') and packet['receipt'].get('memory_mode')!=canonical_memory.mode_for_provider(decision['selected'],c):
            packet=nos_packet.prepare_queue(prompt,c,providers.SYSTEM,decision['selected'],operational_projection=projection)
            controls.enforce_packet(packet,c,providers.SYSTEM)
            classification['estimated_input_tokens']=classify(providers.SYSTEM+packet['prompt'])['estimated_input_tokens']
            decision=route(prompt,controls.restrict(self.connections(),c),self.counts(),classification=classification,
                           excluded=[r['id'] for r in decision['candidates'] if r['id']!=decision['selected']],max_prompt_chars=controls.prompt_limit(c))
        decision['canonical_memory'] = packet['receipt']
        decision["execution_constraints"] = c
        decision["cost_reservation"] = quote
        decision["jev"] = {"status": "not_called_in_preview"}
        return decision

    def submit(self, prompt, request_id, *, routing_prompt=None, start_worker=True, execution_constraints=None, memory_context_id=None, scientific_binding_job_id=None):
        constraints=controls.normalize(execution_constraints)
        validate_prompt(prompt,controls.prompt_limit(constraints))
        supplement=None
        anchor_constraints=constraints
        if scientific_binding_job_id:
            with self.db() as db:
                job=db.execute('SELECT * FROM coordination_jobs WHERE id=?',(scientific_binding_job_id,)).fetchone()
                expected,supplement=binding.effective(db,job)
            if not supplement or expected!=constraints or memory_context_id!=job['memory_context_id'] or routing_prompt!=job['prompt']:raise ValueError('Submission binding differs')
            if request_id!=str(uuid.uuid5(uuid.NAMESPACE_URL,'iald-coordination:'+scientific_binding_job_id)):raise ValueError('Submission request differs')
            if job['stage']!='execution_dispatching' or prompt!=job['prepared_prompt']:raise ValueError('Bound task must match prepared dispatch intent')
            binding.ready(self,supplement)
            anchor_constraints=None
        constraints_json=controls.encode(anchor_constraints)
        routing_prompt = routing_prompt if routing_prompt is not None else prompt
        validate_prompt(routing_prompt,controls.prompt_limit(constraints))
        reference = memory_context_id or opmem.context_id(request_id)
        if not isinstance(request_id, str):
            raise ValueError("Identificador de tarefa inválido.")
        uuid.UUID(request_id)
        if not self.source_status()["ok"]:
            raise ValueError("Fontes do Supercondutor indisponíveis ou alteradas.")
        with self.db() as db:
            existing=db.execute('SELECT * FROM tasks WHERE request_id=?',(request_id,)).fetchone()
        if existing:
            if existing['prompt'] != prompt or (existing['routing_prompt'] or existing['prompt']) != routing_prompt or (existing['execution_constraints'] or 'null') != constraints_json:
                raise ValueError('Identificador já usado com outro pedido/restrições.')
            if existing['scientific_binding_job_id'] != scientific_binding_job_id:raise ValueError('Idempotent binding differs')
            if memory_context_id and existing['memory_context_id'] != reference:
                raise ValueError('Idempotent request has a different memory context')
            return self.task(existing['id'])
        retired=BASE/'state/session_requests'/f'{request_id}.json'
        if retired.is_file() and json.loads(retired.read_bytes()).get('status')=='superseded_before_submission':
            raise ValueError('Pedido retirado antes da submissão; execução proibida.')
        if constraints:
            preview=self.preview(routing_prompt,constraints,memory_context_id=memory_context_id,scientific_binding_job_id=scientific_binding_job_id) if supplement else self.preview(prompt,constraints)
            if not preview['selected']:
                raise ValueError('Executor obrigatório indisponível ou inelegível; sem substituição.')
        if memory_context_id:
            anchor=opmem.sync(self, reference)
            if anchor['objective'] != routing_prompt or anchor['constraints'] != (anchor_constraints or {}):
                raise ValueError('Execution memory must preserve the coordination inscription')
        stamp, task_id = now(), str(uuid.uuid4())
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            existing = db.execute("SELECT * FROM tasks WHERE request_id=?", (request_id,)).fetchone()
            if existing:
                if existing["prompt"] != prompt or (existing["routing_prompt"] or existing["prompt"]) != routing_prompt or (existing["execution_constraints"] or "null") != constraints_json:
                    raise ValueError("Identificador já usado por outra tarefa.")
                if existing["scientific_binding_job_id"] != scientific_binding_job_id:raise ValueError("Idempotent binding differs")
                if memory_context_id and existing["memory_context_id"] != reference:
                    raise ValueError("Idempotent request has a different memory context")
                return self.task(existing["id"])
            if supplement:
                bound_job=db.execute('SELECT * FROM coordination_jobs WHERE id=?',(scientific_binding_job_id,)).fetchone()
                actual,bound=binding.effective(db,bound_job)
                if actual!=constraints or bound!=supplement or bound_job['stage']!='execution_dispatching' or bound_job['prepared_prompt']!=prompt:
                    raise ValueError('Bound dispatch CAS changed')
            pending = db.execute("SELECT count(*) FROM tasks WHERE status IN ('queued','running')").fetchone()[0]
            if pending >= 5:
                raise ValueError("Fila cheia: aguarde uma das tarefas em andamento.")
            db.execute("INSERT INTO tasks(id,request_id,prompt,created_at,updated_at,status,routing_prompt,execution_constraints,memory_context_id,scientific_binding_job_id) VALUES(?,?,?,?,?,'queued',?,?,?,?)",
                       (task_id, request_id, prompt, stamp, stamp, routing_prompt, constraints_json, reference,scientific_binding_job_id))
            opmem.stage(db, reference, routing_prompt, anchor_constraints, "task:"+task_id+":0", phase="queued", handle_id=task_id, next_action="Executar uma vez; preservar resultado incerto.")
        opmem.sync(self, reference)
        if start_worker:self.start_worker()
        return self.task(task_id)

    def start_worker(self):
        threading.Thread(target=self._drain, daemon=True, name="iald-orchestrator").start()

    def task(self, task_id):
        uuid.UUID(task_id)
        with self.db() as db:
            row = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if row is None:
            raise ValueError("Tarefa não encontrada.")
        result = dict(row)
        with self.db() as db:
            result["memory_checkpoint_pending"]=bool(result["memory_context_id"] and db.execute("SELECT 1 FROM memory_outbox WHERE context_id=? AND receipt_json IS NULL LIMIT 1",(result["memory_context_id"],)).fetchone())
        for key in ("decision", "result", "execution_constraints"):
            result[key] = json.loads(result[key]) if result[key] else None
        with self.db() as db:
            c,supplement=binding.task_effective(db,row)
        result['original_execution_constraints']=result['execution_constraints']
        result['effective_execution_constraints']=c
        result['scientific_binding']=supplement
        return result

    def _update(self, task_id, **fields):
        if not set(fields) <= {"status", "decision", "result", "error"}:
            raise ValueError("Invalid state mutation")
        memory_result = fields.get("result")
        memory_phase = fields.get("status")
        fields["updated_at"] = now()
        for key in ("decision", "result"):
            if key in fields:
                fields[key] = json.dumps(fields[key], ensure_ascii=False, allow_nan=False)
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            row=db.execute("SELECT * FROM tasks WHERE id=?",(task_id,)).fetchone()
            if row is not None and row["memory_context_id"] and memory_phase:
                text=(memory_result or {}).get("text")
                fields["memory_version"]=row["memory_version"]+1
                opmem.stage(db,row["memory_context_id"],row["routing_prompt"] or row["prompt"],json.loads(row["execution_constraints"] or "null"),
                    "task:"+task_id+":"+str(fields["memory_version"]),phase=memory_phase,handle_id=task_id,
                    next_action="Conferir resultado e sintetizar." if memory_phase=="result_ready" else "Conferir estado; falha ou incerteza nunca autoriza reenvio.",
                    result=text,source={"id":task_id,"provider":json.loads(row["decision"] or "{}").get("selected"),"sha256":opmem.digest(text) if text else None})
            db.execute("UPDATE tasks SET " + ",".join(k + "=?" for k in fields) + " WHERE id=?", (*fields.values(), task_id))

        if row is not None and row['memory_context_id'] and memory_phase:
            self._flush_memory(task_id,row['memory_context_id'])

    def _flush_memory(self, task_id, reference):
        try:
            opmem.sync(self,reference)
        except Exception as exc:
            # State and provider result already committed. Never make them retryable.
            with self.db() as db:
                db.execute("UPDATE tasks SET error=COALESCE(error || ' | ', '') || ? WHERE id=?",
                    ('Checkpoint de memória pendente: '+type(exc).__name__,task_id))

    def cancel(self, task_id):
        task = self.task(task_id)
        if task["status"] not in ("queued", "running"):
            return task
        event = self.cancel_events.get(task_id)
        if event:
            event.set()
        proc = self.processes.get(task_id)
        if proc and proc.poll() is None:
            proc.kill()
        self._update(task_id, status="cancelled", error="Cancelada. Chamada local em curso pode terminar no servidor; nenhum novo trabalho será enviado.")
        return self.task(task_id)

    def _drain(self):
        # Keep the legacy process lock for the WHOLE drain: old workers and
        # recovery cannot overlap this owner. Only this owner fans out calls.
        from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
        parallel = {'kimi', 'mimo', 'deepseek'}
        with self.worker_lock, process_lock(self.db_path):
            with ThreadPoolExecutor(max_workers=3) as pool:
                active = {}
                while True:
                    for future in list(active):
                        if future.done():
                            # Unexpected worker failure remains running/uncertain;
                            # never reclaim or retry it automatically.
                            future.result()
                            del active[future]
                    occupied = set(active.values())
                    claimed = None
                    with self.db() as db:
                        db.execute("BEGIN IMMEDIATE")
                        # Any persisted running task not owned by our futures is
                        # uncertain. At entry no calls may be recovered by retry.
                        running_count = db.execute("SELECT count(*) FROM tasks WHERE status='running'").fetchone()[0]
                        if running_count > len(active):
                            break
                        if len(active) < 3 and '__exclusive__' not in occupied:
                            for row in db.execute("SELECT * FROM tasks WHERE status='queued' ORDER BY created_at,id"):
                                constraints = binding.task_effective(db,row)[0] or {}
                                provider = constraints.get('required_provider')
                                if provider == 'local' and providers.rite_markers():
                                    break  # Preserve order; no attempt, reservation or busy retry.
                                lane = provider if provider in parallel else '__exclusive__'
                                if lane == '__exclusive__':
                                    if active:
                                        break
                                elif lane in occupied:
                                    continue
                                changed = db.execute("UPDATE tasks SET status='running',updated_at=? WHERE id=? AND status='queued'", (now(), row['id'])).rowcount
                                if changed:
                                    revision=row['memory_version']+1
                                    db.execute('UPDATE tasks SET memory_version=? WHERE id=?',(revision,row['id']))
                                    if row['memory_context_id']:
                                        opmem.stage(db,row['memory_context_id'],row['routing_prompt'] or row['prompt'],json.loads(row['execution_constraints'] or 'null'),
                                            'task:'+row['id']+':'+str(revision),phase='running',handle_id=row['id'],next_action='Conferir pacote e restrições antes do envio único.')
                                    claimed = (dict(row), lane)
                                break
                    if claimed:
                        row, lane = claimed
                        future = pool.submit(self._perform, row['id'], row['prompt'], row['routing_prompt'] or row['prompt'])
                        active[future] = lane
                        continue
                    if not active:
                        return
                    wait(active, timeout=0.2, return_when=FIRST_COMPLETED)

    def _memory_phase(self, task_id, phase):
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            row=db.execute("SELECT * FROM tasks WHERE id=?",(task_id,)).fetchone()
            if not row["memory_context_id"]:
                raise ValueError("Missing operational context")
            revision=row["memory_version"]+1
            db.execute("UPDATE tasks SET memory_version=? WHERE id=?",(revision,task_id))
            opmem.stage(db,row["memory_context_id"],row["routing_prompt"] or row["prompt"],json.loads(row["execution_constraints"] or "null"),
                "task:"+task_id+":"+str(revision),phase=phase,handle_id=task_id,next_action="Aguardar retorno sem repetir o envio." if phase=="dispatch_intent" else "Despachar uma única vez após conferir as restrições.")
        return opmem.sync(self,row["memory_context_id"])

    def _perform(self, task_id, prompt, routing_prompt=None):
        cancel = self.cancel_events[task_id] = threading.Event()
        attempt_id = None
        try:
            if self.task(task_id)["status"] not in ("queued","running"):
                return
            if not self.source_status()["ok"]:
                raise RuntimeError("Âncora do Supercondutor não confere.")
            c=controls.normalize(self.task(task_id)['effective_execution_constraints'])
            if c and c['required_provider'] == 'local':
                providers.require_local_available()
            # Jev is in an audited scientific observation phase. A free-form
            # request has no trustworthy scientific scope marker, so sending it
            # to TypeSafe here could disclose legal or other unrelated content.
            classification = classify(routing_prompt or prompt)
            jev_status = {'status': ('not_called_for_controlled_request' if c else
                                     'not_called_without_scientific_scope')}
            task=self.task(task_id)
            if not task['memory_context_id']:
                raise ValueError('Legacy task has no operational inscription; explicit migration required')
            self._memory_phase(task_id, 'prepared')
            self._memory_phase(task_id, "dispatch_intent")
            binding.ready(self,task['scientific_binding'])
            projection=binding.project(self,task['memory_context_id'],routing_prompt or prompt,task['original_execution_constraints'],task['scientific_binding'])
            packet = nos_packet.prepare_queue(prompt,c,providers.SYSTEM,operational_projection=projection)
            controls.enforce_packet(packet,c,providers.SYSTEM)
            quote=controls.quote(c)
            classification["estimated_input_tokens"] = classify(providers.SYSTEM + packet['prompt'])["estimated_input_tokens"]
            classification['estimate_status'] = 'INCLUDES_SHARED_MEMORY_AND_WRAPPER_EXCLUDES_CLIENT_INTERNALS'
            decision = route(prompt, controls.restrict(self.connections(),c), self.counts(), classification=classification,max_prompt_chars=controls.prompt_limit(c))
            if decision['selected'] in ('mimo','kimi','deepseek') and packet['receipt'].get('memory_mode')!=canonical_memory.mode_for_provider(decision['selected'],c):
                packet=nos_packet.prepare_queue(prompt,c,providers.SYSTEM,decision['selected'],operational_projection=projection)
                controls.enforce_packet(packet,c,providers.SYSTEM)
                classification['estimated_input_tokens']=classify(providers.SYSTEM+packet['prompt'])['estimated_input_tokens']
                decision=route(prompt,controls.restrict(self.connections(),c),self.counts(),classification=classification,
                               excluded=[r['id'] for r in decision['candidates'] if r['id']!=decision['selected']],max_prompt_chars=controls.prompt_limit(c))
            decision["execution_constraints"]=c
            decision["cost_reservation"]=quote
            decision["canonical_memory"] = packet["receipt"]
            decision["jev"] = jev_status
            self._update(task_id, decision=decision)
            if not decision["selected"]:
                raise RuntimeError("Nenhum provedor elegível. Consulte a matriz de seleção e os logins.")
            if cancel.is_set() or self.task(task_id)["status"] == "cancelled":
                return
            if decision["selected"] == "local":
                providers.require_local_available()
            workspace = self.state_dir / "work" / task_id
            workspace.mkdir(parents=True, exist_ok=True)
            with self.db() as db:
                db.execute("BEGIN IMMEDIATE")
                controls.reserve(db,task_id,c,quote,now())
                cursor = db.execute("INSERT INTO attempts(task_id,provider,started_at,status) VALUES(?,?,?,'running')",
                                    (task_id, decision["selected"], now()))
                attempt_id = cursor.lastrowid
            # Observation cannot choose an executor or change admission/constraints.
            try:
                decision["jev_body_shadow"]=jev_body_shadow.observe(task_id,prompt,c,decision["selected"],operational_projection=projection)
            except Exception as exc:
                decision["jev_body_shadow"]={"status":"local_observation_failure","error_type":type(exc).__name__,"effects":"NONE"}
            self._update(task_id, decision=decision)
            result = providers.execute(decision["selected"], prompt, workspace, cancel=cancel, memory_packet=packet, execution_constraints=c,
                         process_callback=lambda p: self.processes.__setitem__(task_id, p))
            # The provider return is durable before any optional follow-up call.
            with self.db() as db:
                controls.settle(db,task_id,c,result)
                db.execute("UPDATE attempts SET finished_at=?,status='returned',usage=? WHERE id=?",
                           (now(), json.dumps(result.get("usage")), attempt_id))
            if not cancel.is_set() and self.task(task_id)["status"] != "cancelled":
                self._update(task_id, status="result_ready", result=result)
                try:
                    returned_projection=binding.project(self,task['memory_context_id'],routing_prompt or prompt,task['original_execution_constraints'],task['scientific_binding'])
                    result["jev_body_shadow"]=jev_body_shadow.observe(task_id,prompt,c,decision["selected"],result=result,operational_projection=returned_projection)
                except Exception as exc:
                    result["jev_body_shadow"]={"status":"local_observation_failure","error_type":type(exc).__name__,"effects":"NONE"}
                self._update(task_id,result=result)
        except providers.ProviderPausedByRite as exc:
            if attempt_id:
                with self.db() as db:
                    db.execute("UPDATE attempts SET finished_at=?,status='paused_before_send' WHERE id=?", (now(), attempt_id))
            if self.task(task_id)["status"] != "cancelled":
                self._update(task_id, status="paused_by_rite", error=str(exc))
            # A reserved race is kept visible, never retried or charged twice automatically.
        except Exception as exc:
            if isinstance(exc, providers.ProviderLimitError):
                self.block_provider(decision["selected"], str(exc))
            if attempt_id:
                with self.db() as db:
                    db.execute("UPDATE attempts SET finished_at=?,status='failed_or_interrupted' WHERE id=?", (now(), attempt_id))
            if self.task(task_id)["status"] != "cancelled":
                message = str(exc) if isinstance(exc, (ValueError, RuntimeError)) else type(exc).__name__
                self._update(task_id, status="failed", error=message[:600])
        finally:
            self.cancel_events.pop(task_id, None)
            self.processes.pop(task_id, None)
