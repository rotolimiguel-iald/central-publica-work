"""Production activation entry point, only after a separate pinned review.

No provider, science, account, credential, trust or third-party MCP restart.
The app's existing supervisor resumes in finally; the existing queue lock and
SQLite write transaction stop queue admissions during the file replacement.
"""
import argparse
from contextlib import contextmanager
import json
from pathlib import Path
import socket
import sqlite3
import psutil
import maintenance
import legacy_app_checks
from queue_lock import process_lock
from transaction import DeploymentError, install, no_alias, prepare, read_json, receipt, sha

WORK = Path(__file__).resolve().parents[1]
CORE = Path(r'C:\IALD\MEMORIA_IALD')
APP = Path(r'C:\IALD\projetos_pyhton\IALD')
QUEUE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')


def allowed_targets(plan):
    app_names = {
        'iald_app_memory.py', 'iald_auto_router.py', 'iald_app_providers.py',
        'iald_web_server.py', 'iald_task_bridge.py', 'iald_task_session.py',
        'iald_chat_jobs.py', 'iald_activity_ui.py', 'iald_native_memory.py',
        'iald_native_activity.py',
        'iald_activity_operations.py', 'iald_jev_control.py', 'app/iald.js',
        'iald-app/www/iald.js', 'iald-app/android/app/src/main/assets/public/iald.js',
        'iald-app/ios/App/App/public/iald.js',
    }
    core_names = {'lib/iald_memory/activity.py', 'lib/iald_memory/store.py',
                  'lib/iald_memory/mission.py'}
    queue_names = {
        'iald_orchestrator/runtime.py', 'iald_orchestrator/coordination.py',
        'iald_orchestrator/operational_memory.py', 'iald_orchestrator/queue_activity.py',
        'iald_orchestrator/activity_bridge.py', 'iald_orchestrator/bench_activity.py',
        'transport_cli.py', 'mcp_server.py', 'queue_activity_session.py', 'bench_activity_cli.py',
        'queue_activity_migrate.py', 'iald_orchestrator/legacy_activity_migration.py',
    }
    allowed = {APP/p for p in app_names} | {CORE/p for p in core_names} | {QUEUE/p for p in queue_names}
    result = [no_alias(item['destination']) for item in plan['files']]
    if not set(result).issubset({p.resolve() for p in allowed}):
        raise DeploymentError('Destination outside organism code allowlist')
    mobile = {APP/p for p in ('iald-app/www/iald.js',
        'iald-app/android/app/src/main/assets/public/iald.js', 'iald-app/ios/App/App/public/iald.js')}
    for item, target in zip(plan['files'], result):
        if 'backup_directory' in item and target not in {p.resolve() for p in mobile}:
            raise DeploymentError('External backups are only for bundled mobile assets')
    return result


@contextmanager
def paused_queue():
    db_path = QUEUE/'state/tasks.sqlite3'
    # The established lock is shared with every existing _drain implementation.
    with process_lock(db_path, blocking=False) as acquired:
        if not acquired:
            raise DeploymentError('Queue execution active; no activation')
        db = sqlite3.connect(db_path.as_uri()+'?mode=rw', uri=True, timeout=1)
        try:
            db.execute('BEGIN IMMEDIATE')
            if db.execute("SELECT COUNT(*) FROM tasks WHERE status='running'").fetchone()[0]:
                raise DeploymentError('Queue has an unresolved running execution')
            yield db
        finally:
            db.rollback()
            db.close()


def assert_frozen(identity, db):
    parent = psutil.Process(identity['supervisor_pid'])
    if (parent.create_time() != identity['supervisor_created'] or
        parent.status() != psutil.STATUS_STOPPED or not db.in_transaction):
        raise DeploymentError('Maintenance ownership lost')
    if psutil.pid_exists(identity['old_web_pid']):
        raise DeploymentError('Old web process exists')
    with socket.socket() as probe:
        probe.settimeout(0.25)
        if probe.connect_ex(('127.0.0.1', 8082)) == 0:
            raise DeploymentError('Web admissions reopened')


def activate(plan_path, review_path, run_name):
    if not run_name.isascii() or not run_name.replace('_','').isalnum():
        raise DeploymentError('Invalid immutable run name')
    plan = read_json(plan_path)
    review = read_json(review_path)
    # The review must also cover the production maintenance entry point and
    # reused primitives, not only the portable transaction function.
    for file in ('controlled.py', 'maintenance.py', 'legacy_app_checks.py', 'queue_lock.py'):
        if review.get('deployment_files', {}).get(file) != sha(Path(__file__).with_name(file).read_bytes()):
            raise DeploymentError('Maintenance source not covered by review')
    targets = allowed_targets(plan)
    # Refuse stale inputs before a maintenance interruption, then revalidate
    # under maintenance in install(). No early check replaces the second one.
    prepare(plan_path, review_path, work_root=WORK, allowed_destinations=targets)
    evidence = WORK/'deployment_r2'/'runs'/run_name
    if evidence.exists():
        raise DeploymentError('Existing activation: inspect receipt before another attempt')
    with paused_queue() as db:
        with maintenance.stopped_web(legacy_app_checks.quiet) as identity:
            result = install(plan_path, review_path, work_root=WORK,
                allowed_destinations=targets,
                assert_quiesced=lambda: assert_frozen(identity, db), evidence_dir=evidence)
            maintenance.assert_quiesced()
    restart = maintenance.await_restart(identity, timeout=60)
    receipt(evidence/'RESTART.json', restart)
    return {'installation': result, 'restart': restart, 'evidence_directory': str(evidence),
            'legacy_mcp_processes_reloaded': False, 'science_engine_restarted': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--plan', required=True)
    parser.add_argument('--review', required=True)
    parser.add_argument('--run-name', required=True)
    args = parser.parse_args()
    print(json.dumps(activate(args.plan, args.review, args.run_name), ensure_ascii=False))
